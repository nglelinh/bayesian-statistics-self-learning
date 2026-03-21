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

Mỗi ngày, ta vẫn làm một việc rất Bayesian:

- ban đầu tin một điều gì đó ở mức vừa phải,
- thấy thêm thông tin mới,
- rồi điều chỉnh niềm tin.

Ví dụ:

- nghe dự báo thời tiết rồi cập nhật kế hoạch,
- xem kết quả xét nghiệm rồi cập nhật chẩn đoán,
- nhìn doanh số tuần đầu rồi cập nhật niềm tin về nhu cầu thị trường.

Định lý Bayes chỉ làm cho quá trình này trở thành một quy tắc toán học rõ ràng.

## 2. Một ví dụ dễ hiểu: bác sĩ chẩn đoán bệnh

Giả sử bác sĩ đang cân nhắc ba khả năng:

- cúm,
- COVID-19,
- viêm phổi vi khuẩn.

Trước khi xem kỹ các triệu chứng cụ thể của bệnh nhân, bác sĩ đã có một niềm tin ban đầu dựa trên:

- mùa đang lưu hành bệnh nào,
- dịch tễ khu vực,
- kinh nghiệm trước đó.

Đó là **prior**.

Sau đó, bác sĩ nhìn dữ liệu mới:

- sốt,
- ho,
- mất vị giác,
- hình ảnh X-quang,
- kết quả test.

Đó là phần dữ liệu đi vào **likelihood**.

Kết hợp hai phần này, bác sĩ có niềm tin cập nhật về chẩn đoán hợp lý nhất. Đó là **posterior**.

![Chẩn đoán y tế với Bayes]({{ site.baseurl }}/img/chapter_img/chapter01/doctor_diagnosis_bayes.png)

## 3. Công thức Bayes

Định lý Bayes viết như sau:

$$
P(\theta \mid D) = \frac{P(D \mid \theta)\,P(\theta)}{P(D)}.
$$

Ở đây:

- $$P(\theta \mid D)$$ là **posterior**,
- $$P(D \mid \theta)$$ là **likelihood**,
- $$P(\theta)$$ là **prior**,
- $$P(D)$$ là **evidence** hay hằng số chuẩn hóa.

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

Nếu một giả thuyết:

- đã có prior cao,
- và dữ liệu cũng hợp với nó,

thì posterior của nó sẽ cao.

Ngược lại, nếu:

- prior đã thấp,
- dữ liệu cũng không ủng hộ,

thì posterior sẽ thấp.

## 5. Ví dụ kinh điển: đồng xu thiên lệch

Giả sử ta muốn biết đồng xu có xác suất ra ngửa $$\theta$$ là bao nhiêu.

### Trước dữ liệu

Ta nghĩ đồng xu có thể gần cân bằng, nhưng chưa chắc. Đó là prior.

### Dữ liệu

Ta tung 10 lần và thấy 7 mặt ngửa.

### Cập nhật

Bayes kết hợp:

- prior ban đầu,
- với dữ liệu 7/10,

để tạo posterior về $$\theta$$.

![Bayes với ví dụ đồng xu]({{ site.baseurl }}/img/chapter_img/chapter01/coin_bayes_visualization.png)

Điều quan trọng là posterior không đơn thuần bằng:

- prior,
- cũng không chỉ bằng tỷ lệ quan sát 0.7.

Nó là sự dung hòa giữa:

- điều ta tin trước đó,
- và điều dữ liệu đang nói.

## 6. Prior, likelihood và posterior thật ra là gì?

### 6.1. Prior

Prior là điều ta tin trước dữ liệu hiện tại.

Ví dụ:

- tỷ lệ đậu môn học trước đây thường quanh 70%,
- một loại thuốc tương tự thường chỉ hiệu quả ở mức vừa phải,
- đồng xu mua từ cửa hàng thường gần cân bằng.

### 6.2. Likelihood

Likelihood đo dữ liệu hiện tại hợp với từng giá trị tham số đến đâu.

Ví dụ:

- nếu đồng xu thật sự cân bằng, dữ liệu 7/10 ngửa hợp lý đến mức nào?
- nếu tỷ lệ đậu thật sự là 0.9, dữ liệu hiện tại có còn hợp lý không?

### 6.3. Posterior

Posterior là niềm tin sau khi cập nhật.

Nó là đối tượng trung tâm của Bayesian inference vì từ posterior ta có thể trả lời:

- tham số có khả năng nằm ở đâu,
- xác suất nó lớn hơn một ngưỡng là bao nhiêu,
- khoảng hợp lý nhất của nó là gì.

![Minh họa Bayes theorem]({{ site.baseurl }}/img/chapter_img/chapter01/bayes_theorem_visualization.png)

## 7. Một ví dụ rất nổi tiếng: xét nghiệm y khoa

Đây là ví dụ giúp người học thấy Bayes mạnh ở đâu.

Giả sử:

- một bệnh hiếm, chỉ 1% dân số mắc,
- test có độ nhạy cao và độ đặc hiệu cao,
- một người nhận kết quả dương tính.

Câu hỏi người bệnh thật sự quan tâm là:

- “Vậy xác suất tôi thật sự mắc bệnh là bao nhiêu?”

Rất nhiều người nhầm tưởng kết quả dương tính gần như đồng nghĩa với chắc chắn mắc bệnh. Nhưng Bayes cho thấy:

- nếu bệnh rất hiếm,
- thì prior ban đầu rất thấp,
- nên ngay cả một xét nghiệm khá tốt cũng chưa chắc đẩy posterior lên mức cực cao.

![Nghịch lý xét nghiệm y khoa]({{ site.baseurl }}/img/chapter_img/chapter01/medical_test_paradox.png)

Đây là một trong những nơi Bayes cho câu trả lời tự nhiên hơn hẳn so với trực giác cảm tính.

### 7.1. Tính số cụ thể cho bài toán xét nghiệm bệnh hiếm (VD1)

Giả sử:

- $$P(D)=0.001$$ (tỷ lệ mắc bệnh ban đầu),
- $$P(+\mid D)=0.9$$ (độ nhạy),
- $$P(+\mid D')=0.01$$ (tỷ lệ dương tính giả).

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

Trong bài toán chẩn đoán nhị phân, confusion matrix giúp đọc đúng ý nghĩa các đại lượng:

- **True Positive (TP)**: có bệnh và test dương tính.
- **False Positive (FP)**: không bệnh nhưng test dương tính.
- **False Negative (FN)**: có bệnh nhưng test âm tính.
- **True Negative (TN)**: không bệnh và test âm tính.

Khi đó:

- **Độ nhạy** $$=P(+\mid D)=\frac{TP}{TP+FN}$$,
- **Độ đặc hiệu** $$=P(-\mid D')=\frac{TN}{TN+FP}$$,
- **Tỷ lệ dương tính giả** $$=P(+\mid D')=1-\text{độ đặc hiệu}$$.

Điều người bệnh quan tâm lại là $$P(D\mid +)$$, tức PPV. Đây là lý do phải dùng Bayes: từ các đại lượng theo hàng/cột của confusion matrix để suy ra xác suất hậu nghiệm thực sự cần cho quyết định.

### 7.3. Ví dụ điều kiện hóa theo ngữ cảnh (VD2)

Giả sử:

- $$P(\text{Icy})=0.7$$, $$P(\text{Not Icy})=0.3$$,
- $$P(\text{One crashes}\mid \text{Icy})=0.8$$,
- $$P(\text{One crashes}\mid \text{Not Icy})=0.1$$.

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

Bạn có thể nghĩ nó như:

- một hằng số chuẩn hóa để đảm bảo posterior là một phân phối xác suất hợp lệ.

Trong thực hành, ta thường nhớ:

$$
P(\theta \mid D) \propto P(D \mid \theta)P(\theta)
$$

và để việc chuẩn hóa cho bước sau.

## 9. Bayes không chỉ dùng một lần

Một nét đẹp lớn của Bayes là tính **cập nhật tuần tự**.

Ví dụ:

- hôm nay bạn có dữ liệu tuần 1,
- ngày mai thêm dữ liệu tuần 2,
- tuần sau có thêm dữ liệu tuần 3.

Bạn không cần suy nghĩ “làm lại từ đầu” theo kiểu hoàn toàn tách biệt. Posterior hiện tại có thể trở thành prior cho lần cập nhật kế tiếp.

![Cập nhật tuần tự trong Bayes]({{ site.baseurl }}/img/chapter_img/chapter01/sequential_updating.png)

Điều này cực kỳ tự nhiên cho:

- dashboard kinh doanh,
- giám sát vận hành,
- và học tập liên tục từ dữ liệu đến theo thời gian.

### 9.1. Ví dụ cập nhật tuần tự với hai xét nghiệm (VD3)

Giả sử:

$$
P(\theta=1)=0.7,\quad P(\theta=0)=0.3,
$$

với $$\theta=1$$ nghĩa là có bệnh.

Xét nghiệm đầu tiên $$Y$$:

- $$P(Y=1\mid \theta=1)=0.95$$,
- $$P(Y=1\mid \theta=0)=0.40$$,

và quan sát được $$Y=1$$.

Khi đó:

$$
P(\theta=1\mid Y=1)=\frac{0.95\times 0.7}{0.95\times 0.7+0.40\times 0.3}
=\frac{0.665}{0.785}\approx 0.847.
$$

Tiếp theo, có xét nghiệm thứ hai $$W$$ độc lập có điều kiện theo $$\theta$$:

- $$P(W=1\mid \theta=1)=0.99 \Rightarrow P(W=0\mid \theta=1)=0.01,$$
- $$P(W=1\mid \theta=0)=0.04 \Rightarrow P(W=0\mid \theta=0)=0.96,$$

và quan sát được $$W=0$$.

Cập nhật lần 2:

$$
P(\theta=1\mid Y=1,W=0)=
\frac{P(W=0\mid \theta=1)P(\theta=1\mid Y=1)}{P(W=0\mid Y=1)}
\approx 0.052.
$$

Tức là posterior thay đổi mạnh theo bằng chứng mới: từ $$0.7 \to 0.847 \to 0.052$$.

## 10. Prior mạnh hay yếu thì sao?

Nếu prior rất mạnh, dữ liệu ít có thể chưa làm posterior thay đổi quá nhiều.

Nếu prior yếu, dữ liệu sẽ có ảnh hưởng lớn hơn.

Đây không phải lỗi của Bayes. Đó chính là điều ta muốn:

- khi kiến thức trước đó rất chắc, ta không nên vứt nó đi quá dễ dàng,
- khi prior mơ hồ, dữ liệu nên được nói mạnh hơn.

![So sánh prior mạnh và prior yếu]({{ site.baseurl }}/img/chapter_img/chapter01/prior_strength_comparison.png)

## 11. Điều Bayes thực sự dạy ta

Bayes không chỉ dạy một công thức. Nó dạy một cách suy nghĩ:

- không có dữ liệu nào tự nói nếu không có mô hình,
- niềm tin ban đầu không phải điều cấm kỵ,
- dữ liệu mới phải có quyền sửa niềm tin cũ,
- và toàn bộ quá trình đó cần được làm minh bạch.

Một khi chấp nhận điều này, bạn sẽ thấy prior và posterior không còn “lạ”, mà cực kỳ tự nhiên.

> **3 ý cần nhớ.**
> 1. Định lý Bayes là quy tắc cập nhật niềm tin khi có thêm bằng chứng mới.
> 2. Prior, likelihood và posterior không phải ba khái niệm rời nhau mà là ba phần của cùng một quy trình suy luận.
> 3. Sức mạnh của Bayes nằm ở chỗ nó cho phép ta kết hợp kiến thức cũ với dữ liệu mới một cách minh bạch.

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
