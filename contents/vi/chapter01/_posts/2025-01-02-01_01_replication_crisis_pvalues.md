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

Sau bài này, bạn cần nắm được ba nội dung chính. Thứ nhất, vì sao nhiều nghiên cứu đã công bố lại không thể tái lập kết quả. Thứ hai, vì sao p-value thường bị hiểu sai và dễ bị lạm dụng. Thứ ba, vì sao những vấn đề đó thúc đẩy cộng đồng khoa học tìm đến các phương pháp suy luận khác, trong đó có thống kê Bayes.

> **Ví dụ mini.** Một nghiên cứu báo cáo p-value < 0.05 cho thấy thuốc mới có hiệu quả, nhưng khi nhóm nghiên cứu khác lặp lại đúng thiết kế thí nghiệm thì không còn quan sát thấy hiệu quả đó nữa. Đây là dạng tình huống điển hình dẫn đến khủng hoảng tái lập.
>
> **Câu hỏi tự kiểm tra.** Một p-value nhỏ có thực sự đồng nghĩa với việc giả thuyết nghiên cứu là đúng không?

## 1. Khủng hoảng tái lập là gì?

Trong khoa học, một kết quả đáng tin cậy không chỉ cần có số liệu “đẹp” trên một bài báo, mà còn phải **lặp lại được** khi nhóm nghiên cứu khác tiến hành lại thí nghiệm theo quy trình tương tự. Tuy nhiên, trong nhiều lĩnh vực như tâm lý học, y học tiền lâm sàng hay khoa học xã hội, không ít kết quả nổi bật đã không thể tái lập.

![Thống kê khủng hoảng tái lập]({{ site.baseurl }}/img/chapter_img/chapter01/replication_crisis_stats.png)

Điều này không có nghĩa là phần lớn các nhà khoa học đều gian lận. Nguyên nhân chủ yếu nằm ở việc dữ liệu thường chứa nhiều nhiễu, cỡ mẫu hay bị giới hạn, trong khi hệ thống công bố lại ưu ái mạnh mẽ những kết quả đạt nhãn “có ý nghĩa thống kê”.

## 2. Cơ chế phía sau khủng hoảng tái lập

Hãy tưởng tượng 20 nhóm nghiên cứu độc lập cùng kiểm tra một giả thuyết mà thực chất là sai. Nếu mỗi nhóm sử dụng ngưỡng $$p < 0.05$$, thì chỉ riêng do biến động ngẫu nhiên, ta vẫn kỳ vọng có khoảng 1 nhóm thu được “kết quả có ý nghĩa thống kê”. Nếu đúng nhóm thu được kết quả “đẹp” ấy được đăng báo còn 19 nhóm còn lại không công bố, thì kho tài liệu khoa học sẽ trông như thể giả thuyết đó đã được củng cố. Đây là một trong những cơ chế đáng lo ngại nhất đằng sau khủng hoảng tái lập.

![Publication bias và file drawer problem]({{ site.baseurl }}/img/chapter_img/chapter01/publication_bias.png)

## 3. P-value thực chất là gì?

Định nghĩa chuẩn của p-value như sau:

> **P-value là xác suất quan sát được dữ liệu cực đoan ngang bằng hoặc hơn dữ liệu đang có, với giả định giả thuyết không $$H_0$$ là đúng.**

Nói gọn hơn, p-value trả lời câu hỏi: **nếu giả thuyết không $$H_0$$ là đúng, thì dữ liệu quan sát được có bất thường không?**

Ví dụ, nếu $$H_0$$ phát biểu rằng thuốc không có hiệu quả, còn dữ liệu cho thấy nhóm dùng thuốc cải thiện nhiều hơn nhóm đối chứng, thì một p-value nhỏ chỉ có nghĩa là dữ liệu này khá bất thường nếu giả thuyết không thực sự đúng. Vấn đề nảy sinh ở chỗ đó **không phải** câu hỏi mà nhà nghiên cứu thực sự muốn trả lời. Nhà nghiên cứu thường muốn biết giả thuyết có khả năng đúng đến đâu, bằng chứng mạnh mức nào, hiệu ứng lớn hay nhỏ, và kết quả đáng tin tới đâu — những câu hỏi mà p-value không trả lời trực tiếp.

## 4. Cách đọc p-value cho đúng

Giả sử một thử nghiệm cho $$p = 0.03$$. Con số này **không** có nghĩa là “xác suất giả thuyết không đúng là 3%”, và cũng không có nghĩa là “xác suất thuốc có hiệu quả là 97%”. Nó chỉ có nghĩa là nếu thuốc thực sự không có hiệu quả, thì xác suất quan sát được dữ liệu này hoặc cực đoan hơn chỉ vào khoảng 3%. Sự khác biệt nghe có vẻ tinh tế, nhưng thực chất là một khoảng cách lớn về mặt logic.

![P-value không phải là xác suất H0 đúng]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_h0_probability.png)

*Hình minh họa: p-value nằm ở hướng $$P(\text{dữ liệu} \mid H_0)$$, không phải ở hướng $$P(H_0 \mid \text{dữ liệu})$$.*

![1 - p cũng không phải là xác suất giả thuyết nghiên cứu đúng]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_one_minus_p.png)

*Hình minh họa: việc lấy `1 - p` rồi xem như xác suất giả thuyết nghiên cứu đúng là một suy luận sai về mặt logic.*

## 5. Những hiểu lầm phổ biến nhất về p-value

Dưới đây là những hiểu lầm rất thường gặp, kể cả trong các bài báo khoa học.

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

Sai. P-value phụ thuộc mạnh vào cỡ mẫu: khi cỡ mẫu rất lớn, một hiệu ứng rất nhỏ vẫn có thể tạo ra p-value nhỏ; ngược lại, khi cỡ mẫu nhỏ, một hiệu ứng tương đối lớn vẫn có thể chưa đủ để vượt qua ngưỡng 0.05.

![Hiểu lầm 2: p nhỏ không đồng nghĩa hiệu ứng lớn]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_effect_size.png)

### Hiểu lầm 3. P-value > 0.05 nghĩa là không có hiệu ứng

Sai. Kết quả này có thể chỉ phản ánh rằng dữ liệu hiện có chưa đủ mạnh để phát hiện hiệu ứng.

![Hiểu lầm 3: p lớn không có nghĩa chắc chắn không có hiệu ứng]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_large_p_no_effect.png)

### Hiểu lầm 4. 0.049 và 0.051 khác nhau về bản chất

Thực tế hai giá trị này gần như không khác nhau. Tuy nhiên, khi biến ngưỡng 0.05 thành một ranh giới đỗ/trượt cứng nhắc, người ta thường diễn giải chúng như hai kết quả đối lập hoàn toàn.

![Hiểu lầm 4: ngưỡng 0.05 như một ranh giới ma thuật]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_alpha_threshold.png)

![Tóm tắt các hiểu lầm lớn về p-value]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_misconception_summary.png)

## 6. Vì sao p-value dễ bị lạm dụng?

Khi hệ thống công bố chỉ ưu tiên kết quả “có ý nghĩa thống kê”, người nghiên cứu dễ bị cuốn vào những thao tác linh hoạt quá mức như thử nhiều biến đầu ra khác nhau, thử nhiều cách lọc dữ liệu, loại bỏ ngoại lai (outlier) có chọn lọc, dừng thu thập dữ liệu ngay khi vừa chạm ngưỡng, hoặc chỉ báo cáo phân tích cho kết quả đẹp nhất. Những hành vi này không phải lúc nào cũng xuất phát từ ý định gian lận; nhiều khi chúng bắt nguồn từ áp lực công bố và tâm lý cho rằng mình chỉ đang “khám phá dữ liệu”. Tuy vậy, hậu quả vẫn giống nhau: tỷ lệ phát hiện giả (false positive) tăng mạnh.

![Các kỹ thuật p-hacking]({{ site.baseurl }}/img/chapter_img/chapter01/phacking_techniques.png)

## 7. Dừng thu thập tùy ý (Optional stopping): một ví dụ dễ gặp

Giả sử bạn bắt đầu với 20 người tham gia và chưa thấy p-value đủ nhỏ. Bạn tuyển thêm 10 người, rồi thêm 10 người nữa, cho đến khi $$p < 0.05$$ thì dừng lại. Thao tác này nghe có vẻ vô hại, nhưng nó âm thầm làm tăng xác suất thu được “kết quả có ý nghĩa thống kê” hoàn toàn do ngẫu nhiên. Trong thống kê Bayes, việc cập nhật tuần tự diễn ra tự nhiên hơn nhiều, còn trong kiểm định tần suất cổ điển, việc quyết định dừng dựa trên dữ liệu đang quan sát sẽ phá vỡ ý nghĩa ban đầu của p-value.

### 7.1. Một ví dụ bằng con số: nhìn dữ liệu cho tới khi p < 0.05

Giả sử một nghiên cứu bắt đầu với 20 người tham gia và thu được $$p=0.18$$. Chưa hài lòng, người nghiên cứu tuyển thêm 10 người và thấy $$p=0.09$$. Vẫn chưa đạt ngưỡng, họ tuyển thêm 10 người nữa, thấy $$p=0.047$$, liền dừng ngay và công bố kết quả có ý nghĩa thống kê.

Vấn đề không nằm ở riêng con số $$0.047$$, mà ở chỗ quy tắc dừng đã phụ thuộc vào chính dữ liệu đang quan sát. Nếu kế hoạch ban đầu là thu đủ 60 người rồi mới kiểm định, p-value cuối cùng hoàn toàn có thể quay lại một mức như $$0.11$$. Do đó, optional stopping làm tăng cơ hội “vừa kịp” chạm ngưỡng, ngay cả khi hiệu ứng thực rất yếu hoặc không tồn tại.

## 8. Thiên lệch công bố (Publication bias): điều làm méo bức tranh khoa học

Ngay cả khi từng nghiên cứu riêng lẻ đều được thực hiện đúng quy trình, bức tranh khoa học vẫn có thể bị sai lệch nếu các kết quả “dương tính” được công bố còn các kết quả “âm tính” bị xếp lại trong ngăn kéo. Khi đó, người đọc chỉ nhìn thấy các nghiên cứu “thành công” và dễ đánh giá quá cao độ mạnh của bằng chứng dành cho một giả thuyết. Đây là lý do ta không nên đánh giá một phát hiện khoa học chỉ dựa trên một bài báo đơn lẻ.

## 9. Ví dụ nổi tiếng: ngoại cảm và những tuyên bố phi thường

Một ví dụ thường được nhắc đến là các nghiên cứu tuyên bố tìm thấy bằng chứng về ngoại cảm. Nếu chỉ nhìn vào p-value, một vài kết quả có vẻ “đáng chú ý”. Tuy nhiên, trực giác khoa học cho thấy một tuyên bố càng phi thường thì càng đòi hỏi bằng chứng mạnh hơn rất nhiều.

P-value không phân biệt được một giả thuyết quen thuộc như “aspirin giúp giảm đau đầu” với một tuyên bố phi thường như “con người nhìn thấy tương lai”; nó chỉ đo mức độ bất thường của dữ liệu dưới giả thuyết không. Phân tích Bayes khác ở chỗ cho phép đưa **mức độ hợp lý ban đầu (prior plausibility)** vào mô hình: một giả thuyết khó tin ngay từ đầu sẽ cần bằng chứng mạnh hơn nhiều để xác suất hậu nghiệm trở nên thuyết phục.

![Cách nhìn Frequentist: p-value đo độ lạ của dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_vs_posterior_frequentist.png)

![Cách nhìn Bayesian: posterior nói trực tiếp về xác suất điều ta quan tâm]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_vs_posterior_bayesian.png)

## 10. Vấn đề cốt lõi: p-value trả lời sai câu hỏi

Đây là điểm quan trọng nhất của bài học. Nhà khoa học thường muốn biết giả thuyết nào đáng tin hơn, tham số có thể nằm trong khoảng nào, dữ liệu ủng hộ giả thuyết mạnh đến mức nào, và độ bất định còn lại là bao nhiêu. Trong khi đó, p-value lại trả lời một câu hỏi khác: nếu giả thuyết không $$H_0$$ đúng thì dữ liệu này bất thường đến đâu. Nó có thể hữu ích trong một số bối cảnh kiểm định nhất định, nhưng không phải câu trả lời trực tiếp cho mối quan tâm khoa học cốt lõi.

## 11. Vì sao bài này mở đường cho thống kê Bayes?

Thống kê Bayes hấp dẫn không phải vì phủ nhận p-value, mà vì hướng đến việc trả lời trực tiếp hơn những câu hỏi ta thực sự quan tâm: xác suất của giả thuyết sau khi quan sát dữ liệu, phân phối của tham số chưa biết, mức độ bất định hiện tại và cách cập nhật niềm tin khi có thông tin mới. Bài học này đóng vai trò khởi động cho Chương 1 bằng cách chỉ ra vì sao nhiều nhà nghiên cứu cảm thấy cách suy luận truyền thống là chưa đủ.

> **3 ý cần nhớ.** Khủng hoảng tái lập không chỉ là lỗi cá nhân của từng nhà nghiên cứu mà còn là vấn đề của cả hệ thống suy luận và cơ chế khuyến khích công bố; p-value dễ bị hiểu sai vì nó trả lời một câu hỏi khác với câu hỏi khoa học cốt lõi; và khi p-value trở thành mục tiêu phải đạt, p-hacking cùng thiên lệch công bố gần như chắc chắn sẽ xuất hiện.

## Video tham khảo

- [p-values: What they are and how to interpret them](https://www.youtube.com/watch?v=vemZtEM63GY) — StatQuest with Josh Starmer, English. **xem trước**. Giải thích câu hỏi thực sự mà p-value trả lời, bổ trợ cho phần chỉ ra các hiểu lầm thường gặp trong bài.
- [p-hacking: What it is and how to avoid it!](https://www.youtube.com/watch?v=HDCOUXE3HMM) — StatQuest with Josh Starmer, English. Phân tích cách p-hacking nảy sinh từ những lựa chọn phân tích linh hoạt quá mức, làm rõ vì sao nhiều kết quả không thể tái lập.
- [The reproducibility crisis and other problems in science | John Ioannidis](https://www.youtube.com/watch?v=vY9mGJQFdyE) — The Institute of Art and Ideas, English. Bài nói chuyện của John Ioannidis về khủng hoảng tái lập, kết nối việc lạm dụng kiểm định với độ tin cậy của các công bố khoa học.

## Câu hỏi tự luyện

1. Vì sao một nghiên cứu có p-value nhỏ vẫn có thể không tái lập được?
2. Hãy giải thích bằng lời sự khác nhau giữa $$P(\text{dữ liệu} \mid H_0)$$ và $$P(H_0 \mid \text{dữ liệu})$$.
3. Vì sao cỡ mẫu lớn có thể làm một hiệu ứng nhỏ nhưng không có ý nghĩa thực tế vẫn cho p-value rất nhỏ?
4. Hãy nêu một ví dụ đời thường về thiên lệch công bố (publication bias) ngoài lĩnh vực khoa học.

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 11.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 1.
- Wasserstein, R. L., & Lazar, N. A. (2016). The ASA Statement on p-Values.

---

*Bài học tiếp theo: [1.2 Xác suất như Độ tin cậy - Quan điểm Bayes]({{ site.baseurl }}/contents/vi/chapter01/01_02_probability_as_plausibility/)*
