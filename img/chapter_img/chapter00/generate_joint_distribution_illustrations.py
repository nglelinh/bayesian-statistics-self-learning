import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def normal_pdf(x, mu, sigma):
    coef = 1.0 / (sigma * np.sqrt(2.0 * np.pi))
    return coef * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def build_joint_and_marginals():
    x = np.linspace(-3.5, 3.5, 400)
    y = np.linspace(-3.5, 3.5, 400)
    xx, yy = np.meshgrid(x, y)

    fx = normal_pdf(x, mu=0.0, sigma=1.0)
    fy = normal_pdf(y, mu=0.5, sigma=1.2)
    joint = np.outer(fy, fx)

    y0 = 1.0
    conditional_x_given_y0 = normal_pdf(x, mu=0.0, sigma=1.0)
    conditional_x_given_y0 = conditional_x_given_y0 / np.trapezoid(conditional_x_given_y0, x)

    return x, y, xx, yy, joint, fx, fy, y0, conditional_x_given_y0


def plot_joint_marginal_figure(output_path):
    x, y, xx, yy, joint, fx, fy, y0, cond = build_joint_and_marginals()

    plt.style.use("seaborn-v0_8-whitegrid")
    fig = plt.figure(figsize=(11, 8.5), dpi=140)
    gs = GridSpec(2, 2, width_ratios=[4.5, 1.5], height_ratios=[1.5, 4.5], hspace=0.12, wspace=0.12)

    ax_top = fig.add_subplot(gs[0, 0])
    ax_joint = fig.add_subplot(gs[1, 0])
    ax_right = fig.add_subplot(gs[1, 1])
    ax_empty = fig.add_subplot(gs[0, 1])
    ax_empty.axis("off")

    levels = np.linspace(joint.min(), joint.max(), 18)
    contour = ax_joint.contourf(xx, yy, joint, levels=levels, cmap="YlGnBu")
    ax_joint.contour(xx, yy, joint, levels=10, colors="white", linewidths=0.4, alpha=0.8)
    ax_joint.axhline(y0, color="#d62728", linestyle="--", linewidth=1.8, label=r"Slice at $y=y_0$")
    ax_joint.set_xlabel(r"$x$")
    ax_joint.set_ylabel(r"$y$")
    ax_joint.set_title("Joint Density $f(x,y)$", fontsize=12)
    ax_joint.legend(loc="upper right", frameon=True)

    cbar = fig.colorbar(contour, ax=ax_joint, shrink=0.92, pad=0.02)
    cbar.set_label("density", rotation=90)

    ax_top.plot(x, fx, color="#1f77b4", linewidth=2.2, label=r"$f_X(x)=\int f(x,y)dy$")
    ax_top.plot(x, cond, color="#d62728", linestyle="--", linewidth=2.0, label=r"$f(x\mid y_0)$")
    ax_top.set_xlim(x.min(), x.max())
    ax_top.set_ylabel("density")
    ax_top.set_title("Marginal and Conditional on x-axis", fontsize=12)
    ax_top.legend(loc="upper right", fontsize=9)

    ax_right.plot(fy, y, color="#2ca02c", linewidth=2.2)
    ax_right.set_xlabel("density")
    ax_right.set_ylim(y.min(), y.max())
    ax_right.set_title(r"$f_Y(y)=\int f(x,y)dx$", fontsize=12)

    fig.suptitle("From One-Variable Distributions to a Joint Distribution", fontsize=15, y=0.98)
    fig.text(
        0.5,
        0.015,
        "Center: joint density. Top/right: marginals via integration. Dashed slice illustrates a conditional distribution.",
        ha="center",
        fontsize=10,
    )

    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    plot_joint_marginal_figure("joint_distribution_marginalization.png")
