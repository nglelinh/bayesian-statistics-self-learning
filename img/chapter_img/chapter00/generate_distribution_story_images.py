#!/usr/bin/env python3
"""
Generate standalone illustration images for the Chapter 00 distribution lessons
00_02_01 through 00_02_04.

Each concept is rendered as its own image instead of using multi-panel collages.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


OUTPUT_DIR = Path(__file__).resolve().parent
RNG = np.random.default_rng(20260322)
COLORS = {
    "blue": "#2E86AB",
    "teal": "#06A77D",
    "orange": "#F18F01",
    "rose": "#A23B72",
    "red": "#D1495B",
    "navy": "#2B2D42",
    "light": "#EDF2F4",
    "gold": "#F4D35E",
    "green": "#2A9D8F",
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


def save_figure(fig: plt.Figure, filename: str) -> None:
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Saved: {filename}")
    plt.close(fig)


def generate_bernoulli_binary_outcomes() -> None:
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    p = 0.35
    x = np.array([0, 1])
    probs = np.array([1 - p, p])
    colors = [COLORS["red"], COLORS["green"]]
    labels = ["Thất bại", "Thành công"]

    bars = ax.bar(x, probs, width=0.55, color=colors, alpha=0.88, edgecolor="white", linewidth=2)
    for bar, prob, label in zip(bars, probs, labels):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            prob + 0.04,
            f"{label}\nP = {prob:.2f}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    ax.set_xticks(x, ["0", "1"])
    ax.set_ylim(0, 0.9)
    ax.set_xlabel("Kết quả của một lần thử")
    ax.set_ylabel("Xác suất")
    ax.set_title("Bernoulli: mỗi lần thử chỉ có hai kết quả")
    ax.text(
        0.03,
        0.95,
        "Ví dụ: một lượt click có xác suất thành công p = 0.35.",
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLORS["blue"], linewidth=1.5),
    )
    save_figure(fig, "bernoulli_binary_outcomes.png")


def generate_binomial_success_count_distribution() -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    n = 12
    p = 0.35
    batches = RNG.binomial(n, p, size=5000)
    x = np.arange(0, n + 1)
    pmf = stats.binom.pmf(x, n, p)

    ax.hist(
        batches,
        bins=np.arange(-0.5, n + 1.5, 1),
        density=True,
        color=COLORS["blue"],
        alpha=0.28,
        edgecolor="white",
        label="Mô phỏng nhiều lô thử",
    )
    ax.plot(x, pmf, marker="o", color=COLORS["orange"], linewidth=2.8, label="PMF Binomial lý thuyết")
    ax.axvline(n * p, color=COLORS["red"], linestyle="--", linewidth=2.2, label=f"Trung bình = np = {n * p:.1f}")
    ax.set_xticks(x)
    ax.set_xlabel("Số lần thành công K")
    ax.set_ylabel("Xác suất / mật độ xấp xỉ")
    ax.set_title("Binomial: đếm số lần thành công sau nhiều lần thử")
    ax.text(
        0.97,
        0.95,
        "Nếu lặp lại Bernoulli n lần độc lập,\nBinomial mô tả phân phối của tổng số lần thành công.",
        transform=ax.transAxes,
        ha="right",
        va="top",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLORS["orange"], linewidth=1.5),
    )
    ax.legend(loc="upper left", framealpha=0.95)
    save_figure(fig, "binomial_success_count_distribution.png")


def generate_poisson_counts_timeline() -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.8))
    rate = 2.0
    horizon = 6.0

    interarrivals = RNG.exponential(scale=1 / rate, size=200)
    event_times = np.cumsum(interarrivals)
    event_times = event_times[event_times <= horizon]
    hourly_counts, _ = np.histogram(event_times, bins=np.arange(0, horizon + 1, 1))

    for hour in range(int(horizon)):
        ax.axvspan(hour, hour + 1, color=COLORS["light"] if hour % 2 == 0 else "#F8F9FA", alpha=0.95)
        ax.text(hour + 0.5, 1.08, f"{hourly_counts[hour]} sự kiện", ha="center", va="bottom", fontweight="bold")

    ax.eventplot(event_times, colors=COLORS["orange"], lineoffsets=0.42, linelengths=0.52, linewidths=3.2)
    ax.set_xlim(0, horizon)
    ax.set_ylim(0, 1.32)
    ax.set_yticks([])
    ax.set_xlabel("Thời gian (giờ)")
    ax.set_title("Poisson: cùng một tốc độ trung bình, nhưng số đếm mỗi giờ vẫn dao động")
    ax.text(
        0.02,
        0.94,
        "Ví dụ với λ = 2 sự kiện/giờ: mỗi khoảng 1 giờ có một số đếm ngẫu nhiên khác nhau.",
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=COLORS["blue"], linewidth=1.5),
    )
    save_figure(fig, "poisson_counts_timeline.png")


def generate_exponential_waiting_time_curve() -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    rate = 2.0
    waits = RNG.exponential(scale=1 / rate, size=4000)
    x = np.linspace(0, 3.5, 400)
    pdf = stats.expon.pdf(x, scale=1 / rate)

    ax.hist(
        waits,
        bins=32,
        density=True,
        color=COLORS["green"],
        alpha=0.30,
        edgecolor="white",
        label="Mô phỏng thời gian chờ",
    )
    ax.plot(x, pdf, color=COLORS["navy"], linewidth=2.8, label="Mật độ Exponential lý thuyết")
    ax.axvline(1 / rate, color=COLORS["red"], linestyle="--", linewidth=2.2, label=f"Kỳ vọng = 1/λ = {1 / rate:.2f}")
    ax.set_xlabel("Thời gian chờ tới sự kiện kế tiếp")
    ax.set_ylabel("Mật độ")
    ax.set_title("Exponential: nếu sự kiện đến nhanh hơn, thời gian chờ trung bình sẽ ngắn hơn")
    ax.text(
        0.04,
        0.94,
        "Đây là mặt còn lại của quá trình Poisson:\nthay vì đếm số sự kiện, ta theo dõi thời gian chờ.",
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=COLORS["green"], linewidth=1.5),
    )
    ax.legend(loc="upper right", framealpha=0.95)
    save_figure(fig, "exponential_waiting_time_curve.png")


def generate_normal_distribution_rule() -> None:
    fig, ax = plt.subplots(figsize=(8.8, 5.6))
    x = np.linspace(-4, 4, 1000)
    pdf = stats.norm.pdf(x, loc=0, scale=1)

    ax.plot(x, pdf, linewidth=3, color=COLORS["navy"])

    x_3 = x[(x >= -3) & (x <= 3)]
    x_2 = x[(x >= -2) & (x <= 2)]
    x_1 = x[(x >= -1) & (x <= 1)]
    ax.fill_between(x_3, stats.norm.pdf(x_3), color=COLORS["rose"], alpha=0.10, label="99.7% trong ±3σ")
    ax.fill_between(x_2, stats.norm.pdf(x_2), color=COLORS["gold"], alpha=0.18, label="95% trong ±2σ")
    ax.fill_between(x_1, stats.norm.pdf(x_1), color=COLORS["green"], alpha=0.28, label="68% trong ±1σ")

    for tick in range(-3, 4):
        ax.axvline(tick, color=COLORS["gray"] if "gray" in COLORS else "#8D99AE", linestyle="--", linewidth=1, alpha=0.6)
        ax.text(tick, -0.014, f"{tick}σ", ha="center")

    ax.set_ylim(-0.03, 0.43)
    ax.set_xlabel("Độ lệch chuẩn tính từ trung bình")
    ax.set_ylabel("Mật độ")
    ax.set_title("Normal: quy tắc 68-95-99.7 giúp đọc độ phân tán rất nhanh")
    ax.legend(loc="upper right", framealpha=0.95)
    save_figure(fig, "normal_distribution_rule.png")


def generate_clt_sample_means_overlay() -> None:
    fig, ax = plt.subplots(figsize=(8.8, 5.6))
    population = RNG.exponential(scale=1.0, size=9000)
    means_5 = RNG.exponential(scale=1.0, size=(3500, 5)).mean(axis=1)
    means_30 = RNG.exponential(scale=1.0, size=(3500, 30)).mean(axis=1)

    sns.kdeplot(population, ax=ax, color=COLORS["orange"], linewidth=2.8, label="Dữ liệu gốc lệch phải")
    sns.kdeplot(means_5, ax=ax, color=COLORS["blue"], linewidth=2.8, label="Trung bình mẫu, n = 5")
    sns.kdeplot(means_30, ax=ax, color=COLORS["green"], linewidth=2.8, label="Trung bình mẫu, n = 30")
    ax.axvline(1.0, color=COLORS["red"], linestyle="--", linewidth=2.2, label="Kỳ vọng thật = 1.0")
    ax.set_xlim(-0.1, 4.2)
    ax.set_xlabel("Giá trị")
    ax.set_ylabel("Mật độ")
    ax.set_title("CLT: khi lấy trung bình mẫu, phân phối dần trở nên tròn và hẹp hơn")
    ax.text(
        0.04,
        0.94,
        "Điểm chính là sự thay đổi của phân phối trung bình mẫu,\nkhông phải dữ liệu gốc bỗng trở thành Normal.",
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=COLORS["blue"], linewidth=1.5),
    )
    ax.legend(loc="upper right", framealpha=0.95)
    save_figure(fig, "clt_sample_means_overlay.png")


def generate_beta_binomial_update_vi() -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    theta = np.linspace(0.001, 0.999, 600)
    prior = stats.beta.pdf(theta, 2, 2)
    posterior = stats.beta.pdf(theta, 10, 4)
    likelihood_shape = theta**8 * (1 - theta) ** 2
    likelihood_shape = likelihood_shape / likelihood_shape.max() * posterior.max()

    ax.plot(theta, prior, color=COLORS["blue"], linewidth=2.8, label="Prior Beta(2,2)")
    ax.plot(theta, likelihood_shape, color=COLORS["orange"], linewidth=2.6, linestyle="--", label="Likelihood shape: 8 thành công / 10")
    ax.plot(theta, posterior, color=COLORS["green"], linewidth=3.0, label="Posterior Beta(10,4)")
    ax.axvline(0.5, color=COLORS["blue"], linestyle=":", linewidth=2)
    ax.axvline(10 / 14, color=COLORS["green"], linestyle=":", linewidth=2)
    ax.set_xlabel("Xác suất thành công p")
    ax.set_ylabel("Mật độ / hình dạng tỷ lệ")
    ax.set_title("Beta-Binomial: dữ liệu tốt kéo niềm tin về p sang phải và sắc hơn")
    ax.text(
        0.04,
        0.80,
        "Prior còn khá rộng quanh 0.5.\nSau 8 thành công trên 10 lần thử, posterior tập trung hơn.",
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=COLORS["green"], linewidth=1.5),
    )
    ax.legend(loc="upper left", framealpha=0.95)
    save_figure(fig, "beta_binomial_update_vi.png")


def generate_gamma_poisson_update_vi() -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    lam = np.linspace(0.001, 6.0, 600)
    prior = stats.gamma.pdf(lam, a=3, scale=1.0)
    posterior = stats.gamma.pdf(lam, a=17, scale=1 / 6)

    ax.plot(lam, prior, color=COLORS["rose"], linewidth=2.8, label="Prior Gamma(3,1)")
    ax.plot(lam, posterior, color=COLORS["navy"], linewidth=3.0, label="Posterior Gamma(17,6)")
    ax.axvline(3.0, color=COLORS["rose"], linestyle=":", linewidth=2)
    ax.axvline(17 / 6, color=COLORS["navy"], linestyle=":", linewidth=2)
    ax.set_xlabel("Rate λ")
    ax.set_ylabel("Mật độ")
    ax.set_title("Gamma-Poisson: quan sát nhiều sự kiện hơn sẽ đẩy posterior sang vùng λ lớn hơn")
    ax.text(
        0.04,
        0.94,
        "Ví dụ: tổng 14 sự kiện trong 5 khoảng thời gian\nkhiến posterior nghiêng về các giá trị λ cao hơn prior.",
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=COLORS["navy"], linewidth=1.5),
    )
    ax.legend(loc="upper right", framealpha=0.95)
    save_figure(fig, "gamma_poisson_update_vi.png")


def main() -> None:
    generate_bernoulli_binary_outcomes()
    generate_binomial_success_count_distribution()
    generate_poisson_counts_timeline()
    generate_exponential_waiting_time_curve()
    generate_normal_distribution_rule()
    generate_clt_sample_means_overlay()
    generate_beta_binomial_update_vi()
    generate_gamma_poisson_update_vi()


if __name__ == "__main__":
    main()
