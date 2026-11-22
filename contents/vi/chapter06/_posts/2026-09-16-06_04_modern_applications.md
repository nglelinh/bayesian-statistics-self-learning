---
layout: post
title: "Bài 6.4: Ứng dụng hiện đại của GLM Bayes"
chapter: '06'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter06
lesson_type: optional
---

## Mục tiêu học tập

Sau bài học tùy chọn này, bạn sẽ biết cách lựa chọn một mô hình GLM Bayes xuất phát từ *câu chuyện sinh dữ liệu của biến kết quả*, thay vì mặc định áp dụng hồi quy tuyến tính cho mọi bài toán. Bạn cũng sẽ nhận ra cách hồi quy logistic, hồi quy Poisson và các họ mô hình liên quan đang được triển khai trong tín dụng, dịch tễ học và đo lường marketing, đồng thời hiểu rằng phân phối hậu nghiệm của xác suất hay cường độ đếm cần được kết hợp với chi phí quyết định.

## Kiến thức cần có

Các bài 6.1–6.3 đã trình bày hồi quy logistic, hồi quy Poisson và đánh giá GLM. Bài học này không nhắc lại các hàm liên kết, mà kết nối trực tiếp những mô hình đó với các hệ thống ứng dụng thực tế giai đoạn 2022–2026.

## Mở đầu

Chương 6 ra đời vì giả định phân phối Gaussian của Chương 4 không phù hợp với dữ liệu nhị phân và dữ liệu đếm. Trong thực tế triển khai sản phẩm, hạn chế này xuất hiện ngay ở các bài toán quen thuộc: một giao dịch có vỡ nợ hay không, số đơn hàng phát sinh trong một giờ, hay số ca bệnh bị báo cáo trễ. Nếu vẫn tối ưu bình phương tối thiểu, ta đang áp đặt một cơ chế sinh dữ liệu không phù hợp với bản chất của quan sát. Vấn đề cốt lõi của bài học này là chọn đúng họ phân phối cho dữ liệu quan sát trước khi nghĩ đến mạng nơ-ron sâu hay hạ tầng đặc trưng phức tạp.

## Phát triển khái niệm

Một mô hình GLM Bayes giữ cấu trúc tuyến tính trên một thang đo phù hợp:

$$
g(\mathbb E[y_i\mid x_i])=x_i^\top\beta,
$$

sau đó đặt phân phối tiên nghiệm lên $$\beta$$ và suy luận phân phối hậu nghiệm. Với hồi quy logistic, $$g$$ là hàm logit và $$y$$ tuân theo phân phối Bernoulli. Với hồi quy Poisson, $$g$$ là hàm log và $$y$$ là dữ liệu đếm. Phân phối hậu nghiệm không trực tiếp trả về một nhãn phân lớp cứng, mà trả về một phân phối xác suất cho xác suất sự kiện hoặc cường độ đếm. Ngưỡng phân loại chỉ xuất hiện ở bước sau, khi hàm mất mát xác định rõ chi phí của dương tính giả so với âm tính giả.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Hồi quy logistic Bayes cho tín dụng, gian lận và rủi ro lâm sàng

Trong câu chuyện sinh dữ liệu, mỗi hồ sơ có một xác suất xảy ra sự kiện hiếm là $$\theta(x)=\mathrm{logit}^{-1}(x^\top\beta)$$, và nhãn quan sát được sinh ra như phép thử Bernoulli với xác suất đó. Phân phối tiên nghiệm trên $$\beta$$ giúp xác suất không bị đẩy cực đoan về 0 hoặc 1 khi gặp một tổ hợp đặc trưng chưa từng xuất hiện — đúng với tinh thần điều chuẩn (regularization) sẽ được trình bày ở Chương 7. Trong thực tế, điều doanh nghiệp cần từ phân phối hậu nghiệm không chỉ là độ chính xác phân lớp cao nhất, mà là một xác suất đã được hiệu chỉnh để làm cơ sở đặt hạn mức, tính phí bảo hiểm hoặc thiết lập ngưỡng phê duyệt. Nghiên cứu của Grinsztajn, Oyallon và Varoquaux (2022) cho thấy trên nhiều tập dữ liệu dạng bảng không đồng nhất, các mô hình nông vẫn vượt trội hơn mạng học sâu; do đó một mô hình logistic Bayes được đặc tả tốt vẫn là lựa chọn rất phù hợp.

### 2. Hồi quy Poisson và Negative Binomial cho dự báo nhu cầu và nowcasting

Số đơn hàng, số cuộc gọi và số ca bệnh theo ngày đều là dữ liệu đếm. Mô hình Poisson giả định phương sai bằng trung bình, nhưng dữ liệu dịch tễ và thương mại thường cần mô hình Negative Binomial để xử lý hiện tượng quá phân tán. Trong bối cảnh dịch bệnh, bài toán ước lượng hiện thời (nowcasting) phải vừa ước lượng cường độ dịch vừa hiệu chỉnh độ trễ khai báo. Mô hình Bayes phân cấp theo các khu vực địa lý thực chất là mở rộng của GLM ở Chương 6 với hệ số chặn thay đổi theo nhóm. Phân phối dự báo hậu nghiệm cho tuần kế tiếp không chỉ là một con số duy nhất, mà là một dải bất định giúp kho vận và bệnh viện lập kế hoạch dự phòng.

### 3. Media mix modeling như một GLM nhân quả có tiên nghiệm

Google Meridian (2024) là một khung mô hình hóa hỗn hợp tiếp thị (marketing mix modeling) theo hướng Bayes: doanh số được mô hình hóa như hàm của các kênh truyền thông đã qua biến đổi trễ quảng cáo (adstock) và lợi suất giảm dần, kết hợp với các yếu tố ngoài truyền thông, cùng phân phối tiên nghiệm có thể hiệu chỉnh bằng kết quả thí nghiệm. Việc suy luận sử dụng MCMC/NUTS. Hàm hợp lý gần với hồi quy chuẩn, nhưng tinh thần vẫn là GLM mở rộng với các biến đổi phi tuyến của mức độ phơi nhiễm. Tài liệu của Meridian nhấn mạnh mục tiêu chính là suy luận nhân quả về ROI, chứ không phải tối thiểu hóa sai số dự báo trên tập kiểm tra (hold-out) — điều này nhắc lại phân biệt quan trọng từ Chương 5 và 6 rằng cùng một họ mô hình có thể phục vụ hai câu hỏi khác nhau.

### 4. Đánh giá GLM: ưu tiên độ hiệu chỉnh trước nhãn cứng

Bài 6.3 đã lưu ý rằng ma trận nhầm lẫn không trung tính về chi phí. Trong tín dụng, bỏ sót một khoản vay vỡ nợ thường tốn kém hơn từ chối nhầm một khách hàng tốt. Trong dịch tễ học, bỏ sót một ổ dịch nghiêm trọng hơn cảnh báo thừa. Vì vậy, phân phối hậu nghiệm của $$\theta(x)$$ cần được kiểm tra bằng biểu đồ độ tin cậy (reliability diagram), thay vì chỉ dựa vào accuracy. Một mô hình GLM có độ phân tách vừa phải nhưng hiệu chỉnh tốt vẫn có thể dẫn đến quyết định hợp lý hơn.

## Diễn giải và nhận định

Hệ số trong hồi quy logistic biểu thị mức thay đổi trên thang log-odds, không phải mức thay đổi cố định trên thang xác suất. Hệ số trong hồi quy Poisson biểu thị mức thay đổi trên thang log-cường độ. Khoảng hậu nghiệm của ROI truyền thông đã gộp chung độ bất định của hiệu ứng adstock, các biến nhiễu và quá trình lấy mẫu. Tuy nhiên, không một khoảng hậu nghiệm nào tự động trở thành quyết định cho đến khi hàm mất mát được xác định rõ.

## Ứng dụng

Phê duyệt tín dụng, phát hiện gian lận, dự báo nhu cầu, nowcasting và phân bổ ngân sách quảng cáo là năm lĩnh vực mà GLM Bayes đã trở thành thành phần vận hành thực tế, không còn dừng ở ví dụ trong sách giáo khoa.

## Giới hạn và hướng mở rộng

Meridian lưu ý rằng hiệu năng dự báo tốt trên tập hold-out không chứng minh ước lượng hiệu ứng truyền thông là đúng. Hồi quy Poisson sẽ kém phù hợp khi dữ liệu có quá nhiều giá trị 0 (zero-inflation). Hồi quy logistic tuyến tính cũng không tự nắm bắt được các tương tác phức tạp nếu ta không chủ động đưa chúng vào mô hình. Chương 7 sẽ tiếp tục đặt câu hỏi nên chọn phân phối tiên nghiệm nào để giữ mô hình GLM khỏi quá khớp khi số lượng biến giải thích tăng lên.

## Video tham khảo

- [Explaining generalized linear models (GLMs) | VNT #15](https://www.youtube.com/watch?v=1fZeBafD1nw) — Very Normal, English. **Xem trước**. Giải thích cách chọn GLM theo kiểu biến kết quả, thay cho thói quen dùng hồi quy tuyến tính cho mọi bài toán.
- [GLM Intro - 4 - Link Function](https://www.youtube.com/watch?v=J4zNmGqttVo) — Meerkat Statistics, English. Trình bày vai trò của hàm liên kết trong việc nối kỳ vọng của biến kết quả với phần dự báo tuyến tính, hỗ trợ cho logistic và Poisson trong thực tế.
- [Statistical Rethinking 2023 - 19 - Generalized Linear Madness](https://www.youtube.com/watch?v=zffwg0xDOgE) — Richard McElreath, English. Phân tích các biến thể GLM ngoài khuôn mẫu sách giáo khoa, mở rộng góc nhìn về các họ mô hình gần logistic và Poisson.

## Bài tập

1. Một mô hình dự đoán vỡ nợ đạt accuracy 98% do chỉ có 2% hồ sơ thực sự vỡ nợ. Trung bình hậu nghiệm của $$\theta(x)$$ trên nhóm rủi ro cao là 0.15. Vì sao chỉ số accuracy đang che khuất đúng đối tượng mà GLM Bayes quan tâm?
2. Viết câu chuyện sinh dữ liệu cho số đơn hàng mỗi giờ tại một nhà kho. Khi nào bạn nên chuyển từ Poisson sang Negative Binomial, và phân phối dự báo hậu nghiệm sẽ thay đổi hình dạng như thế nào?
3. Tài liệu Meridian khuyến nghị không lấy sai số dự báo trên tập hold-out làm tiêu chí chính. Hãy liên hệ khuyến nghị này với sự khác biệt giữa dự báo và suy luận nhân quả ở Chương 5.
4. Hãy chọn một ngưỡng cho mô hình hồi quy logistic khi chi phí âm tính giả cao gấp mười lần dương tính giả. Ngoài ước lượng điểm $$\hat\beta$$, bạn cần thêm thông tin nào từ phân phối hậu nghiệm?

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 16.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 21–22.
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on typical tabular data? *NeurIPS*.
- Google. (2024). *Meridian*: Bayesian marketing mix modeling. [Bayesian inference](https://developers.google.com/meridian/docs/causal-inference/bayesian-inference); [GitHub](https://github.com/google/meridian).
- [Stan User’s Guide, GLM chapters](https://mc-stan.org/docs/stan-users-guide/index.html).
- [PyMC GLM examples](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/GLM_linear.html).
