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

Cuối thế kỷ 19, nhà thống kê Ladislaus Bortkiewicz thống kê số binh sĩ Phổ tử vong vì bị ngựa đá mỗi năm trong 10 quân đoàn suốt 20 năm — một dữ liệu kỳ lạ nhưng lại trở thành minh họa bất hủ cho phân phối Poisson. Cùng một quá trình ngẫu nhiên xảy ra đều đặn theo thời gian, nếu ta hỏi *"có bao nhiêu sự kiện trong 1 giờ?"* ta gặp **Poisson**; còn nếu ta bấm đồng hồ hỏi *"phải chờ bao lâu tới sự kiện kế tiếp?"* ta gặp **Exponential**.

Trong thực hành Bayes hiện đại — từ đếm số cuộc gọi tổng đài, số lỗi máy chủ đến số ca bệnh hiếm mỗi tuần — cặp Poisson–Exponential là điểm khởi đầu để hiểu cách mô hình hóa tốc độ $$\lambda > 0$$ và cặp liên hợp Gamma–Poisson.

---

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách mô hình hóa dữ liệu đếm bằng phân phối Poisson, mô hình hóa thời gian chờ bằng phân phối Exponential, và hiểu vì sao hai phân phối này là hai góc nhìn của cùng một quá trình sự kiện ngẫu nhiên theo thời gian.

## Bản đồ kiến thức nền: Quá trình điểm Poisson, Tính không nhớ và Cặp liên hợp Gamma–Poisson

Ba trụ cột toán học đằng sau bài học này gồm:

- **Quá trình Poisson (Poisson Process):** Mô hình hóa các sự kiện xảy ra ngẫu nhiên, độc lập trên trục thời gian hoặc không gian với tốc độ trung bình không đổi $$\lambda$$. Nó là giới hạn của phân phối Binomial khi số khoảng thời gian nhỏ $$n 	o \infty$$ và xác suất mỗi khoảng $$p 	o 0$$ sao cho $$np = \lambda$$.
- **Tính không nhớ (Memoryless Property) của Exponential:** $$P(T > t + s \mid T > t) = P(T > s)$$. Thời gian đã chờ không làm thay đổi phân phối thời gian phải chờ thêm — đây là lý do phân phối Exponential mô tả cực tốt sự kiện ngẫu nhiên thuần túy nhưng *không* phù hợp với thiết bị bị hao mòn theo tuổi thọ (khi đó cần phân phối Weibull).
- **Cầu nối sang Thống kê Bayes (Gamma–Poisson):** Tốc độ $$\lambda$$ là tham số dương liên tục ($$\lambda > 0$$). Khi đặt prior $$	ext{Gamma}(lpha, eta)$$ lên $$\lambda$$ và quan sát $$n$$ khoảng thời gian có tổng số sự kiện $$S = \sum_{i=1}^n y_i$$, hậu nghiệm lại là $$	ext{Gamma}(lpha + S, eta + n)$$ — một cập nhật dạng đóng cực kỳ gọn gàng.

---

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

## Khung giải thích (nên đọc chậm): Hai mặt của cùng một đồng xu và cập nhật Gamma–Poisson bằng tay

Hãy đọc chậm mối liên hệ toán học giữa đếm sự kiện (Poisson) và thời gian chờ (Exponential):

1. **Biến cố tương đương:** "Thời gian chờ đến sự kiện đầu tiên lớn hơn $$t$$" ($$T > t$$) hoàn toàn tương đương với "Có đúng $$0$$ sự kiện xảy ra trong khoảng $$[0, t]$$" ($$N(t) = 0$$).
2. **Suy ra hàm sống còn (Survival Function):** Với $$N(t) \sim 	ext{Poisson}(\lambda t)$$, ta có $$P(T > t) = P(N(t) = 0) = rac{(\lambda t)^0 e^{-\lambda t}}{0!} = e^{-\lambda t}$$.
3. **Lấy đạo hàm để ra mật độ Exponential:** $$F(t) = 1 - e^{-\lambda t} \implies f(t) = \lambda e^{-\lambda t}$$ với $$t \ge 0$$.
4. **Đưa vào cập nhật Bayes:** Nhân prior $$	ext{Gamma}(lpha, eta) \propto \lambda^{lpha-1} e^{-eta \lambda}$$ với likelihood Poisson $$\prod_{i=1}^n rac{\lambda^{y_i} e^{-\lambda}}{y_i!} \propto \lambda^{\sum y_i} e^{-n\lambda}$$, số mũ của $$\lambda$$ và hệ số trên $$e$$ tự động cộng dồn!

### Ví dụ tính toán cầm tay chỉ việc: Ước lượng tốc độ lỗi máy chủ $$\lambda$$ (lỗi/giờ)

Trước khi triển khai bản cập nhật phần mềm, đội vận hành tin tốc độ lỗi quanh mức 2 lỗi/giờ với độ bất định vừa phải, mã hóa bằng prior $$\lambda \sim 	ext{Gamma}(lpha=4, eta=2)$$ (trung bình tiên nghiệm $$lpha/eta = 4/2 = 2.0$$ lỗi/giờ, tương đương kinh nghiệm 2 giờ quan sát thấy 4 lỗi).

Trong $$n = 3$$ giờ đầu sau khi phát hành, hệ thống ghi nhận số lỗi lần lượt là $$y = (5, 3, 4)$$, tổng $$S = 5 + 3 + 4 = 12$$ lỗi.

- **Bước 1 — Xác suất quan sát được đúng 5 lỗi trong giờ đầu nếu $$\lambda = 2$$:**
  $$P(Y = 5 \mid \lambda = 2) = rac{2^5 e^{-2}}{5!} = rac{32 	imes 0.1353}{120} pprox 0.0361 \quad (3.61\%).$$
- **Bước 2 — Cập nhật hậu nghiệm Gamma–Poisson:**
  $$lpha_{	ext{post}} = 4 + 12 = 16, \qquad eta_{	ext{post}} = 2 + 3 = 5 \implies \lambda \mid y \sim 	ext{Gamma}(16, 5).$$
- **Bước 3 — Tóm tắt hậu nghiệm tính tay:**
  - Trung bình hậu nghiệm: $$\mathbb{E}[\lambda \mid y] = rac{16}{5} = 3.2$$ lỗi/giờ (nằm giữa prior $$2.0$$ và trung bình mẫu $$12/3 = 4.0$$).
  - Độ lệch chuẩn hậu nghiệm: $$rac{\sqrt{16}}{5} = rac{4}{5} = 0.8$$ lỗi/giờ.
  - Thời gian chờ kỳ vọng giữa hai lỗi mới theo ước lượng trung bình hậu nghiệm: $$1 / 3.2 = 0.3125$$ giờ ($$pprox 18.75$$ phút).

**Hiểu lầm cần tránh:** Nhầm giữa tham số *rate* $$eta$$ và tham số *scale* $$	heta = 1/eta$$ của phân phối Gamma khi viết mã Python/SciPy — luôn kiểm tra kỳ vọng $$lpha/eta$$ (rate) hay $$lpha	heta$$ (scale).

**Kiểm tra nhanh:** Nếu quan sát thêm 1 giờ nữa không có lỗi nào ($$y_4 = 0$$), hậu nghiệm mới là $$	ext{Gamma}(16 + 0, 5 + 1) = 	ext{Gamma}(16, 6)$$, trung bình giảm từ $$3.2$$ xuống $$16/6 pprox 2.67$$ lỗi/giờ — ngay cả dữ liệu "không có sự kiện" cũng cung cấp thông tin!

---

## Video tham khảo

- [An Introduction to the Poisson Distribution](https://www.youtube.com/watch?v=jmqZG6roVqU) — jbstatistics, English. **Xem trước.** Trình bày phân phối Poisson như mô hình đếm số sự kiện trong một khoảng cố định, khớp với nửa đầu bài học.
- [Understanding Exponential vs Poisson Distributions](https://www.youtube.com/watch?v=n7K8s4vryCQ) — Explained by Michael, English. Đối chiếu trực tiếp giữa thời gian chờ và số lần đếm, làm rõ mối liên hệ giữa hai phân phối.
- [The Exponential Distribution](https://www.youtube.com/watch?v=wtLQUjfomig) — StatQuest with Josh Starmer, English. Giải thích hình dạng và tham số của phân phối Exponential cho bài toán thời gian chờ.
