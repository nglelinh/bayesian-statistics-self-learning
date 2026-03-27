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

Sau bài này, bạn cần hiểu vì sao nhiều bài toán thực tế không thể dùng chỉ một predictor (biến dự báo). Bạn cũng cần nắm ý nghĩa quan trọng nhất của multiple regression (hồi quy nhiều biến), tức là mỗi hệ số chỉ nên được đọc như ảnh hưởng của một biến khi các biến còn lại được giữ cố định. Đây là nền tảng để đọc đúng kết quả hồi quy ở các bài sau.

> **Ví dụ mini.** Một công ty muốn dự đoán lương của nhân viên. Nếu chỉ nhìn số năm kinh nghiệm, ta sẽ bỏ sót bằng cấp, vị trí công việc và khu vực sống. Multiple regression cho phép đưa nhiều yếu tố vào cùng lúc để bức tranh công bằng và sát thực tế hơn.
>
> **Câu hỏi tự kiểm tra.** Nếu hai người có cùng số năm kinh nghiệm nhưng học vấn khác nhau, một mô hình chỉ có một predictor có mô tả được khác biệt lương giữa họ không?

## 1. Vì sao một predictor thường là chưa đủ?

Trong Chapter 4, ta học mô hình hồi quy tuyến tính đơn:

$$
y = \alpha + \beta x + \epsilon
$$

Mô hình này rất hữu ích để học trực giác, nhưng thế giới thật hiếm khi đơn giản như vậy. Điểm thi chẳng hạn không chỉ phụ thuộc vào số giờ học, mà còn phụ thuộc vào nền tảng kiến thức, chất lượng giấc ngủ và độ khó đề; giá nhà không chỉ phụ thuộc vào diện tích, mà còn phụ thuộc vào vị trí, tuổi căn nhà, số phòng ngủ và hạ tầng xung quanh; còn cân nặng thì không chỉ liên quan đến chiều cao, mà còn liên quan đến tuổi, giới tính, mức độ vận động và chế độ ăn. Nếu ta cố ép một bài toán nhiều nguyên nhân thành mô hình một biến, ta rất dễ vừa bỏ sót thông tin quan trọng, vừa giải thích sai ý nghĩa của hệ số.

Multiple regression ra đời để xử lý chính tình huống này.

## 2. Mô hình nhiều predictors trông như thế nào?

Mô hình tổng quát là:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_k x_k + \epsilon
$$

Trong đó, $$y$$ là outcome (biến kết quả), $$x_1, x_2, \ldots, x_k$$ là các predictors (biến dự báo), $$\alpha$$ là intercept (hệ số chặn), còn mỗi $$\beta_j$$ là hệ số của predictor thứ $$j$$. Ý tưởng của mô hình này rất tự nhiên: ta cộng đóng góp của từng predictor rồi cộng thêm phần nhiễu $$\epsilon$$, bởi vì dữ liệu thật luôn dao động quanh xu hướng trung bình chứ không bao giờ nằm chính xác trên một công thức cứng.

Ba góc nhìn dưới đây cho thấy cùng một outcome có thể được nhìn như nhiều lát cắt hai chiều hoặc như một bề mặt nhiều chiều.

![Cân nặng theo chiều cao, tô màu theo tuổi]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_vs_height_colored_by_age.png)

![Cân nặng theo tuổi, tô màu theo chiều cao]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_vs_age_colored_by_height.png)

![Góc nhìn 3D của cân nặng theo chiều cao và tuổi]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_weight_height_age_3d.png)

Ba hình trên giúp ta thấy một outcome có thể thay đổi theo **nhiều chiều cùng lúc**. Khi nhìn từng đồ thị hai chiều riêng lẻ, ta chỉ thấy một lát cắt của vấn đề. Multiple regression cố gắng ghép các lát cắt đó lại thành một mô hình chung.

## 3. Ý nghĩa quan trọng nhất: "giữ các biến khác cố định"

Đây là ý khó nhất nhưng cũng là ý quan trọng nhất của cả chapter này.

Trong multiple regression, hệ số $$\beta_1$$ không còn nghĩa là:

> cứ $$x_1$$ tăng một đơn vị thì $$y$$ tăng $$\beta_1$$ đơn vị.

Nghĩa đúng là:

> khi các predictor khác được giữ cố định, nếu $$x_1$$ tăng một đơn vị thì $$y$$ thay đổi trung bình khoảng $$\beta_1$$ đơn vị.

Nghe có vẻ chỉ thêm vài chữ, nhưng ý nghĩa thay đổi rất lớn.

### Ví dụ 1: lương, kinh nghiệm và học vấn

Giả sử ta có mô hình:

$$
\text{Lương} = \alpha + \beta_1 \cdot \text{Kinh nghiệm} + \beta_2 \cdot \text{Học vấn} + \epsilon
$$

Khi đó, $$\beta_1$$ phải được đọc là chênh lệch lương kỳ vọng giữa hai người có **cùng học vấn** nhưng khác nhau một năm kinh nghiệm, còn $$\beta_2$$ là chênh lệch lương kỳ vọng giữa hai người có **cùng số năm kinh nghiệm** nhưng khác nhau một bậc học vấn. Đây là cách đọc thực tế hơn rất nhiều so với việc trộn tất cả các khác biệt vào một hệ số duy nhất.

### Ví dụ 2: cân nặng, chiều cao và tuổi

Nếu mô hình là:

$$
\text{Cân nặng} = \alpha + \beta_1 \cdot \text{Chiều cao} + \beta_2 \cdot \text{Tuổi} + \epsilon
$$

thì $$\beta_1$$ nói về ảnh hưởng của chiều cao giữa những người cùng độ tuổi, còn $$\beta_2$$ nói về ảnh hưởng của tuổi giữa những người cùng chiều cao. Nói ngắn gọn, multiple regression luôn so sánh theo kiểu "**mọi thứ khác như nhau, chỉ thay đổi một biến**".

### 3.1. Một ví dụ bằng con số để đọc hệ số cho đúng

Giả sử ta fit được mô hình lương theo kinh nghiệm và học vấn như sau:

$$
\text{Lương} = 8 + 0.6 \cdot \text{Kinh nghiệm} + 2.5 \cdot \text{Sau đại học}.
$$

Ở đây:

- `Kinh nghiệm` được tính bằng số năm,
- `Sau đại học = 1` nếu có bằng sau đại học, và `= 0` nếu không,
- lương tính bằng triệu đồng mỗi tháng.

Khi đó:

- nếu hai người có **cùng học vấn**, người nhiều hơn 1 năm kinh nghiệm có mức lương kỳ vọng cao hơn khoảng **0.6 triệu/tháng**,
- nếu hai người có **cùng số năm kinh nghiệm**, người có bằng sau đại học có mức lương kỳ vọng cao hơn khoảng **2.5 triệu/tháng**.

Ví dụ cụ thể:

- Người A: 5 năm kinh nghiệm, không có bằng sau đại học  
  $$8 + 0.6 \times 5 + 2.5 \times 0 = 11$$
- Người B: 6 năm kinh nghiệm, không có bằng sau đại học  
  $$8 + 0.6 \times 6 + 2.5 \times 0 = 11.6$$
- Người C: 5 năm kinh nghiệm, có bằng sau đại học  
  $$8 + 0.6 \times 5 + 2.5 \times 1 = 13.5$$

So sánh A với B cho ta cách đọc hệ số kinh nghiệm. So sánh A với C cho ta cách đọc hệ số học vấn. Đây chính là logic "giữ các biến khác cố định" được viết ra thành con số.

## 4. Vì sao hệ số trong simple regression và multiple regression có thể khác nhau?

Đây là điều khiến nhiều người mới học bị bối rối.

Một predictor trong simple regression có thể mang theo ảnh hưởng của những biến chưa đưa vào mô hình.

Ví dụ về lương cho thấy điều này rất rõ: nếu người học cao hơn thường cũng có kinh nghiệm nhiều hơn, thì mô hình chỉ dùng học vấn có thể "gom" luôn một phần ảnh hưởng của kinh nghiệm vào hệ số học vấn.

Khi thêm kinh nghiệm vào mô hình, hệ số học vấn có thể giảm xuống. Điều này không có nghĩa là mô hình mới tệ hơn. Ngược lại, nó thường có nghĩa là mô hình mới đang tách bạch các nguồn ảnh hưởng rõ hơn.

### Một cách nghĩ trực giác

Simple regression trả lời:

> nhìn tổng thể, biến này đi cùng outcome như thế nào?

Multiple regression trả lời:

> nếu ta cố giữ các yếu tố khác ổn định, biến này còn liên quan đến outcome như thế nào?

Hai câu hỏi này khác nhau, nên câu trả lời khác nhau là chuyện bình thường.

## 5. Một ví dụ thực tế: dự đoán giá nhà

Giả sử ta muốn dự đoán giá nhà từ ba biến là diện tích, số phòng ngủ và khoảng cách tới trung tâm.

Một mô hình hợp lý là:

$$
\text{Giá nhà} = \alpha + \beta_1 \cdot \text{Diện tích} + \beta_2 \cdot \text{Số phòng ngủ} + \beta_3 \cdot \text{Khoảng cách} + \epsilon
$$

Diễn giải đúng ở đây là: $$\beta_1$$ cho biết giữa hai căn nhà có cùng số phòng ngủ và cùng khoảng cách tới trung tâm, căn rộng hơn 1 mét vuông thì giá kỳ vọng chênh bao nhiêu; $$\beta_2$$ cho biết giữa hai căn có cùng diện tích và vị trí, thêm 1 phòng ngủ thì giá kỳ vọng đổi thế nào; còn $$\beta_3$$ cho biết giữa hai căn có cùng diện tích và số phòng, căn xa trung tâm hơn 1 km thì giá kỳ vọng chênh bao nhiêu.

Nếu không nói rõ "giữ các biến khác cố định", người đọc rất dễ hiểu nhầm hệ số.

### 5.1. Vì sao cùng thêm 1 phòng ngủ mà không phải lúc nào giá cũng tăng như nhau?

Giả sử mô hình ước lượng được:

$$
\text{Giá nhà} = 1.2 + 0.035 \cdot \text{Diện tích} + 0.18 \cdot \text{Số phòng ngủ} - 0.25 \cdot \text{Khoảng cách},
$$

trong đó giá tính bằng **tỷ đồng**, diện tích tính bằng **m²**, còn khoảng cách tới trung tâm tính bằng **km**.

Khi đó, nếu so sánh hai căn nhà có cùng số phòng ngủ và cùng vị trí, căn rộng hơn 10 m² sẽ có giá kỳ vọng cao hơn khoảng:

$$
0.035 \times 10 = 0.35\ \text{tỷ đồng}.
$$

Nếu so sánh hai căn có cùng diện tích và cùng vị trí, căn nhiều hơn 1 phòng ngủ sẽ có giá kỳ vọng cao hơn khoảng:

$$
0.18\ \text{tỷ đồng}.
$$

Nhưng chú ý: hệ số `0.18` này không có nghĩa là "ở mọi hoàn cảnh, cứ thêm 1 phòng ngủ là giá tăng 180 triệu". Nó chỉ đúng cho phép so sánh giữa những căn **đã được giữ cố định diện tích và vị trí**. Trong dữ liệu thật, một phòng ngủ thêm thường cũng đi kèm nhà rộng hơn, nên nếu quên điều kiện này ta sẽ đọc hệ số sai rất nhanh.

## 6. Multiple regression giúp gì cho ta?

### 6.1. Dự đoán tốt hơn

Khi outcome thực sự phụ thuộc vào nhiều yếu tố, thêm predictors phù hợp thường giúp dự đoán sát hơn. Chẳng hạn, dự đoán điểm thi từ chỉ số giờ học thường sẽ kém hơn dự đoán từ giờ học kết hợp với điểm nền tảng và tỷ lệ đi học.

### 6.2. Giải thích công bằng hơn

Ta có thể tách ảnh hưởng của từng biến thay vì đổ mọi thứ lên một predictor duy nhất. Ví dụ, nếu muốn đánh giá hiệu quả một khóa học, ta nên xét đồng thời thời gian học, mức độ tham gia và trình độ đầu vào thay vì chỉ nhìn một thước đo đơn lẻ.

### 6.3. Chuẩn bị cho causal thinking

Multiple regression chưa tự động tạo ra nhân quả, nhưng nó là bước đầu để học cách điều chỉnh cho các biến liên quan, so sánh công bằng hơn giữa các nhóm, và suy nghĩ nghiêm túc về confounding (hiện tượng gây nhiễu) trong bài tiếp theo.

## 7. Điều gì cần cẩn thận khi dùng nhiều predictors?

Thêm nhiều biến không phải lúc nào cũng tốt. Có ít nhất ba tình huống mà ta cần đặc biệt cảnh giác.

### 7.1. Bỏ sót biến quan trọng

Nếu biến quan trọng bị bỏ ra ngoài, các hệ số còn lại có thể bị méo.

### 7.2. Các predictors quá giống nhau

Nếu hai biến gần như đo cùng một thứ, mô hình sẽ khó tách riêng ảnh hưởng của từng biến. Đây là chủ đề của bài 5.3 về multicollinearity.

### 7.3. Đưa biến vào mà không suy nghĩ

Không phải cứ "control cho mọi thứ" là tốt. Có những biến nên đưa vào, nhưng cũng có những biến không nên đưa vào. Đây là nội dung của bài 5.2 về confounding và DAGs.

## 8. Nhìn multiple regression như một câu chuyện sinh dữ liệu

Một cách hiểu theo tinh thần Bayes là xem mô hình như một câu chuyện trong đó mỗi đối tượng có các đặc trưng khác nhau, từng đặc trưng đóng góp một phần vào outcome, và phần còn lại là dao động mà mô hình không giải thích hết được. Với điểm thi, điều này có nghĩa là mỗi sinh viên có số giờ học, điểm đầu vào và tỷ lệ chuyên cần khác nhau; các yếu tố đó kết hợp để tạo ra mức điểm kỳ vọng; còn kết quả thật vẫn dao động thêm vì sức khỏe, tâm lý phòng thi và các yếu tố ngẫu nhiên khác.

Khi nghĩ theo cách này, công thức không còn là ký hiệu khô khan, mà là bản tóm tắt của một quá trình thực tế.

## 9. Khi báo cáo kết quả, nên diễn giải thế nào?

Một cách diễn giải tốt thường có ba phần gắn liền nhau: gọi tên predictor rõ ràng, nói kèm điều kiện "giữ các biến khác cố định", rồi gắn kết quả với đơn vị thực tế thay vì chỉ để lại một hệ số trừu tượng.

Ví dụ:

> Giữ nguyên học vấn và vị trí công việc, mỗi năm kinh nghiệm tăng thêm đi kèm mức lương kỳ vọng cao hơn khoảng X triệu đồng.

Kiểu diễn giải này rõ ràng hơn nhiều so với việc chỉ nói:

> $$\beta_1 = 0.42$$.

## 10. Kết nối sang các bài tiếp theo

Multiple regression là cánh cửa mở sang ba câu hỏi rất thực tế, đó là liệu có biến nào đang làm méo mối quan hệ mình quan tâm hay không, liệu các predictors có giống nhau quá nhiều hay không, và liệu ảnh hưởng của một biến có phụ thuộc vào biến khác hay không. Hiểu chắc bài này sẽ giúp bạn không bị "ngợp" khi chuyển sang confounding, multicollinearity và interaction ở ba bài tiếp theo.

> **3 ý cần nhớ.** Multiple regression cho phép mô tả outcome bằng nhiều predictors cùng lúc, nên phù hợp hơn với các bài toán thực tế; mỗi hệ số trong multiple regression luôn phải được đọc kèm điều kiện "giữ các biến khác cố định"; và khi hệ số thay đổi sau khi thêm predictor mới, đó thường là dấu hiệu mô hình đang tách bạch ảnh hưởng tốt hơn chứ không phải dấu hiệu mô hình sai.

## Câu hỏi tự luyện

1. Trong bài toán dự đoán giá nhà, vì sao chỉ dùng diện tích thường là chưa đủ?
2. "Giữ các biến khác cố định" có ý nghĩa gì trong ví dụ lương theo kinh nghiệm và học vấn?
3. Hãy nghĩ ra một bài toán thực tế trong ngành của bạn cần ít nhất ba predictors.
4. Khi nào một hệ số trong simple regression có thể khác khá xa hệ số tương ứng trong multiple regression?

## Tài liệu tham khảo

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

**Gelman, A., Hill, J., & Vehtari, A. (2020).** *Regression and Other Stories*. Cambridge University Press.

---

*Bài học tiếp theo: [5.2 Confounding và DAGs](/vi/chapter05/confounding-dags/)*
