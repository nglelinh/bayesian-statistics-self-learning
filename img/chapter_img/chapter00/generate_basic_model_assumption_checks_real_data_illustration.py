"""Generate separate real-data charts for assumption checks lesson."""

from pathlib import Path
from math import exp

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression


OUT_DIR = Path(__file__).resolve().parent
DIAMONDS_DIST_PATH = OUT_DIR / "basic_model_assumption_diamonds_distribution.png"
DIAMONDS_RESID_PATH = OUT_DIR / "basic_model_assumption_diamonds_residuals.png"
TAXIS_DIST_PATH = OUT_DIR / "basic_model_assumption_taxis_distribution.png"
TAXIS_PROB_PATH = OUT_DIR / "basic_model_assumption_taxis_probabilities.png"


def poisson_tail_prob_ge(threshold: int, lam: float) -> float:
    term = exp(-lam)
    cdf = term
    for k in range(1, threshold):
        term *= lam / k
        cdf += term
    return 1.0 - cdf


def negbin_moment_tail_prob_ge(threshold: int, mu: float, var: float) -> float:
    k = mu**2 / (var - mu)
    p = (k / (k + mu)) ** k
    cdf = p
    for y in range(1, threshold):
        p *= ((y - 1 + k) / y) * (mu / (k + mu))
        cdf += p
    return 1.0 - cdf


def load_diamonds_summary():
    diamonds = sns.load_dataset("diamonds").dropna()
    x = diamonds[["carat"]].to_numpy()
    y = diamonds["price"].to_numpy()

    model = LinearRegression().fit(x, y)
    fitted = model.predict(x)
    resid = y - fitted
    q95 = float(np.quantile(y, 0.95))
    skew = float(diamonds["price"].skew())
    corr = float(np.corrcoef(np.abs(resid), fitted)[0, 1])
    sample_idx = np.random.default_rng(42).choice(len(y), size=8000, replace=False)
    return y, fitted, resid, q95, skew, corr, sample_idx


def load_taxis_summary():
    taxis = sns.load_dataset("taxis").dropna(subset=["pickup_zone", "pickup"])
    taxis["day"] = pd.to_datetime(taxis["pickup"]).dt.floor("D")
    manhattan = taxis[taxis["pickup_borough"] == "Manhattan"].copy()

    zones = sorted(set(pd.Series(manhattan["pickup_zone"]).dropna().astype(str).tolist()))
    days = pd.date_range(manhattan["day"].min(), manhattan["day"].max(), freq="D")
    full = pd.MultiIndex.from_product([zones, days], names=["pickup_zone", "day"]).to_frame(index=False)
    observed = manhattan.groupby(["pickup_zone", "day"]).size().reset_index()
    observed.columns = ["pickup_zone", "day", "trips"]
    daily_counts = full.merge(observed, on=["pickup_zone", "day"], how="left").fillna({"trips": 0})
    daily_counts["trips"] = daily_counts["trips"].astype(int)

    trips = daily_counts["trips"].to_numpy()
    mu = float(np.mean(trips))
    var = float(np.var(trips, ddof=1))
    p0_obs = float(np.mean(trips == 0))
    p10_obs = float(np.mean(trips >= 10))
    p0_pois = float(exp(-mu))
    p10_pois = float(poisson_tail_prob_ge(10, mu))
    k = mu**2 / (var - mu)
    p0_nb = float((k / (k + mu)) ** k)
    p10_nb = float(negbin_moment_tail_prob_ge(10, mu, var))
    return trips, mu, var, p0_obs, p10_obs, p0_pois, p10_pois, p0_nb, p10_nb


def plot_diamonds_distribution(y, q95, skew):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(y, bins=45, color="#4472c4", edgecolor="white", alpha=0.88, ax=ax)
    ax.axvline(q95, color="#c0392b", linestyle="--", linewidth=2.0)
    ax.set_title("Diamonds: price distribution", fontsize=16, fontweight="bold")
    ax.set_xlabel("Price (USD)", fontsize=13)
    ax.set_ylabel("Count", fontsize=13)
    ax.tick_params(labelsize=11)
    ax.text(
        0.97,
        0.92,
        f"q95 = {q95:.0f}\nskew = {skew:.2f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=12,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.92, "edgecolor": "#999"},
    )
    fig.tight_layout()
    fig.savefig(DIAMONDS_DIST_PATH, dpi=180)
    plt.close(fig)


def plot_diamonds_residuals(fitted, resid, corr, sample_idx):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(fitted[sample_idx], resid[sample_idx], s=8, alpha=0.35, color="#2a9d8f", edgecolors="none")
    ax.axhline(0, color="#555", linewidth=1.2)
    ax.set_title("Diamonds baseline: residual vs fitted", fontsize=16, fontweight="bold")
    ax.set_xlabel("Fitted value", fontsize=13)
    ax.set_ylabel("Residual", fontsize=13)
    ax.tick_params(labelsize=11)
    ax.text(
        0.97,
        0.92,
        f"corr(|e|, yhat) = {corr:.3f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=12,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.92, "edgecolor": "#999"},
    )
    fig.tight_layout()
    fig.savefig(DIAMONDS_RESID_PATH, dpi=180)
    plt.close(fig)


def plot_taxis_distribution(trips, mu, var):
    fig, ax = plt.subplots(figsize=(10, 6))
    bins = (np.arange(0, 16) - 0.5).tolist()
    ax.hist(trips, bins=bins, density=True, color="#8e44ad", alpha=0.82, edgecolor="white")
    ax.set_title("Taxis: trips per zone-day", fontsize=16, fontweight="bold")
    ax.set_xlabel("Trips", fontsize=13)
    ax.set_ylabel("Proportion", fontsize=13)
    ax.set_xlim(-0.5, 14.5)
    ax.tick_params(labelsize=11)
    ax.text(
        0.97,
        0.92,
        f"mean = {mu:.3f}\nvar = {var:.3f}\nvar/mean = {var / mu:.2f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=12,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.92, "edgecolor": "#999"},
    )
    fig.tight_layout()
    fig.savefig(TAXIS_DIST_PATH, dpi=180)
    plt.close(fig)


def plot_taxis_probabilities(p0_obs, p10_obs, p0_pois, p10_pois, p0_nb, p10_nb):
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = ["P(Y=0)", "P(Y>=10)"]
    xloc = np.arange(len(labels))
    width = 0.25
    ax.bar(xloc - width, [p0_obs, p10_obs], width, label="Observed", color="#2c3e50")
    ax.bar(xloc, [p0_pois, p10_pois], width, label="Poisson", color="#e67e22")
    ax.bar(xloc + width, [p0_nb, p10_nb], width, label="NegBin (moment)", color="#16a085")
    ax.set_xticks(xloc)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(p0_obs, p0_nb) * 1.25)
    ax.set_title("Taxis: observed vs model-implied probabilities", fontsize=16, fontweight="bold")
    ax.set_ylabel("Probability", fontsize=13)
    ax.tick_params(labelsize=11)
    ax.legend(frameon=False, fontsize=11)
    fig.tight_layout()
    fig.savefig(TAXIS_PROB_PATH, dpi=180)
    plt.close(fig)


def main():
    sns.set_theme(style="whitegrid")

    y, fitted, resid, q95, skew, corr, sample_idx = load_diamonds_summary()
    plot_diamonds_distribution(y, q95, skew)
    plot_diamonds_residuals(fitted, resid, corr, sample_idx)

    taxis_summary = load_taxis_summary()
    plot_taxis_distribution(taxis_summary[0], taxis_summary[1], taxis_summary[2])
    plot_taxis_probabilities(
        taxis_summary[3],
        taxis_summary[4],
        taxis_summary[5],
        taxis_summary[6],
        taxis_summary[7],
        taxis_summary[8],
    )

    print(f"Saved: {DIAMONDS_DIST_PATH}")
    print(f"Saved: {DIAMONDS_RESID_PATH}")
    print(f"Saved: {TAXIS_DIST_PATH}")
    print(f"Saved: {TAXIS_PROB_PATH}")


if __name__ == "__main__":
    main()
