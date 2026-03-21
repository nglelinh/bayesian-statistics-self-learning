#!/usr/bin/env python3
"""
Generate odds vs probability visualization
Replaces code block at line 252 in 06_01_logistic_regression.md
"""

import numpy as np
import matplotlib.pyplot as plt

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'

# Generate probability range
p_range = np.linspace(0.01, 0.99, 100)
odds_range = p_range / (1 - p_range)
log_odds_range = np.log(odds_range)

# Create figure with 2 panels
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel 1: Probability to Odds
axes[0].plot(p_range, odds_range, 'b-', linewidth=3)
axes[0].axhline(1, color='red', linestyle='--', linewidth=2, alpha=0.7,
               label='odds = 1 (p = 0.5)')
axes[0].axvline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[0].set_xlabel('Probability (p)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Odds', fontsize=12, fontweight='bold')
axes[0].set_title('PROBABILITY → ODDS\nodds = p/(1-p)',
                 fontsize=14, fontweight='bold')
axes[0].grid(alpha=0.3)
axes[0].set_ylim(0, 10)

# Key points annotations
key_probs = [0.2, 0.5, 0.8]
colors = ['#e74c3c', '#f39c12', '#27ae60']
for p_val, color in zip(key_probs, colors):
    odds_val = p_val / (1 - p_val)
    axes[0].scatter([p_val], [odds_val], s=200, zorder=5, edgecolors='black',
                   linewidths=2, color=color)
    axes[0].text(p_val, odds_val + 0.8, f'p={p_val:.1f}\nodds={odds_val:.2f}',
                ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.7, edgecolor='black'))
axes[0].legend(fontsize=10)

# Panel 2: Probability to Log-Odds
axes[1].plot(p_range, log_odds_range, 'g-', linewidth=3)
axes[1].axhline(0, color='red', linestyle='--', linewidth=2, alpha=0.7,
               label='log-odds = 0 (p = 0.5)')
axes[1].axvline(0.5, color='red', linestyle='--', linewidth=2, alpha=0.7)
axes[1].set_xlabel('Probability (p)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Log-Odds', fontsize=12, fontweight='bold')
axes[1].set_title('PROBABILITY → LOG-ODDS\nlog-odds = log(p/(1-p)) = α + βx',
                 fontsize=14, fontweight='bold')
axes[1].grid(alpha=0.3)
axes[1].set_ylim(-4, 4)

# Key points for log-odds
for p_val, color in zip(key_probs, colors):
    log_odds_val = np.log(p_val / (1 - p_val))
    axes[1].scatter([p_val], [log_odds_val], s=200, zorder=5, edgecolors='black',
                   linewidths=2, color=color)
    axes[1].text(p_val, log_odds_val + 0.4, f'p={p_val:.1f}\nlog-odds={log_odds_val:.2f}',
                ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.7, edgecolor='black'))
axes[1].legend(fontsize=10)

plt.tight_layout()
plt.savefig('odds_probability_relationship.png', dpi=300, bbox_inches='tight',
            facecolor='white')
print("✓ Generated: odds_probability_relationship.png")
print("  - Left panel: Probability → Odds transformation")
print("  - Right panel: Probability → Log-Odds (logit) transformation")
print("  - Key points: p=0.2 (odds=0.25), p=0.5 (odds=1.0), p=0.8 (odds=4.0)")

plt.close()
