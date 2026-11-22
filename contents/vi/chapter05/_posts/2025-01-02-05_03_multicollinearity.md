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

Sau bài này, bạn sẽ hiểu đa cộng tuyến (multicollinearity) là gì, vì sao nó gây khó khăn cho việc diễn giải từng hệ số hồi quy và trong bối cảnh nào hiện tượng này thực sự đáng lo ngại. Bạn cũng sẽ phân biệt rạch ròi hai mục tiêu khác nhau của hồi quy là **dự đoán** (prediction) và **diễn giải** (interpretation).

> **Ví dụ ngắn.** Khi dự đoán giá nhà từ diện tích và số phòng ngủ, hai biến này thường biến thiên cùng nhau vì nhà rộng hơn thường có nhiều phòng hơn. Mô hình vẫn có thể dự đoán giá tổng thể khá chính xác, nhưng sẽ rất khó trả lời chắc chắn câu hỏi: "giữ nguyên diện tích thì thêm một phòng ngủ làm giá thay đổi bao nhiêu?".
>
> **Câu hỏi tự kiểm tra.** Khi hai biến dự báo gần như đo lường cùng một đặc trưng, mô hình hồi quy sẽ gặp trở ngại gì trong việc tách riêng ảnh hưởng của từng biến?

## 1. Đa cộng tuyến (Multicollinearity) là gì?

Đa cộng tuyến xảy ra khi hai hoặc nhiều biến dự báo trong cùng một mô hình có tương quan rất cao với nhau. Vì chúng mang thông tin trùng lặp đáng kể, mô hình gặp khó khăn khi phân chia đóng góp riêng cho từng biến. Các ví dụ quen thuộc gồm chiều cao đo bằng cm và inch, diện tích và số phòng ngủ trong cùng một dự án chung cư có thiết kế đồng nhất, hay số giờ học và số bài tập hoàn thành trong một lớp học có kỷ luật cao.

Điều cần nhấn mạnh là đa cộng tuyến không có nghĩa dữ liệu bị sai; nó chỉ phản ánh việc các biến đầu vào đang chia sẻ quá nhiều thông tin giống nhau.

![Tương quan rất cao giữa hai predictors]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_predictor_correlation.png)

![Cả hai predictors đều liên quan mạnh đến outcome]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_both_predict_y.png)

![Tóm tắt vì sao multicollinearity làm khó diễn giải]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_multicollinearity_problem_summary.png)

Ba biểu đồ trên minh họa tình huống điển hình: cả hai biến dự báo đều liên quan mạnh đến biến kết quả, nhưng chúng cũng tương quan chặt với nhau nên mô hình khó phân định mức đóng góp riêng của từng biến.

## 2. Vì sao đa cộng tuyến làm hệ số hồi quy khó diễn giải?

Theo nguyên tắc của hồi quy đa biến, mỗi hệ số phản ánh tác động của một biến khi **giữ các biến còn lại cố định**. Tuy nhiên, nếu hai biến hầu như luôn tăng giảm đồng thời trong dữ liệu, việc giữ cố định biến này trong khi thay đổi biến kia rất hiếm khi xuất hiện thực tế. Trong ví dụ diện tích và số phòng ngủ, nếu dữ liệu có rất ít cặp căn nhà cùng diện tích nhưng khác số phòng ngủ, mô hình sẽ thiếu thông tin để ước lượng chắc chắn hệ số riêng của từng biến.

Hệ quả phổ biến là khoảng tin cậy hậu nghiệm (credible interval) của các hệ số mở rộng đáng kể, dấu của hệ số có thể thay đổi bất ngờ và ước lượng trở nên nhạy cảm chỉ với vài quan sát thêm bớt. Bốn hình dưới so sánh phân phối hậu nghiệm khi hai biến dự báo ít tương quan và khi chúng tương quan rất cao.

![Trường hợp predictors chỉ tương quan nhẹ]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_low_predictor_correlation.png)

![Trường hợp predictors tương quan rất cao]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_high_predictor_correlation.png)

![Posterior khi predictors ít tương quan]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_low_correlation_posterior.png)

![Posterior khi predictors tương quan cao]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_high_correlation_posterior.png)

### 2.1. Ví dụ bằng con số: mô hình tổng thể ổn nhưng hệ số riêng bất ổn

Giả sử ta dự đoán giá nhà bằng `diện tích` và `số phòng ngủ`, với hệ số tương quan giữa hai biến khoảng $$0.92$$. Nếu khớp riêng từng mô hình một biến:

- Chỉ dùng `diện tích`: tăng 1 m² đi kèm tăng trung bình **35 triệu đồng**.
- Chỉ dùng `số phòng ngủ`: tăng 1 phòng đi kèm tăng trung bình **700 triệu đồng**.

Cả hai kết quả đều hợp lý vì mỗi biến đang đại diện cho thông tin chung về quy mô căn nhà. Nhưng khi đưa đồng thời cả hai vào mô hình đa biến, ước lượng có thể trở thành:

- `diện tích`: khoảng **32 triệu đồng/m²** với khoảng hậu nghiệm tương đối gọn.
- `số phòng ngủ`: khoảng **40 triệu đồng/phòng** nhưng khoảng hậu nghiệm rất rộng, chẳng hạn từ **-180** đến **260 triệu đồng**.

Mô hình không hề dự đoán kém đi; nó chỉ phản ánh trung thực rằng dữ liệu hiện có chưa đủ để tách bạch rõ giá trị riêng của số phòng ngủ sau khi đã cố định diện tích.

## 3. Dấu hiệu nhận biết đa cộng tuyến

Trong thực hành, bạn có thể nhận diện đa cộng tuyến qua bốn dấu hiệu: các biến dự báo có tương quan rất cao trên ma trận tương quan hoặc biểu đồ phân tán; hệ số của một biến thay đổi mạnh khi thêm một biến liên quan khác; khoảng tin cậy của từng hệ số rất rộng dù mô hình tổng thể khớp tốt; hoặc dấu của hệ số trái ngược với trực giác chuyên môn. Ví dụ, nếu một doanh nghiệp luôn tăng giảm đồng thời ngân sách quảng cáo Facebook và Instagram, mô hình tổng thể vẫn dự đoán tốt doanh thu từ tổng chi tiêu quảng cáo nhưng khó tách riêng hiệu quả của từng kênh.

## 4. Đa cộng tuyến có phải lúc nào cũng là vấn đề nghiêm trọng?

Câu trả lời là **không** — mức độ ảnh hưởng phụ thuộc trực tiếp vào mục tiêu phân tích:

- **Khi mục tiêu là dự đoán (prediction):** đa cộng tuyến thường không gây cản trở lớn, vì tổ hợp thông tin chung của nhóm biến vẫn giúp dự báo chính xác biến kết quả (chẳng hạn dùng nhiều chỉ số tài chính tương quan để dự báo rủi ro tín dụng).
- **Khi mục tiêu là diễn giải (interpretation):** đa cộng tuyến trở thành rào cản đáng kể, bởi lúc này ta cần xác định biến nào đóng góp bao nhiêu cùng dấu và độ lớn ổn định của từng hệ số.

## 5. Ví dụ thực tế: lương, học vấn và kỹ năng chuyên môn

Giả sử ta giải thích mức lương bằng số năm đi học, bằng cấp cao nhất và điểm đánh giá kỹ năng chuyên môn — ba biến vốn có tương quan mạnh với nhau. Mô hình tổng thể có thể dự đoán lương khá sát, nhưng khó tách bạch riêng phần đóng góp của bằng cấp khi kỹ năng và số năm học cùng biến thiên theo. Cách kết luận trung thực khi đó là:

> Nhóm biến phản ánh nền tảng học thuật và chuyên môn liên hệ mạnh với mức lương, nhưng dữ liệu hiện có chưa đủ để tách riêng chính xác đóng góp của từng yếu tố.

### 5.1. Hình dạng phân phối hậu nghiệm đồng thời trong thống kê Bayes

Nếu vẽ phân phối hậu nghiệm đồng thời (joint posterior) của hệ số `số năm đi học` và hệ số `kỹ năng chuyên môn`, các mẫu thường không tụ thành một đám mây tròn mà kéo dài thành một **dải chéo dốc xuống**. Điều này cho thấy khi mô hình gán trọng số lớn hơn cho học vấn thì phải giảm trọng số của kỹ năng (và ngược lại), vì nhiều tổ hợp hệ số khác nhau cùng giải thích dữ liệu tốt ngang nhau. Do đó, bên cạnh trung bình hậu nghiệm riêng lẻ, cần quan sát cấu trúc tương quan giữa các hệ số trong phân phối hậu nghiệm đồng thời.

## 6. Cơ chế phía sau dải chéo trong phân phối hậu nghiệm

Trong góc nhìn Bayes, đa cộng tuyến hiện lên trực tiếp ở mối liên hệ âm giữa hai hệ số trong phân phối hậu nghiệm: tổng đóng góp của cả hai biến được dữ liệu xác định khá chắc chắn, nhưng tỷ lệ phân chia giữa từng biến lại có độ bất định lớn. Nhờ giữ lại toàn bộ phân phối hậu nghiệm thay vì chỉ một ước lượng điểm, phương pháp Bayes giúp ta nhìn thấy ngay sự bất định này thay vì bị đánh lừa bởi một con số duy nhất.

### Thử nghiệm: tăng tương quan làm phân phối hậu nghiệm kéo thành dải chéo

Tăng hệ số tương quan $$\rho$$ giữa hai biến dự báo để quan sát độ lệch chuẩn của $$b_1$$ tăng theo $$\sqrt{\text{VIF}}$$, $$b_1$$ và $$b_2$$ tương quan âm mạnh trong khi tổng $$b_1 + b_2$$ vẫn ổn định.

<div class="interactive-demo" markdown="1">
<div data-demo="collinear-explainer" data-lang="vi"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 7. Các hướng xử lý đa cộng tuyến

Không có giải pháp duy nhất cho mọi trường hợp; cách xử lý phụ thuộc vào câu hỏi nghiên cứu:

1. **Giữ một biến đại diện:** nếu hai biến gần như đo cùng một đại lượng (như diện tích và số phòng ngủ trong tập dữ liệu đồng nhất), có thể chỉ giữ lại biến mang thông tin trực tiếp hơn.
2. **Gộp thành chỉ số tổng hợp:** kết hợp các biến cùng đo một khái niệm chung (chẳng hạn tạo chỉ số kinh tế – xã hội từ nhiều biến thu nhập và tài sản).
3. **Mở rộng tính đa dạng của dữ liệu:** thu thập thêm dữ liệu ở những bối cảnh nơi các biến dự báo biến thiên độc lập hơn.
4. **Sử dụng phân phối tiên nghiệm điều chuẩn (regularizing priors):** trong thống kê Bayes, phân phối tiên nghiệm thông tin yếu hoặc tiên nghiệm co rút giúp ổn định ước lượng khi dữ liệu không đủ mạnh để tách riêng từng hệ số.
5. **Thừa nhận giới hạn diễn giải:** khi dữ liệu chỉ đủ sức trả lời bài toán dự đoán chứ không đủ để phân rạch từng hệ số, nêu rõ giới hạn này là một kết luận khoa học chuẩn mực.

## 8. Danh mục câu hỏi kiểm tra nhanh

Khi nghi ngờ đa cộng tuyến, hãy lần lượt rà soát: mục tiêu chính là dự đoán hay diễn giải; cặp hoặc nhóm biến nào đang trùng lặp thông tin; nếu bỏ bớt một biến thì chất lượng dự đoán có giảm đáng kể không; nếu giữ cả hai thì khoảng tin cậy còn đủ hẹp để diễn giải không; và liệu gộp thành một khái niệm chung có tự nhiên hơn không.

## 9. Ba hiểu lầm phổ biến

- **"Hệ số đổi dấu chứng tỏ mô hình bị sai":** chưa chắc; đó có thể chỉ là hệ quả của việc phân chia đóng góp giữa hai biến tương quan rất cao.
- **"Các biến dự báo không được phép tương quan với nhau":** trong dữ liệu thực tế, các biến hầu như luôn có mức độ tương quan nhất định; điều quan trọng là hiểu tác động của nó đến độ bất định.
- **"Càng thêm nhiều biến mô hình càng tốt":** thêm các biến lặp lại thông tin sẵn có thường làm giảm khả năng diễn giải mà ít cải thiện hiệu quả dự báo.

## 10. Kết nối sang hiệu ứng tương tác (Interaction Effects)

Cần phân biệt hai khái niệm ở Bài 5.3 và Bài 5.4: **đa cộng tuyến** hỏi liệu các biến dự báo có đang trùng lặp thông tin với nhau không, còn **hiệu ứng tương tác** hỏi liệu tác động của một biến dự báo lên kết quả có thay đổi tùy theo giá trị của biến dự báo khác hay không.

> **3 ý cần nhớ.** Đa cộng tuyến xảy ra khi các biến dự báo chứa thông tin trùng lặp cao, làm phình to bất định của từng hệ số riêng lẻ; hiện tượng này ảnh hưởng mạnh đến mục tiêu diễn giải nhưng thường ít gây hại hơn cho mục tiêu dự đoán; và hướng xử lý phụ thuộc vào mục tiêu cụ thể — từ chọn biến đại diện, gộp biến, dùng tiên nghiệm điều chuẩn đến chấp nhận giới hạn diễn giải của dữ liệu.

## Video tham khảo

- [Multicollinearity (in Regression Analysis)](https://www.youtube.com/watch?v=G1WX5GiFSWQ) — numiqo, English. **xem trước**. Minh họa cách đa cộng tuyến khiến mô hình khó tách riêng tín hiệu của từng biến, khớp với định nghĩa ở đầu bài.
- [Multicollinearity](https://www.youtube.com/watch?v=O4jDva9B3fw) — Ben Lambert, English. Giải thích ảnh hưởng của đa cộng tuyến trong hồi quy, bổ trợ cho phần phân biệt giữa dự báo và diễn giải hệ số.
- [Variance Inflation Factors: testing for multicollinearity](https://www.youtube.com/watch?v=0SBIXgPVex8) — Ben Lambert, English. Trình bày hệ số phóng đại phương sai (VIF), hỗ trợ phần chẩn đoán mức độ tương quan giữa các biến dự báo.

## Câu hỏi tự luyện

1. Vì sao diện tích và số phòng ngủ thường dễ dẫn tới đa cộng tuyến?
2. Hãy nêu một tình huống trong công việc của bạn mà mô hình vẫn dự đoán tốt dù khó diễn giải riêng từng hệ số.
3. Khi hai biến gần như trùng lặp thông tin, bạn sẽ chọn giữ một biến hay gộp cả hai? Giải thích lý do.
4. Trong bài toán phân tích tiền lương, vì sao học vấn và kỹ năng chuyên môn thường gây khó khăn cho việc tách bạch hệ số riêng?

## Tài liệu tham khảo

**Gelman, A., Hill, J., & Vehtari, A. (2020).** *Regression and Other Stories*. Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

---

*Bài học tiếp theo: [5.4 Interaction Effects]({{ site.baseurl }}/contents/vi/chapter05/05_04_interaction_effects/)*
