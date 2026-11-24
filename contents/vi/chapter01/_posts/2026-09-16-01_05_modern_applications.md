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

Từ một định lý viết trên giấy thế kỷ 18, quy tắc Bayes ngày nay chạy âm thầm bên trong hàng tỷ thiết bị mỗi giây: bộ lọc thư rác chấm điểm từng email mới đến, hệ thống dẫn đường xe tự lái hợp nhất tín hiệu radar và camera theo bộ lọc Kalman/Bayes, còn các nền tảng thử nghiệm sản phẩm trực tuyến dùng cập nhật Bayes để ra quyết định nhanh mà không vướng lỗi *optional stopping*.

Bài học này khép lại Chương 1 bằng cách nối nền tảng triết học và công thức Bayes với những kiến trúc thực chiến của khoa học máy tính hiện đại.

---

## Mục tiêu học tập

Sau bài học tùy chọn này, bạn sẽ nhìn định lý Bayes không chỉ như một công thức chẩn đoán trong sách giáo khoa, mà như quy tắc cập nhật niềm tin đang vận hành trong bộ lọc thư rác, hệ thống phát hiện gian lận và bài toán định lượng bất định của mô hình ngôn ngữ. Trọng tâm cần thay đổi nằm ở câu hỏi: không dừng ở “công thức viết thế nào?”, mà đặt câu hỏi “prior, likelihood và posterior nằm ở đâu trong một hệ thống thực tế?”.


## Bản đồ kiến thức nền: Định lý Bayes trong Hệ thống Thông minh và Khoa học Máy tính

Ba trụ cột sau cho thấy cách định lý Bayes vượt ra khỏi sách giáo khoa để vận hành các hệ thống quy mô lớn:

- **Phân loại xác suất & Lọc thông tin (Naive Bayes & Probabilistic Classifiers):** Chuyển bài toán phân loại văn bản, phát hiện gian lận hay chẩn đoán lỗi thành phép tính log-prior cộng tổng log-likelihood từng đặc trưng, cho tốc độ cập nhật trực tuyến cực nhanh.
- **Suy luận trực tuyến & Lọc trạng thái (Recursive Bayesian Filtering):** Trong robot học, định vị GPS và theo dõi mục tiêu, trạng thái ẩn của hệ thống được cập nhật liên tục theo thời gian qua chu kỳ *Dự báo (Predict) → Cập nhật Bayes (Update)* — trong đó bộ lọc Kalman là trường hợp tuyến tính – Gaussian kinh điển.
- **Thử nghiệm thích nghi & Khám phá (Thompson Sampling / Bayesian Optimization):** Thay vì chia lưu lượng cố định kiểu cổ điển, các hệ thống gợi ý và tối ưu siêu tham số rút mẫu trực tiếp từ hậu nghiệm để tự động cân bằng giữa *khai thác* phương án tốt nhất và *khám phá* phương án còn nhiều bất định.

---

## Kiến thức cần có

Bài viết kế thừa các bài 1.1–1.4, không lặp lại phần phê phán p-value hay so sánh Bayesian–frequentist mà đưa trực tiếp cùng một sơ đồ cập nhật vào các ứng dụng khoa học máy tính hiện đại.

## Mở đầu

Chương 1 đã chỉ ra một mâu thuẫn cốt lõi: p-value trả lời một câu hỏi khác với điều người dùng cần, trong khi việc ra quyết định thực tế lại đòi hỏi xác suất của giả thuyết sau khi quan sát dữ liệu. Bộ lọc thư rác, cổng thanh toán và trợ lý hội thoại (chatbot) đều đối mặt với đúng bài toán này. Chúng phải chuyển một quan sát mới — một email, một giao dịch hay một câu trả lời vừa được sinh ra — thành niềm tin đã cập nhật đủ tin cậy để làm cơ sở hành động. Nếu chỉ dừng ở một điểm số xếp hạng, hệ thống vẫn chưa thể xác định nên giữ im lặng hay phát cảnh báo.

## Phát triển khái niệm

Định lý Bayes,

$$
P(H\mid D)=\frac{P(D\mid H)P(H)}{P(D)},
$$

vẫn là phép nhân giữa prior và likelihood rồi chuẩn hóa. Trong các hệ thống thực tế, $$H$$ có thể là “thư rác”, “giao dịch gian lận” hoặc “câu trả lời vừa sinh ra là đúng”, còn $$D$$ là bằng chứng quan sát được. Thách thức chính không nằm ở phép biến đổi đại số, mà ở việc prior thay đổi theo bối cảnh (chẳng hạn tỷ lệ nền của thư rác biến động theo mùa) và sai lầm khi đọc likelihood như thể nó đã là posterior.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Lọc thư rác, phát hiện lừa đảo và phân loại có hiệu chỉnh

Mô hình sinh cổ điển của Naive Bayes vẫn được vận dụng rộng rãi: mỗi từ hoặc đơn vị văn bản (token) được xem là bằng chứng có điều kiện về nhãn thư rác, sau đó các likelihood được nhân với nhau dưới giả định độc lập có điều kiện. Các hệ thống hiện đại thay từ điển rời rạc bằng các biểu diễn đặc hơn (dense representations), nhưng cấu trúc Bayes không thay đổi: prior là tỷ lệ nền của thư rác; likelihood trả lời câu hỏi “email kiểu này xuất hiện thường xuyên hơn dưới nhãn nào?”; còn posterior là xác suất email là thư rác *sau khi đã đọc nội dung*. Nếu ngưỡng hành động bỏ qua tỷ lệ nền, hệ thống đang nhầm lẫn likelihood với posterior — đúng lỗi mà Bài 1.3 đã chỉ ra trong bài toán chẩn đoán y khoa.

### 2. Phát hiện gian lận thanh toán dưới tỷ lệ nền cực thấp

Giao dịch gian lận chiếm tỷ lệ rất nhỏ, nên prior $$P(H)$$ rất thấp. Vì vậy, một tín hiệu “trông có vẻ khả nghi” vẫn có thể chỉ cho ra posterior ở mức vừa phải — đây chính là phiên bản công nghiệp của nghịch lý xét nghiệm bệnh hiếm. Một hệ thống đáng tin cậy phải đưa tỷ lệ nền vào phép tính và chỉ kích hoạt hành động khi posterior vượt ngưỡng được xác định từ chi phí bỏ sót gian lận và chi phí báo động giả. Một điểm xếp hạng cao không đồng nghĩa với xác suất hậu nghiệm cao.

### 3. Mô hình ngôn ngữ tự đánh giá câu trả lời của chính mình

Kadavath et al. (2022) đặt ra một câu hỏi mang đậm tinh thần Bayes: sau khi mô hình ngôn ngữ đề xuất một câu trả lời, xác suất $$P(\text{True})$$ rằng câu trả lời ấy đúng là bao nhiêu? Nghiên cứu cho thấy các mô hình lớn có thể được hiệu chỉnh tốt trên các tác vụ đúng/sai có định dạng rõ ràng, và việc tham khảo nhiều mẫu tự sinh trước khi đánh giá một phương án ứng viên giúp cải thiện khả năng tự đánh giá.

Kuhn, Gal và Farquhar (2023) chỉ ra thêm một điểm nghẽn quan trọng: trong ngôn ngữ tự nhiên, nhiều câu khác nhau về mặt câu chữ nhưng lại mang cùng một ý nghĩa, nên entropy tính trên chuỗi token không phản ánh đúng entropy trên không gian giả thuyết. Phương pháp *semantic entropy* nhóm các câu trả lời tương đương về nghĩa lại với nhau rồi mới đo độ bất định — tức là đo phân phối hậu nghiệm trên không gian giả thuyết thay vì trên không gian chuỗi ký tự.

### 4. Khai thác độ tin cậy đã hiệu chỉnh trực tiếp từ mô hình

Tian et al. (2023) cho thấy rằng với các mô hình ngôn ngữ đã được tinh chỉnh bằng phản hồi của con người, xác suất được diễn đạt trực tiếp bằng lời (chẳng hạn “tôi tin 70%”) đôi khi có độ hiệu chỉnh tốt hơn xác suất điều kiện tính trên token. Điều này không biến chatbot thành một bộ suy luận Bayes chuẩn mực, nhưng cho thấy các hệ thống thực tế đang tìm cách trích xuất một giá trị giống posterior mà người dùng có thể đọc như độ hợp lý (plausibility). Nếu con số đó không khớp với tần suất đúng thực tế, ta lại rơi vào chính vấn đề diễn giải sai mà Chương 1 đã nêu ra từ đầu.

## Diễn giải và nhận định

Posterior trong các hệ thống này trả lời câu hỏi: “giả thuyết này còn đáng tin đến mức nào sau khi có bằng chứng?”, chứ không trả lời “thuật toán đã bác bỏ giả thuyết đối lập hay chưa”. Một giá trị $$P(\text{True})$$ cao trên một câu trả lời ảo giác vẫn có thể xảy ra nếu likelihood được ước lượng quá lạc quan. Định lý Bayes không tự bảo vệ ta khỏi một likelihood sai; nó chỉ buộc ta phải thể hiện minh bạch việc dữ liệu đang kéo prior đi theo hướng nào.

## Ứng dụng

Cả ba lĩnh vực — lọc thư rác/lừa đảo, phát hiện gian lận thanh toán và định lượng bất định ngôn ngữ — đều là các bài toán ra quyết định dưới tỷ lệ nền mất cân bằng và chi phí sai sót không đối xứng. Chúng đặt nền móng trực tiếp cho phân tích quyết định ở Chương 8, nhưng bản chất của chúng đã có thể hiểu rõ chỉ từ định lý Bayes.

## Giới hạn và hướng mở rộng

Giả định độc lập giữa các từ trong Naive Bayes là một mô hình sinh khá thô. Semantic entropy phụ thuộc vào một mô hình đánh giá tương đương nghĩa mà bản thân nó cũng chứa độ bất định. Ngoài ra, một mô hình được hiệu chỉnh tốt trên một bộ tiêu chuẩn đánh giá không bảo đảm vẫn giữ nguyên độ hiệu chỉnh khi phân phối dữ liệu dịch chuyển. Bài học này không đi lại vào lý thuyết cập nhật; Chương 2 sẽ trình bày tường minh các thành phần likelihood, prior và posterior.


## Khung giải thích (nên đọc chậm): Giải phẫu bộ lọc spam Naive Bayes trên thang tỷ số Odds

Để thấy định lý Bayes hoạt động nhanh và gọn thế nào trong khoa học máy tính, hãy theo dõi 4 bước phân loại một email mới:

1. **Thiết lập tỷ số Odds tiên nghiệm:** Dựa trên tỷ lệ spam lịch sử $$P(\text{Spam}) / P(\text{Ham})$$.
2. **Tính hệ số Bayes cho từng từ khóa xuất hiện:** Với mỗi từ $$w_j$$, tính tỷ số $$P(w_j \mid \text{Spam}) / P(w_j \mid \text{Ham})$$.
3. **Nhân dồn các hệ số Bayes (hoặc cộng trên thang log):** Dưới giả định độc lập có điều kiện (Naive Bayes), tỷ số Odds hậu nghiệm bằng Odds tiên nghiệm nhân với tích các hệ số Bayes.
4. **Quy đổi sang xác suất hậu nghiệm và áp ngưỡng chi phí:** $$P(\text{Spam} \mid \mathbf{w}) = \frac{\text{Odds}}{1 + \text{Odds}}$$.

### Ví dụ tính toán cầm tay chỉ việc: Chấm điểm một email chứa hai từ khóa

Giả sử $$20\%$$ email đến là Spam ($$\text{Prior Odds} = 0.20 / 0.80 = 0.25$$). Một email chứa đồng thời hai từ khóa `"khuyến mãi"` và `"chuyển khoản"` có thống kê như sau:

| Từ khóa $$w_j$$ | $$P(w_j \vert \text{Spam})$$ | $$P(w_j \vert \text{Ham})$$ | Hệ số Bayes $$\text{BF}_j = \frac{P(w_j \vert \text{Spam})}{P(w_j \vert \text{Ham})}$$ |
| --- | --- | --- | --- |
| `"khuyến mãi"` | $$0.60$$ | $$0.10$$ | $$0.60 / 0.10 = 6.0$$ |
| `"chuyển khoản"` | $$0.40$$ | $$0.05$$ | $$0.40 / 0.05 = 8.0$$ |

Áp dụng quy tắc nhân tỷ số Odds:

$$
\text{Posterior Odds} = 0.25 \times 6.0 \times 8.0 = 12.0 \implies P(\text{Spam} \mid \mathbf{w}) = \frac{12.0}{1 + 12.0} = \frac{12}{13} \approx 0.9231 \quad (92.31\%).
$$

**Hiểu lầm cần tránh:** Quên làm trơn Laplace (*Laplace smoothing*) khi gặp một từ chưa từng xuất hiện trong tập Spam lịch sử — lúc đó $$P(w_j \mid \text{Spam}) = 0$$ sẽ kéo toàn bộ tích xác suất về 0 bất kể các từ còn lại đáng ngờ đến đâu.

**Kiểm tra nhanh:** Nếu email đó xuất hiện thêm một từ khóa rất đặc trưng cho email công việc ($$\text{BF}_3 = 0.1$$), Odds hậu nghiệm lập tức điều chỉnh về $$12.0 \times 0.1 = 1.2$$, tương ứng xác suất spam giảm xuống $$1.2 / 2.2 \approx 54.5\%$$.

---

## Video tham khảo

- [Naive Bayes từ A-Z: Trực Giác đến Toán Học](https://www.youtube.com/watch?v=SqW_p3311yY) — Gà AI, Tiếng Việt. **xem trước**. Giải thích Naive Bayes từ trực giác đến công thức, minh họa trực tiếp cách đặt bộ lọc thư rác vào sơ đồ prior–likelihood–posterior.
- [Bayes Rule Example of Spam Filter](https://www.youtube.com/watch?v=bc-SL86azrc) — Eric Walden, English. Trình bày cách cập nhật xác suất thư rác của một email theo từng bằng chứng, hỗ trợ ví dụ về tỷ lệ nền thay đổi.
- [MIT 6.S191: Uncertainty in Deep Learning](https://www.youtube.com/watch?v=veYq6EWZyVc) — Alexander Amini, English. Giới thiệu về độ bất định trong học sâu; dù không đề cập trực tiếp đến semantic entropy, bài giảng hỗ trợ lập luận không nên đọc điểm số trên token như posterior của giả thuyết.

## Bài tập

1. Tỷ lệ thư rác tăng từ 5% lên 30% trong mùa lễ, trong khi likelihood của một từ khóa không đổi. Posterior của một email chứa từ khóa đó thay đổi ra sao, và vì sao bộ lọc chỉ dựa vào điểm từ khóa sẽ hoạt động kém chính xác?
2. Một cổng thanh toán báo “điểm gian lận 0.95”. Trước khi khóa giao dịch, bạn cần hỏi thêm hai câu nào: một câu về prior và một câu về ngưỡng quyết định?
3. Vì sao entropy tính trên các câu trả lời khác nhau về câu chữ có thể phóng đại độ bất định so với entropy tính trên ý nghĩa? Hãy lấy một câu hỏi có hai cách diễn đạt đều đúng để minh họa.
4. So sánh $$P(\text{True})$$ của Kadavath et al. với posterior $$P(H\mid D)$$ trong ví dụ chẩn đoán ở Bài 1.3. Thành phần nào đóng vai trò là prior?

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 1.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 4–5.
- Kadavath, S., et al. (2022). Language models (mostly) know what they know. [arXiv:2207.05221](https://arxiv.org/abs/2207.05221).
- Kuhn, L., Gal, Y., & Farquhar, S. (2023). Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. *ICLR*. [arXiv:2302.09664](https://arxiv.org/abs/2302.09664).
- Tian, K., et al. (2023). Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback. [arXiv:2305.14975](https://arxiv.org/abs/2305.14975).
