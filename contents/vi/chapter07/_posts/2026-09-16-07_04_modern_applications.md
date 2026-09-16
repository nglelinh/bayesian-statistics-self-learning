---
layout: post
title: "Bài 7.4: Ứng dụng hiện đại của prior, regularization và học sâu Bayes"
chapter: '07'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter07
lesson_type: optional
---

## Mục tiêu học tập

Sau bài tùy chọn này, bạn đọc weight decay, horseshoe, Laplace approximation và deep ensemble như những cách khác nhau để đặt prior lên một mô hình quá linh hoạt. Mục tiêu không phải thuộc tên thuật toán, mà là thấy overfitting của Chương 7 chính là lý do Bayesian deep learning phải được phát minh: mạng quá giàu tham số nên ta cần một phân phối trên hàm, không một điểm tối ưu.

## Kiến thức cần có

Các bài 7.1–7.3 đã nối prior với regularization, bias–variance, và lựa chọn biến. Bài này không viết lại lý thuyết co hệ số. Nó chỉ cho thấy cùng logic ấy đang được dùng trên mạng nơ-ron và các mô hình bảng cao chiều giai đoạn 2021–2024.

## Mở đầu

Chương 7 mở bằng một đánh đổi: mô hình đủ mềm thì khớp nhiễu, đủ cứng thì bỏ tín hiệu. Trong học sâu, đánh đổi ấy bị phóng đại. Hàng triệu trọng số có thể nội suy tập huấn và vẫn tổng quát hóa, nhưng độ tin mà mạng gắn cho dự báo thường không phải xác suất. Căng thẳng trí tuệ vì thế đổi hình. Không còn là “có nên thêm biến?”, mà là “ta có thể giữ một posterior, dù chỉ trên lớp cuối, đủ trung thực để biết khi nào mô hình không biết?”.

## Phát triển khái niệm

Một prior Gauss trên hệ số,

$$
\beta_j\sim\mathcal N(0,\tau^2),
$$

tương đương weight decay: MAP là tối ưu có phạt $$L_2$$. Horseshoe và spike-and-slab đi xa hơn: chúng cho phép nhiều hệ số gần không và một ít hệ số lớn, tức là feature selection như một posterior, không như một bước lọc trước. Khi $$\beta$$ trở thành hàng triệu trọng số, ta không lấy được MCMC đầy đủ. Các xấp xỉ 2021–2024—Laplace, last-layer Bayes, ensemble—là những cách khác nhau để giữ một phần của $$p(\theta\mid y)$$.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Regularization như prior trong GLM và mạng nông

Câu chuyện sinh không đổi: dữ liệu đến từ một hàm đơn giản cộng nhiễu. Prior hẹp nói “tôi không tin hàm quá gập”. Trong tín dụng hoặc xếp hạng bảng, đó thường vẫn là lựa chọn đúng, đặc biệt khi Grinsztajn et al. (2022) cho thấy mô hình cây và mô hình tuyến tính được regularize còn cạnh tranh với mạng sâu. Chương 7 vì thế không bị học sâu làm cho lỗi thời; học sâu chỉ làm prior trở nên *bắt buộc hơn*.

### 2. Laplace và lớp cuối: posterior cục bộ với giá rẻ

Daxberger et al. (2021) xây Laplace Redux: lấy một MAP, xấp xỉ posterior bằng Gauss từ Hessian (hoặc các proxy), và biến một mạng đã huấn luyện thành một mô hình Bayes với ít thay đổi mã. Harrison, Willes và Snoek (2024) đưa Bayesian last layer thành một loss variational xác định, không cần lấy mẫu, với chi phí chỉ tăng theo bình phương chiều lớp cuối. Câu chuyện sinh được thu nhỏ có chủ ý: đặc trưng được xem như đã học, bất định còn lại sống ở lớp đọc ra. Đó là regularization dưới dạng một phân phối trên siêu phẳng quyết định.

### 3. Có cần mạng Bayes hoàn toàn ngẫu nhiên?

Sharma, Farquhar, Nalisnick và Rainforth (2023) hỏi một câu rất Chương 7: full stochasticity có phải cách duy nhất để không quá khớp và để có predictive distribution giàu? Họ chứng minh những mạng chỉ ngẫu nhiên một phần vẫn là bộ xấp xỉ phổ quát cho phân phối điều kiện, và thực nghiệm không thấy lợi ích hệ thống của việc làm ngẫu nhiên mọi trọng số. Bias–variance ở đây là chi phí bộ nhớ và trung thực suy luận, không chỉ là lỗi dự báo. Feature selection của bài 7.3 xuất hiện lại dưới dạng lựa chọn *tầng nào* được đặt prior.

### 4. Ensemble sâu như xấp xỉ Bayes thực dụng

Deep ensemble—huấn luyện vài mạng từ khởi tạo khác nhau—vẫn là baseline bất định mạnh trong công nghiệp. Wilson và Izmailov đã lập luận rằng chúng xấp xỉ một hỗn hợp trên các mode của posterior. Chúng không thay MCMC của Izmailov et al. (2021), nhưng chúng là cách sản phẩm “mua” đa dạng posterior khi HMC không chạy nổi. Đọc ensemble như nhiều MAP dưới prior ẩn, rồi trung bình dự báo, giữ đúng tinh thần Chương 7: giảm variance bằng cách không tin một điểm.

## Diễn giải và nhận định

Một khoảng Laplace hẹp quanh MAP có thể bỏ mode khác. Một last-layer Bayes tự tin vẫn mù nếu đặc trưng đã collapse. Một ensemble đồng thuận không có nghĩa dữ liệu đã chứng minh giả thuyết; chúng có thể chia sẻ cùng một sai số hệ thống. Prior đã làm việc khi mô hình *từ chối* đi quá xa trên vùng thưa, không khi độ tin luôn cao.

## Ứng dụng

Chấm điểm bảng, phát hiện out-of-distribution, và bất định của mạng phân loại là ba nơi regularization Bayes đã thành kỹ thuật triển khai, không còn là ẩn dụ.

## Giới hạn và hướng mở rộng

Laplace là địa phương. VBLL giả định lớp cuối tuyến tính trên đặc trưng cố định. Ensemble cần nhân chi phí huấn luyện. Không phương pháp nào xóa nhu cầu kiểm tra mô hình ở Chương 8. Bài này cố ý không mở một chương học sâu riêng; nó chỉ cho thấy prior của bài 7.1 đã đi vào các mạng hiện đại bằng những cửa hẹp.

## Bài tập

1. Viết lại weight decay như một prior. Nếu bạn giảm $$\tau$$, bạn đang tuyên bố điều gì về hàm sinh dữ liệu, và bạn chấp nhận bias kiểu gì?
2. Một nhóm chỉ đặt Bayes ở lớp cuối vì “rẻ”. Dựa trên Sharma et al. (2023), lập luận khi nào điều đó đủ và khi nào đặc trưng xác định sẽ giấu bất định.
3. So sánh horseshoe trên hai mươi predictor với dropout trên một mạng. Cái gì đang bị co, và cái gì bị giấu thành thủ thuật tối ưu?
4. Laplace Redux dùng Hessian tại MAP. Vẽ bằng lời một posterior hai mode và nói xấp xỉ ấy sẽ bỏ sót điều gì.

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 14–15.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 17–18.
- Daxberger, E., et al. (2021). Laplace Redux — effortless Bayesian deep learning. *NeurIPS*.
- Harrison, J., Willes, J., & Snoek, J. (2024). Variational Bayesian last layers. *ICLR*. [arXiv:2404.11599](https://arxiv.org/abs/2404.11599).
- Sharma, M., Farquhar, S., Nalisnick, E., & Rainforth, T. (2023). Do Bayesian neural networks need to be fully stochastic? *AISTATS*. [arXiv:2211.06291](https://arxiv.org/abs/2211.06291).
- Izmailov, P., Vikram, S., Hoffman, M. D., & Wilson, A. G. (2021). What are Bayesian neural network posteriors really like? *ICML*.
