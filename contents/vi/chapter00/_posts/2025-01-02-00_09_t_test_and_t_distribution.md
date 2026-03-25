---
layout: post
title: "Bài 0.12: T-test và Phân phối T"
chapter: '00'
order: 12
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu sắc về **t-statistic**, **phân phối t**, và **t-test** - một trong những công cụ thống kê phổ biến nhất trong nghiên cứu khoa học. Bạn sẽ học được tại sao chúng ta cần phân phối t (thay vì phân phối chuẩn), cách tính và diễn giải t-value, và các loại t-test khác nhau. Quan trọng hơn, bạn sẽ hiểu những giả định và hạn chế của t-test, chuẩn bị nền tảng để so sánh với phương pháp Bayesian trong các chương sau.

## Giới thiệu: Vấn đề với Độ lệch Chuẩn Chưa Biết

Hãy tưởng tượng bạn là một nhà nghiên cứu muốn biết liệu chiều cao trung bình của nam sinh viên tại trường đại học của bạn có khác 170 cm hay không. Bạn không thể đo chiều cao của tất cả nam sinh viên, vì vậy bạn lấy mẫu ngẫu nhiên 25 sinh viên và tính chiều cao trung bình mẫu $$\bar{x} = 172.5$$ cm với độ lệch chuẩn mẫu $$s = 6.2$$ cm.

Bạn muốn biết: sự khác biệt giữa 172.5 cm (mẫu) và 170 cm (giả thuyết) có đủ lớn để kết luận rằng chiều cao trung bình thực sự khác 170 cm, hay có thể chỉ là do ngẫu nhiên?

Trong thống kê cổ điển, nếu chúng ta **biết độ lệch chuẩn quần thể** $$\sigma$$, chúng ta có thể sử dụng **z-statistic**:

$$z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

Và z-statistic này tuân theo phân phối chuẩn chuẩn hóa $$N(0, 1)$$.

Nhưng trong thực tế, chúng ta **hiếm khi biết** $$\sigma$$! Chúng ta chỉ có $$s$$ - độ lệch chuẩn mẫu, một ước lượng của $$\sigma$$. Khi chúng ta thay $$\sigma$$ bằng $$s$$, sự không chắc chắn tăng lên, và phân phối của statistic không còn là chuẩn nữa.

Đây chính là lý do chúng ta cần **phân phối t** và **t-statistic**.

## T-statistic: Định nghĩa và Ý nghĩa

**T-statistic** (hay t-value) được định nghĩa tương tự z-statistic, nhưng sử dụng độ lệch chuẩn mẫu $$s$$ thay vì $$\sigma$$:

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

Trong đó, $$\bar{x}$$ là trung bình mẫu, $$\mu_0$$ là giá trị giả thuyết thường đến từ $$H_0$$, $$s$$ là độ lệch chuẩn mẫu, $$n$$ là kích thước mẫu, còn $$s / \sqrt{n}$$ được gọi là **standard error of the mean** (SE), tức độ bất định của trung bình mẫu.

### Diễn giải T-value

T-value đo lường **số lượng standard errors** mà trung bình mẫu cách xa giá trị giả thuyết:

Nếu **$$|t|$$ lớn**, trung bình mẫu cách xa $$\mu_0$$ một số lượng standard errors đáng kể, và điều đó tạo bằng chứng chống lại $$H_0$$; ngược lại, nếu **$$|t|$$ nhỏ**, trung bình mẫu nằm gần $$\mu_0$$ nên dữ liệu chưa tạo được nhiều sức nặng để chống lại giả thuyết không.

*Cách đọc hình: Bốn hình dưới đây tách riêng từng mức độ cực đoan của t-value để bạn nhìn rõ p-value thay đổi thế nào.*

![T-value nhỏ với bằng chứng yếu chống lại H0]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_small_example.png)

*Hình 1a: Với $$t = 0.5$$ và $$df = 15$$, p-value lớn khoảng 0.62 nên dữ liệu khá phù hợp với $$H_0$$.*

![T-value ở vùng lưng chừng gần ngưỡng 0.05]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_borderline_example.png)

*Hình 1b: Với $$t = 2.0$$, p-value khoảng 0.064 nên kết quả ở trạng thái lưng chừng, sát ngưỡng 0.05.*

![T-value lớn với bằng chứng mạnh hơn chống lại H0]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_large_example.png)

*Hình 1c: Với $$t = 3.0$$, p-value nhỏ khoảng 0.009 nên bằng chứng chống lại $$H_0$$ mạnh hơn rõ rệt.*

![Ví dụ chocolate với t âm nhỏ về độ lớn]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_chocolate_example.png)

*Hình 1d: Ở ví dụ chocolate với $$t = -0.70$$, p = 0.495 cho thấy chưa có đủ bằng chứng để chống lại giả thuyết không.*

Vùng được tô màu trong mỗi panel thể hiện "vùng cực đoan" dùng để tính p-value (two-tailed test).

**Ví dụ cụ thể:** quay lại ví dụ chiều cao, ta có $$\bar{x} = 172.5$$ cm, $$\mu_0 = 170$$ cm, $$s = 6.2$$ cm, và $$n = 25$$.

$$t = \frac{172.5 - 170}{6.2 / \sqrt{25}} = \frac{2.5}{1.24} = 2.02$$

T-value = 2.02 có nghĩa là trung bình mẫu cách xa giá trị giả thuyết khoảng 2 standard errors. Đây là một khoảng cách đáng kể, gợi ý có bằng chứng chống lại giả thuyết không.

## Phân phối T: Tại sao Không Phải Phân phối Chuẩn?

Khi chúng ta sử dụng $$s$$ thay vì $$\sigma$$, t-statistic không tuân theo phân phối chuẩn, mà tuân theo **phân phối t** (Student's t-distribution).

### Đặc điểm của Phân phối T

Phân phối t có hình dạng khá giống phân phối chuẩn nhưng đuôi dày hơn, và chính đặc điểm này phản ánh phần không chắc chắn bổ sung khi ta phải ước lượng $$\sigma$$ bằng $$s$$. Phân phối t còn phụ thuộc vào một tham số gọi là **bậc tự do** (degrees of freedom), thường bằng $$df = n - 1$$ trong one-sample t-test, và khi $$n$$ tăng dần thì nó hội tụ về phân phối chuẩn; vì thế với mẫu đủ lớn, chẳng hạn trên 30 quan sát, hai phân phối thường rất khó phân biệt bằng mắt thường.

### Tại sao đuôi dày hơn?

Khi mẫu nhỏ, $$s$$ là một ước lượng không chắc chắn của $$\sigma$$. Đôi khi $$s$$ nhỏ hơn $$\sigma$$ thực, làm cho t-value lớn hơn nó nên có. Đuôi dày hơn của phân phối t "điều chỉnh" cho sự biến động này, làm cho chúng ta khó bác bỏ $$H_0$$ hơn khi mẫu nhỏ - một cách tiếp cận thận trọng hợp lý.

![So sánh Phân phối T và Phân phối Chuẩn]({{ site.baseurl }}/img/chapter_img/chapter00/t_vs_normal_distribution.png)

*Cách đọc hình: Hình này minh họa so sánh phân phối t và phân phối chuẩn. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*

Hình trên so sánh phân phối t với nhiều giá trị df khác nhau. Với **df = 2** tương ứng mẫu rất nhỏ, đuôi phân phối cực dày vì bất định trong việc ước lượng $$\sigma$$ còn rất lớn; với **df = 5** đuôi vẫn dày hơn chuẩn rõ rệt; với **df = 10** độ khác biệt đã giảm đi; còn với **df = 30** thì đường cong gần như không còn phân biệt được với phân phối chuẩn, vốn có thể xem như trường hợp giới hạn khi $$df = \infty$$.

Lưu ý cách các critical values thay đổi: với df = 2 và $$\alpha = 0.05$$ (two-tailed), critical value là ±4.303, trong khi với phân phối chuẩn chỉ là ±1.96. Điều này làm cho việc bác bỏ $$H_0$$ khó hơn nhiều khi mẫu nhỏ - một đặc tính thận trọng và hợp lý.

## Các Loại T-test

Có ba loại t-test phổ biến, tùy thuộc vào thiết kế nghiên cứu:

![Bảng tóm tắt ba loại t-test]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_summary_table.png)

*Hình 2: Bảng tóm tắt nhanh mục đích, công thức và bậc tự do của ba loại t-test phổ biến.*

### 1. One-sample T-test

**Mục đích:** So sánh trung bình của một mẫu với một giá trị đã biết.

**Công thức:**

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

**Degrees of freedom:** $$df = n - 1$$

**Ví dụ:** Kiểm tra xem chiều cao trung bình của nam sinh viên có khác 170 cm không.

![One-sample t-test so sánh một mẫu với giá trị giả thuyết]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_one_sample.png)

*Hình 2a: One-sample t-test so sánh trung bình của một mẫu với một giá trị đã biết hoặc được giả thuyết trước.*

### 2. Independent Two-sample T-test (Unpaired)

**Mục đích:** So sánh trung bình của hai nhóm độc lập.

**Công thức (với giả định phương sai bằng nhau):**

$$t = \frac{\bar{x}_1 - \bar{x}_2}{s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$$

Trong đó $$s_p$$ là **pooled standard deviation**:

$$s_p = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}$$

**Degrees of freedom:** $$df = n_1 + n_2 - 2$$

**Ví dụ:** So sánh chiều cao trung bình của nam sinh viên khoa A và khoa B.

![Independent two-sample t-test so sánh hai nhóm độc lập]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_independent.png)

*Hình 2b: Independent two-sample t-test so sánh hai nhóm độc lập, ví dụ chiều cao giữa hai khoa khác nhau.*

### 3. Paired T-test (Dependent)

**Mục đích:** So sánh trung bình của hai phép đo trên cùng một nhóm đối tượng (before-after, matched pairs).

**Công thức:**

$$t = \frac{\bar{d}}{s_d / \sqrt{n}}$$

Trong đó:
Ở đây, $$\bar{d}$$ là trung bình của các hiệu số, còn $$s_d$$ là độ lệch chuẩn của các hiệu số đó.

**Degrees of freedom:** $$df = n - 1$$

**Ví dụ:** So sánh cân nặng của bệnh nhân trước và sau khi dùng thuốc giảm cân.

![Paired t-test so sánh trước và sau trên cùng một nhóm]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_paired.png)

*Hình 2c: Paired t-test theo dõi cùng một nhóm ở hai thời điểm, nên trọng tâm nằm ở hiệu số của từng cặp đo.*

## Giả Định của T-test

T-test dựa trên một số giả định quan trọng. Khi các giả định này bị vi phạm, kết quả có thể không đáng tin cậy:

### 1. Dữ liệu tuân theo phân phối chuẩn (hoặc n đủ lớn)

**Giả định:** Dữ liệu trong mỗi nhóm tuân theo phân phối chuẩn, hoặc kích thước mẫu đủ lớn (n > 30 là quy tắc ngón tay cái) để Central Limit Theorem có hiệu lực.

Ta có thể kiểm tra giả định này bằng histogram, Q-Q plot, hoặc Shapiro-Wilk test, dù cần nhớ rằng kiểm định sau thường rất nhạy khi kích thước mẫu lớn.

Nếu vi phạm xảy ra với mẫu nhỏ, ta nên cân nhắc các non-parametric tests như Wilcoxon; còn với mẫu lớn, t-test thường vẫn khá robust nhờ định lý giới hạn trung tâm.

### 2. Độc lập giữa các quan sát

**Giả định:** Các quan sát trong mẫu độc lập với nhau.

Những vi phạm phổ biến gồm đo lặp lại trên cùng một đối tượng, dữ liệu có cấu trúc phân cấp, hoặc dữ liệu chuỗi thời gian có phụ thuộc nối tiếp.

### 3. Phương sai bằng nhau (cho two-sample t-test)

**Giả định:** Hai nhóm có phương sai giống nhau (homogeneity of variance).

Ta có thể kiểm tra bằng Levene's test hoặc dùng quy tắc ngón tay cái rằng tỉ lệ $$\frac{s_1}{s_2}$$ không nên vượt quá 2 quá nhiều.

Nếu giả định này vi phạm, Welch's t-test thường là lựa chọn an toàn hơn vì nó không đòi hỏi phương sai bằng nhau.

## Diễn Giải Kết Quả T-test

Khi chúng ta thực hiện t-test, chúng ta nhận được hai thông tin chính:

### 1. T-value

T-value cho biết **mức độ khác biệt** giữa dữ liệu và giả thuyết không; trị tuyệt đối của nó càng lớn thì dữ liệu càng nằm xa kỳ vọng dưới $$H_0$$, và vì thế bằng chứng chống lại $$H_0$$ càng mạnh.

### 2. P-value

P-value cho biết **xác suất quan sát được một t-value ít nhất cực đoan như vậy** nếu $$H_0$$ đúng; p nhỏ, chẳng hạn dưới 0.05, thường được diễn giải là có ý nghĩa thống kê, còn p lớn chỉ cho thấy chưa có đủ bằng chứng để bác bỏ $$H_0$$.

**LƯU Ý QUAN TRỌNG:** P-value **không** cho biết xác suất $$H_0$$ đúng, **không** cho biết tầm quan trọng thực tế của kết quả, và vì thế luôn nên được báo cáo cùng **effect size** và **confidence intervals** thay vì đứng một mình.

## Ví dụ Đầy đủ: One-sample T-test

Hãy thực hiện một ví dụ đầy đủ với dữ liệu thực:

**Bối cảnh:** Một nhà sản xuất chocolate tuyên bố thanh chocolate của họ nặng 100g. Chúng ta nghi ngờ tuyên bố này và cân 16 thanh ngẫu nhiên.

**Dữ liệu (gram):**
```
98, 102, 97, 99, 101, 103, 98, 100, 
99, 101, 97, 102, 100, 98, 101, 99
```

**Bước 1: Thiết lập giả thuyết.** Ta đặt $$H_0: \mu = 100$$, tức thanh chocolate nặng đúng 100g như tuyên bố; $$H_1: \mu \neq 100$$, tức trọng lượng trung bình khác 100g; và dùng mức ý nghĩa $$\alpha = 0.05$$.

**Bước 2: Tính các thống kê mẫu.** Từ dữ liệu, ta có $$n = 16$$, $$\bar{x} = 99.69$$ g, và $$s = 1.78$$ g.

**Bước 3: Tính t-statistic**

$$t = \frac{99.69 - 100}{1.78 / \sqrt{16}} = \frac{-0.31}{0.445} = -0.70$$

**Bước 4: Xác định degrees of freedom**

$$df = n - 1 = 16 - 1 = 15$$

**Bước 5: Tìm p-value**

Với $$t = -0.70$$ và $$df = 15$$, tra bảng t hoặc dùng phần mềm:

$$p = 0.495$$ (two-tailed)

**Bước 6: Kết luận**

$$p = 0.495 > 0.05$$, chúng ta **không bác bỏ** $$H_0$$.

**Diễn giải:** Không có đủ bằng chứng để kết luận rằng trọng lượng trung bình của chocolate khác 100g. Sự khác biệt quan sát được (99.69g) có thể dễ dàng xảy ra do biến động ngẫu nhiên.

**95% Confidence Interval:**

$$\bar{x} \pm t_{0.025, 15} \times \frac{s}{\sqrt{n}} = 99.69 \pm 2.131 \times 0.445 = [98.74, 100.64]$$

Khoảng tin cậy này chứa 100g, phù hợp với kết luận không bác bỏ $$H_0$$.

## So sánh T-test với Z-test

| Đặc điểm | Z-test | T-test |
|----------|--------|--------|
| **Khi nào dùng** | Biết $$\sigma$$ quần thể | Không biết $$\sigma$$ (dùng $$s$$) |
| **Phân phối** | Normal(0, 1) | t-distribution (df) |
| **Đuôi** | Mỏng hơn | Dày hơn |
| **Critical values** | Không đổi | Phụ thuộc vào df |
| **Thực tế** | Hiếm dùng | Rất phổ biến |

**Quan hệ:** Khi $$n \to \infty$$, t-distribution $$\to$$ Normal distribution

## Hạn Chế của T-test và Hướng Bayesian

Mặc dù t-test rất hữu ích, nó vẫn mang những hạn chế gần với p-value. Nó cho ta $$P(\text{data} \mid H_0)$$ chứ không phải $$P(H_0 \mid \text{data})$$, thường bị kéo về kiểu quyết định nhị phân dựa trên ngưỡng tùy ý, không tích hợp kiến thức trước về mức hợp lý của giả thuyết, và có thể cho kết luận sai nếu các giả định nền tảng bị vi phạm đáng kể.

### Phương pháp Bayesian

Trong các chương sau, bạn sẽ thấy cách phương pháp Bayesian giải quyết những hạn chế này. **Bayesian estimation** cung cấp phân phối đầy đủ của tham số thay vì chỉ một t-value đơn lẻ, **credible intervals** có diễn giải trực tiếp hơn confidence intervals, **Bayes factors** cho phép so sánh bằng chứng giữa các giả thuyết, và **priors** cho phép đưa kiến thức trước đó vào suy luận một cách minh bạch.

## Bài tập

**Bài tập 1: Tính T-statistic thủ công.** Một nghiên cứu đo điểm kiểm tra của 10 sinh viên sau khi học bằng phương pháp mới. Điểm trung bình quốc gia là 75. Dữ liệu: 78, 82, 75, 80, 77, 83, 79, 81, 76, 84. (a) Tính $$\bar{x}$$ và $$s$$. (b) Tính t-statistic để kiểm định $$H_0: \mu = 75$$. (c) Với $$\alpha = 0.05$$ (two-tailed), tra bảng t và quyết định bác bỏ $$H_0$$ hay không.

**Bài tập 2: Phân biệt các loại T-test.** Với mỗi tình huống sau, xác định loại t-test nào phù hợp: (a) So sánh điểm thi của học sinh nam và nữ. (b) So sánh huyết áp trước và sau khi tập thể dục của cùng một nhóm người. (c) Kiểm tra xem nhiệt độ trung bình hàng ngày có khác 25°C hay không. (d) So sánh hiệu quả của hai loại thuốc trên hai nhóm bệnh nhân khác nhau.

**Bài tập 3: Diễn giải Kết quả.** Một t-test cho kết quả: $$t(24) = 2.35, p = 0.027$$. (a) df = 24 có nghĩa là gì? (b) Với $$\alpha = 0.05$$, kết luận gì? (c) Nếu đây là one-tailed test thay vì two-tailed, p-value sẽ thay đổi như thế nào? (d) Viết một diễn giải đúng về ý nghĩa của p-value này.

**Bài tập 4: Kiểm tra Giả định.** Bạn có dữ liệu chiều cao của 15 người với giá trị ngoại lai rõ ràng (outlier). (a) Giả định nào của t-test có thể bị vi phạm? (b) Làm thế nào để kiểm tra giả định phân phối chuẩn? (c) Nếu giả định bị vi phạm nghiêm trọng, bạn nên làm gì? (d) Có lựa chọn nào tốt hơn t-test trong trường hợp này không?

**Bài tập 5: T-test vs Bayesian (Suy ngẫm).** Đọc ví dụ chocolate ở trên. (a) Confidence interval [98.74, 100.64] có nghĩa là gì chính xác theo quan điểm frequentist? (b) Nếu bạn là nhà sản xuất, bạn có hài lòng với kết luận "không đủ bằng chứng" không? (c) Những thông tin gì mà t-test không cung cấp mà bạn muốn biết? (d) Bạn nghĩ phương pháp Bayesian có thể giải quyết những vấn đề này như thế nào?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 4: Asymptotics and connections to non-Bayesian approaches

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 11: Null Hypothesis Significance Testing
- Chapter 16: Metric-Predicted Variable on One or Two Groups

### Classic Reference:

**Student (W.S. Gosset). (1908).** The probable error of a mean. *Biometrika*, 6(1), 1-25.
- Bài báo gốc giới thiệu phân phối t

### Supplementary Reading:

**Zimmerman, D. W. (1997).** A note on interpretation of the paired-samples t test. *Journal of Educational and Behavioral Statistics*, 22(3), 349-360.

**Delacre, M., Lakens, D., & Leys, C. (2017).** Why psychologists should by default use Welch's t-test instead of Student's t-test. *International Review of Social Psychology*, 30(1), 92-101.

---

*Bài học tiếp theo: [0.13 Phân phối đồng thời (Joint Distribution)](/vi/chapter00/joint-distribution/)*
