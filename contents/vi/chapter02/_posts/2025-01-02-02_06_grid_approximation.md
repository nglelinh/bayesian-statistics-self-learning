---
layout: post
title: "Bài 2.6: Grid Approximation - Xấp xỉ Lưới"
chapter: '02'
order: 6
owner: Nguyen Le Linh
lang: vi
categories:
- chapter02
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu xấp xỉ lưới (grid approximation) như cây cầu nối từ suy luận Bayes giải tay sang suy luận Bayes bằng tính toán số. Bạn cần nắm ý tưởng rời rạc hóa không gian tham số, tự tính được posterior trên một lưới đơn giản, biết cách khai thác kết quả từ lưới, đồng thời hiểu rõ vì sao phương pháp này gặp giới hạn khi số chiều tham số tăng lên.

> **Ví dụ mini.** Bạn muốn suy luận $$\theta$$ sau khi quan sát 6 mặt ngửa trong 9 lần tung, nhưng thay vì xét liên tục trên toàn đoạn $$[0,1]$$, bạn chỉ đánh giá trên 5 giá trị ứng viên $$0, 0.25, 0.5, 0.75, 1$$. Đó chính là tinh thần của xấp xỉ lưới.
>
> **Câu hỏi tự kiểm tra.** Khi tăng số điểm lưới từ 5 lên 100 hoặc 1000, posterior xấp xỉ sẽ thay đổi như thế nào?

## Mở đầu: khi posterior không có công thức dạng đóng

Ở Bài 2.5, các cặp liên hợp cho phép tính posterior rất gọn. Tuy nhiên, trong thực tế không phải lúc nào mô hình cũng có dạng giải tích thuận tiện như vậy: prior có thể là hỗn hợp của hai niềm tin cạnh tranh, likelihood có thể không liên hợp với prior, hoặc đôi khi ta đơn giản cần một cách tính trực quan để nhìn rõ từng bước cập nhật Bayes. Trong những tình huống đó, xấp xỉ lưới là phương pháp đơn giản nhất để bắt đầu.

![Giới thiệu trực quan về grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_approximation_intro.png)

## 1. Ý tưởng cốt lõi: thay miền liên tục bằng một tập điểm hữu hạn

Giả sử tham số $$\theta$$ nhận giá trị trên đoạn $$[0,1]$$. Thay vì xét vô hạn giá trị liên tục, ta chọn một tập hữu hạn gồm $$G$$ điểm lưới trên đoạn này:

$$
\theta_1,\theta_2,\dots,\theta_G.
$$

Tại mỗi điểm lưới, ta lần lượt tính giá trị prior, likelihood và tích của chúng (posterior chưa chuẩn hóa), sau đó chia cho tổng toàn bộ các giá trị để thu được một phân phối posterior rời rạc hợp lệ. Nói cách khác, **xấp xỉ lưới chuyển bài toán tích phân liên tục thành bài toán chấm điểm và chuẩn hóa trên một tập các giá trị ứng viên.**

## 2. Ví dụ tính tay: 6 mặt ngửa trong 9 lần tung

Giả sử prior là phân phối đều trên $$[0,1]$$, dữ liệu quan sát là 6 mặt ngửa trong 9 lần tung, và ta dùng lưới gồm 5 điểm:

$$
\theta \in \{0,\ 0.25,\ 0.5,\ 0.75,\ 1\}.
$$

Likelihood tỉ lệ với:

$$
\theta^6(1-\theta)^3.
$$

Tính giá trị tại từng điểm lưới:

| $$\theta$$ | prior | likelihood chưa chuẩn hóa | posterior chưa chuẩn hóa |
| --- | --- | --- | --- |
| 0.00 | 1 | 0.000000 | 0.000000 |
| 0.25 | 1 | 0.000103 | 0.000103 |
| 0.50 | 1 | 0.001953 | 0.001953 |
| 0.75 | 1 | 0.002781 | 0.002781 |
| 1.00 | 1 | 0.000000 | 0.000000 |

Tiếp theo, ta chuẩn hóa bằng cách chia mỗi giá trị cho tổng của cột cuối. Kết quả cho thấy trên lưới này, vùng quanh $$0.75$$ được dữ liệu ủng hộ mạnh nhất, vùng quanh $$0.25$$ yếu hơn hẳn, còn hai đầu mút $$0$$ và $$1$$ có trọng số bằng 0. Ví dụ nhỏ này minh họa rằng suy luận Bayes không nhất thiết phải bắt đầu bằng các tích phân phức tạp, mà có thể hiểu trực tiếp như quy trình chấm điểm và chuẩn hóa.

### 2.1. Đọc kết quả posterior rời rạc bằng số

Tổng ba trọng số khác 0 ở bảng trên xấp xỉ:

$$
0.000103 + 0.001953 + 0.002781 = 0.004837.
$$

Sau khi chuẩn hóa, posterior rời rạc trên lưới gồm:

- $$P(\theta=0.25 \mid D) \approx 0.021$$
- $$P(\theta=0.50 \mid D) \approx 0.404$$
- $$P(\theta=0.75 \mid D) \approx 0.575$$

Ngay trên một lưới rất thô như vậy, ta đã có thể tính trực tiếp xác suất của một biến cố, chẳng hạn:

$$
P(\theta \ge 0.5 \mid D) \approx 0.404 + 0.575 = 0.979.
$$

Ưu điểm trực giác của xấp xỉ lưới nằm ở chỗ nó biến posterior thành các xác suất cụ thể có thể cộng, so sánh và diễn giải ngay lập tức.

## 3. Thuật toán xấp xỉ lưới

![Các bước của thuật toán grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_algorithm_steps.png)

Quy trình chuẩn gồm 5 bước:

### Bước 1. Tạo lưới tham số

Ví dụ:

$$
\theta_{\text{grid}} = \text{linspace}(0,1,G).
$$

### Bước 2. Tính prior tại từng điểm lưới

Mỗi điểm trên lưới nhận một giá trị mật độ hoặc trọng số tiền nghiệm tương ứng.

### Bước 3. Tính likelihood tại từng điểm lưới

Với cùng bộ dữ liệu đã quan sát, đánh giá mức độ giải thích dữ liệu tại từng điểm lưới.

### Bước 4. Nhân prior với likelihood

Tích này tạo ra posterior chưa chuẩn hóa:

$$
p(\theta_i \mid D) \propto p(D \mid \theta_i)p(\theta_i).
$$

### Bước 5. Chuẩn hóa

Chia từng giá trị cho tổng toàn bộ trọng số trên lưới để thu được phân phối hậu nghiệm rời rạc hợp lệ.

### Thử nghiệm: từng bước của xấp xỉ lưới

Chia lưới, tính prior, likelihood, nhân rồi chuẩn hóa; tăng số điểm lưới để thấy sai số giảm.

<div class="interactive-demo" markdown="1">
<div data-demo="grid-explainer" data-lang="vi" data-prior="flat" data-k="6" data-n="9" data-points="10"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Đánh đổi giữa độ mịn của lưới và chi phí tính toán

Một lưới 5 điểm đủ để minh họa nguyên lý, nhưng để thu được xấp xỉ chính xác hơn, ta cần lưới mịn hơn như 20, 100 hay 1000 điểm. Khi lưới mịn hơn, phân phối rời rạc càng tiệm cận phân phối liên tục chính xác, kéo theo các thống kê như trung bình hậu nghiệm hay khoảng tin cậy Bayes cũng chính xác hơn.

![Grid rất thô với 5 điểm]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_5.png)

![Grid trung bình với 20 điểm]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_20.png)

![Grid mịn với 100 điểm]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_100.png)

![So sánh grid 5 điểm với posterior chính xác]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_5.png)

![So sánh grid 20 điểm với posterior chính xác]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_20.png)

![So sánh grid 100 điểm với posterior chính xác]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_100.png)

![Ảnh hưởng của kích thước grid]({{ site.baseurl }}/img/chapter_img/chapter02/grid_size_comparison.png)

Vì vậy, ta luôn gặp sự đánh đổi quen thuộc: lưới thô chạy nhanh nhưng sai số lớn, còn lưới mịn chính xác hơn nhưng tốn chi phí tính toán hơn.

## 5. Ví dụ thực tế: prior không liên hợp

Giả sử nhóm phân tích có hai giả thuyết cạnh tranh về tỷ lệ khách quay lại: một giả thuyết cho rằng tỷ lệ nằm quanh $$0.3$$, giả thuyết kia cho rằng nó nằm quanh $$0.7$$. Ta có thể biểu diễn prior này bằng một phân phối hỗn hợp hai đỉnh. Khi đó posterior không còn công thức đóng đơn giản như Beta–Binomial, nhưng xấp xỉ lưới vẫn xử lý dễ dàng: tính mật độ prior hỗn hợp tại từng điểm lưới, nhân với likelihood rồi chuẩn hóa.

![Ví dụ grid với prior mixture]({{ site.baseurl }}/img/chapter_img/chapter02/grid_mixture_prior_example.png)

Ưu điểm lớn của xấp xỉ lưới là không đòi hỏi tính liên hợp; nó chỉ cần ta tính được giá trị của prior và likelihood tại các điểm lưới.

### Thử nghiệm: prior không liên hợp (tam giác lệch)

Với prior không có công thức đóng, lưới vẫn cho posterior chính xác khi đủ mịn.

<div class="interactive-demo" markdown="1">
<div data-demo="grid-explainer" data-lang="vi" data-prior="tri" data-k="8" data-n="12" data-points="100"></div>
</div>

## 6. Khai thác posterior thu được từ lưới

Từ phân phối posterior rời rạc trên lưới, ta có thể tính trực tiếp hầu hết các đại lượng suy luận cần thiết.

### 6.1. Tính trung bình hậu nghiệm

Lấy trung bình có trọng số theo xác suất hậu nghiệm:

$$
E[\theta \mid D] \approx \sum_i \theta_i p(\theta_i \mid D).
$$

![Posterior mean cùng median và mode trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_mean_median_mode.png)

### 6.2. Tính xác suất của một khoảng

Chẳng hạn, xác suất:

$$
P(0.5 \le \theta \le 0.8 \mid D)
$$

được tính bằng tổng trọng số posterior của tất cả các điểm lưới nằm trong đoạn $$[0.5, 0.8]$$.

![Xác suất posterior của một khoảng trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_interval_probability.png)

### 6.3. Tính khoảng tin cậy Bayes (Credible interval)

Ta tính hàm phân phối tích lũy rời rạc bằng cách cộng dồn trọng số trên lưới rồi trích ra các phân vị (quantile) mong muốn.

![Credible interval được lấy từ posterior rời rạc]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_credible_interval.png)

### 6.4. Lấy mẫu từ posterior

Ta có thể lấy mẫu các điểm lưới theo xác suất posterior để phục vụ cho các phép tính hoặc mô phỏng ở bước tiếp theo.

![Lấy mẫu trực tiếp từ posterior trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_sampling.png)

Nhờ cách tiếp cận này, mọi khái niệm suy luận Bayes đều trở nên cụ thể thông qua các phép cộng và phép nhân cơ bản.

## 7. Dự báo hậu nghiệm (Posterior predictive) trên lưới

Sau khi có posterior của tham số trên lưới, ta có thể tính phân phối dự báo cho dữ liệu mới — chẳng hạn dự báo số đơn hàng trong 50 khách tiếp theo từ posterior của tỷ lệ mua hàng — bằng cách lấy trung bình có trọng số các phân phối dự báo điều kiện theo từng điểm lưới:

$$
P(y_{\text{new}} \mid D) = \sum_i P(y_{\text{new}} \mid \theta_i)p(\theta_i \mid D).
$$

![Phân phối posterior predictive lấy từ posterior trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_predictive_distribution.png)

![So sánh posterior predictive từ grid với công thức chính xác]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_predictive_vs_exact.png)

Bước này kết nối trực tiếp suy luận tham số với dự báo thực tế.

## 8. Khi nào xấp xỉ lưới đặc biệt hữu ích?

### 8.1. Khi mới học thống kê Bayes

Xấp xỉ lưới giúp nhìn rõ từng thành phần — prior, likelihood, posterior, bước chuẩn hóa và dự báo hậu nghiệm — thông qua các trọng số cụ thể trên một tập điểm hữu hạn.

### 8.2. Khi mô hình chỉ có 1 tham số

Với bài toán một tham số, phương pháp lưới dễ cài đặt, chạy nhanh và thuận tiện để trực quan hóa bằng đồ thị.

### 8.3. Khi cần đối chiếu kết quả cho mô hình nhỏ

Ngay cả khi sử dụng MCMC về sau, xấp xỉ lưới vẫn là điểm đối chiếu tin cậy cho các mô hình một tham số để kiểm chứng xem thuật toán phức tạp hơn có hoạt động đúng hay không.

![Khi nào nên dùng grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/when_to_use_grid.png)

## 9. Hạn chế lớn nhất: lời nguyền số chiều (Curse of dimensionality)

Hạn chế nghiêm trọng của xấp xỉ lưới xuất hiện ngay khi số tham số tăng lên. Nếu mỗi chiều tham số dùng 100 điểm lưới, thì:

- 1 tham số cần $$100$$ điểm,
- 2 tham số cần $$10{,}000$$ điểm,
- 3 tham số cần $$1{,}000{,}000$$ điểm,
- 4 tham số vọt lên $$100{,}000{,}000$$ điểm.

Tốc độ tăng theo cấp số mũ này gọi là **lời nguyền số chiều (curse of dimensionality)**. Vì vậy, xấp xỉ lưới rất hiệu quả cho bài toán 1 tham số, còn chấp nhận được cho một số bài toán 2 tham số nhỏ, nhưng nhanh chóng trở nên bất khả thi ở các mô hình nhiều tham số trong thực tế.

![Số điểm grid tăng bùng nổ theo số chiều tham số]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_dimensionality_growth.png)

![Bảng tóm tắt vì sao grid approximation nhanh chóng mất khả thi ở nhiều chiều]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_dimensionality_table.png)

## 10. Vị trí của xấp xỉ lưới trong bức tranh tổng thể

Các phương pháp tính posterior nằm trên một trục phát triển tự nhiên: **prior liên hợp** cho lời giải giải tích chính xác và nhanh khi mô hình đủ đơn giản; **xấp xỉ lưới** cung cấp phương pháp số trực quan và linh hoạt cho các mô hình ít tham số; còn **MCMC** là công cụ tổng quát dành cho các mô hình phức tạp nhiều chiều. Xấp xỉ lưới đóng vai trò cây cầu giúp ta hiểu rõ lý do cần đến các phương pháp lấy mẫu ở các chương sau.

![Từ grid đến MCMC]({{ site.baseurl }}/img/chapter_img/chapter02/grid_to_mcmc_bridge.png)

## 11. Những nhầm lẫn phổ biến

### 11.1. “Xấp xỉ lưới luôn cho kết quả chính xác tuyệt đối”

Không đúng. Đây là phương pháp xấp xỉ; độ chính xác phụ thuộc vào độ mịn của lưới, việc lưới có bao phủ đủ vùng mật độ posterior quan trọng hay không, và số chiều tham số.

### 11.2. “Cứ tăng số điểm lưới là giải quyết được mọi bài toán”

Không đúng. Khi số tham số tăng, tổng số điểm lưới tăng theo cấp số mũ khiến chi phí tính toán vượt quá khả năng xử lý rất nhanh.

### 11.3. “Xấp xỉ lưới chỉ là công cụ minh họa, không đáng học”

Ngược lại. Xấp xỉ lưới là công cụ rất hiệu quả để xây dựng trực giác Bayes, hiểu cơ chế hình thành posterior và tạo nền tảng trực tiếp cho MCMC.

## Tóm tắt

**Xấp xỉ lưới (grid approximation) ước lượng posterior bằng cách rời rạc hóa không gian tham số thành một lưới điểm hữu hạn.** Phương pháp này trực quan, dễ cài đặt, không yêu cầu prior liên hợp và đặc biệt phù hợp cho các mô hình ít tham số. Hạn chế cốt lõi của nó là không mở rộng được lên không gian nhiều chiều do lời nguyền số chiều. Nếu prior liên hợp giúp ta hiểu suy luận Bayes bằng giải tích, thì xấp xỉ lưới mở ra cánh cửa sang suy luận Bayes bằng tính toán số.

## Video tham khảo

- [Introduction to the elements of Bayesian statistics. Week 3. Video 2. Grid approx. & probability.](https://www.youtube.com/watch?v=w4fKaBCX02Q) — Peter Blenis, English. **xem trước**. Minh họa cách tính posterior trên lưới điểm và chuẩn hóa bằng tổng, bám sát thuật toán trình bày trong bài.
- [Bayes Week 2, Lecture 1: Grid Approximation](https://www.youtube.com/watch?v=2BhfFLATx8c) — Kevin James, English. Trình bày thêm một ví dụ xây dựng lưới, nhân prior với likelihood và đọc phân phối rời rạc thu được.
- [Statistical Rethinking 2023 - 02 - The Garden of Forking Data](https://www.youtube.com/watch?v=R1vcdhPBlXA) — Richard McElreath, English. Giải thích cách đếm các khả năng sinh dữ liệu, giúp hiểu xấp xỉ lưới như phép rời rạc hóa của quá trình đếm đó.

## Câu hỏi tự luyện

1. Hãy giải thích bằng lời vì sao lưới 5 điểm chỉ cho một xấp xỉ thô.
2. Với bài toán một tham số, vì sao xấp xỉ lưới là công cụ học tập rất hiệu quả?
3. Vì sao xấp xỉ lưới gặp khó khăn nghiêm trọng khi mô hình có 4 hoặc 5 tham số?
4. Hãy nêu một ví dụ prior không liên hợp mà xấp xỉ lưới xử lý thuận tiện hơn giải tích.

## Tài liệu tham khảo

- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2-3.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 6.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 3.

---

*Kết thúc Chapter 02. Bài học tiếp theo: [Chapter 04 - Bayesian Linear Regression]({{ site.baseurl }}/contents/vi/chapter04/)*
