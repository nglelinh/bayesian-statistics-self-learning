---
layout: post
title: "Lesson 0.3: Poisson and Exponential - Counting Events and Waiting Times"
chapter: '00'
order: 3
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

Stand by a quiet highway and watch cars pass at an average rate of $$\lambda = 3$$ cars per minute. Two twin questions immediately arise: *How many cars will pass in the next minute?* (**Poisson**), and *How long will I wait until the very next car arrives?* (**Exponential**). They are not two unrelated textbook formulas—they are two faces of the exact same continuous-time **Poisson process**!

This lesson builds intuitive command over Poisson counts and Exponential waiting times, explains the startling **memoryless property**, warns against real-world overdispersion, and sets up their natural Bayesian conjugate partner: the **Gamma distribution**.

---

## Background Knowledge Map: The Duality of Counts and Waiting Times

Four structural facts link Poisson, Exponential, and Bayesian rate modeling:

1. **Poisson Count Distribution:** Counts independent events occurring at constant rate $$\lambda$$ per unit time: $$P(N=k\mid \lambda) = rac{\lambda^k e^{-\lambda}}{k!}$$ with exact **equidispersion** $$\mathbb{E}[N] = \mathrm{Var}(N) = \lambda$$.
2. **Exponential Waiting Time:** The waiting time $$T$$ until the next event has PDF $$f(t\mid \lambda) = \lambda e^{-\lambda t}$$ ($$t \ge 0$$), mean $$1/\lambda$$, and survival function $$P(T > t) = e^{-\lambda t}$$. Notice that $$P(T > 1) = e^{-\lambda} = P(N = 0)$$—waiting more than 1 minute is literally identical to seeing 0 cars in 1 minute!
3. **The Memoryless Property:** $$P(T > s + t \mid T > s) = P(T > t)$$. Having waited 5 minutes with no bus tells you nothing about the remaining wait if arrivals are truly Poisson (useful for radioactive decay, dangerous for aging machinery!).
4. **Bayesian Gamma–Poisson Conjugacy:** Writing $$L(\lambda) \propto \lambda^{\sum k_i} e^{-n\lambda}$$ has the exact algebraic kernel of a **Gamma distribution**, letting us update our belief about an unknown rate $$\lambda$$ by simple addition!

---

## Learning objectives

After this lesson, you will be able to model count data with the Poisson, model waiting times with the Exponential, and understand why these two distributions are two faces of the same random event process over time.

## 1) When to use the Poisson?

The Poisson is suitable when we count the number of events in a fixed interval:

Typical examples are the number of calls in 1 hour, the number of errors on 1 page of text, or the number of accidents at an intersection in 1 month.

If $$Y$$ is the number of events in the observation interval:

$$
Y \sim \text{Poisson}(\lambda), \quad P(Y=k)=\frac{\lambda^k e^{-\lambda}}{k!},\; k=0,1,2,\dots
$$

Here $$\lambda$$ is the average number of events per interval.

Core properties:

$$
\mathbb{E}[Y]=\lambda, \qquad \mathrm{Var}(Y)=\lambda.
$$

![The Poisson describes the number of events counted in fixed time intervals]({{ site.baseurl }}/img/chapter_img/chapter00/poisson_counts_timeline.png)

*How to read the figure: This figure illustrates that the Poisson describes the number of events counted in fixed time intervals. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

## 2) When to use the Exponential?

The Exponential is suitable when we care about the waiting time until the next event.

If $$T$$ is the waiting time:

$$
T \sim \text{Exponential}(\lambda), \quad f(t)=\lambda e^{-\lambda t},\; t\ge 0.
$$

Expectation:

$$
\mathbb{E}[T]=\frac{1}{\lambda}.
$$

That is, the higher the event rate, the lower the average waiting time.

![The Exponential describes the waiting time until the next event]({{ site.baseurl }}/img/chapter_img/chapter00/exponential_waiting_time_curve.png)

*How to read the figure: This figure illustrates that the Exponential describes the waiting time until the next event. Read the axis labels/legend first, then compare the main trend across the lines, bars or groups of points instead of looking only at individual points.*

## 3) The normalizing constant in Poisson/Exponential

For the Poisson:

$$
P(Y=k)=\frac{\lambda^k e^{-\lambda}}{k!},\quad k=0,1,2,\dots
$$

Where:

Here, $$k!$$ reflects the number of ways of arranging the events in the combinatorial counting argument, while $$e^{-\lambda}$$ is the factor that makes the whole PMF sum to exactly 1.

Indeed:

$$
\sum_{k=0}^{\infty} \frac{\lambda^k e^{-\lambda}}{k!}
=e^{-\lambda}\sum_{k=0}^{\infty}\frac{\lambda^k}{k!}
=e^{-\lambda}e^{\lambda}=1.
$$

For the Exponential:

$$
f(t)=\lambda e^{-\lambda t},\quad t\ge 0.
$$

The constant $$\lambda$$ is the normalizing factor that makes the density integrate to 1:

$$
\int_0^{\infty} \lambda e^{-\lambda t}\,dt=1.
$$

If $$\lambda$$ is dropped, the function $$e^{-\lambda t}$$ is only the exponentially decaying "shape", not yet a valid density.

## 4) The direct link between Poisson and Exponential

If the number of events over time follows a Poisson process with rate $$\lambda$$, then:

The number of events in a longer interval $$\Delta t$$ will have a Poisson($$\lambda\Delta t$$) distribution, while the time between two consecutive events will have an Exponential($$\lambda$$) distribution.

So, the questions "how many events are counted" and "how long to wait until the next event" are really the same model from two viewpoints.

## 5) A short example

A call center receives an average of 6 calls per hour.

Then, the number of calls in 1 hour can be modeled by $$Y\sim\text{Poisson}(6)$$, and the probability that there is no call in 10 minutes, i.e. 1/6 hour, is computed as follows:

$$
P(Y=0)=e^{-6\times(1/6)}=e^{-1}\approx 0.368.
$$

Meanwhile, the average waiting time until the next call is:

$$
\mathbb{E}[T]=\frac{1}{6}\text{ hours}=10\text{ minutes}.
$$

### 5.1) The same $$\lambda$$, answering two different questions

Still with $$\lambda = 6$$ calls per hour:

- In 30 minutes, the expected number of calls is $$6 \times 0.5 = 3$$, so we can ask "will there be overload?" using the Poisson.
- In 5 minutes, the probability of at least one call is:

$$
P(T \leq 5\text{ minutes}) = 1 - e^{-6\times(5/60)} = 1 - e^{-0.5} \approx 0.393.
$$

That is, in the first 5 minutes, the probability that the call center receives at least one call is only about 39.3%.

The important point is: the Poisson helps answer the counting question over a time interval, while the Exponential helps answer the question of how long to wait until the next event. Both use exactly the same underlying rate $$\lambda$$.

## 6) Modeling warnings

If count data has variance much larger than the mean (overdispersion), the Poisson is usually too "tight". Then a Negative Binomial or a hierarchical model may be needed.

If the event rate changes over time (peak/off-peak hours), the assumption of a constant $$\lambda$$ is also no longer appropriate.

## 7) The Bayesian connection

In Bayes, a Gamma prior for $$\lambda$$ combined with a Poisson likelihood gives a Gamma posterior. This is a very useful conjugate pair for event-count problems.

---

*Next lesson: [0.4 Normal and CLT Intuition]({{ site.baseurl }}/contents/en/chapter00/00_02_03_normal_clt_intuition/)*

---

### Worked Numerical Example: Server Errors at Rate $$\lambda = 2$$ per Hour

Suppose a microservice logs errors as a Poisson process with rate $$\lambda = 2$$ errors/hour:
1. **Probability of a completely clean hour ($$N = 0$$):**
   $$P(N = 0) = rac{2^0 e^{-2}}{0!} = e^{-2} pprox 0.1353 \quad (13.5\%).$$
2. **Probability of at least 1 error in an hour ($$N \ge 1$$):**
   $$P(N \ge 1) = 1 - P(N=0) = 1 - 0.1353 = 0.8647 \quad (86.5\%).$$
3. **Probability of waiting more than 30 minutes ($$t = 0.5$$ hr) for the next error:**
   $$P(T > 0.5) = e^{-\lambda t} = e^{-2(0.5)} = e^{-1} pprox 0.3679 \quad (36.8\%).$$
4. **Check the duality:** Probability of 0 errors in 30 minutes (effective rate $$\lambda_{	ext{half}} = 2 	imes 0.5 = 1$$) is $$e^{-1} pprox 0.3679$$—identical to $$P(T > 0.5)$$!

### Deep-Dive Explanation: Four Modeling Checks Before Choosing Poisson/Exponential (Read Slowly)

1. **Always check $$\mathrm{Var}(N)$$ vs. $$\mathbb{E}[N]$$:** If your real-world click or error counts have sample variance $$3	imes$$ larger than the mean, Poisson will understate tail risk—upgrade to a **Gamma–Poisson (Negative Binomial)** mixture.
2. **Scale $$\lambda$$ proportionally to exposure time:** If rate is $$\lambda = 2$$ per hour, over $$t = 3$$ hours the count is $$\mathrm{Poisson}(6)$$, never $$\mathrm{Poisson}(2)$$.
3. **Verify whether memorylessness makes physical sense:** Lightbulbs and servers *age* (hazard rate increases), so Weibull or Gamma waiting times beat Exponential for reliability modeling.
4. **Spot the Bayesian kernel early:** Whenever you see $$\lambda^k e^{-t\lambda}$$, think immediately of a Gamma posterior $$\mathrm{Gamma}(lpha + k,\; eta + t)$$.

**Quick check.** If errors arrive at $$\lambda = 2$$ per hour and you have already waited 45 minutes with zero errors, what is the probability you will wait *at least another 30 minutes* under the memoryless Exponential model?

---

## Reference videos

- [An Introduction to the Poisson Distribution](https://www.youtube.com/watch?v=jmqZG6roVqU) — jbstatistics, English. **watch first**. Watch to grasp the Poisson as a model for counting events in a fixed interval, exactly the first half of the lesson.
- [Understanding Exponential vs Poisson Distributions](https://www.youtube.com/watch?v=n7K8s4vryCQ) — Explained by Michael, English. Watch the comparison of waiting time versus counts, supporting the claim that the Exponential and Poisson are two faces of the same process.
- [The Exponential Distribution](https://www.youtube.com/watch?v=wtLQUjfomig) — StatQuest with Josh Starmer, English. Watch the shape and parameter of the Exponential, used when the lesson moves from counting events to waiting times.
