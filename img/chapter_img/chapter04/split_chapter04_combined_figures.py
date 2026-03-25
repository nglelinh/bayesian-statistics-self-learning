#!/usr/bin/env python3
"""Split combined lesson figures in chapter04 into standalone panel images."""

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
        "frequentist_vs_bayesian_regression.png": {
            "chapter04_frequentist_point_estimate.png": (0.00, 0.00, 0.50, 1.00),
            "chapter04_bayesian_uncertainty_quantification.png": (0.50, 0.00, 1.00, 1.00),
        },
        "regression_generative_story.png": {
            "chapter04_regression_data_generating_process.png": (0.00, 0.00, 0.50, 0.50),
            "chapter04_regression_story_summary.png": (0.50, 0.00, 1.00, 0.50),
            "chapter04_regression_distribution_fixed_height.png": (0.00, 0.50, 0.50, 1.00),
            "chapter04_regression_residual_distribution.png": (0.50, 0.50, 1.00, 1.00),
        },
        "regression_parameter_interpretation.png": {
            "chapter04_intercept_after_centering.png": (0.00, 0.00, 0.3334, 1.00),
            "chapter04_slope_interpretation.png": (0.3333, 0.00, 0.6667, 1.00),
            "chapter04_noise_interpretation.png": (0.6666, 0.00, 1.00, 1.00),
        },
        "standardization_comparison.png": {
            "chapter04_standardization_raw_data.png": (0.00, 0.00, 0.50, 1.00),
            "chapter04_standardization_standardized_data.png": (0.50, 0.00, 1.00, 1.00),
        },
        "prior_intercept_comparison.png": {
            "chapter04_prior_intercept_too_wide.png": (0.00, 0.00, 0.3334, 1.00),
            "chapter04_prior_intercept_weakly_informative.png": (0.3333, 0.00, 0.6667, 1.00),
            "chapter04_prior_intercept_too_narrow.png": (0.6666, 0.00, 1.00, 1.00),
        },
        "prior_slope_comparison.png": {
            "chapter04_prior_slope_too_wide.png": (0.00, 0.00, 0.3334, 1.00),
            "chapter04_prior_slope_weakly_informative.png": (0.3333, 0.00, 0.6667, 1.00),
            "chapter04_prior_slope_too_narrow.png": (0.6666, 0.00, 1.00, 1.00),
        },
        "prior_noise_halfnormal.png": {
            "chapter04_prior_noise_halfnormal_curve.png": (0.00, 0.00, 0.50, 1.00),
            "chapter04_prior_noise_halfnormal_summary.png": (0.50, 0.00, 1.00, 1.00),
        },
        "prior_predictive_slopes.png": {
            "chapter04_prior_predictive_weakly_informative.png": (0.00, 0.00, 0.50, 1.00),
            "chapter04_prior_predictive_too_wide.png": (0.50, 0.00, 1.00, 1.00),
        },
        "prior_sensitivity_analysis.png": {
            "chapter04_prior_sensitivity_posterior_overlay.png": (0.00, 0.00, 0.50, 1.00),
            "chapter04_prior_sensitivity_summary.png": (0.50, 0.00, 1.00, 1.00),
        },
        "posterior_predictive_checks.png": {
            "chapter04_ppc_observed_vs_predicted.png": (0.00, 0.08, 0.3334, 0.56),
            "chapter04_ppc_distribution_at_x5.png": (0.3333, 0.08, 0.6667, 0.56),
            "chapter04_ppc_test_stat_mean.png": (0.6666, 0.08, 1.00, 0.56),
            "chapter04_ppc_residual_distribution.png": (0.00, 0.52, 0.3334, 1.00),
            "chapter04_ppc_variance_check.png": (0.3333, 0.52, 0.6667, 1.00),
            "chapter04_ppc_summary.png": (0.6666, 0.52, 1.00, 1.00),
        },
        "regression_assumptions_diagnostic.png": {
            "chapter04_good_model_scatter.png": (0.00, 0.08, 0.25, 0.40),
            "chapter04_bad_nonlinearity_scatter.png": (0.25, 0.08, 0.50, 0.40),
            "chapter04_bad_heteroskedasticity_scatter.png": (0.50, 0.08, 0.75, 0.40),
            "chapter04_bad_nonnormal_scatter.png": (0.75, 0.08, 1.00, 0.40),
            "chapter04_good_model_residuals.png": (0.00, 0.36, 0.25, 0.70),
            "chapter04_bad_nonlinearity_residuals.png": (0.25, 0.36, 0.50, 0.70),
            "chapter04_bad_heteroskedasticity_residuals.png": (0.50, 0.36, 0.75, 0.70),
            "chapter04_bad_nonnormal_residuals.png": (0.75, 0.36, 1.00, 0.70),
            "chapter04_good_model_qq.png": (0.00, 0.66, 0.25, 1.00),
            "chapter04_bad_nonlinearity_qq.png": (0.25, 0.66, 0.50, 1.00),
            "chapter04_bad_heteroskedasticity_qq.png": (0.50, 0.66, 0.75, 1.00),
            "chapter04_bad_nonnormal_qq.png": (0.75, 0.66, 1.00, 1.00),
        },
    }

    for filename, boxes in custom_jobs.items():
        print(f"Splitting custom: {filename}")
        split_custom_boxes(filename, boxes)


if __name__ == "__main__":
    main()
