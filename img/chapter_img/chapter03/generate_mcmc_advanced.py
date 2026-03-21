#!/usr/bin/env python3
"""
Script để tạo các hình ảnh minh họa nâng cao cho MCMC - Chapter 03

Các visualizations mới:
1. Random Walk vs Directed Sampling (HMC)
2. Acceptance Rate Effects
3. Chain Mixing Quality
4. Warmup/Tuning Phase
5. Multiple Chains Convergence

Sử dụng:
    python3 generate_mcmc_advanced.py

Yêu cầu:
    - numpy
    - matplotlib
    - scipy
    - seaborn

Tác giả: Nguyen Le Linh
Ngày: 09/03/2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import os

# Cấu hình style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

# Tạo thư mục output nếu chưa tồn tại
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_figure(filename):
    """Lưu figure với đường dẫn đầy đủ"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f'✓ Đã tạo: {filename}')
    plt.close()

def target_distribution(x, y):
    """Target: Banana-shaped distribution (challenging for MCMC)"""
    return np.exp(-0.5 * (x**2 / 4 + (y + 0.05*x**2 - 2)**2))

def generate_random_walk_vs_hmc():
    """Hình 1: Random Walk Metropolis vs HMC-like Directed Sampling"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    
    np.random.seed(42)
    n_samples = 500
    
    # Create grid for contour
    x = np.linspace(-6, 6, 200)
    y = np.linspace(-1, 5, 200)
    X, Y = np.meshgrid(x, y)
    Z = target_distribution(X, Y)
    
    # Random Walk Metropolis (small steps)
    rwm_samples = [(0.0, 2.0)]
    rwm_accepted = 0
    
    for _ in range(n_samples - 1):
        current = rwm_samples[-1]
        
        # Propose: random walk with small steps
        proposal = (current[0] + np.random.normal(0, 0.5),
                   current[1] + np.random.normal(0, 0.5))
        
        # Metropolis acceptance
        current_density = target_distribution(current[0], current[1])
        proposal_density = target_distribution(proposal[0], proposal[1])
        
        ratio = proposal_density / current_density
        if np.random.rand() < ratio:
            rwm_samples.append(proposal)
            rwm_accepted += 1
        else:
            rwm_samples.append(current)
    
    rwm_samples = np.array(rwm_samples)
    
    # HMC-like (directed sampling with momentum)
    hmc_samples = [(0.0, 2.0)]
    hmc_accepted = 0
    
    for _ in range(n_samples - 1):
        current = hmc_samples[-1]
        
        # Simulate momentum-based proposal (simplified)
        # Compute gradient direction (towards higher density)
        dx = -current[0] / 4  # Gradient approximation
        dy = -(current[1] + 0.05*current[0]**2 - 2)
        
        # Add momentum
        momentum_x = dx * 0.3 + np.random.normal(0, 0.3)
        momentum_y = dy * 0.3 + np.random.normal(0, 0.3)
        
        proposal = (current[0] + momentum_x,
                   current[1] + momentum_y)
        
        # Metropolis acceptance
        current_density = target_distribution(current[0], current[1])
        proposal_density = target_distribution(proposal[0], proposal[1])
        
        ratio = proposal_density / current_density
        if np.random.rand() < ratio:
            hmc_samples.append(proposal)
            hmc_accepted += 1
        else:
            hmc_samples.append(current)
    
    hmc_samples = np.array(hmc_samples)
    
    # Panel 1: RWM - Contour + Path
    axes[0, 0].contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.6)
    axes[0, 0].plot(rwm_samples[:, 0], rwm_samples[:, 1], 
                    'r-', linewidth=1, alpha=0.5)
    axes[0, 0].plot(rwm_samples[:50, 0], rwm_samples[:50, 1], 
                    'r-', linewidth=2, alpha=0.9, label='First 50 steps')
    axes[0, 0].plot(rwm_samples[0, 0], rwm_samples[0, 1], 
                    'g*', markersize=20, label='Start')
    axes[0, 0].set_title('Random Walk Metropolis\nRandom, aimless exploration', 
                         fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('x', fontsize=11)
    axes[0, 0].set_ylabel('y', fontsize=11)
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].set_xlim([-6, 6])
    axes[0, 0].set_ylim([-1, 5])
    
    # Panel 2: HMC - Contour + Path
    axes[0, 1].contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.6)
    axes[0, 1].plot(hmc_samples[:, 0], hmc_samples[:, 1], 
                    'b-', linewidth=1, alpha=0.5)
    axes[0, 1].plot(hmc_samples[:50, 0], hmc_samples[:50, 1], 
                    'b-', linewidth=2, alpha=0.9, label='First 50 steps')
    axes[0, 1].plot(hmc_samples[0, 0], hmc_samples[0, 1], 
                    'g*', markersize=20, label='Start')
    axes[0, 1].set_title('HMC-like Sampling\nDirected, efficient exploration', 
                         fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('x', fontsize=11)
    axes[0, 1].set_ylabel('y', fontsize=11)
    axes[0, 1].legend(fontsize=9)
    axes[0, 1].set_xlim([-6, 6])
    axes[0, 1].set_ylim([-1, 5])
    
    # Panel 3: Comparison stats
    axes[0, 2].axis('off')
    stats_text = f"""
╔════════════════════════════════════╗
║        COMPARISON STATS            ║
╠════════════════════════════════════╣
║                                    ║
║  RANDOM WALK METROPOLIS:           ║
║    Acceptance: {rwm_accepted/n_samples*100:.1f}%             ║
║    Strategy: Random steps          ║
║    Efficiency: LOW                 ║
║    Autocorr: HIGH                  ║
║                                    ║
║  HMC-LIKE:                         ║
║    Acceptance: {hmc_accepted/n_samples*100:.1f}%             ║
║    Strategy: Gradient-guided       ║
║    Efficiency: HIGH                ║
║    Autocorr: LOW                   ║
║                                    ║
║  WHY HMC BETTER?                   ║
║    ✓ Uses gradient info            ║
║    ✓ Directed moves                ║
║    ✓ Covers space faster           ║
║    ✓ Lower autocorrelation         ║
║                                    ║
╚════════════════════════════════════╝
"""
    axes[0, 2].text(0.5, 0.5, stats_text, fontsize=9, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
    
    # Panel 4: RWM Trace X
    axes[1, 0].plot(rwm_samples[:, 0], linewidth=1, color='red', alpha=0.7)
    axes[1, 0].set_title('RWM: Trace Plot (x)', fontsize=11, fontweight='bold')
    axes[1, 0].set_xlabel('Iteration', fontsize=10)
    axes[1, 0].set_ylabel('x value', fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].text(0.05, 0.95, 'Slow mixing\nMany plateaus', 
                    transform=axes[1, 0].transAxes,
                    fontsize=10, ha='left', va='top',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Panel 5: HMC Trace X
    axes[1, 1].plot(hmc_samples[:, 0], linewidth=1, color='blue', alpha=0.7)
    axes[1, 1].set_title('HMC: Trace Plot (x)', fontsize=11, fontweight='bold')
    axes[1, 1].set_xlabel('Iteration', fontsize=10)
    axes[1, 1].set_ylabel('x value', fontsize=10)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].text(0.05, 0.95, 'Fast mixing\nGood exploration', 
                    transform=axes[1, 1].transAxes,
                    fontsize=10, ha='left', va='top',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    # Panel 6: Autocorrelation comparison
    lag_max = 50
    
    # RWM autocorr
    rwm_x_centered = rwm_samples[:, 0] - np.mean(rwm_samples[:, 0])
    rwm_autocorr = np.correlate(rwm_x_centered, rwm_x_centered, mode='full')
    rwm_autocorr = rwm_autocorr[len(rwm_autocorr)//2:len(rwm_autocorr)//2 + lag_max]
    rwm_autocorr = rwm_autocorr / rwm_autocorr[0]
    
    # HMC autocorr
    hmc_x_centered = hmc_samples[:, 0] - np.mean(hmc_samples[:, 0])
    hmc_autocorr = np.correlate(hmc_x_centered, hmc_x_centered, mode='full')
    hmc_autocorr = hmc_autocorr[len(hmc_autocorr)//2:len(hmc_autocorr)//2 + lag_max]
    hmc_autocorr = hmc_autocorr / hmc_autocorr[0]
    
    axes[1, 2].plot(rwm_autocorr, 'r-', linewidth=2.5, label='RWM', alpha=0.8)
    axes[1, 2].plot(hmc_autocorr, 'b-', linewidth=2.5, label='HMC', alpha=0.8)
    axes[1, 2].axhline(0, color='black', linestyle='-', linewidth=1)
    axes[1, 2].axhline(0.1, color='gray', linestyle='--', linewidth=1.5,
                       label='Threshold')
    axes[1, 2].set_title('Autocorrelation Comparison', fontsize=11, fontweight='bold')
    axes[1, 2].set_xlabel('Lag', fontsize=10)
    axes[1, 2].set_ylabel('Autocorrelation', fontsize=10)
    axes[1, 2].legend(fontsize=10)
    axes[1, 2].grid(True, alpha=0.3)
    axes[1, 2].set_ylim([-0.2, 1.1])
    
    plt.suptitle('Random Walk Metropolis vs HMC-like Directed Sampling\n' + 
                 'HMC uses gradient information for efficient exploration', 
                 fontsize=15, fontweight='bold')
    plt.tight_layout()
    save_figure('random_walk_vs_hmc_directed.png')

def generate_acceptance_rate_effects():
    """Hình 2: Effects of Different Acceptance Rates"""
    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    
    np.random.seed(42)
    n_samples = 1000
    
    # Target: Simple Normal(0, 1)
    target_mean = 0
    target_std = 1
    
    # Different proposal widths → different acceptance rates
    proposal_stds = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    
    for idx, prop_std in enumerate(proposal_stds):
        if idx >= 6:
            break
            
        row = idx // 3
        col = idx % 3
        
        # Run Metropolis
        samples = [0.0]
        accepted = 0
        
        for _ in range(n_samples - 1):
            current = samples[-1]
            proposal = current + np.random.normal(0, prop_std)
            
            # Metropolis
            current_density = stats.norm.pdf(current, target_mean, target_std)
            proposal_density = stats.norm.pdf(proposal, target_mean, target_std)
            
            ratio = proposal_density / current_density
            if np.random.rand() < ratio:
                samples.append(proposal)
                accepted += 1
            else:
                samples.append(current)
        
        samples = np.array(samples)
        acceptance_rate = accepted / n_samples
        
        # Plot trace
        axes[row, col].plot(samples, linewidth=1, alpha=0.7, color='blue')
        axes[row, col].axhline(target_mean, color='red', linestyle='--', 
                               linewidth=2, label='True mean')
        axes[row, col].set_title(f'Proposal σ = {prop_std:.1f}\n' + 
                                 f'Acceptance: {acceptance_rate*100:.1f}%', 
                                 fontsize=11, fontweight='bold')
        axes[row, col].set_xlabel('Iteration', fontsize=10)
        axes[row, col].set_ylabel('Value', fontsize=10)
        axes[row, col].grid(True, alpha=0.3)
        axes[row, col].legend(fontsize=9)
        
        # Color-code by acceptance rate quality
        if 0.2 <= acceptance_rate <= 0.5:
            box_color = 'lightgreen'
            quality = 'GOOD'
        elif 0.1 <= acceptance_rate < 0.2 or 0.5 < acceptance_rate <= 0.7:
            box_color = 'yellow'
            quality = 'OK'
        else:
            box_color = 'lightcoral'
            quality = 'BAD'
        
        axes[row, col].text(0.95, 0.05, quality, 
                           transform=axes[row, col].transAxes,
                           fontsize=12, ha='right', va='bottom', fontweight='bold',
                           bbox=dict(boxstyle='round', facecolor=box_color, alpha=0.9))
    
    # Panel 7-9: Summary and recommendations
    axes[2, 0].axis('off')
    summary1 = """
╔══════════════════════════════╗
║   TOO LOW ACCEPTANCE         ║
║   (< 10%)                    ║
╠══════════════════════════════╣
║                              ║
║  Proposal σ = 5.0, 10.0      ║
║                              ║
║  PROBLEM:                    ║
║    • Proposals too far       ║
║    • Mostly rejected         ║
║    • Chain gets stuck        ║
║    • Poor exploration        ║
║                              ║
║  SOLUTION:                   ║
║    → Reduce proposal width   ║
║                              ║
╚══════════════════════════════╝
"""
    axes[2, 0].text(0.5, 0.5, summary1, fontsize=8.5, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.9))
    
    axes[2, 1].axis('off')
    summary2 = """
╔══════════════════════════════╗
║   OPTIMAL ACCEPTANCE         ║
║   (20-50%)                   ║
╠══════════════════════════════╣
║                              ║
║  Proposal σ = 0.5, 1.0, 2.0  ║
║                              ║
║  PERFECT:                    ║
║    ✓ Balanced exploration    ║
║    ✓ Good mixing             ║
║    ✓ Efficient sampling      ║
║    ✓ Low autocorrelation     ║
║                              ║
║  TARGET:                     ║
║    → 23.4% (optimal theory)  ║
║    → 20-50% (practical)      ║
║                              ║
╚══════════════════════════════╝
"""
    axes[2, 1].text(0.5, 0.5, summary2, fontsize=8.5, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9))
    
    axes[2, 2].axis('off')
    summary3 = """
╔══════════════════════════════╗
║   TOO HIGH ACCEPTANCE        ║
║   (> 70%)                    ║
╠══════════════════════════════╣
║                              ║
║  Proposal σ = 0.1            ║
║                              ║
║  PROBLEM:                    ║
║    • Proposals too close     ║
║    • Almost always accepted  ║
║    • Slow exploration        ║
║    • High autocorrelation    ║
║    • Like random walk        ║
║                              ║
║  SOLUTION:                   ║
║    → Increase proposal width ║
║                              ║
╚══════════════════════════════╝
"""
    axes[2, 2].text(0.5, 0.5, summary3, fontsize=8.5, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
    
    plt.suptitle('Acceptance Rate Effects on MCMC Performance\n' + 
                 'Target: 20-50% for univariate, lower for high-D', 
                 fontsize=15, fontweight='bold')
    plt.tight_layout()
    save_figure('acceptance_rate_effects.png')

def generate_chain_mixing_quality():
    """Hình 3: Chain Mixing Quality Assessment"""
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    
    np.random.seed(42)
    n_samples = 2000
    
    # Generate 3 chains with different mixing quality
    # Good mixing
    good_chain = [0.5]
    for _ in range(n_samples - 1):
        current = good_chain[-1]
        proposal = current + np.random.normal(0, 0.8)
        
        current_density = stats.norm.pdf(current, 0, 1)
        proposal_density = stats.norm.pdf(proposal, 0, 1)
        
        if np.random.rand() < proposal_density / current_density:
            good_chain.append(proposal)
        else:
            good_chain.append(current)
    good_chain = np.array(good_chain)
    
    # Medium mixing
    medium_chain = [0.5]
    for _ in range(n_samples - 1):
        current = medium_chain[-1]
        proposal = 0.8 * current + np.random.normal(0, 0.5)
        
        current_density = stats.norm.pdf(current, 0, 1)
        proposal_density = stats.norm.pdf(proposal, 0, 1)
        
        if np.random.rand() < proposal_density / current_density:
            medium_chain.append(proposal)
        else:
            medium_chain.append(current)
    medium_chain = np.array(medium_chain)
    
    # Poor mixing (stuck)
    poor_chain = [0.5]
    for i in range(n_samples - 1):
        current = poor_chain[-1]
        if i < 500:
            proposal = current + np.random.normal(0, 0.05)  # Stuck in one region
        elif i < 1000:
            proposal = -2 + np.random.normal(0, 0.05)  # Jump to another region
        elif i < 1500:
            proposal = 2 + np.random.normal(0, 0.05)
        else:
            proposal = current + np.random.normal(0, 0.05)
        
        current_density = stats.norm.pdf(current, 0, 1)
        proposal_density = stats.norm.pdf(proposal, 0, 1)
        
        if np.random.rand() < proposal_density / current_density:
            poor_chain.append(proposal)
        else:
            poor_chain.append(current)
    poor_chain = np.array(poor_chain)
    
    chains = [
        (good_chain, 'Good Mixing', 'green'),
        (medium_chain, 'Medium Mixing', 'orange'),
        (poor_chain, 'Poor Mixing (Stuck)', 'red')
    ]
    
    for idx, (chain, label, color) in enumerate(chains):
        # Trace plot
        ax1 = fig.add_subplot(gs[idx, 0])
        ax1.plot(chain, linewidth=1, alpha=0.7, color=color)
        ax1.axhline(0, color='black', linestyle='--', linewidth=2, alpha=0.5)
        ax1.set_title(f'{label}\nTrace Plot', fontsize=11, fontweight='bold')
        ax1.set_xlabel('Iteration', fontsize=10)
        ax1.set_ylabel('Value', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Histogram
        ax2 = fig.add_subplot(gs[idx, 1])
        ax2.hist(chain[200:], bins=50, density=True, alpha=0.7, 
                 color=color, edgecolor='black')
        
        # True distribution
        x_range = np.linspace(-4, 4, 200)
        true_density = stats.norm.pdf(x_range, 0, 1)
        ax2.plot(x_range, true_density, 'k-', linewidth=3, label='True N(0,1)')
        
        ax2.set_title('Histogram vs True', fontsize=11, fontweight='bold')
        ax2.set_xlabel('Value', fontsize=10)
        ax2.set_ylabel('Density', fontsize=10)
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)
        
        # Autocorrelation
        ax3 = fig.add_subplot(gs[idx, 2])
        lag_max = 100
        
        chain_centered = chain - np.mean(chain)
        autocorr = np.correlate(chain_centered, chain_centered, mode='full')
        autocorr = autocorr[len(autocorr)//2:len(autocorr)//2 + lag_max]
        autocorr = autocorr / autocorr[0]
        
        ax3.bar(range(lag_max), autocorr, alpha=0.7, color=color, 
                edgecolor='black', width=1)
        ax3.axhline(0, color='black', linestyle='-', linewidth=1)
        ax3.axhline(0.1, color='red', linestyle='--', linewidth=2,
                    label='Threshold')
        ax3.set_title('Autocorrelation', fontsize=11, fontweight='bold')
        ax3.set_xlabel('Lag', fontsize=10)
        ax3.set_ylabel('ACF', fontsize=10)
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim([-0.2, 1.1])
        
        # ESS
        ess = len(chain) / (1 + 2 * np.sum(autocorr[1:][autocorr[1:] > 0]))
        ax3.text(0.95, 0.95, f'ESS: {ess:.0f}\n({ess/len(chain)*100:.1f}%)', 
                 transform=ax3.transAxes, fontsize=10, ha='right', va='top',
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.9))
        
        if idx == 0:
            ax3.legend(fontsize=9)
    
    plt.suptitle('Chain Mixing Quality Assessment\n' + 
                 'Trace plot + Histogram + Autocorrelation', 
                 fontsize=15, fontweight='bold')
    save_figure('chain_mixing_quality.png')

def generate_warmup_tuning_phase():
    """Hình 4: Warmup/Tuning Phase Visualization"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    np.random.seed(42)
    
    # Simulate adaptive tuning
    n_warmup = 500
    n_sampling = 1000
    n_total = n_warmup + n_sampling
    
    # Start with bad proposal width
    proposal_std = 5.0
    samples = [3.0]  # Bad starting point
    proposal_stds = [proposal_std]
    acceptance_rates = []
    
    window = 50  # Adaptation window
    
    for i in range(n_total - 1):
        current = samples[-1]
        proposal = current + np.random.normal(0, proposal_std)
        
        # Target: N(0, 1)
        current_density = stats.norm.pdf(current, 0, 1)
        proposal_density = stats.norm.pdf(proposal, 0, 1)
        
        accepted = 0
        if np.random.rand() < proposal_density / current_density:
            samples.append(proposal)
            accepted = 1
        else:
            samples.append(current)
        
        acceptance_rates.append(accepted)
        
        # Adaptation during warmup
        if i < n_warmup and (i + 1) % window == 0:
            recent_acceptance = np.mean(acceptance_rates[-window:])
            
            # Adapt proposal width
            if recent_acceptance < 0.2:
                proposal_std *= 0.8  # Decrease
            elif recent_acceptance > 0.5:
                proposal_std *= 1.2  # Increase
        
        proposal_stds.append(proposal_std)
    
    samples = np.array(samples)
    proposal_stds = np.array(proposal_stds)
    
    # Running acceptance rate
    running_acceptance = np.cumsum(acceptance_rates) / np.arange(1, len(acceptance_rates) + 1)
    
    # Panel 1: Trace with warmup highlighted
    axes[0, 0].plot(samples, linewidth=1, alpha=0.7, color='blue')
    axes[0, 0].axvline(n_warmup, color='red', linestyle='--', linewidth=3,
                       label='Warmup end')
    axes[0, 0].axhline(0, color='green', linestyle='--', linewidth=2,
                       label='True mean', alpha=0.6)
    axes[0, 0].axvspan(0, n_warmup, alpha=0.2, color='orange', label='Warmup')
    axes[0, 0].axvspan(n_warmup, n_total, alpha=0.2, color='lightblue', 
                       label='Sampling')
    axes[0, 0].set_title('Trace Plot with Warmup Phase', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Iteration', fontsize=11)
    axes[0, 0].set_ylabel('Value', fontsize=11)
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Panel 2: Proposal width adaptation
    axes[0, 1].plot(proposal_stds, linewidth=2, color='purple')
    axes[0, 1].axvline(n_warmup, color='red', linestyle='--', linewidth=3,
                       label='Warmup end')
    axes[0, 1].axhline(1.0, color='green', linestyle='--', linewidth=2,
                       label='Optimal ~1.0', alpha=0.6)
    axes[0, 1].set_title('Proposal Width Adaptation', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Iteration', fontsize=11)
    axes[0, 1].set_ylabel('Proposal σ', fontsize=11)
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].text(0.5, 0.95, 'Algorithm learns\noptimal step size', 
                    transform=axes[0, 1].transAxes, fontsize=10, ha='center', va='top',
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # Panel 3: Running acceptance rate
    axes[1, 0].plot(running_acceptance, linewidth=2, color='darkgreen')
    axes[1, 0].axvline(n_warmup, color='red', linestyle='--', linewidth=3)
    axes[1, 0].axhline(0.234, color='blue', linestyle='--', linewidth=2,
                       label='Optimal ~23.4%', alpha=0.7)
    axes[1, 0].axhspan(0.2, 0.5, alpha=0.2, color='lightgreen', 
                       label='Good range')
    axes[1, 0].set_title('Running Acceptance Rate', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Iteration', fontsize=11)
    axes[1, 0].set_ylabel('Acceptance Rate', fontsize=11)
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_ylim([0, 1])
    
    # Panel 4: Before vs After warmup comparison
    axes[1, 1].hist(samples[:n_warmup], bins=30, alpha=0.5, density=True,
                    label=f'Warmup (n={n_warmup})', color='orange', edgecolor='black')
    axes[1, 1].hist(samples[n_warmup:], bins=30, alpha=0.5, density=True,
                    label=f'Post-warmup (n={n_sampling})', color='blue', edgecolor='black')
    
    x_range = np.linspace(-4, 4, 200)
    true_density = stats.norm.pdf(x_range, 0, 1)
    axes[1, 1].plot(x_range, true_density, 'k-', linewidth=3, 
                    label='True N(0,1)')
    
    axes[1, 1].set_title('Distribution: Before vs After Warmup', 
                         fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Value', fontsize=11)
    axes[1, 1].set_ylabel('Density', fontsize=11)
    axes[1, 1].legend(fontsize=10)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].text(0.5, 0.95, 'Post-warmup samples\nare cleaner!', 
                    transform=axes[1, 1].transAxes, fontsize=10, ha='center', va='top',
                    bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.suptitle('Warmup/Tuning Phase: Algorithm Learns Optimal Parameters\n' + 
                 'Discard warmup samples - they are biased!', 
                 fontsize=15, fontweight='bold')
    plt.tight_layout()
    save_figure('warmup_tuning_phase.png')

def main():
    """Hàm chính để tạo tất cả các hình ảnh"""
    print('='*70)
    print('BẮT ĐẦU TẠO HÌNH ẢNH MCMC NÂNG CAO CHO CHAPTER 03')
    print('='*70)
    print()
    
    print('Phần 1/4: Random Walk vs HMC Directed Sampling')
    generate_random_walk_vs_hmc()
    print('✓ Hoàn thành phần 1/4\n')
    
    print('Phần 2/4: Acceptance Rate Effects')
    generate_acceptance_rate_effects()
    print('✓ Hoàn thành phần 2/4\n')
    
    print('Phần 3/4: Chain Mixing Quality')
    generate_chain_mixing_quality()
    print('✓ Hoàn thành phần 3/4\n')
    
    print('Phần 4/4: Warmup/Tuning Phase')
    generate_warmup_tuning_phase()
    print('✓ Hoàn thành phần 4/4\n')
    
    print('='*70)
    print('TẤT CẢ HÌNH ẢNH ĐÃ ĐƯỢC TẠO THÀNH CÔNG!')
    print('='*70)
    print()
    print('Danh sách các file đã tạo:')
    print('1. random_walk_vs_hmc_directed.png')
    print('2. acceptance_rate_effects.png')
    print('3. chain_mixing_quality.png')
    print('4. warmup_tuning_phase.png')
    print()
    print(f'Thư mục output: {OUTPUT_DIR}')

if __name__ == '__main__':
    main()
