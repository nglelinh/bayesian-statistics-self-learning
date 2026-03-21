---
layout: post
title: "Bài 3.3: Metropolis-Hastings - Thuật toán MCMC Đầu tiên"
chapter: '03'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu Metropolis-Hastings như thuật toán MCMC nền tảng nhất: đề xuất một điểm mới, so sánh nó với điểm hiện tại, rồi quyết định chấp nhận hay từ chối. Bạn cũng cần nắm trực giác về acceptance rate, mixing, và vì sao random walk vừa đơn giản vừa có nhiều giới hạn.

> **Ví dụ mini.** Hãy tưởng tượng bạn đang tìm vùng đông người nhất trong một lễ hội bằng cách đi thử từng bước nhỏ. Nếu điểm mới có vẻ “đông vui hơn”, bạn thường ở lại; nếu kém hơn, đôi khi bạn vẫn chấp nhận để tránh mắc kẹt ở một góc nhỏ. Đó là tinh thần của Metropolis-Hastings.
>
> **Câu hỏi tự kiểm tra.** Tại sao thuật toán lại không luôn luôn bác bỏ các điểm có posterior thấp hơn điểm hiện tại?

## 1. Ta cần một chuỗi Markov có posterior làm phân phối dừng

Ở bài trước, ta đã học rằng MCMC cần một chuỗi Markov sao cho:

- chạy đủ lâu,
- chuỗi đó phân bố theo posterior.

Metropolis-Hastings là một cách xây chuỗi như vậy.

Ý tưởng của nó rất đơn giản:

1. đang ở một điểm hiện tại,
2. đề xuất một điểm mới,
3. nếu điểm mới tốt hơn thì thường nhận,
4. nếu tệ hơn thì đôi khi vẫn nhận.

Chính bước “đôi khi vẫn nhận” là thứ khiến thuật toán mạnh hơn một quy trình leo dốc tham lam.

## 2. Trực giác: vì sao không chỉ đi tới điểm tốt hơn?

Nếu bạn chỉ luôn đi tới nơi posterior cao hơn, bạn dễ bị:

- mắc kẹt ở một vùng cục bộ,
- không khám phá được toàn bộ posterior,
- và biến bài toán lấy mẫu thành bài toán tối ưu.

Nhưng MCMC không phải tối ưu hóa. Nó cần:

- đi qua các vùng với tần suất đúng theo posterior.

Vì vậy, đôi khi chấp nhận bước “kém hơn” lại là điều rất cần thiết để:

- thoát bẫy,
- di chuyển linh hoạt,
- và giữ đúng phân phối dừng.

## 3. Thuật toán Metropolis-Hastings hoạt động thế nào?

Giả sử đang ở trạng thái hiện tại $$\theta^{(t)}$$.

### Bước 1. Đề xuất một điểm mới

Ta lấy:

$$
\theta^\* \sim q(\theta^\* \mid \theta^{(t)}),
$$

trong đó $$q$$ là proposal distribution.

Nếu proposal là random walk Gaussian, thì:

- điểm mới thường nằm gần điểm hiện tại.

### Bước 2. Tính tỷ lệ chấp nhận

Ta so sánh mức độ hợp lý của điểm mới với điểm cũ thông qua:

$$
\alpha = \min\left(1,\;
\frac{p(\theta^\*\mid D)\,q(\theta^{(t)}\mid \theta^\*)}
{p(\theta^{(t)}\mid D)\,q(\theta^\*\mid \theta^{(t)})}
\right).
$$

Nếu proposal đối xứng, công thức đơn giản hơn:

$$
\alpha = \min\left(1,\;
\frac{p(\theta^\*\mid D)}{p(\theta^{(t)}\mid D)}
\right).
$$

### Bước 3. Chấp nhận hoặc từ chối

- với xác suất $$\alpha$$, chuyển sang $$\theta^\*$$,
- nếu không, ở lại $$\theta^{(t)}$$.

Đó là toàn bộ thuật toán.

## 4. Một cách đọc cực kỳ trực giác

Nếu điểm mới có posterior cao hơn điểm cũ:

- tỷ lệ > 1,
- nên gần như luôn nhận.

Nếu điểm mới có posterior thấp hơn:

- vẫn có thể nhận,
- nhưng với xác suất nhỏ hơn.

Cách hành xử này tạo ra đúng điều ta muốn:

- chuỗi có xu hướng ở nhiều hơn tại các vùng posterior cao,
- nhưng vẫn không bị đóng băng ở một chỗ.

![Metropolis-Hastings minh họa trực quan]({{ site.baseurl }}/img/chapter_img/chapter03/metropolis_hastings.png)

## 5. Ví dụ đồng xu: posterior một tham số

Giả sử posterior của $$\theta$$ là một phân phối trên đoạn $$[0,1]$$. Ta bắt đầu từ một giá trị nào đó, ví dụ $$0.5$$.

Mỗi bước:

- đề xuất một giá trị mới gần đó,
- kiểm tra xem giá trị mới hợp với posterior đến đâu,
- rồi nhận hoặc từ chối.

Sau rất nhiều bước, các giá trị được ghé thăm sẽ phản ánh hình dạng của posterior.

Điểm đẹp ở đây là:

- ta không cần biết hằng số chuẩn hóa của posterior,
- chỉ cần biết posterior tới một hằng số tỉ lệ.

Đây là một trong những lý do MH từng là bước đột phá lớn.

## 6. Proposal distribution ảnh hưởng cực mạnh

Toàn bộ hiệu quả của MH phụ thuộc nhiều vào proposal.

### Proposal quá nhỏ

Chuỗi di chuyển rất chậm:

- acceptance rate cao,
- nhưng mỗi bước chỉ nhích rất ít,
- autocorrelation cao,
- mixing kém.

### Proposal quá lớn

Điểm mới thường rơi vào vùng posterior thấp:

- bị từ chối nhiều,
- chuỗi đứng yên thường xuyên,
- cũng mixing kém.

### Proposal vừa phải

Chuỗi di chuyển đủ xa để khám phá,
nhưng không quá xa để bị từ chối liên tục.

![Ảnh hưởng của acceptance rate]({{ site.baseurl }}/img/chapter_img/chapter03/acceptance_rate_effects.png)

## 7. Good mixing và poor mixing trông như thế nào?

Một chuỗi tốt nên:

- đi qua nhiều vùng hợp lý,
- không mắc kẹt quá lâu,
- không đứng yên quá nhiều,
- không di chuyển quá chậm như con sâu bò.

Ngược lại, poor mixing thường có dạng:

- chuỗi bị dính ở một chỗ,
- nhảy được rất ít,
- hoặc chỉ loanh quanh cục bộ.

![Chất lượng mixing của chain]({{ site.baseurl }}/img/chapter_img/chapter03/chain_mixing_quality.png)

MH đặc biệt dễ bị poor mixing khi:

- posterior có tương quan mạnh,
- posterior nhiều chiều,
- hoặc vùng posterior hẹp và cong.

## 8. Vì sao MH vẫn rất quan trọng dù có HMC?

Ngày nay, trong nhiều mô hình liên tục trơn, HMC và NUTS thường mạnh hơn. Nhưng MH vẫn đáng học vì:

### 8.1. Nó là thuật toán MCMC nguyên bản và dễ hiểu nhất

Nếu chưa hiểu MH, bạn sẽ khó cảm được MCMC đang làm gì.

### 8.2. Nó làm lộ rõ cấu trúc của MCMC

Mọi sampler phức tạp hơn đều vẫn xoay quanh:

- đề xuất,
- đánh giá,
- chấp nhận/từ chối.

### 8.3. Nó hữu ích trong các bài toán đơn giản hoặc không khả vi

Không phải mô hình nào cũng có gradient đẹp như HMC mong muốn.

## 9. Giới hạn lớn nhất của Metropolis-Hastings

MH thường hoạt động như random walk.

Điều này dẫn tới ba vấn đề lớn:

- di chuyển chậm trong không gian nhiều chiều,
- dễ bị autocorrelation cao,
- tốn nhiều bước chỉ để khám phá một posterior hẹp và tương quan mạnh.

Đây chính là động lực để ra đời HMC:

- dùng gradient để đi có hướng,
- thay vì đi dò dẫm kiểu random walk.

![So sánh HMC với MH]({{ site.baseurl }}/img/chapter_img/chapter03/hmc_vs_mh.png)

## 10. Một hình ảnh nên nhớ

Nếu Monte Carlo là “tính trung bình trên mẫu”, thì Metropolis-Hastings là:

- một người đi bộ dò dẫm trong bản đồ posterior,
- bước nào hợp lý thì hay giữ,
- bước nào kém hơn thì đôi khi vẫn thử.

Đó là một cơ chế đơn giản nhưng đủ để tạo ra đúng phân phối dừng ta cần.

> **3 ý cần nhớ.**
> 1. Metropolis-Hastings xây chuỗi MCMC bằng ba bước: đề xuất, tính xác suất chấp nhận, rồi chấp nhận hoặc từ chối.
> 2. Không phải lúc nào cũng nhận các điểm tốt hơn và bác bỏ các điểm kém hơn; việc đôi khi nhận điểm kém là cần thiết để khám phá posterior đúng cách.
> 3. Proposal distribution quyết định mạnh tới hiệu quả của MH, và random walk là lý do khiến MH chậm ở các bài toán khó.

## Câu hỏi tự luyện

1. Vì sao MH không cần biết hằng số chuẩn hóa của posterior?
2. Tại sao proposal quá nhỏ và proposal quá lớn đều có thể làm chain hoạt động kém?
3. Vì sao chấp nhận đôi khi một bước “xấu hơn” lại giúp thuật toán tốt hơn?
4. Hãy giải thích bằng lời vì sao MH mang bản chất random walk.

## Tài liệu tham khảo

- Brooks et al. *Handbook of Markov Chain Monte Carlo*.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 11.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 7.

---

*Bài học tiếp theo: [3.4 Hamiltonian Monte Carlo - Tăng Tốc MCMC với Gradient](/vi/chapter03/hamiltonian-monte-carlo/)*
