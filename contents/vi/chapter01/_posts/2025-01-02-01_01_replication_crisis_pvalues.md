---
layout: post
title: "Bài 1.1: Khủng hoảng Khoa học và Giới hạn của P-values"
chapter: '01'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu ba điều. Thứ nhất, vì sao nhiều nghiên cứu được công bố nhưng lại không tái lập được. Thứ hai, vì sao p-value thường bị hiểu sai và dễ bị lạm dụng. Thứ ba, vì sao những vấn đề đó khiến cộng đồng khoa học phải tìm tới những cách suy luận khác, trong đó có Bayesian statistics.

> **Ví dụ mini.** Một nghiên cứu báo cáo p-value < 0.05 cho thấy thuốc mới có hiệu quả, nhưng khi nhóm khác lặp lại đúng thiết kế thì không còn thấy hiệu quả nữa. Đây chính là kiểu tình huống làm nảy sinh khủng hoảng tái lập.
>
> **Câu hỏi tự kiểm tra.** Một p-value nhỏ có thực sự đồng nghĩa với việc giả thuyết nghiên cứu là đúng không?

## 1. Khủng hoảng tái lập là gì?

Trong khoa học, một kết quả đáng tin không chỉ cần “đẹp” trên một bài báo. Nó cần có khả năng **lặp lại được** khi nhóm khác làm lại thí nghiệm với quy trình tương tự.

Nhưng trong nhiều lĩnh vực như tâm lý học, y học tiền lâm sàng, hay khoa học xã hội, rất nhiều kết quả nổi bật đã không lặp lại được.

![Thống kê khủng hoảng tái lập]({{ site.baseurl }}/img/chapter_img/chapter01/replication_crisis_stats.png)

Điều này không có nghĩa là mọi nhà khoa học đều gian lận. Phần lớn vấn đề nằm ở chỗ dữ liệu thường nhiễu, cỡ mẫu nhiều khi nhỏ, và hệ thống công bố lại thưởng rất mạnh cho những kết quả được gắn nhãn “có ý nghĩa thống kê”.

## 2. Câu chuyện rất đời thường phía sau khủng hoảng này

Hãy tưởng tượng có 20 nhóm nghiên cứu độc lập cùng kiểm tra một giả thuyết mà thực ra là sai. Nếu mỗi nhóm dùng ngưỡng $$p < 0.05$$, thì chỉ do ngẫu nhiên thôi, ta vẫn kỳ vọng sẽ có khoảng 1 nhóm tìm được “kết quả có ý nghĩa”.

Nếu đúng nhóm tìm ra kết quả “đẹp” ấy được công bố, còn 19 nhóm còn lại không công bố gì, thì toàn bộ văn học khoa học sẽ trông như thể giả thuyết vừa được hỗ trợ.

Đó là một trong những cơ chế nguy hiểm nhất đứng sau khủng hoảng tái lập.

![Publication bias và file drawer problem]({{ site.baseurl }}/img/chapter_img/chapter01/publication_bias.png)

## 3. P-value thực ra là gì?

Đây là định nghĩa chuẩn:

> **P-value là xác suất quan sát được dữ liệu ít nhất cực đoan như dữ liệu đang có, giả sử giả thuyết không $$H_0$$ là đúng.**

Nói gọn hơn, p-value trả lời câu hỏi:

**Nếu giả thuyết không $$H_0$$ là đúng, thì dữ liệu này có lạ không?**

Ví dụ, nếu $$H_0$$ nói rằng thuốc không có hiệu quả, còn dữ liệu cho thấy nhóm dùng thuốc cải thiện nhiều hơn nhóm đối chứng, thì một p-value nhỏ chỉ có nghĩa rằng dữ liệu kiểu này khá lạ nếu giả thuyết không thật sự đúng.

Vấn đề bắt đầu từ đây: đó **không phải** là câu hỏi mà nhà nghiên cứu thật sự muốn biết.

Nhà nghiên cứu thường lại muốn biết giả thuyết có khả năng đúng đến đâu, bằng chứng mạnh tới mức nào, hiệu ứng có lớn hay không, và bản thân kết quả có đáng tin tới đâu. P-value không trả lời trực tiếp những câu hỏi đó.

## 4. Một cách đọc p-value dễ hiểu hơn

Giả sử một thử nghiệm cho $$p = 0.03$$. Điều đó **không** có nghĩa là “xác suất giả thuyết không đúng là 3%”, cũng không có nghĩa là “xác suất thuốc có hiệu quả là 97%”.

Nó chỉ có nghĩa rằng nếu thật sự không có hiệu quả, thì xác suất để thấy dữ liệu này hoặc cực đoan hơn chỉ khoảng 3%.

Sự khác biệt nghe có vẻ nhỏ, nhưng thực ra là cả một khoảng cách lớn về logic.

![P-value không phải là xác suất H0 đúng]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_h0_probability.png)

*Hình minh họa: p-value nằm ở hướng $$P(\\text{dữ liệu} \\mid H_0)$$, không phải ở hướng $$P(H_0 \\mid \\text{dữ liệu})$$.*

![1 - p cũng không phải là xác suất giả thuyết nghiên cứu đúng]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_one_minus_p.png)

*Hình minh họa: việc lấy `1 - p` rồi xem như xác suất giả thuyết nghiên cứu đúng là một bước nhảy logic sai.*

## 5. Những hiểu lầm phổ biến nhất về p-value

Đây là những hiểu lầm rất thường gặp, kể cả trong bài báo khoa học.

### Hiểu lầm 1. P-value là xác suất giả thuyết không đúng

Sai. P-value là:

$$
P(\text{dữ liệu hoặc cực đoan hơn} \mid H_0),
$$

không phải:

$$
P(H_0 \mid \text{dữ liệu}).
$$

![Hiểu lầm 1 về p-value]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_h0_probability.png)

### Hiểu lầm 2. P-value nhỏ nghĩa là hiệu ứng lớn

Sai. P-value còn phụ thuộc mạnh vào cỡ mẫu: với cỡ mẫu rất lớn, một hiệu ứng rất nhỏ vẫn có thể cho p-value nhỏ; còn với cỡ mẫu nhỏ, một hiệu ứng tương đối lớn vẫn có thể chưa đủ nhỏ để vượt qua ngưỡng 0.05.

![Hiểu lầm 2: p nhỏ không đồng nghĩa hiệu ứng lớn]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_effect_size.png)

### Hiểu lầm 3. P-value > 0.05 nghĩa là không có hiệu ứng

Sai. Nó có thể chỉ nói rằng dữ liệu hiện tại chưa đủ mạnh để phát hiện hiệu ứng.

![Hiểu lầm 3: p lớn không có nghĩa chắc chắn không có hiệu ứng]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_large_p_no_effect.png)

### Hiểu lầm 4. 0.049 và 0.051 khác nhau về bản chất

Thực ra gần như không. Nhưng khi biến 0.05 thành một vạch thi đỗ/rớt cứng nhắc, người ta thường diễn giải chúng như hai thế giới hoàn toàn khác nhau.

![Hiểu lầm 4: ngưỡng 0.05 như một ranh giới ma thuật]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_alpha_threshold.png)

![Tóm tắt các hiểu lầm lớn về p-value]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_summary.png)

## 6. Vì sao p-value dễ bị lạm dụng?

Khi hệ thống công bố thưởng cho kết quả “có ý nghĩa thống kê”, người nghiên cứu rất dễ bị kéo vào những hành vi như thử nhiều biến đầu ra khác nhau, thử nhiều cách lọc dữ liệu, loại outlier có chọn lọc, dừng thu thập dữ liệu khi vừa chạm ngưỡng, hay chỉ báo cáo phân tích nào đẹp nhất.

Những hành vi đó không phải lúc nào cũng xuất phát từ gian lận. Nhiều khi chúng xuất phát từ áp lực công bố và từ việc người nghiên cứu tự thuyết phục rằng mình chỉ đang “khám phá dữ liệu”.

Nhưng hậu quả thì giống nhau: tỷ lệ phát hiện giả tăng mạnh.

![Các kỹ thuật p-hacking]({{ site.baseurl }}/img/chapter_img/chapter01/phacking_techniques.png)

## 7. Optional stopping: một ví dụ rất dễ gặp

Giả sử bạn bắt đầu với 20 người tham gia và chưa thấy p-value đủ nhỏ. Bạn tuyển thêm 10 người, rồi thêm 10 người nữa, cho tới khi p < 0.05 thì dừng.

Nghe có vẻ vô hại, nhưng đây là một cách âm thầm tăng xác suất tìm được “kết quả có ý nghĩa” chỉ do may rủi.

Trong Bayes, chuyện cập nhật tuần tự tự nhiên hơn nhiều, còn trong kiểm định tần suất cổ điển, việc dừng khi nhìn dữ liệu có thể phá vỡ diễn giải ban đầu của p-value.

### 7.1. Một ví dụ bằng con số: cứ nhìn dần cho tới khi p < 0.05

Giả sử một nghiên cứu bắt đầu với 20 người tham gia và cho ra $$p=0.18$$. Người nghiên cứu chưa hài lòng nên tuyển thêm 10 người, lúc này $$p=0.09$$. Vẫn chưa đủ “đẹp”, nên họ tuyển thêm 10 người nữa và thấy $$p=0.047$$, rồi dừng ngay và công bố kết quả là có ý nghĩa thống kê.

Vấn đề không nằm ở riêng con số $$0.047$$, mà ở chỗ quy tắc dừng đã phụ thuộc vào chính dữ liệu đang được quan sát. Nếu ngay từ đầu kế hoạch là thu đủ 60 người rồi mới kiểm tra, p-value cuối cùng hoàn toàn có thể lại bật về một mức như $$0.11$$. Optional stopping vì thế làm tăng cơ hội “vừa hay” chạm ngưỡng, dù hiệu ứng thật có thể rất yếu hoặc không tồn tại.

## 8. Publication bias: thứ làm bức tranh khoa học méo đi

Ngay cả khi mỗi nghiên cứu riêng lẻ đều làm đúng, khoa học vẫn có thể bị méo nếu các kết quả “dương tính” được công bố, còn các kết quả “âm tính” thì bị để trong ngăn kéo.

Khi đó, người đọc chỉ thấy những nghiên cứu “thành công”, và dễ tưởng rằng bằng chứng cho một giả thuyết đang mạnh hơn thực tế.

Đây là lý do ta không thể đánh giá một phát hiện chỉ bằng một bài báo đơn lẻ.

## 9. Ví dụ nổi tiếng: ngoại cảm và phát hiện phi thường

Một ví dụ hay được nhắc đến là các nghiên cứu tuyên bố có bằng chứng cho ngoại cảm. Nếu chỉ nhìn vào p-value, một số kết quả trông có vẻ “đáng chú ý”. Nhưng trực giác khoa học nói rằng một tuyên bố càng phi thường thì càng cần bằng chứng mạnh hơn rất nhiều.

P-value không biết phân biệt giữa một tuyên bố rất đời thường như “aspirin giúp giảm đau đầu” và một tuyên bố cực kỳ phi thường như “con người nhìn thấy tương lai”. Nó chỉ chấm mức “lạ của dữ liệu dưới giả thuyết không”.

Bayesian analysis khác ở chỗ nó cho phép đưa **prior plausibility** vào. Một giả thuyết rất khó tin từ đầu sẽ cần lượng bằng chứng mạnh hơn nhiều để posterior trở nên thuyết phục.

![Cách nhìn Frequentist: p-value đo độ lạ của dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_vs_posterior_frequentist.png)

![Cách nhìn Bayesian: posterior nói trực tiếp về xác suất điều ta quan tâm]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_vs_posterior_bayesian.png)

## 10. Vấn đề sâu hơn: p-value trả lời sai câu hỏi

Đây là điểm quan trọng nhất của bài.

Nhà khoa học thường muốn biết giả thuyết nào đáng tin hơn, tham số có thể nằm ở đâu, dữ liệu hỗ trợ giả thuyết này mạnh tới mức nào, và mức độ bất định còn lại là bao nhiêu.

P-value lại hỏi một câu khác: nếu giả thuyết không $$H_0$$ là đúng, thì dữ liệu này có lạ hay không.

Nó có thể hữu ích trong một số ngữ cảnh kiểm định, nhưng nó không phải câu trả lời trực tiếp cho mối quan tâm khoa học cốt lõi.

## 11. Vì sao bài này mở đường cho Bayes?

Bayesian statistics hấp dẫn không phải vì nó “ghét p-value”, mà vì nó cố trả lời trực tiếp hơn những điều ta thật sự quan tâm: xác suất của giả thuyết sau khi thấy dữ liệu, phân phối của tham số chưa biết, mức độ bất định hiện tại, và cách cập nhật niềm tin khi có thông tin mới.

Chapter 1 sẽ dần đưa bạn đến đúng điểm đó. Bài này chỉ có vai trò khởi động: chỉ ra vì sao rất nhiều người đã cảm thấy cách suy luận cũ chưa đủ.

> **3 ý cần nhớ.** Khủng hoảng tái lập không chỉ là lỗi của từng nhà nghiên cứu riêng lẻ mà còn là vấn đề của cả hệ thống suy luận và khuyến khích công bố; p-value rất dễ bị hiểu sai vì nó trả lời một câu hỏi khác với câu hỏi khoa học mà ta thực sự quan tâm; và khi p-values trở thành mục tiêu phải đạt, p-hacking cùng publication bias sẽ xuất hiện gần như tất yếu.

## Câu hỏi tự luyện

1. Vì sao một nghiên cứu có p-value nhỏ vẫn có thể không tái lập được?
2. Hãy giải thích bằng lời sự khác nhau giữa $$P(\text{dữ liệu} \mid H_0)$$ và $$P(H_0 \mid \text{dữ liệu})$$.
3. Vì sao cỡ mẫu lớn có thể làm một hiệu ứng nhỏ nhưng vô nghĩa thực tế vẫn cho p-value rất nhỏ?
4. Hãy cho một ví dụ đời thường về publication bias ngoài khoa học.

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 11.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 1.
- Wasserstein, R. L., & Lazar, N. A. (2016). The ASA Statement on p-Values.

---

*Bài học tiếp theo: [1.2 Xác suất như Độ tin cậy - Quan điểm Bayes](/vi/chapter01/probability-as-plausibility/)*
