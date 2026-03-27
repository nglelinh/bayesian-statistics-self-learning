#!/usr/bin/env python3
"""Split combined lesson figures in chapter05 into standalone panel images."""

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


def make_grid_boxes(names, rows, cols, top=0.0, bottom=1.0, left=0.0, right=1.0):
    """Create normalized crop boxes for a regular grid in row-major order."""
    if len(names) != rows * cols:
        raise ValueError("Number of output names must equal rows * cols")

    boxes = {}
    x_edges = np.linspace(left, right, cols + 1)
    y_edges = np.linspace(top, bottom, rows + 1)

    index = 0
    for row in range(rows):
        for col in range(cols):
            boxes[names[index]] = (
                float(x_edges[col]),
                float(y_edges[row]),
                float(x_edges[col + 1]),
                float(y_edges[row + 1]),
            )
            index += 1

    return boxes


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
        "multiple_predictors_visualization.png": make_grid_boxes(
            [
                "chapter05_weight_vs_height_colored_by_age.png",
                "chapter05_weight_vs_age_colored_by_height.png",
                "chapter05_weight_height_age_3d.png",
            ],
            1,
            3,
        ),
        "confounding_dags.png": make_grid_boxes(
            [
                "chapter05_confounding_dag_overview.png",
                "chapter05_simpsons_paradox_overview.png",
                "chapter05_collider_bias_overview.png",
                "chapter05_mediation_overview.png",
            ],
            2,
            2,
            top=0.08,
        ),
        "causal_basic_structures.png": make_grid_boxes(
            [
                "chapter05_fork_structure.png",
                "chapter05_chain_structure.png",
                "chapter05_collider_structure.png",
            ],
            1,
            3,
            top=0.08,
        ),
        "simpsons_paradox.png": make_grid_boxes(
            [
                "chapter05_simpsons_aggregate_bias.png",
                "chapter05_simpsons_stratified_effect.png",
            ],
            1,
            2,
        ),
        "simpsons_paradox_dag.png": make_grid_boxes(
            [
                "chapter05_simpsons_dag_unadjusted.png",
                "chapter05_simpsons_dag_adjusted.png",
            ],
            1,
            2,
            top=0.08,
        ),
        "backdoor_paths_examples.png": make_grid_boxes(
            [
                "chapter05_backdoor_simple.png",
                "chapter05_backdoor_multiple.png",
                "chapter05_backdoor_blocked_by_collider.png",
                "chapter05_backdoor_m_bias.png",
            ],
            2,
            2,
            top=0.08,
        ),
        "adjustment_sets_comparison.png": make_grid_boxes(
            [
                "chapter05_adjustment_valid_z1_z2.png",
                "chapter05_adjustment_valid_but_mediator.png",
                "chapter05_adjustment_invalid_collider.png",
                "chapter05_adjustment_invalid_none.png",
            ],
            2,
            2,
            top=0.08,
        ),
        "collider_bias_berkson.png": make_grid_boxes(
            [
                "chapter05_collider_general_population.png",
                "chapter05_collider_conditioned_sample.png",
            ],
            1,
            2,
            top=0.08,
        ),
        "multicollinearity_demo.png": make_grid_boxes(
            [
                "chapter05_multicollinearity_predictor_correlation.png",
                "chapter05_multicollinearity_both_predict_y.png",
                "chapter05_multicollinearity_problem_summary.png",
            ],
            1,
            3,
        ),
        "multicollinearity_effects.png": make_grid_boxes(
            [
                "chapter05_low_predictor_correlation.png",
                "chapter05_high_predictor_correlation.png",
                "chapter05_low_correlation_posterior.png",
                "chapter05_high_correlation_posterior.png",
            ],
            2,
            2,
            top=0.08,
        ),
        "interaction_effects.png": make_grid_boxes(
            [
                "chapter05_no_interaction_parallel_lines.png",
                "chapter05_with_interaction_different_slopes.png",
                "chapter05_interaction_model_comparison.png",
                "chapter05_interaction_continuous_lines.png",
            ],
            2,
            2,
            top=0.08,
        ),
        "interaction_demo.png": make_grid_boxes(
            [
                "chapter05_additive_model_demo.png",
                "chapter05_interactive_model_demo.png",
            ],
            1,
            2,
        ),
        "conditional_effects.png": make_grid_boxes(
            [
                "chapter05_conditional_effects_by_group.png",
                "chapter05_interaction_difference_distribution.png",
            ],
            1,
            2,
        ),
        "continuous_interaction.png": make_grid_boxes(
            [
                "chapter05_continuous_interaction_3d.png",
                "chapter05_continuous_interaction_contour.png",
            ],
            1,
            2,
        ),
    }

    for filename, boxes in custom_jobs.items():
        print(f"Splitting custom: {filename}")
        split_custom_boxes(filename, boxes)


if __name__ == "__main__":
    main()
