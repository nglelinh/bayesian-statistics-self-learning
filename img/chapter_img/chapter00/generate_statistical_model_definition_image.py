import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def make_figure(output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")

    colors = {
        "param": "#e8f1ff",
        "model": "#fff4de",
        "data": "#e9f9ef",
        "infer": "#f6ebff",
        "edge": "#2f3e4d",
        "arrow": "#3b6ea8",
    }

    boxes = [
        (0.8, 3.7, 2.3, 2.0, colors["param"], "Unknown\nparameter", r"$\theta$"),
        (3.5, 3.7, 2.8, 2.0, colors["model"], "Statistical\nmodel", r"$p(x\mid\theta)$"),
        (6.8, 3.7, 2.3, 2.0, colors["data"], "Observed\ndata", r"$x$"),
        (9.5, 3.7, 1.7, 2.0, colors["infer"], "Bayesian\nupdate", r"$p(\theta\mid x)$"),
    ]

    for x, y, w, h, face, title, formula in boxes:
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.25,rounding_size=0.12",
            linewidth=1.5,
            edgecolor=colors["edge"],
            facecolor=face,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h * 0.67, title, ha="center", va="center", fontsize=12, weight="bold")
        ax.text(x + w / 2, y + h * 0.30, formula, ha="center", va="center", fontsize=16)

    arrows = [
        ((3.1, 4.7), (3.5, 4.7), "assume"),
        ((6.3, 4.7), (6.8, 4.7), "generate"),
        ((9.1, 4.7), (9.5, 4.7), "infer"),
    ]
    for start, end, label in arrows:
        arr = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=18, linewidth=2, color=colors["arrow"])
        ax.add_patch(arr)
        ax.text((start[0] + end[0]) / 2, 5.05, label, fontsize=10, color=colors["arrow"], ha="center")

    eq_box = FancyBboxPatch(
        (1.0, 1.0),
        10.0,
        1.8,
        boxstyle="round,pad=0.3,rounding_size=0.10",
        linewidth=1.2,
        edgecolor="#7a6f8c",
        facecolor="#fbf8ff",
    )
    ax.add_patch(eq_box)
    ax.text(
        6.0,
        2.25,
        r"Model family: $\mathcal{M}=\{p(x\mid\theta):\theta\in\Theta\}$",
        fontsize=15,
        ha="center",
        va="center",
    )
    ax.text(
        6.0,
        1.55,
        r"Bayes update: $p(\theta\mid x)\propto p(x\mid\theta)p(\theta)$",
        fontsize=14,
        ha="center",
        va="center",
    )

    ax.set_title("Statistical model as a data-generating bridge", fontsize=17, weight="bold", pad=14)
    plt.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make_figure("statistical_model_definition_flow.png")
