---
layout: post
title: "Bài 0.2: Các Phân phối Xác suất - Mô tả Sự Biến thiên trong Dữ liệu"
chapter: '00'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu rằng các phân phối xác suất không chỉ là các công thức toán học trừu tượng, mà là những công cụ mạnh mẽ để mô tả và suy luận về các mẫu hình trong dữ liệu thực tế. Bạn sẽ làm quen với một số phân phối xác suất quan trọng nhất, hiểu được nguồn gốc tự nhiên của chúng, và nhận ra khi nào mỗi phân phối là phù hợp để mô hình hóa một tình huống cụ thể. Quan trọng hơn, bạn sẽ bắt đầu thấy các phân phối xác suất như những "câu chuyện" về cách dữ liệu có thể được sinh ra, một quan điểm trung tâm trong tư duy Bayesian.

## Giới thiệu: Từ Xác suất đến Phân phối

Trong bài học trước, chúng ta đã học cách gán xác suất cho các biến cố riêng lẻ. Nhưng trong thực tế, chúng ta thường quan tâm đến các đại lượng số học, như chiều cao của một người, số lần một sự kiện xảy ra, hoặc thời gian chờ đợi giữa các sự kiện. Những đại lượng này được mô hình hóa bằng **biến ngẫu nhiên** (random variables), và cách chúng phân bố xác suất qua các giá trị có thể được mô tả bởi **phân phối xác suất** (probability distributions).

Một phân phối xác suất là một mô tả toán học hoàn chỉnh về cách xác suất được phân bổ qua tất cả các giá trị có thể của một biến ngẫu nhiên. Đối với biến ngẫu nhiên rời rạc, chúng ta sử dụng **hàm khối xác suất** (probability mass function, PMF) để chỉ định xác suất của từng giá trị cụ thể. Đối với biến ngẫu nhiên liên tục, chúng ta sử dụng **hàm mật độ xác suất** (probability density function, PDF), trong đó xác suất được gán cho các khoảng giá trị thay vì các điểm riêng lẻ.

Tại sao chúng ta cần nghiên cứu các phân phối xác suất cụ thể? Vì trong thực tế, nhiều hiện tượng tự nhiên và xã hội tuân theo các mẫu hình có thể dự đoán được. Số lần xuất hiện của một sự kiện hiếm trong một khoảng thời gian cố định thường tuân theo phân phối Poisson. Sai số đo lường trong các thí nghiệm khoa học thường tuân theo phân phối chuẩn. Thời gian chờ đợi giữa các sự kiện ngẫu nhiên độc lập thường tuân theo phân phối mũ. Bằng cách nhận ra những mẫu hình này, chúng ta có thể xây dựng các mô hình hiệu quả hơn và đưa ra các suy luận chính xác hơn.

Trong bài học này, chúng ta sẽ khám phá một số phân phối xác suất quan trọng nhất, tập trung vào trực giác và ứng dụng hơn là chứng minh toán học. Mỗi phân phối sẽ được giới thiệu thông qua một câu chuyện về cách dữ liệu có thể được sinh ra, một cách tiếp cận phù hợp hoàn hảo với tư duy Bayesian.

## Phân phối Bernoulli: Thí nghiệm Đơn giản Nhất

Hãy bắt đầu với phân phối đơn giản nhất có thể: **phân phối Bernoulli**. Đây là phân phối của một thí nghiệm chỉ có hai kết quả có thể, thường được gọi là "thành công" và "thất bại", hoặc $$1$$ và $$0$$. Ví dụ bao gồm toss một đồng xu (Ngửa hoặc Sấp), một bệnh nhân phản ứng với điều trị (Có hoặc Không), hoặc một email là spam (Đúng hoặc Sai).

Một biến ngẫu nhiên $$X$$ tuân theo phân phối Bernoulli với tham số $$p$$ (xác suất thành công) nếu:

$$P(X = 1) = p \quad \text{và} \quad P(X = 0) = 1 - p$$

Chúng ta viết $$X \sim \text{Bernoulli}(p)$$. Tham số $$p$$ hoàn toàn xác định phân phối này. Khi $$p = 0.5$$, thí nghiệm là công bằng (như một đồng xu cân bằng). Khi $$p$$ gần $$1$$, thành công rất có khả năng xảy ra. Khi $$p$$ gần $$0$$, thất bại là kết quả thường gặp.

Phân phối Bernoulli có vẻ đơn giản, nhưng nó là nền tảng cho nhiều phân phối phức tạp hơn. Nó cũng minh họa một nguyên tắc quan trọng: một phân phối xác suất là một mô hình của một quá trình sinh dữ liệu. Khi chúng ta nói $$X \sim \text{Bernoulli}(p)$$, chúng ta đang nói rằng chúng ta tin rằng dữ liệu được sinh ra bởi một quá trình có xác suất thành công cố định $$p$$ trong mỗi lần thử.

## Phân phối Binomial: Đếm Số lần Thành công

Giả sử chúng ta lặp lại một thí nghiệm Bernoulli $$n$$ lần một cách độc lập, mỗi lần với cùng xác suất thành công $$p$$. Tổng số lần thành công trong $$n$$ lần thử là một biến ngẫu nhiên tuân theo **phân phối Binomial** với tham số $$n$$ và $$p$$, ký hiệu là $$X \sim \text{Binomial}(n, p)$$.

Xác suất quan sát được đúng $$k$$ lần thành công trong $$n$$ lần thử là:

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

trong đó $$\binom{n}{k} = \frac{n!}{k!(n-k)!}$$ là hệ số tổ hợp, đếm số cách chọn $$k$$ vị trí cho các lần thành công trong $$n$$ lần thử.

Công thức này có một trực giác rõ ràng. Xác suất của một chuỗi cụ thể gồm $$k$$ lần thành công và $$n-k$$ lần thất bại là $$p^k (1-p)^{n-k}$$ (do tính độc lập). Nhưng có $$\binom{n}{k}$$ chuỗi khác nhau có cùng số lần thành công, vì vậy chúng ta nhân với hệ số này.

Phân phối Binomial xuất hiện tự nhiên trong nhiều tình huống: số lượng bệnh nhân phản ứng với điều trị trong một thử nghiệm lâm sàng, số lượng email spam trong một mẫu ngẫu nhiên, hoặc số lần xuất hiện mặt Ngửa khi toss một đồng xu nhiều lần. Mỗi khi chúng ta đếm số lần một sự kiện nhị phân xảy ra trong một số lần thử cố định và độc lập, phân phối Binomial là mô hình tự nhiên.

Một đặc điểm quan trọng của phân phối Binomial là khi $$n$$ lớn và $$p$$ không quá gần $$0$$ hoặc $$1$$, nó có thể được xấp xỉ tốt bởi phân phối chuẩn. Đây là một ví dụ của định lý giới hạn trung tâm, một kết quả nền tảng trong lý thuyết xác suất mà chúng ta sẽ thảo luận sau.

## Phân phối Poisson: Đếm Các Sự kiện Hiếm

Phân phối Binomial mô hình hóa số lần thành công trong một số lần thử cố định. Nhưng đôi khi, chúng ta không có một số lần thử rõ ràng. Thay vào đó, chúng ta quan tâm đến số lần một sự kiện hiếm xảy ra trong một khoảng thời gian hoặc không gian cố định. Ví dụ: số cuộc gọi đến một tổng đài trong một giờ, số lỗi đánh máy trên một trang, hoặc số tai nạn giao thông tại một ngã tư trong một tháng.

Trong những tình huống này, **phân phối Poisson** thường là mô hình phù hợp. Một biến ngẫu nhiên $$X$$ tuân theo phân phối Poisson với tham số $$\lambda$$ (tốc độ trung bình của sự kiện) nếu:

$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k = 0, 1, 2, \ldots$$

Tham số $$\lambda$$ đại diện cho số lượng trung bình của sự kiện trong khoảng thời gian hoặc không gian được xem xét. Cả giá trị kỳ vọng và phương sai của phân phối Poisson đều bằng $$\lambda$$, một đặc điểm đặc trưng của phân phối này.

Phân phối Poisson có thể được suy ra như một giới hạn của phân phối Binomial khi số lần thử $$n$$ tiến đến vô cùng, xác suất thành công $$p$$ tiến đến $$0$$, nhưng tích $$np$$ (số lần thành công trung bình) tiến đến một hằng số $$\lambda$$. Điều này giải thích tại sao Poisson phù hợp cho các sự kiện hiếm: chúng ta có rất nhiều "cơ hội" cho sự kiện xảy ra ($$n$$ lớn), nhưng mỗi cơ hội có xác suất rất nhỏ ($$p$$ nhỏ).

Phân phối Poisson đóng vai trò quan trọng trong nhiều lĩnh vực, từ quản lý hàng đợi đến dịch tễ học. Trong phân tích dữ liệu Bayesian, nó thường được sử dụng để mô hình hóa dữ liệu đếm, đặc biệt khi các số đếm nhỏ và sự kiện hiếm.

## Phân phối Chuẩn (Gaussian): Phân phối Phổ biến Nhất

Nếu có một phân phối xác suất mà mọi người đều biết, đó là **phân phối chuẩn** (normal distribution), còn được gọi là phân phối Gaussian. Một biến ngẫu nhiên liên tục $$X$$ tuân theo phân phối chuẩn với trung bình $$\mu$$ và độ lệch chuẩn $$\sigma$$ nếu hàm mật độ xác suất của nó là:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right), \quad -\infty < x < \infty$$

Chúng ta viết $$X \sim \mathcal{N}(\mu, \sigma^2)$$. Phân phối này có hình dạng chuông đối xứng, với đỉnh tại $$\mu$$ và độ rộng được kiểm soát bởi $$\sigma$$. Khoảng 68% xác suất nằm trong một độ lệch chuẩn từ trung bình, 95% trong hai độ lệch chuẩn, và 99.7% trong ba độ lệch chuẩn.

Tại sao phân phối chuẩn lại phổ biến đến vậy? Có nhiều lý do. Đầu tiên, nhiều hiện tượng tự nhiên thực sự tuân theo phân phối chuẩn hoặc gần chuẩn: chiều cao người, sai số đo lường, điểm số trong các bài kiểm tra chuẩn hóa. Thứ hai, **định lý giới hạn trung tâm** (Central Limit Theorem) nói rằng tổng (hoặc trung bình) của một số lượng lớn các biến ngẫu nhiên độc lập, bất kể phân phối gốc của chúng, sẽ xấp xỉ tuân theo phân phối chuẩn. Điều này giải thích tại sao phân phối chuẩn xuất hiện trong rất nhiều ngữ cảnh khác nhau.

Thứ ba, phân phối chuẩn có những tính chất toán học rất thuận tiện. Nó được xác định hoàn toàn bởi hai tham số ($$\mu$$ và $$\sigma^2$$). Tổng của các biến ngẫu nhiên chuẩn độc lập cũng là chuẩn. Và trong suy diễn Bayesian, phân phối chuẩn là phân phối liên hợp (conjugate) với chính nó, điều này đơn giản hóa đáng kể các tính toán.

Tuy nhiên, chúng ta cũng cần cẩn thận. Không phải mọi thứ đều tuân theo phân phối chuẩn. Dữ liệu có giới hạn (như xác suất, phải nằm giữa $$0$$ và $$1$$) hoặc dữ liệu lệch (skewed) thường không phù hợp với giả định chuẩn. Việc áp dụng mù quáng phân phối chuẩn mà không kiểm tra giả định có thể dẫn đến suy luận sai lệch.

## Phân phối Beta: Mô hình hóa Xác suất

Trong phân tích Bayesian, chúng ta thường cần mô hình hóa không chỉ dữ liệu quan sát được, mà còn cả các tham số của mô hình. Một tham số đặc biệt quan trọng là xác suất thành công trong một thí nghiệm Bernoulli hoặc Binomial. Vì xác suất phải nằm giữa $$0$$ và $$1$$, chúng ta cần một phân phối được định nghĩa trên khoảng này. **Phân phối Beta** là lựa chọn tự nhiên.

Một biến ngẫu nhiên liên tục $$X$$ tuân theo phân phối Beta với tham số $$\alpha > 0$$ và $$\beta > 0$$ nếu hàm mật độ xác suất của nó là:

$$f(x) = \frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha, \beta)}, \quad 0 < x < 1$$

trong đó $$B(\alpha, \beta) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$$ là hàm Beta, một hằng số chuẩn hóa đảm bảo rằng tích phân của $$f(x)$$ bằng $$1$$.

Phân phối Beta cực kỳ linh hoạt. Bằng cách thay đổi $$\alpha$$ và $$\beta$$, chúng ta có thể tạo ra nhiều hình dạng khác nhau: đồng nhất (khi $$\alpha = \beta = 1$$), lệch về trái hoặc phải, hình chữ U, hoặc tập trung chặt chẽ xung quanh một giá trị cụ thể. Trung bình của phân phối Beta là $$\frac{\alpha}{\alpha+\beta}$$, và phương sai phụ thuộc vào cả $$\alpha$$ và $$\beta$$.

Một tính chất đặc biệt quan trọng của phân phối Beta là nó là phân phối liên hợp với phân phối Binomial. Điều này có nghĩa là nếu chúng ta sử dụng prior Beta cho xác suất thành công, và quan sát dữ liệu Binomial, posterior cũng sẽ là Beta. Tính chất này làm cho phân phối Beta trở thành lựa chọn tự nhiên cho prior trong nhiều vấn đề Bayesian, và chúng ta sẽ sử dụng nó rộng rãi trong khóa học này.

## Phân phối Mũ: Thời gian Chờ đợi

Giả sử các sự kiện xảy ra ngẫu nhiên và độc lập với tốc độ trung bình $$\lambda$$ trên một đơn vị thời gian (theo phân phối Poisson). Thời gian chờ đợi giữa các sự kiện liên tiếp tuân theo **phân phối mũ** (exponential distribution) với tham số $$\lambda$$.

Hàm mật độ xác suất của phân phối mũ là:

$$f(x) = \lambda e^{-\lambda x}, \quad x \geq 0$$

Phân phối này có một tính chất đặc biệt gọi là **tính không nhớ** (memorylessness): xác suất phải chờ thêm $$t$$ đơn vị thời gian nữa không phụ thuộc vào đã chờ bao lâu rồi. Hình thức hóa, $$P(X > s + t \mid X > s) = P(X > t)$$ cho mọi $$s, t \geq 0$$. Điều này phản ánh giả định rằng các sự kiện xảy ra hoàn toàn ngẫu nhiên, không có "bộ nhớ" về quá khứ.

Phân phối mũ được sử dụng rộng rãi để mô hình hóa thời gian sống của các thiết bị điện tử, thời gian phục vụ trong lý thuyết hàng đợi, và thời gian giữa các cuộc gọi đến một tổng đài. Trong phân tích sinh tồn (survival analysis), một nhánh quan trọng của thống kê, phân phối mũ là mô hình cơ bản nhất.

## Phân phối Gamma: Tổng quát hóa Phân phối Mũ

Phân phối mũ mô hình hóa thời gian chờ đợi cho sự kiện đầu tiên. Nhưng nếu chúng ta quan tâm đến thời gian chờ đợi cho sự kiện thứ $$k$$? Hoặc nếu chúng ta muốn một phân phối linh hoạt hơn cho các đại lượng dương? **Phân phối Gamma** cung cấp câu trả lời.

Phân phối Gamma với tham số hình dạng $$\alpha > 0$$ và tham số tốc độ $$\beta > 0$$ có hàm mật độ:

$$f(x) = \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}, \quad x > 0$$

trong đó $$\Gamma(\alpha) = \int_0^\infty t^{\alpha-1} e^{-t} dt$$ là hàm Gamma.

Phân phối mũ là trường hợp đặc biệt của phân phối Gamma với $$\alpha = 1$$. Khi $$\alpha$$ là số nguyên, phân phối Gamma mô hình hóa thời gian chờ đợi cho sự kiện thứ $$\alpha$$ trong một quá trình Poisson. Khi $$\alpha$$ không phải số nguyên, phân phối Gamma vẫn hữu ích như một mô hình linh hoạt cho các đại lượng dương.

Trong suy diễn Bayesian, phân phối Gamma thường được sử dụng như prior cho các tham số tốc độ hoặc độ chính xác (nghịch đảo của phương sai). Nó cũng là phân phối liên hợp với phân phối Poisson, một tính chất hữu ích trong nhiều ứng dụng.

## Lựa chọn Phân phối Phù hợp: Nghệ thuật và Khoa học

Với rất nhiều phân phối xác suất có sẵn, làm thế nào chúng ta biết phân phối nào phù hợp cho một tình huống cụ thể? Đây vừa là nghệ thuật vừa là khoa học, đòi hỏi sự kết hợp giữa hiểu biết về lý thuyết, kinh nghiệm thực tế, và kiểm tra thực nghiệm.

Đầu tiên, hãy xem xét **bản chất của dữ liệu**. Dữ liệu có rời rạc hay liên tục? Nó có giới hạn không (ví dụ, chỉ các giá trị dương, hoặc giữa $$0$$ và $$1$$)? Nó có đối xứng hay lệch? Những câu hỏi này có thể loại bỏ nhiều phân phối không phù hợp.

Thứ hai, suy nghĩ về **quá trình sinh dữ liệu**. Dữ liệu là kết quả của việc đếm các sự kiện? Phân phối Binomial hoặc Poisson có thể phù hợp. Nó là thời gian chờ đợi? Phân phối mũ hoặc Gamma có thể phù hợp. Nó là tổng của nhiều ảnh hưởng nhỏ độc lập? Phân phối chuẩn có thể phù hợp do định lý giới hạn trung tâm.

Thứ ba, xem xét **mục đích của mô hình**. Trong phân tích Bayesian, chúng ta thường chọn phân phối dựa trên tính liên hợp (conjugacy) để đơn giản hóa tính toán, hoặc dựa trên khả năng mã hóa kiến thức prior một cách tự nhiên. Đôi khi, một phân phối không hoàn hảo nhưng đủ tốt và dễ làm việc là lựa chọn thực tế hơn một phân phối phức tạp hơn nhưng chính xác hơn.

Cuối cùng, luôn **kiểm tra giả định**. Sau khi fit một mô hình, hãy kiểm tra xem phân phối được chọn có phù hợp với dữ liệu không thông qua các công cụ như biểu đồ, Q-Q plots, và posterior predictive checks. Nếu không phù hợp, hãy sẵn sàng thử các phân phối khác hoặc xây dựng các mô hình phức tạp hơn.

## Ý nghĩa cho Suy diễn Bayesian

Tất cả các phân phối chúng ta đã thảo luận sẽ xuất hiện lặp đi lặp lại trong khóa học này. Phân phối Binomial và Poisson sẽ mô hình hóa dữ liệu đếm. Phân phối chuẩn sẽ mô hình hóa sai số và nhiều đại lượng liên tục khác. Phân phối Beta sẽ là prior tự nhiên cho xác suất. Phân phối Gamma sẽ là prior cho các tham số tốc độ và độ chính xác.

Nhưng quan trọng hơn những ứng dụng cụ thể này là cách tư duy mà các phân phối xác suất khuyến khích. Trong phân tích Bayesian, chúng ta không chỉ fit dữ liệu vào các mô hình; chúng ta xây dựng các câu chuyện xác suất về cách dữ liệu có thể được sinh ra. Mỗi phân phối đại diện cho một câu chuyện như vậy, một giả thuyết về cơ chế cơ bản tạo ra dữ liệu.

Khi bạn tiến xa hơn trong khóa học này, hãy luôn tự hỏi: "Câu chuyện mà mô hình này đang kể là gì? Nó có hợp lý với những gì tôi biết về vấn đề không? Những giả định nào đang được đưa ra, và chúng có thể bị vi phạm như thế nào?" Cách tư duy này sẽ giúp bạn không chỉ áp dụng các phương pháp Bayesian một cách máy móc, mà còn sử dụng chúng một cách sáng tạo và phê phán để giải quyết các vấn đề thực tế.

## Bài tập

**Bài tập 1: Nhận diện Phân phối.** Cho mỗi tình huống sau, xác định phân phối xác suất nào có thể phù hợp nhất và giải thích lý do: (a) Số lượng khách hàng đến một cửa hàng trong một giờ. (b) Chiều cao của sinh viên nam trong một trường đại học. (c) Thời gian cho đến khi một bóng đèn cháy. (d) Số lần xuất hiện mặt Ngửa trong 20 lần toss đồng xu. (e) Tỷ lệ cử tri ủng hộ một ứng cử viên trong một cuộc bầu cử.

**Bài tập 2: Tính toán với Phân phối Binomial.** Một loại thuốc có xác suất chữa khỏi bệnh là 0.7. Nếu 10 bệnh nhân được điều trị độc lập: (a) Tính xác suất đúng 7 bệnh nhân được chữa khỏi. (b) Tính xác suất ít nhất 8 bệnh nhân được chữa khỏi. (c) Số lượng bệnh nhân được chữa khỏi kỳ vọng là bao nhiêu? Giải thích ý nghĩa thực tế của các con số này.

**Bài tập 3: Phân phối Chuẩn và Quy tắc 68-95-99.7.** Điểm số IQ được chuẩn hóa để tuân theo phân phối chuẩn với trung bình 100 và độ lệch chuẩn 15. (a) Khoảng 68% dân số có điểm IQ trong khoảng nào? (b) Một người có IQ 130 thuộc top bao nhiêu phần trăm? (c) Nếu chúng ta chọn ngẫu nhiên 100 người, chúng ta kỳ vọng bao nhiêu người có IQ trên 115?

**Bài tập 4: Phân phối Beta như Prior.** Giả sử bạn tin rằng xác suất một đồng xu ra Ngửa là khoảng 0.5, nhưng bạn không chắc chắn. (a) Vẽ (hoặc mô tả) hàm mật độ của phân phối Beta(2, 2), Beta(5, 5), và Beta(10, 10). (b) Tất cả ba phân phối này đều có trung bình 0.5. Chúng khác nhau như thế nào về mức độ chắc chắn? (c) Nếu bạn rất chắc chắn rằng đồng xu công bằng, bạn nên chọn phân phối nào? Nếu bạn không chắc chắn lắm thì sao?

**Bài tập 5: Định lý Giới hạn Trung tâm (Thực nghiệm).** Sử dụng R hoặc Python, thực hiện thí nghiệm sau: (a) Sinh 1000 mẫu, mỗi mẫu gồm 30 số ngẫu nhiên từ phân phối đồng nhất trên [0, 1]. (b) Tính trung bình của mỗi mẫu. (c) Vẽ histogram của 1000 trung bình này. (d) Phân phối có hình dạng gì? So sánh với phân phối chuẩn. (e) Lặp lại với kích thước mẫu 5 và 100. Bạn quan sát được gì?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Appendix A: Standard probability distributions
- Chapter 2: Single-parameter models (Beta-Binomial, Poisson-Gamma)

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 4: What is This Stuff Called Probability?
- Chapter 6: Inferring a Binomial Probability via Exact Mathematical Analysis

### Supplementary Reading:

**Wasserman, L. (2004).** *All of Statistics: A Concise Course in Statistical Inference*. Springer.
- Chapters 2-3: Random variables and distributions

---

*Bài học tiếp theo: [0.3 Thống kê Mô tả](/vi/chapter00/descriptive-statistics/)*
