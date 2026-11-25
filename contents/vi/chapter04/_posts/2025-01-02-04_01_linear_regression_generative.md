---
layout: post
title: "Bài 4.1: Bayesian Linear Regression - Mô hình Sinh dữ liệu"
chapter: '04'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

Năm 1886, nhà khoa học người Anh Francis Galton ngồi đối chiếu chiều cao của hàng trăm cặp cha mẹ và con cái trưởng thành tại London. Ông không chỉ thấy một đường thẳng đi lên: ông thấy con của những cặp cha mẹ rất cao vẫn dao động rộng quanh một xu hướng trung bình và có khuynh hướng "hồi quy về trung bình". Từ quan sát ấy, thuật ngữ *hồi quy* (regression) ra đời — và ngay từ khoảnh khắc đầu tiên, bản chất của nó không phải là bài toán hình học vẽ đường thẳng, mà là bài toán mô tả một **quá trình sinh dữ liệu ngẫu nhiên**.

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu hồi quy tuyến tính Bayes như một **mô hình sinh dữ liệu** (generative model), thay vì chỉ là bài toán khớp một đường thẳng vào các điểm dữ liệu. Bạn cũng sẽ nắm rõ vai trò của hệ số chặn (intercept), hệ số dốc (slope) và độ nhiễu (noise) trong mô hình, cũng như lý do hồi quy Bayes luôn giữ lại bất định của cả tham số lẫn dự đoán.

> **Ví dụ ngắn.** Khi mô tả mối liên hệ giữa chiều cao và cân nặng, cách tiếp cận truyền thống thường đặt câu hỏi: "Đường thẳng nào khớp dữ liệu tốt nhất?" Trong khi đó, cách tiếp cận Bayes đặt câu hỏi: "Cân nặng của mỗi người được sinh ra quanh một xu hướng trung bình như thế nào, và mức độ bất định của ta về xu hướng đó là bao nhiêu?"
>
> **Câu hỏi tự kiểm tra.** Vì sao không nên hiểu hồi quy Bayes chỉ đơn thuần là việc tìm một đường thẳng duy nhất?


## Kiến thức cần nhớ: Mô hình sinh dữ liệu, Phân phối có điều kiện và Bất định hai tầng

Với người đọc đã có nền tảng đại học (giải tích, đại số tuyến tính, xác suất cơ bản), bước chuyển lớn nhất khi học hồi quy Bayes không nằm ở công thức mới mà ở cách thay đổi góc nhìn trên ba trụ cột:

- **Phân phối có điều kiện và mô hình sinh dữ liệu (Generative Model):** Thay vì xem $$y = \alpha + \beta x + \varepsilon$$ như một phương trình đại số có thêm "rác" $$\varepsilon$$, thống kê Bayes đọc nó như một họ phân phối xác suất $$p(y \mid x, \alpha, \beta, \sigma) = \mathcal{N}(\alpha + \beta x, \sigma^2)$$. Tại mỗi mức $$x$$, không có một giá trị $$y$$ duy nhất mà có cả một phân phối các giá trị khả dĩ.
- **Tham số như biến ngẫu nhiên trên không gian liên tục:** Nếu xác suất đại học quen gán phân phối cho dữ liệu $$y$$, thì suy luận Bayes gán phân phối cho chính các tham số chưa biết $$(\alpha, \beta, \sigma)$$. Khi kết hợp tiên nghiệm và hàm hợp lý qua định lý Bayes, kết quả không phải một điểm tối ưu mà là mật độ xác suất hậu nghiệm $$p(\alpha, \beta, \sigma \mid x, y)$$ trên $$\mathbb{R}^2 \times \mathbb{R}_+$$.
- **Hai tầng bất định (Epistemic vs. Aleatoric Uncertainty):** Bất định về tham số $$(\alpha, \beta)$$ (*bất định nhận thức*) sẽ thu hẹp dần về 0 khi ta thu thập thêm nhiều dữ liệu; ngược lại, nhiễu cá thể $$\sigma$$ (*bất định ngẫu nhiên nội tại*) vẫn tồn tại ngay cả khi cỡ mẫu tiến ra vô cực. Tách bạch hai tầng này là chìa khóa để phân biệt khoảng tin cậy cho trung bình với khoảng dự đoán cho một cá nhân mới.
## 1. Hồi quy không chỉ là vẽ một đường thẳng

Khi mới học hồi quy, nhiều người thường tiếp cận bài toán bằng cách chọn phương trình đường thẳng $$y = \alpha + \beta x$$ rồi tìm các hệ số sao cho tổng bình phương sai số đạt giá trị nhỏ nhất. Cách làm này hữu ích, nhưng dễ tạo ra cảm giác hồi quy chỉ là một kỹ thuật khớp đường mang tính hình học.

Trong hồi quy Bayes, ta đi sâu hơn một bước: đặt câu hỏi dữ liệu được tạo ra từ quá trình nào, vì sao các điểm quan sát không nằm chính xác trên cùng một đường thẳng, và mức độ bất định của ta đối với chính các tham số của đường thẳng đó lớn đến đâu.

## 2. Quá trình sinh dữ liệu của hồi quy tuyến tính

Giả sử ta muốn mô hình hóa mối quan hệ giữa chiều cao $$x$$ và cân nặng $$y$$. Quá trình sinh dữ liệu có thể được mô tả qua ba bước sau.

### Bước 1. Giả định một xu hướng trung bình

Người cao hơn thường có xu hướng nặng hơn. Ta biểu diễn xu hướng trung bình đó bằng:

$$
\mu_i = \alpha + \beta x_i.
$$

Trong đó, $$\alpha$$ là hệ số chặn (intercept) và $$\beta$$ là hệ số dốc (slope).

### Bước 2. Mỗi cá thể dao động quanh xu hướng trung bình

Trên thực tế, không ai nằm chính xác trên đường trung bình vì cân nặng còn chịu ảnh hưởng của nhiều yếu tố khác như khối lượng cơ, chế độ ăn, giới tính, mức độ vận động hay sai số đo lường. Do đó, ta mô hình hóa giá trị quan sát quanh đường trung bình như sau:

$$
y_i \sim \mathcal{N}(\mu_i,\sigma).
$$

Ở đây, $$\sigma$$ biểu thị độ nhiễu (noise) — tức mức độ phân tán của các quan sát quanh đường hồi quy.

![Quá trình sinh dữ liệu của regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_data_generating_process.png)

![Phân phối cân nặng tại một chiều cao cố định]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_distribution_fixed_height.png)

### Bước 3. Thừa nhận sự bất định về các tham số

Ta không biết trước giá trị chính xác của hệ số chặn $$\alpha$$, hệ số dốc $$\beta$$ hay độ nhiễu $$\sigma$$. Vì vậy, ta gán phân phối tiên nghiệm (prior) cho các tham số này, sau đó kết hợp với dữ liệu quan sát để suy luận phân phối hậu nghiệm (posterior).

![Tóm tắt generative story của regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_story_summary.png)

## 3. Ba tham số cốt lõi cần nắm vững

### 3.1. Hệ số chặn $$\alpha$$

Hệ số chặn là giá trị kỳ vọng của $$y$$ khi $$x = 0$$. Dù thuận tiện về mặt toán học, tham số này không phải lúc nào cũng có ý nghĩa trực quan trong thực tế. Chẳng hạn, nếu $$x$$ là chiều cao tính bằng cm, mốc $$x = 0$$ không tồn tại ở người thật. Vì vậy, trong hồi quy Bayes, ta thường dịch tâm (centering) hoặc chuẩn hóa (standardization) biến đầu vào để hệ số chặn mang ý nghĩa dễ diễn giải hơn.

![Intercept sau khi center biến đầu vào]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_intercept_after_centering.png)

### 3.2. Hệ số dốc $$\beta$$

Hệ số dốc cho biết giá trị trung bình của $$y$$ thay đổi bao nhiêu khi $$x$$ tăng thêm 1 đơn vị. Ví dụ, nếu $$\beta = 0.7$$ kg/cm, mỗi 1 cm chiều cao tăng thêm tương ứng với mức tăng trung bình 0.7 kg cân nặng.

![Diễn giải slope trong hồi quy tuyến tính]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_slope_interpretation.png)

### 3.3. Độ nhiễu $$\sigma$$

Độ nhiễu đo mức độ phân tán của các điểm dữ liệu quanh đường hồi quy. Khi $$\sigma$$ nhỏ, các quan sát tập trung sát đường trung bình; khi $$\sigma$$ lớn, dữ liệu phân tán rộng hơn quanh đường đó.

![Diễn giải noise quanh đường hồi quy]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_noise_interpretation.png)

## 4. Hồi quy Bayes khác phương pháp OLS ở đâu?

### Phương pháp OLS trả lời câu hỏi gì?

Phương pháp bình phương tối thiểu thông thường (OLS — Ordinary Least Squares) tập trung tìm một đường thẳng "tốt nhất" duy nhất theo tiêu chí tối thiểu hóa tổng bình phương sai số.

![Góc nhìn point estimate của OLS]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_frequentist_point_estimate.png)

### Hồi quy Bayes trả lời câu hỏi gì?

Hồi quy Bayes đặt câu hỏi rộng hơn: những đường thẳng nào vẫn hợp lý sau khi quan sát dữ liệu, mức độ bất định của hệ số chặn và hệ số dốc là bao nhiêu, và dự đoán cho một quan sát mới có độ bất định lớn đến mức nào. Nói ngắn gọn, OLS cho một đường ước lượng điểm, còn hồi quy Bayes cho một **phân phối gồm nhiều đường thẳng khả dĩ**.

![Góc nhìn bất định của Bayesian regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bayesian_uncertainty_quantification.png)

### 4.1. Các giả định nền cần nêu rõ trước khi suy luận Bayes

Trước khi tính phân phối hậu nghiệm, cần nêu rõ các giả định cơ bản của mô hình hồi quy tuyến tính:

- Quan hệ trung bình có dạng tuyến tính theo các tham số.
- Sai số có kỳ vọng bằng 0.
- Các sai số độc lập có điều kiện với nhau khi biết biến đầu vào.
- Phương sai của sai số không đổi theo biến đầu vào (tính đồng phương sai — homoscedasticity) trong mô hình cơ bản.
- Ở dạng đơn giản nhất, sai số được giả định tuân theo phân phối Chuẩn (Normal).

Cách tiếp cận Bayes không loại bỏ các giả định này; thay vào đó, nó bổ sung tầng bất định cho tham số và giúp ta kiểm tra lại các giả định một cách minh bạch ở bước kiểm định mô hình (model checking).

![Residual distribution quanh đường hồi quy]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_residual_distribution.png)

### Thử nghiệm: phân phối hậu nghiệm của hồi quy là cả một bó đường thẳng

Thêm từng điểm dữ liệu để quan sát bó đường thẳng khả dĩ thu hẹp dần, đồng thời so sánh với đường OLS và đường thực.

<div class="interactive-demo" markdown="1">
<div data-demo="regression-explainer" data-lang="vi"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 5. Vì sao góc nhìn sinh dữ liệu lại quan trọng?

Khi xem hồi quy là một mô hình sinh dữ liệu, ta sẽ chủ động đặt ra những câu hỏi sát thực tế hơn: dữ liệu được tạo ra theo cơ chế nào, giả định phân phối Chuẩn cho phần dư (residual) có phù hợp không, độ nhiễu có đồng nhất trên toàn miền giá trị của $$x$$ không, và dữ liệu mô phỏng từ mô hình có giống dữ liệu quan sát hay không. Đây chính là ranh giới giữa việc "chạy hồi quy xong là dừng" và việc "xây dựng mô hình rồi kiểm tra lại".

## 6. Viết mô hình Bayes đầy đủ

Một mô hình hồi quy tuyến tính Bayes tối giản được viết như sau:

$$
\alpha \sim p(\alpha)
$$

$$
\beta \sim p(\beta)
$$

$$
\sigma \sim p(\sigma)
$$

$$
y_i \sim \mathcal{N}(\alpha + \beta x_i,\sigma)
$$

Từ mô hình này, ta suy luận phân phối hậu nghiệm đồng thời:

$$
p(\alpha,\beta,\sigma \mid x,y).
$$

Điều quan trọng không nằm ở việc học thuộc ký hiệu, mà ở việc hiểu rõ ba thành phần: phân phối tiên nghiệm (prior) biểu diễn niềm tin trước khi có dữ liệu, hàm hợp lý (likelihood) mô tả cơ chế sinh dữ liệu, và phân phối hậu nghiệm (posterior) là kết quả kết hợp hai thành phần đó sau khi quan sát dữ liệu.

### 6.1. Khung hàm hợp lý – tiên nghiệm – hậu nghiệm cho hồi quy

Với tập dữ liệu $$\mathcal D=\{(x_i,y_i)\}_{i=1}^n$$, hàm hợp lý có dạng:

$$
p(y\mid X,\alpha,\beta,\sigma)=\prod_{i=1}^n \mathcal N(y_i\mid \alpha+\beta x_i,\sigma).
$$

Nếu các tham số được giả định độc lập tiên nghiệm, phân phối tiên nghiệm đồng thời là:

$$
p(\alpha,\beta,\sigma)=p(\alpha)p(\beta)p(\sigma).
$$

Theo định lý Bayes, phân phối hậu nghiệm thỏa mãn:

$$
p(\alpha,\beta,\sigma\mid X,y)
\propto p(y\mid X,\alpha,\beta,\sigma)\,p(\alpha,\beta,\sigma).
$$

Đây là khung tư duy xuyên suốt chương này: mọi suy luận về tham số hồi quy đều bắt nguồn từ một mô hình phân phối đồng thời được xác định rõ ràng.

### 6.2. Khoảng bất định cho hệ số dốc: biết trước và chưa biết phương sai nhiễu

Khi phương sai nhiễu được xem là đã biết trước, phân phối hậu nghiệm của hệ số dốc thường có dạng gần phân phối Chuẩn, và khoảng hậu nghiệm 95% cho $$\beta$$ có dạng:

$$
\mu_{\beta\mid D}\pm z_{0.975}\,\sigma_{\beta\mid D}.
$$

Ngược lại, khi phương sai nhiễu chưa biết và phải được suy luận đồng thời từ dữ liệu, phân phối hậu nghiệm biên của $$\beta$$ thường có đuôi dày hơn (trong thiết lập liên hợp là phân phối Student-t), khiến khoảng hậu nghiệm rộng hơn để phản ánh thêm bất định về nhiễu. Vì vậy, khi báo cáo khoảng ước lượng cho hệ số dốc, cần nêu rõ phương sai nhiễu đang được cố định hay được ước lượng từ dữ liệu.

### Giải thích: Từ 3 điểm dữ liệu đến phân phối hậu nghiệm và hai tầng bất định

Để thấy cơ chế Bayes vận hành cụ thể ra sao thay vì dừng ở ký hiệu tổng quát, hãy tự tay tính một mô hình hồi quy nhỏ từ đầu đến cuối.

1. **Dữ liệu đã dịch tâm:** Giả sử ta quan sát $$n = 3$$ điểm $$(x_i, y_i) \in \{(-1, 1),\ (0, 2),\ (1, 5)\}$$, trong đó $$\bar x = 0$$ và $$\sum x_i^2 = 2$$. Giả sử độ nhiễu đã biết là $$\sigma = 1$$ (độ chính xác dữ liệu $$\tau_y = 1/\sigma^2 = 1$$).
2. **Đặt phân phối tiên nghiệm:** Chọn $$\alpha \sim \mathcal{N}(0, 2^2)$$ (độ chính xác tiên nghiệm $$\tau_{\alpha,0} = 1/4 = 0.25$$) và $$\beta \sim \mathcal{N}(0, 1^2)$$ (độ chính xác $$\tau_{\beta,0} = 1$$), độc lập nhau.
3. **Cập nhật hậu nghiệm bằng tay:** Vì $$\sum x_i = 0$$, trong hàm hợp lý không có tích chéo giữa $$\alpha$$ và $$\beta$$, nên hai tham số cập nhật hoàn toàn độc lập:
   - Với hệ số chặn $$\alpha$$: $$\sum y_i = 1 + 2 + 5 = 8$$. Độ chính xác hậu nghiệm là $$\tau_{\alpha \mid D} = 0.25 + 3 = 3.25$$, suy ra trung bình hậu nghiệm $$\mu_{\alpha \mid D} = 8 / 3.25 \approx 2.462$$ và phương sai $$\operatorname{Var}(\alpha \mid D) = 1/3.25 \approx 0.308$$ ($$\text{SD} \approx 0.555$$).
   - Với hệ số dốc $$\beta$$: $$\sum x_i y_i = (-1)(1) + 0(2) + (1)(5) = 4$$. Độ chính xác hậu nghiệm là $$\tau_{\beta \mid D} = 1 + 2 = 3$$, suy ra trung bình hậu nghiệm $$\mu_{\beta \mid D} = 4/3 \approx 1.333$$ và phương sai $$\operatorname{Var}(\beta \mid D) = 1/3 \approx 0.333$$ ($$\text{SD} \approx 0.577$$).
   *(Lưu ý: ước lượng OLS thuần túy là $$\hat\alpha_{\text{OLS}} = 8/3 \approx 2.667$$ và $$\hat\beta_{\text{OLS}} = 4/2 = 2.0$$; phân phối tiên nghiệm tâm tại 0 đã kéo nhẹ cả hai ước lượng về gần 0 — hiện tượng co cụm điều chuẩn tự nhiên của Bayes.)*
4. **Tách hai tầng bất định khi dự đoán tại $$x_{\text{new}} = 1$$:**
   - Giá trị trung bình dự đoán là $$\mathbb{E}[\mu_{\text{new}} \mid D] = 2.462 + 1.333(1) = 3.795$$.
   - **Tầng 1 (bất định đường trung bình):** $$\operatorname{Var}(\mu_{\text{new}} \mid D) = \operatorname{Var}(\alpha \mid D) + 1^2 \operatorname{Var}(\beta \mid D) = 0.308 + 0.333 = 0.641 \implies \text{SD} \approx 0.80$$.
   - **Tầng 2 (dự đoán một quan sát mới $$y_{\text{new}}$$):** Cộng thêm phương sai nhiễu cá thể $$\sigma^2 = 1$$, ta được $$\operatorname{Var}(y_{\text{new}} \mid D) = 0.641 + 1 = 1.641 \implies \text{SD} \approx 1.28$$.

Chỉ với bốn dòng số học, bạn thấy ngay toàn bộ tinh thần hồi quy Bayes: phân phối hậu nghiệm co cụm nhẹ ước lượng OLS, và dự đoán cho một điểm mới luôn gánh thêm phương sai nhiễu $$\sigma^2$$ bên cạnh bất định tham số.

## 7. Một số ví dụ thực tế khác

Hồi quy Bayes được áp dụng rộng rãi trong nhiều lĩnh vực khác nhau:

- **Giá nhà và diện tích:** biến đầu vào $$x$$ là diện tích, biến đầu ra $$y$$ là giá nhà.
- **Điểm thi và số giờ học:** $$x$$ là số giờ ôn tập, $$y$$ là điểm thi.
- **Doanh thu và chi phí quảng cáo:** $$x$$ là ngân sách quảng cáo, $$y$$ là doanh thu.

Trong mọi trường hợp, cấu trúc mô hình sinh dữ liệu đều giống nhau: tồn tại một xu hướng trung bình, các quan sát thực tế dao động quanh xu hướng đó, và ta luôn có mức độ bất định nhất định đối với các tham số điều khiển xu hướng.

## 8. Hồi quy Bayes tạo dự đoán như thế nào?

Giả sử bạn cần dự đoán cân nặng của một người cao 175 cm. Hồi quy Bayes không chỉ trả về một con số duy nhất, mà cung cấp cả giá trị trung bình dự đoán, phần bất định do chưa biết chính xác $$\alpha$$ và $$\beta$$, cùng phần bất định do độ nhiễu cá thể $$\sigma$$. Nhờ đó, ta không chỉ có dự đoán mà còn biết mức độ tin cậy của dự đoán ấy.

### 8.1. Ví dụ minh họa: dự đoán cân nặng ở chiều cao 175 cm

Giả sử sau khi ước lượng mô hình trên dữ liệu chiều cao – cân nặng, phân phối hậu nghiệm tập trung quanh các giá trị điển hình:

$$
\alpha \approx -55,\qquad \beta \approx 0.75,\qquad \sigma \approx 6.
$$

Ba con số này có thể được diễn giải như sau:

- Hệ số chặn $$\alpha \approx -55$$ xác định vị trí hình học của đường trung bình.
- Hệ số dốc $$\beta \approx 0.75$$ cho biết khi chiều cao tăng thêm 1 cm, cân nặng trung bình tăng khoảng 0.75 kg.
- Độ nhiễu $$\sigma \approx 6$$ kg cho thấy ngay cả giữa những người có cùng chiều cao, cân nặng thực tế vẫn dao động đáng kể quanh mức trung bình.

Với một người mới có chiều cao $$x_{\text{new}}=175$$ cm, giá trị trung bình dự đoán theo bộ tham số đại diện là:

$$
\mu_{\text{new}} = \alpha + \beta x_{\text{new}}
\approx -55 + 0.75 \times 175 = 76.25.
$$

Nếu chỉ dùng một bộ tham số duy nhất, ta sẽ kết luận mức cân nặng trung bình hợp lý là khoảng 76.25 kg. Tuy nhiên, hồi quy Bayes không giả định rằng $$\alpha$$ và $$\beta$$ đã được biết chắc chắn. Hãy xem xét vài mẫu tham số rút ra từ phân phối hậu nghiệm:

| Mẫu hậu nghiệm | $$\alpha$$ | $$\beta$$ | $$\sigma$$ | $$\mu_{\text{new}} = \alpha + \beta \cdot 175$$ |
|---|---:|---:|---:|---:|
| 1 | -52 | 0.73 | 5.8 | 75.75 |
| 2 | -58 | 0.77 | 6.1 | 76.75 |
| 3 | -50 | 0.72 | 5.5 | 76.00 |
| 4 | -57 | 0.76 | 6.4 | 76.00 |

Bảng trên cho thấy: ngay cả khi chưa tính đến nhiễu cá thể, bản thân sự bất định về $$\alpha$$ và $$\beta$$ đã tạo ra một **phân phối cho giá trị trung bình dự đoán**. Thay vì khẳng định mức trung bình đúng bằng 76.25 kg, mô hình cho biết vùng giá trị hợp lý của trung bình tại chiều cao 175 cm nằm khoảng từ 75 đến 77 kg.

Từ đây, cần phân biệt rõ hai câu hỏi khác nhau:

**Câu hỏi 1. Cân nặng trung bình của nhóm người cao 175 cm là bao nhiêu?**

Câu hỏi này hướng tới đại lượng $$\mu_{\text{new}}$$. Khi rút nhiều mẫu từ phân phối hậu nghiệm và tính $$\mu_{\text{new}}$$ cho từng mẫu, ta thu được phân phối hậu nghiệm của giá trị trung bình. Giả sử khoảng hậu nghiệm 89% thu được là:

$$
\mu_{\text{new}} \in [74,\ 78.5]\ \text{kg}.
$$

Khoảng này phản ánh **bất định tham số** — tức sự chưa chắc chắn về vị trí chính xác của đường hồi quy.

**Câu hỏi 2. Một cá nhân cụ thể cao 175 cm sẽ nặng bao nhiêu?**

Câu hỏi này khó hơn vì ngoài bất định tham số còn có biến thiên cá thể quanh đường trung bình. Ta cần dùng phân phối dự báo hậu nghiệm (posterior predictive distribution):

$$
y_{\text{new}} \sim \mathcal{N}(\mu_{\text{new}}, \sigma).
$$

Khi lan truyền đồng thời bất định của $$\alpha, \beta, \sigma$$ và nhiễu cá thể, khoảng dự đoán 89% sẽ rộng hơn đáng kể, chẳng hạn:

$$
y_{\text{new}} \in [66,\ 87]\ \text{kg}.
$$

Khoảng thứ hai rộng hơn nhiều vì nó dự đoán cho **một cá nhân cụ thể** thay vì giá trị trung bình của cả nhóm. Điểm khác biệt này thường dễ bị nhầm lẫn:

- Khoảng của $$\mu_{\text{new}}$$ phản ánh bất định về xu hướng trung bình.
- Khoảng của $$y_{\text{new}}$$ phản ánh bất định về một quan sát mới cụ thể.
- Khoảng dự đoán cho $$y_{\text{new}}$$ luôn rộng hơn vì bao hàm cả biến thiên cá thể.

Theo tinh thần mô hình sinh dữ liệu, quy trình dự đoán Bayes gồm bốn bước:

1. Rút một bộ mẫu tham số $$(\alpha^{(s)}, \beta^{(s)}, \sigma^{(s)})$$ từ phân phối hậu nghiệm.
2. Tính giá trị trung bình dự đoán $$\mu_{\text{new}}^{(s)} = \alpha^{(s)} + \beta^{(s)} x_{\text{new}}$$.
3. Sinh một quan sát mới $$y_{\text{new}}^{(s)} \sim \mathcal{N}(\mu_{\text{new}}^{(s)}, \sigma^{(s)})$$.
4. Lặp lại quá trình trên nhiều lần để thu được phân phối dự báo hậu nghiệm.

Như vậy, dự đoán trong hồi quy Bayes không phải là thay số vào một đường thẳng cố định, mà là tạo ra cả một phân phối các giá trị mới hợp lý sau khi đã cập nhật dữ liệu.

### 8.2. Mở rộng từ hồi quy một biến sang nhiều biến (dạng ma trận)

Khi có nhiều biến giải thích, mô hình được viết gọn dưới dạng ma trận:

$$
y=X\mathbf w+\varepsilon,
$$

trong đó $$\mathbf w=(\alpha,\beta_1,\dots,\beta_p)^\top$$ là vector tham số và $$X$$ là ma trận thiết kế (design matrix). Suy luận Bayes khi đó chuyển từ một hệ số dốc sang một vector hệ số, nhưng cấu trúc tư duy không thay đổi: đặt phân phối tiên nghiệm trên $$\mathbf w$$, xác định hàm hợp lý từ cơ chế sinh dữ liệu và suy luận phân phối hậu nghiệm cho toàn bộ vector tham số.

## 9. Thói quen tư duy cần hình thành

Mỗi khi gặp một bài toán hồi quy, hãy lần lượt trả lời năm câu hỏi: dữ liệu được sinh ra từ quá trình nào, đâu là xu hướng trung bình, đâu là phần nhiễu, những tham số nào chưa biết, và khi dự đoán cho quan sát mới thì cần giữ lại những nguồn bất định nào. Thực hành đều đặn chuỗi câu hỏi này sẽ giúp bạn tiếp cận bài toán như một người làm mô hình hóa Bayes thay vì chỉ chạy thuật toán khớp đường.

> **3 ý cần nhớ.** Hồi quy tuyến tính Bayes là một mô hình sinh dữ liệu, trong đó các quan sát dao động quanh một xu hướng trung bình kèm nhiễu; hệ số chặn, hệ số dốc và độ nhiễu đều là các đại lượng chưa biết cần được suy luận bằng phân phối thay vì ước lượng điểm; và ưu điểm cốt lõi của hồi quy Bayes là giữ lại đầy đủ bất định của cả tham số lẫn dự đoán thay vì chỉ đưa ra một đường thẳng duy nhất.

## Video tham khảo

- [The Essence of Linear Regression!!!](https://www.youtube.com/watch?v=aFDOzpTeg0s) — StatQuest with Josh Starmer, English. **xem trước**. Trình bày hồi quy như mô hình trung bình có điều kiện cộng nhiễu, phù hợp với cách tiếp cận không bắt đầu từ bình phương tối thiểu trong bài.
- [Linear Regression, Clearly Explained!!!](https://www.youtube.com/watch?v=7ArmBVF2dCs) — StatQuest with Josh Starmer, English. Minh họa trực quan hệ số chặn, hệ số dốc và phần dư trên đường hồi quy, bổ trợ cho phần diễn giải $$\alpha$$, $$\beta$$ và $$\sigma$$.
- [Statistical Rethinking 2023 - 03 - Geocentric Models](https://www.youtube.com/watch?v=tNOu-SEacNU) — Richard McElreath, English. Trình bày cách viết mô hình hồi quy dưới dạng mô hình sinh trước khi ước lượng, tương ứng với trình tự của bài học.

## Câu hỏi tự luyện

1. Hãy mô tả quá trình sinh dữ liệu cho mối quan hệ giữa số giờ học và điểm thi.
2. Vì sao $$\sigma$$ là một tham số quan trọng của mô hình chứ không chỉ là phần dư phụ thêm?
3. Sự khác biệt cốt lõi giữa "khớp một đường thẳng" (fit a line) và "mô hình hóa một quá trình" (model a process) là gì?
4. Trong công việc hoặc lĩnh vực bạn quan tâm, bài toán hồi quy nào nên được tiếp cận theo hướng mô hình sinh dữ liệu?

## Tài liệu tham khảo

- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4.
- Gelman, A. et al. *Regression and Other Stories*.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapters on regression.

---

*Bài học tiếp theo: [4.2 Priors for Regression - Chọn Prior có Nguyên tắc]({{ site.baseurl }}/contents/vi/chapter04/04_02_priors_for_regression/)*
