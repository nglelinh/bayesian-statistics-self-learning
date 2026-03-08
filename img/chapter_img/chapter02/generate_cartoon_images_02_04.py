"""
Generate cartoon-style images for Bài 2.4: Posterior - Cập nhật Niềm tin với Dữ liệu
Enhanced version with storytelling about The Bayesian Update Machine
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Wedge
import numpy as np
import os

# Create output directory
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

def create_bayesian_update_machine_intro(output_dir):
    """Image 1: The Bayesian Update Machine - Introduction"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'The Bayesian Update Machine', 
            fontsize=22, fontweight='bold', ha='center')
    ax.text(5, 9, 'Cỗ Máy Kỳ diệu Cập nhật Niềm tin', 
            fontsize=14, ha='center', style='italic', color='gray')
    
    # The Machine (center)
    machine_box = FancyBboxPatch((2, 3.5), 6, 4, boxstyle="round,pad=0.2",
                                 edgecolor='black', facecolor='lightgray', linewidth=3)
    ax.add_patch(machine_box)
    
    ax.text(5, 7, 'BAYESIAN UPDATE MACHINE', 
            fontsize=16, ha='center', fontweight='bold')
    
    # Input 1: PRIOR (top left)
    prior_box = FancyBboxPatch((0.5, 6.5), 1.2, 0.8, boxstyle="round,pad=0.05",
                               edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax.add_patch(prior_box)
    ax.text(1.1, 6.9, 'PRIOR\nP(θ)', fontsize=10, ha='center', fontweight='bold', color='blue')
    
    arrow1 = FancyArrowPatch((1.7, 6.9), (2, 6.5), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='blue')
    ax.add_patch(arrow1)
    
    # Input 2: LIKELIHOOD (top right)
    likelihood_box = FancyBboxPatch((8.3, 6.5), 1.2, 0.8, boxstyle="round,pad=0.05",
                                    edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(likelihood_box)
    ax.text(8.9, 6.9, 'LIKELIHOOD\nP(D|θ)', fontsize=10, ha='center', fontweight='bold', color='green')
    
    arrow2 = FancyArrowPatch((8.3, 6.9), (8, 6.5), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='green')
    ax.add_patch(arrow2)
    
    # Machine internals
    ax.text(5, 6.2, '×', fontsize=40, ha='center', fontweight='bold')
    ax.text(5, 5.5, 'Prior × Likelihood', fontsize=12, ha='center', style='italic')
    
    ax.text(5, 4.8, '÷', fontsize=30, ha='center', fontweight='bold')
    ax.text(5, 4.3, 'Evidence (chuẩn hóa)', fontsize=11, ha='center', style='italic')
    
    # Magic sparkles
    ax.text(3.5, 5.8, '✨', fontsize=20)
    ax.text(6.5, 5.8, '✨', fontsize=20)
    ax.text(3.5, 4.5, '✨', fontsize=20)
    ax.text(6.5, 4.5, '✨', fontsize=20)
    
    # Output: POSTERIOR (bottom)
    arrow3 = FancyArrowPatch((5, 3.5), (5, 2.5), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=4, color='purple')
    ax.add_patch(arrow3)
    
    posterior_box = FancyBboxPatch((3.5, 1), 3, 1.2, boxstyle="round,pad=0.15",
                                   edgecolor='purple', facecolor='plum', linewidth=3)
    ax.add_patch(posterior_box)
    ax.text(5, 1.8, 'POSTERIOR', fontsize=14, ha='center', fontweight='bold', color='purple')
    ax.text(5, 1.4, 'P(θ|D)', fontsize=12, ha='center', fontweight='bold', color='purple')
    ax.text(5, 1.1, 'Niềm tin CẬP NHẬT', fontsize=10, ha='center', style='italic')
    
    # Dr. Emma (left side)
    emma_head = Circle((1.5, 2), 0.3, facecolor='peachpuff', edgecolor='black', linewidth=2)
    ax.add_patch(emma_head)
    emma_body = FancyBboxPatch((1.2, 0.8), 0.6, 1.2, boxstyle="round,pad=0.05",
                               edgecolor='black', facecolor='lightcoral', linewidth=2)
    ax.add_patch(emma_body)
    
    # Emma's eyes
    ax.plot(1.4, 2.05, 'ko', markersize=4)
    ax.plot(1.6, 2.05, 'ko', markersize=4)
    
    # Emma's smile
    smile = patches.Arc((1.5, 1.95), 0.2, 0.15, angle=0, theta1=200, theta2=340, 
                       color='black', linewidth=2)
    ax.add_patch(smile)
    
    ax.text(1.5, 0.5, 'Dr. Emma', fontsize=10, ha='center', fontweight='bold')
    
    # Emma's speech bubble
    bubble = FancyBboxPatch((0.2, 2.5), 2, 1, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='white', linewidth=2)
    ax.add_patch(bubble)
    ax.text(1.2, 3, '"Cỗ máy này sẽ giúp tôi', fontsize=9, ha='center')
    ax.text(1.2, 2.7, 'cập nhật niềm tin', fontsize=9, ha='center')
    
    # Formula box
    formula_box = FancyBboxPatch((0.5, 8), 9, 0.7, boxstyle="round,pad=0.1",
                                 edgecolor='gold', facecolor='lightyellow', linewidth=2)
    ax.add_patch(formula_box)
    ax.text(5, 8.35, 'Posterior = (Likelihood × Prior) / Evidence', 
            fontsize=12, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bayesian_update_machine_intro.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: bayesian_update_machine_intro.png")

def create_bayes_theorem_visual(output_dir):
    """Image 2: Bayes' Theorem Visual Breakdown"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Định lý Bayes: Phân tích Từng Thành phần', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Main formula (center)
    formula_box = FancyBboxPatch((1, 7), 8, 1.5, boxstyle="round,pad=0.15",
                                 edgecolor='black', facecolor='lightgray', linewidth=3)
    ax.add_patch(formula_box)
    ax.text(5, 8.2, 'P(θ | D) = ', fontsize=18, ha='center', fontweight='bold')
    ax.text(6.5, 8.2, 'P(D | θ) · P(θ)', fontsize=16, ha='center')
    ax.text(6.5, 7.6, 'P(D)', fontsize=16, ha='center')
    ax.plot([5.5, 7.5], [7.9, 7.9], 'k-', linewidth=2)
    
    # 4 components in quadrants
    components = [
        {
            'pos': (0.5, 4.5, 4, 2),
            'title': 'POSTERIOR\nP(θ | D)',
            'desc': 'Niềm tin về θ\nSAU khi thấy dữ liệu',
            'role': 'MỤC TIÊU',
            'color': 'plum'
        },
        {
            'pos': (5.5, 4.5, 4, 2),
            'title': 'LIKELIHOOD\nP(D | θ)',
            'desc': 'Dữ liệu phù hợp\nvới θ như thế nào',
            'role': 'BẰNG CHỨNG MỚI',
            'color': 'lightgreen'
        },
        {
            'pos': (0.5, 1.5, 4, 2),
            'title': 'PRIOR\nP(θ)',
            'desc': 'Niềm tin về θ\nTRƯỚC khi thấy dữ liệu',
            'role': 'KIẾN THỨC CŨ',
            'color': 'lightblue'
        },
        {
            'pos': (5.5, 1.5, 4, 2),
            'title': 'EVIDENCE\nP(D)',
            'desc': 'Xác suất của dữ liệu\n(chuẩn hóa)',
            'role': 'HẰNG SỐ',
            'color': 'lightyellow'
        }
    ]
    
    for comp in components:
        x, y, w, h = comp['pos']
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=comp['color'], linewidth=2)
        ax.add_patch(box)
        
        ax.text(x + w/2, y + h - 0.4, comp['title'], 
                fontsize=13, ha='center', fontweight='bold')
        ax.text(x + w/2, y + h/2, comp['desc'], 
                fontsize=10, ha='center', va='center')
        ax.text(x + w/2, y + 0.3, f'Vai trò: {comp["role"]}', 
                fontsize=9, ha='center', style='italic',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    # Arrows showing relationships
    # Prior + Likelihood → Posterior
    arrow1 = FancyArrowPatch((2.5, 3.5), (2.5, 4.5), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='blue')
    ax.add_patch(arrow1)
    
    arrow2 = FancyArrowPatch((7.5, 3.5), (7.5, 4.5), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='green')
    ax.add_patch(arrow2)
    
    # Key insight
    insight_box = FancyBboxPatch((0.5, 0.2), 9, 0.8, boxstyle="round,pad=0.1",
                                 edgecolor='gold', facecolor='lightyellow', linewidth=2)
    ax.add_patch(insight_box)
    ax.text(5, 0.6, '💡 Posterior = Sự cân bằng giữa Kiến thức Cũ (Prior) và Bằng chứng Mới (Likelihood)', 
            fontsize=11, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bayes_theorem_visual.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: bayes_theorem_visual.png")

def create_sequential_updating_story(output_dir):
    """Image 3: Sequential Updating - Emma's Journey"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Sequential Updating: Hành trình của Emma', 
            fontsize=18, fontweight='bold', ha='center')
    ax.text(5, 9, 'Posterior hôm qua = Prior hôm nay', 
            fontsize=13, ha='center', style='italic', color='purple')
    
    # Timeline
    days = [
        {'x': 1.5, 'y': 7, 'day': 'Day 1', 'desc': 'Prior Ban đầu\nBeta(5,5)', 'color': 'lightblue'},
        {'x': 4, 'y': 7, 'day': 'Day 2', 'desc': '10 users\n7 conversions', 'color': 'lightgreen'},
        {'x': 6.5, 'y': 7, 'day': 'Day 3', 'desc': '20 users\n15 conversions', 'color': 'lightyellow'},
        {'x': 9, 'y': 7, 'day': 'Day 4', 'desc': '50 users\n38 conversions', 'color': 'lightcoral'}
    ]
    
    for i, day in enumerate(days):
        # Day box
        box = FancyBboxPatch((day['x']-0.6, day['y']-0.6), 1.2, 1.2, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=day['color'], linewidth=2)
        ax.add_patch(box)
        ax.text(day['x'], day['y']+0.3, day['day'], 
                fontsize=11, ha='center', fontweight='bold')
        ax.text(day['x'], day['y']-0.1, day['desc'], 
                fontsize=9, ha='center', va='center')
        
        # Arrow to next day
        if i < len(days) - 1:
            arrow = FancyArrowPatch((day['x']+0.6, day['y']), (days[i+1]['x']-0.6, days[i+1]['y']), 
                                   arrowstyle='->', mutation_scale=20, 
                                   linewidth=3, color='purple')
            ax.add_patch(arrow)
            ax.text((day['x'] + days[i+1]['x'])/2, day['y']+0.5, 
                    'Update!', fontsize=9, ha='center', style='italic', color='purple')
    
    # Posterior evolution (distributions getting narrower)
    positions = [
        (1.5, 4.5, 'Beta(5,5)\nMean=0.50', 'blue'),
        (4, 4.5, 'Beta(12,8)\nMean=0.60', 'green'),
        (6.5, 4.5, 'Beta(27,13)\nMean=0.68', 'orange'),
        (9, 4.5, 'Beta(65,25)\nMean=0.72', 'red')
    ]
    
    for i, (x, y, label, color) in enumerate(positions):
        # Distribution visualization (simplified bell curve)
        width = 1.2 - i*0.15  # Getting narrower
        height = 1 + i*0.3    # Getting taller
        
        # Draw simplified distribution
        curve_x = np.linspace(x-width/2, x+width/2, 50)
        curve_y = y + height * np.exp(-((curve_x - x)**2) / (2*(width/4)**2))
        ax.plot(curve_x, curve_y, linewidth=2, color=color)
        ax.fill_between(curve_x, y, curve_y, alpha=0.3, color=color)
        
        ax.text(x, y-0.5, label, fontsize=9, ha='center', fontweight='bold')
    
    # Key observations
    obs_box = FancyBboxPatch((0.5, 0.5), 9, 3, boxstyle="round,pad=0.15",
                             edgecolor='purple', facecolor='lavender', linewidth=2)
    ax.add_patch(obs_box)
    
    ax.text(5, 3, '📊 Quan sát Quan trọng:', fontsize=13, ha='center', fontweight='bold')
    
    observations = [
        '1. Posterior hôm qua → Prior hôm nay',
        '2. Độ chắc chắn TĂNG dần (phân phối hẹp hơn)',
        '3. Kiến thức TÍCH LŨY theo thời gian',
        '4. Không cần lưu trữ TẤT CẢ dữ liệu - chỉ cần posterior!'
    ]
    
    for i, obs in enumerate(observations):
        ax.text(5, 2.4 - i*0.4, obs, fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sequential_updating_story.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: sequential_updating_story.png")

def create_posterior_summaries_explained(output_dir):
    """Image 4: Posterior Summaries - Mean, Median, Mode"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Posterior Summaries: Ba Thống kê Quan trọng', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Draw a posterior distribution (Beta(12, 8))
    theta = np.linspace(0, 1, 1000)
    from scipy import stats
    posterior = stats.beta(12, 8)
    pdf = posterior.pdf(theta)
    
    # Scale and position for visualization
    theta_scaled = 2 + theta * 6
    pdf_scaled = 4 + pdf * 2
    
    ax.plot(theta_scaled, pdf_scaled, linewidth=3, color='purple')
    ax.fill_between(theta_scaled, 4, pdf_scaled, alpha=0.3, color='purple')
    
    # Mean
    mean = posterior.mean()
    mean_scaled = 2 + mean * 6
    ax.axvline(mean_scaled, color='red', linestyle='--', linewidth=3,
               label='Mean')
    ax.text(mean_scaled, 7.5, 'MEAN', fontsize=11, ha='center', fontweight='bold', color='red')
    ax.text(mean_scaled, 7.2, f'{mean:.3f}', fontsize=10, ha='center', color='red')
    
    # Median
    median = posterior.median()
    median_scaled = 2 + median * 6
    ax.axvline(median_scaled, color='blue', linestyle='--', linewidth=3,
               label='Median')
    ax.text(median_scaled, 7, 'MEDIAN', fontsize=11, ha='center', fontweight='bold', color='blue')
    ax.text(median_scaled, 6.7, f'{median:.3f}', fontsize=10, ha='center', color='blue')
    
    # Mode (MAP)
    mode = (12 - 1) / (12 + 8 - 2)
    mode_scaled = 2 + mode * 6
    ax.axvline(mode_scaled, color='green', linestyle='--', linewidth=3,
               label='Mode')
    ax.text(mode_scaled, 6.5, 'MODE (MAP)', fontsize=11, ha='center', fontweight='bold', color='green')
    ax.text(mode_scaled, 6.2, f'{mode:.3f}', fontsize=10, ha='center', color='green')
    
    # Explanations
    explanations = [
        {
            'pos': (0.5, 2, 3, 1.5),
            'title': 'MEAN',
            'formula': 'E[θ | D]',
            'desc': 'Trung bình\nTối thiểu hóa MSE',
            'color': 'mistyrose'
        },
        {
            'pos': (3.7, 2, 3, 1.5),
            'title': 'MEDIAN',
            'formula': 'P(θ ≤ m | D) = 0.5',
            'desc': 'Trung vị\nTối thiểu hóa MAE',
            'color': 'lightblue'
        },
        {
            'pos': (6.9, 2, 3, 1.5),
            'title': 'MODE (MAP)',
            'formula': 'argmax P(θ | D)',
            'desc': 'Yếu vị\nGiá trị phổ biến nhất',
            'color': 'lightgreen'
        }
    ]
    
    for exp in explanations:
        x, y, w, h = exp['pos']
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=exp['color'], linewidth=2)
        ax.add_patch(box)
        
        ax.text(x + w/2, y + h - 0.3, exp['title'], 
                fontsize=12, ha='center', fontweight='bold')
        ax.text(x + w/2, y + h/2 + 0.1, exp['formula'], 
                fontsize=10, ha='center', style='italic')
        ax.text(x + w/2, y + 0.3, exp['desc'], 
                fontsize=9, ha='center')
    
    # Key insight
    insight_box = FancyBboxPatch((0.5, 0.3), 9, 1.2, boxstyle="round,pad=0.1",
                                 edgecolor='gold', facecolor='lightyellow', linewidth=2)
    ax.add_patch(insight_box)
    ax.text(5, 1.2, '💡 Ba thống kê này tóm tắt posterior', 
            fontsize=12, ha='center', fontweight='bold')
    ax.text(5, 0.8, 'Chọn thống kê nào tùy thuộc vào mục đích:', fontsize=10, ha='center')
    ax.text(5, 0.5, 'Mean (MSE) | Median (MAE) | Mode (Most likely)', fontsize=9, ha='center')
    
    # Axes
    ax.plot([2, 8], [4, 4], 'k-', linewidth=1)
    ax.text(5, 3.7, 'θ', fontsize=12, ha='center', fontweight='bold')
    ax.text(1.5, 6, 'Mật độ\nPosterior', fontsize=10, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'posterior_summaries_explained.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: posterior_summaries_explained.png")

def create_credible_intervals_vs_confidence(output_dir):
    """Image 5: Credible vs Confidence Intervals - The Battle"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Credible vs Confidence Intervals: Trận Chiến Quan trọng', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Two sides
    # Left: Credible Interval (Bayesian)
    credible_box = FancyBboxPatch((0.3, 4), 4.5, 4.5, boxstyle="round,pad=0.15",
                                  edgecolor='green', facecolor='honeydew', linewidth=3)
    ax.add_patch(credible_box)
    
    ax.text(2.55, 8.2, 'CREDIBLE INTERVAL', fontsize=14, ha='center', fontweight='bold', color='green')
    ax.text(2.55, 7.8, '(Bayesian)', fontsize=11, ha='center', style='italic')
    
    ax.text(2.55, 7.3, 'Định nghĩa:', fontsize=11, ha='center', fontweight='bold')
    ax.text(2.55, 6.9, 'P(a ≤ θ ≤ b | D) = 0.95', fontsize=10, ha='center')
    
    ax.text(2.55, 6.4, 'Diễn giải ĐÚNG:', fontsize=11, ha='center', fontweight='bold')
    ax.text(2.55, 5.9, '"95% xác suất θ\nnằm trong khoảng này"', 
            fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    ax.text(2.55, 5.2, 'Cái gì ngẫu nhiên?', fontsize=10, ha='center', fontweight='bold')
    ax.text(2.55, 4.8, 'Tham số θ\n(biến ngẫu nhiên)', fontsize=9, ha='center')
    
    ax.text(2.55, 4.3, '✅ CÓ THỂ nói về P(θ)', fontsize=10, ha='center', fontweight='bold', color='green')
    
    # Right: Confidence Interval (Frequentist)
    confidence_box = FancyBboxPatch((5.2, 4), 4.5, 4.5, boxstyle="round,pad=0.15",
                                    edgecolor='red', facecolor='mistyrose', linewidth=3)
    ax.add_patch(confidence_box)
    
    ax.text(7.45, 8.2, 'CONFIDENCE INTERVAL', fontsize=14, ha='center', fontweight='bold', color='red')
    ax.text(7.45, 7.8, '(Frequentist)', fontsize=11, ha='center', style='italic')
    
    ax.text(7.45, 7.3, 'Định nghĩa:', fontsize=11, ha='center', fontweight='bold')
    ax.text(7.45, 6.9, 'Trong vô số lần lặp lại,\n95% khoảng chứa θ', fontsize=9, ha='center')
    
    ax.text(7.45, 6.2, 'Diễn giải SAI (phổ biến):', fontsize=11, ha='center', fontweight='bold')
    ax.text(7.45, 5.7, '"95% xác suất θ\nnằm trong khoảng này"', 
            fontsize=10, ha='center', bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    ax.text(7.45, 5.2, '❌ SAI!', fontsize=12, ha='center', fontweight='bold', color='red')
    
    ax.text(7.45, 4.7, 'Cái gì ngẫu nhiên?', fontsize=10, ha='center', fontweight='bold')
    ax.text(7.45, 4.3, 'Khoảng (dữ liệu)\nθ là hằng số!', fontsize=9, ha='center')
    
    # VS symbol
    vs_circle = Circle((5, 6.2), 0.5, facecolor='gold', edgecolor='black', linewidth=3)
    ax.add_patch(vs_circle)
    ax.text(5, 6.2, 'VS', fontsize=16, ha='center', fontweight='bold')
    
    # Comparison table
    table_box = FancyBboxPatch((0.5, 0.5), 9, 3, boxstyle="round,pad=0.15",
                               edgecolor='purple', facecolor='lavender', linewidth=2)
    ax.add_patch(table_box)
    
    ax.text(5, 3.2, '📊 So sánh:', fontsize=13, ha='center', fontweight='bold')
    
    comparisons = [
        ('Credible Interval', 'Confidence Interval'),
        ('✅ Diễn giải trực tiếp', '❌ Diễn giải phức tạp'),
        ('✅ Nói về P(θ)', '❌ Không thể nói về P(θ)'),
        ('✅ Kết hợp prior', '❌ Không kết hợp prior'),
        ('✅ Trực quan', '❌ Cần "vô số lần lặp lại"')
    ]
    
    y_start = 2.6
    for i, (left, right) in enumerate(comparisons):
        y = y_start - i * 0.35
        ax.text(2.5, y, left, fontsize=9, ha='center', fontweight='bold' if i == 0 else 'normal')
        ax.text(7.5, y, right, fontsize=9, ha='center', fontweight='bold' if i == 0 else 'normal')
        if i == 0:
            ax.plot([1, 4], [y-0.1, y-0.1], 'k-', linewidth=1)
            ax.plot([6, 9], [y-0.1, y-0.1], 'k-', linewidth=1)
    
    ax.text(5, 0.8, '💡 Credible Interval cho phép phát biểu trực tiếp về xác suất của θ!', 
            fontsize=11, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'credible_intervals_vs_confidence.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: credible_intervals_vs_confidence.png")

def create_posterior_predictive_distribution(output_dir):
    """Image 6: Posterior Predictive Distribution"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Posterior Predictive Distribution', 
            fontsize=18, fontweight='bold', ha='center')
    ax.text(5, 9, 'Dự đoán Dữ liệu Mới', 
            fontsize=14, ha='center', style='italic', color='purple')
    
    # Process flow
    # Step 1: Posterior
    posterior_box = FancyBboxPatch((0.5, 6.5), 2, 1.5, boxstyle="round,pad=0.1",
                                   edgecolor='purple', facecolor='plum', linewidth=2)
    ax.add_patch(posterior_box)
    ax.text(1.5, 7.5, 'POSTERIOR', fontsize=12, ha='center', fontweight='bold')
    ax.text(1.5, 7.1, 'P(θ | D)', fontsize=11, ha='center')
    ax.text(1.5, 6.8, 'Niềm tin về θ', fontsize=9, ha='center', style='italic')
    
    # Arrow 1
    arrow1 = FancyArrowPatch((2.5, 7.25), (3.5, 7.25), 
                            arrowstyle='->', mutation_scale=25, 
                            linewidth=3, color='purple')
    ax.add_patch(arrow1)
    ax.text(3, 7.6, 'Sample θ', fontsize=9, ha='center', style='italic')
    
    # Step 2: Sample theta
    sample_box = FancyBboxPatch((3.5, 6.5), 2, 1.5, boxstyle="round,pad=0.1",
                                edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax.add_patch(sample_box)
    ax.text(4.5, 7.5, 'SAMPLE θ', fontsize=12, ha='center', fontweight='bold')
    ax.text(4.5, 7.1, 'θ ~ P(θ | D)', fontsize=10, ha='center')
    ax.text(4.5, 6.8, 'Nhiều giá trị θ', fontsize=9, ha='center', style='italic')
    
    # Arrow 2
    arrow2 = FancyArrowPatch((5.5, 7.25), (6.5, 7.25), 
                            arrowstyle='->', mutation_scale=25, 
                            linewidth=3, color='green')
    ax.add_patch(arrow2)
    ax.text(6, 7.6, 'Sample data', fontsize=9, ha='center', style='italic')
    
    # Step 3: Sample new data
    newdata_box = FancyBboxPatch((6.5, 6.5), 2, 1.5, boxstyle="round,pad=0.1",
                                 edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(newdata_box)
    ax.text(7.5, 7.5, 'SAMPLE DATA', fontsize=12, ha='center', fontweight='bold')
    ax.text(7.5, 7.1, '~D ~ P(~D | θ)', fontsize=10, ha='center')
    ax.text(7.5, 6.8, 'Dữ liệu mới', fontsize=9, ha='center', style='italic')
    
    # Result
    arrow3 = FancyArrowPatch((7.5, 6.5), (7.5, 5.5), 
                            arrowstyle='->', mutation_scale=30, 
                            linewidth=4, color='orange')
    ax.add_patch(arrow3)
    
    result_box = FancyBboxPatch((3, 3.5), 4.5, 1.5, boxstyle="round,pad=0.15",
                                edgecolor='orange', facecolor='lightyellow', linewidth=3)
    ax.add_patch(result_box)
    ax.text(5.25, 4.6, 'POSTERIOR PREDICTIVE', fontsize=13, ha='center', fontweight='bold', color='orange')
    ax.text(5.25, 4.2, 'P(~D | D)', fontsize=12, ha='center')
    ax.text(5.25, 3.8, 'Phân phối của dữ liệu MỚI', fontsize=10, ha='center', style='italic')
    
    # Formula
    formula_box = FancyBboxPatch((0.5, 5), 9, 1, boxstyle="round,pad=0.1",
                                 edgecolor='black', facecolor='white', linewidth=2)
    ax.add_patch(formula_box)
    ax.text(5, 5.7, 'Công thức:', fontsize=11, ha='center', fontweight='bold')
    ax.text(5, 5.3, 'P(~D | D) = ∫ P(~D | θ) P(θ | D) dθ', fontsize=11, ha='center')
    
    # Applications
    app_box = FancyBboxPatch((0.5, 0.5), 9, 2.5, boxstyle="round,pad=0.15",
                             edgecolor='purple', facecolor='lavender', linewidth=2)
    ax.add_patch(app_box)
    
    ax.text(5, 2.7, '🎯 Ứng dụng:', fontsize=13, ha='center', fontweight='bold')
    
    applications = [
        '1. MODEL CHECKING: So sánh dữ liệu dự đoán với dữ liệu thực tế',
        '2. PREDICTION: Dự đoán quan sát mới với sự không chắc chắn đầy đủ',
        '3. DECISION MAKING: Đưa ra quyết định dựa trên dự đoán tương lai'
    ]
    
    for i, app in enumerate(applications):
        ax.text(5, 2.2 - i*0.45, app, fontsize=10, ha='center')
    
    ax.text(5, 0.8, '💡 Posterior Predictive kết hợp: (1) Không chắc chắn về θ + (2) Biến động ngẫu nhiên', 
            fontsize=10, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'posterior_predictive_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: posterior_predictive_distribution.png")

def create_prior_to_posterior_transformation(output_dir):
    """Image 7: Prior to Posterior Transformation - When does Prior/Data win?"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Prior-Data Balance: Khi nào Prior thắng? Khi nào Data thắng?', 
            fontsize=17, fontweight='bold', ha='center')
    
    # 2x2 grid of scenarios
    scenarios = [
        {
            'pos': (0.5, 5.5, 4.5, 3.5),
            'title': 'Prior YẾU + Data NHIỀU',
            'result': '→ DATA THẮNG!',
            'prior': 'Beta(1,1)',
            'data': 'n=100',
            'posterior': '≈ MLE',
            'color': 'lightgreen',
            'winner': 'DATA'
        },
        {
            'pos': (5.5, 5.5, 4.5, 3.5),
            'title': 'Prior MẠNH + Data NHIỀU',
            'result': '→ Cân bằng',
            'prior': 'Beta(50,50)',
            'data': 'n=100',
            'posterior': 'Giữa Prior & MLE',
            'color': 'lightyellow',
            'winner': 'BALANCE'
        },
        {
            'pos': (0.5, 1, 4.5, 3.5),
            'title': 'Prior YẾU + Data ÍT',
            'result': '→ Không ổn định',
            'prior': 'Beta(1,1)',
            'data': 'n=5',
            'posterior': 'Gần MLE nhưng rộng',
            'color': 'lightcoral',
            'winner': 'UNSTABLE'
        },
        {
            'pos': (5.5, 1, 4.5, 3.5),
            'title': 'Prior MẠNH + Data ÍT',
            'result': '→ PRIOR THẮNG!',
            'prior': 'Beta(50,50)',
            'data': 'n=5',
            'posterior': '≈ Prior',
            'color': 'lightblue',
            'winner': 'PRIOR'
        }
    ]
    
    for scenario in scenarios:
        x, y, w, h = scenario['pos']
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                            edgecolor='black', facecolor=scenario['color'], linewidth=2)
        ax.add_patch(box)
        
        ax.text(x + w/2, y + h - 0.4, scenario['title'], 
                fontsize=12, ha='center', fontweight='bold')
        ax.text(x + w/2, y + h - 0.9, scenario['result'], 
                fontsize=11, ha='center', fontweight='bold', color='darkred')
        
        ax.text(x + w/2, y + h/2 + 0.5, f'Prior: {scenario["prior"]}', 
                fontsize=10, ha='center')
        ax.text(x + w/2, y + h/2, f'Data: {scenario["data"]}', 
                fontsize=10, ha='center')
        ax.text(x + w/2, y + h/2 - 0.5, f'Posterior: {scenario["posterior"]}', 
                fontsize=10, ha='center', style='italic')
        
        # Winner badge
        if scenario['winner'] == 'DATA':
            badge_color = 'green'
            badge_text = '🏆 DATA'
        elif scenario['winner'] == 'PRIOR':
            badge_color = 'blue'
            badge_text = '🏆 PRIOR'
        elif scenario['winner'] == 'BALANCE':
            badge_color = 'orange'
            badge_text = '⚖️ BALANCE'
        else:
            badge_color = 'red'
            badge_text = '⚠️ UNSTABLE'
        
        badge = FancyBboxPatch((x + w/2 - 0.8, y + 0.2), 1.6, 0.5, boxstyle="round,pad=0.05",
                               edgecolor='black', facecolor=badge_color, linewidth=2, alpha=0.7)
        ax.add_patch(badge)
        ax.text(x + w/2, y + 0.45, badge_text, 
                fontsize=10, ha='center', fontweight='bold', color='white')
    
    # Key insight
    insight_box = FancyBboxPatch((0.5, 0.1), 9, 0.7, boxstyle="round,pad=0.1",
                                 edgecolor='gold', facecolor='lightyellow', linewidth=3)
    ax.add_patch(insight_box)
    ax.text(5, 0.5, '💡 Posterior = Weighted Average của Prior và Data. Trọng số phụ thuộc vào độ mạnh của mỗi nguồn!', 
            fontsize=11, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_to_posterior_transformation.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: prior_to_posterior_transformation.png")

def main():
    """Generate all cartoon images for Bài 2.4"""
    print("\n" + "="*70)
    print("GENERATING CARTOON IMAGES FOR BÀI 2.4: POSTERIOR")
    print("="*70 + "\n")
    
    create_bayesian_update_machine_intro(output_dir)
    create_bayes_theorem_visual(output_dir)
    create_sequential_updating_story(output_dir)
    create_posterior_summaries_explained(output_dir)
    create_credible_intervals_vs_confidence(output_dir)
    create_posterior_predictive_distribution(output_dir)
    create_prior_to_posterior_transformation(output_dir)
    
    print("\n" + "="*70)
    print("✅ ALL 7 CARTOON IMAGES GENERATED SUCCESSFULLY!")
    print("="*70)
    print(f"\nImages saved to: {output_dir}")
    print("\nList of generated images:")
    print("  1. bayesian_update_machine_intro.png")
    print("  2. bayes_theorem_visual.png")
    print("  3. sequential_updating_story.png")
    print("  4. posterior_summaries_explained.png")
    print("  5. credible_intervals_vs_confidence.png")
    print("  6. posterior_predictive_distribution.png")
    print("  7. prior_to_posterior_transformation.png")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
