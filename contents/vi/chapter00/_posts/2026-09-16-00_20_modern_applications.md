---
layout: post
title: "Bài 0.20: Ứng dụng hiện đại của xác suất nền tảng trong khoa học dữ liệu"
chapter: '00'
order: 22
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: optional
---

## Mục tiêu học tập

Sau bài tùy chọn này, bạn không còn nhìn xác suất, phân phối đồng thời (joint distribution), kỳ vọng, log-probability và mô phỏng như phần “ôn trước khi vào Bayes”, mà thấy chúng chính là ngôn ngữ mà khoa học máy tính và khoa học dữ liệu đang dùng khi hỏi một mô hình có được hiệu chỉnh (calibration) hay không, có ổn định số học hay không, và có kể được câu chuyện sinh dữ liệu hay không. Sự chuyển đổi cần đạt được là đổi tư thế: công cụ nền tảng trở thành câu hỏi thiết kế.

## Kiến thức cần có

Bài viết giả định bạn đã học các bài bắt buộc của Chương 0. Nó không thêm lý thuyết xác suất mới. Nó chỉ hỏi điều gì xảy ra khi những ý tưởng ấy rời lớp học và đi vào bộ phân loại, mô hình ngôn ngữ, và chương trình xác suất.

## Mở đầu

Một sinh viên vừa học xong Chương 0 có thể tính trung bình, viết mật độ, và mô phỏng một sampling distribution. Các bài toán công nghiệp trông lớn hơn, nhưng chúng thường hỏng vì cùng những lý do nhỏ: một xác suất được báo cáo không phải tần suất dài hạn, một tích các likelihood quá nhỏ bị underflow, hoặc một mô hình đồng thời được viết như thể các biến độc lập. Căng thẳng trí tuệ của bài này vì thế khiêm tốn nhưng hữu ích. Nếu nền tảng đã có, vì sao hệ thống hiện đại vẫn đọc sai bất định? Vì quy mô không thay thế ý nghĩa của một phát biểu xác suất.

## Phát triển khái niệm

Một số $$p$$ gắn với dự báo là một tuyên bố về quá trình sinh dữ liệu. Nếu mô hình nói $$p=0.9$$ trên một trăm trường hợp, khoảng chín mươi trường hợp ấy phải đúng nếu con số được hiệu chỉnh. Đó chính là ý tưởng sampling distribution, nay áp vào điểm số học máy thay vì vào trung bình mẫu. Cấu trúc đồng thời quan trọng vì cùng một lý do: khi hai biến cố phụ thuộc, tích các biên không còn là câu chuyện về thế giới. Mô phỏng vẫn là cách rẻ nhất để xem câu chuyện ấy có khả thi hay không.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Hiệu chỉnh xác suất của bộ phân loại và mô hình ngôn ngữ

Bộ lọc thư rác, điểm gian lận, và cảnh báo y tế đều xuất ra một số trông giống xác suất. Câu hỏi sinh dữ liệu không phải “mô hình xếp hạng có tốt không?”, mà là “nếu mô hình tuyên bố $$P(\text{dương}\mid x)=0.8$$, có thật tám trên mười trường hợp như vậy xảy ra không?” Kadavath et al. (2022) cho thấy các mô hình ngôn ngữ lớn có thể được hiệu chỉnh khá tốt trên các câu hỏi đúng/sai và trắc nghiệm được định dạng rõ, và có thể được hỏi $$P(\text{True})$$ sau khi chúng đề xuất một câu trả lời. Tian et al. (2023) tiếp tục cho thấy các mô hình tinh chỉnh bằng phản hồi người thường cho độ tin verbalized (nói thành lời) được hiệu chỉnh tốt hơn xác suất token thô. Bài học Chương 0 rất chính xác: một số trong $$[0,1]$$ chưa tự động là xác suất cho đến khi nó chịu được một phép kiểm tra tần suất.

### 2. Log-probability và ổn định số học trong mô hình lớn

Huấn luyện và suy luận trên mạng hiện đại liên tục đánh giá tích các xác suất. Ở thang log, tích trở thành tổng,

$$
\log p(x_{1:n})=\sum_{i=1}^{n}\log p(x_i\mid x_{<i}),
$$

đó là lý do Chương 0 nhấn mạnh log-probability. Cùng một đẳng thức ấy giữ cho likelihood của mô hình ngôn ngữ không bị underflow, và biến thủ thuật log-sum-exp thành một nguyên thủy chuẩn. Mô hình tin rằng các token được sinh tuần tự; máy tính chỉ tin câu chuyện đó nếu phép tính không sụp về không.

### 3. Phân phối đồng thời trong lập trình xác suất

Một chương trình PyMC hoặc NumPyro là một phân phối đồng thời viết dưới dạng công thức sinh: trước hết lấy mẫu tham số, rồi lấy mẫu dữ liệu cho tham số. Đó đúng là định nghĩa mô hình thống kê của Chương 0, nay được biên dịch để các chương sau có thể điều kiện hóa. Khi các predictor dạng bảng phụ thuộc mạnh, chính joint—chứ không phải một đống tóm tắt một chiều—là đối tượng mà mô hình Bayes sau này phải tôn trọng. Grinsztajn, Oyallon và Varoquaux (2022) nhắc rằng trên nhiều bài toán bảng thông thường, ensemble cây vẫn thắng mạng sâu, một phần vì cấu trúc đồng thời rời rạc, dị thể, và không được một mật độ liên tục chung phục vụ tốt.

### 4. Mô phỏng như phép kiểm tra trực giác

Chương 0 dùng mô phỏng để nhìn thấy biến thiên lấy mẫu. Cùng thói quen ấy nay xuất hiện dưới dạng kiểm tra dự báo hậu nghiệm và simulation-based calibration: lấy tham số từ prior, sinh dữ liệu, khớp lại, rồi hỏi xem bất định thu được có trung thực không (Modrák et al., 2025). Trước khi gặp Markov chain Monte Carlo, bạn đã có câu hỏi đúng. Câu chuyện tính toán có tái tạo được câu chuyện xác suất hay không?

## Diễn giải và nhận định

Trong mỗi ứng dụng, posterior hay điểm số đều dễ bị đọc quá. Một $$P(\text{True})$$ đã hiệu chỉnh vẫn chưa chứng minh mô hình “biết”. Một log-likelihood ổn định vẫn chưa phải là likelihood đúng. Một chương trình đồng thời chỉ trung thực bằng các giả định độc lập có điều kiện mà nó viết ra. Thói quen hữu ích là hỏi tần suất nào, phụ thuộc nào, và mô phỏng nào sẽ làm bẽ mặt tuyên bố ấy.

## Ứng dụng

Bốn bối cảnh trên đã phủ xếp hạng, ngôn ngữ, mô hình bảng, và phần mềm tính Bayes. Chúng không phải chủ đề phụ. Chúng là Chương 0 được nói bằng phương ngữ thực hành CS/DS hiện nay.

## Giới hạn và hướng mở rộng

Bài này không thay một học phần deep learning hay probabilistic programming. Hiệu chỉnh có thể hỏng khi phân phối chuyển dịch; số học log không sửa một likelihood sai đặc tả; và kiểm tra bằng mô phỏng chỉ kiểm tra đúng phép tính bạn đã chạy. Các chương tiếp theo bắt đầu cập nhật Bayes.

## Bài tập

1. Một mô hình gian lận xuất $$0.99$$ trên mười giao dịch, trong đó ba giao dịch sau đó được xác nhận là gian lận. Trong một đoạn, hãy nói “sai hiệu chỉnh” nghĩa là gì ở đây và bạn sẽ vẽ đối tượng nào của Chương 0.
2. Giải thích vì sao xác suất token kế tiếp của một mô hình ngôn ngữ có thể trông rất tự tin trên không gian token nhưng vẫn bất định trên không gian nghĩa. Bạn cần thêm tính bất biến nào?
3. Viết một câu chuyện sinh dữ liệu bốn dòng (bằng lời, không cần mã) cho tỷ lệ chuyển đổi Beta–Binomial. Chỉ ra joint, phần quan sát được, và phần chưa quan sát.
4. Một đồng nghiệp nói mô phỏng chỉ để dạy học. Dựa trên ý tưởng simulation-based calibration, hãy biện luận một cách dùng trong công nghiệp.

## Tài liệu tham khảo

- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. *Bayesian Data Analysis* (3rd ed.), Ch. 1.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 4–5.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. [arXiv:2207.05221](https://arxiv.org/abs/2207.05221).
- Tian, K., et al. (2023). Just ask for calibration. [arXiv:2305.14975](https://arxiv.org/abs/2305.14975).
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on typical tabular data? *NeurIPS*.
- Modrák, M., et al. (2025). Simulation-based calibration checking for Bayesian computation. *Bayesian Analysis*, 20(2), 461–488. [arXiv:2211.02383](https://arxiv.org/abs/2211.02383).
- [PyMC conceptual overview](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
