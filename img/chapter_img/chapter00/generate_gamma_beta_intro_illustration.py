"""Generate illustration for Gamma and Beta lesson."""

from math import gamma
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_PATH = Path(__file__).resolve().parent / "gamma_beta_intro_illustration.png"


def beta_function(a: float, b: float) -> float:
    return gamma(a) * gamma(b) / gamma(a + b)


def main() -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

    x = np.linspace(0.2, 6.0, 500)
    y = np.array([gamma(v) for v in x])
    axes[0].plot(x, y, color="#1f77b4", linewidth=2.5, label=r"$\Gamma(x)$")

    n = np.arange(1, 7)
    factorial_points = np.array([gamma(k) for k in n])
    axes[0].scatter(n, factorial_points, color="#d62728", s=45, zorder=3, label=r"$\Gamma(n)=(n-1)!$")
    axes[0].set_title("Gamma extends factorial")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel(r"$\Gamma(x)$")
    axes[0].set_ylim(0, 30)
    axes[0].legend(frameon=False)

    t = np.linspace(0, 1, 500)
    a, b = 2.0, 5.0
    integrand = (t ** (a - 1)) * ((1 - t) ** (b - 1))
    b_ab = beta_function(a, b)
    beta_pdf = integrand / b_ab

    axes[1].plot(t, integrand, color="#ff7f0e", linewidth=2.2, label=r"$t^{a-1}(1-t)^{b-1}$")
    axes[1].fill_between(t, 0, integrand, color="#ffbb78", alpha=0.45)
    axes[1].plot(t, beta_pdf, color="#2ca02c", linewidth=2.2, label=r"$\mathrm{Beta}(a,b)$ pdf")
    axes[1].set_title("Beta as normalization on [0,1]")
    axes[1].set_xlabel("t")
    axes[1].set_ylabel("value")
    axes[1].text(
        0.98,
        0.96,
        rf"$B(2,5)=\int_0^1 t(1-t)^4dt={b_ab:.4f}$",
        transform=axes[1].transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "alpha": 0.9, "edgecolor": "#999"},
    )
    axes[1].legend(frameon=False, loc="upper left")

    fig.suptitle("Gamma and Beta: core relationship for Bayesian normalization", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(OUT_PATH, dpi=180)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
