# Chapter 05 - New Visualizations (March 2026)

## Multiple Regression & Causal Inference

This directory contains 3 new visualizations for interaction effects and causal reasoning.

### New Images Added (March 9, 2026)

**Script**: `generate_interactions_causal.py`

1. **three_way_interaction.png**
   - 3-way interaction visualization (X × Z × Group)
   - 2-panel: 3D surface + faceted 2D slices
   - Use: Advanced interaction modeling

2. **continuous_categorical_interaction_advanced.png**
   - Continuous-categorical interaction with uncertainty
   - 3-panel: Data, posterior slopes, predictions with credible intervals
   - Use: Practical interaction interpretation

3. **causal_inference_dags.png**
   - Directed Acyclic Graphs for causal inference
   - 4-panel: Confounder, mediator, collider, M-bias
   - Use: Introduction to causal reasoning

### Regenerate Images

```bash
python3 generate_interactions_causal.py
```

### Integration Example

```markdown
![Three-Way Interaction]({{ site.baseurl }}/img/chapter_img/chapter05/three_way_interaction.png)

![Continuous-Categorical Interaction]({{ site.baseurl }}/img/chapter_img/chapter05/continuous_categorical_interaction_advanced.png)

![Causal DAGs]({{ site.baseurl }}/img/chapter_img/chapter05/causal_inference_dags.png)
```

### DAG Scenarios Explained

1. **Confounder**: Z affects both X and Y → Must control for Z
2. **Mediator**: X → Z → Y → Should NOT control for Z (blocks causal path)
3. **Collider**: X → Z ← Y → Should NOT control for Z (creates spurious association)
4. **M-bias**: Hidden confounder U with observed collider Z → Complex adjustment

**Total images in chapter**: 13 (3 new + 10 existing)
