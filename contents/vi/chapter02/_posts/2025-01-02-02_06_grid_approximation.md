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

Ví dụ:

- prior có thể là hỗn hợp hai niềm tin khác nhau,
- likelihood có thể không ăn khớp với prior theo dạng giải tích,
- hoặc ta chỉ đơn giản muốn một cách tính trực quan để nhìn thấy Bayes hoạt động.

Lúc đó, grid approximation là cách đơn giản nhất để bắt đầu.

![Giới thiệu trực quan về grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_approximation_intro.png)

## 1. Ý tưởng cốt lõi: thay đường liên tục bằng một tập điểm

Giả sử tham số $$\theta$$ nằm trong đoạn $$[0,1]$$. Thay vì xét mọi giá trị liên tục có thể có của $$\theta$$, ta chọn một số điểm trên đoạn này:

$$
\theta_1,\theta_2,\dots,\theta_G.
$$

Ở mỗi điểm, ta tính:

- prior,
- likelihood,
- posterior chưa chuẩn hóa.

Cuối cùng, ta chuẩn hóa các trọng số này để thu được một posterior rời rạc trên lưới.

Nói bằng lời:

**grid approximation biến một bài toán liên tục thành một bài toán “chấm điểm” trên nhiều điểm ứng viên.**

## 2. Ví dụ tay rất nhỏ: 6 ngửa trong 9 lần tung

Giả sử:

- prior đều trên $$[0,1]$$,
- dữ liệu là 6 ngửa trong 9 lần tung,
- ta dùng grid 5 điểm:

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

Kết quả cho thấy:

- vùng quanh $$0.75$$ được dữ liệu ủng hộ mạnh nhất trên grid này,
- vùng quanh $$0.25$$ yếu hơn hẳn,
- hai đầu $$0$$ và $$1$$ gần như không được dữ liệu ủng hộ.

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

Một lưới 5 điểm giúp ta hiểu ý tưởng. Nhưng để xấp xỉ tốt hơn, ta thường cần lưới mịn hơn:

- 20 điểm,
- 100 điểm,
- 1000 điểm.

![So sánh grid với các độ mịn khác nhau]({{ site.baseurl }}/img/chapter_img/chapter02/grid_approximation_basics.png)

Khi grid mịn hơn:

- posterior rời rạc nhìn giống posterior liên tục hơn,
- các thống kê như mean hay credible interval chính xác hơn.

![Ảnh hưởng của kích thước grid]({{ site.baseurl }}/img/chapter_img/chapter02/grid_size_comparison.png)

Đây là một trade-off rất đơn giản:

- grid thô  $$\rightarrow$$ nhanh nhưng xấp xỉ thô,
- grid mịn  $$\rightarrow$$ chính xác hơn nhưng tốn tính toán hơn.

## 5. Một ví dụ thực tế: prior không liên hợp

Giả sử nhóm phân tích có hai niềm tin cạnh tranh về tỷ lệ khách quay lại:

- giả thuyết 1: tỷ lệ thường quanh $$0.3$$,
- giả thuyết 2: tỷ lệ thường quanh $$0.7$$.

Ta có thể biểu diễn prior như một mixture hai đỉnh. Khi đó posterior thường không còn công thức đóng đẹp như Beta-Binomial nữa. Nhưng grid approximation vẫn xử lý được rất tự nhiên:

1. tính giá trị prior mixture ở từng điểm,
2. tính likelihood dữ liệu ở từng điểm,
3. chuẩn hóa để ra posterior.

![Ví dụ grid với prior mixture]({{ site.baseurl }}/img/chapter_img/chapter02/grid_mixture_prior_example.png)

Đây là lý do grid approximation rất mạnh về mặt trực giác:

- nó không yêu cầu prior phải liên hợp,
- chỉ cần bạn tính được prior và likelihood trên lưới.

## 6. Từ posterior trên grid, ta làm được gì?

Rất nhiều thứ.

### 6.1. Tính posterior mean

Ta lấy trung bình có trọng số:

$$
E[\theta \mid D] \approx \sum_i \theta_i p(\theta_i \mid D).
$$

### 6.2. Tính xác suất của một khoảng

Ví dụ:

$$
P(0.5 \le \theta \le 0.8 \mid D)
$$

chỉ là tổng các trọng số posterior của những điểm nằm trong khoảng đó.

### 6.3. Tính credible interval

Ta cộng dồn xác suất posterior trên grid để lấy các quantile mong muốn.

### 6.4. Lấy mẫu từ posterior

Ta có thể lấy mẫu các điểm grid theo trọng số posterior rồi dùng chúng cho các bước tiếp theo.

![Tính các thống kê từ posterior trên grid]({{ site.baseurl }}/img/chapter_img/chapter02/grid_statistics_computation.png)

Grid approximation rất hay ở chỗ tất cả các khái niệm Bayes trở nên hữu hình bằng các phép cộng và nhân đơn giản.

## 7. Posterior predictive với grid

Một khi đã có posterior trên grid, ta có thể dự đoán dữ liệu mới.

Ví dụ:

- hiện tại đã có posterior về xác suất khách mua hàng,
- ta muốn dự đoán số đơn hàng trong 50 khách tiếp theo.

Ta chỉ cần trung bình hóa phân phối dự đoán điều kiện theo từng điểm trên grid:

$$
P(y_{\text{new}} \mid D) = \sum_i P(y_{\text{new}} \mid \theta_i)p(\theta_i \mid D).
$$

![Posterior predictive từ grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/grid_posterior_predictive.png)

Đây là bước rất quan trọng vì nó nối posterior của tham số với những dự báo thực tế mà người dùng cuối quan tâm.

## 8. Khi nào grid approximation đặc biệt hữu ích?

### 8.1. Khi học Bayes lần đầu

Grid là cách tốt nhất để thấy thật rõ:

- prior,
- likelihood,
- posterior,
- chuẩn hóa,
- và dự đoán.

### 8.2. Khi bài toán chỉ có 1 tham số

Lúc này grid thường rất ổn:

- dễ hiểu,
- dễ code,
- dễ vẽ.

### 8.3. Khi muốn kiểm tra một mô hình nhỏ

Ngay cả khi sau này bạn dùng MCMC, grid vẫn có thể là điểm tham chiếu tốt cho các ví dụ một tham số.

![Khi nào nên dùng grid approximation]({{ site.baseurl }}/img/chapter_img/chapter02/when_to_use_grid.png)

## 9. Điểm yếu lớn nhất: curse of dimensionality

Vấn đề xuất hiện khi số tham số tăng.

Nếu mỗi tham số dùng 100 điểm grid:

- 1 tham số  $$\rightarrow$$ 100 điểm,
- 2 tham số  $$\rightarrow$$ 10,000 điểm,
- 3 tham số  $$\rightarrow$$ 1,000,000 điểm,
- 4 tham số  $$\rightarrow$$ 100,000,000 điểm.

![Curse of dimensionality]({{ site.baseurl }}/img/chapter_img/chapter02/curse_of_dimensionality.png)

Đó là lý do grid approximation:

- rất tuyệt cho bài 1 tham số,
- còn chấp nhận được cho bài 2 tham số nhỏ,
- nhưng nhanh chóng trở nên không khả thi với mô hình thực tế nhiều tham số.

## 10. Grid approximation nằm ở đâu trong bức tranh lớn?

Ta có thể xem các phương pháp tính posterior theo một trục phát triển:

- conjugate prior: nhanh và chính xác nếu bài toán đủ “ngoan”,
- grid approximation: trực quan, linh hoạt, tốt cho mô hình nhỏ,
- MCMC: tổng quát hơn, dùng cho mô hình phức tạp nhiều tham số.

![Từ grid đến MCMC]({{ site.baseurl }}/img/chapter_img/chapter02/grid_to_mcmc_bridge.png)

Grid chính là cây cầu giúp ta hiểu vì sao sau này cần các phương pháp lấy mẫu.

## 11. Những nhầm lẫn phổ biến

### 11.1. “Grid approximation luôn chính xác”

Không. Nó là xấp xỉ. Độ chính xác phụ thuộc vào:

- độ mịn của grid,
- miền grid có phủ đủ vùng posterior hay không,
- và số tham số của bài toán.

### 11.2. “Chỉ cần tăng grid là xong”

Không. Với nhiều tham số, số điểm tăng theo cấp số mũ nên chi phí bùng nổ rất nhanh.

### 11.3. “Grid là đồ chơi, không đáng học”

Ngược lại. Grid là cách rất tốt để xây trực giác Bayes, hiểu posterior được hình thành thế nào, và chuẩn bị cho MCMC.

## Tóm tắt

**Grid approximation là cách xấp xỉ posterior bằng cách rời rạc hóa không gian tham số thành một lưới điểm.**

Ưu điểm:

- rất trực quan,
- dễ triển khai,
- không cần prior liên hợp,
- tốt cho các bài toán nhỏ.

Hạn chế:

- chỉ phù hợp cho rất ít tham số,
- càng nhiều tham số càng nhanh chóng không khả thi.

Nếu conjugacy dạy ta Bayes giải tay, thì grid approximation dạy ta Bayes tính toán.

> **3 ý cần nhớ.**
> 1. Grid approximation biến posterior liên tục thành một bài toán rời rạc gồm nhiều điểm ứng viên.
> 2. Phương pháp này rất trực quan và mạnh cho bài toán nhỏ, nhất là khi prior không liên hợp.
> 3. Điểm yếu cốt lõi của grid là curse of dimensionality, nên nó chỉ phù hợp cho rất ít tham số.

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

*Kết thúc Chapter 02. Bài học tiếp theo: [Chapter 03 - Sampling, Monte Carlo, và MCMC](/vi/chapter03/)*
