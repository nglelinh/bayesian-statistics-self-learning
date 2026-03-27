"""Generate Chapter 07 applied ML workflow figure.

This script builds a synthetic sparse-regression problem, tunes ridge
regularization using validation RMSE, then estimates feature-selection
stability via bootstrap frequency.
"""

import numpy as np
import matplotlib.pyplot as plt


def ridge_fit(x_mat, y_vec, lam):
    p = x_mat.shape[1]
    eye = np.eye(p)
    return np.linalg.solve(x_mat.T @ x_mat + lam * eye, x_mat.T @ y_vec)


def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def bootstrap_stability(x_mat, y_vec, lam, n_boot=200, threshold=0.15, seed=42):
    rng = np.random.default_rng(seed)
    n, p = x_mat.shape
    picks = np.zeros((n_boot, p), dtype=int)

    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        x_boot = x_mat[idx]
        y_boot = y_vec[idx]
        beta_hat = ridge_fit(x_boot, y_boot, lam)
        picks[b] = (np.abs(beta_hat) > threshold).astype(int)

    return picks.mean(axis=0)


def main():
    rng = np.random.default_rng(42)
    n, p = 180, 25

    beta_true = np.zeros(p)
    beta_true[:6] = np.array([2.4, -1.8, 1.2, 0.9, -0.7, 0.5])

    x_mat = rng.normal(0, 1, size=(n, p))
    y_vec = 1.5 + x_mat @ beta_true + rng.normal(0, 1.2, size=n)

    idx = rng.permutation(n)
    train_idx = idx[: int(0.6 * n)]
    val_idx = idx[int(0.6 * n): int(0.8 * n)]
    test_idx = idx[int(0.8 * n):]

    x_train = x_mat[train_idx]
    y_train = y_vec[train_idx]
    x_val = x_mat[val_idx]
    y_val = y_vec[val_idx]
    x_test = x_mat[test_idx]
    y_test = y_vec[test_idx]

    mu_x = x_train.mean(axis=0)
    sd_x = x_train.std(axis=0)
    sd_x[sd_x == 0] = 1.0

    x_train_z = (x_train - mu_x) / sd_x
    x_val_z = (x_val - mu_x) / sd_x
    x_test_z = (x_test - mu_x) / sd_x

    mu_y = y_train.mean()
    sd_y = y_train.std() if y_train.std() > 0 else 1.0

    y_train_z = (y_train - mu_y) / sd_y
    y_val_z = (y_val - mu_y) / sd_y
    y_test_z = (y_test - mu_y) / sd_y

    lambdas = np.logspace(-3, 2, 30)
    train_scores = []
    val_scores = []
    coefs = []

    for lam in lambdas:
        beta_hat = ridge_fit(x_train_z, y_train_z, lam)
        coefs.append(beta_hat)
        train_scores.append(rmse(y_train_z, x_train_z @ beta_hat))
        val_scores.append(rmse(y_val_z, x_val_z @ beta_hat))

    best_idx = int(np.argmin(val_scores))
    best_lambda = float(lambdas[best_idx])
    best_beta = coefs[best_idx]
    test_score = rmse(y_test_z, x_test_z @ best_beta)

    stability = bootstrap_stability(x_train_z, y_train_z, best_lambda)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    axes[0].plot(lambdas, train_scores, marker="o", label="Train RMSE")
    axes[0].plot(lambdas, val_scores, marker="o", label="Validation RMSE")
    axes[0].axvline(best_lambda, color="red", linestyle="--", linewidth=2)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("lambda (log scale)")
    axes[0].set_ylabel("RMSE (z-scale)")
    axes[0].set_title("Validation tuning")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].bar(np.arange(p), best_beta, color="seagreen", edgecolor="black", alpha=0.8)
    axes[1].axhline(0, color="black", linestyle="--", linewidth=1.5)
    axes[1].set_xlabel("Feature index")
    axes[1].set_ylabel("Coefficient")
    axes[1].set_title("Best-model coefficients")
    axes[1].grid(alpha=0.3, axis="y")

    axes[2].bar(np.arange(p), stability, color="steelblue", edgecolor="black", alpha=0.8)
    axes[2].axhline(0.7, color="red", linestyle="--", linewidth=2, label="Stable threshold = 0.7")
    axes[2].set_ylim(0, 1)
    axes[2].set_xlabel("Feature index")
    axes[2].set_ylabel("Selection frequency")
    axes[2].set_title("Bootstrap stability")
    axes[2].legend()
    axes[2].grid(alpha=0.3, axis="y")

    fig.suptitle(
        (
            "Applied ML workflow: split + tune + stability | "
            f"best lambda={best_lambda:.4f}, test RMSE={test_score:.3f}"
        ),
        fontsize=13,
        fontweight="bold",
    )
    fig.tight_layout()
    fig.savefig(
        "img/chapter_img/chapter07/applied_ml_workflow_tradeoffs.png",
        dpi=160,
        bbox_inches="tight",
    )

    print(f"best_lambda={best_lambda:.6f}")
    print(f"test_rmse_z={test_score:.6f}")
    print("Saved: img/chapter_img/chapter07/applied_ml_workflow_tradeoffs.png")


if __name__ == "__main__":
    main()
