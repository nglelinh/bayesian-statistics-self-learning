#!/usr/bin/env python3
"""
Generate comprehensive causal inference diagrams for Chapter 05

Topics covered:
1. Basic DAG concepts (confounders, mediators, colliders)
2. Backdoor paths and d-separation
3. Collider bias (Berkson's paradox)
4. Mediation analysis
5. Adjustment sets
6. Common causal structures (fork, chain, inverted fork)
7. Simpson's paradox with DAGs

Author: Nguyen Le Linh
Date: March 9, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import seaborn as sns

# Set style
sns.set_style('white')
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'

def save_figure(filename, dpi=300):
    """Save figure with high quality"""
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f'✅ Generated: {filename}')
    plt.close()


def draw_node(ax, x, y, label, color='lightblue', size=0.15):
    """Draw a circular node for DAG"""
    circle = Circle((x, y), size, color=color, ec='black', linewidth=2, zorder=3)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', fontsize=12, 
            fontweight='bold', zorder=4)


def draw_arrow(ax, x1, y1, x2, y2, color='black', linewidth=2, style='solid'):
    """Draw an arrow between nodes"""
    # Calculate direction and shorten arrow to stop at circle edge
    dx = x2 - x1
    dy = y2 - y1
    length = np.sqrt(dx**2 + dy**2)
    
    # Shorten by circle radius (0.15)
    factor = (length - 0.17) / length
    x2_adj = x1 + dx * factor
    y2_adj = y1 + dy * factor
    
    arrow = FancyArrowPatch((x1, y1), (x2_adj, y2_adj),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=linewidth, color=color,
                           linestyle=style, zorder=2)
    ax.add_patch(arrow)


def generate_basic_structures():
    """Generate the three basic causal structures: fork, chain, inverted fork"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    structures = [
        ('Fork (Confounder)', 'Z causes both X and Y', 'lightcoral'),
        ('Chain (Mediator)', 'X causes Z, Z causes Y', 'lightgreen'),
        ('Inverted Fork (Collider)', 'X and Y both cause Z', 'lightyellow')
    ]
    
    for idx, (title, desc, color) in enumerate(structures):
        ax = axes[idx]
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        ax.axis('off')
        
        if idx == 0:  # Fork (Confounder)
            # Z at top, X and Y at bottom
            draw_node(ax, 1.5, 2.2, 'Z', color)
            draw_node(ax, 0.7, 0.8, 'X', 'lightblue')
            draw_node(ax, 2.3, 0.8, 'Y', 'lightblue')
            draw_arrow(ax, 1.5, 2.05, 0.85, 0.95)  # Z -> X
            draw_arrow(ax, 1.5, 2.05, 2.15, 0.95)  # Z -> Y
            
            # Show direct path (dashed)
            draw_arrow(ax, 0.85, 0.8, 2.15, 0.8, color='red', 
                      style='dashed', linewidth=1.5)
            
            ax.text(1.5, 2.7, 'CONFOUNDER', ha='center', fontsize=14, 
                   fontweight='bold', color='darkred')
            
        elif idx == 1:  # Chain (Mediator)
            # X -> Z -> Y (horizontal)
            draw_node(ax, 0.5, 1.5, 'X', 'lightblue')
            draw_node(ax, 1.5, 1.5, 'Z', color)
            draw_node(ax, 2.5, 1.5, 'Y', 'lightblue')
            draw_arrow(ax, 0.65, 1.5, 1.35, 1.5)  # X -> Z
            draw_arrow(ax, 1.65, 1.5, 2.35, 1.5)  # Z -> Y
            
            ax.text(1.5, 2.7, 'MEDIATOR', ha='center', fontsize=14, 
                   fontweight='bold', color='darkgreen')
            
        else:  # Inverted Fork (Collider)
            # X and Y at top, Z at bottom
            draw_node(ax, 0.7, 2.2, 'X', 'lightblue')
            draw_node(ax, 2.3, 2.2, 'Y', 'lightblue')
            draw_node(ax, 1.5, 0.8, 'Z', color)
            draw_arrow(ax, 0.85, 2.05, 1.35, 0.95)  # X -> Z
            draw_arrow(ax, 2.15, 2.05, 1.65, 0.95)  # Y -> Z
            
            # Show blocked path (with X symbol)
            ax.plot([0.7, 2.3], [2.2, 2.2], 'r--', linewidth=1.5, alpha=0.5)
            ax.text(1.5, 2.2, '✗', ha='center', va='center', fontsize=20, 
                   color='red', fontweight='bold')
            
            ax.text(1.5, 2.7, 'COLLIDER', ha='center', fontsize=14, 
                   fontweight='bold', color='orange')
        
        # Title and description
        ax.text(1.5, 0.2, title, ha='center', fontsize=13, fontweight='bold')
        ax.text(1.5, -0.1, desc, ha='center', fontsize=10, style='italic')
    
    fig.suptitle('Three Basic Causal Structures', fontsize=16, fontweight='bold', y=0.98)
    save_figure('causal_basic_structures.png')


def generate_confounder_diagram():
    """Detailed confounder example with adjustment"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Unadjusted (biased)
    ax = axes[0]
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Education affects both Income and Health
    draw_node(ax, 2, 3, 'Education\n(Z)', 'lightcoral', 0.25)
    draw_node(ax, 0.8, 1.2, 'Exercise\n(X)', 'lightblue', 0.25)
    draw_node(ax, 3.2, 1.2, 'Health\n(Y)', 'lightblue', 0.25)
    
    draw_arrow(ax, 2, 2.75, 1.1, 1.45)  # Education -> Exercise
    draw_arrow(ax, 2, 2.75, 2.9, 1.45)  # Education -> Health
    draw_arrow(ax, 1.05, 1.2, 2.95, 1.2)  # Exercise -> Health (direct effect)
    
    # Show spurious correlation
    ax.text(2, 0.5, '❌ Spurious Correlation (Backdoor Path Open)', 
           ha='center', fontsize=12, color='red', fontweight='bold')
    ax.text(2, 0.2, 'Exercise ← Education → Health', 
           ha='center', fontsize=10, style='italic')
    
    ax.set_title('UNADJUSTED (Biased Estimate)', fontsize=14, fontweight='bold', pad=20)
    
    # Right: Adjusted (unbiased)
    ax = axes[1]
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Same structure but Education is "blocked"
    draw_node(ax, 2, 3, 'Education\n(Z)', 'lightgray', 0.25)  # Grayed out
    draw_node(ax, 0.8, 1.2, 'Exercise\n(X)', 'lightblue', 0.25)
    draw_node(ax, 3.2, 1.2, 'Health\n(Y)', 'lightblue', 0.25)
    
    # Dashed arrows to show blocked paths
    draw_arrow(ax, 2, 2.75, 1.1, 1.45, color='gray', style='dashed', linewidth=1.5)
    draw_arrow(ax, 2, 2.75, 2.9, 1.45, color='gray', style='dashed', linewidth=1.5)
    
    # Strong direct effect arrow
    draw_arrow(ax, 1.05, 1.2, 2.95, 1.2, color='green', linewidth=3)
    
    # Add "adjusted for" box around Education
    rect = FancyBboxPatch((1.5, 2.5), 1.0, 0.8, boxstyle="round,pad=0.05",
                          edgecolor='red', facecolor='none', linewidth=3, linestyle='--')
    ax.add_patch(rect)
    ax.text(2, 3.6, 'ADJUSTED', ha='center', fontsize=11, 
           color='red', fontweight='bold')
    
    ax.text(2, 0.5, '✅ Causal Effect Identified (Backdoor Path Blocked)', 
           ha='center', fontsize=12, color='green', fontweight='bold')
    ax.text(2, 0.2, 'Only direct effect remains', 
           ha='center', fontsize=10, style='italic')
    
    ax.set_title('ADJUSTED FOR EDUCATION (Unbiased)', fontsize=14, fontweight='bold', pad=20)
    
    fig.suptitle('Confounder: Adjustment Blocks Backdoor Paths', 
                fontsize=16, fontweight='bold', y=0.98)
    save_figure('confounder_adjustment.png')


def generate_mediator_diagram():
    """Detailed mediator example with total vs direct effects"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: Total effect (don't adjust for mediator)
    ax = axes[0]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    draw_node(ax, 1, 2, 'Training\n(X)', 'lightblue', 0.25)
    draw_node(ax, 2.5, 2, 'Skill\n(M)', 'lightgreen', 0.25)
    draw_node(ax, 4, 2, 'Performance\n(Y)', 'lightblue', 0.25)
    
    draw_arrow(ax, 1.25, 2, 2.25, 2)  # Training -> Skill
    draw_arrow(ax, 2.75, 2, 3.75, 2)  # Skill -> Performance
    
    # Show total effect path
    ax.annotate('', xy=(3.75, 2.5), xytext=(1.25, 2.5),
                arrowprops=dict(arrowstyle='->', lw=3, color='green'))
    ax.text(2.5, 2.8, 'Total Effect', ha='center', fontsize=11, 
           color='green', fontweight='bold')
    
    # Labels for indirect effect
    ax.text(1.625, 2.3, 'a', ha='center', fontsize=11, fontweight='bold', color='blue')
    ax.text(3.375, 2.3, 'b', ha='center', fontsize=11, fontweight='bold', color='blue')
    ax.text(2.5, 1.5, 'Indirect Effect = a × b', ha='center', fontsize=10, 
           style='italic', color='blue')
    
    ax.text(2.5, 0.5, '✅ DO NOT adjust for mediator', 
           ha='center', fontsize=12, color='green', fontweight='bold')
    ax.text(2.5, 0.2, 'To measure total effect', 
           ha='center', fontsize=10, style='italic')
    
    ax.set_title('TOTAL EFFECT (via Mediator)', fontsize=14, fontweight='bold', pad=20)
    
    # Right: Direct effect (adjust for mediator)
    ax = axes[1]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    draw_node(ax, 1, 2, 'Training\n(X)', 'lightblue', 0.25)
    draw_node(ax, 2.5, 2, 'Skill\n(M)', 'lightgray', 0.25)  # Grayed out
    draw_node(ax, 4, 2, 'Performance\n(Y)', 'lightblue', 0.25)
    
    # Dashed indirect path (blocked)
    draw_arrow(ax, 1.25, 2, 2.25, 2, color='gray', style='dashed', linewidth=1.5)
    draw_arrow(ax, 2.75, 2, 3.75, 2, color='gray', style='dashed', linewidth=1.5)
    
    # Direct effect (curved arrow)
    from matplotlib.patches import FancyBboxPatch, ConnectionPatch
    arrow = ConnectionPatch((1.25, 1.7), (3.75, 1.7), "data", "data",
                           arrowstyle='->', mutation_scale=20, linewidth=3,
                           color='orange', connectionstyle="arc3,rad=-.3")
    ax.add_artist(arrow)
    ax.text(2.5, 1.2, "Direct Effect (c')", ha='center', fontsize=11, 
           color='orange', fontweight='bold')
    
    # Adjusted box
    rect = FancyBboxPatch((2.0, 1.5), 1.0, 1.0, boxstyle="round,pad=0.05",
                          edgecolor='red', facecolor='none', linewidth=3, linestyle='--')
    ax.add_patch(rect)
    ax.text(2.5, 3.2, 'ADJUSTED', ha='center', fontsize=11, 
           color='red', fontweight='bold')
    
    ax.text(2.5, 0.5, 'Adjust for mediator', 
           ha='center', fontsize=12, color='orange', fontweight='bold')
    ax.text(2.5, 0.2, 'To measure direct effect only', 
           ha='center', fontsize=10, style='italic')
    
    ax.set_title('DIRECT EFFECT (blocking Mediator)', fontsize=14, fontweight='bold', pad=20)
    
    fig.suptitle('Mediator: Total Effect = Direct + Indirect Effects', 
                fontsize=16, fontweight='bold', y=0.98)
    save_figure('mediator_analysis.png')


def generate_collider_bias():
    """Illustrate collider bias (Berkson's paradox)"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left: True (no conditioning on collider)
    ax = axes[0]
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    draw_node(ax, 1, 3, 'Talent\n(X)', 'lightblue', 0.25)
    draw_node(ax, 3, 3, 'Looks\n(Y)', 'lightblue', 0.25)
    draw_node(ax, 2, 1.2, 'Celebrity\n(Z)', 'lightyellow', 0.25)
    
    draw_arrow(ax, 1.15, 2.75, 1.85, 1.45)  # Talent -> Celebrity
    draw_arrow(ax, 2.85, 2.75, 2.15, 1.45)  # Looks -> Celebrity
    
    # Show independence (no arrow)
    ax.plot([1, 3], [3, 3], 'g--', linewidth=2, alpha=0.5)
    ax.text(2, 3.3, '✓ Independent', ha='center', fontsize=11, 
           color='green', fontweight='bold')
    
    ax.text(2, 0.5, '✅ Path is BLOCKED (collider not adjusted)', 
           ha='center', fontsize=12, color='green', fontweight='bold')
    ax.text(2, 0.2, 'Talent and Looks are independent in general population', 
           ha='center', fontsize=10, style='italic')
    
    ax.set_title('GENERAL POPULATION\n(No Collider Bias)', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Right: Biased (conditioning on collider)
    ax = axes[1]
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    draw_node(ax, 1, 3, 'Talent\n(X)', 'lightblue', 0.25)
    draw_node(ax, 3, 3, 'Looks\n(Y)', 'lightblue', 0.25)
    draw_node(ax, 2, 1.2, 'Celebrity\n(Z)', 'lightyellow', 0.25)
    
    draw_arrow(ax, 1.15, 2.75, 1.85, 1.45)  # Talent -> Celebrity
    draw_arrow(ax, 2.85, 2.75, 2.15, 1.45)  # Looks -> Celebrity
    
    # Selection box around Celebrity
    rect = FancyBboxPatch((1.5, 0.7), 1.0, 1.0, boxstyle="round,pad=0.05",
                          edgecolor='red', facecolor='yellow', alpha=0.3, 
                          linewidth=3, linestyle='--')
    ax.add_patch(rect)
    ax.text(2, 0.4, 'CONDITIONED', ha='center', fontsize=11, 
           color='red', fontweight='bold')
    
    # Show spurious negative correlation
    ax.annotate('', xy=(2.75, 2.85), xytext=(1.25, 2.85),
                arrowprops=dict(arrowstyle='<->', lw=2, color='red'))
    ax.text(2, 3.3, '✗ Spurious Correlation!', ha='center', fontsize=11, 
           color='red', fontweight='bold')
    
    ax.text(2, 0.1, '❌ Path is OPENED (collider adjusted)', 
           ha='center', fontsize=12, color='red', fontweight='bold')
    ax.text(2, -0.2, 'Among celebrities: High talent → Low looks (spurious!)', 
           ha='center', fontsize=10, style='italic')
    
    ax.set_title('AMONG CELEBRITIES\n(Collider Bias - Berkson\'s Paradox)', 
                fontsize=14, fontweight='bold', pad=20)
    
    fig.suptitle('Collider Bias: DO NOT Adjust for Colliders!', 
                fontsize=16, fontweight='bold', y=0.98)
    save_figure('collider_bias_berkson.png')


def generate_backdoor_paths():
    """Illustrate backdoor paths and d-separation"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # Example 1: Simple backdoor path
    ax = axes[0, 0]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    draw_node(ax, 1, 2, 'X', 'lightblue', 0.2)
    draw_node(ax, 2.5, 3, 'Z', 'lightcoral', 0.2)
    draw_node(ax, 4, 2, 'Y', 'lightblue', 0.2)
    
    draw_arrow(ax, 1.2, 2, 3.8, 2)  # X -> Y (direct)
    draw_arrow(ax, 2.35, 2.85, 1.15, 2.15)  # Z -> X
    draw_arrow(ax, 2.65, 2.85, 3.85, 2.15)  # Z -> Y
    
    # Highlight backdoor path
    ax.text(2.5, 3.5, 'BACKDOOR PATH', ha='center', fontsize=11, 
           color='red', fontweight='bold', bbox=dict(boxstyle='round', 
           facecolor='yellow', alpha=0.5))
    ax.text(1.2, 1.5, 'X ← Z → Y', ha='center', fontsize=10, 
           style='italic', color='red')
    
    ax.text(2.5, 0.5, 'Must adjust for Z to block backdoor path', 
           ha='center', fontsize=11, fontweight='bold')
    
    ax.set_title('Simple Backdoor Path', fontsize=13, fontweight='bold')
    
    # Example 2: Multiple backdoor paths
    ax = axes[0, 1]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    draw_node(ax, 1, 2.5, 'X', 'lightblue', 0.2)
    draw_node(ax, 4, 2.5, 'Y', 'lightblue', 0.2)
    draw_node(ax, 2.5, 4, 'Z1', 'lightcoral', 0.2)
    draw_node(ax, 2.5, 1, 'Z2', 'lightcoral', 0.2)
    
    draw_arrow(ax, 1.2, 2.5, 3.8, 2.5)  # X -> Y (direct)
    
    # Backdoor path 1
    draw_arrow(ax, 2.35, 3.85, 1.15, 2.65)  # Z1 -> X
    draw_arrow(ax, 2.65, 3.85, 3.85, 2.65)  # Z1 -> Y
    
    # Backdoor path 2
    draw_arrow(ax, 2.35, 1.15, 1.15, 2.35)  # Z2 -> X
    draw_arrow(ax, 2.65, 1.15, 3.85, 2.35)  # Z2 -> Y
    
    ax.text(2.5, 4.5, 'Path 1: X ← Z1 → Y', ha='center', fontsize=9, 
           color='red', style='italic')
    ax.text(2.5, 0.5, 'Path 2: X ← Z2 → Y', ha='center', fontsize=9, 
           color='red', style='italic')
    
    ax.text(2.5, 5.2, 'Must adjust for BOTH Z1 and Z2', 
           ha='center', fontsize=11, fontweight='bold', 
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    ax.set_title('Multiple Backdoor Paths', fontsize=13, fontweight='bold')
    
    # Example 3: Backdoor path with collider (blocked)
    ax = axes[1, 0]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    draw_node(ax, 1, 3.5, 'X', 'lightblue', 0.2)
    draw_node(ax, 1, 1.5, 'Z1', 'lightcoral', 0.2)
    draw_node(ax, 2.5, 2.5, 'C', 'lightyellow', 0.2)  # Collider
    draw_node(ax, 4, 1.5, 'Z2', 'lightcoral', 0.2)
    draw_node(ax, 4, 3.5, 'Y', 'lightblue', 0.2)
    
    draw_arrow(ax, 1.15, 3.35, 3.85, 3.65)  # X -> Y (direct)
    
    # Backdoor path through collider
    draw_arrow(ax, 1, 3.3, 1, 1.7)  # X -> Z1
    draw_arrow(ax, 1.15, 1.5, 2.35, 2.35)  # Z1 -> C
    draw_arrow(ax, 3.85, 1.5, 2.65, 2.35)  # Z2 -> C
    draw_arrow(ax, 4, 1.7, 4, 3.3)  # Z2 -> Y
    
    # Mark collider with X
    ax.text(2.5, 2.5, '✗', ha='center', va='center', fontsize=16, 
           color='green', fontweight='bold', zorder=5)
    
    ax.text(2.5, 0.8, 'X → Z1 → C ← Z2 → Y', ha='center', fontsize=10, 
           style='italic', color='green')
    ax.text(2.5, 0.4, '✅ Path BLOCKED by collider C', 
           ha='center', fontsize=11, color='green', fontweight='bold')
    ax.text(2.5, 0.1, 'DO NOT adjust for C!', 
           ha='center', fontsize=10, style='italic', color='green')
    
    ax.set_title('Backdoor Path with Collider (Naturally Blocked)', 
                fontsize=13, fontweight='bold')
    
    # Example 4: M-bias structure
    ax = axes[1, 1]
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    draw_node(ax, 1, 3, 'X', 'lightblue', 0.2)
    draw_node(ax, 4, 3, 'Y', 'lightblue', 0.2)
    draw_node(ax, 0.5, 1.5, 'U1', 'lightcoral', 0.2)
    draw_node(ax, 4.5, 1.5, 'U2', 'lightcoral', 0.2)
    draw_node(ax, 2.5, 1.5, 'M', 'lightyellow', 0.2)  # Collider (M-bias)
    
    draw_arrow(ax, 1.15, 3, 3.85, 3)  # X -> Y (direct)
    
    # M-bias structure
    draw_arrow(ax, 0.65, 1.65, 0.85, 2.85)  # U1 -> X
    draw_arrow(ax, 0.65, 1.5, 2.35, 1.5)  # U1 -> M
    draw_arrow(ax, 4.35, 1.5, 2.65, 1.5)  # U2 -> M
    draw_arrow(ax, 4.35, 1.65, 4.15, 2.85)  # U2 -> Y
    
    # Mark M with warning
    ax.text(2.5, 1.5, '✗', ha='center', va='center', fontsize=16, 
           color='orange', fontweight='bold', zorder=5)
    
    ax.text(2.5, 0.8, 'X ← U1 → M ← U2 → Y', ha='center', fontsize=10, 
           style='italic', color='orange')
    ax.text(2.5, 0.4, '⚠️  M-BIAS: Adjusting for M opens backdoor!', 
           ha='center', fontsize=11, color='orange', fontweight='bold')
    ax.text(2.5, 0.1, 'DO NOT adjust for M (collider)', 
           ha='center', fontsize=10, style='italic', color='red')
    
    ax.set_title('M-Bias Structure (Common Mistake)', 
                fontsize=13, fontweight='bold')
    
    fig.suptitle('Backdoor Paths and d-Separation', 
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    save_figure('backdoor_paths_examples.png')


def generate_adjustment_sets():
    """Show valid and invalid adjustment sets for a complex DAG"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # Common DAG structure for all examples
    def draw_common_dag(ax, adjusted_nodes=None):
        if adjusted_nodes is None:
            adjusted_nodes = set()
        
        # Node positions
        nodes = {
            'X': (1, 2.5, 'lightblue'),
            'Y': (5, 2.5, 'lightblue'),
            'Z1': (2, 4, 'lightcoral'),
            'Z2': (4, 4, 'lightcoral'),
            'M': (3, 2.5, 'lightgreen'),
            'C': (3, 1, 'lightyellow')
        }
        
        for name, (x, y, color) in nodes.items():
            if name in adjusted_nodes:
                color = 'lightgray'
                # Draw adjustment box
                rect = FancyBboxPatch((x-0.3, y-0.3), 0.6, 0.6, 
                                     boxstyle="round,pad=0.05",
                                     edgecolor='red', facecolor='none', 
                                     linewidth=2, linestyle='--')
                ax.add_patch(rect)
            draw_node(ax, x, y, name, color, 0.2)
        
        # Arrows
        edges = [
            ('X', 'M'), ('M', 'Y'),  # Mediator chain
            ('Z1', 'X'), ('Z1', 'M'),  # Z1 affects X and M
            ('Z2', 'M'), ('Z2', 'Y'),  # Z2 affects M and Y
            ('X', 'C'), ('Y', 'C')  # Collider C
        ]
        
        for source, target in edges:
            x1, y1, _ = nodes[source]
            x2, y2, _ = nodes[target]
            
            # Determine arrow style
            if source in adjusted_nodes or target in adjusted_nodes:
                draw_arrow(ax, x1, y1, x2, y2, color='gray', style='dashed', linewidth=1.5)
            else:
                draw_arrow(ax, x1, y1, x2, y2)
        
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 5)
        ax.axis('off')
    
    # Example 1: Valid - Adjust for Z1 and Z2
    ax = axes[0, 0]
    draw_common_dag(ax, adjusted_nodes={'Z1', 'Z2'})
    ax.text(3, 0.3, '✅ VALID: Blocks all backdoor paths', 
           ha='center', fontsize=12, color='green', fontweight='bold')
    ax.text(3, 0.05, 'Adjustment Set: {Z1, Z2}', 
           ha='center', fontsize=10, style='italic')
    ax.set_title('Valid Adjustment Set 1', fontsize=13, fontweight='bold')
    
    # Example 2: Valid - Adjust for M (blocks all backdoors, but loses indirect effect)
    ax = axes[0, 1]
    draw_common_dag(ax, adjusted_nodes={'M'})
    ax.text(3, 0.3, '✅ VALID: But measures only direct effect', 
           ha='center', fontsize=12, color='orange', fontweight='bold')
    ax.text(3, 0.05, 'Adjustment Set: {M} (blocks X→M→Y indirect path)', 
           ha='center', fontsize=10, style='italic')
    ax.set_title('Valid but Not Recommended (loses mediation)', 
                fontsize=13, fontweight='bold')
    
    # Example 3: Invalid - Adjust for C (collider)
    ax = axes[1, 0]
    draw_common_dag(ax, adjusted_nodes={'C'})
    
    # Highlight spurious path
    ax.annotate('', xy=(4.85, 2.35), xytext=(1.15, 2.35),
                arrowprops=dict(arrowstyle='<->', lw=2, color='red', linestyle='--'))
    
    ax.text(3, 0.3, '❌ INVALID: Opens spurious path through collider', 
           ha='center', fontsize=12, color='red', fontweight='bold')
    ax.text(3, 0.05, 'Adjustment Set: {C} induces collider bias!', 
           ha='center', fontsize=10, style='italic')
    ax.set_title('Invalid Adjustment (Collider Bias)', 
                fontsize=13, fontweight='bold')
    
    # Example 4: Invalid - No adjustment (backdoor paths open)
    ax = axes[1, 1]
    draw_common_dag(ax, adjusted_nodes=set())
    
    # Show multiple backdoor paths
    ax.text(1.5, 4.3, 'X←Z1→M', fontsize=9, color='red', style='italic')
    ax.text(4.5, 4.3, 'M←Z2→Y', fontsize=9, color='red', style='italic')
    
    ax.text(3, 0.3, '❌ INVALID: Backdoor paths remain open', 
           ha='center', fontsize=12, color='red', fontweight='bold')
    ax.text(3, 0.05, 'No adjustment → confounding bias', 
           ha='center', fontsize=10, style='italic')
    ax.set_title('Invalid Adjustment (No Adjustment)', 
                fontsize=13, fontweight='bold')
    
    fig.suptitle('Adjustment Sets: Valid vs Invalid', 
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    save_figure('adjustment_sets_comparison.png')


def generate_simpsons_paradox_dag():
    """Illustrate Simpson's paradox with DAG"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # Left: Aggregate data (confounded)
    ax = axes[0]
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    draw_node(ax, 1, 3.5, 'Treatment\n(X)', 'lightblue', 0.3)
    draw_node(ax, 3, 3.5, 'Recovery\n(Y)', 'lightblue', 0.3)
    draw_node(ax, 2, 1.5, 'Disease\nSeverity\n(Z)', 'lightcoral', 0.35)
    
    draw_arrow(ax, 1.3, 3.5, 2.7, 3.5)  # Treatment -> Recovery
    draw_arrow(ax, 1.8, 1.7, 1.2, 3.2)  # Severity -> Treatment
    draw_arrow(ax, 2.2, 1.7, 2.8, 3.2)  # Severity -> Recovery
    
    # Show spurious negative association
    ax.text(2, 4.2, 'Aggregate Data: Negative Association', 
           ha='center', fontsize=12, fontweight='bold', color='red')
    ax.text(2, 0.5, '❌ Treatment appears harmful', 
           ha='center', fontsize=12, color='red', fontweight='bold')
    ax.text(2, 0.2, '(Sicker patients more likely to receive treatment)', 
           ha='center', fontsize=10, style='italic')
    
    ax.set_title('SIMPSON\'S PARADOX\n(Confounded - No Adjustment)', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Right: Stratified by severity (unconfounded)
    ax = axes[1]
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    draw_node(ax, 1, 3.5, 'Treatment\n(X)', 'lightblue', 0.3)
    draw_node(ax, 3, 3.5, 'Recovery\n(Y)', 'lightblue', 0.3)
    draw_node(ax, 2, 1.5, 'Disease\nSeverity\n(Z)', 'lightgray', 0.35)
    
    # Adjusted paths (dashed)
    draw_arrow(ax, 1.8, 1.7, 1.2, 3.2, color='gray', style='dashed', linewidth=1.5)
    draw_arrow(ax, 2.2, 1.7, 2.8, 3.2, color='gray', style='dashed', linewidth=1.5)
    
    # Strong causal effect
    draw_arrow(ax, 1.3, 3.5, 2.7, 3.5, color='green', linewidth=4)
    
    # Adjusted box
    rect = FancyBboxPatch((1.3, 1.0), 1.4, 1.3, boxstyle="round,pad=0.05",
                          edgecolor='red', facecolor='none', linewidth=3, linestyle='--')
    ax.add_patch(rect)
    ax.text(2, 0.7, 'STRATIFIED', ha='center', fontsize=11, 
           color='red', fontweight='bold')
    
    ax.text(2, 4.2, 'Stratified Data: Positive Association', 
           ha='center', fontsize=12, fontweight='bold', color='green')
    ax.text(2, 0.5, '✅ Treatment is beneficial (in each stratum)', 
           ha='center', fontsize=12, color='green', fontweight='bold')
    ax.text(2, 0.2, '(Controlling for disease severity reveals true effect)', 
           ha='center', fontsize=10, style='italic')
    
    ax.set_title('PARADOX RESOLVED\n(Adjusted for Confounder)', 
                fontsize=14, fontweight='bold', pad=20)
    
    fig.suptitle('Simpson\'s Paradox: Association Reverses After Stratification', 
                fontsize=16, fontweight='bold', y=0.98)
    save_figure('simpsons_paradox_dag.png')


def generate_complete_dag_example():
    """A realistic complex DAG with multiple types of variables"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define nodes with positions and types
    nodes = {
        # Treatment and Outcome
        'Treatment': (2, 4, 'lightblue', 0.3),
        'Outcome': (6, 4, 'lightblue', 0.3),
        
        # Confounders
        'SES': (1, 6.5, 'lightcoral', 0.25),
        'Age': (3, 6.5, 'lightcoral', 0.25),
        
        # Mediator
        'Adherence': (4, 4, 'lightgreen', 0.25),
        
        # Collider
        'Measurement': (4, 1.5, 'lightyellow', 0.25),
        
        # Instrumental variable
        'Randomization': (0.5, 4, 'plum', 0.3),
        
        # Descendant of collider
        'Report': (4, 0.2, 'wheat', 0.2),
    }
    
    # Draw nodes
    for name, (x, y, color, size) in nodes.items():
        draw_node(ax, x, y, name, color, size)
    
    # Draw arrows
    edges = [
        # Confounders
        ('SES', 'Treatment'), ('SES', 'Outcome'),
        ('Age', 'Treatment'), ('Age', 'Outcome'),
        
        # Causal path (through mediator)
        ('Treatment', 'Adherence'), ('Adherence', 'Outcome'),
        
        # Direct effect
        ('Treatment', 'Outcome'),
        
        # Collider
        ('Treatment', 'Measurement'), ('Outcome', 'Measurement'),
        
        # Descendant
        ('Measurement', 'Report'),
        
        # Instrumental variable
        ('Randomization', 'Treatment'),
        
        # Additional confounding
        ('Age', 'Adherence'),
    ]
    
    for source, target in edges:
        x1, y1, _, _ = nodes[source]
        x2, y2, _, _ = nodes[target]
        
        # Color code arrows
        if source == 'Treatment' and target == 'Outcome':
            draw_arrow(ax, x1, y1, x2, y2, color='darkgreen', linewidth=3)
        elif source in ['SES', 'Age']:
            draw_arrow(ax, x1, y1, x2, y2, color='red', linewidth=2)
        elif source == 'Randomization':
            draw_arrow(ax, x1, y1, x2, y2, color='purple', linewidth=2)
        else:
            draw_arrow(ax, x1, y1, x2, y2)
    
    # Add legends
    legend_x, legend_y = 7, 7.5
    legend_items = [
        ('Treatment/Outcome', 'lightblue'),
        ('Confounder', 'lightcoral'),
        ('Mediator', 'lightgreen'),
        ('Collider', 'lightyellow'),
        ('Instrument', 'plum'),
    ]
    
    for i, (label, color) in enumerate(legend_items):
        y_pos = legend_y - i * 0.4
        circle = Circle((legend_x - 0.3, y_pos), 0.15, color=color, 
                       ec='black', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(legend_x + 0.1, y_pos, label, va='center', fontsize=10)
    
    # Add annotations
    annotations = [
        (1, 7.5, 'Confounders\n(adjust for)', 'red'),
        (4, 5, 'Mediator\n(do not adjust\nfor total effect)', 'green'),
        (4, 2.5, 'Collider\n(do not adjust!)', 'orange'),
        (0.5, 5, 'Instrument\n(RCT)', 'purple'),
    ]
    
    for x, y, text, color in annotations:
        ax.text(x, y, text, ha='center', fontsize=9, style='italic',
               color=color, bbox=dict(boxstyle='round', facecolor='white', 
               alpha=0.8, edgecolor=color))
    
    ax.text(4, 7.8, 'Complete DAG: Treatment Effect on Outcome', 
           ha='center', fontsize=16, fontweight='bold')
    
    ax.text(4, -0.5, 'Valid adjustment set: {SES, Age}\n' + 
           'Blocks backdoor paths without inducing collider bias',
           ha='center', fontsize=11, style='italic',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    
    plt.tight_layout()
    save_figure('complete_dag_example.png')


def generate_all_diagrams():
    """Generate all causal inference diagrams"""
    print("\n" + "="*80)
    print("  GENERATING CAUSAL INFERENCE DIAGRAMS FOR CHAPTER 05")
    print("="*80 + "\n")
    
    diagrams = [
        ("Basic causal structures", generate_basic_structures),
        ("Confounder with adjustment", generate_confounder_diagram),
        ("Mediator analysis", generate_mediator_diagram),
        ("Collider bias (Berkson's paradox)", generate_collider_bias),
        ("Backdoor paths examples", generate_backdoor_paths),
        ("Adjustment sets comparison", generate_adjustment_sets),
        ("Simpson's paradox DAG", generate_simpsons_paradox_dag),
        ("Complete DAG example", generate_complete_dag_example),
    ]
    
    for i, (name, func) in enumerate(diagrams, 1):
        print(f"[{i}/{len(diagrams)}] Generating {name}...")
        func()
    
    print("\n" + "="*80)
    print("  ✅ ALL 8 CAUSAL INFERENCE DIAGRAMS GENERATED SUCCESSFULLY!")
    print("="*80)
    print("\nImages saved to current directory.")
    print("\nSummary:")
    print("  • causal_basic_structures.png")
    print("  • confounder_adjustment.png")
    print("  • mediator_analysis.png")
    print("  • collider_bias_berkson.png")
    print("  • backdoor_paths_examples.png")
    print("  • adjustment_sets_comparison.png")
    print("  • simpsons_paradox_dag.png")
    print("  • complete_dag_example.png")


if __name__ == '__main__':
    generate_all_diagrams()
