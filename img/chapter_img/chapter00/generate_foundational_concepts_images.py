import numpy as np
import matplotlib.pyplot as plt


def save_expectation_variance_covariance(output_dir: str) -> None:
    rng = np.random.default_rng(42)
    x = rng.normal(0, 1, 500)
    y_pos = 0.8 * x + rng.normal(0, 0.6, 500)
    y_neg = -0.8 * x + rng.normal(0, 0.6, 500)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), dpi=300)

    axes[0].hist(x, bins=25, color="#4C78A8", alpha=0.85, edgecolor="white")
    axes[0].axvline(np.mean(x), color="#D62728", lw=2, label="mean")
    axes[0].set_title("Expectation as center")
    axes[0].set_xlabel("X")
    axes[0].set_ylabel("count")
    axes[0].legend(frameon=False)

    axes[1].scatter(x, y_pos, s=8, alpha=0.35, color="#2CA02C")
    axes[1].set_title("Positive covariance")
    axes[1].set_xlabel("X")
    axes[1].set_ylabel("Y")

    axes[2].scatter(x, y_neg, s=8, alpha=0.35, color="#FF7F0E")
    axes[2].set_title("Negative covariance")
    axes[2].set_xlabel("X")
    axes[2].set_ylabel("Y")

    fig.suptitle("Expectation, variance, and covariance", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{output_dir}/expectation_variance_covariance_visual.png", bbox_inches="tight")
    plt.close(fig)


def save_lln_clt(output_dir: str) -> None:
    rng = np.random.default_rng(42)
    n = 2000
    samples = rng.exponential(scale=1.0, size=n)
    running_mean = np.cumsum(samples) / np.arange(1, n + 1)

    reps = 3000
    size = 30
    means = rng.exponential(scale=1.0, size=(reps, size)).mean(axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)

    axes[0].plot(running_mean, color="#1F77B4", lw=1.7)
    axes[0].axhline(1.0, color="#D62728", ls="--", lw=1.6, label="true mean")
    axes[0].set_title("LLN: running mean converges")
    axes[0].set_xlabel("n")
    axes[0].set_ylabel("running mean")
    axes[0].legend(frameon=False)

    axes[1].hist(means, bins=35, color="#9467BD", alpha=0.85, edgecolor="white", density=True)
    axes[1].set_title("CLT: sample means near normal")
    axes[1].set_xlabel("sample mean")
    axes[1].set_ylabel("density")

    fig.suptitle("LLN and CLT intuition", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{output_dir}/lln_clt_convergence.png", bbox_inches="tight")
    plt.close(fig)


def save_sampling_distribution(output_dir: str) -> None:
    rng = np.random.default_rng(42)
    reps = 3000
    mu = 0.0
    sigma = 2.0

    means_n20 = rng.normal(mu, sigma, size=(reps, 20)).mean(axis=1)
    means_n200 = rng.normal(mu, sigma, size=(reps, 200)).mean(axis=1)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)
    axes[0].hist(means_n20, bins=35, color="#E45756", alpha=0.8, edgecolor="white")
    axes[0].set_title("Sampling dist (n=20)")
    axes[0].set_xlabel("mean estimate")

    axes[1].hist(means_n200, bins=35, color="#4C78A8", alpha=0.8, edgecolor="white")
    axes[1].set_title("Sampling dist (n=200)")
    axes[1].set_xlabel("mean estimate")

    fig.suptitle("Standard error shrinks as n increases", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{output_dir}/sampling_distribution_standard_error.png", bbox_inches="tight")
    plt.close(fig)


def save_bias_variance(output_dir: str) -> None:
    complexity = np.linspace(1, 10, 200)
    bias2 = 1.3 / complexity
    variance = 0.03 * (complexity - 1.0) ** 2
    mse = bias2 + variance + 0.08

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
    ax.plot(complexity, bias2, label="Bias^2", color="#1F77B4", lw=2)
    ax.plot(complexity, variance, label="Variance", color="#FF7F0E", lw=2)
    ax.plot(complexity, mse, label="MSE", color="#2CA02C", lw=2.2)
    ax.set_xlabel("Model complexity")
    ax.set_ylabel("Error")
    ax.set_title("Bias-variance tradeoff")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    plt.tight_layout()
    fig.savefig(f"{output_dir}/bias_variance_tradeoff_curve.png", bbox_inches="tight")
    plt.close(fig)


def save_log_probability(output_dir: str) -> None:
    n_values = np.arange(1, 81)
    p = 0.01
    direct = p ** n_values
    log_scale = n_values * np.log(p)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)

    axes[0].plot(n_values, direct, color="#D62728", lw=2)
    axes[0].set_yscale("log")
    axes[0].set_title("Direct product p^n")
    axes[0].set_xlabel("n")
    axes[0].set_ylabel("value (log axis)")

    axes[1].plot(n_values, log_scale, color="#1F77B4", lw=2)
    axes[1].set_title("Log-domain sum n*log(p)")
    axes[1].set_xlabel("n")
    axes[1].set_ylabel("log value")

    fig.suptitle("Numerical stability with log-probabilities", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{output_dir}/log_probability_numerical_stability.png", bbox_inches="tight")
    plt.close(fig)


def save_model_assumptions(output_dir: str) -> None:
    rng = np.random.default_rng(42)
    x = np.linspace(0, 10, 140)
    y = 1.2 * x + rng.normal(0, 1.2, x.size)
    y[12] += 8.0
    y[95] -= 7.0

    coef = np.polyfit(x, y, 1)
    y_hat = np.polyval(coef, x)
    resid = y - y_hat

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)

    axes[0].scatter(x, y, s=14, alpha=0.7, color="#4C78A8")
    axes[0].plot(x, y_hat, color="#D62728", lw=2)
    axes[0].set_title("Fit and potential outliers")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")

    axes[1].scatter(y_hat, resid, s=14, alpha=0.7, color="#F58518")
    axes[1].axhline(0, color="#333333", lw=1)
    axes[1].set_title("Residual check")
    axes[1].set_xlabel("fitted")
    axes[1].set_ylabel("residual")

    fig.suptitle("Basic assumption checks", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{output_dir}/basic_model_assumption_checks.png", bbox_inches="tight")
    plt.close(fig)


def save_simulation_workflow(output_dir: str) -> None:
    fig, ax = plt.subplots(figsize=(10.5, 4.3), dpi=300)
    ax.axis("off")

    boxes = [
        (0.4, 1.5, 2.0, 1.2, "Assume model"),
        (2.9, 1.5, 2.0, 1.2, "Set parameters"),
        (5.4, 1.5, 2.0, 1.2, "Simulate data"),
        (7.9, 1.5, 2.0, 1.2, "Compare / revise"),
    ]

    for x, y, w, h, txt in boxes:
        rect = plt.Rectangle((x, y), w, h, ec="#2F3E4D", fc="#EAF2FB", lw=1.6)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=11, fontweight="bold")

    for sx in [2.4, 4.9, 7.4]:
        ax.annotate("", xy=(sx + 0.45, 2.1), xytext=(sx, 2.1), arrowprops=dict(arrowstyle="->", lw=1.8, color="#3B6EA8"))

    ax.annotate("", xy=(1.3, 1.2), xytext=(8.8, 1.2), arrowprops=dict(arrowstyle="->", lw=1.8, color="#6A3D9A"))
    ax.text(5.05, 0.9, "repeat many times", ha="center", va="center", fontsize=10, color="#6A3D9A")

    ax.set_xlim(0, 10.5)
    ax.set_ylim(0.3, 3.5)
    ax.set_title("Simulation workflow for statistical intuition", fontsize=13, fontweight="bold")
    plt.tight_layout()
    fig.savefig(f"{output_dir}/simulation_statistical_intuition_workflow.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    output_dir = "."
    save_expectation_variance_covariance(output_dir)
    save_lln_clt(output_dir)
    save_sampling_distribution(output_dir)
    save_bias_variance(output_dir)
    save_log_probability(output_dir)
    save_model_assumptions(output_dir)
    save_simulation_workflow(output_dir)


if __name__ == "__main__":
    main()
