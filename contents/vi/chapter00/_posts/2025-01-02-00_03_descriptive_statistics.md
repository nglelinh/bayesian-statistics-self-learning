---
layout: post
title: "Bài 0.3: Thống kê Mô tả - Ngôn ngữ Đầu tiên của Dữ liệu"
chapter: '00'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu rằng thống kê mô tả không chỉ là việc tính toán các con số tóm tắt, mà là nghệ thuật kể câu chuyện về dữ liệu. Bạn sẽ học cách sử dụng các thống kê như trung bình, trung vị, và độ lệch chuẩn không phải như những công thức máy móc, mà như những công cụ để hiểu cấu trúc, xu hướng, và sự biến thiên trong dữ liệu. Quan trọng hơn, bạn sẽ phát triển trực giác về khi nào nên sử dụng từng thống kê, và làm thế nào để diễn giải chúng trong bối cảnh của phân tích Bayesian, nơi mà việc hiểu phân phối của dữ liệu là bước đầu tiên quan trọng trước khi xây dựng mô hình.

## Giới thiệu: Tại sao chúng ta cần Thống kê Mô tả?

Hãy tưởng tượng bạn nhận được một tập dữ liệu chứa chiều cao của 10,000 người trưởng thành. Làm thế nào bạn có thể hiểu được dữ liệu này? Bạn không thể nhìn vào từng con số riêng lẻ và rút ra kết luận có ý nghĩa. Bạn cần một cách để tóm tắt, để nắm bắt bản chất của dữ liệu trong một vài con số hoặc hình ảnh có thể hiểu được.

Đây chính là vai trò của thống kê mô tả. Chúng cung cấp cho chúng ta một ngôn ngữ để nói về dữ liệu, một cách để truyền đạt những gì chúng ta thấy trong hàng nghìn hoặc hàng triệu điểm dữ liệu thành một vài đặc điểm quan trọng. Thống kê mô tả trả lời các câu hỏi cơ bản: Giá trị "điển hình" là gì? Dữ liệu phân tán như thế nào? Có giá trị bất thường nào không? Phân phối có đối xứng hay lệch?

Trong phân tích Bayesian, thống kê mô tả đóng vai trò đặc biệt quan trọng. Trước khi chúng ta xây dựng một mô hình xác suất phức tạp, chúng ta cần hiểu dữ liệu của mình. Chúng ta cần biết phân phối nào có thể phù hợp, tham số nào cần ước lượng, và giả định nào có thể bị vi phạm. Thống kê mô tả là bước đầu tiên trong hành trình này, giúp chúng ta xây dựng trực giác về dữ liệu trước khi chúng ta bắt đầu mô hình hóa.

## Thống kê Vị trí Trung tâm: Tìm kiếm Giá trị "Điển hình"

Một trong những câu hỏi đầu tiên chúng ta thường hỏi về một tập dữ liệu là: "Giá trị điển hình là gì?" Nhưng "điển hình" có thể có nhiều ý nghĩa khác nhau, và đó là lý do tại sao chúng ta có nhiều thống kê vị trí trung tâm khác nhau.

### Trung bình: Điểm Cân bằng

**Trung bình số học** (arithmetic mean) là thống kê vị trí trung tâm quen thuộc nhất. Với một tập dữ liệu $$x_1, x_2, \ldots, x_n$$, trung bình được định nghĩa là:

$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

Trung bình có một diễn giải hình học đẹp đẽ: nó là điểm cân bằng của dữ liệu. Nếu bạn tưởng tượng mỗi điểm dữ liệu như một khối lượng trên một thanh thẳng, trung bình là điểm mà thanh sẽ cân bằng. Hình thức hóa hơn, trung bình là giá trị mà tổng các độ lệch từ nó bằng không: $$\sum_{i=1}^{n} (x_i - \bar{x}) = 0$$.

Tuy nhiên, trung bình có một điểm yếu quan trọng: nó rất nhạy cảm với các giá trị ngoại lai (outliers). Một giá trị cực đoan duy nhất có thể kéo trung bình đi xa khỏi phần lớn dữ liệu. Hãy xem xét một ví dụ: thu nhập của 10 người, trong đó 9 người kiếm từ 30,000 đến 50,000 đô la mỗi năm, và một người kiếm 1,000,000 đô la. Trung bình sẽ là khoảng 130,000 đô la, một con số không đại diện cho thu nhập "điển hình" của nhóm này.

Trong phân tích Bayesian, trung bình thường xuất hiện như tham số vị trí của phân phối chuẩn. Khi chúng ta mô hình hóa dữ liệu như $$y_i \sim \mathcal{N}(\mu, \sigma^2)$$, $$\mu$$ là trung bình của phân phối, và ước lượng tự nhiên của nó từ dữ liệu là trung bình mẫu $$\bar{x}$$.

### Trung vị: Giá trị Giữa

**Trung vị** (median) là giá trị ở giữa khi dữ liệu được sắp xếp theo thứ tự tăng dần. Nếu số lượng quan sát $$n$$ là lẻ, trung vị là giá trị thứ $$(n+1)/2$$. Nếu $$n$$ là chẵn, trung vị thường được định nghĩa là trung bình của hai giá trị giữa.

Trung vị có một tính chất quan trọng: nó là **robust** (bền vững) với các giá trị ngoại lai. Bạn có thể thay đổi các giá trị cực đoan trong dữ liệu mà không ảnh hưởng đến trung vị, miễn là bạn không thay đổi thứ tự của các giá trị xung quanh điểm giữa. Trong ví dụ thu nhập ở trên, trung vị sẽ vẫn nằm trong khoảng 30,000-50,000 đô la, phản ánh tốt hơn thu nhập "điển hình".

Trung vị cũng có một diễn giải xác suất tự nhiên: nó là giá trị mà xác suất quan sát được một giá trị nhỏ hơn nó bằng 50%, và xác suất quan sát được một giá trị lớn hơn nó cũng bằng 50%. Đây là phân vị thứ 50 (50th percentile) của phân phối.

Trong phân tích Bayesian, trung vị thường được sử dụng để tóm tắt phân phối posterior, đặc biệt khi phân phối không đối xứng. Thay vì báo cáo trung bình posterior (có thể bị ảnh hưởng bởi đuôi dài), chúng ta thường báo cáo trung vị posterior cùng với khoảng tin cậy.

### So sánh Trung bình và Trung vị: Phát hiện Độ lệch

Mối quan hệ giữa trung bình và trung vị cho chúng ta thông tin về hình dạng của phân phối. Nếu phân phối đối xứng, trung bình và trung vị sẽ gần bằng nhau. Nếu phân phối lệch phải (có đuôi dài ở bên phải), trung bình sẽ lớn hơn trung vị vì nó bị kéo về phía các giá trị lớn. Nếu phân phối lệch trái, trung bình sẽ nhỏ hơn trung vị.

Sự khác biệt này không chỉ là một chi tiết kỹ thuật. Nó cho chúng ta biết liệu phân phối chuẩn có phải là mô hình phù hợp hay không. Nếu trung bình và trung vị khác nhau đáng kể, chúng ta có thể cần xem xét các phân phối lệch như log-normal, gamma, hoặc beta, tùy thuộc vào bản chất của dữ liệu.

## Thống kê Phân tán: Đo lường Sự Không chắc chắn

Biết giá trị trung tâm là không đủ. Hai tập dữ liệu có thể có cùng trung bình nhưng rất khác nhau về độ phân tán. Một tập có thể tập trung chặt chẽ xung quanh trung bình, trong khi tập kia có thể phân tán rộng. Các thống kê phân tán giúp chúng ta định lượng sự biến thiên này.

### Phương sai và Độ lệch Chuẩn: Độ lệch Bình phương Trung bình

**Phương sai mẫu** (sample variance) đo lường độ phân tán trung bình của dữ liệu xung quanh trung bình:

$$s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

Lưu ý rằng chúng ta chia cho $$n-1$$ chứ không phải $$n$$. Đây là **hiệu chỉnh Bessel** (Bessel's correction), được sử dụng để làm cho phương sai mẫu là một ước lượng không chệch (unbiased estimator) của phương sai tổng thể. Lý do cho hiệu chỉnh này là chúng ta đã sử dụng dữ liệu để ước lượng trung bình $$\bar{x}$$, và điều này làm giảm một "bậc tự do" (degree of freedom).

Phương sai có một vấn đề thực tế: đơn vị của nó là bình phương của đơn vị dữ liệu gốc. Nếu chúng ta đo chiều cao bằng cm, phương sai sẽ có đơn vị là cm². Điều này làm cho phương sai khó diễn giải. Để khắc phục, chúng ta sử dụng **độ lệch chuẩn** (standard deviation):

$$s = \sqrt{s^2}$$

Độ lệch chuẩn có cùng đơn vị với dữ liệu gốc và có thể được diễn giải như "độ lệch điển hình" từ trung bình.

Trong phân tích Bayesian, phương sai (hoặc độ chính xác, nghịch đảo của phương sai) là một tham số quan trọng cần được ước lượng. Khi chúng ta mô hình hóa dữ liệu như $$y_i \sim \mathcal{N}(\mu, \sigma^2)$$, $$\sigma^2$$ là phương sai, và ước lượng tự nhiên của nó là phương sai mẫu $$s^2$$.

### Phân vị và Khoảng Tứ phân vị: Thống kê Robust

**Phân vị** (quantiles hoặc percentiles) chia phân phối thành các phần bằng nhau. Phân vị thứ $$p$$ ($$0 < p < 1$$) là giá trị mà $$100p\%$$ dữ liệu nhỏ hơn hoặc bằng nó. Ví dụ, phân vị thứ 0.25 (còn gọi là tứ phân vị thứ nhất, Q1) là giá trị mà 25% dữ liệu nhỏ hơn hoặc bằng nó.

**Khoảng tứ phân vị** (interquartile range, IQR) là khoảng cách giữa tứ phân vị thứ ba (Q3) và tứ phân vị thứ nhất (Q1):

$$\text{IQR} = Q3 - Q1$$

IQR chứa 50% dữ liệu ở giữa và là một thống kê phân tán robust với các giá trị ngoại lai. Nó thường được sử dụng để phát hiện outliers: các giá trị nằm ngoài khoảng $$[Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}]$$ thường được coi là outliers tiềm năng.

Trong phân tích Bayesian, phân vị được sử dụng rộng rãi để tóm tắt phân phối posterior. Thay vì chỉ báo cáo trung bình hoặc trung vị, chúng ta thường báo cáo **khoảng tin cậy** (credible interval), ví dụ như khoảng 95% chứa 95% xác suất posterior. Khoảng này thường được xây dựng từ các phân vị, ví dụ từ phân vị thứ 0.025 đến phân vị thứ 0.975.

## Trực quan hóa: Nhìn thấy Câu chuyện trong Dữ liệu

Các con số tóm tắt là hữu ích, nhưng chúng không thể thay thế được việc nhìn vào dữ liệu. Trực quan hóa cho phép chúng ta thấy các mẫu hình, xu hướng, và bất thường mà các thống kê tóm tắt có thể bỏ lỡ. Trong phân tích Bayesian, trực quan hóa không chỉ là công cụ khám phá ban đầu, mà còn là cách chúng ta kiểm tra mô hình và truyền đạt kết quả.

### Histogram: Ước lượng Phân phối

**Histogram** là một trong những công cụ trực quan hóa cơ bản nhất. Nó chia dữ liệu thành các khoảng (bins) và đếm số lượng quan sát trong mỗi khoảng. Chiều cao của mỗi thanh tỷ lệ với tần số (hoặc mật độ) của dữ liệu trong khoảng đó.

Histogram có thể được xem như một ước lượng thô của hàm mật độ xác suất. Khi số lượng dữ liệu tăng và độ rộng của bins giảm, histogram tiến gần đến PDF thực sự của phân phối. Đây là ý tưởng đằng sau **ước lượng mật độ kernel** (kernel density estimation), một kỹ thuật tinh vi hơn để ước lượng PDF từ dữ liệu.

Một câu hỏi quan trọng khi vẽ histogram là: nên sử dụng bao nhiêu bins? Quá ít bins sẽ làm mất chi tiết, trong khi quá nhiều bins sẽ tạo ra nhiễu. Không có câu trả lời hoàn hảo, nhưng các quy tắc như quy tắc Sturges ($$k = \lceil \log_2 n \rceil + 1$$) hoặc quy tắc Scott có thể cung cấp điểm khởi đầu tốt.

### Box Plot: Tóm tắt Năm Số

**Box plot** (biểu đồ hộp) là một cách trực quan hóa năm thống kê tóm tắt quan trọng: giá trị nhỏ nhất, Q1, trung vị, Q3, và giá trị lớn nhất. Hộp chứa 50% dữ liệu ở giữa (từ Q1 đến Q3), đường trong hộp là trung vị, và các "râu" (whiskers) kéo dài đến các giá trị cực đoan (thường là $$1.5 \times \text{IQR}$$ từ các cạnh của hộp). Các điểm nằm ngoài râu được vẽ riêng như outliers tiềm năng.

Box plot đặc biệt hữu ích để so sánh nhiều nhóm. Chúng ta có thể vẽ nhiều box plots cạnh nhau để so sánh phân phối của các nhóm khác nhau, giúp phát hiện sự khác biệt về vị trí trung tâm, độ phân tán, và độ lệch.

### Scatter Plot: Khám phá Mối quan hệ

Khi chúng ta có hai biến, **scatter plot** (biểu đồ phân tán) cho phép chúng ta thấy mối quan hệ giữa chúng. Mỗi điểm đại diện cho một quan sát, với tọa độ x và y tương ứng với giá trị của hai biến.

Scatter plot giúp chúng ta trả lời các câu hỏi như: Hai biến có tương quan không? Mối quan hệ có tuyến tính hay phi tuyến? Có outliers hoặc nhóm riêng biệt nào không? Những câu hỏi này rất quan trọng trong phân tích Bayesian, vì chúng hướng dẫn chúng ta trong việc lựa chọn mô hình phù hợp.

## Tương quan: Đo lường Mối quan hệ Tuyến tính

Khi chúng ta quan sát mối quan hệ giữa hai biến trong scatter plot, chúng ta thường muốn định lượng mức độ mạnh của mối quan hệ đó. **Hệ số tương quan Pearson** cung cấp một thước đo cho mối quan hệ tuyến tính:

$$r = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}$$

Hệ số tương quan luôn nằm giữa -1 và 1. Giá trị $$r = 1$$ chỉ ra mối quan hệ tuyến tính dương hoàn hảo, $$r = -1$$ chỉ ra mối quan hệ tuyến tính âm hoàn hảo, và $$r = 0$$ chỉ ra không có mối quan hệ tuyến tính.

Tuy nhiên, cần cẩn thận khi diễn giải tương quan. Đầu tiên, tương quan chỉ đo lường mối quan hệ **tuyến tính**. Hai biến có thể có mối quan hệ phi tuyến mạnh nhưng tương quan bằng không. Thứ hai, **tương quan không ngụ ý nhân quả**. Việc hai biến tương quan không có nghĩa là một biến gây ra biến kia; có thể có một biến thứ ba ẩn ảnh hưởng đến cả hai, hoặc mối quan hệ có thể là ngẫu nhiên.

Trong phân tích Bayesian, chúng ta thường mô hình hóa tương quan một cách rõ ràng thông qua các tham số trong mô hình. Ví dụ, trong hồi quy tuyến tính Bayesian, hệ số hồi quy $$\beta$$ mã hóa mối quan hệ giữa biến dự đoán và biến phản hồi, và chúng ta có thể định lượng sự không chắc chắn về mối quan hệ này thông qua phân phối posterior của $$\beta$$.

## Ý nghĩa cho Phân tích Dữ liệu Bayesian

Tất cả các công cụ thống kê mô tả mà chúng ta đã thảo luận không chỉ là bước chuẩn bị cho phân tích Bayesian, mà còn là phần không thể thiếu của nó. Trước khi chúng ta xây dựng một mô hình Bayesian, chúng ta cần hiểu dữ liệu của mình thông qua thống kê mô tả và trực quan hóa. Điều này giúp chúng ta:

**Lựa chọn Phân phối Phù hợp.** Histogram và box plot cho chúng ta thấy hình dạng của phân phối, giúp chúng ta quyết định liệu phân phối chuẩn, log-normal, Poisson, hay một phân phối khác có phù hợp không.

**Phát hiện Outliers và Bất thường.** Các giá trị ngoại lai có thể chỉ ra lỗi đo lường, hoặc chúng có thể là các quan sát hợp lệ nhưng cực đoan. Trong phân tích Bayesian, chúng ta có thể mô hình hóa outliers một cách rõ ràng thông qua các mô hình robust (ví dụ, sử dụng phân phối Student-t thay vì chuẩn).

**Xây dựng Prior Có thông tin.** Thống kê mô tả từ dữ liệu trước đó hoặc kiến thức chuyên môn có thể giúp chúng ta xây dựng prior có thông tin. Ví dụ, nếu chúng ta biết từ nghiên cứu trước rằng trung bình của một tham số nằm trong một khoảng nhất định, chúng ta có thể sử dụng thông tin này để xây dựng prior.

**Kiểm tra Mô hình.** Sau khi fit một mô hình Bayesian, chúng ta sử dụng thống kê mô tả và trực quan hóa để kiểm tra xem mô hình có phù hợp với dữ liệu không. Chúng ta so sánh phân phối posterior predictive với dữ liệu quan sát, sử dụng các công cụ như histogram, scatter plot, và các thống kê tóm tắt.

**Truyền đạt Kết quả.** Cuối cùng, chúng ta sử dụng thống kê mô tả và trực quan hóa để truyền đạt kết quả của phân tích Bayesian. Thay vì chỉ báo cáo các ước lượng điểm, chúng ta báo cáo phân phối posterior đầy đủ thông qua histogram, box plot, và các khoảng tin cậy.

## Bài tập

**Bài tập 1: Tính toán Thống kê Mô tả.** Cho dữ liệu điểm thi của 20 sinh viên: [45, 67, 78, 82, 55, 90, 88, 76, 95, 20, 85, 72, 68, 91, 77, 83, 65, 89, 74, 80]. (a) Tính trung bình, trung vị, và mode. (b) Tính phương sai, độ lệch chuẩn, và IQR. (c) Phát hiện outliers sử dụng quy tắc $$1.5 \times \text{IQR}$$. (d) Giải thích tại sao trung bình và trung vị khác nhau, và điều này nói gì về phân phối của dữ liệu.

**Bài tập 2: Trực quan hóa và Diễn giải.** Sử dụng Python để sinh 1000 quan sát từ: (a) Phân phối chuẩn $$\mathcal{N}(50, 10^2)$$. (b) Phân phối log-normal với tham số $$\mu = 3.5, \sigma = 0.5$$. Với mỗi phân phối, vẽ histogram và box plot, tính trung bình và trung vị, và giải thích sự khác biệt giữa hai phân phối dựa trên các thống kê và biểu đồ.

**Bài tập 3: Tương quan và Nhân quả.** Xem xét hai biến: (a) Doanh số bán kem và số vụ đuối nước (cả hai đều cao vào mùa hè). (b) Số giờ học và điểm thi. Đối với mỗi cặp, thảo luận: Chúng có tương quan không? Có mối quan hệ nhân quả không? Nếu có tương quan nhưng không có nhân quả, giải thích tại sao. Điều này dạy chúng ta gì về việc diễn giải tương quan?

**Bài tập 4: Phát hiện Phân phối.** Cho ba tập dữ liệu (bạn có thể sinh chúng hoặc sử dụng dữ liệu thực): (a) Chiều cao của người trưởng thành. (b) Số lượng email nhận được mỗi ngày. (c) Thời gian chờ đợi giữa các cuộc gọi đến tổng đài. Với mỗi tập dữ liệu, vẽ histogram, tính các thống kê mô tả, và đề xuất một phân phối xác suất phù hợp (chuẩn, Poisson, mũ, v.v.). Giải thích lý do lựa chọn của bạn.

**Bài tập 5: Khám phá Dữ liệu Thực tế.** Tải một dataset thực tế (ví dụ: Iris, Boston Housing, hoặc bất kỳ dataset nào bạn quan tâm). Thực hiện phân tích khám phá dữ liệu đầy đủ: (a) Tính các thống kê mô tả cho tất cả các biến số. (b) Vẽ histogram và box plot cho các biến liên tục. (c) Vẽ scatter plot và tính tương quan cho các cặp biến. (d) Phát hiện và thảo luận về outliers. (e) Viết một đoạn văn ngắn tóm tắt những gì bạn học được về dữ liệu, và đề xuất các phân phối và mô hình có thể phù hợp cho phân tích Bayesian.

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 6: Model checking and improvement (posterior predictive checks)

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 3: The R Programming Language (data exploration)

### Supplementary Reading:

**Tukey, J. W. (1977).** *Exploratory Data Analysis*. Addison-Wesley.
- Classic text on EDA philosophy and techniques

**Wickham, H., & Grolemund, G. (2017).** *R for Data Science*. O'Reilly Media.
- Chapter 7: Exploratory Data Analysis

---

*Bài học tiếp theo: [0.4 Python Cơ bản cho Data Science](/vi/chapter00/python-basics/)*
