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

Sau bài này, bạn sẽ mô hình hóa được dữ liệu đếm bằng Poisson, mô hình hóa thời gian chờ bằng Exponential, và hiểu vì sao hai phân phối này là hai mặt của cùng một quá trình sự kiện ngẫu nhiên theo thời gian.

## 1) Khi nào dùng Poisson?

Poisson phù hợp khi ta đếm số sự kiện trong một khoảng cố định:

Ví dụ điển hình là số cuộc gọi trong 1 giờ, số lỗi trên 1 trang văn bản, hay số tai nạn tại một giao lộ trong 1 tháng.

Nếu $$Y$$ là số sự kiện trong khoảng quan sát:

$$
Y \sim \text{Poisson}(\lambda), \quad P(Y=k)=\frac{\lambda^k e^{-\lambda}}{k!},\; k=0,1,2,\dots
$$

Ở đây $$\lambda$$ là số sự kiện trung bình mỗi khoảng.

Tính chất cốt lõi:

$$
\mathbb{E}[Y]=\lambda, \qquad \mathrm{Var}(Y)=\lambda.
$$

![Poisson mô tả số sự kiện đếm được trong các khoảng thời gian cố định]({{ site.baseurl }}/img/chapter_img/chapter00/poisson_counts_timeline.png)

## 2) Khi nào dùng Exponential?

Exponential phù hợp khi ta quan tâm thời gian chờ đến sự kiện tiếp theo.

Nếu $$T$$ là thời gian chờ:

$$
T \sim \text{Exponential}(\lambda), \quad f(t)=\lambda e^{-\lambda t},\; t\ge 0.
$$

Kỳ vọng:

$$
\mathbb{E}[T]=\frac{1}{\lambda}.
$$

Nghĩa là tốc độ sự kiện càng cao thì thời gian chờ trung bình càng thấp.

![Exponential mô tả thời gian chờ tới sự kiện kế tiếp]({{ site.baseurl }}/img/chapter_img/chapter00/exponential_waiting_time_curve.png)

## 3) Hằng số chuẩn hóa trong Poisson/Exponential

Với Poisson:

$$
P(Y=k)=\frac{\lambda^k e^{-\lambda}}{k!},\quad k=0,1,2,\dots
$$

Trong đó:

Ở đây, $$k!$$ phản ánh số cách sắp xếp các sự kiện trong lập luận đếm tổ hợp, còn $$e^{-\lambda}$$ là nhân tố giúp tổng toàn bộ PMF đóng lại đúng bằng 1.

Thật vậy:

$$
\sum_{k=0}^{\infty} \frac{\lambda^k e^{-\lambda}}{k!}
=e^{-\lambda}\sum_{k=0}^{\infty}\frac{\lambda^k}{k!}
=e^{-\lambda}e^{\lambda}=1.
$$

Với Exponential:

$$
f(t)=\lambda e^{-\lambda t},\quad t\ge 0.
$$

Hằng số $$\lambda$$ là nhân tố chuẩn hóa để tích phân mật độ bằng 1:

$$
\int_0^{\infty} \lambda e^{-\lambda t}\,dt=1.
$$

Nếu bỏ $$\lambda$$, hàm $$e^{-\lambda t}$$ chỉ là "dạng" giảm mũ, chưa phải mật độ hợp lệ.

## 4) Liên hệ trực tiếp giữa Poisson và Exponential

Nếu số sự kiện theo thời gian tuân theo quá trình Poisson tốc độ $$\lambda$$, thì:

Số sự kiện trong khoảng dài $$\Delta t$$ sẽ có phân phối Poisson($$\lambda\Delta t$$), còn thời gian giữa hai sự kiện liên tiếp sẽ có phân phối Exponential($$\lambda$$).

Vì vậy, câu hỏi "đếm bao nhiêu sự kiện" và "chờ bao lâu tới sự kiện tiếp" thực ra là cùng một mô hình dưới hai góc nhìn.

## 5) Ví dụ ngắn

Một tổng đài nhận trung bình 6 cuộc gọi mỗi giờ.

Khi đó, số cuộc gọi trong 1 giờ có thể được mô hình hóa bằng $$Y\sim\text{Poisson}(6)$$, và xác suất không có cuộc gọi nào trong 10 phút, tức 1/6 giờ, được tính như sau:

$$
P(Y=0)=e^{-6\times(1/6)}=e^{-1}\approx 0.368.
$$

Trong khi đó, thời gian chờ trung bình đến cuộc gọi tiếp theo là:

$$
\mathbb{E}[T]=\frac{1}{6}\text{ giờ}=10\text{ phút}.
$$

## 6) Cảnh báo mô hình hóa

Nếu dữ liệu đếm có phương sai lớn hơn trung bình quá nhiều (overdispersion), Poisson thường quá "chặt". Khi đó có thể cần Negative Binomial hoặc mô hình phân cấp.

Nếu tốc độ sự kiện thay đổi theo thời gian (giờ cao điểm/thấp điểm), giả định $$\lambda$$ hằng số cũng không còn phù hợp.

## 7) Liên hệ Bayesian

Trong Bayes, prior Gamma cho $$\lambda$$ kết hợp với likelihood Poisson tạo posterior Gamma. Đây là một cặp liên hợp rất hữu ích cho bài toán đếm sự kiện.

---

*Bài học tiếp theo: [0.4 Normal và trực giác CLT](/vi/chapter00/00_02_03_normal_clt_intuition/)*
