#!/usr/bin/env python3
"""
Script để tạo các hình ảnh minh họa nâng cao cho Chapter 04: Bayesian Regression

Các visualizations mới:
1. Regression Assumptions (Linearity, Homoscedasticity, Normality)
2. Model Diagnostics (Residual plots, Q-Q plots)
3. Posterior Predictive Checks
4. Model Comparison (LOO-CV, WAIC concepts)

Sử dụng:
    python3 generate_regression_diagnostics.py

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

def generate_regression_assumptions():
    """Hình 1: Regression Assumptions - Good vs Bad"""
    fig, axes = plt.subplots(3, 4, figsize=(20, 14))
    
    np.random.seed(42)
    n = 100
    x = np.linspace(0, 10, n)
    
    # GOOD MODEL - Meets all assumptions
    y_good = 2 + 3*x + np.random.normal(0, 2, n)
    residuals_good = y_good - (2 + 3*x)
    
    # BAD MODEL 1 - Non-linearity
    y_nonlinear = 2 + 3*x + 0.5*x**2 + np.random.normal(0, 2, n)
    y_pred_linear = 2 + 3*x  # Wrong model (linear fit)
    residuals_nonlinear = y_nonlinear - y_pred_linear
    
    # BAD MODEL 2 - Heteroscedasticity
    sigma_het = 0.5 + 0.3*x  # Variance increases with x
    y_het = 2 + 3*x + np.random.normal(0, 1, n) * sigma_het
    residuals_het = y_het - (2 + 3*x)
    
    # BAD MODEL 3 - Non-normal residuals (heavy tails)
    y_nonnormal = 2 + 3*x + stats.t.rvs(df=3, size=n) * 2
    residuals_nonnormal = y_nonnormal - (2 + 3*x)
    
    datasets = [
        (x, y_good, residuals_good, 'GOOD MODEL\nMeets All Assumptions', 'green'),
        (x, y_nonlinear, residuals_nonlinear, 'BAD: Non-Linearity', 'red'),
        (x, y_het, residuals_het, 'BAD: Heteroscedasticity', 'orange'),
        (x, y_nonnormal, residuals_nonnormal, 'BAD: Non-Normal Residuals', 'purple')
    ]
    
    for col, (x_data, y_data, residuals, title, color) in enumerate(datasets):
        # Row 1: Scatter plot with fitted line
        axes[0, col].scatter(x_data, y_data, alpha=0.5, s=30, color=color)
        
        # Fit line
        if col == 1:  # Non-linear case
            axes[0, col].plot(x_data, y_pred_linear, 'k--', linewidth=3, 
                             label='Wrong linear fit', alpha=0.7)
            axes[0, col].plot(x_data, 2 + 3*x_data + 0.5*x_data**2, 'g-', 
                             linewidth=2, label='True (quadratic)', alpha=0.7)
        else:
            axes[0, col].plot(x_data, 2 + 3*x_data, 'k-', linewidth=3, 
                             label='Fitted line', alpha=0.7)
        
        axes[0, col].set_title(title, fontsize=11, fontweight='bold')
        axes[0, col].set_xlabel('x', fontsize=10)
        axes[0, col].set_ylabel('y', fontsize=10)
        axes[0, col].legend(fontsize=9)
        axes[0, col].grid(True, alpha=0.3)
        
        # Row 2: Residual plot
        axes[1, col].scatter(x_data, residuals, alpha=0.5, s=30, color=color)
        axes[1, col].axhline(0, color='black', linestyle='--', linewidth=2)
        
        # Add lowess trend line
        from scipy.signal import savgol_filter
        if len(residuals) > 10:
            trend = savgol_filter(residuals, window_length=21, polyorder=3)
            axes[1, col].plot(x_data, trend, 'r-', linewidth=3, 
                             label='Trend', alpha=0.7)
        
        axes[1, col].set_title('Residuals vs Fitted', fontsize=11, fontweight='bold')
        axes[1, col].set_xlabel('x', fontsize=10)
        axes[1, col].set_ylabel('Residuals', fontsize=10)
        axes[1, col].grid(True, alpha=0.3)
        
        # Assessment
        if col == 0:
            assessment = '✓ Good: Random\n✓ No pattern\n✓ Constant variance'
            box_color = 'lightgreen'
        elif col == 1:
            assessment = '✗ Bad: Clear pattern\n✗ Curved trend\n→ Need quadratic'
            box_color = 'lightcoral'
        elif col == 2:
            assessment = '✗ Bad: Fan shape\n✗ Variance increases\n→ Transform y'
            box_color = 'lightyellow'
        else:
            assessment = '✗ Bad: Outliers\n✗ Heavy tails\n→ Robust model'
            box_color = 'lavender'
        
        axes[1, col].text(0.05, 0.95, assessment, 
                         transform=axes[1, col].transAxes,
                         fontsize=9, ha='left', va='top',
                         bbox=dict(boxstyle='round', facecolor=box_color, alpha=0.9))
        
        # Row 3: Q-Q plot for normality check
        stats.probplot(residuals, dist="norm", plot=axes[2, col])
        axes[2, col].set_title('Q-Q Plot (Normality Check)', fontsize=11, fontweight='bold')
        axes[2, col].grid(True, alpha=0.3)
        
        if col == 0 or col == 2:
            qq_assessment = '✓ Good: Points on line'
            qq_color = 'lightgreen'
        else:
            qq_assessment = '✗ Bad: Deviates from line'
            qq_color = 'lightcoral'
        
        axes[2, col].text(0.05, 0.95, qq_assessment,
                         transform=axes[2, col].transAxes,
                         fontsize=9, ha='left', va='top',
                         bbox=dict(boxstyle='round', facecolor=qq_color, alpha=0.9))
    
    plt.suptitle('Regression Assumptions: Good Model vs Common Violations\n' + 
                 'Check: Linearity + Homoscedasticity + Normality', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    save_figure('regression_assumptions_diagnostic.png')

def generate_posterior_predictive_checks():
    """Hình 2: Posterior Predictive Checks"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    
    np.random.seed(42)
    n_obs = 50
    x = np.linspace(0, 10, n_obs)
    
    # True model
    true_alpha = 5
    true_beta = 2
    true_sigma = 3
    y_observed = true_alpha + true_beta * x + np.random.normal(0, true_sigma, n_obs)
    
    # Simulate posterior samples (pretend we have posterior)
    n_posterior_samples = 100
    
    alpha_samples = np.random.normal(true_alpha, 0.5, n_posterior_samples)
    beta_samples = np.random.normal(true_beta, 0.1, n_posterior_samples)
    sigma_samples = np.abs(np.random.normal(true_sigma, 0.3, n_posterior_samples))
    
    # Generate posterior predictive samples
    y_pred_samples = np.zeros((n_posterior_samples, n_obs))
    for i in range(n_posterior_samples):
        mu = alpha_samples[i] + beta_samples[i] * x
        y_pred_samples[i, :] = mu + np.random.normal(0, sigma_samples[i], n_obs)
    
    # Panel 1: Observed vs Posterior Predictive samples
    axes[0, 0].scatter(x, y_observed, color='red', s=80, alpha=0.8, 
                       label='Observed data', zorder=3, edgecolors='black', linewidths=1.5)
    
    # Plot some posterior predictive samples
    for i in range(20):
        axes[0, 0].plot(x, y_pred_samples[i, :], 'b-', alpha=0.1, linewidth=1)
    
    # Posterior predictive mean and intervals
    y_pred_mean = np.mean(y_pred_samples, axis=0)
    y_pred_lower = np.percentile(y_pred_samples, 5, axis=0)
    y_pred_upper = np.percentile(y_pred_samples, 95, axis=0)
    
    axes[0, 0].plot(x, y_pred_mean, 'b-', linewidth=3, label='Post. pred. mean', alpha=0.8)
    axes[0, 0].fill_between(x, y_pred_lower, y_pred_upper, alpha=0.3, color='blue',
                            label='90% pred. interval')
    
    axes[0, 0].set_title('Posterior Predictive Check\nObserved vs Predicted', 
                         fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('x', fontsize=11)
    axes[0, 0].set_ylabel('y', fontsize=11)
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Panel 2: Distribution of y at x=5
    x_test = 5
    idx_test = np.argmin(np.abs(x - x_test))
    
    axes[0, 1].hist(y_pred_samples[:, idx_test], bins=30, alpha=0.7, density=True,
                    color='blue', edgecolor='black', label='Posterior predictive')
    axes[0, 1].axvline(y_observed[idx_test], color='red', linestyle='--', 
                       linewidth=3, label=f'Observed: {y_observed[idx_test]:.1f}')
    axes[0, 1].set_title(f'Posterior Predictive at x={x_test}', 
                         fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('y', fontsize=11)
    axes[0, 1].set_ylabel('Density', fontsize=11)
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Panel 3: Test statistics
    # Compute test statistic: mean(y)
    test_stat_observed = np.mean(y_observed)
    test_stat_predicted = np.mean(y_pred_samples, axis=1)
    
    axes[0, 2].hist(test_stat_predicted, bins=30, alpha=0.7, density=True,
                    color='skyblue', edgecolor='black', label='Predicted mean(y)')
    axes[0, 2].axvline(test_stat_observed, color='red', linestyle='--',
                       linewidth=3, label=f'Observed: {test_stat_observed:.1f}')
    
    # P-value
    p_value = np.mean(test_stat_predicted >= test_stat_observed)
    
    axes[0, 2].set_title(f'Test Statistic: mean(y)\nBayesian p-value={p_value:.3f}', 
                         fontsize=12, fontweight='bold')
    axes[0, 2].set_xlabel('mean(y)', fontsize=11)
    axes[0, 2].set_ylabel('Density', fontsize=11)
    axes[0, 2].legend(fontsize=10)
    axes[0, 2].grid(True, alpha=0.3)
    
    # Panel 4: Residual distribution
    residuals_observed = y_observed - (true_alpha + true_beta * x)
    
    residuals_predicted = []
    for i in range(n_posterior_samples):
        mu = alpha_samples[i] + beta_samples[i] * x
        res = y_pred_samples[i, :] - mu
        residuals_predicted.extend(res)
    
    axes[1, 0].hist(residuals_predicted, bins=50, alpha=0.5, density=True,
                    color='blue', edgecolor='black', label='Predicted residuals')
    axes[1, 0].hist(residuals_observed, bins=20, alpha=0.7, density=True,
                    color='red', edgecolor='black', label='Observed residuals')
    
    axes[1, 0].set_title('Residual Distribution Check', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Residuals', fontsize=11)
    axes[1, 0].set_ylabel('Density', fontsize=11)
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Panel 5: Variance check
    var_observed = np.var(y_observed)
    var_predicted = np.var(y_pred_samples, axis=1)
    
    axes[1, 1].hist(var_predicted, bins=30, alpha=0.7, density=True,
                    color='skyblue', edgecolor='black', label='Predicted var(y)')
    axes[1, 1].axvline(var_observed, color='red', linestyle='--',
                       linewidth=3, label=f'Observed: {var_observed:.1f}')
    
    axes[1, 1].set_title('Variance Check', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('var(y)', fontsize=11)
    axes[1, 1].set_ylabel('Density', fontsize=11)
    axes[1, 1].legend(fontsize=10)
    axes[1, 1].grid(True, alpha=0.3)
    
    # Panel 6: Summary
    axes[1, 2].axis('off')
    summary_text = """
╔═══════════════════════════════════╗
║  POSTERIOR PREDICTIVE CHECKS      ║
╠═══════════════════════════════════╣
║                                   ║
║  IDEA:                            ║
║    Nếu model tốt, dữ liệu         ║
║    quan sát nên "típ" với         ║
║    dữ liệu predicted từ model     ║
║                                   ║
║  WORKFLOW:                        ║
║    1. Sample từ posterior         ║
║    2. Generate ỹ ~ p(ỹ|θ,x)       ║
║    3. Compare ỹ với y_observed    ║
║                                   ║
║  CHECKS:                          ║
║    ✓ Visual: Overlap?             ║
║    ✓ Test statistics              ║
║    ✓ Distribution shape           ║
║    ✓ Mean, variance               ║
║    ✓ Residuals                    ║
║                                   ║
║  INTERPRETATION:                  ║
║    • Good fit: Observed trong     ║
║      posterior predictive         ║
║    • Bad fit: Observed ngoài      ║
║      → Model cần cải thiện        ║
║                                   ║
╚═══════════════════════════════════╝
"""
    axes[1, 2].text(0.5, 0.5, summary_text, fontsize=9, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))
    
    plt.suptitle('Posterior Predictive Checks: Model Validation\n' + 
                 'Generate data from model and compare with observed', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    save_figure('posterior_predictive_checks.png')

def generate_model_comparison_concepts():
    """Hình 3: Model Comparison - LOO-CV and WAIC Concepts"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    np.random.seed(42)
    n = 30
    x = np.linspace(0, 10, n)
    y_true = 2 + 3*x + 0.2*x**2
    y = y_true + np.random.normal(0, 3, n)
    
    # Model 1: Linear (underfitting)
    from numpy.polynomial import Polynomial
    p1 = Polynomial.fit(x, y, 1)
    y_pred1 = p1(x)
    
    # Model 2: Quadratic (just right)
    p2 = Polynomial.fit(x, y, 2)
    y_pred2 = p2(x)
    
    # Model 3: High degree (overfitting)
    p3 = Polynomial.fit(x, y, 8)
    y_pred3 = p3(x)
    
    # Panel 1: Three models
    axes[0, 0].scatter(x, y, color='red', s=80, alpha=0.8, label='Data', 
                       zorder=3, edgecolors='black')
    axes[0, 0].plot(x, y_pred1, 'b--', linewidth=2.5, label='Model 1: Linear', alpha=0.8)
    axes[0, 0].plot(x, y_pred2, 'g-', linewidth=2.5, label='Model 2: Quadratic', alpha=0.8)
    axes[0, 0].plot(x, y_pred3, 'purple', linewidth=2.5, label='Model 3: Degree 8', alpha=0.8)
    axes[0, 0].plot(x, y_true, 'k:', linewidth=3, label='True function', alpha=0.6)
    
    axes[0, 0].set_title('Three Competing Models', fontsize=13, fontweight='bold')
    axes[0, 0].set_xlabel('x', fontsize=11)
    axes[0, 0].set_ylabel('y', fontsize=11)
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Panel 2: In-sample fit vs Out-of-sample prediction
    # Simulate LOO-CV
    loo_errors1 = []
    loo_errors2 = []
    loo_errors3 = []
    
    for i in range(n):
        # Leave one out
        x_train = np.delete(x, i)
        y_train = np.delete(y, i)
        x_test = x[i]
        y_test = y[i]
        
        # Refit models
        p1_loo = Polynomial.fit(x_train, y_train, 1)
        p2_loo = Polynomial.fit(x_train, y_train, 2)
        p3_loo = Polynomial.fit(x_train, y_train, min(8, len(x_train)-1))
        
        # Predict
        loo_errors1.append((y_test - p1_loo(x_test))**2)
        loo_errors2.append((y_test - p2_loo(x_test))**2)
        loo_errors3.append((y_test - p3_loo(x_test))**2)
    
    loo_scores = [np.mean(loo_errors1), np.mean(loo_errors2), np.mean(loo_errors3)]
    model_names = ['Linear\n(Underfit)', 'Quadratic\n(Good)', 'Degree 8\n(Overfit)']
    colors = ['skyblue', 'lightgreen', 'lightcoral']
    
    bars = axes[0, 1].bar(model_names, loo_scores, color=colors, 
                          edgecolor='black', linewidth=2, alpha=0.8)
    axes[0, 1].set_title('LOO-CV Scores\n(Lower is better)', fontsize=13, fontweight='bold')
    axes[0, 1].set_ylabel('Mean Squared Error', fontsize=11)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Highlight best
    best_idx = np.argmin(loo_scores)
    bars[best_idx].set_edgecolor('green')
    bars[best_idx].set_linewidth(4)
    
    for i, score in enumerate(loo_scores):
        axes[0, 1].text(i, score + max(loo_scores)*0.02, f'{score:.2f}', 
                       ha='center', fontsize=11, fontweight='bold')
    
    # Panel 3: Bias-Variance Tradeoff
    axes[1, 0].axis('off')
    tradeoff_text = """
╔═══════════════════════════════════════════════╗
║        BIAS-VARIANCE TRADEOFF                 ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  MODEL 1: LINEAR (UNDERFIT)                   ║
║    • HIGH BIAS: Không capture pattern         ║
║    • LOW VARIANCE: Stable predictions         ║
║    • → Too simple!                            ║
║                                               ║
║  MODEL 2: QUADRATIC (JUST RIGHT)              ║
║    • BALANCED: Vừa đủ complexity              ║
║    • Captures true pattern                    ║
║    • Good generalization                      ║
║    • → BEST MODEL!                            ║
║                                               ║
║  MODEL 3: DEGREE 8 (OVERFIT)                  ║
║    • LOW BIAS: Fits training data perfectly   ║
║    • HIGH VARIANCE: Unstable, wiggly          ║
║    • Poor on new data                         ║
║    • → Too complex!                           ║
║                                               ║
║  GOAL:                                        ║
║    Find sweet spot: Min(Bias² + Variance)     ║
║                                               ║
╚═══════════════════════════════════════════════╝
"""
    axes[1, 0].text(0.5, 0.5, tradeoff_text, fontsize=9, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    # Panel 4: LOO-CV and WAIC explanation
    axes[1, 1].axis('off')
    method_text = """
╔═══════════════════════════════════════════════╗
║     MODEL COMPARISON METHODS                  ║
╠═══════════════════════════════════════════════╣
║                                               ║
║  LOO-CV (Leave-One-Out Cross-Validation):     ║
║    1. For each data point i:                  ║
║       - Train on all except i                 ║
║       - Predict i                             ║
║       - Compute error                         ║
║    2. Average errors                          ║
║                                               ║
║    ✓ Gold standard                            ║
║    ✓ Unbiased estimate                        ║
║    ✗ Computationally expensive                ║
║                                               ║
║  WAIC (Watanabe-Akaike Info Criterion):       ║
║    WAIC = -2 × (lppd - p_WAIC)                ║
║                                               ║
║    lppd: log pointwise pred density           ║
║    p_WAIC: effective # of parameters          ║
║                                               ║
║    ✓ Fast (no retraining)                     ║
║    ✓ Works with any Bayesian model            ║
║    ✓ Approximates LOO-CV                      ║
║                                               ║
║  INTERPRETATION:                              ║
║    → Lower LOO/WAIC = Better                  ║
║    → Compare models                           ║
║    → Account for complexity                   ║
║                                               ║
╚═══════════════════════════════════════════════╝
"""
    axes[1, 1].text(0.5, 0.5, method_text, fontsize=8.5, family='monospace',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9))
    
    plt.suptitle('Model Comparison: LOO-CV and WAIC\n' + 
                 'Balance fit and complexity for best generalization', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    save_figure('model_comparison_loo_waic.png')

def main():
    """Hàm chính để tạo tất cả các hình ảnh"""
    print('='*70)
    print('BẮT ĐẦU TẠO HÌNH ẢNH REGRESSION DIAGNOSTICS CHO CHAPTER 04')
    print('='*70)
    print()
    
    print('Phần 1/3: Regression Assumptions')
    generate_regression_assumptions()
    print('✓ Hoàn thành phần 1/3\n')
    
    print('Phần 2/3: Posterior Predictive Checks')
    generate_posterior_predictive_checks()
    print('✓ Hoàn thành phần 2/3\n')
    
    print('Phần 3/3: Model Comparison (LOO-CV, WAIC)')
    generate_model_comparison_concepts()
    print('✓ Hoàn thành phần 3/3\n')
    
    print('='*70)
    print('TẤT CẢ HÌNH ẢNH ĐÃ ĐƯỢC TẠO THÀNH CÔNG!')
    print('='*70)
    print()
    print('Danh sách các file đã tạo:')
    print('1. regression_assumptions_diagnostic.png')
    print('2. posterior_predictive_checks.png')
    print('3. model_comparison_loo_waic.png')
    print()
    print(f'Thư mục output: {OUTPUT_DIR}')

if __name__ == '__main__':
    main()
