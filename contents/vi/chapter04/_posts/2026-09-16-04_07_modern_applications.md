---
layout: post
title: "Bài 4.7: MCMC hiện đại — NUTS, HMC và hồi quy Bayes trong thực hành"
chapter: '04'
order: 7
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: optional
---

## Mục tiêu học tập

Sau bài tùy chọn này, bạn hiểu Hamiltonian Monte Carlo và NUTS không phải thuật toán trang trí sau hồi quy tuyến tính Bayes, mà là hệ quả tất yếu khi posterior không còn dạng đóng. Bạn sẽ đọc được một chuỗi Stan, PyMC hoặc NumPyro như một xấp xỉ có kiểm soát của cùng mô hình sinh mà Chương 4 đã viết bằng lời.

## Kiến thức cần có

Các bài 4.1–4.6 đã dựng hồi quy tuyến tính như câu chuyện sinh, chọn prior, và lấy posterior bằng PyMC. Bài 4.2b đã nói về MCMC ở mức lý thuyết lớp học. Bài này không viết lại Metropolis. Nó hỏi sampler hiện đại đang làm gì trong các hệ thống 2022–2026, và vì sao hồi quy tuyến tính vẫn là mô hình được lấy mẫu nhiều nhất.

## Mở đầu

Một khi mô hình có intercept, slope, phương sai, và vài biến dự báo, tích prior–likelihood không còn tích phân bằng tay. Lưới của Chương 2 nổ số ô. Chính xác lý thuyết vì thế trở nên không đủ, không vì ý tưởng Bayes yếu đi, mà vì hình học của posterior đã vượt khỏi giấy. Căng thẳng của bài này là: nếu ta không thể vẽ posterior, ta còn tin được chuỗi số mà máy trả về hay không?

## Phát triển khái niệm

Hamiltonian Monte Carlo dùng gradient của log-posterior để đề xuất bước đi xa mà vẫn chấp nhận được. NUTS (No-U-Turn Sampler) dừng quỹ đạo khi nó bắt đầu quay lại, để người dùng không phải chọn độ dài quỹ đạo bằng tay. Điều sampler đang xấp xỉ là kỳ vọng dưới posterior,

$$
\mathbb E[g(\theta)\mid y]\approx\frac{1}{S}\sum_{s=1}^{S}g(\theta^{(s)}),\qquad \theta^{(s)}\sim p(\theta\mid y),
$$

cùng một đối tượng mà hồi quy Bayes dùng cho hệ số, cho dự báo, và cho khoảng hậu nghiệm. Phần mềm không thay mô hình; nó thay giấy nháp.

## Mô hình như câu chuyện sinh dữ liệu

### 1. NUTS trong Stan, PyMC và NumPyro cho hồi quy phân cấp

Câu chuyện sinh vẫn là: tham số ~ prior, dữ liệu ~ chuẩn quanh một mặt phẳng. Sự khác biệt công nghiệp là mặt phẳng ấy có intercept theo quốc gia, theo chiến dịch, hoặc theo máy chủ. Stan User’s Guide và các notebook PyMC/NumPyro đều lấy NUTS làm mặc định vì gradient của log-density có thể lấy bằng vi phân tự động. Khi bạn đọc một khoảng tin cậy cho hệ số quảng cáo, bạn đang đọc một tóm tắt của chuỗi NUTS, không phải một công thức OLS.

### 2. Pathfinder như khởi động ấm, không phải thay thế MCMC

Zhang, Carpenter, Gelman và Vehtari (2022) đề xuất Pathfinder: đi theo một đường tối ưu quasi-Newton, đặt các xấp xỉ Gaussian dọc đường, rồi lấy mẫu từ xấp xỉ có KL nhỏ nhất. Trên nhiều posterior, các mẫu ấy tốt hơn ADVI và rẻ hơn một chuỗi HMC ngắn, nên Stan và các thư viện JAX dùng Pathfinder để khởi động NUTS. Ý nghĩa sư phạm rất đúng với Chương 4. Variational inference xuất hiện vì MCMC cần một chỗ đứng tốt, không vì posterior đã bị thay bằng một tối ưu hóa.

### 3. BlackJAX và MCMC có thể kết hợp trên gia tốc

Cabezas et al. (2024) mô tả BlackJAX như một hộp nguyên tử thống kê—bước Metropolis, động lực Hamiltonian, cơ chế Langevin—viết bằng JAX để biên dịch lên GPU và TPU. Hồi quy Bayes khi ấy không còn là “một chuỗi trên laptop”, mà là cùng một log-density chạy song song hàng nghìn chuỗi. Câu chuyện sinh không đổi; ngân sách tính toán đổi.

### 4. MCMC cho mạng nơ-ron Bayes

Izmailov, Vikram, Hoffman và Wilson (2021) hỏi posterior của một Bayesian neural network trông thế nào nếu ta thật sự chạy HMC đắt, chứ không tin ngay vào dropout hay một Gaussian chéo. Họ thấy các xấp xỉ phổ biến thường không tái tạo được posterior đầy đủ, nhưng dự báo vẫn có thể hữu ích. Bài học cho sinh viên hồi quy tuyến tính là khiêm tốn và sắc: nếu HMC đã khó đọc trên vài chục hệ số có tương quan, thì “MCMC cho deep learning” là cùng một bài toán hình học, chỉ lớn hơn. Chương 7 sẽ gặp lại các xấp xỉ rẻ hơn.

## Diễn giải và nhận định

Một khoảng hậu nghiệm từ NUTS chỉ đáng tin nếu chuỗi đã trộn và mô hình không sai một cách thô. $$\hat R$$ gần 1 không chứng minh mặt phẳng là nhân quả. Pathfinder có thể ngồi ở một mode phụ và làm NUTS khởi động sai chỗ. BlackJAX nhanh không khiến prior trở nên vô hại. Hãy đọc sampler như một kính lúp: nó phóng to đúng mô hình bạn đã viết, kể cả các giả định Gaussian về phần dư.

## Ứng dụng

Hồi quy tuyến tính Bayes là xương sống của media mix, định giá, và các mô hình phân cấp trong A/B. MCMC hiện đại là lý do những mô hình ấy có thể mang prior thật và vẫn ra posterior dùng được, thay vì dừng ở ước lượng điểm.

## Giới hạn và hướng mở rộng

HMC cần log-density khả vi; dữ liệu rời rạc với tham số rời rạc phải đi đường khác. Các mô hình lớn vẫn cần VI, Laplace, hoặc ensemble. Bài này cố ý không mở lại lý thuyết Markov chain. Chương 5 sẽ làm posterior khó hơn bằng cách thêm nhiều predictor và cấu trúc nhân quả.

## Bài tập

1. Một đồng nghiệp bảo “PyMC đã hội tụ vì trace trông ổn”. Bạn sẽ xin thêm hai chẩn đoán nào, và mỗi cái đang kiểm tra giả định hình học nào?
2. Giải thích, không dùng mã, vì sao Pathfinder có thể vừa là variational inference vừa là phần của workflow MCMC.
3. Trong hồi quy giá nhà với sai số đuôi nặng, NUTS vẫn chạy. Posterior đang xấp xỉ mô hình nào, và PPC sẽ tố cáo điều gì?
4. Đọc trang NUTS của Stan hoặc NumPyro. Chỉ ra một câu trong tài liệu nói về *target log density*. Câu ấy tương ứng đối tượng toán nào của bài 4.1?

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 11–12.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 7, 17.
- Zhang, L., Carpenter, B., Gelman, A., & Vehtari, A. (2022). Pathfinder: Parallel quasi-Newton variational inference. *JMLR*, 23(306). [arXiv:2108.03782](https://arxiv.org/abs/2108.03782).
- Cabezas, A., Corenflos, A., Lao, J., Louf, R., et al. (2024). BlackJAX: Composable Bayesian inference in JAX. [arXiv:2402.10797](https://arxiv.org/abs/2402.10797).
- Izmailov, P., Vikram, S., Hoffman, M. D., & Wilson, A. G. (2021). What are Bayesian neural network posteriors really like? *ICML*.
- [Stan HMC/NUTS](https://mc-stan.org/docs/reference-manual/mcmc.html).
- [NumPyro inference](https://num.pyro.ai/en/stable/mcmc.html).
- [PyMC sampling](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
