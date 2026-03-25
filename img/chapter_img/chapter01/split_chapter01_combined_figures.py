#!/usr/bin/env python3
"""Split combined lesson figures in chapter01 into standalone panel images."""

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
    """Detect the sparse title band before the actual panels begin."""
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


def split_grid(filename, rows, cols, outputs, trim_shared_header=True, padding=20):
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


def split_rows(filename, outputs, trim_shared_header=True, padding=20):
    """Split a figure into evenly sized horizontal bands."""
    split_grid(filename, len(outputs), 1, outputs, trim_shared_header=trim_shared_header, padding=padding)


def split_cols(filename, outputs, trim_shared_header=True, padding=20):
    """Split a figure into evenly sized vertical bands."""
    split_grid(filename, 1, len(outputs), outputs, trim_shared_header=trim_shared_header, padding=padding)


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
        "pvalue_misconceptions.png": {
            "chapter01_pvalue_misconception_h0_probability.png": (0.00, 0.06, 0.50, 0.38),
            "chapter01_pvalue_misconception_one_minus_p.png": (0.50, 0.06, 1.00, 0.38),
            "chapter01_pvalue_misconception_alpha_threshold.png": (0.00, 0.36, 0.50, 0.69),
            "chapter01_pvalue_misconception_effect_size.png": (0.50, 0.36, 1.00, 0.69),
            "chapter01_pvalue_misconception_large_p_no_effect.png": (0.00, 0.67, 0.50, 1.00),
            "chapter01_pvalue_misconception_summary.png": (0.50, 0.67, 1.00, 1.00),
        },
        "bayesian_daily_life.png": {
            "chapter01_bayesian_daily_life_night_noise.png": (0.00, 0.06, 0.50, 0.50),
            "chapter01_bayesian_daily_life_restaurant.png": (0.50, 0.06, 1.00, 0.50),
            "chapter01_bayesian_daily_life_weather.png": (0.00, 0.50, 0.50, 1.00),
            "chapter01_bayesian_daily_life_medical.png": (0.50, 0.50, 1.00, 1.00),
        },
        "bayes_theorem_visualization.png": {
            "chapter01_bayes_theorem_prior.png": (0.00, 0.05, 0.50, 0.49),
            "chapter01_bayes_theorem_likelihood.png": (0.50, 0.05, 1.00, 0.49),
            "chapter01_bayes_theorem_posterior.png": (0.00, 0.51, 0.50, 1.00),
            "chapter01_bayes_theorem_prior_vs_posterior.png": (0.50, 0.51, 1.00, 1.00),
        },
        "sequential_updating.png": {
            "chapter01_sequential_updating_prior.png": (0.00, 0.02, 0.50, 0.50),
            "chapter01_sequential_updating_step1.png": (0.50, 0.02, 1.00, 0.50),
            "chapter01_sequential_updating_step2.png": (0.00, 0.50, 0.50, 1.00),
            "chapter01_sequential_updating_batch_comparison.png": (0.50, 0.50, 1.00, 1.00),
        },
        "prior_strength_comparison.png": {
            "chapter01_prior_strength_weak_prior.png": (0.00, 0.00, 0.50, 0.50),
            "chapter01_prior_strength_strong_prior.png": (0.50, 0.00, 1.00, 0.50),
            "chapter01_prior_strength_weak_posterior.png": (0.00, 0.50, 0.50, 1.00),
            "chapter01_prior_strength_strong_posterior.png": (0.50, 0.50, 1.00, 1.00),
        },
        "doctor_diagnosis_bayes.png": {
            "chapter01_doctor_diagnosis_symptoms.png": (0.00, 0.06, 0.50, 0.50),
            "chapter01_doctor_diagnosis_prior.png": (0.50, 0.06, 1.00, 0.50),
            "chapter01_doctor_diagnosis_new_data.png": (0.00, 0.50, 0.50, 1.00),
            "chapter01_doctor_diagnosis_posterior.png": (0.50, 0.50, 1.00, 1.00),
        },
        "pvalue_vs_posterior_probability.png": {
            "chapter01_pvalue_vs_posterior_frequentist.png": (0.00, 0.00, 1.00, 0.50),
            "chapter01_pvalue_vs_posterior_bayesian.png": (0.00, 0.50, 1.00, 1.00),
        },
        "clinical_trial_comparison.png": {
            "chapter01_clinical_trial_frequentist.png": (0.00, 0.06, 1.00, 0.51),
            "chapter01_clinical_trial_bayesian.png": (0.00, 0.49, 1.00, 1.00),
        },
        "frequentist_vs_bayesian_comparison.png": {
            "chapter01_frequentist_vs_bayesian_frequentist.png": (0.00, 0.05, 0.50, 1.00),
            "chapter01_frequentist_vs_bayesian_bayesian.png": (0.50, 0.05, 1.00, 1.00),
        },
        "frequentist_vs_bayesian_philosophy.png": {
            "chapter01_philosophy_frequentist.png": (0.00, 0.04, 0.50, 1.00),
            "chapter01_philosophy_bayesian.png": (0.50, 0.04, 1.00, 1.00),
        },
        "coin_flip_comparison.png": {
            "chapter01_coin_flip_frequentist.png": (0.00, 0.05, 0.50, 1.00),
            "chapter01_coin_flip_bayesian.png": (0.50, 0.05, 1.00, 1.00),
        },
    }

    for filename, boxes in custom_jobs.items():
        print(f"Splitting custom: {filename}")
        split_custom_boxes(filename, boxes)


if __name__ == "__main__":
    main()
