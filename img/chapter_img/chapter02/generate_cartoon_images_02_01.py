#!/usr/bin/env python3
"""
Generate Cartoon-Style Images for Lesson 2.1
Probability Distributions - The Language of Uncertainty

Inspired by: The Cartoon Guide to Statistics, The Manga Guide to Statistics
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrow, Wedge
import numpy as np
from scipy import stats
import os

# Setup
output_dir = os.path.dirname(os.path.abspath(__file__))
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("  GENERATING CARTOON IMAGES FOR LESSON 2.1")
print("  Probability Distributions")
print("="*80)

# --- Image 1: Minh's Point Estimate Problem ---
def create_minh_point_estimate_problem():
    """
    Comic panel: Minh presenting "25%" to confused executives
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Vấn đề của "Một Con Số"', 
            fontsize=20, weight='bold', ha='center')
    
    # Panel 1: Minh presenting
    # Minh (stick figure)
    minh_x, minh_y = 2, 6
    circle = Circle((minh_x, minh_y), 0.3, color='#FFE5B4', ec='black', lw=2)
    ax.add_patch(circle)
    # Body
    ax.plot([minh_x, minh_x], [minh_y-0.3, minh_y-1.2], 'k-', lw=3)
    # Arms (pointing to board)
    ax.plot([minh_x, minh_x+0.8], [minh_y-0.6, minh_y+0.5], 'k-', lw=3)
    ax.plot([minh_x, minh_x-0.3], [minh_y-0.6, minh_y-0.8], 'k-', lw=3)
    # Legs
    ax.plot([minh_x, minh_x-0.3], [minh_y-1.2, minh_y-1.8], 'k-', lw=3)
    ax.plot([minh_x, minh_x+0.3], [minh_y-1.2, minh_y-1.8], 'k-', lw=3)
    
    # Speech bubble
    bubble = FancyBboxPatch((0.5, 7), 1.2, 0.8, boxstyle="round,pad=0.1", 
                            ec='black', fc='white', lw=2)
    ax.add_patch(bubble)
    ax.text(1.1, 7.4, 'Conversion\nrate = 25%!', fontsize=11, ha='center', va='center')
    
    # Whiteboard with "25%"
    board = Rectangle((3.5, 5), 2, 2, fc='white', ec='black', lw=3)
    ax.add_patch(board)
    ax.text(4.5, 6, '25%', fontsize=48, weight='bold', ha='center', va='center', 
            color='blue')
    
    # Executives (3 people, confused)
    exec_positions = [(7, 6), (8, 6), (9, 6)]
    for i, (ex, ey) in enumerate(exec_positions):
        # Head
        circle = Circle((ex, ey), 0.25, color='#FFE5B4', ec='black', lw=2)
        ax.add_patch(circle)
        # Body
        ax.plot([ex, ex], [ey-0.25, ey-1], 'k-', lw=2)
        # Arms (crossed - confused)
        ax.plot([ex-0.3, ex+0.3], [ey-0.5, ey-0.5], 'k-', lw=2)
        # Legs
        ax.plot([ex, ex-0.2], [ey-1, ey-1.5], 'k-', lw=2)
        ax.plot([ex, ex+0.2], [ey-1, ey-1.5], 'k-', lw=2)
        
        # Confused face
        ax.plot([ex-0.08, ex-0.08], [ey+0.05, ey+0.1], 'k-', lw=2)  # eyes
        ax.plot([ex+0.08, ex+0.08], [ey+0.05, ey+0.1], 'k-', lw=2)
        # Wavy mouth (confused)
        x_mouth = np.linspace(ex-0.1, ex+0.1, 20)
        y_mouth = ey - 0.1 + 0.02*np.sin(20*x_mouth)
        ax.plot(x_mouth, y_mouth, 'k-', lw=2)
    
    # Question marks above executives
    ax.text(7, 6.8, '?', fontsize=24, weight='bold', color='red')
    ax.text(8, 6.8, '?', fontsize=24, weight='bold', color='red')
    ax.text(9, 6.8, '?', fontsize=24, weight='bold', color='red')
    
    # Speech bubbles from executives
    bubble2 = FancyBboxPatch((6.5, 4.5), 1.5, 0.6, boxstyle="round,pad=0.1", 
                             ec='black', fc='#FFE5E5', lw=2)
    ax.add_patch(bubble2)
    ax.text(7.25, 4.8, 'Bạn chắc\nchắn không?', fontsize=9, ha='center', va='center')
    
    bubble3 = FancyBboxPatch((7.8, 4.2), 1.8, 0.6, boxstyle="round,pad=0.1", 
                             ec='black', fc='#FFE5E5', lw=2)
    ax.add_patch(bubble3)
    ax.text(8.7, 4.5, 'Nếu thực tế\nchỉ 18% thì sao?', fontsize=9, ha='center', va='center')
    
    # Bottom text
    ax.text(5, 1.5, '❌ MỘT CON SỐ không trả lời:', fontsize=14, weight='bold', 
            ha='center', color='red')
    ax.text(5, 1, '• Bạn chắc chắn đến mức nào?', fontsize=11, ha='center')
    ax.text(5, 0.6, '• P(θ > 20%) = ?', fontsize=11, ha='center')
    ax.text(5, 0.2, '• Risk của quyết định là gì?', fontsize=11, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'minh_point_estimate_problem.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 2: Minh's Distribution Solution ---
def create_minh_distribution_solution():
    """
    Comic panel: Minh presenting distribution, executives happy
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Giải pháp: Phân phối Đầy đủ!', 
            fontsize=20, weight='bold', ha='center', color='green')
    
    # Minh (confident now)
    minh_x, minh_y = 2, 6
    circle = Circle((minh_x, minh_y), 0.3, color='#FFE5B4', ec='black', lw=2)
    ax.add_patch(circle)
    ax.plot([minh_x, minh_x], [minh_y-0.3, minh_y-1.2], 'k-', lw=3)
    ax.plot([minh_x, minh_x+0.8], [minh_y-0.6, minh_y+0.5], 'k-', lw=3)
    ax.plot([minh_x, minh_x-0.3], [minh_y-0.6, minh_y-0.8], 'k-', lw=3)
    ax.plot([minh_x, minh_x-0.3], [minh_y-1.2, minh_y-1.8], 'k-', lw=3)
    ax.plot([minh_x, minh_x+0.3], [minh_y-1.2, minh_y-1.8], 'k-', lw=3)
    
    # Smiley face
    ax.plot([minh_x-0.1, minh_x-0.1], [minh_y+0.05, minh_y+0.1], 'ko', markersize=4)
    ax.plot([minh_x+0.1, minh_x+0.1], [minh_y+0.05, minh_y+0.1], 'ko', markersize=4)
    smile = patches.Arc((minh_x, minh_y-0.05), 0.2, 0.15, theta1=200, theta2=340, lw=2)
    ax.add_patch(smile)
    
    # Speech bubble
    bubble = FancyBboxPatch((0.3, 7), 1.5, 0.9, boxstyle="round,pad=0.1", 
                            ec='black', fc='#E5FFE5', lw=2)
    ax.add_patch(bubble)
    ax.text(1.05, 7.45, 'Posterior:\nBeta(27, 81)\n95% CI:\n[17%, 34%]', 
            fontsize=10, ha='center', va='center')
    
    # Whiteboard with distribution
    board = Rectangle((3.5, 4.5), 3, 3, fc='white', ec='black', lw=3)
    ax.add_patch(board)
    
    # Draw mini distribution
    theta = np.linspace(0, 1, 100)
    post = stats.beta(27, 81)
    pdf = post.pdf(theta)
    # Scale to fit in board
    pdf_scaled = 4.5 + 2.5 * (pdf / pdf.max())
    ax.plot(3.5 + 3*theta, pdf_scaled, 'b-', lw=3)
    ax.fill_between(3.5 + 3*theta, 4.5, pdf_scaled, alpha=0.3, color='blue')
    
    # Annotations on board
    ax.text(5, 7.2, 'P(θ>20%) = 72%', fontsize=11, ha='center', weight='bold', color='green')
    ax.text(5, 6.8, 'Mean = 25%', fontsize=10, ha='center')
    ax.text(5, 6.4, '95% CI = [17%, 34%]', fontsize=10, ha='center')
    
    # Executives (happy now!)
    exec_positions = [(7.5, 6), (8.5, 6), (9.5, 6)]
    for ex, ey in exec_positions:
        # Head
        circle = Circle((ex, ey), 0.25, color='#FFE5B4', ec='black', lw=2)
        ax.add_patch(circle)
        # Body
        ax.plot([ex, ex], [ey-0.25, ey-1], 'k-', lw=2)
        # Arms (thumbs up!)
        ax.plot([ex, ex-0.3], [ey-0.5, ey-0.3], 'k-', lw=3)
        ax.plot([ex-0.3, ex-0.3], [ey-0.3, ey-0.1], 'k-', lw=3)
        ax.plot([ex, ex+0.3], [ey-0.5, ey-0.7], 'k-', lw=2)
        # Legs
        ax.plot([ex, ex-0.2], [ey-1, ey-1.5], 'k-', lw=2)
        ax.plot([ex, ex+0.2], [ey-1, ey-1.5], 'k-', lw=2)
        
        # Happy face
        ax.plot([ex-0.08, ex-0.08], [ey+0.05, ey+0.1], 'ko', markersize=3)
        ax.plot([ex+0.08, ex+0.08], [ey+0.05, ey+0.1], 'ko', markersize=3)
        smile = patches.Arc((ex, ey-0.05), 0.18, 0.12, theta1=200, theta2=340, lw=2)
        ax.add_patch(smile)
    
    # Checkmarks above executives
    ax.text(7.5, 6.7, '✓', fontsize=28, weight='bold', color='green')
    ax.text(8.5, 6.7, '✓', fontsize=28, weight='bold', color='green')
    ax.text(9.5, 6.7, '✓', fontsize=28, weight='bold', color='green')
    
    # Speech bubbles from executives
    bubble2 = FancyBboxPatch((7, 4.5), 1.5, 0.6, boxstyle="round,pad=0.1", 
                             ec='black', fc='#E5FFE5', lw=2)
    ax.add_patch(bubble2)
    ax.text(7.75, 4.8, 'Bây giờ rõ\nràng rồi!', fontsize=10, ha='center', va='center')
    
    bubble3 = FancyBboxPatch((8.3, 4.2), 1.6, 0.6, boxstyle="round,pad=0.1", 
                             ec='black', fc='#E5FFE5', lw=2)
    ax.add_patch(bubble3)
    ax.text(9.1, 4.5, 'Chúng ta có thể\nđịnh lượng risk!', fontsize=9, ha='center', va='center')
    
    # Bottom text
    ax.text(5, 1.5, '✅ PHÂN PHỐI trả lời TẤT CẢ:', fontsize=14, weight='bold', 
            ha='center', color='green')
    ax.text(5, 1, '• Most likely value: 25%', fontsize=11, ha='center')
    ax.text(5, 0.6, '• Uncertainty: 95% CI = [17%, 34%]', fontsize=11, ha='center')
    ax.text(5, 0.2, '• P(θ > 20%) = 72% → Có thể deploy!', fontsize=11, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'minh_distribution_solution.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 3: Distribution as Belief Map ---
def create_distribution_belief_map():
    """
    Visual metaphor: Distribution as a map showing belief landscape
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'Phân phối = "Bản đồ Niềm tin"', 
            fontsize=20, weight='bold', ha='center')
    
    # Left side: Point estimate (single pin on map)
    ax.text(2, 8.5, 'Point Estimate', fontsize=14, weight='bold', ha='center', color='red')
    
    # Map background
    map1 = Rectangle((0.5, 5.5), 3, 2.5, fc='#FFFFCC', ec='black', lw=2)
    ax.add_patch(map1)
    
    # Single pin
    ax.plot([2], [6.8], 'ro', markersize=20)
    ax.plot([2, 2], [6.8, 7.3], 'r-', lw=3)
    ax.text(2, 6.3, '25%', fontsize=16, ha='center', weight='bold')
    
    # X marks for uncertainty
    ax.text(2, 5, '❌ Không biết:', fontsize=11, ha='center', weight='bold', color='red')
    ax.text(2, 4.6, '• Chắc chắn bao nhiêu?', fontsize=9, ha='center')
    ax.text(2, 4.3, '• Có thể sai bao nhiêu?', fontsize=9, ha='center')
    ax.text(2, 4, '• Các giá trị khác?', fontsize=9, ha='center')
    
    # Arrow
    arrow = FancyArrow(3.8, 6.5, 1.4, 0, width=0.3, head_width=0.5, head_length=0.3,
                       fc='green', ec='black', lw=2)
    ax.add_patch(arrow)
    ax.text(4.5, 7, 'UPGRADE!', fontsize=12, weight='bold', ha='center', color='green')
    
    # Right side: Distribution (belief landscape)
    ax.text(8, 8.5, 'Distribution', fontsize=14, weight='bold', ha='center', color='green')
    
    # Map background
    map2 = Rectangle((6, 5.5), 4, 2.5, fc='#CCFFCC', ec='black', lw=2)
    ax.add_patch(map2)
    
    # Draw distribution as landscape
    theta = np.linspace(0, 1, 100)
    post = stats.beta(27, 81)
    pdf = post.pdf(theta)
    # Scale to fit
    pdf_scaled = 5.5 + 2.3 * (pdf / pdf.max())
    ax.plot(6 + 4*theta, pdf_scaled, 'g-', lw=3)
    ax.fill_between(6 + 4*theta, 5.5, pdf_scaled, alpha=0.4, color='green')
    
    # Annotations
    ax.text(8, 7.6, '← Belief "height"', fontsize=9, ha='center')
    ax.annotate('', xy=(7.5, 7.3), xytext=(7.5, 6.8),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
    
    # Checkmarks
    ax.text(8, 5, '✓ Biết TẤT CẢ:', fontsize=11, ha='center', weight='bold', color='green')
    ax.text(8, 4.6, '• Most likely: 25%', fontsize=9, ha='center')
    ax.text(8, 4.3, '• Uncertainty: SD=2.1%', fontsize=9, ha='center')
    ax.text(8, 4, '• All probabilities!', fontsize=9, ha='center')
    
    # Bottom: Interpretation guide
    guide_box = FancyBboxPatch((1, 1), 8, 2, boxstyle="round,pad=0.15", 
                               ec='black', fc='#FFE5CC', lw=2)
    ax.add_patch(guide_box)
    
    ax.text(5, 2.5, '📖 Cách đọc "Bản đồ Niềm tin":', fontsize=13, weight='bold', ha='center')
    ax.text(5, 2.1, '• Cao = Tin nhiều (high probability density)', fontsize=10, ha='center')
    ax.text(5, 1.8, '• Thấp = Tin ít (low probability density)', fontsize=10, ha='center')
    ax.text(5, 1.5, '• Rộng = Không chắc chắn (high uncertainty)', fontsize=10, ha='center')
    ax.text(5, 1.2, '• Hẹp = Chắc chắn (low uncertainty)', fontsize=10, ha='center')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'distribution_belief_map.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 4: Three Priors ---
def create_three_priors():
    """
    Comparison of three types of priors with characters
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    theta = np.linspace(0, 1, 1000)
    
    priors = [
        (1, 1, 'Uniform\nBeta(1,1)', 'Newbie', "Tôi không\nbiết gì!"),
        (2, 6, 'Weakly Informative\nBeta(2,6)', 'Beginner', "Có thể là\n20-30%?"),
        (50, 150, 'Informative\nBeta(50,150)', 'Expert', "Tôi chắc\nchắn ~25%!"),
    ]
    
    for ax, (alpha, beta, title, character, speech) in zip(axes, priors):
        # Plot distribution
        dist = stats.beta(alpha, beta)
        pdf = dist.pdf(theta)
        ax.plot(theta, pdf, 'b-', lw=3)
        ax.fill_between(theta, pdf, alpha=0.3, color='blue')
        
        ax.set_xlabel('θ (Conversion Rate)', fontsize=12)
        ax.set_ylabel('Density', fontsize=12)
        ax.set_title(title, fontsize=14, weight='bold')
        ax.grid(alpha=0.3)
        ax.set_ylim(0, None)
        
        # Add stats
        mean = alpha / (alpha + beta)
        std = np.sqrt(alpha * beta / ((alpha + beta)**2 * (alpha + beta + 1)))
        ax.text(0.5, 0.95, f'Mean = {mean:.2f}\nSD = {std:.2f}', 
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                fontsize=10)
        
        # Add character label
        ax.text(0.5, -0.15, f'👤 {character}', transform=ax.transAxes,
                ha='center', fontsize=11, weight='bold')
        ax.text(0.5, -0.22, speech, transform=ax.transAxes,
                ha='center', fontsize=9, style='italic')
    
    fig.suptitle('Ba Loại Prior: Từ "Không biết gì" đến "Rất chắc chắn"', 
                 fontsize=16, weight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'three_priors.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 5: Likelihood Function ---
def create_likelihood_function():
    """
    Visualize likelihood as a function of theta
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Data: 25 successes out of 100
    n, k = 100, 25
    theta = np.linspace(0, 1, 1000)
    
    # Likelihood (up to proportionality)
    likelihood = theta**k * (1-theta)**(n-k)
    likelihood = likelihood / likelihood.max()  # Normalize for visualization
    
    ax.plot(theta, likelihood, 'purple', lw=3, label='Likelihood')
    ax.fill_between(theta, likelihood, alpha=0.3, color='purple')
    
    # Mark the MLE
    mle = k / n
    ax.axvline(mle, color='red', linestyle='--', lw=2, label=f'MLE = {mle:.2f}')
    
    # Annotations
    ax.annotate('Nếu θ=0.25,\ndata rất có khả năng!', 
                xy=(0.25, 1.0), xytext=(0.4, 0.8),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'),
                fontsize=12, bbox=dict(boxstyle='round', fc='#FFE5E5'))
    
    ax.annotate('Nếu θ=0.50,\ndata ít có khả năng', 
                xy=(0.50, 0.15), xytext=(0.6, 0.4),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue'),
                fontsize=12, bbox=dict(boxstyle='round', fc='#E5E5FF'))
    
    ax.annotate('Nếu θ=0.10,\ndata rất ít có khả năng', 
                xy=(0.10, 0.05), xytext=(0.15, 0.25),
                arrowprops=dict(arrowstyle='->', lw=2, color='blue'),
                fontsize=12, bbox=dict(boxstyle='round', fc='#E5E5FF'))
    
    ax.set_xlabel('θ (Conversion Rate)', fontsize=14)
    ax.set_ylabel('Likelihood (normalized)', fontsize=14)
    ax.set_title(f'Likelihood Function: P(D | θ) với D = {k}/{n} conversions', 
                 fontsize=16, weight='bold')
    ax.legend(fontsize=12)
    ax.grid(alpha=0.3)
    
    # Add text box
    textstr = 'Likelihood cho biết:\n"Với mỗi giá trị θ,\ndata quan sát được\ncó khả năng như thế nào?"'
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'likelihood_function.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 6: Prior to Posterior ---
def create_prior_to_posterior():
    """
    Show the Bayesian update: Prior + Data → Posterior
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Prior, Data, Posterior
    prior_alpha, prior_beta = 2, 6
    n, k = 100, 25
    post_alpha = prior_alpha + k
    post_beta = prior_beta + (n - k)
    
    theta = np.linspace(0, 1, 1000)
    
    # Prior
    prior_dist = stats.beta(prior_alpha, prior_beta)
    prior_pdf = prior_dist.pdf(theta)
    ax.plot(theta, prior_pdf, 'b--', lw=3, label='Prior: Beta(2,6)', alpha=0.7)
    ax.fill_between(theta, prior_pdf, alpha=0.2, color='blue')
    
    # Likelihood (scaled for visualization)
    likelihood = theta**k * (1-theta)**(n-k)
    likelihood_scaled = likelihood / likelihood.max() * prior_pdf.max() * 0.8
    ax.plot(theta, likelihood_scaled, 'purple', lw=2, label=f'Likelihood: {k}/{n}', 
            alpha=0.7, linestyle=':')
    
    # Posterior
    post_dist = stats.beta(post_alpha, post_beta)
    post_pdf = post_dist.pdf(theta)
    ax.plot(theta, post_pdf, 'r-', lw=4, label='Posterior: Beta(27,81)')
    ax.fill_between(theta, post_pdf, alpha=0.3, color='red')
    
    ax.set_xlabel('θ (Conversion Rate)', fontsize=14)
    ax.set_ylabel('Density', fontsize=14)
    ax.set_title('Bayesian Update: Prior × Likelihood → Posterior', 
                 fontsize=16, weight='bold')
    ax.legend(fontsize=13, loc='upper right')
    ax.grid(alpha=0.3)
    
    # Annotations
    # Prior mean
    prior_mean = prior_alpha / (prior_alpha + prior_beta)
    ax.axvline(prior_mean, color='blue', linestyle=':', lw=1, alpha=0.5)
    ax.text(prior_mean, ax.get_ylim()[1]*0.9, f'Prior mean\n{prior_mean:.2f}', 
            ha='center', fontsize=10, color='blue')
    
    # Posterior mean
    post_mean = post_alpha / (post_alpha + post_beta)
    ax.axvline(post_mean, color='red', linestyle=':', lw=1, alpha=0.5)
    ax.text(post_mean, ax.get_ylim()[1]*0.7, f'Posterior mean\n{post_mean:.2f}', 
            ha='center', fontsize=10, color='red')
    
    # Add formula
    formula_text = r'$P(\theta|D) = \frac{P(D|\theta) \cdot P(\theta)}{P(D)}$'
    ax.text(0.02, 0.98, formula_text, transform=ax.transAxes, fontsize=16,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Observations
    obs_text = 'Quan sát:\n• Posterior hẹp hơn Prior\n• Mean dịch về data (25%)\n• Uncertainty giảm!'
    ax.text(0.98, 0.98, obs_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='#E5FFE5', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'prior_to_posterior.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Image 7: Narrow vs Wide Posteriors ---
def create_narrow_vs_wide():
    """
    Compare narrow (certain) vs wide (uncertain) posteriors
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    theta = np.linspace(0, 1, 1000)
    
    # Posterior A: Narrow (n=400)
    post_a = stats.beta(100, 300)
    pdf_a = post_a.pdf(theta)
    axes[0].plot(theta, pdf_a, 'g-', lw=3)
    axes[0].fill_between(theta, pdf_a, alpha=0.3, color='green')
    axes[0].set_title('Posterior A: Narrow (Chắc chắn)', fontsize=14, weight='bold', color='green')
    axes[0].set_xlabel('θ', fontsize=12)
    axes[0].set_ylabel('Density', fontsize=12)
    axes[0].grid(alpha=0.3)
    
    # Add stats
    mean_a = 0.25
    std_a = 0.021
    ci_a = post_a.ppf([0.025, 0.975])
    stats_text_a = f'Mean = {mean_a:.3f}\nSD = {std_a:.3f}\n95% CI = [{ci_a[0]:.2f}, {ci_a[1]:.2f}]\nn = 400'
    axes[0].text(0.5, 0.95, stats_text_a, transform=axes[0].transAxes,
                 verticalalignment='top', fontsize=11,
                 bbox=dict(boxstyle='round', facecolor='#E5FFE5', alpha=0.9))
    
    # Confidence level
    axes[0].text(0.5, 0.05, '✅ Rất chắc chắn!\n✅ Có thể quyết định ngay', 
                 transform=axes[0].transAxes, ha='center', fontsize=11, weight='bold', color='green')
    
    # Posterior B: Wide (n=40)
    post_b = stats.beta(10, 30)
    pdf_b = post_b.pdf(theta)
    axes[1].plot(theta, pdf_b, 'orange', lw=3)
    axes[1].fill_between(theta, pdf_b, alpha=0.3, color='orange')
    axes[1].set_title('Posterior B: Wide (Không chắc chắn)', fontsize=14, weight='bold', color='orange')
    axes[1].set_xlabel('θ', fontsize=12)
    axes[1].set_ylabel('Density', fontsize=12)
    axes[1].grid(alpha=0.3)
    
    # Add stats
    mean_b = 0.25
    std_b = 0.067
    ci_b = post_b.ppf([0.025, 0.975])
    stats_text_b = f'Mean = {mean_b:.3f}\nSD = {std_b:.3f}\n95% CI = [{ci_b[0]:.2f}, {ci_b[1]:.2f}]\nn = 40'
    axes[1].text(0.5, 0.95, stats_text_b, transform=axes[1].transAxes,
                 verticalalignment='top', fontsize=11,
                 bbox=dict(boxstyle='round', facecolor='#FFE5CC', alpha=0.9))
    
    # Confidence level
    axes[1].text(0.5, 0.05, '⚠️ Chưa chắc chắn lắm\n⚠️ Nên thu thập thêm data', 
                 transform=axes[1].transAxes, ha='center', fontsize=11, weight='bold', color='orange')
    
    fig.suptitle('Độ Rộng của Phân phối = Mức độ Không chắc chắn', 
                 fontsize=16, weight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'narrow_vs_wide.png'), 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

# --- Main execution ---
if __name__ == "__main__":
    print("\n[1/7] Creating Minh's point estimate problem...")
    create_minh_point_estimate_problem()
    print("✅ Created: minh_point_estimate_problem.png")
    
    print("\n[2/7] Creating Minh's distribution solution...")
    create_minh_distribution_solution()
    print("✅ Created: minh_distribution_solution.png")
    
    print("\n[3/7] Creating distribution as belief map...")
    create_distribution_belief_map()
    print("✅ Created: distribution_belief_map.png")
    
    print("\n[4/7] Creating three types of priors...")
    create_three_priors()
    print("✅ Created: three_priors.png")
    
    print("\n[5/7] Creating likelihood function...")
    create_likelihood_function()
    print("✅ Created: likelihood_function.png")
    
    print("\n[6/7] Creating prior to posterior transformation...")
    create_prior_to_posterior()
    print("✅ Created: prior_to_posterior.png")
    
    print("\n[7/7] Creating narrow vs wide comparison...")
    create_narrow_vs_wide()
    print("✅ Created: narrow_vs_wide.png")
    
    print("\n" + "="*80)
    print("  ✅ ALL 7 IMAGES CREATED SUCCESSFULLY!")
    print("="*80)
    print("\nImages saved to:", output_dir)
    print("\nNext steps:")
    print("1. Check images in the output directory")
    print("2. Images are already embedded in the enhanced lesson")
    print("3. Ready to continue with Bài 2.2!")
