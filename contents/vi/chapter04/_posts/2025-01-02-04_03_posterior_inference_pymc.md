---
layout: post
title: "Bài 4.3: Posterior Inference với PyMC - Từ Theory đến Practice"
chapter: '04'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần biết cách biến regression Bayes từ generative story thành model chạy được trong PyMC. Bạn cũng cần hiểu một workflow thực hành cơ bản: chuẩn hóa dữ liệu, viết prior, khai báo likelihood, lấy mẫu posterior, đọc diagnostics và diễn giải kết quả.

> **Ví dụ mini.** Sau khi đã hiểu generative story và biết chọn prior hợp lý, bước tiếp theo là viết model thật trong PyMC để lấy posterior của intercept, slope và noise. PyMC không thay bạn nghĩ mô hình; nó giúp bạn triển khai mô hình ấy hiệu quả hơn.
>
> **Câu hỏi tự kiểm tra.** Nếu PyMC đã chạy được posterior rồi, vì sao ta vẫn phải nhìn diagnostics trước khi diễn giải kết quả?

## 1. Từ mô hình trên giấy sang mô hình trong code

Ở bài 4.1 và 4.2, ta đã có đủ ba thành phần:

- generative story,
- prior cho các tham số,
- và trực giác về regression Bayes.

Bài này chỉ làm bước dịch:

- từ suy nghĩ thống kê
- sang mô hình có thể chạy trong PyMC.

Workflow tối thiểu là:

1. chuẩn bị dữ liệu,
2. chuẩn hóa nếu cần,
3. khai báo prior,
4. khai báo likelihood,
5. chạy sampler,
6. kiểm tra diagnostics,
7. đọc posterior.

## 2. Một regression Bayes đơn giản trong PyMC có cấu trúc ra sao?

Tư duy đúng là:

- prior cho $$\alpha$$,
- prior cho $$\beta$$,
- prior cho $$\sigma$$,
- rồi likelihood:

$$
y_i \sim \mathcal{N}(\alpha + \beta x_i,\sigma).
$$

Trong PyMC, bạn chỉ đang viết lại câu chuyện đó bằng code.

Điều quan trọng là:

- code nên phản ánh mô hình,
- không phải mô hình bị bóp méo để khớp một API.

## 3. Vì sao nên chuẩn hóa dữ liệu trước khi fit?

Regression Bayes thường chạy ổn hơn khi biến được scale tốt.

Lợi ích:

- prior dễ chọn,
- intercept dễ diễn giải,
- sampler thường hội tụ ổn hơn,
- posterior ít “méo vì đơn vị đo”.

Vì vậy, trong rất nhiều trường hợp, chuẩn hóa là một bước thực hành nên có.

## 4. Sau khi chạy mẫu, ta đọc gì đầu tiên?

Nhiều người mới học hay nhảy thẳng vào posterior mean và interval. Nhưng thứ nên nhìn đầu tiên là:

- diagnostics.

Tức là:

- trace plot có ổn không,
- R-hat có gần 1 không,
- ESS có đủ không,
- sampler có warning gì không.

Nếu phần này chưa tốt, mọi diễn giải posterior sau đó đều nên được xem là tạm thời.

## 5. Diễn giải posterior trong regression

Khi model chạy ổn, ta mới quay lại các câu hỏi thống kê.

### 5.1. Intercept

Với dữ liệu đã standardize hoặc centered, intercept thường dễ đọc hơn:

- nó mô tả giá trị trung bình của $$y$$ khi $$x$$ ở mức trung tâm.

### 5.2. Slope

Posterior của slope cho biết:

- mối quan hệ dương hay âm,
- mạnh hay yếu,
- và ta chắc đến đâu về điều đó.

Điểm hay của Bayes là bạn có thể hỏi trực tiếp:

- xác suất $$\beta > 0$$ là bao nhiêu?

### 5.3. Noise

Posterior của $$\sigma$$ cho biết:

- mức độ dữ liệu phân tán quanh đường hồi quy,
- tức là model còn bỏ lại bao nhiêu biến thiên chưa giải thích.

## 6. Từ posterior tham số tới dự đoán

Regression Bayes không chỉ để biết slope là bao nhiêu. Nó còn để dự đoán.

Ví dụ:

- với một giá trị $$x$$ mới,
- cân nặng hoặc điểm thi dự đoán sẽ ở đâu,
- và khoảng bất định là bao nhiêu.

Đây là nơi PyMC rất tiện:

- sau khi đã có posterior draws,
- ta có thể chuyển thẳng sang posterior predictive.

## 7. Một workflow tối thiểu lành mạnh khi dùng PyMC cho regression

Bạn có thể nhớ theo checklist sau:

### Trước khi chạy

- biến có cần chuẩn hóa không?
- prior có hợp lý theo thang đo không?
- generative story đã rõ chưa?

### Trong khi chạy

- sampler có cảnh báo gì không?
- warm-up có đủ không?

### Sau khi chạy

- trace plot có ổn không?
- R-hat và ESS có tốt không?
- posterior của tham số nói gì?
- posterior predictive có hợp lý không?

## 8. Những lỗi phổ biến của người mới dùng PyMC cho regression

### 8.1. Xem PyMC như hộp đen

Đây là lỗi lớn nhất.

Nếu không hiểu mô hình, bạn sẽ không biết:

- prior đang nói gì,
- warning đang báo gì,
- posterior có đáng tin không.

### 8.2. Chỉ đọc posterior mean

Posterior mean là chưa đủ. Bạn cần xem:

- interval,
- xác suất vượt ngưỡng,
- hình dạng posterior,
- và prediction uncertainty.

### 8.3. Quên model checking

Regression fit xong chưa phải là xong. Bài sau sẽ nhấn mạnh:

- posterior predictive checks,
- residual analysis,
- prediction quality.

## 9. Điều bài này muốn bạn giữ lại

Mục tiêu không phải là nhớ từng dòng API PyMC. Mục tiêu là:

- nhìn thấy regression Bayes có thể được triển khai rất tự nhiên,
- miễn là bạn giữ đúng workflow tư duy.

PyMC chỉ là công cụ. Phần quan trọng nhất vẫn là:

- câu chuyện mô hình,
- prior,
- diagnostics,
- và cách diễn giải posterior.

> **3 ý cần nhớ.**
> 1. PyMC giúp triển khai regression Bayes theo đúng cấu trúc prior + likelihood + posterior mà bạn đã học.
> 2. Sau khi fit model, diagnostics luôn phải đi trước việc diễn giải posterior.
> 3. Giá trị thật của posterior inference không chỉ là ước lượng tham số, mà còn là khả năng chuyển sang dự đoán và kiểm tra mô hình.

## Câu hỏi tự luyện

1. Hãy liệt kê 5 bước tối thiểu của một workflow regression Bayes với PyMC.
2. Vì sao chuẩn hóa dữ liệu thường giúp cả prior selection lẫn sampling?
3. Nếu posterior của slope trông hợp lý nhưng R-hat chưa tốt, bạn nên làm gì?
4. Trong regression Bayes, tại sao prediction là phần quan trọng không kém estimation?

## Tài liệu tham khảo

- PyMC Documentation.
- ArviZ Documentation.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4-5.

---

*Bài học tiếp theo: [4.4 Model Checking và Prediction - Đảm bảo Model Tốt](/vi/chapter04/model-checking-prediction/)*
