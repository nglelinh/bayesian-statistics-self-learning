---
layout: post
title: "Bài 0.2: Bernoulli và Binomial - Từ Kết quả Nhị phân đến Số lần Thành công"
chapter: '00'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ phân biệt rõ bài toán Bernoulli và Binomial, hiểu mối liên hệ sinh dữ liệu giữa chúng, và biết cách đọc các tham số theo ngôn ngữ thực tế thay vì chỉ nhìn công thức.

## 1) Câu chuyện sinh dữ liệu nhị phân

Nhiều bài toán dữ liệu bắt đầu từ một câu hỏi nhị phân:

Chẳng hạn, một người dùng có click hay không, bệnh nhân có đáp ứng điều trị hay không, hay gói hàng có được giao đúng hẹn hay không.

Mỗi quan sát chỉ có hai trạng thái, nên biến ngẫu nhiên cơ bản là Bernoulli.

$$
X \sim \text{Bernoulli}(p), \quad P(X=1)=p,\; P(X=0)=1-p.
$$

Trong đó $$p$$ là xác suất thành công trong một lần thử.

![Bernoulli mô tả một lần thử nhị phân với hai kết quả có thể]({{ site.baseurl }}/img/chapter_img/chapter00/bernoulli_binary_outcomes.png)

*Cách đọc hình: Hình này minh họa bernoulli mô tả một lần thử nhị phân với hai kết quả có thể. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*

## 2) Từ Bernoulli sang Binomial

Nếu lặp lại thí nghiệm Bernoulli $$n$$ lần độc lập với cùng $$p$$, số lần thành công $$K$$ tuân theo Binomial:

$$
K \sim \text{Binomial}(n,p), \quad P(K=k)=\binom{n}{k}p^k(1-p)^{n-k}.
$$

Đây là bước chuyển quan trọng trong modeling:

Bernoulli mô tả một quan sát nhị phân đơn lẻ, còn Binomial mô tả tổng số lần thành công sau nhiều lần thử cùng loại.

![Binomial đếm số lần thành công sau nhiều lần thử Bernoulli độc lập]({{ site.baseurl }}/img/chapter_img/chapter00/binomial_success_count_distribution.png)

*Cách đọc hình: Hình này minh họa binomial đếm số lần thành công sau nhiều lần thử bernoulli độc lập. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*

Trong hình minh họa này, ta đang dùng tham số $$n=12$$ và $$p=0.35$$.

**Cách đọc biểu đồ `binomial_success_count_distribution.png`:**

- Trục ngang là số lần thành công $$k$$ (từ $$0$$ đến $$n$$), trục dọc là xác suất $$P(K=k)$$.
- Mỗi cột cho biết khả năng nhận được đúng $$k$$ lần thành công sau $$n$$ phép thử.
- Đỉnh phân phối thường nằm gần $$k\approx np$$, nên khi $$p$$ tăng thì khối xác suất dịch sang bên phải.
- Về mặt trực giác, biểu đồ cho ta thấy ngay "số lần thành công nào là khả dĩ nhất" và "mức độ phân tán quanh giá trị kỳ vọng".

## 3) Hằng số chuẩn hóa trong Bernoulli/Binomial

Với Bernoulli, dạng PMF thường viết:

$$
P(X=x)=p^x(1-p)^{1-x},
\quad x\in\{0,1\}.
$$

Điều kiện hợp lệ của một phân phối rời rạc là tổng xác suất bằng 1:

$$
\sum_{x\in\{0,1\}} p^x(1-p)^{1-x}
=(1-p)+p=1.
$$

Với Binomial:

$$
P(K=k)=\binom{n}{k}p^k(1-p)^{n-k},\quad k=0,1,\dots,n.
$$

Ở đây hệ số tổ hợp $$\binom{n}{k}$$ chính là phần đếm số cách sắp xếp $$k$$ lần thành công trong $$n$$ lần thử. Nhờ hệ số này, tổng xác suất đóng đúng về 1:

$$
\sum_{k=0}^{n} \binom{n}{k}p^k(1-p)^{n-k}
=(p+1-p)^n=1.
$$

Nói ngắn gọn: với Bernoulli/Binomial, PMF Binomial đã "tự chuẩn hóa" sẵn: không cần thêm một hằng số ngoài công thức.

## 4) Ý nghĩa của các tham số

Trong mô hình này, $$p$$ diễn tả "mức dễ thành công" của một lần thử, $$n$$ cho biết quy mô của thí nghiệm, còn $$k$$ là kết quả quan sát thực tế sau khi ta đã thực hiện các lần thử đó.

Hai đại lượng hữu ích:

$$
\mathbb{E}[K]=np, \qquad \mathrm{Var}(K)=np(1-p).
$$

Vì vậy, cùng trung bình $$np$$ nhưng khác $$p$$ có thể cho độ phân tán rất khác.

## 5) Ví dụ thực hành ngắn

Giả sử một API có xác suất lỗi mỗi request là $$p=0.05$$. Trong $$n=40$$ request độc lập, số request lỗi $$K$$ có phân phối Binomial.

Trong trường hợp này, kỳ vọng số lỗi là $$\mathbb{E}[K]=40\times 0.05=2$$, còn xác suất để không có lỗi nào xuất hiện được tính như sau:

$$
P(K=0)=(1-0.05)^{40}\approx 0.129.
$$

Diễn giải: dù rate lỗi chỉ 5%, khả năng một lô 40 request hoàn toàn không lỗi chỉ khoảng 12.9%.

## 6) Các lỗi mô hình hóa hay gặp

Những sai lầm phổ biến nhất là dùng Binomial trong khi $$p$$ thật ra thay đổi theo thời gian nhưng vẫn bị giả định là cố định, giả định độc lập dù dữ liệu có phụ thuộc theo nhóm hoặc theo phiên truy cập, và đồng nhất luôn "xác suất quan sát" với "xác suất thật" mà không xét đến độ bất định. Khi gặp các tình huống này, ta cần mở rộng mô hình sang các dạng giàu cấu trúc hơn như hierarchical model, mixture model, hay logistic regression có covariate.

## 7) Liên hệ Bayesian

Trong Bayes, ta thường đặt prior cho $$p$$ rồi cập nhật bằng dữ liệu Binomial. Cặp liên hợp phổ biến nhất là Beta-Binomial (chi tiết ở bài 0.5).

---

*Bài học tiếp theo: [0.3 Poisson và Exponential](/vi/chapter00/00_02_02_poisson_exponential/)*
