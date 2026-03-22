---
layout: post
title: "Bài 0.19: Ước lượng điểm, Bias-Variance, Consistency"
chapter: '00'
order: 19
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu ba tiêu chí cốt lõi để đánh giá estimator: bias, variance, consistency; đồng thời nắm được bias-variance tradeoff như một nguyên lý thiết kế mô hình thay vì một khẩu hiệu.

![Bias variance tradeoff]({{ site.baseurl }}/img/chapter_img/chapter00/bias_variance_tradeoff_curve.png)
*Hinh 1: Bias giam dan khi do phuc tap tang, variance tang dan, va MSE co diem can bang toi uu.*

## 1) Ước lượng điểm là gì?

Ước lượng điểm là một hàm của dữ liệu $$\hat\theta=g(x_1,\dots,x_n)$$ dùng để dự đoán giá trị tham số chưa biết $$\theta$$.

Ví dụ:

Ta có thể dùng $$\bar X$$ để ước lượng $$\mu$$, dùng tỷ lệ mẫu $$\hat p$$ để ước lượng $$p$$, hoặc dùng hệ số hồi quy mẫu để ước lượng slope thật.

## 2) Bias

Bias đo sai lệch hệ thống:

$$
\mathrm{Bias}(\hat\theta)=\mathbb{E}[\hat\theta]-\theta
$$

Khi bias bằng 0, estimator là không chệch; còn khi bias khác 0, estimator có xu hướng lệch có hệ thống về một phía.

## 3) Variance của estimator

Ngay cả estimator không chệch vẫn có thể dao động mạnh giữa các mẫu khác nhau. Dao động đó được đo bằng $$\mathrm{Var}(\hat\theta)$$.

Estimator tốt không chỉ cần ít bias mà còn cần variance hợp lý.

## 4) MSE và bias-variance decomposition

Sai số bình phương kỳ vọng:

$$
\mathrm{MSE}(\hat\theta)=\mathbb{E}[(\hat\theta-\theta)^2]
$$

phân rã thành:

$$
\mathrm{MSE}(\hat\theta)=\mathrm{Bias}(\hat\theta)^2+\mathrm{Var}(\hat\theta)
$$

Đây là nền cho tư duy regularization: chấp nhận một ít bias để giảm variance và cải thiện tổng sai số dự báo.

## 5) Consistency

Estimator $$\hat\theta_n$$ gọi là consistent nếu:

$$
\hat\theta_n \xrightarrow[]{P} \theta \quad \text{khi } n\to\infty
$$

Nói đơn giản: khi dữ liệu đủ nhiều, estimator tiến gần giá trị thật.

## 6) Liên hệ với Bayes

Trong Bayes, ta không chỉ dùng point estimate mà dùng cả posterior. Tuy nhiên, tư duy bias-variance vẫn rất hữu ích:

Prior mạnh thường làm variance giảm nhưng có thể làm bias tăng, còn prior yếu thường giảm bias nhưng variance lại có thể lớn khi dữ liệu còn ít.

## Tóm tắt nhanh

1. Bias đo lệch hệ thống của estimator.
2. Variance đo độ dao động giữa các mẫu.
3. MSE = bias^2 + variance.
4. Consistency nói về hành vi khi cỡ mẫu lớn.

## Câu hỏi tự luyện

1. Có thể có estimator bias nhỏ nhưng MSE lớn không? Vì sao?
2. Vì sao regularization có thể giúp dự báo tốt hơn dù tạo bias?
3. Consistency có đảm bảo tốt ở mẫu nhỏ không?

## Tài liệu tham khảo

- Casella, G., & Berger, R. (2002). *Statistical Inference*.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*.

---

*Bài học tiếp theo: [0.20 Log-probability và Ổn định số](/vi/chapter00/log-probability-numerical-stability/)*
