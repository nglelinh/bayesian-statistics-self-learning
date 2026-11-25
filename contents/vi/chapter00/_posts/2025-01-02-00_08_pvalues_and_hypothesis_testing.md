---
layout: post
title: "Bài 0.11: P-values và Kiểm định Giả thuyết"
chapter: '00'
order: 11
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

Một buổi chiều mùa hè thập niên 1920 ở Cambridge, một nữ đồng nghiệp tuyên bố bà có thể nếm ra tách trà được rót sữa trước hay rót trà trước. Ronald Fisher lập tức thiết kế thí nghiệm pha 8 tách trà (4 sữa trước, 4 trà trước) và tính xác suất đoán đúng hết nếu chỉ đoán mò: $$1 / inom{8}{4} = 1/70 pprox 0.014$$. Từ tách trà ấy, khái niệm **p-value** ra đời — ban đầu chỉ là một thước đo bằng chứng nhẹ nhàng chống lại giả thuyết ngẫu nhiên, nhưng về sau bị biến thành "cửa ải $$p < 0.05$$" đầy tranh cãi trong khoa học hiện đại.

Muốn hiểu vì sao thống kê Bayes ngày càng được giới nghiên cứu ưa chuộng, trước hết ta phải hiểu **chính xác** kiểm định giả thuyết cổ điển đang tính cái gì — và đâu là ranh giới nó không thể vượt qua.

---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu rõ bản chất của **p-value** và kiểm định giả thuyết theo quan điểm tần suất (**frequentist**), không chỉ để áp dụng đúng mà quan trọng hơn là nhận diện rõ các giới hạn của chúng. Bạn sẽ hiểu vì sao p-value thường bị diễn giải sai, vì sao nó không trả lời trực tiếp nhiều câu hỏi mà nhà khoa học quan tâm, và vì sao **phương pháp Bayesian mang lại cách tiếp cận tự nhiên và mạch lạc hơn cho suy diễn thống kê**. Mục tiêu không phải loại bỏ hoàn toàn kiểm định giả thuyết, mà là sử dụng nó một cách phản biện và biết khi nào cần chuyển sang công cụ khác.

## Kiến thức cần nhớ: Kiểm định Frequentist, Sai lầm loại I/II và Góc nhìn đối sánh Bayes

Ba trụ cột giúp bạn đọc sâu bài này mà không rơi vào tranh cãi cảm tính giữa hai trường phái:

- **Kiểm định ý nghĩa thống kê (NHST — Fisher & Neyman–Pearson):** Giả định trước giả thuyết không $$H_0$$ là đúng, rồi tính xác suất thu được dữ liệu cực đoan bằng hoặc hơn dữ liệu đã quan sát: $$p	ext{-value} = P(	ext{dữ liệu cực đoan} \ge 	ext{quan sát} \mid H_0)$$. Chú ý chiều điều kiện: $$H_0$$ nằm ở *vế sau* dấu gạch đứng.
- **Lực thống kê & Tỷ lệ dương tính giả (Power & Base Rate):** Ngưỡng $$lpha = 0.05$$ chỉ kiểm soát tỷ lệ báo động giả *khi $$H_0$$ đúng*. Nó hoàn toàn phớt lờ xác suất tiên nghiệm $$P(H_1)$$ (giả thuyết có hợp lý không trước khi làm thí nghiệm?) và lực kiểm định $$1 - eta$$.
- **Cầu nối sang Thống kê Bayes (Posterior & Bayes Factor):** Điều nhà khoa học thực sự muốn biết là $$P(H_0 \mid 	ext{data})$$ hoặc phân phối hậu nghiệm của độ lớn hiệu ứng $$\delta \mid 	ext{data}$$. Định lý Bayes cho thấy muốn đảo chiều từ $$P(	ext{data} \mid H_0)$$ sang $$P(H_0 \mid 	ext{data})$$, ta *bắt buộc* phải đưa vào prior $$P(H_0)$$ và so sánh với likelihood dưới $$H_1$$.

---

## Giới thiệu: Tại sao chúng ta cần nói về P-values?

Trong một khóa học về phân tích dữ liệu Bayesian, việc tìm hiểu kỹ p-value và kiểm định giả thuyết theo trường phái tần suất xuất phát từ ba lý do chính:

1. **Tính phổ biến trong nghiên cứu**: p-value và kiểm định giả thuyết vẫn là công cụ được dùng rộng rãi nhất trong y học, tâm lý học, kinh tế học và nhiều ngành khoa học khác. Để đọc và đánh giá bài báo khoa học một cách phản biện, cần hiểu chính xác ý nghĩa của p-value.
2. **Tần suất hiểu sai rất cao**: p-value thuộc nhóm khái niệm thống kê dễ bị hiểu nhầm nhất, kể cả trong cộng đồng nghiên cứu. Nắm đúng định nghĩa giúp tránh các diễn giải sai lệch.
3. **Động lực cho cách tiếp cận Bayesian**: thấy rõ những câu hỏi mà p-value không trả lời được sẽ giúp bạn hiểu vì sao khuôn khổ Bayesian phù hợp và trực tiếp hơn trong nhiều bài toán suy luận.

## Khung Kiểm định Giả thuyết: Một Cách Tiếp cận Gián tiếp

Kiểm định giả thuyết theo quan điểm tần suất dựa trên lập luận gián tiếp. Thay vì đánh giá trực tiếp bằng chứng ủng hộ giả thuyết ta quan tâm, ta đặt ra một **giả thuyết không** (null hypothesis), ký hiệu $$H_0$$, biểu thị trạng thái "không có hiệu ứng" hay "không có sự khác biệt", rồi tìm bằng chứng chống lại nó.

Ví dụ, khi đánh giá một loại thuốc mới có làm giảm huyết áp hay không, thay vì hỏi trực tiếp "thuốc có hiệu quả không?" hoặc "mức giảm huyết áp là bao nhiêu?", khung kiểm định giả thuyết yêu cầu thiết lập: **giả thuyết không** $$H_0$$ (thuốc không có tác dụng, mức thay đổi huyết áp trung bình bằng 0) và **giả thuyết thay thế** $$H_1$$ (thuốc có tác dụng, mức thay đổi trung bình khác 0).

Logic kiểm định là: **nếu dữ liệu quan sát được rất khó xảy ra trong trường hợp $$H_0$$ đúng, thì ta có bằng chứng chống lại $$H_0$$ và có thể "bác bỏ" nó**. Lập luận này tương tự phép chứng minh phản chứng trong toán học, nhưng có một điểm khác biệt cơ bản: **trong thống kê, ta không chứng minh tuyệt đối được điều gì mà chỉ định lượng mức độ bất thường của dữ liệu dưới $$H_0$$**.

Khung tư duy này được phát triển từ đầu thế kỷ 20 bởi Ronald Fisher, Jerzy Neyman và Egon Pearson nhằm tạo ra một quy trình ra quyết định khách quan từ dữ liệu. Tuy nhiên, như ta sẽ thấy dưới đây, cách tiếp cận gián tiếp này cũng kéo theo nhiều giới hạn thực tế.

## P-value: Định nghĩa Chính xác

Hãy bắt đầu bằng định nghĩa chuẩn xác của p-value:

**P-value là xác suất quan sát được dữ liệu ít nhất bất thường như dữ liệu thực tế (hoặc cực đoan hơn), với điều kiện giả thuyết không $$H_0$$ là đúng.**

Một cách hình thức, nếu $$T$$ là **thống kê kiểm định** (test statistic) tính từ dữ liệu và $$t_{obs}$$ là giá trị quan sát được, thì (với kiểm định một phía bên phải):

$$p = P(T \geq t_{obs} \mid H_0)$$

(và công thức tương tự cho kiểm định một phía bên trái hoặc hai phía).

Định nghĩa này gồm ba thành phần then chốt:

1. **"Xác suất"**: p-value là một số nằm trong đoạn $$[0, 1]$$.
2. **"Ít nhất bất thường như dữ liệu thực tế"**: không chỉ tính xác suất của riêng kết quả quan sát được mà gộp cả mọi kết quả cực đoan hơn theo hướng kiểm định.
3. **"Với điều kiện giả thuyết không là đúng"**: p-value **không** phải xác suất để $$H_0$$ đúng, mà là xác suất của dữ liệu **nếu** $$H_0$$ đúng.

Sự khác biệt giữa $$P(\text{dữ liệu} \mid H_0)$$ và $$P(H_0 \mid \text{dữ liệu})$$ mang tính nền tảng. P-value cho biết vế thứ nhất, trong khi câu hỏi nhà nghiên cứu thường muốn trả lời lại là vế thứ hai.

---

### Giải thích từng thành phần

#### (1) "Giả thuyết không là đúng" ($$H_0$$ đúng)

Ta luôn **giả định trước** rằng $$H_0$$ đúng, rồi hỏi: nếu $$H_0$$ đúng thật, xác suất để dữ liệu xuất hiện cực đoan như thế này có thấp không? Ví dụ, nếu $$H_0$$ cho rằng thuốc không có tác dụng nhưng dữ liệu lại có vẻ khả quan, p-value trả lời câu hỏi: "nếu thuốc thực sự vô tác dụng, xác suất để vẫn quan sát được kết quả ít nhất cực đoan như vậy là bao nhiêu?"

#### (2) "Dữ liệu bất thường" nghĩa là gì?

"Bất thường" không phải cảm nhận chủ quan mà được đo bằng **thống kê kiểm định** như z-score, t-statistic hay $$\chi^2$$, phản ánh khoảng cách giữa dữ liệu quan sát và kỳ vọng dưới $$H_0$$. Trung bình mẫu lệch càng xa giá trị giả thuyết, chênh lệch giữa hai nhóm càng lớn, hay giá trị thống kê rơi càng sâu vào phần đuôi phân phối, dữ liệu càng được xem là cực đoan.

#### (3) "Ít nhất bất thường như dữ liệu quan sát (hoặc bất thường hơn)"

P-value **không chỉ** tính xác suất của đúng giá trị quan sát được, mà tính:

> Xác suất của kết quả quan sát được **và toàn bộ các kết quả còn cực đoan hơn**.

**Ví dụ (kiểm định hai phía):** nếu quan sát được $$z = 2.1$$, p-value là $$P(\mid Z \mid \geq 2.1 \mid H_0 \text{ đúng})$$, tức gộp cả các giá trị như 2.5, 3.0 và mọi giá trị cực đoan hơn ở cả hai phía đuôi phân phối.

---

### Những điều P-value KHÔNG nói

P-value không phải xác suất giả thuyết không đúng hay sai, không phải xác suất kết quả "xảy ra do ngẫu nhiên", và cũng không đo trực tiếp kích thước hiệu ứng.

**Diễn giải sai:**

> "P-value = 0.03 nghĩa là 97% khả năng $$H_0$$ sai." ❌

**Diễn giải đúng:**

> "Nếu $$H_0$$ đúng, xác suất quan sát được dữ liệu ít nhất cực đoan như thế này là 3%." ✅

---

### Diễn giải trực giác ngắn gọn

Có thể gói gọn bản chất của p-value như sau: **p-value đo mức độ khó tin của dữ liệu dưới giả định rằng $$H_0$$ đúng.** Khi p-value nhỏ, dữ liệu khó phù hợp với $$H_0$$ nên ta có lý do nghi ngờ $$H_0$$; khi p-value lớn, dữ liệu chưa mâu thuẫn mạnh với $$H_0$$.

---

## Một Ví dụ Cụ thể: Kiểm định T

Giả sử ta muốn kiểm tra chiều cao trung bình của nam sinh viên tại một trường đại học có khác 170 cm hay không. Ta đo ngẫu nhiên 25 nam sinh viên và thu được trung bình mẫu $$\bar{x} = 172.5$$ cm, độ lệch chuẩn mẫu $$s = 6.2$$ cm.

Ta thiết lập $$H_0: \mu = 170$$ (chiều cao trung bình quần thể bằng 170 cm) và $$H_1: \mu \neq 170$$ (chiều cao trung bình quần thể khác 170 cm). Thống kê kiểm định t là:

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}} = \frac{172.5 - 170}{6.2 / \sqrt{25}} = \frac{2.5}{1.24} \approx 2.02$$

Với $$n - 1 = 24$$ bậc tự do, xác suất để quan sát được $$\mid t \mid \geq 2.02$$ nếu $$H_0$$ đúng (kiểm định hai phía) là $$p \approx 0.054$$.

![Minh họa P-value trong Kiểm định T]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_ttest_illustration.png)

*Cách đọc hình: Đường cong biểu diễn phân phối t dưới giả thuyết $$H_0$$; phần diện tích tô màu ở hai đuôi ngoài mốc $$\pm 2.02$$ chính là p-value hai phía.*

Kết quả này có nghĩa là: **nếu** chiều cao trung bình quần thể thực sự bằng 170 cm và ta lặp lại việc lấy mẫu ngẫu nhiên 25 người rất nhiều lần, khoảng 5.4% số lần sẽ cho trị tuyệt đối của thống kê t lớn hơn hoặc bằng 2.02. Nó không cho biết xác suất $$H_0$$ đúng là 5.4%, không cho biết xác suất $$H_1$$ đúng là 94.6%, và cũng không nói lên độ lớn hay ý nghĩa thực tiễn của sự chênh lệch.

### Cách đọc hợp lý hơn cho $$p = 0.054$$

Con số $$0.054$$ nằm rất sát ngưỡng 0.05. Thay vì coi đó là "thất bại hoàn toàn", cách hiểu hợp lý hơn là dữ liệu tạo ra mức mâu thuẫn vừa phải với $$H_0$$ nhưng chưa đủ mạnh theo quy ước truyền thống. Một nghiên cứu tương tự cho ra $$p = 0.049$$ thực chất mang lượng bằng chứng gần như tương đương.

Vì thế, nhiều nhà thống kê khuyến nghị không dùng p-value như một công tắc bật/tắt nhị phân, mà cần đọc song song với kích thước hiệu ứng (effect size), khoảng tin cậy (confidence interval), chất lượng thiết kế nghiên cứu và bối cảnh khoa học.

### Thử nghiệm: p-value dưới H₀ phân phối đều

Lặp thí nghiệm nhiều lần: khi không có hiệu ứng vẫn có ~5% thí nghiệm cho p < 0.05.

<div class="interactive-demo" markdown="1">
<div data-demo="pvalue-explainer" data-lang="vi" data-tab="pnull"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## Ngưỡng Ý nghĩa và Quyết định: Quy ước $$\alpha = 0.05$$

Trong thực hành, p-value thường được so sánh với **mức ý nghĩa** (significance level) định trước $$\alpha$$, phổ biến nhất là $$\alpha = 0.05$$ (đôi khi là 0.01 hoặc 0.10).

#### Quy tắc quyết định truyền thống:

Nếu $$p < \alpha$$, ta bác bỏ $$H_0$$ và gọi kết quả là "có ý nghĩa thống kê"; nếu $$p \geq \alpha$$, ta không bác bỏ $$H_0$$ và kết luận chưa đủ bằng chứng chống lại nó.

Trong ví dụ chiều cao ở trên, với $$p = 0.054$$ và $$\alpha = 0.05$$, ta **không bác bỏ** $$H_0$$. Tuy nhiên, hãy chú ý rằng chênh lệch giữa $$p = 0.054$$ và $$p = 0.049$$ rất nhỏ nhưng lại dẫn đến hai kết luận trái ngược nhau ("không có ý nghĩa thống kê" so với "có ý nghĩa thống kê"), dù bằng chứng thực tế trong dữ liệu gần như giống nhau.

![Hai p-value gần nhau nhưng rơi hai phía của ngưỡng alpha]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretation_alpha_cutoff.png)

*Hình minh họa: Khi p-value nằm sát ngưỡng $$\alpha = 0.05$$, một chênh lệch rất nhỏ vẫn bị chia cắt thành hai kết luận nhị phân trái ngược.*

Bản thân ngưỡng $$\alpha = 0.05$$ cũng mang tính quy ước. Ronald Fisher khi đề xuất mốc này đã nhấn mạnh đây chỉ là chỉ dẫn sơ bộ, không phải ranh giới cứng nhắc. Việc áp dụng máy móc ngưỡng 0.05 dẫn đến nhiều hệ quả tiêu cực: khuyến khích hành vi "p-hacking", thu hẹp suy luận thành câu hỏi nhị phân "có hay không có hiệu ứng", và làm mờ đi kích thước hiệu ứng cùng độ bất định của ước lượng.

### Thử nghiệm: công suất của t-test

Công suất tăng theo cỡ mẫu và độ lớn hiệu ứng; tại d = 0 nó bằng α.

<div class="interactive-demo" markdown="1">
<div data-demo="pvalue-explainer" data-lang="vi" data-tab="power"></div>
</div>

## Những Hiểu lầm Phổ biến về P-values

Dưới đây là năm hiểu lầm hay gặp nhất khi diễn giải p-value:

### Hiểu lầm 1: P-value là xác suất giả thuyết không đúng

**Sai:** "$$p = 0.03$$ nghĩa là có 3% khả năng giả thuyết không đúng."

**Đúng:** P-value là xác suất của dữ liệu (hoặc dữ liệu cực đoan hơn) **khi giả định** $$H_0$$ đúng, không phải xác suất $$H_0$$ đúng sau khi đã quan sát dữ liệu. Muốn tính $$P(H_0 \mid \text{dữ liệu})$$, cần dùng định lý Bayes cùng xác suất tiên nghiệm cho $$H_0$$ — điều mà khung tần suất không cung cấp.

![P-value không phải là xác suất của giả thuyết không]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretation_h0_probability.png)

*Hình minh họa: P-value phản ánh xác suất theo chiều $$P(\text{dữ liệu} \mid H_0)$$, chứ không phải chiều $$P(H_0 \mid \text{dữ liệu})$$ mà nhà nghiên cứu thường muốn biết.*

### Hiểu lầm 2: $$1 - p$$ là xác suất giả thuyết thay thế đúng

**Sai:** "Nếu $$p = 0.05$$ thì có 95% khả năng giả thuyết thay thế đúng."

**Đúng:** P-value không cung cấp thông tin trực tiếp về xác suất của giả thuyết thay thế.

### Hiểu lầm 3: P-value nhỏ có nghĩa là hiệu ứng lớn

**Sai:** "$$p < 0.001$$ nghĩa là hiệu ứng rất mạnh."

**Đúng:** P-value nhỏ chỉ cho thấy dữ liệu rất khó xảy ra nếu $$H_0$$ đúng. Điều đó có thể đến từ hiệu ứng lớn, nhưng cũng có thể đến từ cỡ mẫu rất lớn kèm một hiệu ứng thực tế cực nhỏ và không có ý nghĩa ứng dụng.

![P-value nhỏ không đồng nghĩa hiệu ứng lớn]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretation_small_p_large_effect.png)

*Hình minh họa: Một p-value rất nhỏ vẫn có thể xuất hiện với hiệu ứng nhỏ nếu cỡ mẫu đủ lớn.*

![Mẫu lớn với hiệu ứng nhỏ]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_large_n_small_effect.png)

*Hình 1a: Với cỡ mẫu lớn (n = 1000), một hiệu ứng rất nhỏ vẫn có thể đạt ngưỡng "có ý nghĩa thống kê".*

![Mẫu nhỏ với hiệu ứng lớn]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_small_n_large_effect.png)

*Hình 1b: Với cỡ mẫu nhỏ (n = 20), ngay cả hiệu ứng lớn cũng có thể không đạt ngưỡng ý nghĩa thống kê. Vì vậy, p-value không đo trực tiếp kích thước hiệu ứng.*

### Hiểu lầm 4: P-value lớn chứng minh giả thuyết không đúng

**Sai:** "$$p = 0.80$$ chứng tỏ giả thuyết không là đúng."

**Đúng:** P-value lớn chỉ cho biết dữ liệu không mâu thuẫn mạnh với $$H_0$$. Nguyên nhân có thể là $$H_0$$ thực sự đúng, hoặc đơn giản là cỡ mẫu quá nhỏ chưa đủ công suất để phát hiện sự khác biệt. "Không có bằng chứng về hiệu ứng" không đồng nghĩa với "bằng chứng rằng không có hiệu ứng".

![P-value lớn không chứng minh giả thuyết không đúng]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretation_large_p_h0_true.png)

*Hình minh họa: P-value lớn chỉ cho thấy dữ liệu không mâu thuẫn mạnh với $$H_0$$, chứ không chứng minh $$H_0$$ đúng.*

### Hiểu lầm 5: P-value đo lường khả năng tái lập

**Sai:** "$$p = 0.05$$ nghĩa là nếu lặp lại nghiên cứu, tôi có 95% cơ hội thu được kết quả tương tự."

**Đúng:** P-value không đo khả năng tái lập. Trên thực tế, nhiều kết quả có $$p$$ sát mốc 0.05 rất khó tái lập trong các nghiên cứu độc lập sau đó.

## Vấn đề với Kiểm định Giả thuyết Không

Một hạn chế nền tảng của kiểm định giả thuyết là bản thân $$H_0$$ dạng điểm thường khó xảy ra chính xác trong thực tế. Chẳng hạn, giả thuyết "thuốc A và thuốc B có hiệu quả hoàn toàn bằng nhau" gần như chắc chắn sai ở mức sai khác rất nhỏ. Khi cỡ mẫu đủ lớn, ta gần như luôn bác bỏ được $$H_0$$, nhưng kết quả đó không cho biết sự khác biệt có đủ lớn để có giá trị lâm sàng hay thực tiễn hay không.

Câu hỏi trọng tâm của nghiên cứu khoa học thường là "hiệu ứng lớn đến mức nào?" và "độ bất định của ước lượng ra sao?" — những câu hỏi mà kiểm định giả thuyết không trả lời trực tiếp.

![Một ví dụ false positive khi kiểm định lặp lại nhiều lần]({{ site.baseurl }}/img/chapter_img/chapter00/multiple_testing_false_positive_example.png)

*Hình 2a: Khi thực hiện nhiều kiểm định độc lập, chỉ riêng biến động ngẫu nhiên cũng dễ tạo ra một vài kết quả vượt ngưỡng ý nghĩa thống kê.*

![Phân phối p-value gần uniform khi H0 đúng]({{ site.baseurl }}/img/chapter_img/chapter00/multiple_testing_uniform_pvalues.png)

*Hình 2b: Khi $$H_0$$ đúng, p-value phân bố đều trên đoạn $$[0,1]$$, nên thử đủ nhiều kiểm định gần như chắc chắn sẽ xuất hiện vài p-value nhỏ.*

Đây chính là bản chất của bài toán kiểm định bội (multiple testing) và p-hacking: khi chạy 20 kiểm định độc lập với $$\alpha = 0.05$$ dù tất cả $$H_0$$ đều đúng, ta vẫn kỳ vọng gặp trung bình 1 kết quả "có ý nghĩa thống kê" thuần túy do ngẫu nhiên. Đây là một nguyên nhân lớn dẫn đến khủng hoảng tái lập trong khoa học.

## Khoảng Tin cậy: Một Cách Tiếp cận Tốt hơn?

Một công cụ tần suất khác thường được khuyến nghị thay cho việc chỉ báo cáo p-value là **khoảng tin cậy** (confidence interval). Khoảng tin cậy 95% cho tham số $$\theta$$ là một khoảng ngẫu nhiên $$[L, U]$$ xây dựng từ dữ liệu sao cho:

$$P(L \leq \theta \leq U) = 0.95$$

trong đó xác suất được tính trên toàn bộ các mẫu lặp lại có thể (với $$\theta$$ là hằng số cố định).

Khoảng tin cậy cung cấp thêm thông tin về độ lớn hiệu ứng và độ bất định, nhưng cách diễn giải chuẩn vẫn dễ gây nhầm lẫn:

**Diễn giải đúng:** "Nếu lặp lại quy trình lấy mẫu và dựng khoảng tin cậy 95% rất nhiều lần, thì 95% số khoảng thu được sẽ chứa giá trị thật của $$\theta$$."

![Nhiều confidence interval qua các lần lặp thí nghiệm]({{ site.baseurl }}/img/chapter_img/chapter00/confidence_interval_repeated_experiments.png)

*Hình 3a: Khoảng tin cậy tần suất là phát biểu về quy trình lặp lại thí nghiệm: trên nhiều lần lặp, khoảng 95% số khoảng chứa giá trị thật.*

**Diễn giải sai (nhưng rất phổ biến):** "Có 95% khả năng giá trị thật của $$\theta$$ nằm trong khoảng cụ thể này."

Trong khung tần suất, $$\theta$$ là hằng số chưa biết chứ không phải biến ngẫu nhiên, nên xác suất 95% gắn với bản thân quy trình tạo khoảng, không phải với $$\theta$$. Trong khi đó, phát biểu thứ hai — đánh giá trực tiếp xác suất tham số nằm trong một khoảng dựa trên dữ liệu hiện có — lại chính là ý nghĩa của **khoảng tin cậy Bayesian** (credible interval).

![Một credible interval trên posterior của một thí nghiệm cụ thể]({{ site.baseurl }}/img/chapter_img/chapter00/credible_interval_single_posterior.png)

*Hình 3b: Khoảng credible được xác định trực tiếp từ phân phối hậu nghiệm của thí nghiệm hiện tại, cho phép phát biểu trực tiếp về xác suất tham số nằm trong khoảng đó.*

## Tại sao P-values Vẫn Được Sử dụng Rộng rãi?

Bất chấp các hạn chế trên, p-value vẫn phổ biến vì bốn lý do chính: quán tính lịch sử và giảng dạy kéo dài nhiều thập kỷ; vẻ ngoài đơn giản khi gói gọn phân tích vào một con số và một ngưỡng quyết định; áp lực xuất bản khi nhiều tạp chí vẫn ưu tiên kết quả có $$p < 0.05$$; và việc nhiều nhà nghiên cứu chưa được đào tạo bài bản về các phương pháp thay thế như Bayesian. Dù vậy, xu hướng đang dần thay đổi khi nhiều hiệp hội thống kê và tạp chí khoa học lớn đã lên tiếng cảnh báo việc lạm dụng p-value.

### Thử nghiệm: khoảng tin cậy và khoảng đáng tin

Lặp thí nghiệm nhiều lần để thấy ý nghĩa tần suất của “95%”.

<div class="interactive-demo" markdown="1">
<div data-demo="interval-explainer" data-lang="vi"></div>
</div>

## Phương pháp Bayesian: Một Cách Tiếp cận Tự nhiên hơn

Thay vì hỏi gián tiếp "dữ liệu này bất thường đến mức nào nếu $$H_0$$ đúng?", phương pháp Bayesian hỏi trực tiếp: "với dữ liệu quan sát được, niềm tin của ta về tham số nên phân bố ra sao?" Quy trình gồm ba bước:

1. **Thiết lập phân phối tiên nghiệm (prior)**: mã hóa hiểu biết ban đầu về tham số bằng phân phối $$P(\theta)$$.
2. **Cập nhật bằng dữ liệu qua định lý Bayes**: kết hợp prior với hàm hợp lý (likelihood) để thu được phân phối hậu nghiệm (posterior):

$$P(\theta \mid \text{dữ liệu}) = \frac{P(\text{dữ liệu} \mid \theta) \cdot P(\theta)}{P(\text{dữ liệu})}$$

3. **Diễn giải trực tiếp phân phối hậu nghiệm**: đọc ngay xác suất của các vùng giá trị tham số dựa trên dữ liệu đã quan sát.

Ví dụ, thay vì phát biểu "bác bỏ giả thuyết hiệu quả thuốc bằng 0 với $$p = 0.03$$", ta có thể nói trực tiếp: "với dữ liệu này, có 95% xác suất hậu nghiệm rằng hiệu quả giảm huyết áp của thuốc nằm trong khoảng từ 2 đến 8 mmHg". Ngoài ra, khung Bayesian còn cho phép tính xác suất giữa các giả thuyết, kết hợp thông tin từ nhiều nghiên cứu, và đưa ra phân phối dự đoán cho dữ liệu mới.

## Khi nào Nên Sử dụng P-values?

Dù có nhiều giới hạn, p-value vẫn hữu ích trong một số trường hợp: làm công cụ sàng lọc nhanh để phát hiện tín hiệu đáng xem xét thêm, kiểm tra sơ bộ độ phù hợp mô hình, hoặc hỗ trợ một số bài toán ra quyết định nhị phân có quy trình rõ ràng (như kiểm soát chất lượng). Ngay cả khi đó, p-value cần đi kèm kích thước hiệu ứng và khoảng tin cậy.

## Hướng dẫn Thực hành

Khi sử dụng hoặc đọc p-value, không nên báo cáo p-value đơn lẻ mà luôn kèm kích thước hiệu ứng, khoảng tin cậy và cỡ mẫu; tránh biến ngưỡng $$\alpha$$ thành ranh giới nhị phân cứng nhắc; luôn nhớ p-value là $$P(\text{dữ liệu} \mid H_0)$$ chứ không phải $$P(H_0 \mid \text{dữ liệu})$$; và luôn đặt kết quả trong bối cảnh thực tiễn cùng chất lượng thiết kế nghiên cứu. Với nhiều câu hỏi ước lượng và ra quyết định, tiếp cận Bayesian sẽ rõ ràng và phù hợp hơn.

## Ý nghĩa cho Phân tích Dữ liệu Bayesian

Hiểu rõ kiểm định giả thuyết tần suất là nền tảng giúp bạn đánh giá đúng vai trò của thống kê Bayesian. Phương pháp Bayesian chuyển trọng tâm từ kiểm định nhị phân sang ước lượng tham số và dự đoán, cho phép diễn giải trực tiếp xác suất của tham số, không phụ thuộc ngưỡng cắt tùy ý và tích hợp minh bạch thông tin tiên nghiệm. Tất nhiên, thống kê Bayesian không phải lời giải vạn năng — nó có những thách thức riêng về tính toán và lựa chọn prior — nhưng đem lại một khung suy luận nhất quán cho rất nhiều bài toán thực tế.

## Giải thích: Tại sao $$p = 0.04$$ KHÔNG có nghĩa "96% giả thuyết là đúng"?

Đây là nguồn gốc lớn nhất của khủng hoảng tái lập khoa học. Hãy đi chậm qua 4 bước để tự chứng minh bằng số học đơn giản:

1. **Tách biệt hai xác suất điều kiện:** $$p	ext{-value}$$ gắn với $$P(	ext{kết quả đáng kể} \mid H_0)$$, còn điều ta muốn biết là $$P(H_0 \mid 	ext{kết quả đáng kể})$$.
2. **Đưa vào tỷ lệ nền (Base Rate):** Trong một lĩnh vực nghiên cứu thăm dò, giả sử chỉ có 10% giả thuyết thử nghiệm là thực sự có hiệu ứng ($$P(H_1) = 0.10$$, $$P(H_0) = 0.90$$).
3. **Đưa vào ngưỡng $$lpha$$ và lực kiểm định (Power):** Với chuẩn $$lpha = 0.05$$ và lực kiểm định phổ biến $$1 - eta = 0.80$$, ta tính số phát hiện thật và phát hiện giả trên 1.000 thí nghiệm.
4. **Tính xác suất hậu nghiệm bị báo động giả (False Discovery Rate):** Lấy số dương tính giả chia cho tổng số kết quả đạt $$p < 0.05$$.

### Ví dụ tính toán làm từng bước: 1.000 thí nghiệm đạt chuẩn $$p < 0.05$$

Xét 1.000 giả thuyết được kiểm định với $$lpha = 0.05$$, lực kiểm định $$1 - eta = 0.80$$, và tỷ lệ giả thuyết đúng thực sự là $$10\%$$:

| Thực tế | Số thí nghiệm | Đạt $$p < 0.05$$ (Bác bỏ $$H_0$$) | Không đạt $$p < 0.05$$ |
| --- | --- | --- | --- |
| $$H_1$$ đúng (có hiệu ứng thật) | $$100$$ | $$100 	imes 0.80 = 80$$ (dương tính thật) | $$20$$ (âm tính giả) |
| $$H_0$$ đúng (không có hiệu ứng) | $$900$$ | $$900 	imes 0.05 = 45$$ (dương tính giả) | $$855$$ (âm tính thật) |
| **Tổng cộng** | **$$1\,000$$** | **$$80 + 45 = 125$$** | **$$875$$** |

Nhìn vào cột "Đạt $$p < 0.05$$": trong 125 kết quả "có ý nghĩa thống kê", có tới **45 kết quả hoàn toàn là nhiễu ngẫu nhiên**:
$$P(H_0 \mid p < 0.05) = rac{45}{125} = 0.36 \quad (36\%!).$$
Dù chuẩn $$lpha$$ là $$5\%$$, xác suất một phát hiện có $$p < 0.05$$ là **giả mạo** lại lên tới **36%** — cao gấp 7 lần con số 5%!

**Hiểu lầm cần tránh:** Cho rằng $$p > 0.05$$ chứng minh $$H_0$$ đúng (không có hiệu ứng). Với cỡ mẫu nhỏ, $$p > 0.05$$ thường chỉ nói lên rằng *dữ liệu chưa đủ mạnh để kết luận*.

**Kiểm tra nhanh:** Nếu tỷ lệ nền của giả thuyết đúng tăng từ $$10\%$$ lên $$50\%$$ (nhờ nghiên cứu có cơ sở lý thuyết vững), số dương tính thật là $$500 	imes 0.80 = 400$$, dương tính giả là $$500 	imes 0.05 = 25$$, lúc này tỷ lệ giả mạo giảm mạnh còn $$25 / 425 pprox 5.9\%$$. Prior thực sự quyết định chất lượng suy luận!

---

## Video tham khảo

- [p-values: What they are and how to interpret them](https://www.youtube.com/watch?v=vemZtEM63GY) — StatQuest with Josh Starmer, English. **Xem trước.** Giải thích rõ định nghĩa p-value như xác suất của dữ liệu cực đoan dưới giả thuyết không.
- [Hypothesis Testing and The Null Hypothesis, Clearly Explained!!!](https://www.youtube.com/watch?v=0oc49DyA3hU) — StatQuest with Josh Starmer, English. Trình bày vai trò của giả thuyết không và quy trình kiểm định tần suất.
- [Confidence Intervals, Clearly Explained!!!](https://www.youtube.com/watch?v=TqOeMYtOc1w) — StatQuest with Josh Starmer, English. Minh họa cách dựng khoảng tin cậy qua lấy mẫu lặp lại để đối chiếu với khoảng credible Bayesian.

## Bài tập

**Bài tập 1: Diễn giải P-value.** Một nghiên cứu so sánh hai phương pháp giảng dạy và báo cáo "$$p = 0.04$$". Hãy viết: (a) một diễn giải đúng về p-value này, (b) một diễn giải sai phổ biến, và (c) giải thích vì sao cách hiểu sai đó không hợp lệ và gây hậu quả gì.

**Bài tập 2: Kích thước Mẫu và P-value.** Giả sử chiều cao trung bình của nam giới ở quần thể A là 175.0 cm và ở quần thể B là 175.5 cm (chênh lệch rất nhỏ), với độ lệch chuẩn ở cả hai quần thể là 7 cm. (a) Dựa vào kiểm định t hai mẫu, ước lượng cỡ mẫu cần thiết để thu được $$p < 0.05$$. (b) Thảo luận xem "ý nghĩa thống kê" có đồng nghĩa với "ý nghĩa thực tiễn" hay không.

![Tính toán Kích thước Mẫu]({{ site.baseurl }}/img/chapter_img/chapter00/sample_size_calculation.png)

*Hình minh họa: Đường cong thể hiện mối quan hệ giữa kích thước hiệu ứng và cỡ mẫu cần thiết ở mức power = 0.80, $$\alpha = 0.05$$. Để phát hiện hiệu ứng nhỏ (0.5 cm) cần hơn 1,500 người mỗi nhóm, trong khi hiệu ứng lớn (2.0 cm) chỉ cần khoảng 100 người mỗi nhóm.*

**Bài tập 3: Kiểm định bội và P-hacking.** Một nhà nghiên cứu kiểm tra riêng rẽ 20 biến khác nhau xem có tương quan với biến kết quả hay không, mỗi kiểm định dùng mức $$\alpha = 0.05$$. (a) Nếu thực tế không biến nào có tương quan và các kiểm định độc lập, xác suất tìm thấy ít nhất một kết quả "có ý nghĩa thống kê" là bao nhiêu? (b) Đây là ví dụ của vấn đề gì? (c) Đề xuất hai biện pháp khắc phục.

**Bài tập 4: So sánh Khoảng Tin cậy và Khoảng Credible.** Giả sử bạn đọc hai báo cáo: (a) "Khoảng tin cậy 95% cho hiệu quả thuốc là [2, 8] mmHg" (tần suất), và (b) "Khoảng credible 95% cho hiệu quả thuốc là [2, 8] mmHg" (Bayesian). Hãy viết diễn giải chuẩn xác cho từng báo cáo và giải thích khoảng nào trả lời trực tiếp hơn câu hỏi của bác sĩ.

**Bài tập 5: Nghiên cứu Trường hợp.** Tìm một bài báo khoa học trong lĩnh vực bạn quan tâm có sử dụng p-value. (a) Tác giả có diễn giải p-value chính xác không? (b) Bài báo có trình bày kích thước hiệu ứng và khoảng tin cậy không? (c) Nếu làm phản biện, bạn sẽ đề xuất cải thiện phân tích thống kê ra sao? (d) Phương pháp Bayesian có phù hợp hơn cho câu hỏi nghiên cứu đó không và vì sao?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 4: Asymptotics and connections to non-Bayesian approaches
- Chapter 6: Model checking

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 11: Null Hypothesis Significance Testing
- Chapter 12: Bayesian Approaches to Testing a Point ("Null") Hypothesis

### Critical Papers on P-values:

**Wasserstein, R. L., & Lazar, N. A. (2016).** The ASA's statement on p-values: context, process, and purpose. *The American Statistician*, 70(2), 129-133.

**Ioannidis, J. P. (2005).** Why most published research findings are false. *PLoS Medicine*, 2(8), e124.

**Nuzzo, R. (2014).** Scientific method: statistical errors. *Nature*, 506(7487), 150-152.

### Supplementary Reading:

**McShane, B. B., Gal, D., Gelman, A., Robert, C., & Tackett, J. L. (2019).** Abandon statistical significance. *The American Statistician*, 73(sup1), 235-245.

**Greenland, S., Senn, S. J., Rothman, K. J., Carlin, J. B., Poole, C., Goodman, S. N., & Altman, D. G. (2016).** Statistical tests, P values, confidence intervals, and power: a guide to misinterpretations. *European Journal of Epidemiology*, 31(4), 337-350.

---

*Bài học tiếp theo: [0.12 T-test và Phân phối T]({{ site.baseurl }}/contents/vi/chapter00/00_09_t_test_and_t_distribution/)*
