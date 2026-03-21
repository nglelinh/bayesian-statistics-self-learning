---
layout: post
title: "Bài 0.15: Sampling Distribution và Standard Error"
chapter: '00'
order: 15
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ phân biệt rõ dữ liệu gốc với phân phối của ước lượng, hiểu standard error là độ bất định của estimator (không phải độ phân tán của dữ liệu), và dùng trực giác này để đọc kết quả suy luận đúng hơn.

![Sampling distribution va standard error]({{ site.baseurl }}/img/chapter_img/chapter00/sampling_distribution_standard_error.png)
*Hinh 1: Cung mot bai toan nhung n lon hon cho sampling distribution hep hon, tuong ung SE nho hon.*

## 1) Sampling distribution là gì?

Giả sử ta lặp lại cùng một quy trình lấy mẫu nhiều lần và mỗi lần tính một ước lượng $$\hat\theta$$ (ví dụ trung bình mẫu $$\bar X$$). Tập hợp các giá trị $$\hat\theta$$ qua các lần lặp tạo thành **sampling distribution**.

Điểm mấu chốt: sampling distribution là phân phối của **ước lượng**, không phải phân phối của từng điểm dữ liệu.

## 2) Standard Error (SE)

SE là độ lệch chuẩn của sampling distribution:

$$
\mathrm{SE}(\hat\theta)=\sqrt{\mathrm{Var}(\hat\theta)}
$$

Với trung bình mẫu:

$$
\mathrm{SE}(\bar X)=\frac{\sigma}{\sqrt{n}}\approx\frac{s}{\sqrt{n}}
$$

Vậy:

- SD của dữ liệu đo mức phân tán cá thể,
- SE đo mức không chắc chắn của ước lượng.

## 3) Nhầm lẫn phổ biến: SD vs SE

Hai dataset có SD giống nhau nhưng cỡ mẫu khác nhau sẽ có SE khác nhau.

- $$n$$ lớn -> SE nhỏ hơn -> ước lượng ổn định hơn,
- $$n$$ nhỏ -> SE lớn hơn -> kết luận kém chắc chắn hơn.

## 4) SE liên quan gì đến khoảng tin cậy/credible?

Trong tư duy xấp xỉ chuẩn, khoảng bất định thường có dạng:

$$
\hat\theta \pm c\cdot \mathrm{SE}(\hat\theta)
$$

Hệ số $$c$$ tùy mục tiêu (95%, 90%, ...). Dù framework khác nhau (Frequentist hay Bayesian), trực giác về "độ rộng tăng khi SE lớn" vẫn giữ nguyên.

## 5) Liên hệ với Bayesian workflow

Trong Bayes, posterior SD của tham số đóng vai trò gần với SE: nó cho ta độ bất định của tham số sau khi đã kết hợp prior và dữ liệu.

Nếu bạn quen tư duy sampling distribution + SE, việc đọc posterior intervals sẽ dễ hơn nhiều.

## Tóm tắt nhanh

1. Sampling distribution là phân phối của estimator.
2. SE là độ lệch chuẩn của estimator.
3. SD dữ liệu và SE là hai thứ khác nhau.
4. Cỡ mẫu tăng làm SE giảm theo $$1/\sqrt{n}$$.

## Câu hỏi tự luyện

1. Hãy giải thích vì sao SD lớn không đồng nghĩa SE lớn trong mọi trường hợp.
2. Nếu tăng cỡ mẫu từ 100 lên 400 thì SE thay đổi thế nào?
3. Sampling distribution của median có giống của mean không? Vì sao?

## Tài liệu tham khảo

- Rice, J. (2006). *Mathematical Statistics and Data Analysis*.
- Wasserman, L. (2004). *All of Statistics*.

---

*Bài học tiếp theo: [Bài 0.16: Ước lượng điểm, Bias-Variance, Consistency](/vi/chapter00/point-estimation-bias-variance-consistency/)*
