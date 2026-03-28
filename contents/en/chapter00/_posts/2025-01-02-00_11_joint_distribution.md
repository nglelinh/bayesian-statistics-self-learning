---
layout: post
title: "Lesson 0.11: Joint Distributions"
chapter: '00'
order: 11
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

## Learning objectives

After this lesson, you will understand that a joint distribution is the natural extension of one-variable distributions to multiple variables, how to derive marginals and conditionals from the joint, and why this structure is the direct foundation of Bayesian inference.

## 1) Motivation: One variable is often not enough

In previous lessons, we used one-variable distributions:

For the discrete case, we wrote $$p(x)=P(X=x)$$; for the continuous case, we wrote $$f(x)$$ and interpreted probability through the integral $$P(a\le X\le b)=\int_a^b f(x)\,dx$$.

That is a one-dimensional view. Now we extend to two dimensions (and in general, many dimensions): from $$p(x)$$ or $$f(x)$$ to $$p(x,y)$$ or $$f(x,y)$$. So joint distributions are not a separate idea; they are a **direct multivariable extension of distribution functions**.

![Extension from one variable to multiple variables](/bayesian-statistics-self-learning/img/chapter_img/chapter00/joint_distribution_marginalization.png)
*Figure 1: Extension from a one-variable distribution to a two-variable joint distribution. Center: joint density $$f(x,y)$$. Top/right: marginals obtained by integrating along the other axis. The dashed horizontal slice illustrates a conditional distribution.*

In practice, we usually care about several variables at once. For example:

We may care simultaneously about height $$H$$ and weight $$W$$, about study time $$T$$ and exam score $$S$$, or about disease status $$D$$ together with test result $$X$$.

If we model variables separately, we can miss their relationship. Joint distributions answer questions like: "what is the probability that **both** $$H$$ falls in this range and $$W$$ falls in that range?"

## 2) Definition of a joint distribution

### 2.1 Discrete case

For discrete variables $$X, Y$$, the joint distribution is:

$$p(x,y) = P(X=x, Y=y)$$

For this to be valid, we need $$p(x,y) \ge 0$$ for all $$x,y$$ and the double sum $$\sum_x\sum_y p(x,y)=1$$.

Here, $$p(x,y)$$ is the probability that both variables take specific values simultaneously.

### 2.2 Continuous case

For continuous variables $$X, Y$$, we use a joint density:

$$f(x,y)$$

such that:

$$P((X,Y)\in A)=\iint_A f(x,y)\,dx\,dy$$

and:

$$\iint_{\mathbb{R}^2} f(x,y)\,dx\,dy=1$$

As with one-dimensional PDFs, $$f(x,y)$$ is not a point probability; it is a density over the plane.

## 3) From joint to marginal

Marginal distributions describe one variable after "summing out" or integrating out the other. In the discrete case, we have:

$$p_X(x)=\sum_y p(x,y),\qquad p_Y(y)=\sum_x p(x,y)$$

In the continuous case, the corresponding formulas are:

$$f_X(x)=\int_{-\infty}^{\infty} f(x,y)\,dy,\qquad f_Y(y)=\int_{-\infty}^{\infty} f(x,y)\,dx$$

Intuition: a marginal is accumulated mass/density along the other axis.

## 4) Conditional distributions and product rule

When $$Y=y$$ is known, the conditional distribution of $$X$$ is:

$$p(x\mid y)=\frac{p(x,y)}{p_Y(y)}$$

(discrete form; continuous uses the corresponding densities).

This gives the product rule:

$$p(x,y)=p(x\mid y)p_Y(y)=p(y\mid x)p_X(x)$$

This is also the core mechanism behind Bayes:

$$p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}$$

with the key joint relationship:

$$p(\theta,x)=p(x\mid\theta)p(\theta)$$

## 5) Independence vs dependence

Variables $$X, Y$$ are independent if and only if:

$$p(x,y)=p_X(x)p_Y(y)$$

for all $$x,y$$ (or $$f(x,y)=f_X(x)f_Y(y)$$ in the continuous case).

If this identity holds, knowing $$Y$$ does not change our beliefs about $$X$$; if it fails, one variable carries information about the other.

Most interesting Bayesian models exploit dependence structure.

## 6) Short discrete example

Suppose:

Let $$X \in \{0,1\}$$ indicate whether a student attends class, and let $$Y \in \{0,1\}$$ indicate whether that student passes.

with joint table:

$$
\begin{array}{c|cc}
 & y=0 & y=1 \\
\hline
x=0 & 0.30 & 0.10 \\
x=1 & 0.15 & 0.45
\end{array}
$$

As a quick check, the total probability is 1. We also get $$p_X(1)=0.15+0.45=0.60$$, $$p_Y(1)=0.10+0.45=0.55$$, and $$p(Y=1\mid X=1)=0.45/0.60=0.75$$.

Since $$0.75 \ne 0.55$$, knowing $$X=1$$ changes the probability of passing, so the variables are dependent.

### 6.1) Reading the story from the table

If we translate the table into 100 students, we can read it in a very concrete way:

- 45 students attend and pass
- 15 attend but do not pass
- 10 do not attend but still pass
- 30 neither attend nor pass

From this, the pass rate in the attending group is $$45/(45+15)=75\%$$, while in the non-attending group it is only $$10/(10+30)=25\%$$. This makes the point tangible: a joint distribution is not just a symbolic table, but a compact way to describe how two variables move together in an interpretable story.

## 7) Bayesian connection in practice

In Bayesian modeling, we repeatedly use:

$$p(\theta, x)=p(x\mid\theta)p(\theta)$$

Then marginalize over $$\theta$$ to get evidence:

$$p(x)=\int p(x\mid\theta)p(\theta)\,d\theta$$

and normalize to obtain the posterior:

$$p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}$$

So mastering joint, marginal, and conditional distributions is essential before deeper Bayesian inference.

## Quick recap

1. A joint distribution models multiple variables simultaneously.
2. Marginals come from summing/integrating the joint.
3. Conditionals come from dividing joint by marginal.
4. Product rule links joint and conditional: $$p(x,y)=p(x\mid y)p(y)$$.
5. Independence is exactly $$p(x,y)=p(x)p(y)$$.
6. Bayes is built directly on joint-marginal-conditional relationships.

## Exercises

**Exercise 1.** Using the table in Section 6, compute:

- $$p_X(0), p_X(1)$$
- $$p_Y(0), p_Y(1)$$
- $$p(X=1\mid Y=1)$$ and $$p(Y=1\mid X=1)$$

**Exercise 2.** Prove from definitions that:

$$p(x,y)=p(x\mid y)p(y)=p(y\mid x)p(x)$$

**Exercise 3.** Let two continuous variables have joint density $$f(x,y)=c(x+y)$$ on $$0<x<1, 0<y<1$$ and 0 elsewhere.

- Find the constant $$c$$ so that $$f$$ is valid.
- Derive $$f_X(x)$$ and $$f_Y(y)$$.
- Check whether $$X, Y$$ are independent.

## References

- Wasserman, L. (2004). *All of Statistics*. Springer.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.
