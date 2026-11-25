---
layout: post
title: "Bài 1.3: Định lý Bayes - Công cụ Cập nhật Niềm tin"
chapter: '01'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

Năm 1763 — hai năm sau khi mục sư Thomas Bayes qua đời — người bạn thân Richard Price tìm thấy trong di cảo của ông một bản thảo ngắn về bài toán "xác suất ngược": biết kết quả quan sát được trên bàn bi-a, làm sao suy ngược lại vị trí ban đầu của quả bóng ẩn? Bản thảo ấy, cùng công trình độc lập và tổng quát hơn của Pierre-Simon Laplace năm 1774, đã đặt nền móng cho phương trình nổi tiếng nhất của thống kê hiện đại: **Định lý Bayes**.

Điều kỳ diệu của công thức Bayes nằm ở sự cân bằng hoàn hảo: nó biến trực giác học hỏi từ kinh nghiệm thành một phép nhân tường minh giữa *kiến thức ban đầu* (prior) và *bằng chứng dữ liệu* (likelihood), rồi chuẩn hóa bằng *bằng chứng toàn phần* (evidence).

---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu định lý Bayes như một quy tắc cập nhật niềm tin chứ không chỉ là một công thức học thuộc. Bạn cần phân biệt rõ vai trò của prior, likelihood và posterior trong các ví dụ thực tế, đồng thời thấy vì sao định lý Bayes phù hợp với các bài toán chẩn đoán, dự báo và học từ dữ liệu.

> **Ví dụ mini.** Một bác sĩ biết bệnh cúm đang phổ biến trong mùa này, nhưng khi bệnh nhân xuất hiện với bộ triệu chứng đặc trưng cho COVID-19, niềm tin ban đầu cần được điều chỉnh. Định lý Bayes là công cụ thực hiện bước cập nhật đó một cách có nguyên tắc.
>
> **Câu hỏi tự kiểm tra.** Nếu prior là điều bạn tin trước khi thấy dữ liệu, còn likelihood là mức độ dữ liệu phù hợp với từng giả thuyết, thì posterior nên được hiểu là gì?


## Kiến thức cần nhớ: Bốn thành phần của Định lý Bayes và Cơ chế cập nhật tuần tự

Để làm chủ hoàn toàn công thức $$P(\theta \mid y) = \frac{P(y \mid \theta)P(\theta)}{P(y)}$$, hãy nhìn rõ ba trụ cột cấu thành nó:

- **Bốn thành phần giải phẫu (Prior, Likelihood, Evidence, Posterior):** Prior $$P(\theta)$$ mã hóa niềm tin trước dữ liệu; Likelihood $$P(y \mid \theta)$$ đo mức độ tương thích của dữ liệu dưới từng giả thuyết $$\theta$$; Evidence $$P(y) = \sum_\theta P(y \mid \theta)P(\theta)$$ là hằng số chuẩn hóa; và Posterior $$P(\theta \mid y)$$ là niềm tin sau khi tổng hợp cả hai.
- **Dạng tỷ số khả dĩ (Odds Form & Bayes Factor):** Viết dưới dạng tỷ lệ giữa hai giả thuyết: $$\frac{P(H_1 \mid y)}{P(H_0 \mid y)} = \frac{P(y \mid H_1)}{P(y \mid H_0)} \times \frac{P(H_1)}{P(H_0)}$$. Tỷ số ở giữa chính là **hệ số Bayes (Bayes Factor)** — đo trực tiếp sức mạnh bằng chứng của dữ liệu mà không cần tính mẫu số $$P(y)$$.
- **Tính nhất quán của cập nhật tuần tự (Sequential Updating):** Posterior sau quan sát thứ nhất trở thành Prior cho quan sát thứ hai, và kết quả cuối cùng hoàn toàn giống hệt như khi gộp tất cả dữ liệu cập nhật một lần.

---

## 1. Bayes bắt đầu từ một câu hỏi rất quen thuộc

Hằng ngày, chúng ta đều thực hiện một quá trình suy luận gần với Bayes: ban đầu giữ một niềm tin ở mức độ nhất định, sau đó tiếp nhận thông tin mới rồi điều chỉnh lại niềm tin ấy. Quá trình này xuất hiện khi ta nghe dự báo thời tiết để điều chỉnh kế hoạch, xem kết quả xét nghiệm để cập nhật chẩn đoán, hay theo dõi doanh số tuần đầu để điều chỉnh nhận định về nhu cầu thị trường. Định lý Bayes chuyển hóa quá trình trực giác đó thành một quy tắc toán học rõ ràng.

## 2. Ví dụ minh họa: bác sĩ chẩn đoán bệnh

Giả sử bác sĩ đang cân nhắc ba khả năng: cúm, COVID-19 và viêm phổi vi khuẩn. Trước khi xem xét kỹ triệu chứng của bệnh nhân, bác sĩ đã có niềm tin ban đầu dựa trên mùa dịch, tình hình dịch tễ tại khu vực và kinh nghiệm lâm sàng; đó là **prior**. Tiếp theo, bác sĩ thu thập dữ liệu mới như sốt, ho, mất vị giác, phim X-quang hay kết quả xét nghiệm; phần thông tin này đi vào **likelihood**. Khi kết hợp hai thành phần đó lại, bác sĩ thu được niềm tin đã cập nhật về chẩn đoán hợp lý nhất; đó chính là **posterior**.

![Triệu chứng ban đầu của bệnh nhân]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_symptoms.png)

![Prior chẩn đoán trước khi có bằng chứng mạnh]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_prior.png)

![Dữ liệu mới làm thay đổi mức độ hợp lý của từng giả thuyết]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_new_data.png)

![Posterior sau khi cập nhật bằng chứng]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_posterior.png)

## 3. Công thức Bayes

Định lý Bayes được viết như sau:

$$
P(\theta \mid D) = \frac{P(D \mid \theta)\,P(\theta)}{P(D)}.
$$

Trong đó, $$P(\theta \mid D)$$ là **posterior** (hậu nghiệm), $$P(D \mid \theta)$$ là **likelihood** (hàm hợp lý), $$P(\theta)$$ là **prior** (tiền nghiệm), còn $$P(D)$$ là **evidence** (bằng chứng) hay hằng số chuẩn hóa. Khi chỉ cần tập trung vào cấu trúc tỉ lệ, ta thường viết gọn:

$$
\text{posterior} \propto \text{likelihood} \times \text{prior}.
$$

### 3.1. Ôn nhanh xác suất có điều kiện và xác suất toàn phần

Trước khi áp dụng định lý Bayes, ta cần hai công thức cơ bản:

$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)}
$$

và

$$
P(B)=\sum_i P(B\mid A_i)P(A_i),
$$

trong đó $$\{A_i\}$$ là hệ các biến cố xung khắc đôi một và phủ toàn bộ không gian mẫu. Với bài toán nhị phân (có bệnh / không bệnh), công thức xác suất toàn phần có dạng:

$$
P(B)=P(B\mid A)P(A)+P(B\mid A')P(A').
$$

Đây chính là mẫu số chuẩn hóa trong định lý Bayes.

## 4. Đọc công thức bằng lời

Thay vì xem định lý Bayes là một biểu thức khó nhớ, bạn có thể diễn đạt nó bằng lời như sau:

> Niềm tin mới về một giả thuyết tỉ lệ với mức độ dữ liệu ủng hộ giả thuyết đó nhân với mức độ tin cậy ban đầu dành cho giả thuyết đó.

Cách đọc này rất trực quan: nếu một giả thuyết có prior cao và dữ liệu cũng phù hợp với nó thì posterior sẽ cao; ngược lại, nếu prior thấp và dữ liệu không ủng hộ thì posterior sẽ thấp.

## 5. Ví dụ kinh điển: đồng xu thiên lệch

Giả sử ta muốn suy luận xác suất ra mặt ngửa $$\theta$$ của một đồng xu.

### Trước khi có dữ liệu

Ta cho rằng đồng xu có thể gần cân bằng nhưng chưa chắc chắn; niềm tin này được biểu diễn bằng prior.

### Dữ liệu quan sát

Ta tung 10 lần và thu được 7 mặt ngửa.

### Cập nhật

Định lý Bayes kết hợp prior ban đầu với dữ liệu 7/10 để tạo ra phân phối posterior cho $$\theta$$.

![Bayes với ví dụ đồng xu]({{ site.baseurl }}/img/chapter_img/chapter01/coin_bayes_visualization.png)

Điểm cần chú ý là posterior không giữ nguyên ở prior, nhưng cũng không nhảy thẳng về tỷ lệ mẫu 0.7; nó là sự dung hòa giữa kiến thức ban đầu và dữ liệu vừa quan sát.

## 6. Vai trò của prior, likelihood và posterior

### 6.1. Prior

Prior biểu diễn niềm tin trước khi có dữ liệu hiện tại. Chẳng hạn, ta biết tỷ lệ qua môn các khóa trước thường quanh 70%, một loại thuốc tương tự thường có hiệu quả ở mức vừa phải, hay đồng xu mua từ cửa hàng thường gần cân bằng.

### 6.2. Likelihood

Likelihood đo mức độ phù hợp của dữ liệu hiện tại với từng giá trị tham số. Ví dụ, nếu đồng xu thực sự cân bằng thì dữ liệu 7/10 mặt ngửa hợp lý đến mức nào, hoặc nếu tỷ lệ qua môn thực sự là 0.9 thì dữ liệu quan sát có còn phù hợp không.

### 6.3. Posterior

Posterior là niềm tin sau khi đã cập nhật bằng dữ liệu. Đây là đối tượng trung tâm của suy luận Bayes, vì từ posterior ta có thể xác định vùng giá trị khả dĩ của tham số, tính xác suất tham số vượt qua một ngưỡng cụ thể, hoặc tìm khoảng giá trị hợp lý nhất của nó.

![Prior trước khi nhìn dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_prior.png)

![Likelihood cho biết dữ liệu ủng hộ giá trị nào của tham số]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_likelihood.png)

![Posterior sau khi cập nhật bằng dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_posterior.png)

![So sánh prior và posterior để thấy dữ liệu đã kéo niềm tin đi đâu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_prior_vs_posterior.png)

### Thử nghiệm: đếm người thay vì nhân xác suất

Kéo tỉ lệ nền, độ nhạy và độ đặc hiệu; bấm Bước tiếp để xem 1000 người tách thành bệnh/khỏe, dương/âm tính và vì sao kết quả dương tính chưa chắc là bệnh.

<div class="interactive-demo" markdown="1">
<div data-demo="bayesrule-explainer" data-lang="vi" data-tab="tree"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 7. Ví dụ kinh điển: xét nghiệm y khoa

Đây là ví dụ minh họa rõ sức mạnh của định lý Bayes. Giả sử một căn bệnh hiếm chỉ ảnh hưởng đến 1% dân số, xét nghiệm có độ nhạy và độ đặc hiệu đều cao, và một người nhận kết quả dương tính. Câu hỏi người bệnh thực sự quan tâm là: “Xác suất tôi thực sự mắc bệnh là bao nhiêu?”

Nhiều người dễ nhầm rằng kết quả dương tính gần như đồng nghĩa với chắc chắn mắc bệnh. Tuy nhiên, định lý Bayes cho thấy khi bệnh rất hiếm (prior thấp), ngay cả một xét nghiệm có độ chính xác khá cao cũng chưa chắc đẩy xác suất hậu nghiệm lên mức cao. Trong những tình huống như vậy, Bayes cho kết quả chính xác hơn hẳn trực giác cảm tính.

![Nghịch lý xét nghiệm y khoa]({{ site.baseurl }}/img/chapter_img/chapter01/medical_test_paradox.png)

### 7.1. Tính số cụ thể cho bài toán xét nghiệm bệnh hiếm (VD1)

Giả sử tỷ lệ mắc bệnh ban đầu là $$P(D)=0.001$$, độ nhạy là $$P(+\mid D)=0.9$$, và tỷ lệ dương tính giả là $$P(+\mid D')=0.01$$. Ta cần tính:

$$
P(D\mid +)=\frac{P(+\mid D)P(D)}{P(+)}.
$$

Áp dụng công thức xác suất toàn phần:

$$
P(+)=P(+\mid D)P(D)+P(+\mid D')P(D')
$$

$$
=0.9\times 0.001+0.01\times 0.999=0.01089.
$$

Suy ra:

$$
P(D\mid +)=\frac{0.9\times 0.001}{0.01089}\approx 0.0826.
$$

Dù xét nghiệm khá tốt, xác suất hậu nghiệm vẫn chỉ khoảng $$8.26\%$$ do tỷ lệ nền (base rate) của bệnh rất thấp.

### 7.2. Đọc bài toán qua ma trận nhầm lẫn

Trong chẩn đoán nhị phân, **ma trận nhầm lẫn (confusion matrix)** giúp phân biệt rõ các đại lượng: **True Positive (TP)** là có bệnh và xét nghiệm dương tính, **False Positive (FP)** là không bệnh nhưng xét nghiệm dương tính, **False Negative (FN)** là có bệnh nhưng xét nghiệm âm tính, còn **True Negative (TN)** là không bệnh và xét nghiệm âm tính. Khi đó, độ nhạy là $$P(+\mid D)=\frac{TP}{TP+FN}$$, độ đặc hiệu là $$P(-\mid D')=\frac{TN}{TN+FP}$$, và tỷ lệ dương tính giả là $$P(+\mid D')=1-\text{độ đặc hiệu}$$.

Điều người bệnh quan tâm lại là $$P(D\mid +)$$, tức giá trị tiên đoán dương (PPV). Định lý Bayes giúp chuyển từ các xác suất điều kiện theo hàng/cột của ma trận nhầm lẫn sang xác suất hậu nghiệm cần thiết cho quyết định lâm sàng.

### 7.3. Ví dụ điều kiện hóa theo ngữ cảnh (VD2)

Giả sử $$P(\text{Icy})=0.7$$ và $$P(\text{Not Icy})=0.3$$, đồng thời $$P(\text{One crashes}\mid \text{Icy})=0.8$$ còn $$P(\text{One crashes}\mid \text{Not Icy})=0.1$$.

Trước hết, áp dụng công thức xác suất toàn phần:

$$
P(\text{One crashes})=0.8\times 0.7+0.1\times 0.3=0.59.
$$

Nếu quan sát thấy Watson bị tai nạn, ta cập nhật xác suất đường đóng băng:

$$
P(\text{Icy}\mid \text{Watson crashes})=\frac{0.8\times 0.7}{0.59}\approx 0.95.
$$

Từ đó, xác suất Holmes cũng bị tai nạn sau khi biết tin về Watson là:

$$
P(\text{Holmes crashes}\mid \text{Watson crashes})=0.8\times 0.95+0.1\times 0.05=0.765.
$$

Điểm cốt lõi của ví dụ này là ta cập nhật niềm tin về điều kiện môi trường (đường có đóng băng hay không), rồi dùng niềm tin mới đó để suy ra xác suất của sự kiện tiếp theo.

## 8. Vai trò của evidence

Trong công thức Bayes, đại lượng:

$$
P(D)
$$

là xác suất quan sát được dữ liệu tính trên mọi giá trị có thể của tham số. Bạn có thể xem evidence như hằng số chuẩn hóa giúp đảm bảo posterior là một phân phối xác suất hợp lệ (có tổng hoặc tích phân bằng 1). Trong thực hành, ta thường làm việc trước với dạng tỉ lệ:

$$
P(\theta \mid D) \propto P(D \mid \theta)P(\theta)
$$

và thực hiện bước chuẩn hóa ở công đoạn sau.

## 9. Cập nhật tuần tự trong Bayes

Một tính chất quan trọng của thống kê Bayes là khả năng **cập nhật tuần tự**. Giả sử hôm nay bạn có dữ liệu tuần 1, tuần sau có thêm dữ liệu tuần 2, rồi tuần tiếp theo có thêm dữ liệu tuần 3. Bạn không cần bắt đầu lại từ đầu một cách tách biệt; posterior ở bước hiện tại có thể trở thành prior cho lần cập nhật kế tiếp. Tính chất này đặc biệt phù hợp với bảng điều khiển kinh doanh, giám sát vận hành và mọi bài toán cần học liên tục từ dữ liệu đến theo thời gian.

![Bước khởi đầu: prior ban đầu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_prior.png)

![Sau đợt dữ liệu đầu tiên]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_step1.png)

![Sau đợt dữ liệu thứ hai]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_step2.png)

![So sánh cập nhật tuần tự với cập nhật một lần]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_batch_comparison.png)

### 9.1. Ví dụ cập nhật tuần tự với hai xét nghiệm (VD3)

Giả sử:

$$
P(\theta=1)=0.7,\quad P(\theta=0)=0.3,
$$

trong đó $$\theta=1$$ biểu thị trạng thái có bệnh. Xét nghiệm thứ nhất $$Y$$ thỏa mãn $$P(Y=1\mid \theta=1)=0.95$$ và $$P(Y=1\mid \theta=0)=0.40$$, và ta quan sát được $$Y=1$$. Khi đó:

$$
P(\theta=1\mid Y=1)=\frac{0.95\times 0.7}{0.95\times 0.7+0.40\times 0.3}
=\frac{0.665}{0.785}\approx 0.847.
$$

Tiếp theo, xét nghiệm thứ hai $$W$$ độc lập có điều kiện theo $$\theta$$, với $$P(W=1\mid \theta=1)=0.99$$ (nên $$P(W=0\mid \theta=1)=0.01$$) và $$P(W=1\mid \theta=0)=0.04$$ (nên $$P(W=0\mid \theta=0)=0.96$$), và ta quan sát được $$W=0$$. Cập nhật lần thứ hai:

$$
P(\theta=1\mid Y=1,W=0)=
\frac{P(W=0\mid \theta=1)P(\theta=1\mid Y=1)}{P(W=0\mid Y=1)}
\approx 0.055.
$$

Như vậy, xác suất hậu nghiệm thay đổi rõ rệt theo từng bằng chứng mới: từ $$0.7 \to 0.847 \to 0.055$$.

### Thử nghiệm: cập nhật tuần tự qua từng lần tung

Ba loại đồng xu, mỗi lần tung nhân prior với likelihood rồi chuẩn hóa; đổi prior để thấy dữ liệu dần áp đảo.

<div class="interactive-demo" markdown="1">
<div data-demo="bayesrule-explainer" data-lang="vi" data-tab="sequential"></div>
</div>

## 10. Ảnh hưởng của prior mạnh và prior yếu

Nếu prior rất mạnh, một lượng dữ liệu ít có thể chưa làm posterior dịch chuyển nhiều. Ngược lại, nếu prior yếu, dữ liệu sẽ tác động mạnh hơn đến posterior. Đây không phải hạn chế của Bayes mà là hành vi hợp lý: khi kiến thức nền đã vững chắc, ta không nên từ bỏ nó quá dễ dàng trước vài quan sát lẻ tẻ; còn khi kiến thức ban đầu mơ hồ, dữ liệu mới cần có tiếng nói lớn hơn.

### 10.1. Ví dụ cụ thể: cùng dữ liệu, prior khác nhau

Giả sử ta quan sát 6 ca dương tính trong 10 trường hợp:

- Nếu dùng prior yếu Beta$$(1,1)$$, posterior là Beta$$(7,5)$$ với trung bình hậu nghiệm khoảng $$0.583$$.
- Nếu dùng prior mạnh hơn nghiêng về tỷ lệ cao, chẳng hạn Beta$$(20,5)$$, posterior là Beta$$(26,9)$$ với trung bình hậu nghiệm khoảng $$0.743$$.

Cùng một bộ dữ liệu nhưng posterior khác nhau vì prior đưa thông tin thực sự vào bài toán. Điều này phản ánh đúng thực tế: dữ liệu mới luôn được diễn giải trong bối cảnh của những gì ta đã biết từ trước.

![Prior yếu: niềm tin ban đầu còn khá mở]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_weak_prior.png)

![Prior mạnh: niềm tin ban đầu tập trung hơn nhiều]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_strong_prior.png)

![Khi prior yếu, posterior bị dữ liệu kéo mạnh hơn]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_weak_posterior.png)

![Khi prior mạnh, posterior thay đổi ít hơn]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_strong_posterior.png)

## 11. Tư duy cốt lõi của định lý Bayes

Định lý Bayes không chỉ cung cấp một công thức tính xác suất có điều kiện, mà đề xuất một cách suy luận minh bạch: dữ liệu không tự mang ý nghĩa nếu tách khỏi mô hình, kiến thức ban đầu không phải điều cấm kỵ, dữ liệu mới có quyền điều chỉnh niềm tin cũ, và toàn bộ quá trình cập nhật đều được trình bày rõ ràng. Khi nắm được tinh thần đó, các khái niệm prior và posterior sẽ trở nên tự nhiên.

> **3 ý cần nhớ.** Định lý Bayes là quy tắc cập nhật niềm tin khi có thêm bằng chứng mới; prior, likelihood và posterior không phải ba khái niệm tách rời mà là ba mắt xích của cùng một quy trình suy luận; và giá trị của Bayes nằm ở việc kết hợp kiến thức sẵn có với dữ liệu mới một cách minh bạch.


## Giải thích: Tính hậu nghiệm bằng bảng Bayes 4 cột và kiểm chứng cập nhật tuần tự

Thay vì cố nhẩm mẫu số $$P(y)$$ ngay từ đầu, cách làm ít sai nhất khi tính tay là lập **bảng Bayes 4 cột**:

1. **Cột 1 (Giả thuyết $$\theta$$):** Liệt kê đầy đủ các giả thuyết xung khắc.
2. **Cột 2 (Prior $$P(\theta)$$):** Ghi xác suất ban đầu (tổng bằng 1).
3. **Cột 3 (Likelihood $$P(y \mid \theta)$$):** Tính xác suất quan sát đúng dữ liệu $$y$$ dưới từng giả thuyết.
4. **Cột 4 (Tích chưa chuẩn hóa & Chuẩn hóa):** Nhân Cột 2 với Cột 3, cộng tổng để thu $$P(y)$$, rồi chia từng dòng cho tổng đó để ra Posterior.

### Ví dụ tính toán làm từng bước: Phân biệt đồng xu công bằng và đồng xu thiên lệch

Trong túi có 2 đồng xu: $$H_0$$ công bằng ($$p = 0.5$$) với prior $$0.7$$, và $$H_1$$ thiên lệch ($$p = 0.8$$) với prior $$0.3$$. Ta chọn ngẫu nhiên một đồng xu, tung 2 lần độc lập và cả 2 lần đều ra Ngửa ($$y = \text{NN}$$).

| Giả thuyết | Prior $$P(H)$$ | Likelihood $$P(\text{NN} \vert H)$$ | Tích $$P(H)P(\text{NN} \vert H)$$ | Posterior $$P(H \vert \text{NN})$$ |
| --- | --- | --- | --- | --- |
| $$H_0\; (p=0.5)$$ | $$0.70$$ | $$0.5^2 = 0.25$$ | $$0.1750$$ | $$0.1750 / 0.3670 \approx 0.4768$$ |
| $$H_1\; (p=0.8)$$ | $$0.30$$ | $$0.8^2 = 0.64$$ | $$0.1920$$ | $$0.1920 / 0.3670 \approx 0.5232$$ |
| **Tổng** | **$$1.00$$** | — | **$$P(\text{NN}) = 0.3670$$** | **$$1.0000$$** |

Chỉ sau 2 lần ra Ngửa liên tiếp, niềm tin vào đồng xu thiên lệch đã tăng từ $$30\%$$ lên $$52.32\%$$.

**Hiểu lầm cần tránh:** Cộng tổng cột Likelihood rồi thắc mắc vì sao $$0.25 + 0.64 = 0.89 \neq 1$$. Likelihood là hàm theo tham số với dữ liệu cố định, nên **không** nhất thiết có tổng bằng 1.

**Kiểm tra nhanh (Cập nhật tuần tự):** Nếu tách thành từng lần tung: sau lần 1 ra Ngửa, $$P(H_1 \mid \text{N}) = \frac{0.3 \times 0.8}{0.7 \times 0.5 + 0.3 \times 0.8} = \frac{0.24}{0.59} \approx 0.4068$$. Dùng $$0.4068$$ làm prior cho lần 2 ra Ngửa: $$P(H_1 \mid \text{NN}) = \frac{0.4068 \times 0.8}{0.5932 \times 0.5 + 0.4068 \times 0.8} = \frac{0.3254}{0.6220} \approx 0.5232$$ — khớp chính xác tuyệt đối!

---

## Video tham khảo

- [P01.007 — Định lý Bayes cập nhật niềm tin của mô hình ra sao?](https://www.youtube.com/watch?v=zXtcZ-2adK0) — Phạm Thông, Tiếng Việt. **xem trước**. Giải thích bằng tiếng Việt cách prior và dữ liệu cùng cập nhật niềm tin, phù hợp với cách tiếp cận của bài học.
- [Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM) — 3Blue1Brown, English. Minh họa trực quan vai trò của prior, likelihood và hằng số chuẩn hóa trên hình học.
- [Statistical Rethinking 2023 - 02 - The Garden of Forking Data](https://www.youtube.com/watch?v=R1vcdhPBlXA) — Richard McElreath, English. Trình bày ví dụ quả địa cầu nước và đất, nơi định lý Bayes trở thành bài toán đếm các khả năng sinh dữ liệu.

## Câu hỏi tự luyện

1. Trong ví dụ bác sĩ chẩn đoán bệnh, prior đến từ đâu và likelihood đến từ đâu?
2. Vì sao kết quả dương tính của một xét nghiệm chưa chắc đồng nghĩa với xác suất mắc bệnh rất cao?
3. Hãy nêu một ví dụ trong công việc của bạn nơi posterior hôm nay có thể trở thành prior ngày mai.
4. Vì sao posterior không nhất thiết trùng với tỷ lệ quan sát trực tiếp từ dữ liệu?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 5.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 1-2.

---

*Bài học tiếp theo: [1.4 Bayesian vs Frequentist - So Sánh và Lựa Chọn]({{ site.baseurl }}/contents/vi/chapter01/01_04_bayesian_vs_frequentist/)*
