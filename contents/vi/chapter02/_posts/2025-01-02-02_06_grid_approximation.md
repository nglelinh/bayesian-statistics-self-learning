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

Sau bài này, bạn nên hiểu grid approximation như cây cầu đi từ Bayes giải tay sang Bayes tính toán. Bạn cần nắm ý tưởng rời rạc hóa không gian tham số, biết tự tính posterior trên một lưới đơn giản, biết đọc kết quả của grid, và hiểu vì sao phương pháp này rất hay cho học tập nhưng nhanh chóng gặp giới hạn khi số tham số tăng.

> **Ví dụ mini.** Bạn muốn suy luận $$\theta$$ sau khi thấy 6 mặt ngửa trong 9 lần tung, nhưng thay vì làm trên cả đoạn $$[0,1]$$, bạn chỉ xét 5 giá trị ứng viên như $$0, 0.25, 0.5, 0.75, 1$$. Đó chính là tinh thần của grid approximation.
>
> **Câu hỏi tự kiểm tra.** Nếu tăng số điểm grid từ 5 lên 100 hay 1000, bạn mong điều gì sẽ thay đổi ở posterior xấp xỉ?

## Mở đầu: nếu posterior không giải tay được thì sao?

Trong bài conjugacy, mọi thứ rất đẹp vì posterior vẫn nằm trong cùng họ phân phối với prior. Nhưng thực tế không phải lúc nào prior cũng “ngoan” như vậy.

Chẳng hạn, prior có thể là hỗn hợp của hai niềm tin cạnh tranh nhau, likelihood có thể không ăn khớp với prior theo một dạng giải tích đủ đẹp, hoặc đơn giản hơn, ta chỉ muốn một cách tính đủ trực quan để có thể nhìn thấy Bayes đang vận hành như thế nào thay vì chỉ chấp nhận kết quả cuối cùng dưới dạng công thức.

Lúc đó, grid approximation là cách đơn giản nhất để bắt đầu.

![Giới thiệu trực quan về grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_approximation_intro.png)

## 1. Ý tưởng cốt lõi: thay đường liên tục bằng một tập điểm

Giả sử tham số $$\theta$$ nằm trong đoạn $$[0,1]$$. Thay vì xét mọi giá trị liên tục có thể có của $$\theta$$, ta chọn một số điểm trên đoạn này:

$$
\theta_1,\theta_2,\dots,\theta_G.
$$

Ở mỗi điểm, ta tính:

prior, likelihood, và posterior chưa chuẩn hóa.

Cuối cùng, ta chuẩn hóa các trọng số này để thu được một posterior rời rạc trên lưới.

Nói bằng lời:

**grid approximation biến một bài toán liên tục thành một bài toán “chấm điểm” trên nhiều điểm ứng viên.**

## 2. Ví dụ tay rất nhỏ: 6 ngửa trong 9 lần tung

Giả sử prior là phân phối đều trên $$[0,1]$$, dữ liệu là 6 mặt ngửa trong 9 lần tung, và ta dùng một grid gồm 5 điểm:

$$
\theta \in \{0,\ 0.25,\ 0.5,\ 0.75,\ 1\}.
$$

Likelihood tỉ lệ với:

$$
\theta^6(1-\theta)^3.
$$

Ta tính ở từng điểm:

| $$\theta$$ | prior | likelihood chưa chuẩn hóa | posterior chưa chuẩn hóa |
| --- | --- | --- | --- |
| 0.00 | 1 | 0.000000 | 0.000000 |
| 0.25 | 1 | 0.000103 | 0.000103 |
| 0.50 | 1 | 0.001953 | 0.001953 |
| 0.75 | 1 | 0.002781 | 0.002781 |
| 1.00 | 1 | 0.000000 | 0.000000 |

Rồi chuẩn hóa bằng cách chia cho tổng.

Kết quả cho thấy vùng quanh $$0.75$$ là nơi được dữ liệu ủng hộ mạnh nhất trên grid này, vùng quanh $$0.25$$ yếu hơn hẳn, còn hai đầu $$0$$ và $$1$$ gần như không nhận được sự ủng hộ nào đáng kể từ dữ liệu.

Ví dụ này cực kỳ quan trọng vì nó cho ta thấy Bayes không bắt buộc phải bắt đầu bằng tích phân phức tạp. Ta có thể hiểu nó như một quy trình chấm điểm và chuẩn hóa.

## 3. Thuật toán grid approximation

![Các bước của thuật toán grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_algorithm_steps.png)

Quy trình chuẩn có thể viết thành 5 bước.

### Bước 1. Tạo lưới tham số

Ví dụ:

$$
\theta_{\text{grid}} = \text{linspace}(0,1,G).
$$

### Bước 2. Tính prior tại từng điểm

Mỗi điểm trên lưới nhận một trọng số prior.

### Bước 3. Tính likelihood tại từng điểm

Với cùng dữ liệu quan sát, ta xem điểm nào giải thích dữ liệu tốt hơn.

### Bước 4. Nhân prior với likelihood

Đó là posterior chưa chuẩn hóa:

$$
p(\theta_i \mid D) \propto p(D \mid \theta_i)p(\theta_i).
$$

### Bước 5. Chuẩn hóa

Chia cho tổng toàn bộ trọng số để thu được posterior rời rạc hợp lệ.

## 4. Grid mịn hơn thì tốt hơn, nhưng cũng tốn hơn

Một lưới 5 điểm giúp ta nắm ý tưởng, nhưng để xấp xỉ tốt hơn, ta thường phải dùng lưới mịn hơn, chẳng hạn 20 điểm, 100 điểm, hay 1000 điểm, tùy độ chính xác mà ta mong muốn.

![Grid rất thô với 5 điểm]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_5.png)

![Grid trung bình với 20 điểm]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_20.png)

![Grid mịn với 100 điểm]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_resolution_100.png)

Khi grid mịn hơn, posterior rời rạc sẽ nhìn giống posterior liên tục hơn và các thống kê như posterior mean hay credible interval cũng trở nên chính xác hơn.

![So sánh grid 5 điểm với posterior chính xác]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_5.png)

![So sánh grid 20 điểm với posterior chính xác]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_20.png)

![So sánh grid 100 điểm với posterior chính xác]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_vs_exact_100.png)

![Ảnh hưởng của kích thước grid]({{ site.baseurl }}/img/chapter_img/chapter02/grid_size_comparison.png)

Vì vậy, ta luôn đứng trước một trade-off rất đơn giản nhưng không thể né tránh: grid thô thì nhanh nhưng xấp xỉ còn thô, trong khi grid mịn thì chính xác hơn nhưng cũng tốn tính toán hơn.

## 5. Một ví dụ thực tế: prior không liên hợp

Giả sử nhóm phân tích có hai niềm tin cạnh tranh về tỷ lệ khách quay lại, trong đó một giả thuyết cho rằng tỷ lệ này thường quanh $$0.3$$ còn giả thuyết kia cho rằng nó thường quanh $$0.7$$.

Ta có thể biểu diễn prior này như một mixture hai đỉnh. Khi đó posterior thường không còn công thức đóng đẹp như Beta-Binomial nữa, nhưng grid approximation vẫn xử lý được rất tự nhiên vì ta chỉ cần tính giá trị prior mixture ở từng điểm trên lưới, tính likelihood của dữ liệu tại những điểm đó, rồi chuẩn hóa toàn bộ trọng số để thu được posterior.

![Ví dụ grid với prior mixture]({{ site.baseurl }}/img/chapter_img/chapter02/grid_mixture_prior_example.png)

Đây là lý do grid approximation rất mạnh về mặt trực giác: nó không đòi hỏi prior phải liên hợp, mà chỉ yêu cầu rằng ta có thể tính được prior và likelihood trên lưới các giá trị ứng viên.

## 6. Từ posterior trên grid, ta làm được gì?

Rất nhiều thứ, và đó chính là điều làm cho phương pháp này trở nên đáng học hơn là một mẹo tính toán tạm thời.

### 6.1. Tính posterior mean

Ta lấy trung bình có trọng số:

$$
E[\theta \mid D] \approx \sum_i \theta_i p(\theta_i \mid D).
$$

![Posterior mean cùng median và mode trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_mean_median_mode.png)

### 6.2. Tính xác suất của một khoảng

Ví dụ:

$$
P(0.5 \le \theta \le 0.8 \mid D)
$$

chỉ là tổng các trọng số posterior của những điểm nằm trong khoảng đó.

![Xác suất posterior của một khoảng trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_interval_probability.png)

### 6.3. Tính credible interval

Ta cộng dồn xác suất posterior trên grid để lấy các quantile mong muốn.

![Credible interval được lấy từ posterior rời rạc]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_credible_interval.png)

### 6.4. Lấy mẫu từ posterior

Ta có thể lấy mẫu các điểm grid theo trọng số posterior rồi dùng chúng cho các bước tiếp theo.

![Lấy mẫu trực tiếp từ posterior trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_stat_sampling.png)

Grid approximation rất hay ở chỗ tất cả các khái niệm Bayes trở nên hữu hình bằng các phép cộng và nhân đơn giản.

## 7. Posterior predictive với grid

Một khi đã có posterior trên grid, ta có thể dự đoán dữ liệu mới.

Ví dụ, sau khi đã có posterior về xác suất khách mua hàng, ta có thể muốn dự đoán số đơn hàng xuất hiện trong 50 khách tiếp theo.

Ta chỉ cần trung bình hóa phân phối dự đoán điều kiện theo từng điểm trên grid:

$$
P(y_{\text{new}} \mid D) = \sum_i P(y_{\text{new}} \mid \theta_i)p(\theta_i \mid D).
$$

![Phân phối posterior predictive lấy từ posterior trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_predictive_distribution.png)

![So sánh posterior predictive từ grid với công thức chính xác]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_predictive_vs_exact.png)

Đây là bước rất quan trọng vì nó nối posterior của tham số với những dự báo thực tế mà người dùng cuối quan tâm.

## 8. Khi nào grid approximation đặc biệt hữu ích?

### 8.1. Khi học Bayes lần đầu

Grid là một trong những cách tốt nhất để thấy thật rõ prior, likelihood, posterior, bước chuẩn hóa, và cả cách posterior được dùng để tạo ra dự đoán, bởi vì mọi đối tượng đều hiện ra dưới dạng những trọng số cụ thể trên một tập điểm hữu hạn.

### 8.2. Khi bài toán chỉ có 1 tham số

Khi bài toán chỉ có một tham số, grid thường là một lựa chọn rất ổn vì nó vừa dễ hiểu, dễ code, vừa dễ trực quan hóa bằng đồ thị.

### 8.3. Khi muốn kiểm tra một mô hình nhỏ

Ngay cả khi về sau bạn dùng MCMC, grid vẫn có thể đóng vai trò như một điểm tham chiếu tốt cho những ví dụ một tham số, nơi ta muốn biết liệu thuật toán tính toán phức tạp hơn có đang cho ra kết quả hợp lý hay không.

![Khi nào nên dùng grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/when_to_use_grid.png)

## 9. Điểm yếu lớn nhất: curse of dimensionality

Vấn đề xuất hiện khi số tham số tăng.

Nếu mỗi tham số dùng 100 điểm grid, thì một tham số tương ứng với 100 điểm, hai tham số đã nhảy lên 10,000 điểm, ba tham số thành 1,000,000 điểm, và bốn tham số lập tức vọt lên 100,000,000 điểm; chính tốc độ bùng nổ này tạo nên cái gọi là curse of dimensionality.

![Số điểm grid tăng bùng nổ theo số chiều tham số]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_dimensionality_growth.png)

![Bảng tóm tắt vì sao grid approximation nhanh chóng mất khả thi ở nhiều chiều]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_grid_dimensionality_table.png)

Đó là lý do grid approximation rất tuyệt cho bài toán một tham số, còn có thể chấp nhận được cho một số bài hai tham số nhỏ, nhưng lại nhanh chóng trở nên không khả thi khi ta bước sang những mô hình thực tế có nhiều tham số hơn.

## 10. Grid approximation nằm ở đâu trong bức tranh lớn?

Ta có thể xem các phương pháp tính posterior như nằm trên một trục phát triển tự nhiên: conjugate prior cho lời giải nhanh và chính xác nếu bài toán đủ “ngoan”, grid approximation mang lại một cơ chế tính toán trực quan và linh hoạt cho các mô hình nhỏ, còn MCMC là công cụ tổng quát hơn dành cho những mô hình phức tạp với nhiều tham số.

![Từ grid đến MCMC]({{ site.baseurl }}/img/chapter_img/chapter02/grid_to_mcmc_bridge.png)

Grid chính là cây cầu giúp ta hiểu vì sao sau này cần các phương pháp lấy mẫu.

## 11. Những nhầm lẫn phổ biến

### 11.1. “Grid approximation luôn chính xác”

Không. Nó chỉ là xấp xỉ, và độ chính xác của nó phụ thuộc vào độ mịn của grid, vào việc miền grid có phủ đủ vùng posterior quan trọng hay không, và vào chính số tham số của bài toán.

### 11.2. “Chỉ cần tăng grid là xong”

Không. Với nhiều tham số, số điểm tăng theo cấp số mũ nên chi phí bùng nổ rất nhanh.

### 11.3. “Grid là đồ chơi, không đáng học”

Ngược lại. Grid là cách rất tốt để xây trực giác Bayes, hiểu posterior được hình thành thế nào, và chuẩn bị cho MCMC.

## Tóm tắt

**Grid approximation là cách xấp xỉ posterior bằng cách rời rạc hóa không gian tham số thành một lưới điểm.** Ưu thế lớn nhất của phương pháp này là nó rất trực quan, dễ triển khai, không đòi hỏi prior liên hợp, và đặc biệt phù hợp cho những bài toán nhỏ nơi ta muốn nhìn rõ từng bước Bayes đang diễn ra như thế nào. Hạn chế cốt lõi của nó nằm ở chỗ phương pháp này chỉ phù hợp cho rất ít tham số, bởi vì khi số chiều tăng thì số điểm lưới tăng bùng nổ và nhanh chóng làm chi phí tính toán trở nên không thể chấp nhận được. Nếu conjugacy dạy ta Bayes giải tay, thì grid approximation dạy ta Bayes tính toán. Nói gọn lại, điều cần nhớ là grid approximation biến bài toán posterior liên tục thành một bài toán rời rạc trên các điểm ứng viên, nó đặc biệt mạnh cho các mô hình nhỏ và cho những prior không liên hợp, nhưng nó không mở rộng tốt do curse of dimensionality.

## Câu hỏi tự luyện

1. Hãy giải thích bằng lời tại sao grid 5 điểm chỉ cho một xấp xỉ thô.
2. Với bài toán một tham số, vì sao grid approximation là công cụ học rất tốt?
3. Tại sao grid approximation gặp khó khăn nghiêm trọng ở 4 hay 5 tham số?
4. Hãy nêu một ví dụ prior không liên hợp mà grid xử lý dễ hơn giải tích.

## Tài liệu tham khảo

- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2-3.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 6.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 3.

---

*Kết thúc Chapter 02. Bài học tiếp theo: [Chapter 04 - Bayesian Linear Regression](/vi/chapter04/)*
