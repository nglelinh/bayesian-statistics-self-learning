---
layout: post
title: "Bài 5.1: Multiple Regression - Từ Một đến Nhiều Predictors"
chapter: '05'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao phần lớn bài toán thực tế không thể giải quyết thỏa đáng chỉ với một biến dự báo (predictor). Bạn cũng sẽ nắm nguyên tắc cốt lõi của hồi quy đa biến (multiple regression): mỗi hệ số phản ánh tác động của một biến khi tất cả các biến dự báo còn lại trong mô hình được giữ cố định. Đây là nền tảng để đọc đúng kết quả hồi quy trong toàn bộ Chương 5.

> **Ví dụ ngắn.** Một công ty muốn dự đoán mức lương của nhân viên. Nếu chỉ dựa vào số năm kinh nghiệm, mô hình sẽ bỏ sót trình độ học vấn, vị trí công việc và khu vực làm việc. Hồi quy đa biến cho phép đưa đồng thời các yếu tố này vào mô hình để so sánh công bằng và sát thực tế hơn.
>
> **Câu hỏi tự kiểm tra.** Nếu hai người có cùng số năm kinh nghiệm nhưng trình độ học vấn khác nhau, một mô hình chỉ có một biến dự báo có nắm bắt được chênh lệch lương giữa họ không?

## 1. Vì sao một biến dự báo thường là chưa đủ?

Ở Chương 4, ta đã làm quen với hồi quy tuyến tính đơn:

$$
y = \alpha + \beta x + \epsilon
$$

Mô hình này hữu ích để xây dựng trực giác, nhưng các hiện tượng thực tế hiếm khi chỉ chịu tác động của một yếu tố duy nhất. Điểm thi không chỉ phụ thuộc vào số giờ học mà còn chịu ảnh hưởng từ kiến thức nền tảng, chất lượng giấc ngủ và độ khó đề thi; giá nhà phụ thuộc đồng thời vào diện tích, vị trí, tuổi công trình, số phòng ngủ và hạ tầng; còn cân nặng liên quan đến cả chiều cao, độ tuổi, giới tính, mức độ vận động và chế độ ăn. Ép một bài toán nhiều nguyên nhân vào mô hình một biến không chỉ làm mất thông tin quan trọng mà còn dễ dẫn đến diễn giải sai ý nghĩa của hệ số. Hồi quy đa biến được xây dựng để giải quyết chính giới hạn này.

## 2. Cấu trúc của mô hình nhiều biến dự báo

Dạng tổng quát của hồi quy đa biến là:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_k x_k + \epsilon
$$

Trong đó, $$y$$ là biến kết quả (outcome), $$x_1, x_2, \ldots, x_k$$ là các biến dự báo (predictors), $$\alpha$$ là hệ số chặn (intercept), mỗi $$\beta_j$$ là hệ số của biến $$x_j$$, và $$\epsilon$$ là phần nhiễu ngẫu nhiên quanh xu hướng trung bình.

Ba biểu đồ dưới đây minh họa cách cùng một biến kết quả thay đổi đồng thời theo nhiều chiều — khi nhìn từng biểu đồ hai chiều ta chỉ thấy một lát cắt riêng lẻ, còn hồi quy đa biến ghép các lát cắt đó thành một bề mặt chung.

![Cân nặng theo chiều cao, tô màu theo tuổi]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_vs_height_colored_by_age.png)

![Cân nặng theo tuổi, tô màu theo chiều cao]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_vs_age_colored_by_height.png)

![Góc nhìn 3D của cân nặng theo chiều cao và tuổi]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_height_age_3d.png)

## 3. Nguyên tắc cốt lõi: "giữ các biến khác cố định"

Trong hồi quy đa biến, hệ số $$\beta_1$$ không còn được đọc đơn giản là:

> cứ $$x_1$$ tăng thêm 1 đơn vị thì $$y$$ tăng thêm $$\beta_1$$ đơn vị.

Cách đọc chính xác phải là:

> **khi các biến dự báo khác trong mô hình được giữ cố định**, nếu $$x_1$$ tăng thêm 1 đơn vị thì giá trị kỳ vọng của $$y$$ thay đổi trung bình $$\beta_1$$ đơn vị.

Sự bổ sung điều kiện này làm thay đổi căn bản cách diễn giải mô hình.

### Ví dụ 1: lương, kinh nghiệm và học vấn

Xét mô hình:

$$
\text{Lương} = \alpha + \beta_1 \cdot \text{Kinh nghiệm} + \beta_2 \cdot \text{Học vấn} + \epsilon
$$

Ở đây, $$\beta_1$$ là chênh lệch lương kỳ vọng giữa hai người có **cùng trình độ học vấn** nhưng hơn kém nhau 1 năm kinh nghiệm; còn $$\beta_2$$ là chênh lệch lương kỳ vọng giữa hai người có **cùng số năm kinh nghiệm** nhưng khác nhau một bậc học vấn.

### Ví dụ 2: cân nặng, chiều cao và tuổi

Với mô hình:

$$
\text{Cân nặng} = \alpha + \beta_1 \cdot \text{Chiều cao} + \beta_2 \cdot \text{Tuổi} + \epsilon
$$

$$\beta_1$$ phản ánh mức chênh lệch cân nặng theo chiều cao giữa những người cùng độ tuổi, còn $$\beta_2$$ phản ánh mức chênh lệch theo độ tuổi giữa những người cùng chiều cao.

### 3.1. Ví dụ bằng con số

Giả sử mô hình lương ước lượng được là:

$$
\text{Lương} = 8 + 0.6 \cdot \text{Kinh nghiệm} + 2.5 \cdot \text{Sau đại học}.
$$

Trong đó `Kinh nghiệm` tính bằng năm, `Sau đại học` nhận giá trị `1` nếu có bằng sau đại học và `0` nếu không, còn `Lương` tính bằng triệu đồng/tháng. Khi đó:

- Giữa hai người cùng trình độ học vấn, thêm 1 năm kinh nghiệm tương ứng với mức lương kỳ vọng cao hơn **0.6 triệu đồng/tháng**.
- Giữa hai người cùng số năm kinh nghiệm, có bằng sau đại học tương ứng với mức lương kỳ vọng cao hơn **2.5 triệu đồng/tháng**.

Xét ba cá nhân cụ thể:

- **Người A** (5 năm kinh nghiệm, không có bằng sau đại học): $$8 + 0.6 \times 5 + 2.5 \times 0 = 11$$ triệu.
- **Người B** (6 năm kinh nghiệm, không có bằng sau đại học): $$8 + 0.6 \times 6 + 2.5 \times 0 = 11.6$$ triệu.
- **Người C** (5 năm kinh nghiệm, có bằng sau đại học): $$8 + 0.6 \times 5 + 2.5 \times 1 = 13.5$$ triệu.

So sánh A với B cho thấy ý nghĩa của hệ số kinh nghiệm (chênh 0.6 triệu); so sánh A với C cho thấy ý nghĩa của hệ số học vấn (chênh 2.5 triệu).

## 4. Vì sao hệ số thay đổi khi chuyển từ hồi quy đơn sang hồi quy đa biến?

Trong hồi quy đơn, một biến dự báo có thể vô tình gánh luôn phần ảnh hưởng của những biến liên quan chưa được đưa vào mô hình. Chẳng hạn, nếu người có học vấn cao hơn thường cũng có nhiều năm kinh nghiệm hơn, mô hình chỉ dùng biến học vấn sẽ gộp cả một phần tác động của kinh nghiệm vào hệ số học vấn. Khi bổ sung biến kinh nghiệm vào mô hình, hệ số học vấn có thể giảm đi — đó không phải dấu hiệu mô hình tệ hơn, mà là dấu hiệu mô hình đang tách bạch rõ hơn hai nguồn ảnh hưởng.

Nói ngắn gọn, hai mô hình trả lời hai câu hỏi khác nhau:

- **Hồi quy đơn:** Nhìn tổng thể, biến này biến thiên cùng chiều hay ngược chiều với kết quả như thế nào?
- **Hồi quy đa biến:** Khi giữ cố định các biến khác trong mô hình, biến này còn liên hệ với kết quả ở mức độ nào?

## 5. Ví dụ thực tế: dự đoán giá nhà

Giả sử ta mô hình hóa giá nhà theo diện tích, số phòng ngủ và khoảng cách tới trung tâm:

$$
\text{Giá nhà} = \alpha + \beta_1 \cdot \text{Diện tích} + \beta_2 \cdot \text{Số phòng ngủ} + \beta_3 \cdot \text{Khoảng cách} + \epsilon
$$

Mỗi hệ số đều gắn với điều kiện so sánh rõ ràng: $$\beta_1$$ so sánh hai căn nhà cùng số phòng ngủ và cùng khoảng cách tới trung tâm nhưng chênh 1 m² diện tích; $$\beta_2$$ so sánh hai căn cùng diện tích và vị trí nhưng chênh 1 phòng ngủ; $$\beta_3$$ so sánh hai căn cùng diện tích và số phòng ngủ nhưng xa trung tâm hơn 1 km.

### 5.1. Đọc đúng hệ số số phòng ngủ trong mô hình giá nhà

Giả sử mô hình ước lượng được:

$$
\text{Giá nhà} = 1.2 + 0.035 \cdot \text{Diện tích} + 0.18 \cdot \text{Số phòng ngủ} - 0.25 \cdot \text{Khoảng cách},
$$

với giá tính bằng **tỷ đồng**, diện tích tính bằng **m²** và khoảng cách tính bằng **km**. Khi giữ cố định số phòng ngủ và vị trí, căn rộng hơn 10 m² có giá kỳ vọng cao hơn:

$$
0.035 \times 10 = 0.35\ \text{tỷ đồng}.
$$

Khi giữ cố định diện tích và vị trí, căn nhiều hơn 1 phòng ngủ có giá kỳ vọng cao hơn:

$$
0.18\ \text{tỷ đồng}.
$$

Cần lưu ý rằng con số `0.18` chỉ áp dụng khi diện tích và vị trí giữ nguyên (tức chia lại mặt bằng có sẵn thêm một phòng), chứ không phải trong tình huống mở rộng thêm cả diện tích lẫn số phòng ngủ.

## 6. Ba lợi ích chính của hồi quy đa biến

- **Cải thiện độ chính xác dự đoán:** khi biến kết quả phụ thuộc vào nhiều yếu tố, đưa đủ các biến phù hợp giúp giảm sai số dự báo (ví dụ kết hợp giờ học, điểm nền tảng và tỷ lệ chuyên cần để dự đoán điểm thi).
- **Tách bạch ảnh hưởng công bằng hơn:** giúp đánh giá đóng góp riêng của từng yếu tố thay vì dồn mọi biến thiên lên một biến đơn lẻ.
- **Tạo nền tảng cho tư duy nhân quả:** dù bản thân hồi quy đa biến chưa tự động chứng minh quan hệ nhân quả, nó là công cụ để điều chỉnh cho các biến gây nhiễu (confounders) sẽ học ở Bài 5.2.

## 7. Ba rủi ro cần lưu ý khi đưa nhiều biến vào mô hình

- **Bỏ sót biến quan trọng:** thiếu biến có liên quan đến cả biến dự báo lẫn kết quả sẽ làm sai lệch các hệ số còn lại.
- **Các biến dự báo quá giống nhau:** khi hai biến mang thông tin gần như trùng lặp, mô hình khó tách riêng đóng góp của từng biến (chủ đề **đa cộng tuyến** ở Bài 5.3).
- **Đưa biến vào thiếu cân nhắc:** không phải cứ kiểm soát càng nhiều biến càng tốt; có những biến cần điều chỉnh nhưng cũng có những biến nếu đưa vào lại gây thiên lệch (chủ đề **confounding và DAGs** ở Bài 5.2).

## 8. Nhìn hồi quy đa biến như một mô hình sinh dữ liệu

Theo tinh thần Bayes, mỗi quan sát mang một tập đặc trưng riêng; các đặc trưng đó kết hợp để tạo nên giá trị kỳ vọng, còn giá trị quan sát thực tế dao động quanh mức kỳ vọng do các yếu tố chưa quan sát được (như sức khỏe hay tâm lý trong ngày thi). Cách nhìn này giúp ta luôn gắn phương trình toán học với cơ chế thực tế.

## 9. Cách diễn giải kết quả khi báo cáo

Một phát biểu diễn giải chuẩn gồm đủ ba yếu tố: nêu rõ tên biến dự báo, ghi rõ điều kiện "giữ các biến khác cố định" và gắn với đơn vị đo thực tế. Thay vì chỉ viết $$\beta_1 = 0.42$$, hãy diễn đạt:

> Giữ nguyên trình độ học vấn và vị trí công việc, mỗi năm kinh nghiệm tăng thêm đi kèm mức lương kỳ vọng cao hơn khoảng X triệu đồng.

## 10. Kết nối sang các bài tiếp theo

Hồi quy đa biến mở ra ba câu hỏi trọng tâm cho phần còn lại của Chương 5: có biến nào đang gây nhiễu mối quan hệ ta quan tâm không (Bài 5.2), các biến dự báo có trùng lặp thông tin quá mức không (Bài 5.3), và tác động của một biến có thay đổi theo giá trị của biến khác không (Bài 5.4).

> **3 ý cần nhớ.** Hồi quy đa biến cho phép mô tả đồng thời nhiều yếu tố tác động lên biến kết quả; mỗi hệ số luôn phải được đọc kèm điều kiện "giữ các biến khác cố định"; và việc hệ số thay đổi khi thêm biến mới thường phản ánh quá trình tách bạch ảnh hưởng rõ hơn chứ không phải lỗi mô hình.

## Video tham khảo

- [Multiple Regression, Clearly Explained!!!](https://www.youtube.com/watch?v=EkAQAi3a4js) — StatQuest with Josh Starmer, English. **xem trước**. Giải thích từng hệ số là đóng góp có điều kiện khi các biến dự báo khác đã có mặt trong mô hình, khớp với trọng tâm bài học.
- [Statistical Rethinking 2023 - 05 - Elemental Confounds](https://www.youtube.com/watch?v=mBEA7PKDmiY) — Richard McElreath, English. Phân tích vì sao thêm một biến làm thay đổi ý nghĩa hệ số của biến kia, bổ trợ cho mục 4.
- [Covariance and the regression line | Regression | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=ualmyZiPs9w) — Khan Academy, English. Minh họa vai trò của hiệp phương sai trong đường hồi quy, giúp hiểu mối liên hệ giữa các biến dự báo.

## Câu hỏi tự luyện

1. Trong bài toán dự đoán giá nhà, vì sao chỉ dùng biến diện tích thường là chưa đủ?
2. Điều kiện "giữ các biến khác cố định" có ý nghĩa cụ thể như thế nào trong ví dụ lương theo kinh nghiệm và học vấn?
3. Hãy nêu một bài toán thực tế trong lĩnh vực của bạn đòi hỏi ít nhất ba biến dự báo.
4. Trong hoàn cảnh nào một hệ số trong hồi quy đơn sẽ khác biệt đáng kể so với hệ số tương ứng trong hồi quy đa biến?

## Tài liệu tham khảo

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

**Gelman, A., Hill, J., & Vehtari, A. (2020).** *Regression and Other Stories*. Cambridge University Press.

---

*Bài học tiếp theo: [5.2 Confounding và DAGs]({{ site.baseurl }}/contents/vi/chapter05/05_02_confounding_dags/)*
