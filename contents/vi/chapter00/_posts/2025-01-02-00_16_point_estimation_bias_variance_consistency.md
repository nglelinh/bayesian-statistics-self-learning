---
layout: post
title: "Bài 0.18: Ước lượng điểm, Bias-Variance, Consistency"
chapter: '00'
order: 18
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu ba tiêu chí cốt lõi để đánh giá một bộ ước lượng (estimator): độ chệch (bias), phương sai (variance) và tính nhất quán (consistency), đồng thời nắm được sự đánh đổi độ chệch – phương sai (bias–variance tradeoff) như một nguyên lý thực hành khi thiết kế mô hình.

## Giới thiệu: Đánh giá ước lượng không thể chỉ nhìn một mẫu duy nhất

Một bộ ước lượng tốt không chỉ cho kết quả "gần đúng" trong một lần lấy mẫu ngẫu nhiên. Ta cần xem xét hành vi của nó trên nhiều mẫu khả dĩ: có lệch có hệ thống không, có dao động quá mạnh giữa các mẫu không, và khi cỡ mẫu tăng lên thì có hội tụ về giá trị thật không. Ba tiêu chí bias, variance và consistency được xây dựng để trả lời ba câu hỏi này.

![Bias variance tradeoff]({{ site.baseurl }}/img/chapter_img/chapter00/bias_variance_tradeoff_curve.png)

*Hình 1: Khi độ phức tạp mô hình tăng, độ chệch (bias) giảm dần nhưng phương sai (variance) tăng lên, khiến sai số bình phương trung bình (MSE) đạt cực tiểu tại một điểm cân bằng.*

## 1) Ước lượng điểm là gì?

Ước lượng điểm (point estimator) là một hàm của dữ liệu $$\hat\theta=g(x_1,\dots,x_n)$$ dùng để đưa ra một giá trị ước lượng cụ thể cho tham số chưa biết $$\theta$$. Ví dụ, ta dùng trung bình mẫu $$\bar X$$ để ước lượng $$\mu$$, tỷ lệ mẫu $$\hat p$$ để ước lượng $$p$$, hoặc hệ số hồi quy mẫu để ước lượng độ dốc thật.

## 2) Độ chệch (Bias)

Độ chệch đo sai lệch có hệ thống của bộ ước lượng so với giá trị thật:

$$
\mathrm{Bias}(\hat\theta)=\mathbb{E}[\hat\theta]-\theta
$$

Nếu $$\mathrm{Bias}(\hat\theta) = 0$$, bộ ước lượng được gọi là không chệch (unbiased); nếu khác 0, bộ ước lượng có xu hướng lệch hệ thống về một phía.

## 3) Phương sai (Variance) của bộ ước lượng

Ngay cả một bộ ước lượng không chệch vẫn có thể dao động mạnh từ mẫu này sang mẫu khác. Mức độ dao động đó được đo bằng phương sai $$\mathrm{Var}(\hat\theta)$$. Vì vậy, một bộ ước lượng tốt không chỉ cần ít chệch mà còn cần phương sai đủ nhỏ.

## 4) MSE và phân rã độ chệch – phương sai

Sai số bình phương trung bình (Mean Squared Error — MSE):

$$
\mathrm{MSE}(\hat\theta)=\mathbb{E}[(\hat\theta-\theta)^2]
$$

được phân rã thành hai thành phần:

$$
\mathrm{MSE}(\hat\theta)=\mathrm{Bias}(\hat\theta)^2+\mathrm{Var}(\hat\theta)
$$

Đẳng thức này là nền tảng cho tư duy điều chuẩn (regularization): chấp nhận một chút độ chệch để đổi lấy mức giảm phương sai lớn hơn, qua đó hạ tổng sai số dự báo.

### 4.1) Một ví dụ cụ thể về đánh đổi bias – variance

Giả sử cần ước lượng tham số thật $$\theta = 10$$ bằng hai bộ ước lượng:

- Bộ ước lượng A không chệch ($$\mathrm{Bias}=0$$) nhưng có phương sai bằng $$9$$.
- Bộ ước lượng B chệch lên 1 đơn vị ($$\mathrm{Bias}=1$$) nhưng có phương sai chỉ bằng $$4$$.

Khi đó:

$$
\mathrm{MSE}(A) = 0^2 + 9 = 9,
\qquad
\mathrm{MSE}(B) = 1^2 + 4 = 5.
$$

Dù có độ chệch, bộ ước lượng B vẫn đạt MSE thấp hơn vì giảm được phương sai đáng kể. Đây chính là nguyên lý đứng sau các kỹ thuật co rút (shrinkage) và điều chuẩn (regularization).

## 5) Tính nhất quán (Consistency)

Bộ ước lượng $$\hat\theta_n$$ được gọi là nhất quán (consistent) nếu nó hội tụ theo xác suất về giá trị thật khi cỡ mẫu tiến ra vô cùng:

$$
\hat\theta_n \xrightarrow[]{P} \theta \quad \text{khi } n\to\infty
$$

Nói đơn giản, khi lượng dữ liệu ngày càng lớn, ước lượng sẽ càng tiến sát tham số thật.

## 6) Liên hệ với thống kê Bayesian

Trong thống kê Bayesian, ta làm việc với toàn bộ phân phối hậu nghiệm thay vì chỉ một ước lượng điểm. Dù vậy, góc nhìn bias–variance vẫn rất hữu ích: một phân phối tiên nghiệm mạnh thường giúp giảm phương sai ước lượng nhưng có thể kéo theo độ chệch nếu tiên nghiệm đặt lệch; ngược lại, tiên nghiệm yếu ít gây chệch nhưng có thể khiến phương sai lớn khi dữ liệu còn ít.

## Tóm tắt nhanh

1. Độ chệch (bias) đo sai lệch hệ thống của bộ ước lượng.
2. Phương sai (variance) đo độ dao động của bộ ước lượng giữa các mẫu.
3. $$\mathrm{MSE} = \mathrm{Bias}^2 + \mathrm{Var}$$.
4. Tính nhất quán (consistency) mô tả sự hội tụ về giá trị thật khi cỡ mẫu lớn.

## Video tham khảo

- [Unbiasedness vs consistency of estimators - an example](https://www.youtube.com/watch?v=6i7mqDJICzQ) — Ben Lambert, English. **Xem trước.** Minh họa sự khác nhau giữa tính không chệch và tính nhất quán của bộ ước lượng.
- [[Proof] MSE = Variance + Bias²](https://www.youtube.com/watch?v=qmVT35gFW-Q) — math et al, English. Trình bày phép chứng minh phân rã MSE thành bình phương độ chệch cộng phương sai.
- [Population and Estimated Parameters, Clearly Explained!!!](https://www.youtube.com/watch?v=vikkiwjQqfU) — StatQuest with Josh Starmer, English. Giải thích mối liên hệ giữa tham số quần thể và ước lượng mẫu khi cỡ mẫu thay đổi.

## Câu hỏi tự luyện

1. Một bộ ước lượng có độ chệch nhỏ nhưng MSE lớn có thể xảy ra không? Vì sao?
2. Vì sao điều chuẩn (regularization) có thể cải thiện chất lượng dự báo dù làm xuất hiện độ chệch?
3. Tính nhất quán có bảo đảm bộ ước lượng hoạt động tốt trên mẫu nhỏ không?

## Tài liệu tham khảo

- Casella, G., & Berger, R. (2002). *Statistical Inference*.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*.

---

*Bài học tiếp theo: [0.19 Log-probability và Ổn định số]({{ site.baseurl }}/contents/vi/chapter00/00_17_log_probability_numerical_stability/)*
