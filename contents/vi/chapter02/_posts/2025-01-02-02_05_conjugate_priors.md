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

Thế nhưng có một số bài toán rất “ngoan”. Khi ta nhân prior với likelihood, posterior vẫn rơi vào **cùng một họ phân phối** như prior. Những trường hợp đẹp này được gọi là **prior liên hợp**.

![Giới thiệu về các cặp liên hợp]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_intro.png)

## 1. Prior liên hợp là gì?

Ta nói prior $$p(\theta)$$ là liên hợp với likelihood $$p(y \mid \theta)$$ nếu posterior $$p(\theta \mid y)$$ thuộc cùng họ với prior.

Ví dụ:

- prior Beta  $$\rightarrow$$ posterior vẫn là Beta,
- prior Gamma  $$\rightarrow$$ posterior vẫn là Gamma,
- prior Normal  $$\rightarrow$$ posterior vẫn là Normal.

Ý nghĩa của việc này là:

- ta không phải tạo ra một họ phân phối mới hoàn toàn sau cập nhật,
- chỉ cần cập nhật vài tham số,
- nên công thức posterior thường viết được rất gọn.

## 2. Trực giác: vì sao liên hợp xuất hiện?

Liên hợp xuất hiện khi prior và likelihood có “cùng chất liệu đại số”.

Ví dụ:

- likelihood Binomial tạo ra các lũy thừa của $$\theta$$ và $$1-\theta$$,
- prior Beta cũng được xây từ các lũy thừa của $$\theta$$ và $$1-\theta$$.

Khi nhân hai biểu thức này, ta không đổi dạng hàm. Ta chỉ cộng các số mũ. Đó chính là lý do posterior vẫn là Beta.

Nói ngắn gọn:

**Conjugacy là sự ăn khớp giữa hình dạng của prior và hình dạng của likelihood.**

![Vì sao conjugacy tiện lợi]({{ site.baseurl }}/img/chapter_img/chapter02/why_conjugacy_convenient.png)

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

### 3.2. Ý nghĩa trực giác

Nếu prior là Beta$$(2,2)$$ và dữ liệu là 31/40, posterior thành Beta$$(33,11)$$.

Đọc bằng lời:

- prior như đang mang sẵn vài “lần thành công giả tưởng” và “lần thất bại giả tưởng”,
- dữ liệu thật được cộng tiếp vào,
- posterior là tổng hợp của cả hai.

![Minh họa Beta-Binomial conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/beta_binomial_conjugacy_visual.png)

### 3.3. Ví dụ đời thường khác

Beta-Binomial cực kỳ tự nhiên cho các bài toán:

- tỷ lệ khách mua hàng,
- tỷ lệ học viên hoàn thành khóa học,
- tỷ lệ bệnh nhân đáp ứng điều trị,
- tỷ lệ email được mở,
- tỷ lệ sản phẩm lỗi trong kiểm định chất lượng.

Nếu dữ liệu là “đếm số thành công trong tổng số lần thử”, hãy nghĩ tới Binomial. Và nếu tham số là một xác suất, prior Beta là lựa chọn rất tự nhiên.

## 4. Beta-Geometric: khi dữ liệu là số lần chờ đến thành công đầu tiên

### 4.1. Câu chuyện thực tế

Giả sử Nam đi thi chứng chỉ tiếng Anh cho tới khi đậu. Ta muốn suy luận xác suất đậu ở mỗi lần thi là $$\theta$$. Nếu Nam đậu đúng ở lần thứ ba, dữ liệu không phải là “3 lần thi có 1 lần đậu” theo nghĩa Binomial, mà là:

- trượt ở lần 1,
- trượt ở lần 2,
- đậu ở lần 3.

Đó là một kiểu dữ liệu có **thứ tự thời gian** rất rõ.

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

Nếu dữ liệu là “đậu ở lần thứ ba”, posterior được cập nhật như sau:

- có thêm một lần thành công thực,
- có thêm hai lần thất bại thực.

Đó là lý do Beta-Geometric rất hợp với các bài kiểu:

- thi cho tới khi đậu,
- chờ đến khi có khách mua đầu tiên,
- số lần thử cho đến khi hệ thống chạy thành công lần đầu.

## 5. Gamma-Poisson: khi dữ liệu là số đếm theo thời gian

### 4.1. Câu chuyện thực tế

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

### 4.2. Cách đọc

Gamma-Poisson tiện ở chỗ:

- số đếm quan sát được cộng vào tham số shape,
- số khoảng thời gian quan sát được cộng vào rate.

Điều này rất hợp với trực giác:

- càng quan sát lâu, ta càng có nhiều thông tin,
- càng thấy nhiều sự kiện, niềm tin về cường độ trung bình càng dịch lên.

![Minh họa Gamma-Poisson conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/gamma_poisson_conjugacy_detailed.png)

### 4.3. Các bối cảnh rất hợp

- số lỗi hệ thống mỗi ngày,
- số bệnh nhân nhập viện mỗi ca trực,
- số đơn hàng mỗi giờ,
- số sinh viên nghỉ học mỗi tuần,
- số sự cố an ninh mạng mỗi tháng.

## 6. Normal-Normal: khi dữ liệu liên tục dao động quanh một trung bình

### 5.1. Câu chuyện thực tế

Bạn muốn suy luận chiều cao trung bình $$\mu$$ của một nhóm sinh viên. Giả sử độ lệch chuẩn quan sát $$\sigma$$ đã biết, và dữ liệu được mô hình:

$$
Y_i \mid \mu \sim \mathcal{N}(\mu,\sigma^2).
$$

Nếu prior cho $$\mu$$ cũng là Normal:

$$
\mu \sim \mathcal{N}(\mu_0,\tau_0^2),
$$

thì posterior cho $$\mu$$ vẫn là Normal.

### 5.2. Ý nghĩa trực giác

Posterior mean là một dạng **trung bình có trọng số** giữa:

- prior mean,
- và trung bình mẫu.

Trọng số nào mạnh hơn tùy vào:

- prior có hẹp hay không,
- dữ liệu có nhiều hay không,
- độ nhiễu quan sát có lớn hay không.

![Minh họa Normal-Normal conjugacy]({{ site.baseurl }}/img/chapter_img/chapter02/normal_normal_conjugacy_detailed.png)

### 5.3. Những bối cảnh gần gũi

- trung bình chiều cao,
- điểm trung bình một lớp,
- thời gian xử lý trung bình của một tác vụ,
- sai số cảm biến quanh một giá trị thật.

## 7. Cập nhật tuần tự cực kỳ đẹp trong mô hình liên hợp

Đây là một lợi ích lớn của conjugacy.

Giả sử bạn theo dõi tỷ lệ khách nhấp quảng cáo theo từng ngày. Mỗi ngày một ít dữ liệu mới tới. Với Beta-Binomial, bạn không cần giải lại bài toán từ đầu. Chỉ cần:

- lấy posterior hôm qua,
- dùng nó làm prior cho hôm nay,
- cập nhật thêm số lượt thành công và thất bại mới.

Điều tương tự đúng với Gamma-Poisson.

![Cập nhật tuần tự với prior liên hợp]({{ site.baseurl }}/img/chapter_img/chapter02/sequential_updating_story.png)

Trong các hệ thống giám sát vận hành hoặc dashboard theo thời gian thực, đây là ưu điểm rất trực quan.

## 8. Vì sao nên học conjugacy dù sau này dùng MCMC?

Có ba lý do rất đáng học.

### 7.1. Nó cho trực giác cực tốt

Conjugacy cho bạn nhìn thẳng vào cách prior và dữ liệu tương tác.

### 7.2. Nó cho lời giải kiểm chứng

Khi bạn học grid approximation hay MCMC, các mô hình liên hợp là nơi rất tốt để kiểm tra xem code có đang cho kết quả hợp lý không.

### 7.3. Nó vẫn hữu ích trong các bài toán nhỏ

Với mô hình đơn giản, conjugacy cho lời giải:

- nhanh,
- rõ,
- dễ giải thích,
- và thường đủ tốt cho giảng dạy hoặc bài toán một tham số.

![Conjugacy so với các phương pháp tính toán khác]({{ site.baseurl }}/img/chapter_img/chapter02/conjugacy_vs_mcmc.png)

## 9. Nhưng conjugacy không phải lúc nào cũng là lựa chọn tốt nhất

Đây là điểm rất quan trọng.

Ta không nên chọn prior chỉ vì nó liên hợp nếu:

- nó mô tả kiến thức thực tế quá kém,
- nó làm ta bỏ qua cấu trúc quan trọng của bài toán,
- hoặc bài toán đã đủ phức tạp để cần mô hình linh hoạt hơn.

Ví dụ:

- prior thực tế có thể là mixture hai đỉnh,
- tham số có thể bị ràng buộc phức tạp,
- mô hình có nhiều tầng hoặc nhiều tham số liên kết với nhau.

Một điểm dễ bị bỏ qua là **support của tham số cũng quan trọng**. Có những trường hợp phần đại số trông có vẻ quen, nhưng posterior lại không còn rơi gọn vào một họ chuẩn quen thuộc trên đúng miền giá trị đang xét.

Ví dụ, nếu tham số $$\theta$$ bị ràng buộc trong đoạn $$[0,1]$$ nhưng likelihood lại đến từ mô hình Poisson, ta có thể thu được một mật độ không chuẩn hóa kiểu:

$$
\theta^{y+1}e^{-\theta}, \qquad 0 \le \theta \le 1.
$$

Biểu thức này vẫn hoàn toàn hợp lệ để suy luận Bayes, nhưng nó không còn là một ví dụ liên hợp “đẹp” như Beta-Binomial hay Gamma-Poisson nữa. Bài học ở đây là:

- conjugacy phụ thuộc vào cả hình dạng đại số,
- và vào việc posterior có còn nằm gọn trong một họ quen thuộc trên đúng support hay không.

![Giới hạn của prior liên hợp]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_prior_limitations.png)

Lúc đó, ta chuyển sang:

- grid approximation cho bài rất nhỏ,
- MCMC cho các mô hình tổng quát hơn.

## 10. Khi nào nên nghĩ tới cặp liên hợp nào?

![Bảng các cặp liên hợp phổ biến]({{ site.baseurl }}/img/chapter_img/chapter02/conjugate_pairs_table.png)

Bạn có thể nhớ theo câu chuyện dữ liệu:

- xác suất thành công  $$\rightarrow$$ Beta prior + Binomial likelihood,
- số lần chờ đến thành công đầu tiên  $$\rightarrow$$ Beta prior + Geometric likelihood,
- tốc độ đếm sự kiện  $$\rightarrow$$ Gamma prior + Poisson likelihood,
- trung bình của dữ liệu liên tục  $$\rightarrow$$ Normal prior + Normal likelihood.

Nhớ theo **bối cảnh dữ liệu** thường dễ hơn nhớ theo bảng công thức khô.

## 11. Những nhầm lẫn phổ biến

### 10.1. “Conjugate prior là prior tốt nhất”

Không. Nó chỉ là prior thuận tiện về mặt tính toán.

### 10.2. “Học thuộc công thức là đủ”

Không. Nếu không hiểu câu chuyện sinh dữ liệu và ý nghĩa tham số, bạn sẽ rất dễ lắp sai mô hình.

### 10.3. “Thời đại MCMC rồi thì conjugacy vô dụng”

Không. Nó vẫn là nền tảng trực giác và là bộ ví dụ chuẩn để học Bayesian updating.

## Tóm tắt

**Prior liên hợp là những prior khiến posterior vẫn nằm trong cùng họ phân phối sau khi cập nhật.**

Điều đó làm cho Bayes trở nên:

- tính tay được,
- diễn giải dễ,
- cập nhật tuần tự gọn,
- và rất phù hợp cho việc xây trực giác.

Ba cặp bạn nên nhớ đầu tiên là:

- Beta-Binomial,
- Gamma-Poisson,
- Normal-Normal.

Nhưng hãy luôn nhớ: **thuận tiện tính toán không tự động đồng nghĩa với mô hình hóa tốt nhất**.

> **3 ý cần nhớ.**
> 1. Conjugacy xảy ra khi prior và likelihood “ăn khớp” về đại số nên posterior vẫn ở cùng họ phân phối.
> 2. Các cặp liên hợp giúp việc cập nhật Bayes nhanh, gọn và rất tốt cho việc xây trực giác.
> 3. Prior liên hợp là lựa chọn tiện lợi, nhưng không nên ép dùng nếu nó mô tả kiến thức thực tế quá kém.

## Câu hỏi tự luyện

1. Hãy nêu một ví dụ thực tế phù hợp với Beta-Binomial.
2. Vì sao Gamma-Poisson hợp tự nhiên với dữ liệu đếm theo thời gian?
3. Trong Normal-Normal, điều gì quyết định posterior mean gần prior mean hay gần trung bình mẫu hơn?
4. Khi nào bạn sẽ không muốn chọn prior liên hợp dù biết nó rất tiện?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 2.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 6-7.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2-3.

---

*Bài học tiếp theo: [2.6 Grid Approximation - Xấp xỉ Lưới](/vi/chapter02/grid-approximation/)*
