# Chapter 03 - New Visualizations (March 2026)

## Monte Carlo & MCMC Advanced Visualizations

This directory contains 8 new advanced visualizations for Monte Carlo methods and MCMC diagnostics.

### New Images Added (March 9, 2026)

#### Monte Carlo Concepts
**Script**: `generate_monte_carlo_advanced.py`

1. **curse_of_dimensionality_detailed.png**
   - Grid approximation failure in high dimensions
   - Use: Motivation for Monte Carlo methods

2. **monte_carlo_integration_convergence.png**
   - Convergence rates for MC integration
   - Use: MC approximation accuracy

3. **law_of_large_numbers_mcmc.png**
   - LLN demonstration for MCMC
   - Use: Theoretical foundation

4. **effective_sample_size_autocorrelation.png**
   - ESS vs autocorrelation relationship
   - Use: Chain efficiency diagnostics

#### MCMC Diagnostics
**Script**: `generate_mcmc_advanced.py`

5. **random_walk_vs_hmc_directed.png**
   - RWM vs HMC comparison
   - Use: Advanced algorithms introduction

6. **acceptance_rate_effects.png**
   - Proposal distribution tuning
   - Use: MCMC optimization

7. **chain_mixing_quality.png**
   - Visual mixing assessment guide
   - Use: Convergence diagnostics teaching

8. **warmup_tuning_phase.png**
   - Adaptive sampling visualization
   - Use: PyMC/Stan workflow explanation

### Regenerate Images

```bash
# All Monte Carlo images
python3 generate_monte_carlo_advanced.py

# All MCMC diagnostic images
python3 generate_mcmc_advanced.py

# Both scripts
python3 generate_monte_carlo_advanced.py && python3 generate_mcmc_advanced.py
```

### Integration Example

```markdown
![Curse of Dimensionality]({{ site.baseurl }}/img/chapter_img/chapter03/curse_of_dimensionality_detailed.png)
```

**Total images in chapter**: 23 (8 new + 15 existing)
