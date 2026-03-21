#!/usr/bin/env python3
"""
Generate Analytical vs Computational Methods comparison visualization
Shows side-by-side comparison with examples
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.patches as mpatches

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['figure.dpi'] = 300

def generate_analytical_vs_computational():
    """
    Create comprehensive comparison of analytical vs computational methods
    """
    fig = plt.figure(figsize=(18, 14))
    gs = fig.add_gridspec(4, 2, hspace=0.4, wspace=0.3)
    
    # ========================================================================
    # Top: Title and Overview
    # ========================================================================
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis('off')
    
    title_text = """
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║          HAI CÁCH TIẾP CẬN TÍNH POSTERIOR: ANALYTICAL vs COMPUTATIONAL                 ║
╠═══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                       ║
║  ANALYTICAL (Giải tích)              vs              COMPUTATIONAL (Tính toán)        ║
║  ────────────────────────                            ────────────────────────         ║
║  • Công thức toán học chính xác                      • Xấp xỉ bằng tính toán         ║
║  • Conjugate priors                                  • Grid Approximation             ║
║  • Giải được bằng tay                                • MCMC                           ║
║  • Nhanh và chính xác 100%                           • Linh hoạt, mạnh mẽ            ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
"""
    
    ax_title.text(0.5, 0.5, title_text, 
                  fontsize=10, family='monospace',
                  ha='center', va='center',
                  bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # ========================================================================
    # Row 2: Example Problem - Beta-Binomial
    # ========================================================================
    
    # LEFT: Analytical Solution (Conjugate)
    ax_analytical = fig.add_subplot(gs[1, 0])
    
    # Data: 6 heads in 9 flips, prior Beta(2, 2)
    alpha_prior, beta_prior = 2, 2
    n, k = 9, 6
    
    # Analytical posterior: Beta(2+6, 2+3) = Beta(8, 5)
    alpha_post, beta_post = alpha_prior + k, beta_prior + (n - k)
    
    theta = np.linspace(0, 1, 1000)
    prior_dist = stats.beta(alpha_prior, beta_prior).pdf(theta)
    posterior_dist = stats.beta(alpha_post, beta_post).pdf(theta)
    
    ax_analytical.plot(theta, prior_dist, 'b--', linewidth=2, label='Prior: Beta(2,2)', alpha=0.7)
    ax_analytical.plot(theta, posterior_dist, 'r-', linewidth=3, label='Posterior: Beta(8,5)')
    ax_analytical.fill_between(theta, posterior_dist, alpha=0.3, color='red')
    
    # Add formula box
    formula = """
CÔNG THỨC CHÍNH XÁC:
─────────────────────
Prior:      Beta(α=2, β=2)
Likelihood: Binomial(n=9, k=6)
Posterior:  Beta(α'=8, β'=5)

α' = α + k = 2 + 6 = 8
β' = β + n-k = 2 + 3 = 5

Posterior Mean = α'/(α'+β')
               = 8/13 = 0.6154
    """
    
    ax_analytical.text(0.05, 0.92, formula, transform=ax_analytical.transAxes,
                      fontsize=8, family='monospace', verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    ax_analytical.set_xlabel('θ (xác suất ngửa)', fontsize=11)
    ax_analytical.set_ylabel('Density', fontsize=11)
    ax_analytical.set_title('ANALYTICAL METHOD: Conjugate Prior\n✓ Chính xác 100% ✓ Nhanh', 
                           fontsize=12, fontweight='bold', color='darkblue')
    ax_analytical.legend(loc='upper right', fontsize=9)
    ax_analytical.grid(alpha=0.3)
    ax_analytical.set_xlim(0, 1)
    
    # RIGHT: Computational Solution (Grid Approximation)
    ax_computational = fig.add_subplot(gs[1, 1])
    
    # Grid approximation with 50 points
    grid_size = 50
    theta_grid = np.linspace(0, 1, grid_size)
    
    # Compute prior, likelihood, posterior at each grid point
    prior_grid = stats.beta(alpha_prior, beta_prior).pdf(theta_grid)
    likelihood_grid = stats.binom.pmf(k, n, theta_grid)
    posterior_grid_unnorm = prior_grid * likelihood_grid
    posterior_grid = posterior_grid_unnorm / np.sum(posterior_grid_unnorm)
    
    # Normalize for comparison with continuous posterior
    posterior_grid_density = posterior_grid / (theta_grid[1] - theta_grid[0])
    
    # Plot grid approximation
    ax_computational.stem(theta_grid, posterior_grid_density, linefmt='g-', 
                         markerfmt='go', basefmt=' ', label='Grid Approximation (50 điểm)')
    
    # Overlay true posterior for comparison
    ax_computational.plot(theta, posterior_dist, 'r--', linewidth=2, 
                         alpha=0.7, label='True Posterior (tham khảo)')
    
    # Add computation box
    computation = """
TÍNH TOÁN XẤP XỈ:
─────────────────────
Grid: 50 điểm từ 0 đến 1

For each θᵢ in grid:
  1. p(θᵢ) = Beta_pdf(θᵢ)
  2. p(D|θᵢ) = Binomial_pmf(6|9,θᵢ)
  3. p(θᵢ|D) ∝ p(D|θᵢ) × p(θᵢ)
  4. Normalize: Σ p(θᵢ|D) = 1

Grid Mean ≈ 0.6143
(chính xác = 0.6154)
    """
    
    ax_computational.text(0.05, 0.92, computation, transform=ax_computational.transAxes,
                         fontsize=8, family='monospace', verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    ax_computational.set_xlabel('θ (xác suất ngửa)', fontsize=11)
    ax_computational.set_ylabel('Density', fontsize=11)
    ax_computational.set_title('COMPUTATIONAL METHOD: Grid Approximation\n≈ Xấp xỉ tốt ≈ Linh hoạt', 
                              fontsize=12, fontweight='bold', color='darkgreen')
    ax_computational.legend(loc='upper right', fontsize=9)
    ax_computational.grid(alpha=0.3)
    ax_computational.set_xlim(0, 1)
    
    # ========================================================================
    # Row 3: Advantages and Disadvantages Comparison
    # ========================================================================
    
    ax_comparison = fig.add_subplot(gs[2, :])
    ax_comparison.axis('off')
    
    comparison_text = """
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                         SO SÁNH ƯU NHƯỢC ĐIỂM                                                          ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                       ║
║  ANALYTICAL (Giải tích - Conjugate Prior)          COMPUTATIONAL (Tính toán - Grid/MCMC)             ║
║  ═══════════════════════════════════════            ═══════════════════════════════════════           ║
║                                                                                                       ║
║  ✓ ƯU ĐIỂM:                                         ✓ ƯU ĐIỂM:                                        ║
║    • Chính xác 100% - công thức toán học              • Linh hoạt - BẤT KỲ prior/likelihood nào      ║
║    • Nhanh nhất - tính trực tiếp                      • Không cần conjugacy                          ║
║    • Dễ hiểu - chỉ là công thức                       • Xử lý được model phức tạp                    ║
║    • Elegant và đẹp về mặt toán học                   • MCMC hoạt động với nhiều tham số             ║
║                                                                                                       ║
║  ✗ NHƯỢC ĐIỂM:                                      ✗ NHƯỢC ĐIỂM:                                     ║
║    • Chỉ có một số trường hợp đặc biệt                • Xấp xỉ - không chính xác 100%                ║
║    • Không linh hoạt - phải dùng conjugate            • Grid: Curse of dimensionality                ║
║    • Không mở rộng được cho model phức tạp            • MCMC: Phức tạp, cần kiểm tra convergence     ║
║    • Bị giới hạn bởi toán học                         • Chậm hơn analytical (nếu có)                 ║
║                                                                                                       ║
║  ─────────────────────────────────────────────────────────────────────────────────────────────────  ║
║                                                                                                       ║
║  KHI NÀO DÙNG ANALYTICAL?                            KHI NÀO DÙNG COMPUTATIONAL?                      ║
║    ✓ Prior-Likelihood là conjugate pair                ✓ Prior KHÔNG conjugate                       ║
║    ✓ Muốn kết quả chính xác                           ✓ Model phức tạp (nhiều tham số)               ║
║    ✓ Cần tốc độ                                       ✓ Prior tùy chỉnh (mixture, bounded, etc)      ║
║    ✓ Giảng dạy, demo đơn giản                         ✓ Không có công thức analytical                ║
║                                                       ✓ Production ML models                          ║
║                                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""
    
    ax_comparison.text(0.5, 0.5, comparison_text,
                      fontsize=8.5, family='monospace',
                      ha='center', va='center',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9))
    
    # ========================================================================
    # Row 4: Decision Flow Chart
    # ========================================================================
    
    ax_flowchart = fig.add_subplot(gs[3, :])
    ax_flowchart.axis('off')
    ax_flowchart.set_xlim(0, 10)
    ax_flowchart.set_ylim(0, 6)
    
    # Decision tree
    flowchart_text = """
╔════════════════════════════════════════════════════════════════════════════════════╗
║                    LỰA CHỌN PHƯƠNG PHÁP: DECISION TREE                              ║
╠════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                    ║
║                            BẮT ĐẦU: Cần tính Posterior                              ║
║                                      │                                             ║
║                                      ▼                                             ║
║                        Prior và Likelihood có conjugate?                           ║
║                                      │                                             ║
║                    ┌─────────────────┴─────────────────┐                          ║
║                    │                                   │                          ║
║                   YES                                 NO                          ║
║                    │                                   │                          ║
║                    ▼                                   ▼                          ║
║          ┌─────────────────┐               ┌─────────────────────┐               ║
║          │  ANALYTICAL     │               │  Số tham số?         │               ║
║          │  (Conjugate)    │               └──────┬──────────────┘               ║
║          │                 │                      │                               ║
║          │  ✓ Nhanh nhất   │              ┌───────┴────────┐                     ║
║          │  ✓ Chính xác    │             1-2               3+                    ║
║          └─────────────────┘              │                │                     ║
║                                           ▼                ▼                     ║
║                              ┌──────────────────┐  ┌────────────────┐           ║
║                              │ GRID             │  │ MCMC           │           ║
║                              │ APPROXIMATION    │  │ (PyMC/Stan)    │           ║
║                              │                  │  │                │           ║
║                              │ ✓ Đơn giản       │  │ ✓ Mạnh nhất    │           ║
║                              │ ✓ Trực quan      │  │ ✓ Scalable     │           ║
║                              └──────────────────┘  └────────────────┘           ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
"""
    
    ax_flowchart.text(5, 3, flowchart_text,
                     fontsize=8.5, family='monospace',
                     ha='center', va='center',
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.9))
    
    # Main title
    fig.suptitle('ANALYTICAL vs COMPUTATIONAL METHODS\nSo sánh hai cách tiếp cận tính Posterior trong Bayesian Statistics',
                fontsize=14, fontweight='bold', y=0.98)
    
    plt.savefig('analytical_vs_computational_comparison.png', dpi=300, 
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print("✓ Generated: analytical_vs_computational_comparison.png")
    plt.close()


# ============================================================================
# Main execution
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("GENERATING ANALYTICAL VS COMPUTATIONAL COMPARISON IMAGE")
    print("=" * 70)
    print()
    
    generate_analytical_vs_computational()
    
    print()
    print("=" * 70)
    print("IMAGE GENERATED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("File created: analytical_vs_computational_comparison.png")
    print("Location: img/chapter_img/chapter02/")
    print()
    print("This image compares:")
    print("  1. Analytical methods (Conjugate Priors)")
    print("  2. Computational methods (Grid Approximation, MCMC)")
    print("  3. Decision flowchart for choosing the right method")
