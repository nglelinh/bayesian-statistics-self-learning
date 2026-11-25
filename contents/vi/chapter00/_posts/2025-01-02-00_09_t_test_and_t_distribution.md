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

Đầu thế kỷ 20, William Sealy Gosset làm kỹ sư kiểm soát chất lượng tại nhà máy bia Guinness ở Dublin. Khác với các nhà toán học quen làm việc trên tập mẫu hàng nghìn người, Gosset chỉ có thể thử nghiệm trên những mẻ lúa mạch rất nhỏ (3 đến 5 mẫu mỗi lần). Ông nhận ra khi thay độ lệch chuẩn quần thể $$\sigma$$ chưa biết bằng độ lệch chuẩn mẫu $$s$$, thống kê chuẩn hóa không còn tuân theo phân phối Chuẩn nữa mà có **đuôi dày hơn hẳn**. Vì Guinness cấm nhân viên công bố bí mật công nghiệp dưới tên thật, Gosset ký bút danh "Student" năm 1908 — khai sinh ra **phân phối Student-$$t$$**.

Trong thống kê Bayes hiện đại, phân phối Student-$$t$$ còn có một đời sống thứ hai cực kỳ rực rỡ: nó xuất hiện **tự nhiên** khi ta tích phân hóa tham số phương sai chưa biết $$\sigma^2$$ (hậu nghiệm biên của $$\mu$$ trong mô hình Normal–Inverse-Gamma chính là Student-$$t$$!) và là lựa chọn hàng đầu để làm **hồi quy bền vững trước ngoại lai** (BEST — Bayesian Estimation Supersedes the t-Test).

---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu rõ bản chất của **thống kê t (t-statistic)**, **phân phối t** và **kiểm định t (t-test)** — một trong những công cụ thống kê được dùng phổ biến nhất trong nghiên cứu. Bạn sẽ nắm được vì sao cần dùng phân phối t thay cho phân phối chuẩn, cách tính và diễn giải giá trị t, cách phân biệt các dạng t-test, cũng như các giả định và hạn chế của chúng để chuẩn bị đối chiếu với cách tiếp cận Bayesian ở các chương sau.

## Kiến thức cần nhớ: Bất định của phương sai, Phân phối đuôi nặng và Hậu nghiệm biên Student-$$t$$

Ba trụ cột kết nối bài T-test cổ điển với tư duy Bayes chuyên sâu:

- **Hậu quả của việc ước lượng $$\sigma$$ từ mẫu nhỏ:** Khi cỡ mẫu $$n$$ nhỏ, độ lệch chuẩn mẫu $$s$$ có thể ngẫu nhiên bị ước lượng *quá nhỏ*, làm tỷ số $$t = (ar{x} - \mu_0)/(s/\sqrt{n})$$ phình to bất thường. Bậc tự do $$
u = n - 1$$ điều chỉnh độ dày của hai đuôi để bù đắp cho chính sự bất định này.
- **Biểu diễn hỗn hợp tỷ lệ (Scale Mixture of Normals):** Về mặt giải tích, một phân phối Student-$$t$$ thực chất là hỗn hợp vô hạn các phân phối Chuẩn có cùng trung bình nhưng phương sai biến thiên theo phân phối Inverse-Gamma. Chính cấu trúc hỗn hợp này giúp Student-$$t$$ "chấp nhận" ngoại lai mà không bị kéo lệch tâm mạnh như phân phối Chuẩn.
- **Cầu nối sang Thống kê Bayes (Mô hình BEST của Kruschke):** Thay vì chỉ ra một p-value nhị phân từ T-test, cách tiếp cận Bayes đặt likelihood Student-$$t$$ cho từng nhóm và tính phân phối hậu nghiệm của hiệu hai trung bình $$\mu_1 - \mu_2$$, hiệu độ lệch chuẩn $$\sigma_1 - \sigma_2$$ và độ lớn hiệu ứng (*effect size*) cùng một lúc.

---

## Giới thiệu: Vấn đề khi Chưa biết Độ lệch Chuẩn Quần thể

Giả sử bạn muốn kiểm tra chiều cao trung bình của nam sinh viên một trường đại học có khác 170 cm hay không. Vì không thể đo toàn bộ sinh viên, bạn chọn ngẫu nhiên 25 người và tính được trung bình mẫu $$\bar{x} = 172.5$$ cm cùng độ lệch chuẩn mẫu $$s = 6.2$$ cm. Câu hỏi đặt ra là chênh lệch giữa 172.5 cm và 170 cm có đủ lớn để bác bỏ giả thuyết ban đầu hay chỉ là biến động ngẫu nhiên do lấy mẫu.

Trong thống kê cổ điển, nếu **biết trước độ lệch chuẩn quần thể** $$\sigma$$, ta dùng **thống kê z (z-statistic)**:

$$z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

Khi đó $$z$$ tuân theo phân phối chuẩn tắc $$\mathcal{N}(0, 1)$$. Tuy nhiên, trên thực tế ta **hiếm khi biết** $$\sigma$$ mà chỉ ước lượng nó bằng độ lệch chuẩn mẫu $$s$$. Việc thay $$\sigma$$ bằng $$s$$ làm tăng độ bất định, khiến phân phối của thống kê kiểm định không còn là phân phối chuẩn nữa. Đây chính là lý do ra đời của **phân phối t** và **thống kê t**.

## T-statistic: Định nghĩa và Ý nghĩa

**Thống kê t** (hay t-value) có công thức tương tự z-statistic, nhưng thay $$\sigma$$ bằng độ lệch chuẩn mẫu $$s$$:

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

Trong đó, $$\bar{x}$$ là trung bình mẫu, $$\mu_0$$ là giá trị giả thuyết trong $$H_0$$, $$s$$ là độ lệch chuẩn mẫu, $$n$$ là cỡ mẫu, còn $$s / \sqrt{n}$$ là **sai số chuẩn của trung bình** (standard error of the mean — SE), phản ánh mức độ bất định của trung bình mẫu.

### Diễn giải giá trị T

Giá trị t cho biết trung bình mẫu nằm cách giá trị giả thuyết $$\mu_0$$ bao nhiêu lần sai số chuẩn. Nếu **$$|t|$$ lớn**, trung bình mẫu cách xa $$\mu_0$$ đáng kể, tạo bằng chứng mạnh hơn chống lại $$H_0$$; ngược lại, nếu **$$|t|$$ nhỏ**, trung bình mẫu nằm gần $$\mu_0$$ nên chưa có nhiều bằng chứng để nghi ngờ giả thuyết không.

*Cách đọc hình: Bốn biểu đồ dưới đây minh họa các mức độ cực đoan khác nhau của giá trị t và sự thay đổi tương ứng của p-value.*

![T-value nhỏ với bằng chứng yếu chống lại H0]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_small_example.png)

*Hình 1a: Với $$t = 0.5$$ và $$df = 15$$, p-value lớn (khoảng 0.62) nên dữ liệu phù hợp với $$H_0$$.*

![T-value ở vùng lưng chừng gần ngưỡng 0.05]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_borderline_example.png)

*Hình 1b: Với $$t = 2.0$$, p-value khoảng 0.064, nằm ở vùng lưng chừng sát ngưỡng 0.05.*

![T-value lớn với bằng chứng mạnh hơn chống lại H0]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_large_example.png)

*Hình 1c: Với $$t = 3.0$$, p-value nhỏ (khoảng 0.009) nên bằng chứng chống lại $$H_0$$ rõ rệt hơn.*

![Ví dụ chocolate với t âm nhỏ về độ lớn]({{ site.baseurl }}/img/chapter_img/chapter00/t_value_chocolate_example.png)

*Hình 1d: Minh họa trường hợp $$t = -0.70$$ cho $$p = 0.495$$, thể hiện chưa có đủ bằng chứng chống lại giả thuyết không.*

Phần diện tích tô màu ở hai đuôi trong mỗi hình biểu thị "vùng cực đoan" dùng để tính p-value hai phía (two-tailed test).

**Ví dụ cụ thể:** quay lại bài toán chiều cao với $$\bar{x} = 172.5$$ cm, $$\mu_0 = 170$$ cm, $$s = 6.2$$ cm và $$n = 25$$:

$$t = \frac{172.5 - 170}{6.2 / \sqrt{25}} = \frac{2.5}{1.24} \approx 2.02$$

Giá trị $$t \approx 2.02$$ cho thấy trung bình mẫu lệch khoảng 2 sai số chuẩn so với 170 cm.

## Phân phối T: Tại sao Không phải Phân phối Chuẩn?

Khi thay $$\sigma$$ bằng $$s$$, thống kê t tuân theo **phân phối t** (Student's t-distribution) thay vì phân phối chuẩn.

### Đặc điểm của Phân phối T

Phân phối t có dạng hình chuông đối xứng giống phân phối chuẩn nhưng **đuôi dày hơn**, phản ánh phần bất định tăng thêm do phải ước lượng $$\sigma$$ bằng $$s$$. Hình dạng của nó phụ thuộc vào tham số **bậc tự do** (degrees of freedom, ký hiệu $$df$$; bằng $$n - 1$$ trong kiểm định t một mẫu). Khi cỡ mẫu $$n$$ tăng lên, ước lượng $$s$$ ngày càng gần $$\sigma$$ nên phân phối t hội tụ dần về phân phối chuẩn tắc; với mẫu trên 30 quan sát, hai đường cong gần như trùng nhau khi nhìn bằng mắt thường.

### Vì sao đuôi dày hơn?

Khi cỡ mẫu nhỏ, $$s$$ dao động mạnh quanh $$\sigma$$. Trong những mẫu mà $$s$$ ngẫu nhiên nhỏ hơn $$\sigma$$ thật, giá trị $$|t|$$ sẽ bị phóng đại lên. Phần đuôi dày hơn của phân phối t giúp điều chỉnh cho sự bất định này, đòi hỏi bằng chứng mạnh hơn mới bác bỏ $$H_0$$ khi mẫu nhỏ.

![So sánh Phân phối T và Phân phối Chuẩn]({{ site.baseurl }}/img/chapter_img/chapter00/t_vs_normal_distribution.png)

*Hình minh họa: So sánh phân phối t theo các bậc tự do khác nhau với phân phối chuẩn tắc. Với **df = 2** (mẫu rất nhỏ), đuôi rất dày do bất định trong ước lượng $$\sigma$$ lớn; với **df = 5** đuôi vẫn dày hơn chuẩn rõ rệt; với **df = 10** sai khác thu hẹp; còn ở **df = 30**, đường cong gần như trùng với phân phối chuẩn (giới hạn khi $$df \to \infty$$).*

Điều này thể hiện trực tiếp qua các giá trị tới hạn (critical value) ở mức $$\alpha = 0.05$$ (kiểm định hai phía): với $$df = 2$$, ngưỡng tới hạn là $$\pm 4.303$$, trong khi ở phân phối chuẩn chỉ là $$\pm 1.96$$. Do đó, khi mẫu nhỏ, việc bác bỏ $$H_0$$ thận trọng hơn nhiều.

### Thử nghiệm: phân phối t với mẫu nhỏ

Mô phỏng thống kê t và so với mật độ t và chuẩn khi n tăng.

<div class="interactive-demo" markdown="1">
<div data-demo="pvalue-explainer" data-lang="vi" data-tab="tdist"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## Các Loại T-test

Tùy thiết kế nghiên cứu, có ba dạng t-test thường gặp:

![Bảng tóm tắt ba loại t-test]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_summary_table.png)

*Hình 2: Bảng tóm tắt mục đích, công thức và bậc tự do của ba dạng kiểm định t phổ biến.*

### 1. Kiểm định T một mẫu (One-sample T-test)

**Mục đích:** So sánh trung bình của một mẫu với một giá trị tham chiếu $$\mu_0$$ đã biết.

**Công thức:**

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

**Bậc tự do:** $$df = n - 1$$.

**Ví dụ:** Kiểm tra chiều cao trung bình của nam sinh viên có khác 170 cm hay không.

![One-sample t-test so sánh một mẫu với giá trị giả thuyết]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_one_sample.png)

*Hình 2a: One-sample t-test so sánh trung bình của một mẫu với một giá trị giả thuyết cho trước.*

### 2. Kiểm định T hai mẫu độc lập (Independent Two-sample T-test)

**Mục đích:** So sánh trung bình của hai nhóm độc lập.

**Công thức (với giả định phương sai hai nhóm bằng nhau):**

$$t = \frac{\bar{x}_1 - \bar{x}_2}{s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$$

trong đó $$s_p$$ là **độ lệch chuẩn gộp** (pooled standard deviation):

$$s_p = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1 + n_2 - 2}}$$

**Bậc tự do:** $$df = n_1 + n_2 - 2$$.

**Ví dụ:** So sánh chiều cao trung bình giữa nam sinh viên khoa A và khoa B.

![Independent two-sample t-test so sánh hai nhóm độc lập]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_independent.png)

*Hình 2b: Independent two-sample t-test so sánh trung bình giữa hai nhóm độc lập.*

### 3. Kiểm định T ghép cặp (Paired T-test)

**Mục đích:** So sánh trung bình của hai phép đo trên cùng một nhóm đối tượng (trước–sau, hoặc các cặp ghép tương ứng).

**Công thức:**

$$t = \frac{\bar{d}}{s_d / \sqrt{n}}$$

trong đó $$\bar{d}$$ là trung bình các hiệu số của từng cặp đo và $$s_d$$ là độ lệch chuẩn của các hiệu số đó.

**Bậc tự do:** $$df = n - 1$$ (với $$n$$ là số cặp).

**Ví dụ:** So sánh cân nặng bệnh nhân trước và sau khi dùng thuốc giảm cân.

![Paired t-test so sánh trước và sau trên cùng một nhóm]({{ site.baseurl }}/img/chapter_img/chapter00/t_test_type_paired.png)

*Hình 2c: Paired t-test theo dõi cùng một nhóm ở hai thời điểm và phân tích hiệu số của từng cặp quan sát.*

## Các Giả định của T-test

Kết quả t-test dựa trên ba giả định chính; nếu các giả định này bị vi phạm nghiêm trọng, kết luận có thể sai lệch:

### 1. Dữ liệu phân phối chuẩn (hoặc cỡ mẫu đủ lớn)

Dữ liệu trong mỗi nhóm cần xấp xỉ phân phối chuẩn, hoặc cỡ mẫu đủ lớn (quy tắc kinh nghiệm thường lấy $$n > 30$$) để định lý giới hạn trung tâm (CLT) phát huy tác dụng. Ta có thể kiểm tra bằng histogram, biểu đồ Q-Q (Q-Q plot) hoặc kiểm định Shapiro–Wilk (lưu ý kiểm định này rất nhạy khi cỡ mẫu lớn). Nếu mẫu nhỏ và vi phạm mạnh tính chuẩn, nên cân nhắc kiểm định phi tham số như Wilcoxon; với mẫu lớn, t-test thường vẫn khá bền vững nhờ CLT.

### 2. Tính độc lập giữa các quan sát

Các quan sát trong mẫu phải độc lập với nhau. Giả định này thường bị vi phạm khi đo lặp lại nhiều lần trên cùng đối tượng, khi dữ liệu có cấu trúc phân cấp theo nhóm, hoặc khi dữ liệu là chuỗi thời gian có tự tương quan.

### 3. Phương sai bằng nhau (đối với two-sample t-test)

Student's two-sample t-test giả định hai nhóm có cùng phương sai (homogeneity of variance). Có thể kiểm tra bằng kiểm định Levene hoặc kiểm tra nhanh xem tỷ số $$\frac{s_1}{s_2}$$ có vượt quá 2 hay không. Nếu phương sai khác nhau đáng kể, nên dùng **Welch's t-test** vì kiểm định này không đòi hỏi giả định phương sai bằng nhau.

## Diễn giải Kết quả T-test

Một kiểm định t trả về hai đại lượng chính:

1. **Giá trị t (t-value)**: đo khoảng cách giữa dữ liệu quan sát và giả thuyết không theo đơn vị sai số chuẩn; $$|t|$$ càng lớn thì bằng chứng chống lại $$H_0$$ càng mạnh.
2. **P-value**: xác suất quan sát được giá trị t ít nhất cực đoan như vậy nếu $$H_0$$ đúng. P-value nhỏ hơn mức $$\alpha$$ (thường là 0.05) thường được gọi là "có ý nghĩa thống kê", còn p-value lớn chỉ cho biết chưa có đủ bằng chứng để bác bỏ $$H_0$$.

**Lưu ý quan trọng:** p-value **không** cho biết xác suất $$H_0$$ đúng và **không** đo tầm quan trọng thực tiễn của hiệu ứng; do đó luôn cần báo cáo kèm **kích thước hiệu ứng (effect size)** và **khoảng tin cậy (confidence interval)**.

## Ví dụ Đầy đủ: One-sample T-test

**Bối cảnh:** Một nhà sản xuất tuyên bố mỗi thanh chocolate nặng 100 g. Ta cân ngẫu nhiên 16 thanh để kiểm chứng.

**Dữ liệu (gram):**
```
98, 102, 97, 99, 101, 103, 98, 100, 
99, 101, 97, 102, 100, 98, 101, 99
```

**Bước 1: Thiết lập giả thuyết.** Đặt $$H_0: \mu = 100$$ (trọng lượng trung bình bằng 100 g), $$H_1: \mu \neq 100$$ (trọng lượng trung bình khác 100 g), và chọn mức ý nghĩa $$\alpha = 0.05$$.

**Bước 2: Tính các thống kê mẫu.** Từ 16 quan sát, ta thu được $$n = 16$$, trung bình mẫu $$\bar{x} = 99.69$$ g (chính xác là $$1595/16 = 99.6875$$ g), và độ lệch chuẩn mẫu $$s = 1.85$$ g (chính xác là $$\sqrt{51.4375 / 15} \approx 1.852$$ g).

**Bước 3: Tính thống kê t.**

$$t = \frac{99.6875 - 100}{1.852 / \sqrt{16}} = \frac{-0.3125}{0.463} \approx -0.68$$

**Bước 4: Xác định bậc tự do.**

$$df = n - 1 = 16 - 1 = 15$$

**Bước 5: Tính p-value.** Với $$t \approx -0.68$$ và $$df = 15$$, kiểm định hai phía cho:

$$p \approx 0.510$$

**Bước 6: Kết luận.** Vì $$p = 0.510 > 0.05$$, ta **không bác bỏ** $$H_0$$. Chưa có đủ bằng chứng thống kê để kết luận trọng lượng trung bình của thanh chocolate khác 100 g; mức chênh lệch quan sát được (99.69 g so với 100 g) hoàn toàn có thể do biến động lấy mẫu.

**Khoảng tin cậy 95%:**

$$\bar{x} \pm t_{0.025, 15} \times \frac{s}{\sqrt{n}} = 99.69 \pm 2.131 \times 0.463 = [98.70, 100.67]$$

Khoảng tin cậy này chứa giá trị 100 g, nhất quán với kết luận không bác bỏ $$H_0$$.

### Đọc thêm bằng kích thước hiệu ứng (effect size)

Chuẩn hóa độ lệch trung bình theo độ lệch chuẩn mẫu (Cohen's $$d$$):

$$
d = \frac{99.6875 - 100}{1.852} \approx -0.17
$$

Đây là kích thước hiệu ứng rất nhỏ: không chỉ p-value lớn mà bản thân độ lệch trung bình cũng không đáng kể về mặt thực tế. Ví dụ này cho thấy một kết quả thống kê nên được đọc qua cả ba góc độ: chiều hướng hiệu ứng, độ lớn hiệu ứng và độ bất định xung quanh ước lượng.

## So sánh T-test với Z-test

| Đặc điểm | Z-test | T-test |
|----------|--------|--------|
| **Điều kiện sử dụng** | Biết $$\sigma$$ quần thể | Không biết $$\sigma$$ (ước lượng bằng $$s$$) |
| **Phân phối** | $$\mathcal{N}(0, 1)$$ | Phân phối t theo bậc tự do $$df$$ |
| **Độ dày đuôi** | Mỏng hơn | Dày hơn |
| **Giá trị tới hạn** | Cố định | Phụ thuộc vào $$df$$ |
| **Mức độ sử dụng thực tế** | Ít gặp | Rất phổ biến |

**Mối liên hệ:** khi $$n \to \infty$$, phân phối t hội tụ về phân phối chuẩn tắc.

## Hạn chế của T-test và Hướng tiếp cận Bayesian

T-test kế thừa các giới hạn cốt lõi của p-value: nó chỉ trả về $$P(\text{data} \mid H_0)$$ thay vì $$P(H_0 \mid \text{data})$$, dễ dẫn tới quyết định nhị phân theo ngưỡng cố định, không tích hợp được kiến thức tiên nghiệm và có thể sai lệch khi các giả định bị vi phạm.

### Hướng tiếp cận Bayesian

Trong các chương tiếp theo, bạn sẽ thấy thống kê Bayesian khắc phục những điểm này như thế nào: **ước lượng Bayesian** cung cấp toàn bộ phân phối hậu nghiệm của tham số thay vì chỉ một giá trị t; **khoảng credible** có diễn giải xác suất trực tiếp; **Bayes factor** so sánh định lượng mức độ ủng hộ của dữ liệu giữa các giả thuyết; và **phân phối tiên nghiệm (prior)** cho phép đưa hiểu biết nền vào mô hình một cách minh bạch.

## Giải thích: Tính tay một phép kiểm định $$t$$ và nhìn thấy hậu nghiệm biên Student-$$t$$

Hãy đi chậm qua 4 bước để vừa làm chủ phép tính tay T-test cổ điển, vừa nhìn thấy bản chất Bayes ẩn bên trong:

1. **Tính trung bình mẫu $$ar{x}$$ và độ lệch chuẩn mẫu $$s$$** (chia cho $$n - 1$$, bậc tự do $$
u = n - 1$$).
2. **Tính sai số chuẩn $$	ext{SE} = s/\sqrt{n}$$:** Đo độ dao động dự kiến của trung bình mẫu.
3. **Tính thống kê $$t = rac{ar{x} - \mu_0}{	ext{SE}}$$** và so với giá trị tới hạn $$t_{
u, 0.975}$$ (với $$
u = 3$$ là $$3.182$$, lớn hơn hẳn mốc $$1.96$$ của phân phối Chuẩn!).
4. **Góc nhìn Bayes tương ứng:** Với prior không thông tin chuẩn hóa $$p(\mu, \sigma^2) \propto 1/\sigma^2$$, phân phối hậu nghiệm chính xác của $$\mu$$ sau khi tích phân hóa $$\sigma^2$$ chính là phân phối Student-$$t$$ dịch chuyển:
   $$rac{\mu - ar{x}}{s/\sqrt{n}} \;\Bigert\; 	ext{data} \;\sim\; t_{n-1}.$$

### Ví dụ tính toán làm từng bước: 4 mẻ thí nghiệm nhỏ kiểm tra hàm lượng chuẩn $$\mu_0 = 100$$

Bạn đo hàm lượng hoạt chất trên $$n = 4$$ mẫu thử độc lập và thu được: $$x = \{104, 108, 102, 106\}$$.

- **Bước 1 — Trung bình và độ lệch chuẩn mẫu:**
  - $$ar{x} = rac{104 + 108 + 102 + 106}{4} = rac{420}{4} = 105$$.
  - Độ lệch so với $$105$$: $$-1, +3, -3, +1$$; tổng bình phương $$= 1 + 9 + 9 + 1 = 20$$.
  - $$s^2 = rac{20}{4 - 1} = rac{20}{3} pprox 6.667 \implies s pprox 2.582$$.
- **Bước 2 — Sai số chuẩn và thống kê $$t$$:**
  - $$	ext{SE} = rac{2.582}{\sqrt{4}} = rac{2.582}{2} = 1.291$$.
  - $$t = rac{105 - 100}{1.291} pprox 3.873$$ với bậc tự do $$
u = 3$$.
- **Bước 3 — Đối chiếu hai trường phái trên cùng con số:**
  - *Frequentist:* Vì $$t = 3.873 > t_{3, 0.975} = 3.182$$, ta bác bỏ $$H_0: \mu = 100$$ ở mức $$lpha = 0.05$$ ($$p pprox 0.030$$).
  - *Bayes (với prior tham chiếu $$1/\sigma^2$$):* Khoảng tin cậy hậu nghiệm 95% của $$\mu$$ là $$105 \pm 3.182 	imes 1.291 = [100.89, 109.11]$$, và ta được phép phát biểu trực tiếp: *"Xác suất hậu nghiệm để hàm lượng thật lớn hơn 100 là $$1 - P(T_3 \le -3.873) pprox 98.5\%$$."*

**Hiểu lầm cần tránh:** Dùng mốc $$\pm 1.96 	imes 	ext{SE}$$ cho mẫu nhỏ $$n = 4$$: khoảng thu được sẽ chỉ là $$[102.47, 107.53]$$ — hẹp giả tạo tới gần 40% vì đã bỏ qua bất định của $$\sigma$$!

**Kiểm tra nhanh:** Khi $$n$$ tăng lên trên 30, giá trị tới hạn $$t_{n-1, 0.975}$$ tiến rất sát về $$1.96$$ (ví dụ $$t_{30, 0.975} pprox 2.042$$), cho thấy sự bất định do chưa biết $$\sigma$$ dần tan biến khi có nhiều dữ liệu.

---

## Video tham khảo

- [Introduction to the t Distribution (non-technical)](https://www.youtube.com/watch?v=Uv6nGIgZMVw) — jbstatistics, English. **Xem trước.** Giải thích trực quan vì sao phải dùng phân phối t thay cho phân phối chuẩn khi ước lượng độ lệch chuẩn từ mẫu.
- [Introduction to t statistics | Confidence intervals | AP Statistics | Khan Academy](https://www.youtube.com/watch?v=a2rd4Qy8yNI) — Khan Academy, English. Trình bày thống kê t và khoảng tin cậy tương ứng qua ví dụ cụ thể.
- [StatQuickie: Which t test to use](https://www.youtube.com/watch?v=nnBJeb_I-q8) — StatQuest with Josh Starmer, English. Hướng dẫn chọn đúng loại t-test theo thiết kế thu thập mẫu.

## Bài tập

**Bài tập 1: Tính thống kê t thủ công.** Đo điểm kiểm tra của 10 sinh viên học theo phương pháp mới: 78, 82, 75, 80, 77, 83, 79, 81, 76, 84. Biết điểm trung bình toàn quốc là 75. (a) Tính $$\bar{x}$$ và $$s$$. (b) Tính thống kê t cho giả thuyết $$H_0: \mu = 75$$. (c) Với $$\alpha = 0.05$$ (hai phía), tra bảng t và nêu kết luận.

**Bài tập 2: Phân biệt các loại t-test.** Xác định dạng t-test phù hợp cho từng tình huống: (a) so sánh điểm thi của học sinh nam và nữ; (b) so sánh huyết áp trước và sau khi tập thể dục của cùng một nhóm người; (c) kiểm tra nhiệt độ trung bình hàng ngày có khác 25°C hay không; (d) so sánh hiệu quả hai loại thuốc trên hai nhóm bệnh nhân độc lập.

**Bài tập 3: Diễn giải kết quả.** Một kiểm định t cho kết quả $$t(24) = 2.35, p = 0.027$$. (a) $$df = 24$$ cho biết điều gì? (b) Với $$\alpha = 0.05$$, kết luận ra sao? (c) Nếu chuyển sang kiểm định một phía (đúng chiều), p-value thay đổi thế nào? (d) Viết một câu diễn giải chuẩn xác cho p-value này.

**Bài tập 4: Kiểm tra giả định.** Bạn có dữ liệu chiều cao của 15 người trong đó xuất hiện một giá trị ngoại lai rõ rệt. (a) Giả định nào của t-test có nguy cơ bị vi phạm? (b) Kiểm tra giả định phân phối chuẩn bằng cách nào? (c) Khi giả định bị vi phạm nặng ở mẫu nhỏ, nên xử lý ra sao? (d) Có phương pháp nào thay thế tốt hơn t-test trong tình huống này không?

**Bài tập 5: T-test và Bayesian (suy ngẫm).** Xem lại ví dụ chocolate ở trên. (a) Khoảng tin cậy 95% $$[98.70, 100.67]$$ có ý nghĩa chính xác là gì theo quan điểm tần suất? (b) Ở góc độ nhà sản xuất, kết luận "chưa đủ bằng chứng bác bỏ $$H_0$$" đã đủ cho quyết định thực tế chưa? (c) Những thông tin nào bạn muốn biết mà t-test không cung cấp trực tiếp? (d) Phương pháp Bayesian có thể giải quyết những câu hỏi đó như thế nào?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 4: Asymptotics and connections to non-Bayesian approaches

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 11: Null Hypothesis Significance Testing
- Chapter 16: Metric-Predicted Variable on One or Two Groups

### Classic Reference:

**Student (W.S. Gosset). (1908).** The probable error of a mean. *Biometrika*, 6(1), 1-25.
- Bài báo gốc giới thiệu phân phối t.

### Supplementary Reading:

**Zimmerman, D. W. (1997).** A note on interpretation of the paired-samples t test. *Journal of Educational and Behavioral Statistics*, 22(3), 349-360.

**Delacre, M., Lakens, D., & Leys, C. (2017).** Why psychologists should by default use Welch's t-test instead of Student's t-test. *International Review of Social Psychology*, 30(1), 92-101.

---

*Bài học tiếp theo: [0.13 Phân phối đồng thời (Joint Distribution)]({{ site.baseurl }}/contents/vi/chapter00/00_11_joint_distribution/)*
