#!/usr/bin/env python3
"""
Generate Cartoon-Style Images for Lesson 1.3
Định lý Bayes - Công cụ Cập nhật Niềm tin

Inspired by:
- The Lady Tasting Tea
- Naked Statistics
- How to Lie with Statistics
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyArrow, FancyBboxPatch, Wedge, Polygon
from scipy import stats
import os

# Ensure output directory exists
output_dir = '/Users/nguyenlelinh/teaching/bayesian-statistics-self-learning/img/chapter_img/chapter01'
os.makedirs(output_dir, exist_ok=True)

# Set Vietnamese font support
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# --- Image 1: Dr. Mai's Diagnosis Story ---
def create_doctor_diagnosis_story():
    """
    4-panel comic: Doctor Mai diagnosing patient
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Bac si Mai va Benh nhan Bi an", 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Panel 1: Initial symptoms
    ax = axes[0, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("1. Trieu chung ban dau", fontsize=14, fontweight='bold')
    
    # Doctor
    ax.add_patch(Circle((0.25, 0.6), 0.08, color='peachpuff'))
    ax.add_patch(Rectangle((0.21, 0.4), 0.08, 0.2, color='white'))
    
    # Patient
    ax.add_patch(Circle((0.65, 0.6), 0.08, color='lightgreen'))
    ax.add_patch(Rectangle((0.61, 0.4), 0.08, 0.2, color='lightblue'))
    # Sick face
    ax.text(0.65, 0.55, ':(', ha='center', fontsize=20)
    
    # Symptoms
    ax.text(0.5, 0.25, 'Sot 38.5C\nHo khan\nMet moi', ha='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', 
                     edgecolor='red', linewidth=2))
    
    # Doctor's thought
    ax.text(0.25, 0.85, "Hmm...\nCo the la gi?", ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    ax.axis('off')
    
    # Panel 2: Prior beliefs
    ax = axes[0, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("2. PRIOR (Niem tin ban dau)", fontsize=14, fontweight='bold')
    
    # Bar chart of priors
    diseases = ['Cam cum\n50%', 'COVID-19\n30%', 'Viem phoi\n20%']
    probs = [0.50, 0.30, 0.20]
    colors = ['lightblue', 'orange', 'lightcoral']
    
    y_pos = [0.7, 0.5, 0.3]
    for i, (disease, prob, color, y) in enumerate(zip(diseases, probs, colors, y_pos)):
        # Bar
        ax.add_patch(Rectangle((0.1, y-0.05), prob*0.8, 0.1, 
                               facecolor=color, edgecolor='black', linewidth=2))
        # Label
        ax.text(0.05, y, disease, ha='right', va='center', fontsize=10)
        # Percentage
        ax.text(0.1 + prob*0.8 + 0.02, y, f'{prob:.0%}', 
                va='center', fontsize=10, fontweight='bold')
    
    ax.text(0.5, 0.15, 'Dua tren kinh nghiem\nvà mùa dich', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Panel 3: New evidence (loss of smell)
    ax = axes[1, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("3. DATA moi: Mat khuu giac!", fontsize=14, fontweight='bold')
    
    # Doctor asking
    ax.add_patch(Circle((0.25, 0.6), 0.08, color='peachpuff'))
    ax.add_patch(Rectangle((0.21, 0.4), 0.08, 0.2, color='white'))
    ax.text(0.25, 0.75, "Anh co mat\nkhuu giac khong?", ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # Patient responding
    ax.add_patch(Circle((0.65, 0.6), 0.08, color='lightgreen'))
    ax.add_patch(Rectangle((0.61, 0.4), 0.08, 0.2, color='lightblue'))
    ax.text(0.65, 0.75, "Co! Tu hom qua\ntoi khong ngui\nduoc gi ca!", 
            ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor='black', linewidth=1))
    
    # Likelihood info
    ax.text(0.5, 0.2, 'LIKELIHOOD:\nP(mat khuu giac | Cam cum) = 10%\n'
                      'P(mat khuu giac | COVID) = 80%\n'
                      'P(mat khuu giac | Viem phoi) = 5%', 
            ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', 
                     edgecolor='green', linewidth=2))
    
    ax.axis('off')
    
    # Panel 4: Updated beliefs (Posterior)
    ax = axes[1, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("4. POSTERIOR (Cap nhat niem tin)", fontsize=14, fontweight='bold')
    
    # Updated bar chart
    diseases_post = ['Cam cum\n15%', 'COVID-19\n75%', 'Viem phoi\n10%']
    probs_post = [0.15, 0.75, 0.10]
    
    for i, (disease, prob, color, y) in enumerate(zip(diseases_post, probs_post, colors, y_pos)):
        # Bar
        ax.add_patch(Rectangle((0.1, y-0.05), prob*0.8, 0.1, 
                               facecolor=color, edgecolor='black', linewidth=2))
        # Label
        ax.text(0.05, y, disease, ha='right', va='center', fontsize=10)
        # Percentage
        ax.text(0.1 + prob*0.8 + 0.02, y, f'{prob:.0%}', 
                va='center', fontsize=10, fontweight='bold')
        
        # Arrow showing change
        if i == 1:  # COVID increased
            ax.annotate('', xy=(0.1 + prob*0.8, y), xytext=(0.1 + probs[i]*0.8, y),
                       arrowprops=dict(arrowstyle='->', lw=3, color='red'))
    
    ax.text(0.5, 0.15, 'Sau khi biet mat khuu giac:\nCOVID-19 tang tu 30% -> 75%!', 
            ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', 
                     edgecolor='red', linewidth=2))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'doctor_diagnosis_bayes.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 2: Bayes Machine ---
def create_bayes_machine():
    """
    Visual representation of Bayes theorem as a machine
    """
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('BAYES MACHINE: May Cap nhat Niem tin', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Machine body
    ax.add_patch(Rectangle((0.15, 0.15), 0.7, 0.7, 
                           facecolor='lightgray', edgecolor='black', linewidth=3))
    ax.text(0.5, 0.8, 'BAYES MACHINE', ha='center', fontsize=14, 
            fontweight='bold')
    
    # Input 1: Prior
    ax.add_patch(Rectangle((0.05, 0.65), 0.15, 0.08, 
                           facecolor='lightblue', edgecolor='black', linewidth=2))
    ax.text(0.125, 0.69, 'PRIOR', ha='center', fontsize=10, fontweight='bold')
    ax.annotate('', xy=(0.2, 0.69), xytext=(0.15, 0.69),
               arrowprops=dict(arrowstyle='->', lw=2))
    
    # Input 2: Data
    ax.add_patch(Rectangle((0.05, 0.52), 0.15, 0.08, 
                           facecolor='lightgreen', edgecolor='black', linewidth=2))
    ax.text(0.125, 0.56, 'DATA', ha='center', fontsize=10, fontweight='bold')
    ax.annotate('', xy=(0.2, 0.56), xytext=(0.15, 0.56),
               arrowprops=dict(arrowstyle='->', lw=2))
    
    # Process 1: Likelihood
    ax.add_patch(Rectangle((0.25, 0.55), 0.5, 0.12, 
                           facecolor='yellow', edgecolor='black', linewidth=2))
    ax.text(0.5, 0.61, 'Tinh LIKELIHOOD', ha='center', fontsize=11, 
            fontweight='bold')
    ax.text(0.5, 0.58, 'P(Data | theta)', ha='center', fontsize=9)
    
    # Process 2: Multiply
    ax.add_patch(Rectangle((0.25, 0.40), 0.5, 0.12, 
                           facecolor='orange', edgecolor='black', linewidth=2))
    ax.text(0.5, 0.46, 'NHAN: Prior x Likelihood', ha='center', fontsize=11, 
            fontweight='bold')
    ax.text(0.5, 0.43, 'P(theta) x P(Data|theta)', ha='center', fontsize=9)
    
    # Arrow down
    ax.annotate('', xy=(0.5, 0.40), xytext=(0.5, 0.55),
               arrowprops=dict(arrowstyle='->', lw=3))
    
    # Process 3: Normalize
    ax.add_patch(Rectangle((0.25, 0.25), 0.5, 0.12, 
                           facecolor='lightcoral', edgecolor='black', linewidth=2))
    ax.text(0.5, 0.31, 'CHUAN HOA: Chia cho Evidence', ha='center', 
            fontsize=11, fontweight='bold')
    ax.text(0.5, 0.28, '/ P(Data)', ha='center', fontsize=9)
    
    # Arrow down
    ax.annotate('', xy=(0.5, 0.25), xytext=(0.5, 0.40),
               arrowprops=dict(arrowstyle='->', lw=3))
    
    # Output: Posterior
    ax.add_patch(Rectangle((0.8, 0.25), 0.15, 0.12, 
                           facecolor='lightgreen', edgecolor='black', linewidth=3))
    ax.text(0.875, 0.33, 'POSTERIOR', ha='center', fontsize=10, 
            fontweight='bold')
    ax.text(0.875, 0.28, 'P(theta|Data)', ha='center', fontsize=8)
    ax.annotate('', xy=(0.8, 0.31), xytext=(0.75, 0.31),
               arrowprops=dict(arrowstyle='->', lw=3, color='green'))
    
    # Formula at bottom
    ax.text(0.5, 0.10, r'P(theta | Data) = [P(Data | theta) x P(theta)] / P(Data)', 
            ha='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', 
                     edgecolor='red', linewidth=2))
    
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bayes_machine.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 3: Medical Test Paradox ---
def create_medical_test_paradox():
    """
    Visualization of the medical test paradox
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('MEDICAL TEST PARADOX: Tai sao Prior quan trong!', 
                 fontsize=16, fontweight='bold')
    
    # Left panel: Population breakdown
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_title('1000 nguoi lam test', fontsize=14, fontweight='bold')
    
    # Draw people with disease (1% = 10 people)
    for i in range(10):
        x = i % 5
        y = 9 - i // 5
        ax1.add_patch(Circle((x*2 + 0.5, y), 0.3, color='red', alpha=0.7))
        ax1.text(x*2 + 0.5, y, 'D', ha='center', va='center', 
                fontsize=8, color='white', fontweight='bold')
    
    # Draw people without disease (99% = 990 people, show sample)
    np.random.seed(42)
    for i in range(50):  # Show sample
        x = np.random.uniform(0, 10)
        y = np.random.uniform(0, 8)
        ax1.add_patch(Circle((x, y), 0.2, color='green', alpha=0.3))
    
    # Legend
    ax1.text(5, 0.5, 'Co benh: 10 nguoi (1%)\nKhong benh: 990 nguoi (99%)', 
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='black', linewidth=2))
    
    ax1.axis('off')
    
    # Right panel: Test results
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title('Ket qua test DUONG TINH', fontsize=14, fontweight='bold')
    
    # True positives
    ax2.add_patch(Rectangle((0.1, 0.6), 0.15, 0.25, 
                            facecolor='darkgreen', edgecolor='black', linewidth=2))
    ax2.text(0.175, 0.8, 'TRUE\nPOSITIVE', ha='center', va='center', 
            fontsize=10, color='white', fontweight='bold')
    ax2.text(0.175, 0.68, '10 nguoi', ha='center', fontsize=9, color='white')
    
    # False positives
    ax2.add_patch(Rectangle((0.3, 0.6), 0.6, 0.25, 
                            facecolor='darkred', edgecolor='black', linewidth=2))
    ax2.text(0.6, 0.8, 'FALSE POSITIVE', ha='center', va='center', 
            fontsize=10, color='white', fontweight='bold')
    ax2.text(0.6, 0.68, '50 nguoi', ha='center', fontsize=9, color='white')
    
    # Total
    ax2.text(0.5, 0.5, 'TONG TEST DUONG TINH: 60 nguoi', ha='center', 
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow'))
    
    # Probability
    ax2.text(0.5, 0.35, 'P(co benh | test +) = 10/60 = 16.7%', 
            ha='center', fontsize=14, fontweight='bold', color='red',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     edgecolor='red', linewidth=3))
    
    # Explanation
    ax2.text(0.5, 0.15, 'Chi 16.7% nguoi test duong tinh\nTHUC SU co benh!\n\n'
                       'Vi sao? Prior qua THAP (1%)', 
            ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                     edgecolor='orange', linewidth=2))
    
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'medical_test_paradox.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 4: Prior × Likelihood = Posterior (Coin Example) ---
def create_coin_bayes_visualization():
    """
    Visual demonstration of Bayes theorem with coin flipping
    """
    # Parameters
    n_heads = 7
    n_tails = 3
    n_total = n_heads + n_tails
    
    # Prior: Beta(2, 2)
    prior_alpha, prior_beta = 2, 2
    
    # Posterior: Beta(2+7, 2+3)
    post_alpha = prior_alpha + n_heads
    post_beta = prior_beta + n_tails
    
    # Theta values
    theta = np.linspace(0, 1, 1000)
    
    # Distributions
    prior = stats.beta(prior_alpha, prior_beta).pdf(theta)
    likelihood_raw = stats.binom(n_total, theta).pmf(n_heads)
    likelihood = likelihood_raw / likelihood_raw.max() * prior.max()  # Scale
    posterior = stats.beta(post_alpha, post_beta).pdf(theta)
    
    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('DINH LY BAYES: Prior x Likelihood = Posterior', 
                 fontsize=16, fontweight='bold')
    
    # Prior
    axes[0].plot(theta, prior, 'b-', linewidth=3)
    axes[0].fill_between(theta, prior, alpha=0.3)
    axes[0].set_title('PRIOR: Beta(2, 2)', fontsize=14, fontweight='bold', color='blue')
    axes[0].set_xlabel('theta (P(Ngua))', fontsize=12)
    axes[0].set_ylabel('Density', fontsize=12)
    axes[0].axvline(0.5, color='red', linestyle='--', linewidth=2, label='Mean = 0.5')
    axes[0].legend(fontsize=10)
    axes[0].text(0.5, 0.9, '"Dong xu co the\ngan cong bang"', 
                transform=axes[0].transAxes, ha='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', 
                         edgecolor='blue', linewidth=2, alpha=0.8))
    axes[0].grid(alpha=0.3)
    
    # Likelihood
    axes[1].plot(theta, likelihood, 'g-', linewidth=3)
    axes[1].fill_between(theta, likelihood, alpha=0.3, color='green')
    axes[1].set_title('LIKELIHOOD: 7 Ngua / 10 lan', fontsize=14, 
                     fontweight='bold', color='green')
    axes[1].set_xlabel('theta (P(Ngua))', fontsize=12)
    axes[1].set_ylabel('Likelihood (scaled)', fontsize=12)
    axes[1].axvline(0.7, color='red', linestyle='--', linewidth=2, label='MLE = 0.7')
    axes[1].legend(fontsize=10)
    axes[1].text(0.5, 0.9, '"Data goi y\ntheta ~ 0.7"', 
                transform=axes[1].transAxes, ha='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', 
                         edgecolor='green', linewidth=2, alpha=0.8))
    axes[1].grid(alpha=0.3)
    
    # Posterior
    axes[2].plot(theta, posterior, 'r-', linewidth=3)
    axes[2].fill_between(theta, posterior, alpha=0.3, color='red')
    axes[2].set_title('POSTERIOR: Beta(9, 5)', fontsize=14, 
                     fontweight='bold', color='red')
    axes[2].set_xlabel('theta (P(Ngua))', fontsize=12)
    axes[2].set_ylabel('Density', fontsize=12)
    post_mean = post_alpha / (post_alpha + post_beta)
    axes[2].axvline(post_mean, color='blue', linestyle='--', linewidth=2, 
                   label=f'Mean = {post_mean:.2f}')
    axes[2].legend(fontsize=10)
    axes[2].text(0.5, 0.9, '"Thoa hiep giua\nprior va data"', 
                transform=axes[2].transAxes, ha='center', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                         edgecolor='orange', linewidth=2, alpha=0.8))
    axes[2].grid(alpha=0.3)
    
    # Add summary text
    fig.text(0.5, 0.02, 
             f'Prior mean: 0.50  |  MLE (data only): 0.70  |  Posterior mean: {post_mean:.2f}  '
             f'→ Posterior la SU THOA HIEP!',
             ha='center', fontsize=12, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', 
                      edgecolor='red', linewidth=2))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'coin_bayes_visualization.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Image 5: Prior Strength Comparison ---
def create_prior_strength_comparison():
    """
    Compare weak vs strong priors
    """
    # Data
    n_heads, n_tails = 7, 3
    
    # Weak prior
    weak_prior = (2, 2)
    weak_post = (weak_prior[0] + n_heads, weak_prior[1] + n_tails)
    
    # Strong prior
    strong_prior = (20, 20)
    strong_post = (strong_prior[0] + n_heads, strong_prior[1] + n_tails)
    
    # Plot
    theta = np.linspace(0, 1, 1000)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('PRIOR STRENGTH: Manh vs Yeu', fontsize=16, fontweight='bold')
    
    # Weak prior
    axes[0, 0].plot(theta, stats.beta(*weak_prior).pdf(theta), 'b-', linewidth=2)
    axes[0, 0].fill_between(theta, stats.beta(*weak_prior).pdf(theta), alpha=0.3)
    axes[0, 0].set_title('Weak Prior: Beta(2, 2)', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Density', fontsize=11)
    axes[0, 0].text(0.5, 0.9, 'Khong chac chan lam\n(Flat, spread out)', 
                   transform=axes[0, 0].transAxes, ha='center',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    axes[0, 0].grid(alpha=0.3)
    
    # Weak posterior
    axes[0, 1].plot(theta, stats.beta(*weak_post).pdf(theta), 'r-', linewidth=2)
    axes[0, 1].fill_between(theta, stats.beta(*weak_post).pdf(theta), 
                           alpha=0.3, color='red')
    axes[0, 1].set_title('Weak Posterior: Beta(9, 5)', fontsize=12, fontweight='bold')
    weak_mean = weak_post[0]/(weak_post[0]+weak_post[1])
    axes[0, 1].axvline(weak_mean, color='black', linestyle='--', linewidth=2,
                      label=f'Mean = {weak_mean:.2f}')
    axes[0, 1].legend()
    axes[0, 1].text(0.5, 0.9, 'Thay doi NHIEU!\n(0.50 -> 0.64)', 
                   transform=axes[0, 1].transAxes, ha='center',
                   bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    axes[0, 1].grid(alpha=0.3)
    
    # Strong prior
    axes[1, 0].plot(theta, stats.beta(*strong_prior).pdf(theta), 'b-', linewidth=2)
    axes[1, 0].fill_between(theta, stats.beta(*strong_prior).pdf(theta), alpha=0.3)
    axes[1, 0].set_title('Strong Prior: Beta(20, 20)', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('theta', fontsize=11)
    axes[1, 0].set_ylabel('Density', fontsize=11)
    axes[1, 0].text(0.5, 0.9, 'RAT chac chan!\n(Narrow, peaked)', 
                   transform=axes[1, 0].transAxes, ha='center',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    axes[1, 0].grid(alpha=0.3)
    
    # Strong posterior
    axes[1, 1].plot(theta, stats.beta(*strong_post).pdf(theta), 'r-', linewidth=2)
    axes[1, 1].fill_between(theta, stats.beta(*strong_post).pdf(theta), 
                           alpha=0.3, color='red')
    axes[1, 1].set_title('Strong Posterior: Beta(27, 23)', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('theta', fontsize=11)
    strong_mean = strong_post[0]/(strong_post[0]+strong_post[1])
    axes[1, 1].axvline(strong_mean, color='black', linestyle='--', linewidth=2,
                      label=f'Mean = {strong_mean:.2f}')
    axes[1, 1].legend()
    axes[1, 1].text(0.5, 0.9, 'Thay doi IT!\n(0.50 -> 0.54)', 
                   transform=axes[1, 1].transAxes, ha='center',
                   bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    axes[1, 1].grid(alpha=0.3)
    
    # Summary
    fig.text(0.5, 0.02, 
             'BAI HOC: Prior manh KHO THAY DOI. Can nhieu data hon de "thuyet phuc"!',
             ha='center', fontsize=12, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', 
                      edgecolor='red', linewidth=2))
    
    plt.tight_layout(rect=[0, 0.05, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'prior_strength_detailed.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# --- Main execution ---
if __name__ == "__main__":
    print("="*80)
    print("  GENERATING CARTOON-STYLE IMAGES FOR LESSON 1.3")
    print("  Dinh ly Bayes - Cong cu Cap nhat Niem tin")
    print("="*80)
    
    print("\n[1/5] Creating Dr. Mai's diagnosis story...")
    create_doctor_diagnosis_story()
    print("✅ Created: doctor_diagnosis_bayes.png")
    
    print("\n[2/5] Creating Bayes machine...")
    create_bayes_machine()
    print("✅ Created: bayes_machine.png")
    
    print("\n[3/5] Creating medical test paradox...")
    create_medical_test_paradox()
    print("✅ Created: medical_test_paradox.png")
    
    print("\n[4/5] Creating coin Bayes visualization...")
    create_coin_bayes_visualization()
    print("✅ Created: coin_bayes_visualization.png")
    
    print("\n[5/5] Creating prior strength comparison...")
    create_prior_strength_comparison()
    print("✅ Created: prior_strength_detailed.png")
    
    print("\n" + "="*80)
    print("  ✅ ALL CARTOON IMAGES CREATED SUCCESSFULLY!")
    print("="*80)
    
    print("\nGenerated files:")
    print("  1. doctor_diagnosis_bayes.png - Dr. Mai's diagnosis story")
    print("  2. bayes_machine.png - Bayes theorem as a machine")
    print("  3. medical_test_paradox.png - Medical test paradox")
    print("  4. coin_bayes_visualization.png - Prior × Likelihood = Posterior")
    print("  5. prior_strength_detailed.png - Weak vs Strong priors")
    print("\n" + "="*80)
