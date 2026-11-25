---
layout: post
title: "Lesson 0.10: Probability Density Function (PDF) - In Detail"
chapter: '00'
order: 10
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

A student plots a continuous probability distribution, sees a peak value of `f(x) = 3.5`, and panics: *"Wait—how can a probability be greater than 1?!"* That moment of confusion is one of the most important conceptual hurdles in continuous probability: **a Probability Density Function (PDF) is NOT a probability**—it is probability *per unit length* (density), just as physical density (kg/m$$^3$$) only becomes mass when you multiply by volume!

This lesson builds crystal-clear intuition for continuous PDFs, CDFs, why $$P(X = c) = 0$$ at any exact point, and how density values greater than 1 arise routinely in tight Bayesian posteriors.

---

## Key ideas: Density, Area, and Continuous Bayesian Posteriors

Four concepts eliminate every misconception about continuous densities:

1. **Density vs. Probability Mass:** For a continuous variable $$X$$, $$f(x) \ge 0$$ can be *arbitrarily large* (e.g., $$f(x) = 10$$ on $$[0, 0.1]$$) as long as the total **area** integrates to 1: $$\int_{-\infty}^{\infty} f(x)\,dx = 1$$.
2. **Intervals Carry Probability, Points Have Zero Area:** $$P(a \le X \le b) = \int_a^b f(x)\,dx = F(b) - F(a)$$, whereas for any single exact point $$c$$, $$P(X = c) = 0$$.
3. **PDF–CDF Derivative Pair:** The Cumulative Distribution Function $$F(x) = P(X \le x)$$ climbs monotonically from 0 to 1, and its slope is the PDF: $$f(x) = F'(x)$$.
4. **Why Posterior PDFs Easily Exceed 1:** As you collect more data, a Bayesian posterior narrows around the true parameter (say width $$pprox 0.02$$); to keep total area equal to 1, its peak height *must* shoot up to roughly $$1 / 0.02 = 50$$!

---

## Learning objectives

This lesson presents a systematic treatment of the **probability density function (PDF), the essential difference between the PDF and the probability mass function (PMF)**, as well as how to correctly interpret the PDF in continuous models. 

## 1. From Discrete to Continuous

### 1.1. Discrete Random Variables - PMF

For a **discrete** random variable $$X$$, we have the **Probability Mass Function (PMF)** $$P(X = x)$$. This function gives the exact probability that the random variable takes a specific value. For example, when rolling a fair die, each face from 1 to 6 has probability $$P(X = k) = 1/6$$. The important thing to remember is that for a discrete variable, $$P(X = x)$$ **is a true probability**, with values from 0 to 1, and the sum of all probabilities equals 1.

The **properties of the PMF** can be summarized briefly as follows: $$P(X = x) \geq 0$$ for all $$x$$, the sum of all probabilities $$\sum_{\text{all } x} P(X = x)$$ equals 1, and most importantly $$P(X = x)$$ in the discrete case really is a probability with a direct meaning.

![PMF of a fair die]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_pmf_dice.png)

*How to read the figure: Look at each bar individually, because in a PMF each bar is exactly the probability at a specific value.*
*Figure 1: The PMF of a fair die. Each value from 1 to 6 carries exactly probability $$1/6$$, and the sum of all the bars equals 1.*

### 1.2. The Problem with Continuous Variables

Now consider a continuous random variable. Suppose adult height follows a normal distribution $$X \sim \mathcal{N}(170, 10^2)$$ cm. A natural question is: what is $$P(X = 170)$$?

The surprising answer is **0**! In fact, $$P(X = k)$$ equals 0 for **every** specific value $$k$$, whether 170, 170.5, or 170.000001. The reason is that there are **infinitely many** possible values the height can take. Between 170 cm and 171 cm, there are infinitely many different values: 170.1, 170.01, 170.001, and so on to infinity. If each value had a positive probability, the sum of all probabilities would be infinite, violating the basic principle that the sum must equal 1.

![A continuous variable and the probability at a single point]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_continuous_height.png)

*How to read the figure: Distinguish the red dot from the whole curve. The red dot shows the density value at 170 cm, while probability must still be understood as the area over an interval.*
*Figure 2: For a continuous variable such as height, $$P(X=170)=0$$ even though $$f(170)$$ is nonzero. What is meaningful is the probability over an interval of heights, not at a single point.*

**Solution**: Instead of asking for the probability at a point, we ask for the probability over an **interval**:

$$P(a \leq X \leq b)$$

For example, $$P(169.5 \leq X \leq 170.5)$$ is the probability that the height lies between 169.5 cm and 170.5 cm. This probability can be computed and is nonzero.

## 2. The Probability Density Function (PDF)

### 2.1. Formal Definition

For a continuous random variable $$X$$, the **Probability Density Function (PDF)** $$f(x)$$ is the function satisfying:

$$P(a \leq X \leq b) = \int_a^b f(x) \, dx$$

This is the most important definition of the lesson. The probability that $$X$$ lies in the interval $$[a, b]$$ is computed by the **integral** (the area under the curve) of the density function $$f(x)$$ from $$a$$ to $$b$$.

**The most important note** is that $$f(x)$$ is not a probability. It is a probability density, and only the integral, i.e., the area under the curve of $$f(x)$$, carries real probability meaning.

This is the source of many common misunderstandings about the PDF. Many people confuse this and think $$f(x)$$ is the probability at the point $$x$$, but this is completely wrong. Remember: $$f(x)$$ is only a density, like mass density in physics.

### 2.2. Why Is It Called "Density"?

The concept of "density" in statistics is analogous to **mass density** in physics. In physics, the mass density $$\rho(x)$$ (unit: kg/m³) is not a mass, but only tells how mass is distributed in space. To compute the actual mass, we must integrate: $$\text{Mass} = \int \rho(x) \, dx$$.

![Mass density in physics]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_mass_density_analogy.png)

*Figure 3: In physics, $$\rho(x)$$ is only the mass density; the real mass comes from the area under the curve $$\rho(x)$$ over the interval of interest.*

Similarly in statistics, the probability density $$f(x)$$ is not a probability, but tells how probability is "concentrated" around $$x$$; to get an actual probability, we must integrate $$\int f(x)\,dx$$, i.e., the area under the curve over the interval of interest.

![Probability density in statistics]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_probability_density_analogy.png)

*Figure 4: In statistics too, $$f(x)$$ is not a probability; probability appears only when we take the area under the curve over an interval, for example $$[-1,1]$$.*

When $$f(x)$$ is high at a point $$x$$, it means probability is "concentrated" around that point - in other words, in a small interval around $$x$$ there is more probability. When $$f(x)$$ is low, probability is "sparser" around that point.

### 2.3. Properties of the PDF

**Property 1: Non-negativity**: $$f(x) \geq 0$$ for all $$x$$

A probability density is never negative. This makes sense because a negative density would lead to negative probability (when integrated), which is meaningless.

**Property 2: The integral equals 1**: 

$$\int_{-\infty}^{\infty} f(x) \, dx = 1$$

The total area under the whole PDF curve must equal 1, because the total probability of all possible outcomes must equal 1.

**Property 3: $$f(x)$$ can be greater than 1!**

This is an important point and often causes confusion. Since $$f(x)$$ is not a probability, it can perfectly well be greater than 1. As long as the integral (total area) still equals 1, the PDF is valid.

A first example is a very narrow normal distribution. When the standard deviation is small enough, the peak of the curve will exceed 1 and still be valid because the total area is still 1.

![A narrow normal distribution can have a peak greater than 1]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_normal.png)

*Figure 5: With $$X \sim \mathcal{N}(0, 0.3^2)$$, the peak $$f(0)$$ exceeds 1, but the entire area under the curve is still 1.*

A second example is the uniform distribution on the interval $$[0, 0.5]$$. Here the PDF is exactly 2 over the whole interval, so the height is greater than 1 but the area is still only $$2 \times 0.5 = 1$$.

![The uniform distribution on [0, 0.5] has density equal to 2]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_uniform.png)

*Figure 6: The uniform distribution on $$[0, 0.5]$$ has $$f(x)=2>1$$. What makes it valid is not the height, but that the total area is still 1.*

Finally, there are distributions such as Beta(0.5, 0.5) that go even further: the density can shoot up near the endpoints 0 and 1. Even so, as long as the total integral is finite and equals 1, this is still a valid PDF.

![A Beta distribution whose density rises sharply at the endpoints]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_beta.png)

*Figure 7: With Beta(0.5, 0.5), the density becomes very high near 0 and 1. This again reminds us that $$f(x)$$ is not a point probability.*

## 3. A Deeper Understanding of the PDF

### 3.1. The PDF as the Limit of a Histogram

An intuitive way to understand the PDF is through the histogram. When we draw a histogram of data with an increasing sample size and a decreasing bin width, the histogram gradually approaches the theoretical PDF curve. Mathematically, as the sample size $$n \to \infty$$ and the bin width $$\Delta x \to 0$$, the histogram converges to the PDF.

*How to read the sequence of figures below: go from small $$n$$ to large $$n$$ and watch the blue histogram gradually hug the red theoretical PDF curve.*

![Histogram with n = 100]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n100.png)

*Figure 8: With $$n=100$$, the histogram is still rough and fluctuates strongly around the theoretical curve.*

![Histogram with n = 500]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n500.png)

*Figure 9: When $$n=500$$, the bell shape begins to be clearer but there are still significant differences in individual bins.*

![Histogram with n = 1,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n1000.png)

*Figure 10: With $$n=1{,}000$$, the histogram already mimics the PDF fairly well, although sampling noise is still clearly visible.*

![Histogram with n = 5,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n5000.png)

*Figure 11: At $$n=5{,}000$$, the overall outline of the histogram is close to the theoretical PDF.*

![Histogram with n = 10,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n10000.png)

*Figure 12: When $$n=10{,}000$$, the difference is mostly just small fluctuations due to sampling.*

![Histogram with n = 50,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n50000.png)

*Figure 13: With $$n=50{,}000$$, the histogram almost coincides with the theoretical PDF, showing that the PDF is the ideal limit when there is a great deal of data.*

This observation is very important because it connects the theoretical PDF with real data. In practice, we never have infinite data, so we work with histograms or other estimates of the PDF. But as we get more data, our estimate gets closer to the true PDF.

### 3.2. Probability over Small Intervals

Another useful way to understand the PDF is through approximation over small intervals. For a very small interval $$[x, x + \Delta x]$$:

$$P(x \leq X \leq x + \Delta x) \approx f(x) \cdot \Delta x$$

This formula shows that the probability in a small interval is approximately the height of the PDF times the width of the interval. This is exactly the formula for the area of a rectangle with height $$f(x)$$ and width $$\Delta x$$.

The smaller $$\Delta x$$ is, the more accurate the approximation. Mathematically, we can write:

$$f(x) = \lim_{\Delta x \to 0} \frac{P(x \leq X \leq x + \Delta x)}{\Delta x}$$

This formula shows that the PDF is the "derivative" of probability with respect to the variable $$x$$. In other words, $$f(x)$$ measures the rate of change of probability as we move along the $$x$$ axis.

*How to read the sequence of figures below: compare the dashed green rectangle with the orange area as $$\Delta x$$ gets smaller and smaller.*

![Approximation with delta x equal to 0.5]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_05.png)

*Figure 14: With $$\Delta x = 0.5$$, the approximating rectangle is still rather coarse so the error is still clearly visible.*

![Approximation with delta x equal to 0.1]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_01.png)

*Figure 15: When $$\Delta x = 0.1$$, the rectangle hugs the true area much more closely.*

![Approximation with delta x equal to 0.01]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_001.png)

*Figure 16: With $$\Delta x = 0.01$$, the approximation $$f(x)\Delta x$$ almost coincides with the true probability over a very small interval.*

### 3.3. The Units of the PDF

An important but often overlooked aspect of the PDF is its units. If the random variable $$X$$ has units, such as cm, kg, or seconds, then $$f(x)$$ has units of **1/(units of X)**, and $$f(x)\cdot dx$$ becomes a unitless quantity, which is exactly why it can be interpreted as a probability.

For example, if $$X$$ is height in cm, then $$f(x)$$ has units of 1/cm. If we convert to meters, $$f(x)$$ will have units of 1/m, and its numerical value will change accordingly. Specifically, if $$f(170 \text{ cm}) = 0.04 \text{ (1/cm)}$$, then $$f(1.70 \text{ m}) = 4.0 \text{ (1/m)}$$ - increased by a factor of 100 because we switched from cm to m.

![PDF when measuring height in cm]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_units_cm_only.png)

*Figure 17: When measured in cm, the value at the center is about $$f(170)=0.04$$ with units of 1/cm.*

![PDF when measuring height in m]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_units_m_only.png)

*Figure 18: The same distribution but switched to meters, the value at the center rises to about $$f(1.70)=4.0$$ with units of 1/m. The physical shape of the distribution does not change, only the scale and the units of the density change.*

However, **probability does not depend on units**. $$P(160 \text{ cm} \leq X \leq 180 \text{ cm}) = P(1.60 \text{ m} \leq X \leq 1.80 \text{ m})$$. This makes sense because probability is an abstract concept with no physical unit of measurement.

The dependence of $$f(x)$$ on units is another important reason why we cannot regard $$f(x)$$ as a probability. Probability must be unchanged regardless of which unit system we use, but $$f(x)$$ changes with the units.

## 4. Comparing the PMF and the PDF

To consolidate understanding, let us compare the PMF and the PDF directly:

On the discrete side, a typical PMF such as Binomial(10, 0.5) assigns probability directly to each integer value.

![Example PMF of a Binomial distribution]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_binomial_pmf_example.png)

*Figure 19: In a PMF, the bar at $$x=5$$ is exactly the probability $$P(X=5)=0.246$$ and can be read directly from the figure.*

On the continuous side, a typical PDF such as Normal(0,1) gives us only the density at each point and not the point probability.

![Example PDF of the standard normal distribution]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_normal_density_example.png)

*Figure 20: In a PDF, the value $$f(0)=0.399$$ is only the density at the point 0, while $$P(X=0)=0$$ because this is a continuous variable.*

| Feature | PMF (Discrete) | PDF (Continuous) |
|----------|---------------|----------------|
| **Notation** | $$P(X = x)$$ | $$f(x)$$ |
| **Meaning** | Probability | Probability density |
| **Value** | $$0 \leq P(X=x) \leq 1$$ | $$f(x) \geq 0$$ (can be > 1) |
| **P(X = x)** | Meaningful | = 0 (meaningless) |
| **Sum/Integral** | $$\sum P(X=x) = 1$$ | $$\int f(x)dx = 1$$ |
| **Interval probability** | $$\sum_{a}^{b} P(X=x)$$ | $$\int_a^b f(x)dx$$ |
| **Units** | Unitless | 1/(units of X) |

The core difference is: with a PMF, $$P(X=x)$$ **is a probability**, whereas with a PDF, $$f(x)$$ **is not a probability** but only a density. Only when we sum (discrete) or integrate (continuous) do we get real probability.

## 5. Common Mistakes

### Mistake 1: Thinking $$f(x)$$ is a probability

This is the most common mistake. Many people look at the normal distribution with mean 170 cm and standard deviation 10 cm, compute $$f(170) = 0.04$$, and then say "the probability that the height equals 170 cm is 0.04". This is completely **wrong**. The wrong interpretation would be to write "$$P(X = 170) = f(170) = 0.04$$", whereas the correct interpretation must be "$$P(X = 170) = 0$$ because this is a continuous variable, and $$f(170) = 0.04$$ is only the density at that point".

### Mistake 2: Thinking $$f(x) \leq 1$$

Because probability never exceeds 1, many people automatically assume the PDF cannot exceed 1 either. But as we have seen, this is **wrong**. The statement "$$f(x)$$ must be less than or equal to 1" is false, while the correct statement is "$$f(x) \geq 0$$ and can perfectly well be greater than 1, as long as the total integral $$\int f(x)dx = 1$$".

For example, the uniform distribution on $$[0, 0.2]$$ has $$f(x) = 5 > 1$$, but is perfectly valid because the area is $$5 \times 0.2 = 1$$.

### Mistake 3: Comparing $$f(x)$$ across different units

Because $$f(x)$$ depends on units, comparing $$f(170 \text{ cm})$$ with $$f(1.70 \text{ m})$$ is meaningless. They have different units and different numerical values, so what can be compared meaningfully is not the density at a point but the probabilities over corresponding intervals, because probability carries no units.

## 6. Applications in Bayesian Statistics

### 6.1. Prior and Posterior Are PDFs

In Bayesian analysis, both the prior distribution $$p(\theta)$$ and the posterior distribution $$p(\theta \mid x)$$ are PDFs if the parameter $$\theta$$ is continuous. This means $$p(\theta)$$ is not a point probability but a **density of belief**, so an expression such as $$p(\theta = 0.5)$$ has no direct probabilistic interpretation; what is meaningful is the probability over an interval, for example $$P(a \leq \theta \leq b) = \int_a^b p(\theta)\,d\theta$$, and because it is a density, $$p(\theta)$$ can also be greater than 1.

![Prior and posterior as two density functions]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_bayesian_prior_posterior.png)

*Figure 21: In Bayesian analysis, the prior and the posterior are both PDF curves over the parameter space. They describe the density of belief before and after observing data.*

For example, suppose we have a prior $$\theta \sim \text{Beta}(2, 2)$$ for the success probability of an experiment, and observe 7 successes in 10 trials. The posterior will be $$\theta \mid x \sim \text{Beta}(9, 5)$$. When we say "the 95% credible interval is [0.395, 0.827]", the precise meaning is:

$$P(0.395 \leq \theta \leq 0.827 \mid x) = \int_{0.395}^{0.827} p(\theta \mid x) \, d\theta = 0.95$$

![A credible interval as the area under the posterior]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_bayesian_credible_interval.png)

*Figure 22: The 95% credible interval is the blue area under the posterior PDF, not the height of the curve at some point.*

This is the integral (area) of the posterior PDF, not the value of the PDF at any point.

### 6.2. The Likelihood Function

The likelihood function $$L(\theta) = p(x \mid \theta)$$ is also proportional to a PDF. When the data $$x$$ is fixed, the likelihood is a function of the parameter $$\theta$$. If the model is $$X \sim \mathcal{N}(\mu, \sigma^2)$$ with known $$\sigma$$, then:

$$L(\mu) = \prod_{i=1}^{n} f(x_i \mid \mu) = \prod_{i=1}^{n} \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x_i-\mu)^2}{2\sigma^2}\right)$$

Here, each $$f(x_i \mid \mu)$$ is the value of the PDF at the data point $$x_i$$, with parameter $$\mu$$. The Maximum Likelihood Estimate (MLE) is the value $$\hat{\mu}$$ that maximizes $$L(\mu)$$.

---

### Worked Numerical Example: A Tight Triangular/Uniform Density Whose Height Exceeds 1

Consider a narrow uniform posterior $$	heta \sim \mathrm{Uniform}(0.40,\; 0.65)$$ (width $$w = 0.65 - 0.40 = 0.25$$):
1. **Constant PDF height:** To make total area equal 1, the density height must be:
   $$f(	heta) = rac{1}{0.25} = \mathbf{4.0} \quad 	ext{for } 	heta \in [0.40, 0.65]$$
   —four times larger than 1, and 100% mathematically valid!
2. **Probability of a small interval $$[0.45, 0.50]$$ (width $$0.05$$):**
   $$P(0.45 \le 	heta \le 0.50) = 	ext{height} 	imes 	ext{width} = 4.0 	imes 0.05 = \mathbf{0.20} \quad (20\%).$$
3. **Check a Normal density peak:** For $$\mathcal{N}(0, \sigma^2)$$ with $$\sigma = 0.1$$, the peak height at $$x=0$$ is $$f(0) = rac{1}{\sigma\sqrt{2\pi}} = rac{1}{0.1 	imes 2.5066} pprox \mathbf{3.99} > 1$$!

### Explanation: Four Rules for Reading Continuous PDFs Correctly

1. **Always check the units of the horizontal axis:** If you change units from meters to kilometers, interval widths shrink by $$1000	imes$$, so PDF heights multiply by $$1000	imes$$ to keep total area equal to 1!
2. **Read *ratios* of densities, not raw heights:** Saying $$f(0.7) / f(0.5) = 2.28$$ means a tiny interval around $$0.7$$ is $$2.28	imes$$ as probable as an equally wide interval around $$0.5$$—this ratio is scale-free and drives Metropolis–Hastings acceptance!
3. **Use the CDF (or quantiles) for tail probabilities:** `F(b) - F(a)` answers probability questions directly without hand integration.
4. **Don’t panic when log-density is positive:** Whenever $$f(x) > 1$$ (a tight posterior!), $$\log f(x) > 0$$—completely normal for continuous PDFs (only discrete PMFs must satisfy $$\log P \le 0$$)!

**Quick check.** If a continuous random variable has a positive log-density $$\log f(x) = +2.3$$ at a point $$x$$, is there a bug in your code—or what is the density height $$f(x) = e^{2.3}$$?

---

## Reference videos

- [Probability density and mass functions](https://www.youtube.com/watch?v=hDjcxi9p0ak) — Intelligent Systems Lab, English. **watch first**. Watch to separate the probability mass function from the density function, exactly the PMF vs PDF distinction the lesson places at its center.
- [Probability Distribution Functions (PMF, PDF, CDF)](https://www.youtube.com/watch?v=YXLVjCKVP7U) — zedstatistics, English. Watch the relationship among the PMF, PDF and cumulative distribution function, supporting the part on reading probability over an interval.
- [Why “probability of 0” does not mean “impossible” | Probabilities of probabilities, part 2](https://www.youtube.com/watch?v=ZA4JkHKZM50) — 3Blue1Brown, English. Watch why the density at a point is not the probability of that point, used when the lesson interprets the PDF of a continuous variable.

## Exercises

**Exercise 1**: Explain why $$P(X = 170) = 0$$ for a continuous variable, but $$f(170)$$ can be nonzero. What is the difference between these two quantities?

**Exercise 2**: Given $$f(x) = 2x$$ on $$[0, 1]$$ and $$f(x) = 0$$ outside.
   - Check that this is a valid PDF (integral equals 1)
   - Compute $$P(0.2 \leq X \leq 0.5)$$
   - Is $$f(0.3) = 0.6$$ a probability? If not, what does it mean?

**Exercise 3**: Create two normal distributions with the same mean but different standard deviations (for example $$\sigma = 1$$ and $$\sigma = 2$$). Compare the values of $$f(x)$$ at the mean. Which distribution has the larger $$f(\mu)$$? Why?

**Exercise 4**: Height $$X \sim \mathcal{N}(170 \text{ cm}, 10^2)$$.
   - If $$f(170 \text{ cm}) = 0.04 \text{ (1/cm)}$$, what is $$f(1.70 \text{ m})$$ (in units of 1/m)?
   - Compute $$P(160 \leq X \leq 180)$$ in both unit systems. Are the results the same?
   - Explain why the probability stays the same but $$f(x)$$ changes with the units.

**Exercise 5**: Given the prior $$\theta \sim \text{Beta}(1, 1)$$ (uniform distribution) and data: 3 successes in 5 trials.
   - Find the posterior $$p(\theta \mid x)$$
   - Is $$p(0.5 \mid x)$$ a probability? If not, what does it mean?
   - Compute the 90% credible interval for $$\theta$$
   - Explain the meaning of "$$P(a \leq \theta \leq b \mid x) = 0.90$$" in the language of the PDF integral

## References

**Wasserman, L. (2004).** *All of Statistics: A Concise Course in Statistical Inference*. Springer.
- Chapter 2: Random Variables - The part on the PDF and its difference from the PMF

**Casella, G., & Berger, R. L. (2002).** *Statistical Inference* (2nd Edition). Duxbury.
- Chapter 1: Probability Theory - Detailed explanation of the PDF and its mathematical properties

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Appendix A: Standard probability distributions - Using the PDF in a Bayesian context

**Seeing Theory - Probability Distributions**: [https://seeing-theory.brown.edu/](https://seeing-theory.brown.edu/)
- Interactive visualization of PDF concepts

---

*A correct understanding of the PDF is an important foundation for Bayesian Statistics! Remember: $$f(x)$$ is density, not probability. Only the integral of $$f(x)$$ gives probability.*

---

*Next lesson: [0.11 P-values and Hypothesis Testing]({{ site.baseurl }}/contents/en/chapter00/00_08_pvalues_and_hypothesis_testing/)*
