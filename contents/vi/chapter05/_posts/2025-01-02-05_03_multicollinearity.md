---
layout: post
title: "Bài 5.3: Multicollinearity - Khi Predictors Tương quan"
chapter: '05'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu multicollinearity (đa cộng tuyến) là gì, tại sao nó làm cho việc diễn giải coefficients (các hệ số) trở nên khó khăn, và khi nào nó thực sự đáng lo. Bạn cũng cần phân biệt rõ hai mục tiêu khác nhau của hồi quy, đó là **prediction** (dự đoán) và **interpretation** (diễn giải).

> **Ví dụ mini.** Bạn dự đoán giá nhà bằng diện tích và số phòng ngủ. Hai biến này thường đi cùng nhau: nhà rộng hơn thường cũng có nhiều phòng hơn. Khi đó mô hình có thể dự đoán giá khá tốt, nhưng lại lúng túng khi phải trả lời chính xác "giữ mọi thứ khác cố định thì thêm một phòng ngủ làm giá tăng bao nhiêu?".
>
> **Câu hỏi tự kiểm tra.** Nếu hai predictors gần như đo cùng một thứ, mô hình sẽ gặp khó khăn gì khi tách riêng ảnh hưởng của từng biến?

## 1. Multicollinearity là gì?

Multicollinearity xảy ra khi hai hoặc nhiều predictors (biến dự báo) trong cùng một mô hình có tương quan cao với nhau. Nói đơn giản hơn, chúng thường di chuyển cùng nhau, mang thông tin trùng lặp đáng kể, và vì thế mô hình khó biết nên "ghi công" cho biến nào. Những ví dụ rất điển hình là chiều cao tính bằng cm và chiều cao tính bằng inch, diện tích nhà và số phòng ngủ trong một khu chung cư có thiết kế khá giống nhau, hoặc số giờ học và số bài tập đã hoàn thành trong một lớp học kỷ luật cao.

Vấn đề không phải là dữ liệu sai. Vấn đề là các predictors quá giống nhau về mặt thông tin.

Ba góc nhìn dưới đây tóm tắt trực giác cơ bản nhất của multicollinearity.

![Tương quan rất cao giữa hai predictors]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_predictor_correlation.png)

![Cả hai predictors đều liên quan mạnh đến outcome]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_both_predict_y.png)

![Tóm tắt vì sao multicollinearity làm khó diễn giải]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_problem_summary.png)

Hình trên cho thấy tình huống rất điển hình: cả hai predictors đều liên quan đến outcome, nhưng chúng cũng quá giống nhau nên mô hình khó tách biệt ai đóng góp bao nhiêu.

## 2. Tại sao multicollinearity làm hệ số trở nên khó đọc?

Hãy quay lại nguyên tắc của multiple regression:

> mỗi hệ số được hiểu là ảnh hưởng của một biến khi giữ các biến khác cố định.

Vấn đề là nếu hai biến thường luôn cùng tăng cùng giảm, điều kiện "giữ biến kia cố định" trở nên khá xa lạ với dữ liệu thật.

### Ví dụ: diện tích và số phòng ngủ

Trong thực tế, căn nhà diện tích lớn thường có nhiều phòng ngủ hơn, còn căn nhỏ thường có ít phòng ngủ hơn.

Nếu hỏi:

> giữa hai căn có cùng diện tích nhưng khác 1 phòng ngủ thì giá chênh bao nhiêu?

đó là một câu hỏi hợp lý. Nhưng nếu dữ liệu của bạn hiếm khi có những cặp nhà như vậy, mô hình sẽ không có nhiều thông tin để trả lời chắc chắn.

Kết quả thường là credible interval (khoảng khả tín) của các hệ số rộng hơn, dấu của hệ số có thể đổi chiều bất ngờ, và các hệ số trở nên rất nhạy với việc thêm bớt chỉ vài quan sát.

So sánh dưới đây cho thấy khác biệt giữa bối cảnh predictor ít tương quan và predictor gần như trùng lặp.

![Trường hợp predictors chỉ tương quan nhẹ]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_low_predictor_correlation.png)

![Trường hợp predictors tương quan rất cao]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_high_predictor_correlation.png)

![Posterior khi predictors ít tương quan]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_low_correlation_posterior.png)

![Posterior khi predictors tương quan cao]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_high_correlation_posterior.png)

### 2.1. Một ví dụ bằng con số: mô hình tổng thể ổn nhưng hệ số riêng lúng túng

Giả sử ta dự đoán giá nhà bằng `diện tích` và `số phòng ngủ`, và hai biến này có tương quan rất cao, chẳng hạn khoảng $$0.92$$.

Nếu fit riêng từng mô hình đơn, ta có thể thấy:

- mô hình chỉ có `diện tích`: thêm 1 m² đi kèm tăng khoảng **35 triệu đồng**,
- mô hình chỉ có `số phòng ngủ`: thêm 1 phòng đi kèm tăng khoảng **700 triệu đồng**.

Hai kết quả này đều nghe hợp lý vì mỗi biến đang đại diện cho gần như cùng một gói thông tin về "độ lớn của căn nhà".

Nhưng khi đưa cả hai vào cùng một mô hình, kết quả có thể chuyển thành:

- `diện tích`: khoảng **32 triệu đồng/m²** với interval khá ổn,
- `số phòng ngủ`: khoảng **40 triệu đồng/phòng** nhưng interval rất rộng, chẳng hạn từ **-180** đến **260 triệu**.

Ở đây model chưa chắc dự đoán tệ. Điều nó đang nói là: "tôi vẫn biết nhà lớn hơn thường đắt hơn, nhưng dữ liệu này chưa đủ tách thật rõ giá trị riêng của số phòng ngủ sau khi diện tích đã được giữ cố định".

Đây là kiểu tình huống rất điển hình của multicollinearity: thông tin tổng thể về nhóm biến vẫn hữu ích, nhưng việc chia công cho từng biến trở nên bất ổn.

## 3. Dấu hiệu nhận biết trong thực tế

Khi làm việc với dữ liệu, bạn có thể nghi ngờ multicollinearity nếu thấy predictors có tương quan rất cao trên scatter plot hoặc correlation matrix (ma trận tương quan), nếu hệ số của từng biến "nhảy loạn" khi thêm một predictor mới, nếu interval của coefficients rộng dù mô hình tổng thể vẫn fit khá ổn, hoặc nếu dấu của hệ số trái với trực giác chuyên môn. Chẳng hạn, trong mô hình dự đoán doanh thu, ngân sách quảng cáo cho Facebook và Instagram có thể rất giống nhau vì công ty thường tăng giảm chúng cùng lúc; hậu quả là mô hình khó nói kênh nào hiệu quả hơn, dù tổng ngân sách quảng cáo nhìn chung vẫn dự đoán doanh thu tốt.

## 4. Multicollinearity có phải lúc nào cũng xấu không?

Không.

Đây là điểm rất quan trọng.

### 4.1. Nếu mục tiêu là prediction

Nếu mục tiêu chính là prediction, multicollinearity nhiều khi không quá đáng sợ, vì model vẫn có thể dự đoán outcome tốt, tổng thông tin từ nhóm predictors đó vẫn hữu ích, và điều bạn cần chủ yếu là dự báo chính xác chứ không phải giải thích riêng từng coefficient. Ví dụ, một mô hình dự đoán nguy cơ tín dụng có thể dùng nhiều chỉ số tài chính khá giống nhau mà vẫn cho dự báo chấp nhận được.

### 4.2. Nếu mục tiêu là interpretation

Nếu mục tiêu là interpretation, multicollinearity trở thành vấn đề lớn hơn nhiều, bởi vì lúc này bạn thực sự quan tâm biến nào quan trọng, cường độ ảnh hưởng riêng của từng biến là bao nhiêu, và dấu cũng như độ lớn của coefficients có ổn định hay không. Khi các predictors chồng lấn quá nhiều, toàn bộ sức mạnh diễn giải ấy sẽ yếu đi rõ rệt.

## 5. Một ví dụ đời thường: lương và học vấn

Giả sử bạn muốn giải thích lương bằng số năm đi học, bằng cấp cao nhất, và kỹ năng chuyên môn được kiểm tra.

Ba biến này liên quan khá mạnh với nhau.

Điều có thể xảy ra là mô hình tổng thể vẫn dự đoán lương tương đối tốt, nhưng lại rất khó nói chính xác riêng bằng cấp đóng góp bao nhiêu nếu kỹ năng và số năm đi học cũng tăng theo.

Khi đó, câu trả lời thành thật hơn sẽ là:

> Bộ biến về nền tảng học thuật và chuyên môn liên quan mạnh đến lương, nhưng dữ liệu hiện tại không đủ tách bạch rõ đóng góp riêng của từng thành phần.

Đây là kiểu diễn giải trưởng thành hơn là cố ép mỗi coefficient thành một "sự thật chắc chắn".

### 5.1. Dấu hiệu Bayes rất hay gặp: các posterior kéo thành dải chéo

Nếu bạn vẽ joint posterior của `số năm đi học` và `điểm kỹ năng chuyên môn`, bạn có thể thấy các mẫu không tạo thành một đám mây tròn gọn mà thành một dải chéo đi xuống.

Điều đó thường có nghĩa là:

- khi posterior gán ảnh hưởng lớn hơn cho học vấn, nó sẽ gán ảnh hưởng nhỏ hơn cho kỹ năng,
- và ngược lại, nhiều tổ hợp khác nhau vẫn giải thích dữ liệu gần như tốt ngang nhau.

Vì vậy, điều nên đọc đầu tiên không phải chỉ là posterior mean của từng hệ số, mà còn là **cấu trúc phụ thuộc giữa các hệ số** trong posterior chung.

## 6. Vì sao posterior của các hệ số thường dính chặt với nhau?

Trong bối cảnh Bayes, multicollinearity thường lộ ra ở joint posterior (hậu nghiệm chung) của coefficients: khi một hệ số tăng thì hệ số kia có xu hướng giảm, bởi vì nhiều tổ hợp khác nhau vẫn có thể tạo ra dự đoán gần giống nhau.

Ta có thể hình dung model đang nói:

> Tôi biết tổng đóng góp của nhóm biến này khá quan trọng, nhưng tôi chưa thật sự chắc nên chia công cho từng biến ra sao.

Đây là lý do ta hay thấy posterior của các hệ số kéo dài theo một hướng chéo thay vì tròn gọn.

## 7. Nên xử lý multicollinearity như thế nào?

Không có một đáp án duy nhất cho mọi trường hợp. Ta chọn cách xử lý theo mục tiêu phân tích.

### 7.1. Giữ một biến đại diện

Nếu hai biến gần như đo cùng một thứ, đôi khi cách đơn giản nhất là chỉ giữ một biến. Ví dụ, ta có thể giữ diện tích và bỏ số phòng ngủ nếu trong bộ dữ liệu hiện tại chúng gần như lặp lại cùng một thông tin.

### 7.2. Gộp thành chỉ số tổng hợp

Nếu nhiều biến cùng mô tả một khái niệm, ta có thể tạo composite score (điểm tổng hợp). Ví dụ, nhiều biến về điều kiện kinh tế hộ gia đình có thể gộp lại thành một chỉ số kinh tế xã hội.

### 7.3. Thu thập dữ liệu đa dạng hơn

Đây là cách rất hiệu quả nhưng hay bị quên.

Nếu dữ liệu chỉ đến từ một bối cảnh quá đồng nhất, predictors sẽ dễ đi cùng nhau. Mở rộng phạm vi dữ liệu có thể giúp tách bạch tín hiệu tốt hơn.

### 7.4. Dùng prior có tính regularization

Trong Bayes, prior hợp lý có thể giúp ổn định ước lượng khi dữ liệu không đủ mạnh để tách riêng từng hiệu ứng. Các chương sau sẽ quay lại kỹ hơn với regularization.

### 7.5. Chấp nhận giới hạn diễn giải

Đôi khi điều đúng nhất là thừa nhận:

> dữ liệu này phù hợp cho prediction hơn là để diễn giải riêng từng coefficient.

Đó không phải thất bại. Đó là một kết luận khoa học trung thực.

## 8. Một checklist rất thực dụng

Khi nghi ngờ multicollinearity, bạn có thể tự hỏi một chuỗi câu rất thực dụng: mục tiêu của mình là prediction hay interpretation, predictors nào đang trùng lặp thông tin, nếu bỏ bớt một biến thì năng lực dự đoán có giảm nhiều không, nếu giữ cả hai thì mình có còn diễn giải hệ số một cách tự tin hay không, và liệu có nên gộp chúng thành một khái niệm rộng hơn hay không.

## 9. Điều người học hay hiểu sai

### Hiểu sai 1: "Hệ số bị lệch dấu thì mô hình chắc chắn sai"

Chưa chắc. Có thể mô hình đang cố chia công giữa các predictors quá giống nhau.

### Hiểu sai 2: "Tương quan giữa predictors là cấm kỵ"

Không đúng. Dữ liệu đời thật rất thường có predictors tương quan. Điều quan trọng là hiểu hệ quả của chuyện đó.

### Hiểu sai 3: "Cứ thêm biến là tốt"

Nếu biến mới chỉ lặp lại thông tin cũ, bạn có thể làm mô hình khó diễn giải hơn mà không thu thêm được nhiều giá trị.

## 10. Kết nối sang interaction effects

Multicollinearity hỏi:

> các predictors có quá giống nhau không?

Interaction effects ở bài tiếp theo hỏi:

> ảnh hưởng của một predictor có thay đổi theo predictor khác không?

Một bên là vấn đề **trùng lặp thông tin**, một bên là vấn đề **phụ thuộc lẫn nhau về hiệu ứng**. Phân biệt được hai chuyện này sẽ giúp bạn đọc multiple regression chính xác hơn nhiều.

> **3 ý cần nhớ.** Multicollinearity xảy ra khi predictors mang thông tin quá giống nhau, khiến mô hình khó tách riêng ảnh hưởng của từng biến; đây là vấn đề đặc biệt nghiêm trọng khi mục tiêu là diễn giải coefficients, nhưng có thể ít nghiêm trọng hơn nếu mục tiêu chỉ là prediction; và cách xử lý luôn phụ thuộc vào mục tiêu, từ bỏ bớt biến, gộp biến, dùng prior ổn định hơn, thu thập dữ liệu đa dạng hơn cho đến chấp nhận giới hạn diễn giải.

## Câu hỏi tự luyện

1. Vì sao diện tích và số phòng ngủ dễ tạo ra multicollinearity?
2. Hãy nêu một ví dụ trong công việc của bạn mà prediction vẫn ổn dù coefficients khó diễn giải.
3. Nếu hai biến gần như trùng lặp thông tin, bạn sẽ cân nhắc giữ một biến hay gộp hai biến? Vì sao?
4. Trong nghiên cứu lương, vì sao học vấn và kỹ năng chuyên môn có thể gây khó khăn cho việc diễn giải riêng từng hệ số?

## Tài liệu tham khảo

**Gelman, A., Hill, J., & Vehtari, A. (2020).** *Regression and Other Stories*. Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

---

*Bài học tiếp theo: [5.4 Interaction Effects](/vi/chapter05/interaction-effects/)*
