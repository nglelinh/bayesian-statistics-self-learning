---
layout: post
title: "Bài 4.6: Case Study Nâng Cao - Model Checking & Prediction Trên Dataset Phức Tạp"
chapter: '04'
order: 7
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

Khi đối diện một bảng dữ liệu gần 54.000 viên kim cương với hệ số tương quan giữa trọng lượng `carat` và giá `price` lên tới $$0.922$$, cám dỗ lớn nhất của người phân tích là kết luận bài toán đã xong. Thế nhưng thị trường kim cương không vận hành theo đường thẳng: một viên kim cương 2 carat không đắt gấp đôi viên 1 carat, mà đắt gấp nhiều lần vì độ hiếm tăng theo hàm mũ, và chênh lệch giữa hai hạng chất lượng `cut` có thể lên tới hàng nghìn đô la. Đây là sân tập thực sự cho quy trình Bayes đa tầng.

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách vận hành đầy đủ một quy trình Bayes trên tập dữ liệu có cấu trúc phức tạp, nơi việc khớp được mô hình mới chỉ là điều kiện cần chứ chưa phải điều kiện đủ. Trọng tâm của bài là rèn luyện năng lực lập luận định lượng: chẩn đoán sai lệch, xác định rõ nguyên nhân cấu trúc và đề xuất can thiệp đúng chỗ thay vì chỉnh sửa theo cảm tính.

> **Ví dụ dẫn nhập.** Trong tập dữ liệu kim cương, `carat` và `price` có tương quan rất cao, nhưng một mô hình tuyến tính đơn giản vẫn có thể sai lệch nghiêm trọng ở đuôi phải của phân phối giá — tức hoạt động ổn ở vùng phổ thông nhưng thất bại ở phân khúc mang giá trị kinh tế cao nhất.
>
> **Câu hỏi tự kiểm tra.** Vì sao một chỉ số tổng hợp rất cao như tương quan trên 0.9 vẫn chưa đủ để kết luận mô hình đáng tin cậy cho bài toán dự đoán thực tế?


## Bản đồ kiến thức nền: Phân phối Log-Normal, Độ bao phủ có điều kiện và Gộp một phần (Partial Pooling)

Để làm chủ một bài toán quy mô lớn và phi đồng nhất như `diamonds`, ba công cụ lý thuyết sau đóng vai trò xương sống:

- **Phân phối Log-Normal và hiệu chỉnh bất đẳng thức Jensen:** Nếu $$\log Y \sim \mathcal{N}(\mu, \sigma^2)$$ thì $$Y = e^{\log Y}$$ có trung vị là $$e^\mu$$, nhưng vì hàm mũ lồi chặt (bất đẳng thức Jensen: $$\mathbb{E}[e^Z] > e^{\mathbb{E}[Z]}$$), kỳ vọng thực sự là $$\mathbb{E}[Y] = \exp(\mu + \sigma^2/2)$$. Quên số hạng $$\sigma^2/2$$ sẽ tạo ra sai lệch định giá thấp có hệ thống trên thang tiền tệ gốc.
- **Đánh giá có điều kiện (Conditional Calibration) và độ bao phủ ngoài mẫu:** Một khoảng dự đoán 90% có thể đạt độ bao phủ tổng thể 92% nhờ thừa bao phủ ở 90% dữ liệu phổ thông (kim cương nhỏ), trong khi chỉ bao phủ 72% ở 10% phân khúc cao cấp (kim cương lớn). Chia miền theo dải `carat` biến kiểm định tổng thể thành kính hiển vi phát hiện sai lệch cục bộ.
- **Mô hình phân cấp và cơ chế co cụm (Partial Pooling / Shrinkage):** Khi dữ liệu chia thành nhiều nhóm có cỡ mẫu chênh lệch, đặt tiên nghiệm chung $$\alpha_g \sim \mathcal{N}(\alpha_0, \tau_\alpha^2)$$ cho phép các nhóm chia sẻ thông tin thống kê. Nhóm nhiều dữ liệu giữ sát trung bình riêng; nhóm ít dữ liệu tự động co nhẹ về trung tâm chung $$\alpha_0$$ theo tỷ lệ độ chính xác.
## 1. Bối cảnh dữ liệu: vì sao `diamonds` là phép thử khó?

Ta làm việc với tập dữ liệu `diamonds` (trong thư viện `seaborn`), gồm biến phản hồi `price` và nhiều biến mô tả cả kích thước hình học lẫn chất lượng như `carat`, `cut`, `color`, `clarity`, `depth`, `table`. Tập dữ liệu này buộc người phân tích đối diện đồng thời với ba lớp phức tạp: mối quan hệ tuy mạnh nhưng không đồng nhất trên toàn miền biến dự báo, cấu trúc phân nhóm mang ý nghĩa thực chất, và hành vi đuôi phải của giá ảnh hưởng trực tiếp tới bài toán định giá.

### 1.1. Trích đoạn dữ liệu quan sát

| carat | cut | color | clarity | depth | table | price | x | y | z |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|
| 0.23 | Ideal | E | SI2 | 61.5 | 55.0 | 326 | 3.95 | 3.98 | 2.43 |
| 0.21 | Premium | E | SI1 | 59.8 | 61.0 | 326 | 3.89 | 3.84 | 2.31 |
| 0.23 | Good | E | VS1 | 56.9 | 65.0 | 327 | 4.05 | 4.07 | 2.31 |
| 0.29 | Premium | I | VS2 | 62.4 | 58.0 | 334 | 4.20 | 4.23 | 2.63 |
| 0.31 | Good | J | SI2 | 63.3 | 58.0 | 335 | 4.34 | 4.35 | 2.75 |

### 1.2. Tóm tắt định lượng ban đầu

Trên `n = 53,940` quan sát, biến `carat` có trung bình khoảng 0.798 và trung vị khoảng 0.70, trong khi `price` có trung bình khoảng 3932.8 nhưng trung vị chỉ khoảng 2401 — dấu hiệu rõ rệt của phân phối lệch phải. Tương quan Pearson giữa `carat` và `price` đạt khoảng 0.922, rất mạnh ở mức tổng thể; tuy vậy, chỉ khoảng 3.07% quan sát rơi vào vùng `price > 15000`, và chính phân khúc nhỏ này lại là nơi sai lệch mô hình gây tổn thất lớn nhất trong bài toán định giá cao cấp.

## 2. Từ số liệu đến lập luận định lượng

Một phân tích chặt chẽ không dừng ở nhận xét định tính như "có vẻ lệch", mà phải gắn từng kết luận với một thước đo thống kê cụ thể.

Hệ số tương quan mẫu giữa `carat` và `price` được tính bởi:

$$
r_{xy}=\frac{\sum_{i=1}^{n}(x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_{i=1}^{n}(x_i-\bar x)^2}\sqrt{\sum_{i=1}^{n}(y_i-\bar y)^2}} \approx 0.922.
$$

Con số này chỉ xác nhận rằng `carat` và `price` biến thiên đồng pha mạnh theo nghĩa tuyến tính toàn cục. Nó không đảm bảo phần dư phân bố ngẫu nhiên quanh 0, không đảm bảo phương sai sai số đồng nhất và không đảm bảo mô hình dự báo tốt ở đuôi phải. Nói cách khác, tương quan cao cho thấy có tín hiệu mạnh, nhưng chưa chứng minh cấu trúc mô hình sinh dữ liệu là đúng.

Tương tự, tỷ lệ quan sát ở vùng đuôi phải được định lượng cụ thể:

$$
\hat p_{\text{price}>15000}=\frac{1}{n}\sum_{i=1}^{n}\mathbf 1(y_i>15000)\approx 0.0307.
$$

Dù chỉ chiếm khoảng 3% số lượng quan sát, vùng đuôi này lại mang trọng số giá trị rất lớn; do đó một mô hình khớp tốt ở trung tâm nhưng sai ở đuôi vẫn tiềm ẩn rủi ro cao khi dùng cho định giá hoặc quản trị danh mục cao cấp.

Cuối cùng, để kiểm tra giả định phương sai đồng nhất, ta sử dụng chỉ báo:

$$
\operatorname{corr}(\lvert e_i \rvert,x_i), \qquad e_i=y_i-\hat y_i.
$$

Khi độ lớn phần dư tăng theo biến dự báo, giả định dùng chung một mức nhiễu $$\sigma$$ cho toàn bộ miền dữ liệu sẽ không còn phù hợp.

## 3. Mô hình cơ sở: điểm chuẩn cần thiết nhưng chưa phải đích đến

Ta bắt đầu với mô hình tuyến tính Gaussian cơ sở:

$$
\text{price}_i \sim \mathcal N(\mu_i,\sigma), \qquad \mu_i=\alpha+\beta\,\text{carat}_i.
$$

Ta xây dựng mô hình này **không phải vì tin rằng dữ liệu đơn giản đến mức đó, mà vì mọi cải thiện về sau đều cần một mốc chuẩn rõ ràng để đối chiếu**. Trên tập `diamonds`, mô hình cơ sở thường nắm bắt khá tốt xu hướng trung bình chung, nhưng sớm bộc lộ ba hạn chế: biên độ sai số tăng mạnh theo `carat`, đuôi phải của `price` bị nén quá mỏng và sự khác biệt theo nhóm chất lượng (`cut`, `clarity`, `color`) chưa được mô tả.

## 4. Kiểm tra dự báo hậu nghiệm (PPC) nhiều tầng

Với dữ liệu phức tạp, một phép kiểm tra PPC duy nhất là không đủ. Ta cần chuỗi kiểm tra đi từ toàn cục đến có điều kiện để xác định chính xác mô hình đúng ở đâu và sai ở đâu.

Ở **tầng toàn cục**, ta so sánh phân phối dữ liệu quan sát với phân phối dự báo hậu nghiệm để kiểm tra đồng thời vị trí trung tâm, độ phân tán và độ dày vùng đuôi — bước giúp phát hiện sớm các sai lệch thô.

![So sánh dữ liệu quan sát và posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_observed_vs_predicted.png)

Ở **tầng thống kê mục tiêu**, ta đối chiếu mô hình qua các đại lượng định lượng cụ thể:

$$
T_1(y)=\bar y,\quad T_2(y)=\operatorname{Var}(y),\quad T_3(y)=Q_{0.95}(y),\quad T_4(y)=\frac{1}{n}\sum_{i=1}^{n}\mathbf 1(y_i>15000).
$$

Nếu mô hình tái tạo tốt $$T_1$$ nhưng lệch rõ rệt ở $$T_3$$ hoặc $$T_4$$, kết luận chính xác phải là "mô hình ổn ở trung tâm nhưng yếu ở vùng đuôi" — sự phân biệt mang ý nghĩa quyết định đối với các bài toán định giá phân khúc cao.

![PPC cho mean]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_test_stat_mean.png)

![PPC cho variance]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_variance_check.png)

Ở **tầng có điều kiện theo biến dự báo**, ta chia `carat` thành từng dải giá trị $$B_k$$ và kiểm tra riêng thay vì gộp chung:

$$
T_{\text{bin},k}(y)=\operatorname{Var}(y\mid x\in B_k),\qquad T^{(0.95)}_{\text{bin},k}(y)=Q_{0.95}(y\mid x\in B_k).
$$

Cách kiểm tra này giúp phát hiện tình huống mô hình khớp tốt ở dải `carat` phổ biến nhưng sai lệch có hệ thống ở dải `carat` lớn.

Ở **tầng theo nhóm chất lượng**, ta kiểm tra khả năng tái tạo trung bình theo từng nhóm `cut`, `clarity`, `color`:

$$
T_g(y)=\bar y_g.
$$

Khi mô hình chỉ dùng `carat` không tái hiện được chênh lệch giữa các nhóm này, đó là bằng chứng cho thấy mô hình sinh dữ liệu đang bỏ sót yếu tố cấu trúc quan trọng.

## 5. Phân tích phần dư: chẩn đoán cơ chế sai lệch

Nếu PPC cung cấp bức tranh ở mức phân phối, thì phân tích phần dư giúp soi sát cơ chế sai lệch. Câu hỏi trọng tâm không phải "phần dư có nhỏ không" mà là "phần dư có còn chứa cấu trúc có hệ thống không".

![Dấu hiệu heteroskedasticity trên scatter]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_scatter.png)

![Residuals vs fitted: dạng quạt]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_residuals.png)

![Q-Q plot khi đuôi residual lệch]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_qq.png)

Trên dữ liệu `diamonds`, hình quạt trên biểu đồ phần dư theo giá trị ước lượng cho thấy độ bất định tăng rõ rệt theo quy mô giá và `carat`, còn độ lệch ở hai đầu biểu đồ Q–Q cho thấy giả định phân phối Chuẩn đơn giản chưa đủ để mô tả vùng đuôi. Hệ quả là khoảng dự đoán ở vùng `carat` cao sẽ bị hẹp hơn thực tế nếu giữ nguyên mô hình cơ sở.

## 6. Dự đoán cho ra quyết định và độ bao phủ ngoài mẫu

Trong báo cáo dự đoán, cần phân biệt rạch ròi giữa bất định của giá trị trung bình có điều kiện và bất định của một quan sát mới:

$$
p(\mu_*\mid y,x_*) \quad \text{và} \quad p(\tilde y_*\mid y,x_*).
$$

Phân phối thứ hai luôn rộng hơn vì bao hàm cả nhiễu cá thể. Dùng khoảng của $$p(\mu_*\mid y,x_*)$$ để dự báo giá cho một viên kim cương cụ thể sẽ dẫn đến đánh giá quá lạc quan về độ chính xác.

Một thước đo thực nghiệm quan trọng khác là **tỷ lệ bao phủ ngoài mẫu** (out-of-sample coverage):

$$
\text{Coverage}_{90\%}=\frac{1}{m}\sum_{j=1}^{m}\mathbf 1\{y_j^{\text{test}}\in \text{PI}_{90\%}(x_j)\}.
$$

Nếu tỷ lệ bao phủ sụt giảm mạnh ở vùng `carat` lớn, đó là bằng chứng trực tiếp cho thấy mô hình chưa đáng tin cậy ở phân khúc giá cao, bất kể các chỉ số tổng thể có vẻ thuận lợi.

## 7. Điều chỉnh mô hình: đi từ triệu chứng đến can thiệp

Một quy trình hoàn chỉnh phải chuyển hóa kết quả chẩn đoán thành bước sửa đổi có cơ chế rõ ràng. Mỗi can thiệp chỉ hợp lệ khi trả lời được ba câu hỏi: triệu chứng nào cần xử lý, thành phần toán học nào được thay đổi và tiêu chí hậu kiểm nào xác nhận sự cải thiện là thực chất.

Trên tập `diamonds`, ba nhóm triệu chứng xuất hiện đồng thời: đuôi phải của `price` dày hơn dự báo Gaussian, biên độ phần dư tăng theo `carat` và có sai lệch theo nhóm chất lượng. Tương ứng với đó là ba hướng can thiệp có cơ sở lý thuyết rõ ràng.

### 7.1. Can thiệp 1: biến đổi log để xử lý đuôi phải và nhiễu nhân

Khi biến giá lệch phải mạnh, giả định nhiễu cộng (additive noise) ở thang đo gốc thường không hợp lý bằng giả định nhiễu nhân (multiplicative noise) — nơi biến động theo tỷ lệ phần trăm ổn định hơn biến động tuyệt đối. Khi đó, mô hình:

$$
\log(\text{price}_i) \sim \mathcal N(\mu_i,\sigma)
$$

phản ánh sát hơn cơ chế sinh dữ liệu, giúp phân phối phần dư cân đối hơn, giảm hiện tượng phương sai thay đổi và khắc phục tình trạng khoảng dự đoán quá hẹp ở vùng `carat` lớn.

Tuy nhiên, khi quy đổi dự báo từ thang log về thang giá gốc, cần lưu ý giá trị kỳ vọng của phân phối log-normal không phải là $$\exp(\mu_*)$$ mà là:

$$
\mathbb E[\text{price}_*\mid y,x_*]=\exp\!\left(\mu_*+\frac{\sigma_*^2}{2}\right),
$$

trong đó $$\mu_*$$ và $$\sigma_*$$ là trung bình và độ lệch chuẩn điều kiện trên thang log. Bỏ qua số hạng $$\sigma_*^2/2$$ sẽ dẫn đến ước lượng thấp có hệ thống trên thang đo gốc.

![Minh họa can thiệp 1: log-transform giảm heteroskedasticity và cải thiện coverage ở vùng carat cao]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_log_transform.png)

### 7.2. Can thiệp 2: mô hình hóa quan hệ phi tuyến có kiểm soát

Nếu phần dư vẫn còn độ cong sau khi ổn định thang đo, vấn đề nằm ở dạng hàm trung bình. Khi đó ta mở rộng hàm tuyến tính:

$$
\mu_i=\alpha+\beta\,\text{carat}_i
$$

thành một hàm phi tuyến linh hoạt hơn dựa trên các hàm cơ sở (basis functions như spline):

$$
\mu_i=\alpha+f(\text{carat}_i), \qquad f(\cdot)=\sum_{k=1}^{K} w_k B_k(\cdot),
$$

trong đó phân phối tiên nghiệm trên các trọng số $$w_k$$ đóng vai trò điều chuẩn để tránh quá khớp. Cách làm này giúp đường trung bình bám sát cả đầu thấp lẫn đầu cao của `carat`, cải thiện đồng bộ kết quả PPC theo từng dải giá trị.

![Minh họa can thiệp 2: mô hình phi tuyến bắt được độ cong của quan hệ carat-price tốt hơn mô hình tuyến tính]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_nonlinear.png)

### 7.3. Can thiệp 3: đưa cấu trúc nhóm vào mô hình bằng gộp một phần (partial pooling)

Với các biến phân loại như `cut`, `color`, `clarity`, cách tiếp cận Bayes tự nhiên là dùng mô hình phân cấp (hierarchical model), chẳng hạn cho phép hệ số chặn thay đổi theo nhóm:

$$
\mu_i=\alpha_{g(i)}+f(\text{carat}_i), \qquad \alpha_g\sim\mathcal N(\alpha_0,\tau_\alpha).
$$

Cơ chế **gộp một phần** (partial pooling) dung hòa hai cực đoan: không ép mọi nhóm giống hệt nhau (gộp hoàn toàn — complete pooling), nhưng cũng không để các nhóm ước lượng tách biệt hoàn toàn (không gộp — no pooling). Nhờ đó, các nhóm có ít quan sát được co nhẹ về trung tâm chung một cách có nguyên tắc, giúp giảm phương sai ước lượng và ổn định dự báo ngoài mẫu. Nếu sau bước này PPC theo nhóm vẫn chưa đạt, ta có thể cân nhắc thêm hệ số dốc theo nhóm, tương tác giữa `carat` và chất lượng hoặc phương sai khác nhau theo phân khúc.

![Minh họa can thiệp 3: thêm cấu trúc nhóm giúp calibration theo cut gần dữ liệu quan sát hơn]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_group_effects.png)

### Thử nghiệm: gộp một phần (partial pooling) co các nhóm về trung bình chung

Tăng $$\tau$$ để quan sát sự chuyển dịch từ gộp hoàn toàn sang không gộp và đối chiếu với phân phối hậu nghiệm của $$\tau$$.

<div class="interactive-demo" markdown="1">
<div data-demo="pooling-explainer" data-lang="vi"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

### Khung giải thích (nên đọc chậm): Tính tay hiệu chỉnh Log-Normal và công thức co cụm Partial Pooling

Hai công thức cốt lõi ở mục 7.1 và 7.3 sẽ trở nên cực kỳ rõ ràng khi bạn tự thay số kiểm tra bằng tay:

**1. Kiểm chứng hiệu chỉnh Log-Normal (Can thiệp 1):**
Giả sử mô hình `log(price)` dự đoán cho một viên kim cương cụ thể với phân phối dự báo trên thang log là $$\mathcal{N}(\mu_* = 8.0,\ \sigma_*^2 = 0.4^2)$$:

- Nếu quy đổi ngây thơ bằng $$\exp(\mu_*)$$: ta nhận được $$\exp(8.0) \approx 2\,981$$ USD (đây thực chất là **trung vị** dự đoán, không phải giá kỳ vọng).
- Quy đổi đúng cho **giá kỳ vọng**:
  $$\mathbb{E}[\text{price}_* \mid y, x_*] = \exp\!\left(8.0 + \frac{0.4^2}{2}\right) = \exp(8.08) \approx 3\,229\text{ USD}.$$
- Mức chênh lệch là $$+248$$ USD (tương đương **+8.3%**) chỉ do độ bất đối xứng của hàm mũ. Khi độ nhiễu $$\sigma_*$$ càng lớn, sai lệch do bỏ quên $$\sigma_*^2/2$$ càng nghiêm trọng.

**2. Kiểm chứng cơ chế co cụm Partial Pooling (Can thiệp 3):**
Giả sử trên thang log, trung tâm chung giữa các nhóm chất lượng là $$\alpha_0 = 8.0$$ với phương sai giữa các nhóm $$\tau_\alpha^2 = 0.25$$ (độ chính xác tiên nghiệm $$1/\tau_\alpha^2 = 4$$), còn nhiễu trong từng nhóm có phương sai $$\sigma^2 = 1.0$$. Xét một nhóm hiếm chỉ có $$n_g = 2$$ viên kim cương với trung bình mẫu $$\bar y_g = 9.0$$ (độ chính xác dữ liệu $$n_g/\sigma^2 = 2$$). Hậu nghiệm của hệ số chặn nhóm $$\alpha_g$$ là trung bình trọng số theo độ chính xác:

$$\hat\alpha_g = \frac{\frac{n_g}{\sigma^2}\bar y_g + \frac{1}{\tau_\alpha^2}\alpha_0}{\frac{n_g}{\sigma^2} + \frac{1}{\tau_\alpha^2}} = \frac{2(9.0) + 4(8.0)}{2 + 4} = \frac{50}{6} \approx 8.33.$$

Thay vì tin tuyệt đối vào trung bình noisy $$9.0$$ từ chỉ 2 viên (no pooling), partial pooling kéo ước lượng 2/3 quãng đường về trung tâm chung $$8.0$$. Ngược lại, với một nhóm lớn có $$n_g = 200$$ viên, trọng số dữ liệu là $$200$$ áp đảo hoàn toàn trọng số tiên nghiệm $$4$$, nên ước lượng bám sát dữ liệu của chính nhóm đó.

### 7.4. Tiêu chí đánh giá sau mỗi bước điều chỉnh

Một sửa đổi chỉ được xem là thành công khi vượt qua cùng bộ tiêu chí hậu kiểm (PPC toàn cục, PPC vùng đuôi, PPC theo dải `carat`, chẩn đoán phần dư và tỷ lệ bao phủ ngoài mẫu) và thỏa mãn đồng thời hai điều kiện: giảm rõ rệt sai lệch ở triệu chứng mục tiêu và không làm suy giảm chất lượng ở những vùng trước đó đã ổn định.

Trình tự khuyến nghị là đi từ can thiệp ít xâm lấn đến thay đổi cấu trúc sâu: trước hết xử lý thang đo bằng biến đổi log, tiếp theo xử lý độ cong bằng hàm phi tuyến có điều chuẩn, rồi mới bổ sung cấu trúc nhóm phân cấp. Thứ tự này giúp tách bạch nguyên nhân và kiểm chứng rõ hiệu quả của từng bước.

### 7.5. Minh họa kết quả thử nghiệm qua từng bước can thiệp

Bảng sau tóm tắt một vòng thử nghiệm định hướng trên tập dữ liệu `diamonds` (chia tập huấn luyện/kiểm tra theo tỷ lệ 80/20, đánh giá trên cùng bộ tiêu chí):

| Mô hình minh họa | Tín hiệu cần xử lý | Kết quả quan sát | Diễn giải |
|---|---|---|---|
| Baseline: `price ~ carat` (Gaussian) | Phương sai thay đổi | $$\operatorname{corr}(\lvert e \rvert,\text{carat})\approx 0.579$$ | Biên độ sai số tăng mạnh theo `carat`, bác bỏ giả định nhiễu đồng nhất. |
| Baseline: `price ~ carat` (Gaussian) | Bao phủ ở vùng giá cao | Tỷ lệ bao phủ 90% toàn cục khoảng 0.921, nhưng ở nhóm `carat` cao chỉ khoảng 0.728 | Khoảng dự đoán có vẻ đạt chuẩn toàn cục nhưng thiếu bao phủ nghiêm trọng ở phân khúc quan trọng nhất. |
| Can thiệp 1: `log(price) ~ carat` | Ổn định phương sai theo biến dự báo | $$\operatorname{corr}(\lvert e_{\log} \rvert,\text{carat})\approx 0.269$$ | Chỉ báo phương sai thay đổi giảm rõ rệt, phù hợp với giả thuyết nhiễu nhân. |
| Can thiệp 1: `log(price) ~ carat` | Bao phủ ở vùng `carat` cao | Tỷ lệ bao phủ 90% ở nhóm `carat` cao tăng lên khoảng 0.850 | Chất lượng dự báo ở phân khúc lớn được cải thiện đáng kể so với baseline. |
| Can thiệp 1 (kiểm tra vùng đuôi) | Hiệu chuẩn vùng đuôi | $$Q_{0.95}$$ dự báo hậu nghiệm có xu hướng cao hơn thực tế | Biến đổi log khắc phục tình trạng thiếu bao phủ nhưng có thể hiệu chỉnh quá mức ở đuôi, do đó vẫn cần kiểm tra PPC vùng đuôi riêng. |
| Can thiệp 3 không phân cấp (hiệu ứng cố định thô) | Khác biệt theo nhóm chất lượng | Một số nhóm hiếm có trung bình dự báo tăng vọt bất thường | Minh chứng thực tế cho sự cần thiết của **partial pooling** thay vì ước lượng nhóm tự do hoàn toàn. |

Kết quả cho thấy hiệu ứng của từng can thiệp không mang tính đơn điệu kiểu "càng phức tạp càng tốt". Một can thiệp tốt phải giải quyết đúng triệu chứng mục tiêu mà không tạo ra biến dạng mới ở tầng kiểm tra khác; vì vậy đánh giá hậu kiểm luôn là bước bắt buộc.

## 8. Kết luận phương pháp luận

Tập dữ liệu `diamonds` cho thấy một bài học quan trọng của mô hình hóa Bayes: chỉ số đẹp ở cấp toàn cục có thể che giấu sai lệch nghiêm trọng ở cấp có điều kiện. Thiếu kiểm tra mô hình theo nhiều tầng, ta rất dễ nhầm lẫn giữa "mô hình bắt được tín hiệu" và "mô hình đủ tin cậy để ra quyết định". Chu trình đúng luôn là: khớp mô hình, kiểm tra đa tầng, giải thích sai lệch theo cơ chế, điều chỉnh có mục tiêu rồi kiểm định lại.

## Video tham khảo

- [Multiple Regression, Clearly Explained!!!](https://www.youtube.com/watch?v=EkAQAi3a4js) — StatQuest with Josh Starmer, English. **xem trước**. Giải thích ý nghĩa hệ số hồi quy nhiều biến khi kiểm soát các biến còn lại, phù hợp với cấu trúc đa biến của bài.
- [What is a posterior predictive check and why is it useful?](https://www.youtube.com/watch?v=yDPJnV9vcHs) — Ben Lambert, English. Trình bày kiểm tra dự báo hậu nghiệm, bổ trợ cho luận điểm rằng khớp được mô hình chưa phải điều kiện đủ.
- [Oriol Abril-Pla - Model criticism with ArviZ | Pydata London 26](https://www.youtube.com/watch?v=HHPAzNan7Uw) — PyData, English. Hướng dẫn quy trình phê bình mô hình bằng ArviZ, liên kết trực tiếp chẩn đoán lấy mẫu và PPC thành một quy trình thống nhất.

## Câu hỏi tự luyện

1. Nếu mô hình tái tạo tốt $$\bar y$$ nhưng lệch mạnh ở $$Q_{0.95}(y)$$, bạn sẽ đánh giá thế nào về khả năng ứng dụng mô hình cho phân khúc cao cấp?
2. Trong bài toán dự đoán giá trị, vì sao sai số ở đuôi phải thường gây hệ quả nghiêm trọng hơn sai số ở vùng trung tâm?
3. Khi đã đưa biến `cut` vào mô hình nhưng PPC theo nhóm vẫn chưa đạt, bạn sẽ ưu tiên rà soát giả định cấu trúc nào tiếp theo?
4. Vì sao tỷ lệ bao phủ ngoài mẫu tính riêng theo từng dải `carat` cung cấp nhiều thông tin hơn tỷ lệ bao phủ gộp toàn tập dữ liệu?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*Kết thúc Chapter 4. Bài học tiếp theo: [Chapter 5 - Multiple Predictors và Causal Thinking]({{ site.baseurl }}/contents/vi/chapter05/)*
