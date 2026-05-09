---
layout: post
title: "Bài 4.6: Case Study Nâng Cao - Model Checking & Prediction Trên Dataset Phức Tạp"
chapter: '04'
order: 6
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần nắm được cách vận hành đầy đủ một Bayesian workflow trên dữ liệu có cấu trúc phức tạp, nơi việc "fit được mô hình" mới chỉ là điều kiện cần chứ chưa bao giờ là điều kiện đủ. Trọng tâm của bài không nằm ở việc có thể viết ra thêm một phương trình hồi quy, mà ở năng lực lập luận: từ chẩn đoán sai lệch, xác định dạng sai lệch, đến đề xuất sửa mô hình sao cho sửa đúng nguyên nhân thay vì sửa theo trực giác kỹ thuật.

> **Ví dụ dẫn nhập.** Trong dữ liệu kim cương, `carat` và `price` có tương quan rất cao, nhưng một mô hình tuyến tính đơn giản vẫn có thể thất bại nghiêm trọng ở đuôi phân phối giá, tức đúng ở vùng "an toàn" nhưng sai ở vùng mang giá trị kinh tế lớn nhất.
>
> **Câu hỏi tự kiểm tra.** Vì sao một chỉ số tổng hợp rất đẹp như tương quan 0.9+ vẫn không đủ để kết luận mô hình đáng tin cho prediction thực chiến?

## 1. Bối cảnh dữ liệu: vì sao `diamonds` là một bài kiểm tra khó

Ta dùng dataset `diamonds` (seaborn), với biến phản hồi `price` và nhiều biến mô tả đồng thời cả kích thước hình học lẫn chất lượng cảm quan như `carat`, `cut`, `color`, `clarity`, `depth`, `table`. Điều làm dataset này có giá trị sư phạm cao là nó buộc ta đối diện với ba lớp phức tạp cùng lúc: quan hệ mạnh nhưng không thuần nhất theo toàn miền predictor, cấu trúc nhóm có ý nghĩa thực chất, và hành vi đuôi của giá trị phản hồi có ảnh hưởng trực tiếp đến chất lượng ra quyết định.

### 1.1. Trích một phần dữ liệu quan sát

| carat | cut | color | clarity | depth | table | price | x | y | z |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|
| 0.23 | Ideal | E | SI2 | 61.5 | 55.0 | 326 | 3.95 | 3.98 | 2.43 |
| 0.21 | Premium | E | SI1 | 59.8 | 61.0 | 326 | 3.89 | 3.84 | 2.31 |
| 0.23 | Good | E | VS1 | 56.9 | 65.0 | 327 | 4.05 | 4.07 | 2.31 |
| 0.29 | Premium | I | VS2 | 62.4 | 58.0 | 334 | 4.20 | 4.23 | 2.63 |
| 0.31 | Good | J | SI2 | 63.3 | 58.0 | 335 | 4.34 | 4.35 | 2.75 |

### 1.2. Tóm tắt định lượng để đặt nền cho lập luận

Với `n = 53,940`, biến `carat` có trung bình xấp xỉ 0.798 và median khoảng 0.70, trong khi `price` có trung bình khoảng 3932.8 nhưng median chỉ khoảng 2401, cho thấy phân phối giá lệch phải đáng kể. Tương quan Pearson giữa `carat` và `price` khoảng 0.922, tức cực kỳ mạnh ở mức tổng thể; tuy vậy, tỷ lệ quan sát rơi vào vùng `price > 15000` vẫn chỉ khoảng 3.07%, và chính vùng nhỏ này lại là nơi mọi sai lệch mô hình trở nên đắt giá nhất nếu bài toán dùng cho định giá cao cấp.

## 2. Từ số liệu đến lập luận: phải chứng minh bằng công thức

Một bài phân tích nghiêm túc không được phép dừng ở câu chữ kiểu "có vẻ" hay "trông như". Mỗi kết luận trọng yếu cần có đối tượng thống kê và phép đo tương ứng.

Hệ số tương quan mẫu giữa `carat` và `price` được xác định bởi

$$
r_{xy}=\frac{\sum_{i=1}^{n}(x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum_{i=1}^{n}(x_i-\bar x)^2}\sqrt{\sum_{i=1}^{n}(y_i-\bar y)^2}},
$$

và cho giá trị khoảng 0.922. Con số này chỉ cho phép ta phát biểu rằng biến động của `carat` và `price` đồng pha mạnh theo nghĩa tuyến tính toàn cục; nó không hề đảm bảo rằng residual đã ngẫu nhiên quanh 0, không hề đảm bảo phương sai sai số đồng nhất, cũng không hề bảo lãnh rằng mô hình dự báo tốt ở đuôi phải. Nói cách khác, tương quan cao là bằng chứng về tín hiệu, chứ chưa phải bằng chứng về tính đúng đắn của cấu trúc mô hình sinh dữ liệu.

Tương tự, phát biểu "đuôi phải hiếm" cũng phải có định nghĩa rõ ràng:

$$
\hat p_{\text{price}>15000}=\frac{1}{n}\sum_{i=1}^{n}\mathbf 1(y_i>15000)\approx 0.0307.
$$

Mặc dù tỷ lệ này chỉ quanh 3%, vùng đuôi lại có trọng số kinh tế vượt trội trong nhiều bài toán thực tế; vì vậy, một mô hình đúng ở trung tâm nhưng sai ở đuôi vẫn là mô hình rủi ro cao nếu mục tiêu ứng dụng là định giá, kiểm soát danh mục cao cấp, hoặc đánh giá kịch bản cực trị.

Cuối cùng, để kiểm tra giả định phương sai đồng nhất, ta có thể dùng chỉ báo định hướng

$$
\operatorname{corr}(\lvert e_i \rvert,x_i), \qquad e_i=y_i-\hat y_i,
$$

vì khi độ lớn residual đồng biến theo predictor thì giả định "một mức nhiễu chung cho toàn miền" trở nên khó bảo vệ về mặt thực nghiệm.

## 3. Mô hình cơ sở: cần thiết như một baseline, nhưng không thể là đích đến

Ta bắt đầu bằng mô hình tuyến tính Gaussian cơ sở

$$
\text{price}_i \sim \mathcal N(\mu_i,\sigma), \qquad \mu_i=\alpha+\beta\,\text{carat}_i,
$$

**không phải vì tin rằng thế giới thật đơn giản đến mức đó, mà vì mọi cải thiện sau này đều cần một điểm chuẩn để so sánh. Baseline là thiết bị đo lường tiến bộ, không phải tuyên ngôn về chân lý**. Trên `diamonds`, baseline thường tái hiện khá tốt xu hướng trung bình, nhưng dễ bộc lộ ba giới hạn: độ rộng sai số tăng theo `carat`, hành vi đuôi phải của `price` bị nén mỏng, và khác biệt cấu trúc theo `cut`/`clarity` chưa được mô tả.

## 4. Posterior predictive checks nhiều tầng: từ toàn cục đến có điều kiện

Trong dữ liệu phức tạp, một PPC duy nhất gần như luôn thiếu. Ta cần một chuỗi kiểm tra có cấu trúc, đi từ câu hỏi rộng đến câu hỏi hẹp, để biết mô hình đúng ở đâu và sai ở đâu.

Ở tầng toàn cục, ta so sánh phân phối quan sát với phân phối posterior predictive để xem mô hình có giữ được đồng thời vị trí trung tâm, độ phân tán và độ dày đuôi hay không; đây là bước loại bỏ nhanh các mô hình sai thô.

![So sánh dữ liệu quan sát và posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_observed_vs_predicted.png)

Ở tầng thống kê mục tiêu, thay vì nói chung chung "nhìn cũng giống", ta buộc mô hình trả lời bằng các đại lượng cụ thể:

$$
T_1(y)=\bar y,\quad T_2(y)=\operatorname{Var}(y),\quad T_3(y)=Q_{0.95}(y),\quad T_4(y)=\mathbf 1(y>15000).
$$

Nếu mô hình khớp tốt $$T_1$$ nhưng lệch đáng kể ở $$T_3$$ hoặc $$T_4$$, kết luận hợp lệ không thể là "mô hình tốt", mà phải là "mô hình tốt ở trung tâm, yếu ở đuôi"; sự phân biệt này có ý nghĩa quyết định khi mục tiêu phân tích liên quan trực tiếp đến rủi ro cao giá trị.

![PPC cho mean]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_test_stat_mean.png)

![PPC cho variance]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_variance_check.png)

Ở tầng có điều kiện theo predictor, ta kiểm tra từng dải `carat` thay vì trộn toàn bộ vào một phân phối chung. Ý tưởng là cùng một mô hình có thể đúng ở vùng trung tâm nhưng sai hệ thống ở vùng `carat` lớn, nơi biên độ biến động giá rộng hơn đáng kể. Về mặt định lượng, ta có thể theo dõi

$$
T_{\text{bin},k}(y)=\operatorname{Var}(y\mid x\in B_k),\qquad T^{(0.95)}_{\text{bin},k}(y)=Q_{0.95}(y\mid x\in B_k),
$$

và so sánh giá trị quan sát với phân phối posterior predictive của từng bin.

Ở tầng theo nhóm chất lượng, dữ liệu như `diamonds` buộc ta kiểm tra khả năng tái tạo khác biệt giữa các nhóm `cut`, `clarity`, `color`. Nếu mô hình chỉ dùng `carat`, việc không tái tạo được trung bình theo nhóm

$$
T_g(y)=\bar y_g
$$

không phải là "lỗi nhỏ", mà là bằng chứng rằng generative story đang thiếu cơ chế cấu trúc quan trọng.

## 5. Residual analysis: nơi mô hình bị chất vấn nghiêm khắc nhất

Nếu PPC cho ta bức tranh ở mức phân phối, residual analysis cho ta kính hiển vi ở cấp cơ chế. Câu hỏi trung tâm không phải "residual có nhỏ không" mà là "residual có còn mang thông tin có cấu trúc không". Khi residual còn cấu trúc, mô hình vẫn chưa học hết quy luật sinh dữ liệu.

![Dấu hiệu heteroskedasticity trên scatter]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_scatter.png)

![Residuals vs fitted: dạng quạt]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_residuals.png)

![Q-Q plot khi đuôi residual lệch]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_qq.png)

Trong case `diamonds`, dạng quạt ở residual-vs-fitted thường gợi ý mạnh rằng độ bất định tăng theo mức giá hoặc kích thước, còn sai lệch ở Q-Q plot cho thấy giả định Normal đơn giản có thể chưa đủ mềm để mô tả đuôi. Hệ quả trực tiếp là prediction interval ở vùng `carat` cao dễ bị hẹp giả tạo nếu ta cố giữ mô hình cơ sở.

## 6. Prediction cho ra quyết định: phân biệt đúng hai loại bất định

Một điểm thường bị bỏ qua trong báo cáo thực hành là sự khác biệt giữa bất định của trung bình điều kiện và bất định của một quan sát mới. Hai đối tượng này được mô tả bởi

$$
p(\mu_*\mid y,x_*) \quad \text{và} \quad p(\tilde y_*\mid y,x_*),
$$

trong đó phân phối thứ hai luôn rộng hơn vì bao gồm cả nhiễu quan sát mới. Nếu dùng khoảng của $$p(\mu_*\mid y,x_*)$$ để phát biểu về một viên kim cương cụ thể, ta đã tạo ra mức tự tin giả tạo ngay từ định nghĩa.

Với bài toán prediction, một chỉ báo vận hành quan trọng là coverage ngoài mẫu:

$$
\text{Coverage}_{90\%}=\frac{1}{m}\sum_{j=1}^{m}\mathbf 1\{y_j^{\text{test}}\in \text{PI}_{90\%}(x_j)\}.
$$

Khi coverage tụt thấp rõ rệt ở vùng `carat` lớn, đó là bằng chứng thực nghiệm rằng model chưa phù hợp cho sử dụng thực chiến ở phân khúc giá cao, bất kể các chỉ số tổng quát có thể đang đẹp.

## 7. Model revision: từ triệu chứng đến can thiệp

Một workflow trưởng thành không dừng ở chẩn đoán; nó phải chuyển chẩn đoán thành can thiệp có cơ chế. Nói cách khác, mỗi thao tác sửa mô hình chỉ được xem là hợp lệ khi ta trả lời được đồng thời ba câu hỏi: triệu chứng nào của dữ liệu đang được xử lý, thành phần toán học nào của mô hình được thay đổi để xử lý triệu chứng ấy, và bằng chứng hậu kiểm nào cho phép kết luận rằng thay đổi đó thực sự có hiệu lực thay vì chỉ làm mô hình "đẹp" hơn về mặt hình thức.

Trong case `diamonds`, ba cụm triệu chứng thường xuất hiện cùng nhau: đuôi phải của `price` dày hơn dự báo của Gaussian đơn giản, biên độ residual tăng theo `carat`, và sai lệch có điều kiện theo nhóm chất lượng. Từ đó, ba hướng can thiệp có cơ sở lý thuyết rõ ràng nhất là biến đổi thang phản hồi, nới lỏng cấu trúc tuyến tính của hàm trung bình, và đưa hiệu ứng nhóm vào generative story.

### 7.1. Can thiệp 1: biến đổi log để xử lý đuôi phải và nhiễu nhân

Khi phân phối `price` lệch phải mạnh, giả định nhiễu cộng (additive noise) ở thang gốc thường không còn phù hợp. Một cách diễn đạt giàu cơ chế hơn là xem sai số theo dạng nhân (multiplicative), tức biến động tương đối ổn định hơn biến động tuyệt đối. Khi đó mô hình

$$
\log(\text{price}_i) \sim \mathcal N(\mu_i,\sigma),
$$

không chỉ là thủ thuật kỹ thuật, mà là một phát biểu về cơ chế sinh dữ liệu: độ bất định tỷ lệ phần trăm hợp lý hơn độ bất định tuyệt đối ở các mức giá rất khác nhau. Hiệu ứng thực tế kỳ vọng sau can thiệp này là phân phối residual cân hơn, chỉ báo heteroskedasticity giảm, và prediction interval ở vùng `carat` lớn bớt hẹp giả tạo.

Tuy nhiên, log-transform kéo theo yêu cầu diễn giải đúng khi quay lại thang gốc. Nếu hậu nghiệm trên thang log có trung bình điều kiện $$\mu_*$$ và độ lệch chuẩn $$\sigma_*$$, giá trị kỳ vọng trên thang giá không đơn thuần là $$\exp(\mu_*)$$ mà là

$$
\mathbb E[\text{price}_*\mid y,x_*]=\exp\!\left(\mu_*+\frac{\sigma_*^2}{2}\right),
$$

vì vậy báo cáo dự báo cần nhất quán với phép biến đổi để tránh underestimation có hệ thống ở thang nguyên thủy.

![Minh hoa can thiep 1: log-transform giam heteroskedasticity va cai thien coverage vung carat cao]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_log_transform.png)

### 7.2. Can thiệp 2: thay tuyến tính cứng bằng cấu trúc phi tuyến có kiểm soát

Nếu residual cho thấy độ cong còn sót lại, vấn đề không nằm ở nhiễu mà nằm ở dạng của hàm trung bình. Khi đó thay đổi đúng chỗ là nới mô hình

$$
\mu_i=\alpha+\beta\,\text{carat}_i
$$

thành một hàm linh hoạt hơn, chẳng hạn

$$
\mu_i=\alpha+f(\text{carat}_i), \qquad f(\cdot)=\sum_{k=1}^{K} w_k B_k(\cdot),
$$

trong đó $$B_k$$ là các basis functions (spline/piecewise basis) và prior trên $$w_k$$ đóng vai trò regularization để tránh overfit. Điểm then chốt là "phi tuyến có kiểm soát" khác về bản chất với việc thêm đa thức tùy ý: ta tăng năng lực biểu diễn đúng phần cong mà residual phát hiện, nhưng vẫn duy trì kỷ luật Bayes bằng prior để giữ khả năng tổng quát hóa.

Kết quả mong đợi sau can thiệp là đường trung bình posterior bám sát hơn ở cả đầu thấp và đầu cao của `carat`, đồng thời PPC có điều kiện theo từng bin của predictor cải thiện đồng bộ thay vì chỉ cải thiện ở trung tâm.

![Minh hoa can thiep 2: mo hinh phi tuyen bat duoc do cong cua quan he carat-price tot hon tuyen tinh]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_nonlinear.png)

### 7.3. Can thiệp 3: đưa cấu trúc nhóm vào generative story bằng partial pooling

Khi dữ liệu chứa các biến phân nhóm như `cut`, `color`, `clarity`, mô hình một biến liên tục khó có thể tái tạo khác biệt cấu trúc giữa các phân khúc chất lượng. Thay vì thêm biến giả độc lập theo kiểu thuần kỹ thuật, cách tiếp cận Bayes tự nhiên hơn là mô hình phân cấp (hierarchical model), ví dụ với intercept theo nhóm:

$$
\mu_i=\alpha_{g(i)}+f(\text{carat}_i), \qquad \alpha_g\sim\mathcal N(\alpha_0,\tau_\alpha).
$$

Partial pooling giúp dung hòa hai cực đoan: không ép mọi nhóm giống hệt nhau (complete pooling), nhưng cũng không để mỗi nhóm tự do quá mức (no pooling). Hệ quả phương pháp luận rất quan trọng là các nhóm ít dữ liệu được "co" về trung tâm một cách có nguyên tắc, từ đó giảm phương sai ước lượng và tăng ổn định dự báo ngoài mẫu.

Nếu sau khi đưa hiệu ứng nhóm mà PPC theo nhóm vẫn chưa đạt, đó là tín hiệu rằng cấu trúc nhóm hiện tại chưa đủ: có thể cần slope theo nhóm, tương tác giữa `carat` và chất lượng, hoặc mô hình hóa sai số khác nhau theo phân khúc.

![Minh hoa can thiep 3: them cau truc nhom giup calibration theo cut gan du lieu quan sat hon]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_46_intervention_group_effects.png)

### 7.4. Giao thức đánh giá sau mỗi can thiệp: khi nào được phép nói "đã tốt hơn"

Một sửa đổi chỉ nên được chấp nhận khi vượt qua đánh giá hậu kiểm theo cùng bộ tiêu chí, bao gồm PPC toàn cục, PPC theo đuôi, PPC có điều kiện theo bin predictor, residual diagnostics, và coverage ngoài mẫu. Về nguyên tắc, mô hình mới cần thỏa hai điều kiện cùng lúc: (i) giảm sai lệch ở triệu chứng mục tiêu, và (ii) không tạo suy giảm đáng kể ở các vùng trước đó vốn đã ổn. Nếu chỉ cải thiện một biểu đồ nhưng làm tệ đi coverage ở vùng quyết định, can thiệp đó chưa thể xem là thành công.

Trình tự can thiệp khuyến nghị cho case này là đi từ thay đổi ít xâm lấn đến thay đổi cấu trúc sâu: trước hết ổn định thang đo bằng log-transform, sau đó xử lý độ cong bằng hàm phi tuyến có regularization, cuối cùng mới mở rộng sang hiệu ứng nhóm phân cấp. Trình tự này giúp ta giữ khả năng truy nguyên nguyên nhân, vì mỗi bước đều có một giả thuyết rõ ràng và một tín hiệu chẩn đoán tương ứng để kiểm chứng.

### 7.5. Kết quả minh họa cụ thể cho các bước can thiệp

Để tránh cảm giác "khuyến nghị chung chung", ta tóm tắt một vòng thử nghiệm định hướng trên chính dataset này (chia train/test 80/20, dùng cùng một bộ tiêu chí đánh giá) nhằm minh họa hướng dịch chuyển của kết quả sau từng can thiệp.

| Mô hình minh họa | Tín hiệu cần sửa | Kết quả quan sát được | Diễn giải |
|---|---|---|---|
| Baseline: `price ~ carat` (Gaussian) | Heteroskedasticity | $$\operatorname{corr}(\lvert e \rvert,\text{carat})\approx 0.579$$ | Biên độ sai số tăng mạnh theo `carat`, nên giả định nhiễu đồng nhất là yếu. |
| Baseline: `price ~ carat` (Gaussian) | Độ tin cậy interval ở vùng giá trị cao | Coverage 90% toàn cục khoảng 0.921, nhưng ở nhóm `carat` cao chỉ khoảng 0.728 | Interval nhìn "đủ rộng" toàn cục nhưng thiếu bao phủ nghiêm trọng đúng ở vùng quan trọng nhất. |
| Can thiệp 1: `log(price) ~ carat` | Ổn định phương sai theo predictor | $\operatorname{corr}(\lvert e_{\log} \rvert,\text{carat})\approx 0.269$ | Chỉ báo heteroskedasticity giảm rõ rệt, phù hợp với giả thuyết nhiễu nhân. |
| Can thiệp 1: `log(price) ~ carat` | Coverage vùng `carat` cao | Coverage 90% ở vùng `carat` cao tăng lên khoảng 0.850 | Dự báo ở phân khúc lớn được cải thiện đáng kể so với baseline. |
| Can thiệp 1 (kiểm tra đuôi) | Calibration tail | $$Q_{0.95}$$ posterior predictive có xu hướng vượt mức quan sát | Bài học quan trọng: log-transform có thể sửa thiếu bao phủ ở vùng cao nhưng cũng có nguy cơ over-correct ở đuôi, nên vẫn cần PPC tail riêng. |
| Can thiệp 3 theo kiểu không phân cấp (fixed effects thô) | Khác biệt theo nhóm chất lượng | Một số nhóm hiếm bị dự báo trung bình vọt bất thường | Đây là minh chứng vì sao cần **partial pooling** thay vì thêm nhóm theo kiểu tự do hoàn toàn. |

Kết quả trên cho thấy thông điệp cốt lõi của step 7: mỗi can thiệp đều có hiệu ứng đo được, nhưng hiệu ứng không đơn điệu theo nghĩa "càng phức tạp càng tốt". Can thiệp đúng là can thiệp làm giảm đúng triệu chứng mục tiêu mà không tạo méo mới ở tầng kiểm tra khác; vì vậy quy trình đánh giá sau sửa mô hình là bắt buộc, không phải phần phụ.

## 8. Kết luận phương pháp luận từ bài 4.6

Case `diamonds` cho thấy một sự thật xuyên suốt của Bayesian modeling: chỉ số đẹp ở cấp tổng thể có thể cùng tồn tại với sai lệch nghiêm trọng ở cấp điều kiện, và nếu thiếu model checking có cấu trúc, ta sẽ dễ nhầm lẫn giữa "mô hình có tín hiệu" và "mô hình đáng tin cho quyết định". Bởi vậy, chu trình đúng không bao giờ là fit rồi kết luận, mà luôn phải là fit, kiểm tra theo nhiều tầng, diễn giải sai lệch bằng ngôn ngữ cơ chế, rồi mới sửa mô hình và đánh giá lại.

## Câu hỏi tự luyện

1. Nếu mô hình tái tạo tốt $$\bar y$$ nhưng trượt mạnh ở $$Q_{0.95}(y)$$, bạn sẽ kết luận thế nào về khả năng dùng mô hình cho phân khúc cao cấp?
2. Trong bối cảnh prediction, vì sao sai số ở đuôi phải thường nguy hiểm hơn sai số ở vùng trung tâm?
3. Khi đã thêm `cut` mà PPC theo nhóm vẫn chưa đạt, bạn sẽ ưu tiên kiểm tra lại giả định cấu trúc nào trước?
4. Vì sao coverage ngoài mẫu theo từng dải `carat` hữu ích hơn coverage gộp toàn bộ dữ liệu?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*Kết thúc Chapter 4. Bài học tiếp theo: [Chapter 5 - Multiple Predictors và Causal Thinking](/vi/chapter05/)*
