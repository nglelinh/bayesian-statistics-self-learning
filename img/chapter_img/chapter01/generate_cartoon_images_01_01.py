#!/usr/bin/env python3
"""
Generate Cartoon-Style Images for Lesson 1.1
Khủng hoảng Khoa học và Giới hạn của P-values

Inspired by:
- The Cartoon Guide to Statistics
- The Manga Guide to Statistics
- How to Lie with Statistics
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyArrow, FancyBboxPatch, Wedge
import matplotlib.patheffects as pe
import os

# Ensure output directory exists
output_dir = '/Users/nguyenlelinh/teaching/bayesian-statistics-self-learning/img/chapter_img/chapter01'
os.makedirs(output_dir, exist_ok=True)

# Set Vietnamese font support
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# --- Image 1: Dr. Sarah's Story ---
def create_sarah_story():
    """
    4-panel comic: Dr. Sarah's replication failure
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Câu chuyện của Dr. Sarah: Bi kịch Tái lập", 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Panel 1: Reading the paper
    ax = axes[0, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("1. Đọc paper trên Nature", fontsize=14, fontweight='bold')
    
    # Sarah reading
    ax.add_patch(Circle((0.3, 0.6), 0.08, color='peachpuff'))  # Head
    ax.add_patch(Rectangle((0.26, 0.4), 0.08, 0.2, color='lightblue'))  # Body
    
    # Paper
    ax.add_patch(Rectangle((0.4, 0.5), 0.3, 0.4, color='white', 
                           edgecolor='black', linewidth=2))
    ax.text(0.55, 0.8, 'NATURE', ha='center', fontsize=12, 
            fontweight='bold', color='red')
    ax.text(0.55, 0.7, 'Compound X', ha='center', fontsize=10)
    ax.text(0.55, 0.65, 'kills cancer!', ha='center', fontsize=10)
    ax.text(0.55, 0.58, 'p < 0.001', ha='center', fontsize=12, 
            fontweight='bold', color='green',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Speech bubble
    ax.text(0.3, 0.85, "Wow! Phát hiện\nđột phá!", ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=2))
    
    ax.axis('off')
    
    # Panel 2: Working in lab
    ax = axes[0, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("2. Làm việc 6 tháng trong lab", fontsize=14, fontweight='bold')
    
    # Lab equipment
    ax.add_patch(Rectangle((0.2, 0.3), 0.15, 0.25, color='lightgray', 
                           edgecolor='black', linewidth=2))
    ax.text(0.275, 0.4, 'LAB', ha='center', fontsize=8)
    
    # Sarah working
    ax.add_patch(Circle((0.5, 0.6), 0.08, color='peachpuff'))
    ax.add_patch(Rectangle((0.46, 0.4), 0.08, 0.2, color='lightblue'))
    
    # Sweat drops
    for x, y in [(0.45, 0.7), (0.55, 0.72), (0.48, 0.75)]:
        ax.add_patch(Circle((x, y), 0.02, color='lightblue', alpha=0.7))
    
    # Clock showing late night
    circle = Circle((0.8, 0.8), 0.1, color='white', edgecolor='black', linewidth=2)
    ax.add_patch(circle)
    ax.plot([0.8, 0.8], [0.8, 0.88], 'k-', linewidth=2)  # Hour hand
    ax.plot([0.8, 0.85], [0.8, 0.8], 'k-', linewidth=1.5)  # Minute hand
    ax.text(0.8, 0.65, '3:00 AM', ha='center', fontsize=10, fontweight='bold')
    
    # Money spent
    ax.text(0.5, 0.15, '$50,000 spent', ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax.axis('off')
    
    # Panel 3: Disappointing results
    ax = axes[1, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("3. Kết quả thất vọng", fontsize=14, fontweight='bold')
    
    # Computer screen
    ax.add_patch(Rectangle((0.3, 0.4), 0.4, 0.35, color='lightblue', 
                           edgecolor='black', linewidth=3))
    ax.text(0.5, 0.65, 'RESULTS', ha='center', fontsize=12, fontweight='bold')
    ax.text(0.5, 0.55, 'p = 0.67', ha='center', fontsize=16, 
            fontweight='bold', color='red',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    ax.text(0.5, 0.45, 'No effect!', ha='center', fontsize=10, color='red')
    
    # Sad Sarah
    ax.add_patch(Circle((0.2, 0.6), 0.08, color='peachpuff'))
    ax.add_patch(Rectangle((0.16, 0.4), 0.08, 0.2, color='lightblue'))
    # Sad face
    ax.plot([0.18, 0.18], [0.62, 0.61], 'k-', linewidth=2)  # Left eye
    ax.plot([0.22, 0.22], [0.62, 0.61], 'k-', linewidth=2)  # Right eye
    ax.add_patch(Wedge((0.2, 0.58), 0.03, 200, 340, color='black'))  # Sad mouth
    
    # Thought bubble
    ax.text(0.2, 0.85, "Tại sao...?\n6 tháng công sức...", 
            ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', 
                     edgecolor='black', linewidth=2))
    
    ax.axis('off')
    
    # Panel 4: The truth revealed
    ax = axes[1, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("4. Sự thật được tiết lộ", fontsize=14, fontweight='bold')
    
    # Phone conversation
    ax.add_patch(Rectangle((0.15, 0.5), 0.3, 0.35, color='lightyellow', 
                           edgecolor='black', linewidth=2))
    ax.text(0.3, 0.78, 'Original Author:', ha='center', fontsize=9, 
            fontweight='bold')
    ax.text(0.3, 0.70, '"Chúng tôi test', ha='center', fontsize=8)
    ax.text(0.3, 0.65, '15 compounds', ha='center', fontsize=8)
    ax.text(0.3, 0.60, 'X là cái duy nhất', ha='center', fontsize=8)
    ax.text(0.3, 0.55, 'có p < 0.05"', ha='center', fontsize=8)
    
    # P-HACKING label
    ax.text(0.3, 0.35, 'P-HACKING!', ha='center', fontsize=14, 
            fontweight='bold', color='red',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', 
                     edgecolor='red', linewidth=3))
    
    # Angry Sarah
    ax.add_patch(Circle((0.7, 0.6), 0.08, color='peachpuff'))
    ax.add_patch(Rectangle((0.66, 0.4), 0.08, 0.2, color='lightblue'))
    # Angry face
    ax.plot([0.68, 0.67], [0.62, 0.61], 'k-', linewidth=2)  # Left eye
    ax.plot([0.72, 0.73], [0.62, 0.61], 'k-', linewidth=2)  # Right eye
    ax.plot([0.66, 0.74], [0.57, 0.57], 'r-', linewidth=2)  # Angry mouth
    
    # Anger marks
    for x, y in [(0.62, 0.7), (0.78, 0.7), (0.7, 0.75)]:
        ax.text(x, y, '!', fontsize=16, color='red', fontweight='bold')
    
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sarah_replication_story.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 2: Replication Crisis Statistics ---
def create_replication_crisis_stats():
    """
    Bar chart showing replication rates across fields
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    fields = ['Tâm lý học\n(2015)', 'Y học\ntiền lâm sàng\n(2012)', 
              'Sinh học\n(2016)', 'Kinh tế\n(2016)']
    replication_rates = [36, 11, 25, 61]
    colors = ['#ff6b6b', '#ee5a6f', '#ff8787', '#ffa07a']
    
    bars = ax.bar(fields, replication_rates, color=colors, edgecolor='black', 
                  linewidth=2, alpha=0.8)
    
    # Add value labels on bars
    for i, (bar, rate) in enumerate(zip(bars, replication_rates)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{rate}%', ha='center', va='bottom', fontsize=14, 
                fontweight='bold')
    
    # Add 50% reference line
    ax.axhline(y=50, color='green', linestyle='--', linewidth=2, 
               label='50% (Acceptable)')
    
    # Add danger zone
    ax.axhspan(0, 50, alpha=0.2, color='red', label='Danger Zone')
    
    ax.set_ylabel('Tỷ lệ tái lập thành công (%)', fontsize=14, fontweight='bold')
    ax.set_title('KHỦNG HOẢNG TÁI LẬP: Tỷ lệ nghiên cứu tái lập thành công', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    # Add warning text
    ax.text(0.5, 0.95, '⚠️ CẢNH BÁO: Đa số nghiên cứu KHÔNG tái lập được!', 
            transform=ax.transAxes, ha='center', fontsize=13, 
            fontweight='bold', color='red',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', 
                     edgecolor='red', linewidth=3, alpha=0.9))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'replication_crisis_stats.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 3: P-value Misconceptions ---
def create_pvalue_misconceptions():
    """
    Visual guide to common p-value misconceptions
    """
    fig, axes = plt.subplots(3, 2, figsize=(16, 18))
    fig.suptitle('5 HIỂU LẦM CHẾT NGƯỜI VỀ P-VALUES', 
                 fontsize=18, fontweight='bold', y=0.995)
    
    misconceptions = [
        {
            'title': 'Hiểu lầm 1: P-value = P(H₀ đúng)',
            'wrong': 'p = 0.03\n→ H₀ có 3%\nxác suất đúng',
            'right': 'p = P(data|H₀)\nKHÔNG PHẢI\nP(H₀|data)',
            'explanation': 'H₀ không phải\nbiến ngẫu nhiên!'
        },
        {
            'title': 'Hiểu lầm 2: 1-p = P(H₁ đúng)',
            'wrong': 'p = 0.01\n→ H₁ có 99%\nxác suất đúng',
            'right': 'Có thể có\nNHIỀU H₁\nkhác nhau',
            'explanation': 'P-value không\nnói gì về H₁!'
        },
        {
            'title': 'Hiểu lầm 3: p<0.05 = "Có ý nghĩa"',
            'wrong': 'p = 0.049 ✅\np = 0.051 ❌',
            'right': 'Ngưỡng 0.05\nhoàn toàn\nTÙY Ý',
            'explanation': 'Fisher chọn\n0.05 năm 1925\nvì tiện!'
        },
        {
            'title': 'Hiểu lầm 4: p nhỏ = Hiệu ứng lớn',
            'wrong': 'p < 0.001\n→ Hiệu ứng\nrất mạnh!',
            'right': 'p phụ thuộc\nCẢ effect size\nVÀ sample size',
            'explanation': 'Mẫu lớn + hiệu ứng\nnhỏ → p nhỏ!'
        },
        {
            'title': 'Hiểu lầm 5: p>0.05 = H₀ đúng',
            'wrong': 'p = 0.30\n→ H₀ đúng\nKhông có hiệu ứng',
            'right': 'Có thể mẫu\nquá nhỏ\n(low power)',
            'explanation': 'Absence of evidence\n≠ Evidence of absence'
        },
    ]
    
    for idx, (ax, misconception) in enumerate(zip(axes.flat, misconceptions)):
        if idx >= len(misconceptions):
            ax.axis('off')
            continue
            
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(misconception['title'], fontsize=12, fontweight='bold', pad=10)
        
        # Wrong box (left)
        ax.add_patch(Rectangle((0.05, 0.3), 0.35, 0.5, 
                               facecolor='#ffcccc', edgecolor='red', linewidth=3))
        ax.text(0.225, 0.75, '❌ SAI', ha='center', fontsize=11, 
                fontweight='bold', color='red')
        ax.text(0.225, 0.55, misconception['wrong'], ha='center', va='center',
                fontsize=9, multialignment='center')
        
        # Right box (right)
        ax.add_patch(Rectangle((0.6, 0.3), 0.35, 0.5, 
                               facecolor='#ccffcc', edgecolor='green', linewidth=3))
        ax.text(0.775, 0.75, '✅ ĐÚNG', ha='center', fontsize=11, 
                fontweight='bold', color='green')
        ax.text(0.775, 0.55, misconception['right'], ha='center', va='center',
                fontsize=9, multialignment='center')
        
        # Arrow
        ax.annotate('', xy=(0.6, 0.55), xytext=(0.4, 0.55),
                   arrowprops=dict(arrowstyle='->', lw=3, color='black'))
        
        # Explanation box (bottom)
        ax.text(0.5, 0.12, misconception['explanation'], 
                ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                         edgecolor='orange', linewidth=2),
                multialignment='center')
        
        ax.axis('off')
    
    # Last panel: Summary
    ax = axes.flat[5]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('💡 BÀI HỌC', fontsize=14, fontweight='bold', pad=10)
    
    summary_text = """
    P-values BỊ HIỂU SAI
    RẤT NHIỀU!
    
    Ngay cả các nhà khoa học
    cũng thường nhầm lẫn
    
    → Cần cách tiếp cận tốt hơn
    → BAYESIAN!
    """
    
    ax.text(0.5, 0.5, summary_text, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', 
                     edgecolor='blue', linewidth=3),
            multialignment='center')
    
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'pvalue_misconceptions.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 4: P-hacking Techniques ---
def create_phacking_techniques():
    """
    Cartoon illustration of p-hacking techniques
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('🎣 P-HACKING: 6 KỸ THUẬT PHỔ BIẾN', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    techniques = [
        {
            'title': '1. Cherry-picking\nOutcomes',
            'desc': 'Test 20 biến\nChỉ báo cáo\ncái p < 0.05',
            'icon': '🍒'
        },
        {
            'title': '2. Optional\nStopping',
            'desc': 'Thu thập dữ liệu\nKiểm tra p-value\nDừng khi p < 0.05',
            'icon': '🛑'
        },
        {
            'title': '3. Outlier\nRemoval',
            'desc': 'Loại bỏ outliers\ncó chọn lọc\nđể giảm p',
            'icon': '🗑️'
        },
        {
            'title': '4. Subgroup\nAnalysis',
            'desc': 'Chia nhiều nhóm\nTest từng nhóm\nBáo cáo nhóm tốt nhất',
            'icon': '✂️'
        },
        {
            'title': '5. Multiple\nTests',
            'desc': 'Thử nhiều tests\nkhác nhau\nChọn cái cho p nhỏ',
            'icon': '🎰'
        },
        {
            'title': '6. HARKing',
            'desc': 'Hypothesizing\nAfter Results\nare Known',
            'icon': '🔮'
        },
    ]
    
    for ax, tech in zip(axes.flat, techniques):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_title(tech['title'], fontsize=12, fontweight='bold')
        
        # Icon
        ax.text(0.5, 0.7, tech['icon'], ha='center', fontsize=48)
        
        # Description
        ax.text(0.5, 0.35, tech['desc'], ha='center', va='center', 
                fontsize=10, multialignment='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                         edgecolor='red', linewidth=2))
        
        # Warning
        ax.add_patch(Rectangle((0.1, 0.05), 0.8, 0.12, 
                               facecolor='red', alpha=0.3))
        ax.text(0.5, 0.11, '⚠️ INCREASES FALSE POSITIVES', 
                ha='center', fontsize=8, fontweight='bold', color='red')
        
        ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'phacking_techniques.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 5: Publication Bias (File Drawer) ---
def create_publication_bias():
    """
    Illustration of the file drawer problem
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('📁 PUBLICATION BIAS: "File Drawer Problem"', 
                 fontsize=18, fontweight='bold')
    
    # Left panel: What actually happened
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_title('THỰC TẾ: 20 labs test cùng giả thuyết SAI', 
                  fontsize=14, fontweight='bold')
    
    # Draw 20 labs
    np.random.seed(42)
    for i in range(20):
        row = i // 5
        col = i % 5
        x = 0.1 + col * 0.18
        y = 0.75 - row * 0.18
        
        # Lab icon
        ax1.add_patch(Rectangle((x, y), 0.12, 0.12, 
                                facecolor='lightgray', edgecolor='black', linewidth=1))
        ax1.text(x + 0.06, y + 0.09, f'Lab {i+1}', ha='center', fontsize=7)
        
        # Result
        if i == 19:  # One false positive
            ax1.text(x + 0.06, y + 0.04, 'p=0.04', ha='center', fontsize=7, 
                    color='green', fontweight='bold')
            ax1.text(x + 0.06, y - 0.03, '✅', ha='center', fontsize=12)
        else:
            ax1.text(x + 0.06, y + 0.04, 'p>0.05', ha='center', fontsize=7, 
                    color='red')
            ax1.text(x + 0.06, y - 0.03, '❌', ha='center', fontsize=12)
    
    # Summary
    ax1.text(0.5, 0.08, '19 labs: p > 0.05 (negative)\n1 lab: p < 0.05 (false positive)', 
            ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', 
                     edgecolor='black', linewidth=2))
    
    ax1.axis('off')
    
    # Right panel: What gets published
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title('ĐƯỢC PUBLISH: Chỉ kết quả "positive"', 
                  fontsize=14, fontweight='bold')
    
    # File drawer (bottom)
    ax2.add_patch(Rectangle((0.1, 0.1), 0.8, 0.4, 
                            facecolor='gray', edgecolor='black', linewidth=3))
    ax2.text(0.5, 0.3, '📁 FILE DRAWER', ha='center', fontsize=14, 
            fontweight='bold', color='white')
    ax2.text(0.5, 0.2, '19 negative results\n(GIẤU ĐI)', ha='center', 
            fontsize=11, color='white', multialignment='center')
    
    # Published paper (top)
    ax2.add_patch(Rectangle((0.25, 0.6), 0.5, 0.3, 
                            facecolor='white', edgecolor='black', linewidth=3))
    ax2.text(0.5, 0.85, '📰 PUBLISHED!', ha='center', fontsize=14, 
            fontweight='bold', color='green')
    ax2.text(0.5, 0.75, 'Lab 20: p < 0.05', ha='center', fontsize=11)
    ax2.text(0.5, 0.68, '(False positive)', ha='center', fontsize=9, 
            color='red', style='italic')
    
    # Arrow
    ax2.annotate('', xy=(0.5, 0.6), xytext=(0.5, 0.5),
                arrowprops=dict(arrowstyle='->', lw=4, color='red'))
    
    # Warning
    ax2.text(0.5, 0.05, '⚠️ Literature: 100% nghiên cứu "hỗ trợ" giả thuyết\n'
                       'Thực tế: Giả thuyết SAI!', 
            ha='center', fontsize=11, fontweight='bold', color='red',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', 
                     edgecolor='red', linewidth=3))
    
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'publication_bias.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 6: Frequentist vs Bayesian Comparison ---
def create_frequentist_vs_bayesian():
    """
    Side-by-side comparison of approaches
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    fig.suptitle('⚔️ FREQUENTIST vs BAYESIAN', 
                 fontsize=18, fontweight='bold')
    
    # Frequentist panel
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_title('FREQUENTIST (P-value)', fontsize=14, fontweight='bold', 
                  color='red')
    
    freq_items = [
        ('Câu hỏi:', 'P(data | H₀)', 0.85),
        ('Tham số:', 'Cố định, không biết', 0.75),
        ('Prior:', 'KHÔNG sử dụng', 0.65),
        ('Output:', 'P-value (một số)', 0.55),
        ('Diễn giải:', 'Phức tạp, dễ sai', 0.45),
        ('Quyết định:', 'Nhị phân (reject/not)', 0.35),
        ('Multiple tests:', 'Cần điều chỉnh', 0.25),
    ]
    
    for label, value, y in freq_items:
        ax1.text(0.15, y, label, fontsize=11, fontweight='bold')
        ax1.text(0.55, y, value, fontsize=11,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffcccc', 
                         edgecolor='red', linewidth=1))
    
    # Problems
    ax1.text(0.5, 0.12, '❌ PROBLEMS', ha='center', fontsize=12, 
            fontweight='bold', color='red')
    ax1.text(0.5, 0.05, 'Dễ hiểu sai\nDễ bị thao túng\nKhông trả lời câu hỏi quan tâm', 
            ha='center', fontsize=9, multialignment='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', 
                     edgecolor='red', linewidth=2))
    
    ax1.axis('off')
    
    # Bayesian panel
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title('BAYESIAN', fontsize=14, fontweight='bold', color='green')
    
    bayes_items = [
        ('Câu hỏi:', 'P(H | data)', 0.85),
        ('Tham số:', 'Biến ngẫu nhiên', 0.75),
        ('Prior:', 'Tích hợp tự nhiên', 0.65),
        ('Output:', 'Posterior distribution', 0.55),
        ('Diễn giải:', 'Trực tiếp, trực quan', 0.45),
        ('Quyết định:', 'Liên tục (degree)', 0.35),
        ('Multiple tests:', 'Tự nhiên xử lý', 0.25),
    ]
    
    for label, value, y in bayes_items:
        ax2.text(0.15, y, label, fontsize=11, fontweight='bold')
        ax2.text(0.55, y, value, fontsize=11,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#ccffcc', 
                         edgecolor='green', linewidth=1))
    
    # Advantages
    ax2.text(0.5, 0.12, '✅ ADVANTAGES', ha='center', fontsize=12, 
            fontweight='bold', color='green')
    ax2.text(0.5, 0.05, 'Diễn giải tự nhiên\nTích hợp prior knowledge\nĐịnh lượng uncertainty', 
            ha='center', fontsize=9, multialignment='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', 
                     edgecolor='green', linewidth=2))
    
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'frequentist_vs_bayesian_comparison.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Main execution ---
if __name__ == "__main__":
    print("="*80)
    print("  GENERATING CARTOON-STYLE IMAGES FOR LESSON 1.1")
    print("  Khủng hoảng Khoa học và Giới hạn của P-values")
    print("="*80)
    
    print("\n[1/6] Creating Dr. Sarah's story...")
    create_sarah_story()
    print("✅ Created: sarah_replication_story.png")
    
    print("\n[2/6] Creating replication crisis statistics...")
    create_replication_crisis_stats()
    print("✅ Created: replication_crisis_stats.png")
    
    print("\n[3/6] Creating p-value misconceptions...")
    create_pvalue_misconceptions()
    print("✅ Created: pvalue_misconceptions.png")
    
    print("\n[4/6] Creating p-hacking techniques...")
    create_phacking_techniques()
    print("✅ Created: phacking_techniques.png")
    
    print("\n[5/6] Creating publication bias illustration...")
    create_publication_bias()
    print("✅ Created: publication_bias.png")
    
    print("\n[6/6] Creating Frequentist vs Bayesian comparison...")
    create_frequentist_vs_bayesian()
    print("✅ Created: frequentist_vs_bayesian_comparison.png")
    
    print("\n" + "="*80)
    print("  ✅ ALL CARTOON IMAGES CREATED SUCCESSFULLY!")
    print("="*80)
    
    print("\nGenerated files:")
    print("  1. sarah_replication_story.png - Dr. Sarah's tragic story")
    print("  2. replication_crisis_stats.png - Statistics across fields")
    print("  3. pvalue_misconceptions.png - 5 deadly misconceptions")
    print("  4. phacking_techniques.png - 6 common p-hacking techniques")
    print("  5. publication_bias.png - File drawer problem")
    print("  6. frequentist_vs_bayesian_comparison.png - Side-by-side comparison")
    print("\n" + "="*80)
