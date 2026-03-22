---
layout: post
title: "Bài 0.17: Luật số lớn và Định lý giới hạn trung tâm"
chapter: '00'
order: 17
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao trung bình mẫu ổn định khi số mẫu tăng (LLN), vì sao tổng/trung bình nhiều biến ngẫu nhiên có xu hướng gần chuẩn (CLT), và vì sao hai định lý này là nền cho tư duy mô phỏng, ước lượng, và kiểm định.

![LLN va CLT truc quan]({{ site.baseurl }}/img/chapter_img/chapter00/lln_clt_convergence.png)
*Hinh 1: Ben trai la hoi tu trung binh chay (LLN); ben phai la phan phoi trung binh mau gan dang chuan (CLT).* 

## 1) Luật số lớn (LLN): trung bình mẫu hội tụ

Gọi $$X_1,\dots,X_n$$ độc lập cùng phân phối, có kỳ vọng $$\mu$$. Trung bình mẫu:

$$
\bar X_n = \frac{1}{n}\sum_{i=1}^n X_i
$$

LLN nói rằng khi $$n\to\infty$$, $$\bar X_n$$ tiến gần $$\mu$$ (theo xác suất).

Trực giác: nhiễu ngẫu nhiên "triệt tiêu dần" khi lấy trung bình trên nhiều quan sát.

## 2) CLT: phân phối của trung bình mẫu gần chuẩn

Với điều kiện đủ nhẹ, ta có:

$$
\frac{\bar X_n-\mu}{\sigma/\sqrt{n}} \Rightarrow \mathcal N(0,1)
$$

Hệ quả thực hành:

$$
\bar X_n \approx \mathcal N\left(\mu,\frac{\sigma^2}{n}\right)
$$

ngay cả khi phân phối gốc không chuẩn (n đủ lớn).

## 3) LLN và CLT khác nhau thế nào?

**LLN** trả lời câu hỏi trung bình mẫu có hội tụ về giá trị đúng hay không, còn **CLT** trả lời câu hỏi tốc độ và dạng bất định quanh giá trị đúng trông như thế nào. Nói cách khác, LLN là câu chuyện "đúng về đâu", còn CLT là câu chuyện "dao động ra sao quanh cái đúng".

## 4) Liên hệ với sai số chuẩn

Từ CLT, độ lớn dao động của $$\bar X_n$$ tỉ lệ với $$1/\sqrt{n}$$. Đây là lý do sai số chuẩn giảm chậm:

Muốn sai số giảm 2 lần, ta thường phải tăng cỡ mẫu lên khoảng 4 lần.

Đây là trực giác quan trọng khi thiết kế thí nghiệm và đánh giá độ tin cậy của ước lượng.

## 5) Liên hệ với Bayes và mô phỏng

Trong Bayes:

Monte Carlo estimate cũng dựa vào ý tưởng trung bình mẫu, số mẫu posterior càng tăng thì estimate càng ổn định hơn, và rất nhiều chẩn đoán về uncertainty thực chất đều dựa trên trực giác của LLN và CLT.

## Tóm tắt nhanh

1. LLN: trung bình mẫu hội tụ về kỳ vọng thật khi số mẫu lớn.
2. CLT: phân phối của trung bình mẫu gần chuẩn với phương sai $$\sigma^2/n$$.
3. LLN nói về hội tụ; CLT nói về dao động quanh điểm hội tụ.
4. Cả hai là nền tảng cho suy luận và mô phỏng thống kê.

## Câu hỏi tự luyện

1. Vì sao LLN không đủ để suy ra khoảng bất định của $$\bar X$$?
2. Hãy giải thích bằng lời vì sao sai số chuẩn giảm theo $$1/\sqrt{n}$$.
3. CLT có yêu cầu dữ liệu gốc phải chuẩn không?

## Tài liệu tham khảo

- Casella, G., & Berger, R. (2002). *Statistical Inference*.
- Wasserman, L. (2004). *All of Statistics*.

---

*Bài học tiếp theo: [0.18 Sampling Distribution và Standard Error](/vi/chapter00/sampling-distribution-standard-error/)*
