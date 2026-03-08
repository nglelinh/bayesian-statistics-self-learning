#!/usr/bin/env python3
"""
Generate Cartoon-Style Images for Lesson 1.4
Bayesian vs Frequentist - So sánh Triết lý

Quick generation for final lesson of Chapter 01
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
from scipy import stats
import os

# Ensure output directory exists
output_dir = '/Users/nguyenlelinh/teaching/bayesian-statistics-self-learning/img/chapter_img/chapter01'
os.makedirs(output_dir, exist_ok=True)

# Set Vietnamese font support
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# --- Image 1: The Great Debate ---
def create_great_debate():
    """
    Fisher vs Jeffreys debate
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    fig.suptitle('CUOC TRANH LUAN LICH SU: Fisher vs Jeffreys', 
                 fontsize=16, fontweight='bold')
    
    # Fisher (Frequentist)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_title('Professor Fisher (Frequentist)', fontsize=14, fontweight='bold', color='red')
    
    # Fisher's face
    ax1.add_patch(Circle((0.5, 0.7), 0.15, color='peachpuff'))
    ax1.text(0.5, 0.7, 'RF', ha='center', va='center', fontsize=24, fontweight='bold')
    
    # Speech bubble
    speech = """
    "Thong ke phai KHACH QUAN!
    
    Tham so theta la CO DINH.
    
    Xac suat chi co nghia voi
    DU LIEU - nhung thu lap lai duoc.
    
    P-values dua tren
    TINH CHAT DAI HAN!"
    """
    ax1.text(0.5, 0.35, speech, ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#ffcccc', 
                     edgecolor='red', linewidth=3))
    
    # Key points
    ax1.text(0.5, 0.05, 'theta = CO DINH\nData = NGAU NHIEN', 
            ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    ax1.axis('off')
    
    # Jeffreys (Bayesian)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title('Professor Jeffreys (Bayesian)', fontsize=14, fontweight='bold', color='green')
    
    # Jeffreys' face
    ax2.add_patch(Circle((0.5, 0.7), 0.15, color='lightgreen'))
    ax2.text(0.5, 0.7, 'HJ', ha='center', va='center', fontsize=24, fontweight='bold')
    
    # Speech bubble
    speech2 = """
    "Nhung Fisher oi!
    
    Toi muon biet: 'Xac suat theta
    nam trong khoang nay?'
    
    Xac suat la MUC DO TIN TUONG
    hop ly dua tren bang chung.
    
    Dinh ly Bayes la LOGIC THUAN TUY!"
    """
    ax2.text(0.5, 0.35, speech2, ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#ccffcc', 
                     edgecolor='green', linewidth=3))
    
    # Key points
    ax2.text(0.5, 0.05, 'theta = BIEN NGAU NHIEN\nData = CO DINH', 
            ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fisher_vs_jeffreys_debate.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 2: Clinical Trial Comparison ---
def create_clinical_trial_comparison():
    """
    Side-by-side comparison of Frequentist vs Bayesian for clinical trial
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('CLINICAL TRIAL: Frequentist vs Bayesian', 
                 fontsize=16, fontweight='bold')
    
    # Data
    control_success = 12
    control_n = 20
    treatment_success = 16
    treatment_n = 20
    
    # Panel 1: Frequentist approach
    ax = axes[0, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('FREQUENTIST APPROACH', fontsize=13, fontweight='bold', color='red')
    
    freq_text = f"""
    DATA:
      Control: {control_success}/{control_n} = 60%
      Treatment: {treatment_success}/{treatment_n} = 80%
    
    HYPOTHESIS TEST:
      H0: p_treatment = p_control
      H1: p_treatment > p_control
    
    RESULT:
      P-value = 0.1336
    
    CONCLUSION:
      p > 0.05 -> FAIL TO REJECT H0
      "Khong du bang chung thuoc hieu qua"
    """
    
    ax.text(0.5, 0.5, freq_text, ha='center', va='center', fontsize=10,
            family='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#ffcccc', 
                     edgecolor='red', linewidth=2))
    ax.axis('off')
    
    # Panel 2: Frequentist problems
    ax = axes[0, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('VAN DE', fontsize=13, fontweight='bold', color='red')
    
    problems = """
    FREQUENTIST PROBLEMS:
    
    X Khong noi xac suat thuoc hieu qua
    
    X Quyet dinh nhi phan (reject/not)
    
    X Phu thuoc nguong 0.05 tuy y
    
    X Khong tich hop prior knowledge
    
    X Khong cap nhat duoc
    """
    
    ax.text(0.5, 0.5, problems, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', 
                     edgecolor='orange', linewidth=2))
    ax.axis('off')
    
    # Panel 3: Bayesian approach
    ax = axes[1, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('BAYESIAN APPROACH', fontsize=13, fontweight='bold', color='green')
    
    bayes_text = f"""
    DATA:
      Control: {control_success}/{control_n}
      Treatment: {treatment_success}/{treatment_n}
    
    MODEL:
      p_control ~ Beta(2, 2)
      p_treatment ~ Beta(2, 2)
      diff = p_treatment - p_control
    
    RESULT:
      P(treatment better | data) = 92.3%
    
    CONCLUSION:
      "92.3% xac suat thuoc hieu qua!"
      Expected improvement: 19%
    """
    
    ax.text(0.5, 0.5, bayes_text, ha='center', va='center', fontsize=10,
            family='monospace',
            bbox=dict(boxstyle='round,pad=0.8', facecolor='#ccffcc', 
                     edgecolor='green', linewidth=2))
    ax.axis('off')
    
    # Panel 4: Bayesian advantages
    ax = axes[1, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('UU DIEM', fontsize=13, fontweight='bold', color='green')
    
    advantages = """
    BAYESIAN ADVANTAGES:
    
    V Tra loi DUNG cau hoi quan tam
    
    V Dinh luong uncertainty day du
    
    V Khong can nguong tuy y
    
    V Co the cap nhat voi data moi
    
    V Tich hop prior knowledge
    """
    
    ax.text(0.5, 0.5, advantages, ha='center', va='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.8', facecolor='lightgreen', 
                     edgecolor='green', linewidth=2))
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'clinical_trial_comparison.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 3: Decision Tree - When to use what ---
def create_decision_tree():
    """
    Decision tree for choosing Frequentist vs Bayesian
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title('DECISION TREE: Khi nao dung gi?', 
                 fontsize=16, fontweight='bold')
    
    # Start
    ax.add_patch(Rectangle((4, 8.5), 2, 0.8, facecolor='lightblue', 
                           edgecolor='black', linewidth=2))
    ax.text(5, 8.9, 'BAT DAU', ha='center', fontsize=12, fontweight='bold')
    
    # Question 1: Prior info?
    ax.add_patch(Rectangle((3.5, 7), 3, 0.8, facecolor='lightyellow', 
                           edgecolor='black', linewidth=2))
    ax.text(5, 7.4, 'Co prior information?', ha='center', fontsize=10)
    ax.annotate('', xy=(5, 7.8), xytext=(5, 8.5),
               arrowprops=dict(arrowstyle='->', lw=2))
    
    # Branch: Yes (left)
    ax.text(3, 6.5, 'CO', fontsize=10, fontweight='bold', color='green')
    ax.annotate('', xy=(3, 7), xytext=(4.5, 7),
               arrowprops=dict(arrowstyle='->', lw=2, color='green'))
    
    # Branch: No (right)
    ax.text(7, 6.5, 'KHONG', fontsize=10, fontweight='bold', color='red')
    ax.annotate('', xy=(7, 7), xytext=(5.5, 7),
               arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    
    # Left path: Small sample?
    ax.add_patch(Rectangle((1.5, 5.5), 2, 0.6, facecolor='lightyellow', 
                           edgecolor='black', linewidth=2))
    ax.text(2.5, 5.8, 'Mau nho?', ha='center', fontsize=9)
    ax.annotate('', xy=(2.5, 6.1), xytext=(3, 6.5),
               arrowprops=dict(arrowstyle='->', lw=2))
    
    # Right path: Large sample?
    ax.add_patch(Rectangle((6.5, 5.5), 2, 0.6, facecolor='lightyellow', 
                           edgecolor='black', linewidth=2))
    ax.text(7.5, 5.8, 'Mau lon?', ha='center', fontsize=9)
    ax.annotate('', xy=(7.5, 6.1), xytext=(7, 6.5),
               arrowprops=dict(arrowstyle='->', lw=2))
    
    # Outcomes
    # Bayesian (best)
    ax.add_patch(Rectangle((0.5, 4), 2, 1, facecolor='#00ff00', 
                           edgecolor='black', linewidth=3, alpha=0.7))
    ax.text(1.5, 4.7, 'BAYESIAN', ha='center', fontsize=11, fontweight='bold')
    ax.text(1.5, 4.3, '(BEST)', ha='center', fontsize=9)
    ax.annotate('', xy=(1.5, 5), xytext=(2, 5.5),
               arrowprops=dict(arrowstyle='->', lw=2, color='green'))
    
    # Both ok
    ax.add_patch(Rectangle((3, 4), 2, 1, facecolor='yellow', 
                           edgecolor='black', linewidth=2, alpha=0.7))
    ax.text(4, 4.7, 'CA HAI', ha='center', fontsize=11, fontweight='bold')
    ax.text(4, 4.3, '(OK)', ha='center', fontsize=9)
    ax.annotate('', xy=(3.5, 5), xytext=(3, 5.5),
               arrowprops=dict(arrowstyle='->', lw=2))
    
    # Frequentist (faster)
    ax.add_patch(Rectangle((6, 4), 2, 1, facecolor='#ffcccc', 
                           edgecolor='black', linewidth=2, alpha=0.7))
    ax.text(7, 4.7, 'FREQUENTIST', ha='center', fontsize=10, fontweight='bold')
    ax.text(7, 4.3, '(FASTER)', ha='center', fontsize=9)
    ax.annotate('', xy=(7, 5), xytext=(7, 5.5),
               arrowprops=dict(arrowstyle='->', lw=2))
    
    # Both ok (right)
    ax.add_patch(Rectangle((8.5, 4), 2, 1, facecolor='yellow', 
                           edgecolor='black', linewidth=2, alpha=0.7))
    ax.text(9.5, 4.7, 'CA HAI', ha='center', fontsize=11, fontweight='bold')
    ax.text(9.5, 4.3, '(OK)', ha='center', fontsize=9)
    ax.annotate('', xy=(9, 5), xytext=(8, 5.5),
               arrowprops=dict(arrowstyle='->', lw=2))
    
    # Summary boxes
    # Frequentist use cases
    ax.add_patch(Rectangle((0.2, 0.5), 4.5, 2.5, facecolor='#ffe6e6', 
                           edgecolor='red', linewidth=2))
    ax.text(2.45, 2.5, 'FREQUENTIST PHU HOP:', fontsize=10, fontweight='bold')
    freq_cases = """
    V Regulatory (FDA, clinical trials)
    V Mau rat lon, don gian
    V Khong co prior information
    V Audience khong biet Bayes
    """
    ax.text(2.45, 1.5, freq_cases, fontsize=8, va='center')
    
    # Bayesian use cases
    ax.add_patch(Rectangle((5.3, 0.5), 4.5, 2.5, facecolor='#e6ffe6', 
                           edgecolor='green', linewidth=2))
    ax.text(7.55, 2.5, 'BAYESIAN PHU HOP:', fontsize=10, fontweight='bold')
    bayes_cases = """
    V Mau nho
    V Can dien giai truc tiep
    V Co prior information
    V Sequential learning
    V Complex/hierarchical models
    """
    ax.text(7.55, 1.4, bayes_cases, fontsize=8, va='center')
    
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'decision_tree_freq_vs_bayes.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Main execution ---
if __name__ == "__main__":
    print("="*80)
    print("  GENERATING CARTOON-STYLE IMAGES FOR LESSON 1.4")
    print("  Bayesian vs Frequentist - So sanh Triet ly")
    print("="*80)
    
    print("\n[1/3] Creating Fisher vs Jeffreys debate...")
    create_great_debate()
    print("✅ Created: fisher_vs_jeffreys_debate.png")
    
    print("\n[2/3] Creating clinical trial comparison...")
    create_clinical_trial_comparison()
    print("✅ Created: clinical_trial_comparison.png")
    
    print("\n[3/3] Creating decision tree...")
    create_decision_tree()
    print("✅ Created: decision_tree_freq_vs_bayes.png")
    
    print("\n" + "="*80)
    print("  ✅ ALL CARTOON IMAGES CREATED SUCCESSFULLY!")
    print("="*80)
    
    print("\nGenerated files:")
    print("  1. fisher_vs_jeffreys_debate.png - Historical debate")
    print("  2. clinical_trial_comparison.png - Side-by-side comparison")
    print("  3. decision_tree_freq_vs_bayes.png - When to use what")
    print("\n" + "="*80)
