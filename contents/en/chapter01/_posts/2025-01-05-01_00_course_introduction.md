---
layout: post
title: "Course Introduction: Bayesian Data Analysis"
chapter: '01'
order: 0
owner: Nguyen Le Linh
lang: en
categories:
- chapter01
lesson_type: required
---

Most statistics courses hand you a confusing flowchart of 25 disconnected tests—pick a $$z$$-test here, a Mann–Whitney there, a chi-squared somewhere else—and leave you memorizing edge cases. **Bayesian Data Analysis** replaces that entire zoo with **one unified, generative engine**: write a probability story for how your data arose, condition on the data you actually observed, and inspect the resulting posterior distribution!

Welcome to the course roadmap: this introduction shows you how all twelve chapters connect—from Chapter 0’s probability foundations through conjugate algebra, MCMC/HMC sampling, hierarchical partial pooling, and real-world Bayesian decision analysis.

---

## Key ideas: The Four-Stage Journey of Bayesian Data Analysis

1. **Stage 1 — Foundations & Updating (Chapters 0–2):** Probability as plausibility, Bayes’ rule, likelihoods, priors, posteriors, and exact conjugate families (Beta–Binomial, Normal–Normal, Gamma–Poisson).
2. **Stage 2 — Computation Beyond Conjugacy (Chapters 3–4):** Grid approximation, Quadratic/Laplace approximation, and **Markov Chain Monte Carlo (MCMC / Metropolis / HMC-NUTS)** so you can fit *any* model you can write down.
3. **Stage 3 — Regression, GLMs, Causality & Regularization (Chapters 5–7):** Multiple predictors, DAGs & confounding, Logistic/Poisson GLMs, and shrinkage priors that prevent overfitting.
4. **Stage 4 — Criticism, Decisions & Hierarchical Models (Chapters 8–12):** Posterior Predictive Checks (PPC), WAIC/LOO model comparison, Bayesian decision theory, and hands-on coding labs.

---

## Welcome to Bayesian Statistics

This course is built for one very clear goal: to help you learn to **think in probabilities**, instead of just memorizing statistical formulas as disconnected pieces. In practice, we constantly face questions such as whether a hypothesis is credible, whether new data changes an old belief, and, if we must decide today, how large the risk of being wrong is. Bayesian statistics is especially strong at exactly these questions, because it does not just give a "test result", but provides a unified way of thinking about **belief, data, uncertainty and decisions**.

> **Mini example.** When you hear a forecast of "70% chance of rain", you do not need to repeat tomorrow infinitely many times to understand what it means. You only need to know the current level of confidence to decide whether to bring an umbrella.
>
> **Quick check.** In your opinion, why is the way of thinking "update beliefs when more information arrives" closer to real life than many disconnected statistical formulas?

![Bayesian reasoning in everyday life]({{ site.baseurl }}/img/chapter_img/chapter01/bayesian_daily_life_small.png)

## What will this course help you learn?

If you study this course well, you will not only know "what Bayes' theorem is", but also how to use Bayesian thinking on real problems.

### 1. Understand probability as a language of degrees of belief

You will see why in Bayes, probability is understood not only as long-run frequency but also as a language describing the plausibility of a hypothesis, especially in situations where uncertainty is unavoidable.

### 2. Understand how to build a data-generating model

A good Bayesian model does not start from code. It starts from the question of how the data was generated, which parameters are still unknown, and which prior reasonably reflects what we already know.

### 3. Understand how to update beliefs with data

This is the heart of the whole course: the **prior** is what we initially believe, the **likelihood** is how the data speaks under each hypothesis or parameter value, and the **posterior** is the belief updated after those two parts meet.

![The Bayes machine: from prior to posterior]({{ site.baseurl }}/img/chapter_img/chapter01/bayes_machine_small.png)

### 4. Know how to use modern tools for Bayesian inference

After the foundations, the course moves into tools such as **grid approximation**, Monte Carlo and MCMC, then PyMC to implement real models, as well as model diagnostic techniques and predictive checks.

### 5. Know how to interpret results honestly

You will learn how to answer the questions that researchers, business people and engineers really care about, such as what the probability is that a parameter is greater than 0, which range of values is still plausible, how uncertain the future forecast is, and whether the model is missing an important structure.

## Why learn Bayes from the very beginning?

Many people come to Bayes after learning frequentist statistics and feeling that something is "hard to swallow" about p-values, confidence intervals or hypothesis testing. That is perfectly normal.

Bayes is attractive for three big reasons.

### 1. It is close to the intuition of learning from new information

In life, we already think in a very Bayesian way: hearing a weather forecast and then updating plans, seeing a medical test and then updating a diagnosis, or watching the first few purchases and then adjusting beliefs about market demand. We hardly ever think in the style of "I reject the hypothesis at the 5% significance level", because everyday language is closer to updating beliefs than to formal testing rituals.

### 2. It is more honest about uncertainty

Bayes does not only answer "what is the estimate", but also tells us how sure we are, which values remain possible, and, if we must forecast the future, how the risk region should be understood.

### 3. It fits modern data science very well

Bayes is especially strong in contexts such as little data but a need for quick decisions, hierarchical models, forecasting and recommendation, medical analysis, A/B testing, or machine learning with **quantification of uncertainty**.

## Resources to consult throughout the course

### Main resource

**Richard McElreath (2020)** - *Statistical Rethinking* (2nd Edition)

The strength of this resource is its very good modeling intuition, an explanation style close to beginners, and a tight connection between theory and practical models.

### Supplementary resources

**Andrew Gelman et al. (2013)** - *Bayesian Data Analysis* (3rd Edition)

The strength of this resource is its very solid foundation, broad coverage, and high suitability when you want to go deeper after having built initial intuition.

**John K. Kruschke (2014)** - *Doing Bayesian Data Analysis*

The strength of this resource is its very high pedagogy, many illustrative examples, and a very good connection between concepts and interpretation.

## Course information and assessment

### Core reference materials

1. Gelman, A. et al. *Bayesian Data Analysis*.
2. Congdon, P. *Bayesian Statistical Modelling*.
3. Lee, P. M. *Bayesian Statistics: An Introduction*.

### Assessment components

The current assessment consists of 20% regular work, 30% mid-term in a practical format, and 50% final in a practical format as well.

## You do not need to be good at math to learn Bayes

You only need enough patience to accept that uncertainty is something that must be modeled, that data does not speak for itself without a model, and that updating beliefs consistently is the core of inference. If you keep that spirit, Bayes will no longer be a hard chapter of statistics, but a very natural way of thinking.

> **3 key ideas.** This course does not only teach the Bayes formula but also a whole way of thinking about learning from data; Bayesian statistics is strong in connecting models, uncertainty and decision-making in the same workflow; and to study this course well, you should always prioritize modeling intuition first and only then computational technique.

## Moving on from here

The next lesson is [1.1 Replication Crisis & P-values](/en/chapter01/replication-crisis-pvalues/). This is where Chapter 1 begins to ask: if traditional statistical inference has too many limitations, do we have a better option?

If you need to review the foundations before entering the chapter, you can see [Chapter 00: Prerequisites](/en/chapter00/).

---

### Worked Numerical Example: One Complete Mini Bayesian Cycle in 3 Lines of Arithmetic

Before writing a single line of Stan or PyMC, see the entire Bayesian workflow on a 3-flip coin experiment (`H, H, T` — 2 heads, 1 tail) starting from a flat $$\mathrm{Beta}(1,1)$$ prior:
1. **Update:** $$\mathrm{Beta}(1 + 2,\; 1 + 1) = \mathrm{Beta}(3, 2)$$.
2. **Summarize:** Posterior mean $$\mathbb{E}[p\mid D] = \frac{3}{3+2} = \mathbf{0.60}$$, mode $$\frac{3-1}{3+2-2} = \mathbf{0.667}$$.
3. **Predict next flip (Posterior Predictive):** Probability Flip 4 is Heads equals the posterior mean **$$60\%$$**—automatically hedging between the raw sample rate (66.7%) and prior ignorance (50%)!

### Explanation: Four Study Habits That Make This Course Stick

1. **Always sketch the generative story first:** Every model in Chapters 1–12 can be drawn as a 3-line prior $$\to$$ likelihood diagram.
2. **Run and break every Python lab:** Change the prior strength, cut $$n$$ in half, or inject an outlier to *see* how the posterior reacts.
3. **Never separate inference from checking:** Fitting a posterior is only step 1; Posterior Predictive Checks tell you whether your model actually resembles reality.
4. **Think in distributions, not single numbers:** Train yourself to ask *"how wide is my uncertainty?"* every time you see a point estimate.

**Quick check.** In the 3-flip example above (`Beta(3, 2)` posterior), if you observe 100 more flips (60 Heads, 40 Tails), what is the updated posterior Beta distribution?

---

## Reference videos

- [The Bayesian Trap](https://www.youtube.com/watch?v=R13BD8qKeTg) — Veritasium, English. **watch first**. Watch the base-rate trap when updating beliefs, exactly the lesson's invitation to think in probabilities instead of memorizing formulas.
- [Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM) — 3Blue1Brown, English. Watch the geometry of Bayes' theorem, supporting the roadmap the lesson promises from prior and likelihood to posterior.
- [Statistical Rethinking 2023 - 01 - The Golem of Prague](https://www.youtube.com/watch?v=FdnMWdICdRs) — Richard McElreath, English. Watch the opening lecture of Statistical Rethinking on models as tools that need to be supervised, in the same spirit as this course.
