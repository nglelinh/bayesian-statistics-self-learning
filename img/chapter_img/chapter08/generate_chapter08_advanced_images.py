#!/usr/bin/env python3
"""
Generate additional illustrations for Chapter 08.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def savefig(name: str) -> None:
    path = os.path.join(OUTPUT_DIR, name)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    print(f"Created: {name}")
    plt.close()


def make_waic_loo_comparison() -> None:
    np.random.seed(42)
    models = ["M1\nLinear", "M2\nQuadratic", "M3\nCubic", "M4\nOverfit"]
    elpd = np.array([-230.5, -221.2, -220.4, -224.8])
    se = np.array([6.2, 5.1, 5.4, 7.0])

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    x = np.arange(len(models))
    ax.errorbar(x, elpd, yerr=se, fmt="o", capsize=6, color="#1f77b4", linewidth=2)
    best = np.argmax(elpd)
    ax.scatter([best], [elpd[best]], color="#d62728", s=90, zorder=3, label="Best elpd")
    ax.axhline(elpd[best], linestyle="--", color="#d62728", alpha=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylabel("Estimated elpd (higher is better)")
    ax.set_title("WAIC/LOO Comparison: Estimate and Uncertainty")
    ax.grid(alpha=0.25, axis="y")
    ax.legend()
    savefig("chapter08_waic_loo_comparison.png")


def make_selection_vs_stacking() -> None:
    np.random.seed(42)
    grid = np.linspace(-3, 6, 500)

    # model A and B predictive densities (illustrative)
    mu_a, sd_a = 1.0, 0.9
    mu_b, sd_b = 2.1, 1.2
    dens_a = np.exp(-0.5 * ((grid - mu_a) / sd_a) ** 2) / (sd_a * np.sqrt(2 * np.pi))
    dens_b = np.exp(-0.5 * ((grid - mu_b) / sd_b) ** 2) / (sd_b * np.sqrt(2 * np.pi))

    w_a, w_b = 0.58, 0.42
    dens_mix = w_a * dens_a + w_b * dens_b

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(grid, dens_a, color="#1f77b4", linewidth=2, label="Model A predictive")
    ax.plot(grid, dens_b, color="#ff7f0e", linewidth=2, label="Model B predictive")
    ax.plot(grid, dens_mix, color="#2ca02c", linewidth=3, label="Stacking predictive")
    ax.axvline(mu_a, color="#1f77b4", linestyle="--", alpha=0.4)
    ax.axvline(mu_b, color="#ff7f0e", linestyle="--", alpha=0.4)
    ax.set_title("Selection vs Stacking: Predictive Distribution")
    ax.set_xlabel("Future outcome y")
    ax.set_ylabel("Density")
    ax.grid(alpha=0.25)
    ax.legend()
    savefig("chapter08_selection_vs_stacking.png")


def make_expected_loss_threshold() -> None:
    q = np.linspace(0, 1, 400)  # posterior probability of risk event
    loss_fp = 5.0
    loss_fn = 40.0

    # actions: alert vs no alert
    risk_alert = loss_fp * (1 - q)
    risk_noalert = loss_fn * q
    q_star = loss_fp / (loss_fp + loss_fn)

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(q, risk_alert, color="#d62728", linewidth=2.5, label="Risk(alert)")
    ax.plot(q, risk_noalert, color="#1f77b4", linewidth=2.5, label="Risk(no alert)")
    ax.axvline(q_star, linestyle="--", color="black", alpha=0.6, label=f"Threshold q*={q_star:.3f}")
    ax.set_xlabel("Posterior probability q = P(event | data)")
    ax.set_ylabel("Expected loss")
    ax.set_title("Bayes Decision Rule from Expected Loss")
    ax.grid(alpha=0.25)
    ax.legend()
    savefig("chapter08_expected_loss_threshold.png")


def make_voi_curve() -> None:
    cost = np.linspace(0, 15, 250)
    voi = 7.0
    net = voi - cost

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(cost, net, color="#2ca02c", linewidth=2.8, label="Net benefit = VOI - Cost")
    ax.axhline(0, linestyle="--", color="black", alpha=0.6)
    ax.axvline(voi, linestyle=":", color="#d62728", linewidth=2, label=f"Break-even cost = {voi:.1f}")
    ax.fill_between(cost, net, 0, where=net >= 0, alpha=0.2, color="#2ca02c", label="Collect data region")
    ax.fill_between(cost, net, 0, where=net < 0, alpha=0.2, color="#d62728", label="Do not collect region")
    ax.set_xlabel("Cost of additional information")
    ax.set_ylabel("Expected net benefit")
    ax.set_title("Value of Information Decision Curve")
    ax.grid(alpha=0.25)
    ax.legend()
    savefig("chapter08_voi_decision_curve.png")


def main() -> None:
    make_waic_loo_comparison()
    make_selection_vs_stacking()
    make_expected_loss_threshold()
    make_voi_curve()
    print("Done")


if __name__ == "__main__":
    main()
