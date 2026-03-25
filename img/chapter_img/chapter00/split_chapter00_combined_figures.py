#!/usr/bin/env python3
"""Split combined lesson figures in chapter00 into standalone panel images."""

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


def detect_shared_header_height(image, threshold=0.02, window=24):
    """Detect a sparse shared title band before the actual panels begin."""
    rgba = np.asarray(image.convert("RGBA"))
    visible_pixels = np.any(rgba[:, :, :3] < 245, axis=2) | (rgba[:, :, 3] < 250)
    row_density = visible_pixels.mean(axis=1)
    rolling_density = np.convolve(row_density, np.ones(window) / window, mode="same")

    candidate_rows = np.where(rolling_density > threshold)[0]
    if candidate_rows.size == 0:
        return 0

    runs = []
    start = candidate_rows[0]
    previous = candidate_rows[0]

    for row in candidate_rows[1:]:
        if row - previous > window:
            runs.append((start, previous))
            start = row
        previous = row
    runs.append((start, previous))

    first_run = runs[0]
    if first_run[0] > image.height * 0.15:
        return max(0, int(first_run[0]) - 8)

    if len(runs) > 1:
        return min(image.height, int(first_run[1]) + 8)

    return max(0, int(first_run[0]) - 8)


def split_grid(filename, rows, cols, outputs, trim_shared_header=False, padding=20):
    """Split a figure into an even grid of panels."""
    if len(outputs) != rows * cols:
        raise ValueError(f"{filename}: outputs must match rows * cols.")

    image = Image.open(BASE_DIR / filename).convert("RGBA")
    if trim_shared_header:
        image = image.crop((0, detect_shared_header_height(image), image.width, image.height))

    cell_width = image.width / cols
    cell_height = image.height / rows

    for index, output_name in enumerate(outputs):
        row, col = divmod(index, cols)
        left = round(col * cell_width)
        upper = round(row * cell_height)
        right = round((col + 1) * cell_width)
        lower = round((row + 1) * cell_height)

        panel = trim_whitespace(image.crop((left, upper, right, lower)), padding=padding).convert("RGB")
        panel.save(BASE_DIR / output_name)
        print(f"  -> {output_name}")


def split_custom_grid(filename, outputs, trim_shared_header=False, padding=20):
    """Split a figure using normalized crop boxes while keeping a grid-like workflow."""
    image = Image.open(BASE_DIR / filename).convert("RGBA")
    if trim_shared_header:
        image = image.crop((0, detect_shared_header_height(image), image.width, image.height))

    for output_name, (x0, y0, x1, y1) in outputs.items():
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


def split_custom_boxes(filename, boxes, trim_shared_header=False, padding=20):
    """Split a figure using normalized crop boxes."""
    image = Image.open(BASE_DIR / filename).convert("RGBA")
    if trim_shared_header:
        image = image.crop((0, detect_shared_header_height(image), image.width, image.height))

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
    grid_jobs = [
        (
            "descriptive_mean_vs_median.png",
            1,
            2,
            [
                "descriptive_mean_median_symmetric.png",
                "descriptive_mean_median_right_skewed.png",
            ],
        ),
        (
            "descriptive_spread_and_boxplot.png",
            1,
            2,
            [
                "descriptive_spread_same_mean_diff_sd.png",
                "descriptive_boxplot_iqr_outliers.png",
            ],
        ),
        (
            "descriptive_correlation_patterns.png",
            1,
            3,
            [
                "descriptive_correlation_linear.png",
                "descriptive_correlation_nonlinear.png",
                "descriptive_correlation_hidden_groups.png",
            ],
        ),
        (
            "effect_size_vs_sample_size.png",
            2,
            1,
            [
                "pvalue_large_n_small_effect.png",
                "pvalue_small_n_large_effect.png",
            ],
        ),
        (
            "pvalue_misinterpretations.png",
            2,
            2,
            [
                "pvalue_misinterpretation_h0_probability.png",
                "pvalue_misinterpretation_small_p_large_effect.png",
                "pvalue_misinterpretation_large_p_h0_true.png",
                "pvalue_misinterpretation_alpha_cutoff.png",
            ],
        ),
        (
            "multiple_testing_problem.png",
            2,
            1,
            [
                "multiple_testing_false_positive_example.png",
                "multiple_testing_uniform_pvalues.png",
            ],
        ),
        (
            "confidence_vs_credible_intervals.png",
            2,
            1,
            [
                "confidence_interval_repeated_experiments.png",
                "credible_interval_single_posterior.png",
            ],
        ),
        (
            "t_value_interpretation.png",
            2,
            2,
            [
                "t_value_small_example.png",
                "t_value_borderline_example.png",
                "t_value_large_example.png",
                "t_value_chocolate_example.png",
            ],
        ),
        (
            "expectation_variance_covariance_visual.png",
            1,
            3,
            [
                "expectation_center_histogram.png",
                "covariance_positive_scatter.png",
                "covariance_negative_scatter.png",
            ],
        ),
        (
            "lln_clt_convergence.png",
            1,
            2,
            [
                "lln_running_mean_convergence.png",
                "clt_sample_means_histogram.png",
            ],
        ),
        (
            "sampling_distribution_standard_error.png",
            1,
            2,
            [
                "sampling_distribution_n20.png",
                "sampling_distribution_n200.png",
            ],
        ),
        (
            "log_probability_numerical_stability.png",
            1,
            2,
            [
                "log_probability_direct_product.png",
                "log_probability_log_sum.png",
            ],
        ),
        (
            "basic_model_assumption_checks.png",
            1,
            2,
            [
                "basic_model_fit_outliers.png",
                "basic_model_residual_check.png",
            ],
        ),
    ]

    for filename, rows, cols, outputs in grid_jobs:
        print(f"Splitting grid: {filename}")
        split_grid(filename, rows, cols, outputs, trim_shared_header=True)

    print("Splitting custom grid: basic_model_assumption_checks.png")
    split_custom_grid(
        "basic_model_assumption_checks.png",
        {
            "basic_model_fit_outliers.png": (0.00, 0.02, 0.50, 1.00),
            "basic_model_residual_check.png": (0.50, 0.02, 1.00, 1.00),
        },
        trim_shared_header=True,
    )

    print("Splitting custom: t_test_types.png")
    split_custom_boxes(
        "t_test_types.png",
        {
            "t_test_type_one_sample.png": (0.02, 0.02, 0.98, 0.32),
            "t_test_type_independent.png": (0.00, 0.405, 0.50, 0.68),
            "t_test_type_paired.png": (0.50, 0.405, 1.00, 0.68),
            "t_test_type_summary_table.png": (0.10, 0.70, 0.90, 1.00),
        },
        trim_shared_header=True,
    )


if __name__ == "__main__":
    main()
