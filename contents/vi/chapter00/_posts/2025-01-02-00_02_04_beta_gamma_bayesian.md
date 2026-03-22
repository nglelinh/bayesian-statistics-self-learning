---
layout: post
title: "Bài 0.5: Beta và Gamma - Phân phối cho Xác suất và Tham số Dương"
chapter: '00'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu Beta bắt nguồn từ nhu cầu mô tả các đại lượng nằm trong đoạn $$[0,1]$$, đọc được ý nghĩa tham số $$\alpha,\beta$$, và nắm được vai trò của hằng số chuẩn hóa để tạo thành một phân phối hợp lệ.

## 1) Bắt đầu từ vấn đề thực tế: mô tả một tỉ lệ chưa biết

Trong thực tế, ta thường gặp các đại lượng dạng tỉ lệ như:

- tỉ lệ khách hàng sẽ click,
- tỉ lệ sản phẩm lỗi,
- tỉ lệ học viên hoàn thành khóa học.

Các đại lượng này có một điểm chung: luôn nằm giữa 0 và 1.

Ta cần một phân phối đủ linh hoạt để mô tả nhiều kiểu hình dạng khác nhau trên đoạn đó: có thể nghiêng trái, nghiêng phải, hoặc tập trung quanh một vùng trung tâm. Đó chính là vai trò của phân phối Beta.

## 2) Beta cho xác suất

$$
p\sim\text{Beta}(\alpha,\beta), \quad 0<p<1.
$$

Diễn giải nhanh:

$$\alpha-1$$ có thể được hiểu như phần nghiêng về "thành công", còn $$\beta-1$$ nghiêng về "thất bại".

Trung bình:

$$
\mathbb{E}[p]=\frac{\alpha}{\alpha+\beta}.
$$

Khi $$\alpha+\beta$$ lớn, phân phối tập trung hơn; khi nhỏ, phân phối dàn rộng hơn.

Hằng số chuẩn hóa của Beta là:

$$
B(\alpha,\beta)=\int_0^1 p^{\alpha-1}(1-p)^{\beta-1}\,dp
=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}.
$$

Do đó mật độ đầy đủ phải viết:

$$
f(p)=\frac{1}{B(\alpha,\beta)}p^{\alpha-1}(1-p)^{\beta-1},\quad 0<p<1.
$$

## 3) Hàm Gamma và cầu nối tới hàm Beta

Để hiểu rõ hơn hằng số chuẩn hóa của Beta, ta cần hàm Gamma:

$$
\Gamma(z)=\int_0^{\infty} t^{z-1}e^{-t}\,dt,\quad z>0.
$$

Hàm Gamma là phần mở rộng của giai thừa sang số thực dương, với tính chất:

$$
\Gamma(z+1)=z\,\Gamma(z),\qquad \Gamma(n+1)=n!\;(n\in\mathbb{N}).
$$

Nhờ đó, hằng số chuẩn hóa của Beta có thể viết gọn:

$$
B(\alpha,\beta)=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}.
$$

Ý nghĩa thực dụng: ta biến một tích phân chuẩn hóa khó tính trực tiếp thành tỉ số Gamma để tính toán ổn định và rõ cấu trúc hơn.

## 4) Beta giải quyết vấn đề gì?

Beta cho ta một cách mô tả có hệ thống câu hỏi: "tỉ lệ thật có xu hướng nằm vùng nào trong đoạn $$[0,1]$$, và mức độ tập trung mạnh hay yếu ra sao?"

Nói ngắn gọn:

- $$\alpha$$ và $$\beta$$ điều khiển hình dạng,
- $$\frac{\alpha}{\alpha+\beta}$$ cho vị trí trung tâm,
- $$\alpha+\beta$$ cho mức độ tập trung.

Nhờ vậy, Beta không chỉ cho một con số tỉ lệ, mà còn cho cả độ bất định quanh tỉ lệ đó.

## 5) Ví dụ đọc hình dạng Beta

Giả sử $$\alpha=2,\beta=5$$ thì mật độ nghiêng về phía gần 0; nếu đổi thành $$\alpha=8,\beta=3$$ thì mật độ nghiêng về phía gần 1.

Nói cách khác, cặp $$\alpha,\beta$$ điều khiển cả vị trí và độ tập trung của phân phối trên đoạn $$[0,1]$$.

![So sánh hình dạng Beta với các bộ tham số khác nhau]({{ site.baseurl }}/img/chapter_img/chapter00/beta_binomial_update_vi.png)

*Cách đọc hình: Hình này minh họa cách thay đổi tham số làm dịch chuyển và co giãn hình dạng của phân phối Beta trên đoạn $$[0,1]$$.*

## 6) Gamma cho tham số dương

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

## 7) Ví dụ trực giác với Gamma

Với shape-rate:

- nếu giữ $$\alpha$$ và tăng $$\beta$$, phân phối dịch về gần 0 hơn,
- nếu tăng $$\alpha$$, phân phối có đỉnh rõ hơn và bớt lệch hơn.

Điều này hữu ích khi mô tả các đại lượng dương như thời gian chờ, cường độ sự kiện, hoặc biến có đuôi phải.

## 8) Dạng chưa chuẩn hóa và dạng chuẩn hóa

Trong thực hành, ta thường gặp dạng "kernel" trước, ví dụ:

$$
g(p)=p^{\alpha-1}(1-p)^{\beta-1}.
$$

Đây chưa phải mật độ hợp lệ vì tích phân trên $$[0,1]$$ chưa chắc bằng 1. Để thành mật độ, cần chia cho hằng số chuẩn hóa:

$$
f(p)=\frac{1}{B(\alpha,\beta)}g(p).
$$

Ý tưởng tương tự áp dụng cho Gamma: phần mũ và lũy thừa cho hình dạng, còn hệ số phía trước bảo đảm tổng xác suất bằng 1.

## 9) Mẹo thực hành

Khi dùng Gamma, luôn ghi rõ tham số hóa shape-rate hay shape-scale. Khi đọc tài liệu, hãy kiểm tra kỹ ký hiệu để tránh nhầm giữa rate $$\beta$$ và scale $$\theta=1/\beta$$.

## Tổng kết

Beta và Gamma là hai họ phân phối nền tảng trong thống kê: Beta cho biến trong $$[0,1]$$ và Gamma cho biến dương. Điểm quan trọng nhất của bài là biết chọn đúng miền và hiểu vai trò của hằng số chuẩn hóa để biến một "hình dạng" thành một phân phối hợp lệ.

---

*Bài học tiếp theo: [0.6 Thống kê Mô tả](/vi/chapter00/descriptive-statistics/)*
