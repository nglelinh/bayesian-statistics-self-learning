---
layout: post
title: "Bài 0.18: Kiểm tra giả định mô hình cơ bản"
chapter: '00'
order: 18
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách kiểm tra nhanh nhưng có hệ thống các giả định cốt lõi của mô hình (dạng phân phối, tính độc lập, cấu trúc sai số), nhận diện dấu hiệu sai mô hình (misspecification), và biến kết quả kiểm tra thành hành động cải tiến mô hình.

![Kiem tra gia dinh mo hinh co ban]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_checks.png)
*Hinh 1: Minh hoa fit va residual de nhin nhanh outlier, xu huong phan du, va dau hieu misspecification.*

## 1) Giả định mô hình là gì và nằm ở đâu?

Mỗi mô hình thống kê ngầm nói rằng:

- dữ liệu sinh từ một cơ chế cụ thể,
- nhiễu có cấu trúc nào đó,
- quan hệ giữa biến đầu vào và đầu ra có dạng nhất định.

Nếu giả định sai nghiêm trọng, suy luận có thể lệch dù code chạy hoàn hảo.

Trong thực hành, giả định thường xuất hiện ở 3 nơi:

- **Likelihood**: dữ liệu thuộc họ phân phối nào (Gaussian, Poisson, Binomial, ...).
- **Mean structure**: quan hệ trung bình giữa $$x$$ và $$y$$ (tuyến tính, phi tuyến, có tương tác hay không).
- **Noise structure**: phương sai có hằng hay thay đổi theo mức dự báo; dữ liệu có phụ thuộc theo thời gian/nhóm không.

## 2) Bộ kiểm tra tối thiểu nên làm

### 2.1 Kiểm tra phân phối đầu ra

1. Vẽ histogram/density của $$y$$.
2. So sánh trực giác với likelihood đang chọn.
3. Tự hỏi: dữ liệu có bị lệch mạnh, có nhiều số 0, có biên tự nhiên (0-1) không?

Ví dụ:

- Dữ liệu đếm nhiều số 0 -> Gaussian thường không phù hợp.
- Dữ liệu tỷ lệ trong $$[0,1]$$ -> cần mô hình phù hợp miền giá trị (không nên dự báo ra ngoài miền).

### 2.2 Kiểm tra phần dư

Phần dư thường được viết:

$$
e_i = y_i - \hat y_i
$$

Kỳ vọng cơ bản của một mô hình tạm ổn:

- phần dư dao động quanh 0,
- không có xu hướng rõ theo $$\hat y$$ hoặc theo $$x$$,
- không tạo "hình dạng có cấu trúc" (đường cong, hình phễu, cụm theo nhóm).

### 2.3 Kiểm tra outlier và điểm ảnh hưởng mạnh

Không phải outlier nào cũng "xấu". Chúng có thể là:

- lỗi dữ liệu,
- trường hợp hiếm nhưng hợp lệ,
- tín hiệu rằng mô hình đang thiếu biến hoặc sai likelihood.

Điều quan trọng là kiểm tra độ nhạy: bỏ/tái trọng số một vài điểm liệu kết luận có đổi đáng kể không.

### 2.4 Kiểm tra giả định độc lập

Giả định độc lập dễ vỡ trong dữ liệu thực tế:

- theo **thời gian** (tự tương quan),
- theo **nhóm** (học sinh trong cùng lớp, bệnh nhân cùng bệnh viện),
- theo **không gian** (điểm đo gần nhau thường giống nhau).

Nếu bỏ qua phụ thuộc, khoảng bất định thường bị đánh giá quá lạc quan (quá hẹp).

## 3) Bản đồ "dấu hiệu -> hành động"

- Residual có hình cong -> thêm thành phần phi tuyến hoặc biến tương tác.
- Residual hình phễu (variance tăng theo mức dự báo) -> dùng mô hình phương sai thay đổi hoặc đổi likelihood.
- Nhiều giá trị cực đoan hơn dự kiến -> cân nhắc likelihood heavy-tail (như Student-t).
- Dữ liệu đếm dư số 0 -> cân nhắc Poisson/Negative Binomial hoặc zero-inflated.
- Có phụ thuộc theo nhóm/thời gian -> cân nhắc hierarchical model hoặc cấu trúc tương quan.

## 4) Ví dụ dữ liệu thực tế: nêu rõ nguồn số liệu và suy luận

Để tránh tình trạng "nhận xét cảm tính", phần này dùng dữ liệu công khai có thể tái lập trực tiếp bằng Python (`seaborn.load_dataset`).

### Ví dụ 1: Dữ liệu `diamonds` (giá kim cương)

**Nguồn dữ liệu**: `seaborn.load_dataset("diamonds")`, $$n=53{,}940$$ quan sát.

**Bài toán**: mô hình hóa giá $$y$$ theo trọng lượng `carat`.

**Bước 1 - Kiểm tra phân phối đầu ra**:

- Trên dữ liệu thực, `price` có `min=326`, `median=2401`, `max=18823`.
- Độ lệch phải `skewness = 1.618`.
- Ngưỡng phân vị 95% là `13107.1`, đúng 5% quan sát nằm ở đuôi cao.

Kết luận: nhận xét "đuôi phải dài" không phải cảm giác thị giác, mà xuất phát từ thống kê mô tả cụ thể.

![Diamonds price distribution]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_diamonds_distribution.png)
*Hinh 2: Histogram gia kim cuong (diamonds) voi vach q95, cho thay phan phoi lech phai va duoi cao.*

**Bước 2 - Fit baseline và kiểm tra residual**:

Mô hình baseline:

$$
y_i \sim \mathcal{N}(\mu_i, \sigma), \quad \mu_i = \alpha + \beta\,\text{carat}_i
$$

Chẩn đoán định lượng trên residual:

- Tương quan $$\mathrm{corr}(|e_i|, \hat y_i)=0.579$$ (mạnh, dương).
- MAE nhóm fitted thấp vs cao lần lượt là `478.4` và `2059.1`; tỉ lệ `4.30` lần.

Kết luận: phương sai residual tăng mạnh theo mức dự báo, vi phạm giả định đồng nhất phương sai.

![Diamonds residual vs fitted]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_diamonds_residuals.png)
*Hinh 3: Residual vs fitted cua mo hinh baseline tren diamonds; do phan tan residual mo rong khi fitted tang (dau hieu heteroscedasticity).*

**Bước 3 - Cập nhật mô hình và kiểm tra lại**:

Mô hình cập nhật (ổn định hơn):

$$
\log y_i = \alpha + \beta_1\,\text{carat}_i + \beta_2\,\text{carat}_i^2 + \epsilon_i,
$$

với $$\epsilon_i$$ có thể xem gần Gaussian hơn trên thang log.

Chỉ số sau cập nhật:

- $$\mathrm{corr}(|e_i|, \hat y_i)$$ giảm từ `0.579` xuống `0.047`.
- Tỉ lệ MAE cao/thấp giảm từ `4.30` xuống `1.16`.

Kết luận: kiểm tra giả định chỉ ra vấn đề cụ thể, và mô hình cập nhật xử lý đúng vấn đề đó.

---

### Ví dụ 2: Dữ liệu `taxis` (đếm số chuyến theo zone-ngày)

**Nguồn dữ liệu**: `seaborn.load_dataset("taxis")`.

**Cách tạo biến đếm**:

1. Giữ các chuyến có `pickup_borough = Manhattan`.
2. Gộp theo cặp `(pickup_zone, day)` để tạo biến đếm `trips`.
3. Điền đầy đủ mọi tổ hợp zone-ngày để bảo toàn các ngày có 0 chuyến.

Sau khi tổng hợp, có $$n=1953$$ ô quan sát zone-ngày.

**Bước 1 - Kiểm tra giả định Poisson cơ bản**:

- Trung bình `mean(trips)=2.697`.
- Phương sai `var(trips)=7.441`.
- Tỉ lệ `var/mean = 2.76` (>1 rõ rệt), cho thấy overdispersion.

Theo Poisson, $$\mathbb{E}[Y]=\mathrm{Var}(Y)$$, nên dấu hiệu trên là vi phạm trực tiếp.

![Taxis trip-count distribution]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_taxis_distribution.png)
*Hinh 4: Phan phoi so chuyen theo zone-ngay trong taxis, kem thong ke mean, variance, va var/mean de nhan dien overdispersion.*

**Bước 2 - Kiểm tra phần zero và đuôi phải**:

- Tỉ lệ zero quan sát: `P(Y=0)=0.245`.
- Poisson với $$\lambda=2.697$$ dự báo `P(Y=0)=e^{-\lambda}=0.067`.

Sai khác zero rất lớn, cho thấy Poisson thiếu linh hoạt.

Với đuôi phải:

- Quan sát: `P(Y>=10)=0.0261`.
- Poisson dự báo: `P(Y>=10)=0.00050`.

Poisson đánh giá thấp mạnh các ngày có lưu lượng cao.

![Observed vs model implied probabilities on taxis]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_taxis_probabilities.png)
*Hinh 5: So sanh xac suat quan sat voi xac suat suy ra tu Poisson va Negative Binomial cho hai thong ke muc tieu: $$P(Y=0)$$ va $$P(Y\ge 10)$$.*

**Bước 3 - Cập nhật và kiểm tra lại**:

Ước lượng Negative Binomial theo moment matching (từ mean/variance) cho tham số phân tán $$k=1.534$$:

- Dự báo `P(Y=0)=0.211` (gần hơn 0.245 so với Poisson).
- Dự báo `P(Y>=10)=0.0279` (gần quan sát 0.0261).

Kết luận: chỉ riêng kiểm tra giả định bằng thống kê mô tả đã đủ chứng minh Poisson baseline không phù hợp, và Negative Binomial là cập nhật có cơ sở dữ liệu.

---

### Điều cần rút ra từ hai ví dụ

1. Mỗi kết luận chẩn đoán cần gắn với một con số kiểm chứng cụ thể, không chỉ mô tả bằng lời.
2. Kiểm tra giả định nên đi theo chuỗi: phân phối -> residual -> thống kê mục tiêu (zero, tail, heteroscedasticity).
3. Cập nhật mô hình chỉ có ý nghĩa khi cùng bộ chỉ số chẩn đoán được cải thiện sau cập nhật.

## 5) Quy trình 15 phút trước khi tin kết quả

1. Xem phân phối của biến mục tiêu.
2. Fit mô hình đơn giản làm baseline.
3. Vẽ residual vs fitted và residual vs predictor chính.
4. Tìm điểm ảnh hưởng mạnh và kiểm tra độ nhạy kết luận.
5. Kiểm tra dấu hiệu phụ thuộc theo thời gian/nhóm.
6. Ghi lại 1-2 giả định có rủi ro cao nhất.
7. Cập nhật mô hình rồi so sánh lại.

Mục tiêu là giảm rủi ro suy luận sai, không phải làm đủ mọi biểu đồ có thể.

## 6) Sai mô hình không phải thất bại, mà là tín hiệu cập nhật

Trong tư duy Bayesian workflow:

1. Đề xuất mô hình,
2. Fit mô hình,
3. Kiểm tra hệ quả dự báo và giả định,
4. Cải tiến mô hình.

Mục tiêu không phải "chứng minh mô hình đúng", mà là làm mô hình phù hợp hơn với dữ liệu và câu hỏi thực tế.

## 7) Liên hệ với các chương sau

Các kỹ thuật kiểm tra sâu hơn như posterior predictive checks, WAIC, LOO sẽ xuất hiện ở chương sau. Bài này giúp bạn có nền trực giác để hiểu chúng không chỉ là chỉ số, mà là công cụ phát hiện sai lệch mô hình.

## Tóm tắt nhanh

1. Mô hình luôn đi kèm giả định.
2. Giả định sai có thể làm kết luận sai.
3. Bộ kiểm tra tối thiểu gồm: phân phối, residual, outlier/influence, phụ thuộc.
4. Dấu hiệu sai mô hình phải dẫn tới hành động chỉnh likelihood/cấu trúc mô hình.
5. Misspecification là thông tin để cải thiện mô hình, không phải "thất bại".

## Câu hỏi tự luyện

1. Nêu một tình huống vi phạm giả định độc lập trong dữ liệu thực và đề xuất cách sửa mô hình.
2. Vì sao kiểm tra residual vs fitted giúp phát hiện sai dạng hàm trung bình?
3. Nếu có outlier mạnh, bạn sẽ phân biệt "lỗi dữ liệu" và "tín hiệu thật" bằng cách nào?
4. Chọn một bài toán bạn từng làm và liệt kê 2 giả định rủi ro nhất của mô hình đó.

## Tài liệu tham khảo

- Gelman, A., et al. (2013). *Bayesian Data Analysis*.
- McElreath, R. (2020). *Statistical Rethinking*.

---

*Bài học tiếp theo: [Bài 0.19: Mô phỏng để kiểm tra trực giác thống kê](/vi/chapter00/simulation-for-statistical-intuition/)*
