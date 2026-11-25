---
layout: post
title: "Bài 4.4: Model Checking và Prediction - Đảm bảo Model Tốt"
chapter: '04'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

Một cỗ máy MCMC có thể chạy trơn tru, cho $$\hat{R} = 1.00$$, số mẫu hiệu dụng lên tới hàng nghìn và khoảng tin cậy 95% của hệ số dốc hẹp như sợi chỉ — nhưng mô hình đó vẫn có thể **sai hoàn toàn**. Lý do rất đơn giản: định lý Bayes chỉ trả lời chính xác *trong phạm vi thế giới giả định của mô hình bạn viết ra*. Muốn biết thế giới giả định ấy có giống thế giới thực hay không, ta phải cho mô hình tự sinh lại dữ liệu và đặt dữ liệu giả lập ấy cạnh dữ liệu thật — bước phê bình mô hình mà George Box gọi là linh hồn của vòng lặp khoa học.

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu rằng việc khớp mô hình (fitting) mới chỉ là nửa đầu của quy trình hồi quy Bayes. Nửa còn lại là kiểm tra xem mô hình có mô tả dữ liệu một cách hợp lý hay không, đồng thời sử dụng phân phối hậu nghiệm để dự đoán dữ liệu mới kèm đầy đủ mức độ bất định. Trọng tâm của bài là kỹ thuật **kiểm tra dự báo hậu nghiệm** (posterior predictive check — PPC) và phân tích phần dư.

> **Ví dụ ngắn.** Một đường hồi quy có thể trông khớp mắt trên biểu đồ phân tán, nhưng nếu dữ liệu giả lập từ mô hình không giống dữ liệu thực tế thì mô hình vẫn đang có vấn đề. Kiểm tra mô hình là cách chủ động chất vấn giả định của chính mình thay vì mặc nhiên tin vào kết quả sau khi chạy xong thuật toán.
>
> **Câu hỏi tự kiểm tra.** Vì sao một phân phối hậu nghiệm "trông gọn đẹp" vẫn chưa đủ cơ sở để kết luận mô hình là tốt?


## Kiến thức cần nhớ: Tích phân dự báo hậu nghiệm, Thống kê kiểm tra và Giải phẫu phần dư

Bước kiểm tra mô hình (model checking) và dự đoán trong thống kê Bayes dựa trên ba khái niệm then chốt:

- **Phân phối dự báo hậu nghiệm (Posterior Predictive Distribution):** Tích phân $$p(\tilde y \mid y) = \int p(\tilde y \mid \theta)p(\theta \mid y)\,d\theta$$ gộp đồng thời bất định tham số $$p(\theta \mid y)$$ và nhiễu sinh dữ liệu $$p(\tilde y \mid \theta)$$. Trong thực hành, nó đóng hai vai trò: dự đoán cho quan sát mới ngoài mẫu và tạo tập dữ liệu tái lập $$y_{\text{rep}}$$ để kiểm tra mô hình.
- **Thống kê kiểm tra $$T(y)$$ và giá trị $$p$$ dự báo hậu nghiệm (Bayesian $$p$$-value):** Thay vì chỉ nhìn mắt thường, ta chọn một hàm thống kê $$T(y)$$ phản ánh khía cạnh quan tâm (trung bình, phương sai, cực đại, độ lệch) rồi đo tỷ lệ mẫu mô phỏng vượt quá giá trị quan sát: $$p_B = P(T(y_{\text{rep}}) \ge T(y_{\text{obs}}) \mid y)$$. Nếu $$p_B$$ quá gần 0 hoặc 1 (chẳng hạn $$<0.05$$ hoặc $$>0.95$$), mô hình đang bỏ sót đặc trưng đó của dữ liệu.
- **Giải phẫu phần dư (Residual Diagnostics):** Phần dư $$e_i = y_i - \mathbb{E}[\tilde y_i \mid y]$$ là "dấu vân tay" của những gì mô hình chưa giải thích được. Hình cong tố cáo quan hệ phi tuyến; hình quạt tố cáo phương sai thay đổi (heteroskedasticity); biểu đồ Q–Q cong chữ S ở hai đầu tố cáo sai số đuôi dày (heavy tails).
## 1. Khớp dữ liệu tốt chưa đồng nghĩa với mô hình tốt

Nhiều người học hồi quy thường dừng lại ngay sau khi ước lượng hệ số dốc và đọc khoảng tin cậy. Tuy nhiên, một quy trình Bayes đầy đủ đòi hỏi ta phải đặt thêm ba câu hỏi quan trọng: mô hình có tái tạo được đặc trưng của dữ liệu quan sát không, phần dư (residual) có còn chứa quy luật có hệ thống nào không, và dự đoán cho dữ liệu mới có hợp lý trong thực tế hay không.

Nhà thống kê George Box có câu nói nổi tiếng:

> “All models are wrong, but some are useful.”

Mục tiêu của việc kiểm tra không phải là tìm ra một mô hình "hoàn hảo tuyệt đối", mà là xác nhận mô hình đủ hữu ích, phản ánh trung thực mức độ bất định và không bỏ sót những cấu trúc quan trọng của dữ liệu.

## 2. Phân phối dự báo hậu nghiệm (Posterior Predictive Distribution) là gì?

Khi đã có phân phối hậu nghiệm $$p(\theta \mid y)$$ của các tham số, ta có thể mô phỏng dữ liệu mới $$\tilde y$$ từ mô hình thông qua phân phối dự báo hậu nghiệm:

$$
p(\tilde y \mid y) = \int p(\tilde y \mid \theta)\,p(\theta \mid y)\,d\theta.
$$

Công thức này là cầu nối trực tiếp giữa suy luận tham số và dự đoán dữ liệu tương lai (hoặc dữ liệu tái tạo từ chính mô hình):

- $$\tilde y$$ là dữ liệu mới hoặc dữ liệu mô phỏng cần dự đoán.
- $$\theta$$ là vector tham số của mô hình.
- $$p(\theta \mid y)$$ thể hiện mức độ hợp lý của từng giá trị tham số sau khi đã quan sát dữ liệu $$y$$.
- $$p(\tilde y \mid \theta)$$ là cơ chế sinh dữ liệu mới khi cố định tham số ở $$\theta$$.

Nói cách khác, tích phân trên là một phép trung bình có trọng số trên mọi khả năng của tham số, trong đó trọng số chính là phân phối hậu nghiệm $$p(\theta \mid y)$$: **những bộ tham số phù hợp với dữ liệu hơn sẽ đóng góp trọng số lớn hơn vào dự đoán cuối cùng**.

Trong thực hành MCMC, tích phân này được xấp xỉ trực tiếp bằng trung bình trên các mẫu hậu nghiệm:

$$
p(\tilde y \mid y) \approx \frac{1}{S}\sum_{s=1}^{S} p(\tilde y \mid \theta^{(s)}), \quad \theta^{(s)} \sim p(\theta \mid y).
$$

Ta chỉ cần rút nhiều mẫu $$\theta^{(s)}$$ từ phân phối hậu nghiệm, ứng với mỗi mẫu sinh ra một tập dữ liệu mới $$\tilde y^{(s)}$$, rồi tổng hợp lại để thu được phân phối dự báo hậu nghiệm.

## 3. Kiểm tra dự báo hậu nghiệm (Posterior Predictive Check — PPC)

PPC đặt ra một câu hỏi thực tế:

> Nếu mô hình của ta mô tả đúng quá trình sinh dữ liệu, liệu dữ liệu giả lập từ mô hình có mang những đặc trưng giống dữ liệu quan sát hay không?

Quy trình gồm ba bước: rút nhiều bộ tham số từ phân phối hậu nghiệm, sinh dữ liệu giả lập từ từng bộ tham số đó và đối chiếu dữ liệu giả lập với dữ liệu thực tế. Nếu dữ liệu giả lập tái hiện được hình dạng phân phối, độ phân tán và các quy luật chính của dữ liệu quan sát, ta có cơ sở vững chắc hơn để tin tưởng mô hình.

![Tóm tắt workflow của posterior predictive check]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_summary.png)

### 3.1. Ví dụ minh họa: hệ số dốc rõ rệt nhưng mô hình vẫn sai cấu trúc

Giả sử ta mô hình hóa mối quan hệ giữa số giờ học và điểm thi bằng một đường thẳng. Phân phối hậu nghiệm của hệ số dốc có thể rất rõ ràng: dương, khoảng tin cậy hẹp và xác suất $$\beta > 0$$ gần bằng 1.

Tuy nhiên, giả sử trên thực tế mối quan hệ đó có tính bão hòa: học thêm giúp điểm tăng nhanh ở giai đoạn đầu nhưng tăng chậm dần khi số giờ học đã cao (đường cong lõm xuống). Khi đó, mô hình đường thẳng sẽ bộc lộ ba dấu hiệu sai lệch:

- PPC sinh ra nhiều điểm dự đoán cao bất hợp lý ở vùng số giờ học lớn.
- Phần dư ở vùng giữa có xu hướng dương, còn phần dư ở hai đầu (học rất ít hoặc rất nhiều) có xu hướng âm, tạo thành mẫu hình cong rõ rệt.
- Đường dự đoán trung bình có vẻ khớp tổng thể nhưng sai lệch có hệ thống tại những vùng giá trị $$x$$ quan trọng.

Ví dụ này cho thấy phân phối hậu nghiệm của tham số có thể rất "chắc chắn" chỉ vì mô hình đang khớp chặt vào một giả định cấu trúc sai. PPC và phân tích phần dư giúp phát hiện chính những sai lệch dạng này.

## 4. Cần kiểm tra những khía cạnh nào trong PPC?

Không có một phép kiểm tra đơn lẻ nào đủ cho mọi bài toán; ta nên đánh giá mô hình từ nhiều góc độ:

### 4.1. Phân phối tổng thể

So sánh biểu đồ tần suất hoặc đường mật độ của dữ liệu giả lập với dữ liệu thực tế để xem hình dạng tổng thể có tương đồng không.

![So sánh phân phối posterior predictive tại một giá trị x đại diện]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_distribution_at_x5.png)

### 4.2. Trung bình, độ phân tán và vùng đuôi

Kiểm tra xem mô hình có tái hiện được giá trị trung bình, phương sai, giá trị cực tiểu/cực đại và hành vi vùng đuôi (tail behavior) của dữ liệu quan sát hay không.

![Kiểm tra mean của dữ liệu quan sát trong posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_test_stat_mean.png)

![Kiểm tra variance của dữ liệu quan sát trong posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_variance_check.png)

### 4.3. Mối quan hệ giữa biến dự báo và biến phản hồi

Trong hồi quy, điều cốt yếu là kiểm tra xem mô hình có tái hiện đúng xu hướng và độ rộng phân tán giữa biến dự báo $$x$$ và biến phản hồi $$y$$ trên toàn miền dữ liệu hay không.

![So sánh dữ liệu quan sát với các mẫu posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_observed_vs_predicted.png)

### 4.4. Thống kê đặc thù theo bài toán

Tùy lĩnh vực, bạn nên bổ sung các đại lượng kiểm tra riêng như tỷ lệ điểm ngoại lai (outlier), độ lệch, độ bất đối xứng hoặc tỷ lệ quan sát vượt một ngưỡng quan trọng.

## 5. Phân tích phần dư (Residual Analysis)

Ngay cả trong hồi quy Bayes, phần dư vẫn là công cụ chẩn đoán sắc bén. Ta thường kiểm tra biểu đồ phần dư theo giá trị ước lượng (residual vs. fitted), phần dư theo biến dự báo, phân phối phần dư và biểu đồ Q–Q để phát hiện phương sai thay đổi (heteroskedasticity), quan hệ phi tuyến (nonlinearity) hoặc sai số có đuôi dày.

Bốn tình huống điển hình dưới đây giúp bạn nhận diện nhanh các dạng sai lệch: mô hình phù hợp, mô hình bỏ sót quan hệ phi tuyến, mô hình có phương sai tăng theo $$x$$ và mô hình có phần dư đuôi dày.

![Residual distribution: quan sát vs posterior predictive]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_ppc_residual_distribution.png)

Ở biểu đồ phân tán dữ liệu gốc, bốn kịch bản này có dạng như sau:

![Scatter plot của mô hình tốt]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_good_model_scatter.png)

![Scatter plot khi quan hệ thật là phi tuyến]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonlinearity_scatter.png)

![Scatter plot khi phương sai tăng theo x]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_scatter.png)

![Scatter plot khi residual có đuôi dày]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_scatter.png)

Trên biểu đồ phần dư theo giá trị ước lượng, mô hình phù hợp sẽ cho phần dư phân bố ngẫu nhiên quanh mức 0, không tạo thành hình cong hay hình quạt:

![Residuals vs fitted của mô hình tốt]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_good_model_residuals.png)

![Residuals vs fitted cho dấu hiệu phi tuyến]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonlinearity_residuals.png)

![Residuals vs fitted cho dấu hiệu heteroskedasticity]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_residuals.png)

![Residuals vs fitted với residual nặng đuôi]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_residuals.png)

Biểu đồ Q–Q cho phép đối chiếu phân phối phần dư với giả định phân phối Chuẩn:

![Q-Q plot của residual trong mô hình tốt]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_good_model_qq.png)

![Q-Q plot khi mô hình bỏ sót phi tuyến]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonlinearity_qq.png)

![Q-Q plot khi có heteroskedasticity]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_heteroskedasticity_qq.png)

![Q-Q plot khi residual có đuôi dày]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bad_nonnormal_qq.png)

Khi phần dư xuất hiện mẫu hình có hệ thống, mô hình nhiều khả năng đang bỏ sót yếu tố phi tuyến, hiệu ứng tương tác (interaction), phương sai thay đổi hoặc một biến giải thích quan trọng.

## 6. Dự đoán Bayes khác gì dự đoán điểm?

Thay vì chỉ trả về một giá trị trung bình duy nhất như hồi quy cổ điển, dự đoán Bayes giữ lại đầy đủ cả bất định của tham số lẫn độ nhiễu của quan sát mới. Nhờ đó, ta không chỉ nêu con số dự đoán (chẳng hạn 72) mà còn chỉ rõ khoảng giá trị hợp lý và mức độ tin cậy đi kèm — thông tin thiết thực hơn nhiều cho việc ra quyết định.

## 7. Khoảng dự đoán và hai nguồn bất định

Một dự đoán Bayes luôn bao gồm hai tầng bất định:

1. **Bất định tham số:** ta chưa biết giá trị chính xác của $$\alpha, \beta, \sigma$$.
2. **Bất định của quan sát mới:** ngay cả khi biết chính xác tham số, từng quan sát thực tế vẫn dao động quanh đường trung bình với độ lệch chuẩn $$\sigma$$.

Vì vậy, **khoảng dự đoán** (prediction interval) cho một quan sát mới luôn rộng hơn khoảng hậu nghiệm của giá trị trung bình (mean response).

### 7.1. Ví dụ ngắn tránh nhầm lẫn hai loại khoảng

Giả sử với nhóm học sinh học 6 giờ, mô hình cho:

- Khoảng hậu nghiệm cho điểm trung bình (mean score): từ 7.4 đến 8.2.
- Khoảng dự đoán cho một học sinh cụ thể mới: từ 6.0 đến 9.3.

Khoảng thứ nhất trả lời câu hỏi về điểm trung bình của cả nhóm học sinh cùng học 6 giờ; khoảng thứ hai trả lời câu hỏi về khoảng điểm khả dĩ của một cá nhân cụ thể. Dùng nhầm khoảng thứ nhất để dự báo cho một cá nhân sẽ tạo ra cảm giác chắc chắn quá mức so với thực tế.

### Giải thích: Tính tay Bayesian $$p$$-value và phân tách hai nguồn phương sai dự đoán

Hãy tự kiểm chứng hai phép tính cốt lõi của kiểm tra mô hình và dự đoán bằng những con số nhỏ gọn:

**1. Tự tính Bayesian $$p$$-value cho độ phân tán:**
Giả sử trên tập dữ liệu thực tế, bạn đo được độ lệch chuẩn mẫu là $$T(y_{\text{obs}}) = 4.2$$. Bạn rút $$S = 10$$ tập dữ liệu giả lập $$y_{\text{rep}}^{(1)}, \dots, y_{\text{rep}}^{(10)}$$ từ phân phối dự báo hậu nghiệm và tính được 10 độ lệch chuẩn mô phỏng:

$$\{2.8,\ 3.0,\ 3.1,\ 3.3,\ 3.4,\ 3.5,\ 3.6,\ 3.7,\ 3.9,\ 4.3\}.$$

Đếm số giá trị $$\ge 4.2$$: chỉ có đúng 1 trên 10 tập ($$4.3$$), nên $$p_B = 1/10 = 0.10$$ (nếu chạy $$S=1000$$ tập và chỉ có 12 tập vượt quá $$4.2$$ thì $$p_B = 0.012$$). Khi $$p_B$$ rất nhỏ như vậy, dữ liệu thực phân tán rộng hơn nhiều so với điều mô hình giả định — ta cần xem lại giả định nhiễu hoặc bổ sung biến giải thích.

**2. Tự phân tách phương sai của $$\mu_{\text{new}}$$ và $$y_{\text{new}}$$:**
Giả sử tại mức 6 giờ học, bất định đường trung bình có $$\mathrm{SD}(\mu_{\text{new}} \mid y) = 0.30$$ (tức phương sai $$0.30^2 = 0.09$$), còn độ nhiễu cá thể quanh đường hồi quy là $$\sigma = 0.80$$ (phương sai $$0.80^2 = 0.64$$). Theo quy tắc cộng phương sai của hai nguồn bất định độc lập:

- **Cho điểm trung bình nhóm:** $$\mathrm{SD}(\mu_{\text{new}} \mid y) = 0.30 \implies$$ khoảng 95% rộng $$\pm 1.96(0.30) \approx \pm 0.59$$ điểm.
- **Cho một học sinh cụ thể:** $$\operatorname{Var}(y_{\text{new}} \mid y) = 0.09 + 0.64 = 0.73 \implies \mathrm{SD}(y_{\text{new}} \mid y) = \sqrt{0.73} \approx 0.854 \implies$$ khoảng 95% rộng $$\pm 1.96(0.854) \approx \pm 1.67$$ điểm.

Ngay cả khi ta thu thập 100.000 học sinh để phương sai đường trung bình giảm từ $$0.09$$ về gần $$0$$, độ lệch chuẩn dự đoán cho một học sinh mới vẫn bị chặn dưới bởi $$\sigma = 0.80$$.

## 8. Kiểm tra mô hình không phải phép thử nhị phân

Đừng nhìn việc kiểm tra mô hình theo lối trắng–đen "hoàn hảo hoặc loại bỏ". Mục đích thực sự là xác định mô hình đang lệch ở đâu, mức độ lệch ra sao và sai lệch đó có ảnh hưởng đến câu hỏi thực tế mà ta cần giải quyết hay không. Một mô hình hơi lệch ở vùng đuôi vẫn có thể dùng tốt nếu mục tiêu chỉ là ước lượng xu hướng trung bình; nhưng nếu bài toán liên quan đến quản trị rủi ro cực trị, chính sai lệch ở đuôi lại là vấn đề nghiêm trọng cần khắc phục.

## 9. Cần làm gì khi mô hình không vượt qua kiểm tra?

Thay vì phản ứng máy móc bằng cách tăng số mẫu MCMC, hãy rà soát mô hình theo ba hướng chính:

- **Cấu trúc mô hình sinh dữ liệu:** có quan hệ phi tuyến, hiệu ứng tương tác hay cấu trúc phân nhóm/phân cấp (hierarchical structure) nào bị bỏ sót không?
- **Phân phối tiên nghiệm:** tiên nghiệm có quá rộng, quá hẹp hoặc tạo ra dự báo tiên nghiệm thiếu hợp lý không?
- **Đặc điểm dữ liệu:** dữ liệu có điểm ngoại lai, sai số đo lường, biến giải thích bị thiếu hoặc phương sai thay đổi đáng kể không?

Chẩn đoán tốt chính là cơ sở trực tiếp cho bước sửa đổi mô hình (model revision) đúng hướng.

## 10. Quy trình khép kín của hồi quy Bayes

Chương 4 xây dựng một quy trình làm việc hoàn chỉnh gồm bảy bước liên kết chặt chẽ: xác định quá trình sinh dữ liệu, chọn phân phối tiên nghiệm có nguyên tắc, suy luận phân phối hậu nghiệm, kiểm tra chẩn đoán hội tụ của bộ lấy mẫu, kiểm tra mô hình bằng PPC và phân tích phần dư, tạo dự đoán kèm bất định, rồi điều chỉnh mô hình khi cần thiết. Khi thực hiện đầy đủ bảy bước này, hồi quy trở thành một quy trình mô hình hóa khoa học thay vì chỉ là thao tác gọi hàm.

## 11. Những sai lầm phổ biến

- **Tin vào phân phối hậu nghiệm mà không kiểm tra mô hình:** hậu nghiệm chỉ có giá trị khi mô hình tạo ra nó mô tả dữ liệu một cách hợp lý.
- **Chỉ đánh giá độ khớp trên dữ liệu huấn luyện:** chất lượng thực sự của mô hình thể hiện rõ nhất ở khả năng dự đoán dữ liệu mới.
- **Chỉ kiểm tra một tiêu chí PPC duy nhất:** một mô hình có thể khớp tốt giá trị trung bình nhưng sai lệch nghiêm trọng về phương sai hoặc vùng đuôi; cần kiểm tra trên nhiều thống kê khác nhau.

## 12. Tổng kết bài học

Hồi quy Bayes không dừng lại ở việc lấy được phân phối hậu nghiệm của tham số. Giá trị thực tiễn của mô hình nằm ở khả năng tái tạo đặc trưng dữ liệu và đưa ra dự đoán trung thực về bất định. Thiếu bước kiểm tra và dự đoán, quy trình hồi quy Bayes mới chỉ hoàn thành một nửa.

> **3 ý cần nhớ.** Kiểm tra dự báo hậu nghiệm (PPC) đánh giá xem mô hình có sinh ra dữ liệu giống dữ liệu thực tế hay không; phân tích phần dư và khoảng dự đoán giúp thẩm định tính hữu ích thực sự của mô hình; và một quy trình Bayes hoàn chỉnh luôn bao gồm kiểm tra, dự đoán và điều chỉnh mô hình khi phát hiện sai lệch.

## Video tham khảo

- [What is a posterior predictive check and why is it useful?](https://www.youtube.com/watch?v=yDPJnV9vcHs) — Ben Lambert, English. **xem trước**. Giải thích bản chất của kiểm tra dự báo hậu nghiệm và lý do cần kiểm tra khả năng tái tạo dữ liệu, khớp với trọng tâm của bài.
- [Quantile-Quantile Plots (QQ plots), Clearly Explained!!!](https://www.youtube.com/watch?v=okjYjClSjOg) — StatQuest with Josh Starmer, English. Hướng dẫn đọc biểu đồ Q–Q, hỗ trợ phần đối chiếu phân phối phần dư với giả định Chuẩn.
- [Residual plots | Exploring bivariate numerical data | AP Statistics | Khan Academy](https://www.youtube.com/watch?v=VamMrPZ-8fc) — Khan Academy, English. Minh họa cách dùng biểu đồ phần dư phát hiện cấu trúc còn sót, bổ trợ cho mục phân tích phần dư.

## Câu hỏi tự luyện

1. Vì sao một mô hình đã chạy hội tụ nhưng chưa qua kiểm tra PPC thì chưa nên tin dùng hoàn toàn?
2. Sự khác nhau giữa bất định của giá trị trung bình dự đoán và bất định của một quan sát mới là gì?
3. Hãy nêu ba đặc trưng bạn có thể so sánh giữa dữ liệu thực tế và dữ liệu mô phỏng từ phân phối dự báo hậu nghiệm.
4. Nếu biểu đồ phần dư xuất hiện dạng cong rõ rệt, bạn sẽ nghi ngờ giả định nào của mô hình đang bị vi phạm?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), chapters on model checking.
- Gelman, A. et al. *Regression and Other Stories*.
- McElreath, R. *Statistical Rethinking* (2nd ed.), chapters on posterior predictive checks.

---

*Bài học tiếp theo: [Bài 4.5 - Case Study Model Checking & Prediction]({{ site.baseurl }}/contents/vi/chapter04/04_05_case_study_model_checking_prediction/)*
