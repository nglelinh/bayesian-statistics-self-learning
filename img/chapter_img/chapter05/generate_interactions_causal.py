#!/usr/bin/env python3
"""
Script để tạo các hình ảnh minh họa nâng cao cho Chapter 05: Multiple Regression & Causal Inference

Các visualizations mới:
1. 3-Way Interactions
2. Continuous-Categorical Interactions
3. Interaction Effects Visualization
4. Causal Inference DAGs (Colliders, Mediators, Confounders)
5. Backdoor Paths and d-separation

Sử dụng:
    python3 generate_interactions_causal.py

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

def generate_three_way_interaction():
    """Hình 1: 3-Way Interaction Visualization"""
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    np.random.seed(42)
    n = 200
    
    # Generate data with 3-way interaction
    # Y = β0 + β1*X1 + β2*X2 + β3*X3 + β12*X1*X2 + β13*X1*X3 + β23*X2*X3 + β123*X1*X2*X3
    x1 = np.random.uniform(0, 10, n)  # Continuous
    x2 = np.random.choice([0, 1], n)  # Binary (e.g., Treatment)
    x3 = np.random.choice([0, 1], n)  # Binary (e.g., Gender)
    
    # True model with 3-way interaction
    y = (50 + 2*x1 + 10*x2 + 5*x3 + 
         1.5*x1*x2 +  # X1-X2 interaction
         0.8*x1*x3 +  # X1-X3 interaction
         8*x2*x3 +    # X2-X3 interaction
         0.5*x1*x2*x3 +  # 3-way interaction
         np.random.normal(0, 5, n))
    
    # Panel 1: X2=0, split by X3
    ax1 = fig.add_subplot(gs[0, 0])
    
    mask_x2_0_x3_0 = (x2 == 0) & (x3 == 0)
    mask_x2_0_x3_1 = (x2 == 0) & (x3 == 1)
    
    ax1.scatter(x1[mask_x2_0_x3_0], y[mask_x2_0_x3_0], 
               alpha=0.6, s=50, color='blue', label='X2=0, X3=0')
    ax1.scatter(x1[mask_x2_0_x3_1], y[mask_x2_0_x3_1], 
               alpha=0.6, s=50, color='lightblue', label='X2=0, X3=1')
    
    # Fit lines
    x_range = np.linspace(0, 10, 100)
    y_pred_0_0 = 50 + 2*x_range
    y_pred_0_1 = 50 + 2*x_range + 5 + 0.8*x_range
    
    ax1.plot(x_range, y_pred_0_0, 'b-', linewidth=3, alpha=0.8)
    ax1.plot(x_range, y_pred_0_1, 'lightblue', linewidth=3, linestyle='--', alpha=0.8)
    
    ax1.set_title('X2=0 (Control Group)\nEffect of X1 depends on X3', 
                  fontsize=12, fontweight='bold')
    ax1.set_xlabel('X1 (Continuous)', fontsize=11)
    ax1.set_ylabel('Y (Outcome)', fontsize=11)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: X2=1, split by X3
    ax2 = fig.add_subplot(gs[0, 1])
    
    mask_x2_1_x3_0 = (x2 == 1) & (x3 == 0)
    mask_x2_1_x3_1 = (x2 == 1) & (x3 == 1)
    
    ax2.scatter(x1[mask_x2_1_x3_0], y[mask_x2_1_x3_0], 
               alpha=0.6, s=50, color='red', label='X2=1, X3=0')
    ax2.scatter(x1[mask_x2_1_x3_1], y[mask_x2_1_x3_1], 
               alpha=0.6, s=50, color='orange', label='X2=1, X3=1')
    
    # Fit lines with interaction
    y_pred_1_0 = 50 + 2*x_range + 10 + 1.5*x_range
    y_pred_1_1 = 50 + 2*x_range + 10 + 5 + 1.5*x_range + 0.8*x_range + 8 + 0.5*x_range
    
    ax2.plot(x_range, y_pred_1_0, 'r-', linewidth=3, alpha=0.8)
    ax2.plot(x_range, y_pred_1_1, 'orange', linewidth=3, linestyle='--', alpha=0.8)
    
    ax2.set_title('X2=1 (Treatment Group)\nEffect AMPLIFIED when X3=1!', 
                  fontsize=12, fontweight='bold')
    ax2.set_xlabel('X1 (Continuous)', fontsize=11)
    ax2.set_ylabel('Y (Outcome)', fontsize=11)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Comparison table
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.axis('off')
    
    comparison_text = """
╔═══════════════════════════════════╗
║   3-WAY INTERACTION EFFECTS       ║
╠═══════════════════════════════════╣
║                                   ║
║  SLOPES (Effect of X1 on Y):      ║
║                                   ║
║  X2=0, X3=0:  2.0  (baseline)     ║
║  X2=0, X3=1:  2.8  (↑ 0.8)        ║
║                                   ║
║  X2=1, X3=0:  3.5  (↑ 1.5)        ║
║  X2=1, X3=1:  4.8  (↑ 2.8!)       ║
║                                   ║
║  KEY INSIGHT:                     ║
║    Effect of X1 depends on        ║
║    BOTH X2 AND X3!                ║
║                                   ║
║    When X2=1 AND X3=1:            ║
║    → Synergistic effect           ║
║    → Slope is HIGHEST (4.8)       ║
║                                   ║
║  INTERPRETATION:                  ║
║    Treatment (X2=1) works         ║
║    best for X3=1 group            ║
║    at high levels of X1           ║
║                                   ║
╚═══════════════════════════════════╝
"""
    ax3.text(0.5, 0.5, comparison_text, fontsize=9, family='monospace',
             ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Panel 4: Marginal effect of X2 (Treatment)
    ax4 = fig.add_subplot(gs[1, 0])
    
    x1_levels = [2, 5, 8]
    x3_levels = [0, 1]
    colors_x3 = ['blue', 'red']
    
    for x3_val, color in zip(x3_levels, colors_x3):
        effects = []
        for x1_val in x1_levels:
            # Effect of X2: Y(X2=1) - Y(X2=0)
            y_x2_0 = 50 + 2*x1_val + 5*x3_val + 0.8*x1_val*x3_val
            y_x2_1 = (50 + 2*x1_val + 10 + 5*x3_val + 
                     1.5*x1_val + 0.8*x1_val*x3_val + 8*x3_val + 0.5*x1_val*x3_val)
            effects.append(y_x2_1 - y_x2_0)
        
        ax4.plot(x1_levels, effects, 'o-', linewidth=3, markersize=12,
                color=color, label=f'X3={x3_val}', alpha=0.8)
    
    ax4.set_title('Marginal Effect of X2 (Treatment)\nDepends on X1 AND X3', 
                  fontsize=12, fontweight='bold')
    ax4.set_xlabel('X1 Level', fontsize=11)
    ax4.set_ylabel('Treatment Effect (X2=1 - X2=0)', fontsize=11)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    ax4.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    
    # Panel 5: Heatmap of predicted Y
    ax5 = fig.add_subplot(gs[1, 1])
    
    x1_grid = np.linspace(0, 10, 50)
    x2_vals = [0, 1]
    x3_vals = [0, 1]
    
    # Create 2x2 grid showing all combinations
    fig_inset, axes_inset = plt.subplots(2, 2, figsize=(6, 6))
    
    for i, x2_val in enumerate(x2_vals):
        for j, x3_val in enumerate(x3_vals):
            y_pred = (50 + 2*x1_grid + 10*x2_val + 5*x3_val + 
                     1.5*x1_grid*x2_val + 0.8*x1_grid*x3_val + 
                     8*x2_val*x3_val + 0.5*x1_grid*x2_val*x3_val)
            
            axes_inset[i, j].plot(x1_grid, y_pred, linewidth=3, 
                                 color=plt.cm.RdYlBu_r(i*0.5 + j*0.25))
            axes_inset[i, j].set_title(f'X2={x2_val}, X3={x3_val}', 
                                      fontsize=9, fontweight='bold')
            axes_inset[i, j].set_xlabel('X1', fontsize=8)
            axes_inset[i, j].set_ylabel('Y', fontsize=8)
            axes_inset[i, j].grid(True, alpha=0.3)
            axes_inset[i, j].set_ylim([40, 120])
    
    plt.close(fig_inset)
    
    # Show combined effect
    for x2_val in [0, 1]:
        for x3_val in [0, 1]:
            y_pred = (50 + 2*x1_grid + 10*x2_val + 5*x3_val + 
                     1.5*x1_grid*x2_val + 0.8*x1_grid*x3_val + 
                     8*x2_val*x3_val + 0.5*x1_grid*x2_val*x3_val)
            
            linestyle = '-' if x2_val == 0 else '--'
            color = 'blue' if x3_val == 0 else 'red'
            alpha = 0.4 if x2_val == 0 else 0.8
            
            ax5.plot(x1_grid, y_pred, linestyle=linestyle, linewidth=2.5,
                    color=color, alpha=alpha, 
                    label=f'X2={x2_val}, X3={x3_val}')
    
    ax5.set_title('All Combinations Overlay', fontsize=12, fontweight='bold')
    ax5.set_xlabel('X1', fontsize=11)
    ax5.set_ylabel('Y (Predicted)', fontsize=11)
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # Panel 6: Summary
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    
    summary_text = """
╔═══════════════════════════════════╗
║    WHEN TO USE 3-WAY INTERACT?    ║
╠═══════════════════════════════════╣
║                                   ║
║  DEFINITION:                      ║
║    Y = β0 + β1X1 + β2X2 + β3X3    ║
║        + β12X1X2 + β13X1X3        ║
║        + β23X2X3                  ║
║        + β123X1X2X3               ║
║                                   ║
║  INTERPRETATION:                  ║
║    Effect of X1 depends on        ║
║    combination of X2 AND X3       ║
║                                   ║
║  EXAMPLES:                        ║
║    • Drug effect by dose,         ║
║      age, and gender              ║
║    • Education returns by         ║
║      experience and industry      ║
║    • Marketing: price × ad ×      ║
║      customer segment             ║
║                                   ║
║  CAUTION:                         ║
║    ⚠ Hard to interpret            ║
║    ⚠ Need large sample size       ║
║    ⚠ Theory should guide          ║
║    ⚠ Visualize carefully          ║
║                                   ║
║  ALTERNATIVES:                    ║
║    → Stratified analysis          ║
║    → Subgroup-specific models     ║
║                                   ║
╚═══════════════════════════════════╝
"""
    ax6.text(0.5, 0.5, summary_text, fontsize=8.5, family='monospace',
             ha='center', va='center',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))
    
    plt.suptitle('3-Way Interaction: X1 × X2 × X3\n' + 
                 'Effect of one variable depends on TWO others simultaneously', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    save_figure('three_way_interaction.png')

def generate_continuous_categorical_interaction():
    """Hình 2: Continuous-Categorical Interaction"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    
    np.random.seed(42)
    n_per_group = 100
    
    # Three categories: A, B, C
    categories = ['A', 'B', 'C']
    colors = ['blue', 'green', 'red']
    
    # Generate data
    x_continuous = []
    y_outcome = []
    category_list = []
    
    # Different slopes for each category
    slopes = [1.0, 2.5, 0.2]  # A: weak, B: strong, C: almost flat
    intercepts = [20, 15, 30]
    
    for i, (cat, slope, intercept) in enumerate(zip(categories, slopes, intercepts)):
        x = np.random.uniform(0, 10, n_per_group)
        y = intercept + slope * x + np.random.normal(0, 3, n_per_group)
        
        x_continuous.extend(x)
        y_outcome.extend(y)
        category_list.extend([cat] * n_per_group)
    
    x_continuous = np.array(x_continuous)
    y_outcome = np.array(y_outcome)
    category_array = np.array(category_list)
    
    # Panel 1: Scatter plot with regression lines
    for i, (cat, color, slope, intercept) in enumerate(zip(categories, colors, slopes, intercepts)):
        mask = category_array == cat
        axes[0, 0].scatter(x_continuous[mask], y_outcome[mask], 
                          alpha=0.5, s=40, color=color, label=f'Category {cat}')
        
        x_range = np.linspace(0, 10, 100)
        y_pred = intercept + slope * x_range
        axes[0, 0].plot(x_range, y_pred, color=color, linewidth=3, alpha=0.8)
    
    axes[0, 0].set_title('Continuous-Categorical Interaction\nDifferent slopes for each category', 
                         fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('X (Continuous predictor)', fontsize=11)
    axes[0, 0].set_ylabel('Y (Outcome)', fontsize=11)
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Panel 2: Marginal effects
    x_levels = np.array([2, 5, 8])
    
    for i, (cat, color, slope, intercept) in enumerate(zip(categories, colors, slopes, intercepts)):
        effects = []
        for x_level in x_levels:
            # Marginal effect at this x level
            dy_dx = slope
            effects.append(dy_dx)
        
        axes[0, 1].plot(x_levels, effects, 'o-', linewidth=3, markersize=12,
                       color=color, label=f'Category {cat}: slope={slope}', alpha=0.8)
    
    axes[0, 1].set_title('Marginal Effects (Slopes)\nConstant within category, differ across', 
                         fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('X Level', fontsize=11)
    axes[0, 1].set_ylabel('∂Y/∂X (Slope)', fontsize=11)
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    
    # Panel 3: Model comparison
    axes[0, 2].axis('off')
    
    model_text = """
╔═══════════════════════════════════╗
║   MODEL SPECIFICATION             ║
╠═══════════════════════════════════╣
║                                   ║
║  NO INTERACTION:                  ║
║    Y = β0 + β1·X + β2·I(Cat=B)    ║
║           + β3·I(Cat=C)           ║
║                                   ║
║    → Parallel lines               ║
║    → Same slope for all           ║
║    → Only intercepts differ       ║
║                                   ║
║  WITH INTERACTION:                ║
║    Y = β0 + β1·X + β2·I(Cat=B)    ║
║           + β3·I(Cat=C)           ║
║           + β4·X·I(Cat=B)         ║
║           + β5·X·I(Cat=C)         ║
║                                   ║
║    → Non-parallel lines           ║
║    → Different slopes!            ║
║    → Both slopes & intercepts     ║
║       differ                      ║
║                                   ║
║  COEFFICIENTS:                    ║
║    β1: Slope for Category A       ║
║    β4: CHANGE in slope for B      ║
║    β5: CHANGE in slope for C      ║
║                                   ║
╚═══════════════════════════════════╝
"""
    axes[0, 2].text(0.5, 0.5, model_text, fontsize=9, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
    
    # Panel 4: Prediction at different X levels
    x_test_levels = [1, 5, 9]
    
    x_pos = np.arange(len(x_test_levels))
    width = 0.25
    
    for i, (cat, color, slope, intercept) in enumerate(zip(categories, colors, slopes, intercepts)):
        predictions = [intercept + slope * x for x in x_test_levels]
        axes[1, 0].bar(x_pos + i*width, predictions, width, 
                      label=f'Category {cat}', color=color, alpha=0.7, edgecolor='black')
    
    axes[1, 0].set_title('Predicted Y at Different X Levels', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('X Level', fontsize=11)
    axes[1, 0].set_ylabel('Predicted Y', fontsize=11)
    axes[1, 0].set_xticks(x_pos + width)
    axes[1, 0].set_xticklabels([f'X={x}' for x in x_test_levels])
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Panel 5: Effect size comparison
    # Compute effect of going from X=2 to X=8
    delta_x = 6
    
    effect_sizes = [slope * delta_x for slope in slopes]
    
    bars = axes[1, 1].bar(categories, effect_sizes, color=colors, 
                         alpha=0.7, edgecolor='black', linewidth=2)
    axes[1, 1].set_title(f'Effect Size: Y(X=8) - Y(X=2)\nCategory B has STRONGEST effect', 
                         fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Category', fontsize=11)
    axes[1, 1].set_ylabel('Effect Size (ΔY)', fontsize=11)
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    # Highlight largest
    max_idx = np.argmax(effect_sizes)
    bars[max_idx].set_edgecolor('red')
    bars[max_idx].set_linewidth(4)
    
    for i, effect in enumerate(effect_sizes):
        axes[1, 1].text(i, effect + max(effect_sizes)*0.02, 
                       f'{effect:.1f}', ha='center', fontsize=11, fontweight='bold')
    
    # Panel 6: Real-world examples
    axes[1, 2].axis('off')
    
    examples_text = """
╔═══════════════════════════════════╗
║   REAL-WORLD EXAMPLES             ║
╠═══════════════════════════════════╣
║                                   ║
║  1. INCOME vs EDUCATION           ║
║     by INDUSTRY                   ║
║     • Tech: Steep slope           ║
║     • Retail: Flat slope          ║
║     • Finance: Medium slope       ║
║                                   ║
║  2. DRUG DOSE vs RESPONSE         ║
║     by GENOTYPE                   ║
║     • Type A: Strong response     ║
║     • Type B: Weak response       ║
║     • Type C: No response         ║
║                                   ║
║  3. PRICE vs SALES                ║
║     by CUSTOMER SEGMENT           ║
║     • Premium: Less sensitive     ║
║     • Budget: Very sensitive      ║
║     • Mid: Moderate               ║
║                                   ║
║  KEY INSIGHT:                     ║
║    The relationship between       ║
║    continuous X and Y is NOT      ║
║    the same across categories!    ║
║                                   ║
║    → Need interaction term        ║
║    → Separate analysis per group  ║
║                                   ║
╚═══════════════════════════════════╝
"""
    axes[1, 2].text(0.5, 0.5, examples_text, fontsize=8.5, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    plt.suptitle('Continuous-Categorical Interaction\n' + 
                 'Relationship between X and Y differs by category', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    save_figure('continuous_categorical_interaction_advanced.png')

def draw_dag_node(ax, x, y, label, color='lightblue', size=0.15):
    """Helper function to draw a DAG node"""
    circle = plt.Circle((x, y), size, color=color, ec='black', linewidth=2, zorder=3)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold', zorder=4)

def draw_dag_arrow(ax, x1, y1, x2, y2, color='black', style='-', width=2):
    """Helper function to draw a DAG arrow"""
    dx = x2 - x1
    dy = y2 - y1
    ax.arrow(x1, y1, dx*0.8, dy*0.8, head_width=0.08, head_length=0.08,
            fc=color, ec=color, linestyle=style, linewidth=width, zorder=2)

def generate_causal_dags():
    """Hình 3: Causal Inference DAGs"""
    fig, axes = plt.subplots(3, 3, figsize=(18, 16))
    
    # Configure all axes
    for ax in axes.flat:
        ax.set_xlim([0, 2])
        ax.set_ylim([0, 1.5])
        ax.axis('off')
        ax.set_aspect('equal')
    
    # Panel 1: Confounder
    ax = axes[0, 0]
    draw_dag_node(ax, 1, 1.2, 'Z', 'yellow')
    draw_dag_node(ax, 0.5, 0.3, 'X', 'lightblue')
    draw_dag_node(ax, 1.5, 0.3, 'Y', 'lightgreen')
    
    draw_dag_arrow(ax, 1, 1.05, 0.65, 0.45, 'red', '-', 3)
    draw_dag_arrow(ax, 1, 1.05, 1.35, 0.45, 'red', '-', 3)
    draw_dag_arrow(ax, 0.65, 0.3, 1.35, 0.3, 'blue', '-', 3)
    
    ax.set_title('CONFOUNDER\n"Common Cause"', fontsize=13, fontweight='bold')
    ax.text(1, 0.05, 'Z affects BOTH X and Y\n→ Creates spurious correlation\n→ MUST control for Z', 
           ha='center', fontsize=10, 
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Panel 2: Mediator
    ax = axes[0, 1]
    draw_dag_node(ax, 0.5, 0.75, 'X', 'lightblue')
    draw_dag_node(ax, 1, 0.75, 'M', 'orange')
    draw_dag_node(ax, 1.5, 0.75, 'Y', 'lightgreen')
    
    draw_dag_arrow(ax, 0.65, 0.75, 0.85, 0.75, 'blue', '-', 3)
    draw_dag_arrow(ax, 1.15, 0.75, 1.35, 0.75, 'blue', '-', 3)
    
    ax.set_title('MEDIATOR\n"Causal Chain"', fontsize=13, fontweight='bold')
    ax.text(1, 0.2, 'X → M → Y\nM transmits effect of X to Y\n→ SHOULD NOT control for M\n(unless studying direct effect)', 
           ha='center', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Panel 3: Collider
    ax = axes[0, 2]
    draw_dag_node(ax, 0.5, 1.2, 'X', 'lightblue')
    draw_dag_node(ax, 1.5, 1.2, 'Y', 'lightgreen')
    draw_dag_node(ax, 1, 0.3, 'C', 'lightcoral')
    
    draw_dag_arrow(ax, 0.65, 1.05, 0.85, 0.45, 'blue', '-', 3)
    draw_dag_arrow(ax, 1.35, 1.05, 1.15, 0.45, 'blue', '-', 3)
    
    ax.set_title('COLLIDER\n"Common Effect"', fontsize=13, fontweight='bold')
    ax.text(1, 0.05, 'X → C ← Y\nC is caused by X AND Y\n→ MUST NOT control for C\n(creates spurious association!)', 
           ha='center', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    # Panel 4: Confounding example
    axes[1, 0].axis('off')
    confound_text = """
╔═════════════════════════════════════╗
║      CONFOUNDER EXAMPLE             ║
╠═════════════════════════════════════╣
║                                     ║
║  SCENARIO:                          ║
║    Does coffee (X) cause            ║
║    heart disease (Y)?               ║
║                                     ║
║  DAG:                               ║
║         Smoking (Z)                 ║
║          /        \\                 ║
║    Coffee (X)   Heart Disease (Y)  ║
║                                     ║
║  PROBLEM:                           ║
║    Smokers drink more coffee        ║
║    Smoking causes heart disease     ║
║    → Coffee-heart correlation       ║
║       is SPURIOUS!                  ║
║                                     ║
║  SOLUTION:                          ║
║    Control for Smoking (Z)          ║
║    Then estimate X → Y              ║
║                                     ║
║  MODEL:                             ║
║    Y ~ X + Z  (include Z)           ║
║                                     ║
╚═════════════════════════════════════╝
"""
    axes[1, 0].text(0.5, 0.5, confound_text, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Panel 5: Mediator example
    axes[1, 1].axis('off')
    mediator_text = """
╔═════════════════════════════════════╗
║       MEDIATOR EXAMPLE              ║
╠═════════════════════════════════════╣
║                                     ║
║  SCENARIO:                          ║
║    Does education (X) increase      ║
║    income (Y)?                      ║
║                                     ║
║  DAG:                               ║
║    Education → Skills → Income      ║
║        (X)       (M)      (Y)       ║
║                                     ║
║  MECHANISM:                         ║
║    Education builds Skills          ║
║    Skills increase Income           ║
║    → Skills MEDIATE the effect      ║
║                                     ║
║  TOTAL EFFECT:                      ║
║    Y ~ X  (don't control M)         ║
║    Captures full pathway            ║
║                                     ║
║  DIRECT EFFECT:                     ║
║    Y ~ X + M  (control M)           ║
║    Effect NOT through Skills        ║
║    (e.g., signaling)                ║
║                                     ║
╚═════════════════════════════════════╝
"""
    axes[1, 1].text(0.5, 0.5, mediator_text, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Panel 6: Collider example
    axes[1, 2].axis('off')
    collider_text = """
╔═════════════════════════════════════╗
║       COLLIDER EXAMPLE              ║
╠═════════════════════════════════════╣
║                                     ║
║  SCENARIO:                          ║
║    Beauty (X) and Talent (Y)        ║
║    both lead to Fame (C)            ║
║                                     ║
║  DAG:                               ║
║    Beauty → Fame ← Talent           ║
║      (X)     (C)     (Y)            ║
║                                     ║
║  COLLIDER BIAS:                     ║
║    Among famous people:             ║
║    Beauty and Talent appear         ║
║    NEGATIVELY correlated!           ║
║                                     ║
║  WHY?                               ║
║    If you're famous but not         ║
║    beautiful, you must be           ║
║    very talented!                   ║
║                                     ║
║  DANGER:                            ║
║    Controlling for Fame (C)         ║
║    creates FALSE negative           ║
║    correlation between X and Y      ║
║                                     ║
║  ⚠ NEVER control for collider!      ║
║                                     ║
╚═════════════════════════════════════╝
"""
    axes[1, 2].text(0.5, 0.5, collider_text, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.9))
    
    # Panel 7: Complex DAG - Backdoor path
    ax = axes[2, 0]
    
    # Multiple paths from X to Y
    draw_dag_node(ax, 0.3, 0.75, 'X', 'lightblue')
    draw_dag_node(ax, 1.7, 0.75, 'Y', 'lightgreen')
    draw_dag_node(ax, 0.6, 1.3, 'A', 'yellow')
    draw_dag_node(ax, 1.4, 1.3, 'B', 'yellow')
    draw_dag_node(ax, 1, 0.3, 'M', 'orange')
    
    # Direct path X → Y
    draw_dag_arrow(ax, 0.45, 0.75, 1.55, 0.75, 'blue', '-', 3)
    
    # Backdoor path: X ← A → B → Y
    draw_dag_arrow(ax, 0.5, 1.15, 0.4, 0.9, 'red', '--', 2)
    draw_dag_arrow(ax, 0.75, 1.3, 1.25, 1.3, 'red', '--', 2)
    draw_dag_arrow(ax, 1.5, 1.15, 1.6, 0.9, 'red', '--', 2)
    
    # Mediator path: X → M → Y
    draw_dag_arrow(ax, 0.5, 0.6, 0.85, 0.4, 'green', ':', 2)
    draw_dag_arrow(ax, 1.15, 0.4, 1.5, 0.6, 'green', ':', 2)
    
    ax.set_title('BACKDOOR PATH\nMultiple Paths from X to Y', fontsize=13, fontweight='bold')
    ax.text(1, 0.05, 'Blue: Direct path (causal)\nRed: Backdoor (confounding)\nGreen: Mediator\n→ Close backdoor by controlling A or B', 
           ha='center', fontsize=9,
           bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))
    
    # Panel 8: d-separation
    axes[2, 1].axis('off')
    dsep_text = """
╔═════════════════════════════════════╗
║        d-SEPARATION RULES           ║
╠═════════════════════════════════════╣
║                                     ║
║  RULE 1: CHAIN (Mediator)           ║
║    X → M → Y                        ║
║    • NOT d-separated: X⊥Y? NO       ║
║    • Control M: X⊥Y|M? YES          ║
║                                     ║
║  RULE 2: FORK (Confounder)          ║
║    X ← Z → Y                        ║
║    • NOT d-separated: X⊥Y? NO       ║
║    • Control Z: X⊥Y|Z? YES          ║
║                                     ║
║  RULE 3: COLLIDER                   ║
║    X → C ← Y                        ║
║    • d-separated: X⊥Y? YES!         ║
║    • Control C: X⊥Y|C? NO!          ║
║                                     ║
║  KEY INSIGHT:                       ║
║    To identify causal effect X→Y:   ║
║    1. Find all paths X to Y         ║
║    2. Block backdoor paths          ║
║    3. Don't block causal paths      ║
║    4. Don't open colliders          ║
║                                     ║
╚═════════════════════════════════════╝
"""
    axes[2, 1].text(0.5, 0.5, dsep_text, fontsize=9, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
    
    # Panel 9: Summary table
    axes[2, 2].axis('off')
    summary_table = """
╔═════════════════════════════════════╗
║    WHEN TO CONTROL VARIABLES?       ║
╠═════════════════════════════════════╣
║                                     ║
║  TYPE          CONTROL?   WHY?      ║
║  ───────────────────────────────    ║
║                                     ║
║  Confounder      YES     Block      ║
║  (Z→X, Z→Y)              spurious   ║
║                          association║
║                                     ║
║  Mediator        NO      Don't      ║
║  (X→M→Y)                 block      ║
║                          causal     ║
║                          pathway    ║
║                                     ║
║  Collider        NO!     Don't open ║
║  (X→C←Y)                 new path   ║
║                                     ║
║  Descendant      MAYBE   Depends on ║
║  of collider             DAG        ║
║                                     ║
║  Instrumental    NO      Keep for   ║
║  Variable                 IV method ║
║                                     ║
║  ───────────────────────────────    ║
║                                     ║
║  GOLDEN RULE:                       ║
║    Draw the DAG first!              ║
║    Then decide what to control      ║
║                                     ║
╚═════════════════════════════════════╝
"""
    axes[2, 2].text(0.5, 0.5, summary_table, fontsize=8.5, family='monospace',
                   ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    plt.suptitle('Causal Inference with DAGs: Confounders, Mediators, Colliders\n' + 
                 'Understanding causal structure is KEY to valid inference', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    save_figure('causal_inference_dags.png')

def main():
    """Hàm chính để tạo tất cả các hình ảnh"""
    print('='*70)
    print('BẮT ĐẦU TẠO HÌNH ẢNH INTERACTIONS & CAUSAL INFERENCE CHO CHAPTER 05')
    print('='*70)
    print()
    
    print('Phần 1/3: 3-Way Interaction')
    generate_three_way_interaction()
    print('✓ Hoàn thành phần 1/3\n')
    
    print('Phần 2/3: Continuous-Categorical Interaction')
    generate_continuous_categorical_interaction()
    print('✓ Hoàn thành phần 2/3\n')
    
    print('Phần 3/3: Causal Inference DAGs')
    generate_causal_dags()
    print('✓ Hoàn thành phần 3/3\n')
    
    print('='*70)
    print('TẤT CẢ HÌNH ẢNH ĐÃ ĐƯỢC TẠO THÀNH CÔNG!')
    print('='*70)
    print()
    print('Danh sách các file đã tạo:')
    print('1. three_way_interaction.png')
    print('2. continuous_categorical_interaction_advanced.png')
    print('3. causal_inference_dags.png')
    print()
    print(f'Thư mục output: {OUTPUT_DIR}')

if __name__ == '__main__':
    main()
