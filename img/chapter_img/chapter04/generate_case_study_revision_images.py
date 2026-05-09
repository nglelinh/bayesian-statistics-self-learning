#!/usr/bin/env python3
"""
Generate intervention illustrations for Chapter 4.6.

Outputs:
- chapter04_46_intervention_log_transform.png
- chapter04_46_intervention_nonlinear.png
- chapter04_46_intervention_group_effects.png
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def savefig(name: str) -> None:
    path = os.path.join(OUTPUT_DIR, name)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    print(f"Created: {name}")
    plt.close()


def split_data(df: pd.DataFrame, seed: int = 42):
    rng = np.random.default_rng(seed)
    idx = np.arange(len(df))
    rng.shuffle(idx)
    n_train = int(0.8 * len(df))
    tr = idx[:n_train]
    te = idx[n_train:]
    return df.iloc[tr].copy(), df.iloc[te].copy()


def design_add_cut(df: pd.DataFrame, cut_levels: list[str]) -> np.ndarray:
    cols = [np.ones(len(df)), df["carat"].to_numpy(float)]
    cut_arr = df["cut"].astype(str).to_numpy()
    for c in cut_levels[1:]:
        cols.append((cut_arr == c).astype(float))
    return np.column_stack(cols)


def generate_log_transform_figure(df: pd.DataFrame) -> None:
    train_df, test_df = split_data(df, seed=42)

    x_tr = train_df["carat"].to_numpy(float)
    y_tr = train_df["price"].to_numpy(float)
    x_te = test_df["carat"].to_numpy(float)
    y_te = test_df["price"].to_numpy(float)

    # Raw linear on original scale
    xmat_tr = np.column_stack([np.ones_like(x_tr), x_tr])
    beta_raw = np.linalg.lstsq(xmat_tr, y_tr, rcond=None)[0]
    yhat_tr = xmat_tr @ beta_raw
    resid_raw = y_tr - yhat_tr

    xmat_te = np.column_stack([np.ones_like(x_te), x_te])
    yhat_te = xmat_te @ beta_raw
    sigma_raw = np.std(resid_raw, ddof=2)
    z90 = 1.6448536269514722
    lo_raw = yhat_te - z90 * sigma_raw
    hi_raw = yhat_te + z90 * sigma_raw
    mask_hi = x_te >= np.quantile(x_te, 0.75)
    cov_hi_raw = np.mean((y_te[mask_hi] >= lo_raw[mask_hi]) & (y_te[mask_hi] <= hi_raw[mask_hi]))

    # Log-linear
    ly_tr = np.log(y_tr)
    beta_log = np.linalg.lstsq(xmat_tr, ly_tr, rcond=None)[0]
    lyhat_tr = xmat_tr @ beta_log
    resid_log = ly_tr - lyhat_tr

    lyhat_te = xmat_te @ beta_log
    sigma_log = np.std(resid_log, ddof=2)
    lo_log = np.exp(lyhat_te - z90 * sigma_log)
    hi_log = np.exp(lyhat_te + z90 * sigma_log)
    cov_hi_log = np.mean((y_te[mask_hi] >= lo_log[mask_hi]) & (y_te[mask_hi] <= hi_log[mask_hi]))

    corr_raw = np.corrcoef(np.abs(df["price"] - (np.column_stack([np.ones(len(df)), df["carat"]]) @ beta_raw)), df["carat"])[0, 1]
    corr_log = np.corrcoef(np.abs(np.log(df["price"]) - (np.column_stack([np.ones(len(df)), df["carat"]]) @ beta_log)), df["carat"])[0, 1]

    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

    # Subsample for visual clarity
    sample = train_df.sample(n=6000, random_state=42)
    sx = sample["carat"].to_numpy(float)
    sy = sample["price"].to_numpy(float)
    syhat_raw = beta_raw[0] + beta_raw[1] * sx
    syhat_log = beta_log[0] + beta_log[1] * sx

    axes[0].scatter(syhat_raw, sy - syhat_raw, s=5, alpha=0.18, color="#1f77b4")
    axes[0].axhline(0, color="black", linestyle="--", linewidth=1.5)
    axes[0].set_title("Can thiệp 1: Trước can thiệp (thang giá gốc)")
    axes[0].set_xlabel("Fitted price")
    axes[0].set_ylabel("Residual")
    axes[0].text(
        0.03,
        0.95,
        f"corr(|e|, carat) = {corr_raw:.3f}\nCoverage90 (carat cao) = {cov_hi_raw:.3f}",
        transform=axes[0].transAxes,
        va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )

    axes[1].scatter(syhat_log, np.log(sy) - syhat_log, s=5, alpha=0.18, color="#2ca02c")
    axes[1].axhline(0, color="black", linestyle="--", linewidth=1.5)
    axes[1].set_title("Can thiệp 1: Sau log-transform")
    axes[1].set_xlabel("Fitted log(price)")
    axes[1].set_ylabel("Residual (log-scale)")
    axes[1].text(
        0.03,
        0.95,
        f"corr(|e_log|, carat) = {corr_log:.3f}\nCoverage90 (carat cao) = {cov_hi_log:.3f}",
        transform=axes[1].transAxes,
        va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )

    fig.suptitle("Intervention 1: Log-transform giam heteroskedasticity va cai thien coverage vung carat cao", y=1.02, fontsize=13)
    plt.tight_layout()
    savefig("chapter04_46_intervention_log_transform.png")


def generate_nonlinear_figure(df: pd.DataFrame) -> None:
    train_df, test_df = split_data(df, seed=42)
    x_tr = train_df["carat"].to_numpy(float)
    y_tr = np.log(train_df["price"].to_numpy(float))
    x_te = test_df["carat"].to_numpy(float)
    y_te = np.log(test_df["price"].to_numpy(float))

    x1_tr = np.column_stack([np.ones_like(x_tr), x_tr])
    b1 = np.linalg.lstsq(x1_tr, y_tr, rcond=None)[0]
    x1_te = np.column_stack([np.ones_like(x_te), x_te])
    rmse_lin = np.sqrt(np.mean((y_te - (x1_te @ b1)) ** 2))

    x2_tr = np.column_stack([np.ones_like(x_tr), x_tr, x_tr**2])
    b2 = np.linalg.lstsq(x2_tr, y_tr, rcond=None)[0]
    x2_te = np.column_stack([np.ones_like(x_te), x_te, x_te**2])
    rmse_quad = np.sqrt(np.mean((y_te - (x2_te @ b2)) ** 2))

    grid = np.linspace(df["carat"].min(), df["carat"].quantile(0.99), 250)
    y_lin = b1[0] + b1[1] * grid
    y_quad = b2[0] + b2[1] * grid + b2[2] * grid**2

    # Binned means as empirical trend
    bins = np.quantile(df["carat"], np.linspace(0, 1, 15))
    bins = np.unique(bins)
    tmp = df[["carat", "price"]].copy()
    tmp["bin"] = pd.cut(tmp["carat"], bins=bins, include_lowest=True)
    binned = tmp.groupby("bin", observed=False).agg(carat_mean=("carat", "mean"), logprice_mean=("price", lambda s: np.log(s).mean())).dropna()

    sns.set_style("whitegrid")
    plt.figure(figsize=(8.8, 5.6))
    sample = df.sample(n=7000, random_state=42)
    plt.scatter(sample["carat"], np.log(sample["price"]), s=5, alpha=0.12, color="#7f7f7f", label="Du lieu mau (log-price)")
    plt.plot(grid, y_lin, color="#1f77b4", linewidth=2.4, label=f"Tuyen tinh (RMSE test={rmse_lin:.3f})")
    plt.plot(grid, y_quad, color="#d62728", linewidth=2.4, label=f"Phi tuyen bac 2 (RMSE test={rmse_quad:.3f})")
    plt.scatter(binned["carat_mean"], binned["logprice_mean"], color="black", s=30, label="Trung binh theo bin carat")
    plt.xlabel("carat")
    plt.ylabel("log(price)")
    plt.title("Intervention 2: Mo rong ham trung binh tu tuyen tinh sang phi tuyen")
    plt.legend(frameon=True)
    plt.tight_layout()
    savefig("chapter04_46_intervention_nonlinear.png")


def generate_group_figure(df: pd.DataFrame) -> None:
    train_df, test_df = split_data(df, seed=42)

    x_tr = train_df["carat"].to_numpy(float)
    y_tr = train_df["price"].to_numpy(float)
    x_te = test_df["carat"].to_numpy(float)
    y_te = test_df["price"].to_numpy(float)

    # Baseline price ~ carat
    xmat_tr = np.column_stack([np.ones_like(x_tr), x_tr])
    b_base = np.linalg.lstsq(xmat_tr, y_tr, rcond=None)[0]
    pred_base = np.column_stack([np.ones_like(x_te), x_te]) @ b_base

    # Add cut effects (illustration of group structure)
    cut_levels = sorted(df["cut"].astype(str).unique())
    xg_tr = design_add_cut(train_df, cut_levels)
    xg_te = design_add_cut(test_df, cut_levels)
    b_group = np.linalg.lstsq(xg_tr, y_tr, rcond=None)[0]
    pred_group = xg_te @ b_group

    obs_mean = test_df.groupby("cut", observed=False)["price"].mean()
    base_mean = pd.Series(pred_base, index=test_df.index).groupby(test_df["cut"]).mean()[obs_mean.index]
    group_mean = pd.Series(pred_group, index=test_df.index).groupby(test_df["cut"]).mean()[obs_mean.index]

    gmae_base = np.mean(np.abs(base_mean - obs_mean))
    gmae_group = np.mean(np.abs(group_mean - obs_mean))

    labels = obs_mean.index.astype(str).tolist()
    x_pos = np.arange(len(labels))
    width = 0.26

    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 5.6))
    plt.bar(x_pos - width, obs_mean.values, width=width, color="#4c78a8", label="Quan sat (test)")
    plt.bar(x_pos, base_mean.values, width=width, color="#f58518", label="Khong co group effect")
    plt.bar(x_pos + width, group_mean.values, width=width, color="#54a24b", label="Them group effect (cut)")

    plt.xticks(x_pos, labels)
    plt.ylabel("Mean price by cut")
    plt.title("Intervention 3: Dua cau truc nhom vao mo hinh de cai thien calibration theo cut")
    plt.legend()
    plt.text(
        0.01,
        0.98,
        f"Group MAE (khong group) = {gmae_base:.1f}\nGroup MAE (them group) = {gmae_group:.1f}",
        transform=plt.gca().transAxes,
        va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )

    plt.tight_layout()
    savefig("chapter04_46_intervention_group_effects.png")


def main() -> None:
    sns.set_context("notebook")
    df = sns.load_dataset("diamonds").dropna(subset=["carat", "price", "cut"]).copy()
    generate_log_transform_figure(df)
    generate_nonlinear_figure(df)
    generate_group_figure(df)
    print("Done.")


if __name__ == "__main__":
    main()
