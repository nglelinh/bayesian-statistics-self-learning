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

Sau bài này, bạn sẽ phân biệt rõ phân phối Bernoulli và Binomial, hiểu cơ chế sinh dữ liệu nối giữa hai phân phối này, và biết cách diễn giải các tham số theo ngôn ngữ thực tế thay vì chỉ đọc công thức.

## 1) Câu chuyện sinh dữ liệu nhị phân

Nhiều bài toán dữ liệu bắt đầu từ một câu hỏi nhị phân, chẳng hạn một người dùng có nhấp chuột hay không, bệnh nhân có đáp ứng điều trị hay không, hay gói hàng có được giao đúng hẹn hay không. Vì mỗi quan sát chỉ nhận một trong hai trạng thái, biến ngẫu nhiên cơ bản để mô tả nó là phân phối Bernoulli:

$$
X \sim \text{Bernoulli}(p), \quad P(X=1)=p,\; P(X=0)=1-p.
$$

Trong đó, $$p$$ là xác suất thành công trong một phép thử.

![Bernoulli mô tả một lần thử nhị phân với hai kết quả có thể]({{ site.baseurl }}/img/chapter_img/chapter00/bernoulli_binary_outcomes.png)

*Cách đọc hình: Biểu đồ minh họa phân phối Bernoulli cho một phép thử nhị phân với hai kết quả có thể (0 và 1). Chú ý độ cao hai cột biểu thị xác suất $$1-p$$ và $$p$$, với tổng luôn bằng 1.*

## 2) Từ Bernoulli sang Binomial

Nếu lặp lại phép thử Bernoulli $$n$$ lần độc lập với cùng xác suất thành công $$p$$, tổng số lần thành công $$K$$ sẽ tuân theo phân phối Binomial:

$$
K \sim \text{Binomial}(n,p), \quad P(K=k)=\binom{n}{k}p^k(1-p)^{n-k}.
$$

Đây là bước chuyển quan trọng trong mô hình hóa: Bernoulli mô tả một quan sát nhị phân đơn lẻ, còn Binomial mô tả tổng số lần thành công sau nhiều phép thử cùng loại.

![Binomial đếm số lần thành công sau nhiều lần thử Bernoulli độc lập]({{ site.baseurl }}/img/chapter_img/chapter00/binomial_success_count_distribution.png)

Trong hình minh họa này, ta dùng tham số $$n=12$$ và $$p=0.35$$.

**Cách đọc biểu đồ `binomial_success_count_distribution.png`:**

- Trục ngang là số lần thành công $$k$$ (từ $$0$$ đến $$n$$), trục dọc là xác suất $$P(K=k)$$.
- Mỗi cột cho biết xác suất thu được đúng $$k$$ lần thành công sau $$n$$ phép thử.
- Đỉnh phân phối thường nằm gần $$k\approx np$$, nên khi $$p$$ tăng thì khối lượng xác suất dịch sang phải.
- Về trực giác, biểu đồ cho thấy ngay giá trị $$k$$ nào dễ xảy ra nhất và mức độ phân tán quanh giá trị kỳ vọng.

## 3) Hằng số chuẩn hóa trong Bernoulli và Binomial

Với Bernoulli, hàm khối lượng xác suất (PMF) thường được viết gọn là:

$$
P(X=x)=p^x(1-p)^{1-x},
\quad x\in\{0,1\}.
$$

Điều kiện để một phân phối rời rạc hợp lệ là tổng xác suất bằng 1:

$$
\sum_{x\in\{0,1\}} p^x(1-p)^{1-x}
=(1-p)+p=1.
$$

Với Binomial:

$$
P(K=k)=\binom{n}{k}p^k(1-p)^{n-k},\quad k=0,1,\dots,n.
$$

Hệ số tổ hợp $$\binom{n}{k}$$ đếm số cách bố trí $$k$$ lần thành công trong $$n$$ phép thử. Nhờ hệ số này, tổng xác suất trên toàn bộ miền giá trị bằng đúng 1:

$$
\sum_{k=0}^{n} \binom{n}{k}p^k(1-p)^{n-k}
=(p+1-p)^n=1.
$$

Nói ngắn gọn, cả PMF của Bernoulli lẫn Binomial đều đã được chuẩn hóa sẵn, không cần nhân thêm hằng số chuẩn hóa nào bên ngoài.

## 4) Ý nghĩa của các tham số

Trong mô hình Binomial, $$p$$ biểu thị khả năng thành công của mỗi phép thử, $$n$$ cho biết quy mô thí nghiệm (số phép thử), còn $$k$$ là số lần thành công quan sát được. Hai đặc trưng tóm tắt quan trọng nhất của phân phối này là kỳ vọng và phương sai:

$$
\mathbb{E}[K]=np, \qquad \mathrm{Var}(K)=np(1-p).
$$

Từ công thức trên có thể thấy hai thí nghiệm cùng kỳ vọng $$np$$ nhưng khác $$p$$ vẫn có thể có độ phân tán rất khác nhau.

## 5) Ví dụ thực hành ngắn

Giả sử một API có xác suất lỗi ở mỗi yêu cầu (request) là $$p=0.05$$. Trong $$n=40$$ yêu cầu độc lập, số yêu cầu lỗi $$K$$ tuân theo phân phối Binomial. Khi đó, số lỗi kỳ vọng là $$\mathbb{E}[K]=40\times 0.05=2$$, còn xác suất không có lỗi nào xảy ra là:

$$
P(K=0)=(1-0.05)^{40}\approx 0.129.
$$

Như vậy, dù tỷ lệ lỗi chỉ là 5%, khả năng một lô 40 yêu cầu hoàn toàn không phát sinh lỗi chỉ vào khoảng 12.9%.

### 5.1) Cùng kỳ vọng 2, nhưng độ bất định khác nhau

Xét hai tình huống sau:

- Một bài kiểm tra ngắn có 4 câu, mỗi câu trả lời đúng với xác suất $$0.5$$.
- Một chiến dịch email gửi đến 20 khách hàng, mỗi khách phản hồi với xác suất $$0.1$$.

Cả hai đều có số thành công kỳ vọng bằng 2:

$$
4 \times 0.5 = 2, \qquad 20 \times 0.1 = 2.
$$

Tuy nhiên, phương sai của chúng khác nhau:

$$
4 \times 0.5 \times 0.5 = 1, \qquad 20 \times 0.1 \times 0.9 = 1.8.
$$

Dù cùng có trung bình 2 lần thành công, chiến dịch email có mức dao động lớn hơn rõ rệt. Vì vậy, chỉ nhìn kỳ vọng $$np$$ là chưa đủ; cần xem thêm phương sai $$np(1-p)$$ để đánh giá độ ổn định của kết quả.

## 6) Các lỗi mô hình hóa thường gặp

Ba sai lầm hay gặp khi dùng Binomial là: giả định $$p$$ cố định dù thực tế xác suất thay đổi theo thời gian; giả định các phép thử độc lập dù dữ liệu phụ thuộc theo nhóm hoặc theo phiên truy cập; và đồng nhất tỷ lệ quan sát được với xác suất thật mà bỏ qua độ bất định. Trong những trường hợp này, cần mở rộng sang các mô hình có cấu trúc phù hợp hơn như mô hình phân cấp (hierarchical model), mô hình hỗn hợp (mixture model), hoặc hồi quy logistic có biến giải thích (covariate).

## 7) Liên hệ Bayesian

Trong thống kê Bayesian, ta thường đặt phân phối tiên nghiệm (prior) cho tham số $$p$$ rồi cập nhật bằng dữ liệu Binomial. Cặp liên hợp phổ biến nhất là Beta–Binomial, sẽ được trình bày chi tiết ở Bài 0.5.

---

*Bài học tiếp theo: [0.3 Poisson và Exponential]({{ site.baseurl }}/contents/vi/chapter00/00_02_02_poisson_exponential/)*

## Video tham khảo

- [Bernoulli and Binomial Random Variables](https://www.youtube.com/watch?v=Tc6g-Y-l0Rg) — Steve Brunton, English. **Xem trước.** Giúp tách bạch một phép thử nhị phân với tổng số lần thành công trên nhiều phép thử.
- [The Binomial Distribution and Test, Clearly Explained!!!](https://www.youtube.com/watch?v=J8jNoF-K8E8) — StatQuest with Josh Starmer, English. Minh họa ví dụ đếm số lần thành công và công thức tổ hợp, hỗ trợ cách diễn giải tham số theo dữ liệu thực tế.
- [Binomial distributions | Probabilities of probabilities, part 1](https://www.youtube.com/watch?v=8idr1WZ1A7Q) — 3Blue1Brown, English. Cho thấy Binomial như một mô hình sinh dữ liệu nhị phân lặp lại, làm cầu nối sang các bài suy diễn Bayesian phía sau.
