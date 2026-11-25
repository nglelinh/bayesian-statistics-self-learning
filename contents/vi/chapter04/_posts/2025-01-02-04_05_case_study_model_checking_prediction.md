---
layout: post
title: "Bài 4.5: Case Study Model Checking & Prediction - Đi Trọn Workflow Trên Một Dataset"
chapter: '04'
order: 6
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

Lý thuyết kiểm tra mô hình chỉ thực sự sống dậy khi ta đặt nó lên một tập dữ liệu có thật. Tập dữ liệu `tips` ghi lại 244 bàn ăn trong một nhà hàng thoạt nhìn cực kỳ hiền lành: hóa đơn càng cao, tiền boa càng cao. Thế nhưng chỉ cần đi trọn vẹn sáu bước của quy trình Bayes, ta sẽ chứng kiến một bài học kinh điển: một đường thẳng Gaussian có thể ước lượng rất chuẩn mức tiền boa trung bình 3 đô la, nhưng lại gán xác suất cho tiền boa âm ở bàn nhỏ và đánh giá quá thấp rủi ro biến động ở bàn lớn.

## Mục tiêu học tập

Sau bài này, bạn sẽ thực hành trọn vẹn một quy trình hồi quy Bayes trên tập dữ liệu cụ thể: xây dựng mô hình, đánh giá chất lượng lấy mẫu, kiểm tra mô hình bằng dự báo hậu nghiệm (PPC), phân tích phần dư, báo cáo dự đoán kèm đúng loại bất định và đề xuất điều chỉnh mô hình dựa trên bằng chứng định lượng.

> **Ví dụ ngắn.** Khi dự đoán tiền boa (`tip`) từ tổng hóa đơn (`total_bill`) tại nhà hàng, một mô hình tuyến tính có thể cho hệ số dốc rất rõ ràng. Tuy nhiên, câu hỏi thực tế là: mô hình đó có tái tạo được đặc trưng của dữ liệu thực tế và đưa ra khoảng dự đoán đáng tin cậy cho các bàn ăn mới hay không?
>
> **Câu hỏi tự kiểm tra.** Nếu phân phối hậu nghiệm cho hệ số dốc dương rõ rệt nhưng PPC thất bại ở vùng hóa đơn lớn, bạn nên rút ra kết luận gì?


## Kiến thức cần nhớ: Phương sai giải thích được, Thống kê đuôi và Nhiễu cộng vs. Nhiễu nhân

Để đọc hiểu trọn vẹn nghiên cứu tình huống `tips`, cần nắm chắc ba khái niệm cầu nối giữa thống kê mô tả và mô hình hóa Bayes:

- **Tương quan tuyến tính và phần phương sai chưa giải thích ($$1 - R^2$$):** Hệ số tương quan $$r_{xy} \approx 0.676$$ kéo theo $$R^2 \approx 0.46$$, nghĩa là hơn một nửa (54%) biến thiên của tiền boa nằm ngoài đường thẳng theo `total_bill`. Điều này báo trước rằng việc mô hình hóa phần nhiễu $$\sigma$$ và kiểm tra cấu trúc phần dư quan trọng không kém việc ước lượng hệ số dốc.
- **Hành vi vùng đuôi (Tail Behavior) và thống kê chỉ thị:** Trung bình mẫu rất "dễ chiều" — ngay cả mô hình sai phân phối vẫn thường tái tạo đúng trung bình. Các thống kê đuôi như phân vị 95% $$Q_{0.95}(y)$$ hay tỷ lệ vượt ngưỡng $$\frac{1}{n}\sum \mathbf{1}(y_i > 6)$$ mới là phép thử sắc bén để phát hiện sự bất đối xứng và đuôi dày.
- **Nhiễu cộng (Additive Noise) so với nhiễu nhân (Multiplicative Noise):** Trong dữ liệu tài chính và dịch vụ, sai số thường tỷ lệ với quy mô giao dịch (ví dụ tiền boa dao động quanh 15% hóa đơn, lệch $$\pm 5\%$$). Nhiễu cộng $$y = \mu + \varepsilon$$ giữ biên độ cố định theo đô la nên dễ sinh giá trị âm ở hóa đơn nhỏ và quá hẹp ở hóa đơn lớn; chuyển sang thang log $$\log y \sim \mathcal{N}(\mu_{\log}, \sigma_{\log}^2)$$ chuyển nhiễu nhân thành nhiễu cộng đồng phương sai.
## 1. Giới thiệu tập dữ liệu `tips`

Ta sử dụng tập dữ liệu `tips` (từ thư viện `seaborn`), trong đó mỗi dòng tương ứng với một bàn ăn, `total_bill` là tổng hóa đơn và `tip` là tiền boa. Mục tiêu chính là mô hình hóa và dự đoán `tip` theo `total_bill`; mục tiêu quan trọng không kém là kiểm tra xem mô hình tuyến tính Gaussian cơ sở có đủ phù hợp hay không thay vì mặc nhiên tin vào hệ số dốc.

Tập dữ liệu này đủ gọn để dễ quan sát trực giác, đồng thời đủ thực tế để bộc lộ các vấn đề kinh điển trong kiểm tra mô hình: khả năng phi tuyến nhẹ, phương sai tăng theo quy mô hóa đơn và hành vi vùng đuôi không hoàn toàn phù hợp với phân phối Chuẩn đơn giản.

### 1.1. Trích đoạn dữ liệu

Bảng dưới trình bày 5 dòng đầu của tập dữ liệu `tips`:

| total_bill | tip | sex | smoker | day | time | size |
|---:|---:|---|---|---|---|---:|
| 16.99 | 1.01 | Female | No | Sun | Dinner | 2 |
| 10.34 | 1.66 | Male | No | Sun | Dinner | 3 |
| 21.01 | 3.50 | Male | No | Sun | Dinner | 3 |
| 23.68 | 3.31 | Male | No | Sun | Dinner | 3 |
| 24.59 | 3.61 | Female | No | Sun | Dinner | 4 |

### 1.2. Tóm tắt dữ liệu trước khi mô hình hóa

Trên toàn bộ 244 quan sát:

- `total_bill`: trung bình khoảng 19.79, độ lệch chuẩn khoảng 8.90, nhỏ nhất 3.07, lớn nhất 50.81.
- `tip`: trung bình khoảng 3.00, độ lệch chuẩn khoảng 1.38, nhỏ nhất 1.00, lớn nhất 10.00.
- Tương quan tuyến tính giữa `total_bill` và `tip` đạt khoảng 0.676 (dương, mức trung bình đến khá).

Một điểm đáng lưu ý cho bước kiểm tra phía sau: chỉ khoảng 2.9% quan sát có `tip > 6`, nhưng đây lại là vùng phản ánh hành vi đuôi phải (tail behavior) — nơi mô hình tuyến tính Gaussian thường dễ sai lệch:

- **Vì sao tỷ lệ 2.9% vẫn quan trọng?** Các trường hợp ở đuôi phải thường gắn với những giao dịch có giá trị lớn; dù ít gặp, chúng quyết định độ chính xác của dự báo trong các kịch bản rủi ro hoặc doanh thu cao.
- **Vì sao mô hình Gaussian cơ sở dễ lệch ở đuôi?** Mô hình giả định sai số đối xứng và dùng một độ lệch chuẩn nhiễu $$\sigma$$ cố định cho mọi mức hóa đơn. Trong dữ liệu dịch vụ, độ phân tán tiền boa thường tăng theo mức hóa đơn, khiến đuôi phải dày hơn so với dự báo của phân phối Chuẩn đồng phương sai.
- **Hệ quả nếu bỏ qua vùng đuôi:** mô hình có thể khớp tốt giá trị trung bình nhưng đánh giá thấp xác suất xuất hiện tiền boa cao, khiến khoảng dự đoán ở vùng hóa đơn lớn bị hẹp hơn thực tế.
- **Cách kiểm tra trong PPC:** bên cạnh trung bình và phương sai, cần bổ sung các thống kê kiểm tra vùng đuôi như:

$$
T_1(y)=\frac{1}{n}\sum_{i=1}^{n}\mathbf 1(y_i>6),\quad T_2(y)=\max(y),\quad T_3(y)=Q_{0.95}(y).
$$

Nếu giá trị quan sát $$T(y_{obs})$$ rơi ra rìa hoặc nằm ngoài phân phối mô phỏng $$T(y_{rep})$$, đó là bằng chứng cho thấy mô hình chưa tái hiện tốt hành vi vùng đuôi.

### 1.3. Cơ sở định lượng cho các nhận định ban đầu

Để tránh đánh giá cảm tính, ta gắn mỗi nhận định với công thức thống kê cụ thể. Hệ số tương quan Pearson giữa `total_bill` và `tip` là:

$$
r_{xy}=\frac{\sum_{i=1}^{n}(x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_{i=1}^{n}(x_i-\bar x)^2}\sqrt{\sum_{i=1}^{n}(y_i-\bar y)^2}}.
$$

Giá trị $$r_{xy}\approx 0.676$$ cho thấy hai điều rõ ràng: chiều hướng dương (hóa đơn cao hơn đi kèm tiền boa có xu hướng cao hơn) và cường độ ở mức vừa đến khá. Trong hồi quy tuyến tính một biến, hệ số xác định thỏa mãn:

$$
R^2 \approx r_{xy}^2.
$$

Với $$r_{xy}\approx 0.676$$, ta có $$R^2\approx 0.46$$ — nghĩa là đường thẳng đơn giản mới giải thích khoảng 46% biến thiên của `tip`. Tỷ lệ quan sát ở vùng đuôi phải (`tip > 6`) được định nghĩa bởi:

$$
\hat p_{\text{tip}>6}=\frac{1}{n}\sum_{i=1}^{n}\mathbf 1(y_i>6)\approx 0.029.
$$

Cuối cùng, để phát hiện sớm hiện tượng phương sai thay đổi (heteroskedasticity), ta tính tương quan giữa độ lớn phần dư và biến dự báo:

$$
\operatorname{corr}(|e_i|,x_i), \quad e_i=y_i-\hat y_i.
$$

Nếu chỉ số này dương đáng kể, biên độ sai số tăng theo `total_bill` và giả định nhiễu đồng nhất cần được xem xét lại.

## 2. Bước 1 – Xây dựng và khớp mô hình cơ sở

Mô hình cơ sở (baseline) có dạng:

$$
\text{tip}_i \sim \mathcal{N}(\mu_i, \sigma), \quad \mu_i = \alpha + \beta\,x_i,
$$

trong đó $$x_i$$ là `total_bill` đã chuẩn hóa. Cơ chế sinh dữ liệu ở đây giả định mỗi bàn ăn có mức tiền boa kỳ vọng tuyến tính theo hóa đơn, dao động quanh đường trung bình với một độ nhiễu chung $$\sigma$$, cùng phân phối tiên nghiệm thông tin yếu nhằm tránh quá khớp ở vùng hóa đơn rất lớn. Kết quả ước lượng sẽ cho hệ số dốc dương rõ rệt, nhưng ta chỉ coi đây là điểm xuất phát để tiến hành kiểm định.

## 3. Bước 2 – Kiểm tra chẩn đoán bộ lấy mẫu

Trước khi diễn giải bất kỳ tham số nào, cần xác nhận quá trình lấy mẫu MCMC đạt yêu cầu: trace plot trộn đều giữa các chuỗi, $$\hat{R}$$ tiệm cận 1.00 cho các tham số chính, ESS đủ lớn để ước lượng ổn định cả vùng đuôi và không có cảnh báo divergence có hệ thống. Mọi kết quả PPC phía sau chỉ có ý nghĩa khi các mẫu hậu nghiệm đã thực sự đáng tin cậy.

## 4. Bước 3 – Kiểm tra dự báo hậu nghiệm (PPC)

Dựa trên phân phối dự báo hậu nghiệm từ Bài 4.4:

$$
p(\tilde y \mid y)=\int p(\tilde y \mid \theta)\,p(\theta\mid y)\,d\theta,
$$

ta kiểm tra xem dữ liệu `tip` mô phỏng từ mô hình cơ sở có khớp với dữ liệu thực tế ở cả vùng trung tâm lẫn vùng đuôi hay không.

### 4.1. Đối chiếu phân phối tổng thể

So sánh dữ liệu quan sát `y` với dữ liệu mô phỏng `y_rep` để kiểm tra độ trùng khớp của đường mật độ, khả năng tái tạo đuôi phải (tiền boa cao) và miền giá trị cực tiểu/cực đại.

![Hình 2 - So sánh quan sát và posterior predictive trên toàn phân phối]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_observed_vs_predicted.png)

### 4.2. Đối chiếu trung bình, phương sai và thống kê đuôi

Tính các thống kê như trung bình, phương sai và tỷ lệ `tip > 6` trên cả dữ liệu thực và các tập dữ liệu mô phỏng. Nếu giá trị thực tế nằm quá xa so với phân phối mô phỏng, mô hình đang thiếu một phần cấu trúc quan trọng.

![Hình 3 - Kiểm tra mean bằng posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_test_stat_mean.png)

![Hình 4 - Kiểm tra variance bằng posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_variance_check.png)

Với tập dữ liệu `tips`, mô hình cơ sở thường tái tạo trung bình tổng thể khá tốt nhưng dễ lệch về phương sai ở vùng hóa đơn lớn — dấu hiệu sớm của hiện tượng phương sai thay đổi.

### 4.3. Đối chiếu mối quan hệ giữa `total_bill` và `tip`

Vẽ nhiều tập dự báo hậu nghiệm chồng lên biểu đồ phân tán thực tế giúp quan sát xem mô hình có dự đoán lệch ở vùng `total_bill` lớn hay không và độ rộng phân tán có mở rộng theo hóa đơn hay không. Đây thường là nơi phát hiện sớm nhất dấu hiệu phi tuyến hoặc phương sai thay đổi.

![Hình 5 - So sánh quan hệ predictor-response giữa dữ liệu thật và mẫu posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_distribution_at_x5.png)

## 5. Bước 4 – Phân tích phần dư để tìm sai lệch có hệ thống

Xét phần dư hậu nghiệm:

$$
r_i = y_i - \mathbb{E}[\tilde y_i \mid y].
$$

Ta kiểm tra ba biểu đồ cơ bản: phần dư theo giá trị ước lượng, phần dư theo `total_bill` và biểu đồ Q–Q. Các tín hiệu cần chú ý gồm: mẫu hình cong gợi ý quan hệ phi tuyến, dạng hình quạt gợi ý phương sai thay đổi, và đuôi lệch mạnh trên biểu đồ Q–Q gợi ý giả định phân phối Chuẩn quá hẹp. Trên tập `tips`, biên độ phần dư thường có xu hướng mở rộng khi `total_bill` tăng, cho thấy giả định đồng phương sai chưa thật sự phù hợp.

![Hình 6 - Residual distribution: quan sát so với posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_residual_distribution.png)

![Hình 7 - Residuals vs fitted để nhận diện pattern hệ thống]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_residuals.png)

## 6. Bước 5 – Dự đoán cho trường hợp cụ thể

Giả sử cần dự đoán tiền boa cho một bàn ăn mới có `total_bill = 40`. Cần tách bạch và báo cáo rõ hai loại khoảng bất định:

1. **Khoảng hậu nghiệm cho tiền boa trung bình** tại mức hóa đơn 40 (ví dụ: khoảng 5.8 đến 6.5).
2. **Khoảng dự đoán (prediction interval) cho một bàn ăn cụ thể** (ví dụ: khoảng 3.8 đến 8.7).

Khoảng thứ hai rộng hơn đáng kể vì gộp thêm độ nhiễu cá thể của bàn ăn mới. Khi ứng dụng vào thực tế, nếu mục tiêu là lập kế hoạch doanh thu trung bình thì dùng khoảng của trung bình; nếu mục tiêu là đánh giá biến động hoặc rủi ro của từng giao dịch cụ thể thì phải dùng khoảng dự đoán.

### Giải thích: Tính tay sự sụp đổ của mô hình nhiễu cộng ở hai đầu hóa đơn

Hãy đặt hai mô hình — tuyến tính Gaussian nhiễu cộng và mô hình tỷ lệ log-normal — lên cùng hai bàn ăn thực tế để thấy sự khác biệt bằng con số cụ thể:

1. **Mô hình cơ sở nhiễu cộng:** Giả sử hậu nghiệm tập trung quanh $$\hat\mu = 0.92 + 0.105\,x$$ với độ lệch chuẩn nhiễu cố định $$\sigma = 1.02$$ USD.
   - **Tại bàn nhỏ ($$x = 10$$ USD):** Trung bình dự đoán $$\hat\mu = 0.92 + 1.05 = 1.97$$ USD. Khoảng dự đoán 95% xấp xỉ $$1.97 \pm 1.96(1.02) = [-0.03,\ 3.97]$$ USD. Mô hình cho phép **tiền boa âm** — điều bất khả thi về mặt vật lý!
   - **Tại bàn lớn ($$x = 40$$ USD):** Trung bình dự đoán $$\hat\mu = 0.92 + 4.20 = 5.12$$ USD. Khoảng dự đoán 95% là $$5.12 \pm 2.00 = [3.12,\ 7.12]$$ USD (biên độ chỉ $$\pm 2.00$$ USD). Trong khi đó, khách ăn 40 USD boa trong khoảng 10%–25% sẽ trải rộng từ $$4.00$$ đến $$10.00$$ USD — mô hình cơ sở đã cắt mất phần đuôi trên.
2. **Mô hình nhiễu nhân trên thang log:** Xét $$\log(\text{tip}) \sim \mathcal{N}(\log(0.15\,x),\ 0.25^2)$$ (tương ứng tiền boa trung vị 15% hóa đơn, độ phân tán tương đối khoảng 25%).
   - **Tại bàn nhỏ ($$x = 10$$ USD):** Trung vị $$1.50$$ USD; khoảng 95% là $$1.50 \times e^{\pm 1.96(0.25)} = 1.50 \times [0.613,\ 1.632] = [0.92,\ 2.45]$$ USD — hoàn toàn dương và chặt chẽ.
   - **Tại bàn lớn ($$x = 40$$ USD):** Trung vị $$6.00$$ USD; khoảng 95% là $$6.00 \times [0.613,\ 1.632] = [3.68,\ 9.79]$$ USD — tự động giãn rộng tương xứng với quy mô hóa đơn.

Chỉ cần so sánh hai phép nhân trên, bạn thấy ngay vì sao PPC ở vùng đuôi lại thúc đẩy ta chuyển sang mô hình log hoặc heteroskedastic.

## 7. Bước 6 – Điều chỉnh mô hình dựa trên bằng chứng chẩn đoán

Khi PPC và phần dư chỉ ra rằng mô hình tuyến tính cơ sở dự đoán thiếu ở đuôi phải và có phương sai tăng theo `total_bill`, ta có ba hướng điều chỉnh có cơ sở:

- Biến đổi log cho biến phản hồi, chẳng hạn mô hình hóa $$\log(\text{tip})$$.
- Mô hình hóa độ nhiễu $$\sigma$$ thay đổi theo biến dự báo `total_bill`.
- Bổ sung thành phần phi tuyến nhẹ (như spline hoặc đa thức bậc thấp).

Nguyên tắc cốt lõi là mọi chỉnh sửa đều phải xuất phát trực tiếp từ dấu hiệu sai lệch mà PPC và phân tích phần dư chỉ ra, thay vì thử nghiệm cảm tính.

### 7.1. So sánh ba phương án mô hình

| Phương án | Vấn đề xử lý chính | Ưu điểm | Hạn chế cần lưu ý |
|---|---|---|---|
| Tuyến tính Gaussian cơ sở | Làm mốc tham chiếu ban đầu | Đơn giản, dễ diễn giải | Dễ lệch ở vùng đuôi và khi phương sai thay đổi |
| Log-tip Gaussian | Thu gọn đuôi phải, ổn định phương sai | Thường cải thiện PPC vùng đuôi | Cần cẩn thận khi quy đổi ngược về đơn vị gốc |
| Heteroskedastic Gaussian | Cho phép $$\sigma$$ thay đổi theo `total_bill` | Khoảng dự đoán trung thực hơn ở hóa đơn lớn | Tăng số tham số và chi phí kiểm tra mô hình |

Cả ba phương án cần được đối chiếu trên cùng một bộ tiêu chí PPC và phân tích phần dư trước khi chọn mô hình phù hợp nhất.

## 8. Tổng kết quy trình thực hành

Trên tập dữ liệu `tips`, ta đã đi trọn sáu bước của quy trình hồi quy Bayes: (1) xây dựng và khớp mô hình cơ sở, (2) kiểm tra chẩn đoán bộ lấy mẫu, (3) chạy PPC nhiều góc độ, (4) phân tích phần dư, (5) báo cáo dự đoán đúng loại bất định và (6) đề xuất sửa đổi mô hình dựa trên bằng chứng.

### 8.1. Danh mục kiểm tra dùng lại cho các bài toán khác

1. Khảo sát cấu trúc dữ liệu và vùng đuôi trước khi mô hình hóa.
2. Xác nhận các chỉ số hội tụ MCMC đạt ngưỡng tối thiểu.
3. Thực hiện PPC ở ba tầng: phân phối tổng thể, thống kê mục tiêu và quan hệ `x -> y`.
4. Kiểm tra mẫu hình có hệ thống trên phần dư thay vì chỉ nhìn trung bình.
5. Báo cáo rõ ràng khoảng trung bình và khoảng dự đoán cá thể.
6. Chỉ điều chỉnh mô hình khi có tín hiệu sai lệch cụ thể từ bước kiểm tra.

## 9. Những sai lầm thường gặp

- **Dừng lại khi thấy hệ số dốc dương:** hệ số dốc có ý nghĩa thống kê không đảm bảo mô hình tái tạo tốt dữ liệu trên toàn miền giá trị.
- **Nhầm lẫn hai loại khoảng bất định:** dùng khoảng của giá trị trung bình để nói về một bàn ăn cụ thể sẽ tạo ra mức độ chắc chắn giả tạo.
- **Sửa mô hình theo cảm tính:** áp dụng các phép biến đổi tùy hứng mà không gắn với bằng chứng từ PPC hay phần dư sẽ làm mất tính kỷ luật khoa học.
- **Không nêu rõ phạm vi tin cậy:** một mô hình có thể hoạt động tốt ở vùng hóa đơn trung bình nhưng kém ổn định ở vùng hóa đơn rất lớn; cần nêu rõ giới hạn này khi báo cáo.

## 10. Điểm cốt lõi cần giữ lại

Một quy trình làm việc Bayes hoàn chỉnh luôn vận hành theo vòng lặp: **mô hình hóa $$\to$$ kiểm tra $$\to$$ dự đoán $$\to$$ điều chỉnh**. Ngay cả với một tập dữ liệu gọn như `tips`, việc đi đủ vòng lặp này là điều kiện cần để đưa ra kết luận có trách nhiệm.

## Video tham khảo

- [What is a posterior predictive check and why is it useful?](https://www.youtube.com/watch?v=yDPJnV9vcHs) — Ben Lambert, English. **xem trước**. Nêu rõ câu hỏi trung tâm của kiểm tra dự báo hậu nghiệm trước khi áp dụng lên dữ liệu `tips`.
- [L4: Interpretable Linear Regressions (State of Bayes Lecture Series)](https://www.youtube.com/watch?v=fpS0NjqNHn8) — PyMC Labs, English. Minh họa cách xây dựng và diễn giải hồi quy Bayes, hỗ trợ phần thiết lập mô hình của bài.
- [Simple Linear Regression:  Checking Assumptions with Residual Plots](https://www.youtube.com/watch?v=iMdtTCX2Q70) — jbstatistics, English. Hướng dẫn đọc biểu đồ phần dư để kiểm tra giả định mô hình, bổ trợ cho mục 5.

## Câu hỏi tự luyện

1. Với tập dữ liệu `tips`, ngoài trung bình và phương sai, bạn sẽ chọn thêm thống kê nào cho PPC và vì sao?
2. Nếu biểu đồ phần dư theo giá trị ước lượng tạo hình chữ U, bạn sẽ ưu tiên điều chỉnh mô hình theo hướng nào trước?
3. Vì sao khoảng dự đoán cho một bàn ăn mới luôn rộng hơn khoảng hậu nghiệm của mức tiền boa trung bình?
4. Nếu mô hình dự đoán tốt ở vùng hóa đơn trung bình nhưng lệch ở vùng đuôi phải, điều đó ảnh hưởng ra sao đến quyết định kinh doanh?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*Bài học tiếp theo: [Bài 4.6 - Case Study Nâng Cao trên Dataset Phức Tạp]({{ site.baseurl }}/contents/vi/chapter04/04_06_case_study_complex_dataset/)*
