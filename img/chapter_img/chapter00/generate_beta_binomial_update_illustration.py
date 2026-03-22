"""Generate illustration for Beta-Binomial 7/10 update example."""

from math import gamma
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_PATH = Path(__file__).resolve().parent / "beta_binomial_update_7of10.png"


def beta_fn(a: float, b: float) -> float:
    return gamma(a) * gamma(b) / gamma(a + b)


def beta_pdf(theta: np.ndarray, a: float, b: float) -> np.ndarray:
    return (theta ** (a - 1)) * ((1 - theta) ** (b - 1)) / beta_fn(a, b)


def main() -> None:
    theta = np.linspace(1e-4, 1 - 1e-4, 1000)

    prior = beta_pdf(theta, 2, 2)
    like_shape = (theta**7) * ((1 - theta) ** 3)
    like_shape = like_shape / like_shape.max() * 3.2
    posterior = beta_pdf(theta, 9, 5)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(9.2, 5.4))

    ax.plot(theta, prior, linewidth=2.2, color="#1f77b4", label="Prior: Beta(2,2)")
    ax.plot(theta, like_shape, linewidth=2.2, color="#ff7f0e", linestyle="--", label="Likelihood shape: theta^7(1-theta)^3")
    ax.plot(theta, posterior, linewidth=2.6, color="#2ca02c", label="Posterior: Beta(9,5)")

    ax.axvline(0.5, color="#888", linewidth=1.0, alpha=0.8)
    ax.axvline(0.7, color="#888", linewidth=1.0, alpha=0.8)

    ax.set_title("Beta-Binomial update example: y=7 successes out of n=10", fontsize=14, fontweight="bold")
    ax.set_xlabel("theta", fontsize=12)
    ax.set_ylabel("density / scaled shape", fontsize=12)
    ax.tick_params(labelsize=11)
    ax.legend(frameon=False, fontsize=10, loc="upper left")

    ax.text(
        0.98,
        0.95,
        "p(theta|y) = [1/B(9,5)] theta^8 (1-theta)^4",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.9, "edgecolor": "#999"},
    )

    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=180)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
