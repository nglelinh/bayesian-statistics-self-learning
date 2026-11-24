---
layout: post
title: "Lesson 1.5: Modern Applications of Bayes' Theorem in Computer Science"
chapter: '01'
order: 5
owner: Nguyen Le Linh
lang: en
categories:
- chapter01
lesson_type: optional
---

Thomas Bayes sketched his theorem in the 1760s using billiard balls on a flat table; two and a half centuries later, that exact equation is quietly running inside **self-driving car sensor fusion (Kalman & Particle Filters)**, **email spam filters**, **Thompson Sampling bandits** routing millions of ads and recommendations, and **Bayesian Optimization** tuning billion-dollar neural-network hyperparameters!

This optional bridge shows how Bayes’ theorem powers modern computer science systems in 2022–2026—where uncertainty isn’t an academic nuisance, it is the exact signal algorithms use to **explore vs. exploit**.

---

## Background Knowledge Map: Three Ways Bayes’ Theorem Ships in Computer Science

1. **Sequential Filtering (Robotics & Tracking):** Kalman filters (exact linear-Gaussian Bayes) and Particle filters fuse noisy GPS + LiDAR + IMU streams every 20 milliseconds by turning the previous millisecond’s posterior into the next millisecond’s prior.
2. **Thompson Sampling (Multi-Armed Bandits):** Instead of wasting 50% of traffic on a losing A/B variant for weeks, Thompson Sampling samples $$\theta_k \sim \mathrm{Beta}(\alpha_k, \beta_k)$$ for each arm and plays the winner—automatically shifting traffic toward better options while keeping exploration alive!
3. **Bayesian Optimization (Hyperparameter & Drug Discovery):** Fits a Gaussian Process posterior over an expensive black-box objective and queries the next point maximizing Expected Improvement (EI)—cutting expensive GPU/lab trials by 5–10×.

---

## Learning objectives

After this optional lesson, you no longer see Bayes' theorem as a diagnostic formula in a textbook, but as a rule for updating beliefs that is running inside spam filtering, fraud detection, and the quantification of uncertainty in language models. What needs to change is the question: not "how is the formula written?", but "where do the prior, likelihood and posterior sit in a real system?".

## Prerequisites

This lesson builds on lessons 1.1–1.4. It does not rewrite the critique of the p-value or the Bayesian–frequentist comparison. It only brings the same updating diagram into recent computer science products.

## Introduction

Chapter 1 created a tension: the p-value answers a question that users usually do not ask, while the decision really needs the probability of a hypothesis after the data. Spam filters, payment gateways, and chatbots all live in exactly that tension. They must turn a new observation—an email, a transaction, a generated answer—into an updated belief honest enough to act on. If there is only a ranking score, the system still does not know whether it should stay silent or raise a warning.

## Conceptual development

Bayes' theorem,

$$
P(H\mid D)=\frac{P(D\mid H)P(H)}{P(D)},
$$

is still the same multiplication of prior by likelihood followed by normalization. In a product, $$H$$ can be "spam", "fraudulent transaction", or "the answer just generated is correct". $$D$$ is the observed evidence. The hard part is not the algebra, but a skewed prior (the spam base rate changes with the season) and a likelihood being read as if it were already the posterior.

## Models as generative stories

### 1. Spam, scams and calibrated classification

The classic generative story of Naive Bayes is still alive: each token is treated as conditional evidence about the spam label, and then the likelihoods are multiplied under an independence assumption. Modern systems replace the dictionary with denser representations, but the Bayesian question does not change. The prior is the base rate of spam; the likelihood is "under which label does an email like this appear more often?"; the posterior is the probability that the email is spam *after having read the content*. If the action threshold ignores the base rate, you are using the likelihood as if it were already the posterior—exactly the mistake that lesson 1.3 warns about in medical diagnosis.

### 2. Payment fraud as updating under an extremely low base rate

Fraud is rare. The prior $$P(H)$$ is therefore very small, so a "suspicious-looking" signal can still leave a moderate posterior. That is the industrial version of the rare-disease test paradox. An honest system must keep the base rate in the formula, and then act only when the posterior exceeds a threshold set by the cost of misses and false alarms. A high ranking score is not yet an updated belief.

### 3. Language models evaluating their own answers

Kadavath et al. (2022) ask a very Bayesian question: after a model proposes an answer, what is the probability $$P(\text{True})$$ that the answer is correct? They find that large models can be well calibrated on formatted true/false tasks, and that looking at many self-generated samples before evaluating one candidate helps self-evaluation. Kuhn, Gal and Farquhar (2023) point out a new bottleneck: in language, many sentences differ in wording but share the same meaning, so entropy over token strings is not entropy over hypotheses. Semantic entropy groups sentences of equivalent meaning and only then measures uncertainty—that is, it measures the posterior over the space of hypotheses, not over the space of character strings.

### 4. Asking the model for calibrated confidence

Tian et al. (2023) show that, for models fine-tuned with human feedback, verbalized probabilities ("I am 70% sure") are sometimes better calibrated than the conditional probabilities on tokens. This does not turn a chatbot into a Bayesian sampler, but it shows that products are trying to extract a posterior that users can read as plausibility. If that number does not match the true frequency of being correct, we are repeating the interpretation crisis with which Chapter 1 began.

## Interpretation and insight

The posterior in these systems answers "how credible is this hypothesis after the evidence?". It does not answer "the algorithm has rejected the alternative hypothesis". A high $$P(\text{True})$$ on a hallucinated answer can still occur if the likelihood is too optimistic. Bayes does not protect us from a wrong likelihood; it only forces us to say clearly where the prior is being pulled by the data.

## Applications

The three domains—spam/scams, fraud, and language uncertainty—are all decision problems under skewed base rates and asymmetric costs. They directly prepare for the decision analysis of Chapter 8, but can already be understood with Bayes' theorem alone.

## Limitations and extensions

Naive Bayes with independent words is a crude generative story. Semantic entropy needs a model of meaning equivalence, which is itself uncertain. Calibration on one benchmark does not guarantee calibration after a distribution shift. This lesson deliberately does not rewrite updating theory; Chapter 2 will turn that diagram into an explicit likelihood, prior and posterior.

---

### Worked Numerical Example: One Step of a Naive Bayes Spam Filter in Log-Odds

Suppose 20% of incoming emails are Spam ($$\text{prior odds} = \frac{0.20}{0.80} = 0.25$$). An email contains the word `"lottery"`, which appears in 40% of Spam emails ($$P(\text{"lottery"}\mid\text{Spam}) = 0.40$$) but only 1% of Ham emails ($$P(\text{"lottery"}\mid\text{Ham}) = 0.01$$):

1. **Likelihood Ratio (Bayes Factor):**
   $$\mathrm{LR} = \frac{0.40}{0.01} = \mathbf{40}.$$
2. **Posterior Odds = Prior Odds $$\times$$ Likelihood Ratio:**
   $$\text{Posterior Odds} = 0.25 \times 40 = \mathbf{10.0} \quad (\text{10-to-1 in favor of Spam!}).$$
3. **Convert back to probability:**
   $$P(\text{Spam} \mid \text{"lottery"}) = \frac{10}{10 + 1} = \frac{10}{11} \approx \mathbf{90.9\%}!$$

### Deep-Dive Explanation: Four Takeaways on Bayesian Algorithms in CS (Read Slowly)

1. **Odds form makes sequential updates pure multiplication (or log-addition):** Every new word or sensor reading simply adds $$\ln(\mathrm{LR})$$ to the running log-odds!
2. **Uncertainty drives smart exploration:** In Thompson Sampling and Bayesian Optimization, *high posterior variance* is a feature—it tells the agent where learning has the highest payoff.
3. **Naive independence assumptions still rank accurately:** Even when words in Naive Bayes are correlated, the *decision ranking* often remains strong—though raw probabilities become overconfident and need calibration.
4. **Always pair online Bayesian bandits with guardrails:** Delayed reward feedback and non-stationary traffic require windowed or discounted updates so stale posteriors don’t lock onto yesterday’s winner.

**Quick check.** In the Naive Bayes spam example above, if the email *also* contains the word `"invoice"` with $$P(\text{"invoice"}\mid\text{Spam}) = 0.05$$ and $$P(\text{"invoice"}\mid\text{Ham}) = 0.25$$ ($$\mathrm{LR} = 0.20$$), what are the new posterior odds and posterior spam probability?

---

## Reference videos

- [Naive Bayes từ A-Z: Trực Giác đến Toán Học](https://www.youtube.com/watch?v=SqW_p3311yY) — Gà AI, Vietnamese. **watch first**. Watch Naive Bayes from intuition to formula, exactly the part of the lesson that places the spam filter in the prior–likelihood–posterior diagram.
- [Bayes Rule Example of Spam Filter](https://www.youtube.com/watch?v=bc-SL86azrc) — Eric Walden, English. Watch an email having its spam probability updated with each piece of evidence, supporting the shifting-base-rate example.
- [MIT 6.S191: Uncertainty in Deep Learning](https://www.youtube.com/watch?v=veYq6EWZyVc) — Alexander Amini, English. Watch the uncertainty of deep learning models; the video does not discuss semantic entropy, but supports the part of the lesson about not reading token scores as the posterior of a hypothesis.

## Exercises

1. The spam rate rises from 5% to 30% during the holiday season. The likelihood of a keyword does not change. How does the posterior of an email containing that keyword change, and why will a filter that uses only the keyword score fail?
2. A payment gateway reports "fraud score 0.95". Which two further questions would you ask before closing the transaction, one about the prior and one about the decision threshold?
3. Why can entropy over answers that differ in wording exaggerate uncertainty compared with entropy over meanings? Take a question that has two correct ways of being phrased.
4. Compare Kadavath et al.'s $$P(\text{True})$$ with the posterior $$P(H\mid D)$$ in the diagnostic example of lesson 1.3. What plays the role of the prior?

## References

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 1.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 4–5.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. [arXiv:2207.05221](https://arxiv.org/abs/2207.05221).
- Kuhn, L., Gal, Y., & Farquhar, S. (2023). Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. *ICLR*. [arXiv:2302.09664](https://arxiv.org/abs/2302.09664).
- Tian, K., et al. (2023). Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. [arXiv:2305.14975](https://arxiv.org/abs/2305.14975).
