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

Sau bài này, bạn cần biết cách biến regression Bayes từ generative story (câu chuyện sinh dữ liệu) thành model chạy được trong PyMC. Bạn cũng cần hiểu một workflow (quy trình làm việc) thực hành cơ bản: chuẩn hóa dữ liệu, viết prior, khai báo likelihood (hàm hợp lý), lấy mẫu posterior, đọc diagnostics (chẩn đoán) và diễn giải kết quả.

> **Ví dụ mini.** Sau khi đã hiểu generative story và biết chọn prior hợp lý, bước tiếp theo là viết model thật trong PyMC để lấy posterior của intercept (hệ số chặn), slope (hệ số dốc) và noise (độ nhiễu). PyMC không thay bạn nghĩ mô hình; nó giúp bạn triển khai mô hình ấy hiệu quả hơn.
>
> **Câu hỏi tự kiểm tra.** Nếu PyMC đã chạy được posterior rồi, vì sao ta vẫn phải nhìn diagnostics trước khi diễn giải kết quả?

## 1. Từ mô hình trên giấy sang mô hình trong code

Ở bài 4.1 và 4.2, ta đã có đủ ba thành phần: generative story (câu chuyện sinh dữ liệu), prior cho các tham số, và trực giác về regression Bayes.

Bài này chủ yếu làm một bước dịch rất thực tế: chuyển từ suy nghĩ thống kê sang một mô hình có thể chạy được trong PyMC.

Workflow tối thiểu ở đây là chuẩn bị dữ liệu, chuẩn hóa nếu cần, khai báo prior, khai báo likelihood, chạy sampler (bộ lấy mẫu), kiểm tra diagnostics (chẩn đoán), rồi mới đọc posterior.

## 2. Một regression Bayes đơn giản trong PyMC có cấu trúc ra sao?

Tư duy đúng là luôn bắt đầu từ prior cho $$\alpha$$, prior cho $$\beta$$, prior cho $$\sigma$$, rồi mới đi đến likelihood:

$$
y_i \sim \mathcal{N}(\alpha + \beta x_i,\sigma).
$$

Trong PyMC, bạn chỉ đang viết lại câu chuyện đó bằng code.

Điều quan trọng là code nên phản ánh mô hình, chứ không phải mô hình bị bóp méo chỉ để khớp với một API cụ thể.

## 3. Vì sao nên chuẩn hóa dữ liệu trước khi fit?

Regression Bayes thường chạy ổn hơn khi biến được scale tốt.

Lợi ích của việc chuẩn hóa là prior dễ chọn hơn, intercept dễ diễn giải hơn, sampler thường hội tụ ổn hơn, và posterior cũng ít bị “méo vì đơn vị đo” hơn.

Vì vậy, trong rất nhiều trường hợp, chuẩn hóa là một bước thực hành nên có.

## 4. Sau khi chạy mẫu, ta đọc gì đầu tiên?

Nhiều người mới học hay nhảy thẳng vào posterior mean và interval. Nhưng thứ nên nhìn đầu tiên thực ra là diagnostics, nghĩa là trace plot (đồ thị vệt mẫu) có ổn không, R-hat có gần 1 không, ESS (số mẫu hiệu dụng) có đủ không, và sampler có phát ra warning (cảnh báo) gì không.

Nếu phần này chưa tốt, mọi diễn giải posterior sau đó đều nên được xem là tạm thời.

## 5. Diễn giải posterior trong regression

Khi model chạy ổn, ta mới quay lại các câu hỏi thống kê.

### 5.1. Intercept

Với dữ liệu đã standardize (chuẩn hóa) hoặc centered (đưa về quanh trung tâm), intercept thường dễ đọc hơn vì nó mô tả giá trị trung bình của $$y$$ khi $$x$$ ở mức trung tâm.

### 5.2. Slope

Posterior của slope cho biết mối quan hệ đang dương hay âm, mạnh hay yếu, và ta chắc đến đâu về điều đó. Điểm hay của Bayes là bạn có thể hỏi trực tiếp xác suất $$\beta > 0$$ là bao nhiêu.

### 5.3. Noise

Posterior của $$\sigma$$ cho biết mức độ dữ liệu phân tán quanh đường hồi quy, tức là model còn bỏ lại bao nhiêu biến thiên chưa giải thích.

### 5.4. Ví dụ Session 7: cập nhật từ prior sang posterior cho tham số hồi quy

Giả sử sau khi fit mô hình tuyến tính một biến với PyMC, ta thu được tóm tắt sau:

- Prior: $$\alpha\sim\mathcal N(60,20),\;\beta\sim\mathcal N(0,2),\;\sigma\sim\text{HalfNormal}(5)$$.
- Posterior summary:
  - $$\alpha\mid D\approx \mathcal N(63.2,\,1.1^2)$$
  - $$\beta\mid D\approx \mathcal N(0.78,\,0.09^2)$$
  - $$\sigma\mid D$$ có trung bình hậu nghiệm khoảng $$2.4$$.

Diễn giải nhanh theo tinh thần Buổi 7:

- dữ liệu đã kéo intercept từ vùng prior quanh 60 lên khoảng 63.2,
- slope dương rõ rệt với bất định nhỏ (SD 0.09),
- độ nhiễu còn lại khoảng 2.4 đơn vị phản hồi.

Nếu cần khoảng hậu nghiệm gần 95% cho slope (xấp xỉ Normal):

$$
0.78\pm 1.96\times 0.09\Rightarrow [0.604,\;0.956].
$$

Khoảng này không cắt 0, nên bằng chứng hậu nghiệm ủng hộ quan hệ dương khá rõ.

## 6. Từ posterior tham số tới dự đoán

Regression Bayes không chỉ để biết slope là bao nhiêu. Nó còn để dự đoán. Chẳng hạn, với một giá trị $$x$$ mới, ta muốn biết cân nặng hoặc điểm thi dự đoán sẽ ở đâu, và khoảng bất định đi kèm với dự đoán đó rộng đến mức nào.

Đây là nơi PyMC rất tiện, vì sau khi đã có posterior draws (các mẫu rút ra từ posterior), ta có thể chuyển thẳng sang posterior predictive (dự báo hậu nghiệm) tương đối tự nhiên.

## 7. Một workflow tối thiểu lành mạnh khi dùng PyMC cho regression

Bạn có thể ghi nhớ workflow (quy trình) này như ba chặng nối tiếp nhau, trong đó mỗi chặng đều có một câu hỏi trung tâm cần được trả lời rõ ràng trước khi sang bước kế tiếp:

### Trước khi chạy

Trước khi chạy, hãy hỏi biến có cần chuẩn hóa không, prior có hợp lý theo đúng thang đo dữ liệu không, và generative story đã thật sự rõ chưa.

### Trong khi chạy

Trong khi chạy, hãy để ý sampler có cảnh báo gì không và giai đoạn warm-up (làm nóng) có đủ hay chưa.

### Sau khi chạy

Sau khi chạy, hãy xem trace plot có ổn không, R-hat và ESS có tốt không, posterior của tham số đang nói gì, và posterior predictive có hợp lý hay không.

### Ghi chú cho bối cảnh biết/không biết phương sai

Trong thực hành PyMC, ta thường suy luận cả $$\sigma$$ nên interval của slope đã phản ánh bất định về nhiễu. Nếu bạn cố định $$\sigma$$ từ trước (bài toán đặc thù), interval cho slope thường hẹp hơn. Khi báo cáo kết quả, nên nêu rõ bạn đang ở kịch bản nào.

## 8. Những lỗi phổ biến của người mới dùng PyMC cho regression

### 8.1. Xem PyMC như hộp đen

Đây là lỗi lớn nhất.

Nếu không hiểu mô hình, bạn sẽ không biết prior đang nói gì, warning đang báo điều gì, và posterior có thật sự đáng tin hay không.

### 8.2. Chỉ đọc posterior mean

Posterior mean là chưa đủ. Bạn cần xem interval (khoảng bất định), xác suất vượt ngưỡng, hình dạng posterior, và cả prediction uncertainty (bất định dự đoán).

### 8.3. Quên model checking

Regression fit xong chưa phải là xong. Bài sau sẽ nhấn mạnh posterior predictive checks (kiểm tra dự báo hậu nghiệm), residual analysis (phân tích phần dư), và prediction quality (chất lượng dự đoán).

## 9. Điều bài này muốn bạn giữ lại

Mục tiêu không phải là nhớ từng dòng API PyMC. Mục tiêu là nhìn thấy regression Bayes có thể được triển khai rất tự nhiên miễn là bạn giữ đúng workflow tư duy. PyMC chỉ là công cụ; phần quan trọng nhất vẫn là câu chuyện mô hình, prior, diagnostics, và cách diễn giải posterior.

> **3 ý cần nhớ.** PyMC giúp triển khai regression Bayes theo đúng cấu trúc prior + likelihood + posterior mà bạn đã học; sau khi fit model, diagnostics luôn phải đi trước việc diễn giải posterior; và giá trị thật của posterior inference không chỉ nằm ở ước lượng tham số mà còn ở khả năng chuyển sang dự đoán và kiểm tra mô hình.

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
