---
layout: post
title: "Lesson 0.6: Descriptive Statistics - The First Language of Data"
chapter: '00'
order: 6
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

When a tech billionaire walks into a neighborhood coffee shop with 9 ordinary customers, the *mean* net worth inside the shop instantly shoots above $100 million—yet nine out of ten people in the room still can’t buy a yacht! That single anecdote explains why **descriptive statistics** is never just busywork before modeling: choosing the wrong summary (mean vs. median, SD vs. IQR) can completely misrepresent a skewed dataset—and later, a skewed Bayesian posterior!

This lesson builds sharp numerical intuition for measures of center, spread, and shape, showing how robust quantiles (`median`, `IQR`) protect you from outliers and prepare you to summarize MCMC posterior draws accurately.

---

## Key ideas: Summarizing Data—and Summarizing Bayesian Posteriors

Every descriptive summary you compute on raw data reappears directly when summarizing posterior samples:

1. **Measures of Location (Mean, Median, Mode):** The mean minimizes squared error ($$L_2$$ loss), the median minimizes absolute error ($$L_1$$ loss) and resists extreme outliers, and the mode marks the highest-density peak (analogous to MAP in Bayesian inference).
2. **Measures of Spread (Variance, SD, IQR):** Standard deviation measures typical squared distance from the mean; **Interquartile Range** ($$\mathrm{IQR} = Q_3 - Q_1$$) captures the middle 50% of data without being distorted by heavy tails.
3. **Skewness & Quantile Intervals:** When a distribution is strongly right-skewed (income, waiting times, variance parameters $$\sigma^2$$), reporting `mean ± 2 SD` can even cross below zero—whereas quantile summaries (`median [Q_2.5%, Q_97.5%]`) stay honest.
4. **Bridge to Posterior Summaries:** In Bayesian analysis via MCMC, you summarize thousands of posterior draws using the exact same toolkit: posterior mean, posterior median, posterior SD, and 95% credible intervals!

---

## Learning Objectives

After completing this lesson, you will understand that descriptive statistics is not just about computing summary numbers, but the art of telling a story about data. You will learn to use statistics such as the mean, median, and standard deviation not as mechanical formulas, but as tools for understanding the structure, trends, and variability in data. More importantly, you will develop intuition about when to use each statistic, and how to interpret them in the context of Bayesian analysis, where understanding the distribution of the data is an important first step before building a model.

## Introduction: Why Do We Need Descriptive Statistics?

Imagine you receive a dataset containing the heights of 10,000 adults. How can you understand this data? You cannot look at each individual number and draw meaningful conclusions. You need a way to summarize, to capture the essence of the data in a few numbers or comprehensible pictures.

This is exactly the role of descriptive statistics. They give us a language for talking about data, a way to convey what we see in thousands or millions of data points as a few important characteristics. Descriptive statistics answers basic questions: What is the "typical" value? How is the data spread out? Are there any unusual values? Is the distribution symmetric or skewed?

In Bayesian analysis, descriptive statistics plays a particularly important role. Before we build a complex probability model, we need to understand our data. We need to know which distribution might fit, which parameters need to be estimated, and which assumptions might be violated. Descriptive statistics is the first step on this journey, helping us build intuition about the data before we start modeling.

## Measures of Central Tendency: Searching for the "Typical" Value

One of the first questions we usually ask about a dataset is: "What is the typical value?" But "typical" can mean many different things, and that is why we have several different measures of central tendency.

### The Mean: The Balance Point

The **arithmetic mean** is the most familiar measure of central tendency. For a dataset $$x_1, x_2, \ldots, x_n$$, the mean is defined as:

$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

The mean has a beautiful geometric interpretation: it is the balance point of the data. If you imagine each data point as a mass on a straight rod, the mean is the point at which the rod would balance. More formally, the mean is the value for which the sum of deviations from it is zero: $$\sum_{i=1}^{n} (x_i - \bar{x}) = 0$$.

However, the mean has an important weakness: it is very sensitive to outliers. A single extreme value can pull the mean far away from most of the data. Consider an example: the incomes of 10 people, 9 of whom earn between 30,000 and 50,000 dollars per year, and one who earns 1,000,000 dollars. The mean would be about 130,000 dollars, a number that does not represent the "typical" income of this group.

In Bayesian analysis, the mean often appears as the location parameter of the normal distribution. When we model data as $$y_i \sim \mathcal{N}(\mu, \sigma^2)$$, $$\mu$$ is the mean of the distribution, and its natural estimate from the data is the sample mean $$\bar{x}$$.

### The Median: The Middle Value

The **median** is the middle value when the data is sorted in increasing order. If the number of observations $$n$$ is odd, the median is the $$(n+1)/2$$-th value. If $$n$$ is even, the median is usually defined as the average of the two middle values.

The median has an important property: it is **robust** to outliers. You can change the extreme values in the data without affecting the median, as long as you do not change the order of the values around the middle. In the income example above, the median would still lie in the range of 30,000-50,000 dollars, better reflecting the "typical" income.

The median also has a natural probabilistic interpretation: it is the value for which the probability of observing a smaller value is 50%, and the probability of observing a larger value is also 50%. This is the 50th percentile of the distribution.

In Bayesian analysis, the median is often used to summarize the posterior distribution, especially when the distribution is asymmetric. Instead of reporting the posterior mean (which can be affected by a long tail), we often report the posterior median together with a credible interval.

### Comparing the Mean and Median: Detecting Skewness

The relationship between the mean and the median gives us information about the shape of the distribution. If the distribution is symmetric, the mean and median will be close to equal. If the distribution is right-skewed (with a long tail on the right), the mean will be larger than the median because it is pulled toward large values. If the distribution is left-skewed, the mean will be smaller than the median.

This difference is not just a technical detail. It tells us whether the normal distribution is a suitable model. If the mean and median differ significantly, we may need to consider skewed distributions such as the log-normal, gamma, or beta, depending on the nature of the data.

*How to read the figure: The two figures below separate the two cases so you can clearly see the positions of the mean and median in each type of distribution.*

![Symmetric distribution with the mean close to the median]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_mean_median_symmetric.png)

*Figure 1a: In a nearly symmetric distribution, the mean and median almost coincide.*

![Right-skewed distribution with the mean pulled toward the tail]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_mean_median_right_skewed.png)

*Figure 1b: When data is right-skewed, the long tail pulls the mean to the right more strongly than the median. This is a very useful visual sign before choosing a model.*

### A very short example: the mean and median tell two different stories

Suppose the monthly incomes (million VND) of 10 people are:

$$
30,\ 31,\ 32,\ 33,\ 34,\ 35,\ 36,\ 37,\ 38,\ 120
$$

Then:

- The mean is $$42.6$$
- The median is $$34.5$$

If we only report the mean, it is easy to think this group has a "typical" income of more than 40 million. But in fact 9 out of 10 people lie in the range of 30 to 38 million, and one very large value has pulled the mean up strongly. This example shows why descriptive statistics should always be read together, instead of looking at just a single number.

## Measures of Spread: Quantifying Uncertainty

Knowing the central value is not enough. Two datasets can have the same mean but be very different in spread. One may be tightly concentrated around the mean, while the other may be widely dispersed. Measures of spread help us quantify this variability.

### Variance and Standard Deviation: The Mean Squared Deviation

The **sample variance** measures the average spread of the data around the mean:

$$s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

Note that we divide by $$n-1$$ rather than $$n$$. This is **Bessel's correction**, used to make the sample variance an unbiased estimator of the population variance. The reason for this correction is that we have already used the data to estimate the mean $$\bar{x}$$, and this removes one "degree of freedom".

Variance has a practical problem: its unit is the square of the original data's unit. If we measure height in cm, the variance will have units of cm². This makes variance hard to interpret. To remedy this, we use the **standard deviation**:

$$s = \sqrt{s^2}$$

The standard deviation has the same unit as the original data and can be interpreted as the "typical deviation" from the mean.

In Bayesian analysis, the variance (or the precision, the inverse of the variance) is an important parameter to be estimated. When we model data as $$y_i \sim \mathcal{N}(\mu, \sigma^2)$$, $$\sigma^2$$ is the variance, and its natural estimate is the sample variance $$s^2$$.

### Quantiles and the Interquartile Range: Robust Statistics

**Quantiles** (or percentiles) divide the distribution into equal parts. The $$p$$-th quantile ($$0 < p < 1$$) is the value such that $$100p\%$$ of the data is less than or equal to it. For example, the 0.25 quantile (also called the first quartile, Q1) is the value such that 25% of the data is less than or equal to it.

The **interquartile range** (IQR) is the distance between the third quartile (Q3) and the first quartile (Q1):

$$\text{IQR} = Q3 - Q1$$

The IQR contains the middle 50% of the data and is a measure of spread that is robust to outliers. It is often used to detect outliers: values lying outside the interval $$[Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}]$$ are usually regarded as potential outliers.

In Bayesian analysis, quantiles are widely used to summarize the posterior distribution. Instead of only reporting the mean or median, we often report a **credible interval**, for example a 95% interval that contains 95% of the posterior probability. This interval is usually constructed from quantiles, for example from the 0.025 quantile to the 0.975 quantile.

*How to read the figure: The group of figures below separates the story about spread from the story about the IQR in the box plot.*

![Two distributions with the same mean but different spread]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_spread_same_mean_diff_sd.png)

*Figure 2a: Two datasets with approximately the same mean but very different spread.*

![Box plot showing the IQR and outliers]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_boxplot_iqr_outliers.png)

*Figure 2b: The box plot shows the box containing the middle 50% of the data, the median lying inside the box, and the red points being potential outliers under the $$1.5 \times \text{IQR}$$ rule.*

## Visualization: Seeing the Story in the Data

Summary numbers are useful, but they cannot replace looking at the data. Visualization lets us see patterns, trends, and anomalies that summary statistics may miss. In Bayesian analysis, visualization is not only an initial exploration tool, but also the way we check models and communicate results.

### Histogram: Estimating the Distribution

A **histogram** is one of the most basic visualization tools. It divides the data into intervals (bins) and counts the number of observations in each interval. The height of each bar is proportional to the frequency (or density) of the data in that interval.

A histogram can be viewed as a rough estimate of the probability density function. As the amount of data grows and the bin width shrinks, the histogram approaches the true PDF of the distribution. This is the idea behind **kernel density estimation**, a more sophisticated technique for estimating the PDF from data.

An important question when drawing a histogram is: how many bins should we use? Too few bins lose detail, while too many bins create noise. There is no perfect answer, but rules such as Sturges' rule ($$k = \lceil \log_2 n \rceil + 1$$) or Scott's rule can provide a good starting point.

### Box Plot: The Five-Number Summary

A **box plot** is a way of visualizing five important summary statistics: the minimum, Q1, the median, Q3, and the maximum. The box contains the middle 50% of the data (from Q1 to Q3), the line inside the box is the median, and the "whiskers" extend to the extreme values (usually $$1.5 \times \text{IQR}$$ from the edges of the box). Points lying beyond the whiskers are drawn separately as potential outliers.

Box plots are especially useful for comparing multiple groups. We can draw several box plots side by side to compare the distributions of different groups, helping detect differences in central location, spread, and skewness.

### Scatter Plot: Exploring Relationships

When we have two variables, a **scatter plot** lets us see the relationship between them. Each point represents an observation, with x and y coordinates corresponding to the values of the two variables.

A scatter plot helps us answer questions such as: Are the two variables correlated? Is the relationship linear or nonlinear? Are there outliers or distinct groups? These questions are very important in Bayesian analysis, because they guide us in choosing a suitable model.

## Correlation: Measuring Linear Relationships

When we observe the relationship between two variables in a scatter plot, we usually want to quantify how strong that relationship is. The **Pearson correlation coefficient** provides a measure of linear relationships:

$$r = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}$$

The correlation coefficient always lies between -1 and 1. A value of $$r = 1$$ indicates a perfect positive linear relationship, $$r = -1$$ indicates a perfect negative linear relationship, and $$r = 0$$ indicates no linear relationship.

However, we must be careful when interpreting correlation. First, correlation only measures **linear** relationships. Two variables can have a strong nonlinear relationship but zero correlation. Second, **correlation does not imply causation**. Two variables being correlated does not mean one causes the other; there may be a hidden third variable affecting both, or the relationship may be due to chance.

*How to read the figure: The three figures below separate each type of relationship so you can see why a single correlation coefficient can hide many important things.*

![Positive linear relationship in a scatter plot]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_correlation_linear.png)

*Figure 3a: A positive linear relationship is a case that Pearson $$r$$ describes quite well.*

![Nonlinear relationship in a scatter plot]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_correlation_nonlinear.png)

*Figure 3b: A nonlinear relationship can be very clear by eye but Pearson $$r$$ underestimates it.*

![Correlation caused by a hidden group in a scatter plot]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_correlation_hidden_groups.png)

*Figure 3c: Correlation can appear because of a hidden group variable, so we should always look at the plot before trusting a summary coefficient.*

In Bayesian analysis, we usually model correlation explicitly through parameters in the model. For example, in Bayesian linear regression, the regression coefficient $$\beta$$ encodes the relationship between the predictor and the response variable, and we can quantify the uncertainty about this relationship through the posterior distribution of $$\beta$$.

---

### Worked Numerical Example: Watching One Outlier Hijack the Mean & SD While Median & IQR Hold Steady

Compare two tiny 5-person salary datasets (in thousands of dollars):
- **Clean sample:** `[40, 45, 50, 55, 60]`
- **Outlier sample:** `[40, 45, 50, 55, 500]`

| Summary Statistic | Clean Sample `[40,45,50,55,60]` | Outlier Sample `[40,45,50,55,500]` | Change Caused by 1 Outlier |
| :--- | :--- | :--- | :--- |
| **Mean ($$ar{x}$$)** | $$50.0$$ | $$138.0$$ | **$$+176\%$$ explosion!** |
| **Median ($$Q_2$$)** | $$50.0$$ | $$50.0$$ | **$$0\%$$ (unchanged!)** |
| **Sample SD ($$s$$)** | $$7.91$$ | $$202.4$$ | **$$25.6	imes$$ larger!** |
| **IQR ($$Q_3 - Q_1$$)** | $$55 - 45 = 10.0$$ | $$55 - 45 = 10.0$$ | **$$0\%$$ (unchanged!)** |

Look at `138 ± 202` on the outlier sample: it gives a lower bound of $$-64$$ thousand dollars—completely nonsensical—while `median = 50, IQR = 10` remains rock-solid!

### Explanation: Four Rules for Honest Data & Posterior Summaries

1. **Always pair a location statistic with a spread statistic:** A mean without SD (or median without IQR/quantiles) hides half the story.
2. **Compare mean vs. median as an instant skewness detector:** If `mean >> median`, you have a heavy right tail; investigate outliers or consider log-transforming before assuming Gaussianity.
3. **Plot the histogram or boxplot alongside numbers:** Summary numbers cannot detect bimodality (two distinct clusters with an empty middle!).
4. **Apply the same discipline to Bayesian posteriors:** For skewed parameters like variance $$\sigma^2$$ or small-sample rates, report posterior median and 95% equal-tailed or HDI credible intervals alongside the mean.

**Quick check.** If a dataset has 5 values `[10, 12, 14, 16, 18]` and you add `+100` to *every* single value, how do the mean, median, SD, and IQR change?

---

## Reference videos

- [StatQuest: Histograms, Clearly Explained](https://www.youtube.com/watch?v=qBigTkBLU6g) — StatQuest with Josh Starmer, English. **watch first**. Watch to see that a histogram is a way of telling the shape of the data before computing a single summary number, exactly the spirit of the lesson's opening.
- [Finding mean, median, and mode | Descriptive statistics | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=k3aKKasOmIw) — Khan Academy, English. Watch how the mean, median and mode answer different questions, supporting the part on measures of location.
- [Pearson's Correlation, Clearly Explained!!!](https://www.youtube.com/watch?v=xZ_z8KWkhXE) — StatQuest with Josh Starmer, English. Watch the Pearson correlation coefficient and its limits, used for the part of the lesson on measuring linear relationships.

## Exercises

**Exercise 1: Computing Descriptive Statistics.** Given the exam scores of 20 students: [45, 67, 78, 82, 55, 90, 88, 76, 95, 20, 85, 72, 68, 91, 77, 83, 65, 89, 74, 80]. (a) Compute the mean, median, and mode. (b) Compute the variance, standard deviation, and IQR. (c) Detect outliers using the $$1.5 \times \text{IQR}$$ rule. (d) Explain why the mean and median differ, and what this says about the distribution of the data.

**Exercise 2: Visualization and Interpretation.** Use Python to generate 1000 observations from: (a) The normal distribution $$\mathcal{N}(50, 10^2)$$. (b) The log-normal distribution with parameters $$\mu = 3.5, \sigma = 0.5$$. For each distribution, draw a histogram and box plot, compute the mean and median, and explain the difference between the two distributions based on the statistics and plots.

**Exercise 3: Correlation and Causation.** Consider two pairs of variables: (a) Ice cream sales and the number of drowning incidents (both are high in summer). (b) Hours of study and exam scores. For each pair, discuss: Are they correlated? Is there a causal relationship? If there is correlation but no causation, explain why. What does this teach us about interpreting correlation?

**Exercise 4: Identifying Distributions.** Given three datasets (you can generate them or use real data): (a) The heights of adults. (b) The number of emails received per day. (c) The waiting time between calls arriving at a call center. For each dataset, draw a histogram, compute descriptive statistics, and propose a suitable probability distribution (normal, Poisson, exponential, etc.). Explain the reasons for your choice.

**Exercise 5: Exploring Real Data.** Download a real dataset (for example: Iris, Boston Housing, or any dataset you are interested in). Carry out a complete exploratory data analysis: (a) Compute descriptive statistics for all numeric variables. (b) Draw histograms and box plots for the continuous variables. (c) Draw scatter plots and compute correlations for pairs of variables. (d) Detect and discuss outliers. (e) Write a short paragraph summarizing what you learned about the data, and propose distributions and models that might suit a Bayesian analysis.

## References

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 6: Model checking and improvement (posterior predictive checks)

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 3: The R Programming Language (data exploration)

### Supplementary Reading:

**Tukey, J. W. (1977).** *Exploratory Data Analysis*. Addison-Wesley.
- Classic text on EDA philosophy and techniques

**Wickham, H., & Grolemund, G. (2017).** *R for Data Science*. O'Reilly Media.
- Chapter 7: Exploratory Data Analysis

---

*Next lesson: [0.7 Basic Python for Data Science]({{ site.baseurl }}/contents/en/chapter00/00_04_python_basics/)*
