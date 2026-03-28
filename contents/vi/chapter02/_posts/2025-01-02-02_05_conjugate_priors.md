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

## Mục tiêu học tập

Sau bài này, bạn nên hiểu prior liên hợp không phải là “mẹo học thuộc”, mà là những cặp prior-likelihood khiến việc cập nhật Bayes trở nên rất gọn. Bạn cũng nên nhìn được ý nghĩa thực tế của các cặp liên hợp phổ biến, biết khi nào chúng cực kỳ tiện, và khi nào ta nên bỏ chúng để dùng phương pháp tính toán tổng quát hơn.

> **Ví dụ mini.** Nếu prior cho tỷ lệ đậu là Beta$$(2,2)$$ và dữ liệu mới là 7 sinh viên đậu trên 10 em, posterior trở thành Beta$$(9,5)$$. Ta không phải tìm một họ phân phối mới, chỉ cần cập nhật tham số.
>
> **Câu hỏi tự kiểm tra.** Điều gì làm cho một prior được gọi là “liên hợp” với likelihood?

## Mở đầu: vì sao có những bài Bayes giải tay rất đẹp?

Trong các bài trước, ta đã học rằng:

$$
P(\theta \mid D) \propto P(D \mid \theta)P(\theta).
$$

Về mặt ý tưởng, công thức này rất đơn giản. Nhưng khi bắt tay vào tính thật, ta thường gặp một vấn đề: posterior phải được chuẩn hóa, và bước chuẩn hóa đó có thể rất khó.

Thế nhưng có một số bài toán rất “đẹp”. Khi ta nhân prior với likelihood, posterior vẫn rơi vào **cùng một họ phân phối** như prior. Những trường hợp đẹp này được gọi là **prior liên hợp**.

![Giới thiệu về các cặp liên hợp]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_intro.png)

Nếu bạn thấy phần prior liên hợp dễ gây cảm giác “ngợp công thức”, cách tốt nhất không phải là cố nhớ thật nhiều biểu thức ngay từ đầu, mà là giữ trong đầu một chuỗi câu hỏi rất cơ bản nhưng đủ mạnh: 
- tham số chưa biết thực sự là gì, 
- dữ liệu đến dưới dạng nào, 
- likelihood nào mô tả đúng kiểu dữ liệu ấy, 
- và cuối cùng có prior nào có cùng cấu trúc với likelihood đến mức sau khi cập nhật thì posterior vẫn nằm trong đúng họ phân phối ban đầu hay không.

Chỉ cần đi theo bốn câu hỏi đó, bạn sẽ thấy các cặp liên hợp quen thuộc xuất hiện khá tự nhiên. 
- Khi dữ liệu kể câu chuyện “đếm số thành công trong $$n$$ lần thử”, likelihood phù hợp thường là Binomial và prior tự nhiên cho xác suất thành công là Beta; 
- khi dữ liệu là “phải chờ đến lần thử thứ mấy mới có thành công đầu tiên”, ta chuyển sang Geometric nhưng vẫn giữ được prior Beta; 
- khi quan sát là số sự kiện xảy ra theo thời gian, Poisson thường là lựa chọn hợp lý và Gamma trở thành prior liên hợp tự nhiên cho cường độ đếm; 
- còn khi mục tiêu là suy luận trung bình của dữ liệu liên tục dao động quanh một giá trị trung tâm, ta gặp cặp Normal-Normal. 
 
Bạn không cần học thuộc toàn bộ các cặp này ngay ở lần đọc đầu tiên; chỉ cần nhận ra mình đang đứng trước một bài toán về tỷ lệ, thời gian chờ, tốc độ đếm hay trung bình liên tục, phần còn lại sẽ trở nên dễ theo dõi hơn rất nhiều.

## 1. Prior liên hợp là gì?

**Ta nói prior $$p(\theta)$$ là liên hợp với likelihood $$p(y \mid \theta)$$ nếu posterior $$p(\theta \mid y)$$ thuộc cùng họ với prior.**

Ví dụ:

prior Beta  $$\rightarrow$$ posterior vẫn là Beta, prior Gamma  $$\rightarrow$$ posterior vẫn là Gamma, và prior Normal  $$\rightarrow$$ posterior vẫn là Normal.

Ý nghĩa thực tế của hiện tượng này nằm ở chỗ ta không phải phát minh ra một họ phân phối mới sau mỗi lần cập nhật Bayes, mà chỉ cần điều chỉnh một số tham số của họ phân phối vốn đã quen thuộc; vì vậy, biểu thức posterior thường gọn, trong sáng, và đặc biệt hữu ích cho việc xây trực giác về cách prior và dữ liệu tương tác với nhau.

Trước khi đi sâu, nếu bạn muốn ôn nhanh vai trò hàm Gamma, miền tham số của Beta/Gamma/Normal, và lưu ý xấp xỉ Normal, xem lại phần bổ sung ở [Bài 2.1: Phân phối Xác suất](/vi/chapter02/probability-distributions/).

## 2. Trực giác: vì sao liên hợp xuất hiện?

Liên hợp xuất hiện khi prior và likelihood có “cùng chất liệu đại số”, nghĩa là khi viết chúng ra dưới dạng hàm của tham số, ta thấy chúng được tạo nên từ cùng những khối biểu thức cơ bản. Chẳng hạn, likelihood Binomial tạo ra các lũy thừa của $$\theta$$ và $$1-\theta$$, trong khi prior Beta cũng được xây đúng từ hai thành phần đó; vì vậy, khi nhân prior với likelihood, ta không làm thay đổi họ hàm mà chỉ cộng các số mũ lại với nhau, và chính điều này giải thích tại sao posterior vẫn tiếp tục là một phân phối Beta.

Nói ngắn gọn:

**Conjugacy là sự ăn khớp giữa hình dạng của prior và hình dạng của likelihood.**

## 3. Beta-Binomial: ví dụ quan trọng nhất để bắt đầu

### 3.1. Câu chuyện thực tế

Một giáo viên muốn suy luận tỷ lệ sinh viên qua môn $$\theta$$. Có 40 sinh viên và 31 em qua môn.

Nếu mỗi sinh viên được xem như một phép thử thành công-thất bại độc lập, ta dùng:

$$
Y \mid \theta \sim \text{Binomial}(n,\theta).
$$

Giả sử prior là:

$$
\theta \sim \text{Beta}(\alpha,\beta).
$$

Khi đó posterior là:

$$
\theta \mid y \sim \text{Beta}(\alpha + y,\beta + n - y).
$$

Nếu muốn thấy rõ phép biến đổi đại số, ta chỉ cần nhìn phần phụ thuộc vào $$\theta$$:

$$
p(\theta)\propto \theta^{\alpha-1}(1-\theta)^{\beta-1}
$$

và:

$$
p(y\mid \theta)\propto \theta^y(1-\theta)^{n-y}.
$$

Do đó:

$$
p(\theta\mid y)\propto p(y\mid \theta)p(\theta)
\propto \theta^{\alpha+y-1}(1-\theta)^{\beta+n-y-1},
$$

nên:

$$
\theta\mid y\sim \text{Beta}(\alpha+y,\beta+n-y).
$$

Nếu dữ liệu được viết dưới dạng $$y_1,\dots,y_n$$ với mỗi quan sát là Bernoulli, đặt $$s=\sum_{i=1}^n y_i$$ thì ta cũng có:

$$
\theta\mid y_{1:n}\sim \text{Beta}(\alpha+s,\beta+n-s).
$$

Từ đó, posterior mean là:

$$
E[\theta\mid y]=\frac{\alpha+y}{\alpha+\beta+n}.
$$

### 3.2. Ý nghĩa trực giác

Nếu prior là Beta$$(2,2)$$ và dữ liệu là 31/40, posterior thành Beta$$(33,11)$$.

Đọc bằng lời, prior giống như đang mang sẵn một lượng thông tin ban đầu có thể được hiểu như vài “lần thành công giả tưởng” và vài “lần thất bại giả tưởng”; khi dữ liệu thật xuất hiện, ta chỉ việc cộng thông tin mới đó vào, và posterior là kết quả tổng hợp giữa niềm tin ban đầu với bằng chứng quan sát được.

### 3.2.1. Một ví dụ cập nhật tuần tự rất trực tiếp

Ta cũng có thể thấy vẻ đẹp của conjugacy qua cập nhật từng đợt. Bắt đầu với prior Beta$$(2,2)$$:

- Sau đợt 1, nếu thấy 3 sinh viên qua môn trên 4 em, posterior là Beta$$(5,3)$$.
- Sau đợt 2, nếu quan sát thêm 28 sinh viên qua môn trên 36 em, posterior mới là Beta$$(33,11)$$.

Kết quả cuối cùng đúng bằng việc cập nhật một lần với toàn bộ dữ liệu 31/40. Đây là lý do prior liên hợp rất thuận tiện: ta không cần giải lại bài toán từ đầu, mà chỉ việc cộng thêm thông tin mới vào các tham số của phân phối.

![Minh họa Beta-Binomial conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/beta_binomial_conjugacy_visual.png)

### 3.3. Ví dụ đời thường khác

Beta-Binomial đặc biệt tự nhiên trong các bài toán như tỷ lệ khách mua hàng sau khi nhìn quảng cáo, tỷ lệ học viên hoàn thành khóa học, tỷ lệ bệnh nhân đáp ứng điều trị, tỷ lệ email được mở, hay tỷ lệ sản phẩm lỗi trong kiểm định chất lượng. Điểm chung của các bối cảnh này là dữ liệu luôn có dạng “đếm số thành công trong một tổng số lần thử đã biết”, nên Binomial là likelihood hợp lý, và khi tham số cần suy luận là một xác suất thì prior Beta trở thành lựa chọn rất thuận tự nhiên.

## 4. Beta-Geometric: khi dữ liệu là số lần chờ đến thành công đầu tiên

### 4.1. Câu chuyện thực tế

Giả sử Nam đi thi chứng chỉ tiếng Anh cho tới khi đậu. Ta muốn suy luận xác suất đậu ở mỗi lần thi là $$\theta$$. Nếu Nam đậu đúng ở lần thứ ba, dữ liệu không nên được đọc như “3 lần thi có 1 lần đậu” theo tinh thần Binomial, mà phải được hiểu như một chuỗi có thứ tự thời gian rất rõ gồm hai lần trượt liên tiếp rồi mới đến một lần đậu ở lần thứ ba.

Nếu mô hình là Geometric theo quy ước “đếm số lần thử cho đến thành công đầu tiên”, ta có:

$$
Y \mid \theta \sim \text{Geometric}(\theta),
$$

với likelihood:

$$
P(Y=y \mid \theta) = \theta(1-\theta)^{y-1}.
$$

Nếu prior vẫn là:

$$
\theta \sim \text{Beta}(\alpha,\beta),
$$

thì posterior trở thành:

$$
\theta \mid y \sim \text{Beta}(\alpha + 1,\beta + y - 1).
$$

Với một quan sát thời gian chờ $$y$$, likelihood có thể viết lại dưới dạng:

$$
p(y\mid \theta)=\theta(1-\theta)^{y-1}\propto \theta^1(1-\theta)^{y-1}.
$$

Trong khi đó, prior Beta cho ta:

$$
p(\theta)\propto \theta^{\alpha-1}(1-\theta)^{\beta-1}.
$$

Nhân hai phần này lại:

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

và posterior trở thành:

$$
\theta\mid y_{1:m}\sim \text{Beta}\left(\alpha+m,\beta+\sum_{i=1}^m y_i-m\right).
$$

Posterior mean tương ứng là:

$$
E[\theta\mid y_{1:m}]=\frac{\alpha+m}{\alpha+\beta+\sum_{i=1}^m y_i}.
$$

### 4.2. Vì sao vẫn liên hợp?

Điểm mấu chốt là likelihood Geometric vẫn tạo ra đúng hai “chất liệu đại số” quen thuộc:

$$
\theta^1(1-\theta)^{y-1}.
$$

Khi nhân với prior Beta:

$$
\theta^{\alpha-1}(1-\theta)^{\beta-1},
$$

ta chỉ cộng số mũ của $$\theta$$ và $$1-\theta$$. Vì thế, posterior vẫn ở trong họ Beta.

### 4.3. Cách đọc trực giác

Nếu dữ liệu là “đậu ở lần thứ ba”, cách đọc trực giác của posterior là ta vừa ghi nhận một lần thành công thực sự, đồng thời cũng ghi nhận hai lần thất bại thực sự xuất hiện trước đó. Chính vì vậy, Beta-Geometric đặc biệt phù hợp với những tình huống như thi cho tới khi đậu, chờ đến khi có khách mua đầu tiên, hay đếm xem cần bao nhiêu lần thử trước khi một hệ thống vận hành thành công lần đầu tiên.

### 4.4. Đừng nhầm Beta-Geometric với Beta-Binomial

Đây là chỗ người mới học rất hay lẫn. Binomial trả lời câu hỏi “trong số $$n$$ lần thử cố định, có bao nhiêu lần thành công?”, còn Geometric trả lời câu hỏi “phải đợi tới lần thử thứ mấy mới có thành công đầu tiên?”. Hai mô hình này khác nhau ở chính cách dữ liệu được tổ chức và diễn giải, mặc dù cả hai vẫn có thể dùng prior Beta vì likelihood của chúng đều được xây từ cùng hai thành phần cơ bản là “thành công” và “thất bại”.

## 5. Gamma-Poisson: khi dữ liệu là số đếm theo thời gian

### 5.1. Câu chuyện thực tế

Một tổng đài muốn suy luận số cuộc gọi trung bình mỗi giờ $$\lambda$$. Trong 8 giờ gần nhất, số cuộc gọi lần lượt là:

$$
7, 9, 8, 6, 10, 8, 11, 7.
$$

Nếu số cuộc gọi theo giờ được mô hình bằng Poisson:

$$
Y_i \mid \lambda \sim \text{Poisson}(\lambda),
$$

và prior là:

$$
\lambda \sim \text{Gamma}(\alpha,\beta),
$$

thì posterior là:

$$
\lambda \mid y_{1:n} \sim \text{Gamma}\left(\alpha + \sum_i y_i,\beta + n\right)
$$

theo tham số hóa shape-rate.

Nếu viết rõ phần phụ thuộc vào $$\lambda$$, prior Gamma có dạng:

$$
p(\lambda)\propto \lambda^{\alpha-1}e^{-\beta\lambda}.
$$

Còn likelihood Poisson cho $$n$$ quan sát là:

$$
p(y_{1:n}\mid \lambda)=\prod_{i=1}^n \frac{e^{-\lambda}\lambda^{y_i}}{y_i!}
\propto \lambda^{\sum_{i=1}^n y_i}e^{-n\lambda}.
$$

Vì vậy:

$$
p(\lambda\mid y_{1:n})\propto p(y_{1:n}\mid \lambda)p(\lambda)
\propto \lambda^{\alpha+\sum_i y_i-1}e^{-(\beta+n)\lambda},
$$

nên:

$$
\lambda\mid y_{1:n}\sim \text{Gamma}\left(\alpha+\sum_i y_i,\beta+n\right).
$$

Posterior mean là:

$$
E[\lambda\mid y]=\frac{\alpha+\sum_i y_i}{\beta+n}.
$$

Nếu mỗi quan sát gắn với mức phơi nhiễm $$t_i$$ và mô hình là $$Y_i\mid \lambda \sim \text{Poisson}(t_i\lambda)$$, công thức cập nhật chỉ thay $$n$$ bằng tổng mức phơi nhiễm:

$$
\lambda\mid y_{1:n}\sim \text{Gamma}\left(\alpha+\sum_i y_i,\beta+\sum_i t_i\right).
$$

### 5.2. Cách đọc

Gamma-Poisson tiện ở chỗ số đếm quan sát được sẽ cộng vào tham số shape, còn số khoảng thời gian hoặc số đơn vị phơi nhiễm được quan sát sẽ cộng vào rate. Cách cập nhật này rất hợp với trực giác, bởi vì càng quan sát lâu thì ta càng có nhiều thông tin về cường độ xảy ra sự kiện, và càng nhìn thấy nhiều sự kiện thì niềm tin của ta về cường độ trung bình cũng càng được kéo lên.

![Prior Gamma và posterior sau khi thấy dữ liệu đếm]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_prior_posterior.png)

![Tóm tắt công thức cập nhật Gamma-Poisson]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_formula_summary.png)

![Posterior predictive trong mô hình Gamma-Poisson]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_posterior_predictive.png)

![Cập nhật tuần tự trong Gamma-Poisson]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_gamma_poisson_sequential_updates.png)

### 5.3. Các bối cảnh rất hợp

Các bối cảnh điển hình cho cặp Gamma-Poisson bao gồm số lỗi hệ thống mỗi ngày, số bệnh nhân nhập viện trong mỗi ca trực, số đơn hàng theo giờ, số sinh viên nghỉ học theo tuần, hoặc số sự cố an ninh mạng theo tháng; nói ngắn gọn, hễ dữ liệu là số đếm gắn với một khoảng thời gian hay một đơn vị phơi nhiễm, cặp này thường rất đáng nghĩ tới.

### 5.4. Công thức nhớ nhanh

Với Gamma-Poisson, bạn có thể đọc công thức như một quy tắc ghi sổ rất cơ học nhưng rất hữu ích: posterior shape bằng prior shape cộng với tổng số sự kiện đã quan sát, còn posterior rate bằng prior rate cộng với số khoảng thời gian hay số đơn vị phơi nhiễm đã được theo dõi. Nói cách khác, ta đồng thời cập nhật cả mức độ hoạt động lẫn độ dài của quá trình quan sát.

### 5.5. Ví dụ cập nhật sự cố mất điện (Gamma-Poisson)

Giả sử một trạm điện theo dõi số sự cố mất điện theo tuần. Đặt:

$$
Y_i\mid\lambda \sim \text{Poisson}(\lambda),\quad i=1,\dots,6.
$$

Prior kỹ thuật ban đầu:

$$
\lambda \sim \text{Gamma}(\alpha_0=4,\beta_0=2)
$$

(shape-rate), nên prior mean là $$E[\lambda]=2$$ sự cố/tuần.

Quan sát 6 tuần có tổng số sự cố:

$$
\sum_{i=1}^6 y_i = 18.
$$

Posterior:

$$
\lambda\mid y_{1:6}\sim \text{Gamma}(\alpha_0+\sum y_i,\beta_0+n)
=\text{Gamma}(22,8).
$$

Suy ra posterior mean:

$$
E[\lambda\mid y]=\frac{22}{8}=2.75.
$$

Diễn giải: sau dữ liệu mới, mức sự cố trung bình ước lượng tăng từ 2 lên 2.75 sự cố/tuần.

## 6. Normal-Normal: khi dữ liệu liên tục dao động quanh một trung bình

### 6.1. Câu chuyện thực tế

Bạn muốn suy luận chiều cao trung bình $$\mu$$ của một nhóm sinh viên. Giả sử độ lệch chuẩn quan sát $$\sigma$$ đã biết, và dữ liệu được mô hình:

$$
Y_i \mid \mu \sim \mathcal{N}(\mu,\sigma^2).
$$

Nếu prior cho $$\mu$$ cũng là Normal:

$$
\mu \sim \mathcal{N}(\mu_0,\tau_0^2),
$$

thì posterior cho $$\mu$$ vẫn là Normal.

Nếu viết mọi thứ như một hàm theo $$\mu$$, likelihood của $$n$$ quan sát có phần hạt nhân:

$$
p(y_{1:n}\mid \mu)\propto \exp\left(-\frac{1}{2\sigma^2}\sum_{i=1}^n (y_i-\mu)^2\right)
\propto \exp\left(-\frac{n}{2\sigma^2}(\mu-\bar y)^2\right),
$$

trong đó:

$$
\bar y=\frac{1}{n}\sum_{i=1}^n y_i.
$$

Còn prior Normal có dạng:

$$
p(\mu)\propto \exp\left(-\frac{(\mu-\mu_0)^2}{2\tau_0^2}\right).
$$

Khi nhân prior với likelihood và hoàn thành bình phương, ta thu được:

$$
\mu\mid y_{1:n}\sim \mathcal{N}(\mu_n,\tau_n^2),
$$

với:

$$
\tau_n^2=\left(\frac{1}{\tau_0^2}+\frac{n}{\sigma^2}\right)^{-1}
$$

và:

$$
\mu_n=\tau_n^2\left(\frac{\mu_0}{\tau_0^2}+\frac{n\bar y}{\sigma^2}\right)
=\frac{\mu_0/\tau_0^2+n\bar y/\sigma^2}{1/\tau_0^2+n/\sigma^2}.
$$

Nói cách khác:

$$
E[\mu\mid y]=\mu_n,\qquad \mathrm{Var}(\mu\mid y)=\tau_n^2.
$$

### 6.2. Ý nghĩa trực giác

Posterior mean trong mô hình này là một dạng **trung bình có trọng số** giữa prior mean và trung bình mẫu, trong đó nguồn thông tin nào đáng tin hơn sẽ được trao trọng số lớn hơn. Trọng số cụ thể phụ thuộc vào prior có tập trung mạnh hay không, dữ liệu có nhiều hay ít, và độ nhiễu quan sát lớn đến mức nào.

![Prior Normal và posterior sau khi kết hợp với dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_prior_posterior.png)

![Tóm tắt công thức cập nhật Normal-Normal]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_formula_summary.png)

![Ảnh hưởng của kích thước mẫu trong Normal-Normal]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_sample_size_effect.png)

![Trọng số tương đối của prior và dữ liệu trong Normal-Normal]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_normal_normal_prior_data_weights.png)

### 6.3. Những bối cảnh gần gũi

Normal-Normal gần gũi với nhiều bài toán quen thuộc như suy luận chiều cao trung bình của một nhóm người, điểm trung bình của một lớp học, thời gian xử lý trung bình của một quy trình, hoặc sai số của cảm biến dao động quanh một giá trị thật chưa biết.

### 6.4. Công thức nhớ nhanh

Nếu bạn quên công thức chi tiết, vẫn có thể nhớ đúng tinh thần của Normal-Normal bằng hai ý sau được gộp lại trong một câu duy nhất: posterior mean luôn bị kéo về phía nguồn thông tin chính xác hơn, còn posterior variance sẽ co lại khi dữ liệu trở nên nhiều hơn hoặc nhiễu quan sát nhỏ đi. Nói ngắn gọn nhưng vẫn chặt chẽ, trong mô hình Normal-Normal, Bayes đang lấy một trung bình có trọng số theo độ tin cậy của từng nguồn thông tin.

### 6.5. Ví dụ Bayes estimate và posterior risk (Normal-Normal)

Giả sử cần suy luận trung bình thời gian xử lý hồ sơ $$\mu$$ (phút), với phương sai quan sát đã biết:

$$
Y_i\mid\mu \sim \mathcal{N}(\mu,\sigma^2),\quad \sigma^2=25.
$$

Prior chuyên gia:

$$
\mu\sim \mathcal{N}(\mu_0=50,\tau_0^2=100).
$$

Quan sát $$n=16$$ hồ sơ, trung bình mẫu $$\bar y=55$$.

Posterior variance:

$$
\tau_n^2=\left(\frac{1}{\tau_0^2}+\frac{n}{\sigma^2}\right)^{-1}
=\left(\frac{1}{100}+\frac{16}{25}\right)^{-1}\approx 1.538.
$$

Posterior mean:

$$
\mu_n=\tau_n^2\left(\frac{\mu_0}{\tau_0^2}+\frac{n\bar y}{\sigma^2}\right)
\approx 54.92.
$$

Vậy:

$$
\mu\mid y \sim \mathcal{N}(54.92,1.538).
$$

Với hàm mất mát bình phương, Bayes estimate là posterior mean:

$$
\hat\mu_{Bayes}=E[\mu\mid y]=54.92.
$$

Posterior risk tại Bayes estimate bằng chính posterior variance:

$$
R(\hat\mu_{Bayes})=E\left[(\mu-\hat\mu_{Bayes})^2\mid y\right]=\mathrm{Var}(\mu\mid y)=1.538.
$$

Diễn giải: so với prior ban đầu, dữ liệu đã kéo ước lượng trung tâm về gần 55 và giảm mạnh bất định hậu nghiệm.

## 7. Cập nhật tuần tự cực kỳ đẹp trong mô hình liên hợp

Đây là một lợi ích rất lớn của conjugacy. Giả sử bạn theo dõi tỷ lệ khách nhấp quảng cáo theo từng ngày và mỗi ngày lại có thêm một ít dữ liệu mới; với Beta-Binomial, bạn không cần giải lại toàn bộ bài toán từ đầu, mà chỉ cần lấy posterior của ngày hôm qua làm prior cho ngày hôm nay rồi cập nhật thêm số lượt thành công và thất bại mới. Điều tương tự cũng đúng với Gamma-Poisson, nơi thông tin mới có thể được hấp thụ vào posterior bằng một phép cập nhật tham số rất gọn.

![Cập nhật tuần tự với prior liên hợp]({{ site.baseurl }}/img/chapter_img/chapter02/sequential_updating_story.png)

Trong các hệ thống giám sát vận hành hoặc dashboard theo thời gian thực, đây là ưu điểm rất trực quan.

## 9. Nhưng conjugacy không phải lúc nào cũng là lựa chọn tốt nhất

Đây là điểm rất quan trọng. Ta không nên chọn prior chỉ vì nó liên hợp nếu lựa chọn ấy mô tả kiến thức thực tế quá kém, khiến ta bỏ qua cấu trúc quan trọng của bài toán, hoặc đơn giản là bài toán đã đủ phức tạp để đòi hỏi một mô hình linh hoạt hơn. Chẳng hạn, prior thực tế có thể có dạng mixture hai đỉnh, tham số có thể chịu những ràng buộc phức tạp, hoặc mô hình có thể bao gồm nhiều tầng và nhiều tham số phụ thuộc lẫn nhau; trong các trường hợp như vậy, sự tiện lợi đại số không còn là tiêu chí quyết định nữa.

Một điểm dễ bị bỏ qua là **support của tham số cũng quan trọng**. Có những trường hợp phần đại số trông có vẻ quen, nhưng posterior lại không còn rơi gọn vào một họ chuẩn quen thuộc trên đúng miền giá trị đang xét.

Ví dụ, nếu tham số $$\theta$$ bị ràng buộc trong đoạn $$[0,1]$$ nhưng likelihood lại đến từ mô hình Poisson, ta có thể thu được một mật độ không chuẩn hóa kiểu:

$$
\theta^{y+1}e^{-\theta}, \qquad 0 \le \theta \le 1.
$$

Biểu thức này vẫn hoàn toàn hợp lệ để suy luận Bayes, nhưng nó không còn là một ví dụ liên hợp “đẹp” như Beta-Binomial hay Gamma-Poisson nữa. Bài học quan trọng ở đây là conjugacy không chỉ phụ thuộc vào hình dạng đại số của mật độ, mà còn phụ thuộc vào việc posterior có còn nằm gọn trong một họ phân phối quen thuộc trên đúng support của tham số hay không.

![Prior liên hợp có thể biểu diễn kém khi prior lý tưởng bị chặn miền]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_truncated_prior.png)

![Tổng quan các tình huống conjugacy không còn phù hợp]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_overview.png)

![Mixture prior là ví dụ điển hình khiến conjugate prior trở nên gượng ép]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_mixture_prior.png)

![Cây quyết định nhanh để chọn ở lại với conjugacy hay chuyển sang MCMC]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_conjugate_limit_decision_tree.png)

Khi điều kiện ấy không còn thỏa, ta thường chuyển sang grid approximation cho những bài cực nhỏ hoặc sang MCMC cho các mô hình tổng quát và linh hoạt hơn.

## 10. Khi nào nên nghĩ tới cặp liên hợp nào?

![Bảng các cặp liên hợp phổ biến]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_table.png)

Bạn có thể nhớ các cặp này theo câu chuyện dữ liệu thay vì học thuộc bảng công thức. Nếu tham số là xác suất thành công trong một số lần thử xác định, hãy nghĩ tới Beta prior đi với Binomial likelihood; nếu bài toán hỏi phải chờ bao lâu hay phải thử đến lần thứ mấy mới có thành công đầu tiên, hãy nghĩ tới Beta prior đi với Geometric likelihood; nếu mục tiêu là suy luận cường độ của số đếm theo thời gian, cặp Gamma-Poisson thường là lựa chọn tự nhiên; còn nếu tham số cần suy luận là trung bình của dữ liệu liên tục, cặp Normal-Normal là điểm khởi đầu hợp lý. Cách nhớ theo bối cảnh dữ liệu như vậy thường bền hơn nhiều so với việc cố học thuộc các biểu thức một cách rời rạc.

## 11. Những nhầm lẫn phổ biến

### 11.1. “Conjugate prior là prior tốt nhất”

Không. Nó chỉ là prior thuận tiện về mặt tính toán.

### 11.2. “Học thuộc công thức là đủ”

Không. Nếu không hiểu câu chuyện sinh dữ liệu và ý nghĩa tham số, bạn sẽ rất dễ lắp sai mô hình.

### 11.3. “Thời đại MCMC rồi thì conjugacy vô dụng”

Không. Nó vẫn là nền tảng trực giác và là bộ ví dụ chuẩn để học Bayesian updating.

## Tóm tắt

**Prior liên hợp là những prior khiến posterior vẫn nằm trong cùng họ phân phối sau khi cập nhật.** Chính đặc điểm này làm cho suy luận Bayes trong các ví dụ đơn giản trở nên dễ tính tay hơn, dễ diễn giải hơn, dễ cập nhật tuần tự hơn, và đặc biệt hữu ích cho việc xây trực giác trước khi chuyển sang những phương pháp tính toán tổng quát hơn. Bốn cặp cơ bản mà bạn nên nhớ đầu tiên trong bài này là Beta-Binomial, Beta-Geometric, Gamma-Poisson, và Normal-Normal; tuy nhiên, điều cần giữ lại lâu dài hơn chính là nguyên tắc rằng sự thuận tiện về mặt tính toán không tự động đồng nghĩa với một lựa chọn mô hình hóa tốt nhất. Nói gọn lại trong ba ý, conjugacy xuất hiện khi prior và likelihood ăn khớp với nhau về đại số nên posterior vẫn ở trong cùng một họ phân phối, các cặp liên hợp giúp cho việc cập nhật Bayes vừa nhanh vừa sáng sủa về mặt trực giác, nhưng prior liên hợp vẫn chỉ là một lựa chọn thuận tiện chứ không nên bị ép dùng nếu nó mô tả kiến thức thực tế quá kém.

## Câu hỏi tự luyện

1. Hãy nêu một ví dụ thực tế phù hợp với Beta-Binomial.
2. Beta-Geometric khác Beta-Binomial ở kiểu dữ liệu nào, dù cả hai cùng dùng prior Beta?
3. Vì sao Gamma-Poisson hợp tự nhiên với dữ liệu đếm theo thời gian?
4. Trong Normal-Normal, điều gì quyết định posterior mean gần prior mean hay gần trung bình mẫu hơn?
5. Khi nào bạn sẽ không muốn chọn prior liên hợp dù biết nó rất tiện?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 2.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 6-7.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2-3.

---

*Bài học tiếp theo: [2.6 Grid Approximation - Xấp xỉ Lưới](/vi/chapter02/grid-approximation/)*
