---
layout: post
title: "Bài 5.4: Interaction Effects - Khi Effects Phụ thuộc Nhau"
chapter: '05'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu interaction effect là gì và vì sao nhiều hiện tượng thực tế không thể được mô tả bằng mô hình cộng đơn giản. Bạn cũng cần biết cách đọc interaction theo kiểu "ảnh hưởng của một biến thay đổi theo bối cảnh của biến khác" thay vì cố ép mọi coefficient thành các hiệu ứng cố định.

> **Ví dụ mini.** Một chương trình luyện thi có thể giúp học sinh khá tiến bộ rất nhanh, nhưng với học sinh mất gốc thì hiệu quả lại nhỏ hơn nếu chưa có học liệu bổ trợ. Khi đó ảnh hưởng của số giờ học không cố định cho mọi người, mà phụ thuộc vào trình độ đầu vào.
>
> **Câu hỏi tự kiểm tra.** Nếu hiệu quả của một predictor thay đổi theo mức của predictor khác, mô hình cộng đơn giản sẽ bỏ sót điều gì?

## 1. Thế giới thật hiếm khi chỉ là "cộng lại"

Trong hồi quy cộng đơn giản, ta viết:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \epsilon
$$

Mô hình này nói rằng:

- ảnh hưởng của $$x_1$$ là như nhau ở mọi mức của $$x_2$$,
- và ảnh hưởng của $$x_2$$ cũng là như nhau ở mọi mức của $$x_1$$.

Nhưng trong thực tế, rất nhiều hiện tượng không vận hành như vậy.

Ví dụ:

- hiệu quả của quảng cáo phụ thuộc vào chất lượng sản phẩm,
- tác động của chế độ ăn phụ thuộc vào mức độ vận động,
- ảnh hưởng của số giờ học phụ thuộc vào nền tảng kiến thức,
- tác động của thuốc phụ thuộc vào độ tuổi hoặc tình trạng bệnh nền.

Khi đó ta cần interaction.

## 2. Interaction effect là gì?

Interaction xảy ra khi ảnh hưởng của một predictor lên outcome **thay đổi theo giá trị của predictor khác**.

Một mô hình có interaction giữa $$x_1$$ và $$x_2$$ thường viết:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \beta_3 (x_1 x_2) + \epsilon
$$

Thành phần mới $$\beta_3 (x_1 x_2)$$ là interaction term.

Nếu $$\beta_3$$ khác 0 một cách đáng kể, điều đó gợi ý rằng:

- slope của $$x_1$$ thay đổi khi $$x_2$$ thay đổi,
- hoặc nhìn ngược lại, slope của $$x_2$$ thay đổi khi $$x_1$$ thay đổi.

![Interaction effects]({{ site.baseurl }}/img/chapter_img/chapter05/interaction_effects.png)

## 3. Nhìn bằng hình sẽ dễ hiểu hơn nhìn bằng công thức

![Interaction demo]({{ site.baseurl }}/img/chapter_img/chapter05/interaction_demo.png)

Hãy so sánh hai tình huống:

### Mô hình additive

Các đường gần như song song.

Điều đó có nghĩa:

- khác nhóm thì mức nền có thể khác,
- nhưng tác động của $$x_1$$ lên $$y$$ gần như giống nhau giữa các nhóm.

### Mô hình có interaction

Các đường có slope khác nhau rõ rệt.

Điều đó có nghĩa:

- cùng tăng một đơn vị $$x_1$$,
- nhưng outcome tăng mạnh hay yếu còn tùy vào mức của $$x_2$$.

Đây chính là trực giác cốt lõi của interaction.

## 4. Ví dụ thực tế để thấy interaction rõ hơn

### Ví dụ 1: thời gian học và trình độ đầu vào

Outcome là điểm cuối kỳ.

Predictors:

- số giờ học mỗi tuần,
- trình độ đầu vào.

Nếu học sinh đã có nền tảng tốt, thêm 1 giờ học có thể giúp tăng điểm khá rõ. Nhưng với học sinh mất gốc, thêm 1 giờ học chưa chắc tạo khác biệt lớn nếu các lỗ hổng kiến thức cơ bản chưa được lấp.

Khi đó:

- ảnh hưởng của giờ học phụ thuộc vào trình độ đầu vào,
- nên interaction là hợp lý.

### Ví dụ 2: quảng cáo và chất lượng sản phẩm

Quảng cáo có thể hiệu quả hơn nhiều khi sản phẩm vốn đã tốt. Nếu sản phẩm kém, tăng quảng cáo có thể chỉ giúp người ta biết đến sản phẩm nhanh hơn chứ không giúp chuyển đổi bền vững.

Tức là:

- effect của ngân sách quảng cáo phụ thuộc vào chất lượng sản phẩm.

### Ví dụ 3: điều trị và mức độ bệnh

Một phác đồ có thể rất hiệu quả với ca nhẹ nhưng ít hiệu quả hơn với ca rất nặng, hoặc ngược lại. Khi đó effect của treatment thay đổi theo severity.

## 5. Cách đọc interaction cho đúng

Sai lầm phổ biến nhất là cố đọc $$\beta_1$$ như một hiệu ứng chung cố định, dù mô hình đã có interaction.

Khi có interaction:

$$
\frac{\partial y}{\partial x_1} = \beta_1 + \beta_3 x_2
$$

Điều này nói rằng ảnh hưởng của $$x_1$$ **không phải một con số duy nhất** nữa. Nó phụ thuộc vào $$x_2$$.

### Ví dụ với biến nhị phân

Nếu $$x_2$$ là biến nhóm với:

- $$x_2 = 0$$: nhóm đối chứng,
- $$x_2 = 1$$: nhóm can thiệp,

thì:

- ở nhóm đối chứng, effect của $$x_1$$ là $$\beta_1$$,
- ở nhóm can thiệp, effect của $$x_1$$ là $$\beta_1 + \beta_3$$.

Nghĩa là interaction cho ta biết mức độ mà intervention làm mạnh hơn hoặc yếu đi ảnh hưởng của $$x_1$$.

![Conditional effects]({{ site.baseurl }}/img/chapter_img/chapter05/conditional_effects.png)

## 6. Interaction không chỉ dành cho biến nhị phân

Interaction cũng rất thường gặp giữa hai biến liên tục.

Ví dụ:

- nhiệt độ và độ ẩm cùng ảnh hưởng đến mức tiêu thụ điện,
- thu nhập và tuổi cùng ảnh hưởng đến hành vi chi tiêu,
- thời gian học và chất lượng giấc ngủ cùng ảnh hưởng đến điểm thi.

![Continuous interaction]({{ site.baseurl }}/img/chapter_img/chapter05/continuous_interaction.png)

Trong trường hợp continuous x continuous, hình ảnh như contour plot hoặc surface plot thường trực quan hơn bảng hệ số rất nhiều. Vì thế, interaction là một chủ đề mà **visualization gần như bắt buộc**.

## 7. Khi nào nên nghĩ đến interaction?

### 7.1. Khi lý thuyết chuyên môn gợi ý

Nếu hiểu biết ngành nói rằng effect thay đổi theo bối cảnh, interaction nên được xem xét.

Ví dụ:

- thuốc và tuổi,
- đào tạo và trình độ nền,
- giá và phân khúc khách hàng.

### 7.2. Khi đồ thị gợi ý các slope khác nhau

Nếu bạn vẽ dữ liệu theo nhóm và thấy các đường không song song, đó là tín hiệu rất rõ.

### 7.3. Khi mô hình cộng đơn giản để lại residual có cấu trúc

Một số pattern residual có thể cho thấy model đang bỏ sót sự phụ thuộc giữa các predictors.

## 8. Điều người mới học hay hiểu nhầm

### Hiểu nhầm 1: "Main effect không còn ý nghĩa nữa"

Không hẳn. Main effect vẫn có nghĩa, nhưng nghĩa của nó phụ thuộc vào cách bạn mã hóa và center variables.

Ví dụ:

- nếu biến liên tục được center quanh giá trị trung bình,
- thì main effect thường là ảnh hưởng của predictor tại mức trung bình của biến kia.

Đây là lý do việc standardize hoặc center predictors thường rất hữu ích trước khi diễn giải interaction.

### Hiểu nhầm 2: "Có interaction thì phải bỏ main effects"

Thông thường không nên làm vậy. Interaction thường đi cùng main effects để mô hình còn giữ được ý nghĩa diễn giải cơ bản.

### Hiểu nhầm 3: "Chỉ cần nhìn vào p-value hay interval của interaction là đủ"

Chưa đủ. Với interaction, hình vẽ và conditional effects quan trọng ngang hoặc hơn con số tóm tắt.

## 9. Một ví dụ gần gũi: tập luyện và chế độ ăn

Giả sử outcome là số kg giảm trong 8 tuần.

Predictors:

- số buổi tập mỗi tuần,
- mức độ tuân thủ chế độ ăn.

Nếu ăn uống rất kém, tăng thêm 1 buổi tập có thể chỉ cải thiện nhỏ. Nhưng nếu chế độ ăn được giữ tốt, cùng 1 buổi tập thêm đó có thể tạo khác biệt lớn hơn.

Đây là kiểu tình huống mà mô hình cộng:

$$
\text{Giảm cân} = \alpha + \beta_1 \cdot \text{Tập luyện} + \beta_2 \cdot \text{Chế độ ăn} + \epsilon
$$

có thể bỏ sót một phần quan trọng của câu chuyện.

Mô hình có interaction sẽ hợp lý hơn:

$$
\text{Giảm cân} = \alpha + \beta_1 \cdot \text{Tập luyện} + \beta_2 \cdot \text{Chế độ ăn} + \beta_3 \cdot (\text{Tập luyện} \times \text{Chế độ ăn}) + \epsilon
$$

## 10. Cách báo cáo interaction cho người không chuyên

Đừng bắt đầu bằng:

> interaction coefficient bằng 0.63.

Hãy bắt đầu bằng ngôn ngữ tình huống:

> Tác động của giờ học không giống nhau cho mọi học sinh. Ở nhóm có nền tảng tốt, thêm thời gian học đi kèm mức tăng điểm mạnh hơn rõ rệt so với nhóm nền tảng yếu.

Sau đó mới đưa ra con số nếu cần.

Kiểu diễn giải này giúp người đọc hiểu bản chất hiện tượng trước, rồi mới xem phần định lượng.

## 11. Chapter 5 khép lại ở đây

Đến cuối chapter này, bạn đã có một bộ công cụ rất quan trọng để đọc hồi quy cho đúng:

- nhiều predictors cùng lúc,
- confounding và causal structure,
- multicollinearity,
- interaction effects.

Đây là lúc hồi quy thôi không còn là "vẽ một đường thẳng", mà trở thành một cách suy nghĩ về cơ chế tạo dữ liệu.

> **3 ý cần nhớ.**
>
> Interaction xảy ra khi ảnh hưởng của một predictor thay đổi theo mức của predictor khác, nên không thể luôn diễn giải hiệu ứng như một con số cố định cho mọi trường hợp.
>
> Khi mô hình có interaction, cách đọc tốt nhất là đọc theo conditional effects và dùng hình minh họa thay vì chỉ nhìn bảng coefficients.
>
> Interaction rất thường gặp trong đời sống thật vì hiệu quả của can thiệp, hành vi hay điều kiện hiếm khi giống nhau trong mọi bối cảnh.

## Câu hỏi tự luyện

1. Hãy nêu một ví dụ trong đời sống mà ảnh hưởng của một biến phụ thuộc rõ vào một biến khác.
2. Vì sao các đường không song song trên biểu đồ nhóm là dấu hiệu có thể có interaction?
3. Trong ví dụ giờ học và trình độ đầu vào, interaction giúp mô tả điều gì mà mô hình additive bỏ sót?
4. Nếu biến liên tục không được center, việc diễn giải main effects trong mô hình interaction có thể khó ở điểm nào?

## Tài liệu tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

---

*Chương tiếp theo: [Chapter 06: Model Comparison](/vi/chapter06/)*
