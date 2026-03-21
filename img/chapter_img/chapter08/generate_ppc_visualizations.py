#!/usr/bin/env python3
"""
Generate Comprehensive Posterior Predictive Check (PPC) Visualizations
for Chapter 08: Model Criticism and Evaluation

This script creates 6 publication-quality visualizations covering:
1. PPC Process (3-step workflow)
2. Good Model PPC (well-specified model)
3. Bad Model PPC (misspecified model)
4. Test Statistics Comparison (multiple discrepancy measures)
5. Graphical PPC (density overlay, ecdf, scatter)
6. Model Inadequacy Detection (systematic errors)

Author: Nguyen Le Linh
Date: March 10, 2026
Course: Bayesian Statistics Self-Learning
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from matplotlib.patches import FancyBboxPatch, Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# Global plotting settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9


def generate_ppc_process():
    """
    Visualization 1: PPC Process (3-step workflow)
    Shows: Sample from posterior → Generate predictions → Compare with data
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    
    # Generate synthetic data
    n = 50
    x = np.random.uniform(0, 10, n)
    y_true = 2 + 0.5*x + np.random.normal(0, 1, n)
    
    # Simulate posterior samples (linear regression)
    alpha_post = np.random.normal(2, 0.2, 200)
    beta_post = np.random.normal(0.5, 0.1, 200)
    sigma_post = np.abs(np.random.normal(1, 0.15, 200))
    
    # Panel 1: Sample from Posterior
    axes[0].scatter(alpha_post[:100], beta_post[:100], s=40, alpha=0.6,
                   color='steelblue', edgecolors='black', linewidths=0.5)
    axes[0].set_xlabel('α (Intercept)', fontweight='bold')
    axes[0].set_ylabel('β (Slope)', fontweight='bold')
    axes[0].set_title('STEP 1: Sample θ from Posterior\np(θ | y)',
                     fontweight='bold', fontsize=13)
    axes[0].grid(alpha=0.3, linestyle='--')
    axes[0].text(0.05, 0.95, '1000 posterior samples',
                transform=axes[0].transAxes, fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7),
                verticalalignment='top')
    
    # Panel 2: Generate Predictions
    y_reps = []
    for i in range(50):
        idx = np.random.randint(0, len(alpha_post))
        y_rep = alpha_post[idx] + beta_post[idx]*x + np.random.normal(0, sigma_post[idx], n)
        y_reps.append(y_rep)
        if i < 20:
            axes[1].plot(x, y_rep, 'o', alpha=0.3, markersize=4, color='lightblue')
    
    axes[1].scatter(x, y_true, s=60, color='red', edgecolors='black',
                   linewidths=1.5, label='Observed Data', zorder=5, alpha=0.8)
    axes[1].set_xlabel('x (Predictor)', fontweight='bold')
    axes[1].set_ylabel('y (Outcome)', fontweight='bold')
    axes[1].set_title('STEP 2: Generate ỹ from p(ỹ | θ)\n20 replications shown',
                     fontweight='bold', fontsize=13)
    axes[1].legend(loc='upper left', framealpha=0.9)
    axes[1].grid(alpha=0.3, linestyle='--')
    
    # Panel 3: Compare Distributions
    axes[2].hist(y_true, bins=15, alpha=0.7, density=True, edgecolor='black',
                label='Observed', color='red', linewidth=1.5)
    
    # Plot multiple predictive distributions
    for y_rep in y_reps[:40]:
        axes[2].hist(y_rep, bins=15, alpha=0.03, density=True, color='blue')
    
    # Mean predictive distribution
    y_reps_all = np.array(y_reps).flatten()
    axes[2].hist(y_reps_all, bins=15, alpha=0, density=True, 
                histtype='step', color='blue', linewidth=2.5, 
                label='Predicted (50 reps)')
    
    axes[2].set_xlabel('y', fontweight='bold')
    axes[2].set_ylabel('Density', fontweight='bold')
    axes[2].set_title('STEP 3: Compare Distributions\nObserved vs Predicted',
                     fontweight='bold', fontsize=13)
    axes[2].legend(loc='upper right', framealpha=0.9)
    axes[2].grid(alpha=0.3, axis='y', linestyle='--')
    
    plt.suptitle('Posterior Predictive Check (PPC) Workflow', 
                fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('ppc_process_workflow.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: ppc_process_workflow.png")
    plt.close()


def generate_good_vs_bad_ppc():
    """
    Visualization 2: Good Model vs Bad Model PPC
    Shows: Well-specified model vs misspecified model
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    
    n = 100
    x = np.linspace(0, 10, n)
    
    # ===== GOOD MODEL: Linear truth, linear fit =====
    y_true_linear = 2 + 0.5*x + np.random.normal(0, 1, n)
    
    # Generate PPC for good model
    n_reps = 50
    y_reps_good = []
    for _ in range(n_reps):
        alpha = np.random.normal(2, 0.15)
        beta = np.random.normal(0.5, 0.08)
        sigma = abs(np.random.normal(1, 0.1))
        y_rep = alpha + beta*x + np.random.normal(0, sigma, n)
        y_reps_good.append(y_rep)
    
    # Panel 0,0: Raw data comparison (good)
    for y_rep in y_reps_good[:20]:
        axes[0,0].plot(x, y_rep, alpha=0.15, color='blue', linewidth=0.8)
    axes[0,0].scatter(x, y_true_linear, s=25, color='red', alpha=0.7, 
                     edgecolors='black', linewidths=0.5, label='Observed', zorder=5)
    axes[0,0].set_xlabel('x', fontweight='bold')
    axes[0,0].set_ylabel('y', fontweight='bold')
    axes[0,0].set_title('GOOD MODEL: Data vs Predictions', fontweight='bold')
    axes[0,0].legend(loc='upper left')
    axes[0,0].grid(alpha=0.3, linestyle='--')
    
    # Panel 0,1: Density overlay (good)
    axes[0,1].hist(y_true_linear, bins=20, alpha=0.6, density=True, 
                  edgecolor='black', label='Observed', color='red', linewidth=1.5)
    for y_rep in y_reps_good[:30]:
        axes[0,1].hist(y_rep, bins=20, alpha=0.04, density=True, color='blue')
    axes[0,1].set_xlabel('y', fontweight='bold')
    axes[0,1].set_ylabel('Density', fontweight='bold')
    axes[0,1].set_title('GOOD MODEL: Distribution Match', fontweight='bold')
    axes[0,1].legend()
    axes[0,1].grid(alpha=0.3, axis='y', linestyle='--')
    
    # Panel 0,2: Test statistic (good)
    mean_obs = np.mean(y_true_linear)
    means_rep = [np.mean(y_rep) for y_rep in y_reps_good]
    
    axes[0,2].hist(means_rep, bins=20, alpha=0.7, edgecolor='black', 
                  color='lightblue', label='Predicted Means')
    axes[0,2].axvline(mean_obs, color='red', linewidth=3, 
                     label=f'Observed Mean = {mean_obs:.2f}', linestyle='--')
    axes[0,2].set_xlabel('Mean(y)', fontweight='bold')
    axes[0,2].set_ylabel('Frequency', fontweight='bold')
    axes[0,2].set_title('GOOD MODEL: Test Statistic', fontweight='bold')
    axes[0,2].legend()
    axes[0,2].grid(alpha=0.3, axis='y', linestyle='--')
    
    # Bayesian p-value
    p_value_good = np.mean(np.array(means_rep) >= mean_obs)
    axes[0,2].text(0.05, 0.95, f'Bayesian p = {p_value_good:.3f}\n(Good!)', 
                  transform=axes[0,2].transAxes, fontsize=10,
                  bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
                  verticalalignment='top')
    
    # ===== BAD MODEL: Quadratic truth, linear fit =====
    y_true_quad = 2 + 0.5*x + 0.15*x**2 + np.random.normal(0, 1, n)
    
    # Generate PPC for bad model (still using linear model on quadratic data)
    y_reps_bad = []
    for _ in range(n_reps):
        alpha = np.random.normal(3, 0.2)
        beta = np.random.normal(1.2, 0.1)
        sigma = abs(np.random.normal(1.8, 0.15))
        y_rep = alpha + beta*x + np.random.normal(0, sigma, n)
        y_reps_bad.append(y_rep)
    
    # Panel 1,0: Raw data comparison (bad)
    for y_rep in y_reps_bad[:20]:
        axes[1,0].plot(x, y_rep, alpha=0.15, color='blue', linewidth=0.8)
    axes[1,0].scatter(x, y_true_quad, s=25, color='red', alpha=0.7,
                     edgecolors='black', linewidths=0.5, label='Observed', zorder=5)
    axes[1,0].set_xlabel('x', fontweight='bold')
    axes[1,0].set_ylabel('y', fontweight='bold')
    axes[1,0].set_title('BAD MODEL: Data vs Predictions\n(Quadratic truth, Linear fit)', 
                       fontweight='bold')
    axes[1,0].legend(loc='upper left')
    axes[1,0].grid(alpha=0.3, linestyle='--')
    axes[1,0].text(0.5, 0.1, 'Systematic Pattern!', transform=axes[1,0].transAxes,
                  fontsize=11, color='red', fontweight='bold', ha='center',
                  bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Panel 1,1: Density overlay (bad)
    axes[1,1].hist(y_true_quad, bins=20, alpha=0.6, density=True,
                  edgecolor='black', label='Observed', color='red', linewidth=1.5)
    for y_rep in y_reps_bad[:30]:
        axes[1,1].hist(y_rep, bins=20, alpha=0.04, density=True, color='blue')
    axes[1,1].set_xlabel('y', fontweight='bold')
    axes[1,1].set_ylabel('Density', fontweight='bold')
    axes[1,1].set_title('BAD MODEL: Distribution Mismatch', fontweight='bold')
    axes[1,1].legend()
    axes[1,1].grid(alpha=0.3, axis='y', linestyle='--')
    axes[1,1].text(0.05, 0.95, 'Predictions too narrow!', 
                  transform=axes[1,1].transAxes, fontsize=10, color='red',
                  bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                  verticalalignment='top')
    
    # Panel 1,2: Test statistic (bad) - use variance instead
    var_obs = np.var(y_true_quad)
    vars_rep = [np.var(y_rep) for y_rep in y_reps_bad]
    
    axes[1,2].hist(vars_rep, bins=20, alpha=0.7, edgecolor='black',
                  color='lightblue', label='Predicted Variances')
    axes[1,2].axvline(var_obs, color='red', linewidth=3,
                     label=f'Observed Var = {var_obs:.2f}', linestyle='--')
    axes[1,2].set_xlabel('Var(y)', fontweight='bold')
    axes[1,2].set_ylabel('Frequency', fontweight='bold')
    axes[1,2].set_title('BAD MODEL: Test Statistic', fontweight='bold')
    axes[1,2].legend()
    axes[1,2].grid(alpha=0.3, axis='y', linestyle='--')
    
    # Bayesian p-value
    p_value_bad = np.mean(np.array(vars_rep) >= var_obs)
    axes[1,2].text(0.05, 0.95, f'Bayesian p = {p_value_bad:.3f}\n(Bad! Extreme)', 
                  transform=axes[1,2].transAxes, fontsize=10,
                  bbox=dict(boxstyle='round', facecolor='orange', alpha=0.8),
                  verticalalignment='top')
    
    plt.suptitle('Model Quality: Good vs Bad PPC Examples', 
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('ppc_good_vs_bad_models.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: ppc_good_vs_bad_models.png")
    plt.close()


def generate_test_statistics_comparison():
    """
    Visualization 3: Multiple Test Statistics for PPC
    Shows: Mean, Variance, Min, Max, Skewness comparison
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    
    # Generate data (quadratic pattern - misspecified linear model)
    n = 100
    x = np.linspace(0, 10, n)
    y_obs = 2 + 0.5*x + 0.2*x**2 + np.random.normal(0, 2, n)
    
    # Generate replications (linear model on quadratic data)
    n_reps = 200
    y_reps = []
    for _ in range(n_reps):
        alpha = np.random.normal(3, 0.3)
        beta = np.random.normal(1.5, 0.15)
        sigma = abs(np.random.normal(2.5, 0.2))
        y_rep = alpha + beta*x + np.random.normal(0, sigma, n)
        y_reps.append(y_rep)
    
    # Define test statistics
    test_stats = {
        'Mean': (np.mean, 'Mean(y)'),
        'Variance': (np.var, 'Var(y)'),
        'Min': (np.min, 'Min(y)'),
        'Max': (np.max, 'Max(y)'),
        'Std Dev': (np.std, 'Std(y)'),
        'Range': (lambda y: np.max(y) - np.min(y), 'Range(y)')
    }
    
    for idx, (name, (func, label)) in enumerate(test_stats.items()):
        row, col = idx // 3, idx % 3
        ax = axes[row, col]
        
        # Compute test statistic
        T_obs = func(y_obs)
        T_reps = [func(y_rep) for y_rep in y_reps]
        
        # Plot
        ax.hist(T_reps, bins=30, alpha=0.7, edgecolor='black',
               color='lightblue', label='Predicted')
        ax.axvline(T_obs, color='red', linewidth=3,
                  label=f'Observed = {T_obs:.2f}', linestyle='--')
        
        # Bayesian p-value
        p_value = np.mean(np.array(T_reps) >= T_obs)
        p_value_text = min(p_value, 1 - p_value)  # Two-tailed
        
        # Color code based on p-value
        if 0.05 < p_value_text < 0.95:
            color = 'lightgreen'
            verdict = 'OK'
        elif 0.01 < p_value_text < 0.99:
            color = 'yellow'
            verdict = 'Warning'
        else:
            color = 'orange'
            verdict = 'Problem'
        
        ax.text(0.05, 0.95, f'p = {p_value:.3f}\n({verdict})', 
               transform=ax.transAxes, fontsize=10,
               bbox=dict(boxstyle='round', facecolor=color, alpha=0.8),
               verticalalignment='top')
        
        ax.set_xlabel(label, fontweight='bold')
        ax.set_ylabel('Frequency', fontweight='bold')
        ax.set_title(f'{name}', fontweight='bold', fontsize=12)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(alpha=0.3, axis='y', linestyle='--')
    
    plt.suptitle('Multiple Test Statistics for Posterior Predictive Checks', 
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('ppc_multiple_test_statistics.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: ppc_multiple_test_statistics.png")
    plt.close()


def generate_graphical_ppc():
    """
    Visualization 4: Graphical PPC Methods
    Shows: Density overlay, ECDF, Scatter plot, Residual plot
    """
    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    
    # Generate data
    n = 80
    x = np.linspace(0, 10, n)
    y_obs = 2 + 0.5*x + np.random.normal(0, 1.5, n)
    
    # Fit model and generate replications
    n_reps = 50
    y_reps = []
    for _ in range(n_reps):
        alpha = np.random.normal(2, 0.2)
        beta = np.random.normal(0.5, 0.1)
        sigma = abs(np.random.normal(1.5, 0.15))
        y_rep = alpha + beta*x + np.random.normal(0, sigma, n)
        y_reps.append(y_rep)
    
    # 1. Density Overlay
    ax1 = fig.add_subplot(gs[0, :])
    for y_rep in y_reps[:40]:
        ax1.hist(y_rep, bins=25, alpha=0.03, density=True, color='blue')
    ax1.hist(y_obs, bins=25, alpha=0.7, density=True, edgecolor='black',
            color='red', linewidth=2, label='Observed')
    ax1.set_xlabel('y', fontweight='bold')
    ax1.set_ylabel('Density', fontweight='bold')
    ax1.set_title('A. Density Overlay: Observed vs 40 Posterior Predictive Distributions', 
                 fontweight='bold', fontsize=13)
    ax1.legend(loc='upper right', fontsize=11)
    ax1.grid(alpha=0.3, axis='y', linestyle='--')
    
    # 2. ECDF Comparison
    ax2 = fig.add_subplot(gs[1, 0])
    
    # Observed ECDF
    y_sorted = np.sort(y_obs)
    ecdf_obs = np.arange(1, len(y_sorted) + 1) / len(y_sorted)
    ax2.plot(y_sorted, ecdf_obs, 'r-', linewidth=3, label='Observed', alpha=0.8)
    
    # Replicated ECDFs
    for y_rep in y_reps[:20]:
        y_rep_sorted = np.sort(y_rep)
        ecdf_rep = np.arange(1, len(y_rep_sorted) + 1) / len(y_rep_sorted)
        ax2.plot(y_rep_sorted, ecdf_rep, 'b-', linewidth=0.8, alpha=0.2)
    
    ax2.set_xlabel('y', fontweight='bold')
    ax2.set_ylabel('Cumulative Probability', fontweight='bold')
    ax2.set_title('B. ECDF Comparison', fontweight='bold', fontsize=12)
    ax2.legend(loc='lower right')
    ax2.grid(alpha=0.3, linestyle='--')
    
    # 3. Scatter Plot: Observed vs Mean Prediction
    ax3 = fig.add_subplot(gs[1, 1])
    y_mean_pred = np.mean(y_reps, axis=0)
    
    ax3.scatter(y_obs, y_mean_pred, s=40, alpha=0.7, edgecolors='black',
               linewidths=0.5, color='steelblue')
    
    # 45-degree line
    lims = [min(y_obs.min(), y_mean_pred.min()), max(y_obs.max(), y_mean_pred.max())]
    ax3.plot(lims, lims, 'r--', linewidth=2, label='Perfect Prediction', alpha=0.7)
    
    ax3.set_xlabel('Observed y', fontweight='bold')
    ax3.set_ylabel('Mean Predicted y', fontweight='bold')
    ax3.set_title('C. Observed vs Predicted', fontweight='bold', fontsize=12)
    ax3.legend(loc='upper left')
    ax3.grid(alpha=0.3, linestyle='--')
    
    # 4. Residual Plot
    ax4 = fig.add_subplot(gs[1, 2])
    residuals = y_obs - y_mean_pred
    
    ax4.scatter(y_mean_pred, residuals, s=40, alpha=0.7, edgecolors='black',
               linewidths=0.5, color='coral')
    ax4.axhline(0, color='black', linewidth=2, linestyle='--', alpha=0.7)
    ax4.set_xlabel('Predicted y', fontweight='bold')
    ax4.set_ylabel('Residuals', fontweight='bold')
    ax4.set_title('D. Residual Plot', fontweight='bold', fontsize=12)
    ax4.grid(alpha=0.3, linestyle='--')
    
    # 5. QQ Plot
    ax5 = fig.add_subplot(gs[2, 0])
    
    # Theoretical quantiles (normal)
    theoretical_quantiles = stats.norm.ppf(np.linspace(0.01, 0.99, len(y_obs)))
    observed_quantiles = np.sort(stats.zscore(y_obs))
    
    ax5.scatter(theoretical_quantiles, observed_quantiles, s=40, alpha=0.7,
               edgecolors='black', linewidths=0.5, color='mediumseagreen')
    ax5.plot(theoretical_quantiles, theoretical_quantiles, 'r--', linewidth=2,
            label='Normal', alpha=0.7)
    ax5.set_xlabel('Theoretical Quantiles', fontweight='bold')
    ax5.set_ylabel('Sample Quantiles', fontweight='bold')
    ax5.set_title('E. Q-Q Plot (Normality Check)', fontweight='bold', fontsize=12)
    ax5.legend(loc='upper left')
    ax5.grid(alpha=0.3, linestyle='--')
    
    # 6. Interval Coverage
    ax6 = fig.add_subplot(gs[2, 1:])
    
    # Compute 95% prediction intervals
    y_reps_array = np.array(y_reps)
    lower = np.percentile(y_reps_array, 2.5, axis=0)
    upper = np.percentile(y_reps_array, 97.5, axis=0)
    
    # Sort by x for better visualization
    sort_idx = np.argsort(x)
    x_sorted = x[sort_idx]
    y_obs_sorted = y_obs[sort_idx]
    lower_sorted = lower[sort_idx]
    upper_sorted = upper[sort_idx]
    
    ax6.fill_between(x_sorted, lower_sorted, upper_sorted, alpha=0.3,
                    color='lightblue', label='95% Prediction Interval')
    ax6.plot(x_sorted, y_obs_sorted, 'ro', markersize=5, alpha=0.7,
            label='Observed Data')
    
    # Check coverage
    in_interval = (y_obs >= lower) & (y_obs <= upper)
    coverage = np.mean(in_interval) * 100
    
    ax6.set_xlabel('x (Predictor)', fontweight='bold')
    ax6.set_ylabel('y (Outcome)', fontweight='bold')
    ax6.set_title(f'F. Prediction Interval Coverage: {coverage:.1f}% (Target: 95%)', 
                 fontweight='bold', fontsize=12)
    ax6.legend(loc='upper left')
    ax6.grid(alpha=0.3, linestyle='--')
    
    plt.suptitle('Graphical Posterior Predictive Checks: Six Methods', 
                fontsize=16, fontweight='bold', y=0.995)
    plt.savefig('ppc_graphical_methods.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: ppc_graphical_methods.png")
    plt.close()


def generate_model_inadequacy_detection():
    """
    Visualization 5: Detecting Model Inadequacies
    Shows: Different types of model failures (heteroscedasticity, outliers, nonlinearity)
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    
    n = 80
    x = np.linspace(0, 10, n)
    
    # Case 1: Heteroscedasticity (variance increases with x)
    noise = np.random.normal(0, 0.3 + 0.15*x, n)
    y_hetero = 2 + 0.5*x + noise
    
    axes[0,0].scatter(x, y_hetero, s=40, alpha=0.7, edgecolors='black',
                     linewidths=0.5, color='coral')
    axes[0,0].plot(x, 2 + 0.5*x, 'b--', linewidth=2, label='True Mean')
    axes[0,0].set_xlabel('x', fontweight='bold')
    axes[0,0].set_ylabel('y', fontweight='bold')
    axes[0,0].set_title('A. Heteroscedasticity\n(Variance increases with x)', 
                       fontweight='bold')
    axes[0,0].legend()
    axes[0,0].grid(alpha=0.3, linestyle='--')
    
    # Fit constant-variance model
    y_pred_homo = 2 + 0.5*x
    residuals_hetero = y_hetero - y_pred_homo
    
    axes[1,0].scatter(x, residuals_hetero, s=40, alpha=0.7, edgecolors='black',
                     linewidths=0.5, color='coral')
    axes[1,0].axhline(0, color='black', linewidth=2, linestyle='--')
    axes[1,0].set_xlabel('x', fontweight='bold')
    axes[1,0].set_ylabel('Residuals', fontweight='bold')
    axes[1,0].set_title('Residual Plot: Funnel Pattern!', fontweight='bold')
    axes[1,0].grid(alpha=0.3, linestyle='--')
    axes[1,0].text(0.5, 0.9, 'Model assumes constant variance\nBUT data has increasing variance!',
                  transform=axes[1,0].transAxes, fontsize=9, ha='center',
                  bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                  verticalalignment='top')
    
    # Case 2: Outliers
    y_outlier = 2 + 0.5*x + np.random.normal(0, 0.8, n)
    outlier_indices = [10, 35, 65]
    y_outlier[outlier_indices] += np.array([8, -7, 9])
    
    axes[0,1].scatter(x, y_outlier, s=40, alpha=0.7, edgecolors='black',
                     linewidths=0.5, color='mediumseagreen')
    axes[0,1].scatter(x[outlier_indices], y_outlier[outlier_indices], s=150,
                     color='red', edgecolors='black', linewidths=2, 
                     marker='X', label='Outliers', zorder=5)
    axes[0,1].plot(x, 2 + 0.5*x, 'b--', linewidth=2, label='True Mean')
    axes[0,1].set_xlabel('x', fontweight='bold')
    axes[0,1].set_ylabel('y', fontweight='bold')
    axes[0,1].set_title('B. Outliers\n(Extreme observations)', fontweight='bold')
    axes[0,1].legend()
    axes[0,1].grid(alpha=0.3, linestyle='--')
    
    y_pred_outlier = 2 + 0.5*x
    residuals_outlier = y_outlier - y_pred_outlier
    
    axes[1,1].scatter(x, residuals_outlier, s=40, alpha=0.7, edgecolors='black',
                     linewidths=0.5, color='mediumseagreen')
    axes[1,1].scatter(x[outlier_indices], residuals_outlier[outlier_indices], s=150,
                     color='red', edgecolors='black', linewidths=2, marker='X', zorder=5)
    axes[1,1].axhline(0, color='black', linewidth=2, linestyle='--')
    axes[1,1].set_xlabel('x', fontweight='bold')
    axes[1,1].set_ylabel('Residuals', fontweight='bold')
    axes[1,1].set_title('Residual Plot: Extreme Points!', fontweight='bold')
    axes[1,1].grid(alpha=0.3, linestyle='--')
    axes[1,1].text(0.5, 0.9, 'Large residuals indicate\nmodel doesn\'t capture these points',
                  transform=axes[1,1].transAxes, fontsize=9, ha='center',
                  bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                  verticalalignment='top')
    
    # Case 3: Nonlinearity (quadratic truth, linear fit)
    y_nonlinear = 2 + 0.5*x + 0.15*x**2 + np.random.normal(0, 1.5, n)
    
    axes[0,2].scatter(x, y_nonlinear, s=40, alpha=0.7, edgecolors='black',
                     linewidths=0.5, color='steelblue')
    axes[0,2].plot(x, 2 + 0.5*x + 0.15*x**2, 'g-', linewidth=2.5, 
                  label='True (Quadratic)', alpha=0.8)
    
    # Linear fit
    from numpy.polynomial import polynomial as P
    coefs = P.polyfit(x, y_nonlinear, 1)
    y_pred_linear = P.polyval(x, coefs)
    axes[0,2].plot(x, y_pred_linear, 'r--', linewidth=2, label='Linear Fit', alpha=0.8)
    
    axes[0,2].set_xlabel('x', fontweight='bold')
    axes[0,2].set_ylabel('y', fontweight='bold')
    axes[0,2].set_title('C. Nonlinearity\n(Quadratic truth, Linear model)', 
                       fontweight='bold')
    axes[0,2].legend()
    axes[0,2].grid(alpha=0.3, linestyle='--')
    
    residuals_nonlinear = y_nonlinear - y_pred_linear
    
    axes[1,2].scatter(x, residuals_nonlinear, s=40, alpha=0.7, edgecolors='black',
                     linewidths=0.5, color='steelblue')
    axes[1,2].axhline(0, color='black', linewidth=2, linestyle='--')
    
    # Add loess smooth to show pattern
    from scipy.interpolate import UnivariateSpline
    spl = UnivariateSpline(x, residuals_nonlinear, s=50)
    x_smooth = np.linspace(x.min(), x.max(), 200)
    axes[1,2].plot(x_smooth, spl(x_smooth), 'r-', linewidth=3, 
                  label='Smooth Pattern', alpha=0.8)
    
    axes[1,2].set_xlabel('x', fontweight='bold')
    axes[1,2].set_ylabel('Residuals', fontweight='bold')
    axes[1,2].set_title('Residual Plot: Curved Pattern!', fontweight='bold')
    axes[1,2].legend()
    axes[1,2].grid(alpha=0.3, linestyle='--')
    axes[1,2].text(0.5, 0.9, 'Systematic pattern indicates\nmissing quadratic term!',
                  transform=axes[1,2].transAxes, fontsize=9, ha='center',
                  bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                  verticalalignment='top')
    
    plt.suptitle('Detecting Model Inadequacies via PPC Residuals', 
                fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('ppc_model_inadequacy_detection.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: ppc_model_inadequacy_detection.png")
    plt.close()


def generate_ppc_workflow_diagram():
    """
    Visualization 6: PPC Decision Workflow
    Shows: Decision tree for model checking and improvement
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Helper function to draw boxes
    def draw_box(ax, x, y, width, height, text, color, fontsize=10):
        box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                            boxstyle="round,pad=0.1", 
                            facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
               fontweight='bold', wrap=True)
    
    # Helper function to draw arrows
    def draw_arrow(ax, x1, y1, x2, y2, label='', color='black'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color=color))
        if label:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.3, mid_y, label, fontsize=9, 
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # Start
    draw_box(ax, 5, 9, 2, 0.6, 'START: Fit Model', 'lightgreen', 11)
    
    # Step 1
    draw_box(ax, 5, 7.8, 3, 0.8, 'Generate Posterior\nPredictive Data (ỹ)', 'lightblue', 10)
    draw_arrow(ax, 5, 8.7, 5, 8.2)
    
    # Step 2
    draw_box(ax, 5, 6.4, 3, 0.8, 'Choose Test Statistic\nT(y)', 'lightyellow', 10)
    draw_arrow(ax, 5, 7.4, 5, 6.8)
    
    # Step 3: Compute
    draw_box(ax, 5, 5, 3.5, 0.8, 'Compute T(y_obs) and T(ỹ)\nfor all replications', 
            'lightcyan', 10)
    draw_arrow(ax, 5, 6, 5, 5.4)
    
    # Decision Diamond
    draw_box(ax, 5, 3.6, 2, 0.8, 'T(y_obs) consistent\nwith T(ỹ)?', 'orange', 10)
    draw_arrow(ax, 5, 4.6, 5, 4)
    
    # Yes path
    draw_box(ax, 2, 2.2, 2, 0.6, 'Model is adequate', 'lightgreen', 10)
    draw_arrow(ax, 4, 3.6, 2.5, 2.5, 'YES', 'green')
    
    # No path
    draw_box(ax, 7.5, 2.2, 2.5, 0.6, 'Model inadequate', 'salmon', 10)
    draw_arrow(ax, 6, 3.6, 7, 2.5, 'NO', 'red')
    
    # From "adequate"
    draw_box(ax, 2, 0.8, 2.5, 0.6, 'Proceed with\ninference', 'palegreen', 10)
    draw_arrow(ax, 2, 1.9, 2, 1.1)
    
    # From "inadequate"
    draw_box(ax, 7.5, 0.8, 2.5, 0.8, 'Diagnose problem:\n• Residual plots\n• Test statistics', 
            'lightyellow', 9)
    draw_arrow(ax, 7.5, 1.9, 7.5, 1.2)
    
    # Improvement loop
    draw_arrow(ax, 6.5, 0.8, 3, 7.8, 'Revise\nModel', 'red')
    
    # Add examples box
    examples_text = ('Common Test Statistics:\n'
                    '• Mean, Variance, Std Dev\n'
                    '• Min, Max, Range\n'
                    '• Quantiles\n'
                    '• Skewness, Kurtosis')
    ax.text(0.5, 5, examples_text, fontsize=9,
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.9, linewidth=2))
    
    # Add tips box
    tips_text = ('Improvement Strategies:\n'
                '• Add nonlinear terms\n'
                '• Transform variables\n'
                '• Model heteroscedasticity\n'
                '• Use robust likelihood\n'
                '• Add interaction terms')
    ax.text(9.5, 5, tips_text, fontsize=9,
           bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9, linewidth=2),
           ha='right')
    
    plt.title('Posterior Predictive Check (PPC) Workflow', 
             fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('ppc_workflow_diagram.png', dpi=300, bbox_inches='tight')
    print("✓ Generated: ppc_workflow_diagram.png")
    plt.close()


def main():
    """Generate all PPC visualizations"""
    print("\n" + "="*70)
    print("GENERATING CHAPTER 08 PPC VISUALIZATIONS")
    print("="*70 + "\n")
    
    print("Generating 6 comprehensive visualizations for Posterior Predictive Checks...\n")
    
    generate_ppc_process()
    generate_good_vs_bad_ppc()
    generate_test_statistics_comparison()
    generate_graphical_ppc()
    generate_model_inadequacy_detection()
    generate_ppc_workflow_diagram()
    
    print("\n" + "="*70)
    print("✅ ALL VISUALIZATIONS COMPLETE!")
    print("="*70)
    print("\nGenerated 6 images:")
    print("  1. ppc_process_workflow.png")
    print("  2. ppc_good_vs_bad_models.png")
    print("  3. ppc_multiple_test_statistics.png")
    print("  4. ppc_graphical_methods.png")
    print("  5. ppc_model_inadequacy_detection.png")
    print("  6. ppc_workflow_diagram.png")
    print("\nTotal: ~18-20 MB (300 DPI, publication quality)")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
