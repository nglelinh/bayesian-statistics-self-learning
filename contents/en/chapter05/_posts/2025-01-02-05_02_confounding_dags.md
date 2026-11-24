---
layout: post
title: "Lesson 5.2: Confounding and DAGs - Causal Inference Basics"
chapter: '05'
order: 2
owner: Nguyen Le Linh
lang: en
categories:
- chapter05
lesson_type: required
---

Here is one of the most famous traps in data science: a hospital records data on mild and severe patients and discovers that **patients who receive Treatment T have *lower* survival rates than untreated patients**—yet when you stratify by disease severity, Treatment T *improves* survival in both mild and severe patients! Worse still, in a different causal structure (a **collider**), throwing *every* available column into your regression can manufacture a completely fake causal effect even when the true effect is zero!

**Directed Acyclic Graphs (DAGs)**—pioneered by Judea Pearl and popularized in Bayesian data analysis by Richard McElreath—give you a crystal-clear graphical grammar for causal inference: **forks** (confounders you *must* control for), **pipes** (mediators), and **colliders** (traps you must *never* condition on!).

---

## Background Knowledge Map: The Four Elemental Causal Structures in DAGs

Every complex causal web reduces to combinations of four 3-node junctions:

1. **The Fork (Confounder: $$X \leftarrow Z \rightarrow Y$$):** Common cause $$Z$$ creates a non-causal "backdoor" path between $$X$$ and $$Y$$. **Rule:** Conditioning on $$Z$$ *closes* the backdoor and removes confounding bias!
2. **The Pipe (Mediator: $$X \rightarrow Z \rightarrow Y$$):** $$X$$ causes $$Y$$ *through* $$Z$$. **Rule:** Conditioning on $$Z$$ blocks the causal path—do *not* control for a post-treatment mediator if you want the **total** causal effect of $$X$$ on $$Y$$!
3. **The Collider (Common Effect: $$X \rightarrow Z \leftarrow Y$$):** $$X$$ and $$Y$$ are initially independent, yet both cause $$Z$$. **Rule:** Conditioning on $$Z$$ *opens* a spurious path (**collider / Berkson’s bias**) — **NEVER** control for a collider!
4. **The Backdoor Criterion:** To identify the causal effect of $$X$$ on $$Y$$ from observational data, choose an adjustment set $$S$$ that blocks every backdoor path into $$X$$ while containing no descendants of $$X$$.

---

## Learning objectives

After this lesson, you need to understand what confounding is and why it makes us misread data. You also need to know that a DAG is a tool for thinking about causal relationships, from which you decide when to adjust for a variable and when not to. This is the foundation of causal inference.

> **Mini example.** A hospital sees that patients given stronger treatment have a lower recovery rate. The conclusion "stronger treatment makes everything worse" sounds very plausible, but it can be completely wrong if severe cases were already given stronger treatment to begin with. The severity of the illness at admission may be the confounding variable.
>
> **Quick check.** If a variable affects both the treatment and the outcome, what can happen if we ignore it?

## 1. How does correlation differ from causation?

In real data, two variables going together do not necessarily have a direct causal relationship.

A very famous example is that ice cream sales rise in summer, and the number of drowning incidents also rises in summer. This does not mean ice cream causes drowning; both rise because of **hot weather**. The problem here is that we see a correlation but do not see the structure that produces it.

Confounding is one of the most common reasons we mistake correlation for causation.

## 2. What is a confounder?

A variable is called a **confounder** if it affects the predictor or treatment $$X$$, and also affects the outcome $$Y$$, but does not lie on the causal path from $$X$$ to $$Y$$.

### Example 1: coffee and heart disease

Suppose we observe that people who drink a lot of coffee have a higher risk of heart disease. We might hastily conclude that coffee is the culprit. But if more stressed people both drink more coffee and have a higher cardiovascular risk, then **stress** may be the confounder.

### Example 2: extra tutoring and exam scores

If weak students tend to attend more tutoring, while exam results depend strongly on initial ability, then **entry level** is a confounder when we study the effectiveness of tutoring.

![Confounding overview diagram]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_confounding_dag_overview.png)

The key point is that confounding creates an extra line of association between $$X$$ and $$Y$$. If it is not handled, we easily attribute the confounder's effect to the treatment's effect.

## 3. What is a DAG and why is it useful?

**DAG** stands for *Directed Acyclic Graph*, which can be understood as a directed graph with no cycles. More specifically, *Directed* means the arrows have direction, *Acyclic* means there are no closed loops, and *Graph* means a diagram representing relationships between variables.

A DAG helps us answer a very practical question:

> In this causal question, which variables should go into the model, and which should not?

Instead of rushing into running a regression, we draw the story first.

## 4. Three basic structures to remember

Most complex DAGs are assembled from the following three basic structures.

### 4.1. Fork: a common cause

$$
Z \rightarrow X,\quad Z \rightarrow Y
$$

This is the structure of confounding.

For example, age affects the level of exercise and also affects blood pressure. If we want to study how exercise affects blood pressure, **age** is a variable that should be adjusted for.

![Fork structure: a common cause creating confounding]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_fork_structure.png)

### 4.2. Chain: a mediating variable

$$
X \rightarrow M \rightarrow Y
$$

This is a mediator. For example, exercise lowers weight, and weight loss in turn helps improve blood sugar.

If we want to measure the **total effect** of exercise on blood sugar, we should not adjust for weight, because that blocks part of the true pathway of influence.

![Chain structure: the mediator lies on the path of influence]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_chain_structure.png)

![Overview of mediation in a causal story]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_mediation_overview.png)

### 4.3. Collider: two arrows pointing into one node

$$
X \rightarrow C \leftarrow Y
$$

A collider is dangerous because when we condition on it, we can create a spurious correlation.

For example, ability and luck both affect being hired; if we look only at the group that was hired, we may see that people who are "less lucky" are often "very good", and vice versa.

That is not a true law of the whole population, but a consequence of looking only at the collider.

![Collider structure: conditioning can open up a spurious correlation]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_collider_structure.png)

![Overview of collider bias in a causal diagram]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_collider_bias_overview.png)

### Experiment: a confounder biases the coefficient and adjusting for Z fixes it

Simulate the fork Z → X, Z → Y: the naive estimate, stratification (Simpson's paradox), then regression with Z.

<div class="interactive-demo" markdown="1">
<div data-demo="confound-explainer" data-lang="en" data-tab="fork"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 5. Practical rule: should we control or not?

A short memory aid is: **do control for confounders**, **do not control for mediators if the goal is the total effect**, and **do not control for colliders**. This rule sounds simple, but applying it correctly requires a sufficiently clear causal diagram.

## 6. Simpson's Paradox: an example that makes many people change how they think

![Quick illustration of Simpson's Paradox]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_paradox_overview.png)

![Aggregated data produces a wrong conclusion about the treatment]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_aggregate_bias.png)

![Splitting by severity shows the true effect of the treatment]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_stratified_effect.png)

Simpson's Paradox occurs when looking at the whole data shows one trend, but when split by an important group that trend reverses. For example in medicine, looking at the whole, the group given aggressive treatment seems to recover worse, but when patients are split by severity, within each severity group aggressive treatment is better. The reason is that severe cases were given stronger treatment, while those same severe cases were also harder to recover to begin with.

The variable "severity" distorted the treatment-outcome relationship when it was ignored.

![DAG of Simpson's Paradox before adjusting for the confounder]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_dag_unadjusted.png)

![DAG after adjusting for severity to reveal the causal effect]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_dag_adjusted.png)

This is a very good example to remind ourselves that:

> aggregated data can tell a wrong story if we do not separate the right structure.

### 6.1. A very short table to see this paradox

Suppose a hospital has two treatment levels, **aggressive treatment** and **standard treatment**, and patients are divided into two groups, **severe cases** and **mild cases**:

| Patient group | Aggressive treatment | Standard treatment |
|---|---:|---:|
| Severe cases | 24/80 recovered = 30% | 6/30 recovered = 20% |
| Mild cases | 54/60 recovered = 90% | 144/180 recovered = 80% |

Within **each severity group**, aggressive treatment is better.

But if we pool all patients together:

- aggressive treatment: $$78/140 \approx 55.7\%$$ recovered,
- standard treatment: $$150/210 \approx 71.4\%$$ recovered.

Looking at the whole, aggressive treatment seems worse. The reason is not that the treatment harms patients, but that the aggressive-treatment group contains a larger share of severe cases. This is a very intuitive way to see how confounding can reverse the story.

## 7. What is a backdoor path?

A **backdoor path** can be understood as a non-causal path linking the treatment $$X$$ to the outcome $$Y$$ through common causes. The goal of adjustment is to block the backdoor paths that need blocking, but not to block the true causal path of influence from $$X$$ to $$Y$$.

The examples below show that a backdoor path can be simple, have multiple branches, be blocked already by a collider, or be opened by mistake through M-bias.

![Simple backdoor path example]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_backdoor_simple.png)

![Example with multiple backdoor paths that must be blocked at the same time]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_backdoor_multiple.png)

![Backdoor path naturally blocked by a collider]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_backdoor_blocked_by_collider.png)

![M-bias: wrong adjustment can open a backdoor path]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_backdoor_m_bias.png)

For example, if we want to know how extra tutoring $$X$$ affects exam scores $$Y$$, while initial ability $$Z$$ affects both attending tutoring and exam scores, then the path $$X \leftarrow Z \rightarrow Y$$ is a backdoor path. Adjusting for $$Z$$ helps block this path.

## 8. How do sufficient adjustment and wrong adjustment differ?

Comparing the four adjustment set choices below will help clearly show the difference between sufficient adjustment, adjustment that loses mediation, adjusting for a collider, and not adjusting at all.

![Valid adjustment set blocks the backdoor paths that need blocking]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_adjustment_valid_z1_z2.png)

![Valid adjustment set but only the direct effect remains]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_adjustment_valid_but_mediator.png)

![Wrong adjustment set because it adjusts for a collider]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_adjustment_invalid_collider.png)

![No adjustment leaves the backdoor paths open]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_adjustment_invalid_none.png)

A **valid adjustment set** is a set of variables that blocks all the backdoor paths that need blocking, does not open new wrong paths, and does not accidentally block the part of the effect that we want to measure. Therefore, we do not need to adjust for "as many as possible"; what matters is to adjust for the **right variables**.

### A real-world example

In a study of the effect of exercise on cardiovascular health, **age** and **eating habits** may be confounders, **current weight** may be a mediator, and the **number of hospital admissions** may be a collider if it is both influenced by health and related to the likelihood of being medically monitored. If we stuff everything into one model without thinking, we can easily create bias ourselves.

A more practical way to put it is:

- if the goal is the **total effect** of exercise on cardiovascular health, we usually want to adjust for `age` and `eating habits`,
- but we should not rush to adjust for `current weight` if weight is itself part of the pathway through which exercise has its effect,
- and we certainly should not add `number of hospital admissions` just because "the data is there", if this variable plays the role of a collider.

The important point is that a good adjustment set must come from the causal story, not from the habit of stuffing every data column into the model.

## 9. Collider bias: a very common mistake when "controlling for everything"

![In the general population, the two causes of a collider can be independent]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_collider_general_population.png)

![When conditioning on the collider, a spurious correlation appears]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_collider_conditioned_sample.png)

Collider bias often appears when we look only at a selected group.

For example, ability and luck both affect being admitted to a highly competitive company. In the general population, ability and luck may be unrelated, but in the group that was admitted, less lucky people usually have to be better to still get in.

The result is that we see a spurious negative correlation between ability and luck in the selected group.

A very important lesson:

> Adding any variable to the model does not necessarily make the analysis better.

### Experiment: conditioning on a collider creates a spurious correlation

X and Y are independent but both point into C; just filtering on C makes them negatively correlated.

<div class="interactive-demo" markdown="1">
<div data-demo="confound-explainer" data-lang="en" data-tab="collider"></div>
</div>

## 10. A very practical DAG workflow

When facing a causal question, you can follow the four fairly practical steps below.

### Step 1. Define the question

First, determine whether you are asking about the effect of $$X$$ on $$Y$$, or simply want to predict $$Y$$. If the goal is causal, the DAG becomes especially important.

### Step 2. List the relevant variables

At the variable-listing step, think in everyday language: what affects the treatment, what affects the outcome, what lies between the treatment and the outcome, and what is the common result of two different things.

### Step 3. Draw the arrows according to the real story

There is no need to draw beautifully from the start. What matters is to draw the correct domain intuition.

### Step 4. Decide the adjustment set

At the final step, ask yourself which variables need to be adjusted for to block backdoor paths, and which must not be adjusted for because they are actually mediators or colliders.

## 11. An interactive tool for practicing DAGs

You can use the website's DAG Explorer tool to draw the situations in this lesson yourself:

**[Open the Interactive DAG Explorer]({{ site.baseurl }}/tools/dag-explorer/standalone.html){:target="_blank"}**

A suggestion is to draw the ice cream and drowning example, the extra tutoring and exam scores example, the exercise - weight loss - health example, and then try changing one variable from confounder to collider to see how the logic changes.

## 12. The most important point of this lesson

Confounding is not a minor technical error. It is the central problem of every analysis that wants to talk about causes.

If we do not think causally first, the regression can run beautifully, the interval can look very convincing, but the final conclusion is still wrong.

> **3 key ideas.** A confounder is a variable that affects both the treatment and the outcome, so if we ignore it we easily misestimate the effect we care about; a DAG is a tool for drawing the causal structure before running the model, so that we can decide which variables should and should not be adjusted for; and we should not "control for everything", because confounders usually need adjustment, while mediators and colliders must be handled carefully depending on the question.

---

### Worked Numerical Example: Seeing Collider Bias Appear Out of Thin Air (4 Actors)

Suppose **Acting Talent ($$X \in \{0,1\}$$)** and **Looks ($$Y \in \{0,1\}$$)** are completely **independent** in the general population (each 50%, so 4 equally likely combinations of 25% each), and Hollywood casts anyone with *either* high talent *or* great looks (**Fame $$Z = 1 \iff X=1 \text{ or } Y=1$$**):

| Talent ($$X$$) | Looks ($$Y$$) | Population Share | Famous ($$Z=1$$)? |
| :--- | :--- | :--- | :--- |
| $$1$$ (High) | $$1$$ (High) | $$25\%$$ | **Yes** |
| $$1$$ (High) | $$0$$ (Low) | $$25\%$$ | **Yes** |
| $$0$$ (Low) | $$1$$ (High) | $$25\%$$ | **Yes** |
| $$0$$ (Low) | $$0$$ (Low) | $$25\%$$ | No (excluded!) |

- **In the full population (unconditioned):** $$P(X=1 \mid Y=1) = 50\% = P(X=1)$$ (zero correlation!).
- **Conditioned on being Famous ($$Z = 1$$, the top 3 rows):**
  - If a famous actor has High Looks ($$Y=1$$, rows 1 & 3): $$P(X=1 \mid Y=1, Z=1) = \mathbf{50\%}$$.
  - If a famous actor has Low Looks ($$Y=0$$, row 2 only!): $$P(X=1 \mid Y=0, Z=1) = \mathbf{100\%}$$!
  Conditioning on the collider $$Z$$ created a **strong negative correlation** between Talent and Looks where none existed in reality!

### Deep-Dive Explanation: Four Causal Rules Before Running Any Observational Regression (Read Slowly)

1. **Draw the DAG *before* choosing regression predictors:** Data alone cannot tell a Fork from a Pipe or a Collider—causal structure comes from domain science!
2. **Stop calling every regression coefficient a "causal effect":** Only variables whose backdoor paths are properly closed have causal interpretations (avoid the *Table 2 Fallacy* of reading all covariates in one model as causal!).
3. **Never throw "all available columns" into a causal regression ("causal salad"):** Including a collider or post-treatment variable actively *destroys* causal identification.
4. **Use `dagitty` or the backdoor rule to verify your adjustment set:** Even a 5-node DAG can hide subtle backdoor paths that human intuition misses.

**Quick check.** You want to estimate the **total** causal effect of a new fertilizer ($$X$$) on crop yield ($$Y$$), and you also measured mid-season fungus levels ($$Z$$), which the fertilizer *reduces* ($$X \rightarrow Z \rightarrow Y$$). Should you include mid-season fungus $$Z$$ as a predictor in your regression—and why?

---

## Reference videos

- [Statistical Rethinking 2023 - 05 - Elemental Confounds](https://www.youtube.com/watch?v=mBEA7PKDmiY) — Richard McElreath, English. **watch first**. Watch confounding drawn as shared arrows, exactly the part of the lesson that separates correlation from direct causal relationship.
- [Statistical Rethinking 2023 - 06 - Good & Bad Controls](https://www.youtube.com/watch?v=uanZZLlzKHw) — Richard McElreath, English. Watch correct and incorrect controls, supporting the decision of when to adjust for a variable.
- [4.6 - The Backdoor Adjustment](https://www.youtube.com/watch?v=U1S8Rq8IcrY) — Brady Neal - Causal Inference, English. Watch the backdoor adjustment, used where the lesson turns a DAG into a rule of adjusting or not.

## Practice questions

1. In a study of the effect of tutoring on exam scores, which variable could be a confounder?
2. Why shouldn't a mediator always be controlled for?
3. Think of a collider example in your own life or work.
4. What does Simpson's Paradox teach us about reading aggregated data?
5. Try drawing a simple DAG for the question: "Does exercise help you sleep better?"

## References

**Pearl, J. (2009).** *Causality: Models, Reasoning, and Inference* (2nd Edition). Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

**Hernan, M. A., & Robins, J. M. (2020).** *Causal Inference: What If*. Chapman & Hall/CRC.

---

*Next lesson: [5.3 Multicollinearity]({{ site.baseurl }}/contents/en/chapter05/05_03_multicollinearity/)*
