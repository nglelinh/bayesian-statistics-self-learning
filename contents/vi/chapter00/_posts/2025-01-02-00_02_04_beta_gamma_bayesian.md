---
layout: post
title: "Bài 0.5: Beta và Gamma trong Bayes - Prior cho Xác suất và Tham số Dương"
chapter: '00'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ biết khi nào dùng Beta/Gamma làm prior, diễn giải được tham số theo trực giác dữ liệu, và thực hiện được hai cập nhật liên hợp cơ bản: Beta-Binomial và Gamma-Poisson.

## 1) Vì sao cần prior đúng miền giá trị?

Trong Bayes, prior phải tôn trọng miền của tham số:

Nếu tham số là xác suất $$p$$ thì nó buộc phải nằm trong $$[0,1]$$, còn nếu là rate hoặc precision thì nó phải dương.

Do đó:

Beta phù hợp cho xác suất, còn Gamma phù hợp cho các tham số dương.

## 2) Beta cho xác suất

$$
p\sim\text{Beta}(\alpha,\beta), \quad 0<p<1.
$$

Diễn giải nhanh:

$$\alpha-1$$ có thể được hiểu như phần nghiêng về "thành công", còn $$\beta-1$$ nghiêng về "thất bại".

Trung bình prior:

$$
\mathbb{E}[p]=\frac{\alpha}{\alpha+\beta}.
$$

Khi $$\alpha+\beta$$ lớn, prior "chắc" hơn; khi nhỏ, prior "mềm" hơn.

Hằng số chuẩn hóa của Beta là:

$$
B(\alpha,\beta)=\int_0^1 p^{\alpha-1}(1-p)^{\beta-1}\,dp
=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}.
$$

Do đó mật độ đầy đủ phải viết:

$$
f(p)=\frac{1}{B(\alpha,\beta)}p^{\alpha-1}(1-p)^{\beta-1},\quad 0<p<1.
$$

## 3) Cập nhật Beta-Binomial

Giả sử prior $$p\sim\text{Beta}(\alpha,\beta)$$ và dữ liệu có $$k$$ thành công trên $$n$$ lần thử:

$$
k\mid p \sim \text{Binomial}(n,p).
$$

Posterior:

$$
p\mid D \sim \text{Beta}(\alpha+k,\beta+n-k).
$$

Ví dụ: prior Beta(2,2), quan sát 8 thành công trên 10 lần:

$$
p\mid D \sim \text{Beta}(10,4).
$$

Đọc bằng lời: dữ liệu đẩy niềm tin về phía xác suất thành công cao hơn.

![Beta-Binomial cập nhật niềm tin về xác suất thành công p]({{ site.baseurl }}/img/chapter_img/chapter00/beta_binomial_update_vi.png)

## 4) Gamma cho tham số dương

Một cách tham số hóa thường dùng theo shape-rate:

$$
\lambda\sim\text{Gamma}(\alpha,\beta), \quad
f(\lambda)=\frac{\beta^\alpha}{\Gamma(\alpha)}\lambda^{\alpha-1}e^{-\beta\lambda},\; \lambda>0.
$$

Kỳ vọng:

$$
\mathbb{E}[\lambda]=\frac{\alpha}{\beta}.
$$

Ở đây $$\frac{\beta^\alpha}{\Gamma(\alpha)}$$ là hằng số chuẩn hóa để:

$$
\int_0^{\infty} f(\lambda)\,d\lambda=1.
$$

Nếu bỏ tỉ số này, ta chỉ có "hình dạng" $$\lambda^{\alpha-1}e^{-\beta\lambda}$$, chưa phải phân phối hợp lệ.

## 5) Cập nhật Gamma-Poisson

Giả sử $$y_1,\dots,y_n\mid\lambda\sim\text{Poisson}(\lambda)$$ và prior $$\lambda\sim\text{Gamma}(\alpha,\beta)$$.

Đặt $$S=\sum_{i=1}^n y_i$$, posterior là:

$$
\lambda\mid D\sim\text{Gamma}(\alpha+S,\beta+n).
$$

Ví dụ: prior Gamma(3,1), quan sát dữ liệu đếm có tổng $$S=14$$ trong $$n=5$$ khoảng quan sát:

$$
\lambda\mid D\sim\text{Gamma}(17,6).
$$

![Gamma-Poisson cập nhật niềm tin về rate dương λ]({{ site.baseurl }}/img/chapter_img/chapter00/gamma_poisson_update_vi.png)

## 6) Dạng chưa chuẩn hóa và dạng chuẩn hóa trong Bayes

Trong thực hành Bayes, ta thường viết trước ở dạng tỉ lệ:

$$
p(\theta\mid D)\propto p(D\mid\theta)p(\theta).
$$

Sau đó nhận diện họ phân phối và thêm hằng số chuẩn hóa tương ứng.

Ví dụ Beta-Binomial:

$$
p\mid D\propto p^{\alpha+k-1}(1-p)^{\beta+n-k-1}
$$

và dạng chuẩn hóa đầy đủ là:

$$
f(p\mid D)=\frac{1}{B(\alpha+k,\beta+n-k)}p^{\alpha+k-1}(1-p)^{\beta+n-k-1}.
$$

Tương tự, Gamma-Poisson dùng hằng số chuẩn hóa của họ Gamma với tham số hậu nghiệm mới.

## 7) Mẹo thực hành

Trong thực hành, bạn nên luôn ghi rõ tham số hóa Gamma đang dùng là shape-rate hay shape-scale, dùng prior predictive check để xem prior có sinh ra dữ liệu hợp lý hay không, và nếu prior ảnh hưởng mạnh tới kết quả thì nên báo cáo sensitivity analysis với vài prior hợp lý khác.

## Tổng kết

Beta và Gamma không chỉ là hai công thức quen mặt trong Bayes. Chúng là hai "vật chứa niềm tin" rất thực dụng: một cho xác suất, một cho tham số dương. Khi kết hợp với Binomial/Poisson, chúng cho cập nhật liên hợp gọn, dễ diễn giải, và giúp bạn nhìn rõ logic prior -> likelihood -> posterior.

---

*Bài học tiếp theo: [0.6 Thống kê Mô tả](/vi/chapter00/descriptive-statistics/)*
