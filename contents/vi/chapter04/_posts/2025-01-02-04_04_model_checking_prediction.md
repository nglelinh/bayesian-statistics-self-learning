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

Sau bài này, bạn cần hiểu rằng fit model mới chỉ là nửa đầu của regression Bayes. Nửa còn lại là kiểm tra model có đang mô tả dữ liệu hợp lý hay không, và dùng posterior để dự đoán dữ liệu mới một cách trung thực. Bạn cũng cần nắm posterior predictive checks như công cụ trung tâm của bước này.

> **Ví dụ mini.** Một đường hồi quy có thể nhìn rất đẹp trên scatter plot, nhưng nếu nó không sinh ra dữ liệu giống dữ liệu thật thì model vẫn có vấn đề. Model checking là cách chất vấn mô hình thay vì chỉ tin vì nó đã chạy xong.
>
> **Câu hỏi tự kiểm tra.** Vì sao một posterior “trông ổn” chưa đủ để kết luận mô hình là tốt?

## 1. Fit tốt chưa chắc model tốt

Đây là một chuyển biến quan trọng trong tư duy.

Nhiều người học regression dừng lại ở:

- ước lượng slope,
- xem interval,
- rồi kết luận.

Nhưng một Bayesian workflow trưởng thành sẽ hỏi thêm:

- model này có tái tạo được dữ liệu quan sát không?
- residual có còn pattern đáng ngờ không?
- dự đoán cho dữ liệu mới có hợp lý không?

George Box có câu rất nổi tiếng:

> “All models are wrong, but some are useful.”

Mục tiêu không phải tìm model “đúng tuyệt đối”, mà là:

- model đủ hữu ích,
- đủ trung thực,
- và không bỏ sót các cấu trúc quan trọng của dữ liệu.

## 2. Posterior predictive distribution là gì?

Giả sử bạn đã có posterior của các tham số. Khi đó bạn có thể sinh dữ liệu mới $$\tilde y$$ từ model:

$$
p(\tilde y \mid y) = \int p(\tilde y \mid \theta)\,p(\theta \mid y)\,d\theta.
$$

Ý nghĩa:

- không chỉ suy luận về tham số,
- mà còn suy luận về dữ liệu tương lai hoặc dữ liệu tái tạo từ model.

Đây là cầu nối giữa:

- estimation,
- và prediction.

## 3. Posterior predictive check (PPC) là gì?

PPC hỏi một câu rất thực tế:

> Nếu model của tôi đúng, dữ liệu giả lập sinh từ model có giống dữ liệu thật không?

Quy trình:

1. lấy nhiều mẫu tham số từ posterior,
2. từ mỗi mẫu tham số, sinh dữ liệu giả,
3. so sánh dữ liệu giả với dữ liệu quan sát.

Nếu dữ liệu giả:

- có hình dạng,
- độ phân tán,
- và các pattern tương tự dữ liệu thật,

thì model có vẻ đang ổn hơn.

![Posterior predictive checks]({{ site.baseurl }}/img/chapter_img/chapter04/posterior_predictive_checks.png)

## 4. PPC nên nhìn những gì?

Không có một kiểm tra duy nhất phù hợp cho mọi bài toán. Bạn nên nhìn nhiều góc:

### 4.1. Phân phối tổng thể

Histogram hoặc density của dữ liệu giả có giống dữ liệu thật không?

### 4.2. Trung bình và độ phân tán

Model có tái hiện được:

- mean,
- variance,
- min/max hợp lý,
- hoặc tail behavior không?

### 4.3. Quan hệ giữa predictor và response

Với regression, điều rất quan trọng là:

- mô hình có tái hiện đúng pattern giữa $$x$$ và $$y$$ không?

### 4.4. Statistic chuyên biệt theo bài toán

Ví dụ:

- số outlier,
- độ lệch,
- độ bất đối xứng,
- tỷ lệ vượt ngưỡng.

## 5. Residual analysis vẫn rất quan trọng

Ngay cả trong Bayesian regression, residual vẫn là một gương soi tốt cho mô hình.

Ta thường nhìn:

- residual vs fitted,
- residual vs predictor,
- phân phối residual,
- dấu hiệu heteroskedasticity,
- dấu hiệu nonlinearity.

![Regression assumptions và diagnostics]({{ site.baseurl }}/img/chapter_img/chapter04/regression_assumptions_diagnostic.png)

Nếu residual cho thấy pattern có hệ thống, model có thể đang bỏ sót:

- phi tuyến,
- interaction,
- heteroskedasticity,
- hoặc biến quan trọng chưa đưa vào.

## 6. Prediction trong Bayes khác gì prediction điểm?

Trong regression cổ điển, nhiều người chỉ quen với:

- một giá trị dự đoán trung bình.

Bayesian prediction đi xa hơn:

- nó giữ lại bất định của tham số,
- và cả bất định do noise của quan sát mới.

Điều này cho phép bạn nói:

- không chỉ “dự đoán là 72”,
- mà còn “vùng giá trị hợp lý của dự đoán nằm ở đâu, và ta chắc đến mức nào”.

Đó là kiểu dự báo hữu ích hơn nhiều cho ra quyết định.

## 7. Prediction interval và uncertainty

Có hai nguồn bất định chính:

### 7.1. Bất định tham số

Ta chưa biết chính xác $$\alpha,\beta,\sigma$$.

### 7.2. Bất định của quan sát mới

Ngay cả nếu biết tham số hoàn hảo, quan sát mới vẫn dao động quanh đường trung bình.

Prediction interval vì vậy luôn rộng hơn uncertainty chỉ của mean response.

Đây là điều rất quan trọng khi báo cáo dự báo cho người dùng cuối.

## 8. Model checking không phải để “bắt model hoàn hảo”

Đừng hiểu model checking như trò:

- hoặc model hoàn hảo,
- hoặc vứt đi.

Nó là quá trình để hỏi:

- model đang sai ở đâu,
- sai ở mức nào,
- sai đó có ảnh hưởng tới câu hỏi thực tế mà ta quan tâm hay không.

Ví dụ:

- nếu model hơi lệch ở tail nhưng vẫn dự đoán trung bình rất tốt, có thể vẫn chấp nhận được,
- nhưng nếu bạn quan tâm rủi ro cực đoan thì lỗi ở tail lại rất nghiêm trọng.

## 9. Khi model kiểm tra không ổn, ta nên làm gì?

Không nên phản ứng máy móc kiểu “chạy sampler thêm”.

Thay vào đó, hãy nghĩ:

### 1. Generative story có thiếu không?

- có phi tuyến không?
- có interaction không?
- có nhóm/hierarchical structure không?

### 2. Prior có vấn đề không?

- quá rộng,
- quá hẹp,
- prior predictive đã hợp lý chưa?

### 3. Dữ liệu có gì đặc biệt không?

- outlier,
- measurement error,
- biến bị thiếu,
- heteroskedasticity.

Model checking tốt là thứ mở đường cho model revision tốt.

## 10. Một workflow khép kín của regression Bayes

Chapter 4 thực ra đang dạy một workflow đầy đủ:

1. kể generative story,
2. chọn prior có nguyên tắc,
3. fit posterior,
4. kiểm tra diagnostics của sampler,
5. kiểm tra model bằng PPC và residual,
6. dùng posterior để dự đoán,
7. quay lại sửa mô hình nếu cần.

Nếu bạn làm đủ bảy bước này, regression không còn là “chạy một hàm”, mà là một quy trình mô hình hóa thật sự.

## 11. Những sai lầm phổ biến

### 11.1. Tin posterior mà không kiểm tra model

Posterior chỉ đáng tin nếu mô hình sinh ra posterior ấy còn hợp lý.

### 11.2. Chỉ nhìn fit trên dữ liệu cũ

Dự đoán cho dữ liệu mới mới là nơi model bộc lộ giá trị thực.

### 11.3. Chỉ làm một PPC duy nhất

Một model có thể qua một tiêu chí nhưng trượt ở tiêu chí khác. Hãy kiểm tra nhiều góc nhìn.

## 12. Điều nên giữ lại sau bài này

Regression Bayes không kết thúc ở posterior. Nó thực sự sống ở chỗ:

- mô hình có giải thích dữ liệu hợp lý không,
- và dự đoán của nó có hữu ích không.

Nếu không có bước checking và prediction, Bayesian regression mới chỉ đi được nửa chặng đường.

> **3 ý cần nhớ.**
> 1. Posterior predictive check là cách hỏi xem model có sinh ra dữ liệu giống dữ liệu thật không.
> 2. Residual analysis và prediction là hai phần quan trọng để đánh giá model có thực sự hữu ích hay không.
> 3. Fit model chỉ là bước đầu; Bayesian workflow hoàn chỉnh luôn bao gồm checking, prediction và revision nếu cần.

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
