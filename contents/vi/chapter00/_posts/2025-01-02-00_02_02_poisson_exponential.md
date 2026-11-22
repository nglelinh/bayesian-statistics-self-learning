---
layout: post
title: "Bài 0.3: Poisson và Exponential - Đếm Sự kiện và Thời gian Chờ"
chapter: '00'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách mô hình hóa dữ liệu đếm bằng phân phối Poisson, mô hình hóa thời gian chờ bằng phân phối Exponential, và hiểu vì sao hai phân phối này là hai góc nhìn của cùng một quá trình sự kiện ngẫu nhiên theo thời gian.

## 1) Khi nào dùng Poisson?

Phân phối Poisson phù hợp khi ta đếm số sự kiện xảy ra trong một khoảng cố định, chẳng hạn số cuộc gọi trong 1 giờ, số lỗi trên 1 trang văn bản, hay số tai nạn tại một giao lộ trong 1 tháng.

Nếu $$Y$$ là số sự kiện trong khoảng quan sát:

$$
Y \sim \text{Poisson}(\lambda), \quad P(Y=k)=\frac{\lambda^k e^{-\lambda}}{k!},\; k=0,1,2,\dots
$$

Ở đây, $$\lambda$$ là số sự kiện trung bình trong mỗi khoảng. Tính chất đặc trưng của phân phối Poisson là kỳ vọng và phương sai bằng nhau:

$$
\mathbb{E}[Y]=\lambda, \qquad \mathrm{Var}(Y)=\lambda.
$$

![Poisson mô tả số sự kiện đếm được trong các khoảng thời gian cố định]({{ site.baseurl }}/img/chapter_img/chapter00/poisson_counts_timeline.png)

*Cách đọc hình: Biểu đồ minh họa cách phân phối Poisson mô tả số sự kiện đếm được trong các khoảng thời gian cố định; hãy đối chiếu trục giá trị đếm với xác suất tương ứng để thấy vị trí đỉnh và độ rộng của phân phối.*

## 2) Khi nào dùng Exponential?

Phân phối Exponential phù hợp khi đại lượng quan tâm là thời gian chờ cho đến sự kiện tiếp theo. Nếu $$T$$ là thời gian chờ:

$$
T \sim \text{Exponential}(\lambda), \quad f(t)=\lambda e^{-\lambda t},\; t\ge 0.
$$

Kỳ vọng của $$T$$ là:

$$
\mathbb{E}[T]=\frac{1}{\lambda}.
$$

Điều này hoàn toàn thuận tự nhiên: tốc độ xảy ra sự kiện $$\lambda$$ càng cao thì thời gian chờ trung bình càng ngắn.

![Exponential mô tả thời gian chờ tới sự kiện kế tiếp]({{ site.baseurl }}/img/chapter_img/chapter00/exponential_waiting_time_curve.png)

*Cách đọc hình: Đường cong minh họa hàm mật độ Exponential cho thời gian chờ tới sự kiện kế tiếp, giảm dần theo hàm mũ khi thời gian chờ tăng lên.*

## 3) Hằng số chuẩn hóa trong Poisson và Exponential

Với phân phối Poisson:

$$
P(Y=k)=\frac{\lambda^k e^{-\lambda}}{k!},\quad k=0,1,2,\dots
$$

Trong công thức này, $$k!$$ xuất hiện từ lập luận đếm tổ hợp về số cách sắp xếp các sự kiện, còn $$e^{-\lambda}$$ là hệ số chuẩn hóa bảo đảm tổng toàn bộ PMF bằng đúng 1:

$$
\sum_{k=0}^{\infty} \frac{\lambda^k e^{-\lambda}}{k!}
=e^{-\lambda}\sum_{k=0}^{\infty}\frac{\lambda^k}{k!}
=e^{-\lambda}e^{\lambda}=1.
$$

Với phân phối Exponential:

$$
f(t)=\lambda e^{-\lambda t},\quad t\ge 0.
$$

Hệ số $$\lambda$$ chính là hằng số chuẩn hóa để tích phân hàm mật độ trên $$[0, \infty)$$ bằng 1:

$$
\int_0^{\infty} \lambda e^{-\lambda t}\,dt=1.
$$

Nếu bỏ $$\lambda$$, biểu thức $$e^{-\lambda t}$$ mới chỉ thể hiện dạng suy giảm theo hàm mũ chứ chưa phải một hàm mật độ xác suất hợp lệ.

## 4) Liên hệ trực tiếp giữa Poisson và Exponential

Nếu các sự kiện xảy ra theo một quá trình Poisson với tốc độ $$\lambda$$, thì số sự kiện trong khoảng thời gian dài $$\Delta t$$ tuân theo phân phối $$\text{Poisson}(\lambda\Delta t)$$, còn khoảng thời gian giữa hai sự kiện liên tiếp tuân theo phân phối $$\text{Exponential}(\lambda)$$. Vì vậy, hai câu hỏi "có bao nhiêu sự kiện trong một khoảng thời gian" và "phải chờ bao lâu đến sự kiện tiếp theo" thực chất xuất phát từ cùng một mô hình.

## 5) Ví dụ ngắn

Giả sử một tổng đài nhận trung bình 6 cuộc gọi mỗi giờ. Số cuộc gọi trong 1 giờ có thể mô hình hóa bằng $$Y\sim\text{Poisson}(6)$$. Khi đó, xác suất không có cuộc gọi nào trong 10 phút (tức $$1/6$$ giờ) là:

$$
P(Y=0)=e^{-6\times(1/6)}=e^{-1}\approx 0.368.
$$

Trong khi đó, thời gian chờ trung bình đến cuộc gọi tiếp theo là:

$$
\mathbb{E}[T]=\frac{1}{6}\text{ giờ}=10\text{ phút}.
$$

### 5.1) Cùng một $$\lambda$$, trả lời hai câu hỏi khác nhau

Vẫn với tốc độ $$\lambda = 6$$ cuộc gọi mỗi giờ:

- Trong 30 phút, số cuộc gọi kỳ vọng là $$6 \times 0.5 = 3$$, nên ta dùng phân phối Poisson để đánh giá nguy cơ quá tải theo số cuộc gọi.
- Trong 5 phút đầu, xác suất xuất hiện ít nhất một cuộc gọi được tính bằng Exponential:

$$
P(T \leq 5\text{ phút}) = 1 - e^{-6\times(5/60)} = 1 - e^{-0.5} \approx 0.393.
$$

Nghĩa là trong 5 phút đầu, xác suất tổng đài nhận ít nhất một cuộc gọi vào khoảng 39.3%.

Điểm mấu chốt là Poisson trả lời câu hỏi về số lần đếm trong một khoảng thời gian cố định, còn Exponential trả lời câu hỏi về thời gian chờ đến sự kiện kế tiếp; cả hai cùng dùng chung một tham số tốc độ $$\lambda$$.

## 6) Cảnh báo mô hình hóa

Nếu dữ liệu đếm có phương sai lớn hơn trung bình đáng kể (hiện tượng quá phân tán — overdispersion), phân phối Poisson thường quá chặt; khi đó nên cân nhắc phân phối Negative Binomial hoặc mô hình phân cấp. Ngoài ra, nếu tốc độ sự kiện thay đổi theo thời gian (như giờ cao điểm và giờ thấp điểm), giả định $$\lambda$$ là hằng số cũng không còn phù hợp.

## 7) Liên hệ Bayesian

Trong thống kê Bayesian, việc kết hợp phân phối tiên nghiệm Gamma cho $$\lambda$$ với hàm hợp lý (likelihood) Poisson sẽ cho phân phối hậu nghiệm (posterior) cũng thuộc họ Gamma. Đây là cặp liên hợp rất tiện lợi cho các bài toán đếm sự kiện.

---

*Bài học tiếp theo: [0.4 Normal và trực giác CLT]({{ site.baseurl }}/contents/vi/chapter00/00_02_03_normal_clt_intuition/)*

## Video tham khảo

- [An Introduction to the Poisson Distribution](https://www.youtube.com/watch?v=jmqZG6roVqU) — jbstatistics, English. **Xem trước.** Trình bày phân phối Poisson như mô hình đếm số sự kiện trong một khoảng cố định, khớp với nửa đầu bài học.
- [Understanding Exponential vs Poisson Distributions](https://www.youtube.com/watch?v=n7K8s4vryCQ) — Explained by Michael, English. Đối chiếu trực tiếp giữa thời gian chờ và số lần đếm, làm rõ mối liên hệ giữa hai phân phối.
- [The Exponential Distribution](https://www.youtube.com/watch?v=wtLQUjfomig) — StatQuest with Josh Starmer, English. Giải thích hình dạng và tham số của phân phối Exponential cho bài toán thời gian chờ.
