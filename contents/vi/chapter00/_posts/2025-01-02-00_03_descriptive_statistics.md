---
layout: post
title: "Bài 0.6: Thống kê Mô tả - Ngôn ngữ Đầu tiên của Dữ liệu"
chapter: '00'
order: 6
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu rằng thống kê mô tả không chỉ là việc tính các con số tóm tắt, mà là cách nắm bắt cấu trúc, xu hướng và mức độ biến thiên của dữ liệu. Bạn sẽ biết cách diễn giải trung bình, trung vị và độ lệch chuẩn theo bản chất dữ liệu thay vì áp dụng máy móc, đồng thời hình thành trực giác chọn thống kê phù hợp trong phân tích Bayesian — nơi việc khám phá phân phối dữ liệu luôn là bước khởi đầu trước khi xây dựng mô hình.

## Giới thiệu: Tại sao chúng ta cần Thống kê Mô tả?

Giả sử bạn nhận được tập dữ liệu chiều cao của 10,000 người trưởng thành. Việc nhìn từng giá trị riêng lẻ không thể cho bạn kết luận rõ ràng; bạn cần những đại lượng tóm tắt và biểu đồ để nắm được đặc điểm chính của tập dữ liệu.

Đó là vai trò của thống kê mô tả. Nó giúp thu gọn hàng nghìn hay hàng triệu quan sát thành một số đặc trưng dễ theo dõi, trả lời các câu hỏi nền tảng: giá trị "điển hình" nằm ở đâu, dữ liệu phân tán mạnh hay yếu, có giá trị bất thường nào không, và phân phối đối xứng hay bị lệch?

Trong phân tích Bayesian, bước này càng quan trọng. Trước khi thiết lập một mô hình xác suất, ta cần hiểu dữ liệu để chọn họ phân phối phù hợp, xác định tham số cần ước lượng và nhận diện sớm các giả định có nguy cơ bị vi phạm.

## Thống kê Vị trí Trung tâm: Tìm kiếm Giá trị "Điển hình"

Câu hỏi đầu tiên khi tiếp cận dữ liệu thường là "giá trị điển hình là gì?". Tuy nhiên, khái niệm "điển hình" có nhiều cách hiểu khác nhau, nên ta có nhiều thước đo vị trí trung tâm tương ứng.

### Trung bình: Điểm Cân bằng

**Trung bình số học** (arithmetic mean) là thước đo vị trí trung tâm quen thuộc nhất. Với tập dữ liệu $$x_1, x_2, \ldots, x_n$$, trung bình được định nghĩa là:

$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

Về mặt hình học, trung bình đóng vai trò như điểm cân bằng của dữ liệu: nếu coi mỗi điểm dữ liệu là một vật nặng đặt trên một thanh thẳng, thanh sẽ cân bằng tại $$\bar{x}$$. Một cách hình thức, trung bình là giá trị làm tổng các độ lệch so với nó bằng không: $$\sum_{i=1}^{n} (x_i - \bar{x}) = 0$$.

Điểm yếu lớn của trung bình là rất nhạy cảm với giá trị ngoại lai (outlier): chỉ một giá trị cực lớn cũng có thể kéo trung bình ra xa phần lớn dữ liệu. Chẳng hạn, xét thu nhập của 10 người, trong đó 9 người kiếm từ 30,000 đến 50,000 đô la mỗi năm và một người kiếm 1,000,000 đô la. Khi đó trung bình khoảng 130,000 đô la — con số không phản ánh mức thu nhập điển hình của nhóm.

Trong phân tích Bayesian, trung bình thường gắn với tham số vị trí của phân phối chuẩn. Khi mô hình hóa dữ liệu dưới dạng $$y_i \sim \mathcal{N}(\mu, \sigma^2)$$, $$\mu$$ là trung bình của phân phối và trung bình mẫu $$\bar{x}$$ là ước lượng tự nhiên từ dữ liệu.

### Trung vị: Giá trị Giữa

**Trung vị** (median) là giá trị nằm chính giữa khi sắp xếp dữ liệu theo thứ tự tăng dần. Nếu số quan sát $$n$$ là lẻ, trung vị là giá trị thứ $$(n+1)/2$$; nếu $$n$$ là chẵn, trung vị là trung bình của hai giá trị ở giữa.

Ưu điểm nổi bật của trung vị là tính **bền vững (robust)** trước các giá trị ngoại lai. Việc thay đổi các giá trị cực đoan không làm thay đổi trung vị, miễn là thứ tự quanh điểm giữa giữ nguyên. Trong ví dụ thu nhập ở trên, trung vị vẫn nằm trong khoảng 30,000–50,000 đô la, phản ánh sát hơn thu nhập điển hình của nhóm.

Trung vị cũng có diễn giải xác suất rõ ràng: xác suất quan sát một giá trị nhỏ hơn trung vị là 50%, và lớn hơn trung vị cũng là 50% (tức phân vị thứ 50). Trong phân tích Bayesian, khi phân phối hậu nghiệm (posterior) bị lệch hoặc có đuôi dài, người ta thường dùng trung vị hậu nghiệm kèm khoảng tin cậy thay vì chỉ báo cáo trung bình hậu nghiệm.

### So sánh Trung bình và Trung vị: Phát hiện Độ lệch

So sánh trung bình và trung vị giúp nhận diện hình dạng phân phối. Nếu phân phối đối xứng, trung bình và trung vị gần bằng nhau. Nếu phân phối lệch phải (đuôi dài về phía giá trị lớn), trung bình lớn hơn trung vị; nếu lệch trái, trung bình nhỏ hơn trung vị.

Thông tin này có ý nghĩa trực tiếp khi chọn mô hình: nếu trung bình và trung vị chênh lệch rõ rệt, phân phối chuẩn có thể không phù hợp và ta nên cân nhắc các phân phối lệch như log-normal, Gamma hoặc Beta tùy theo bản chất dữ liệu.

*Cách đọc hình: Hai hình dưới đây tách riêng hai trường hợp để bạn nhìn rõ vị trí tương đối giữa trung bình và trung vị trong từng dạng phân phối.*

![Phân phối đối xứng với trung bình gần trung vị]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_mean_median_symmetric.png)

*Hình 1a: Ở phân phối gần đối xứng, trung bình và trung vị gần như trùng nhau.*

![Phân phối lệch phải với trung bình bị kéo về phía đuôi]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_mean_median_right_skewed.png)

*Hình 1b: Khi dữ liệu lệch phải, đuôi dài kéo trung bình sang phải mạnh hơn trung vị — một dấu hiệu trực quan quan trọng trước khi chọn mô hình.*

### Một ví dụ ngắn: trung bình và trung vị kể hai câu chuyện khác nhau

Giả sử thu nhập tháng (triệu đồng) của 10 người là:

$$
30,\ 31,\ 32,\ 33,\ 34,\ 35,\ 36,\ 37,\ 38,\ 120
$$

Khi đó:

- Trung bình là $$42.6$$.
- Trung vị là $$34.5$$.

Nếu chỉ báo cáo trung bình, người đọc dễ lầm tưởng mức thu nhập điển hình vượt quá 40 triệu, trong khi thực tế 9/10 người nằm trong khoảng 30–38 triệu và chỉ một giá trị cực lớn đã kéo trung bình lên cao. Ví dụ này cho thấy các chỉ số thống kê mô tả cần được đọc song song thay vì dựa vào một con số đơn lẻ.

## Thống kê Phân tán: Đo lường Sự Không chắc chắn

Chỉ biết vị trí trung tâm là chưa đủ. Hai tập dữ liệu có thể có cùng trung bình nhưng mức độ biến thiên rất khác nhau: một tập tập trung chặt quanh trung bình, tập kia phân tán rộng. Các thống kê phân tán giúp định lượng sự biến thiên đó.

### Phương sai và Độ lệch Chuẩn: Độ lệch Bình phương Trung bình

**Phương sai mẫu** (sample variance) đo mức độ phân tán trung bình của dữ liệu quanh trung bình mẫu:

$$s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2$$

Lưu ý mẫu số là $$n-1$$ thay vì $$n$$. Đây là **hiệu chỉnh Bessel** (Bessel's correction), giúp phương sai mẫu trở thành ước lượng không chệch (unbiased estimator) của phương sai tổng thể, do ta đã dùng dữ liệu để ước lượng $$\bar{x}$$ làm mất đi một bậc tự do (degree of freedom).

Hạn chế của phương sai là đơn vị đo bị bình phương so với dữ liệu gốc (ví dụ chiều cao đo bằng cm thì phương sai có đơn vị cm²), khiến việc diễn giải trực tiếp kém tự nhiên. Vì vậy, ta thường dùng **độ lệch chuẩn** (standard deviation):

$$s = \sqrt{s^2}$$

Độ lệch chuẩn có cùng đơn vị với dữ liệu gốc và có thể hiểu như độ lệch điển hình của các quan sát so với trung bình. Trong phân tích Bayesian, phương sai (hoặc độ chính xác — nghịch đảo của phương sai) là tham số then chốt cần ước lượng; chẳng hạn với mô hình $$y_i \sim \mathcal{N}(\mu, \sigma^2)$$, $$\sigma^2$$ là phương sai và $$s^2$$ là ước lượng tự nhiên từ mẫu.

### Phân vị và Khoảng Tứ phân vị: Thống kê Bền vững

**Phân vị** (quantile hoặc percentile) chia phân phối theo tỷ lệ phần trăm. Phân vị thứ $$p$$ ($$0 < p < 1$$) là giá trị mà $$100p\%$$ dữ liệu nhỏ hơn hoặc bằng nó; ví dụ phân vị 0.25 (tứ phân vị thứ nhất, Q1) là mốc có 25% dữ liệu nhỏ hơn hoặc bằng nó.

**Khoảng tứ phân vị** (interquartile range, IQR) là hiệu giữa tứ phân vị thứ ba (Q3) và tứ phân vị thứ nhất (Q1):

$$\text{IQR} = Q3 - Q1$$

IQR bao phủ 50% dữ liệu ở giữa và bền vững trước giá trị ngoại lai. Quy tắc phổ biến để nhận diện giá trị ngoại lai tiềm năng là kiểm tra các điểm nằm ngoài đoạn $$[Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}]$$.

Trong phân tích Bayesian, phân vị được dùng rộng rãi để tóm tắt phân phối hậu nghiệm. Bên cạnh trung bình hoặc trung vị, ta thường báo cáo **khoảng tin cậy** (credible interval), chẳng hạn khoảng 95% được xác định từ phân vị 0.025 đến phân vị 0.975, chứa 95% khối lượng xác suất hậu nghiệm.

*Cách đọc hình: Hai hình dưới đây tách riêng câu chuyện về độ phân tán theo độ lệch chuẩn và cách biểu diễn IQR trên biểu đồ hộp (box plot).*

![Hai phân phối có cùng trung bình nhưng độ phân tán khác nhau]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_spread_same_mean_diff_sd.png)

*Hình 2a: Hai tập dữ liệu có trung bình gần như bằng nhau nhưng độ phân tán khác nhau rõ rệt.*

![Box plot thể hiện IQR và outlier]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_boxplot_iqr_outliers.png)

*Hình 2b: Biểu đồ hộp hiển thị phần hộp chứa 50% dữ liệu ở giữa, đường trung vị bên trong hộp, và các điểm đỏ đánh dấu giá trị ngoại lai tiềm năng theo quy tắc $$1.5 \times \text{IQR}$$.*

## Trực quan hóa: Nhìn thấy Câu chuyện trong Dữ liệu

Các chỉ số tóm tắt rất hữu ích nhưng không thể thay thế việc quan sát trực tiếp dữ liệu. Trực quan hóa giúp phát hiện cấu trúc, xu hướng và điểm bất thường mà các con số tóm tắt dễ bỏ sót. Trong phân tích Bayesian, biểu đồ vừa phục vụ bước khám phá ban đầu, vừa hỗ trợ kiểm tra mô hình và trình bày kết quả.

### Histogram: Ước lượng Phân phối

**Histogram** chia miền dữ liệu thành các khoảng (bin) và đếm số quan sát rơi vào từng khoảng, với chiều cao mỗi cột tỷ lệ với tần số hoặc mật độ trong khoảng đó.

Có thể xem histogram như một ước lượng thô của hàm mật độ xác suất (PDF). Khi cỡ mẫu tăng và độ rộng khoảng giảm, histogram tiến gần tới PDF thực của phân phối — đây cũng là nền tảng của **ước lượng mật độ hạt nhân** (kernel density estimation, KDE). Khi vẽ histogram, việc chọn số lượng bin rất quan trọng: quá ít bin làm mất chi tiết hình dạng, còn quá nhiều bin dễ gây nhiễu. Các quy tắc kinh nghiệm như quy tắc Sturges ($$k = \lceil \log_2 n \rceil + 1$$) hoặc quy tắc Scott thường là điểm khởi đầu hợp lý.

### Box Plot: Tóm tắt Năm Số

**Box plot** (biểu đồ hộp) trực quan hóa năm mốc tóm tắt: giá trị nhỏ nhất, Q1, trung vị, Q3 và giá trị lớn nhất. Phần hộp bao phủ 50% dữ liệu ở giữa (từ Q1 đến Q3), vạch ngang trong hộp là trung vị, còn hai râu (whiskers) kéo dài tới các quan sát cực trị trong ngưỡng (thường tối đa $$1.5 \times \text{IQR}$$ tính từ hai cạnh hộp); những điểm vượt ngoài ngưỡng được vẽ riêng như giá trị ngoại lai tiềm năng.

Biểu đồ hộp đặc biệt tiện lợi khi so sánh nhiều nhóm song song, giúp nhận ra nhanh sự khác biệt về vị trí trung tâm, độ phân tán và độ lệch giữa các nhóm.

### Scatter Plot: Khám phá Mối quan hệ

Với hai biến số, **scatter plot** (biểu đồ phân tán) biểu diễn mỗi quan sát bằng một điểm có tọa độ $$(x, y)$$. Biểu đồ này giúp kiểm tra hai biến có tương quan hay không, quan hệ có dạng tuyến tính hay phi tuyến, và dữ liệu có giá trị ngoại lai hay tách thành nhiều cụm riêng biệt hay không — những thông tin trực tiếp định hướng việc chọn mô hình Bayesian.

## Tương quan: Đo lường Mối quan hệ Tuyến tính

Để định lượng độ mạnh của mối quan hệ tuyến tính thấy trên biểu đồ phân tán, ta dùng **hệ số tương quan Pearson**:

$$r = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}$$

Hệ số $$r$$ luôn nằm trong đoạn $$[-1, 1]$$: $$r = 1$$ ứng với quan hệ tuyến tính dương hoàn hảo, $$r = -1$$ ứng với quan hệ tuyến tính âm hoàn hảo, và $$r = 0$$ cho thấy không có quan hệ tuyến tính.

Cần lưu ý hai điểm quan trọng khi diễn giải tương quan. Thứ nhất, hệ số Pearson chỉ đo lường quan hệ **tuyến tính**: hai biến có thể liên hệ phi tuyến rất chặt nhưng vẫn có $$r \approx 0$$. Thứ hai, **tương quan không đồng nghĩa với nhân quả**: hai biến tương quan có thể cùng chịu ảnh hưởng từ một biến ẩn thứ ba hoặc chỉ trùng hợp ngẫu nhiên.

*Cách đọc hình: Ba hình dưới đây tách riêng từng dạng quan hệ để cho thấy vì sao một hệ số tương quan duy nhất có thể che khuất cấu trúc thật của dữ liệu.*

![Quan hệ tuyến tính dương trong scatter plot]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_correlation_linear.png)

*Hình 3a: Với quan hệ tuyến tính dương, hệ số Pearson $$r$$ phản ánh khá sát xu hướng dữ liệu.*

![Quan hệ phi tuyến trong scatter plot]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_correlation_nonlinear.png)

*Hình 3b: Quan hệ phi tuyến rất rõ trên biểu đồ nhưng lại bị hệ số Pearson $$r$$ đánh giá thấp.*

![Tương quan do nhóm ẩn trong scatter plot]({{ site.baseurl }}/img/chapter_img/chapter00/descriptive_correlation_hidden_groups.png)

*Hình 3c: Tương quan tổng thể có thể phát sinh do cấu trúc nhóm ẩn, nên luôn cần quan sát biểu đồ trước khi tin vào một con số tóm tắt.*

Trong phân tích Bayesian, mối quan hệ giữa các biến thường được mô hình hóa tường minh qua tham số mô hình. Chẳng hạn, trong hồi quy tuyến tính Bayesian, hệ số hồi quy $$\beta$$ biểu diễn mối liên hệ giữa biến giải thích và biến phản hồi, còn phân phối hậu nghiệm của $$\beta$$ định lượng độ bất định quanh ước lượng đó.

## Video tham khảo

- [StatQuest: Histograms, Clearly Explained](https://www.youtube.com/watch?v=qBigTkBLU6g) — StatQuest with Josh Starmer, English. **Xem trước.** Giải thích cách dùng histogram để quan sát hình dạng phân phối trước khi tóm tắt bằng số liệu.
- [Finding mean, median, and mode | Descriptive statistics | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=k3aKKasOmIw) — Khan Academy, English. Phân biệt vai trò của trung bình, trung vị và yếu vị (mode) trong thống kê vị trí.
- [Pearson's Correlation, Clearly Explained!!!](https://www.youtube.com/watch?v=xZ_z8KWkhXE) — StatQuest with Josh Starmer, English. Trình bày ý nghĩa và giới hạn của hệ số tương quan Pearson.

## Bài tập

**Bài tập 1: Tính toán Thống kê Mô tả.** Cho dữ liệu điểm thi của 20 sinh viên: [45, 67, 78, 82, 55, 90, 88, 76, 95, 20, 85, 72, 68, 91, 77, 83, 65, 89, 74, 80]. (a) Tính trung bình, trung vị và yếu vị (mode). (b) Tính phương sai, độ lệch chuẩn và IQR. (c) Xác định giá trị ngoại lai theo quy tắc $$1.5 \times \text{IQR}$$. (d) Giải thích vì sao trung bình và trung vị khác nhau, và điều này phản ánh gì về hình dạng phân phối dữ liệu.

**Bài tập 2: Trực quan hóa và Diễn giải.** Dùng Python sinh 1000 quan sát từ: (a) phân phối chuẩn $$\mathcal{N}(50, 10^2)$$, và (b) phân phối log-normal với tham số $$\mu = 3.5, \sigma = 0.5$$. Với mỗi phân phối, vẽ histogram và box plot, tính trung bình và trung vị, rồi giải thích sự khác biệt giữa hai phân phối dựa trên thống kê và biểu đồ.

**Bài tập 3: Tương quan và Nhân quả.** Xét hai cặp biến: (a) doanh số bán kem và số vụ đuối nước (cả hai cùng tăng vào mùa hè), và (b) số giờ học và điểm thi. Với mỗi cặp, hãy phân tích: hai biến có tương quan không, có quan hệ nhân quả không, và nếu có tương quan mà không có nhân quả thì nguyên nhân là gì? Điều này rút ra lưu ý gì khi diễn giải tương quan?

**Bài tập 4: Nhận diện Phân phối.** Xét ba tập dữ liệu (có thể tự mô phỏng hoặc lấy dữ liệu thực): (a) chiều cao người trưởng thành, (b) số email nhận được mỗi ngày, và (c) thời gian chờ giữa hai cuộc gọi đến tổng đài. Với mỗi tập dữ liệu, vẽ histogram, tính thống kê mô tả và đề xuất một phân phối xác suất phù hợp (chuẩn, Poisson, mũ, v.v.), kèm giải thích.

**Bài tập 5: Khám phá Dữ liệu Thực tế.** Chọn một tập dữ liệu thực tế (ví dụ Iris, Boston Housing hoặc tập dữ liệu bạn quan tâm) và thực hiện phân tích khám phá: (a) tính thống kê mô tả cho các biến số, (b) vẽ histogram và box plot cho các biến liên tục, (c) vẽ scatter plot và tính tương quan theo cặp biến, (d) phát hiện và bàn luận về giá trị ngoại lai, (e) viết một đoạn tóm tắt ngắn về đặc điểm dữ liệu cùng đề xuất phân phối và mô hình phù hợp cho phân tích Bayesian.

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

*Bài học tiếp theo: [0.7 Python Cơ bản cho Data Science]({{ site.baseurl }}/contents/vi/chapter00/00_04_python_basics/)*
