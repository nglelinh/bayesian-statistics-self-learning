#!/usr/bin/env python3
"""
Generate illustrations for Lesson 00-07: Probability Density Functions (PDF)
This script creates comprehensive visualizations for understanding PDF concepts.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy import integrate
import matplotlib.patches as mpatches
from pathlib import Path
from PIL import Image

# Set Vietnamese font and style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150

OUTPUT_DIR = Path(__file__).resolve().parent


def save_current_figure(filename):
    """Save the active matplotlib figure next to this script."""
    output_path = OUTPUT_DIR / filename
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Generated: {output_path.name}")


def trim_whitespace(image, padding=20, threshold=245):
    """Trim outer whitespace while keeping a small visual margin."""
    rgba = np.asarray(image.convert("RGBA"))
    visible_pixels = np.any(rgba[:, :, :3] < threshold, axis=2) | (rgba[:, :, 3] < 250)
    coordinates = np.argwhere(visible_pixels)

    if coordinates.size == 0:
        return image

    y0, x0 = coordinates.min(axis=0)
    y1, x1 = coordinates.max(axis=0) + 1

    x0 = max(0, x0 - padding)
    y0 = max(0, y0 - padding)
    x1 = min(image.width, x1 + padding)
    y1 = min(image.height, y1 + padding)

    return image.crop((x0, y0, x1, y1))


def detect_shared_header_height(image, threshold=0.02, window=24):
    """Detect a sparse shared title band that should be removed before splitting."""
    rgba = np.asarray(image.convert("RGBA"))
    visible_pixels = np.any(rgba[:, :, :3] < 245, axis=2) | (rgba[:, :, 3] < 250)
    row_density = visible_pixels.mean(axis=1)
    rolling_density = np.convolve(row_density, np.ones(window) / window, mode='same')

    candidate_rows = np.where(rolling_density > threshold)[0]
    if candidate_rows.size == 0:
        return 0

    return max(0, int(candidate_rows[0]) - 8)


def split_figure_grid(filename, rows, cols, output_names, trim_shared_header=False, padding=20):
    """Split a multi-panel figure into standalone images."""
    if len(output_names) != rows * cols:
        raise ValueError("Number of output names must match rows * cols.")

    image = Image.open(OUTPUT_DIR / filename).convert("RGBA")

    if trim_shared_header:
        top_trim = detect_shared_header_height(image)
        image = image.crop((0, top_trim, image.width, image.height))

    cell_width = image.width / cols
    cell_height = image.height / rows

    for index, output_name in enumerate(output_names):
        row, col = divmod(index, cols)
        left = round(col * cell_width)
        upper = round(row * cell_height)
        right = round((col + 1) * cell_width)
        lower = round((row + 1) * cell_height)

        panel = image.crop((left, upper, right, lower))
        panel = trim_whitespace(panel, padding=padding).convert("RGB")
        panel.save(OUTPUT_DIR / output_name)
        print(f"  -> Split: {output_name}")

def generate_pmf_vs_continuous():
    """1. PMF (discrete) vs continuous variable problem"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: PMF - Dice
    outcomes = [1, 2, 3, 4, 5, 6]
    probabilities = [1/6] * 6
    
    bars = axes[0].bar(outcomes, probabilities, width=0.6, alpha=0.7, 
                       color='steelblue', edgecolor='black', linewidth=2)
    
    for bar, prob in zip(bars, probabilities):
        height = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{prob:.3f}', ha='center', va='bottom', 
                    fontsize=10, fontweight='bold')
    
    axes[0].set_xlabel('Giá trị (x)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('P(X = x)', fontsize=12, fontweight='bold')
    axes[0].set_title('PMF: Xúc xắc (Biến rời rạc)\nP(X=x) LÀ XÁC SUẤT', 
                     fontsize=13, fontweight='bold')
    axes[0].set_xticks(outcomes)
    axes[0].set_ylim(0, 0.25)
    axes[0].grid(axis='y', alpha=0.3)
    
    total_prob = sum(probabilities)
    axes[0].text(3.5, 0.22, f'Σ P(X=x) = {total_prob:.1f}', 
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6))
    
    # Right: Continuous variable problem
    x = np.linspace(140, 200, 1000)
    mu, sigma = 170, 10
    pdf = stats.norm.pdf(x, mu, sigma)
    
    axes[1].plot(x, pdf, 'b-', linewidth=2.5, label='f(x): Mật độ')
    axes[1].fill_between(x, pdf, alpha=0.3, color='lightblue')
    
    # Mark a specific point
    axes[1].scatter([170], [stats.norm.pdf(170, mu, sigma)], 
                   s=200, color='red', zorder=5, edgecolor='black', linewidth=2)
    axes[1].axvline(170, color='red', linestyle='--', alpha=0.5, linewidth=2)
    
    axes[1].text(170, stats.norm.pdf(170, mu, sigma) + 0.005,
                'P(X = 170) = 0!\n(Có vô số giá trị)', 
                ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6))
    
    axes[1].set_xlabel('Chiều cao (cm)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('f(x)', fontsize=12, fontweight='bold')
    axes[1].set_title('Biến liên tục: Chiều cao\nP(X=x) = 0 cho mọi x cụ thể', 
                     fontsize=13, fontweight='bold')
    axes[1].grid(alpha=0.3)
    axes[1].legend(fontsize=10)
    
    plt.tight_layout()
    save_current_figure('pmf_vs_continuous.png')
    split_figure_grid(
        'pmf_vs_continuous.png',
        rows=1,
        cols=2,
        output_names=[
            'pdf_pmf_dice.png',
            'pdf_continuous_height.png',
        ],
    )
    plt.close()


def generate_density_analogy():
    """2. Density analogy: mass density vs probability density"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Mass density
    x_mass = np.linspace(0, 10, 100)
    density_mass = 2 + 0.5 * np.sin(x_mass)
    
    axes[0].plot(x_mass, density_mass, 'b-', linewidth=2.5)
    axes[0].fill_between(x_mass, density_mass, alpha=0.3, color='lightblue')
    axes[0].set_xlabel('Vị trí (m)', fontsize=13, fontweight='bold')
    axes[0].set_ylabel('Mật độ khối lượng ρ(x)\n(kg/m³)', fontsize=13, fontweight='bold')
    axes[0].set_title('Mật độ Khối lượng (Vật lý)\nρ(x) KHÔNG PHẢI khối lượng', 
                     fontsize=14, fontweight='bold')
    axes[0].grid(alpha=0.3)
    
    # Highlight region
    x_fill = x_mass[(x_mass >= 3) & (x_mass <= 7)]
    density_fill = 2 + 0.5 * np.sin(x_fill)
    axes[0].fill_between(x_fill, density_fill, alpha=0.6, color='orange')
    axes[0].axvline(3, color='red', linestyle='--', linewidth=2)
    axes[0].axvline(7, color='red', linestyle='--', linewidth=2)
    axes[0].text(5, 1, 'Khối lượng = ∫₃⁷ ρ(x)dx', 
                fontsize=12, ha='center', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Right: Probability density
    x_prob = np.linspace(-4, 4, 200)
    pdf = stats.norm.pdf(x_prob, 0, 1)
    
    axes[1].plot(x_prob, pdf, 'b-', linewidth=2.5)
    axes[1].fill_between(x_prob, pdf, alpha=0.3, color='lightblue')
    axes[1].set_xlabel('x', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('Mật độ xác suất f(x)', fontsize=13, fontweight='bold')
    axes[1].set_title('Mật độ Xác suất (Thống kê)\nf(x) KHÔNG PHẢI xác suất', 
                     fontsize=14, fontweight='bold')
    axes[1].grid(alpha=0.3)
    
    # Highlight region
    x_fill = x_prob[(x_prob >= -1) & (x_prob <= 1)]
    pdf_fill = stats.norm.pdf(x_fill, 0, 1)
    axes[1].fill_between(x_fill, pdf_fill, alpha=0.6, color='orange')
    axes[1].axvline(-1, color='red', linestyle='--', linewidth=2)
    axes[1].axvline(1, color='red', linestyle='--', linewidth=2)
    prob = stats.norm.cdf(1, 0, 1) - stats.norm.cdf(-1, 0, 1)
    axes[1].text(0, 0.15, f'Xác suất = ∫₋₁¹ f(x)dx\n= {prob:.3f}', 
                fontsize=12, ha='center', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    save_current_figure('density_analogy.png')
    split_figure_grid(
        'density_analogy.png',
        rows=1,
        cols=2,
        output_names=[
            'pdf_mass_density_analogy.png',
            'pdf_probability_density_analogy.png',
        ],
    )
    plt.close()


def generate_pdf_can_exceed_one():
    """3. PDF can be greater than 1"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Example 1: Normal with small sigma
    x1 = np.linspace(-2, 2, 200)
    pdf1 = stats.norm.pdf(x1, 0, 0.3)
    
    axes[0].plot(x1, pdf1, 'b-', linewidth=2.5)
    axes[0].fill_between(x1, pdf1, alpha=0.3, color='lightblue')
    axes[0].axhline(y=1, color='red', linestyle='--', linewidth=2.5, label='y = 1')
    axes[0].set_xlabel('x', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('f(x)', fontsize=12, fontweight='bold')
    axes[0].set_title(f'N(0, 0.3²)\nf(0) = {pdf1.max():.2f} > 1', 
                     fontsize=13, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(alpha=0.3)
    axes[0].text(0, pdf1.max()/2, f'f(x) > 1\nNHƯNG\n∫f(x)dx = 1 ✓', 
                ha='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6))
    
    # Example 2: Uniform on [0, 0.5]
    x2 = np.linspace(-0.5, 1, 400)
    pdf2 = np.where((x2 >= 0) & (x2 <= 0.5), 2, 0)
    
    axes[1].plot(x2, pdf2, 'b-', linewidth=2.5)
    axes[1].fill_between(x2, pdf2, alpha=0.3, color='lightblue')
    axes[1].axhline(y=1, color='red', linestyle='--', linewidth=2.5, label='y = 1')
    axes[1].set_xlabel('x', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('f(x)', fontsize=12, fontweight='bold')
    axes[1].set_title('Uniform[0, 0.5]\nf(x) = 2 > 1', 
                     fontsize=13, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(alpha=0.3)
    axes[1].set_ylim(-0.2, 2.5)
    axes[1].text(0.25, 1.5, f'f(x) = 2\nDiện tích = 2 × 0.5 = 1 ✓', 
                ha='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6))
    
    # Example 3: Beta with alpha, beta < 1
    x3 = np.linspace(0.001, 0.999, 200)
    pdf3 = stats.beta.pdf(x3, 0.5, 0.5)
    
    axes[2].plot(x3, pdf3, 'b-', linewidth=2.5)
    axes[2].fill_between(x3, pdf3, alpha=0.3, color='lightblue')
    axes[2].axhline(y=1, color='red', linestyle='--', linewidth=2.5, label='y = 1')
    axes[2].set_xlabel('x', fontsize=12, fontweight='bold')
    axes[2].set_ylabel('f(x)', fontsize=12, fontweight='bold')
    axes[2].set_title('Beta(0.5, 0.5)\nf(x) → ∞ tại x=0,1', 
                     fontsize=13, fontweight='bold')
    axes[2].legend(fontsize=10)
    axes[2].grid(alpha=0.3)
    axes[2].set_ylim(0, 5)
    axes[2].text(0.5, 2.5, 'f(x) CÓ THỂ > 1\nvì không phải xác suất!', 
                ha='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.6))
    
    plt.tight_layout()
    save_current_figure('pdf_can_exceed_one.png')
    split_figure_grid(
        'pdf_can_exceed_one.png',
        rows=1,
        cols=3,
        output_names=[
            'pdf_exceeds_one_normal.png',
            'pdf_exceeds_one_uniform.png',
            'pdf_exceeds_one_beta.png',
        ],
    )
    plt.close()


def generate_histogram_to_pdf():
    """4. Histogram converges to PDF as n increases"""
    np.random.seed(42)
    mu, sigma = 0, 1
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    axes = axes.flatten()
    
    sample_sizes = [100, 500, 1000, 5000, 10000, 50000]
    bin_counts = [10, 20, 30, 40, 50, 60]
    
    x_theory = np.linspace(-4, 4, 200)
    pdf_theory = stats.norm.pdf(x_theory, mu, sigma)
    
    for idx, (n, bins) in enumerate(zip(sample_sizes, bin_counts)):
        samples = np.random.normal(mu, sigma, n)
        
        axes[idx].hist(samples, bins=bins, density=True, alpha=0.6, 
                      color='steelblue', edgecolor='black', linewidth=1.5,
                      label=f'Histogram (n={n})')
        axes[idx].plot(x_theory, pdf_theory, 'r-', linewidth=3, 
                      label='PDF lý thuyết N(0,1)')
        axes[idx].set_xlabel('x', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Mật độ', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'n = {n:,}, bins = {bins}', 
                           fontsize=12, fontweight='bold')
        axes[idx].legend(fontsize=9)
        axes[idx].grid(alpha=0.3)
        axes[idx].set_xlim(-4, 4)
        axes[idx].set_ylim(0, 0.5)
    
    plt.suptitle('Histogram tiến đến PDF khi n → ∞', 
                fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    save_current_figure('histogram_to_pdf.png')
    split_figure_grid(
        'histogram_to_pdf.png',
        rows=2,
        cols=3,
        output_names=[
            'pdf_histogram_n100.png',
            'pdf_histogram_n500.png',
            'pdf_histogram_n1000.png',
            'pdf_histogram_n5000.png',
            'pdf_histogram_n10000.png',
            'pdf_histogram_n50000.png',
        ],
        trim_shared_header=True,
    )
    plt.close()


def generate_small_interval_approximation():
    """5. Probability in small intervals: P(x ≤ X ≤ x+Δx) ≈ f(x)·Δx"""
    mu, sigma = 0, 1
    x0 = 1.0
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    delta_xs = [0.5, 0.1, 0.01]
    
    for idx, dx in enumerate(delta_xs):
        x = np.linspace(-3, 3, 200)
        pdf = stats.norm.pdf(x, mu, sigma)
        
        axes[idx].plot(x, pdf, 'b-', linewidth=2.5, label='PDF: N(0,1)')
        
        # Fill area under curve
        x_fill = np.linspace(x0, x0 + dx, 100)
        pdf_fill = stats.norm.pdf(x_fill, mu, sigma)
        axes[idx].fill_between(x_fill, pdf_fill, alpha=0.5, color='orange',
                              label=f'∫ f(x)dx (xác suất thực)')
        
        # Rectangle approximation
        rect_height = stats.norm.pdf(x0, mu, sigma)
        rect = mpatches.Rectangle((x0, 0), dx, rect_height, 
                                  fill=False, edgecolor='green', 
                                  linewidth=3, linestyle='--')
        axes[idx].add_patch(rect)
        axes[idx].plot([x0, x0+dx], [rect_height, rect_height], 
                      'g--', linewidth=3, label=f'f({x0})·Δx (xấp xỉ)')
        
        # Calculate probabilities
        prob_exact = stats.norm.cdf(x0 + dx, mu, sigma) - stats.norm.cdf(x0, mu, sigma)
        prob_approx = rect_height * dx
        error = abs(prob_exact - prob_approx)
        
        axes[idx].set_xlabel('x', fontsize=12, fontweight='bold')
        axes[idx].set_ylabel('f(x)', fontsize=12, fontweight='bold')
        axes[idx].set_title(f'Δx = {dx}\n' + 
                           f'Thực: {prob_exact:.6f}\n' +
                           f'Xấp xỉ: {prob_approx:.6f}\n' +
                           f'Sai số: {error:.6f}', 
                           fontsize=11, fontweight='bold')
        axes[idx].legend(fontsize=9, loc='upper left')
        axes[idx].grid(alpha=0.3)
        axes[idx].set_xlim(-0.5, 2.5)
    
    plt.suptitle('P(x ≤ X ≤ x+Δx) ≈ f(x)·Δx\nXấp xỉ tốt khi Δx nhỏ', 
                fontsize=15, fontweight='bold')
    plt.tight_layout()
    save_current_figure('small_interval_approximation.png')
    split_figure_grid(
        'small_interval_approximation.png',
        rows=1,
        cols=3,
        output_names=[
            'pdf_small_interval_dx_05.png',
            'pdf_small_interval_dx_01.png',
            'pdf_small_interval_dx_001.png',
        ],
        trim_shared_header=True,
    )
    plt.close()


def generate_pdf_units():
    """6. Units of PDF: 1/(unit of X)"""
    mu_cm, sigma_cm = 170, 10  # cm
    mu_m, sigma_m = 1.70, 0.10  # m
    
    x_cm = np.linspace(140, 200, 200)
    pdf_cm = stats.norm.pdf(x_cm, mu_cm, sigma_cm)
    
    x_m = x_cm / 100
    pdf_m = stats.norm.pdf(x_m, mu_m, sigma_m)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Units: cm
    axes[0].plot(x_cm, pdf_cm, 'b-', linewidth=2.5)
    axes[0].fill_between(x_cm, pdf_cm, alpha=0.3, color='lightblue')
    axes[0].axvline(170, color='red', linestyle='--', linewidth=2)
    axes[0].set_xlabel('Chiều cao (cm)', fontsize=13, fontweight='bold')
    axes[0].set_ylabel('f(x) [đơn vị: 1/cm]', fontsize=13, fontweight='bold')
    f_170 = stats.norm.pdf(170, mu_cm, sigma_cm)
    axes[0].set_title(f'PDF với đơn vị cm\nf(170 cm) = {f_170:.4f} (1/cm)', 
                     fontsize=13, fontweight='bold')
    axes[0].grid(alpha=0.3)
    axes[0].scatter([170], [f_170], s=200, color='red', 
                   zorder=5, edgecolor='black', linewidth=2)
    
    # Units: m
    axes[1].plot(x_m, pdf_m, 'r-', linewidth=2.5)
    axes[1].fill_between(x_m, pdf_m, alpha=0.3, color='lightcoral')
    axes[1].axvline(1.70, color='blue', linestyle='--', linewidth=2)
    axes[1].set_xlabel('Chiều cao (m)', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('f(x) [đơn vị: 1/m]', fontsize=13, fontweight='bold')
    f_170m = stats.norm.pdf(1.70, mu_m, sigma_m)
    axes[1].set_title(f'PDF với đơn vị m\nf(1.70 m) = {f_170m:.4f} (1/m)', 
                     fontsize=13, fontweight='bold')
    axes[1].grid(alpha=0.3)
    axes[1].scatter([1.70], [f_170m], s=200, color='blue', 
                   zorder=5, edgecolor='black', linewidth=2)
    
    # Add note about conversion
    axes[1].text(0.5, 0.95, f'Chú ý: {f_170:.4f} × 100 = {f_170m:.4f}\n(vì 1/cm × 100 = 1/m)',
                transform=axes[1].transAxes, fontsize=11, fontweight='bold',
                verticalalignment='top', bbox=dict(boxstyle='round', 
                facecolor='yellow', alpha=0.6))
    
    plt.tight_layout()
    save_current_figure('pdf_units.png')
    split_figure_grid(
        'pdf_units.png',
        rows=1,
        cols=2,
        output_names=[
            'pdf_units_cm_only.png',
            'pdf_units_m_only.png',
        ],
    )
    plt.close()


def generate_pmf_pdf_comparison():
    """7. Direct comparison: PMF vs PDF"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # PMF - Discrete
    x_discrete = np.arange(0, 11)
    pmf = stats.binom.pmf(x_discrete, 10, 0.5)
    
    axes[0].bar(x_discrete, pmf, width=0.6, alpha=0.7, color='steelblue',
               edgecolor='black', linewidth=2)
    axes[0].set_xlabel('x', fontsize=13, fontweight='bold')
    axes[0].set_ylabel('P(X = x)', fontsize=13, fontweight='bold')
    axes[0].set_title('PMF: Binomial(10, 0.5)\nP(X=x) LÀ XÁC SUẤT\n0 ≤ P(X=x) ≤ 1', 
                     fontsize=13, fontweight='bold', color='darkblue')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Highlight one value
    axes[0].bar([5], [pmf[5]], width=0.6, color='red', alpha=0.7, 
               edgecolor='black', linewidth=2)
    axes[0].text(5, pmf[5] + 0.02, f'P(X=5) = {pmf[5]:.3f}\nÝ nghĩa trực tiếp!', 
                ha='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # PDF - Continuous
    x_continuous = np.linspace(-4, 4, 200)
    pdf = stats.norm.pdf(x_continuous, 0, 1)
    
    axes[1].plot(x_continuous, pdf, 'b-', linewidth=2.5)
    axes[1].fill_between(x_continuous, pdf, alpha=0.3, color='lightblue')
    axes[1].set_xlabel('x', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('f(x)', fontsize=13, fontweight='bold')
    axes[1].set_title('PDF: Normal(0, 1)\nf(x) KHÔNG PHẢI xác suất\nf(x) CÓ THỂ > 1', 
                     fontsize=13, fontweight='bold', color='darkred')
    axes[1].grid(alpha=0.3)
    
    # Highlight one point
    x_point = 0
    f_point = stats.norm.pdf(x_point, 0, 1)
    axes[1].scatter([x_point], [f_point], s=300, color='red', 
                   zorder=5, edgecolor='black', linewidth=2)
    axes[1].text(x_point + 0.8, f_point, 
                f'f(0) = {f_point:.3f}\nNHƯNG P(X=0) = 0!', 
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    save_current_figure('pmf_pdf_comparison.png')
    split_figure_grid(
        'pmf_pdf_comparison.png',
        rows=1,
        cols=2,
        output_names=[
            'pdf_binomial_pmf_example.png',
            'pdf_normal_density_example.png',
        ],
    )
    plt.close()


def generate_bayesian_pdf_application():
    """8. PDF in Bayesian statistics: Prior and Posterior"""
    theta = np.linspace(0, 1, 200)
    prior = stats.beta.pdf(theta, 2, 2)
    posterior = stats.beta.pdf(theta, 9, 5)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Prior vs Posterior
    axes[0].plot(theta, prior, 'b-', linewidth=3, label='Prior: Beta(2, 2)', alpha=0.7)
    axes[0].fill_between(theta, prior, alpha=0.2, color='blue')
    axes[0].plot(theta, posterior, 'r-', linewidth=3, label='Posterior: Beta(9, 5)')
    axes[0].fill_between(theta, posterior, alpha=0.3, color='red')
    axes[0].set_xlabel('θ (xác suất thành công)', fontsize=13, fontweight='bold')
    axes[0].set_ylabel('f(θ)', fontsize=13, fontweight='bold')
    axes[0].set_title('Prior và Posterior là PDF\nf(θ) là MẬT ĐỘ tin cậy (không phải xác suất)', 
                     fontsize=13, fontweight='bold')
    axes[0].legend(fontsize=12, loc='upper left')
    axes[0].grid(alpha=0.3)
    axes[0].text(0.5, 2.2, 'Data: 7 thành công / 10 thử',
                ha='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Right: Credible Interval
    axes[1].plot(theta, posterior, 'r-', linewidth=3, label='Posterior PDF')
    axes[1].fill_between(theta, posterior, alpha=0.3, color='red')
    
    # 95% Credible Interval
    lower = stats.beta.ppf(0.025, 9, 5)
    upper = stats.beta.ppf(0.975, 9, 5)
    theta_ci = theta[(theta >= lower) & (theta <= upper)]
    posterior_ci = stats.beta.pdf(theta_ci, 9, 5)
    axes[1].fill_between(theta_ci, posterior_ci, alpha=0.6, color='green',
                        label=f'95% CI: [{lower:.3f}, {upper:.3f}]')
    axes[1].axvline(lower, color='green', linestyle='--', linewidth=2)
    axes[1].axvline(upper, color='green', linestyle='--', linewidth=2)
    
    # Mark mean
    mean_post = 9/(9+5)
    axes[1].axvline(mean_post, color='darkred', linestyle='-', linewidth=2.5,
                   label=f'Mean: {mean_post:.3f}')
    
    axes[1].set_xlabel('θ', fontsize=13, fontweight='bold')
    axes[1].set_ylabel('f(θ)', fontsize=13, fontweight='bold')
    axes[1].set_title('Khoảng Tin cậy từ Posterior PDF\nP(0.395 ≤ θ ≤ 0.827) = 0.95', 
                     fontsize=13, fontweight='bold')
    axes[1].legend(fontsize=11, loc='upper left')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    save_current_figure('bayesian_pdf_application.png')
    split_figure_grid(
        'bayesian_pdf_application.png',
        rows=1,
        cols=2,
        output_names=[
            'pdf_bayesian_prior_posterior.png',
            'pdf_bayesian_credible_interval.png',
        ],
    )
    plt.close()


def generate_summary_infographic():
    """9. Summary infographic of key PDF concepts"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')
    
    summary_text = """
HÀM MẬT ĐỘ XÁC SUẤT (PDF) - TÓM TẮT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ĐỊNH NGHĨA QUAN TRỌNG NHẤT
   • f(x) là MẬT ĐỘ xác suất, KHÔNG PHẢI xác suất
   • Chỉ có TÍCH PHÂN của f(x) mới là xác suất:
     P(a ≤ X ≤ b) = ∫ₐᵇ f(x)dx

2. TÍNH CHẤT CƠ BẢN
   ✓ f(x) ≥ 0 với mọi x (không âm)
   ✓ ∫₋∞^∞ f(x)dx = 1 (tổng diện tích = 1)
   ✓ f(x) CÓ THỂ > 1 (vì không phải xác suất!)
   ✓ P(X = x) = 0 với mọi x (biến liên tục)

3. Ý NGHĨA CỦA MẬT ĐỘ
   • f(x) đo "độ tập trung" xác suất tại x
   • f(x) cao → xác suất tập trung quanh x
   • f(x) thấp → xác suất thưa thớt quanh x
   • Với khoảng nhỏ: P(x ≤ X ≤ x+Δx) ≈ f(x)·Δx

4. ĐƠN VỊ QUAN TRỌNG
   • Nếu X có đơn vị U → f(x) có đơn vị 1/U
   • f(x)·dx không có đơn vị (là xác suất)
   • Ví dụ: Chiều cao (cm) → f(x) có đơn vị (1/cm)

5. SO SÁNH PMF vs PDF
   ┌─────────────────┬────────────────┬───────────────┐
   │   Đặc điểm      │  PMF (Rời rạc) │ PDF (Liên tục)│
   ├─────────────────┼────────────────┼───────────────┤
   │ Ký hiệu         │ P(X = x)       │ f(x)          │
   │ Ý nghĩa         │ Xác suất       │ Mật độ        │
   │ Giá trị         │ 0 ≤ P ≤ 1      │ f ≥ 0 (có thể >1)│
   │ P(X = x)        │ Có nghĩa       │ = 0           │
   │ Tổng            │ Σ P(x) = 1     │ ∫ f(x)dx = 1  │
   └─────────────────┴────────────────┴───────────────┘

6. 3 SAI LẦM THƯỜNG GẶP
   ❌ "f(x) là xác suất" → SAI!
   ❌ "f(x) phải ≤ 1" → SAI!
   ❌ "P(X = x) = f(x)" → SAI!

7. TRONG BAYESIAN STATISTICS
   • Prior p(θ) là PDF (mật độ tin cậy ban đầu)
   • Posterior p(θ|x) là PDF (mật độ tin cậy sau data)
   • Likelihood L(θ) tỷ lệ với PDF
   • Credible Interval = tích phân Posterior PDF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NHỚ: f(x) giống như "mật độ khối lượng" trong vật lý
     Không phải khối lượng, nhưng tích phân nó ra khối lượng!
"""
    
    ax.text(0.5, 0.5, summary_text, fontsize=11.5, family='monospace',
           ha='center', va='center', linespacing=1.8,
           bbox=dict(boxstyle='round,pad=1.5', facecolor='lightblue', 
                    alpha=0.4, edgecolor='darkblue', linewidth=3))
    
    plt.tight_layout()
    save_current_figure('pdf_summary_infographic.png')
    plt.close()


def main():
    """Generate all illustrations"""
    print("=" * 60)
    print("Generating PDF Concept Illustrations")
    print("=" * 60)
    
    generate_pmf_vs_continuous()
    generate_density_analogy()
    generate_pdf_can_exceed_one()
    generate_histogram_to_pdf()
    generate_small_interval_approximation()
    generate_pdf_units()
    generate_pmf_pdf_comparison()
    generate_bayesian_pdf_application()
    generate_summary_infographic()
    
    print("=" * 60)
    print("✓ All illustrations generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
