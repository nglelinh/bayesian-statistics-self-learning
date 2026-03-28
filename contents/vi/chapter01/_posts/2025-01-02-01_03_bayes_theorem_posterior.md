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

## Mục tiêu học tập

Sau bài này, bạn cần hiểu định lý Bayes như một quy tắc cập nhật niềm tin chứ không chỉ là một công thức thuộc lòng. Bạn phải đọc được vai trò của prior, likelihood và posterior trong một ví dụ thực tế, và biết vì sao Bayes trở nên tự nhiên trong các bài toán chẩn đoán, dự báo và học từ dữ liệu.

> **Ví dụ mini.** Một bác sĩ biết bệnh cúm đang phổ biến trong mùa này, nhưng khi bệnh nhân xuất hiện với bộ triệu chứng rất đặc trưng cho COVID-19, niềm tin ban đầu cần được cập nhật. Định lý Bayes chính là công cụ để làm việc đó một cách có nguyên tắc.
>
> **Câu hỏi tự kiểm tra.** Nếu prior là điều bạn tin trước dữ liệu, còn likelihood là mức độ dữ liệu phù hợp với từng giả thuyết, thì posterior nên được hiểu là gì?

## 1. Bayes bắt đầu từ một câu hỏi rất đời thường

Mỗi ngày, ta vẫn làm một việc rất Bayesian: ban đầu tin một điều gì đó ở mức vừa phải, sau đó thấy thêm thông tin mới, rồi điều chỉnh niềm tin. Điều này xuất hiện khi ta nghe dự báo thời tiết và cập nhật kế hoạch, khi xem kết quả xét nghiệm để cập nhật chẩn đoán, hay khi nhìn doanh số tuần đầu để điều chỉnh niềm tin về nhu cầu thị trường. Định lý Bayes chỉ biến quá trình tưởng như trực giác ấy thành một quy tắc toán học rõ ràng.

## 2. Một ví dụ dễ hiểu: bác sĩ chẩn đoán bệnh

Giả sử bác sĩ đang cân nhắc ba khả năng là cúm, COVID-19, và viêm phổi vi khuẩn. Trước khi xem kỹ các triệu chứng cụ thể của bệnh nhân, bác sĩ đã có một niềm tin ban đầu dựa trên mùa đang lưu hành bệnh nào, dịch tễ khu vực, và kinh nghiệm trước đó; đó chính là **prior**. Sau đó, bác sĩ nhìn vào dữ liệu mới như sốt, ho, mất vị giác, hình ảnh X-quang, hay kết quả test; đó là phần thông tin đi vào **likelihood**. Kết hợp hai phần này với nhau, bác sĩ có niềm tin cập nhật về chẩn đoán hợp lý nhất; đó là **posterior**.

![Triệu chứng ban đầu của bệnh nhân]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_symptoms.png)

![Prior chẩn đoán trước khi có bằng chứng mạnh]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_prior.png)

![Dữ liệu mới làm thay đổi mức độ hợp lý của từng giả thuyết]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_new_data.png)

![Posterior sau khi cập nhật bằng chứng]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_doctor_diagnosis_posterior.png)

## 3. Công thức Bayes

Định lý Bayes viết như sau:

$$
P(\theta \mid D) = \frac{P(D \mid \theta)\,P(\theta)}{P(D)}.
$$

Ở đây, $$P(\theta \mid D)$$ là **posterior**, $$P(D \mid \theta)$$ là **likelihood**, $$P(\theta)$$ là **prior**, còn $$P(D)$$ là **evidence** hay hằng số chuẩn hóa.

Nếu chỉ cần nhìn cấu trúc, ta thường nhớ dạng ngắn:

$$
\text{posterior} \propto \text{likelihood} \times \text{prior}.
$$

### 3.1. Ôn nhanh xác suất có điều kiện và xác suất toàn phần

Trước khi dùng Bayes, ta cần hai mảnh ghép rất ngắn:

$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)}
$$

và

$$
P(B)=\sum_i P(B\mid A_i)P(A_i)
$$

trong đó $$\{A_i\}$$ là các trường hợp loại trừ nhau và phủ toàn bộ khả năng.

Với bài toán nhị phân (có bệnh/không bệnh), công thức toàn phần thường viết:

$$
P(B)=P(B\mid A)P(A)+P(B\mid A')P(A').
$$

Đây chính là mẫu số chuẩn hóa trong định lý Bayes.

## 4. Đọc công thức bằng lời

Đừng vội nhìn Bayes như một công thức đáng sợ. Hãy đọc nó bằng tiếng Việt đơn giản:

> Niềm tin mới của tôi về giả thuyết tỷ lệ với mức độ dữ liệu ủng hộ giả thuyết đó, nhân với mức độ tôi đã tin giả thuyết đó từ trước.

Đây là một ý cực kỳ tự nhiên.

Nếu một giả thuyết đã có prior cao và dữ liệu cũng hợp với nó, thì posterior của nó sẽ cao. Ngược lại, nếu prior đã thấp và dữ liệu cũng không ủng hộ, thì posterior sẽ thấp.

## 5. Ví dụ kinh điển: đồng xu thiên lệch

Giả sử ta muốn biết đồng xu có xác suất ra ngửa $$\theta$$ là bao nhiêu.

### Trước dữ liệu

Ta nghĩ đồng xu có thể gần cân bằng, nhưng chưa chắc; đó là prior.

### Dữ liệu

Ta tung 10 lần và thấy 7 mặt ngửa.

### Cập nhật

Bayes kết hợp prior ban đầu với dữ liệu 7/10 để tạo posterior về $$\theta$$.

![Bayes với ví dụ đồng xu]({{ site.baseurl }}/img/chapter_img/chapter01/coin_bayes_visualization.png)

Điều quan trọng là posterior không đơn thuần bằng prior, cũng không chỉ bằng tỷ lệ quan sát 0.7. Nó là sự dung hòa giữa điều ta tin trước đó và điều dữ liệu đang nói.

## 6. Prior, likelihood và posterior thật ra là gì?

### 6.1. Prior

Prior là điều ta tin trước dữ liệu hiện tại. Chẳng hạn, ta có thể biết rằng tỷ lệ đậu môn học trước đây thường quanh 70%, một loại thuốc tương tự thường chỉ hiệu quả ở mức vừa phải, hay đồng xu mua từ cửa hàng thường gần cân bằng.

### 6.2. Likelihood

Likelihood đo dữ liệu hiện tại hợp với từng giá trị tham số đến đâu. Ví dụ, nếu đồng xu thật sự cân bằng thì dữ liệu 7/10 ngửa hợp lý đến mức nào, hay nếu tỷ lệ đậu thật sự là 0.9 thì dữ liệu hiện tại có còn hợp lý không.

### 6.3. Posterior

Posterior là niềm tin sau khi cập nhật. Nó là đối tượng trung tâm của Bayesian inference vì từ posterior ta có thể trả lời tham số có khả năng nằm ở đâu, xác suất nó lớn hơn một ngưỡng là bao nhiêu, hay khoảng giá trị hợp lý nhất của nó là gì.

![Prior trước khi nhìn dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_prior.png)

![Likelihood cho biết dữ liệu ủng hộ giá trị nào của tham số]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_likelihood.png)

![Posterior sau khi cập nhật bằng dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_posterior.png)

![So sánh prior và posterior để thấy dữ liệu đã kéo niềm tin đi đâu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayes_theorem_prior_vs_posterior.png)

## 7. Một ví dụ rất nổi tiếng: xét nghiệm y khoa

Đây là ví dụ giúp người học thấy Bayes mạnh ở đâu.

Giả sử có một bệnh hiếm mà chỉ 1% dân số mắc, test có độ nhạy cao và độ đặc hiệu cao, và một người nhận kết quả dương tính. Câu hỏi người bệnh thật sự quan tâm là: “Vậy xác suất tôi thật sự mắc bệnh là bao nhiêu?”

Rất nhiều người nhầm tưởng kết quả dương tính gần như đồng nghĩa với chắc chắn mắc bệnh. Nhưng Bayes cho thấy rằng nếu bệnh rất hiếm thì prior ban đầu rất thấp, nên ngay cả một xét nghiệm khá tốt cũng chưa chắc đẩy posterior lên mức cực cao.

![Nghịch lý xét nghiệm y khoa]({{ site.baseurl }}/img/chapter_img/chapter01/medical_test_paradox.png)

Đây là một trong những nơi Bayes cho câu trả lời tự nhiên hơn hẳn so với trực giác cảm tính.

### 7.1. Tính số cụ thể cho bài toán xét nghiệm bệnh hiếm (VD1)

Giả sử $$P(D)=0.001$$ là tỷ lệ mắc bệnh ban đầu, $$P(+\mid D)=0.9$$ là độ nhạy, và $$P(+\mid D')=0.01$$ là tỷ lệ dương tính giả.

Ta cần:

$$
P(D\mid +)=\frac{P(+\mid D)P(D)}{P(+)}.
$$

Với xác suất toàn phần:

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

Dù test khá tốt, posterior vẫn chỉ khoảng $$8.26\%$$ vì bệnh quá hiếm (base rate thấp).

### 7.2. Đọc bài toán qua ma trận nhầm lẫn

Trong bài toán chẩn đoán nhị phân, **confusion matrix** giúp đọc đúng ý nghĩa các đại lượng: **True Positive (TP)** là có bệnh và test dương tính, **False Positive (FP)** là không bệnh nhưng test dương tính, **False Negative (FN)** là có bệnh nhưng test âm tính, còn **True Negative (TN)** là không bệnh và test âm tính. Khi đó, độ nhạy là $$P(+\mid D)=\frac{TP}{TP+FN}$$, độ đặc hiệu là $$P(-\mid D')=\frac{TN}{TN+FP}$$, và tỷ lệ dương tính giả là $$P(+\mid D')=1-\text{độ đặc hiệu}$$.

Điều người bệnh quan tâm lại là $$P(D\mid +)$$, tức PPV. Đây là lý do phải dùng Bayes: từ các đại lượng theo hàng/cột của confusion matrix để suy ra xác suất hậu nghiệm thực sự cần cho quyết định.

### 7.3. Ví dụ điều kiện hóa theo ngữ cảnh (VD2)

Giả sử $$P(\text{Icy})=0.7$$ và $$P(\text{Not Icy})=0.3$$, đồng thời $$P(\text{One crashes}\mid \text{Icy})=0.8$$ còn $$P(\text{One crashes}\mid \text{Not Icy})=0.1$$.

Đầu tiên, dùng xác suất toàn phần:

$$
P(\text{One crashes})=0.8\times 0.7+0.1\times 0.3=0.59.
$$

Giả sử đã quan sát thấy Watson bị tai nạn. Khi đó:

$$
P(\text{Icy}\mid \text{Watson crashes})=\frac{0.8\times 0.7}{0.59}\approx 0.95.
$$

Xác suất Holmes bị tai nạn sau khi biết Watson bị tai nạn:

$$
P(\text{Holmes crashes}\mid \text{Watson crashes})=0.8\times 0.95+0.1\times 0.05=0.765.
$$

Điểm quan trọng: ta cập nhật niềm tin về điều kiện môi trường (đường băng), rồi suy ra xác suất sự kiện quan tâm.

## 8. Evidence có vai trò gì?

Trong công thức:

$$
P(D)
$$

là xác suất quan sát dữ liệu dưới mọi giá trị có thể của tham số.

Bạn có thể nghĩ evidence như một hằng số chuẩn hóa để bảo đảm posterior là một phân phối xác suất hợp lệ.

Trong thực hành, ta thường nhớ:

$$
P(\theta \mid D) \propto P(D \mid \theta)P(\theta)
$$

và để việc chuẩn hóa cho bước sau.

## 9. Bayes không chỉ dùng một lần

Một nét đẹp lớn của Bayes là tính **cập nhật tuần tự**.

Ví dụ, hôm nay bạn có dữ liệu tuần 1, ngày mai thêm dữ liệu tuần 2, rồi tuần sau có thêm dữ liệu tuần 3. Bạn không cần suy nghĩ “làm lại từ đầu” theo kiểu hoàn toàn tách biệt; posterior hiện tại có thể trở thành prior cho lần cập nhật kế tiếp.

![Bước khởi đầu: prior ban đầu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_prior.png)

![Sau đợt dữ liệu đầu tiên]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_step1.png)

![Sau đợt dữ liệu thứ hai]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_step2.png)

![So sánh cập nhật tuần tự với cập nhật một lần]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_sequential_updating_batch_comparison.png)

Điều này cực kỳ tự nhiên cho dashboard kinh doanh, giám sát vận hành, và mọi tình huống học tập liên tục từ dữ liệu đến theo thời gian.

### 9.1. Ví dụ cập nhật tuần tự với hai xét nghiệm (VD3)

Giả sử:

$$
P(\theta=1)=0.7,\quad P(\theta=0)=0.3,
$$

với $$\theta=1$$ nghĩa là có bệnh.

Xét nghiệm đầu tiên $$Y$$ thỏa $$P(Y=1\mid \theta=1)=0.95$$ và $$P(Y=1\mid \theta=0)=0.40$$, và ta quan sát được $$Y=1$$.

Khi đó:

$$
P(\theta=1\mid Y=1)=\frac{0.95\times 0.7}{0.95\times 0.7+0.40\times 0.3}
=\frac{0.665}{0.785}\approx 0.847.
$$

Tiếp theo, có xét nghiệm thứ hai $$W$$ độc lập có điều kiện theo $$\theta$$, với $$P(W=1\mid \theta=1)=0.99$$ nên $$P(W=0\mid \theta=1)=0.01$$, còn $$P(W=1\mid \theta=0)=0.04$$ nên $$P(W=0\mid \theta=0)=0.96$$, và ta quan sát được $$W=0$$.

Cập nhật lần 2:

$$
P(\theta=1\mid Y=1,W=0)=
\frac{P(W=0\mid \theta=1)P(\theta=1\mid Y=1)}{P(W=0\mid Y=1)}
\approx 0.052.
$$

Tức là posterior thay đổi mạnh theo bằng chứng mới: từ $$0.7 \to 0.847 \to 0.052$$.

## 10. Prior mạnh hay yếu thì sao?

Nếu prior rất mạnh, dữ liệu ít có thể chưa làm posterior thay đổi quá nhiều. Nếu prior yếu, dữ liệu sẽ có ảnh hưởng lớn hơn. Đây không phải lỗi của Bayes mà chính là điều ta mong muốn: khi kiến thức trước đó rất chắc, ta không nên vứt nó đi quá dễ dàng; còn khi prior mơ hồ, dữ liệu nên được nói mạnh hơn.

### 10.1. Một ví dụ cụ thể: cùng dữ liệu, prior khác nhau

Giả sử ta quan sát 6 ca dương tính trong 10 trường hợp.

- Nếu prior yếu là Beta$$(1,1)$$, posterior sẽ là Beta$$(7,5)$$ với posterior mean khoảng $$0.583$$.
- Nếu prior mạnh hơn và nghiêng sẵn về tỷ lệ cao, chẳng hạn Beta$$(20,5)$$, posterior sẽ là Beta$$(26,9)$$ với posterior mean khoảng $$0.743$$.

Cùng một dữ liệu nhưng posterior khác nhau vì prior mang thông tin thật sự vào bài toán. Đây không phải “Bayes tùy hứng”, mà là cách Bayes nói rõ một điều vốn luôn tồn tại trong thực tế: dữ liệu mới luôn được đọc trong bối cảnh của những gì ta đã biết từ trước.

![Prior yếu: niềm tin ban đầu còn khá mở]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_weak_prior.png)

![Prior mạnh: niềm tin ban đầu tập trung hơn nhiều]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_strong_prior.png)

![Khi prior yếu, posterior bị dữ liệu kéo mạnh hơn]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_weak_posterior.png)

![Khi prior mạnh, posterior thay đổi ít hơn]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_prior_strength_strong_posterior.png)

## 11. Điều Bayes thực sự dạy ta

Bayes không chỉ dạy một công thức. Nó dạy một cách suy nghĩ, trong đó dữ liệu không tự nói nếu không có mô hình, niềm tin ban đầu không phải điều cấm kỵ, dữ liệu mới phải có quyền sửa niềm tin cũ, và toàn bộ quá trình cập nhật đó cần được trình bày minh bạch.

Một khi chấp nhận điều này, bạn sẽ thấy prior và posterior không còn “lạ”, mà cực kỳ tự nhiên.

> **3 ý cần nhớ.** Định lý Bayes là quy tắc cập nhật niềm tin khi có thêm bằng chứng mới; prior, likelihood và posterior không phải ba khái niệm rời nhau mà là ba phần của cùng một quy trình suy luận; và sức mạnh của Bayes nằm ở chỗ nó cho phép ta kết hợp kiến thức cũ với dữ liệu mới một cách minh bạch.

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

*Bài học tiếp theo: [1.4 Bayesian vs Frequentist - So Sánh và Lựa Chọn](/vi/chapter01/bayesian-vs-frequentist/)*
