#!/usr/bin/env python3
"""
Generate cartoon-style illustrations for Lesson 1.2: Probability as Plausibility
Inspired by: The Cartoon Guide to Statistics, The Manga Guide to Statistics
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
from matplotlib import font_manager
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Vietnamese font support
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

def create_linh_umbrella_story():
    """
    Cartoon 1: Linh's Umbrella Decision
    Story-based illustration showing Bayesian thinking in daily life
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Câu chuyện của Linh: Quyết định Mang Ô', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Scene 1: Morning - Checking weather
    ax1 = axes[0, 0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    # Character (simple stick figure)
    # Head
    circle = Circle((3, 7), 0.8, color='#FFE4B5', ec='black', linewidth=2)
    ax1.add_patch(circle)
    # Eyes
    ax1.plot([2.7, 3.3], [7.2, 7.2], 'ko', markersize=8)
    # Smile
    theta = np.linspace(3.8, 5.5, 20)
    x_smile = 3 + 0.4 * np.cos(theta)
    y_smile = 7 + 0.4 * np.sin(theta) - 0.3
    ax1.plot(x_smile, y_smile, 'k-', linewidth=2)
    # Body
    ax1.plot([3, 3], [6.2, 4], 'k-', linewidth=3)
    # Arms
    ax1.plot([3, 2], [5.5, 4.5], 'k-', linewidth=3)
    ax1.plot([3, 4], [5.5, 4.5], 'k-', linewidth=3)
    # Legs
    ax1.plot([3, 2.5], [4, 2], 'k-', linewidth=3)
    ax1.plot([3, 3.5], [4, 2], 'k-', linewidth=3)
    
    # Phone
    phone = FancyBboxPatch((1.5, 4), 0.8, 1.2, boxstyle="round,pad=0.05",
                           facecolor='#87CEEB', edgecolor='black', linewidth=2)
    ax1.add_patch(phone)
    ax1.text(1.9, 4.6, '📱', fontsize=30, ha='center')
    
    # Weather forecast
    forecast_box = FancyBboxPatch((5, 6), 4, 3, boxstyle="round,pad=0.1",
                                  facecolor='white', edgecolor='blue', linewidth=2)
    ax1.add_patch(forecast_box)
    ax1.text(7, 8.3, '🌧️ Dự báo Thời tiết', fontsize=12, ha='center', fontweight='bold')
    ax1.text(7, 7.5, 'Xác suất mưa:', fontsize=11, ha='center')
    ax1.text(7, 6.8, '70%', fontsize=24, ha='center', fontweight='bold', color='blue')
    
    # Thought bubble
    thought = Circle((4.5, 8.5), 0.3, color='white', ec='gray', linewidth=2)
    ax1.add_patch(thought)
    thought2 = Circle((5, 9), 0.5, color='white', ec='gray', linewidth=2)
    ax1.add_patch(thought2)
    thought3 = Circle((6, 9.5), 0.8, color='white', ec='gray', linewidth=2)
    ax1.add_patch(thought3)
    ax1.text(6, 9.5, '70%?\n🤔', fontsize=10, ha='center', va='center')
    
    ax1.text(5, 0.5, 'Scene 1: Sáng thứ Hai, 7:00 AM', 
             fontsize=12, ha='center', style='italic')
    
    # Scene 2: Confusion - Frequentist interpretation
    ax2 = axes[0, 1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    # Confused character
    circle = Circle((3, 7), 0.8, color='#FFE4B5', ec='black', linewidth=2)
    ax2.add_patch(circle)
    ax2.plot([2.7, 3.3], [7.2, 7.2], 'ko', markersize=8)
    # Confused expression
    ax2.plot([2.8, 3.2], [6.8, 6.8], 'k-', linewidth=3)
    ax2.text(3, 8.5, '???', fontsize=30, ha='center', fontweight='bold', color='red')
    
    # Frequentist definition box
    freq_box = FancyBboxPatch((4.5, 4), 5, 5, boxstyle="round,pad=0.1",
                              facecolor='#FFE4E1', edgecolor='red', linewidth=3)
    ax2.add_patch(freq_box)
    ax2.text(7, 8.3, '📚 Định nghĩa Tần suất:', fontsize=11, ha='center', fontweight='bold')
    ax2.text(7, 7.5, 'P(A) = lim(n→∞) f/n', fontsize=12, ha='center', style='italic')
    ax2.text(7, 6.5, '"Lặp lại vô số lần..."', fontsize=10, ha='center')
    ax2.text(7, 5.8, '🌍🌍🌍 Vũ trụ song song?', fontsize=10, ha='center')
    ax2.text(7, 5, '❌ "Hôm nay" chỉ xảy ra 1 lần!', 
             fontsize=10, ha='center', color='red', fontweight='bold')
    
    ax2.text(5, 0.5, 'Scene 2: Linh bối rối với định nghĩa tần suất', 
             fontsize=12, ha='center', style='italic')
    
    # Scene 3: Bayesian understanding
    ax3 = axes[1, 0]
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    
    # Happy character
    circle = Circle((3, 7), 0.8, color='#FFE4B5', ec='black', linewidth=2)
    ax3.add_patch(circle)
    ax3.plot([2.7, 3.3], [7.2, 7.2], 'ko', markersize=8)
    # Big smile
    theta = np.linspace(3.5, 6, 30)
    x_smile = 3 + 0.5 * np.cos(theta)
    y_smile = 7 + 0.5 * np.sin(theta) - 0.4
    ax3.plot(x_smile, y_smile, 'k-', linewidth=3)
    ax3.text(3, 8.5, '💡', fontsize=30, ha='center')
    
    # Bayesian interpretation box
    bayes_box = FancyBboxPatch((4.5, 3.5), 5, 5.5, boxstyle="round,pad=0.1",
                               facecolor='#E0FFE0', edgecolor='green', linewidth=3)
    ax3.add_patch(bayes_box)
    ax3.text(7, 8.5, '🧠 Quan điểm Bayesian:', fontsize=11, ha='center', fontweight='bold')
    ax3.text(7, 7.8, '"70% = Độ tin cậy"', fontsize=12, ha='center', 
             style='italic', color='green', fontweight='bold')
    ax3.text(7, 7, '✅ Dựa trên thông tin:', fontsize=10, ha='center')
    ax3.text(7, 6.4, '• Nhiệt độ, độ ẩm', fontsize=9, ha='center')
    ax3.text(7, 5.9, '• Mô hình dự báo', fontsize=9, ha='center')
    ax3.text(7, 5.4, '• Kinh nghiệm lịch sử', fontsize=9, ha='center')
    ax3.text(7, 4.5, '→ Tôi tin 70% sẽ mưa!', 
             fontsize=11, ha='center', color='green', fontweight='bold')
    
    ax3.text(5, 0.5, 'Scene 3: Linh hiểu theo Bayesian - Tự nhiên hơn!', 
             fontsize=12, ha='center', style='italic')
    
    # Scene 4: Decision - Take umbrella
    ax4 = axes[1, 1]
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    ax4.axis('off')
    
    # Character with umbrella
    circle = Circle((3, 7), 0.8, color='#FFE4B5', ec='black', linewidth=2)
    ax4.add_patch(circle)
    ax4.plot([2.7, 3.3], [7.2, 7.2], 'ko', markersize=8)
    theta = np.linspace(3.5, 6, 30)
    x_smile = 3 + 0.5 * np.cos(theta)
    y_smile = 7 + 0.5 * np.sin(theta) - 0.4
    ax4.plot(x_smile, y_smile, 'k-', linewidth=3)
    
    # Umbrella
    umbrella_top = patches.Wedge((4.5, 6), 1.5, 0, 180, 
                                 facecolor='red', edgecolor='black', linewidth=2)
    ax4.add_patch(umbrella_top)
    ax4.plot([4.5, 4.5], [6, 3], 'k-', linewidth=4)
    ax4.plot([4.5, 5], [3, 2.5], 'k-', linewidth=3)
    
    # Rain
    for i in range(15):
        x = np.random.uniform(0.5, 9.5)
        y = np.random.uniform(8, 9.5)
        ax4.plot([x, x-0.1], [y, y-0.5], 'b-', linewidth=2, alpha=0.6)
    
    # Decision box
    decision_box = FancyBboxPatch((5.5, 5), 4, 3, boxstyle="round,pad=0.1",
                                  facecolor='#FFD700', edgecolor='orange', linewidth=3)
    ax4.add_patch(decision_box)
    ax4.text(7.5, 7.5, '🎯 Quyết định:', fontsize=12, ha='center', fontweight='bold')
    ax4.text(7.5, 6.8, 'Mang ô!', fontsize=14, ha='center', fontweight='bold', color='red')
    ax4.text(7.5, 6, '✅ Đúng là trời mưa!', fontsize=11, ha='center', color='green')
    
    ax4.text(5, 0.5, 'Scene 4: Linh mang ô - Quyết định đúng đắn!', 
             fontsize=12, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig('linh_umbrella_story.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: linh_umbrella_story.png")
    plt.close()

def create_coin_flip_comparison():
    """
    Cartoon 2: Coin Flip - Frequentist vs Bayesian
    Visual comparison of two approaches
    """
    fig, axes = plt.subplots(1, 2, figsize=(18, 10))
    fig.suptitle('Đồng xu của Bạn bè: Hai Cách Tiếp cận', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Left: Frequentist approach
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    # Title
    ax1.text(5, 9.5, '👨‍🔬 Nhà Thống kê Tần suất', 
             fontsize=16, ha='center', fontweight='bold', color='red')
    
    # Character with glasses (serious)
    circle = Circle((2, 7.5), 0.6, color='#FFE4B5', ec='black', linewidth=2)
    ax1.add_patch(circle)
    # Glasses
    ax1.add_patch(Circle((1.8, 7.6), 0.2, fill=False, ec='black', linewidth=2))
    ax1.add_patch(Circle((2.2, 7.6), 0.2, fill=False, ec='black', linewidth=2))
    ax1.plot([2, 2], [7.6, 7.6], 'k-', linewidth=2)
    # Serious expression
    ax1.plot([1.8, 2.2], [7.3, 7.3], 'k-', linewidth=2)
    
    # Analysis box
    analysis_box = FancyBboxPatch((3.5, 3), 6, 6, boxstyle="round,pad=0.15",
                                  facecolor='#FFE4E1', edgecolor='red', linewidth=3)
    ax1.add_patch(analysis_box)
    
    ax1.text(6.5, 8.5, '📊 Phân tích:', fontsize=13, ha='center', fontweight='bold')
    ax1.text(6.5, 7.9, 'Dữ liệu: 8 Ngửa / 10 lần', fontsize=11, ha='center')
    ax1.text(6.5, 7.3, '━━━━━━━━━━━━━━━━━━━━', fontsize=11, ha='center')
    ax1.text(6.5, 6.7, '1️⃣ Ước lượng điểm:', fontsize=11, ha='center', fontweight='bold')
    ax1.text(6.5, 6.2, 'θ̂ = 8/10 = 0.8', fontsize=12, ha='center', style='italic')
    ax1.text(6.5, 5.5, '2️⃣ Khoảng tin cậy 95%:', fontsize=11, ha='center', fontweight='bold')
    ax1.text(6.5, 5, '[0.49, 0.95]', fontsize=12, ha='center', style='italic', color='blue')
    ax1.text(6.5, 4.3, '⚠️ Diễn giải (phức tạp!):', fontsize=10, ha='center', fontweight='bold')
    ax1.text(6.5, 3.7, '"Nếu lặp lại vô số lần,\n95% khoảng sẽ chứa θ thực"', 
             fontsize=9, ha='center', style='italic')
    
    # Speech bubble
    bubble = FancyBboxPatch((0.5, 5), 2.5, 1.5, boxstyle="round,pad=0.1",
                           facecolor='white', edgecolor='black', linewidth=2)
    ax1.add_patch(bubble)
    ax1.text(1.75, 5.75, '"Tôi không thể nói\nxác suất của θ"', 
             fontsize=9, ha='center', va='center')
    # Arrow to bubble
    arrow = FancyArrowPatch((2, 7), (2, 6.5), arrowstyle='->', 
                           mutation_scale=20, linewidth=2)
    ax1.add_patch(arrow)
    
    # Right: Bayesian approach
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    # Title
    ax2.text(5, 9.5, '🧠 Nhà Thống kê Bayesian', 
             fontsize=16, ha='center', fontweight='bold', color='green')
    
    # Character (friendly)
    circle = Circle((2, 7.5), 0.6, color='#FFE4B5', ec='black', linewidth=2)
    ax2.add_patch(circle)
    ax2.plot([1.8, 2.2], [7.6, 7.6], 'ko', markersize=8)
    # Big smile
    theta = np.linspace(3.5, 6, 20)
    x_smile = 2 + 0.4 * np.cos(theta)
    y_smile = 7.5 + 0.4 * np.sin(theta) - 0.3
    ax2.plot(x_smile, y_smile, 'k-', linewidth=2)
    
    # Analysis box
    analysis_box = FancyBboxPatch((3.5, 2.5), 6, 6.5, boxstyle="round,pad=0.15",
                                  facecolor='#E0FFE0', edgecolor='green', linewidth=3)
    ax2.add_patch(analysis_box)
    
    ax2.text(6.5, 8.5, '🧠 Phân tích:', fontsize=13, ha='center', fontweight='bold')
    ax2.text(6.5, 7.9, 'Dữ liệu: 8 Ngửa / 10 lần', fontsize=11, ha='center')
    ax2.text(6.5, 7.3, '━━━━━━━━━━━━━━━━━━━━', fontsize=11, ha='center')
    ax2.text(6.5, 6.7, '1️⃣ Prior (niềm tin ban đầu):', fontsize=11, ha='center', fontweight='bold')
    ax2.text(6.5, 6.2, 'Beta(2, 2) ~ tin đồng xu công bằng', fontsize=10, ha='center')
    ax2.text(6.5, 5.6, '2️⃣ Likelihood (bằng chứng):', fontsize=11, ha='center', fontweight='bold')
    ax2.text(6.5, 5.1, 'Binomial(8|10, θ)', fontsize=10, ha='center', style='italic')
    ax2.text(6.5, 4.5, '3️⃣ Posterior (cập nhật):', fontsize=11, ha='center', fontweight='bold')
    ax2.text(6.5, 4, 'Beta(10, 4)', fontsize=10, ha='center', style='italic')
    ax2.text(6.5, 3.4, 'Trung bình: 0.71', fontsize=10, ha='center')
    ax2.text(6.5, 2.9, 'Khoảng 95%: [0.50, 0.89]', fontsize=10, ha='center', color='blue')
    
    # Speech bubble
    bubble = FancyBboxPatch((0.3, 4.5), 2.8, 2, boxstyle="round,pad=0.1",
                           facecolor='white', edgecolor='black', linewidth=2)
    ax2.add_patch(bubble)
    ax2.text(1.7, 5.5, '"Tôi tin 95% rằng\nθ nằm trong\n[0.50, 0.89]!"', 
             fontsize=9, ha='center', va='center', color='green', fontweight='bold')
    # Arrow to bubble
    arrow = FancyArrowPatch((2, 7), (2, 6.5), arrowstyle='->', 
                           mutation_scale=20, linewidth=2, color='green')
    ax2.add_patch(arrow)
    
    # Conclusion
    ax2.text(6.5, 1.5, '✅ Trả lời câu hỏi bạn quan tâm!', 
             fontsize=12, ha='center', fontweight='bold', color='green',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('coin_flip_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: coin_flip_comparison.png")
    plt.close()

def create_dutch_book_cartoon():
    """
    Cartoon 3: Dutch Book Argument
    Humorous illustration of inconsistent probabilities
    """
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Dutch Book: Khi Xác suất Không Nhất quán', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Create grid
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Panel 1: Your probabilities
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    ax1.text(5, 9, '📝 Xác suất của Bạn:', fontsize=14, ha='center', fontweight='bold')
    
    prob_box = FancyBboxPatch((1, 4), 8, 4.5, boxstyle="round,pad=0.15",
                              facecolor='#FFE4B5', edgecolor='black', linewidth=2)
    ax1.add_patch(prob_box)
    
    ax1.text(5, 7.8, 'P(A) = 0.6', fontsize=13, ha='center')
    ax1.text(5, 7.2, 'P(B) = 0.5', fontsize=13, ha='center')
    ax1.text(5, 6.6, 'P(A ∩ B) = 0.4', fontsize=13, ha='center')
    ax1.text(5, 6, 'P(A ∪ B) = 0.6', fontsize=13, ha='center')
    ax1.text(5, 5, '⚠️ Có gì đó sai sai...', fontsize=12, ha='center', 
             style='italic', color='red', fontweight='bold')
    
    # Panel 2: The gambler
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    ax2.text(5, 9, '🎰 Người Cá cược Thông minh:', fontsize=14, ha='center', fontweight='bold')
    
    # Evil character
    circle = Circle((3, 6.5), 0.8, color='#FFE4B5', ec='black', linewidth=2)
    ax2.add_patch(circle)
    ax2.plot([2.7, 3.3], [6.7, 6.7], 'ko', markersize=8)
    # Evil smile
    theta = np.linspace(3, 6.3, 30)
    x_smile = 3 + 0.5 * np.cos(theta)
    y_smile = 6.5 + 0.5 * np.sin(theta) - 0.4
    ax2.plot(x_smile, y_smile, 'r-', linewidth=3)
    
    # Money bag
    ax2.text(7, 6.5, '💰', fontsize=60, ha='center')
    
    # Speech bubble
    bubble = FancyBboxPatch((4, 4), 5, 2, boxstyle="round,pad=0.1",
                           facecolor='white', edgecolor='black', linewidth=2)
    ax2.add_patch(bubble)
    ax2.text(6.5, 5, '"Hehe... Tôi sẽ thiết lập\ncác cược để chắc chắn\nthắng tiền!"', 
             fontsize=10, ha='center', va='center', style='italic')
    
    # Panel 3: The bets
    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    
    ax3.text(5, 9.5, '🎲 Các Cược được Thiết lập:', fontsize=14, ha='center', fontweight='bold')
    
    # Bet boxes
    bet1 = FancyBboxPatch((0.5, 6), 2.8, 2.5, boxstyle="round,pad=0.1",
                          facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax3.add_patch(bet1)
    ax3.text(1.9, 8, 'Cược 1:', fontsize=11, ha='center', fontweight='bold')
    ax3.text(1.9, 7.5, 'A xảy ra', fontsize=10, ha='center')
    ax3.text(1.9, 7, 'Trả: 60đ', fontsize=10, ha='center')
    ax3.text(1.9, 6.5, 'Nhận: 100đ', fontsize=10, ha='center', color='green')
    
    bet2 = FancyBboxPatch((3.6, 6), 2.8, 2.5, boxstyle="round,pad=0.1",
                          facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax3.add_patch(bet2)
    ax3.text(5, 8, 'Cược 2:', fontsize=11, ha='center', fontweight='bold')
    ax3.text(5, 7.5, 'B xảy ra', fontsize=10, ha='center')
    ax3.text(5, 7, 'Trả: 50đ', fontsize=10, ha='center')
    ax3.text(5, 6.5, 'Nhận: 100đ', fontsize=10, ha='center', color='green')
    
    bet3 = FancyBboxPatch((6.7, 6), 2.8, 2.5, boxstyle="round,pad=0.1",
                          facecolor='#FFB6C1', edgecolor='black', linewidth=2)
    ax3.add_patch(bet3)
    ax3.text(8.1, 8, 'Cược 3:', fontsize=11, ha='center', fontweight='bold')
    ax3.text(8.1, 7.5, 'A∩B KHÔNG', fontsize=10, ha='center')
    ax3.text(8.1, 7, 'Trả: 60đ', fontsize=10, ha='center')
    ax3.text(8.1, 6.5, 'Nhận: 100đ', fontsize=10, ha='center', color='green')
    
    # Total
    total_box = FancyBboxPatch((1, 3), 8, 2, boxstyle="round,pad=0.15",
                               facecolor='#FFD700', edgecolor='red', linewidth=3)
    ax3.add_patch(total_box)
    ax3.text(5, 4.5, 'Tổng bạn trả: 60 + 50 + 60 = 170đ', 
             fontsize=12, ha='center', fontweight='bold')
    ax3.text(5, 3.8, '❌ Bạn LUÔN thua tiền bất kể kết quả!', 
             fontsize=12, ha='center', color='red', fontweight='bold')
    
    # Lesson
    lesson_box = FancyBboxPatch((1, 0.5), 8, 2, boxstyle="round,pad=0.15",
                                facecolor='#E0FFE0', edgecolor='green', linewidth=3)
    ax3.add_patch(lesson_box)
    ax3.text(5, 2, '💡 Bài học:', fontsize=12, ha='center', fontweight='bold')
    ax3.text(5, 1.5, 'Xác suất phải tuân theo quy tắc để nhất quán!', 
             fontsize=11, ha='center')
    ax3.text(5, 1, 'P(A ∪ B) = P(A) + P(B) - P(A ∩ B) = 0.6 + 0.5 - 0.4 = 0.7 ≠ 0.6', 
             fontsize=10, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig('dutch_book_cartoon.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: dutch_book_cartoon.png")
    plt.close()

def create_bayesian_daily_life():
    """
    Cartoon 4: You're Already Bayesian!
    Showing Bayesian thinking in everyday situations
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Bạn Đã Là Bayesian! - Tư duy Bayesian trong Cuộc sống', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # Situation 1: Strange noise at night
    ax1 = axes[0, 0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    ax1.text(5, 9.5, '🌙 Tình huống 1: Tiếng động lạ trong đêm', 
             fontsize=12, ha='center', fontweight='bold')
    
    # Dark background
    night_bg = Rectangle((0, 0), 10, 9, facecolor='#1a1a2e', alpha=0.3)
    ax1.add_patch(night_bg)
    
    # Person in bed
    bed = Rectangle((1, 3), 3, 1.5, facecolor='#8B4513', edgecolor='black', linewidth=2)
    ax1.add_patch(bed)
    blanket = Rectangle((1, 4.5), 3, 0.5, facecolor='#4169E1', edgecolor='black', linewidth=2)
    ax1.add_patch(blanket)
    # Head
    circle = Circle((2.5, 5.5), 0.4, color='#FFE4B5', ec='black', linewidth=2)
    ax1.add_patch(circle)
    ax1.plot([2.3, 2.7], [5.6, 5.6], 'ko', markersize=6)
    
    # Sound effect
    ax1.text(7, 7, '🔊', fontsize=40, ha='center')
    ax1.text(7, 6, 'THUMP!', fontsize=16, ha='center', fontweight='bold', color='red')
    
    # Thought process
    thought_box = FancyBboxPatch((4.5, 1), 5, 4.5, boxstyle="round,pad=0.1",
                                 facecolor='white', edgecolor='blue', linewidth=2)
    ax1.add_patch(thought_box)
    ax1.text(7, 5, '🧠 Suy nghĩ Bayesian:', fontsize=10, ha='center', fontweight='bold')
    ax1.text(7, 4.5, 'Prior:', fontsize=9, ha='center', fontweight='bold')
    ax1.text(7, 4.1, '• Mèo: 70%', fontsize=8, ha='center')
    ax1.text(7, 3.7, '• Gió: 25%', fontsize=8, ha='center')
    ax1.text(7, 3.3, '• Trộm: 5%', fontsize=8, ha='center')
    ax1.text(7, 2.7, 'Evidence: Bước chân nặng', fontsize=9, ha='center', style='italic')
    ax1.text(7, 2.2, 'Posterior:', fontsize=9, ha='center', fontweight='bold', color='red')
    ax1.text(7, 1.8, '• Trộm: 60% ⬆️', fontsize=8, ha='center', color='red')
    ax1.text(7, 1.4, '• Mèo: 10% ⬇️', fontsize=8, ha='center')
    
    # Situation 2: Choosing restaurant
    ax2 = axes[0, 1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    ax2.text(5, 9.5, '🍽️ Tình huống 2: Chọn Nhà hàng', 
             fontsize=12, ha='center', fontweight='bold')
    
    # Restaurant
    restaurant = Rectangle((1, 5), 3, 3, facecolor='#FFA07A', edgecolor='black', linewidth=2)
    ax2.add_patch(restaurant)
    ax2.text(2.5, 7.5, '🍜', fontsize=30, ha='center')
    ax2.text(2.5, 6.5, 'Nhà hàng A', fontsize=10, ha='center', fontweight='bold')
    
    # Stars (review)
    for i, x in enumerate([1.5, 2, 2.5, 3, 3.5]):
        ax2.text(x, 5.5, '⭐', fontsize=12, ha='center')
    
    # Update process
    update_box = FancyBboxPatch((4.5, 1), 5, 7.5, boxstyle="round,pad=0.15",
                                facecolor='#FFFACD', edgecolor='orange', linewidth=2)
    ax2.add_patch(update_box)
    
    ax2.text(7, 8, '🔄 Cập nhật Liên tục:', fontsize=11, ha='center', fontweight='bold')
    
    # Step 1
    ax2.text(7, 7.2, '1️⃣ Prior (từ review):', fontsize=9, ha='center', fontweight='bold')
    ax2.text(7, 6.8, '"Nhà hàng ngon": 70%', fontsize=9, ha='center')
    ax2.add_patch(Rectangle((5, 6.4), 4, 0.05, facecolor='green', alpha=0.7))
    
    # Step 2
    ax2.text(7, 5.8, '2️⃣ Evidence: Đông khách', fontsize=9, ha='center', fontweight='bold')
    ax2.text(7, 5.4, 'Update: 70% → 85% ⬆️', fontsize=9, ha='center', color='green')
    ax2.add_patch(Rectangle((5, 5, 0), 4.5, 0.05, facecolor='green', alpha=0.7))
    
    # Step 3
    ax2.text(7, 4.4, '3️⃣ Evidence: Món ăn chậm', fontsize=9, ha='center', fontweight='bold')
    ax2.text(7, 4, 'Update: 85% → 60% ⬇️', fontsize=9, ha='center', color='orange')
    ax2.add_patch(Rectangle((5, 3.6), 3.5, 0.05, facecolor='orange', alpha=0.7))
    
    # Step 4
    ax2.text(7, 3, '4️⃣ Evidence: Không ngon', fontsize=9, ha='center', fontweight='bold')
    ax2.text(7, 2.6, 'Update: 60% → 40% ⬇️', fontsize=9, ha='center', color='red')
    ax2.add_patch(Rectangle((5, 2.2), 2.5, 0.05, facecolor='red', alpha=0.7))
    
    ax2.text(7, 1.5, '❌ Quyết định: Không quay lại!', 
             fontsize=10, ha='center', fontweight='bold', color='red')
    
    # Situation 3: Weather decision
    ax3 = axes[1, 0]
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    
    ax3.text(5, 9.5, '☀️ Tình huống 3: Dự đoán Thời tiết', 
             fontsize=12, ha='center', fontweight='bold')
    
    # Sky
    sky = Rectangle((0, 5), 10, 4, facecolor='#87CEEB', alpha=0.5)
    ax3.add_patch(sky)
    
    # Sun
    sun = Circle((2, 7.5), 0.8, color='yellow', ec='orange', linewidth=2)
    ax3.add_patch(sun)
    
    # Clouds
    for x in [5, 6.5, 8]:
        cloud = Circle((x, 7), 0.5, color='white', ec='gray', linewidth=1)
        ax3.add_patch(cloud)
    
    # Bayesian process
    process_box = FancyBboxPatch((1, 0.5), 8, 4, boxstyle="round,pad=0.15",
                                 facecolor='white', edgecolor='blue', linewidth=2)
    ax3.add_patch(process_box)
    
    ax3.text(5, 4, '🧠 Quá trình Bayesian:', fontsize=11, ha='center', fontweight='bold')
    ax3.text(5, 3.4, 'Prior: "Mùa khô, ít mưa" → 20%', fontsize=9, ha='center')
    ax3.arrow(4, 3.1, 0, -0.3, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
    ax3.text(5, 2.6, 'Evidence: Mây đen kéo đến', fontsize=9, ha='center', style='italic')
    ax3.arrow(4, 2.3, 0, -0.3, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
    ax3.text(5, 1.8, 'Posterior: "Sẽ mưa" → 70%', fontsize=9, ha='center', color='blue')
    ax3.arrow(4, 1.5, 0, -0.3, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
    ax3.text(5, 1, '🌂 Action: Mang ô!', fontsize=10, ha='center', fontweight='bold', color='green')
    
    # Situation 4: Medical diagnosis
    ax4 = axes[1, 1]
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    ax4.axis('off')
    
    ax4.text(5, 9.5, '🏥 Tình huống 4: Chẩn đoán Y tế', 
             fontsize=12, ha='center', fontweight='bold')
    
    # Doctor
    circle = Circle((2, 6.5), 0.6, color='#FFE4B5', ec='black', linewidth=2)
    ax4.add_patch(circle)
    ax4.text(2, 7.5, '👨‍⚕️', fontsize=30, ha='center')
    
    # Patient
    circle2 = Circle((8, 6.5), 0.6, color='#FFE4B5', ec='black', linewidth=2)
    ax4.add_patch(circle2)
    ax4.text(8, 5.5, '🤒', fontsize=30, ha='center')
    
    # Diagnosis process
    diag_box = FancyBboxPatch((1, 0.5), 8, 4.5, boxstyle="round,pad=0.15",
                              facecolor='#E0FFE0', edgecolor='green', linewidth=2)
    ax4.add_patch(diag_box)
    
    ax4.text(5, 4.5, '🩺 Chẩn đoán Bayesian:', fontsize=11, ha='center', fontweight='bold')
    ax4.text(5, 3.9, 'Prior (theo mùa):', fontsize=9, ha='center', fontweight='bold')
    ax4.text(5, 3.5, 'Cảm cúm: 30%, COVID: 10%, Dị ứng: 60%', fontsize=8, ha='center')
    ax4.text(5, 3, 'Evidence: Sốt cao, ho, đau người', fontsize=9, ha='center', style='italic')
    ax4.text(5, 2.5, 'Posterior:', fontsize=9, ha='center', fontweight='bold')
    ax4.text(5, 2.1, 'Cảm cúm: 70% ⬆️', fontsize=9, ha='center', color='red', fontweight='bold')
    ax4.text(5, 1.7, 'COVID: 25% ⬆️', fontsize=9, ha='center')
    ax4.text(5, 1.3, 'Dị ứng: 5% ⬇️', fontsize=9, ha='center')
    ax4.text(5, 0.8, '💊 Điều trị: Thuốc cảm cúm + test COVID', 
             fontsize=9, ha='center', fontweight='bold', color='green')
    
    plt.tight_layout()
    plt.savefig('bayesian_daily_life.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: bayesian_daily_life.png")
    plt.close()

def main():
    """Generate all cartoon-style images"""
    print("\n" + "="*70)
    print("  GENERATING CARTOON-STYLE IMAGES FOR LESSON 1.2")
    print("  Inspired by: The Cartoon Guide & The Manga Guide to Statistics")
    print("="*70 + "\n")
    
    create_linh_umbrella_story()
    create_coin_flip_comparison()
    create_dutch_book_cartoon()
    create_bayesian_daily_life()
    
    print("\n" + "="*70)
    print("  ✅ ALL CARTOON IMAGES CREATED SUCCESSFULLY!")
    print("="*70)
    print("\nGenerated files:")
    print("  1. linh_umbrella_story.png - Linh's umbrella decision story")
    print("  2. coin_flip_comparison.png - Frequentist vs Bayesian comparison")
    print("  3. dutch_book_cartoon.png - Dutch Book argument illustration")
    print("  4. bayesian_daily_life.png - Bayesian thinking in daily life")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
