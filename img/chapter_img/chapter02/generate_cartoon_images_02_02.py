#!/usr/bin/env python3
"""
Generate Cartoon-Style Images for Lesson 2.2
Likelihood - The Data Story

Inspired by: Detective stories, The Cartoon Guide to Statistics
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrow, Polygon
import numpy as np
from scipy import stats
import os

# Setup
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("  GENERATING CARTOON IMAGES FOR LESSON 2.2")
print("  Likelihood - The Data Story")
print("="*80)

# --- Image 1: Detective Anna's Investigation ---
def create_anna_coin_investigation():
    """
    Comic: Detective Anna investigating suspicious coin
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Vu an Dong xu Bi nghi ngo', 
            fontsize=20, weight='bold', ha='center')
    
    # Detective Anna (left)
    anna_x, anna_y = 2, 5.5
    # Head
    circle = Circle((anna_x, anna_y), 0.35, color='#FFE5B4', ec='black', lw=2)
    ax.add_patch(circle)
    # Detective hat
    hat = Polygon([(anna_x-0.4, anna_y+0.35), (anna_x+0.4, anna_y+0.35), 
                   (anna_x+0.3, anna_y+0.7), (anna_x-0.3, anna_y+0.7)],
                  fc='#8B4513', ec='black', lw=2)
    ax.add_patch(hat)
    # Body
    ax.plot([anna_x, anna_x], [anna_y-0.35, anna_y-1.3], 'k-', lw=3)
    # Arms (holding magnifying glass)
    ax.plot([anna_x, anna_x+0.8], [anna_y-0.6, anna_y-0.2], 'k-', lw=3)
    # Magnifying glass
    circle_glass = Circle((anna_x+1.1, anna_y-0.1), 0.25, fc='white', ec='black', lw=2, alpha=0.5)
    ax.add_patch(circle_glass)
    # Other arm
    ax.plot([anna_x, anna_x-0.4], [anna_y-0.6, anna_y-0.9], 'k-', lw=3)
    # Legs
    ax.plot([anna_x, anna_x-0.3], [anna_y-1.3, anna_y-2], 'k-', lw=3)
    ax.plot([anna_x, anna_x+0.3], [anna_y-1.3, anna_y-2], 'k-', lw=3)
    
    # Serious face
    ax.plot([anna_x-0.12, anna_x-0.12], [anna_y+0.05, anna_y+0.1], 'k-', lw=2)
    ax.plot([anna_x+0.12, anna_x+0.12], [anna_y+0.05, anna_y+0.1], 'k-', lw=2)
    ax.plot([anna_x-0.15, anna_x+0.15], [anna_y-0.15, anna_y-0.15], 'k-', lw=2)
    
    # Label
    ax.text(anna_x, anna_y-2.5, 'Detective Anna\n(Data Scientist, FBI)', 
            ha='center', fontsize=10, weight='bold')
    
    # Evidence table (center)
    table = Rectangle((3.5, 4), 2.5, 2, fc='#8B4513', ec='black', lw=3)
    ax.add_patch(table)
    
    # Coin on table
    coin = Circle((4.75, 5.5), 0.3, fc='gold', ec='black', lw=2)
    ax.add_patch(coin)
    ax.text(4.75, 5.5, '$', fontsize=20, ha='center', va='center', weight='bold')
    
    # Data paper
    paper = Rectangle((4, 4.5), 1.2, 0.7, fc='white', ec='black', lw=2)
    ax.add_patch(paper)
    ax.text(4.6, 4.85, 'DATA:\n7/10\nHeads', ha='center', va='center', fontsize=9, weight='bold')
    
    # Casino Manager (right)
    manager_x, manager_y = 7.5, 5.5
    # Head
    circle = Circle((manager_x, manager_y), 0.35, color='#FFE5B4', ec='black', lw=2)
    ax.add_patch(circle)
    # Body (suit)
    suit = Rectangle((manager_x-0.3, manager_y-1.3), 0.6, 0.95, fc='black', ec='black', lw=2)
    ax.add_patch(suit)
    # Arms (worried gesture)
    ax.plot([manager_x, manager_x-0.5], [manager_y-0.6, manager_y-0.3], 'k-', lw=3)
    ax.plot([manager_x, manager_x+0.5], [manager_y-0.6, manager_y-0.3], 'k-', lw=3)
    # Legs
    ax.plot([manager_x, manager_x-0.25], [manager_y-1.3, manager_y-2], 'k-', lw=3)
    ax.plot([manager_x, manager_x+0.25], [manager_y-1.3, manager_y-2], 'k-', lw=3)
    
    # Worried face
    ax.plot([manager_x-0.12, manager_x-0.12], [manager_y+0.05, manager_y+0.1], 'k-', lw=2)
    ax.plot([manager_x+0.12, manager_x+0.12], [manager_y+0.05, manager_y+0.1], 'k-', lw=2)
    # Worried mouth
    worry = patches.Arc((manager_x, manager_y-0.25), 0.2, 0.15, theta1=20, theta2=160, lw=2)
    ax.add_patch(worry)
    
    # Label
    ax.text(manager_x, manager_y-2.5, 'Casino Manager\n(Worried)', 
            ha='center', fontsize=10, weight='bold')
    
    # Speech bubbles
    # Manager's question
    bubble1 = FancyBboxPatch((6.3, 6.5), 2.2, 0.9, boxstyle="round,pad=0.1", 
                             ec='black', fc='#FFE5E5', lw=2)
    ax.add_patch(bubble1)
    ax.text(7.4, 6.95, 'Dong xu nay co\nbi gian lan khong?\nYES or NO?', 
            fontsize=10, ha='center', va='center')
    
    # Anna's response
    bubble2 = FancyBboxPatch((0.3, 6.8), 2.5, 1.2, boxstyle="round,pad=0.1", 
                             ec='black', fc='#E5FFE5', lw=2)
    ax.add_patch(bubble2)
    ax.text(1.55, 7.4, 'Khong don gian!\nToi can tinh\nLIKELIHOOD\ncho cac gia tri\ntheta khac nhau', 
            fontsize=9, ha='center', va='center')
    
    # Bottom: Key question
    question_box = FancyBboxPatch((1, 0.5), 8, 1.5, boxstyle="round,pad=0.15", 
                                  ec='black', fc='#FFFFCC', lw=3)
    ax.add_patch(question_box)
    
    ax.text(5, 1.6, 'CAU HOI DUNG:', fontsize=13, weight='bold', ha='center', color='green')
    ax.text(5, 1.2, '"NEU dong xu co bias theta, thi kha nang toi thay', fontsize=11, ha='center')
    ax.text(5, 0.85, 'data nay (7/10 Heads) la bao nhieu?"', fontsize=11, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'anna_coin_investigation.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 2: Likelihood vs Probability Concept ---
def create_likelihood_vs_probability_concept():
    """
    Visual comparison: Likelihood vs Probability
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # Left: Likelihood (function of θ)
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(5, 9, 'LIKELIHOOD', fontsize=18, weight='bold', ha='center', color='green')
    ax.text(5, 8.3, 'L(θ | D) = P(D | θ)', fontsize=14, ha='center', style='italic')
    
    # Box
    box1 = FancyBboxPatch((1, 5), 8, 2.5, boxstyle="round,pad=0.15", 
                          ec='green', fc='#E5FFE5', lw=3)
    ax.add_patch(box1)
    
    ax.text(5, 6.8, 'Ham cua θ (data D co dinh)', fontsize=12, ha='center', weight='bold')
    ax.text(5, 6.3, '• Data da quan sat duoc', fontsize=10, ha='center')
    ax.text(5, 5.9, '• Thay doi theta de xem gia tri nao', fontsize=10, ha='center')
    ax.text(5, 5.5, '  lam data hop ly hon', fontsize=10, ha='center')
    
    # Example
    ex_box1 = FancyBboxPatch((1, 2), 8, 2.3, boxstyle="round,pad=0.15", 
                             ec='black', fc='#FFFFCC', lw=2)
    ax.add_patch(ex_box1)
    
    ax.text(5, 3.8, 'Vi du:', fontsize=11, weight='bold', ha='center')
    ax.text(5, 3.4, 'Data: 7 Heads in 10 tosses', fontsize=10, ha='center')
    ax.text(5, 3, 'NEU theta=0.5: P(7/10) = 0.117', fontsize=10, ha='center', color='blue')
    ax.text(5, 2.6, 'NEU theta=0.7: P(7/10) = 0.267', fontsize=10, ha='center', color='blue')
    ax.text(5, 2.2, 'NEU theta=0.9: P(7/10) = 0.121', fontsize=10, ha='center', color='blue')
    
    ax.text(5, 1.2, 'Tra loi: "Data hop ly NHAT voi theta=0.7"', 
            fontsize=10, ha='center', weight='bold', color='green')
    
    ax.text(5, 0.3, 'KHONG phai xac suat cua theta!', 
            fontsize=11, ha='center', weight='bold', color='red')
    
    # Right: Probability (Posterior)
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(5, 9, 'PROBABILITY (Posterior)', fontsize=18, weight='bold', ha='center', color='blue')
    ax.text(5, 8.3, 'P(θ | D)', fontsize=14, ha='center', style='italic')
    
    # Box
    box2 = FancyBboxPatch((1, 5), 8, 2.5, boxstyle="round,pad=0.15", 
                          ec='blue', fc='#E5E5FF', lw=3)
    ax.add_patch(box2)
    
    ax.text(5, 6.8, 'Phan phoi xac suat cua θ', fontsize=12, ha='center', weight='bold')
    ax.text(5, 6.3, '• Tich phan bang 1 qua theta', fontsize=10, ha='center')
    ax.text(5, 5.9, '• Co the dien giai truc tiep', fontsize=10, ha='center')
    ax.text(5, 5.5, '  ve xac suat cua theta', fontsize=10, ha='center')
    
    # Example
    ex_box2 = FancyBboxPatch((1, 2), 8, 2.3, boxstyle="round,pad=0.15", 
                             ec='black', fc='#FFFFCC', lw=2)
    ax.add_patch(ex_box2)
    
    ax.text(5, 3.8, 'Vi du:', fontsize=11, weight='bold', ha='center')
    ax.text(5, 3.4, 'Cho truoc data: 7/10 Heads', fontsize=10, ha='center')
    ax.text(5, 3, 'P(0.6 < theta < 0.8 | data) = 0.72', fontsize=10, ha='center', color='blue')
    ax.text(5, 2.6, 'P(theta > 0.5 | data) = 0.89', fontsize=10, ha='center', color='blue')
    ax.text(5, 2.2, 'Mean(theta | data) = 0.67', fontsize=10, ha='center', color='blue')
    
    ax.text(5, 1.2, 'Tra loi: "Co 72% xac suat theta trong [0.6,0.8]"', 
            fontsize=10, ha='center', weight='bold', color='blue')
    
    ax.text(5, 0.3, 'Day MOI la xac suat cua theta!', 
            fontsize=11, ha='center', weight='bold', color='green')
    
    fig.suptitle('Likelihood ≠ Probability!', fontsize=20, weight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'likelihood_vs_probability_concept.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 3: Likelihood as Data Story ---
def create_likelihood_data_story():
    """
    Metaphor: Likelihood as "data generator story"
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Likelihood = "Cau chuyen Sinh Data"', 
            fontsize=20, weight='bold', ha='center')
    
    # Three scenarios
    scenarios = [
        (2, 'theta = 0.5\n(Fair coin)', 0.117, '#FFE5E5'),
        (5, 'theta = 0.7\n(Biased)', 0.267, '#E5FFE5'),
        (8, 'theta = 0.9\n(Very biased)', 0.121, '#FFE5CC'),
    ]
    
    for x_pos, title, likelihood, color in scenarios:
        # Box
        box = FancyBboxPatch((x_pos-1.2, 5), 2.4, 3.5, boxstyle="round,pad=0.15", 
                             ec='black', fc=color, lw=2)
        ax.add_patch(box)
        
        # Title
        ax.text(x_pos, 8.2, title, fontsize=12, weight='bold', ha='center')
        
        # Coin
        coin = Circle((x_pos, 7.3), 0.3, fc='gold', ec='black', lw=2)
        ax.add_patch(coin)
        ax.text(x_pos, 7.3, '$', fontsize=18, ha='center', va='center', weight='bold')
        
        # Arrow down
        arrow = FancyArrow(x_pos, 6.8, 0, -0.5, width=0.1, head_width=0.3, head_length=0.2,
                          fc='black', ec='black')
        ax.add_patch(arrow)
        
        # Data
        ax.text(x_pos, 6, 'Data:\n7/10 Heads', fontsize=10, ha='center', weight='bold')
        
        # Likelihood value
        ax.text(x_pos, 5.4, f'L = {likelihood:.3f}', fontsize=13, ha='center', 
                weight='bold', color='blue')
    
    # Arrows and labels
    # Scenario 1 → 2
    ax.annotate('', xy=(4, 6.5), xytext=(3, 6.5),
                arrowprops=dict(arrowstyle='->', lw=3, color='green'))
    ax.text(3.5, 7, 'More\nplausible!', fontsize=10, ha='center', weight='bold', color='green')
    
    # Scenario 2 → 3
    ax.annotate('', xy=(7, 6.5), xytext=(6, 6.5),
                arrowprops=dict(arrowstyle='->', lw=3, color='red'))
    ax.text(6.5, 7, 'Less\nplausible!', fontsize=10, ha='center', weight='bold', color='red')
    
    # Winner
    winner_box = FancyBboxPatch((3.8, 3.5), 2.4, 1, boxstyle="round,pad=0.15", 
                                ec='green', fc='#E5FFE5', lw=4)
    ax.add_patch(winner_box)
    ax.text(5, 4.3, 'WINNER!', fontsize=16, weight='bold', ha='center', color='green')
    ax.text(5, 3.9, 'Data hop ly NHAT\nvoi theta=0.7', fontsize=11, ha='center')
    
    # Bottom interpretation
    interp_box = FancyBboxPatch((1, 0.5), 8, 2.3, boxstyle="round,pad=0.15", 
                                ec='black', fc='#FFFFCC', lw=3)
    ax.add_patch(interp_box)
    
    ax.text(5, 2.4, 'Likelihood hoi:', fontsize=13, weight='bold', ha='center')
    ax.text(5, 2, '"NEU the gioi hoat dong THEO CACH NAY (theta = gia tri nao do),', 
            fontsize=11, ha='center', style='italic')
    ax.text(5, 1.6, 'thi kha nang toi thay data ma toi da thay la bao nhieu?"', 
            fontsize=11, ha='center', style='italic')
    ax.text(5, 1.1, 'Chung ta hoi cau hoi nay cho NHIEU gia tri theta khac nhau,', 
            fontsize=10, ha='center')
    ax.text(5, 0.7, 'va so sanh cac cau tra loi!', fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'likelihood_data_story.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 4: Likelihood Ratio Visualization ---
def create_likelihood_ratio():
    """
    Visual explanation of likelihood ratio
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Data
    n, k = 10, 7
    theta_grid = np.linspace(0, 1, 1000)
    likelihood = stats.binom.pmf(k, n, theta_grid)
    
    # Plot likelihood
    ax.plot(theta_grid, likelihood, 'g-', lw=4, label='Likelihood')
    ax.fill_between(theta_grid, likelihood, alpha=0.3, color='green')
    
    # Mark two specific values
    theta1, theta2 = 0.5, 0.7
    L1 = stats.binom.pmf(k, n, theta1)
    L2 = stats.binom.pmf(k, n, theta2)
    
    # Vertical lines
    ax.axvline(theta1, color='blue', linestyle='--', lw=3, alpha=0.7)
    ax.axvline(theta2, color='red', linestyle='--', lw=3, alpha=0.7)
    
    # Points
    ax.scatter([theta1], [L1], s=300, color='blue', zorder=5, edgecolors='black', linewidths=2)
    ax.scatter([theta2], [L2], s=300, color='red', zorder=5, edgecolors='black', linewidths=2)
    
    # Labels
    ax.text(theta1, L1+0.02, f'θ₁={theta1}\nL₁={L1:.3f}', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', fc='#E5E5FF', alpha=0.9))
    ax.text(theta2, L2+0.02, f'θ₂={theta2}\nL₂={L2:.3f}', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', fc='#FFE5E5', alpha=0.9))
    
    # Likelihood Ratio
    LR = L2 / L1
    ax.text(0.6, 0.22, f'Likelihood Ratio:\nLR = L₂/L₁ = {LR:.2f}', 
            fontsize=14, weight='bold',
            bbox=dict(boxstyle='round', fc='yellow', alpha=0.9, pad=0.5))
    
    # Interpretation
    ax.text(0.6, 0.15, f'Data hop ly hon {LR:.2f}x\nvoi θ₂=0.7 so voi θ₁=0.5', 
            fontsize=12, ha='center',
            bbox=dict(boxstyle='round', fc='#E5FFE5', alpha=0.9))
    
    ax.set_xlabel('θ (Probability of Heads)', fontsize=14)
    ax.set_ylabel('Likelihood', fontsize=14)
    ax.set_title('Likelihood Ratio: Comparing Two Hypotheses', fontsize=16, weight='bold')
    ax.legend(fontsize=12)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'likelihood_ratio.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 5: Prior × Likelihood → Posterior ---
def create_prior_likelihood_posterior():
    """
    Bayesian update visualization
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Setup
    theta_grid = np.linspace(0, 1, 1000)
    
    # Prior: Beta(2, 2)
    prior = stats.beta(2, 2).pdf(theta_grid)
    
    # Data: 7 Heads in 10 tosses
    n, k = 10, 7
    likelihood = stats.binom.pmf(k, n, theta_grid)
    likelihood_scaled = likelihood / likelihood.max() * prior.max() * 0.8
    
    # Posterior: Beta(2+7, 2+3) = Beta(9, 5)
    posterior = stats.beta(2+k, 2+(n-k)).pdf(theta_grid)
    
    # Plot
    ax.plot(theta_grid, prior, 'b--', lw=3, label='Prior: Beta(2,2)', alpha=0.7)
    ax.fill_between(theta_grid, prior, alpha=0.2, color='blue')
    
    ax.plot(theta_grid, likelihood_scaled, 'g:', lw=3, label=f'Likelihood (scaled): {k}/{n}', alpha=0.7)
    
    ax.plot(theta_grid, posterior, 'r-', lw=4, label='Posterior: Beta(9,5)')
    ax.fill_between(theta_grid, posterior, alpha=0.3, color='red')
    
    # Annotations
    # Prior mean
    prior_mean = 2 / (2 + 2)
    ax.axvline(prior_mean, color='blue', linestyle=':', lw=1, alpha=0.5)
    ax.text(prior_mean-0.05, ax.get_ylim()[1]*0.85, 'Prior\nmean', 
            ha='right', fontsize=10, color='blue')
    
    # MLE
    mle = k / n
    ax.axvline(mle, color='green', linestyle=':', lw=1, alpha=0.5)
    ax.text(mle+0.05, ax.get_ylim()[1]*0.75, 'MLE', 
            ha='left', fontsize=10, color='green')
    
    # Posterior mean
    post_mean = (2+k) / (2+k+2+(n-k))
    ax.axvline(post_mean, color='red', linestyle=':', lw=1, alpha=0.5)
    ax.text(post_mean+0.05, ax.get_ylim()[1]*0.95, 'Posterior\nmean', 
            ha='left', fontsize=10, color='red')
    
    ax.set_xlabel('θ', fontsize=14)
    ax.set_ylabel('Density', fontsize=14)
    ax.set_title('Bayesian Update: Prior × Likelihood → Posterior', fontsize=16, weight='bold')
    ax.legend(fontsize=13, loc='upper left')
    ax.grid(alpha=0.3)
    
    # Formula
    formula = r'$P(\theta|D) \propto P(D|\theta) \cdot P(\theta)$'
    ax.text(0.98, 0.98, formula, transform=ax.transAxes, fontsize=16,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Interpretation
    interpretation = "Likelihood 'keo' Prior\nve phia gia tri\nduoc data ho tro"
    ax.text(0.02, 0.98, interpretation, transform=ax.transAxes, fontsize=12,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_likelihood_posterior.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Main execution ---
if __name__ == "__main__":
    print("\n[1/5] Creating Detective Anna's investigation...")
    create_anna_coin_investigation()
    print("✅ Created: anna_coin_investigation.png")
    
    print("\n[2/5] Creating likelihood vs probability concept...")
    create_likelihood_vs_probability_concept()
    print("✅ Created: likelihood_vs_probability_concept.png")
    
    print("\n[3/5] Creating likelihood as data story...")
    create_likelihood_data_story()
    print("✅ Created: likelihood_data_story.png")
    
    print("\n[4/5] Creating likelihood ratio visualization...")
    create_likelihood_ratio()
    print("✅ Created: likelihood_ratio.png")
    
    print("\n[5/5] Creating prior × likelihood → posterior...")
    create_prior_likelihood_posterior()
    print("✅ Created: prior_likelihood_posterior.png")
    
    print("\n" + "="*80)
    print("  ✅ ALL 5 IMAGES CREATED SUCCESSFULLY!")
    print("="*80)
    print("\nImages saved to:", output_dir)
    print("\nNote: Additional images (binomial_likelihood, poisson_likelihood, etc.)")
    print("are generated by code examples in the lesson itself.")
    print("\nNext steps:")
    print("1. Check images in the output directory")
    print("2. Images are already embedded in the enhanced lesson")
    print("3. Ready to continue with Bài 2.3!")
