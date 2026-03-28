---
layout: post
title: "Bài 0.17: Sampling Distribution và Standard Error"
chapter: '00'
order: 17
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ phân biệt rõ dữ liệu gốc với phân phối của ước lượng, hiểu standard error là độ bất định của estimator (không phải độ phân tán của dữ liệu), và dùng trực giác này để đọc kết quả suy luận đúng hơn.

## Giới thiệu: từ một mẫu dữ liệu đến độ tin cậy của ước lượng

Trong thực hành, ta thường chỉ có một mẫu dữ liệu duy nhất, nhưng vẫn cần trả lời câu hỏi "ước lượng hiện tại ổn định đến đâu nếu quy trình lấy mẫu được lặp lại?". Sampling distribution và standard error chính là ngôn ngữ để lượng hóa câu hỏi đó một cách khoa học.

## 1) Sampling distribution là gì?

Giả sử ta lặp lại cùng một quy trình lấy mẫu nhiều lần và mỗi lần tính một ước lượng $$\hat\theta$$ (ví dụ trung bình mẫu $$\bar X$$). Tập hợp các giá trị $$\hat\theta$$ qua các lần lặp tạo thành **sampling distribution**.

Điểm mấu chốt: sampling distribution là phân phối của **ước lượng**, không phải phân phối của từng điểm dữ liệu.

![Sampling distribution của trung bình mẫu với n = 20]({{ site.baseurl }}/img/chapter_img/chapter00/sampling_distribution_n20.png)

*Hình 1a: Với cùng một bài toán nhưng cỡ mẫu còn nhỏ, sampling distribution của trung bình mẫu vẫn khá rộng.*

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

SD của dữ liệu đo mức phân tán giữa các cá thể, còn SE đo mức không chắc chắn của chính ước lượng.

## 3) Nhầm lẫn phổ biến: SD vs SE

Hai dataset có SD giống nhau nhưng cỡ mẫu khác nhau sẽ có SE khác nhau.

Nếu $$n$$ lớn hơn thì SE nhỏ hơn và ước lượng ổn định hơn, còn nếu $$n$$ nhỏ thì SE lớn hơn và kết luận vì thế cũng kém chắc chắn hơn.

![Sampling distribution của trung bình mẫu với n = 200]({{ site.baseurl }}/img/chapter_img/chapter00/sampling_distribution_n200.png)

*Hình 1b: Khi tăng cỡ mẫu lên $$n = 200$$, sampling distribution hẹp lại rõ rệt, tương ứng với standard error nhỏ hơn.*

### 3.1) Một ví dụ SD và SE rất dễ bị lẫn

Giả sử cân nặng của một nhóm người có độ lệch chuẩn khoảng 12 kg.

- Nếu lấy mẫu $$n=25$$ người, sai số chuẩn của trung bình là $$12/\sqrt{25}=2.4$$ kg.
- Nếu lấy mẫu $$n=100$$ người, sai số chuẩn của trung bình là $$12/\sqrt{100}=1.2$$ kg.

Điều quan trọng là SD của dữ liệu cá nhân vẫn là 12 kg trong cả hai trường hợp. Thứ thay đổi là độ bất định của **ước lượng trung bình**. Đây là lý do SD và SE không thể dùng thay nhau, dù nhiều người mới học rất hay lẫn hai đại lượng này.

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

*Bài học tiếp theo: [0.18 Ước lượng điểm, Bias-Variance, Consistency](/vi/chapter00/point-estimation-bias-variance-consistency/)*
