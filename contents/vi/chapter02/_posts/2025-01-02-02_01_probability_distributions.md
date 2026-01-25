---
layout: post
title: "Bài 2.1: Phân phối Xác suất - Ngôn ngữ của Sự Không chắc chắn"
chapter: '02'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter02
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu tại sao phân phối xác suất là công cụ trung tâm trong phân tích Bayesian, và tại sao việc mô tả sự không chắc chắn bằng phân phối đầy đủ vượt trội hơn nhiều so với việc chỉ báo cáo ước lượng điểm. Bạn sẽ nắm vững cách sử dụng phân phối để mã hóa niềm tin về tham số, dữ liệu, và dự đoán. Quan trọng hơn, bạn sẽ phát triển trực giác về cách các phân phối khác nhau thể hiện các mức độ không chắc chắn khác nhau, và cách chúng tương tác trong suy diễn Bayesian.

## Giới thiệu: Vấn đề với Ước lượng Điểm

Hãy tưởng tượng bạn là một nhà phân tích dữ liệu cho một công ty thương mại điện tử. Bạn đang thử nghiệm một thiết kế mới cho trang web, và bạn muốn ước lượng tỷ lệ chuyển đổi (conversion rate) - tỷ lệ khách hàng thực hiện mua hàng sau khi xem trang. Sau một tuần thử nghiệm với 100 khách hàng, bạn quan sát được 25 chuyển đổi.

Một nhà thống kê tần suất sẽ báo cáo: "Tỷ lệ chuyển đổi ước lượng là 25%." Đây là một **ước lượng điểm** - một con số duy nhất. Nhưng hãy suy nghĩ về những gì con số này không nói cho bạn biết:

Bạn có chắc chắn tỷ lệ thực sự là chính xác 25% không? Tất nhiên là không. Với chỉ 100 quan sát, có rất nhiều sự không chắc chắn. Tỷ lệ thực có thể là 20%, hoặc 30%, hoặc bất kỳ giá trị nào xung quanh 25%.

Nếu bạn đã quan sát 1000 khách hàng và thấy 250 chuyển đổi, bạn sẽ cũng báo cáo 25%, nhưng bạn sẽ tự tin hơn nhiều về con số này. Làm thế nào ước lượng điểm có thể phân biệt giữa hai tình huống này?

Nếu sếp của bạn hỏi: "Xác suất tỷ lệ chuyển đổi thực sự lớn hơn 20% là bao nhiêu?", bạn không thể trả lời chỉ với một ước lượng điểm.

Đây là lý do tại sao trong phân tích Bayesian, chúng ta không chỉ báo cáo ước lượng điểm. Chúng ta báo cáo **phân phối xác suất đầy đủ** - một mô tả hoàn chỉnh về sự không chắc chắn của chúng ta về tham số. Phân phối này cho chúng ta biết không chỉ giá trị có khả năng nhất, mà còn mức độ không chắc chắn xung quanh nó, và xác suất của mọi giá trị có thể khác.

## Phân phối Xác suất: Mã hóa Niềm tin

Trong quan điểm Bayesian, một phân phối xác suất là một cách để mã hóa niềm tin hoặc kiến thức của chúng ta về một đại lượng không chắc chắn. Hãy nghĩ về nó như một "bản đồ niềm tin" - nó cho chúng ta biết mức độ tin tưởng của chúng ta vào mỗi giá trị có thể.

Giả sử chúng ta có một tham số $$\theta$$ (ví dụ, tỷ lệ chuyển đổi), và chúng ta không chắc chắn về giá trị thực của nó. **Một phân phối xác suất $$P(\theta)$$ gán một "trọng số niềm tin" cho mỗi giá trị có thể của $$\theta$$. Các giá trị có xác suất cao hơn là những giá trị chúng ta tin có khả năng cao hơn; các giá trị có xác suất thấp hơn là những giá trị chúng ta tin ít có khả năng hơn.**

Có hai loại phân phối xác suất chính:

**Phân phối Rời rạc:** Sử dụng cho các biến có thể nhận một tập hợp đếm được các giá trị (ví dụ, số lần ra Ngửa trong 10 lần toss đồng xu). Chúng được mô tả bởi **hàm khối xác suất** (PMF), $$P(X = x)$$, cho xác suất của mỗi giá trị cụ thể.

**Phân phối Liên tục:** Sử dụng cho các biến có thể nhận bất kỳ giá trị nào trong một khoảng (ví dụ, tỷ lệ chuyển đổi giữa 0 và 1). Chúng được mô tả bởi **hàm mật độ xác suất** (PDF), $$p(\theta)$$. Lưu ý rằng với biến liên tục, xác suất của một điểm cụ thể là 0; thay vào đó, chúng ta nói về xác suất của các khoảng: $$P(a < \theta < b) = \int_a^b p(\theta) d\theta$$.

Một tính chất quan trọng của mọi phân phối xác suất là chúng phải **chuẩn hóa**: tổng (cho rời rạc) hoặc tích phân (cho liên tục) qua tất cả các giá trị có thể phải bằng 1. Điều này phản ánh thực tế là một trong các khả năng phải xảy ra.

## Ba Vai trò của Phân phối trong Bayesian

Trong phân tích Bayesian, phân phối xác suất xuất hiện ở ba vị trí quan trọng, tương ứng với ba thành phần của định lý Bayes:

### 1. Prior Distribution - Mã hóa Kiến thức Ban đầu

**Prior** $$P(\theta)$$ là một phân phối xác suất mô tả niềm tin của chúng ta về tham số $$\theta$$ **trước khi** quan sát dữ liệu. Nó trả lời câu hỏi: "Dựa trên kiến thức trước đó, lý thuyết, hoặc kinh nghiệm, chúng ta tin rằng $$\theta$$ có khả năng nằm ở đâu?"

Prior có thể đến từ nhiều nguồn:
- Nghiên cứu trước đó
- Kiến thức chuyên môn
- Lý thuyết khoa học
- Ràng buộc vật lý (ví dụ, xác suất phải nằm giữa 0 và 1)

Prior có thể **informative** (chứa nhiều thông tin) hoặc **weakly informative/non-informative** (chứa ít thông tin, để dữ liệu "nói"). Ví dụ, nếu chúng ta biết từ nghiên cứu trước rằng tỷ lệ chuyển đổi thường nằm giữa 20% và 30%, chúng ta có thể sử dụng một prior Beta tập trung trong khoảng này. Nếu chúng ta không biết gì, chúng ta có thể sử dụng prior đồng nhất (uniform) trên [0, 1].

### 2. Likelihood - Mô tả Quá trình Sinh Dữ liệu

**Likelihood** $$P(D \mid \theta)$$ là một phân phối xác suất mô tả xác suất của dữ liệu $$D$$ cho mỗi giá trị có thể của tham số $$\theta$$. Nó trả lời câu hỏi: "Nếu $$\theta$$ có giá trị cụ thể này, dữ liệu chúng ta quan sát được sẽ có khả năng như thế nào?"

Likelihood không phải là một phân phối xác suất của $$\theta$$ (nó không chuẩn hóa qua $$\theta$$). Thay vào đó, nó là một hàm của $$\theta$$ cho dữ liệu cố định. Nhưng nó có hình dạng của một phân phối, và hình dạng này cho chúng ta biết giá trị $$\theta$$ nào làm cho dữ liệu quan sát được có khả năng cao nhất.

Likelihood được xác định bởi **mô hình sinh dữ liệu** (generative model) - câu chuyện của chúng ta về cách dữ liệu được tạo ra. Ví dụ, nếu chúng ta mô hình hóa số chuyển đổi như một quá trình Binomial (mỗi khách hàng độc lập có xác suất $$\theta$$ chuyển đổi), likelihood là phân phối Binomial.

### 3. Posterior Distribution - Niềm tin Cập nhật

**Posterior** $$P(\theta \mid D)$$ là một phân phối xác suất mô tả niềm tin của chúng ta về tham số $$\theta$$ **sau khi** quan sát dữ liệu $$D$$. Nó trả lời câu hỏi: "Dựa trên prior và dữ liệu quan sát, chúng ta bây giờ tin rằng $$\theta$$ có khả năng nằm ở đâu?"

Posterior là kết quả của việc áp dụng định lý Bayes:

$$P(\theta \mid D) = \frac{P(D \mid \theta) \cdot P(\theta)}{P(D)}$$

Posterior kết hợp thông tin từ cả prior và likelihood. Nó là sự thỏa hiệp giữa kiến thức trước đó và bằng chứng mới. Hình dạng của posterior phụ thuộc vào cả prior và likelihood, và mức độ mà nó nghiêng về cái này hay cái kia phụ thuộc vào độ mạnh tương đối của chúng.

## Tham số hóa Phân phối: Mô tả Hình dạng

Mỗi họ phân phối (Normal, Beta, Gamma, v.v.) có một hoặc nhiều **tham số** xác định hình dạng cụ thể của nó. Hiểu các tham số này là chìa khóa để sử dụng phân phối hiệu quả trong phân tích Bayesian.

Hãy xem xét một số ví dụ:

**Phân phối Beta:** Được sử dụng cho các tham số giữa 0 và 1 (như xác suất). Nó có hai tham số, $$\alpha$$ và $$\beta$$, kiểm soát hình dạng:
- Trung bình: $$\frac{\alpha}{\alpha + \beta}$$
- Phương sai: $$\frac{\alpha \beta}{(\alpha + \beta)^2 (\alpha + \beta + 1)}$$
- Khi $$\alpha = \beta$$, phân phối đối xứng xung quanh 0.5
- Khi $$\alpha > \beta$$, phân phối lệch về phải (giá trị cao hơn)
- Khi $$\alpha$$ và $$\beta$$ cả hai lớn, phân phối tập trung chặt chẽ xung quanh trung bình

![Họ Phân phối Beta với các tham số khác nhau]({{ site.baseurl }}/img/chapter_img/chapter02/beta_distribution_family.png)

**Phân phối Normal (Gaussian):** Được sử dụng cho các đại lượng liên tục không bị giới hạn. Nó có hai tham số:
- $$\mu$$ (trung bình): Vị trí trung tâm của phân phối
- $$\sigma^2$$ (phương sai): Độ rộng của phân phối; $$\sigma$$ nhỏ hơn = phân phối hẹp hơn = ít không chắc chắn hơn

**Phân phối Gamma:** Được sử dụng cho các đại lượng dương. Nó có hai tham số (có nhiều cách tham số hóa, nhưng một cách phổ biến là):
- $$\alpha$$ (shape): Kiểm soát hình dạng; $$\alpha$$ lớn hơn = phân phối đối xứng hơn
- $$\beta$$ (rate): Kiểm soát scale; $$\beta$$ lớn hơn = giá trị nhỏ hơn có khả năng cao hơn

Việc chọn tham số phù hợp cho prior là một nghệ thuật. Chúng ta muốn prior phản ánh kiến thức thực sự của chúng ta, nhưng không quá mạnh đến mức áp đảo dữ liệu. Một quy tắc chung là: nếu bạn có kiến thức mạnh, sử dụng prior informative; nếu không, sử dụng prior weakly informative cho phép một phạm vi rộng các giá trị nhưng vẫn loại trừ các giá trị cực đoan không hợp lý.

## Độ Rộng của Phân phối: Định lượng Sự Không chắc chắn

Một khía cạnh quan trọng của phân phối là **độ rộng** của nó, thường được đo bằng độ lệch chuẩn hoặc phương sai. Độ rộng này định lượng mức độ không chắc chắn của chúng ta.

Một phân phối **hẹp** (phương sai nhỏ) có nghĩa là chúng ta khá chắc chắn về giá trị của tham số. Hầu hết khối lượng xác suất tập trung trong một khoảng nhỏ. Ví dụ, nếu posterior của chúng ta cho tỷ lệ chuyển đổi là Beta(100, 300), với trung bình 0.25 và độ lệch chuẩn 0.02, chúng ta khá chắc chắn rằng tỷ lệ thực nằm gần 0.25.

Một phân phối **rộng** (phương sai lớn) có nghĩa là chúng ta không chắc chắn lắm. Xác suất được phân tán qua một khoảng rộng. Ví dụ, nếu posterior của chúng ta là Beta(3, 9), với cùng trung bình 0.25 nhưng độ lệch chuẩn 0.12, chúng ta ít chắc chắn hơn nhiều - tỷ lệ thực có thể ở bất kỳ đâu từ 0.1 đến 0.5.

Khi chúng ta thu thập thêm dữ liệu, posterior thường trở nên hẹp hơn. Điều này phản ánh thực tế là chúng ta đang học hỏi từ dữ liệu và trở nên chắc chắn hơn về giá trị thực của tham số. Tốc độ mà posterior hẹp lại phụ thuộc vào lượng thông tin trong dữ liệu và độ mạnh của prior.

## Khoảng Tin cậy: Tóm tắt Phân phối

Mặc dù phân phối đầy đủ chứa tất cả thông tin về sự không chắc chắn của chúng ta, đôi khi chúng ta cần tóm tắt nó bằng một vài con số. Một cách phổ biến là sử dụng **khoảng tin cậy** (credible interval) hoặc **khoảng xác suất cao nhất** (highest posterior density interval, HPDI).

Một **khoảng tin cậy 95%** là một khoảng chứa 95% khối lượng xác suất của posterior. Nó trả lời câu hỏi: "Dựa trên dữ liệu và prior, có 95% xác suất tham số nằm trong khoảng này."

Lưu ý sự khác biệt với **khoảng tin cậy tần suất** (confidence interval), có diễn giải phức tạp hơn nhiều về hành vi dài hạn của một quy trình. Khoảng tin cậy Bayesian có diễn giải trực tiếp và trực quan mà chúng ta thực sự muốn.

Có nhiều cách để xây dựng khoảng tin cậy. Cách đơn giản nhất là **equal-tailed interval**: lấy các phân vị 2.5% và 97.5% của posterior. Cách khác là HPDI: khoảng hẹp nhất chứa 95% xác suất. Đối với phân phối đối xứng, hai cách này cho kết quả giống nhau, nhưng đối với phân phối lệch, HPDI thường được ưa thích vì nó chứa các giá trị có mật độ cao nhất.

## Ý nghĩa cho Phân tích Bayesian

Phân phối xác suất không chỉ là công cụ toán học trong phân tích Bayesian - chúng là ngôn ngữ mà chúng ta sử dụng để nói về sự không chắc chắn. Mỗi giai đoạn của phân tích Bayesian liên quan đến việc làm việc với phân phối:

**Chỉ định Prior:** Chúng ta chọn một phân phối phản ánh kiến thức trước đó của chúng ta.

**Định nghĩa Likelihood:** Chúng ta chỉ định một mô hình sinh dữ liệu, xác định likelihood như một phân phối.

**Tính Posterior:** Chúng ta kết hợp prior và likelihood để có posterior - một phân phối mới mã hóa niềm tin cập nhật của chúng ta.

**Dự đoán:** Chúng ta sử dụng posterior để tính **posterior predictive distribution** - phân phối của dữ liệu tương lai, tính đến sự không chắc chắn về tham số.

**Truyền đạt:** Chúng ta trực quan hóa và tóm tắt posterior để truyền đạt kết quả.

Trong các bài học tiếp theo, chúng ta sẽ đi sâu vào từng thành phần này, bắt đầu với likelihood, sau đó prior, và cuối cùng là cách chúng kết hợp để tạo ra posterior. Nhưng nền tảng cho tất cả điều này là hiểu biết vững chắc về phân phối xác suất như công cụ để mã hóa và cập nhật niềm tin.

## Bài tập

**Bài tập 1: Diễn giải Phân phối.** Xem xét hai posterior cho cùng một tham số: (a) Beta(10, 10) với trung bình 0.5. (b) Beta(100, 100) với trung bình 0.5. Cả hai có cùng trung bình, nhưng chúng khác nhau như thế nào? Vẽ hoặc mô tả chúng. Posterior nào thể hiện sự không chắc chắn nhiều hơn? Tại sao?

**Bài tập 2: Prior và Posterior.** Bạn bắt đầu với prior Beta(2, 2) cho xác suất một đồng xu ra Ngửa. (a) Vẽ prior này. Nó nói gì về niềm tin ban đầu của bạn? (b) Bạn toss đồng xu 10 lần và thấy 7 Ngửa. Posterior là Beta(9, 5). Vẽ prior và posterior trên cùng một đồ thị. (c) Posterior đã thay đổi như thế nào so với prior? Nó hẹp hơn hay rộng hơn? Trung bình đã dịch chuyển về đâu? (d) Điều này dạy bạn gì về cách dữ liệu cập nhật niềm tin?

**Bài tập 3: Khoảng Tin cậy.** Một posterior cho tham số $$\theta$$ là Normal(50, 10²). (a) Tính khoảng tin cậy 95% equal-tailed. (b) Diễn giải khoảng này bằng lời đơn giản. (c) So sánh với diễn giải của khoảng tin cậy tần suất 95%. Cái nào dễ hiểu hơn?

**Bài tập 4: Ảnh hưởng của Cỡ mẫu.** Sử dụng Python, mô phỏng tình huống sau: Tỷ lệ chuyển đổi thực là 0.3. Bạn bắt đầu với prior Beta(2, 2). (a) Với n = 10 quan sát, tính posterior. (b) Với n = 100 quan sát, tính posterior. (c) Với n = 1000 quan sát, tính posterior. (d) Vẽ prior và ba posterior trên cùng một đồ thị. Bạn quan sát được gì về cách posterior thay đổi khi cỡ mẫu tăng?

**Bài tập 5: Suy ngẫm về Phân phối.** Viết một đoạn văn ngắn (300-400 từ) suy ngẫm về: (a) Tại sao việc mô tả sự không chắc chắn bằng phân phối đầy đủ tốt hơn việc chỉ báo cáo ước lượng điểm? (b) Trong thực hành khoa học hoặc kinh doanh, khi nào thông tin về sự không chắc chắn đặc biệt quan trọng? (c) Làm thế nào phân phối giúp chúng ta đưa ra quyết định tốt hơn?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 1: Probability and inference
- Chapter 2: Single-parameter models

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 4: What is This Stuff Called Probability?
- Chapter 5: Bayes' Rule

**McElreath, R. (2020).** *Statistical Rethinking: A Bayesian Course with Examples in R and Stan* (2nd Edition). CRC Press.
- Chapter 2: Small Worlds and Large Worlds
- Chapter 3: Sampling the Imaginary

### Supplementary Reading:

**Jaynes, E. T. (2003).** *Probability Theory: The Logic of Science*. Cambridge University Press.
- Chapter 3: Elementary sampling theory

---

*Bài học tiếp theo: [2.2 Likelihood - Mô hình Sinh Dữ liệu](/vi/chapter02/likelihood/)*
