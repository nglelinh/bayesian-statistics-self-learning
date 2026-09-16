---
layout: post
title: "Bài 5.5: Ứng dụng hiện đại của hồi quy đa biến và tư duy nhân quả"
chapter: '05'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: optional
---

## Mục tiêu học tập

Sau bài tùy chọn này, bạn đọc được một hệ số trong mô hình nhiều predictor như một tuyên bố nhân quả có điều kiện, không như một hệ số “quan trọng hơn” chỉ vì phần mềm in ra sao. Bạn sẽ thấy confounding, đa cộng tuyến và tương tác không phải lỗi hồi quy, mà là hình dạng của dữ liệu sản phẩm: thử nghiệm A/B trên chợ, hệ gợi ý, và hồ sơ y tế theo thời gian.

## Kiến thức cần có

Các bài 5.1–5.4 đã đặt multiple regression, DAG, đa cộng tuyến và tương tác. Bài này không vẽ lại định nghĩa back-door. Nó chỉ đưa cùng những sơ đồ ấy vào các bài báo và hệ thống 2022–2026.

## Mở đầu

Chương 5 bắt đầu từ một thất vọng quen thuộc: thêm biến thì $$R^2$$ tăng, nhưng câu chuyện về “tác động” lại vỡ. Trong khoa học máy tính ứng dụng, thất vọng ấy đắt hơn. Một nền tảng có thể thêm hàng trăm feature vào một mô hình nâng hạng, rồi tuyên bố đã “kiểm soát mọi thứ”. Nếu một trong những feature ấy là biến trung gian hoặc collider, hệ số của xử lý không còn là hiệu ứng ta muốn. Căng thẳng của bài này là: dữ liệu càng nhiều cột, DAG càng cần, không càng thừa.

## Phát triển khái niệm

Một hệ số $$\beta_j$$ trong

$$
y_i=\alpha+\sum_j\beta_j x_{ij}+\varepsilon_i
$$

chỉ mang nghĩa nhân quả sau khi tập điều khiển đã chặn các đường back-door và không mở ra đường mới. Cinelli, Forney và Pearl (2022) gọi đúng vấn đề này là good and bad controls: không phải mọi covariate “liên quan” đều nên vào phương trình. Tương tác nói một chuyện khác, rằng $$\beta_j$$ bản thân nó có thể là hàm của một biến khác. Đa cộng tuyến thì không phải thiên lệch nhân quả; nó là bất định hậu nghiệm phình ra khi các cột kể cùng một câu.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Good and bad controls trong thử nghiệm sản phẩm

Câu chuyện sinh của một A/B trên marketplace thường có sẵn confounding: người dùng chủ động, cung cầu cùng lúc, và một can thiệp trên một phía thay đổi phía kia. Thêm biến “số lần nhấp sau khi thấy biến thể” có thể là bad control nếu nhấp nằm trên đường từ xử lý đến doanh thu. Cinelli et al. (2022) cho một catalog các DAG nhỏ nơi trực giác “càng kiểm soát càng sạch” thất bại. Một nhóm thực nghiệm trung thực vẽ DAG trước khi mở feature store, rồi mới hỏi hồi quy Bayes nên điều kiện hóa trên biến nào.

### 2. Học DAG và giới hạn của tối ưu hóa

Bello, Aragam và Ravikumar (2022) đưa bài toán học DAG về một đặc trưng acyclicity log-det trên M-matrix, rồi tối ưu liên tục (DAGMA). Đây là một phát triển khoa học máy tính rõ ràng: thay vì giả sử đồ thị, ta cố học nó. Nhưng câu chuyện sinh vẫn cần giả định—thường là mô hình phương trình cấu trúc cộng tính, nhiễu độc lập. Một DAG học được từ log nhấp không tự động là DAG nghiệp vụ. Hồi quy đa biến của Chương 5 vẫn cần người phân tích chịu trách nhiệm về các mũi tên không quan sát được.

### 3. Transformer nhân quả cho kết cục theo thời gian

Melnychuk, Frauen và Feuerriegel (2022) xây Causal Transformer để ước lượng kết cục phản thực trên dữ liệu dọc, ví dụ phác đồ điều trị trong MIMIC. Câu chuyện sinh là: đồng biến theo thời gian, điều trị, và kết cục phụ thuộc lẫn nhau trên một chân trời dài; confounding thay đổi theo thời gian. Kiến trúc transformer không xóa confounding. Nó cố học một biểu diễn vừa đoán được kết cục vừa *không* đoán được việc gán điều trị hiện tại, nhờ một loss đối kháng. Đó là phiên bản học sâu của cùng ý tưởng Chương 5: muốn $$\beta$$ của điều trị đọc được, phải chặn đường gây nhiễu, không phải thêm lớp mạng.

### 4. Tương tác và đa cộng tuyến trong cá nhân hóa

Một hệ gợi ý viết “hiệu ứng của giảm giá phụ thuộc vào mức độ mới của người dùng” chính là interaction. Hai embedding gần cộng tuyến sẽ cho posterior rộng trên từng hệ số dù dự báo vẫn tốt—đúng hiện tượng bài 5.3. Trong sản phẩm, điều đó có nghĩa: đừng diễn giải từng tọa độ embedding như một cơ chế; hãy diễn giải các dự báo và các tương tác đã được đặt tên.

## Diễn giải và nhận định

Một khoảng hậu nghiệm hẹp trên $$\beta_{\text{xử lý}}$$ sau khi đã nhồi hai mươi kiểm soát không phải bằng chứng nhân quả. Nó có thể là bad control đã chặn đường hoặc collider đã mở đường. Ngược lại, một khoảng rộng sau khi chỉ điều kiện hóa đúng tập tối thiểu vẫn có thể là ước lượng trung thực. Chương 5 dạy đúng thứ tự: DAG trước, độ hẹp sau.

## Ứng dụng

Thử nghiệm marketplace, nâng hạng có kiểm soát, điều trị cá nhân hóa, và diễn giải embedding đều là multiple regression cộng với một câu hỏi nhân quả. Bayes thêm một thứ mà OLS thường giấu: bất định còn lại sau khi cấu trúc đã được khai báo.

## Giới hạn và hướng mở rộng

Học DAG từ quan sát không giải được tính không nhận diện khi thiếu giả định. Causal Transformer cần giả định về tuần tự thời gian và về khả năng cân bằng biểu diễn. Bài này không thay thế một học phần suy luận nhân quả. Chương 6 sẽ đổi họ likelihood khi $$y$$ không còn Gaussian, nhưng bài toán confounding vẫn đi theo.

## Bài tập

1. Vẽ một DAG ba nút cho “hiển thị quảng cáo → nhấp → mua”. Nếu mục tiêu là hiệu ứng của hiển thị lên mua, việc hồi quy có điều kiện trên nhấp là good hay bad control, và vì sao?
2. Một mô hình cá nhân hóa có hai feature tương quan 0.97. Dự báo hold-out tốt nhưng hai hệ số đổi dấu khi bạn bỏ một phần trăm dữ liệu. Bạn sẽ diễn giải hệ số nào, nếu có?
3. Causal Transformer tối thiểu hóa khả năng đoán điều trị từ biểu diễn. Câu ấy đang nhắm tới confounding nào của bài 5.2?
4. DAGMA trả về một đồ thị từ log sản phẩm. Liệt kê hai mũi tên bạn *không* cho phép mô hình tự vẽ trừ khi có kiến thức nghiệp vụ.

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 5, 14.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 18.
- Cinelli, C., Forney, A., & Pearl, J. (2022). A crash course in good and bad controls. *Sociological Methods & Research*. [doi:10.1177/00491241221099552](https://doi.org/10.1177/00491241221099552).
- Bello, K., Aragam, B., & Ravikumar, P. (2022). DAGMA: Learning DAGs via M-matrices and a log-determinant acyclicity characterization. *NeurIPS*. [arXiv:2209.08011](https://arxiv.org/abs/2209.08011).
- Melnychuk, V., Frauen, D., & Feuerriegel, S. (2022). Causal Transformer for estimating counterfactual outcomes. *ICML*. [arXiv:2204.07258](https://arxiv.org/abs/2204.07258).
