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

Từ những bài toán tung đồng xu cổ điển ở đầu Chương 0, toàn bộ hệ sinh thái khoa học dữ liệu hiện đại — từ thử nghiệm A/B trực tuyến, dự báo nhu cầu chuỗi cung ứng, đến đánh giá độ tin cậy của mô hình AI — đều đang vận hành trên đúng cùng một khung xác suất nền tảng. Điểm khác biệt duy nhất là quy mô dữ liệu lớn hơn, độ trễ quyết định ngắn hơn và hậu quả của việc hiểu sai xác suất cũng đắt giá hơn.

Bài tổng kết Chương 0 này nối các khái niệm tưởng chừng rời rạc (phân phối, log-probability, luật số lớn, mô phỏng) thành một bức tranh ứng dụng thực chiến, sẵn sàng đưa bạn bước vào thế giới suy diễn Bayes ở Chương 1.

---

## Mục tiêu học tập

Sau bài đọc mở rộng này, bạn sẽ không còn xem xác suất, phân phối đồng thời (joint distribution), kỳ vọng, log-probability và mô phỏng chỉ là phần "ôn tập trước khi học Bayes", mà nhận ra chúng chính là ngôn ngữ cốt lõi mà khoa học máy tính và khoa học dữ liệu hiện đại sử dụng khi đánh giá một mô hình có được hiệu chỉnh (calibration) hay không, có ổn định số học hay không, và có phản ánh đúng cơ chế sinh dữ liệu hay không. Mục tiêu là thay đổi góc nhìn: đưa các khái niệm nền tảng trở thành câu hỏi thiết kế trực tiếp cho hệ thống thực tế.


## Kiến thức cần nhớ: Xác suất nền tảng trong hệ thống dữ liệu và AI hiện đại

Bốn trụ cột dưới đây cho thấy kiến thức Chương 0 được "cài đặt" trực tiếp vào các hệ thống sản phẩm như thế nào:

- **Mô hình sinh dữ liệu trong kỹ thuật phần mềm & ML:** Các họ phân phối rời rạc/liên tục (Bernoulli, Poisson, Normal, Beta) là viên gạch cơ bản của hàm mất mát: tối thiểu hóa cross-entropy hay MSE thực chất là tối đa hóa log-likelihood của các phân phối này.
- **Tính toán số quy mô lớn (Log-space & Vectorization):** Mọi thư viện hiện đại (PyTorch, JAX, PyMC) đều dùng `log_softmax`, `logsumexp` và tính toán song song trên GPU/CPU để tránh tràn số khi xử lý hàng triệu điểm dữ liệu.
- **Định lượng bất định và ra quyết định (Uncertainty Quantification):** Thay vì chỉ xuất ra một điểm dự báo, các hệ thống hiện đại cần phân phối dự báo đầy đủ để đo rủi ro đuôi, phát hiện lệch phân phối (*distribution shift*) và tối ưu hóa quyết định kinh doanh.

---

## Kiến thức cần có

Bài viết giả định bạn đã hoàn thành các bài bắt buộc trong Chương 0. Nội dung không bổ sung lý thuyết xác suất mới, mà đặt câu hỏi điều gì xảy ra khi các khái niệm này bước ra khỏi lớp học để đi vào bộ phân loại, mô hình ngôn ngữ và lập trình xác suất.

## Mở đầu

Sau khi học xong Chương 0, bạn đã có thể tính kỳ vọng, viết hàm mật độ và mô phỏng phân phối lấy mẫu. Các hệ thống trong công nghiệp có quy mô lớn hơn nhiều, nhưng thường gặp sự cố từ chính những lỗi nền tảng quen thuộc: con số được báo cáo như xác suất nhưng không khớp tần suất dài hạn, tích các giá trị hợp lý bị underflow về 0, hoặc mô hình đồng thời giả định các biến độc lập trái với thực tế. Câu hỏi trung tâm của bài vì thế giản dị nhưng thiết thực: vì sao nhiều hệ thống hiện đại vẫn ước lượng sai độ bất định dù đã có sẵn lý thuyết nền? Lý do là quy mô dữ liệu hay mô hình không thể thay thế ý nghĩa chặt chẽ của một phát biểu xác suất.

## Phát triển khái niệm

Một con số $$p$$ gắn kèm dự báo là một phát biểu về quá trình sinh dữ liệu. Nếu mô hình đưa ra $$p=0.9$$ cho một trăm trường hợp, thì khoảng chín mươi trường hợp trong số đó cần thực sự xảy ra nếu xác suất đó được hiệu chỉnh tốt — đây chính là tinh thần của phân phối lấy mẫu áp dụng cho điểm số học máy thay vì chỉ cho trung bình mẫu. Cấu trúc phân phối đồng thời cũng quan trọng không kém: khi các biến phụ thuộc nhau, tích của các phân phối biên không còn mô tả đúng thực tế. Và mô phỏng vẫn là cách ít tốn kém nhất để kiểm tra xem giả định mô hình có hợp lý hay không.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Hiệu chỉnh xác suất của bộ phân loại và mô hình ngôn ngữ

Bộ lọc thư rác, mô hình phát hiện gian lận và hệ thống cảnh báo y tế đều xuất ra các con số nằm trong đoạn $$[0,1]$$. Câu hỏi đúng theo góc nhìn sinh dữ liệu không chỉ là "mô hình xếp hạng có tốt không?", mà là "khi mô hình dự báo $$P(\text{dương}\mid x)=0.8$$, liệu có đúng khoảng tám trên mười trường hợp như vậy xảy ra không?" Kadavath et al. (2022) cho thấy các mô hình ngôn ngữ lớn có thể đạt mức hiệu chỉnh khá tốt trên các câu hỏi đúng/sai hoặc trắc nghiệm có định dạng rõ ràng khi được hỏi $$P(\text{True})$$ cho câu trả lời vừa sinh. Tian et al. (2023) tiếp tục chỉ ra rằng các mô hình tinh chỉnh theo phản hồi của con người thường cho mức độ tự tin diễn đạt bằng lời (verbalized confidence) được hiệu chỉnh tốt hơn so với xác suất token thô. Bài học từ Chương 0 vẫn giữ nguyên giá trị: một con số nằm trong $$[0,1]$$ chưa tự động là xác suất cho đến khi nó vượt qua phép kiểm tra hiệu chỉnh theo tần suất.

### 2. Log-probability và ổn định số học trong mô hình lớn

Quá trình huấn luyện và suy luận trên các mạng nơ-ron hiện đại liên tục phải tính tích của rất nhiều xác suất. Chuyển sang thang log giúp biến tích thành tổng:

$$
\log p(x_{1:n})=\sum_{i=1}^{n}\log p(x_i\mid x_{<i}),
$$

đây chính là lý do Chương 0 nhấn mạnh log-probability. Đẳng thức này ngăn hàm hợp lý của mô hình ngôn ngữ bị underflow và biến kỹ thuật log-sum-exp thành một phép toán cơ sở tiêu chuẩn. Về mặt lý thuyết, mô hình giả định các token được sinh tuần tự; về mặt thực thi, máy tính chỉ duy trì được tính đúng đắn đó nếu phép tính không sụp về 0.

### 3. Phân phối đồng thời trong lập trình xác suất

Một chương trình viết bằng PyMC hoặc NumPyro thực chất định nghĩa một phân phối đồng thời dưới dạng quy trình sinh dữ liệu: trước hết lấy mẫu tham số, sau đó sinh dữ liệu có điều kiện theo tham số đó. Đây chính là định nghĩa mô hình thống kê của Chương 0 được biểu diễn thành mã để thực hiện suy diễn ở các chương sau. Khi các biến giải thích dạng bảng có phụ thuộc phức tạp, chính phân phối đồng thời — chứ không phải tập hợp các thống kê tóm tắt một chiều rời rạc — mới là đối tượng mà mô hình Bayesian cần mô tả. Grinsztajn, Oyallon và Varoquaux (2022) cũng chỉ ra rằng trên nhiều bài toán dữ liệu bảng thông thường, các mô hình tổ hợp cây vẫn vượt trội mạng học sâu, một phần vì cấu trúc đồng thời của dữ liệu bảng thường rời rạc, không đồng nhất và khó được biểu diễn tốt bởi một hàm mật độ liên tục trơn.

### 4. Mô phỏng như phép kiểm tra trực giác

Chương 0 dùng mô phỏng để quan sát biến thiên lấy mẫu. Cùng nguyên lý đó được mở rộng trong thực hành Bayesian thành kiểm tra dự báo hậu nghiệm (posterior predictive check) và hiệu chỉnh dựa trên mô phỏng (simulation-based calibration): rút tham số từ phân phối tiên nghiệm, sinh dữ liệu giả, khớp lại mô hình rồi kiểm tra xem độ bất định thu được có khớp với quy trình sinh hay không (Modrák et al., 2025). Ngay trước khi bước vào Markov chain Monte Carlo, bạn đã nắm được câu hỏi cốt lõi: thuật toán tính toán có tái tạo chính xác mô hình xác suất ban đầu hay không?

## Diễn giải và nhận định

Trong cả bốn ứng dụng trên, phân phối hậu nghiệm hay điểm xác suất đều dễ bị suy diễn quá mức. Một giá trị $$P(\text{True})$$ được hiệu chỉnh tốt chưa đồng nghĩa với việc mô hình thực sự "hiểu" bài toán; một hàm log-likelihood ổn định về mặt số học không biến một hàm hợp lý sai đặc tả thành đúng; và một chương trình xác suất chỉ đáng tin ngang với các giả định độc lập có điều kiện mà nó đặt ra. Thói quen cần duy trì là luôn hỏi: tần suất kiểm chứng là gì, giả định phụ thuộc nào đang được dùng, và phép mô phỏng nào có thể kiểm chứng hoặc bác bỏ tuyên bố đó?

## Ứng dụng

Bốn tình huống trên bao phủ các bài toán xếp hạng, mô hình ngôn ngữ, dữ liệu bảng và phần mềm suy diễn Bayesian. Chúng không phải các chủ đề tách rời, mà là chính kiến thức Chương 0 được thể hiện trong ngôn ngữ thực hành hiện đại của khoa học máy tính và khoa học dữ liệu.

## Giới hạn và hướng mở rộng

Bài viết này không thay thế một học phần về học sâu hay lập trình xác suất. Độ hiệu chỉnh có thể suy giảm khi phân phối dữ liệu dịch chuyển; tính toán trên thang log không khắc phục được mô hình sai đặc tả; và kiểm tra bằng mô phỏng chỉ xác nhận được phần tính toán nằm trong kịch bản bạn đã chạy. Các chương tiếp theo sẽ đi trực tiếp vào quy trình cập nhật Bayesian.


## Giải thích: Từ một bài toán sản phẩm thực tế về đúng mô hình xác suất

Khi đối diện một bài toán khoa học dữ liệu mới, hãy đi chậm qua bốn bước ánh xạ sau:

1. **Xác định bản chất biến đầu ra:** Nhị phân (Bernoulli/Binomial), số đếm (Poisson/Negative Binomial), hay liên tục (Normal/Log-normal/Student-$$t$$)?
2. **Kiểm tra hàm mất mát tương đương:** Chọn hàm mất mát chính là ngầm chọn một giả định likelihood (ví dụ MSE ứng với sai số Gaussian đồng phương sai).
3. **Đo bất định ở hai cấp độ:** Tách biệt bất định ngẫu nhiên tự nhiên (*aleatoric* — không giảm khi thêm dữ liệu) và bất định tri thức (*epistemic* — giảm theo $$1/\sqrt{n}$$ khi thêm dữ liệu).
4. **Kiểm chứng bằng mô phỏng trước khi triển khai:** Sinh dữ liệu giả lập để đo hiệu quả quyết định trước khi chạy trên người dùng thật.

### Ví dụ tính toán làm từng bước: So sánh hàm mất mát Log-Loss trên mô hình dự báo xác suất

Giả sử một mô hình phân loại rủi ro gian lận dự đoán xác suất cho 3 giao dịch có nhãn thật lần lượt là $$y = (1, 0, 1)$$. So sánh Mô hình A (hiệu chỉnh tốt) và Mô hình B (quá tự tin và đoán sai giao dịch thứ 3):

| Giao dịch | Nhãn thật $$y_i$$ | Dự báo $$p_i$$ (Mô hình A) | $$-\ln p_i(y_i)$$ (A) | Dự báo $$p_i$$ (Mô hình B) | $$-\ln p_i(y_i)$$ (B) |
| --- | --- | --- | --- | --- | --- |
| 1 | $$1$$ | $$0.80$$ | $$-\ln(0.80) \approx 0.223$$ | $$0.99$$ | $$-\ln(0.99) \approx 0.010$$ |
| 2 | $$0$$ | $$0.20$$ | $$-\ln(0.80) \approx 0.223$$ | $$0.01$$ | $$-\ln(0.99) \approx 0.010$$ |
| 3 | $$1$$ | $$0.40$$ | $$-\ln(0.40) \approx 0.916$$ | $$0.01$$ | $$-\ln(0.01) \approx 4.605$$ |
| **Log-loss trung bình** | — | — | **$$0.454$$** | — | **$$1.542$$** |

Dù cả hai mô hình đều đoán đúng 2/3 giao dịch (cùng độ chính xác 66.7%), Mô hình B bị phạt nặng gấp hơn **3 lần** trên thang log-loss ($$1.542$$ so với $$0.454$$) vì quá tự tin khi sai. Đây chính là lý do các hệ thống AI hiện đại ưu tiên điểm chấm xác suất nghiêm ngặt (*proper scoring rules*) như log-loss thay vì chỉ nhìn accuracy.

**Hiểu lầm cần tránh:** Chỉ tối ưu hóa độ chính xác phân loại (accuracy) mà bỏ qua hiệu chỉnh xác suất (*calibration*) và log-loss — khiến mô hình đưa ra các quyết định rủi ro cực đoan khi gặp trường hợp biên.

**Kiểm tra nhanh:** Nếu Mô hình B đoán xác suất $$0.001$$ cho một ca dương tính thật, riêng một lỗi đó đã đóng góp $$-\ln(0.001) \approx 6.908$$ vào tổng mất mát — lớn hơn tổng sai số của 30 dự đoán có xác suất $$0.80$$ cộng lại.

---

## Video tham khảo

- [Naive Bayes, Clearly Explained!!!](https://www.youtube.com/watch?v=O2L2Uv9pdDA) — StatQuest with Josh Starmer, English. **Xem trước.** Minh họa Naive Bayes như một bộ phân loại xây dựng trực tiếp từ xác suất có điều kiện.
- [Why Log Probabilities Are Everywhere in AI - Underflow Error in HMMs and Viterbi Algorithm](https://www.youtube.com/watch?v=HghZrdnrNQY) — Algorithms and AI, English. Giải thích vì sao các mô hình chuỗi và mô hình ngôn ngữ bắt buộc làm việc trên thang log-probability.
- [MIT 6.S191: Uncertainty in Deep Learning](https://www.youtube.com/watch?v=veYq6EWZyVc) — Alexander Amini, English. Giới thiệu bài toán định lượng độ bất định trong học sâu, cho thấy kỳ vọng và phân phối xác suất được dùng ra sao trong các mô hình hiện đại.

## Bài tập

1. Một mô hình phát hiện gian lận xuất xác suất $$0.99$$ trên mười giao dịch, nhưng thực tế chỉ có ba giao dịch được xác nhận là gian lận. Viết một đoạn ngắn giải thích "sai hiệu chỉnh" ở đây nghĩa là gì và bạn sẽ dùng khái niệm nào của Chương 0 để trực quan hóa vấn đề này.
2. Giải thích vì sao xác suất token tiếp theo của một mô hình ngôn ngữ có thể rất tự tin trên không gian token nhưng vẫn còn nhiều bất định trên không gian ngữ nghĩa. Để đánh giá đúng độ bất định ngữ nghĩa, cần thêm khái niệm tương đương hay tính bất biến nào?
3. Viết một câu chuyện sinh dữ liệu gồm bốn dòng (bằng lời, không cần mã nguồn) cho mô hình tỷ lệ chuyển đổi Beta–Binomial, chỉ rõ phân phối đồng thời, phần quan sát được và phần chưa quan sát được.
4. Giả sử một đồng nghiệp cho rằng mô phỏng chỉ dùng để giảng dạy. Dựa trên ý tưởng simulation-based calibration, hãy lập luận về một ứng dụng thực tiễn của mô phỏng trong công nghiệp.

## Tài liệu tham khảo

- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. *Bayesian Data Analysis* (3rd ed.), Ch. 1.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 4–5.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. [arXiv:2207.05221](https://arxiv.org/abs/2207.05221).
- Tian, K., et al. (2023). Just ask for calibration. [arXiv:2305.14975](https://arxiv.org/abs/2305.14975).
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on typical tabular data? *NeurIPS*.
- Modrák, M., et al. (2025). Simulation-based calibration checking for Bayesian computation. *Bayesian Analysis*, 20(2), 461–488. [arXiv:2211.02383](https://arxiv.org/abs/2211.02383).
- [PyMC conceptual overview](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
