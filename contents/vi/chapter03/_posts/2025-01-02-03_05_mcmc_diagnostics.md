---
layout: post
title: "Bài 3.5: MCMC Diagnostics - Đảm bảo Chất lượng Mẫu"
chapter: '03'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu vì sao MCMC diagnostics là bước bắt buộc chứ không phải phần phụ. Bạn cũng cần đọc được những công cụ chẩn đoán quan trọng như trace plot, R-hat, ESS và autocorrelation, đồng thời hiểu các tín hiệu phổ biến của convergence kém, mixing kém và chain chưa đáng tin.

> **Ví dụ mini.** Bạn chạy MCMC được 10,000 mẫu và thấy histogram trông rất đẹp. Nhưng nếu chuỗi chưa hội tụ, histogram đẹp đó vẫn có thể đánh lừa bạn. Diagnostics là cách kiểm tra xem các mẫu ấy có thật sự đại diện cho posterior hay chưa.
>
> **Câu hỏi tự kiểm tra.** Vì sao “có rất nhiều mẫu” không tự động đồng nghĩa với “mẫu đáng tin”?

## 1. Tại sao diagnostics lại quan trọng đến vậy?

MCMC không cho bạn mẫu độc lập hoàn hảo. Nó cho bạn:

- một chuỗi phụ thuộc,
- cần thời gian warm-up,
- có thể bị kẹt,
- có thể trộn kém,
- và đôi khi có thể thất bại mà nhìn qua vẫn tưởng ổn.

Vì vậy, nếu bỏ qua diagnostics, bạn có nguy cơ:

- báo cáo posterior sai,
- tin vào khoảng bất định không đáng tin,
- và đưa ra quyết định dựa trên mẫu kém chất lượng.

Nói cách khác:

**không có diagnostics, MCMC chỉ là niềm tin mù quáng vào sampler.**

## 2. Trace plot: công cụ đơn giản nhưng cực mạnh

Trace plot vẽ giá trị tham số theo iteration.

Một trace plot tốt thường trông như:

- một “con sâu bướm lông xù”,
- dao động quanh vùng ổn định,
- không có xu hướng tăng giảm rõ,
- không bị đứng yên quá lâu.

![MCMC diagnostics: good vs bad traces]({{ site.baseurl }}/img/chapter_img/chapter03/mcmc_diagnostics.png)

### Dấu hiệu tốt

- chain dao động quanh một vùng ổn định,
- không có drift dài,
- nhiều chain chồng lên nhau khá tốt.

### Dấu hiệu xấu

- chain có xu hướng trôi dần,
- chain bị kẹt trong một vùng,
- các chain bắt đầu từ các điểm khác nhau nhưng không gặp nhau,
- hoặc chuỗi đứng yên quá thường xuyên.

## 3. Mixing là gì, và vì sao nó quan trọng?

Mixing tốt nghĩa là chuỗi:

- di chuyển đủ qua các vùng hợp lý của posterior,
- không bị kẹt cục bộ,
- và không lặp lại thông tin quá nhiều lần.

Mixing kém nghĩa là:

- dù iteration nhiều,
- thông tin thật sự thu được không nhiều.

![Chất lượng mixing của chain]({{ site.baseurl }}/img/chapter_img/chapter03/chain_mixing_quality.png)

Đây là lý do bạn có thể có:

- 10,000 draws trên giấy tờ,
- nhưng “giá trị thực dụng” chỉ tương đương vài trăm mẫu độc lập.

## 4. Autocorrelation: vấn đề của chuỗi phụ thuộc

Mẫu MCMC gần nhau theo thời gian thường giống nhau hơn mẫu độc lập. Đó là autocorrelation.

Autocorrelation cao nghĩa là:

- chain đi quá chậm,
- mỗi mẫu mới không thêm nhiều thông tin mới,
- và hiệu suất thống kê giảm.

![Effective sample size và autocorrelation]({{ site.baseurl }}/img/chapter_img/chapter03/effective_sample_size_autocorrelation.png)

Trực giác:

- nếu 100 mẫu liên tiếp gần như giống nhau,
- thì không thể xem chúng như 100 quan sát độc lập thật sự.

## 5. Effective Sample Size (ESS)

Để phản ánh chuyện đó, ta dùng **effective sample size**.

ESS trả lời:

> Chuỗi hiện tại, dù có bao nhiêu draw danh nghĩa, tương đương với bao nhiêu mẫu độc lập thật sự?

Nếu:

- draws nhiều nhưng autocorrelation cao,

thì ESS có thể thấp đáng kể.

ESS cao là dấu hiệu tốt vì:

- thông tin hữu ích trên mỗi mẫu tốt hơn,
- ước lượng mean, quantile, interval ổn định hơn.

## 6. R-hat: các chain có thực sự hội tụ cùng một nơi chưa?

R-hat là một diagnostic rất quan trọng trong workflow hiện đại.

Ý tưởng:

- chạy nhiều chain từ các điểm khởi đầu khác nhau,
- xem biến thiên giữa các chain và trong từng chain có đồng nhất chưa.

Nếu các chain đều đang cùng phản ánh một posterior ổn định, thì:

- R-hat sẽ gần 1.

Trong thực hành:

- R-hat càng gần 1 càng tốt,
- giá trị lệch đáng kể khỏi 1 là tín hiệu cần chú ý.

![Convergence diagnostics]({{ site.baseurl }}/img/chapter_img/chapter03/convergence_diagnostics.png)

## 7. Một workflow đọc diagnostics nên bắt đầu thế nào?

Thay vì chỉ nhìn một con số, bạn nên đi theo thứ tự:

### 1. Nhìn trace plot

Chuỗi có trông ổn không?

### 2. Nhìn R-hat

Các chain đã thật sự đồng thuận chưa?

### 3. Nhìn ESS

Số mẫu hiệu quả có đủ chưa?

### 4. Nhìn autocorrelation

Chuỗi có đang dính nhau quá mạnh không?

### 5. Nếu dùng HMC/NUTS, nhìn thêm các cảnh báo chuyên biệt

Ví dụ:

- divergence,
- energy problems,
- tree depth warnings.

## 8. Các vấn đề phổ biến và cách nghĩ về nguyên nhân

### 8.1. Chain có trend dài

Khả năng:

- chưa warm-up đủ,
- posterior khó,
- chain bắt đầu quá xa.

### 8.2. Chain bị kẹt

Khả năng:

- proposal kém,
- posterior nhiều vùng tách biệt,
- sampler di chuyển quá chậm.

### 8.3. R-hat cao

Khả năng:

- nhiều chain chưa gặp nhau,
- có multimodality,
- hoặc sampler chưa hội tụ.

### 8.4. ESS thấp

Khả năng:

- autocorrelation cao,
- sampler đi quá chậm,
- nhiều draw nhưng thông tin lặp lại nhiều.

## 9. Diagnostics không phải để “trang trí báo cáo”

Nhiều người mới học có xu hướng:

- fit model,
- lấy mean posterior,
- vẽ một histogram đẹp,
- rồi coi như xong.

Đó là một thói quen nguy hiểm.

Diagnostics không phải đồ phụ thêm ở cuối. Nó là bước để trả lời:

- liệu ta có quyền tin vào các mẫu này chưa?

Nếu diagnostics báo xấu, việc diễn giải posterior ngay lúc đó có thể là quá sớm.

## 10. Khi diagnostics xấu, nên nghĩ gì trước?

Thay vì chỉ cố “chạy thêm lâu hơn”, hãy nghĩ theo các lớp nguyên nhân:

### Lớp 1. Sampler

- step size,
- warm-up,
- algorithm choice.

### Lớp 2. Parametrization

- mô hình có thể cần reparameterization,
- chuẩn hóa biến đầu vào,
- non-centered parameterization.

### Lớp 3. Bản thân mô hình

- posterior có quá phức tạp không,
- prior có quá rộng hay quá lạ không,
- mô hình có nhận diện kém không.

Điều này rất quan trọng: diagnostics xấu không chỉ là lỗi “máy chạy chưa đủ”, mà đôi khi là tín hiệu mô hình chưa ổn.

## 11. Một thói quen chuyên nghiệp nên có

Sau mỗi lần fit model, hãy tự hỏi:

- trace plot có ổn không?
- R-hat đã gần 1 chưa?
- ESS có đủ không?
- autocorrelation có quá cao không?
- sampler có cảnh báo gì không?

Khi làm Bayesian nghiêm túc, đây không phải checklist tùy chọn. Đây là phần của workflow bắt buộc.

> **3 ý cần nhớ.**
> 1. Nhiều mẫu chưa chắc là nhiều thông tin nếu chain hội tụ kém hoặc autocorrelation cao.
> 2. Trace plot, R-hat và ESS là ba diagnostics cốt lõi cần kiểm tra gần như mọi lần chạy MCMC.
> 3. Diagnostics xấu không chỉ đòi hỏi chạy lâu hơn; đôi khi nó báo rằng sampler, cách tham số hóa hoặc chính mô hình đang có vấn đề.

## Câu hỏi tự luyện

1. Vì sao trace plot đẹp là điều cần nhưng chưa đủ?
2. Hãy giải thích ESS bằng lời theo cách dễ hiểu với người mới học.
3. R-hat đang cố kiểm tra điều gì khi ta chạy nhiều chain?
4. Nếu chain bị autocorrelation rất cao, điều đó ảnh hưởng thế nào đến chất lượng suy luận posterior?

## Tài liệu tham khảo

- Vehtari et al. Rank-normalization, folding, and localization: an improved R-hat.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 11.
- ArviZ documentation on diagnostics.

---

*Bài học tiếp theo: [3.6 PyMC - Bayesian Modeling trong Thực tế](/vi/chapter03/pymc-implementation/)*
