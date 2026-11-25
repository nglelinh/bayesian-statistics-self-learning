---
layout: post
title: "Bài 2.5: Prior liên hợp và đại số của cập nhật Bayes"
chapter: '02'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter02
lesson_type: required
---

Trước khi máy tính và MCMC ra đời, các nhà thống kê Bayes đối mặt với một bức tường toán học khổng lồ: mẫu số $$p(y) = \int p(y \mid \theta) p(\theta)\,d\theta$$ của định lý Bayes thường không thể tính được bằng giải tích sơ cấp. Để vượt qua bức tường ấy, Howard Raiffa và Robert Schlaifer (1961) đã hệ thống hóa một ý tưởng tuyệt đẹp: chọn phân phối prior sao cho khi nhân với likelihood, phân phối hậu nghiệm quay về **đúng cùng một họ phân phối** với prior — gọi là **prior liên hợp (conjugate prior)**.

Dù ngày nay ta có PyMC và MCMC cho các mô hình tổng quát, việc làm chủ các cặp liên hợp kinh điển (Beta–Binomial, Gamma–Poisson, Normal–Normal) vẫn vô giá: chúng là những ví dụ giải tích trong suốt nhất giúp ta hiểu bản chất phép cập nhật Bayes bằng những phép cộng trừ sơ cấp.

---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu prior liên hợp (conjugate prior) không phải là “mẹo học thuộc”, mà là những cặp prior–likelihood giúp phép cập nhật Bayes có dạng giải tích rất gọn. Bạn cũng cần nắm được ý nghĩa thực tế của các cặp liên hợp phổ biến, biết khi nào chúng hữu ích và khi nào cần chuyển sang các phương pháp tính toán tổng quát hơn.

> **Ví dụ mini.** Nếu prior cho tỷ lệ qua môn là Beta$$(2,2)$$ và dữ liệu mới là 7 sinh viên đậu trên 10 người, posterior trở thành Beta$$(9,5)$$. Ta không phải tìm một họ phân phối mới mà chỉ cần cập nhật hai tham số.
>
> **Câu hỏi tự kiểm tra.** Điều gì làm cho một prior được gọi là “liên hợp” với một likelihood?


## Kiến thức cần nhớ: Họ mũ, Thống kê đủ và Bốn cặp liên hợp kinh điển

Tính liên hợp không phải sự trùng hợp ngẫu nhiên mà xuất phát trực tiếp từ cấu trúc toán học của **họ phân phối mũ (Exponential Family)**:

- **Cấu trúc lõi (Kernel Matching):** Một cặp prior–likelihood là liên hợp khi phần phụ thuộc vào $$\theta$$ của prior có cùng dạng đại số với phần phụ thuộc vào $$\theta$$ của likelihood (nhờ vậy khi nhân lại, ta chỉ cần cộng các số mũ).
- **Cập nhật qua Thống kê đủ (Sufficient Statistics):** Mọi cặp liên hợp đều cập nhật siêu tham số chỉ bằng các thống kê đủ của dữ liệu (như $$(n, \sum y_i)$$ cho Gamma–Poisson và Normal–Normal, hay $$(n, k)$$ cho Beta–Binomial) — giúp cập nhật trực tuyến với bộ nhớ $$O(1)$$.
- **Giới hạn và Cầu nối sang MCMC:** Trong mô hình hồi quy logistic, mô hình hỗn hợp hay mô hình phân cấp nhiều tầng, không tồn tại prior liên hợp cho toàn bộ mô hình. Khi đó ta chuyển sang xấp xỉ lưới (Bài 2.6) và MCMC (Chương 3–4).

---

## Mở đầu: vì sao một số bài toán Bayes có thể giải tay gọn gàng?

Trong các bài trước, ta đã biết:

$$
P(\theta \mid D) \propto P(D \mid \theta)P(\theta).
$$

Về mặt nguyên lý, biểu thức này rất rõ ràng. Tuy nhiên, khi tính toán thực tế, ta phải chuẩn hóa posterior — và tích phân chuẩn hóa thường rất khó giải bằng tay.

Dù vậy, có một số trường hợp đặc biệt mà khi nhân prior với likelihood, posterior vẫn rơi vào **cùng một họ phân phối** với prior. Những trường hợp đó gọi là **prior liên hợp (conjugate prior)**.

![Giới thiệu về các cặp liên hợp]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_intro.png)

Nếu cảm thấy phần này có nhiều công thức, thay vì cố ghi nhớ máy móc, bạn nên đi theo bốn câu hỏi cơ bản:

- Tham số chưa biết thực chất là đại lượng gì?
- Dữ liệu quan sát có dạng như thế nào?
- Likelihood nào mô tả đúng cơ chế sinh dữ liệu đó?
- Có họ prior nào đồng dạng về mặt đại số với likelihood để sau khi nhân lại, posterior vẫn thuộc cùng họ phân phối ban đầu không?

Đi theo đúng trình tự này, các cặp liên hợp quen thuộc sẽ xuất hiện rất tự nhiên:

- Khi dữ liệu đếm số thành công trong $$n$$ phép thử cố định, likelihood là Binomial và prior liên hợp cho xác suất thành công là Beta.
- Khi dữ liệu đếm số lần thử cho đến khi có thành công đầu tiên, likelihood là Geometric và prior liên hợp vẫn là Beta.
- Khi dữ liệu là số sự kiện xảy ra theo thời gian hoặc đơn vị phơi nhiễm, likelihood là Poisson và prior liên hợp cho cường độ là Gamma.
- Khi dữ liệu liên tục dao động quanh một trung bình chưa biết (với phương sai đã biết), ta có cặp Normal–Normal.

Bạn chỉ cần nhận diện mình đang đứng trước bài toán về tỷ lệ, thời gian chờ rời rạc, tốc độ đếm hay trung bình liên tục; phần cập nhật tham số sẽ trở nên dễ theo dõi hơn nhiều.

## 1. Prior liên hợp là gì?

**Ta nói prior $$p(\theta)$$ là liên hợp với likelihood $$p(y \mid \theta)$$ nếu posterior $$p(\theta \mid y)$$ thuộc cùng một họ phân phối với prior.**

Ví dụ: prior Beta $$\rightarrow$$ posterior vẫn là Beta; prior Gamma $$\rightarrow$$ posterior vẫn là Gamma; prior Normal $$\rightarrow$$ posterior vẫn là Normal.

Nhờ tính chất này, ta không cần tìm một họ phân phối mới sau mỗi lần cập nhật mà chỉ cần cập nhật các tham số của họ phân phối ban đầu. Biểu thức posterior vì thế ngắn gọn, dễ diễn giải và rất hữu ích để xây dựng trực giác về sự tương tác giữa prior và dữ liệu.

Trước khi đi sâu, nếu muốn ôn lại vai trò của hàm Gamma, miền tham số của Beta/Gamma/Normal và lưu ý về xấp xỉ Normal, bạn có thể xem lại [Bài 2.1: Phân phối Xác suất](/vi/chapter02/probability-distributions/).

## 2. Trực giác: vì sao tính liên hợp xuất hiện?

Tính liên hợp xuất hiện khi prior và likelihood có “cùng cấu trúc đại số” theo tham số. Chẳng hạn, likelihood Binomial chứa các lũy thừa của $$\theta$$ và $$1-\theta$$, trong khi prior Beta cũng được cấu tạo từ đúng hai thừa số đó. Khi nhân prior với likelihood, ta không làm đổi dạng hàm mà chỉ cộng các số mũ tương ứng, nên posterior vẫn thuộc họ Beta.

Nói ngắn gọn: **tính liên hợp (conjugacy) là sự tương thích về cấu trúc đại số giữa prior và likelihood.**

## 3. Beta–Binomial: cặp liên hợp nền tảng

### 3.1. Mô hình và phép cập nhật

Một giảng viên muốn suy luận tỷ lệ sinh viên qua môn $$\theta$$ dựa trên lớp 40 sinh viên có 31 em qua môn. Nếu xem mỗi sinh viên là một phép thử Bernoulli độc lập, ta có:

$$
Y \mid \theta \sim \text{Binomial}(n,\theta).
$$

Với prior:

$$
\theta \sim \text{Beta}(\alpha,\beta),
$$

posterior tương ứng là:

$$
\theta \mid y \sim \text{Beta}(\alpha + y,\beta + n - y).
$$

Kiểm tra nhanh phần phụ thuộc vào $$\theta$$:

$$
p(\theta)\propto \theta^{\alpha-1}(1-\theta)^{\beta-1}
$$

và

$$
p(y\mid \theta)\propto \theta^y(1-\theta)^{n-y}.
$$

Nhân hai biểu thức lại:

$$
p(\theta\mid y)\propto p(y\mid \theta)p(\theta)
\propto \theta^{\alpha+y-1}(1-\theta)^{\beta+n-y-1},
$$

suy ra:

$$
\theta\mid y\sim \text{Beta}(\alpha+y,\beta+n-y).
$$

Nếu dữ liệu được viết ở dạng từng quan sát Bernoulli $$y_1,\dots,y_n$$ và đặt $$s=\sum_{i=1}^n y_i$$ thì:

$$
\theta\mid y_{1:n}\sim \text{Beta}(\alpha+s,\beta+n-s).
$$

Trung bình hậu nghiệm là:

$$
E[\theta\mid y]=\frac{\alpha+y}{\alpha+\beta+n}.
$$

### 3.2. Ý nghĩa trực giác

Với prior Beta$$(2,2)$$ và dữ liệu 31/40, posterior trở thành Beta$$(33,11)$$. Có thể hiểu prior như đang mang sẵn một số “lần thành công giả định” ($$\alpha$$) và “lần thất bại giả định” ($$\beta$$); khi dữ liệu thực xuất hiện, ta chỉ cần cộng số thành công và thất bại quan sát được vào hai tham số này.

### 3.2.1. Ví dụ cập nhật tuần tự

Tính liên hợp cũng cho thấy sự nhất quán của cập nhật từng đợt. Bắt đầu từ prior Beta$$(2,2)$$:

- Sau đợt 1 (3 sinh viên qua môn trên 4 em), posterior là Beta$$(5,3)$$.
- Sau đợt 2 (thêm 28 sinh viên qua môn trên 36 em), posterior mới là Beta$$(33,11)$$.

Kết quả cuối cùng trùng khớp hoàn toàn với việc cập nhật một lần bằng toàn bộ dữ liệu 31/40.

![Minh họa Beta-Binomial conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/beta_binomial_conjugacy_visual.png)

### 3.3. Các bối cảnh ứng dụng phổ biến

Cặp Beta–Binomial phù hợp với nhiều bài toán thực tế như tỷ lệ mua hàng sau khi xem quảng cáo, tỷ lệ hoàn thành khóa học, tỷ lệ đáp ứng điều trị, tỷ lệ mở email hay tỷ lệ sản phẩm lỗi trong kiểm định chất lượng — nơi dữ liệu là số thành công trong một số lần thử xác định trước.

### Thử nghiệm: Beta–Binomial qua từng lần tung

Tung từng lần, xem Beta(a + k, b + n − k) thay đổi, khoảng 95% và đối chiếu bằng lưới.

<div class="interactive-demo" markdown="1">
<div data-demo="conjugate-explainer" data-lang="vi" data-tab="betabinom"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Beta–Geometric: khi dữ liệu là số lần thử đến thành công đầu tiên

### 4.1. Mô hình và phép cập nhật

Giả sử Nam thi chứng chỉ tiếng Anh cho tới khi đậu và ta muốn suy luận xác suất đậu mỗi lần thi $$\theta$$. Nếu Nam đậu đúng ở lần thứ ba, dữ liệu không phải “3 lần thi có 1 lần đậu” theo kiểu Binomial, mà là chuỗi có thứ tự gồm 2 lần trượt liên tiếp rồi đến 1 lần đậu ở lần thứ ba.

Theo quy ước phân phối Geometric đếm tổng số lần thử cho đến thành công đầu tiên:

$$
Y \mid \theta \sim \text{Geometric}(\theta),
$$

với likelihood:

$$
P(Y=y \mid \theta) = \theta(1-\theta)^{y-1}.
$$

Với prior:

$$
\theta \sim \text{Beta}(\alpha,\beta),
$$

posterior là:

$$
\theta \mid y \sim \text{Beta}(\alpha + 1,\beta + y - 1).
$$

Thật vậy, kết hợp:

$$
p(y\mid \theta)=\theta(1-\theta)^{y-1}\propto \theta^1(1-\theta)^{y-1}
$$

và

$$
p(\theta)\propto \theta^{\alpha-1}(1-\theta)^{\beta-1},
$$

ta thu được:

$$
p(\theta\mid y)\propto \theta^{\alpha}(1-\theta)^{\beta+y-2},
$$

nên:

$$
\theta\mid y\sim \text{Beta}(\alpha+1,\beta+y-1).
$$

Nếu có $$m$$ quan sát độc lập $$y_1,\dots,y_m$$ thì:

$$
p(y_{1:m}\mid \theta)=\prod_{i=1}^m \theta(1-\theta)^{y_i-1}
=\theta^m(1-\theta)^{\sum_{i=1}^m y_i-m},
$$

suy ra posterior là:

$$
\theta\mid y_{1:m}\sim \text{Beta}\left(\alpha+m,\beta+\sum_{i=1}^m y_i-m\right),
$$

với trung bình hậu nghiệm:

$$
E[\theta\mid y_{1:m}]=\frac{\alpha+m}{\alpha+\beta+\sum_{i=1}^m y_i}.
$$

### 4.2. Vì sao vẫn giữ được tính liên hợp?

Likelihood Geometric vẫn gồm hai thừa số quen thuộc:

$$
\theta^1(1-\theta)^{y-1}.
$$

Khi nhân với hạt nhân của prior Beta:

$$
\theta^{\alpha-1}(1-\theta)^{\beta-1},
$$

ta chỉ cộng số mũ của $$\theta$$ và $$1-\theta$$, nên posterior vẫn thuộc họ Beta.

### 4.3. Cách đọc trực giác

Với quan sát “đậu ở lần thứ ba”, dữ liệu cung cấp đúng 1 lần thành công và 2 lần thất bại xảy ra trước đó. Vì vậy, Beta–Geometric rất phù hợp cho các tình huống như thi cho đến khi đậu, chờ đến khách hàng mua đầu tiên, hay đếm số lần thử trước khi hệ thống vận hành thành công lần đầu.

### 4.4. Phân biệt Beta–Geometric và Beta–Binomial

Binomial trả lời câu hỏi “trong $$n$$ lần thử cố định, có bao nhiêu lần thành công?”, còn Geometric trả lời câu hỏi “cần đến lần thử thứ mấy mới xuất hiện thành công đầu tiên?”. Hai mô hình khác nhau về thiết kế thí nghiệm và cơ chế sinh dữ liệu, dù cùng dùng prior Beta vì đều xây dựng trên xác suất thành công và thất bại.

## 5. Gamma–Poisson: khi dữ liệu là số đếm theo thời gian

### 5.1. Mô hình và phép cập nhật

Một tổng đài muốn suy luận số cuộc gọi trung bình mỗi giờ $$\lambda$$. Trong 8 giờ gần nhất, số cuộc gọi quan sát được lần lượt là:

$$
7, 9, 8, 6, 10, 8, 11, 7.
$$

Nếu mô hình hóa số cuộc gọi mỗi giờ bằng Poisson:

$$
Y_i \mid \lambda \sim \text{Poisson}(\lambda),
$$

và đặt prior Gamma theo tham số hóa shape–rate:

$$
\lambda \sim \text{Gamma}(\alpha,\beta),
$$

thì posterior là:

$$
\lambda \mid y_{1:n} \sim \text{Gamma}\left(\alpha + \sum_i y_i,\beta + n\right).
$$

Thật vậy, prior Gamma có hạt nhân:

$$
p(\lambda)\propto \lambda^{\alpha-1}e^{-\beta\lambda},
$$

còn likelihood Poisson cho $$n$$ quan sát là:

$$
p(y_{1:n}\mid \lambda)=\prod_{i=1}^n \frac{e^{-\lambda}\lambda^{y_i}}{y_i!}
\propto \lambda^{\sum_{i=1}^n y_i}e^{-n\lambda}.
$$

Nhân lại ta được:

$$
p(\lambda\mid y_{1:n})\propto p(y_{1:n}\mid \lambda)p(\lambda)
\propto \lambda^{\alpha+\sum_i y_i-1}e^{-(\beta+n)\lambda},
$$

nên:

$$
\lambda\mid y_{1:n}\sim \text{Gamma}\left(\alpha+\sum_i y_i,\beta+n\right),
$$

với trung bình hậu nghiệm:

$$
E[\lambda\mid y]=\frac{\alpha+\sum_i y_i}{\beta+n}.
$$

Trường hợp tổng quát khi mỗi quan sát có mức phơi nhiễm $$t_i$$ và $$Y_i\mid \lambda \sim \text{Poisson}(t_i\lambda)$$, ta thay $$n$$ bằng tổng mức phơi nhiễm:

$$
\lambda\mid y_{1:n}\sim \text{Gamma}\left(\alpha+\sum_i y_i,\beta+\sum_i t_i\right).
$$

### 5.2. Ý nghĩa trực giác

Trong cặp Gamma–Poisson, tổng số sự kiện quan sát được cộng vào tham số hình dạng (shape), còn số khoảng thời gian hoặc tổng mức phơi nhiễm cộng vào tham số tốc độ (rate). Cách cập nhật này phản ánh trực tiếp cả cường độ sự kiện lẫn thời lượng theo dõi.

![Prior Gamma và posterior sau khi thấy dữ liệu đếm]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_prior_posterior.png)

![Tóm tắt công thức cập nhật Gamma-Poisson]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_formula_summary.png)

![Posterior predictive trong mô hình Gamma-Poisson]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_posterior_predictive.png)

![Cập nhật tuần tự trong Gamma-Poisson]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_sequential_updates.png)

### 5.3. Các bối cảnh ứng dụng

Gamma–Poisson thường dùng cho số lỗi hệ thống mỗi ngày, số bệnh nhân nhập viện mỗi ca trực, số đơn hàng mỗi giờ, số sinh viên nghỉ học mỗi tuần hoặc số sự cố an ninh mạng mỗi tháng — nói chung là các bài toán đếm sự kiện trên một đơn vị thời gian hoặc phơi nhiễm.

### 5.4. Quy tắc nhớ nhanh

Tham số shape hậu nghiệm bằng shape tiền nghiệm cộng tổng số sự kiện quan sát được; tham số rate hậu nghiệm bằng rate tiền nghiệm cộng tổng số khoảng thời gian (hoặc đơn vị phơi nhiễm) đã theo dõi.

### 5.5. Ví dụ: cập nhật số sự cố mất điện

Một trạm điện theo dõi số sự cố mất điện hằng tuần với mô hình:

$$
Y_i\mid\lambda \sim \text{Poisson}(\lambda),\quad i=1,\dots,6.
$$

Prior kỹ thuật ban đầu (shape–rate) là:

$$
\lambda \sim \text{Gamma}(\alpha_0=4,\beta_0=2),
$$

ứng với trung bình tiền nghiệm $$E[\lambda]=2$$ sự cố/tuần. Sau 6 tuần, tổng số sự cố ghi nhận là:

$$
\sum_{i=1}^6 y_i = 18.
$$

Posterior là:

$$
\lambda\mid y_{1:6}\sim \text{Gamma}(\alpha_0+\sum y_i,\beta_0+n)
=\text{Gamma}(22,8),
$$

với trung bình hậu nghiệm:

$$
E[\lambda\mid y]=\frac{22}{8}=2.75.
$$

Như vậy, dữ liệu mới kéo ước lượng cường độ sự cố trung bình từ 2 lên 2.75 sự cố/tuần.

### Thử nghiệm: Gamma–Poisson qua từng quan sát

Prior Gamma trên tốc độ λ, cập nhật sau mỗi khoảng quan sát.

<div class="interactive-demo" markdown="1">
<div data-demo="conjugate-explainer" data-lang="vi" data-tab="gammapoisson"></div>
</div>

## 6. Normal–Normal: khi dữ liệu liên tục dao động quanh một trung bình

### 6.1. Mô hình và phép cập nhật

Giả sử bạn muốn suy luận chiều cao trung bình $$\mu$$ của một nhóm sinh viên, với độ lệch chuẩn quan sát $$\sigma$$ đã biết:

$$
Y_i \mid \mu \sim \mathcal{N}(\mu,\sigma^2).
$$

Nếu prior cho $$\mu$$ cũng là phân phối Normal:

$$
\mu \sim \mathcal{N}(\mu_0,\tau_0^2),
$$

thì posterior cho $$\mu$$ vẫn là phân phối Normal. Cụ thể, phần hạt nhân của likelihood theo $$\mu$$ là:

$$
p(y_{1:n}\mid \mu)\propto \exp\left(-\frac{1}{2\sigma^2}\sum_{i=1}^n (y_i-\mu)^2\right)
\propto \exp\left(-\frac{n}{2\sigma^2}(\mu-\bar y)^2\right),
$$

trong đó:

$$
\bar y=\frac{1}{n}\sum_{i=1}^n y_i.
$$

Prior Normal có hạt nhân:

$$
p(\mu)\propto \exp\left(-\frac{(\mu-\mu_0)^2}{2\tau_0^2}\right).
$$

Nhân prior với likelihood và nhóm bình phương hoàn chỉnh theo $$\mu$$, ta thu được:

$$
\mu\mid y_{1:n}\sim \mathcal{N}(\mu_n,\tau_n^2),
$$

với:

$$
\tau_n^2=\left(\frac{1}{\tau_0^2}+\frac{n}{\sigma^2}\right)^{-1}
$$

và

$$
\mu_n=\tau_n^2\left(\frac{\mu_0}{\tau_0^2}+\frac{n\bar y}{\sigma^2}\right)
=\frac{\mu_0/\tau_0^2+n\bar y/\sigma^2}{1/\tau_0^2+n/\sigma^2}.
$$

Nói cách khác:

$$
E[\mu\mid y]=\mu_n,\qquad \mathrm{Var}(\mu\mid y)=\tau_n^2.
$$

### 6.2. Ý nghĩa trực giác

Trung bình hậu nghiệm trong mô hình Normal–Normal là **trung bình có trọng số** giữa trung bình tiền nghiệm $$\mu_0$$ và trung bình mẫu $$\bar y$$, với trọng số tỉ lệ thuận với độ chính xác (nghịch đảo phương sai) của từng nguồn thông tin. Nguồn nào chính xác hơn (prior hẹp hơn, cỡ mẫu lớn hơn, hoặc nhiễu quan sát nhỏ hơn) sẽ chi phối mạnh hơn.

![Prior Normal và posterior sau khi kết hợp với dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_prior_posterior.png)

![Tóm tắt công thức cập nhật Normal-Normal]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_formula_summary.png)

![Ảnh hưởng của kích thước mẫu trong Normal-Normal]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_sample_size_effect.png)

![Trọng số tương đối của prior và dữ liệu trong Normal-Normal]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_prior_data_weights.png)

### 6.3. Các bối cảnh ứng dụng

Normal–Normal thường gặp khi suy luận chiều cao trung bình, điểm trung bình của lớp học, thời gian xử lý trung bình của một quy trình, hoặc sai số đo đạc của cảm biến quanh một giá trị thực chưa biết.

### 6.4. Cách nhớ ngắn gọn

Trong mô hình Normal–Normal, trung bình hậu nghiệm luôn dịch về phía nguồn thông tin có độ chính xác cao hơn, còn phương sai hậu nghiệm co nhỏ lại khi cỡ mẫu tăng hoặc nhiễu quan sát giảm.

### 6.5. Ví dụ: ước lượng Bayes và rủi ro hậu nghiệm trong Normal–Normal

Giả sử cần suy luận thời gian xử lý hồ sơ trung bình $$\mu$$ (tính bằng phút), với phương sai quan sát đã biết:

$$
Y_i\mid\mu \sim \mathcal{N}(\mu,\sigma^2),\quad \sigma^2=25.
$$

Prior từ chuyên gia:

$$
\mu\sim \mathcal{N}(\mu_0=50,\tau_0^2=100).
$$

Quan sát $$n=16$$ hồ sơ cho trung bình mẫu $$\bar y=55$$. Khi đó:

- Phương sai hậu nghiệm:

$$
\tau_n^2=\left(\frac{1}{\tau_0^2}+\frac{n}{\sigma^2}\right)^{-1}
=\left(\frac{1}{100}+\frac{16}{25}\right)^{-1}\approx 1.538.
$$

- Trung bình hậu nghiệm:

$$
\mu_n=\tau_n^2\left(\frac{\mu_0}{\tau_0^2}+\frac{n\bar y}{\sigma^2}\right)
\approx 54.92.
$$

Vậy:

$$
\mu\mid y \sim \mathcal{N}(54.92,1.538).
$$

Dưới hàm tổn thất bình phương, ước lượng Bayes tối ưu là trung bình hậu nghiệm:

$$
\hat\mu_{Bayes}=E[\mu\mid y]=54.92,
$$

và rủi ro hậu nghiệm (posterior risk) tại ước lượng này bằng chính phương sai hậu nghiệm:

$$
R(\hat\mu_{Bayes})=E\left[(\mu-\hat\mu_{Bayes})^2\mid y\right]=\mathrm{Var}(\mu\mid y)=1.538.
$$

So với prior ban đầu, dữ liệu đã kéo ước lượng trung tâm về sát 55 và thu hẹp mạnh độ bất định hậu nghiệm.

### Thử nghiệm: Normal–Normal và trọng số theo độ chính xác

Kéo μ₀, τ₀, σ để thấy posterior là trung bình có trọng số giữa prior và dữ liệu.

<div class="interactive-demo" markdown="1">
<div data-demo="conjugate-explainer" data-lang="vi" data-tab="normalnormal"></div>
</div>

## 7. Cập nhật tuần tự trong mô hình liên hợp

Một lợi ích thiết thực của tính liên hợp là khả năng cập nhật tuần tự rất gọn. Chẳng hạn, khi theo dõi tỷ lệ nhấp quảng cáo hằng ngày bằng Beta–Binomial, bạn chỉ cần lấy posterior ngày hôm qua làm prior cho hôm nay rồi cộng thêm số lượt thành công và thất bại mới. Tương tự với Gamma–Poisson, thông tin mới được hấp thụ ngay qua phép cộng tham số — rất phù hợp với các hệ thống giám sát vận hành và bảng điều khiển thời gian thực.

![Cập nhật tuần tự với prior liên hợp]({{ site.baseurl }}/img/chapter_img/chapter02/sequential_updating_story.png)

## 8. Giới hạn của prior liên hợp

Ta không nên chọn prior chỉ vì tính liên hợp nếu lựa chọn đó phản ánh kém kiến thức thực tế, làm mất cấu trúc quan trọng của bài toán, hoặc khi mô hình có nhiều tầng và nhiều tham số phụ thuộc lẫn nhau (chẳng hạn prior hỗn hợp hai đỉnh hoặc tham số bị ràng buộc miền phức tạp).

Một điểm thường bị bỏ qua là **miền xác định (support) của tham số**. Ngay cả khi phần biểu thức đại số trông quen thuộc, posterior vẫn có thể không rơi vào một họ phân phối chuẩn nếu miền giá trị bị chặn. Ví dụ, nếu tham số $$\theta$$ bị giới hạn trong $$[0,1]$$ nhưng likelihood có dạng Poisson, mật độ chưa chuẩn hóa sẽ có dạng:

$$
\theta^{y+1}e^{-\theta}, \qquad 0 \le \theta \le 1.
$$

Biểu thức này vẫn hoàn toàn hợp lệ cho suy luận Bayes, nhưng không còn thuộc một họ liên hợp dạng đóng quen thuộc như Beta–Binomial hay Gamma–Poisson. Do đó, tính liên hợp đòi hỏi cả sự tương thích đại số lẫn sự khớp nhau về miền giá trị của tham số.

![Prior liên hợp có thể biểu diễn kém khi prior lý tưởng bị chặn miền]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_truncated_prior.png)

![Tổng quan các tình huống conjugacy không còn phù hợp]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_overview.png)

![Mixture prior là ví dụ điển hình khiến conjugate prior trở nên gượng ép]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_mixture_prior.png)

![Cây quyết định nhanh để chọn ở lại với conjugacy hay chuyển sang MCMC]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_decision_tree.png)

Khi bài toán không còn liên hợp, ta chuyển sang xấp xỉ lưới (grid approximation) cho mô hình rất nhỏ hoặc MCMC cho các mô hình tổng quát hơn.

## 9. Chọn cặp liên hợp theo bối cảnh dữ liệu

![Bảng các cặp liên hợp phổ biến]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_table.png)

Thay vì học thuộc bảng công thức, bạn nên gắn mỗi cặp với câu chuyện dữ liệu tương ứng: xác suất thành công trong $$n$$ phép thử cố định dẫn tới Beta–Binomial; số lần thử cho đến thành công đầu tiên dẫn tới Beta–Geometric; cường độ sự kiện đếm theo thời gian dẫn tới Gamma–Poisson; và trung bình của dữ liệu liên tục dẫn tới Normal–Normal.

## 10. Những nhầm lẫn phổ biến

### 10.1. “Prior liên hợp luôn là prior tốt nhất”

Không đúng. Nó chỉ là lựa chọn thuận tiện về mặt tính toán.

### 10.2. “Chỉ cần học thuộc công thức là đủ”

Không đúng. Nếu không hiểu cơ chế sinh dữ liệu và ý nghĩa của tham số, ta rất dễ áp dụng sai mô hình.

### 10.3. “Đã có MCMC thì không cần học prior liên hợp”

Không đúng. Prior liên hợp vẫn là nền tảng xây dựng trực giác về cập nhật Bayes và vẫn được dùng rộng rãi trong nhiều hệ thống cần độ trễ thấp.

## Tóm tắt

**Prior liên hợp là prior đảm bảo posterior thuộc cùng một họ phân phối sau khi cập nhật.** Nhờ tính chất này, các bài toán cơ bản có thể giải tay gọn gàng, dễ diễn giải và cập nhật tuần tự nhanh chóng. Bốn cặp nền tảng cần nắm gồm Beta–Binomial, Beta–Geometric, Gamma–Poisson và Normal–Normal. Tuy nhiên, cần luôn ghi nhớ rằng sự tiện lợi về đại số không đồng nghĩa với mô hình tốt nhất: khi prior liên hợp không còn phản ánh đúng thực tế, ta nên chuyển sang các phương pháp tính toán linh hoạt hơn.


## Giải thích: Công thức cập nhật 3 cặp liên hợp cốt lõi và ví dụ Gamma–Poisson

Bất cứ khi nào nhận ra bài toán thuộc họ liên hợp, bạn chỉ cần làm đúng 3 bước: (1) xác định cặp likelihood–prior khớp miền, (2) tính thống kê đủ từ dữ liệu, và (3) cộng trực tiếp vào siêu tham số của prior:

| Dữ liệu / Likelihood | Prior liên hợp | Thống kê đủ | Công thức cập nhật Hậu nghiệm |
| --- | --- | --- | --- |
| Nhị phân: $$\text{Binomial}(n, p)$$ | $$\text{Beta}(\alpha, \beta)$$ | $$(n, k)$$ | $$\text{Beta}(\alpha + k,\; \beta + n - k)$$ |
| Đếm sự kiện: $$\text{Poisson}(\lambda)$$ | $$\text{Gamma}(\alpha, \beta)$$ (rate) | $$(n, \sum y_i)$$ | $$\text{Gamma}\!\left(\alpha + \sum y_i,\; \beta + n\right)$$ |
| Liên tục (biết $$\sigma^2$$): $$\mathcal{N}(\mu, \sigma^2)$$ | $$\mathcal{N}(\mu_0, \tau_0^2)$$ | $$(n, \bar y)$$ | Độ chính xác $$\tau_n^{-2} = \tau_0^{-2} + \frac{n}{\sigma^2}$$, trung bình $$\mu_n = \tau_n^2\!\left(\frac{\mu_0}{\tau_0^2} + \frac{n\bar y}{\sigma^2}\right)$$ |

### Ví dụ tính toán làm từng bước: Ước lượng tốc độ lỗi máy chủ bằng Gamma–Poisson

Giả sử số lỗi máy chủ mỗi giờ tuân theo $$\text{Poisson}(\lambda)$$. Trước khi nâng cấp hệ thống, đội ngũ đặt prior $$\lambda \sim \text{Gamma}(\alpha = 6, \beta = 2)$$ (tương ứng kỳ vọng ban đầu $$\alpha/\beta = 6/2 = 3.0$$ lỗi/giờ, dựa trên 2 giờ quan sát giả định). Sau nâng cấp, ta theo dõi $$n = 5$$ giờ và ghi nhận số lỗi lần lượt là $$1, 2, 0, 2, 1$$ (tổng $$\sum y_i = 6$$ lỗi).

1. **Cập nhật siêu tham số:**
   $$\alpha_{\text{post}} = 6 + 6 = 12, \qquad \beta_{\text{post}} = 2 + 5 = 7.$$
2. **Phân phối hậu nghiệm:** $$\lambda \mid y \sim \text{Gamma}(12, 7)$$.
3. **Kỳ vọng và độ lệch chuẩn hậu nghiệm:**
   $$\mathbb{E}[\lambda \mid y] = \frac{12}{7} \approx 1.714\text{ lỗi/giờ}, \qquad \mathrm{SD}(\lambda \mid y) = \frac{\sqrt{12}}{7} \approx 0.495\text{ lỗi/giờ}.$$

Ta thấy kỳ vọng hậu nghiệm $$1.714$$ nằm đúng giữa kỳ vọng prior ($$3.0$$) và trung bình mẫu ($$6/5 = 1.2$$), với trọng số $$2/7$$ cho prior và $$5/7$$ cho dữ liệu: $$\frac{2}{7}(3.0) + \frac{5}{7}(1.2) = \frac{12}{7} \approx 1.714$$.

**Hiểu lầm cần tránh:** Nhầm lẫn giữa hai cách tham số hóa của phân phối Gamma: **shape–rate** ($$\alpha, \beta$$ với trung bình $$\alpha/\beta$$) và **shape–scale** ($$\alpha, \theta = 1/\beta$$ với trung bình $$\alpha\theta$$). Khi lập trình bằng `scipy.stats.gamma`, luôn kiểm tra xem thư viện dùng `scale = 1/beta` hay `rate = beta`.

**Kiểm tra nhanh:** Nếu theo dõi thêm 3 giờ nữa và không có lỗi nào ($$0, 0, 0$$), ta chỉ cần cập nhật tiếp từ $$\text{Gamma}(12, 7)$$ thành $$\text{Gamma}(12 + 0, 7 + 3) = \text{Gamma}(12, 10)$$ với kỳ vọng mới giảm xuống $$1.20$$ lỗi/giờ.

---

## Video tham khảo

- [What is a conjugate prior?](https://www.youtube.com/watch?v=aPNrhR0dFi8) — Ben Lambert, English. **xem trước**. Giải thích định nghĩa prior liên hợp và lý do posterior giữ nguyên họ phân phối, giúp hiểu bản chất thay vì học thuộc.
- [Bayesian Updates and Conjugate Priors](https://www.youtube.com/watch?v=GqSX-8AQL90) — Steve Brunton, English. Minh họa quá trình cập nhật Bayes trên các cặp liên hợp quen thuộc cùng ý nghĩa thực tế của chúng.
- [20 - Beta conjugate prior to Binomial and Bernoulli likelihoods](https://www.youtube.com/watch?v=hKYvZF9wXkk) — Ox educ, English. Trình bày chi tiết phép cập nhật Beta–Binomial dựa trên số lần thành công và thất bại.

## Câu hỏi tự luyện

1. Hãy nêu một ví dụ thực tế phù hợp với cặp Beta–Binomial.
2. Beta–Geometric khác Beta–Binomial ở kiểu dữ liệu nào, dù cả hai cùng sử dụng prior Beta?
3. Vì sao Gamma–Poisson phù hợp với dữ liệu đếm theo thời gian?
4. Trong mô hình Normal–Normal, yếu tố nào quyết định trung bình hậu nghiệm nằm gần trung bình tiền nghiệm hay gần trung bình mẫu hơn?
5. Khi nào bạn không nên dùng prior liên hợp dù biết nó thuận tiện về mặt tính toán?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 2.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 6-7.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2-3.

---

*Bài học tiếp theo: [2.6 Grid Approximation - Xấp xỉ Lưới]({{ site.baseurl }}/contents/vi/chapter02/02_06_grid_approximation/)*
