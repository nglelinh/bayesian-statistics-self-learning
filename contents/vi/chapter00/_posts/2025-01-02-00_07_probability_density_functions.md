---
layout: post
title: "Bài 0.10: Hàm Mật độ Xác suất (PDF) - Chi tiết"
chapter: '00'
order: 10
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Bài học này trình bày một cách hệ thống về hàm mật độ xác suất (PDF), sự khác biệt bản chất giữa PDF và hàm khối xác suất (PMF), cũng như cách diễn giải đúng PDF trong các mô hình liên tục. Sau khi học xong, bạn sẽ hiểu vì sao $$f(x)$$ không phải là xác suất điểm, vì sao $$f(x)$$ có thể lớn hơn 1 mà vẫn hợp lệ, và vì sao tư duy "xác suất là diện tích" là điều kiện nền tảng để đọc prior, likelihood và posterior trong Bayesian.

## 1. Từ Rời rạc đến Liên tục

### 1.1. Biến Ngẫu nhiên Rời rạc - PMF

Với biến ngẫu nhiên **rời rạc** $$X$$, chúng ta có **Probability Mass Function (PMF)** $$P(X = x)$$. Hàm này cho biết xác suất chính xác để biến ngẫu nhiên nhận một giá trị cụ thể. Ví dụ, khi tung xúc xắc công bằng, mỗi mặt từ 1 đến 6 có xác suất $$P(X = k) = 1/6$$. Điều quan trọng cần nhớ là với biến rời rạc, $$P(X = x)$$ **là xác suất thực sự**, có giá trị từ 0 đến 1, và tổng của tất cả các xác suất bằng 1.

**Tính chất của PMF** có thể được tóm lại ngắn gọn như sau: $$P(X = x) \geq 0$$ với mọi $$x$$, tổng của tất cả các xác suất $$\sum_{\text{all } x} P(X = x)$$ bằng 1, và quan trọng nhất là $$P(X = x)$$ trong trường hợp rời rạc thực sự là một xác suất với ý nghĩa trực tiếp.

### 1.2. Vấn đề với Biến Liên tục

Bây giờ hãy xem xét một biến ngẫu nhiên liên tục. Giả sử chiều cao người trưởng thành tuân theo phân phối chuẩn $$X \sim \mathcal{N}(170, 10^2)$$ cm. Một câu hỏi tự nhiên là: $$P(X = 170)$$ bằng bao nhiêu?

Câu trả lời đáng ngạc nhiên là **bằng 0**! Thực tế, $$P(X = k)$$ bằng 0 với **mọi** giá trị cụ thể $$k$$, dù là 170, 170.5, hay 170.000001. Lý do là có **vô số** giá trị có thể mà chiều cao có thể nhận. Giữa 170 cm và 171 cm, có vô hạn các giá trị khác nhau: 170.1, 170.01, 170.001, và cứ thế tiếp tục đến vô cùng. Nếu mỗi giá trị có xác suất dương, thì tổng tất cả các xác suất sẽ là vô hạn, vi phạm nguyên tắc cơ bản rằng tổng phải bằng 1.

![PMF vs Biến Liên tục]({{ site.baseurl }}/img/chapter_img/chapter00/pmf_vs_continuous.png)

*Cách đọc hình: Hình này minh họa pmf vs biến liên tục. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 1: So sánh PMF với biến liên tục. Bên trái: PMF của xúc xắc, $$P(X=x)$$ là xác suất có ý nghĩa. Bên phải: Với biến liên tục như chiều cao, $$P(X=170)=0$$ vì có vô số giá trị có thể. Thay vào đó, chúng ta cần hỏi về xác suất trong một khoảng.*

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

Tương tự trong thống kê, mật độ xác suất $$f(x)$$ không phải là xác suất, mà cho biết xác suất được "tập trung" quanh $$x$$ như thế nào; muốn có xác suất thực tế, ta phải lấy tích phân $$\int f(x)\,dx$$, tức diện tích dưới đường cong trên khoảng quan tâm.

![Tương tự Mật độ]({{ site.baseurl }}/img/chapter_img/chapter00/density_analogy.png)

*Cách đọc hình: Hình này minh họa tương tự mật độ. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 2: Tương tự giữa mật độ khối lượng (vật lý) và mật độ xác suất (thống kê). Trong cả hai trường hợp, mật độ không phải là đại lượng cuối cùng (khối lượng hoặc xác suất), mà chỉ có tích phân của mật độ mới cho ta đại lượng cần tìm.*

Khi $$f(x)$$ cao tại một điểm $$x$$, điều đó có nghĩa là xác suất "tập trung" quanh điểm đó - nói cách khác, trong một khoảng nhỏ xung quanh $$x$$, có nhiều xác suất hơn. Khi $$f(x)$$ thấp, xác suất "thưa thớt" hơn quanh điểm đó.

### 2.3. Tính chất của PDF

**Tính chất 1: Không âm**: $$f(x) \geq 0$$ với mọi $$x$$

Mật độ xác suất không bao giờ âm. Điều này hợp lý vì mật độ âm sẽ dẫn đến xác suất âm (khi lấy tích phân), điều này vô nghĩa.

**Tính chất 2: Tích phân bằng 1**: 

$$\int_{-\infty}^{\infty} f(x) \, dx = 1$$

Tổng diện tích dưới toàn bộ đường cong PDF phải bằng 1, vì tổng xác suất của tất cả các kết quả có thể phải bằng 1.

**Tính chất 3: $$f(x)$$ có thể lớn hơn 1!**

Đây là điểm quan trọng và thường gây nhầm lẫn. Vì $$f(x)$$ không phải là xác suất, nó hoàn toàn có thể lớn hơn 1. Miễn là tích phân (diện tích tổng) vẫn bằng 1, thì PDF hợp lệ.

![PDF có thể > 1]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_can_exceed_one.png)

*Cách đọc hình: Hình này minh họa pdf có thể > 1. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 3: Các ví dụ cho thấy PDF có thể lớn hơn 1. Bên trái: Phân phối chuẩn với độ lệch chuẩn nhỏ (0.3) có $$f(0) > 1$$. Giữa: Phân phối đều trên [0, 0.5] có $$f(x) = 2 > 1$$. Phải: Phân phối Beta(0.5, 0.5) có $$f(x)$$ tiến đến vô cùng tại đầu mút. Trong tất cả các trường hợp, tích phân vẫn bằng 1.*

Hãy xem xét phân phối đều trên khoảng $$[0, 0.5]$$. PDF của phân phối này là $$f(x) = 2$$ trên khoảng này và $$f(x) = 0$$ ở ngoài. Rõ ràng $$f(x) = 2 > 1$$, nhưng tích phân là $$\int_0^{0.5} 2 \, dx = 2 \times 0.5 = 1$$, hoàn toàn hợp lệ. Phân phối chuẩn với độ lệch chuẩn rất nhỏ cũng có giá trị PDF lớn hơn 1 tại đỉnh, và một số phân phối Beta thậm chí có PDF tiến đến vô cùng tại một số điểm!

## 3. Hiểu Sâu về PDF

### 3.1. PDF là Giới hạn của Histogram

Một cách trực quan để hiểu PDF là thông qua histogram. Khi chúng ta vẽ histogram của dữ liệu với số lượng mẫu tăng lên và độ rộng của các bin giảm xuống, histogram sẽ dần dần tiến gần đến đường cong PDF lý thuyết. Về mặt toán học, khi số lượng mẫu $$n \to \infty$$ và độ rộng bin $$\Delta x \to 0$$, histogram hội tụ về PDF.

![Histogram tiến đến PDF]({{ site.baseurl }}/img/chapter_img/chapter00/histogram_to_pdf.png)

*Cách đọc hình: Hình này minh họa histogram tiến đến pdf. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 4: Minh họa histogram tiến đến PDF khi số lượng mẫu tăng. Với n = 100, histogram còn rất thô. Khi n tăng lên 50,000, histogram khớp gần như hoàn hảo với đường cong PDF lý thuyết (màu đỏ). Điều này cho thấy PDF là "giới hạn lý tưởng" của histogram khi có vô hạn dữ liệu.*

Quan sát này rất quan trọng vì nó kết nối PDF lý thuyết với dữ liệu thực tế. Trong thực tế, chúng ta không bao giờ có vô hạn dữ liệu, vì vậy chúng ta làm việc với histogram hoặc các ước lượng khác của PDF. Nhưng khi có nhiều dữ liệu hơn, ước lượng của chúng ta sẽ gần với PDF thực tế hơn.

### 3.2. Xác suất trong Khoảng Nhỏ

Một cách hữu ích khác để hiểu PDF là thông qua xấp xỉ cho các khoảng nhỏ. Với khoảng rất nhỏ $$[x, x + \Delta x]$$:

$$P(x \leq X \leq x + \Delta x) \approx f(x) \cdot \Delta x$$

Công thức này cho thấy rằng xác suất trong một khoảng nhỏ xấp xỉ bằng chiều cao của PDF nhân với độ rộng của khoảng. Đây chính xác là công thức tính diện tích của một hình chữ nhật với chiều cao $$f(x)$$ và độ rộng $$\Delta x$$.

Khi $$\Delta x$$ càng nhỏ, xấp xỉ càng chính xác. Về mặt toán học, chúng ta có thể viết:

$$f(x) = \lim_{\Delta x \to 0} \frac{P(x \leq X \leq x + \Delta x)}{\Delta x}$$

Công thức này cho thấy PDF là "đạo hàm" của xác suất theo biến $$x$$. Nói cách khác, $$f(x)$$ đo tốc độ thay đổi của xác suất khi chúng ta di chuyển dọc theo trục $$x$$.

![Xấp xỉ Khoảng Nhỏ]({{ site.baseurl }}/img/chapter_img/chapter00/small_interval_approximation.png)

*Cách đọc hình: Hình này minh họa xấp xỉ khoảng nhỏ. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 5: Xấp xỉ $$P(x \leq X \leq x+\Delta x) \approx f(x) \cdot \Delta x$$. Với $$\Delta x = 0.5$$, sai số rõ rệt. Với $$\Delta x = 0.1$$, xấp xỉ tốt hơn. Với $$\Delta x = 0.01$$, xấp xỉ gần như hoàn hảo. Hình chữ nhật màu xanh lá (xấp xỉ) gần như khớp với diện tích màu cam (xác suất thực) khi $$\Delta x$$ nhỏ.*

### 3.3. Đơn vị của PDF

Một khía cạnh quan trọng nhưng thường bị bỏ qua của PDF là đơn vị của nó. Nếu biến ngẫu nhiên $$X$$ có đơn vị, chẳng hạn cm, kg, hay giây, thì $$f(x)$$ sẽ có đơn vị là **1/(đơn vị của X)**, còn $$f(x)\cdot dx$$ sẽ trở thành một đại lượng không đơn vị, và სწორედ vì thế mới có thể được diễn giải như xác suất.

Ví dụ, nếu $$X$$ là chiều cao tính bằng cm, thì $$f(x)$$ có đơn vị 1/cm. Nếu chúng ta chuyển đổi sang mét, $$f(x)$$ sẽ có đơn vị 1/m, và giá trị số học của nó sẽ thay đổi theo. Cụ thể, nếu $$f(170 \text{ cm}) = 0.04 \text{ (1/cm)}$$, thì $$f(1.70 \text{ m}) = 4.0 \text{ (1/m)}$$ - tăng lên 100 lần vì chúng ta chuyển từ cm sang m.

![Đơn vị của PDF]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_units.png)

*Cách đọc hình: Hình này minh họa đơn vị của pdf. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 6: PDF thay đổi theo đơn vị của biến ngẫu nhiên. Bên trái: Chiều cao tính bằng cm, $$f(170) = 0.04$$ (1/cm). Bên phải: Cùng phân phối nhưng tính bằng mét, $$f(1.70) = 4.0$$ (1/m). Chú ý rằng $$0.04 \times 100 = 4.0$$, phản ánh hệ số chuyển đổi. Tuy nhiên, xác suất (diện tích dưới đường cong) không thay đổi.*

Tuy nhiên, **xác suất không phụ thuộc vào đơn vị**. $$P(160 \text{ cm} \leq X \leq 180 \text{ cm}) = P(1.60 \text{ m} \leq X \leq 1.80 \text{ m})$$. Điều này hợp lý vì xác suất là một khái niệm trừu tượng không có đơn vị đo lường vật lý.

Sự phụ thuộc vào đơn vị của $$f(x)$$ là một lý do quan trọng khác tại sao chúng ta không thể coi $$f(x)$$ là xác suất. Xác suất phải không đổi bất kể hệ đơn vị nào chúng ta sử dụng, nhưng $$f(x)$$ thay đổi theo đơn vị.

## 4. So sánh PMF và PDF

Để củng cố hiểu biết, hãy so sánh trực tiếp PMF và PDF:

![So sánh PMF và PDF]({{ site.baseurl }}/img/chapter_img/chapter00/pmf_pdf_comparison.png)

*Cách đọc hình: Hình này minh họa so sánh pmf và pdf. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 7: So sánh trực tiếp PMF và PDF. Trái: PMF của Binomial(10, 0.5), $$P(X=5) = 0.246$$ LÀ xác suất có ý nghĩa trực tiếp. Phải: PDF của Normal(0,1), $$f(0) = 0.399$$ KHÔNG PHẢI xác suất, và $$P(X=0) = 0$$.*

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

![Ứng dụng Bayesian]({{ site.baseurl }}/img/chapter_img/chapter00/bayesian_pdf_application.png)

*Cách đọc hình: Hình này minh họa ứng dụng bayesian. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 8: Prior và Posterior trong Bayesian statistics đều là PDF. Trái: Prior Beta(2,2) (màu xanh) và Posterior Beta(9,5) (màu đỏ) sau khi quan sát 7 thành công trong 10 thử. Phải: Khoảng tin cậy 95% được tính bằng tích phân posterior PDF, cho $$P(0.395 \leq \theta \leq 0.827) = 0.95$$.*

Ví dụ, giả sử chúng ta có prior $$\theta \sim \text{Beta}(2, 2)$$ cho xác suất thành công của một thử nghiệm, và quan sát 7 thành công trong 10 lần thử. Posterior sẽ là $$\theta \mid x \sim \text{Beta}(9, 5)$$. Khi chúng ta nói "khoảng tin cậy 95% là [0.395, 0.827]", ý nghĩa chính xác là:

$$P(0.395 \leq \theta \leq 0.827 \mid x) = \int_{0.395}^{0.827} p(\theta \mid x) \, d\theta = 0.95$$

Đây là tích phân (diện tích) của posterior PDF, không phải là giá trị của PDF tại bất kỳ điểm nào.

### 6.2. Likelihood Function

Likelihood function $$L(\theta) = p(x \mid \theta)$$ cũng tỷ lệ với PDF. Khi dữ liệu $$x$$ được cố định, likelihood là hàm của tham số $$\theta$$. Nếu mô hình là $$X \sim \mathcal{N}(\mu, \sigma^2)$$ với $$\sigma$$ biết trước, thì:

$$L(\mu) = \prod_{i=1}^{n} f(x_i \mid \mu) = \prod_{i=1}^{n} \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x_i-\mu)^2}{2\sigma^2}\right)$$

Ở đây, mỗi $$f(x_i \mid \mu)$$ là giá trị của PDF tại điểm dữ liệu $$x_i$$, với tham số $$\mu$$. Maximum Likelihood Estimate (MLE) là giá trị $$\hat{\mu}$$ làm cực đại $$L(\mu)$$.

## 7. Tóm tắt Quan trọng

Hãy củng cố những điểm quan trọng nhất về PDF:

![Tóm tắt PDF]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_summary_infographic.png)

*Cách đọc hình: Hình này minh họa tóm tắt pdf. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hình 9: Bảng tóm tắt các khái niệm quan trọng về PDF. Hãy xem lại bảng này thường xuyên để củng cố hiểu biết.*

**7 điểm quan trọng nhất** có thể gói lại trong một mạch lập luận ngắn như sau: $$f(x)$$ là mật độ chứ không phải xác suất; chỉ có tích phân của $$f(x)$$ trên một khoảng mới là xác suất; vì là mật độ nên $$f(x)$$ có thể lớn hơn 1; với biến liên tục thì $$P(X=x)=0$$ cho mọi điểm đơn lẻ; $$f(x)$$ mang đơn vị nghịch đảo của đơn vị đo của $$X$$ nên sẽ thay đổi khi đổi hệ đơn vị, trong khi xác suất thì không; về mặt trực giác, PDF là giới hạn lý tưởng của histogram khi dữ liệu ngày càng nhiều và bin ngày càng nhỏ; và trong Bayesian, cả prior lẫn posterior đều là các PDF nên toàn bộ suy luận phải được hiểu trên các khoảng và diện tích, không phải trên xác suất điểm.

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
