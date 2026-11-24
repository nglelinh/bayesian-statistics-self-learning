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

Một trong những cú sốc trực giác đầu tiên khi chuyển từ xác suất rời rạc sang liên tục là nghịch lý sau: nếu bạn chọn ngẫu nhiên một số thực trên đoạn $$[0, 1]$$, xác suất trúng đúng số $$0.500000\ldots$$ là **bằng 0**, thế nhưng khi bạn nhấn nút, máy tính vẫn trả về *một* con số cụ thể nào đó! Làm sao hàng vô hạn biến cố có xác suất 0 lại cộng lại thành xác suất 1?

Câu trả lời là **Hàm Mật độ Xác suất (PDF)** — khái niệm tương tự mật độ khối lượng trong vật lý. Hiểu rõ sự khác biệt giữa *mật độ tại một điểm* và *xác suất trên một khoảng* là điều kiện bắt buộc để đọc đúng đồ thị prior/posterior, tránh bối rối khi thấy trục tung PDF cao vượt quá 1, và hiểu bản chất hàm hợp lý liên tục.

---

## Mục tiêu học tập

Bài học này trình bày có hệ thống về **hàm mật độ xác suất (PDF)**, làm rõ **sự khác biệt bản chất giữa PDF và hàm khối lượng xác suất (PMF)**, cũng như cách diễn giải chính xác PDF trong các mô hình xác suất liên tục.

## Bản đồ kiến thức nền: Độ đo Lebesgue, Tích phân mật độ và Biểu diễn Hậu nghiệm liên tục

Ba trụ cột toán học làm nên bản chất của PDF trong thống kê Bayes:

- **Từ PMF sang PDF (Hàm khối lượng vs. Hàm mật độ):** Với biến rời rạc, $$P(X = x)$$ là xác suất trực tiếp nằm trong $$[0, 1]$$. Với biến liên tục, $$f(x)$$ là **mật độ xác suất trên mỗi đơn vị chiều dài** (đơn vị $$[	ext{đơn vị của } x]^{-1}$$), nên $$f(x)$$ có thể lớn hơn 1 miễn là $$f(x) \ge 0$$ và $$\int_{-\infty}^{\infty} f(x)\,dx = 1$$.
- **Hàm phân phối tích lũy (CDF) & Hàm phân vị (Quantile):** $$F(x) = \int_{-\infty}^x f(t)\,dt$$ là cây cầu biến mật độ thành xác suất thật trên khoảng: $$P(a \le X \le b) = F(b) - F(a)$$. Ngược lại, hàm phân vị $$F^{-1}(q)$$ chính là công cụ xây dựng **khoảng tin cậy Bayes** (*credible intervals*).
- **Cầu nối sang Suy diễn Bayes:** Trong mô hình liên tục, cả prior $$p(	heta)$$, likelihood $$p(y \mid 	heta)$$ (với $$y$$ liên tục) và posterior $$p(	heta \mid y)$$ đều là mật độ. Khi lấy mẫu MCMC, máy tính không tính trực tiếp tích phân $$F(x)$$ mà sinh ra hàng nghìn điểm mẫu có mật độ dày đặc đúng theo chiều cao của $$p(	heta \mid y)$$.

---

## 1. Từ Rời rạc đến Liên tục

### 1.1. Biến Ngẫu nhiên Rời rạc — PMF

Với biến ngẫu nhiên **rời rạc** $$X$$, ta có **hàm khối lượng xác suất (Probability Mass Function — PMF)** ký hiệu là $$P(X = x)$$. Hàm này cho biết xác suất chính xác để biến ngẫu nhiên nhận một giá trị cụ thể. Chẳng hạn, khi tung một con xúc xắc công bằng, mỗi mặt từ 1 đến 6 có xác suất $$P(X = k) = 1/6$$.

**Các tính chất cơ bản của PMF**: $$P(X = x) \geq 0$$ với mọi $$x$$, tổng toàn bộ các xác suất $$\sum_{\text{all } x} P(X = x) = 1$$, và quan trọng nhất là $$P(X = x)$$ mang trực tiếp ý nghĩa một xác suất nằm trong đoạn $$[0, 1]$$.

![PMF của xúc xắc công bằng]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_pmf_dice.png)

*Cách đọc hình: Quan sát chiều cao từng cột riêng lẻ, vì ở PMF mỗi cột biểu thị trực tiếp xác suất tại một giá trị cụ thể.*
*Hình 1: PMF của xúc xắc công bằng. Mỗi giá trị từ 1 đến 6 có xác suất $$1/6$$ và tổng chiều cao các cột bằng 1.*

### 1.2. Vấn đề với Biến Liên tục

Bây giờ xét một biến ngẫu nhiên liên tục, chẳng hạn chiều cao người trưởng thành tuân theo phân phối chuẩn $$X \sim \mathcal{N}(170, 10^2)$$ cm. Câu hỏi đặt ra là $$P(X = 170)$$ bằng bao nhiêu?

Câu trả lời là **bằng 0**. Thực chất, $$P(X = k) = 0$$ với **mọi** giá trị cụ thể $$k$$, dù là 170, 170.5 hay 170.000001. Lý do là biến liên tục có **vô số** giá trị khả dĩ: ngay giữa 170 cm và 171 cm đã có vô hạn điểm như 170.1, 170.01, 170.001... Nếu mỗi điểm riêng lẻ đều mang xác suất dương thì tổng xác suất sẽ vượt quá 1, trái với tiên đề chuẩn hóa.

![Biến liên tục và xác suất tại một điểm]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_continuous_height.png)

*Cách đọc hình: Phân biệt chấm đỏ với toàn bộ đường cong. Chấm đỏ chỉ thể hiện giá trị mật độ tại 170 cm, còn xác suất phải được tính bằng diện tích trên một khoảng.*
*Hình 2: Với biến liên tục như chiều cao, $$P(X=170)=0$$ dù $$f(170)$$ khác 0; chỉ xác suất trên một khoảng mới có giá trị dương.*

**Cách khắc phục**: thay vì hỏi xác suất tại một điểm đơn lẻ, ta hỏi xác suất biến ngẫu nhiên rơi vào một **khoảng**:

$$P(a \leq X \leq b)$$

Chẳng hạn, $$P(169.5 \leq X \leq 170.5)$$ là xác suất chiều cao nằm giữa 169.5 cm và 170.5 cm — đại lượng này có thể tính được và mang giá trị dương.

## 2. Hàm Mật độ Xác suất (PDF)

### 2.1. Định nghĩa Chính thức

Với biến ngẫu nhiên liên tục $$X$$, **hàm mật độ xác suất (Probability Density Function — PDF)** $$f(x)$$ là hàm thỏa mãn:

$$P(a \leq X \leq b) = \int_a^b f(x) \, dx$$

Đây là định nghĩa trọng tâm của bài học: xác suất để $$X$$ rơi vào đoạn $$[a, b]$$ bằng **tích phân** (diện tích dưới đường cong) của $$f(x)$$ từ $$a$$ đến $$b$$.

**Lưu ý quan trọng**: $$f(x)$$ không phải là xác suất, mà là mật độ xác suất. Chỉ tích phân — tức diện tích dưới đường cong $$f(x)$$ trên một khoảng — mới là xác suất. Nhầm lẫn $$f(x)$$ với xác suất tại điểm $$x$$ là lỗi phổ biến nhất khi học về biến liên tục.

### 2.2. Tại sao gọi là "Mật độ"?

Khái niệm "mật độ" trong xác suất tương tự **mật độ khối lượng** trong vật lý. Mật độ khối lượng $$\rho(x)$$ (đơn vị: kg/m³) không phải là khối lượng mà cho biết khối lượng phân bố dày hay thưa trong không gian; muốn tính khối lượng trên một miền, ta phải lấy tích phân $$\text{Khối lượng} = \int \rho(x) \, dx$$.

![Mật độ khối lượng trong vật lý]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_mass_density_analogy.png)

*Hình 3: Trong vật lý, $$\rho(x)$$ là mật độ khối lượng; khối lượng thực sự bằng diện tích dưới đường $$\rho(x)$$ trên đoạn xét.*

Tương tự, mật độ xác suất $$f(x)$$ cho biết xác suất tập trung quanh $$x$$ đến mức nào, còn xác suất thực tế là tích phân $$\int f(x)\,dx$$ trên khoảng quan tâm. Khi $$f(x)$$ lớn quanh một điểm $$x$$, một khoảng nhỏ quanh $$x$$ sẽ chứa nhiều xác suất hơn; khi $$f(x)$$ nhỏ, xác suất quanh điểm đó thưa hơn.

![Mật độ xác suất trong thống kê]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_probability_density_analogy.png)

*Hình 4: Trong xác suất, $$f(x)$$ là mật độ; xác suất chỉ xuất hiện khi lấy diện tích dưới đường cong trên một khoảng, ví dụ $$[-1,1]$$.*

### 2.3. Tính chất của PDF

**Tính chất 1: Không âm.** $$f(x) \geq 0$$ với mọi $$x$$, vì mật độ âm sẽ dẫn đến xác suất âm khi lấy tích phân.

**Tính chất 2: Tích phân toàn phần bằng 1.**

$$\int_{-\infty}^{\infty} f(x) \, dx = 1$$

Tổng diện tích dưới toàn bộ đường cong mật độ bằng 1, tương ứng tổng xác suất của không gian mẫu.

**Tính chất 3: $$f(x)$$ có thể lớn hơn 1.**

Vì $$f(x)$$ là mật độ chứ không phải xác suất, nó hoàn toàn có thể vượt quá 1 miễn là tổng diện tích dưới đường cong vẫn bằng 1.

Ví dụ đầu tiên là một phân phối chuẩn rất hẹp: khi độ lệch chuẩn đủ nhỏ, đỉnh đường cong vượt trên 1 nhưng diện tích toàn phần vẫn bằng 1.

![Phân phối chuẩn hẹp có thể có đỉnh lớn hơn 1]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_normal.png)

*Hình 5: Với $$X \sim \mathcal{N}(0, 0.3^2)$$, đỉnh $$f(0)$$ vượt quá 1, nhưng toàn bộ diện tích dưới đường cong vẫn bằng 1.*

Ví dụ thứ hai là phân phối đều trên đoạn $$[0, 0.5]$$: mật độ bằng 2 trên toàn đoạn, nhưng diện tích là $$2 \times 0.5 = 1$$.

![Phân phối đều trên [0, 0.5] có mật độ bằng 2]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_uniform.png)

*Hình 6: Phân phối đều trên $$[0, 0.5]$$ có $$f(x)=2>1$$; điều kiện hợp lệ nằm ở diện tích toàn phần bằng 1, không phải chiều cao nhỏ hơn 1.*

Ví dụ thứ ba là phân phối $$\text{Beta}(0.5, 0.5)$$: mật độ tăng không bị chặn khi tiến gần hai đầu mút 0 và 1, nhưng tích phân toàn phần vẫn hữu hạn và bằng 1 nên vẫn là một PDF hợp lệ.

![Phân phối Beta có mật độ tăng rất mạnh ở đầu mút]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_exceeds_one_beta.png)

*Hình 7: Với $$\text{Beta}(0.5, 0.5)$$, mật độ tăng rất cao gần 0 và 1, minh họa rõ hơn rằng $$f(x)$$ không phải xác suất điểm.*

## 3. Hiểu Sâu về PDF

### 3.1. PDF là Giới hạn của Histogram

Một cách trực quan để hiểu PDF là thông qua histogram. Khi số lượng mẫu $$n$$ tăng lên và độ rộng các khoảng (bin) $$\Delta x$$ thu nhỏ dần, đường bao của histogram (được chuẩn hóa theo mật độ) tiến dần về đường cong PDF lý thuyết. Về mặt toán học, khi $$n \to \infty$$ và $$\Delta x \to 0$$, histogram hội tụ về PDF.

*Cách đọc chuỗi hình dưới đây: theo dõi từ $$n$$ nhỏ đến $$n$$ lớn để thấy histogram màu xanh dần ôm sát đường PDF lý thuyết màu đỏ.*

![Histogram với n = 100]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n100.png)

*Hình 8: Với $$n=100$$, histogram còn thô và dao động mạnh quanh đường cong lý thuyết.*

![Histogram với n = 500]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n500.png)

*Hình 9: Khi $$n=500$$, dạng hình chuông rõ hơn nhưng từng bin vẫn còn chênh lệch đáng kể.*

![Histogram với n = 1,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n1000.png)

*Hình 10: Với $$n=1{,}000$$, histogram bám khá sát đường PDF dù nhiễu lấy mẫu vẫn còn rõ.*

![Histogram với n = 5,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n5000.png)

*Hình 11: Ở $$n=5{,}000$$, đường bao chung của histogram đã rất gần PDF lý thuyết.*

![Histogram với n = 10,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n10000.png)

*Hình 12: Khi $$n=10{,}000$$, sai khác chỉ còn là các dao động nhỏ do lấy mẫu.*

![Histogram với n = 50,000]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_histogram_n50000.png)

*Hình 13: Với $$n=50{,}000$$, histogram gần như trùng với PDF lý thuyết, cho thấy PDF là giới hạn lý tưởng khi cỡ mẫu rất lớn.*

Mối liên hệ này nối PDF lý thuyết với dữ liệu thực tế: ta không bao giờ có vô hạn quan sát, nên phải ước lượng mật độ từ mẫu hữu hạn, và cỡ mẫu càng lớn thì ước lượng càng gần PDF thật.

### 3.2. Xác suất trong Khoảng Nhỏ

Trên một khoảng rất nhỏ $$[x, x + \Delta x]$$, xác suất có thể xấp xỉ bởi diện tích hình chữ nhật chiều cao $$f(x)$$ và bề rộng $$\Delta x$$:

$$P(x \leq X \leq x + \Delta x) \approx f(x) \cdot \Delta x$$

Khi $$\Delta x$$ càng nhỏ, xấp xỉ càng chính xác; lấy giới hạn khi $$\Delta x \to 0$$, ta có:

$$f(x) = \lim_{\Delta x \to 0} \frac{P(x \leq X \leq x + \Delta x)}{\Delta x}$$

Như vậy, $$f(x)$$ đóng vai trò đạo hàm của xác suất tích lũy theo $$x$$, đo tốc độ tích lũy xác suất dọc theo trục $$x$$.

*Cách đọc chuỗi hình dưới đây: so sánh hình chữ nhật nét đứt màu xanh lá với diện tích thật màu cam khi $$\Delta x$$ thu nhỏ dần.*

![Xấp xỉ với delta x bằng 0.5]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_05.png)

*Hình 14: Với $$\Delta x = 0.5$$, hình chữ nhật xấp xỉ còn thô nên sai số hiện rõ.*

![Xấp xỉ với delta x bằng 0.1]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_01.png)

*Hình 15: Khi $$\Delta x = 0.1$$, diện tích hình chữ nhật đã bám sát diện tích thật hơn nhiều.*

![Xấp xỉ với delta x bằng 0.01]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_small_interval_dx_001.png)

*Hình 16: Với $$\Delta x = 0.01$$, xấp xỉ $$f(x)\Delta x$$ gần như trùng với xác suất thật trên khoảng rất nhỏ.*

### 3.3. Đơn vị của PDF

Một đặc điểm thường bị bỏ qua là PDF có đơn vị đo. Nếu biến ngẫu nhiên $$X$$ mang đơn vị (như cm, kg hay giây), thì $$f(x)$$ có đơn vị là **1/(đơn vị của X)**, nhờ đó tích $$f(x)\cdot dx$$ trở thành đại lượng không thứ nguyên và mang ý nghĩa xác suất.

Ví dụ, nếu $$X$$ là chiều cao đo bằng cm thì $$f(x)$$ có đơn vị 1/cm; khi đổi sang mét, $$f(x)$$ có đơn vị 1/m và giá trị số tăng gấp 100 lần: nếu $$f(170 \text{ cm}) = 0.04 \text{ (1/cm)}$$ thì $$f(1.70 \text{ m}) = 4.0 \text{ (1/m)}$$.

![PDF khi đo chiều cao bằng cm]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_units_cm_only.png)

*Hình 17: Khi đo bằng cm, mật độ tại trung tâm khoảng $$f(170)=0.04$$ với đơn vị 1/cm.*

![PDF khi đo chiều cao bằng m]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_units_m_only.png)

*Hình 18: Cùng phân phối đó nhưng đổi sang mét, mật độ tại trung tâm là $$f(1.70)=4.0$$ với đơn vị 1/m; bản chất phân phối không đổi, chỉ thang đo và đơn vị mật độ thay đổi.*

Ngược lại, **xác suất không phụ thuộc vào đơn vị đo**: $$P(160 \text{ cm} \leq X \leq 180 \text{ cm}) = P(1.60 \text{ m} \leq X \leq 1.80 \text{ m})$$. Việc $$f(x)$$ thay đổi theo đơn vị là một lý do nữa khẳng định $$f(x)$$ không thể là xác suất.

## 4. So sánh PMF và PDF

Ở biến rời rạc, một PMF điển hình như $$\text{Binomial}(10, 0.5)$$ gán xác suất trực tiếp cho từng giá trị nguyên.

![Ví dụ PMF của phân phối Binomial]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_binomial_pmf_example.png)

*Hình 19: Với PMF, độ cao cột tại $$x=5$$ chính là xác suất $$P(X=5)=0.246$$ và đọc được trực tiếp trên biểu đồ.*

Ở biến liên tục, một PDF điển hình như $$\mathcal{N}(0,1)$$ chỉ cho biết mật độ tại từng điểm, không phải xác suất tại điểm đó.

![Ví dụ PDF của phân phối chuẩn tắc]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_normal_density_example.png)

*Hình 20: Với PDF, giá trị $$f(0)=0.399$$ là mật độ tại 0, còn xác suất tại đúng điểm đó vẫn là $$P(X=0)=0$$.*

| Đặc điểm | PMF (Rời rạc) | PDF (Liên tục) |
|----------|---------------|----------------|
| **Ký hiệu** | $$P(X = x)$$ | $$f(x)$$ |
| **Ý nghĩa** | Xác suất | Mật độ xác suất |
| **Giá trị** | $$0 \leq P(X=x) \leq 1$$ | $$f(x) \geq 0$$ (có thể > 1) |
| **P(X = x)** | Có nghĩa | = 0 |
| **Tổng/Tích phân** | $$\sum P(X=x) = 1$$ | $$\int f(x)dx = 1$$ |
| **Xác suất khoảng** | $$\sum_{a}^{b} P(X=x)$$ | $$\int_a^b f(x)dx$$ |
| **Đơn vị** | Không đơn vị | 1/(đơn vị của X) |

Điểm khác biệt cốt lõi: với PMF, $$P(X=x)$$ **là xác suất**; với PDF, $$f(x)$$ **chỉ là mật độ**, và xác suất chỉ xuất hiện khi lấy tích phân trên một khoảng.

## 5. Các Sai lầm Thường gặp

### Sai lầm 1: Nghĩ $$f(x)$$ là xác suất

Với phân phối chuẩn chiều cao có trung bình 170 cm và độ lệch chuẩn 10 cm, ta tính được $$f(170) = 0.04$$. Viết "$$P(X = 170) = f(170) = 0.04$$" là sai; diễn giải đúng là "$$P(X = 170) = 0$$ vì đây là biến liên tục, còn $$f(170) = 0.04$$ là mật độ xác suất tại 170 cm".

### Sai lầm 2: Nghĩ $$f(x) \leq 1$$

Do xác suất không vượt quá 1, nhiều người suy luận nhầm rằng PDF cũng phải nhỏ hơn hoặc bằng 1. Thực tế, $$f(x)$$ chỉ cần không âm và thỏa mãn $$\int f(x)dx = 1$$. Ví dụ, phân phối đều trên $$[0, 0.2]$$ có $$f(x) = 5 > 1$$ nhưng hoàn toàn hợp lệ vì diện tích bằng $$5 \times 0.2 = 1$$.

### Sai lầm 3: So sánh trực tiếp $$f(x)$$ giữa các đơn vị khác nhau

Vì $$f(x)$$ phụ thuộc vào đơn vị đo, so sánh trực tiếp $$f(170 \text{ cm})$$ với $$f(1.70 \text{ m})$$ không có ý nghĩa. Thay vào đó, ta chỉ nên so sánh các xác suất trên những khoảng tương ứng vì xác suất là đại lượng không thứ nguyên.

## 6. Ứng dụng trong Thống kê Bayesian

### 6.1. Prior và Posterior là PDF

Trong phân tích Bayesian với tham số liên tục $$\theta$$, cả phân phối tiên nghiệm (prior) $$p(\theta)$$ và phân phối hậu nghiệm (posterior) $$p(\theta \mid x)$$ đều là PDF. Điều đó có nghĩa là $$p(\theta)$$ biểu diễn **mật độ niềm tin** (density of belief) chứ không phải xác suất điểm: giá trị $$p(\theta = 0.5)$$ có thể lớn hơn 1, còn xác suất có ý nghĩa luôn gắn với một khoảng, chẳng hạn $$P(a \leq \theta \leq b) = \int_a^b p(\theta)\,d\theta$$.

![Prior và posterior như hai hàm mật độ]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_bayesian_prior_posterior.png)

*Hình 21: Trong thống kê Bayesian, prior và posterior là hai đường PDF trên không gian tham số, thể hiện mật độ niềm tin trước và sau khi cập nhật dữ liệu.*

Ví dụ, với prior $$\theta \sim \text{Beta}(2, 2)$$ cho xác suất thành công của một thử nghiệm và dữ liệu gồm 7 lần thành công trong 10 phép thử, posterior là $$\theta \mid x \sim \text{Beta}(9, 5)$$. Phát biểu "khoảng tin cậy 95% là [0.395, 0.827]" có nghĩa chính xác là:

$$P(0.395 \leq \theta \leq 0.827 \mid x) = \int_{0.395}^{0.827} p(\theta \mid x) \, d\theta = 0.95$$

![Khoảng tin cậy như diện tích dưới posterior]({{ site.baseurl }}/img/chapter_img/chapter00/pdf_bayesian_credible_interval.png)

*Hình 22: Khoảng tin cậy 95% tương ứng phần diện tích màu xanh dưới đường posterior PDF, không phải chiều cao mật độ tại một điểm.*

### 6.2. Hàm Hợp lý (Likelihood Function)

Hàm hợp lý $$L(\theta) = p(x \mid \theta)$$ cũng được xây dựng từ PDF. Khi dữ liệu $$x$$ đã cố định, hàm hợp lý được xem là hàm theo tham số $$\theta$$. Với mô hình $$X \sim \mathcal{N}(\mu, \sigma^2)$$ ($$\sigma$$ đã biết):

$$L(\mu) = \prod_{i=1}^{n} f(x_i \mid \mu) = \prod_{i=1}^{n} \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x_i-\mu)^2}{2\sigma^2}\right)$$

Mỗi thừa số $$f(x_i \mid \mu)$$ là giá trị PDF tại quan sát $$x_i$$ ứng với tham số $$\mu$$, và ước lượng hợp lý cực đại (MLE) là giá trị $$\hat{\mu}$$ làm cực đại $$L(\mu)$$.

## Khung giải thích (nên đọc chậm): Tại sao PDF có thể lớn hơn 1 — và cách đọc diện tích bằng tay

Hãy đọc chậm bốn quy tắc vàng để không bao giờ hiểu sai đồ thị PDF của prior hay posterior:

1. **Mật độ không phải xác suất:** $$f(x_0)$$ không phải là $$P(X = x_0)$$. Thay vào đó, với khoảng rất hẹp bề rộng $$\Delta x$$, xác suất xấp xỉ bằng diện tích hình chữ nhật nhỏ: $$P(x_0 \le X \le x_0 + \Delta x) pprox f(x_0)\,\Delta x$$.
2. **Đổi đơn vị làm đổi chiều cao PDF:** Nếu đo chiều dài bằng mét thay vì centimet, miền giá trị bị nén lại 100 lần, nên chiều cao PDF bắt buộc phải **tăng gấp 100 lần** để tổng diện tích vẫn giữ nguyên bằng 1.
3. **Tỷ số mật độ mới mang ý nghĩa bất biến theo đơn vị:** Khi so sánh hai điểm $$x_1$$ và $$x_2$$, tỷ số $$f(x_1)/f(x_2)$$ cho biết một khoảng hẹp quanh $$x_1$$ có xác suất lớn gấp bao nhiêu lần khoảng cùng bề rộng quanh $$x_2$$ — đây chính là thứ thuật toán **Metropolis–Hastings** sử dụng trong tỷ số chấp nhận!
4. **Khoảng tin cậy Bayes là bài toán diện tích:** Tìm khoảng 95% hậu nghiệm nghĩa là tìm $$[a, b]$$ sao cho $$\int_a^b p(	heta \mid y)\,d	heta = 0.95$$.

### Ví dụ tính toán cầm tay chỉ việc: Kiểm tra PDF tam giác và tính xác suất khoảng

Xét một hàm mật độ đơn giản trên đoạn $$[0, 0.5]$$ (ví dụ một prior tam giác tập trung gần $$0.5$$):
$$f(	heta) = c\,	heta \quad 	ext{với } 0 \le 	heta \le 0.5, \quad 	ext{và } f(	heta) = 0 	ext{ ở ngoài.}$$

- **Bước 1 — Tìm hằng số chuẩn hóa $$c$$ sao cho tổng diện tích bằng 1:**
  $$\int_0^{0.5} c\,	heta\,d	heta = c \left[rac{	heta^2}{2}ight]_0^{0.5} = c \cdot rac{0.25}{2} = rac{c}{8} = 1 \implies c = 8.$$
- **Bước 2 — Kiểm tra giá trị PDF tại đỉnh $$	heta = 0.5$$:**
  $$f(0.5) = 8 	imes 0.5 = 4 > 1!$$
  Điều này hoàn toàn hợp lệ: hình tam giác có đáy $$0.5$$ và chiều cao $$4$$ nên diện tích đúng bằng $$rac{1}{2} 	imes 0.5 	imes 4 = 1$$.
- **Bước 3 — Tính xác suất $$	heta$$ rơi vào khoảng $$[0.25, 0.50]$$:**
  $$P(0.25 \le 	heta \le 0.50) = \int_{0.25}^{0.50} 8	heta\,d	heta = \left[4	heta^2ight]_{0.25}^{0.50} = 4(0.25) - 4(0.0625) = 1 - 0.25 = 0.75.$$
- **Bước 4 — Xấp xỉ xác suất trên khoảng hẹp $$[0.40, 0.41]$$ bằng công thức $$f(x)\Delta x$$:**
  $$f(0.405) 	imes 0.01 = (8 	imes 0.405) 	imes 0.01 = 3.24 	imes 0.01 = 0.0324$$ (đúng tuyệt đối vì $$f$$ tuyến tính!).

**Hiểu lầm cần tránh:** Thấy $$f(	heta) = 4$$ rồi kết luận "mô hình bị lỗi vì xác suất vượt quá 1" hoặc dùng trực tiếp $$f(	heta)$$ để cộng dồn mà quên nhân với bề rộng $$\Delta 	heta$$.

**Kiểm tra nhanh:** Kỳ vọng của phân phối tam giác trên là $$\mathbb{E}[	heta] = \int_0^{0.5} 	heta \cdot 8	heta\,d	heta = \left[rac{8	heta^3}{3}ight]_0^{0.5} = rac{8 	imes 0.125}{3} = rac{1}{3} pprox 0.333$$.

---

## Video tham khảo

- [Probability density and mass functions](https://www.youtube.com/watch?v=hDjcxi9p0ak) — Intelligent Systems Lab, English. **Xem trước.** Phân biệt trực quan hàm khối lượng xác suất (PMF) và hàm mật độ xác suất (PDF).
- [Probability Distribution Functions (PMF, PDF, CDF)](https://www.youtube.com/watch?v=YXLVjCKVP7U) — zedstatistics, English. Giải thích mối liên hệ giữa PMF, PDF và hàm phân phối tích lũy (CDF) khi tính xác suất trên khoảng.
- [Why “probability of 0” does not mean “impossible” | Probabilities of probabilities, part 2](https://www.youtube.com/watch?v=ZA4JkHKZM50) — 3Blue1Brown, English. Làm rõ vì sao xác suất tại một điểm bằng 0 với biến liên tục và vai trò của hàm mật độ.

## Bài tập

**Bài tập 1**: Giải thích vì sao $$P(X = 170) = 0$$ đối với biến liên tục nhưng $$f(170)$$ vẫn có thể khác 0. Hai đại lượng này khác nhau ở điểm nào?

**Bài tập 2**: Cho $$f(x) = 2x$$ trên đoạn $$[0, 1]$$ và $$f(x) = 0$$ ngoài đoạn đó.
   - Kiểm tra xem đây có phải là PDF hợp lệ hay không (tích phân bằng 1).
   - Tính $$P(0.2 \leq X \leq 0.5)$$.
   - Giá trị $$f(0.3) = 0.6$$ có phải là xác suất không? Nếu không, nó có ý nghĩa gì?

**Bài tập 3**: Xét hai phân phối chuẩn có cùng trung bình nhưng khác độ lệch chuẩn (ví dụ $$\sigma = 1$$ và $$\sigma = 2$$). So sánh giá trị $$f(\mu)$$ tại trung bình; phân phối nào có $$f(\mu)$$ lớn hơn và vì sao?

**Bài tập 4**: Cho chiều cao $$X \sim \mathcal{N}(170 \text{ cm}, 10^2)$$.
   - Nếu $$f(170 \text{ cm}) = 0.04 \text{ (1/cm)}$$, thì $$f(1.70 \text{ m})$$ bằng bao nhiêu (đơn vị 1/m)?
   - Tính $$P(160 \leq X \leq 180)$$ theo cả hai hệ đơn vị và đối chiếu kết quả.
   - Giải thích vì sao xác suất bất biến còn $$f(x)$$ thay đổi theo đơn vị.

**Bài tập 5**: Cho phân phối tiên nghiệm $$\theta \sim \text{Beta}(1, 1)$$ (phân phối đều) và dữ liệu gồm 3 lần thành công trong 5 phép thử.
   - Tìm phân phối hậu nghiệm $$p(\theta \mid x)$$.
   - Giá trị $$p(0.5 \mid x)$$ có phải là xác suất không? Nếu không, nó có ý nghĩa gì?
   - Tính khoảng tin cậy 90% cho $$\theta$$.
   - Diễn giải biểu thức "$$P(a \leq \theta \leq b \mid x) = 0.90$$" bằng ngôn ngữ tích phân của PDF.

## Tài liệu tham khảo

**Wasserman, L. (2004).** *All of Statistics: A Concise Course in Statistical Inference*. Springer.
- Chapter 2: Random Variables — phần trình bày về PDF và sự khác biệt với PMF.

**Casella, G., & Berger, R. L. (2002).** *Statistical Inference* (2nd Edition). Duxbury.
- Chapter 1: Probability Theory — giải thích chi tiết về PDF và các tính chất toán học.

**Gelman, A., et al. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Appendix A: Standard probability distributions — sử dụng PDF trong bối cảnh Bayesian.

**Seeing Theory - Probability Distributions**: [https://seeing-theory.brown.edu/](https://seeing-theory.brown.edu/)
- Công cụ trực quan hóa tương tác về các khái niệm PDF.

---

*Tóm lại, cần luôn phân biệt: $$f(x)$$ là mật độ xác suất, không phải xác suất; chỉ tích phân của $$f(x)$$ trên một khoảng mới là xác suất.*

*Bài học tiếp theo: [0.11 P-values và Kiểm định Giả thuyết]({{ site.baseurl }}/contents/vi/chapter00/00_08_pvalues_and_hypothesis_testing/)*
