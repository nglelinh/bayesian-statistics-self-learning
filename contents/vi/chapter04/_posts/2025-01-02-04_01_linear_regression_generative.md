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

## Mục tiêu học tập

Sau bài này, bạn cần nhìn hồi quy tuyến tính Bayes như một **câu chuyện sinh dữ liệu**, chứ không chỉ là bài toán “fit một đường thẳng”. Bạn cũng cần hiểu vai trò của intercept (hệ số chặn), slope (hệ số dốc) và noise (độ nhiễu) trong mô hình, và vì sao Bayesian regression luôn giữ lại bất định của tham số lẫn dự đoán.

> **Ví dụ mini.** Bạn muốn mô tả mối liên hệ giữa chiều cao và cân nặng. Cách nhìn cũ là “tìm đường thẳng tốt nhất”. Cách nhìn Bayes là “mỗi người có cân nặng được sinh ra quanh một xu hướng trung bình, và ta chưa chắc chắn về xu hướng đó”.
>
> **Câu hỏi tự kiểm tra.** Vì sao regression theo tinh thần Bayes không nên được hiểu đơn giản là tìm một đường thẳng duy nhất?

## 1. Regression không chỉ là vẽ đường thẳng

Khi mới học hồi quy, nhiều người được dạy rằng chỉ cần chọn một đường thẳng $$y = \alpha + \beta x$$ rồi tìm đường làm sai số bình phương nhỏ nhất.

Cách đó hữu ích, nhưng nó dễ khiến ta nghĩ regression chỉ là một kỹ thuật fitting hình học.

Trong Bayesian regression, ta nhìn sâu hơn và buộc mình phải hỏi dữ liệu đến từ đâu, tại sao các điểm không nằm đúng trên một đường, và ta bất định đến mức nào về chính các tham số của đường đó.

## 2. Câu chuyện sinh dữ liệu của hồi quy tuyến tính

Giả sử ta muốn mô hình hóa mối quan hệ giữa chiều cao $$x$$ và cân nặng $$y$$.

Câu chuyện sinh dữ liệu có thể kể như sau.

### Bước 1. Có một xu hướng trung bình

Người cao hơn thường nặng hơn. Ta mô tả xu hướng đó bằng:

$$
\mu_i = \alpha + \beta x_i.
$$

Ở đây $$\alpha$$ là intercept (hệ số chặn) còn $$\beta$$ là slope (hệ số dốc).

### Bước 2. Mỗi cá nhân dao động quanh xu hướng đó

Không ai nằm chính xác trên đường trung bình, vì còn nhiều yếu tố khác như khối cơ, chế độ ăn, giới tính, mức độ vận động, hay sai số đo lường.

Vì vậy ta viết:

$$
y_i \sim \mathcal{N}(\mu_i,\sigma).
$$

Ở đây $$\sigma$$ là độ nhiễu quanh đường hồi quy.

![Quá trình sinh dữ liệu của regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_data_generating_process.png)

![Phân phối cân nặng tại một chiều cao cố định]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_distribution_fixed_height.png)

### Bước 3. Ta chưa biết chính xác các tham số

Ta không biết thật sự intercept là bao nhiêu, slope là bao nhiêu, và noise là bao nhiêu.

Nên ta đặt prior cho chúng, rồi dùng dữ liệu để suy luận posterior.

![Tóm tắt generative story của regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_story_summary.png)

## 3. Ba tham số cần hiểu thật chắc

### 3.1. Intercept $$\alpha$$

Intercept là giá trị trung bình của $$y$$ khi $$x = 0$$.

Về mặt toán học, nó rất tiện. Nhưng về mặt thực tế, nó không phải lúc nào cũng dễ diễn giải.

Ví dụ, nếu $$x$$ là chiều cao tính bằng cm, thì $$x=0$$ hầu như không có ý nghĩa thực tế.

Vì thế trong regression Bayes, ta thường center (đưa biến về quanh trung tâm) hoặc standardize (chuẩn hóa) biến đầu vào để intercept có ý nghĩa dễ đọc hơn.

![Intercept sau khi center biến đầu vào]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_intercept_after_centering.png)

### 3.2. Slope $$\beta$$

Slope cho biết trung bình $$y$$ thay đổi bao nhiêu khi $$x$$ tăng 1 đơn vị.

Ví dụ, nếu $$\beta = 0.7$$ kg/cm, thì mỗi cm chiều cao tăng tương ứng với mức tăng trung bình 0.7 kg cân nặng.

![Diễn giải slope trong hồi quy tuyến tính]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_slope_interpretation.png)

### 3.3. Noise $$\sigma$$

Noise cho biết mức độ các điểm dữ liệu phân tán quanh đường hồi quy. Nếu $$\sigma$$ nhỏ thì dữ liệu bám sát đường hơn, còn nếu $$\sigma$$ lớn thì dữ liệu phân tán mạnh hơn.

![Diễn giải noise quanh đường hồi quy]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_noise_interpretation.png)

## 4. Bayesian regression khác OLS ở đâu?

### OLS thường trả lời

OLS (ordinary least squares, tức bình phương tối thiểu thông thường) thường trả lời câu hỏi về việc đường thẳng “tốt nhất” là gì theo một tiêu chí tối ưu hóa nhất định.

![Góc nhìn point estimate của OLS]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_frequentist_point_estimate.png)

### Bayesian regression trả lời

Bayesian regression thì trả lời một câu hỏi rộng hơn nhiều: những đường thẳng nào còn hợp lý sau khi thấy dữ liệu, mức độ bất định của slope và intercept là bao nhiêu, và dự đoán cho một quan sát mới sẽ bất định đến mức nào. Nói cách khác, OLS cho bạn một đường trung tâm, còn Bayes cho bạn một **phân phối của các đường có thể**.

![Góc nhìn bất định của Bayesian regression]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_bayesian_uncertainty_quantification.png)

### 4.1. Các giả định cổ điển cần nói rõ trước khi suy luận Bayes

Trước khi đi vào posterior, ta nên nhắc rõ các giả định nền của linear regression:

- quan hệ trung bình có dạng tuyến tính theo tham số,
- sai số có kỳ vọng bằng 0,
- sai số độc lập có điều kiện theo biến đầu vào,
- phương sai sai số ổn định (homoscedastic) trong mô hình cơ bản,
- với bản đơn giản nhất, sai số thường được giả sử Normal.

Bayes không "xóa" các giả định này; Bayes chỉ thêm một lớp bất định cho tham số và cho phép ta kiểm tra giả định minh bạch hơn ở bước model checking.

![Residual distribution quanh đường hồi quy]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_regression_residual_distribution.png)

## 5. Vì sao “generative” (sinh dữ liệu) là một từ rất quan trọng?

Nếu bạn xem regression như generative model (mô hình sinh dữ liệu), bạn sẽ tự hỏi đúng những câu hỏi hơn: dữ liệu được sinh ra từ quá trình nào, giả định Normal cho residual (phần dư) có hợp lý không, noise có đồng nhất theo mọi giá trị của $$x$$ không, và mô hình này có thực sự tạo ra dữ liệu giống dữ liệu thật hay không.

Đây là khác biệt rất quan trọng giữa thái độ “fit xong là xong” và thái độ “mô hình hóa rồi kiểm tra”.

## 6. Viết mô hình Bayes đầy đủ

Một Bayesian linear regression tối giản có dạng:

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

Từ đó ta suy ra posterior:

$$
p(\alpha,\beta,\sigma \mid x,y).
$$

Điều quan trọng không phải là thuộc công thức này, mà là hiểu prior (phân phối tiên nghiệm) đang nói điều gì trước dữ liệu, likelihood (hàm hợp lý) đang kể dữ liệu đến từ đâu, và posterior (phân phối hậu nghiệm) là câu trả lời xuất hiện sau khi hai thứ ấy được ghép lại.

### 6.1. Khung joint likelihood - prior - posterior cho hồi quy

Với dữ liệu $$\mathcal D=\{(x_i,y_i)\}_{i=1}^n$$, ta có:

$$
p(y\mid X,\alpha,\beta,\sigma)=\prod_{i=1}^n \mathcal N(y_i\mid \alpha+\beta x_i,\sigma).
$$

Joint prior (nếu giả sử độc lập tiên nghiệm):

$$
p(\alpha,\beta,\sigma)=p(\alpha)p(\beta)p(\sigma).
$$

Từ đó:

$$
p(\alpha,\beta,\sigma\mid X,y)
\propto p(y\mid X,\alpha,\beta,\sigma)\,p(\alpha,\beta,\sigma).
$$

Đây là cách nhìn thống nhất của Buổi 7: mọi suy luận tham số hồi quy đều xuất phát từ một joint model rõ ràng.

### 6.2. Khoảng cho slope: biết phương sai và không biết phương sai

Khi phương sai nhiễu coi như đã biết, posterior của slope thường có dạng gần Normal và khoảng hậu nghiệm cho $$\beta$$ đọc theo kiểu:

$$
\mu_{\beta\mid D}\pm z_{0.975}\,\sigma_{\beta\mid D}.
$$

Khi phương sai chưa biết và được suy luận cùng dữ liệu, hậu nghiệm của $$\beta$$ thường có đuôi dày hơn (thực hành gần Student-t), nên khoảng hậu nghiệm thường rộng hơn để phản ánh thêm bất định.

Vì vậy, khi báo cáo "interval của slope", cần nói rõ bạn đang ở bối cảnh biết hay không biết phương sai nhiễu.

## 7. Một ví dụ thực tế khác ngoài chiều cao - cân nặng

Regression Bayes xuất hiện ở rất nhiều nơi:

### Giá nhà và diện tích

Ở đây $$x$$ có thể là diện tích còn $$y$$ là giá nhà.

### Điểm thi và số giờ học

Ở đây $$x$$ có thể là số giờ ôn tập còn $$y$$ là điểm thi.

### Doanh thu và chi phí quảng cáo

Ở đây $$x$$ có thể là ngân sách quảng cáo còn $$y$$ là doanh thu.

Trong mọi ví dụ đó, tư duy generative (sinh dữ liệu) vẫn giống nhau: có một xu hướng trung bình, dữ liệu thật dao động quanh xu hướng đó, và ta vẫn bất định về chính các tham số điều khiển xu hướng ấy.

## 8. Regression Bayes cho dự đoán như thế nào?

Giả sử bạn muốn dự đoán cân nặng của một người cao 175 cm.

Regression Bayes không chỉ cho một con số duy nhất. Nó cho một giá trị trung bình dự đoán, bất định do chưa chắc về $$\alpha$$ và $$\beta$$, và cả bất định do noise cá thể $$\sigma$$.

Đây là một điểm rất mạnh: ta không chỉ dự đoán, mà còn biết nên tự tin đến đâu vào dự đoán đó.

### 8.1. Một ví dụ cụ thể: dự đoán cân nặng ở 175 cm

Giả sử sau khi fit mô hình trên dữ liệu chiều cao - cân nặng, posterior của ta cho thấy các giá trị điển hình như sau:

$$
\alpha \approx -55,\qquad \beta \approx 0.75,\qquad \sigma \approx 6.
$$

Ta có thể hiểu ba con số này theo ngôn ngữ đời thường như sau:

- intercept khoảng $$-55$$ giúp xác định vị trí của đường trung bình,
- slope khoảng $$0.75$$ nghĩa là cao thêm 1 cm thì cân nặng trung bình tăng khoảng 0.75 kg,
- noise khoảng $$6$$ kg nghĩa là ngay cả ở cùng một chiều cao, cân nặng thực tế của từng người vẫn còn dao động khá đáng kể quanh mức trung bình.

Với một người mới có chiều cao $$x_{\text{new}}=175$$, trung bình dự đoán của mô hình là:

$$
\mu_{\text{new}} = \alpha + \beta x_{\text{new}}
\approx -55 + 0.75 \times 175 = 76.25.
$$

Nếu chỉ nhìn vào một bộ tham số đại diện, ta có thể nói: "với người cao 175 cm, cân nặng trung bình hợp lý theo mô hình là khoảng 76.25 kg". Nhưng Bayesian regression không dừng ở đó, vì nó không giả vờ rằng $$\alpha$$ và $$\beta$$ đã được biết chính xác.

Hãy tưởng tượng posterior cho ta một vài mẫu tham số như sau:

| Mẫu posterior | $$\alpha$$ | $$\beta$$ | $$\sigma$$ | $$\mu_{\text{new}} = \alpha + \beta \cdot 175$$ |
|---|---:|---:|---:|---:|
| 1 | -52 | 0.73 | 5.8 | 75.75 |
| 2 | -58 | 0.77 | 6.1 | 76.75 |
| 3 | -50 | 0.72 | 5.5 | 76.00 |
| 4 | -57 | 0.76 | 6.4 | 76.00 |

Bảng này cho thấy một ý rất quan trọng: ngay cả trước khi tính đến noise cá thể, chỉ riêng việc chưa chắc về intercept và slope cũng đã tạo ra một **phân phối của giá trị trung bình dự đoán**. Nói cách khác, mô hình không nói "chắc chắn là 76.25 kg", mà nói "vùng hợp lý cho giá trị trung bình ở chiều cao 175 cm nằm quanh khoảng 75 đến 77 kg".

Đây là lúc cần tách rất rõ hai câu hỏi khác nhau:

**Câu hỏi 1.** Trung bình cân nặng của những người cao 175 cm là bao nhiêu?

Câu hỏi này nhắm vào $$\mu_{\text{new}}$$. Nếu lấy rất nhiều mẫu từ posterior rồi tính $$\mu_{\text{new}}$$ cho từng mẫu, ta sẽ có một posterior distribution cho giá trị trung bình. Giả sử sau bước này ta thu được khoảng hậu nghiệm 89% xấp xỉ:

$$
\mu_{\text{new}} \in [74,\ 78.5]\ \text{kg}.
$$

Khoảng này phản ánh **bất định tham số**: ta chưa biết hoàn toàn chính xác đường hồi quy nằm ở đâu.

**Câu hỏi 2.** Một cá nhân cụ thể cao 175 cm sẽ nặng bao nhiêu?

Câu hỏi này khó hơn, vì ngoài bất định tham số còn có thêm dao động cá thể quanh đường trung bình. Khi đó ta phải dùng posterior predictive distribution:

$$
y_{\text{new}} \sim \mathcal{N}(\mu_{\text{new}}, \sigma).
$$

Nếu tiếp tục lan truyền cả bất định của $$\alpha,\beta,\sigma$$ lẫn noise mới này, ta có thể nhận được một khoảng dự đoán 89% rộng hơn, chẳng hạn:

$$
y_{\text{new}} \in [66,\ 87]\ \text{kg}.
$$

Khoảng này rộng hơn nhiều so với khoảng cho $$\mu_{\text{new}}$$ vì nó trả lời cho **một người cụ thể**, không phải cho trung bình của cả nhóm người cùng chiều cao.

Đó chính là điểm mà nhiều người mới học regression hay bỏ qua:

- khoảng cho $$\mu_{\text{new}}$$ trả lời về xu hướng trung bình,
- khoảng cho $$y_{\text{new}}$$ trả lời về một quan sát mới thực sự,
- khoảng thứ hai luôn rộng hơn vì nó giữ lại cả biến thiên cá thể.

Nhìn theo tinh thần generative, quy trình dự đoán Bayes thực chất là:

1. Lấy một mẫu từ posterior của $$\alpha,\beta,\sigma$$.
2. Tính $$\mu_{\text{new}}^{(s)} = \alpha^{(s)} + \beta^{(s)} x_{\text{new}}$$.
3. Sinh một giá trị mới $$y_{\text{new}}^{(s)} \sim \mathcal{N}(\mu_{\text{new}}^{(s)}, \sigma^{(s)})$$.
4. Lặp lại rất nhiều lần để tạo posterior predictive distribution.

Vì vậy, regression Bayes cho dự đoán không phải bằng cách "cắm số vào một đường thẳng duy nhất", mà bằng cách tạo ra cả một phân phối của những giá trị mới hợp lý sau khi đã nhìn dữ liệu.

### 8.2. Cầu nối từ hồi quy 1 biến sang nhiều biến (dạng ma trận)

Với nhiều biến giải thích, ta viết:

$$
y=X\mathbf w+\varepsilon,
$$

trong đó $$\mathbf w=(\alpha,\beta_1,\dots,\beta_p)^\top$$ và $$X$$ là ma trận thiết kế.

Khi đó, suy luận Bayes chuyển từ "một slope" sang "một vector hệ số", nhưng tư duy không đổi: prior trên $$\mathbf w$$, likelihood từ mô hình sinh dữ liệu, và posterior cho toàn bộ vector tham số.

## 9. Một thói quen quan trọng từ bài này

Mỗi khi thấy một bài toán regression, hãy tự ép mình đi qua một chuỗi câu hỏi rất cụ thể: dữ liệu đang được sinh ra như thế nào, đâu là xu hướng trung bình, đâu là phần noise, tham số nào còn chưa biết, và khi tạo dự đoán mới thì những bất định nào cần được giữ lại. Nếu làm được như vậy, bạn đã bắt đầu nghĩ như người làm Bayesian modeling (mô hình hóa Bayes) chứ không chỉ như người chạy hồi quy.

> **3 ý cần nhớ.** Bayesian linear regression là một generative model trong đó dữ liệu được sinh quanh một xu hướng trung bình có nhiễu; intercept, slope và noise đều là các đại lượng chưa biết cần được suy luận chứ không chỉ ước lượng bằng một con số điểm; và điểm mạnh của regression Bayes nằm ở chỗ nó giữ lại bất định của cả tham số lẫn dự đoán thay vì chỉ đưa ra một đường thẳng duy nhất.

## Câu hỏi tự luyện

1. Hãy kể generative story cho mối quan hệ giữa số giờ học và điểm thi.
2. Vì sao $$\sigma$$ là một tham số rất quan trọng chứ không chỉ là “phần dư” phụ thêm?
3. Khác biệt lớn nhất giữa “fit a line” và “model a process” là gì?
4. Trong công việc của bạn, bài toán regression nào nên được nhìn theo tinh thần generative?

## Tài liệu tham khảo

- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4.
- Gelman, A. et al. *Regression and Other Stories*.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapters on regression.

---

*Bài học tiếp theo: [4.2 Priors for Regression - Chọn Prior có Nguyên tắc](/vi/chapter04/priors-for-regression/)*
