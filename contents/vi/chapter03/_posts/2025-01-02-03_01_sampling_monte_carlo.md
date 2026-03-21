---
layout: post
title: "Bài 3.1: Từ Tích phân Khó đến Sampling - Nền tảng Monte Carlo"
chapter: '03'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu vì sao sampling là chìa khóa của Bayesian computation hiện đại. Bạn cũng cần thấy được ý tưởng rất quan trọng của Monte Carlo: khi tích phân quá khó, ta có thể thay nó bằng mô phỏng ngẫu nhiên và trung bình mẫu. Quan trọng hơn, bạn cần cảm được vì sao đây không chỉ là một “mẹo số học”, mà là một cách rất thực tế để học từ phân phối posterior.

> **Ví dụ mini.** Bạn muốn biết xác suất trung bình một khách hàng sẽ chi tiêu bao nhiêu tiền trong tuần tới, nhưng posterior của tham số trong mô hình quá phức tạp để tính tích phân bằng tay. Thay vì cố giải công thức, ta lấy nhiều mẫu từ posterior rồi tính trung bình trên các mẫu đó.
>
> **Câu hỏi tự kiểm tra.** Nếu bạn lấy đủ nhiều mẫu từ đúng posterior, vì sao trung bình của các mẫu lại có thể thay thế cho tích phân?

## 1. Vấn đề thật sự của Bayes trong thực hành

Ở Chapter 2, ta đã thấy những ví dụ rất đẹp như Beta-Binomial, nơi posterior có công thức đóng. Nhưng đó mới chỉ là phần “dễ thương” của Bayes.

Trong thực tế, mô hình thường có dạng như:

- hồi quy logistic,
- mô hình phân cấp,
- mixture model,
- mô hình có nhiều tham số tương quan mạnh,

và khi đó posterior không còn cho ta một công thức gọn để lấy mean, variance hay credible interval.

Ta thường phải tính những đại lượng kiểu:

$$
E[f(\theta)\mid D] = \int f(\theta)\,p(\theta\mid D)\,d\theta.
$$

Vấn đề là tích phân này có thể rất khó, đặc biệt khi:

- số tham số lớn,
- posterior méo hoặc đa đỉnh,
- hoặc ta chỉ biết posterior tới một hằng số tỉ lệ.

## 2. Grid approximation vì sao không đủ?

Bạn có thể nghĩ tới grid approximation:

- chia không gian tham số thành nhiều điểm,
- tính posterior ở từng điểm,
- rồi cộng lại để xấp xỉ tích phân.

Ý tưởng này rất tốt cho 1 hoặc 2 tham số. Nhưng khi số tham số tăng, số điểm cần tính tăng cực nhanh.

Ví dụ:

- 1 tham số, 100 điểm  $$\rightarrow$$ 100 điểm,
- 2 tham số  $$\rightarrow$$ 10,000 điểm,
- 3 tham số  $$\rightarrow$$ 1,000,000 điểm,
- 5 tham số  $$\rightarrow$$ 10,000,000,000 điểm.

![Curse of dimensionality chi tiết]({{ site.baseurl }}/img/chapter_img/chapter03/curse_of_dimensionality_detailed.png)

Đây là lúc ta cần một cách nghĩ khác:

- không cố phủ kín toàn bộ không gian,
- mà chỉ ghé thăm những vùng quan trọng theo đúng phân phối posterior.

## 3. Monte Carlo: thay tích phân bằng trung bình trên mẫu

Đây là ý tưởng quan trọng nhất của bài.

Nếu ta có thể lấy mẫu:

$$
\theta^{(1)},\theta^{(2)},\dots,\theta^{(S)} \sim p(\theta\mid D),
$$

thì ta có thể xấp xỉ:

$$
E[f(\theta)\mid D]
\approx
\frac{1}{S}\sum_{s=1}^{S} f\big(\theta^{(s)}\big).
$$

Nói đơn giản:

- tích phân kỳ vọng dưới posterior
- được thay bằng trung bình của hàm trên các mẫu rút ra từ posterior.

Đây là Monte Carlo estimation.

## 4. Một ví dụ cực dễ hiểu: ước lượng diện tích bằng ném điểm ngẫu nhiên

Monte Carlo không chỉ là chuyện của Bayes. Ý tưởng của nó có thể hiểu bằng ví dụ hình học.

Giả sử bạn muốn ước lượng diện tích của một hình tròn nội tiếp trong hình vuông. Bạn:

1. ném thật nhiều điểm ngẫu nhiên vào hình vuông,
2. đếm xem có bao nhiêu điểm rơi vào trong hình tròn,
3. dùng tỷ lệ đó để suy ra diện tích hình tròn.

Không hề có tích phân giải tay ở đây, nhưng bạn vẫn ước lượng được đại lượng cần biết bằng mô phỏng ngẫu nhiên.

Đó chính là tinh thần của Monte Carlo:

- thay vì giải chính xác,
- ta mô phỏng thật nhiều,
- rồi dùng trung bình để tiến gần đáp án.

![Monte Carlo integration và sự hội tụ]({{ site.baseurl }}/img/chapter_img/chapter03/monte_carlo_integration_convergence.png)

## 5. Vì sao Monte Carlo hoạt động?

Lý do sâu hơn nằm ở **luật số lớn**.

Nếu các mẫu được lấy từ đúng phân phối mục tiêu, thì khi số mẫu tăng:

- trung bình mẫu sẽ tiến gần tới kỳ vọng thật.

Nói dễ hiểu hơn:

- một vài mẫu đầu có thể rất dao động,
- nhưng càng lấy nhiều mẫu, trung bình càng ổn định.

![Luật số lớn trong bối cảnh MCMC]({{ site.baseurl }}/img/chapter_img/chapter03/law_of_large_numbers_mcmc.png)

Đây là lý do Monte Carlo rất thực dụng:

- không cần giải tích đẹp,
- chỉ cần lấy mẫu đúng cách và đủ nhiều.

## 6. Monte Carlo giúp ta tính được những gì?

Rất nhiều thứ.

### 6.1. Posterior mean

$$
E[\theta\mid D] \approx \frac{1}{S}\sum_{s=1}^S \theta^{(s)}.
$$

### 6.2. Xác suất vượt ngưỡng

Ví dụ:

$$
P(\theta > 0.5 \mid D)
$$

được ước lượng bằng tỷ lệ số mẫu thỏa mãn điều kiện đó.

### 6.3. Credible interval

Ta chỉ cần lấy quantile từ dãy mẫu posterior.

### 6.4. Posterior predictive

Ta có thể sinh dữ liệu mới từ từng mẫu tham số rồi ghép lại để dự báo tương lai.

Chính vì vậy, khi đã có mẫu từ posterior, phần lớn các câu hỏi Bayesian trở nên rất dễ trả lời.

## 7. Khó khăn còn lại: lấy mẫu từ posterior như thế nào?

Đây là nút thắt của cả chương.

Trong các ví dụ đơn giản, ta có thể lấy mẫu trực tiếp từ phân phối quen thuộc. Nhưng với posterior phức tạp, ta thường:

- không biết cách lấy mẫu trực tiếp,
- chỉ biết posterior đến một hằng số tỉ lệ,
- và không thể tạo các mẫu độc lập dễ dàng.

Vì vậy, Monte Carlo mới chỉ giải quyết **một nửa bài toán**.

Nửa còn lại là:

- làm sao tạo ra các mẫu gần như đến từ posterior?

Câu trả lời là:

- Markov chains,
- MCMC,
- Metropolis-Hastings,
- HMC,
- NUTS.

Đó là lý do Chapter 3 đi theo đúng thứ tự này.

## 8. Một trực giác rất quan trọng

Trong Bayesian computation, mục tiêu không phải là biết công thức đẹp của posterior. Mục tiêu là:

- ghé thăm posterior đủ tốt,
- lấy đủ nhiều mẫu đại diện,
- rồi dùng các mẫu ấy để tính mọi đại lượng ta cần.

Đây là một thay đổi rất lớn trong tư duy:

- từ “giải công thức” sang “mô phỏng thông minh”.

## 9. Monte Carlo tốt ở đâu, yếu ở đâu?

### Điểm mạnh

- rất tổng quát,
- không đòi hỏi công thức đóng,
- tự nhiên với nhiều loại câu hỏi hậu nghiệm,
- càng nhiều mẫu càng ổn định.

### Điểm yếu

- nếu chưa lấy mẫu được từ posterior thì chưa làm gì được,
- tốc độ hội tụ theo $$1/\sqrt{S}$$ nên muốn chính xác hơn nhiều phải lấy khá nhiều mẫu,
- chất lượng kết quả phụ thuộc mạnh vào chất lượng mẫu.

Điều này dẫn thẳng tới các bài sau:

- Markov chain để hiểu chuỗi phụ thuộc,
- Metropolis-Hastings để biết cách sinh mẫu,
- HMC để tăng hiệu quả,
- diagnostics để kiểm tra mẫu có đáng tin không.

> **3 ý cần nhớ.**
> 1. Monte Carlo biến bài toán tích phân khó thành bài toán lấy mẫu rồi tính trung bình trên mẫu.
> 2. Nếu lấy được mẫu từ đúng posterior, ta có thể ước lượng gần như mọi đại lượng Bayesian quan tâm.
> 3. Vấn đề lớn nhất không phải là “tính trung bình thế nào” mà là “làm sao lấy được mẫu tốt từ posterior”.

## Câu hỏi tự luyện

1. Vì sao grid approximation thất bại nhanh khi số tham số tăng?
2. Hãy giải thích bằng lời vì sao trung bình trên mẫu có thể thay thế cho tích phân kỳ vọng.
3. Khi đã có mẫu posterior, bạn có thể tính được những loại đại lượng nào?
4. Trong Chapter 3, vì sao Monte Carlo mới chỉ là bước đầu chứ chưa phải lời giải đầy đủ?

## Tài liệu tham khảo

- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 3.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 11.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 7.

---

*Bài học tiếp theo: [3.2 Markov Chains - Nền tảng Toán học của MCMC](/vi/chapter03/markov-chain/)*
