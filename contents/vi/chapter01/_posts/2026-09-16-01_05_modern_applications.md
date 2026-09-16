---
layout: post
title: "Bài 1.5: Ứng dụng hiện đại của định lý Bayes trong khoa học máy tính"
chapter: '01'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: optional
---

## Mục tiêu học tập

Sau bài tùy chọn này, bạn nhìn định lý Bayes không còn như công thức chẩn đoán trong sách, mà như quy tắc cập nhật niềm tin đang vận hành trong lọc thư rác, phát hiện gian lận, và lượng hóa bất định của mô hình ngôn ngữ. Điều cần thay đổi là câu hỏi: không hỏi “công thức viết thế nào?”, mà hỏi “prior, likelihood và posterior đang đứng ở đâu trong một hệ thống thật?”.

## Kiến thức cần có

Bài viết dựa trên các bài 1.1–1.4. Nó không viết lại phê phán p-value hay so sánh Bayesian–frequentist. Nó chỉ đưa cùng một sơ đồ cập nhật vào các sản phẩm khoa học máy tính gần đây.

## Mở đầu

Chương 1 đã tạo một căng thẳng: p-value trả lời một câu hỏi mà người dùng thường không đặt, trong khi quyết định thực sự cần xác suất của giả thuyết sau dữ liệu. Lọc thư rác, cổng thanh toán, và chatbot đều sống trong đúng căng thẳng ấy. Chúng phải biến một quan sát mới—một email, một giao dịch, một câu trả lời được sinh ra—thành một niềm tin cập nhật đủ trung thực để hành động. Nếu chỉ có điểm số xếp hạng, hệ thống vẫn chưa biết mình nên im hay nên cảnh báo.

## Phát triển khái niệm

Định lý Bayes,

$$
P(H\mid D)=\frac{P(D\mid H)P(H)}{P(D)},
$$

vẫn là cùng một phép nhân prior với likelihood rồi chuẩn hóa. Trong sản phẩm, $$H$$ có thể là “thư rác”, “giao dịch gian lận”, hoặc “câu trả lời vừa sinh là đúng”. $$D$$ là bằng chứng quan sát được. Phần khó không phải đại số, mà là prior bị lệch (tỷ lệ nền thư rác thay đổi theo mùa) và likelihood bị đọc như thể đã là posterior.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Thư rác, lừa đảo và phân loại có hiệu chỉnh

Câu chuyện sinh cổ điển của Naive Bayes vẫn còn sống: mỗi token được xem như bằng chứng có điều kiện về nhãn thư rác, rồi các likelihood được nhân dưới giả định độc lập. Hệ thống hiện đại thay từ điển bằng biểu diễn dày hơn, nhưng câu hỏi Bayes không đổi. Prior là tỷ lệ nền của thư rác; likelihood là “email kiểu này xuất hiện nhiều hơn dưới nhãn nào?”; posterior là xác suất thư ấy là rác *sau khi đã đọc nội dung*. Nếu ngưỡng hành động bỏ qua tỷ lệ nền, bạn đang dùng likelihood như thể nó đã là posterior—đúng lỗi mà bài 1.3 cảnh báo trong chẩn đoán y khoa.

### 2. Gian lận thanh toán như cập nhật dưới tỷ lệ nền cực thấp

Gian lận hiếm. Prior $$P(H)$$ vì thế rất nhỏ, nên một tín hiệu “trông khả nghi” vẫn có thể để lại posterior vừa phải. Đó là phiên bản công nghiệp của nghịch lý xét nghiệm hiếm bệnh. Một hệ thống trung thực phải giữ tỷ lệ nền trong công thức, rồi chỉ hành động khi posterior vượt ngưỡng do chi phí bỏ sót và báo động giả quy định. Điểm xếp hạng cao chưa phải niềm tin đã cập nhật.

### 3. Mô hình ngôn ngữ tự đánh giá câu trả lời của chính mình

Kadavath et al. (2022) hỏi một câu rất Bayesian: sau khi mô hình đề xuất một câu trả lời, xác suất $$P(\text{True})$$ rằng câu ấy đúng là bao nhiêu? Họ thấy các mô hình lớn có thể được hiệu chỉnh tốt trên nhiệm vụ đúng/sai được định dạng, và việc nhìn nhiều mẫu tự sinh trước khi đánh giá một ứng viên sẽ giúp self-evaluation. Kuhn, Gal và Farquhar (2023) chỉ ra một nút thắt mới: trong ngôn ngữ, nhiều câu khác chữ nhưng cùng nghĩa, nên entropy trên chuỗi token không phải entropy trên giả thuyết. Semantic entropy nhóm các câu tương đương nghĩa rồi mới đo bất định—tức là đo posterior trên không gian giả thuyết, không trên không gian xâu ký tự.

### 4. Hỏi mô hình lấy độ tin đã hiệu chỉnh

Tian et al. (2023) cho thấy, với các mô hình đã tinh chỉnh bằng phản hồi người, xác suất nói thành lời (“tôi tin 70%”) đôi khi được hiệu chỉnh tốt hơn xác suất điều kiện trên token. Điều này không biến chatbot thành một Bayesian sampler, nhưng nó cho thấy sản phẩm đang cố trích một posterior mà người dùng có thể đọc như độ hợp lý (plausibility). Nếu con số ấy không khớp tần suất đúng, ta đang lặp lại khủng hoảng diễn giải mà Chương 1 mở đầu.

## Diễn giải và nhận định

Posterior trong các hệ thống này trả lời “giả thuyết này còn đáng tin bao nhiêu sau bằng chứng?”. Nó không trả lời “thuật toán đã bác bỏ giả thuyết đối lập”. Một $$P(\text{True})$$ cao trên một câu trả lời ảo giác vẫn có thể xảy ra nếu likelihood quá lạc quan. Bayes không bảo vệ ta khỏi likelihood sai; nó chỉ buộc ta nói rõ prior đang bị dữ liệu kéo đi đâu.

## Ứng dụng

Ba miền—thư rác/lừa đảo, gian lận, và bất định ngôn ngữ—đều là bài toán ra quyết định dưới tỷ lệ nền lệch và chi phí không đối xứng. Chúng chuẩn bị trực tiếp cho phân tích quyết định ở Chương 8, nhưng đã có thể được hiểu chỉ bằng định lý Bayes.

## Giới hạn và hướng mở rộng

Naive Bayes độc lập từ là một câu chuyện sinh thô. Semantic entropy cần một mô hình tương đương nghĩa, bản thân nó cũng bất định. Hiệu chỉnh trên một chuẩn đánh giá không bảo đảm hiệu chỉnh sau khi phân phối dịch chuyển. Bài này cố ý không viết lại lý thuyết cập nhật; Chương 2 sẽ biến sơ đồ ấy thành likelihood, prior và posterior tường minh.

## Bài tập

1. Tỷ lệ thư rác tăng từ 5% lên 30% trong mùa lễ. Likelihood của một từ khóa không đổi. Posterior của một email chứa từ khóa ấy đổi thế nào, và vì sao bộ lọc chỉ dùng điểm từ khóa sẽ trượt?
2. Một cổng thanh toán báo “điểm gian lận 0.95”. Bạn sẽ hỏi thêm hai câu nào trước khi đóng giao dịch, một về prior và một về ngưỡng quyết định?
3. Vì sao entropy trên các câu trả lời khác chữ có thể phóng đại bất định so với entropy trên các nghĩa? Hãy lấy một câu hỏi có hai cách diễn đạt đúng.
4. So sánh $$P(\text{True})$$ của Kadavath et al. với posterior $$P(H\mid D)$$ trong ví dụ chẩn đoán của bài 1.3. Cái gì đóng vai trò prior?

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 1.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 4–5.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. [arXiv:2207.05221](https://arxiv.org/abs/2207.05221).
- Kuhn, L., Gal, Y., & Farquhar, S. (2023). Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. *ICLR*. [arXiv:2302.09664](https://arxiv.org/abs/2302.09664).
- Tian, K., et al. (2023). Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. [arXiv:2305.14975](https://arxiv.org/abs/2305.14975).
