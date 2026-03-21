---
layout: post
title: "Bài 4.4: Model Checking và Prediction - Đảm bảo Model Tốt"
chapter: '04'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu rằng fit model mới chỉ là nửa đầu của regression Bayes. Nửa còn lại là kiểm tra model có đang mô tả dữ liệu hợp lý hay không, và dùng posterior để dự đoán dữ liệu mới một cách trung thực. Bạn cũng cần nắm posterior predictive checks (kiểm tra dự báo hậu nghiệm) như công cụ trung tâm của bước này.

> **Ví dụ mini.** Một đường hồi quy có thể nhìn rất đẹp trên scatter plot, nhưng nếu nó không sinh ra dữ liệu giống dữ liệu thật thì model vẫn có vấn đề. Model checking là cách chất vấn mô hình thay vì chỉ tin vì nó đã chạy xong.
>
> **Câu hỏi tự kiểm tra.** Vì sao một posterior “trông ổn” chưa đủ để kết luận mô hình là tốt?

## 1. Fit tốt chưa chắc model tốt

Đây là một chuyển biến quan trọng trong tư duy.

Nhiều người học regression dừng lại ở chỗ ước lượng slope, xem interval, rồi kết luận như thể công việc đã hoàn tất.

Nhưng một Bayesian workflow (quy trình Bayes) trưởng thành sẽ hỏi thêm những câu khó hơn: model này có tái tạo được dữ liệu quan sát không, residual (phần dư) có còn pattern (mẫu hình) đáng ngờ không, và dự đoán cho dữ liệu mới có thực sự hợp lý hay không.

George Box có câu rất nổi tiếng:

> “All models are wrong, but some are useful.”

Mục tiêu không phải tìm ra một model “đúng tuyệt đối”, mà là một model đủ hữu ích, đủ trung thực, và không bỏ sót những cấu trúc quan trọng của dữ liệu.

## 2. Posterior predictive distribution (phân phối dự báo hậu nghiệm) là gì?

Giả sử bạn đã có posterior của các tham số. Khi đó bạn có thể sinh dữ liệu mới $$\tilde y$$ từ model:

$$
p(\tilde y \mid y) = \int p(\tilde y \mid \theta)\,p(\theta \mid y)\,d\theta.
$$

Ý nghĩa của posterior predictive distribution là ta không chỉ suy luận về tham số, mà còn suy luận về dữ liệu tương lai hoặc dữ liệu tái tạo từ chính model.

Đây chính là cầu nối giữa estimation và prediction.

## 3. Posterior predictive check (PPC, kiểm tra dự báo hậu nghiệm) là gì?

PPC hỏi một câu rất thực tế:

> Nếu model của tôi đúng, dữ liệu giả lập sinh từ model có giống dữ liệu thật không?

Quy trình cơ bản của PPC là lấy nhiều mẫu tham số từ posterior, từ mỗi mẫu đó sinh dữ liệu giả, rồi so sánh dữ liệu giả với dữ liệu quan sát.

Nếu dữ liệu giả có hình dạng, độ phân tán, và các pattern tương tự dữ liệu thật, thì model có nhiều cơ sở hơn để được xem là đang ổn.

![Posterior predictive checks]({{ site.baseurl }}/img/chapter_img/chapter04/posterior_predictive_checks.png)

## 4. PPC nên nhìn những gì?

Không có một kiểm tra duy nhất phù hợp cho mọi bài toán. Bạn nên nhìn nhiều góc:

### 4.1. Phân phối tổng thể

Histogram hoặc density của dữ liệu giả có giống dữ liệu thật không?

### 4.2. Trung bình và độ phân tán

Model có tái hiện được mean (trung bình), variance (phương sai), min/max hợp lý, hay tail behavior (hành vi phần đuôi) của dữ liệu thật hay không?

### 4.3. Quan hệ giữa predictor và response

Với regression, điều rất quan trọng là mô hình có tái hiện đúng pattern giữa predictor (biến dự báo) $$x$$ và response (biến phản hồi) $$y$$ hay không.

### 4.4. Statistic chuyên biệt theo bài toán

Ví dụ, số outlier (điểm ngoại lai), độ lệch, độ bất đối xứng, hay tỷ lệ vượt ngưỡng.

## 5. Residual analysis (phân tích phần dư) vẫn rất quan trọng

Ngay cả trong Bayesian regression, residual vẫn là một gương soi tốt cho mô hình.

Ta thường nhìn residual vs fitted (phần dư theo giá trị ước lượng), residual vs predictor (phần dư theo biến dự báo), phân phối residual, dấu hiệu heteroskedasticity (phương sai thay đổi), và dấu hiệu nonlinearity (phi tuyến).

![Regression assumptions và diagnostics]({{ site.baseurl }}/img/chapter_img/chapter04/regression_assumptions_diagnostic.png)

Nếu residual cho thấy pattern có hệ thống, model có thể đang bỏ sót phi tuyến, interaction (tương tác), heteroskedasticity, hoặc một biến quan trọng nào đó chưa được đưa vào.

## 6. Prediction trong Bayes khác gì prediction điểm?

Trong regression cổ điển, nhiều người chỉ quen với một giá trị dự đoán trung bình duy nhất.

Bayesian prediction đi xa hơn ở chỗ nó giữ lại bất định của tham số, và cả bất định do noise (độ nhiễu) của quan sát mới.

Điều này cho phép bạn nói không chỉ “dự đoán là 72”, mà còn “vùng giá trị hợp lý của dự đoán nằm ở đâu, và ta chắc đến mức nào”.

Đó là kiểu dự báo hữu ích hơn nhiều cho ra quyết định.

## 7. Prediction interval (khoảng dự đoán) và uncertainty (bất định)

Có hai nguồn bất định chính:

### 7.1. Bất định tham số

Ta chưa biết chính xác $$\alpha,\beta,\sigma$$.

### 7.2. Bất định của quan sát mới

Ngay cả nếu biết tham số hoàn hảo, quan sát mới vẫn dao động quanh đường trung bình.

Prediction interval vì vậy luôn rộng hơn uncertainty chỉ của mean response (giá trị trung bình phản hồi).

Đây là điều rất quan trọng khi báo cáo dự báo cho người dùng cuối.

## 8. Model checking không phải để “bắt model hoàn hảo”

Đừng hiểu model checking như một trò chơi nhị phân kiểu hoặc model hoàn hảo hoặc phải vứt đi.

Nó là quá trình để hỏi model đang sai ở đâu, sai ở mức nào, và sai lệch đó có ảnh hưởng đến câu hỏi thực tế mà ta quan tâm hay không.

Ví dụ, nếu model hơi lệch ở tail nhưng vẫn dự đoán trung bình rất tốt thì có thể nó vẫn chấp nhận được; nhưng nếu bạn đang quan tâm đến rủi ro cực đoan thì chính lỗi ở tail lại trở thành vấn đề rất nghiêm trọng.

## 9. Khi model kiểm tra không ổn, ta nên làm gì?

Không nên phản ứng máy móc kiểu “chạy sampler thêm”.

Thay vào đó, hãy nghĩ theo ba hướng lớn sau:

### 9.1. Generative story (câu chuyện sinh dữ liệu) có thiếu không?

Hãy hỏi có phi tuyến không, có interaction (tương tác) không, hay có nhóm/hierarchical structure (cấu trúc phân cấp) nào đang bị bỏ quên không.

### 9.2. Prior có vấn đề không?

Hãy xem prior có quá rộng, quá hẹp, hay prior predictive (dự báo từ prior) của nó đã thực sự hợp lý chưa.

### 9.3. Dữ liệu có gì đặc biệt không?

Hãy kiểm tra xem dữ liệu có outlier, measurement error (sai số đo lường), biến bị thiếu, hay heteroskedasticity nào đáng chú ý không.

Model checking tốt là thứ mở đường cho model revision (sửa đổi mô hình) tốt.

## 10. Một workflow (quy trình) khép kín của regression Bayes

Chapter 4 thực ra đang dạy một workflow đầy đủ: kể generative story (câu chuyện sinh dữ liệu), chọn prior có nguyên tắc, fit posterior, kiểm tra diagnostics (chẩn đoán) của sampler, kiểm tra model bằng PPC và residual, dùng posterior để dự đoán, rồi quay lại sửa mô hình nếu cần.

Nếu bạn làm đủ bảy bước này, regression không còn là “chạy một hàm”, mà là một quy trình mô hình hóa thật sự.

## 11. Những sai lầm phổ biến

### 11.1. Tin posterior mà không kiểm tra model

Posterior chỉ đáng tin nếu mô hình sinh ra posterior ấy còn hợp lý.

### 11.2. Chỉ nhìn fit trên dữ liệu cũ

Dự đoán cho dữ liệu mới mới là nơi model bộc lộ giá trị thực.

### 11.3. Chỉ làm một PPC duy nhất

Một model có thể qua một tiêu chí nhưng trượt ở tiêu chí khác. Hãy kiểm tra nhiều góc nhìn.

## 12. Điều nên giữ lại sau bài này

Regression Bayes không kết thúc ở posterior. Nó thực sự sống ở chỗ mô hình có giải thích dữ liệu hợp lý hay không, và dự đoán mà nó tạo ra có thực sự hữu ích hay không.

Nếu không có bước checking và prediction, Bayesian regression mới chỉ đi được nửa chặng đường.

> **3 ý cần nhớ.** Posterior predictive check là cách hỏi xem model có sinh ra dữ liệu giống dữ liệu thật không; residual analysis (phân tích phần dư) và prediction là hai phần quan trọng để đánh giá model có thực sự hữu ích hay không; và fit model chỉ là bước đầu vì Bayesian workflow hoàn chỉnh luôn bao gồm checking, prediction, và revision (sửa đổi) nếu cần.

## Câu hỏi tự luyện

1. Vì sao một model fit xong nhưng chưa qua PPC thì chưa nên tin hoàn toàn?
2. Sự khác nhau giữa uncertainty của mean prediction và uncertainty của một quan sát mới là gì?
3. Hãy nêu ba thứ bạn có thể so sánh giữa dữ liệu thật và dữ liệu posterior predictive.
4. Nếu residual cho thấy pattern cong rõ rệt, bạn sẽ nghi ngờ điều gì ở mô hình?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*Kết thúc Chapter 4. Bài học tiếp theo: [Chapter 5 - Multiple Predictors và Causal Thinking](/vi/chapter05/)*
