---
layout: post
title: "Bài 0.20: Log-probability và Ổn định số"
chapter: '00'
order: 20
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao thực hành Bayesian gần như luôn làm việc trên log-probability, nhận diện underflow/overflow trong tính toán xác suất, và nắm kỹ thuật log-sum-exp để chuẩn hóa an toàn.

![Log probability va on dinh so]({{ site.baseurl }}/img/chapter_img/chapter00/log_probability_numerical_stability.png)
*Hinh 1: Tich xac suat truc tiep rat de bi underflow, trong khi bieu dien tren thang log on dinh hon.*

## 1) Vì sao dùng log?

Likelihood thường là tích của nhiều số nhỏ:

$$
L(\theta)=\prod_{i=1}^n p(x_i\mid\theta)
$$

Khi $$n$$ lớn, tích này dễ về 0 trên máy tính (underflow). Dùng log:

$$
\log L(\theta)=\sum_{i=1}^n \log p(x_i\mid\theta)
$$

giúp:

Biến tích thành tổng, làm tính toán ổn định số hơn, và giúp tối ưu hóa cũng như suy luận dễ hơn đáng kể.

## 2) Underflow và overflow

**Underflow** là khi một số dương quá nhỏ bị làm tròn thành 0, còn **overflow** là khi một số quá lớn vượt quá khả năng biểu diễn của máy.

Trong Bayes, cả hai đều có thể phá hỏng tính posterior nếu ta tính trực tiếp trên thang xác suất.

## 3) Kỹ thuật log-sum-exp

Khi cần tính:

$$
\log\sum_i e^{a_i}
$$

ta không nên tính thẳng. Dùng mẹo ổn định:

$$
\log\sum_i e^{a_i}=m+\log\sum_i e^{a_i-m},\quad m=\max_i a_i
$$

Nhờ trừ $$m$$, các số mũ không bùng nổ hoặc biến mất quá nhanh.

## 4) Liên hệ với softmax và chuẩn hóa posterior

Nhiều bài toán cần chuyển log-weights thành xác suất. Công thức an toàn:

$$
w_i = \frac{e^{a_i-m}}{\sum_j e^{a_j-m}}
$$

với $$m=\max_j a_j$$.

Đây chính là softmax ổn định số, dùng rộng rãi trong thống kê và machine learning.

## 5) Thói quen thực hành nên có

1. Tính log-likelihood thay vì likelihood.
2. Chuẩn hóa trên thang log khi có thể.
3. Tránh trừ hai số rất gần nhau ở thang xác suất.
4. Kiểm tra giá trị `-inf`, `nan`, `inf` trong pipeline.

## Tóm tắt nhanh

1. Log-probability là công cụ chống bất ổn số.
2. Underflow/overflow là lỗi kỹ thuật nhưng tác động trực tiếp lên suy luận.
3. Log-sum-exp là kỹ thuật bắt buộc để cộng xác suất ở thang log.
4. Hầu hết thư viện Bayes hiện đại đều vận hành theo logic này.

## Câu hỏi tự luyện

1. Vì sao cộng log-probability lại ổn định hơn nhân probability?
2. Khi nào cần log-sum-exp thay vì phép cộng trực tiếp?
3. Hãy nêu một hậu quả nếu quên xử lý underflow trong posterior weights.

## Tài liệu tham khảo

- Murphy, K. (2012). *Machine Learning: A Probabilistic Perspective*.
- Bishop, C. (2006). *Pattern Recognition and Machine Learning*.

---

*Bài học tiếp theo: [0.21 Kiểm tra giả định mô hình cơ bản](/vi/chapter00/basic-model-assumption-checks/)*
