---
layout: post
title: "Lesson 0.1: Probability Foundations - The Language of Uncertainty"
chapter: '00'
order: 1
owner: Nguyen Le Linh
lang: en
categories:
- chapter00
lesson_type: required
---

Suppose a hospital screens 10,000 people for a rare condition that affects 1% of the population using a test with 99% sensitivity and 95% specificity. When a patient tests positive, most people—even experienced physicians—intuitively guess there is a 95% or 99% chance they have the disease. Yet the true probability is just **16.7%**! That jarring gap between gut instinct and mathematical reality is why **probability theory** is the indispensable foundation of Bayesian data analysis.

This opening lesson builds the exact grammar of uncertainty—sample spaces, conditional probability, independence, and the law of total probability—so that when Bayes’ theorem arrives in Chapter 1, every piece feels like transparent arithmetic rather than magic.

---

## Key ideas: Four Axiomatic Pillars Behind Bayesian Reasoning

Every Bayesian calculation in this entire course is built from just four elementary probability rules:

1. **Kolmogorov Axioms & Normalization:** Probabilities lie in $$[0,1]$$, mutually exclusive events add, and the total probability of the entire sample space equals $$1$$—the exact constraint that defines the normalizing constant (evidence) in Bayes’ rule.
2. **Conditional Probability & Product Rule:** Knowing event $$B$$ occurred shrinks the universe from $$\Omega$$ to $$B$$, giving $$P(A\mid B) = rac{P(A\cap B)}{P(B)}$$ and the product rule $$P(A\cap B) = P(A\mid B)P(B)$$.
3. **Law of Total Probability (Marginalization):** Partitioning uncertainty across all mutually exclusive hypotheses $$H_1,\dots,H_k$$ gives $$P(D) = \sum_i P(D\mid H_i)P(H_i)$$—the denominator of Bayes’ theorem!
4. **Independence vs. Conditional Independence:** Two events are independent when $$P(A\mid B)=P(A)$$. In Bayesian modeling, data points $$y_1,\dots,y_n$$ are rarely marginally independent, yet they *are* **conditionally independent given the parameter $$	heta$$**, letting likelihoods factor cleanly into products.

---

## Learning Objectives

After completing this lesson, you will understand that probability is not just a collection of computational formulas, but a complete mathematical language for describing, quantifying, and reasoning about uncertainty. You will firmly grasp the basic concepts of sample spaces, events, and the rules of probability, and understand why these concepts are an indispensable foundation for Bayesian inference. More importantly, you will begin to see probability as a way of encoding beliefs and updating those beliefs when new information arrives.

## Introduction: Why Do We Need Probability?

In the real world, we rarely have perfect information. A doctor diagnoses a disease based on unclear symptoms. A scientist tries to infer natural laws from noisy data. An engineer designs a system that must work well even when environmental conditions change unpredictably. In all of these situations, uncertainty is not a nuisance to be eliminated, but a fundamental feature of the problem that needs to be modeled and managed in a principled way.

Probability gives us the mathematical language to do this. It lets us **quantify the degree of belief** in different propositions, combine information from many sources, and make rational decisions even when we cannot be certain about the outcome. **In this course on Bayesian data analysis, probability is not only a computational tool but also the way we think about data, models, and inference.**

Before we can use probability for Bayesian inference, we need to understand its foundations well. This lesson will build the basic concepts carefully, not only so that you can compute probabilities, but also so that you understand the meaning of those numbers and how they connect to statistical inference.

## Sample Spaces and Events: Describing What Can Happen

Every probability analysis begins by clearly identifying what can happen. We call the set of all possible outcomes of an experiment or random process the **sample space**, usually denoted $$\Omega$$. Each element of the sample space represents a specific, complete, and distinguishable outcome.

Consider a simple example: flipping a fair coin. The sample space here is $$\Omega = \{\text{Tails}, \text{Heads}\}$$. Each time we flip, we observe one of these two outcomes, and no other outcome can occur. The simplicity of this example should not obscure its importance: identifying the sample space precisely is the first and most important step in every probability analysis.

In many real situations, the sample space can be much more complicated. If we flip the coin twice, the sample space becomes $$\Omega = \{TT, TH, HT, HH\}$$, where $$T$$ is Tails and $$H$$ is Heads. If we measure the height of a randomly chosen person, the sample space is the set of all possible positive values (in practice, limited by biological constraints), and this is a continuous space rather than a discrete one.

Once we have identified the sample space, we can talk about **events**. An event is a subset of the sample space, representing a set of outcomes that we care about. For example, in the experiment of flipping a coin twice, the event "at least one Tails" corresponds to the set $$\{TT, TH, HT\}$$. The event "both flips are Tails" corresponds to the set $$\{TT\}$$.

Defining events as subsets of the sample space may seem abstract, but it allows us to use set theory to reason about probability. We can talk about the union of two events (at least one of the two occurs), the intersection of two events (both occur together), and the complement of an event (that event does not occur). These operations will correspond directly to the probability rules we will discuss next.

## Defining Probability: From Frequency to Belief

**There are many ways to understand what probability is**, and how we understand it deeply affects how we use it. In this course, we will mainly work with the **Bayesian view of probability**, but first let us look at the traditional **frequentist view** to understand the difference.

According to the frequentist view, the probability of an event is defined as the relative frequency with which that event occurs when we repeat the experiment infinitely many times. If we flip a fair coin many times, the proportion of Tails will approach $$0.5$$ as the number of flips increases. **This is an objective and easy-to-understand definition, but it has an important limitation: it only makes sense for events that can be repeated many times. We cannot talk about "the probability of rain tomorrow" or "the probability that a scientific hypothesis is true" in the frequentist sense, because these events cannot be repeated under identical conditions.**

The **Bayesian view of probability** is broader and more flexible. In this view, probability is a measure of the **degree of belief** or the **plausibility** of a proposition, based on available information. A probability of $$0$$ means we are completely certain that the proposition is false, a probability of $$1$$ means we are completely certain that it is true, and values in between express different degrees of uncertainty. Importantly, **Bayesian probability can change as we gather more information, and this is exactly the basis of Bayesian inference.**

However we understand probability, it must follow some basic mathematical rules to ensure consistency. These rules, called the probability axioms, are the foundation of all of probability theory.

## The Probability Axioms: The Rules of the Game

For probability to be a useful mathematical tool, it must obey some basic rules. These rules, formalized by the Russian mathematician Andrey Kolmogorov in 1933, define what we can and cannot do with probability.

**Axiom 1: Non-negativity.** The probability of any event is non-negative. For every event $$A$$, we have $$P(A) \geq 0$$. This is intuitive: we cannot have a "negative probability" for an event. A probability of zero means the event definitely does not occur.

**Axiom 2: Normalization.** The probability of the whole sample space is $$1$$. In other words, $$P(\Omega) = 1$$. This reflects the fact that one of the possible outcomes must occur. We are completely certain that *something* will happen, even when we are not sure *what* will happen.

**Axiom 3: Additivity.** If two events $$A$$ and $$B$$ are **mutually exclusive**, meaning they cannot occur together ($$A \cap B = \emptyset$$), then the probability of their union equals the sum of the individual probabilities: $$P(A \cup B) = P(A) + P(B)$$. This extends to any finite or countable collection of mutually exclusive events.

These three axioms may seem simple, but they have profound consequences. From them, we can derive all the other probability rules we will need. For example, we can prove that the probability of the complement event $$A^c$$ (the event that $$A$$ does not occur) is $$P(A^c) = 1 - P(A)$$. To see this, note that $$A$$ and $$A^c$$ are mutually exclusive and their union is the whole sample space, so $$P(A) + P(A^c) = P(\Omega) = 1$$.

Another important consequence is the **general addition rule** for any two events (not necessarily mutually exclusive):

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

We must subtract $$P(A \cap B)$$ because otherwise we would count the outcomes in both $$A$$ and $$B$$ twice. This formula is analogous to the inclusion-exclusion principle in set theory, and it illustrates the deep connection between probability and set theory.

## Conditional Probability: Updating Beliefs with New Information

One of the most important concepts in probability theory, and especially important for Bayesian inference, is **conditional probability**. This is the probability of an event, given that we know another event has occurred.

Suppose we are interested in the probability of event $$A$$, but we know that event $$B$$ has occurred. How does this information change our assessment of how likely $$A$$ is? The conditional probability of $$A$$ given $$B$$, denoted $$P(A \mid B)$$, is defined as:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$$

provided $$P(B) > 0$$.

This definition has a clear intuition. When we know that $$B$$ has occurred, the space of possible outcomes shrinks to only the outcomes in $$B$$. In this shrunken space, the probability of $$A$$ is proportional to the probability that both $$A$$ and $$B$$ occur, normalized by the probability of $$B$$ to ensure that the total probability in the new space is still $$1$$.

Consider a concrete example. Suppose we flip a fair coin twice. The sample space is $$\{TT, TH, HT, HH\}$$, and each outcome has probability $$1/4$$. The probability of the event "both flips are Tails" ($$A = \{TT\}$$) is $$P(A) = 1/4$$. But suppose we are told that "at least one Tails" ($$B = \{TT, TH, HT\}$$). With this information, the conditional probability of $$A$$ given $$B$$ is:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{P(\{TT\})}{P(\{TT, TH, HT\})} = \frac{1/4}{3/4} = \frac{1}{3}$$

Notice that the probability increases from $$1/4$$ to $$1/3$$ when we learn additional information. This is a simple example of updating beliefs based on new evidence, a central idea in Bayesian inference.

### A Variant That Is Easy to Confuse

Still with two coin flips, let us compare two different conditions:

- If we know **at least one flip is Tails**, the probability that both flips are Tails is $$1/3$$.
- But if we know **the first flip is Tails**, the probability that both flips are Tails is $$1/2$$.

The two problems sound quite similar, but the conditioning information is not the same, so the conditional probability also differs. This is a very important lesson: in probability, the meaning of "knowing additional information" depends entirely on which possibilities the conditioning event has removed from the sample space.

From the definition of conditional probability, we can derive the **multiplication rule**:

$$P(A \cap B) = P(A \mid B) \cdot P(B) = P(B \mid A) \cdot P(A)$$

This rule gives us two different ways to compute the probability of the intersection of two events, and their equivalence will lead to one of the most important formulas in statistics: Bayes' theorem.

## Independence: When Information Does Not Change Beliefs

Two events $$A$$ and $$B$$ are called **independent** if knowing that one occurs does not change the probability of the other. Formally, $$A$$ and $$B$$ are independent if and only if:

$$P(A \mid B) = P(A)$$

or equivalently:

$$P(A \cap B) = P(A) \cdot P(B)$$

Independence is a strong assumption and is often untrue in practice, but it significantly simplifies probability computations and is the foundation of many statistical models. For example, when we flip a coin many times, we usually assume the flips are independent of each other, meaning the outcome of one flip does not affect the probabilities of subsequent flips.

However, in many real situations, events are not independent. If we draw two cards from a deck without replacement, the outcome of the second draw depends on the first. If we observe the temperature on two consecutive days, they tend to be correlated with each other. Recognizing and modeling these dependencies is an important part of Bayesian data analysis.

## Conditional Independence: When Dependence Vanishes Once the Latent Variable Is Known

There is a more subtle situation than ordinary independence: two events may **not be independent when viewed globally**, but become independent once we know an additional latent variable $$C$$.

We say $$A$$ and $$B$$ are **conditionally independent given $$C$$** if:

$$
P(A \cap B \mid C) = P(A \mid C)P(B \mid C).
$$

The intuition is this:

When we do not know $$C$$, we are mixing several different data-generating mechanisms into a single picture; once we know $$C$$, we know exactly which mechanism we are in; and within each individual mechanism, $$A$$ and $$B$$ may no longer influence each other.

For example, suppose we randomly choose one of two coins:

The first coin is fair, while the second coin always lands heads.

Then we flip the chosen coin twice. Let:

Let $$C$$ be the event "coin 1 was chosen", $$A$$ the event "the first flip lands heads", and $$B$$ the event "the second flip lands heads".

If we **know in advance which coin was chosen**, the two flips are conditionally independent:

Under the fair coin, each flip is independent with probability of heads equal to $$1/2$$; under the always-heads coin, the two flips are still independent in the sense that both are certain to land heads.

But if we **do not know** which coin was chosen, then $$A$$ and $$B$$ are no longer independent in the ordinary sense. The reason is that the outcome of the first flip reveals information about which kind of coin we are holding, and that information changes our belief about the second flip.

This is a very important idea in Bayes:

Dependence does not always come from variables "directly affecting" each other; sometimes it appears simply because we do not yet know a latent variable that governs both at once.

When you move on to mixture models, hierarchical models or causal graphs, you will meet this idea again many times.

## The Law of Total Probability: Divide and Compute

Sometimes, the easiest way to compute the probability of an event is to split it into simpler cases. The **law of total probability** lets us do this systematically.

Suppose we have a partition of the sample space into mutually exclusive events $$B_1, B_2, \ldots, B_n$$ such that $$\bigcup_{i=1}^n B_i = \Omega$$. This means every outcome belongs to exactly one of the $$B_i$$. Then the probability of any event $$A$$ can be computed by:

$$P(A) = \sum_{i=1}^n P(A \mid B_i) \cdot P(B_i)$$

This formula says that to compute $$P(A)$$, we can consider each case $$B_i$$, compute the probability of $$A$$ in that case ($$P(A \mid B_i)$$), multiply by the probability of that case ($$P(B_i)$$), and add everything up.

This rule is especially useful in hierarchical models, where we have **latent variables that are not directly observed**. In Bayesian inference, we often use this rule to "marginalize out" nuisance parameters, focusing on what we really want to infer.

## Implications for Bayesian Inference

All the concepts we have discussed in this lesson are not merely abstract theory. They are the foundation on which all of Bayesian data analysis is built.

**In Bayesian inference, we will use conditional probability to update beliefs about model parameters as we observe data. We will use the law of total probability to marginalize out nuisance parameters. We will use the probability axioms to ensure that our inferences are consistent and sensible.**

More importantly, we will apply the Bayesian view of probability as **degree of belief**. This lets us talk about "the probability of a hypothesis" or "the probability of a parameter value", concepts that have no meaning in frequentist statistics but are very natural and useful in Bayesian statistics.

As you progress through this course, you will see that every Bayesian tool, from the simple Bayes' theorem to complex hierarchical models, is built from the basic probability principles we have discussed here. Understanding these foundations deeply will help you not only apply Bayesian methods correctly, but also understand why they work and when they may fail.

---

### Worked Numerical Example: Solving the Rare-Disease Screening Paradox by Hand

Consider a population of $$10{,}000$$ people with disease prevalence $$P(D) = 0.01$$ ($$100$$ sick, $$9{,}900$$ healthy), test sensitivity $$P(+\mid D) = 0.99$$, and false-positive rate $$P(+\mid 
eg D) = 0.05$$:

| Group | Population Count | Positive Test (`+`) | Negative Test (`-`) |
| :--- | :--- | :--- | :--- |
| **Has Disease ($$D$$)** | $$100$$ | $$100 	imes 0.99 = \mathbf{99}$$ | $$1$$ |
| **Healthy ($$
eg D$$)** | $$9{,}900$$ | $$9{,}900 	imes 0.05 = \mathbf{495}$$ | $$9{,}405$$ |
| **Total** | $$10{,}000$$ | **$$594$$** | $$9{,}406$$ |

Read the exact conditional probability straight off the `+` column:

$$P(D \mid +) = rac{99}{99 + 495} = rac{99}{594} = rac{1}{6} pprox \mathbf{16.67\%}!$$

Even with a 99%-accurate test, five out of six positive results are false alarms because healthy people outnumber sick people 99-to-1!

### Explanation: Four Rules to Never Misfire on Conditional Probability

1. **Never confuse $$P(A\mid B)$$ with $$P(B\mid A)$$:** Confusing $$P(+\mid D) = 99\%$$ with $$P(D\mid +) = 16.7\%$$ is the *base-rate fallacy*—the #1 statistical error in medicine, law, and machine learning.
2. **Always check the denominator (marginal evidence):** Conditioning replaces the whole sample space with the slice where the observed evidence holds (`594` positive tests, not `10,000` people).
3. **Distinguish mutually exclusive from independent:** If $$A$$ and $$B$$ are mutually exclusive (and have positive probability), knowing $$A$$ happened guarantees $$B$$ did *not*—making them maximally *dependent*, not independent!
4. **Convert probabilities into natural counts of 10,000 when stuck:** A 2×2 frequency table turns abstract conditional formulas into effortless mental arithmetic.

**Quick check.** If the same patient takes a *second*, conditionally independent test (same 99% sensitivity, 5% false-positive rate) and tests positive *again*, does $$P(D \mid +, +)$$ jump above 75%? *(Hint: update the prior from $$1\%$$ to $$16.67\%$$!)*

---

## Reference videos

- [The Main Ideas behind Probability Distributions](https://www.youtube.com/watch?v=oI3hZJqXJuc) — StatQuest with Josh Starmer, English. **watch first**. Watch to read a distribution as a story about degrees of certainty, exactly the opening part where the lesson treats probability as the language of uncertainty.
- [Conditional Probabilities, Clearly Explained!!!](https://www.youtube.com/watch?v=_IgyaD7vOOA) — StatQuest with Josh Starmer, English. Watch the part on conditional probability, since that is the computation the lesson uses to go from the sample space to inference once new information is available.
- [Random variables | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=3v9w79NhsfI) — Khan Academy, English. Watch how random variables are defined, supporting the part that distinguishes observed outcomes from still-unknown quantities.

## Exercises

**Exercise 1: Basic Probability.** A box contains 5 red marbles, 3 blue marbles, and 2 yellow marbles. We draw one marble at random. (a) Determine the sample space. (b) Compute the probability of drawing a red marble. (c) Compute the probability of drawing a marble that is not yellow. Explain your reasoning in words, not just formulas.

**Exercise 2: Conditional Probability.** In a class, 60% of students study Python, 40% study R, and 25% study both. (a) If a student is chosen at random and we know the student studies Python, what is the probability that the student also studies R? (b) Are the events "studies Python" and "studies R" independent? Explain using both computation and intuition.

**Exercise 3: The Law of Total Probability.** A company manufactures products at three factories A, B, and C with production shares of 50%, 30%, and 20% respectively. The defect rates from each factory are 2%, 3%, and 5% respectively. (a) Compute the probability that a randomly chosen product is defective. (b) If a product is found to be defective, what is the probability it came from factory C? (Hint: Part (b) requires Bayes' theorem, which we will study in the next lesson, but try to reason intuitively.)

**Exercise 4: Simpson's Paradox.** Consider two treatments A and B tested on two groups of patients: a mild-illness group and a severe-illness group. In the mild group, A succeeds 90/100 times and B succeeds 85/90 times. In the severe group, A succeeds 20/100 times and B succeeds 15/110 times. (a) In each group, which treatment has the higher success rate? (b) Compute the overall success rate of each treatment. (c) Explain why the result seems paradoxical. What does this teach us about the importance of considering latent variables?

**Exercise 5: Reflections on Probability.** Write a short paragraph (200-300 words) explaining the difference between the frequentist view and the Bayesian view of probability. Give an example of a situation where the Bayesian view seems more natural, and explain why. Reflect on how the way we understand probability can affect how we design experiments and interpret results.

## References

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 1: Probability and inference
- Appendix A: Standard probability distributions

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 4: What is This Stuff Called Probability?

### Supplementary Reading:

**Jaynes, E. T. (2003).** *Probability Theory: The Logic of Science*. Cambridge University Press.
- Chapters 1-2: Plausible reasoning and quantitative rules

---

*Next lesson: [0.2 Bernoulli and Binomial]({{ site.baseurl }}/contents/en/chapter00/00_02_01_bernoulli_binomial/)*
