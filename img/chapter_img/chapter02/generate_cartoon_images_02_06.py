"""
Generate cartoon-style images for Bài 2.6: Grid Approximation
Enhanced version with storytelling about The Grid Explorer
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle, Polygon
import numpy as np
import os

# Create output directory
output_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(output_dir, exist_ok=True)

def create_grid_approximation_intro(output_dir):
    """Image 1: Grid Approximation Introduction"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Grid Approximation: Chia nhỏ và Chinh phục', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Dr. Maya
    maya_head = Circle((2, 8), 0.3, facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(maya_head)
    ax.plot(1.9, 8.05, 'ko', markersize=4)
    ax.plot(2.1, 8.05, 'ko', markersize=4)
    smile = patches.Arc((2, 7.95), 0.2, 0.15, angle=0, theta1=200, theta2=340, 
                       color='black', linewidth=2)
    ax.add_patch(smile)
    ax.text(2, 7.4, 'Dr. Maya', fontsize=11, ha='center', fontweight='bold')
    
    # Speech bubble
    bubble = FancyBboxPatch((0.3, 8.5), 2.5, 0.8, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='white', linewidth=2)
    ax.add_patch(bubble)
    ax.text(1.55, 8.9, '"Không conjugate? Grid!"', fontsize=10, ha='center', fontweight='bold')
    
    # Grid visualization
    grid_box = FancyBboxPatch((4, 5), 5, 4, boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor='lightgray', linewidth=2)
    ax.add_patch(grid_box)
    
    # Draw grid points
    n_points = 10
    for i in range(n_points):
        for j in range(5):
            x = 4.5 + i * 0.45
            y = 5.5 + j * 0.7
            size = 30 + 50 * np.exp(-((i-5)**2 + (j-2)**2)/10)  # Bigger in center
            ax.plot(x, y, 'o', markersize=size/10, color='purple', alpha=0.6)
    
    ax.text(6.5, 8.7, 'GRID APPROXIMATION', fontsize=14, ha='center', fontweight='bold')
    ax.text(6.5, 8.3, 'Chia θ thành lưới điểm', fontsize=11, ha='center')
    
    # The idea
    idea_box = FancyBboxPatch((0.5, 3), 3, 1.5, boxstyle="round,pad=0.1",
                              edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax.add_patch(idea_box)
    ax.text(2, 4.2, 'Ý TƯỞNG', fontsize=12, ha='center', fontweight='bold')
    ax.text(2, 3.8, 'Không tính được chính xác?', fontsize=9, ha='center')
    ax.text(2, 3.5, '→ XẤP XỈ!', fontsize=10, ha='center', fontweight='bold')
    ax.text(2, 3.2, 'Chia nhỏ + Tính từng điểm', fontsize=9, ha='center')
    
    # The process
    process_box = FancyBboxPatch((4, 3), 5, 1.5, boxstyle="round,pad=0.1",
                                 edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(process_box)
    ax.text(6.5, 4.2, 'QUY TRÌNH', fontsize=12, ha='center', fontweight='bold')
    ax.text(6.5, 3.8, '1. Chia θ thành n điểm', fontsize=9, ha='center')
    ax.text(6.5, 3.5, '2. Tính p(θᵢ|D) tại mỗi điểm', fontsize=9, ha='center')
    ax.text(6.5, 3.2, '3. Chuẩn hóa → Done!', fontsize=9, ha='center')
    
    # Key insight
    insight_box = FancyBboxPatch((0.5, 0.5), 9, 2, boxstyle="round,pad=0.15",
                                 edgecolor='gold', facecolor='lightyellow', linewidth=3)
    ax.add_patch(insight_box)
    ax.text(5, 2.2, '💡 GRID APPROXIMATION', fontsize=14, ha='center', fontweight='bold')
    ax.text(5, 1.8, '✅ Đơn giản, dễ hiểu', fontsize=11, ha='center')
    ax.text(5, 1.5, '✅ Linh hoạt (mọi prior/likelihood)', fontsize=11, ha='center')
    ax.text(5, 1.2, '✅ Chính xác với grid mịn', fontsize=11, ha='center')
    ax.text(5, 0.9, '❌ Chỉ dùng cho 1-2 tham số (curse of dimensionality)', fontsize=11, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'grid_approximation_intro.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: grid_approximation_intro.png")

def create_grid_algorithm_steps(output_dir):
    """Image 2: Grid Algorithm 5 Steps"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Thuật toán Grid: 5 Bước Đơn giản', 
            fontsize=18, fontweight='bold', ha='center')
    
    steps = [
        {
            'y': 8,
            'num': '1',
            'title': 'TẠO GRID',
            'desc': 'θ_grid = [θ₁, θ₂, ..., θₙ]',
            'color': 'lightblue'
        },
        {
            'y': 6.5,
            'num': '2',
            'title': 'TÍNH PRIOR',
            'desc': 'prior_vals = [p(θ₁), p(θ₂), ..., p(θₙ)]',
            'color': 'lightgreen'
        },
        {
            'y': 5,
            'num': '3',
            'title': 'TÍNH LIKELIHOOD',
            'desc': 'like_vals = [p(D|θ₁), ..., p(D|θₙ)]',
            'color': 'lightyellow'
        },
        {
            'y': 3.5,
            'num': '4',
            'title': 'NHÂN',
            'desc': 'post_unnorm = prior_vals × like_vals',
            'color': 'lightcoral'
        },
        {
            'y': 2,
            'num': '5',
            'title': 'CHUẨN HÓA',
            'desc': 'post_vals = post_unnorm / Σ',
            'color': 'plum'
        }
    ]
    
    for i, step in enumerate(steps):
        # Number circle
        circle = Circle((1.5, step['y']), 0.4, facecolor='gold', edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(1.5, step['y'], step['num'], fontsize=18, ha='center', va='center', fontweight='bold')
        
        # Step box
        box = FancyBboxPatch((2.5, step['y']-0.5), 7, 1, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=step['color'], linewidth=2)
        ax.add_patch(box)
        
        ax.text(6, step['y']+0.2, step['title'], fontsize=13, ha='center', fontweight='bold')
        ax.text(6, step['y']-0.2, step['desc'], fontsize=10, ha='center', family='monospace')
        
        # Arrow to next
        if i < len(steps) - 1:
            arrow = FancyArrowPatch((1.5, step['y']-0.5), (1.5, steps[i+1]['y']+0.5), 
                                   arrowstyle='->', mutation_scale=25, 
                                   linewidth=3, color='purple')
            ax.add_patch(arrow)
    
    # Result
    result_box = FancyBboxPatch((0.5, 0.3), 9, 1, boxstyle="round,pad=0.1",
                                edgecolor='green', facecolor='lightgreen', linewidth=3)
    ax.add_patch(result_box)
    ax.text(5, 1, '🎉 DONE! Posterior approximation hoàn thành!', 
            fontsize=13, ha='center', fontweight='bold')
    ax.text(5, 0.6, 'Giờ có thể tính mean, CI, sample, posterior predictive...', 
            fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'grid_algorithm_steps.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: grid_algorithm_steps.png")

def create_grid_size_comparison(output_dir):
    """Image 3: Grid Size Comparison - Coarse vs Fine"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Grid Size: Thô vs Mịn', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Three grids
    grids = [
        {'x': 1, 'size': 5, 'label': 'THÔ\n5 điểm', 'color': 'lightcoral', 'status': '❌ Không chính xác'},
        {'x': 4, 'size': 20, 'label': 'TRUNG BÌNH\n20 điểm', 'color': 'lightyellow', 'status': '⚠️ OK'},
        {'x': 7, 'size': 100, 'label': 'MỊN\n100 điểm', 'color': 'lightgreen', 'status': '✅ Chính xác'}
    ]
    
    for grid in grids:
        # Grid box
        box = FancyBboxPatch((grid['x'], 5), 2, 3, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor=grid['color'], linewidth=2)
        ax.add_patch(box)
        
        # Draw grid points
        n = grid['size']
        if n <= 20:
            # Draw actual points
            for i in range(n):
                x = grid['x'] + 0.2 + (i % 5) * 0.35
                y = 5.5 + (i // 5) * 0.5
                if y < 7.8:
                    ax.plot(x, y, 'o', markersize=8, color='purple')
        else:
            # Draw many small points
            for i in range(50):
                x = grid['x'] + 0.2 + np.random.rand() * 1.6
                y = 5.5 + np.random.rand() * 2.3
                ax.plot(x, y, 'o', markersize=3, color='purple', alpha=0.5)
        
        # Label
        ax.text(grid['x']+1, 8.3, grid['label'], fontsize=11, ha='center', fontweight='bold')
        ax.text(grid['x']+1, 4.7, grid['status'], fontsize=10, ha='center')
    
    # Trade-off
    tradeoff_box = FancyBboxPatch((0.5, 0.5), 9, 4, boxstyle="round,pad=0.15",
                                  edgecolor='purple', facecolor='lavender', linewidth=2)
    ax.add_patch(tradeoff_box)
    
    ax.text(5, 4.2, '⚖️ TRADE-OFF', fontsize=14, ha='center', fontweight='bold')
    
    ax.text(2.5, 3.5, 'Grid THÔ (ít điểm)', fontsize=12, ha='center', fontweight='bold', color='red')
    ax.text(2.5, 3.1, '✅ Nhanh', fontsize=10, ha='center')
    ax.text(2.5, 2.8, '❌ Không chính xác', fontsize=10, ha='center')
    ax.text(2.5, 2.5, '❌ Bỏ sót vùng quan trọng', fontsize=9, ha='center')
    
    ax.text(7.5, 3.5, 'Grid MỊN (nhiều điểm)', fontsize=12, ha='center', fontweight='bold', color='green')
    ax.text(7.5, 3.1, '✅ Chính xác', fontsize=10, ha='center')
    ax.text(7.5, 2.8, '✅ Bao phủ tốt', fontsize=10, ha='center')
    ax.text(7.5, 2.5, '❌ Chậm', fontsize=9, ha='center')
    
    ax.text(5, 1.8, '💡 KHUYẾN NGHỊ', fontsize=13, ha='center', fontweight='bold')
    ax.text(5, 1.4, '• 1 tham số: 100-1000 điểm', fontsize=11, ha='center')
    ax.text(5, 1.1, '• 2 tham số: 50×50 = 2,500 điểm', fontsize=11, ha='center')
    ax.text(5, 0.8, '• 3+ tham số: KHÔNG dùng grid → MCMC!', fontsize=11, ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'grid_size_comparison.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: grid_size_comparison.png")

def create_when_to_use_grid(output_dir):
    """Image 4: When to Use Grid Approximation"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Khi nào dùng Grid Approximation?', 
            fontsize=18, fontweight='bold', ha='center')
    
    # When to USE
    use_box = FancyBboxPatch((0.3, 5), 4.5, 4, boxstyle="round,pad=0.15",
                             edgecolor='green', facecolor='honeydew', linewidth=3)
    ax.add_patch(use_box)
    
    ax.text(2.55, 8.7, '✅ KHI NÀO DÙNG', fontsize=14, ha='center', fontweight='bold', color='green')
    
    use_cases = [
        ('📚', 'Học tập, giảng dạy'),
        ('🔬', '1-2 tham số'),
        ('❌', 'Prior KHÔNG conjugate'),
        ('🎨', 'Cần trực quan hóa'),
        ('✅', 'Kiểm tra kết quả MCMC'),
        ('🎯', 'Model đơn giản')
    ]
    
    y = 8
    for emoji, text in use_cases:
        ax.text(2.55, y, f'{emoji} {text}', fontsize=11, ha='center')
        y -= 0.5
    
    # When NOT to use
    not_use_box = FancyBboxPatch((5.2, 5), 4.5, 4, boxstyle="round,pad=0.15",
                                 edgecolor='red', facecolor='mistyrose', linewidth=3)
    ax.add_patch(not_use_box)
    
    ax.text(7.45, 8.7, '❌ KHI NÀO KHÔNG DÙNG', fontsize=14, ha='center', fontweight='bold', color='red')
    
    not_use_cases = [
        ('3️⃣', '3+ tham số'),
        ('🚀', 'Cần tốc độ cao'),
        ('🏗️', 'Model phức tạp'),
        ('📊', 'Production system'),
        ('💾', 'Big data'),
        ('🔄', 'Hierarchical model')
    ]
    
    y = 8
    for emoji, text in not_use_cases:
        ax.text(7.45, y, f'{emoji} {text}', fontsize=11, ha='center')
        y -= 0.5
    
    # Decision guide
    guide_box = FancyBboxPatch((0.5, 0.5), 9, 4, boxstyle="round,pad=0.15",
                               edgecolor='blue', facecolor='lightcyan', linewidth=2)
    ax.add_patch(guide_box)
    
    ax.text(5, 4.2, '🎯 DECISION GUIDE', fontsize=14, ha='center', fontweight='bold')
    
    ax.text(5, 3.6, '1 tham số + Prior không conjugate?', fontsize=11, ha='center')
    ax.text(5, 3.3, '→ ✅ GRID (100-1000 điểm)', fontsize=10, ha='center', color='green', fontweight='bold')
    
    ax.text(5, 2.8, '2 tham số + Cần trực quan?', fontsize=11, ha='center')
    ax.text(5, 2.5, '→ ✅ GRID (50×50)', fontsize=10, ha='center', color='green', fontweight='bold')
    
    ax.text(5, 2, '3+ tham số?', fontsize=11, ha='center')
    ax.text(5, 1.7, '→ ❌ KHÔNG GRID → MCMC!', fontsize=10, ha='center', color='red', fontweight='bold')
    
    ax.text(5, 1.2, 'Có conjugate prior?', fontsize=11, ha='center')
    ax.text(5, 0.9, '→ ✅ CONJUGATE (nhanh hơn grid)', fontsize=10, ha='center', color='blue', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'when_to_use_grid.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: when_to_use_grid.png")

def create_grid_to_mcmc_bridge(output_dir):
    """Image 5: Bridge from Grid to MCMC"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Từ Grid đến MCMC: Cầu nối', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Grid (left)
    grid_box = FancyBboxPatch((0.3, 5), 3.5, 3.5, boxstyle="round,pad=0.15",
                              edgecolor='blue', facecolor='lightblue', linewidth=3)
    ax.add_patch(grid_box)
    
    ax.text(2.05, 8.2, 'GRID', fontsize=14, ha='center', fontweight='bold')
    ax.text(2.05, 7.8, 'APPROXIMATION', fontsize=12, ha='center', fontweight='bold')
    
    ax.text(2.05, 7.2, '• Tính TẤT CẢ điểm', fontsize=10, ha='center')
    ax.text(2.05, 6.8, '• Chậm với nhiều param', fontsize=10, ha='center')
    ax.text(2.05, 6.4, '• Đơn giản, dễ hiểu', fontsize=10, ha='center')
    ax.text(2.05, 6, '• 1-2 tham số', fontsize=10, ha='center')
    ax.text(2.05, 5.5, '• Curse of dimensionality', fontsize=9, ha='center', style='italic')
    
    # Arrow
    arrow = FancyArrowPatch((3.8, 6.75), (6.2, 6.75), 
                           arrowstyle='->', mutation_scale=40, 
                           linewidth=5, color='purple')
    ax.add_patch(arrow)
    ax.text(5, 7.3, 'EVOLUTION', fontsize=12, ha='center', fontweight='bold', color='purple')
    
    # MCMC (right)
    mcmc_box = FancyBboxPatch((6.2, 5), 3.5, 3.5, boxstyle="round,pad=0.15",
                              edgecolor='red', facecolor='mistyrose', linewidth=3)
    ax.add_patch(mcmc_box)
    
    ax.text(7.95, 8.2, 'MCMC', fontsize=14, ha='center', fontweight='bold')
    ax.text(7.95, 7.8, '(Chapter 03)', fontsize=12, ha='center', fontweight='bold')
    
    ax.text(7.95, 7.2, '• Sample THÔNG MINH', fontsize=10, ha='center')
    ax.text(7.95, 6.8, '• Nhanh với nhiều param', fontsize=10, ha='center')
    ax.text(7.95, 6.4, '• Phức tạp hơn', fontsize=10, ha='center')
    ax.text(7.95, 6, '• 1-∞ tham số', fontsize=10, ha='center')
    ax.text(7.95, 5.5, '• Modern standard', fontsize=9, ha='center', style='italic')
    
    # Key insight
    insight_box = FancyBboxPatch((0.5, 0.5), 9, 4, boxstyle="round,pad=0.15",
                                 edgecolor='gold', facecolor='lightyellow', linewidth=3)
    ax.add_patch(insight_box)
    
    ax.text(5, 4.2, '💡 KEY INSIGHT', fontsize=15, ha='center', fontweight='bold')
    
    ax.text(5, 3.6, 'GRID: Tính posterior tại MỌI điểm', fontsize=12, ha='center')
    ax.text(5, 3.3, '→ Chậm với nhiều tham số', fontsize=10, ha='center', style='italic')
    
    ax.text(5, 2.8, '⬇️', fontsize=16, ha='center')
    
    ax.text(5, 2.4, 'NHẬN RA: Không cần tính TẤT CẢ!', fontsize=12, ha='center', fontweight='bold')
    ax.text(5, 2.1, 'Chỉ cần sample vùng QUAN TRỌNG (posterior cao)', fontsize=10, ha='center')
    
    ax.text(5, 1.6, '⬇️', fontsize=16, ha='center')
    
    ax.text(5, 1.2, 'MCMC: Sample THÔNG MINH từ posterior', fontsize=12, ha='center', fontweight='bold', color='red')
    ax.text(5, 0.9, '→ Nhanh hơn, mạnh hơn, linh hoạt hơn!', fontsize=10, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'grid_to_mcmc_bridge.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: grid_to_mcmc_bridge.png")

def main():
    """Generate all cartoon images for Bài 2.6"""
    print("\n" + "="*70)
    print("GENERATING CARTOON IMAGES FOR BÀI 2.6: GRID APPROXIMATION")
    print("="*70 + "\n")
    
    create_grid_approximation_intro(output_dir)
    create_grid_algorithm_steps(output_dir)
    create_grid_size_comparison(output_dir)
    create_when_to_use_grid(output_dir)
    create_grid_to_mcmc_bridge(output_dir)
    
    print("\n" + "="*70)
    print("✅ ALL 5 CARTOON IMAGES GENERATED SUCCESSFULLY!")
    print("="*70)
    print(f"\nImages saved to: {output_dir}")
    print("\nList of generated images:")
    print("  1. grid_approximation_intro.png")
    print("  2. grid_algorithm_steps.png")
    print("  3. grid_size_comparison.png")
    print("  4. when_to_use_grid.png")
    print("  5. grid_to_mcmc_bridge.png")
    print("\n" + "="*70)
    print("🎉 CHAPTER 02 COMPLETE! 🎉")
    print("="*70)

if __name__ == "__main__":
    main()
