---
layout: post
title: "Bài 4.5: Case Study Model Checking & Prediction - Đi Trọn Workflow Trên Một Dataset"
chapter: '04'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần làm được một workflow (quy trình) đầy đủ và có chiều sâu trên một dataset cụ thể: xây mô hình Bayes, đánh giá chất lượng sampling, kiểm tra model bằng posterior predictive checks (PPC), phân tích residual (phần dư), báo cáo prediction (dự đoán) đúng loại bất định, và đề xuất model revision (sửa mô hình) dựa trên bằng chứng.

> **Ví dụ mini.** Bạn dự đoán tiền tip từ tổng hóa đơn trong dữ liệu nhà hàng. Model tuyến tính có thể cho slope rất đẹp, nhưng câu hỏi thực chiến là: model đó có thực sự sinh ra dữ liệu giống thực tế và dự đoán đáng tin cho khách mới hay không?
>
> **Câu hỏi tự kiểm tra.** Nếu slope hậu nghiệm dương rõ rệt nhưng PPC thất bại ở vùng hóa đơn lớn, bạn nên tin điều gì?

## 1. Dataset cụ thể: `tips` (seaborn)

Ta dùng dataset `tips`, trong đó:

- `total_bill`: tổng hóa đơn,
- `tip`: tiền tip,
- mỗi dòng là một bàn ăn.

Mục tiêu chính: mô hình hóa và dự đoán `tip` theo `total_bill`.

Mục tiêu phụ: kiểm tra xem một mô hình tuyến tính Gaussian cơ sở có đủ tốt hay không, thay vì mặc định tin vào slope hậu nghiệm.

Lý do dataset này phù hợp cho bài 4.5 là nó đủ nhỏ để đọc trực giác, nhưng đủ thực tế để thấy các vấn đề model checking: có thể phi tuyến nhẹ, phương sai tăng theo mức hóa đơn, và tail behavior (hành vi đuôi phân phối) không hoàn toàn lý tưởng cho Normal đơn giản.

### 1.1. Xem nhanh một phần dữ liệu

Bảng dưới là 5 dòng đầu của dataset `tips` để bạn có cảm giác trực quan về dữ liệu:

| total_bill | tip | sex | smoker | day | time | size |
|---:|---:|---|---|---|---|---:|
| 16.99 | 1.01 | Female | No | Sun | Dinner | 2 |
| 10.34 | 1.66 | Male | No | Sun | Dinner | 3 |
| 21.01 | 3.50 | Male | No | Sun | Dinner | 3 |
| 23.68 | 3.31 | Male | No | Sun | Dinner | 2 |
| 24.59 | 3.61 | Female | No | Sun | Dinner | 4 |

### 1.2. Tóm tắt dữ liệu trước khi modeling

Trên toàn bộ 244 quan sát:

- `total_bill`: trung bình khoảng 19.79, độ lệch chuẩn khoảng 8.90, min 3.07, max 50.81,
- `tip`: trung bình khoảng 3.00, độ lệch chuẩn khoảng 1.38, min 1.00, max 10.00,
- tương quan tuyến tính giữa `total_bill` và `tip` khoảng 0.676 (dương, mức vừa đến khá).

Điểm quan trọng cho bước checking sau này:

- chỉ khoảng 2.9% quan sát có `tip > 6`,
- nhưng đây lại là vùng quyết định hành vi đuôi (tail behavior), nơi mô hình tuyến tính Gaussian thường dễ sai.

Làm rõ luận điểm này:

- **Vì sao 2.9% vẫn quan trọng?** Trong bài toán dự báo, lỗi ở đuôi thường gắn với các trường hợp có ảnh hưởng lớn (hóa đơn lớn, tip lớn). Dù hiếm, các điểm này quyết định chất lượng dự báo ở kịch bản rủi ro hoặc giá trị cao.
- **Vì sao mô hình Gaussian tuyến tính dễ sai ở đuôi?** Mô hình cơ sở giả định sai số đối xứng và có một độ nhiễu chung $$\sigma$$ cho mọi mức `total_bill`. Thực tế dữ liệu dịch vụ thường có phương sai tăng theo mức hóa đơn, nên đuôi phải có thể dày hơn dự đoán của Normal đơn giản.
- **Hệ quả nếu bỏ qua vùng đuôi:** mô hình có thể vẫn khớp mean tốt nhưng đánh giá thấp xác suất tip rất cao, làm prediction interval ở vùng hóa đơn lớn bị hẹp giả tạo.
- **Cách kiểm tra đúng trong PPC:** ngoài mean/variance, nên kiểm tra thêm statistic theo đuôi, ví dụ

$$
T(y)=\mathbf 1(y>6),\quad T(y)=\max(y),\quad T(y)=Q_{0.95}(y).
$$

Nếu $$T(y_{obs})$$ nằm ở rìa hoặc ngoài phân phối $$T(y_{rep})$$, đó là dấu hiệu model chưa tái tạo được tail behavior.

### 1.3. Diễn giải các kết quả lập luận bằng công thức

Để tránh kiểu kết luận "nhìn hình rồi đoán", ta ghi rõ công thức phía sau các nhận định quan trọng.

Hệ số tương quan tuyến tính mẫu (Pearson) giữa `total_bill` và `tip` được tính bởi:

$$
r_{xy}=\frac{\sum_{i=1}^{n}(x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_{i=1}^{n}(x_i-\bar x)^2}\sqrt{\sum_{i=1}^{n}(y_i-\bar y)^2}}.
$$

Với dataset này, $$r_{xy}\approx 0.676$$, nên ta có hai kết luận tách bạch:

- dấu dương: hóa đơn tăng thì tip có xu hướng tăng,
- độ lớn khoảng 0.68: quan hệ tuyến tính ở mức vừa đến khá, không yếu nhưng cũng chưa phải gần hoàn hảo.

Tỷ lệ vùng đuôi phải (`tip > 6`) được tính bởi:

$$
\hat p_{\text{tip}>6}=\frac{1}{n}\sum_{i=1}^{n}\mathbf 1(y_i>6),
$$

và cho giá trị khoảng 0.029 (2.9%). Vì tỷ lệ này nhỏ, mọi kết luận về tail phải được kiểm tra bằng PPC thay vì chỉ nhìn mean.

Một liên hệ nhanh để đọc mức giải thích tuyến tính là:

$$
R^2 \approx r_{xy}^2.
$$

Do đó, với $$r_{xy}\approx 0.676$$ thì $$R^2\approx 0.46$$, nghĩa là mô hình tuyến tính mới giải thích khoảng 46% biến thiên của `tip`. Đây là lý do ta phải tiếp tục model checking và residual analysis.

Cuối cùng, để nhận diện nhanh heteroskedasticity, ta nhìn tương quan giữa độ lớn residual và predictor:

$$
\operatorname{corr}(|e_i|,x_i), \quad e_i=y_i-\hat y_i.
$$

Nếu chỉ báo này dương đáng kể, biên độ sai số có xu hướng tăng theo `total_bill`, và giả định sai số đồng nhất cần được xem xét lại.

## 2. Bước 1 - Viết generative story và fit model cơ sở

Model cơ sở (baseline) của case study:

$$
\text{tip}_i \sim \mathcal{N}(\mu_i, \sigma), \quad \mu_i = \alpha + \beta\,x_i,
$$

với $$x_i$$ là `total_bill` đã chuẩn hóa.

Diễn giải generative story:

- mỗi bàn ăn có một kỳ vọng tip phụ thuộc tuyến tính vào mức hóa đơn,
- quanh kỳ vọng đó, tip dao động với một độ nhiễu chung $$\sigma$$,
- prior nên đủ regularize để tránh overfit ở vùng dữ liệu thưa (hóa đơn rất lớn).

Kết quả fit tuyến tính thường cho slope dương rõ rệt. Tuy nhiên, ở bài này ta coi đó chỉ là điểm xuất phát, không phải kết luận cuối.

## 3. Bước 2 - Kiểm tra sampler diagnostics trước khi nói về ý nghĩa

Trước khi diễn giải slope/intercept, cần xem:

- trace plot có trộn tốt không,
- `r_hat` có gần 1 không,
- ESS có đủ lớn không,
- có warning về divergence hoặc sampling pathologies không.

Nếu diagnostics không ổn, các kết luận về posterior và prediction đều chưa đáng tin.

Mốc thực hành nên bám:

- `r_hat` tiệm cận 1.00 cho các tham số chính,
- ESS đủ lớn để ước lượng ổn định tail quantiles,
- không có divergence có hệ thống.

Lý do cần nghiêm túc bước này: PPC tốt/xấu chỉ có ý nghĩa khi posterior samples đã đáng tin.

## 4. Bước 3 - Posterior predictive distribution và PPC

Theo bài 4.4, ta dùng:

$$
p(\tilde y \mid y)=\int p(\tilde y \mid \theta)\,p(\theta\mid y)\,d\theta.
$$

Trong ngữ cảnh dataset `tips`, câu hỏi PPC là:

> Nếu model cơ sở đúng, dữ liệu tip giả lập có giống dữ liệu tip thật ở cả vùng trung tâm lẫn vùng đuôi không?

### 4.1. So sánh phân phối tổng thể

So `y` quan sát với `y_rep` từ posterior predictive:

- histogram/density có trùng nhau tương đối không,
- đuôi phải (tip rất cao) có bị model đánh giá quá thấp không,
- min/max mô phỏng có hợp lý không.

![Hình 2 - So sánh quan sát và posterior predictive trên toàn phân phối]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_observed_vs_predicted.png)

### 4.2. So sánh mean, variance, và statistic chuyên biệt

Tính statistic trên dữ liệu thật và trên từng mẫu giả lập:

- mean,
- variance,
- tỷ lệ tip vượt ngưỡng (ví dụ `tip > 6`).

Nếu giá trị quan sát rơi ở rìa quá xa so với phân phối posterior predictive của statistic, model đang thiếu một phần cấu trúc dữ liệu.

![Hình 3 - Kiểm tra mean bằng posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_test_stat_mean.png)

![Hình 4 - Kiểm tra variance bằng posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_variance_check.png)

Trong case `tips`, mô hình cơ sở thường tái tạo mean khá ổn nhưng dễ lệch ở variance vùng hóa đơn lớn. Điều này là tín hiệu sớm của heteroskedasticity.

### 4.3. So sánh quan hệ `x -> y`

Với regression, quan trọng nhất là hình dạng quan hệ:

- vẽ nhiều đường/regression draws từ posterior predictive trên scatter thật,
- xem model có dự đoán quá lạc quan ở vùng `total_bill` lớn không,
- xem độ rộng dự báo có tăng theo `x` hay không.

Đây thường là nơi phát hiện nonlinearity hoặc heteroskedasticity sớm nhất.

![Hình 5 - So sánh quan hệ predictor-response giữa dữ liệu thật và mẫu posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_distribution_at_x5.png)

## 5. Bước 4 - Residual analysis để tìm sai lệch có hệ thống

Residual chuẩn hóa đơn giản:

$$
r_i = y_i - \mathbb{E}[y_i \mid y].
$$

Nên xem ít nhất ba đồ thị:

- residual vs fitted,
- residual vs `total_bill`,
- Q-Q plot của residual.

Dấu hiệu cần chú ý:

- pattern cong: gợi ý quan hệ phi tuyến,
- dạng quạt: gợi ý phương sai thay đổi,
- tail lệch mạnh trên Q-Q: gợi ý giả định Normal có thể quá đơn giản.

Trong case `tips`, một tín hiệu hay gặp là biên độ residual tăng theo `total_bill`. Đây là lý do mô hình sai số đồng nhất (homoskedastic) có thể chưa đủ tốt.

![Hình 6 - Residual distribution: quan sát so với posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_residual_distribution.png)

![Hình 7 - Residuals vs fitted để nhận diện pattern hệ thống]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_residuals.png)

## 6. Bước 5 - Prediction cho trường hợp cụ thể

Giả sử dự đoán cho bàn ăn mới có `total_bill = 40`.

Bạn nên báo cáo **hai loại bất định**:

1. khoảng hậu nghiệm của mean tip tại mức hóa đơn đó,
2. prediction interval cho một bàn cụ thể mới.

Ví dụ diễn giải:

- mean tip ở mức hóa đơn 40 có thể quanh 5.8 đến 6.5,
- nhưng một bàn cụ thể có thể rộng hơn, ví dụ 3.8 đến 8.7.

Khoảng thứ hai rộng hơn vì nó cộng cả bất định tham số và nhiễu cá thể mới.

Điểm báo cáo quan trọng cho ra quyết định:

- nếu mục tiêu là planning doanh thu trung bình, dùng khoảng của mean response,
- nếu mục tiêu là rủi ro một giao dịch cụ thể, dùng prediction interval.

## 7. Bước 6 - Khi check không ổn: sửa model có nguyên nhân

Giả sử PPC và residual cho thấy:

- model tuyến tính gốc dự đoán thiếu ở đuôi phải,
- phương sai tăng theo `total_bill`.

Một hướng sửa hợp lý:

- dùng log-transform cho response, ví dụ $$\log(\text{tip})$$,
- hoặc model hóa $$\sigma$$ theo `x`,
- hoặc thêm thành phần phi tuyến nhẹ (spline/polynomial bậc thấp).

Thông điệp quan trọng: không sửa model bằng cảm giác. Hãy sửa theo đúng dấu hiệu sai lệch mà PPC và residual chỉ ra.

### 7.1. So sánh nhanh ba ứng viên model

| Ứng viên | Xử lý vấn đề chính | Điểm mạnh | Rủi ro |
|---|---|---|---|
| Tuyến tính Gaussian cơ sở | Mốc tham chiếu ban đầu | Dễ diễn giải | Dễ sai ở tail và phương sai thay đổi |
| Log-tip Gaussian | Co đuôi phải, ổn định phương sai hơn | Thường cải thiện PPC tail | Diễn giải ngược về đơn vị gốc cần cẩn thận |
| Heteroskedastic Gaussian | Cho phép $$\sigma$$ đổi theo `total_bill` | Trung thực hơn về prediction interval ở hóa đơn lớn | Tăng độ phức tạp và chi phí kiểm tra |

Trong thực hành, bạn nên so sánh các ứng viên này bằng cùng một bộ PPC/residual criteria trước khi kết luận model nào hữu ích nhất.

## 8. Tóm tắt workflow 4.4 trên một case thật

Trên dataset `tips`, ta đã đi đúng chu trình:

1. nêu generative story và fit model,
2. kiểm tra diagnostics,
3. làm posterior predictive checks,
4. đọc residual để tìm pattern,
5. dự đoán cho tình huống cụ thể với uncertainty rõ ràng,
6. đề xuất model revision dựa trên evidence.

Đây là phiên bản thực chiến của thông điệp bài 4.4: regression Bayes chỉ hoàn chỉnh khi bạn kiểm tra và sửa mô hình, không dừng ở mỗi posterior của tham số.

### 8.1. Checklist phân tích chuyên sâu (dùng lại cho bài toán khác)

1. kiểm tra cấu trúc dữ liệu và vùng đuôi trước khi fit,
2. xác nhận sampler đạt chuẩn tối thiểu,
3. chạy PPC ở ba tầng: phân phối tổng thể, statistic mục tiêu, quan hệ `x -> y`,
4. đọc residual theo pattern chứ không chỉ nhìn trung bình,
5. báo cáo prediction đúng loại bất định,
6. chỉ sửa model khi có dấu hiệu sai lệch rõ ràng từ check.

## 9. Những sai lầm phổ biến trong case study này

### 9.1. Dừng ở việc "slope dương"

Slope dương không đảm bảo model sinh dữ liệu hợp lý trên toàn miền của predictor.

### 9.2. Báo cáo sai loại khoảng

Dùng khoảng của mean response để nói về một cá nhân/bàn ăn cụ thể sẽ gây chắc chắn giả tạo.

### 9.3. Sửa model mà không dựa trên check

Thử nhiều biến đổi tùy hứng mà không bám vào dấu hiệu residual/PPC làm workflow mất tính khoa học.

### 9.4. Báo cáo kết quả mà không nói rõ phạm vi áp dụng

Một model có thể ổn ở vùng `total_bill` trung tâm nhưng yếu ở vùng rất lớn. Nếu không nêu rõ điều này, người dùng dễ hiểu sai mức độ tin cậy của dự báo.

## 10. Điều nên giữ lại sau bài này

Một Bayesian workflow trưởng thành luôn đi theo vòng lặp:

**mô hình hóa -> kiểm tra -> dự đoán -> sửa mô hình**.

Case `tips` cho thấy ngay cả bài toán nhỏ cũng cần đầy đủ vòng lặp này để kết luận có trách nhiệm.

## Câu hỏi tự luyện

1. Với dataset `tips`, bạn sẽ chọn statistic nào cho PPC ngoài mean/variance, và vì sao?
2. Nếu residual vs fitted tạo hình chữ U, bạn sẽ thử sửa mô hình theo hướng nào trước?
3. Tại sao prediction interval cho một bàn mới luôn rộng hơn khoảng bất định của mean tip?
4. Nếu mô hình dự đoán tốt vùng trung tâm nhưng fail ở tail phải, điều này ảnh hưởng gì đến quyết định kinh doanh?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*Bài học tiếp theo: [Bài 4.6 - Case Study Nâng Cao trên Dataset Phức Tạp](/vi/chapter04/2025/01/02/04_06_case_study_complex_dataset.html)*
