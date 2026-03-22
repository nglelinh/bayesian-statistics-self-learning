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

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu sắc về **p-values** và kiểm định giả thuyết theo quan điểm tần suất (**frequentist**), không chỉ để áp dụng chúng một cách đúng đắn, mà quan trọng hơn là để nhận ra những hạn chế cơ bản của chúng. Bạn sẽ hiểu tại sao **p-values** thường bị hiểu sai, tại sao chúng không trả lời những câu hỏi mà nhà khoa học thực sự quan tâm, và tại sao **phương pháp Bayesian cung cấp một cách tiếp cận tự nhiên và mạch lạc hơn cho suy diễn thống kê**. Bài học này không phải để bạn từ bỏ hoàn toàn kiểm định giả thuyết, mà để bạn sử dụng nó một cách có phê phán và biết khi nào nên tìm kiếm các phương pháp thay thế.

## Giới thiệu: Tại sao chúng ta cần nói về P-values?

Trong khóa học về phân tích dữ liệu Bayesian, tại sao chúng ta lại dành thời gian để thảo luận về p-values và kiểm định giả thuyết theo quan điểm tần suất? Câu trả lời có ba lý do quan trọng.

1. Thứ nhất, p-values và kiểm định giả thuyết vẫn là công cụ thống kê được sử dụng rộng rãi nhất trong nghiên cứu khoa học hiện đại. Cho dù bạn làm việc trong y học, tâm lý học, kinh tế học, hay bất kỳ lĩnh vực nào khác, bạn sẽ gặp p-values trong hầu hết các bài báo khoa học mà bạn đọc. Để có thể đọc và đánh giá nghiên cứu một cách phê phán, bạn cần hiểu p-values thực sự có nghĩa là gì.

2. Thứ hai, p-values là một trong những khái niệm thống kê bị hiểu sai nhiều nhất, ngay cả trong cộng đồng nghiên cứu. Nhiều nhà khoa học sử dụng p-values hàng ngày nhưng không thực sự hiểu chúng đo lường điều gì. Việc hiểu đúng về p-values sẽ giúp bạn tránh những sai lầm phổ biến và nguy hiểm này.

3. Thứ ba, và quan trọng nhất, việc hiểu rõ những hạn chế của p-values sẽ giúp bạn đánh giá cao sức mạnh và sự tự nhiên của phương pháp Bayesian. Khi bạn thấy rõ những gì p-values không thể cho bạn biết, bạn sẽ hiểu tại sao phương pháp Bayesian lại cung cấp một cách tiếp cận tốt hơn cho nhiều câu hỏi nghiên cứu.

Bài học này sẽ xây dựng một sự hiểu biết sâu sắc về p-values, không phải để bạn trở thành người ủng hộ chúng, mà để bạn có thể sử dụng chúng một cách có trách nhiệm và biết khi nào nên vượt qua chúng.

## Khung Kiểm định Giả thuyết: Một Cách Tiếp cận Gián tiếp

Kiểm định giả thuyết theo quan điểm tần suất dựa trên một logic gián tiếp có phần phản trực giác. Thay vì trực tiếp đánh giá bằng chứng cho giả thuyết mà chúng ta quan tâm, chúng ta xây dựng một **giả thuyết không** (null hypothesis), thường ký hiệu là $$H_0$$, đại diện cho trạng thái "không có hiệu ứng" hoặc "không có sự khác biệt", và sau đó cố gắng tìm bằng chứng chống lại nó.

Ví dụ, giả sử chúng ta muốn biết liệu một loại thuốc mới có hiệu quả trong việc giảm huyết áp hay không. Thay vì trực tiếp hỏi "Thuốc này có hiệu quả không?" hoặc "Hiệu quả của thuốc là bao nhiêu?", khung kiểm định giả thuyết yêu cầu chúng ta thiết lập:

**Giả thuyết không** $$H_0$$ nói rằng thuốc không có hiệu quả, tức sự thay đổi trung bình trong huyết áp bằng 0, trong khi **giả thuyết thay thế** $$H_1$$ nói rằng thuốc có hiệu quả, tức sự thay đổi trung bình đó khác 0.

Logic của kiểm định giả thuyết là: **nếu dữ liệu quan sát được sẽ rất bất thường nếu $$H_0$$ đúng, thì chúng ta có bằng chứng chống lại $$H_0$$ và có thể "bác bỏ" nó**. Đây là một hình thức suy luận bằng phản chứng (proof by contradiction), tương tự như trong toán học, nhưng với một điểm khác biệt quan trọng: **trong thống kê, chúng ta không bao giờ có thể chứng minh điều gì một cách chắc chắn, chỉ có thể nói về mức độ bất thường của dữ liệu**.

Cách tiếp cận gián tiếp này có nguồn gốc lịch sử từ công trình của Ronald Fisher, Jerzy Neyman, và Egon Pearson vào đầu thế kỷ 20. Nó được thiết kế để cung cấp một quy trình khách quan cho việc đưa ra quyết định dựa trên dữ liệu. Tuy nhiên, như chúng ta sẽ thấy, tính khách quan này đi kèm với một cái giá đắt.

## P-value: Định nghĩa Chính xác

P-value là khái niệm trung tâm của kiểm định giả thuyết, nhưng cũng là một trong những khái niệm bị hiểu sai nhiều nhất trong thống kê. Hãy bắt đầu với định nghĩa chính xác:

**P-value là xác suất quan sát được dữ liệu ít nhất bất thường như dữ liệu thực tế (hoặc bất thường hơn), với điều kiện giả thuyết không là đúng.**

Hình thức hóa, nếu $$T$$ là một **thống kê kiểm định** (test statistic) được tính từ dữ liệu, và $$t_{obs}$$ là giá trị quan sát được của nó, thì:

$$p = P(T \geq t_{obs} \mid H_0)$$

(đối với kiểm định một phía, hoặc công thức tương tự cho kiểm định hai phía)

Hãy phân tích cẩn thận định nghĩa này, vì mỗi phần đều quan trọng:

1. **"Xác suất"**: P-value là một xác suất, nằm giữa 0 và 1.

2. **"Quan sát được dữ liệu ít nhất bất thường như..."**: Chúng ta không chỉ tính xác suất của dữ liệu chính xác mà chúng ta quan sát, mà là xác suất của dữ liệu này cộng với tất cả các kết quả "cực đoan hơn" theo một hướng nhất định.

3. **"Với điều kiện giả thuyết không là đúng"**: Đây là phần quan trọng nhất và thường bị bỏ qua. P-value **không** cho bạn biết xác suất giả thuyết không đúng. Nó cho bạn biết xác suất của dữ liệu **nếu** giả thuyết không đúng.

Sự khác biệt giữa $$P(\text{dữ liệu} \mid H_0)$$ và $$P(H_0 \mid \text{dữ liệu})$$ là cơ bản. P-value cho bạn cái trước, nhưng những gì nhà khoa học thực sự muốn biết thường là cái sau. Đây chính là một trong những nguồn gốc chính của sự hiểu sai về p-values.

---

### Giải thích từng thành phần

#### (1) "Giả thuyết không là đúng" ($$H_0$$ đúng)

Điều kiện này cực kỳ quan trọng:

Ta luôn **giả sử trước** rằng $$H_0$$ đúng, rồi mới hỏi: nếu $$H_0$$ đúng thật, thì dữ liệu có dạng như thế này có hiếm không?

**Ví dụ:**

Nếu $$H_0$$ nói rằng thuốc không có tác dụng nhưng dữ liệu lại cho cảm giác thuốc có vẻ hiệu quả, thì p-value sẽ trả lời câu hỏi: nếu thuốc thật sự không có tác dụng, xác suất để vẫn quan sát được kết quả ít nhất cực đoan như thế này là bao nhiêu?

#### (2) "Dữ liệu bất thường" nghĩa là gì?

"Bất thường" không phải là cảm tính, mà được định nghĩa bằng:

"Bất thường" ở đây không phải là cảm giác chủ quan mà được định nghĩa thông qua **thống kê kiểm định** như z-score, t-statistic hay $$\chi^2$$, tức mức độ mà dữ liệu nằm xa kỳ vọng dưới $$H_0$$.

Ví dụ, trung bình mẫu có thể lệch xa trung bình dự kiến theo $$H_0$$, sai khác giữa hai nhóm có thể rất lớn, hoặc giá trị thống kê có thể rơi sâu vào phần đuôi của phân phối; càng xa tâm kỳ vọng, dữ liệu càng cực đoan và vì thế càng bị xem là bất thường.

#### (3) "Ít nhất bất thường như dữ liệu quan sát (hoặc bất thường hơn)"

Đây là phần hay bị bỏ sót nhưng rất quan trọng.

P-value **không chỉ** tính xác suất đúng bằng kết quả bạn thấy, mà tính:

> Xác suất của kết quả quan sát được **và tất cả kết quả còn cực đoan hơn**.

**Ví dụ (kiểm định hai phía):** giả sử ta quan sát được $$z = 2.1$$. Khi đó, p-value là $$P(\mid Z \mid \geq 2.1 \mid H_0 \text{ đúng})$$. Nói cách khác, ta không chỉ tính xác suất đúng bằng 2.1, mà còn tính cả những giá trị như 2.5, 3.0, và mọi giá trị còn cực đoan hơn ở cả hai phía.

---

### Những điều P-value KHÔNG nói

Đây là điểm rất hay bị hiểu sai: p-value không phải là xác suất giả thuyết không sai, không phải là xác suất kết quả "do ngẫu nhiên", và cũng không phải là thước đo trực tiếp của kích thước hiệu ứng.

**Ví dụ sai:**

> "P-value = 0.03 nghĩa là 97% khả năng $$H_0$$ sai" ❌

**Diễn giải đúng:**

> "Nếu $$H_0$$ đúng, thì xác suất quan sát được dữ liệu ít nhất cực đoan như thế này là 3%." ✅

---

### Diễn giải trực giác ngắn gọn

Một cách nói đơn giản nhưng đúng bản chất:

**P-value đo mức độ "khó tin" của dữ liệu, nếu ta tin rằng giả thuyết không là đúng.**

Nói gọn hơn, p nhỏ cho thấy dữ liệu khó xảy ra nếu $$H_0$$ đúng nên ta có lý do để nghi ngờ $$H_0$$ hơn, còn p lớn chỉ cho thấy dữ liệu không mâu thuẫn mạnh với $$H_0$$.
---

## Một Ví dụ Cụ thể: Kiểm định T

Hãy xem xét một ví dụ cụ thể để làm rõ các khái niệm. Giả sử chúng ta muốn kiểm tra liệu chiều cao trung bình của nam sinh viên tại một trường đại học có khác 170 cm hay không. Chúng ta đo chiều cao của 25 nam sinh viên được chọn ngẫu nhiên và tính được chiều cao trung bình mẫu là $$\bar{x} = 172.5$$ cm với độ lệch chuẩn mẫu $$s = 6.2$$ cm.

Chúng ta thiết lập $$H_0$$ rằng $$\mu = 170$$, tức chiều cao trung bình quần thể là 170 cm, còn $$H_1$$ rằng $$\mu \neq 170$$, tức chiều cao trung bình quần thể khác 170 cm.

Thống kê kiểm định t được tính bằng:

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}} = \frac{172.5 - 170}{6.2 / \sqrt{25}} = \frac{2.5}{1.24} \approx 2.02$$

Với $$n - 1 = 24$$ bậc tự do, chúng ta tra bảng phân phối t (hoặc sử dụng phần mềm) để tìm xác suất quan sát được giá trị $$\mid t \mid \geq 2.02$$ nếu $$H_0$$ đúng. Giả sử chúng ta tìm được $$p \approx 0.054$$.

![Minh họa P-value trong Kiểm định T]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_ttest_illustration.png)

Điều này có nghĩa là gì? Nó có nghĩa là **nếu** chiều cao trung bình quần thể thực sự là 170 cm, và chúng ta lặp lại thí nghiệm này nhiều lần (mỗi lần lấy 25 mẫu ngẫu nhiên), thì khoảng 5.4% số lần chúng ta sẽ quan sát được một giá trị t có độ lớn ít nhất bằng 2.02.

P-value này không cho biết xác suất $$H_0$$ đúng là 5.4%, cũng không cho biết xác suất $$H_1$$ đúng là 94.6%; nó cũng không nói trực tiếp kích thước hiệu ứng là bao nhiêu hay nghiên cứu có ý nghĩa thực tiễn đến mức nào.

## Ngưỡng Ý nghĩa và Quyết định: Quy ước $$\alpha = 0.05$$

Trong thực hành, p-values thường được so sánh với một **mức ý nghĩa** (significance level) được định trước, thường ký hiệu là $$\alpha$$. Quy ước phổ biến nhất là $$\alpha = 0.05$$, mặc dù các giá trị khác như 0.01 hoặc 0.10 cũng đôi khi được sử dụng.

#### Quy tắc quyết định đơn giản:

Theo quy ước truyền thống, nếu $$p < \alpha$$ thì ta bác bỏ $$H_0$$ và gọi kết quả là "có ý nghĩa thống kê"; còn nếu $$p \geq \alpha$$ thì ta không bác bỏ $$H_0$$ và nói rằng chưa có đủ bằng chứng thống kê để chống lại nó.

Trong ví dụ chiều cao của chúng ta, với $$p = 0.054$$ và $$\alpha = 0.05$$, chúng ta sẽ **không bác bỏ** $$H_0$$. Chúng ta sẽ kết luận rằng không có đủ bằng chứng để nói rằng chiều cao trung bình khác 170 cm.

Nhưng hãy dừng lại và suy nghĩ về điều này. Sự khác biệt giữa $$p = 0.054$$ và $$p = 0.049$$ là rất nhỏ, nhưng nó dẫn đến hai kết luận hoàn toàn khác nhau theo quy tắc này. Một kết quả được gọi là "có ý nghĩa thống kê" và kết quả kia "không có ý nghĩa thống kê", mặc dù bằng chứng trong dữ liệu gần như giống hệt nhau.

Hơn nữa, ngưỡng $$\alpha = 0.05$$ là hoàn toàn tùy ý. Ronald Fisher, người đề xuất nó, đã nói rõ ràng rằng đây chỉ là một hướng dẫn thô, không phải là một quy tắc cứng nhắc. Tuy nhiên, trong thực hành, nó đã trở thành một ngưỡng ma thuật mà các nhà nghiên cứu cảm thấy phải vượt qua để công bố kết quả của họ.

Việc dựa vào ngưỡng cứng nhắc này có nhiều hậu quả tiêu cực: nó khuyến khích "p-hacking", đẩy người nghiên cứu vào tư duy nhị phân kiểu "có hay không có hiệu ứng", và làm lu mờ những thông tin quan trọng hơn như kích thước hiệu ứng hay độ không chắc chắn của ước lượng.

## Những Hiểu lầm Phổ biến về P-values

P-values là một trong những khái niệm bị hiểu sai nhiều nhất trong khoa học. Hãy xem xét một số hiểu lầm phổ biến:

### Hiểu lầm 1: P-value là xác suất giả thuyết không đúng

**Sai:** "$$p = 0.03$$ có nghĩa là có 3% cơ hội giả thuyết không đúng."

**Đúng:** P-value là xác suất của dữ liệu (hoặc dữ liệu cực đoan hơn) **nếu** giả thuyết không đúng, không phải xác suất giả thuyết không đúng **cho** dữ liệu.

Sự khác biệt này là cơ bản. Để tính $$P(H_0 \mid \text{dữ liệu})$$, chúng ta cần định lý Bayes và một prior probability cho $$H_0$$, điều mà khung tần suất không cung cấp.

### Hiểu lầm 2: $$1 - p$$ là xác suất giả thuyết thay thế đúng

**Sai:** "Nếu $$p = 0.05$$, thì có 95% cơ hội giả thuyết thay thế đúng."

**Đúng:** P-value không cho bạn bất kỳ thông tin trực tiếp nào về xác suất của giả thuyết thay thế.

### Hiểu lầm 3: P-value nhỏ có nghĩa là hiệu ứng lớn

**Sai:** "$$p < 0.001$$ có nghĩa là hiệu ứng rất mạnh."

**Đúng:** P-value nhỏ chỉ có nghĩa là dữ liệu sẽ rất bất thường nếu $$H_0$$ đúng. Điều này có thể xảy ra do hiệu ứng lớn, nhưng cũng có thể xảy ra do kích thước mẫu lớn với hiệu ứng nhỏ.

Ví dụ, với mẫu đủ lớn, bạn có thể tìm thấy sự khác biệt "có ý nghĩa thống kê" giữa hai nhóm ngay cả khi sự khác biệt thực tế là rất nhỏ và không có ý nghĩa thực tiễn.

![So sánh Kích thước Hiệu ứng và Kích thước Mẫu]({{ site.baseurl }}/img/chapter_img/chapter00/effect_size_vs_sample_size.png)

Hình trên minh họa một điểm quan trọng: bên trái, với mẫu lớn (n=1000), một hiệu ứng rất nhỏ (chỉ 0.5 cm) có thể cho p-value "có ý nghĩa thống kê", trong khi bên phải, với mẫu nhỏ (n=20), ngay cả hiệu ứng lớn (5 cm) cũng có thể không đạt ngưỡng ý nghĩa thống kê.

### Hiểu lầm 4: P-value lớn chứng minh giả thuyết không đúng

**Sai:** "$$p = 0.80$$ có nghĩa là giả thuyết không đúng."

**Đúng:** P-value lớn chỉ có nghĩa là dữ liệu không bất thường nếu $$H_0$$ đúng. Điều này có thể xảy ra vì $$H_0$$ thực sự đúng, hoặc vì chúng ta không có đủ dữ liệu để phát hiện sự khác biệt.

"Không có bằng chứng về hiệu ứng" không giống với "bằng chứng về không có hiệu ứng".

### Hiểu lầm 5: P-value đo lường khả năng tái lập

**Sai:** "$$p = 0.05$$ có nghĩa là nếu tôi lặp lại nghiên cứu, tôi có 95% cơ hội tìm thấy kết quả tương tự."

**Đúng:** P-value không cho bạn biết gì về khả năng tái lập. Trên thực tế, nghiên cứu cho thấy nhiều kết quả với $$p$$ gần 0.05 không thể tái lập được.

![Các Hiểu lầm Phổ biến về P-values]({{ site.baseurl }}/img/chapter_img/chapter00/pvalue_misinterpretations.png)

Hình trên tóm tắt bốn hiểu lầm chính về p-values: (1) P-value không phải là xác suất của H₀, (2) P-value nhỏ không có nghĩa là hiệu ứng lớn, (3) P-value lớn không chứng minh H₀ đúng, và (4) ngưỡng α = 0.05 là hoàn toàn tùy ý.

## Vấn đề với Kiểm định Giả thuyết Không

Một vấn đề cơ bản với khung kiểm định giả thuyết là bản thân giả thuyết không thường không hợp lý. Trong nhiều tình huống thực tế, chúng ta biết trước rằng giả thuyết không chắc chắn là sai.

Ví dụ, xem xét giả thuyết không "thuốc A và thuốc B có hiệu quả hoàn toàn giống nhau". Trong thực tế, hai loại thuốc khác nhau gần như chắc chắn sẽ có một số khác biệt, dù nhỏ đến mức nào, trong hiệu quả của chúng. Với mẫu đủ lớn, chúng ta luôn có thể bác bỏ giả thuyết không này, nhưng điều đó không cho chúng ta biết điều gì hữu ích về việc liệu sự khác biệt có đủ lớn để quan trọng hay không.

Câu hỏi thực sự mà nhà khoa học quan tâm thường không phải là "Có hiệu ứng nào không?" mà là "Hiệu ứng lớn như thế nào?" và "Chúng ta có chắc chắn về ước lượng của mình đến mức nào?" Kiểm định giả thuyết không trả lời những câu hỏi này một cách trực tiếp.

![Vấn đề Multiple Testing]({{ site.baseurl }}/img/chapter_img/chapter00/multiple_testing_problem.png)

Hình trên minh họa vấn đề multiple testing (p-hacking): khi thực hiện 20 kiểm định độc lập với α = 0.05, ngay cả khi H₀ đúng cho tất cả các kiểm định (không có hiệu ứng thực sự), chúng ta vẫn kỳ vọng tìm thấy khoảng 1 kết quả "có ý nghĩa thống kê" do ngẫu nhiên. Đây là một trong những nguồn gốc chính của khủng hoảng tái lập trong khoa học.

## Khoảng Tin cậy: Một Cách Tiếp cận Tốt hơn?

Một phương pháp tần suất thay thế cho kiểm định giả thuyết là **khoảng tin cậy** (confidence intervals). Khoảng tin cậy 95% cho một tham số $$\theta$$ là một khoảng $$[L, U]$$ được xây dựng từ dữ liệu sao cho:

$$P(L \leq \theta \leq U) = 0.95$$

trong đó xác suất được tính trên tất cả các mẫu có thể (với $$\theta$$ cố định).

Khoảng tin cậy có vẻ hấp dẫn hơn p-values vì chúng cung cấp thông tin về kích thước hiệu ứng và độ không chắc chắn. Tuy nhiên, chúng vẫn có một vấn đề diễn giải cơ bản.

**Diễn giải đúng:** "Nếu chúng ta lặp lại thí nghiệm nhiều lần và tính khoảng tin cậy 95% mỗi lần, thì 95% các khoảng sẽ chứa giá trị thật của $$\theta$$."

**Diễn giải sai (nhưng phổ biến):** "Có 95% cơ hội giá trị thật của $$\theta$$ nằm trong khoảng này."

Sự khác biệt là tinh tế nhưng quan trọng. Trong khung tần suất, $$\theta$$ là một giá trị cố định (dù không biết), không phải một biến ngẫu nhiên, vì vậy không có ý nghĩa khi nói về "xác suất" của nó. Xác suất trong định nghĩa khoảng tin cậy là về các khoảng, không phải về tham số.

Tuy nhiên, những gì nhà khoa học thực sự muốn biết là diễn giải thứ hai: cho dữ liệu cụ thể này, khả năng tham số nằm trong khoảng này là bao nhiêu? Đây chính xác là những gì **khoảng tin cậy Bayesian** (credible intervals) cung cấp.

![So sánh Confidence Intervals và Credible Intervals]({{ site.baseurl }}/img/chapter_img/chapter00/confidence_vs_credible_intervals.png)

Hình trên minh họa sự khác biệt cơ bản giữa confidence intervals (tần suất) và credible intervals (Bayesian). Phần trên cho thấy 50 khoảng tin cậy 95% từ các thí nghiệm khác nhau - khoảng 95% trong số chúng chứa giá trị thật (đường xanh lá), nhưng chúng ta không thể nói về xác suất cho một khoảng cụ thể. Phần dưới cho thấy một khoảng credible 95% cho một thí nghiệm cụ thể - chúng ta có thể nói trực tiếp rằng "có 95% xác suất tham số nằm trong khoảng này".

## Tại sao P-values Vẫn Được Sử dụng Rộng rãi?

Với tất cả những vấn đề này, tại sao p-values và kiểm định giả thuyết vẫn chiếm ưu thế trong nghiên cứu khoa học? Lý do đầu tiên là lịch sử và quán tính học thuật: p-values đã được dạy và sử dụng suốt nhiều thập kỷ, nên việc thay đổi thực hành thống kê của cả cộng đồng khoa học diễn ra rất chậm. Lý do thứ hai là tính đơn giản bề ngoài của chúng: chỉ một con số và một quy tắc quyết định tưởng như rõ ràng, dù sự đơn giản đó thực ra che giấu nhiều vấn đề. Lý do thứ ba đến từ cơ chế xuất bản, vì nhiều tạp chí vẫn ưu tiên các kết quả "có ý nghĩa thống kê" với $$p < 0.05$$. Cuối cùng, rất nhiều nhà nghiên cứu chưa được đào tạo đầy đủ về các phương pháp thay thế như Bayesian hoặc các phương pháp thống kê hiện đại khác.

Tuy nhiên, có những dấu hiệu cho thấy điều này đang thay đổi. Nhiều tổ chức thống kê và tạp chí khoa học đã đưa ra các tuyên bố cảnh báo về việc lạm dụng p-values và khuyến khích các phương pháp thay thế.

## Phương pháp Bayesian: Một Cách Tiếp cận Tự nhiên hơn

Phương pháp Bayesian cung cấp một cách tiếp cận tự nhiên và trực tiếp hơn cho các câu hỏi mà kiểm định giả thuyết cố gắng trả lời. Thay vì hỏi "Dữ liệu này sẽ bất thường như thế nào nếu giả thuyết không đúng?", phương pháp Bayesian hỏi "Cho dữ liệu này, niềm tin của chúng ta về tham số nên là gì?"

Trong khung Bayesian:

1. **Chúng ta bắt đầu với một prior**: Trước khi thấy dữ liệu, chúng ta mã hóa niềm tin ban đầu của mình về tham số trong một phân phối prior $$P(\theta)$$.

2. **Chúng ta cập nhật với dữ liệu**: Sử dụng định lý Bayes, chúng ta kết hợp prior với likelihood của dữ liệu để có được phân phối posterior:

$$P(\theta \mid \text{dữ liệu}) = \frac{P(\text{dữ liệu} \mid \theta) \cdot P(\theta)}{P(\text{dữ liệu})}$$

3. **Chúng ta diễn giải posterior trực tiếp**: Phân phối posterior cho chúng ta biết trực tiếp về xác suất của các giá trị khác nhau của $$\theta$$ cho dữ liệu quan sát được.

Ví dụ, thay vì nói "chúng ta bác bỏ giả thuyết rằng hiệu quả thuốc là 0 với $$p = 0.03$$", chúng ta có thể nói "cho dữ liệu này, có 95% xác suất posterior rằng hiệu quả thuốc nằm giữa 2 và 8 mmHg". Câu sau trả lời trực tiếp câu hỏi mà nhà khoa học quan tâm.

Hơn nữa, phương pháp Bayesian cho phép ta tính xác suất của các giả thuyết khác nhau, kết hợp thông tin từ nhiều nghiên cứu một cách tự nhiên, đưa ra dự đoán cho dữ liệu tương lai, và định lượng độ không chắc chắn theo cách trực tiếp, dễ diễn giải hơn.

## Khi nào Nên Sử dụng P-values?

Mặc dù có nhiều hạn chế, p-values không phải lúc nào cũng vô dụng. Chúng vẫn có thể hữu ích như một công cụ sàng lọc nhanh để phát hiện những mẫu dữ liệu đáng được điều tra thêm, như một cách kiểm tra sơ bộ mức phù hợp của mô hình, hoặc trong những bối cảnh thật sự cần quyết định nhị phân rõ ràng, chẳng hạn một số bài toán kiểm soát chất lượng.

Tuy nhiên, ngay cả trong những trường hợp này, p-values nên được sử dụng với sự hiểu biết đầy đủ về hạn chế của chúng và nên được bổ sung bằng các thước đo khác như kích thước hiệu ứng và khoảng tin cậy.

## Hướng dẫn Thực hành

Nếu buộc phải sử dụng hoặc diễn giải p-values, bạn không nên chỉ báo cáo riêng p-value mà cần đi kèm kích thước hiệu ứng, khoảng tin cậy, và kích thước mẫu; cũng không nên dùng một ngưỡng cứng nhắc để biến việc suy luận thành quyết định nhị phân đơn giản. Điều quan trọng là luôn nhớ p-value là $$P(\text{dữ liệu} \mid H_0)$$ chứ không phải $$P(H_0 \mid \text{dữ liệu})$$, đồng thời phải đặt kết quả vào bối cảnh của kích thước hiệu ứng, ý nghĩa thực tiễn, và chất lượng thiết kế nghiên cứu. Trong nhiều câu hỏi, Bayesian hoặc các phương pháp dựa trên ước lượng sẽ là lựa chọn phù hợp hơn.

## Ý nghĩa cho Phân tích Dữ liệu Bayesian

Bài học này về p-values và kiểm định giả thuyết không chỉ là một bài tập học thuật. Nó cung cấp động lực quan trọng cho việc học phương pháp Bayesian.

Khi bạn tiến xa hơn trong khóa học này, bạn sẽ thấy rằng phương pháp Bayesian giải quyết nhiều vấn đề mà chúng ta đã thảo luận. Nó cho phép ta nói trực tiếp về xác suất của giả thuyết và tham số, cung cấp các ước lượng độ không chắc chắn dễ diễn giải hơn, không phụ thuộc vào những ngưỡng quyết định tùy ý, hỗ trợ việc kết hợp kiến thức trước đó một cách tự nhiên, và chuyển trọng tâm từ kiểm định đơn thuần sang ước lượng và dự đoán.

Tuy nhiên, phương pháp Bayesian không phải là một giải pháp ma thuật cho tất cả các vấn đề. Nó có những thách thức riêng của nó, đặc biệt là về mặt tính toán và việc lựa chọn prior. Nhưng đối với nhiều câu hỏi nghiên cứu, nó cung cấp một cách tiếp cận tự nhiên và mạch lạc hơn so với kiểm định giả thuyết truyền thống.

## Bài tập

**Bài tập 1: Diễn giải P-values.** Một nghiên cứu so sánh hai phương pháp giảng dạy và báo cáo "$$p = 0.04$$". Viết ba diễn giải: (a) một diễn giải đúng về ý nghĩa của p-value này, (b) một diễn giải sai phổ biến, và (c) giải thích tại sao diễn giải sai là sai và tại sao sự khác biệt quan trọng.

**Bài tập 2: Kích thước Mẫu và P-values.** Giả sử chiều cao trung bình của nam giới trong quần thể A là 175.0 cm và trong quần thể B là 175.5 cm (sự khác biệt rất nhỏ). Độ lệch chuẩn trong cả hai quần thể là 7 cm. (a) Sử dụng công thức kiểm định t cho hai mẫu, ước lượng kích thước mẫu cần thiết để có $$p < 0.05$$ khi so sánh hai quần thể này. (b) Thảo luận về ý nghĩa của kết quả này: liệu "ý nghĩa thống kê" có tương đương với "ý nghĩa thực tiễn" không?

![Tính toán Kích thước Mẫu]({{ site.baseurl }}/img/chapter_img/chapter00/sample_size_calculation.png)

Hình trên cho thấy mối quan hệ giữa kích thước hiệu ứng và kích thước mẫu cần thiết để phát hiện hiệu ứng đó với power = 0.80 và α = 0.05. Lưu ý rằng để phát hiện hiệu ứng nhỏ (0.5 cm), chúng ta cần mẫu rất lớn (hơn 1500 người mỗi nhóm), trong khi hiệu ứng lớn (2.0 cm) chỉ cần khoảng 100 người mỗi nhóm.

**Bài tập 3: P-hacking.** Một nhà nghiên cứu thu thập dữ liệu về 20 biến khác nhau và kiểm định xem mỗi biến có tương quan với một kết quả quan tâm hay không, sử dụng $$\alpha = 0.05$$ cho mỗi kiểm định. (a) Nếu thực tế không có biến nào tương quan với kết quả, xác suất tìm thấy ít nhất một kết quả "có ý nghĩa thống kê" là bao nhiêu? (b) Đây là một ví dụ của vấn đề gì? (c) Đề xuất hai cách để giải quyết vấn đề này.

**Bài tập 4: So sánh Khoảng Tin cậy và Credible Intervals.** Giả sử bạn đọc hai báo cáo: (a) "Khoảng tin cậy 95% cho hiệu quả thuốc là [2, 8] mmHg" (tần suất), và (b) "Khoảng credible 95% cho hiệu quả thuốc là [2, 8] mmHg" (Bayesian). Viết diễn giải chính xác cho mỗi khoảng. Khoảng nào trả lời trực tiếp hơn câu hỏi mà bác sĩ quan tâm? Tại sao?

**Bài tập 5: Nghiên cứu Trường hợp.** Tìm một bài báo khoa học trong lĩnh vực bạn quan tâm sử dụng p-values. (a) Tác giả có diễn giải p-values đúng không? (b) Họ có báo cáo kích thước hiệu ứng và khoảng tin cậy không? (c) Nếu bạn là người phản biện, bạn sẽ đề xuất những cải tiến gì cho phân tích thống kê? (d) Liệu phương pháp Bayesian có phù hợp hơn cho câu hỏi nghiên cứu này không? Tại sao?

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

*Bài học tiếp theo: [0.12 T-test và Phân phối T](/vi/chapter00/t-test-and-t-distribution/)*
