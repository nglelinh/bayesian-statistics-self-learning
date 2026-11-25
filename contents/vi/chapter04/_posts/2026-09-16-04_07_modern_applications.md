---
layout: post
title: "Bài 4.7: MCMC hiện đại — NUTS, HMC và hồi quy Bayes trong thực hành"
chapter: '04'
order: 8
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: optional
---

Trong gần nửa thế kỷ sau khi Metropolis–Hastings ra đời, thống kê Bayes vẫn bị giới hạn trong những mô hình nhỏ vì chi phí lấy mẫu quá đắt đỏ. Bước ngoặt chỉ thực sự xảy ra trong thập kỷ gần đây khi ba mảnh ghép hội tụ: thuật toán NUTS tự động điều chỉnh quỹ đạo Hamilton, vi phân tự động trên đồ thị tính toán, và các thư viện chạy song song hàng nghìn chuỗi trên GPU/TPU như BlackJAX hay NumPyro. Định lý Bayes không hề thay đổi, nhưng động cơ tính toán phía sau nó đã bước sang một kỷ nguyên hoàn toàn mới.

## Mục tiêu học tập

Sau bài tùy chọn này, bạn sẽ hiểu Hamiltonian Monte Carlo (HMC) và NUTS không phải phần phụ kỹ thuật đứng sau hồi quy tuyến tính Bayes, mà là giải pháp tất yếu khi phân phối hậu nghiệm không còn công thức dạng đóng. Bạn cũng sẽ biết cách đọc kết quả lấy mẫu từ Stan, PyMC hay NumPyro như một xấp xỉ số có kiểm soát cho đúng mô hình sinh dữ liệu đã thiết lập ở Chương 4.


## Kiến thức cần nhớ: Tập điển hình nhiều chiều, Tích phân Leapfrog và Suy luận lai

Để hiểu vì sao các bộ lấy mẫu giai đoạn 2022–2026 lại có hình hài như ngày nay, cần nhìn rõ ba trụ cột toán học:

- **Tập điển hình (Typical Set) trong không gian nhiều chiều:** Ở 1 chiều, phần lớn khối lượng xác suất nằm quanh đỉnh mật độ (mode). Nhưng ở $$d = 100$$ chiều, thể tích hình cầu tăng theo $$r^{d-1}$$ nên xác suất tập trung trong một lớp vỏ mỏng nằm *cách xa* đỉnh gọi là tập điển hình. Thuật toán tìm cực đại (MAP) bị hút vào đỉnh (nơi ít khối lượng xác suất), còn bước đi ngẫu nhiên dễ nhảy văng khỏi lớp vỏ mỏng đó; HMC dùng động lượng để lướt êm dọc theo đúng lớp vỏ này.
- **Tích phân bảo toàn thể tích (Symplectic Leapfrog Integrator):** Khi mô phỏng phương trình Hamilton rời rạc theo thời gian, phương pháp Euler thông thường làm năng lượng trôi dạt và phá vỡ tính thuận nghịch. Tích phân leapfrog (nửa bước động lượng – trọn bước vị trí – nửa bước động lượng) bảo toàn thể tích pha và gần như bảo toàn năng lượng $$H(\theta, r)$$, giúp tỷ lệ chấp nhận Metropolis tiến sát 100% ngay cả khi bước nhảy rất xa.
- **Phối hợp Suy luận biến phân và MCMC (Pathfinder + NUTS):** Suy luận biến phân (VI) tối ưu nhanh phân kỳ Kullback–Leibler $$\mathrm{KL}(q \Vert p)$$ để tìm một xấp xỉ Gaussian thô gần vùng tập điển hình; dùng nó làm điểm khởi động (warm-start) giúp NUTS bỏ qua giai đoạn dò đường tốn kém mà vẫn giữ nguyên tính chính xác tiệm cận của MCMC.
## Kiến thức cần có

Các bài 4.1–4.6 đã xây dựng hồi quy tuyến tính như một mô hình sinh dữ liệu, trình bày cách chọn phân phối tiên nghiệm và suy luận hậu nghiệm với PyMC, còn Bài 4.2b đã giới thiệu nền tảng toán học của MCMC. Bài này không lặp lại thuật toán Metropolis mà tập trung vào cách các bộ lấy mẫu hiện đại vận hành trong giai đoạn 2022–2026 và lý do hồi quy tuyến tính vẫn là lớp mô hình được lấy mẫu phổ biến nhất.

## Mở đầu

Ngay khi mô hình có hệ số chặn, hệ số dốc, độ nhiễu và vài biến dự báo, tích giữa phân phối tiên nghiệm và hàm hợp lý không còn tính tích phân được bằng tay, trong khi phương pháp lưới ở Chương 2 bùng nổ về số ô tính toán. Rào cản không nằm ở tư duy Bayes, mà ở hình học nhiều chiều của phân phối hậu nghiệm. Câu hỏi trung tâm của bài là: khi không thể vẽ trực tiếp phân phối hậu nghiệm, ta dựa vào đâu để tin tưởng chuỗi số mà máy tính trả về?

## Phát triển khái niệm

Hamiltonian Monte Carlo sử dụng đạo hàm (gradient) của hàm mật độ log hậu nghiệm để đề xuất những bước di chuyển xa mà vẫn duy trì tỷ lệ chấp nhận cao. Biến thể NUTS (No-U-Turn Sampler) tự động dừng quỹ đạo khi nó bắt đầu quay ngược lại, giúp người dùng không phải tự chỉnh độ dài quỹ đạo bằng tay. Về bản chất, đại lượng mà bộ lấy mẫu đang xấp xỉ là kỳ vọng theo phân phối hậu nghiệm:

$$
\mathbb E[g(\theta)\mid y]\approx\frac{1}{S}\sum_{s=1}^{S}g(\theta^{(s)}),\qquad \theta^{(s)}\sim p(\theta\mid y),
$$

chính là công cụ mà hồi quy Bayes dùng để tính ước lượng hệ số, khoảng tin cậy hậu nghiệm và dự báo. Phần mềm lấy mẫu không thay thế mô hình thống kê, mà thay thế phần tính tích phân thủ công.

## Mô hình trong thực hành hiện đại

### 1. NUTS trong Stan, PyMC và NumPyro cho hồi quy phân cấp

Cấu trúc sinh dữ liệu cốt lõi vẫn không đổi: tham số tuân theo phân phối tiên nghiệm, còn dữ liệu dao động theo phân phối Chuẩn quanh một siêu phẳng tuyến tính. Điểm khác biệt trong thực tế công nghiệp là siêu phẳng ấy thường có hệ số chặn thay đổi theo quốc gia, chiến dịch hoặc máy chủ. Tài liệu hướng dẫn của Stan cùng hệ sinh thái PyMC và NumPyro đều chọn NUTS làm mặc định vì đạo hàm của hàm mật độ log có thể tính chính xác bằng vi phân tự động (automatic differentiation). Khi đọc một khoảng tin cậy hậu nghiệm cho hệ số quảng cáo, thực chất bạn đang đọc bản tóm tắt của các mẫu NUTS chứ không phải công thức OLS.

### 2. Pathfinder: bước khởi động ấm thay vì thay thế MCMC

Zhang, Carpenter, Gelman và Vehtari (2022) đề xuất thuật toán Pathfinder: bám theo quỹ đạo tối ưu quasi-Newton, dựng các xấp xỉ Gaussian dọc theo đường đi rồi lấy mẫu từ xấp xỉ có phân kỳ KL nhỏ nhất. Trên nhiều phân phối hậu nghiệm, các mẫu này có chất lượng cao hơn ADVI và tốn ít chi phí hơn một chuỗi HMC ngắn, nên Stan và các thư viện trên nền JAX dùng Pathfinder để khởi động ấm cho NUTS. Ý nghĩa thực hành ở đây rất rõ: suy luận biến phân (variational inference) đóng vai trò tìm điểm xuất phát tốt cho MCMC, chứ không thay thế hoàn toàn việc lấy mẫu hậu nghiệm.

### 3. BlackJAX và MCMC dạng mô-đun trên phần cứng tăng tốc

Cabezas et al. (2024) xây dựng BlackJAX như một tập hợp các khối thuật toán thống kê cơ sở — bước Metropolis, động lực học Hamilton, cơ chế Langevin — viết trên JAX để biên dịch trực tiếp lên GPU và TPU. Khi đó, hồi quy Bayes không còn giới hạn ở vài chuỗi chạy tuần tự trên máy tính cá nhân, mà cùng một hàm mật độ log có thể chạy song song hàng nghìn chuỗi. Mô hình sinh dữ liệu giữ nguyên; điều thay đổi là quy mô năng lực tính toán.

### 4. MCMC cho mạng nơ-ron Bayes

Izmailov, Vikram, Hoffman và Wilson (2021) khảo sát hình dạng thực sự của phân phối hậu nghiệm trong mạng nơ-ron Bayes khi chạy HMC quy mô lớn, thay vì mặc định tin vào dropout hay xấp xỉ Gaussian đường chéo. Kết quả cho thấy các phương pháp xấp xỉ phổ biến thường không tái tạo được đầy đủ phân phối hậu nghiệm thực, dù dự báo thu được vẫn có thể hữu ích. Bài học rút ra cho người học hồi quy tuyến tính rất rõ ràng: nếu HMC đã gặp thách thức hình học ngay trên vài chục hệ số có tương quan, thì MCMC cho học sâu chính là cùng một bài toán hình học đó ở quy mô lớn hơn. Chương 7 sẽ trình bày các phương pháp xấp xỉ nhẹ hơn cho bối cảnh này.

### Giải thích: Chạy tay 1 bước tích phân Leapfrog trong HMC

Vì sao HMC có thể đi một quãng đường dài mà xác suất chấp nhận vẫn gần bằng 1? Hãy tự tay tính đúng một bước leapfrog trên phân phối chuẩn hóa 1 chiều $$p(\theta \mid y) \propto \exp(-\theta^2/2)$$:

1. **Thiết lập Hamiltonian:** Thế năng $$U(\theta) = -\log \tilde p(\theta) = \frac{1}{2}\theta^2$$ nên gradient là $$\nabla U(\theta) = \theta$$; động năng $$K(r) = \frac{1}{2}r^2$$ (khối lượng đơn vị $$M = 1$$).
2. **Trạng thái xuất phát:** Giả sử chuỗi đang ở $$\theta_0 = 1.0$$ và rút động lượng $$r_0 = 0.0$$. Tổng năng lượng ban đầu:
   $$H(\theta_0, r_0) = \frac{1}{2}(1.0)^2 + \frac{1}{2}(0.0)^2 = 0.5000.$$
3. **Thực hiện 1 bước leapfrog với kích thước bước khá lớn $$\epsilon = 0.5$$:**
   - *Nửa bước động lượng:* $$r_{1/2} = r_0 - \frac{\epsilon}{2}\nabla U(\theta_0) = 0 - 0.25(1.0) = -0.25$$.
   - *Trọn bước vị trí:* $$\theta_1 = \theta_0 + \epsilon r_{1/2} = 1.0 + 0.5(-0.25) = 0.875$$.
   - *Nửa bước động lượng cuối:* $$r_1 = r_{1/2} - \frac{\epsilon}{2}\nabla U(\theta_1) = -0.25 - 0.25(0.875) = -0.46875$$.
4. **Kiểm tra bảo toàn năng lượng và bước chấp nhận Metropolis:**
   $$H(\theta_1, r_1) = \frac{1}{2}(0.875)^2 + \frac{1}{2}(-0.46875)^2 = 0.38281 + 0.10986 = 0.49268.$$
   Độ lệch năng lượng chỉ là $$\Delta H = 0.49268 - 0.5000 = -0.00732$$, nên xác suất chấp nhận $$\alpha = \min(1, e^{-\Delta H}) = \min(1, e^{+0.00732}) = 1$$!

Ngay cả với bước $$\epsilon = 0.5$$ rất thô, tích phân leapfrog vẫn giữ năng lượng gần như bất biến — đó chính là bí mật toán học đằng sau hiệu năng vượt trội của NUTS trong Stan, PyMC và BlackJAX.

## Diễn giải và nhận định

Một khoảng hậu nghiệm từ NUTS chỉ đáng tin khi các chuỗi đã trộn đều và bản thân mô hình không sai lệch thô bạo. Chỉ số $$\hat R$$ gần 1 không chứng minh được mối quan hệ là nhân quả. Pathfinder có thể dừng ở một cực đại cục bộ (mode phụ) khiến NUTS khởi động lệch vùng, còn tốc độ của BlackJAX không làm một phân phối tiên nghiệm bất hợp lý trở nên vô hại. Hãy xem bộ lấy mẫu như một kính lúp: nó phóng đại trung thực đúng mô hình bạn đã khai báo, bao gồm cả những giả định chưa chuẩn xác về phần dư.

## Ứng dụng

Hồi quy tuyến tính Bayes là nền tảng của mô hình phân bổ ngân sách truyền thông (media mix modeling), định giá và các mô hình phân cấp trong thử nghiệm A/B. MCMC hiện đại giúp các mô hình này tích hợp được phân phối tiên nghiệm thực chất và trả về phân phối hậu nghiệm đầy đủ thay vì chỉ dừng ở ước lượng điểm.

## Giới hạn và hướng mở rộng

HMC đòi hỏi hàm mật độ log phải khả vi theo tham số; các bài toán có tham số rời rạc cần những phương pháp xử lý khác. Với các mô hình có kích thước rất lớn, thực hành vẫn cần đến suy luận biến phân (VI), xấp xỉ Laplace hoặc tổ hợp mô hình (ensemble). Bài này không đi sâu lại lý thuyết chuỗi Markov; Chương 5 sẽ tiếp tục mở rộng độ phức tạp của phân phối hậu nghiệm khi đưa thêm nhiều biến dự báo và tư duy nhân quả.

## Video tham khảo

- [The intuition behind the Hamiltonian Monte Carlo algorithm](https://www.youtube.com/watch?v=a-wydhEuAm0) — Ben Lambert, English. **xem trước**. Giải thích trực giác HMC trước khi tiếp cận NUTS như cơ chế tự chọn độ dài quỹ đạo, nối tiếp bước chuyển từ Metropolis sang bộ lấy mẫu hiện đại.
- [Michael Betancourt: Scalable Bayesian Inference with Hamiltonian Monte Carlo](https://www.youtube.com/watch?v=jUSZboSq1zg) — London Machine Learning Meetup, English. Michael Betancourt trình bày về suy luận Bayes quy mô lớn bằng Hamiltonian Monte Carlo.
- [#78 Exploring MCMC Sampler Algorithms, with Matt D. Hoffman](https://www.youtube.com/watch?v=KVpAziPblks) — Learning Bayesian Statistics, English. Matt Hoffman, đồng tác giả của NUTS, trao đổi về các thuật toán lấy mẫu MCMC, bổ trợ cho phần diễn giải chuỗi mẫu từ PyMC và Stan.

## Bài tập

1. Một đồng nghiệp nhận xét "PyMC đã hội tụ vì trace plot trông ổn". Bạn sẽ yêu cầu thêm hai chỉ số chẩn đoán nào, và mỗi chỉ số kiểm tra khía cạnh hình học gì của chuỗi?
2. Giải thích bằng lời (không dùng mã nguồn) vì sao Pathfinder vừa là một phương pháp suy luận biến phân, vừa có thể đóng vai trò một bước trong quy trình MCMC.
3. Trong bài toán hồi quy giá nhà có sai số đuôi dày, NUTS vẫn chạy xong bình thường. Phân phối hậu nghiệm thu được đang xấp xỉ mô hình nào, và kiểm tra PPC sẽ chỉ ra dấu hiệu sai lệch gì?
4. Đọc trang tài liệu về NUTS của Stan hoặc NumPyro và chỉ ra một câu đề cập đến *target log density*. Đối tượng đó tương ứng với thành phần toán học nào trong Bài 4.1?

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 11–12.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 7, 17.
- Zhang, L., Carpenter, B., Gelman, A., & Vehtari, A. (2022). Pathfinder: Parallel quasi-Newton variational inference. *JMLR*, 23(306). [arXiv:2108.03782](https://arxiv.org/abs/2108.03782).
- Cabezas, A., Corenflos, A., Lao, J., Louf, R., et al. (2024). BlackJAX: Composable Bayesian inference in JAX. [arXiv:2402.10797](https://arxiv.org/abs/2402.10797).
- Izmailov, P., Vikram, S., Hoffman, M. D., & Wilson, A. G. (2021). What are Bayesian neural network posteriors really like? *ICML*.
- [Stan HMC/NUTS](https://mc-stan.org/docs/reference-manual/mcmc.html).
- [NumPyro inference](https://num.pyro.ai/en/stable/mcmc.html).
- [PyMC sampling](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
