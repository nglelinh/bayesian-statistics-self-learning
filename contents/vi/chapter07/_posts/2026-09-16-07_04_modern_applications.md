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

Sau bài học tùy chọn này, bạn sẽ nhìn nhận weight decay, horseshoe, xấp xỉ Laplace và deep ensemble như những cách khác nhau để đặt phân phối tiên nghiệm lên các mô hình quá linh hoạt. Mục tiêu không phải là ghi nhớ tên thuật toán, mà là thấy rằng vấn đề quá khớp ở Chương 7 chính là động lực dẫn đến học sâu Bayes (Bayesian deep learning): khi mạng nơ-ron có quá nhiều tham số, ta cần một phân phối trên tập các hàm thay vì chỉ một nghiệm tối ưu điểm duy nhất.

## Kiến thức cần có

Các bài 7.1–7.3 đã kết nối phân phối tiên nghiệm với điều chuẩn, đánh đổi độ lệch – phương sai và chọn biến. Bài học này không nhắc lại lý thuyết co rút hệ số, mà cho thấy cùng tư duy đó đang được vận dụng trong mạng nơ-ron và các mô hình dữ liệu bảng nhiều chiều giai đoạn 2021–2024.

## Mở đầu

Chương 7 bắt đầu bằng một sự đánh đổi quen thuộc: mô hình quá linh hoạt sẽ khớp cả nhiễu, còn quá cứng nhắc sẽ bỏ sót tín hiệu. Trong học sâu, sự đánh đổi này bị khuếch đại lên rất nhiều. Hàng triệu trọng số có thể khớp hoàn toàn tập huấn luyện mà vẫn khái quát hóa tốt, nhưng mức độ tự tin mà mạng gắn cho dự báo thường không phản ánh đúng xác suất thực tế. Vì thế, câu hỏi trung tâm không còn là "có nên thêm biến hay không?", mà chuyển thành "liệu ta có thể duy trì một phân phối hậu nghiệm — dù chỉ trên lớp cuối — đủ trung thực để nhận biết khi nào mô hình không chắc chắn?".

## Phát triển khái niệm

Một tiên nghiệm chuẩn trên hệ số:

$$
\beta_j\sim\mathcal N(0,\tau^2),
$$

tương đương với weight decay: ước lượng MAP chính là nghiệm tối ưu có phạt $$L_2$$. Các tiên nghiệm horseshoe và spike-and-slab đi xa hơn khi cho phép phần lớn hệ số tiến gần về 0 nhưng vẫn giữ lại một ít hệ số lớn, biến việc chọn biến thành một phần của suy luận hậu nghiệm thay vì một bước lọc tách rời. Khi $$\beta$$ trở thành hàng triệu trọng số của mạng nơ-ron, ta không thể chạy MCMC đầy đủ. Các phương pháp xấp xỉ giai đoạn 2021–2024 — như xấp xỉ Laplace, suy luận Bayes ở lớp cuối (last-layer Bayes) và ensemble — là những cách khác nhau để giữ lại một phần thông tin của phân phối hậu nghiệm $$p(\theta\mid y)$$.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Điều chuẩn dưới dạng tiên nghiệm trong GLM và mô hình nông

Câu chuyện sinh dữ liệu vẫn giữ nguyên: dữ liệu xuất phát từ một hàm tương đối đơn giản cộng thêm nhiễu. Một tiên nghiệm hẹp thể hiện niềm tin rằng hàm mục tiêu không biến thiên quá gấp khúc. Trong bài toán chấm điểm tín dụng hoặc xếp hạng trên dữ liệu bảng, đây thường vẫn là lựa chọn phù hợp, đặc biệt khi Grinsztajn et al. (2022) chỉ ra rằng các mô hình cây và mô hình tuyến tính có điều chuẩn vẫn cạnh tranh tốt với mạng học sâu. Do đó, kiến thức Chương 7 không hề lỗi thời trong kỷ nguyên học sâu; ngược lại, học sâu khiến vai trò của tiên nghiệm càng trở nên *thiết yếu hơn*.

### 2. Xấp xỉ Laplace và lớp cuối: Hậu nghiệm cục bộ với chi phí thấp

Daxberger et al. (2021) xây dựng khung Laplace Redux: bắt đầu từ nghiệm MAP, xấp xỉ phân phối hậu nghiệm bằng phân phối chuẩn dựa trên ma trận Hessian (hoặc các xấp xỉ của nó), qua đó chuyển một mạng đã huấn luyện thành mô hình Bayes với rất ít thay đổi về mã nguồn. Harrison, Willes và Snoek (2024) phát triển lớp cuối Bayes biến phân (Variational Bayesian Last Layers — VBLL) dưới dạng một hàm mất mát xác định, không cần lấy mẫu, với chi phí tính toán chỉ tăng theo bình phương số chiều của lớp cuối. Trong cách tiếp cận này, câu chuyện sinh dữ liệu được thu gọn có chủ đích: bộ biểu diễn đặc trưng được coi là đã học cố định, còn độ bất định tập trung ở lớp đầu ra. Điều chuẩn ở đây thể hiện dưới dạng một phân phối trên siêu phẳng quyết định.

### 3. Mạng nơ-ron Bayes có cần ngẫu nhiên hóa toàn bộ trọng số?

Sharma, Farquhar, Nalisnick và Rainforth (2023) đặt ra một câu hỏi gắn trực tiếp với tinh thần của Chương 7: liệu ngẫu nhiên hóa toàn bộ trọng số (full stochasticity) có phải cách duy nhất để tránh quá khớp và thu được phân phối dự báo giàu thông tin hay không? Nhóm tác giả chứng minh rằng các mạng chỉ ngẫu nhiên hóa một phần vẫn là bộ xấp xỉ phổ quát cho phân phối điều kiện, và thực nghiệm không cho thấy lợi ích rõ rệt của việc đặt biến ngẫu nhiên lên mọi trọng số. Sự đánh đổi ở đây mở rộng sang chi phí bộ nhớ và tính trung thực của suy luận, chứ không chỉ là sai số dự báo. Bài toán chọn biến của bài 7.3 lúc này xuất hiện trở lại dưới dạng lựa chọn *tầng nào* của mạng cần đặt phân phối tiên nghiệm.

### 4. Deep ensemble như một xấp xỉ Bayes thực dụng

Deep ensemble — huấn luyện nhiều mạng độc lập từ các điểm khởi tạo khác nhau — vẫn là chuẩn đối chiếu mạnh về ước lượng bất định trong công nghiệp. Wilson và Izmailov lập luận rằng phương pháp này có thể được hiểu như xấp xỉ một phân phối hỗn hợp quanh nhiều đỉnh (mode) của hậu nghiệm. Dù không thay thế được MCMC chuẩn như trong khảo sát của Izmailov et al. (2021), deep ensemble là cách thực dụng để nắm bắt sự đa dạng của hậu nghiệm khi HMC không khả thi về mặt tính toán. Nhìn nhận ensemble như nhiều nghiệm MAP dưới một tiên nghiệm ẩn rồi lấy trung bình dự báo vẫn giữ trọn tinh thần Chương 7: giảm phương sai bằng cách không đặt toàn bộ niềm tin vào một ước lượng điểm duy nhất.

## Diễn giải và nhận định

Một xấp xỉ Laplace hẹp quanh nghiệm MAP có thể bỏ sót các mode khác của hậu nghiệm. Một mô hình Bayes lớp cuối vẫn có thể tự tin sai lầm nếu không gian đặc trưng phía trước bị suy biến (feature collapse). Ngay cả khi các mô hình trong một ensemble đồng thuận với nhau, điều đó không chứng minh giả thuyết là đúng vì chúng có thể cùng chia sẻ một sai số hệ thống. Phân phối tiên nghiệm chỉ phát huy đúng tác dụng khi giúp mô hình *dè dặt hơn* trên những vùng dữ liệu thưa, chứ không phải khi giữ độ tự tin luôn ở mức cao.

## Ứng dụng

Chấm điểm dữ liệu bảng, phát hiện dữ liệu ngoài phân phối (out-of-distribution) và ước lượng độ bất định trong các mạng phân loại là ba lĩnh vực mà điều chuẩn Bayes đã trở thành kỹ thuật triển khai thực tế.

## Giới hạn và hướng mở rộng

Xấp xỉ Laplace chỉ có giá trị cục bộ. VBLL giả định lớp cuối tuyến tính trên bộ đặc trưng cố định. Deep ensemble làm tăng chi phí huấn luyện theo số lượng mô hình thành phần. Không có phương pháp nào thay thế được nhu cầu kiểm chứng mô hình sẽ trình bày ở Chương 8. Bài học này không nhằm mở rộng thành một chương riêng về học sâu, mà chỉ cho thấy cách tư duy về tiên nghiệm từ bài 7.1 đã đi vào các kiến trúc mạng hiện đại theo những hướng tiếp cận thực dụng.

## Video tham khảo

- [The Bayesian interpretation of weight decay 43 Machine Learning](https://www.youtube.com/watch?v=RckG_kNv1Kc) — Professor tutorials, English. **Xem trước**. Giải thích weight decay dưới góc nhìn tiên nghiệm trên trọng số, nối trực tiếp điều chuẩn với mạng nơ-ron.
- [Uncertainty estimation and Bayesian Neural Networks - Marcin Możejko](https://www.youtube.com/watch?v=dj-FKXxy7HQ) — PyData, English. Trình bày ước lượng bất định bằng mạng nơ-ron Bayes, củng cố vai trò của tiên nghiệm đối với các mô hình có độ linh hoạt cao.
- [MIT 6.S191: Uncertainty in Deep Learning](https://www.youtube.com/watch?v=veYq6EWZyVc) — Alexander Amini, English. Giới thiệu các phương pháp lượng hóa bất định trong học sâu, bao gồm họ phương pháp ensemble.

## Bài tập

1. Biểu diễn lại weight decay dưới dạng một phân phối tiên nghiệm. Khi giảm $$\tau$$, bạn đang đặt giả định gì về hàm sinh dữ liệu và chấp nhận loại độ lệch (bias) nào?
2. Một nhóm kỹ sư chỉ áp dụng suy luận Bayes ở lớp cuối để tiết kiệm chi phí tính toán. Dựa trên kết quả của Sharma et al. (2023), hãy lập luận khi nào cách làm này là đủ và khi nào các tầng đặc trưng xác định sẽ che giấu độ bất định.
3. So sánh tiên nghiệm horseshoe trên 20 biến dự báo với dropout trên một mạng nơ-ron: thành phần nào đang được co rút, và thành phần nào đang được che giấu dưới dạng thủ thuật tối ưu?
4. Laplace Redux sử dụng ma trận Hessian tại nghiệm MAP. Hãy mô tả một phân phối hậu nghiệm có hai mode và giải thích xấp xỉ Laplace sẽ bỏ sót điều gì.

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 14–15.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 17–18.
- Daxberger, E., et al. (2021). Laplace Redux — effortless Bayesian deep learning. *NeurIPS*.
- Harrison, J., Willes, J., & Snoek, J. (2024). Variational Bayesian last layers. *ICLR*. [arXiv:2404.11599](https://arxiv.org/abs/2404.11599).
- Sharma, M., Farquhar, S., Nalisnick, E., & Rainforth, T. (2023). Do Bayesian neural networks need to be fully stochastic? *AISTATS*. [arXiv:2211.06291](https://arxiv.org/abs/2211.06291).
- Izmailov, P., Vikram, S., Hoffman, M. D., & Wilson, A. G. (2021). What are Bayesian neural network posteriors really like? *ICML*.
