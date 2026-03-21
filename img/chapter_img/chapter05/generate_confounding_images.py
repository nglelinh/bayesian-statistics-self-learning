#!/usr/bin/env python3
"""
Generate images for Chapter 05.02: Confounding and DAGs
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

def linear_regression_fit(X, y):
    """Simple linear regression: y = a + bx"""
    X_mean = np.mean(X)
    y_mean = np.mean(y)
    b = np.sum((X - X_mean) * (y - y_mean)) / np.sum((X - X_mean)**2)
    a = y_mean - b * X_mean
    return a, b

def predict(X, a, b):
    """Predict using linear model"""
    return a + b * X

def draw_dag_node(ax, x, y, label, color='lightblue'):
    """Draw a node in DAG"""
    circle = mpatches.Circle((x, y), 0.08, color=color, ec='black', linewidth=2, zorder=3)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', fontsize=14, fontweight='bold', zorder=4)

def draw_dag_arrow(ax, x1, y1, x2, y2):
    """Draw an arrow in DAG"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=20, linewidth=2,
                           color='black', zorder=2)
    ax.add_patch(arrow)

# Set style
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# Image 1: Simpson's Paradox
print("Generating simpsons_paradox.png...")
np.random.seed(42)
n = 50

# Group A (severe cases): High treatment intensity, but worse outcomes
treatment_A = np.random.uniform(7, 10, n)
success_A = 40 + 2*treatment_A + np.random.normal(0, 3, n)

# Group B (mild cases): Low treatment intensity, better outcomes  
treatment_B = np.random.uniform(0, 3, n)
success_B = 80 + 2*treatment_B + np.random.normal(0, 3, n)

# Combine
treatment_all = np.concatenate([treatment_A, treatment_B])
success_all = np.concatenate([success_A, success_B])
severity = np.array(['Severe']*n + ['Mild']*n)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Overall (ignoring severity)
a_overall, b_overall = linear_regression_fit(treatment_all, success_all)
x_line = np.linspace(0, 10, 100)

axes[0].scatter(treatment_all, success_all, s=80, alpha=0.6, edgecolors='black')
axes[0].plot(x_line, predict(x_line, a_overall, b_overall), 
            'r-', linewidth=3, label=f'β = {b_overall:.2f}')
axes[0].set_xlabel('Treatment Intensity', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
axes[0].set_title('IGNORING Severity\n' +
                 f'β = {b_overall:.2f} (NEGATIVE!)\n' +
                 'More treatment → Worse outcome?',
                 fontsize=14, fontweight='bold', color='red')
axes[0].legend(fontsize=11)
axes[0].grid(alpha=0.3)

# By severity group
colors = {'Severe': 'red', 'Mild': 'blue'}
for sev in ['Severe', 'Mild']:
    mask = severity == sev
    axes[1].scatter(treatment_all[mask], success_all[mask], 
                   s=80, alpha=0.6, label=sev, 
                   color=colors[sev], edgecolors='black')
    
    # Fit within group
    a_group, b_group = linear_regression_fit(treatment_all[mask], success_all[mask])
    axes[1].plot(x_line, predict(x_line, a_group, b_group),
                '-', linewidth=2, color=colors[sev],
                label=f'{sev}: β = {b_group:.2f}')

axes[1].set_xlabel('Treatment Intensity', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Success Rate (%)', fontsize=12, fontweight='bold')
axes[1].set_title('CONTROLLING for Severity\n' +
                 'β = +2 (POSITIVE!) for both groups\n' +
                 'More treatment → Better outcome!',
                 fontsize=14, fontweight='bold', color='green')
axes[1].legend(fontsize=11)
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('simpsons_paradox.png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"  ✓ Saved: simpsons_paradox.png")
plt.close()

# Image 2: DAG Types
print("Generating dag_types.png...")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# 1. Simple causation: X → Y
axes[0, 0].set_xlim(-0.2, 1.2)
axes[0, 0].set_ylim(-0.5, 0.5)
axes[0, 0].axis('off')
axes[0, 0].set_title('Simple Causation\nX → Y', fontsize=13, fontweight='bold')
draw_dag_node(axes[0, 0], 0, 0, 'X', 'lightblue')
draw_dag_node(axes[0, 0], 1, 0, 'Y', 'lightblue')
draw_dag_arrow(axes[0, 0], 0.08, 0, 0.92, 0)
axes[0, 0].text(0.5, -0.35, 'X causes Y\nNo confounding',
               ha='center', fontsize=11)

# 2. Confounding: Z → X, Z → Y
axes[0, 1].set_xlim(-0.2, 1.2)
axes[0, 1].set_ylim(-0.2, 1.2)
axes[0, 1].axis('off')
axes[0, 1].set_title('Confounding\nZ → X, Z → Y', fontsize=13, fontweight='bold')
draw_dag_node(axes[0, 1], 0.5, 1, 'Z', 'lightcoral')
draw_dag_node(axes[0, 1], 0, 0, 'X', 'lightcoral')
draw_dag_node(axes[0, 1], 1, 0, 'Y', 'lightcoral')
draw_dag_arrow(axes[0, 1], 0.45, 0.93, 0.05, 0.07)
draw_dag_arrow(axes[0, 1], 0.55, 0.93, 0.95, 0.07)
axes[0, 1].text(0.5, -0.15, 'Z confounds X-Y relationship\nMUST control for Z',
               ha='center', fontsize=11)

# 3. Mediation: X → M → Y
axes[0, 2].set_xlim(-0.2, 1.2)
axes[0, 2].set_ylim(-0.5, 0.5)
axes[0, 2].axis('off')
axes[0, 2].set_title('Mediation\nX → M → Y', fontsize=13, fontweight='bold')
draw_dag_node(axes[0, 2], 0, 0, 'X', 'lightgreen')
draw_dag_node(axes[0, 2], 0.5, 0, 'M', 'lightgreen')
draw_dag_node(axes[0, 2], 1, 0, 'Y', 'lightgreen')
draw_dag_arrow(axes[0, 2], 0.08, 0, 0.42, 0)
draw_dag_arrow(axes[0, 2], 0.58, 0, 0.92, 0)
axes[0, 2].text(0.5, -0.35, 'M is mediator\nDO NOT control for M\n(blocks causal path)',
               ha='center', fontsize=11)

# 4. Collider: X → C ← Y
axes[1, 0].set_xlim(-0.2, 1.2)
axes[1, 0].set_ylim(-0.2, 1.2)
axes[1, 0].axis('off')
axes[1, 0].set_title('Collider\nX → C ← Y', fontsize=13, fontweight='bold')
draw_dag_node(axes[1, 0], 0, 1, 'X', 'lightyellow')
draw_dag_node(axes[1, 0], 1, 1, 'Y', 'lightyellow')
draw_dag_node(axes[1, 0], 0.5, 0, 'C', 'lightyellow')
draw_dag_arrow(axes[1, 0], 0.05, 0.93, 0.45, 0.07)
draw_dag_arrow(axes[1, 0], 0.95, 0.93, 0.55, 0.07)
axes[1, 0].text(0.5, -0.15, 'C is collider\nDO NOT control for C\n(creates spurious correlation)',
               ha='center', fontsize=11)

# 5. Chain: X → M → Y with confounding
axes[1, 1].set_xlim(-0.2, 1.2)
axes[1, 1].set_ylim(-0.2, 1.7)
axes[1, 1].axis('off')
axes[1, 1].set_title('Complex: Chain + Confounding', fontsize=13, fontweight='bold')
draw_dag_node(axes[1, 1], 0.5, 1.5, 'Z', 'lightpink')
draw_dag_node(axes[1, 1], 0, 0.5, 'X', 'lightpink')
draw_dag_node(axes[1, 1], 0.5, 0.5, 'M', 'lightpink')
draw_dag_node(axes[1, 1], 1, 0.5, 'Y', 'lightpink')
draw_dag_arrow(axes[1, 1], 0.08, 0.5, 0.42, 0.5)
draw_dag_arrow(axes[1, 1], 0.58, 0.5, 0.92, 0.5)
draw_dag_arrow(axes[1, 1], 0.45, 1.43, 0.05, 0.57)
draw_dag_arrow(axes[1, 1], 0.55, 1.43, 0.95, 0.57)
axes[1, 1].text(0.5, -0.1, 'Multiple causal paths\nCareful analysis needed',
               ha='center', fontsize=11)

# 6. Summary text
axes[1, 2].axis('off')
summary_text = """
DAG RULES FOR CAUSAL INFERENCE

✓ MUST control for:
  • Confounders (Z → X, Z → Y)
  • Backdoor paths to X

✗ DO NOT control for:
  • Mediators (X → M → Y)
  • Colliders (X → C ← Y)
  • Descendants of treatment

Key principle:
Block all backdoor paths
Keep all frontdoor paths open
"""
axes[1, 2].text(0.5, 0.5, summary_text, fontsize=12, family='monospace',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.savefig('dag_types.png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"  ✓ Saved: dag_types.png")
plt.close()

print("\n✅ All images generated successfully!")
