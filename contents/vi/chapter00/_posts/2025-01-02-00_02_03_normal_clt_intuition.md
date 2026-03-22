---
layout: post
title: "Bài 0.4: Normal và Trực giác CLT - Khi nào Dữ liệu có dạng Chuông?"
chapter: '00'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vai trò của phân phối Normal, diễn giải đúng tham số $$\mu,\sigma$$, và biết dùng trực giác định lý giới hạn trung tâm (CLT) để giải thích vì sao nhiều đại lượng tổng hợp có dạng gần chuẩn.

## 1) Phân phối Normal là gì?

Với biến liên tục $$X$$:

$$
X\sim\mathcal{N}(\mu,\sigma^2),
$$

hàm mật độ là:

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

Ở đây, $$\mu$$ cho biết vị trí trung tâm của phân phối, còn $$\sigma$$ đo mức độ phân tán quanh trung tâm đó. Một quy tắc nhớ nhanh thường dùng là khoảng $$\mu\pm\sigma$$ chứa xấp xỉ 68% khối lượng xác suất, khoảng $$\mu\pm 2\sigma$$ chứa khoảng 95%, và khoảng $$\mu\pm 3\sigma$$ chứa khoảng 99.7%.

![Quy tắc 68-95-99.7 của phân phối Normal]({{ site.baseurl }}/img/chapter_img/chapter00/normal_distribution_rule.png)

*Cách đọc hình: Hình này minh họa quy tắc 68-95-99.7 của phân phối normal. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*

## 2) Vì sao Normal xuất hiện nhiều?

CLT cho biết: khi cộng (hoặc lấy trung bình) nhiều thành phần nhiễu độc lập, tổng hợp thường tiến gần dạng chuẩn, ngay cả khi từng thành phần ban đầu không chuẩn.

Vì vậy các đại lượng như sai số đo lường, trung bình điểm số, tổng ảnh hưởng từ nhiều yếu tố nhỏ thường gần Normal.

![CLT làm phân phối của trung bình mẫu dần trở nên tròn và hẹp hơn]({{ site.baseurl }}/img/chapter_img/chapter00/clt_sample_means_overlay.png)

*Cách đọc hình: Hình này minh họa clt làm phân phối của trung bình mẫu dần trở nên tròn và hẹp hơn. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*

## 3) Hằng số chuẩn hóa của Normal đến từ đâu?

Mật độ Normal có dạng:

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

Hệ số $$\frac{1}{\sigma\sqrt{2\pi}}$$ là hằng số chuẩn hóa để bảo đảm:

$$
\int_{-\infty}^{\infty} f(x)\,dx=1.
$$

Đặt biến chuẩn hóa $$z=\frac{x-\mu}{\sigma}$$ thì:

$$
\int_{-\infty}^{\infty} f(x)\,dx
=\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz
=1.
$$

Nghĩa là toàn bộ "khối lượng xác suất" của đường cong chuông bằng đúng 1, nên mới là một mật độ hợp lệ.

## 4) Ví dụ trực giác

Giả sử điểm kiểm tra cuối kỳ chịu ảnh hưởng của nhiều yếu tố nhỏ:

Chẳng hạn như chất lượng ngủ, mức ôn tập, độ khó từng câu, và trạng thái tâm lý khi làm bài.

Mỗi yếu tố biến thiên nhỏ, nhưng tổng hợp của chúng thường cho phân phối điểm gần dạng chuông. Đây là lý do dùng mô hình Normal cho sai số hoặc cho điểm tổng là hợp lý trong nhiều bối cảnh.

## 5) Khi nào không nên dùng Normal?

Normal không còn là lựa chọn tốt khi dữ liệu bị chặn miền, chẳng hạn xác suất chỉ nằm trong $$[0,1]$$ hoặc thời gian chờ luôn dương, khi dữ liệu là số đếm nguyên không âm, hoặc khi phân phối bị lệch mạnh, có đuôi dày, hay chứa nhiều outlier. Trong những trường hợp này, giả định Normal có thể làm cho khoảng bất định bị sai lệch đáng kể.

## 6) Liên hệ Bayesian

Trong Bayesian modeling, phân phối Normal xuất hiện ở nhiều tầng khác nhau: nó có thể đóng vai trò likelihood cho dữ liệu liên tục, làm prior cho các hệ số hồi quy, hoặc xuất hiện như một xấp xỉ thuận tiện của posterior khi cỡ mẫu đủ lớn. Tuy vậy, workflow Bayesian luôn đòi hỏi kiểm tra mô hình cẩn thận, thay vì mặc định rằng cứ dữ liệu liên tục là có thể gán Normal một cách vô điều kiện.

## Câu hỏi tự luyện

1. Nêu một đại lượng liên tục nên dùng Normal và giải thích vì sao.
2. Nêu một đại lượng liên tục nhưng không nên dùng Normal và đề xuất phân phối thay thế.
3. CLT giúp gì cho trực giác về phân phối của trung bình mẫu?

---

*Bài học tiếp theo: [0.5 Beta và Gamma](/vi/chapter00/00_02_04_beta_gamma_bayesian/)*
