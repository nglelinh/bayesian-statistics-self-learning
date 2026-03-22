---
layout: post
title: "Bài 0.16: Kỳ vọng, Phương sai, và Hiệp phương sai"
chapter: '00'
order: 16
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu kỳ vọng như "mức trung bình dài hạn", phương sai như "độ phân tán quanh trung bình", hiệp phương sai như "mức thay đổi cùng chiều hay ngược chiều" giữa hai biến, và biết vì sao ba khái niệm này xuất hiện liên tục trong mọi mô hình Bayesian.

![Ky vong phuong sai hiep phuong sai truc quan]({{ site.baseurl }}/img/chapter_img/chapter00/expectation_variance_covariance_visual.png)
*Hinh 1: Minh hoa truc quan cho ky vong (trong tam phan phoi) va hiep phuong sai duong/am giua hai bien.*

## 1) Kỳ vọng: giá trị trung bình theo phân phối

Với biến rời rạc:

$$
\mathbb{E}[X] = \sum_x x\,p(x)
$$

Với biến liên tục:

$$
\mathbb{E}[X] = \int x f(x)\,dx
$$

Kỳ vọng không nhất thiết là giá trị ta quan sát trực tiếp nhiều nhất. Nó là "trọng tâm xác suất" của phân phối.

## 2) Phương sai: độ bất định quanh trung bình

$$
\mathrm{Var}(X)=\mathbb{E}\big[(X-\mathbb{E}[X])^2\big]
$$

Viết lại dạng tính nhanh:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2
$$

Độ lệch chuẩn là:

$$
\mathrm{SD}(X)=\sqrt{\mathrm{Var}(X)}
$$

Về trực giác, phương sai lớn cho thấy dữ liệu phân tán mạnh, còn phương sai nhỏ cho thấy dữ liệu tập trung hơn quanh trung bình.

## 3) Hiệp phương sai: quan hệ cùng biến thiên

Với hai biến $$X, Y$$:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}\big[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\big]
$$

Khi $$\mathrm{Cov}>0$$, hai biến có xu hướng tăng cùng nhau; khi $$\mathrm{Cov}<0$$, một biến tăng thì biến kia thường giảm; còn khi hiệp phương sai gần 0, quan hệ tuyến tính giữa chúng yếu hoặc gần như không đáng kể.

Lưu ý: hiệp phương sai phụ thuộc đơn vị đo. Vì vậy thực hành thường dùng tương quan:

$$
\rho_{XY}=\frac{\mathrm{Cov}(X,Y)}{\mathrm{SD}(X)\mathrm{SD}(Y)}
$$

## 4) Các tính chất cần nhớ

1. $$\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$$
2. $$\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$$
3. $$\mathrm{Var}(X+Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)+2\mathrm{Cov}(X,Y)$$
4. Nếu $$X,Y$$ độc lập thì $$\mathrm{Cov}(X,Y)=0$$

Tính chất (4) chỉ đi một chiều: cov bằng 0 chưa chắc độc lập.

## 5) Liên hệ với Bayes

Trong Bayesian inference:

Posterior mean chính là kỳ vọng theo posterior, độ không chắc chắn thường được báo bằng posterior SD hoặc posterior variance, và khi có nhiều tham số thì covariance matrix cho biết mức phụ thuộc giữa các tham số đó.

Nói cách khác, học Bayes mà không chắc kỳ vọng/phương sai/hiệp phương sai thì rất khó diễn giải kết quả.

## Tóm tắt nhanh

1. Kỳ vọng là trung bình theo phân phối.
2. Phương sai đo mức phân tán quanh trung bình.
3. Hiệp phương sai đo mức thay đổi cùng chiều/ngược chiều của hai biến.
4. Ba đại lượng này là ngôn ngữ cơ bản để diễn giải posterior.

## Câu hỏi tự luyện

1. Vì sao kỳ vọng không luôn nằm ở đỉnh của phân phối?
2. Hãy nêu ví dụ hai biến có hiệp phương sai âm trong đời sống.
3. Tại sao nói cov bằng 0 chưa đủ kết luận độc lập?

## Tài liệu tham khảo

- Wasserman, L. (2004). *All of Statistics*. Springer.
- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.

---

*Bài học tiếp theo: [0.17 Luật số lớn và Định lý giới hạn trung tâm](/vi/chapter00/law-large-numbers-clt/)*
