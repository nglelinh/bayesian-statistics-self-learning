#!/usr/bin/env python3
"""
Generate illustration images for lesson 00_03_descriptive_statistics.

These figures focus on visual intuition:
- mean vs median under symmetry and skewness
- same center but different spread, plus box plot / IQR intuition
- correlation patterns and the limits of Pearson correlation
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


OUTPUT_DIR = Path(__file__).resolve().parent
RNG = np.random.default_rng(20260321)
COLORS = {
    "blue": "#2E86AB",
    "teal": "#06A77D",
    "orange": "#F18F01",
    "rose": "#A23B72",
    "red": "#D62246",
    "navy": "#2B2D42",
    "light": "#EDF2F4",
    "gold": "#F4D35E",
}


plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "figure.titlesize": 18,
        "figure.titleweight": "bold",
    }
)


def save_figure(filename: str) -> None:
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Saved: {filename}")
    plt.close()


def add_mean_median_lines(ax: plt.Axes, data: np.ndarray) -> tuple[float, float]:
    mean_value = float(np.mean(data))
    median_value = float(np.median(data))
    ax.axvline(mean_value, color=COLORS["red"], linewidth=2.5, linestyle="--", label=f"Trung bình = {mean_value:.1f}")
    ax.axvline(
        median_value,
        color=COLORS["navy"],
        linewidth=2.5,
        linestyle="-",
        label=f"Trung vị = {median_value:.1f}",
    )
    return mean_value, median_value


def generate_mean_vs_median() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))

    symmetric = RNG.normal(loc=70, scale=8, size=500)
    skewed = RNG.lognormal(mean=4.05, sigma=0.45, size=600)

    datasets = [
        (
            axes[0],
            symmetric,
            "Phân phối gần đối xứng",
            "Khi dữ liệu cân đối, trung bình và trung vị gần nhau.",
            COLORS["blue"],
            (40, 100),
        ),
        (
            axes[1],
            skewed,
            "Phân phối lệch phải",
            "Đuôi phải kéo trung bình sang phải mạnh hơn trung vị.",
            COLORS["orange"],
            (20, 130),
        ),
    ]

    for ax, data, title, subtitle, color, xlim in datasets:
        sns.histplot(data, bins=24, stat="density", color=color, alpha=0.45, edgecolor="white", ax=ax)
        sns.kdeplot(data, color=color, linewidth=2.5, ax=ax)
        mean_value, median_value = add_mean_median_lines(ax, data)

        ax.set_title(title, color=color)
        ax.set_xlabel("Giá trị quan sát")
        ax.set_ylabel("Mật độ")
        ax.set_xlim(*xlim)
        ax.text(
            0.02,
            0.92,
            subtitle,
            transform=ax.transAxes,
            va="top",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=color, linewidth=1.5),
        )
        ax.text(
            0.02,
            0.78,
            f"Chênh lệch mean - median = {mean_value - median_value:.1f}",
            transform=ax.transAxes,
            va="top",
            fontweight="bold",
            color=COLORS["navy"],
        )
        ax.legend(loc="upper right", framealpha=0.95)

    fig.suptitle("Trung bình và Trung vị kể gì về hình dạng phân phối?")
    save_figure("descriptive_mean_vs_median.png")


def generate_spread_and_boxplot() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))

    tight = RNG.normal(loc=75, scale=4, size=400)
    wide = RNG.normal(loc=75, scale=13, size=400)
    box_data = np.concatenate([RNG.normal(loc=72, scale=8, size=120), np.array([112, 118])])

    ax = axes[0]
    sns.kdeplot(tight, fill=True, color=COLORS["teal"], alpha=0.35, linewidth=2.2, ax=ax, label="Độ lệch chuẩn nhỏ")
    sns.kdeplot(wide, fill=True, color=COLORS["rose"], alpha=0.20, linewidth=2.2, ax=ax, label="Độ lệch chuẩn lớn")
    ax.axvline(np.mean(tight), color=COLORS["navy"], linestyle="--", linewidth=2.5, label="Cùng trung bình xấp xỉ 75")
    ax.set_title("Cùng trung bình, độ phân tán vẫn có thể rất khác")
    ax.set_xlabel("Điểm số")
    ax.set_ylabel("Mật độ")
    ax.set_xlim(25, 125)
    ax.text(
        0.03,
        0.82,
        "Hai nhóm đều có trung tâm tương tự,\nnhưng một nhóm bất định hơn nhiều.",
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLORS["navy"], linewidth=1.5),
    )
    ax.legend(loc="upper left", framealpha=0.95)

    ax = axes[1]
    bp = ax.boxplot(
        box_data,
        vert=False,
        widths=0.45,
        patch_artist=True,
        boxprops=dict(facecolor=COLORS["gold"], edgecolor=COLORS["navy"], linewidth=2),
        medianprops=dict(color=COLORS["red"], linewidth=3),
        whiskerprops=dict(color=COLORS["navy"], linewidth=2),
        capprops=dict(color=COLORS["navy"], linewidth=2),
        flierprops=dict(marker="o", markerfacecolor=COLORS["red"], markeredgecolor="white", markersize=8, alpha=0.9),
    )
    q1, median, q3 = np.percentile(box_data, [25, 50, 75])
    iqr = q3 - q1

    ax.axvspan(q1, q3, color=COLORS["gold"], alpha=0.18)
    ax.text(q1, 1.26, "Q1", ha="center", color=COLORS["navy"], fontweight="bold")
    ax.text(median, 0.74, "Median", ha="center", color=COLORS["red"], fontweight="bold")
    ax.text(q3, 1.26, "Q3", ha="center", color=COLORS["navy"], fontweight="bold")
    ax.annotate(
        f"IQR = Q3 - Q1 = {iqr:.1f}",
        xy=((q1 + q3) / 2, 1),
        xytext=(median, 1.42),
        ha="center",
        arrowprops=dict(arrowstyle="<->", color=COLORS["rose"], linewidth=2),
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=COLORS["rose"], linewidth=1.5),
    )
    ax.set_title("Box plot: phần giữa của dữ liệu và các outlier")
    ax.set_xlabel("Giá trị quan sát")
    ax.set_yticks([])
    ax.set_xlim(35, 125)
    ax.text(
        0.03,
        0.15,
        "Hộp chứa 50% dữ liệu ở giữa.\nCác điểm đỏ là outlier tiềm năng theo quy tắc 1.5 × IQR.",
        transform=ax.transAxes,
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLORS["red"], linewidth=1.5),
    )

    fig.suptitle("Độ phân tán và IQR giúp ta đọc mức độ bất định của dữ liệu")
    save_figure("descriptive_spread_and_boxplot.png")


def generate_correlation_patterns() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.7))

    x_linear = np.linspace(0, 10, 80)
    y_linear = 1.8 * x_linear + RNG.normal(0, 2.0, size=x_linear.size)

    x_curve = np.linspace(-3, 3, 120)
    y_curve = x_curve**2 + RNG.normal(0, 0.35, size=x_curve.size)

    hidden_group = np.repeat([0, 1], 50)
    x_group = np.concatenate([RNG.normal(40, 5, 50), RNG.normal(70, 5, 50)])
    y_group = np.concatenate([RNG.normal(55, 6, 50), RNG.normal(82, 6, 50)])
    group_colors = np.where(hidden_group == 0, COLORS["blue"], COLORS["orange"])

    scenarios = [
        (axes[0], x_linear, y_linear, COLORS["teal"], "Tuyến tính dương", "Pearson r đo tốt"),
        (axes[1], x_curve, y_curve, COLORS["rose"], "Phi tuyến rõ rệt", "r gần 0 vẫn có cấu trúc"),
    ]

    for ax, x_data, y_data, color, title, subtitle in scenarios:
        ax.scatter(x_data, y_data, s=40, color=color, alpha=0.8, edgecolor="white", linewidth=0.5)
        if title == "Tuyến tính dương":
            coef = np.polyfit(x_data, y_data, 1)
            line = np.poly1d(coef)
            ax.plot(x_data, line(x_data), color=COLORS["navy"], linewidth=2.5)
        else:
            order = np.argsort(x_data)
            ax.plot(x_data[order], y_data[order], color=COLORS["navy"], linewidth=2.0, alpha=0.7)

        corr = np.corrcoef(x_data, y_data)[0, 1]
        ax.set_title(title, color=color)
        ax.set_xlabel("Biến X")
        ax.set_ylabel("Biến Y")
        ax.text(
            0.03,
            0.94,
            f"{subtitle}\nr = {corr:.2f}",
            transform=ax.transAxes,
            va="top",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=color, linewidth=1.5),
        )

    ax = axes[2]
    ax.scatter(x_group, y_group, s=42, c=group_colors, alpha=0.82, edgecolor="white", linewidth=0.5)
    corr_group = np.corrcoef(x_group, y_group)[0, 1]
    ax.set_title("Tương quan do nhóm ẩn", color=COLORS["orange"])
    ax.set_xlabel("Biến X")
    ax.set_ylabel("Biến Y")
    ax.text(
        0.03,
        0.94,
        f"Nhìn chung có vẻ tương quan mạnh,\nnhưng màu sắc gợi ý một biến thứ ba.\nr = {corr_group:.2f}",
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=COLORS["orange"], linewidth=1.5),
    )
    ax.text(44, 90, "Nhóm A", color=COLORS["blue"], fontweight="bold")
    ax.text(72, 97, "Nhóm B", color=COLORS["orange"], fontweight="bold")

    fig.suptitle("Scatter plot giúp thấy điều mà một hệ số tương quan có thể bỏ lỡ")
    save_figure("descriptive_correlation_patterns.png")


def main() -> None:
    generate_mean_vs_median()
    generate_spread_and_boxplot()
    generate_correlation_patterns()


if __name__ == "__main__":
    main()
