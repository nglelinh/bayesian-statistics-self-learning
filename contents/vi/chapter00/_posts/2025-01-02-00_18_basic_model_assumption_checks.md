---
layout: post
title: "Bài 0.20: Kiểm tra giả định mô hình cơ bản"
chapter: '00'
order: 20
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách kiểm tra nhanh nhưng có hệ thống các giả định cốt lõi của mô hình (dạng phân phối, tính độc lập, cấu trúc sai số), nhận diện dấu hiệu sai mô hình (misspecification), và biến kết quả kiểm tra thành hành động cải tiến mô hình.

![Kiem tra gia dinh mo hinh co ban]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_checks.png)

*Cách đọc hình: Hình này minh họa kiem tra gia dinh mo hinh co ban. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hinh 1: Minh hoa fit va residual de nhin nhanh outlier, xu huong phan du, va dau hieu misspecification.*

## 1) Giả định mô hình là gì và nằm ở đâu?

Mỗi mô hình thống kê ngầm nói rằng dữ liệu được sinh từ một cơ chế nào đó, nhiễu có một cấu trúc nhất định, và quan hệ giữa biến đầu vào với biến đầu ra có một dạng hình học hoặc xác suất cụ thể.

Nếu giả định sai nghiêm trọng, suy luận có thể lệch dù code chạy hoàn hảo.

Trong thực hành, giả định thường xuất hiện ở 3 nơi. Thứ nhất là ở **likelihood**, tức dữ liệu thuộc họ phân phối nào như Gaussian, Poisson hay Binomial. Thứ hai là ở **mean structure**, tức quan hệ trung bình giữa $$x$$ và $$y$$ là tuyến tính, phi tuyến, hay có tương tác. Thứ ba là ở **noise structure**, nơi ta hỏi phương sai có hằng hay thay đổi theo mức dự báo, và dữ liệu có phụ thuộc theo thời gian hoặc theo nhóm hay không.

## 2) Bộ kiểm tra tối thiểu nên làm

### 2.1 Kiểm tra phân phối đầu ra

1. Vẽ histogram/density của $$y$$.
2. So sánh trực giác với likelihood đang chọn.
3. Tự hỏi: dữ liệu có bị lệch mạnh, có nhiều số 0, có biên tự nhiên (0-1) không?

Ví dụ, dữ liệu đếm có quá nhiều số 0 thường không phù hợp với Gaussian, còn dữ liệu tỷ lệ nằm trong $$[0,1]$$ đòi hỏi một mô hình tôn trọng miền giá trị đó thay vì dự báo ra ngoài khoảng hợp lệ.

### 2.2 Kiểm tra phần dư

Phần dư thường được viết:

$$
e_i = y_i - \hat y_i
$$

Kỳ vọng cơ bản của một mô hình tạm ổn là phần dư dao động quanh 0, không tạo ra xu hướng rõ ràng theo $$\hat y$$ hoặc theo $$x$$, và không để lộ những hình dạng có cấu trúc như đường cong, hình phễu, hay các cụm tách biệt theo nhóm.

### 2.3 Kiểm tra outlier và điểm ảnh hưởng mạnh

Không phải outlier nào cũng "xấu". Chúng có thể là lỗi dữ liệu, trường hợp hiếm nhưng hợp lệ, hoặc tín hiệu cho thấy mô hình đang thiếu biến hay dùng sai likelihood.

Điều quan trọng là kiểm tra độ nhạy: bỏ/tái trọng số một vài điểm liệu kết luận có đổi đáng kể không.

### 2.4 Kiểm tra giả định độc lập

Giả định độc lập dễ vỡ trong dữ liệu thực tế. Ta có thể gặp phụ thuộc theo **thời gian** do tự tương quan, theo **nhóm** như học sinh trong cùng lớp hoặc bệnh nhân trong cùng bệnh viện, và theo **không gian** khi các điểm đo gần nhau thường giống nhau hơn.

Nếu bỏ qua phụ thuộc, khoảng bất định thường bị đánh giá quá lạc quan (quá hẹp).

## 3) Bản đồ "dấu hiệu -> hành động"

Nếu residual có hình cong, ta nên nghĩ đến việc thêm thành phần phi tuyến hoặc biến tương tác. Nếu residual có dạng hình phễu, nghĩa là phương sai tăng theo mức dự báo, ta cần cân nhắc mô hình phương sai thay đổi hoặc thay likelihood. Nếu xuất hiện nhiều giá trị cực đoan hơn mong đợi, likelihood heavy-tail như Student-t có thể phù hợp hơn. Nếu dữ liệu đếm có quá nhiều số 0, Poisson hoặc Negative Binomial, thậm chí dạng zero-inflated, thường đáng cân nhắc. Còn nếu có phụ thuộc theo nhóm hoặc theo thời gian, hierarchical model hay cấu trúc tương quan rõ ràng sẽ là hướng mở rộng hợp lý.

## 4) Ví dụ dữ liệu thực tế: nêu rõ nguồn số liệu và suy luận

Để tránh tình trạng "nhận xét cảm tính", phần này dùng dữ liệu công khai có thể tái lập trực tiếp bằng Python (`seaborn.load_dataset`).

### Ví dụ 1: Dữ liệu `diamonds` (giá kim cương)

**Nguồn dữ liệu**: `seaborn.load_dataset("diamonds")`, $$n=53{,}940$$ quan sát.

**Bài toán**: mô hình hóa giá $$y$$ theo trọng lượng `carat`.

**Bước 1 - Kiểm tra phân phối đầu ra**: trên dữ liệu thực, `price` có `min=326`, `median=2401`, `max=18823`, độ lệch phải với `skewness = 1.618`, và ngưỡng phân vị 95% là `13107.1`, tức đúng 5% quan sát nằm ở đuôi cao.

Kết luận: nhận xét "đuôi phải dài" không phải cảm giác thị giác, mà xuất phát từ thống kê mô tả cụ thể.

![Diamonds price distribution]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_diamonds_distribution.png)

*Cách đọc hình: Hình này minh họa diamonds price distribution. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hinh 2: Histogram gia kim cuong (diamonds) voi vach q95, cho thay phan phoi lech phai va duoi cao.*

**Bước 2 - Fit baseline và kiểm tra residual**:

Mô hình baseline:

$$
y_i \sim \mathcal{N}(\mu_i, \sigma), \quad \mu_i = \alpha + \beta\,\text{carat}_i
$$

Chẩn đoán định lượng trên residual cho thấy tương quan $$\mathrm{corr}(|e_i|, \hat y_i)=0.579$$ là mạnh và dương, còn MAE của nhóm fitted thấp và cao lần lượt là `478.4` và `2059.1`, tức chênh nhau tới `4.30` lần.

Kết luận: phương sai residual tăng mạnh theo mức dự báo, vi phạm giả định đồng nhất phương sai.

![Diamonds residual vs fitted]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_diamonds_residuals.png)

*Cách đọc hình: Hình này minh họa diamonds residual vs fitted. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hinh 3: Residual vs fitted cua mo hinh baseline tren diamonds; do phan tan residual mo rong khi fitted tang (dau hieu heteroscedasticity).*

**Bước 3 - Cập nhật mô hình và kiểm tra lại**:

Mô hình cập nhật (ổn định hơn):

$$
\log y_i = \alpha + \beta_1\,\text{carat}_i + \beta_2\,\text{carat}_i^2 + \epsilon_i,
$$

với $$\epsilon_i$$ có thể xem gần Gaussian hơn trên thang log.

Sau khi cập nhật mô hình, $$\mathrm{corr}(|e_i|, \hat y_i)$$ giảm từ `0.579` xuống `0.047`, còn tỉ lệ MAE cao/thấp giảm từ `4.30` xuống `1.16`.

Kết luận: kiểm tra giả định chỉ ra vấn đề cụ thể, và mô hình cập nhật xử lý đúng vấn đề đó.

---

### Ví dụ 2: Dữ liệu `taxis` (đếm số chuyến theo zone-ngày)

**Nguồn dữ liệu**: `seaborn.load_dataset("taxis")`.

**Cách tạo biến đếm**:

1. Giữ các chuyến có `pickup_borough = Manhattan`.
2. Gộp theo cặp `(pickup_zone, day)` để tạo biến đếm `trips`.
3. Điền đầy đủ mọi tổ hợp zone-ngày để bảo toàn các ngày có 0 chuyến.

Sau khi tổng hợp, có $$n=1953$$ ô quan sát zone-ngày.

**Bước 1 - Kiểm tra giả định Poisson cơ bản**: ta có `mean(trips)=2.697`, `var(trips)=7.441`, nên tỉ lệ `var/mean = 2.76`, lớn hơn 1 một cách rõ rệt và vì thế cho thấy overdispersion.

Theo Poisson, $$\mathbb{E}[Y]=\mathrm{Var}(Y)$$, nên dấu hiệu trên là vi phạm trực tiếp.

![Taxis trip-count distribution]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_taxis_distribution.png)

*Cách đọc hình: Hình này minh họa taxis trip-count distribution. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hinh 4: Phan phoi so chuyen theo zone-ngay trong taxis, kem thong ke mean, variance, va var/mean de nhan dien overdispersion.*

**Bước 2 - Kiểm tra phần zero và đuôi phải**: tỉ lệ zero quan sát là `P(Y=0)=0.245`, trong khi Poisson với $$\lambda=2.697$$ chỉ dự báo `P(Y=0)=e^{-\lambda}=0.067`.

Sai khác zero rất lớn, cho thấy Poisson thiếu linh hoạt.

Ở đuôi phải, xác suất quan sát được `P(Y>=10)=0.0261`, trong khi Poisson chỉ dự báo `P(Y>=10)=0.00050`.

Poisson đánh giá thấp mạnh các ngày có lưu lượng cao.

![Observed vs model implied probabilities on taxis]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_taxis_probabilities.png)

*Cách đọc hình: Hình này minh họa observed vs model implied probabilities on taxis. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hinh 5: So sanh xac suat quan sat voi xac suat suy ra tu Poisson va Negative Binomial cho hai thong ke muc tieu: $$P(Y=0)$$ va $$P(Y\ge 10)$$.*

**Bước 3 - Cập nhật và kiểm tra lại**:

Ước lượng Negative Binomial theo moment matching với tham số phân tán $$k=1.534$$ cho dự báo `P(Y=0)=0.211`, gần hơn nhiều với mức 0.245 quan sát được, và cho `P(Y>=10)=0.0279`, gần sát với mức 0.0261 của dữ liệu.

Kết luận: chỉ riêng kiểm tra giả định bằng thống kê mô tả đã đủ chứng minh Poisson baseline không phù hợp, và Negative Binomial là cập nhật có cơ sở dữ liệu.

---

### Điều cần rút ra từ hai ví dụ

Điều quan trọng nhất là mỗi kết luận chẩn đoán phải gắn với một con số kiểm chứng cụ thể chứ không chỉ dừng ở mô tả bằng lời; việc kiểm tra nên đi theo chuỗi hợp lý từ phân phối đầu ra, sang residual, rồi tới các thống kê mục tiêu như zero, tail, hay heteroscedasticity; và việc cập nhật mô hình chỉ thực sự có giá trị khi cùng một bộ chỉ số chẩn đoán cho thấy sự cải thiện rõ rệt sau cập nhật.

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

*Bài học tiếp theo: [0.21 Mô phỏng để kiểm tra trực giác thống kê](/vi/chapter00/simulation-for-statistical-intuition/)*
