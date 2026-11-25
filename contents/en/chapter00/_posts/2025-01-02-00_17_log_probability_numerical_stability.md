---
layout: post
title: "Lesson 0.19: Log-probability and Numerical Stability"
chapter: '00'
order: 19
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

Try multiplying 400 probabilities of `0.1` together in Python (`0.1 ** 400`). Instead of a tiny positive number, IEEE 754 `float64` silently rounds the answer to **exact `0.0`** (*numerical underflow*)! Now try dividing `0.0 / 0.0` in Bayes’ rule, and your entire inference pipeline crashes with `NaN`! That is why **no serious Bayesian library ever multiplies raw probabilities**—everything runs in **log-probability space** using the **Log-Sum-Exp trick**.

This lesson equips you with the exact floating-point survival kit used inside Stan, PyMC, and every deep-learning framework: turning products into log-sums, computing log-normalizers safely with `logsumexp`, and checking gradients without overflow or underflow.

---

## Key ideas: Floating-Point Arithmetic Inside Bayesian Samplers

Four numerical-computing rules keep Bayesian software from ever returning `0.0 / 0.0 = NaN`:

1. **IEEE 754 `float64` Dynamic Range:** Positive `float64` numbers span roughly $$10^{-308}$$ to $$10^{+308}$$. Multiplying even 500 typical likelihood densities (each $$\sim 0.1$$) immediately underflows below $$10^{-308}$$ to exact zero!
2. **Log-Space Turns Products Into Sums:** $$\log\prod_{i=1}^n p(y_i\mid	heta) = \sum_{i=1}^n \log p(y_i\mid	heta)$$. Even for $$n = 1{,}000{,}000$$ data points, the sum sits comfortably around $$-2.3	imes 10^6$$—nowhere near underflow!
3. **The Log-Sum-Exp (LSE) Trick:** To normalize log-weights $$\ell_1,\dots,\ell_M$$ without `exp(-1000) == 0.0`, subtract $$m = \max_j \ell_j$$ first:
   $$\ln\sum_{j=1}^M e^{\ell_j} = m + \ln\sum_{j=1}^M e^{\ell_j - m}.$$
   Since every shifted exponent $$\ell_j - m \le 0$$ and at least one equals $$0$$ ($$e^0 = 1$$), overflow is impossible and total underflow is impossible!
4. **Log-Ratio Acceptance in MCMC:** Metropolis–Hastings computes $$\log lpha = \log p(	heta^*) - \log p(	heta)$$ directly in log space and compares against $$\log u$$ ($$u \sim \mathrm{Uniform}(0,1)$$)—never exponentiating giant log-posteriors!

---

## Learning objectives

After this lesson, you will understand why Bayesian practice almost always works on the log scale, recognize underflow, overflow, `-inf`, `nan` in probability computations, know how to write log-likelihoods and log-posteriors correctly, and master the log-sum-exp technique for safely normalizing posterior weights.

## Introduction: being mathematically correct is not enough, it must also be stable on a machine

Many probability formulas are perfectly correct on paper but fail when put into a computer. The reason is not in the statistics, but in the fact that computers can only store numbers with finite precision. In Bayesian computation, likelihoods and posteriors often contain products of very many numbers smaller than 1; if computed directly, they are easily rounded to 0. In the opposite direction, some exponentials can blow up to `inf`. Then the theoretical model is still right but the algorithm has broken.

So log-probability is not just a programming trick. It is the standard way to turn a probability model into a stable computation that can be optimized, normalized, and sampled reliably.

## 1) Where is the real problem?

Computers do not store real numbers with infinite precision. With the `float64` type, only a finite range of values can be represented. In probability models, this becomes a problem as soon as we deal with:

1. Products of very many probabilities smaller than 1.
2. Exponentials of numbers with very large magnitude.
3. Normalizations that require dividing extremely small numbers by the sum of other extremely small numbers.

A very simple example:

$$
10^{-3}\times 10^{-3}\times \cdots \times 10^{-3}\quad \text{(1000 times)} = 10^{-3000}
$$

This number is perfectly valid mathematically, but on a computer it is almost certainly rounded to 0. Then we no longer know how small the true value is; we only know it has "fallen out of the representable range".

## 2) What is log-probability and why does it save the day?

If $$p>0$$, we can work with $$\log p$$ instead of $$p$$. In statistics, the default here is the natural log.

The most important point is:

$$
\log\left(\prod_{i=1}^n p(x_i\mid\theta)\right)=\sum_{i=1}^n \log p(x_i\mid\theta)
$$

That is, the log turns products into sums. This is the core reason the log domain is more stable.

In practice, working on the log scale has three big benefits:

1. It avoids underflow from multiplying too many small numbers.
2. It turns products into sums, making them easier to optimize and easier to check.
3. It combines the prior with the likelihood very naturally in Bayes.

A small note on language: for continuous variables, more precisely we are working with the **log-density** and not the probability at a point. In Bayesian practice, however, people usually call it **log-probability** for short.

### 2.1) A familiar formula when moving to the log scale

For the Binomial model:

$$
p(k\mid n,\theta)=\binom{n}{k}\theta^k(1-\theta)^{n-k}
$$

taking the log gives us:

$$
\log p(k\mid n,\theta)=\log\binom{n}{k}+k\log\theta+(n-k)\log(1-\theta)
$$

Instead of multiplying very small numbers like $$\theta^k$$ and $$(1-\theta)^{n-k}$$, we just add the corresponding log-terms.

![Directly multiplying many small probabilities easily causes underflow]({{ site.baseurl }}/img/chapter_img/chapter00/log_probability_direct_product.png)

*Figure 1a: Computing directly on the probability scale makes the product of many small numbers quickly hit 0 on a computer.*

### 2.2) Maximizing the likelihood does not change when taking the log

Since the log function is monotonically increasing, we have:

$$
\arg\max_\theta L(\theta)=\arg\max_\theta \log L(\theta)
$$

This means: if our goal is to find the MLE or MAP, we can optimize on the log scale without changing the optimal solution.

## 3) A very concrete numerical example: mathematically right but numerically wrong

Suppose we have 1000 independent observations, and for some parameter value, each observation contributes a probability of about 0.01. Then:

$$
L = 0.01^{1000} = 10^{-2000}
$$

On paper, this is a positive number. But on a computer, this value usually becomes:

```python
0.0
```

That is, **underflow**.

Meanwhile, the log-likelihood is still perfectly useful:

$$
\log L = 1000\log(0.01)\approx -4605.17
$$

This is a large negative number, but still finite and still comparable.

The important point is: Bayesian algorithms usually do not need to know the absolute probability. They only need to know which value is **relatively larger**. If two parameters give:

$$
\log L_1=-4605,\qquad \log L_2=-4700
$$

then we immediately know $$L_1 > L_2$$, even though if we exponentiate both on a computer they might both become 0.

## 4) Underflow, overflow, `-inf`, and `nan`

These are four signals you will meet very often when coding probability models:

**Underflow**

A positive number that is too small gets rounded to 0.

A typical example is the product of very many small likelihood terms, or `np.exp(-1000)` being almost 0 on a machine.

**Overflow**

A number that is too large exceeds what the machine can represent and becomes `inf`.

A typical example is `np.exp(1000)`, which exceeds the storage capacity of `float64`.

**`-inf`**

Usually appears when taking $$\log(0)$$. In probability models, this is sometimes legitimate: if the model assigns probability 0 to the observed data, then the log-probability of that state really is $$-\infty$$.

**`nan`**

Appears when the computation has lost numerical meaning, for example `0/0`, `inf - inf`, or normalizing a weight vector in which all entries have underflowed to 0.

So the log domain does not make everything "absolutely safe". It only pushes the risk much lower. You still have to check for `-inf`, `inf`, and `nan` in the pipeline.

## 5) In Bayes, we almost always work with the log-posterior

Bayes' formula written in terms of probabilities is:

$$
p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}
$$

Taking the log:

$$
\log p(\theta\mid x)=\log p(x\mid\theta)+\log p(\theta)-\log p(x)
$$

Or more compactly:

$$
\log p(\theta\mid x)=\log p(x\mid\theta)+\log p(\theta)+C
$$

where $$C$$ is a constant not depending on $$\theta$$.

This is extremely important because:

1. To compare two parameter values, we do not need to fully normalize the posterior.
2. MAP only needs to maximize the unnormalized log-posterior.
3. Many MCMC, HMC, NUTS, and variational inference algorithms all operate on the joint log-probability.

In other words: in modern Bayesian practice, what the library internally actually computes is usually the **log-likelihood** or the **unnormalized log-posterior**, not the posterior on the ordinary probability scale.

## 6) When are we forced to return to the probability scale?

We cannot always stay on the log scale. We often have to return to the probability scale when we:

1. Need to normalize weights so they sum to 1.
2. Need to compute a posterior on a grid (grid approximation).
3. Need to convert log-weights into sampling probabilities.
4. Need to compute softmax in machine learning or Bayesian classification.

The problem is that if the log-weights are very negative, the direct computation

$$
e^{a_i}
$$

can underflow to 0 for every $$i$$. Then the subsequent normalization step becomes `0/0`, producing `nan`.

## 7) Log-sum-exp: a normalization technique you must know

When we need to compute:

$$
\log\sum_i e^{a_i}
$$

we should not compute it directly. The stable formula is:

$$
\log\sum_i e^{a_i}=m+\log\sum_i e^{a_i-m},\qquad m=\max_i a_i
$$

The idea is very simple: pull $$e^m$$ out of the sum. Since every $$a_i-m\le 0$$, the new exponents no longer explode.

### 7.1) Why does subtracting `max` make sense?

When normalizing weights, what we need is the **relative ratios** among values. For any constant $$c$$:

$$
\frac{e^{a_i}}{\sum_j e^{a_j}}
=
\frac{e^{a_i-c}}{\sum_j e^{a_j-c}}
$$

That is, we can subtract the same constant from all log-weights without changing the final probabilities. Choosing $$c=\max_j a_j$$ is the safest choice.

![Addition on the log scale is more stable with log-sum-exp]({{ site.baseurl }}/img/chapter_img/chapter00/log_probability_log_sum.png)

*Figure 1b: Log-sum-exp keeps the addition of probabilities stable by pulling all exponents to around the largest value.*

### 7.2) A small but very important example

Suppose the three log-weights are:

$$
a=(-1000,\,-1001,\,-1005)
$$

If computed directly:

$$
e^{-1000},\ e^{-1001},\ e^{-1005}
$$

then on a computer all three may become 0.

But if we subtract the max, we get:

$$
a-\max(a)=(0,\,-1,\,-5)
$$

Then:

$$
(e^0,\ e^{-1},\ e^{-5}) \approx (1,\ 0.3679,\ 0.0067)
$$

and after normalization, the weights are approximately:

$$
(0.727,\ 0.268,\ 0.005)
$$

That is, the probability information is actually still intact; only the direct computation has lost it.

## 8) A short Python example

The following code illustrates two very typical errors: underflow when multiplying likelihoods directly and `nan` errors when normalizing log-weights the wrong way.

```python
import numpy as np

# Example 1: multiplying probabilities directly
p = 0.01
n = 1000

likelihood = p ** n
log_likelihood = n * np.log(p)

print(likelihood)      # 0.0  -> underflow
print(log_likelihood)  # -4605.170185988091

# Example 2: normalizing log-weights the wrong way
log_weights = np.array([-1000.0, -1001.0, -1005.0])

bad_weights = np.exp(log_weights)
bad_weights = bad_weights / bad_weights.sum()
print(bad_weights)     # [nan nan nan]

# Stable way: subtract the max before exponentiating
m = np.max(log_weights)
good_weights = np.exp(log_weights - m)
good_weights = good_weights / good_weights.sum()
print(good_weights)    # [0.727..., 0.268..., 0.0049...]
```

What to take away is not "Python is annoying", but:

1. If you are already on the log scale, do not exponentiate too early.
2. When you need to normalize, subtract `max` or use `log-sum-exp`.

## 9) Very common practical mistakes

1. You have $$\log a$$ and $$\log b$$ but use $$\log a + \log b$$ in place of $$\log(a+b)$$. This is a fundamental difference: $$\log a + \log b = \log(ab)$$, not the log of a sum. When you need to add probabilities in the log domain, you must use log-sum-exp.
2. Computing the likelihood on the ordinary scale first, then taking the log afterwards. If the likelihood has already underflowed to 0, taking the log only gives $$-\infty$$; the lost information cannot be recovered.
3. Exponentiating the log-posterior too early just to "look at it familiarly". Many inference steps do not need to return to the probability scale.
4. Always treating $$-\infty$$ as a bug. Actually $$-\infty$$ is sometimes a legitimate signal that the model is assigning probability 0 to some configuration. What to do is check whether it is a consequence of the model or a numerical error.
5. Forgetting that for continuous variables, the log-density can be positive if the density exceeds 1. This is not necessarily wrong.

## 10) Good habits when coding Bayesian models

1. Write functions that return the log-likelihood or log-posterior, not the raw likelihood.
2. Add likelihood contributions on the log scale.
3. Only exponentiate at the final step, when you really need normalized probabilities.
4. Use the `subtract max` or log-sum-exp technique when normalizing weights.
5. Always check `np.isfinite(...)` at important steps.

If you have to remember just one sentence from this lesson, remember this one:

**In Bayes, stay on the log scale for as long as possible.**

## Quick summary

1. Many probability computations are right on paper but unstable on a computer.
2. Log-probability turns products into sums, helping avoid underflow and making optimization easier.
3. In Bayes, we usually work with the log-likelihood and the unnormalized log-posterior.
4. When you need to add or normalize probabilities in the log domain, you must use log-sum-exp or the subtract-`max` technique.
5. `-inf`, `inf`, and `nan` are not minor details; they are very important diagnostic signals.

---

### Worked Numerical Example: Rescuing `exp(-1000) + exp(-1001)` With Log-Sum-Exp

Suppose two candidate models have unnormalized log-posteriors $$\ell_1 = -1000.0$$ and $$\ell_2 = -1001.0$$:
- **Naive `float64` evaluation:** `np.exp(-1000.0)` returns `0.0`, `np.exp(-1001.0)` returns `0.0`, and `0.0 / (0.0 + 0.0)` explodes into **`NaN`**!
- **Log-Sum-Exp trick by hand:**
  1. Shift by the maximum: $$m = \max(-1000.0, -1001.0) = -1000.0$$.
  2. Compute shifted exponentials: $$e^{-1000 - (-1000)} = e^0 = 1.0$$ and $$e^{-1001 - (-1000)} = e^{-1} pprox 0.3679$$.
  3. Log-normalizer:
     $$\mathrm{LSE} = -1000.0 + \ln(1 + 0.3679) = -1000.0 + 0.3133 = \mathbf{-999.6867}.$$
  4. Exact normalized posterior probabilities:
     $$P(M_1) = e^{-1000.0 - (-999.6867)} = e^{-0.3133} pprox \mathbf{0.7311}, \qquad P(M_2) = e^{-1.3133} pprox \mathbf{0.2689}!$$

Zero underflow, zero overflow, and exact to full machine precision!

### Explanation: Four Numerical Rules Every Bayesian Coder Must Follow

1. **Always call `.logpdf()` / `.logpmf()`, never `np.log(dist.pdf(...))`:** Taking `log` *after* `pdf` underflows to `0.0` still returns `-inf`! Built-in `.logpdf()` evaluates the algebraic log formula directly.
2. **Use `scipy.special.logsumexp` (or `log1p` / `expm1`) for every normalization step:** Never hand-roll `np.exp(log_p) / np.sum(np.exp(log_p))`.
3. **Subtract the maximum log-posterior before plotting a grid:** Plotting `np.exp(log_post - log_post.max())` keeps peak height at `1.0` so grid normalization never underflows.
4. **Remember that continuous log-densities can be positive:** Only discrete log-probabilities are always $$\le 0$$; seeing `log_p = +1.8` for a narrow continuous Normal or Beta is completely healthy!

**Quick check.** Using the Log-Sum-Exp trick by hand, compute the exact normalized probabilities for two models with log-posteriors $$\ell_1 = -500.0$$ and $$\ell_2 = -500.0$$!

---

## Reference videos

- [Logs (logarithms), Clearly Explained!!!](https://www.youtube.com/watch?v=VSi0Z04fWj0) — StatQuest with Josh Starmer, English. **watch first**. Watch the log rules for products and sums, the algebraic foundation for the part of the lesson that moves from likelihood to log-likelihood.
- [Why Log Probabilities Are Everywhere in AI - Underflow Error in HMMs and Viterbi Algorithm](https://www.youtube.com/watch?v=HghZrdnrNQY) — Algorithms and AI, English. Watch underflow when multiplying many small probabilities, exactly the numerical failure the lesson illustrates with a product of probabilities.
- [The log-sum-exp trick (NLP817 5.12)](https://www.youtube.com/watch?v=MZ2VM32h37g) — Herman Kamper, English. Watch the log-sum-exp trick, supporting the part of the lesson about normalizing without returning to the probability scale too early.

## Practice questions

1. Why can two different likelihood values both show up as `0.0` on a machine, while the two corresponding log-likelihoods remain comparable?
2. Explain in words why subtracting `max` does not change the final softmax.
3. When is $$-\infty$$ a legitimate signal from the model, and when might it be a numerical bug?
4. Why can $$\log a + \log b$$ not replace $$\log(a+b)$$?

## References

- Murphy, K. (2012). *Machine Learning: A Probabilistic Perspective*.
- Bishop, C. (2006). *Pattern Recognition and Machine Learning*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis*.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*.

---

*Next lesson: [0.20 Basic Model Assumption Checks]({{ site.baseurl }}/contents/en/chapter00/00_18_basic_model_assumption_checks/)*
