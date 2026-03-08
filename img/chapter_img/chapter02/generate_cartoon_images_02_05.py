"""
Generate cartoon-style images for Bài 2.5: Conjugate Priors
Enhanced version with storytelling about The Conjugate Pairs
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Polygon
import numpy as np
import os

# Create output directory
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

def create_conjugate_pairs_intro(output_dir):
    """Image 1: The Conjugate Pairs Matching Game"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'The Conjugate Pairs: Trò Chơi Ghép Đôi', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Dr. Alex
    alex_head = Circle((2, 8), 0.3, facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(alex_head)
    ax.plot(1.9, 8.05, 'ko', markersize=4)
    ax.plot(2.1, 8.05, 'ko', markersize=4)
    smile = patches.Arc((2, 7.95), 0.2, 0.15, angle=0, theta1=200, theta2=340, 
                       color='black', linewidth=2)
    ax.add_patch(smile)
    ax.text(2, 7.4, 'Dr. Alex', fontsize=11, ha='center', fontweight='bold')
    
    # Speech bubble
    bubble = FancyBboxPatch((0.3, 8.5), 2.5, 0.8, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='white', linewidth=2)
    ax.add_patch(bubble)
    ax.text(1.55, 8.9, '"Tìm cặp đôi hoàn hảo!"', fontsize=10, ha='center', fontweight='bold')
    
    # Three perfect couples
    couples = [
        {
            'y': 6,
            'prior': 'BETA',
            'like': 'BINOMIAL',
            'post': 'BETA',
            'color': 'lightblue',
            'param': 'θ ∈ [0,1]',
            'app': 'Xác suất'
        },
        {
            'y': 4,
            'prior': 'NORMAL',
            'like': 'NORMAL',
            'post': 'NORMAL',
            'color': 'lightgreen',
            'param': 'μ ∈ ℝ',
            'app': 'Mean'
        },
        {
            'y': 2,
            'prior': 'GAMMA',
            'like': 'POISSON',
            'post': 'GAMMA',
            'color': 'lightyellow',
            'param': 'λ > 0',
            'app': 'Count'
        }
    ]
    
    for couple in couples:
        y = couple['y']
        
        # Prior box
        prior_box = FancyBboxPatch((1, y-0.4), 1.5, 0.8, boxstyle="round,pad=0.05",
                                   edgecolor='black', facecolor=couple['color'], linewidth=2)
        ax.add_patch(prior_box)
        ax.text(1.75, y, couple['prior'], fontsize=11, ha='center', fontweight='bold')
        
        # + symbol
        ax.text(2.7, y, '+', fontsize=16, ha='center', fontweight='bold')
        
        # Likelihood box
        like_box = FancyBboxPatch((3, y-0.4), 1.5, 0.8, boxstyle="round,pad=0.05",
                                  edgecolor='black', facecolor=couple['color'], linewidth=2)
        ax.add_patch(like_box)
        ax.text(3.75, y, couple['like'], fontsize=11, ha='center', fontweight='bold')
        
        # Arrow
        arrow = FancyArrowPatch((4.6, y), (5.4, y), 
                               arrowstyle='->', mutation_scale=20, 
                               linewidth=3, color='purple')
        ax.add_patch(arrow)
        
        # Posterior box
        post_box = FancyBboxPatch((5.5, y-0.4), 1.5, 0.8, boxstyle="round,pad=0.05",
                                  edgecolor='purple', facecolor=couple['color'], linewidth=3)
        ax.add_patch(post_box)
        ax.text(6.25, y, couple['post'], fontsize=11, ha='center', fontweight='bold', color='purple')
        
        # Info
        ax.text(8, y+0.2, couple['param'], fontsize=9, ha='center')
        ax.text(8, y-0.2, couple['app'], fontsize=9, ha='center', style='italic')
        
        # Heart symbol
        ax.text(6.25, y+0.6, '❤', fontsize=15, ha='center', color='red')
    
    # Key insight
    insight_box = FancyBboxPatch((0.5, 0.3), 9, 1, boxstyle="round,pad=0.1",
                                 edgecolor='gold', facecolor='lightyellow', linewidth=3)
    ax.add_patch(insight_box)
    ax.text(5, 1.1, '💡 CONJUGATE PAIR: Prior + Likelihood cùng họ → Posterior cùng họ!', 
            fontsize=12, ha='center', fontweight='bold')
    ax.text(5, 0.7, '→ Có CÔNG THỨC ĐÓNG - không cần MCMC!', 
            fontsize=11, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'conjugate_pairs_intro.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: conjugate_pairs_intro.png")

def create_beta_binomial_conjugacy_visual(output_dir):
    """Image 2: Beta-Binomial Conjugacy Visual"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Beta-Binomial Conjugacy: The Perfect Couple', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Flow diagram
    # Prior
    prior_box = FancyBboxPatch((0.5, 7), 2, 1.5, boxstyle="round,pad=0.1",
                               edgecolor='blue', facecolor='lightblue', linewidth=3)
    ax.add_patch(prior_box)
    ax.text(1.5, 7.9, 'PRIOR', fontsize=13, ha='center', fontweight='bold')
    ax.text(1.5, 7.5, 'Beta(α, β)', fontsize=11, ha='center')
    ax.text(1.5, 7.2, '"Pseudo-counts"', fontsize=9, ha='center', style='italic')
    
    # Likelihood
    like_box = FancyBboxPatch((3.5, 7), 2, 1.5, boxstyle="round,pad=0.1",
                              edgecolor='green', facecolor='lightgreen', linewidth=3)
    ax.add_patch(like_box)
    ax.text(4.5, 7.9, 'LIKELIHOOD', fontsize=13, ha='center', fontweight='bold')
    ax.text(4.5, 7.5, 'Binomial(n, θ)', fontsize=11, ha='center')
    ax.text(4.5, 7.2, 'k successes', fontsize=9, ha='center', style='italic')
    
    # Arrow down
    arrow1 = FancyArrowPatch((1.5, 7), (1.5, 6), 
                            arrowstyle='->', mutation_scale=25, 
                            linewidth=3, color='blue')
    ax.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((4.5, 7), (4.5, 6), 
                            arrowstyle='->', mutation_scale=25, 
                            linewidth=3, color='green')
    ax.add_patch(arrow2)
    
    # Magic box
    magic_box = FancyBboxPatch((1, 4.5), 4, 1.3, boxstyle="round,pad=0.1",
                               edgecolor='purple', facecolor='plum', linewidth=3)
    ax.add_patch(magic_box)
    ax.text(3, 5.5, '✨ CONJUGACY MAGIC ✨', fontsize=13, ha='center', fontweight='bold')
    ax.text(3, 5.1, 'α + k, β + (n-k)', fontsize=11, ha='center')
    ax.text(3, 4.8, 'Just ADD counts!', fontsize=10, ha='center', style='italic')
    
    # Arrow down
    arrow3 = FancyArrowPatch((3, 4.5), (3, 3.5), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=4, color='purple')
    ax.add_patch(arrow3)
    
    # Posterior
    post_box = FancyBboxPatch((1.5, 2), 3, 1.3, boxstyle="round,pad=0.15",
                              edgecolor='purple', facecolor='plum', linewidth=3)
    ax.add_patch(post_box)
    ax.text(3, 3, 'POSTERIOR', fontsize=14, ha='center', fontweight='bold', color='purple')
    ax.text(3, 2.6, 'Beta(α+k, β+n-k)', fontsize=12, ha='center')
    ax.text(3, 2.3, 'CÙNG HỌ với Prior!', fontsize=10, ha='center', fontweight='bold')
    
    # Interpretation
    interp_box = FancyBboxPatch((6, 5), 3.5, 4, boxstyle="round,pad=0.15",
                                edgecolor='black', facecolor='lightyellow', linewidth=2)
    ax.add_patch(interp_box)
    ax.text(7.75, 8.7, 'DIỄN GIẢI', fontsize=13, ha='center', fontweight='bold')
    ax.text(7.75, 8.3, '─────────────', fontsize=10, ha='center')
    ax.text(7.75, 7.9, 'α: thành công "giả"', fontsize=10, ha='center')
    ax.text(7.75, 7.5, 'β: thất bại "giả"', fontsize=10, ha='center')
    ax.text(7.75, 7.1, 'k: thành công THỰC', fontsize=10, ha='center')
    ax.text(7.75, 6.7, 'n-k: thất bại THỰC', fontsize=10, ha='center')
    ax.text(7.75, 6.2, '─────────────', fontsize=10, ha='center')
    ax.text(7.75, 5.8, 'Posterior = Prior + Data', fontsize=10, ha='center', fontweight='bold')
    ax.text(7.75, 5.4, '(Cộng số đếm!)', fontsize=9, ha='center', style='italic')
    
    # Example
    ex_box = FancyBboxPatch((0.5, 0.3), 9, 1.3, boxstyle="round,pad=0.1",
                            edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(ex_box)
    ax.text(5, 1.4, 'VÍ DỤ: Prior Beta(2,2) + Data 35/50 → Posterior Beta(37,17)', 
            fontsize=11, ha='center', fontweight='bold')
    ax.text(5, 1, '2 + 35 = 37 thành công | 2 + 15 = 17 thất bại', 
            fontsize=10, ha='center')
    ax.text(5, 0.6, '→ Không cần MCMC! Chỉ cần CỘNG!', 
            fontsize=10, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'beta_binomial_conjugacy_visual.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: beta_binomial_conjugacy_visual.png")

def create_conjugate_pairs_table(output_dir):
    """Image 3: Complete Table of Conjugate Pairs"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Bảng Tổng hợp Các Cặp Conjugate', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Table
    table_data = [
        ['#', 'PRIOR', 'LIKELIHOOD', 'POSTERIOR', 'PARAM', 'ỨNG DỤNG'],
        ['1', 'Beta', 'Binomial', 'Beta', 'θ∈[0,1]', 'Tỷ lệ, A/B test'],
        ['2', 'Normal', 'Normal', 'Normal', 'μ∈ℝ', 'Chiều cao, temp'],
        ['3', 'Gamma', 'Poisson', 'Gamma', 'λ>0', 'Count, lỗi'],
        ['4', 'Gamma', 'Exponential', 'Gamma', 'λ>0', 'Thời gian chờ'],
        ['5', 'Inv-Gamma', 'Normal', 'Inv-Gamma', 'σ²>0', 'Variance'],
        ['6', 'Dirichlet', 'Multinomial', 'Dirichlet', 'θ vector', 'Topic model']
    ]
    
    colors = ['lightgray'] + ['lightblue', 'lightgreen', 'lightyellow', 
                              'lightcoral', 'plum', 'lightcyan']
    
    y_start = 8.5
    row_height = 0.8
    col_widths = [0.5, 1.5, 1.8, 1.5, 1.3, 2]
    x_start = 0.8
    
    for i, row in enumerate(table_data):
        x = x_start
        for j, (cell, width) in enumerate(zip(row, col_widths)):
            # Cell box
            box = Rectangle((x, y_start - i*row_height), width, row_height,
                          edgecolor='black', facecolor=colors[i], linewidth=1)
            ax.add_patch(box)
            
            # Text
            fontsize = 10 if i == 0 else 9
            fontweight = 'bold' if i == 0 else 'normal'
            ax.text(x + width/2, y_start - i*row_height + row_height/2, 
                   cell, fontsize=fontsize, ha='center', va='center', fontweight=fontweight)
            
            x += width
    
    # Highlight top 3
    star_y = [y_start - 1*row_height + row_height/2,
              y_start - 2*row_height + row_height/2,
              y_start - 3*row_height + row_height/2]
    
    for y in star_y:
        ax.text(0.4, y, '⭐', fontsize=15, ha='center', va='center')
    
    # Note
    note_box = FancyBboxPatch((0.5, 0.5), 9, 1.5, boxstyle="round,pad=0.15",
                              edgecolor='gold', facecolor='lightyellow', linewidth=2)
    ax.add_patch(note_box)
    ax.text(5, 1.7, '⭐ TOP 3 QUAN TRỌNG NHẤT', 
            fontsize=13, ha='center', fontweight='bold')
    ax.text(5, 1.3, '1. Beta-Binomial: Xác suất, tỷ lệ (A/B testing)', 
            fontsize=10, ha='center')
    ax.text(5, 1, '2. Normal-Normal: Mean (chiều cao, nhiệt độ)', 
            fontsize=10, ha='center')
    ax.text(5, 0.7, '3. Gamma-Poisson: Count data (số lỗi, traffic)', 
            fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'conjugate_pairs_table.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: conjugate_pairs_table.png")

def create_why_conjugacy_convenient(output_dir):
    """Image 4: Why Conjugacy is Convenient"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Tại sao Conjugacy Tiện lợi?', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Two paths: Conjugate vs MCMC
    # Left: Conjugate (easy)
    easy_box = FancyBboxPatch((0.3, 4), 4.5, 5, boxstyle="round,pad=0.15",
                              edgecolor='green', facecolor='honeydew', linewidth=3)
    ax.add_patch(easy_box)
    
    ax.text(2.55, 8.7, 'CONJUGATE PRIOR', fontsize=14, ha='center', fontweight='bold', color='green')
    ax.text(2.55, 8.3, '✨ DỄ DÀNG ✨', fontsize=12, ha='center')
    
    benefits = [
        ('✅', 'Công thức ĐÓNG', 'Analytical solution'),
        ('⚡', 'Nhanh', '~milliseconds'),
        ('🎯', 'Chính xác', '100% exact'),
        ('🔄', 'Sequential easy', 'Chỉ cần cộng'),
        ('📖', 'Dễ hiểu', 'Intuitive')
    ]
    
    y = 7.5
    for emoji, title, desc in benefits:
        ax.text(2.55, y, f'{emoji} {title}', fontsize=11, ha='center', fontweight='bold')
        ax.text(2.55, y-0.3, desc, fontsize=9, ha='center', style='italic')
        y -= 0.9
    
    # Right: MCMC (hard)
    hard_box = FancyBboxPatch((5.2, 4), 4.5, 5, boxstyle="round,pad=0.15",
                              edgecolor='red', facecolor='mistyrose', linewidth=3)
    ax.add_patch(hard_box)
    
    ax.text(7.45, 8.7, 'MCMC (NON-CONJUGATE)', fontsize=14, ha='center', fontweight='bold', color='red')
    ax.text(7.45, 8.3, '⚠️ PHỨC TẠP ⚠️', fontsize=12, ha='center')
    
    drawbacks = [
        ('❌', 'Không có công thức', 'Numerical only'),
        ('🐌', 'Chậm', '~seconds/minutes'),
        ('~', 'Xấp xỉ', 'Approximation'),
        ('🔄', 'Sequential hard', 'Phải chạy lại'),
        ('🤔', 'Khó debug', 'Convergence?')
    ]
    
    y = 7.5
    for emoji, title, desc in drawbacks:
        ax.text(7.45, y, f'{emoji} {title}', fontsize=11, ha='center', fontweight='bold')
        ax.text(7.45, y-0.3, desc, fontsize=9, ha='center', style='italic')
        y -= 0.9
    
    # BUT note
    but_box = FancyBboxPatch((5.2, 4.3), 4.5, 0.8, boxstyle="round,pad=0.05",
                             edgecolor='orange', facecolor='gold', linewidth=2, alpha=0.7)
    ax.add_patch(but_box)
    ax.text(7.45, 4.7, '🌟 NHƯNG: Rất linh hoạt!', fontsize=10, ha='center', fontweight='bold')
    
    # Decision
    decision_box = FancyBboxPatch((0.5, 0.5), 9, 3, boxstyle="round,pad=0.15",
                                  edgecolor='purple', facecolor='lavender', linewidth=2)
    ax.add_patch(decision_box)
    
    ax.text(5, 3.2, '🎯 KHI NÀO DÙNG CÁI NÀO?', fontsize=14, ha='center', fontweight='bold')
    
    ax.text(2.5, 2.6, '✅ CONJUGATE', fontsize=12, ha='center', fontweight='bold', color='green')
    ax.text(2.5, 2.2, '• Model đơn giản', fontsize=9, ha='center')
    ax.text(2.5, 1.9, '• Prior standard', fontsize=9, ha='center')
    ax.text(2.5, 1.6, '• Cần nhanh', fontsize=9, ha='center')
    ax.text(2.5, 1.3, '• Giảng dạy', fontsize=9, ha='center')
    ax.text(2.5, 1, '• Real-time', fontsize=9, ha='center')
    ax.text(2.5, 0.7, '(Beta, Normal, Gamma)', fontsize=8, ha='center', style='italic')
    
    ax.text(7.5, 2.6, '✅ MCMC', fontsize=12, ha='center', fontweight='bold', color='red')
    ax.text(7.5, 2.2, '• Model phức tạp', fontsize=9, ha='center')
    ax.text(7.5, 1.9, '• Prior phức tạp', fontsize=9, ha='center')
    ax.text(7.5, 1.6, '• Likelihood không std', fontsize=9, ha='center')
    ax.text(7.5, 1.3, '• Hierarchical', fontsize=9, ha='center')
    ax.text(7.5, 1, '• Modern practice', fontsize=9, ha='center')
    ax.text(7.5, 0.7, '(Logistic, Neural Net)', fontsize=8, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'why_conjugacy_convenient.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: why_conjugacy_convenient.png")

def create_when_to_use_conjugate_priors(output_dir):
    """Image 5: Decision Tree - When to Use Conjugate Priors"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Decision Tree: Conjugate hay MCMC?', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Start
    start_box = FancyBboxPatch((3.5, 8), 3, 0.8, boxstyle="round,pad=0.1",
                               edgecolor='black', facecolor='lightgray', linewidth=2)
    ax.add_patch(start_box)
    ax.text(5, 8.4, 'Prior đơn giản?', fontsize=12, ha='center', fontweight='bold')
    
    # Branch 1
    arrow1a = FancyArrowPatch((4, 8), (2, 7), 
                             arrowstyle='->', mutation_scale=20, 
                             linewidth=2, color='green')
    ax.add_patch(arrow1a)
    ax.text(3, 7.7, 'YES', fontsize=10, ha='center', color='green', fontweight='bold')
    
    arrow1b = FancyArrowPatch((6, 8), (8, 7), 
                             arrowstyle='->', mutation_scale=20, 
                             linewidth=2, color='red')
    ax.add_patch(arrow1b)
    ax.text(7, 7.7, 'NO', fontsize=10, ha='center', color='red', fontweight='bold')
    
    # Level 2 - YES path
    box2a = FancyBboxPatch((0.5, 6), 3, 0.8, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='lightgreen', linewidth=2)
    ax.add_patch(box2a)
    ax.text(2, 6.4, 'Likelihood đơn giản?', fontsize=11, ha='center', fontweight='bold')
    
    # Level 2 - NO path
    mcmc_box1 = FancyBboxPatch((7, 6), 2, 0.8, boxstyle="round,pad=0.1",
                               edgecolor='red', facecolor='mistyrose', linewidth=2)
    ax.add_patch(mcmc_box1)
    ax.text(8, 6.4, '→ MCMC', fontsize=11, ha='center', fontweight='bold', color='red')
    
    # Branch 2
    arrow2a = FancyArrowPatch((1.2, 6), (1, 5), 
                             arrowstyle='->', mutation_scale=20, 
                             linewidth=2, color='green')
    ax.add_patch(arrow2a)
    ax.text(0.5, 5.7, 'YES', fontsize=10, ha='center', color='green', fontweight='bold')
    
    arrow2b = FancyArrowPatch((2.8, 6), (4, 5), 
                             arrowstyle='->', mutation_scale=20, 
                             linewidth=2, color='red')
    ax.add_patch(arrow2b)
    ax.text(3.4, 5.7, 'NO', fontsize=10, ha='center', color='red', fontweight='bold')
    
    # Level 3 - YES path
    box3a = FancyBboxPatch((0, 3.5), 2, 1.3, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='lightgreen', linewidth=2)
    ax.add_patch(box3a)
    ax.text(1, 4.4, 'Có conjugate?', fontsize=11, ha='center', fontweight='bold')
    ax.text(1, 4.1, '(Beta, Normal,', fontsize=9, ha='center')
    ax.text(1, 3.8, 'Gamma...)', fontsize=9, ha='center')
    
    # Level 3 - NO path
    mcmc_box2 = FancyBboxPatch((3, 4), 2, 0.8, boxstyle="round,pad=0.1",
                               edgecolor='red', facecolor='mistyrose', linewidth=2)
    ax.add_patch(mcmc_box2)
    ax.text(4, 4.4, '→ MCMC', fontsize=11, ha='center', fontweight='bold', color='red')
    
    # Branch 3
    arrow3a = FancyArrowPatch((1, 3.5), (1, 2.5), 
                             arrowstyle='->', mutation_scale=20, 
                             linewidth=2, color='green')
    ax.add_patch(arrow3a)
    ax.text(0.5, 3.2, 'YES', fontsize=10, ha='center', color='green', fontweight='bold')
    
    arrow3b = FancyArrowPatch((2, 3.9), (3, 3), 
                             arrowstyle='->', mutation_scale=20, 
                             linewidth=2, color='red')
    ax.add_patch(arrow3b)
    ax.text(2.5, 3.7, 'NO', fontsize=10, ha='center', color='red', fontweight='bold')
    
    # Final - CONJUGATE
    final_box = FancyBboxPatch((0, 0.8), 2, 1.5, boxstyle="round,pad=0.15",
                               edgecolor='green', facecolor='lightgreen', linewidth=3)
    ax.add_patch(final_box)
    ax.text(1, 2, '✅ CONJUGATE!', fontsize=13, ha='center', fontweight='bold', color='green')
    ax.text(1, 1.6, '• Nhanh', fontsize=9, ha='center')
    ax.text(1, 1.4, '• Chính xác', fontsize=9, ha='center')
    ax.text(1, 1.2, '• Dễ hiểu', fontsize=9, ha='center')
    ax.text(1, 1, '• Analytical', fontsize=9, ha='center')
    
    # Final - MCMC path
    mcmc_box3 = FancyBboxPatch((2.5, 2), 2, 0.8, boxstyle="round,pad=0.1",
                               edgecolor='red', facecolor='mistyrose', linewidth=2)
    ax.add_patch(mcmc_box3)
    ax.text(3.5, 2.4, '→ MCMC', fontsize=11, ha='center', fontweight='bold', color='red')
    
    # Examples
    ex_box = FancyBboxPatch((5.5, 0.5), 4, 4.5, boxstyle="round,pad=0.15",
                            edgecolor='blue', facecolor='lightcyan', linewidth=2)
    ax.add_patch(ex_box)
    
    ax.text(7.5, 4.7, 'VÍ DỤ CỤ THỂ', fontsize=13, ha='center', fontweight='bold')
    
    ax.text(7.5, 4.2, '✅ CONJUGATE:', fontsize=11, ha='left', fontweight='bold', color='green')
    ax.text(7.5, 3.8, '• A/B testing (Beta-Bin)', fontsize=9, ha='left')
    ax.text(7.5, 3.5, '• Chiều cao (Normal-Normal)', fontsize=9, ha='left')
    ax.text(7.5, 3.2, '• Count lỗi (Gamma-Poisson)', fontsize=9, ha='left')
    
    ax.text(7.5, 2.7, '❌ MCMC:', fontsize=11, ha='left', fontweight='bold', color='red')
    ax.text(7.5, 2.3, '• Logistic regression', fontsize=9, ha='left')
    ax.text(7.5, 2, '• Hierarchical model', fontsize=9, ha='left')
    ax.text(7.5, 1.7, '• Neural network', fontsize=9, ha='left')
    ax.text(7.5, 1.4, '• Prior phức tạp', fontsize=9, ha='left')
    ax.text(7.5, 1.1, '• Mixture model', fontsize=9, ha='left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'when_to_use_conjugate_priors.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: when_to_use_conjugate_priors.png")

def create_conjugacy_vs_mcmc(output_dir):
    """Image 6: Conjugacy vs MCMC - Head to Head Comparison"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Conjugacy vs MCMC: So sánh Trực tiếp', 
            fontsize=18, fontweight='bold', ha='center')
    
    # VS symbol
    vs_circle = Circle((5, 7.5), 0.6, facecolor='gold', edgecolor='black', linewidth=3)
    ax.add_patch(vs_circle)
    ax.text(5, 7.5, 'VS', fontsize=18, ha='center', fontweight='bold')
    
    # Left: Conjugate
    conj_box = FancyBboxPatch((0.3, 4), 4, 5, boxstyle="round,pad=0.15",
                              edgecolor='green', facecolor='honeydew', linewidth=3)
    ax.add_patch(conj_box)
    
    ax.text(2.3, 8.7, 'CONJUGATE', fontsize=15, ha='center', fontweight='bold', color='green')
    ax.text(2.3, 8.3, 'Analytical Solution', fontsize=11, ha='center', style='italic')
    
    # Right: MCMC
    mcmc_box = FancyBboxPatch((5.7, 4), 4, 5, boxstyle="round,pad=0.15",
                              edgecolor='red', facecolor='mistyrose', linewidth=3)
    ax.add_patch(mcmc_box)
    
    ax.text(7.7, 8.7, 'MCMC', fontsize=15, ha='center', fontweight='bold', color='red')
    ax.text(7.7, 8.3, 'Numerical Approximation', fontsize=11, ha='center', style='italic')
    
    # Comparison aspects
    aspects = [
        ('Công thức', '✅ CÓ (đóng)', '❌ KHÔNG CÓ', 7.7),
        ('Tốc độ', '⚡ ~ms', '🐌 ~sec/min', 7.2),
        ('Chính xác', '🎯 100%', '~ 99%', 6.7),
        ('Linh hoạt', '⚠️ Giới hạn', '✅ Rất cao', 6.2),
        ('Model', '📊 Đơn giản', '🏗️ Phức tạp OK', 5.7),
        ('Sequential', '✅ Dễ', '❌ Khó', 5.2),
        ('Debug', '✅ Dễ', '⚠️ Khó', 4.7),
        ('Learning', '📖 Dễ', '📚 Khó', 4.2)
    ]
    
    for aspect, conj, mcmc, y in aspects:
        # Aspect name
        ax.text(0.7, y, aspect, fontsize=10, ha='left', fontweight='bold')
        
        # Conjugate value
        ax.text(2.3, y, conj, fontsize=9, ha='center')
        
        # MCMC value
        ax.text(7.7, y, mcmc, fontsize=9, ha='center')
    
    # Verdict
    verdict_box = FancyBboxPatch((0.5, 0.5), 9, 3, boxstyle="round,pad=0.15",
                                 edgecolor='purple', facecolor='lavender', linewidth=3)
    ax.add_patch(verdict_box)
    
    ax.text(5, 3.2, '⚖️ VERDICT', fontsize=15, ha='center', fontweight='bold')
    
    ax.text(5, 2.6, 'CONJUGATE: Hoàn hảo cho model đơn giản', 
            fontsize=11, ha='center', fontweight='bold', color='green')
    ax.text(5, 2.3, '→ Nhanh, chính xác, dễ hiểu', 
            fontsize=10, ha='center')
    ax.text(5, 2, '→ Best for: A/B testing, simple inference, teaching', 
            fontsize=9, ha='center', style='italic')
    
    ax.text(5, 1.5, 'MCMC: Cần thiết cho model phức tạp', 
            fontsize=11, ha='center', fontweight='bold', color='red')
    ax.text(5, 1.2, '→ Linh hoạt, powerful, modern', 
            fontsize=10, ha='center')
    ax.text(5, 0.9, '→ Best for: Hierarchical, logistic, neural net, research', 
            fontsize=9, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'conjugacy_vs_mcmc.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: conjugacy_vs_mcmc.png")

def main():
    """Generate all cartoon images for Bài 2.5"""
    print("\n" + "="*70)
    print("GENERATING CARTOON IMAGES FOR BÀI 2.5: CONJUGATE PRIORS")
    print("="*70 + "\n")
    
    create_conjugate_pairs_intro(output_dir)
    create_beta_binomial_conjugacy_visual(output_dir)
    create_conjugate_pairs_table(output_dir)
    create_why_conjugacy_convenient(output_dir)
    create_when_to_use_conjugate_priors(output_dir)
    create_conjugacy_vs_mcmc(output_dir)
    
    print("\n" + "="*70)
    print("✅ ALL 6 CARTOON IMAGES GENERATED SUCCESSFULLY!")
    print("="*70)
    print(f"\nImages saved to: {output_dir}")
    print("\nList of generated images:")
    print("  1. conjugate_pairs_intro.png")
    print("  2. beta_binomial_conjugacy_visual.png")
    print("  3. conjugate_pairs_table.png")
    print("  4. why_conjugacy_convenient.png")
    print("  5. when_to_use_conjugate_priors.png")
    print("  6. conjugacy_vs_mcmc.png")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
