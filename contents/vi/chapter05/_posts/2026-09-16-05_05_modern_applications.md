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

Sau bài tùy chọn này, bạn sẽ biết cách đọc hệ số trong mô hình nhiều biến dự báo như một phát biểu nhân quả có điều kiện, thay vì đánh giá tầm quan trọng chỉ dựa vào dấu sao ý nghĩa thống kê trên bảng kết quả. Bạn cũng sẽ thấy hiện tượng gây nhiễu (confounding), đa cộng tuyến và hiệu ứng tương tác không phải là "lỗi" của hồi quy, mà là đặc trưng tự nhiên của dữ liệu ứng dụng hiện đại như thử nghiệm A/B trên nền tảng thị trường (marketplace), hệ gợi ý và hồ sơ y tế dọc theo thời gian.

## Kiến thức cần có

Các bài 5.1–5.4 đã trình bày hồi quy đa biến, DAG, đa cộng tuyến và hiệu ứng tương tác. Bài này không nhắc lại định nghĩa đường cửa sau (backdoor), mà đặt chính những khái niệm đó vào các nghiên cứu và hệ thống thực tế giai đoạn 2022–2026.

## Mở đầu

Chương 5 mở ra từ một tình huống quen thuộc: thêm biến mới có thể làm tăng $$R^2$$, nhưng lại làm sai lệch câu chuyện về tác động nhân quả. Trong khoa học máy tính và sản phẩm số, cái giá của sai lầm này còn lớn hơn. Một nền tảng có thể đưa hàng trăm đặc trưng (feature) vào mô hình xếp hạng rồi cho rằng mình đã "kiểm soát mọi thứ". Nếu trong số đó có biến trung gian hoặc collider, hệ số của biến can thiệp sẽ không còn phản ánh đúng hiệu ứng mục tiêu. Thông điệp xuyên suốt bài này là: tập dữ liệu càng nhiều cột thì đồ thị nhân quả DAG càng cần thiết, chứ không hề thừa.

## Phát triển khái niệm

Trong phương trình hồi quy đa biến:

$$
y_i=\alpha+\sum_j\beta_j x_{ij}+\varepsilon_i
$$

hệ số $$\beta_j$$ chỉ mang ý nghĩa nhân quả khi tập biến kiểm soát đã chặn được toàn bộ các đường cửa sau mà không mở ra đường phi nhân quả mới. Cinelli, Forney và Pearl (2022) hệ thống hóa vấn đề này dưới khái niệm *good and bad controls*: không phải mọi hiệp biến có liên quan đều nên đưa vào phương trình. Trong khi đó, hiệu ứng tương tác cho thấy bản thân $$\beta_j$$ có thể là hàm theo một biến khác; còn đa cộng tuyến không gây thiên lệch nhân quả mà làm mở rộng bất định hậu nghiệm khi nhiều cột cùng phản ánh một nguồn thông tin.

## Mô hình trong các hệ thống hiện đại

### 1. Biến kiểm soát đúng và sai (Good and Bad Controls) trong thử nghiệm sản phẩm

Cơ chế sinh dữ liệu của một thử nghiệm A/B trên nền tảng thị trường (marketplace) thường chứa sẵn yếu tố gây nhiễu do hành vi chủ động của người dùng và tương tác cung – cầu hai phía. Đưa biến "số lượt nhấp sau khi thấy biến thể" vào mô hình phân tích doanh thu là một biến kiểm soát sai (bad control) nếu lượt nhấp nằm trên con đường nhân quả từ can thiệp tới doanh thu. Cinelli et al. (2022) cung cấp một hệ thống các DAG mẫu cho thấy trực giác "kiểm soát càng nhiều càng sạch" dễ thất bại ra sao. Thực hành đúng là vẽ DAG trước khi chọn đặc trưng từ kho dữ liệu, rồi mới xác định mô hình hồi quy Bayes cần điều kiện hóa trên tập biến nào.

### 2. Học cấu trúc DAG từ dữ liệu và giới hạn của tối ưu hóa

Bello, Aragam và Ravikumar (2022) chuyển bài toán học DAG thành một bài toán tối ưu liên tục (DAGMA) bằng đặc trưng không chu trình dựa trên log-determinant của ma trận M. Đây là bước tiến đáng chú ý về mặt thuật toán: thay vì chỉ giả định đồ thị, ta tìm cách ước lượng nó từ dữ liệu. Tuy vậy, cách tiếp cận này vẫn phụ thuộc vào các giả định sinh dữ liệu cụ thể — thường là mô hình phương trình cấu trúc cộng tính với nhiễu độc lập. Một DAG học từ nhật ký nhấp chuột không tự động tương đương với cấu trúc nhân quả nghiệp vụ; người phân tích vẫn phải chịu trách nhiệm về các yếu tố gây nhiễu không quan sát được.

### 3. Causal Transformer cho dữ liệu kết cục theo thời gian

Melnychuk, Frauen và Feuerriegel (2022) đề xuất kiến trúc *Causal Transformer* nhằm ước lượng kết cục phản thực trên dữ liệu dọc theo thời gian, chẳng hạn phác đồ điều trị trong cơ sở dữ liệu y tế MIMIC. Trong bối cảnh này, các hiệp biến thay đổi theo thời gian, quyết định điều trị và kết cục tác động qua lại liên tục qua nhiều mốc thời gian, tạo ra hiện tượng gây nhiễu biến thiên theo thời gian. Bản thân kiến trúc transformer không tự xóa bỏ confounding; mô hình phải dùng hàm mất mát đối kháng để học một biểu diễn vừa dự đoán tốt kết cục vừa không dự đoán được việc gán điều trị hiện tại. Đây chính là phiên bản học sâu của nguyên tắc Chương 5: muốn ước lượng đúng tác động điều trị thì phải chặn đường gây nhiễu, chứ không chỉ tăng độ sâu mạng nơ-ron.

### 4. Tương tác và đa cộng tuyến trong hệ thống cá nhân hóa

Trong hệ gợi ý, phát biểu "hiệu quả của mã giảm giá phụ thuộc vào mức độ gắn bó của người dùng" chính là một hiệu ứng tương tác. Trong khi đó, hai vector nhúng (embedding) gần cộng tuyến sẽ tạo ra phân phối hậu nghiệm rất rộng cho từng hệ số riêng lẻ dù dự báo tổng thể vẫn chính xác — đúng như hiện tượng đã phân tích ở Bài 5.3. Về mặt thực hành sản phẩm, không nên cố diễn giải từng tọa độ embedding như một cơ chế độc lập, mà nên tập trung vào chất lượng dự báo và các tương tác giữa những khái niệm có ý nghĩa nghiệp vụ rõ ràng.

## Diễn giải và nhận định

Một khoảng hậu nghiệm hẹp cho $$\beta_{\text{xử lý}}$$ sau khi đưa vào hàng chục biến kiểm soát không phải là bằng chứng nhân quả, vì rất có thể biến trung gian đã chặn mất một phần hiệu ứng hoặc collider đã tạo ra thiên lệch. Ngược lại, một khoảng rộng hơn thu được từ tập điều chỉnh tối thiểu hợp lệ lại có thể là ước lượng trung thực hơn. Trình tự đúng của Chương 5 luôn là: xác định cấu trúc DAG trước, đánh giá độ hẹp của khoảng ước lượng sau.

## Ứng dụng

Thử nghiệm trên nền tảng thị trường, mô hình xếp hạng có kiểm soát, cá nhân hóa điều trị và diễn giải đặc trưng nhúng đều là bài toán hồi quy đa biến kết hợp với câu hỏi nhân quả. Góc nhìn Bayes bổ sung một thông tin mà OLS thường dễ làm mờ đi: mức độ bất định còn lại sau khi đã khai báo rõ cấu trúc mô hình.

## Giới hạn và hướng mở rộng

Học DAG thuần túy từ dữ liệu quan sát không giải quyết được tính không nhận diện (non-identifiability) nếu thiếu giả định cấu trúc. Causal Transformer cũng đòi hỏi các giả định về thứ tự thời gian và tính cân bằng biểu diễn. Bài này chỉ giới thiệu cầu nối ứng dụng chứ không thay thế một học phần đầy đủ về suy luận nhân quả. Ở Chương 6, ta sẽ mở rộng họ hàm hợp lý cho các biến kết quả không tuân theo phân phối Chuẩn, nhưng các nguyên tắc về confounding vẫn giữ nguyên giá trị.

## Video tham khảo

- [A Crash Course in Good and Bad Controls with Carlos Cinelli](https://www.youtube.com/watch?v=IFgHw_E521U) — Spark: a centre for social research innovation, English. **xem trước**. Giới thiệu ngắn gọn về biến kiểm soát đúng và sai, phù hợp với cách tiếp cận hệ số hồi quy như phát biểu nhân quả có điều kiện.
- [Statistical Rethinking 2023 - 06 - Good & Bad Controls](https://www.youtube.com/watch?v=uanZZLlzKHw) — Richard McElreath, English. Trình bày các sơ đồ good và bad controls, củng cố lập luận rằng confounding là vấn đề cấu trúc dữ liệu chứ không phải lỗi phần mềm.
- [Causality: Closing Back Doors](https://www.youtube.com/watch?v=IajzIKW518M) — Econometrics, Causality, and Coding with Dr. HK, English. Hướng dẫn cách đóng đường cửa sau trên DAG, kết nối tư duy nhân quả với hồi quy đa biến.

## Bài tập

1. Vẽ một DAG ba nút cho chuỗi "hiển thị quảng cáo $$\rightarrow$$ nhấp chuột $$\rightarrow$$ mua hàng". Nếu mục tiêu là ước lượng tác động của việc hiển thị lên hành vi mua hàng, điều kiện hóa trên biến nhấp chuột là *good control* hay *bad control*? Giải thích vì sao.
2. Một mô hình cá nhân hóa có hai đặc trưng tương quan 0.97. Kết quả dự báo trên tập kiểm tra rất tốt, nhưng dấu của hai hệ số đảo chiều khi loại bỏ 1% dữ liệu. Bạn có nên diễn giải riêng từng hệ số không? Vì sao?
3. Việc *Causal Transformer* giảm thiểu khả năng dự đoán biến điều trị từ biểu diễn ẩn đang nhằm xử lý dạng gây nhiễu nào đã học ở Bài 5.2?
4. Giả sử thuật toán DAGMA trả về một đồ thị từ nhật ký sản phẩm. Hãy nêu hai mũi tên nhân quả mà bạn sẽ không cho phép mô hình tự vẽ nếu không có cơ sở nghiệp vụ.

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 5, 14.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 18.
- Cinelli, C., Forney, A., & Pearl, J. (2022). A crash course in good and bad controls. *Sociological Methods & Research*. [doi:10.1177/00491241221099552](https://doi.org/10.1177/00491241221099552).
- Bello, K., Aragam, B., & Ravikumar, P. (2022). DAGMA: Learning DAGs via M-matrices and a log-determinant acyclicity characterization. *NeurIPS*. [arXiv:2209.08011](https://arxiv.org/abs/2209.08011).
- Melnychuk, V., Frauen, D., & Feuerriegel, S. (2022). Causal Transformer for estimating counterfactual outcomes. *ICML*. [arXiv:2204.07258](https://arxiv.org/abs/2204.07258).
