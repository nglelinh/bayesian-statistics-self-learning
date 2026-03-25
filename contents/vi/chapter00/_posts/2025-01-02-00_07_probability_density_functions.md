---
layout: post
title: "Bài 0.10: Hàm Mật độ Xác suất (Probability Density Function - PDF) - Chi tiết"
chapter: '00'
order: 10
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Bài học này trình bày một cách hệ thống về **hàm mật độ xác suất (PDF), sự khác biệt bản chất giữa PDF và hàm khối xác suất (PMF)**, cũng như cách diễn giải đúng PDF trong các mô hình liên tục. 

## 1. Từ Rời rạc đến Liên tục

### 1.1. Biến Ngẫu nhiên Rời rạc - PMF

Với biến ngẫu nhiên **rời rạc** $$X$$, chúng ta có **Probability Mass Function (PMF)** $$P(X = x)$$. Hàm này cho biết xác suất chính xác để biến ngẫu nhiên nhận một giá trị cụ thể. Ví dụ, khi tung xúc xắc công bằng, mỗi mặt từ 1 đến 6 có xác suất $$P(X = k) = 1/6$$. Điều quan trọng cần nhớ là với biến rời rạc, $$P(X = x)$$ **là xác suất thực sự**, có giá trị từ 0 đến 1, và tổng của tất cả các xác suất bằng 1.

**Tính chất của PMF** có thể được tóm lại ngắn gọn như sau: $$P(X = x) \geq 0$$ với mọi $$x$$, tổng của tất cả các xác suất $$\sum_{\text{all } x} P(X = x)$$ bằng 1, và quan trọng nhất là $$P(X = x)$$ trong trường hợp rời rạc thực sự là một xác suất với ý nghĩa trực tiếp.

![PMF của xúc xắc công bằng]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_pmf_dice.png)

*Cách đọc hình: Hãy nhìn từng cột riêng lẻ, vì ở PMF mỗi cột chính là xác suất tại một giá trị cụ thể.*
*Hình 1: PMF của xúc xắc công bằng. Mỗi giá trị 1 đến 6 mang đúng xác suất $$1/6$$, và tổng tất cả các cột bằng 1.*

### 1.2. Vấn đề với Biến Liên tục

Bây giờ hãy xem xét một biến ngẫu nhiên liên tục. Giả sử chiều cao người trưởng thành tuân theo phân phối chuẩn $$X \sim \mathcal{N}(170, 10^2)$$ cm. Một câu hỏi tự nhiên là: $$P(X = 170)$$ bằng bao nhiêu?

Câu trả lời đáng ngạc nhiên là **bằng 0**! Thực tế, $$P(X = k)$$ bằng 0 với **mọi** giá trị cụ thể $$k$$, dù là 170, 170.5, hay 170.000001. Lý do là có **vô số** giá trị có thể mà chiều cao có thể nhận. Giữa 170 cm và 171 cm, có vô hạn các giá trị khác nhau: 170.1, 170.01, 170.001, và cứ thế tiếp tục đến vô cùng. Nếu mỗi giá trị có xác suất dương, thì tổng tất cả các xác suất sẽ là vô hạn, vi phạm nguyên tắc cơ bản rằng tổng phải bằng 1.

![Biến liên tục và xác suất tại một điểm]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_continuous_height.png)

*Cách đọc hình: Hãy phân biệt chấm đỏ với cả đường cong. Chấm đỏ cho thấy giá trị mật độ tại 170 cm, còn xác suất vẫn phải được hiểu bằng diện tích trên một khoảng.*
*Hình 2: Với biến liên tục như chiều cao, $$P(X=170)=0$$ dù $$f(170)$$ khác 0. Điều có ý nghĩa là xác suất trên một khoảng chiều cao, không phải tại một điểm đơn lẻ.*

**Giải pháp**: Thay vì hỏi xác suất tại một điểm, chúng ta hỏi xác suất trong một **khoảng**:

$$P(a \leq X \leq b)$$

Ví dụ, $$P(169.5 \leq X \leq 170.5)$$ là xác suất chiều cao nằm giữa 169.5 cm và 170.5 cm. Xác suất này có thể được tính toán và có giá trị khác 0.

## 2. Hàm Mật độ Xác suất (PDF)

### 2.1. Định nghĩa Chính thức

Cho biến ngẫu nhiên liên tục $$X$$, **Probability Density Function (PDF)** $$f(x)$$ là hàm thỏa mãn:

$$P(a \leq X \leq b) = \int_a^b f(x) \, dx$$

Đây là định nghĩa quan trọng nhất của bài học. Xác suất để $$X$$ nằm trong khoảng $$[a, b]$$ được tính bằng **tích phân** (diện tích dưới đường cong) của hàm mật độ $$f(x)$$ từ $$a$$ đến $$b$$.

**Chú ý quan trọng nhất** là $$f(x)$$ không phải là xác suất. Nó là mật độ xác suất, và chỉ có tích phân, tức diện tích dưới đường cong của $$f(x)$$, mới mang ý nghĩa xác suất thực sự.

Đây là nguồn gốc của nhiều hiểu lầm phổ biến về PDF. Nhiều người nhầm lẫn và nghĩ rằng $$f(x)$$ là xác suất tại điểm $$x$$, nhưng điều này hoàn toàn sai. Hãy nhớ: $$f(x)$$ chỉ là mật độ, giống như mật độ khối lượng trong vật lý.

### 2.2. Tại sao gọi là "Mật độ"?

Khái niệm "mật độ" trong thống kê tương tự **mật độ khối lượng** trong vật lý. Trong vật lý, mật độ khối lượng $$\rho(x)$$ (đơn vị: kg/m³) không phải là khối lượng, mà chỉ cho biết khối lượng phân bố như thế nào trong không gian. Để tính khối lượng thực tế, chúng ta phải lấy tích phân: $$\text{Khối lượng} = \int \rho(x) \, dx$$.

![Mật độ khối lượng trong vật lý]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_mass_density_analogy.png)

*Hình 3: Trong vật lý, $$\rho(x)$$ chỉ là mật độ khối lượng; khối lượng thực sự đến từ diện tích dưới đường $$\rho(x)$$ trên đoạn quan tâm.*

Tương tự trong thống kê, mật độ xác suất $$f(x)$$ không phải là xác suất, mà cho biết xác suất được "tập trung" quanh $$x$$ như thế nào; muốn có xác suất thực tế, ta phải lấy tích phân $$\int f(x)\,dx$$, tức diện tích dưới đường cong trên khoảng quan tâm.

![Mật độ xác suất trong thống kê]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_probability_density_analogy.png)

*Hình 4: Trong thống kê cũng vậy, $$f(x)$$ không phải xác suất; xác suất chỉ xuất hiện khi ta lấy diện tích dưới đường cong trên một khoảng, chẳng hạn $$[-1,1]$$.*

Khi $$f(x)$$ cao tại một điểm $$x$$, điều đó có nghĩa là xác suất "tập trung" quanh điểm đó - nói cách khác, trong một khoảng nhỏ xung quanh $$x$$, có nhiều xác suất hơn. Khi $$f(x)$$ thấp, xác suất "thưa thớt" hơn quanh điểm đó.

### 2.3. Tính chất của PDF

**Tính chất 1: Không âm**: $$f(x) \geq 0$$ với mọi $$x$$

Mật độ xác suất không bao giờ âm. Điều này hợp lý vì mật độ âm sẽ dẫn đến xác suất âm (khi lấy tích phân), điều này vô nghĩa.

**Tính chất 2: Tích phân bằng 1**: 

$$\int_{-\infty}^{\infty} f(x) \, dx = 1$$

Tổng diện tích dưới toàn bộ đường cong PDF phải bằng 1, vì tổng xác suất của tất cả các kết quả có thể phải bằng 1.

**Tính chất 3: $$f(x)$$ có thể lớn hơn 1!**

Đây là điểm quan trọng và thường gây nhầm lẫn. Vì $$f(x)$$ không phải là xác suất, nó hoàn toàn có thể lớn hơn 1. Miễn là tích phân (diện tích tổng) vẫn bằng 1, thì PDF hợp lệ.

Một ví dụ đầu tiên là phân phối chuẩn rất hẹp. Khi độ lệch chuẩn đủ nhỏ, đỉnh của đường cong sẽ vượt qua mức 1 mà vẫn hợp lệ vì diện tích tổng thể vẫn bằng 1.

![Phân phối chuẩn hẹp có thể có đỉnh lớn hơn 1]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_normal.png)

*Hình 5: Với $$X \sim \mathcal{N}(0, 0.3^2)$$, đỉnh $$f(0)$$ vượt quá 1, nhưng toàn bộ diện tích dưới đường cong vẫn bằng 1.*

Một ví dụ thứ hai là phân phối đều trên khoảng $$[0, 0.5]$$. Ở đây PDF bằng đúng 2 trên toàn bộ khoảng, nên chiều cao lớn hơn 1 nhưng diện tích vẫn chỉ là $$2 \times 0.5 = 1$$.

![Phân phối đều trên [0, 0.5] có mật độ bằng 2]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_uniform.png)

*Hình 6: Phân phối đều trên $$[0, 0.5]$$ có $$f(x)=2>1$$. Điều làm nó hợp lệ không phải chiều cao, mà là diện tích toàn phần vẫn bằng 1.*

Cuối cùng, có những phân phối như Beta(0.5, 0.5) còn đi xa hơn: mật độ có thể tăng vọt ở gần đầu mút 0 và 1. Dù vậy, miễn là tích phân toàn phần hữu hạn và bằng 1 thì đây vẫn là một PDF hợp lệ.

![Phân phối Beta có mật độ tăng rất mạnh ở đầu mút]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_beta.png)

*Hình 7: Với Beta(0.5, 0.5), mật độ tiến rất cao ở gần 0 và 1. Điều này càng nhắc lại rằng $$f(x)$$ không phải xác suất điểm.*

## 3. Hiểu Sâu về PDF

### 3.1. PDF là Giới hạn của Histogram

Một cách trực quan để hiểu PDF là thông qua histogram. Khi chúng ta vẽ histogram của dữ liệu với số lượng mẫu tăng lên và độ rộng của các bin giảm xuống, histogram sẽ dần dần tiến gần đến đường cong PDF lý thuyết. Về mặt toán học, khi số lượng mẫu $$n \to \infty$$ và độ rộng bin $$\Delta x \to 0$$, histogram hội tụ về PDF.

*Cách đọc chuỗi hình dưới đây: đi từ $$n$$ nhỏ đến $$n$$ lớn và quan sát histogram màu xanh dần ôm sát đường PDF lý thuyết màu đỏ.*

![Histogram với n = 100]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n100.png)

*Hình 8: Với $$n=100$$, histogram vẫn còn thô và dao động mạnh quanh đường cong lý thuyết.*

![Histogram với n = 500]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n500.png)

*Hình 9: Khi $$n=500$$, hình dạng chuông bắt đầu rõ hơn nhưng vẫn còn sai khác đáng kể ở từng bin.*

![Histogram với n = 1,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n1000.png)

*Hình 10: Với $$n=1{,}000$$, histogram đã mô phỏng khá tốt đường PDF, dù nhiễu lấy mẫu vẫn còn thấy rõ.*

![Histogram với n = 5,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n5000.png)

*Hình 11: Ở $$n=5{,}000$$, đường bao chung của histogram đã gần với PDF lý thuyết.*

![Histogram với n = 10,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n10000.png)

*Hình 12: Khi $$n=10{,}000$$, khác biệt chủ yếu chỉ còn ở các dao động nhỏ do lấy mẫu.*

![Histogram với n = 50,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n50000.png)

*Hình 13: Với $$n=50{,}000$$, histogram gần như trùng với PDF lý thuyết, cho thấy PDF là giới hạn lý tưởng khi dữ liệu rất nhiều.*

Quan sát này rất quan trọng vì nó kết nối PDF lý thuyết với dữ liệu thực tế. Trong thực tế, chúng ta không bao giờ có vô hạn dữ liệu, vì vậy chúng ta làm việc với histogram hoặc các ước lượng khác của PDF. Nhưng khi có nhiều dữ liệu hơn, ước lượng của chúng ta sẽ gần với PDF thực tế hơn.

### 3.2. Xác suất trong Khoảng Nhỏ

Một cách hữu ích khác để hiểu PDF là thông qua xấp xỉ cho các khoảng nhỏ. Với khoảng rất nhỏ $$[x, x + \Delta x]$$:

$$P(x \leq X \leq x + \Delta x) \approx f(x) \cdot \Delta x$$

Công thức này cho thấy rằng xác suất trong một khoảng nhỏ xấp xỉ bằng chiều cao của PDF nhân với độ rộng của khoảng. Đây chính xác là công thức tính diện tích của một hình chữ nhật với chiều cao $$f(x)$$ và độ rộng $$\Delta x$$.

Khi $$\Delta x$$ càng nhỏ, xấp xỉ càng chính xác. Về mặt toán học, chúng ta có thể viết:

$$f(x) = \lim_{\Delta x \to 0} \frac{P(x \leq X \leq x + \Delta x)}{\Delta x}$$

Công thức này cho thấy PDF là "đạo hàm" của xác suất theo biến $$x$$. Nói cách khác, $$f(x)$$ đo tốc độ thay đổi của xác suất khi chúng ta di chuyển dọc theo trục $$x$$.

*Cách đọc chuỗi hình dưới đây: so sánh hình chữ nhật nét đứt màu xanh lá với phần diện tích màu cam khi $$\Delta x$$ ngày càng nhỏ.*

![Xấp xỉ với delta x bằng 0.5]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_05.png)

*Hình 14: Với $$\Delta x = 0.5$$, hình chữ nhật xấp xỉ còn khá thô nên sai số vẫn nhìn thấy rõ.*

![Xấp xỉ với delta x bằng 0.1]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_01.png)

*Hình 15: Khi $$\Delta x = 0.1$$, hình chữ nhật đã bám sát hơn nhiều vào diện tích thực.*

![Xấp xỉ với delta x bằng 0.01]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_001.png)

*Hình 16: Với $$\Delta x = 0.01$$, xấp xỉ $$f(x)\Delta x$$ gần như trùng với xác suất thực trên khoảng rất nhỏ.*

### 3.3. Đơn vị của PDF

Một khía cạnh quan trọng nhưng thường bị bỏ qua của PDF là đơn vị của nó. Nếu biến ngẫu nhiên $$X$$ có đơn vị, chẳng hạn cm, kg, hay giây, thì $$f(x)$$ sẽ có đơn vị là **1/(đơn vị của X)**, còn $$f(x)\cdot dx$$ sẽ trở thành một đại lượng không đơn vị, và chính vì thế mới có thể được diễn giải như xác suất.

Ví dụ, nếu $$X$$ là chiều cao tính bằng cm, thì $$f(x)$$ có đơn vị 1/cm. Nếu chúng ta chuyển đổi sang mét, $$f(x)$$ sẽ có đơn vị 1/m, và giá trị số học của nó sẽ thay đổi theo. Cụ thể, nếu $$f(170 \text{ cm}) = 0.04 \text{ (1/cm)}$$, thì $$f(1.70 \text{ m}) = 4.0 \text{ (1/m)}$$ - tăng lên 100 lần vì chúng ta chuyển từ cm sang m.

![PDF khi đo chiều cao bằng cm]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_units_cm_only.png)

*Hình 17: Khi đo bằng cm, giá trị tại trung tâm là khoảng $$f(170)=0.04$$ với đơn vị 1/cm.*

![PDF khi đo chiều cao bằng m]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_units_m_only.png)

*Hình 18: Cùng phân phối nhưng đổi sang mét thì giá trị tại trung tâm tăng lên khoảng $$f(1.70)=4.0$$ với đơn vị 1/m. Hình dạng vật lý của phân phối không đổi, chỉ thang đo và đơn vị của mật độ thay đổi.*

Tuy nhiên, **xác suất không phụ thuộc vào đơn vị**. $$P(160 \text{ cm} \leq X \leq 180 \text{ cm}) = P(1.60 \text{ m} \leq X \leq 1.80 \text{ m})$$. Điều này hợp lý vì xác suất là một khái niệm trừu tượng không có đơn vị đo lường vật lý.

Sự phụ thuộc vào đơn vị của $$f(x)$$ là một lý do quan trọng khác tại sao chúng ta không thể coi $$f(x)$$ là xác suất. Xác suất phải không đổi bất kể hệ đơn vị nào chúng ta sử dụng, nhưng $$f(x)$$ thay đổi theo đơn vị.

## 4. So sánh PMF và PDF

Để củng cố hiểu biết, hãy so sánh trực tiếp PMF và PDF:

Ở phía rời rạc, một PMF điển hình như Binomial(10, 0.5) gán xác suất trực tiếp cho từng giá trị nguyên.

![Ví dụ PMF của phân phối Binomial]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_binomial_pmf_example.png)

*Hình 19: Ở PMF, cột tại $$x=5$$ chính là xác suất $$P(X=5)=0.246$$ và có thể đọc trực tiếp từ hình.*

Ở phía liên tục, một PDF điển hình như Normal(0,1) chỉ cho ta mật độ tại từng điểm chứ không cho xác suất điểm.

![Ví dụ PDF của phân phối chuẩn tắc]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_normal_density_example.png)

*Hình 20: Ở PDF, giá trị $$f(0)=0.399$$ chỉ là mật độ tại điểm 0, còn $$P(X=0)=0$$ vì đây là biến liên tục.*

| Đặc điểm | PMF (Rời rạc) | PDF (Liên tục) |
|----------|---------------|----------------|
| **Ký hiệu** | $$P(X = x)$$ | $$f(x)$$ |
| **Ý nghĩa** | Xác suất | Mật độ xác suất |
| **Giá trị** | $$0 \leq P(X=x) \leq 1$$ | $$f(x) \geq 0$$ (có thể > 1) |
| **P(X = x)** | Có nghĩa | = 0 (vô nghĩa) |
| **Tổng/Tích phân** | $$\sum P(X=x) = 1$$ | $$\int f(x)dx = 1$$ |
| **Xác suất khoảng** | $$\sum_{a}^{b} P(X=x)$$ | $$\int_a^b f(x)dx$$ |
| **Đơn vị** | Không đơn vị | 1/(đơn vị của X) |

Sự khác biệt cốt lõi là: với PMF, $$P(X=x)$$ **là xác suất**, trong khi với PDF, $$f(x)$$ **không phải xác suất** mà chỉ là mật độ. Chỉ khi lấy tổng (rời rạc) hoặc tích phân (liên tục) chúng ta mới có xác suất thực sự.

## 5. Các Sai lầm Thường gặp

### Sai lầm 1: Nghĩ $$f(x)$$ là xác suất

Đây là sai lầm phổ biến nhất. Nhiều người nhìn vào phân phối chuẩn với trung bình 170 cm và độ lệch chuẩn 10 cm, tính được $$f(170) = 0.04$$, rồi nói "xác suất chiều cao bằng 170 cm là 0.04". Điều này hoàn toàn **sai**. Diễn giải sai sẽ là viết "$$P(X = 170) = f(170) = 0.04$$", trong khi diễn giải đúng phải là "$$P(X = 170) = 0$$ vì đây là biến liên tục, còn $$f(170) = 0.04$$ chỉ là mật độ tại điểm đó".

### Sai lầm 2: Nghĩ $$f(x) \leq 1$$

Vì xác suất không bao giờ vượt quá 1, nhiều người tự động giả định rằng PDF cũng không thể vượt quá 1. Nhưng như chúng ta đã thấy, điều này **sai**. Phát biểu "$$f(x)$$ phải nhỏ hơn hoặc bằng 1" là sai, còn phát biểu đúng là "$$f(x) \geq 0$$ và hoàn toàn có thể lớn hơn 1, miễn là tích phân toàn phần $$\int f(x)dx = 1$$".

Ví dụ, phân phối đều trên $$[0, 0.2]$$ có $$f(x) = 5 > 1$$, nhưng hoàn toàn hợp lệ vì diện tích là $$5 \times 0.2 = 1$$.

### Sai lầm 3: So sánh $$f(x)$$ giữa các đơn vị khác nhau

Vì $$f(x)$$ phụ thuộc vào đơn vị, việc so sánh $$f(170 \text{ cm})$$ với $$f(1.70 \text{ m})$$ là vô nghĩa. Chúng có đơn vị khác nhau và giá trị số học khác nhau, nên điều có thể so sánh một cách có ý nghĩa không phải là mật độ tại điểm mà là các xác suất trên những khoảng tương ứng, bởi xác suất không mang đơn vị.

## 6. Ứng dụng trong Bayesian Statistics

### 6.1. Prior và Posterior là PDF

Trong phân tích Bayesian, cả phân phối prior $$p(\theta)$$ và phân phối posterior $$p(\theta \mid x)$$ đều là PDF nếu tham số $$\theta$$ liên tục. Điều đó có nghĩa là $$p(\theta)$$ không phải là xác suất điểm mà là **mật độ tin cậy** (density of belief), nên biểu thức như $$p(\theta = 0.5)$$ không có diễn giải xác suất trực tiếp; điều có ý nghĩa là xác suất trên một khoảng, chẳng hạn $$P(a \leq \theta \leq b) = \int_a^b p(\theta)\,d\theta$$, và vì là mật độ nên $$p(\theta)$$ cũng có thể lớn hơn 1.

![Prior và posterior như hai hàm mật độ]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_bayesian_prior_posterior.png)

*Hình 21: Trong Bayesian, prior và posterior đều là các đường PDF trên không gian tham số. Chúng mô tả mật độ niềm tin trước và sau khi quan sát dữ liệu.*

Ví dụ, giả sử chúng ta có prior $$\theta \sim \text{Beta}(2, 2)$$ cho xác suất thành công của một thử nghiệm, và quan sát 7 thành công trong 10 lần thử. Posterior sẽ là $$\theta \mid x \sim \text{Beta}(9, 5)$$. Khi chúng ta nói "khoảng tin cậy 95% là [0.395, 0.827]", ý nghĩa chính xác là:

$$P(0.395 \leq \theta \leq 0.827 \mid x) = \int_{0.395}^{0.827} p(\theta \mid x) \, d\theta = 0.95$$

![Khoảng tin cậy như diện tích dưới posterior]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_bayesian_credible_interval.png)

*Hình 22: Khoảng tin cậy 95% là diện tích màu xanh dưới posterior PDF, không phải là chiều cao của đường cong tại một điểm nào đó.*

Đây là tích phân (diện tích) của posterior PDF, không phải là giá trị của PDF tại bất kỳ điểm nào.

### 6.2. Likelihood Function

Likelihood function $$L(\theta) = p(x \mid \theta)$$ cũng tỷ lệ với PDF. Khi dữ liệu $$x$$ được cố định, likelihood là hàm của tham số $$\theta$$. Nếu mô hình là $$X \sim \mathcal{N}(\mu, \sigma^2)$$ với $$\sigma$$ biết trước, thì:

$$L(\mu) = \prod_{i=1}^{n} f(x_i \mid \mu) = \prod_{i=1}^{n} \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x_i-\mu)^2}{2\sigma^2}\right)$$

Ở đây, mỗi $$f(x_i \mid \mu)$$ là giá trị của PDF tại điểm dữ liệu $$x_i$$, với tham số $$\mu$$. Maximum Likelihood Estimate (MLE) là giá trị $$\hat{\mu}$$ làm cực đại $$L(\mu)$$.


## Bài tập

**Bài tập 1**: Giải thích tại sao $$P(X = 170) = 0$$ với biến liên tục, nhưng $$f(170)$$ có thể khác 0. Sự khác biệt giữa hai đại lượng này là gì?

**Bài tập 2**: Cho $$f(x) = 2x$$ trên $$[0, 1]$$ và $$f(x) = 0$$ ở ngoài.
   - Kiểm tra rằng đây là PDF hợp lệ (tích phân bằng 1)
   - Tính $$P(0.2 \leq X \leq 0.5)$$
   - $$f(0.3) = 0.6$$ có phải là xác suất không? Nếu không, nó có ý nghĩa gì?

**Bài tập 3**: Tạo hai phân phối chuẩn với cùng trung bình nhưng độ lệch chuẩn khác nhau (ví dụ $$\sigma = 1$$ và $$\sigma = 2$$). So sánh giá trị $$f(x)$$ tại trung bình. Phân phối nào có $$f(\mu)$$ lớn hơn? Tại sao?

**Bài tập 4**: Chiều cao $$X \sim \mathcal{N}(170 \text{ cm}, 10^2)$$.
   - Nếu $$f(170 \text{ cm}) = 0.04 \text{ (1/cm)}$$, thì $$f(1.70 \text{ m})$$ bằng bao nhiêu (đơn vị 1/m)?
   - Tính $$P(160 \leq X \leq 180)$$ với cả hai hệ đơn vị. Kết quả có giống nhau không?
   - Giải thích tại sao xác suất không đổi nhưng $$f(x)$$ thay đổi theo đơn vị.

**Bài tập 5**: Cho prior $$\theta \sim \text{Beta}(1, 1)$$ (phân phối đều) và dữ liệu: 3 thành công trong 5 lần thử.
   - Tìm posterior $$p(\theta \mid x)$$
   - $$p(0.5 \mid x)$$ có phải là xác suất không? Nếu không, nó có ý nghĩa gì?
   - Tính khoảng tin cậy 90% cho $$\theta$$
   - Giải thích ý nghĩa của "$$P(a \leq \theta \leq b \mid x) = 0.90$$" bằng ngôn ngữ tích phân PDF

## Tài liệu tham khảo

**Wasserman, L. (2004).** *All of Statistics: A Concise Course in Statistical Inference*. Springer.
- Chapter 2: Random Variables - Phần về PDF và sự khác biệt với PMF

**Casella, G., & Berger, R. L. (2002).** *Statistical Inference* (2nd Edition). Duxbury.
- Chapter 1: Probability Theory - Giải thích chi tiết về PDF và tính chất toán học

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Appendix A: Standard probability distributions - Sử dụng PDF trong context Bayesian

**Seeing Theory - Probability Distributions**: [https://seeing-theory.brown.edu/](https://seeing-theory.brown.edu/)
- Interactive visualization of PDF concepts

---

*Hiểu đúng về PDF là nền tảng quan trọng cho Bayesian Statistics! Hãy nhớ: $$f(x)$$ là mật độ, không phải xác suất. Chỉ có tích phân của $$f(x)$$ mới là xác suất.*

---

*Bài học tiếp theo: [0.11 P-values và Kiểm định Giả thuyết](/vi/chapter00/pvalues-and-hypothesis-testing/)*
