#!/usr/bin/env python3
"""Split combined lesson figures in chapter02 into standalone panel images."""

from pathlib import Path

import numpy as np
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent


def trim_whitespace(image, padding=20, threshold=245):
    """Trim outer whitespace while keeping a small visual margin."""
    rgba = np.asarray(image.convert("RGBA"))
    visible_pixels = np.any(rgba[:, :, :3] < threshold, axis=2) | (rgba[:, :, 3] < 250)
    coordinates = np.argwhere(visible_pixels)

    if coordinates.size == 0:
        return image

    y0, x0 = coordinates.min(axis=0)
    y1, x1 = coordinates.max(axis=0) + 1

    x0 = max(0, x0 - padding)
    y0 = max(0, y0 - padding)
    x1 = min(image.width, x1 + padding)
    y1 = min(image.height, y1 + padding)

    return image.crop((x0, y0, x1, y1))


def split_custom_boxes(filename, boxes, padding=20):
    """Split a figure using normalized crop boxes."""
    image = Image.open(BASE_DIR / filename).convert("RGBA")

    for output_name, (x0, y0, x1, y1) in boxes.items():
        crop = image.crop(
            (
                round(x0 * image.width),
                round(y0 * image.height),
                round(x1 * image.width),
                round(y1 * image.height),
            )
        )
        panel = trim_whitespace(crop, padding=padding).convert("RGB")
        panel.save(BASE_DIR / output_name)
        print(f"  -> {output_name}")


def main():
    custom_jobs = {
        "narrow_vs_wide.png": {
            "chapter02_narrow_distribution.png": (0.00, 0.05, 0.50, 1.00),
            "chapter02_wide_distribution.png": (0.50, 0.05, 1.00, 1.00),
        },
        "likelihood_vs_probability_concept.png": {
            "chapter02_likelihood_concept.png": (0.00, 0.05, 0.50, 1.00),
            "chapter02_posterior_probability_concept.png": (0.50, 0.05, 1.00, 1.00),
        },
        "likelihood_log_likelihood_comparison.png": {
            "chapter02_likelihood_curve_large_n.png": (0.00, 0.00, 0.50, 1.00),
            "chapter02_log_likelihood_curve_large_n.png": (0.50, 0.00, 1.00, 1.00),
        },
        "three_priors.png": {
            "chapter02_prior_flat_uniform.png": (0.00, 0.00, 0.50, 0.50),
            "chapter02_prior_centered_half.png": (0.50, 0.00, 1.00, 0.50),
            "chapter02_prior_centered_low_moderate.png": (0.00, 0.50, 0.50, 1.00),
            "chapter02_prior_centered_low_strong.png": (0.50, 0.50, 1.00, 1.00),
        },
        "prior_regularization_small_data.png": {
            "chapter02_prior_regularization_likelihood.png": (0.00, 0.00, 0.3334, 1.00),
            "chapter02_prior_regularization_prior.png": (0.3333, 0.00, 0.6667, 1.00),
            "chapter02_prior_regularization_posterior.png": (0.6666, 0.00, 1.00, 1.00),
        },
        "posterior_probability_calculations.png": {
            "chapter02_posterior_probability_interval.png": (0.00, 0.00, 0.3334, 1.00),
            "chapter02_posterior_probability_above_half.png": (0.3333, 0.00, 0.6667, 1.00),
            "chapter02_posterior_probability_above_eighty.png": (0.6666, 0.00, 1.00, 1.00),
        },
        "posterior_credible_intervals.png": {
            "chapter02_credible_interval_95.png": (0.00, 0.00, 0.50, 1.00),
            "chapter02_credible_interval_90.png": (0.50, 0.00, 1.00, 1.00),
        },
        "sequential_updating.png": {
            "chapter02_sequential_update_step1.png": (0.00, 0.07, 0.50, 0.53),
            "chapter02_sequential_update_step2.png": (0.50, 0.07, 1.00, 0.53),
            "chapter02_sequential_update_step3.png": (0.00, 0.53, 0.50, 1.00),
            "chapter02_sequential_update_step4.png": (0.50, 0.53, 1.00, 1.00),
        },
        "gamma_poisson_conjugacy_detailed.png": {
            "chapter02_gamma_poisson_prior_posterior.png": (0.00, 0.00, 0.50, 0.50),
            "chapter02_gamma_poisson_formula_summary.png": (0.50, 0.00, 1.00, 0.50),
            "chapter02_gamma_poisson_posterior_predictive.png": (0.00, 0.50, 0.50, 1.00),
            "chapter02_gamma_poisson_sequential_updates.png": (0.50, 0.50, 1.00, 1.00),
        },
        "normal_normal_conjugacy_detailed.png": {
            "chapter02_normal_normal_prior_posterior.png": (0.00, 0.00, 0.50, 0.50),
            "chapter02_normal_normal_formula_summary.png": (0.50, 0.00, 1.00, 0.50),
            "chapter02_normal_normal_sample_size_effect.png": (0.00, 0.50, 0.50, 1.00),
            "chapter02_normal_normal_prior_data_weights.png": (0.50, 0.50, 1.00, 1.00),
        },
        "conjugate_prior_limitations.png": {
            "chapter02_conjugate_limit_truncated_prior.png": (0.00, 0.00, 0.50, 0.50),
            "chapter02_conjugate_limit_overview.png": (0.50, 0.00, 1.00, 0.50),
            "chapter02_conjugate_limit_mixture_prior.png": (0.00, 0.50, 0.50, 1.00),
            "chapter02_conjugate_limit_decision_tree.png": (0.50, 0.50, 1.00, 1.00),
        },
        "grid_approximation_basics.png": {
            "chapter02_grid_resolution_5.png": (0.00, 0.00, 0.3334, 0.50),
            "chapter02_grid_resolution_20.png": (0.3333, 0.00, 0.6667, 0.50),
            "chapter02_grid_resolution_100.png": (0.6666, 0.00, 1.00, 0.50),
            "chapter02_grid_vs_exact_5.png": (0.00, 0.50, 0.3334, 1.00),
            "chapter02_grid_vs_exact_20.png": (0.3333, 0.50, 0.6667, 1.00),
            "chapter02_grid_vs_exact_100.png": (0.6666, 0.50, 1.00, 1.00),
        },
        "grid_statistics_computation.png": {
            "chapter02_grid_stat_mean_median_mode.png": (0.00, 0.00, 0.50, 0.50),
            "chapter02_grid_stat_credible_interval.png": (0.50, 0.00, 1.00, 0.50),
            "chapter02_grid_stat_interval_probability.png": (0.00, 0.50, 0.50, 1.00),
            "chapter02_grid_stat_sampling.png": (0.50, 0.50, 1.00, 1.00),
        },
        "grid_posterior_predictive.png": {
            "chapter02_grid_predictive_distribution.png": (0.00, 0.00, 0.50, 1.00),
            "chapter02_grid_predictive_vs_exact.png": (0.50, 0.00, 1.00, 1.00),
        },
        "curse_of_dimensionality.png": {
            "chapter02_grid_dimensionality_growth.png": (0.00, 0.00, 0.50, 1.00),
            "chapter02_grid_dimensionality_table.png": (0.50, 0.00, 1.00, 1.00),
        },
    }

    for filename, boxes in custom_jobs.items():
        print(f"Splitting custom: {filename}")
        split_custom_boxes(filename, boxes)


if __name__ == "__main__":
    main()
