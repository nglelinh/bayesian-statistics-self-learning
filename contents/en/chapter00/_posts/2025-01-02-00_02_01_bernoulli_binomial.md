---
layout: post
title: "Lesson 0.2: Bernoulli and Binomial - From Binary Outcomes to the Number of Successes"
chapter: '00'
order: 2
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

Every click-through rate, medical trial recovery, and A/B test conversion begins with the simplest possible random experiment: a single yes-or-no trial with success probability $$p$$. Stack $$n$$ independent copies of that trial together and count the successes, and you get the **Binomial distribution**—the exact likelihood engine behind the most famous Bayesian update in history (the Beta–Binomial model!).

This lesson builds fluent intuition for **Bernoulli** and **Binomial** models, distinguishes ordered sequences from unordered counts via $$inom{n}{k}$$, and previews how flipping the question from *"given $$p$$, what is $$P(k)$$?"* to *"given $$k$$, what is plausible for $$p$$?"* launches Bayesian inference.

---

## Key ideas: From Binary Trials to Bayesian Likelihoods

Four concepts turn coin-flip math into a real-world statistical workhorse:

1. **Bernoulli Trial ($$n=1$$):** Models a single binary outcome $$X \in \{0,1\}$$ with mean $$p$$ and variance $$p(1-p)$$ (maximized at $$p=0.5$$, where uncertainty is greatest).
2. **Binomial Count ($$n$$ i.i.d. trials):** Counts $$K = \sum_{i=1}^n X_i$$ with PMF $$P(K=k\mid p) = inom{n}{k} p^k (1-p)^{n-k}$$, mean $$np$$, and variance $$np(1-p)$$.
3. **Combinatorial Multiplicity $$inom{n}{k}$$:** Counts how many distinct sequences produce $$k$$ successes. Crucially, $$inom{n}{k}$$ does **not** depend on $$p$$—so in Bayesian updating it cancels out as a constant!
4. **Likelihood View (Fixing $$k$$, Varying $$p$$):** Holding observed data $$(n, k)$$ fixed and reading $$L(p) \propto p^k(1-p)^{n-k}$$ as a function of $$p$$ turns the Binomial PMF into a Bayesian likelihood ready to multiply by a Beta prior.

---

## Learning objectives

After this lesson, you will clearly distinguish Bernoulli and Binomial problems, understand the data-generating relationship between them, and know how to read the parameters in practical language instead of just looking at formulas.

## 1) The story of binary data generation

Many data problems start from a binary question:

For example, whether a user clicks or not, whether a patient responds to treatment or not, or whether a package is delivered on time or not.

Each observation has only two states, so the basic random variable is Bernoulli.

$$
X \sim \text{Bernoulli}(p), \quad P(X=1)=p,\; P(X=0)=1-p.
$$

Here $$p$$ is the probability of success in a single trial.

![Bernoulli describes a single binary trial with two possible outcomes]({{ site.baseurl }}/img/chapter_img/chapter00/bernoulli_binary_outcomes.png)

*How to read the figure: This figure illustrates that a Bernoulli describes a single binary trial with two possible outcomes. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

## 2) From Bernoulli to Binomial

If we repeat the Bernoulli experiment $$n$$ times independently with the same $$p$$, the number of successes $$K$$ follows a Binomial:

$$
K \sim \text{Binomial}(n,p), \quad P(K=k)=\binom{n}{k}p^k(1-p)^{n-k}.
$$

This is an important step in modeling:

A Bernoulli describes a single binary observation, while a Binomial describes the total number of successes after many trials of the same kind.

![The Binomial counts the number of successes after many independent Bernoulli trials]({{ site.baseurl }}/img/chapter_img/chapter00/binomial_success_count_distribution.png)

*How to read the figure: This figure illustrates that the Binomial counts the number of successes after many independent Bernoulli trials. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

In this illustration, we are using the parameters $$n=12$$ and $$p=0.35$$.

**How to read the chart `binomial_success_count_distribution.png`:**

- The horizontal axis is the number of successes $$k$$ (from $$0$$ to $$n$$), the vertical axis is the probability $$P(K=k)$$.
- Each bar shows the chance of getting exactly $$k$$ successes after $$n$$ trials.
- The peak of the distribution usually lies near $$k\approx np$$, so as $$p$$ increases the probability mass shifts to the right.
- Intuitively, the chart immediately shows us "which number of successes is most likely" and "how spread out it is around the expected value".

## 3) The normalizing constant in Bernoulli/Binomial

For the Bernoulli, the PMF is usually written:

$$
P(X=x)=p^x(1-p)^{1-x},
\quad x\in\{0,1\}.
$$

The validity condition of a discrete distribution is that the probabilities sum to 1:

$$
\sum_{x\in\{0,1\}} p^x(1-p)^{1-x}
=(1-p)+p=1.
$$

For the Binomial:

$$
P(K=k)=\binom{n}{k}p^k(1-p)^{n-k},\quad k=0,1,\dots,n.
$$

Here the binomial coefficient $$\binom{n}{k}$$ is exactly the count of the ways to arrange $$k$$ successes among $$n$$ trials. Thanks to this coefficient, the total probability closes to exactly 1:

$$
\sum_{k=0}^{n} \binom{n}{k}p^k(1-p)^{n-k}
=(p+1-p)^n=1.
$$

In short: for the Bernoulli/Binomial, the Binomial PMF is already "self-normalized": no extra constant is needed outside the formula.

## 4) The meaning of the parameters

In this model, $$p$$ expresses the "ease of success" of one trial, $$n$$ gives the scale of the experiment, and $$k$$ is the actual observed outcome after we have carried out those trials.

Two useful quantities:

$$
\mathbb{E}[K]=np, \qquad \mathrm{Var}(K)=np(1-p).
$$

So, the same mean $$np$$ but a different $$p$$ can give very different spread.

## 5) A short practical example

Suppose an API has an error probability of $$p=0.05$$ per request. In $$n=40$$ independent requests, the number of failed requests $$K$$ has a Binomial distribution.

In this case, the expected number of errors is $$\mathbb{E}[K]=40\times 0.05=2$$, and the probability that no error appears at all is computed as follows:

$$
P(K=0)=(1-0.05)^{40}\approx 0.129.
$$

Interpretation: even though the error rate is only 5%, the chance that a batch of 40 requests has no errors at all is only about 12.9%.

### 5.1) Same expectation of 2, but the uncertainty is not the same

Suppose we compare the following two situations:

- A quiz with 4 questions, each correct with probability $$0.5$$.
- An email campaign with 20 customers, each responding with probability $$0.1$$.

Both give an expected number of successes equal to 2:

$$
4 \times 0.5 = 2, \qquad 20 \times 0.1 = 2.
$$

But the variance differs:

$$
4 \times 0.5 \times 0.5 = 1, \qquad 20 \times 0.1 \times 0.9 = 1.8.
$$

Interpretation: even with the same "mean of 2 successes", the email campaign fluctuates clearly more. So reading $$np$$ alone is not enough; we also have to look at $$np(1-p)$$ to understand whether the result is stable.

## 6) Common modeling mistakes

The most common mistakes are using a Binomial when $$p$$ actually changes over time but is still assumed fixed, assuming independence even though the data depends on groups or on visit sessions, and equating the "observed probability" with the "true probability" without considering uncertainty. In these situations, we need to extend the model to richer forms such as hierarchical models, mixture models, or logistic regression with covariates.

## 7) The Bayesian connection

In Bayes, we usually put a prior on $$p$$ and then update with Binomial data. The most common conjugate pair is the Beta-Binomial (details in lesson 0.5).

---

*Next lesson: [0.3 Poisson and Exponential]({{ site.baseurl }}/contents/en/chapter00/00_02_02_poisson_exponential/)*

---

### Worked Numerical Example: Comparing Two Hypotheses for 7 Conversions in 10 Visits

Suppose a landing page gets $$k = 7$$ signups out of $$n = 10$$ independent visitors. First, compute the exact Binomial probability under two competing conversion rates—$$p = 0.5$$ vs. $$p = 0.7$$ (noting $$inom{10}{7} = rac{10	imes 9	imes 8}{3	imes 2	imes 1} = 120$$):

| Candidate Rate $$p$$ | $$p^7$$ | $$(1-p)^3$$ | Exact PMF $$120\,p^7(1-p)^3$$ | Relative Likelihood |
| :--- | :--- | :--- | :--- | :--- |
| $$p = 0.5$$ | $$0.00781$$ | $$0.1250$$ | $$0.1172$$ | $$1.00	imes$$ (baseline) |
| $$p = 0.7$$ | $$0.08235$$ | $$0.0270$$ | **$$0.2668$$** | **$$2.28	imes$$ more likely!** |

Notice the Bayesian insight: the data (7 out of 10) is $$2.28$$ times more probable under $$p=0.7$$ than under $$p=0.5$$, yet $$p=0.5$$ still has a completely non-trivial likelihood ($$11.7\%$$)—so with only 10 visits, we shouldn’t declare victory too soon!

### Explanation: Four Rules for Binomial Modeling in Practice

1. **Check all three Binomial assumptions:** Fixed $$n$$, constant $$p$$ across trials, and conditional independence. If one user clicks 10 times in a row, independence fails and variance explodes (*overdispersion*).
2. **Know why $$inom{n}{k}$$ vanishes in Bayes’ rule:** Because $$inom{n}{k}$$ is identical for every candidate $$p$$, the likelihood ratio between $$p=0.7$$ and $$p=0.5$$ depends *only* on $$p^k(1-p)^{n-k}$$.
3. **Standard error shrinks like $$1/\sqrt{n}$$:** For the sample proportion $$\hat{p} = K/n$$, $$\mathrm{SD}(\hat{p}) = \sqrt{p(1-p)/n}$$—bounded above by $$0.5/\sqrt{n}$$ at $$p=0.5$$.
4. **Watch the zero-success edge case:** Observing $$0$$ conversions in $$5$$ visits gives MLE $$\hat{p} = 0$$ (claiming conversion is impossible!), whereas a Bayesian Beta prior smoothly keeps small positive rates plausible.

**Quick check.** For $$n = 10$$ trials and $$p = 0.5$$, what are the exact mean $$\mathbb{E}[K]$$ and standard deviation $$\mathrm{SD}(K)$$?

---

## Reference videos

- [Bernoulli and Binomial Random Variables](https://www.youtube.com/watch?v=Tc6g-Y-l0Rg) — Steve Brunton, English. **watch first**. Watch to separate a single binary trial from the number of successes over many trials, exactly the Bernoulli and Binomial focus of the lesson.
- [The Binomial Distribution and Test, Clearly Explained!!!](https://www.youtube.com/watch?v=J8jNoF-K8E8) — StatQuest with Josh Starmer, English. Watch the example of counting successes and the combination formula, supporting the part that reads parameters in real-data language.
- [Binomial distributions | Probabilities of probabilities, part 1](https://www.youtube.com/watch?v=8idr1WZ1A7Q) — 3Blue1Brown, English. Watch to see the Binomial as the generative model of repeated binary data, a bridge to how Bayes uses this distribution in later lessons.
