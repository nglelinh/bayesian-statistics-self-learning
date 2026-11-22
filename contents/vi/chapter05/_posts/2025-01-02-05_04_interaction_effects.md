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

Sau bài này, bạn sẽ hiểu hiệu ứng tương tác (interaction effect) là gì và vì sao nhiều hiện tượng thực tế không thể mô tả đầy đủ bằng mô hình cộng đơn giản. Bạn cũng sẽ biết cách diễn giải tương tác theo hiệu ứng có điều kiện — tức tác động của một biến thay đổi tùy theo giá trị của biến khác — thay vì xem mọi hệ số là hằng số cố định.

> **Ví dụ ngắn.** Một chương trình luyện thi có thể giúp học sinh có nền tảng khá tiến bộ rất nhanh, nhưng lại kém hiệu quả hơn ở học sinh mất gốc nếu chưa được bổ sung kiến thức cơ bản. Khi đó, tác động của số giờ học không cố định cho mọi học sinh mà phụ thuộc vào trình độ đầu vào.
>
> **Câu hỏi tự kiểm tra.** Nếu tác động của một biến dự báo thay đổi theo mức của một biến dự báo khác, mô hình cộng đơn giản sẽ bỏ sót điều gì?

## 1. Các yếu tố trong thực tế hiếm khi chỉ cộng dồn độc lập

Mô hình hồi quy cộng (additive model) có dạng:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \epsilon
$$

Cấu trúc này giả định tác động của $$x_1$$ lên $$y$$ hoàn toàn giống nhau ở mọi mức của $$x_2$$, và ngược lại. Tuy nhiên, trong thực tế nhiều mối quan hệ phụ thuộc lẫn nhau: hiệu quả quảng cáo phụ thuộc vào chất lượng sản phẩm, tác động của chế độ ăn phụ thuộc vào mức độ vận động, hiệu quả của giờ học phụ thuộc vào kiến thức nền tảng và hiệu quả thuốc phụ thuộc vào độ tuổi hay bệnh nền. Để mô tả những tình huống này, ta cần đưa hạng tương tác vào mô hình.

## 2. Hiệu ứng tương tác (Interaction Effect) là gì?

Hiệu ứng tương tác xảy ra khi tác động của một biến dự báo lên biến kết quả **thay đổi theo giá trị của một biến dự báo khác**. Mô hình có tương tác giữa $$x_1$$ và $$x_2$$ được viết là:

$$
y = \alpha + \beta_1 x_1 + \beta_2 x_2 + \beta_3 (x_1 x_2) + \epsilon
$$

Số hạng mới $$\beta_3 (x_1 x_2)$$ gọi là **hạng tương tác (interaction term)**. Khi $$\beta_3$$ khác 0 đáng kể, hệ số dốc của $$x_1$$ sẽ thay đổi theo giá trị của $$x_2$$ (và tương tự, hệ số dốc của $$x_2$$ thay đổi theo $$x_1$$).

![Trường hợp không có interaction: các đường gần song song]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_no_interaction_parallel_lines.png)

![Trường hợp có interaction: slope thay đổi theo nhóm]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_with_interaction_different_slopes.png)

![So sánh mô hình có và không có interaction]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_interaction_model_comparison.png)

## 3. Phân biệt mô hình cộng và mô hình tương tác bằng đồ thị

![Mô hình additive với các đường gần song song]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_additive_model_demo.png)

![Mô hình interactive với các slope khác nhau]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_interactive_model_demo.png)

Nhìn trực quan trên đồ thị giúp nhận diện ngay sự khác biệt giữa hai mô hình:

- **Mô hình cộng (additive):** các đường hồi quy giữa các nhóm song song với nhau. Mức nền (hệ số chặn) có thể khác nhau giữa các nhóm, nhưng độ dốc của $$x_1$$ là như nhau.
- **Mô hình có tương tác:** các đường hồi quy có độ dốc khác nhau rõ rệt. Cùng tăng thêm một đơn vị $$x_1$$, mức thay đổi của $$y$$ mạnh hay yếu còn tùy thuộc vào mức của $$x_2$$.

## 4. Ba ví dụ thực tế về hiệu ứng tương tác

- **Thời gian học và trình độ đầu vào:** học sinh đã có kiến thức nền tốt có thể tăng điểm rõ rệt khi học thêm 1 giờ mỗi tuần, trong khi học sinh mất gốc có thể cần lấp lỗ hổng cơ bản trước khi giờ học thêm phát huy tác dụng tương đương.
- **Ngân sách quảng cáo và chất lượng sản phẩm:** tăng chi tiêu quảng cáo mang lại doanh thu bền vững hơn nhiều khi sản phẩm có chất lượng tốt; với sản phẩm kém, quảng cáo mạnh có thể chỉ làm lộ nhược điểm nhanh hơn mà không giữ được khách hàng.
- **Phác đồ điều trị và mức độ bệnh:** một phương pháp điều trị có thể đạt hiệu quả cao ở nhóm bệnh nhẹ nhưng giảm tác dụng ở nhóm bệnh nặng (hoặc ngược lại).

### Thử nghiệm: từ mô hình cộng đến mô hình có tương tác

So sánh ba bước mở rộng: một đường chung $$\to$$ hai đường song song $$\to$$ hai đường khác độ dốc, và quan sát tổng bình phương phần dư (RSS) thay đổi ra sao.

<div class="interactive-demo" markdown="1">
<div data-demo="confound-explainer" data-lang="vi" data-tab="interaction"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 5. Cách diễn giải mô hình có tương tác

Sai lầm phổ biến nhất là đọc $$\beta_1$$ như một tác động chung cố định dù mô hình đã chứa hạng tương tác. Đạo hàm riêng theo $$x_1$$ cho thấy:

$$
\frac{\partial y}{\partial x_1} = \beta_1 + \beta_3 x_2
$$

Như vậy, ảnh hưởng của $$x_1$$ không còn là một hằng số mà là một hàm phụ thuộc vào $$x_2$$.

Khi $$x_2$$ là biến nhị phân ($$x_2 = 0$$ cho nhóm đối chứng và $$x_2 = 1$$ cho nhóm can thiệp), tác động của $$x_1$$ ở nhóm đối chứng là $$\beta_1$$, còn ở nhóm can thiệp là $$\beta_1 + \beta_3$$. Hệ số $$\beta_3$$ đo chính xác mức chênh lệch về độ dốc giữa hai nhóm.

![Conditional effects của x₁ theo từng nhóm x₂]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_conditional_effects_by_group.png)

![Interaction như chênh lệch giữa hai conditional effects]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_interaction_difference_distribution.png)

### 5.1. Ví dụ bằng con số

Giả sử mô hình điểm cuối kỳ có dạng:

$$
\text{Điểm} = 4 + 0.2 \cdot \text{Giờ học} + 1.0 \cdot \text{Nền tảng tốt} + 0.25 \cdot (\text{Giờ học} \times \text{Nền tảng tốt}),
$$

trong đó `Nền tảng tốt = 0` ứng với nhóm mất gốc và `= 1` ứng với nhóm có kiến thức nền ổn định. Khi đó, mỗi giờ học tăng thêm giúp nhóm mất gốc tăng trung bình **0.2 điểm**, còn nhóm nền tảng tốt tăng trung bình $$0.2 + 0.25 = 0.45$$ điểm.

Kiểm tra qua bốn trường hợp cụ thể:

- Học sinh mất gốc, học 2 giờ: $$4 + 0.2 \times 2 = 4.4$$ điểm.
- Học sinh nền tảng tốt, học 2 giờ: $$4 + 0.2 \times 2 + 1 + 0.25 \times 2 = 5.9$$ điểm.
- Học sinh mất gốc, học 6 giờ: $$4 + 0.2 \times 6 = 5.2$$ điểm (tăng 0.8 điểm so với mức 2 giờ).
- Học sinh nền tảng tốt, học 6 giờ: $$4 + 0.2 \times 6 + 1 + 0.25 \times 6 = 7.7$$ điểm (tăng 1.8 điểm so với mức 2 giờ).

Mức tăng điểm khi nâng từ 2 lên 6 giờ học khác nhau rõ rệt giữa hai nhóm — đó chính là biểu hiện định lượng của hiệu ứng tương tác.

## 6. Tương tác giữa hai biến liên tục

Hiệu ứng tương tác không chỉ giới hạn ở biến nhị phân mà còn xuất hiện phổ biến giữa hai biến liên tục, chẳng hạn nhiệt độ và độ ẩm cùng ảnh hưởng đến tiêu thụ điện, thu nhập và độ tuổi cùng ảnh hưởng đến chi tiêu, hay thời gian học và chất lượng giấc ngủ cùng ảnh hưởng đến điểm thi.

![Các đường hiệu ứng khi cả hai biến đều liên tục]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_interaction_continuous_lines.png)

![Góc nhìn 3D của tương tác giữa hai biến liên tục]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_continuous_interaction_3d.png)

![Contour plot của tương tác giữa hai biến liên tục]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_continuous_interaction_contour.png)

Với tương tác giữa hai biến liên tục, các đồ thị trực quan như biểu đồ đường đồng mức (contour plot), biểu đồ bề mặt 3D hoặc đồ thị hiệu ứng có điều kiện tại vài mức tiêu biểu của biến kia dễ đọc hơn nhiều so với bảng hệ số thuần túy.

## 7. Khi nào nên cân nhắc đưa hạng tương tác vào mô hình?

- **Khi kiến thức chuyên môn gợi ý:** cơ chế thực tế cho thấy tác động của một yếu tố thay đổi theo bối cảnh (như thuốc theo độ tuổi, đào tạo theo trình độ nền hay giá bán theo phân khúc khách hàng).
- **Khi đồ thị phân nhóm cho thấy độ dốc khác nhau:** các đường xu hướng theo từng nhóm không song song.
- **Khi mô hình cộng để lại phần dư có cấu trúc:** phần dư thể hiện sự phụ thuộc hệ thống giữa các biến dự báo.

## 8. Ba hiểu lầm thường gặp

- **"Có hạng tương tác thì hiệu ứng chính (main effect) mất ý nghĩa":** không đúng. Hiệu ứng chính vẫn có ý nghĩa, nhưng phụ thuộc vào cách mã hóa và dịch tâm biến. Nếu dịch tâm các biến liên tục quanh giá trị trung bình, hệ số chính $$\beta_1$$ chính là tác động của $$x_1$$ tại mức trung bình của $$x_2$$.
- **"Đưa hạng tương tác vào thì có thể bỏ hiệu ứng chính":** thông thường luôn nên giữ lại cả các hiệu ứng chính để mô hình duy trì tính nhất quán và khả năng diễn giải.
- **"Chỉ cần xem khoảng tin cậy của $$\beta_3$$ là đủ":** chưa đủ; trực quan hóa hiệu ứng có điều kiện (conditional effects) giúp nắm bắt bản chất tương tác rõ ràng hơn nhiều.

## 9. Ví dụ gần gũi: tập luyện và chế độ ăn

Xét bài toán giảm cân trong 8 tuần theo số buổi tập mỗi tuần và mức độ tuân thủ chế độ ăn. Nếu chế độ ăn kém, tăng thêm 1 buổi tập có thể chỉ mang lại thay đổi nhỏ; nhưng khi chế độ ăn được kiểm soát tốt, cùng 1 buổi tập thêm có thể tạo khác biệt lớn hơn. Mô hình cộng:

$$
\text{Giảm cân} = \alpha + \beta_1 \cdot \text{Tập luyện} + \beta_2 \cdot \text{Chế độ ăn} + \epsilon
$$

sẽ bỏ qua sự cộng hưởng này, trong khi mô hình có tương tác:

$$
\text{Giảm cân} = \alpha + \beta_1 \cdot \text{Tập luyện} + \beta_2 \cdot \text{Chế độ ăn} + \beta_3 \cdot (\text{Tập luyện} \times \text{Chế độ ăn}) + \epsilon
$$

cho phép kiểm chứng trực tiếp cơ chế: nếu $$\beta_3 > 0$$, hai yếu tố **khuếch đại** nhau; ngược lại nếu $$\beta_3 < 0$$, chúng có xu hướng **bù trừ** hoặc thay thế một phần cho nhau.

## 10. Trình bày kết quả tương tác cho người đọc không chuyên

Thay vì mở đầu bằng con số kỹ thuật kiểu "hệ số tương tác bằng 0.63", hãy diễn đạt bằng ngôn ngữ tình huống trước:

> Tác động của số giờ học không giống nhau giữa các nhóm học sinh. Ở nhóm có kiến thức nền tốt, tăng thời gian học đi kèm mức cải thiện điểm số mạnh hơn rõ rệt so với nhóm nền tảng yếu.

Sau đó mới bổ sung các con số ước lượng và khoảng bất định tương ứng.

## 11. Tổng kết Chương 5

Kết thúc Chương 5, bạn đã nắm bốn trụ cột của hồi quy đa biến: diễn giải hệ số có điều kiện, phân tích cấu trúc nhân quả và biến gây nhiễu bằng DAG, nhận diện và xử lý đa cộng tuyến, cùng cách mô hình hóa hiệu ứng tương tác. Nhờ đó, hồi quy chuyển từ kỹ thuật khớp đường thuần túy thành công cụ suy luận có cấu trúc về cơ chế sinh dữ liệu.

> **3 ý cần nhớ.** Hiệu ứng tương tác xuất hiện khi tác động của một biến thay đổi theo giá trị của biến khác; khi mô hình có tương tác, cần diễn giải qua hiệu ứng có điều kiện kết hợp biểu đồ trực quan thay vì chỉ đọc từng hệ số riêng lẻ; và tương tác rất phổ biến trong thực tế vì hiệu quả của can thiệp hiếm khi đồng nhất ở mọi bối cảnh.

## Video tham khảo

- [GLM Part 6: Interaction effects: How to interpret and identify them](https://www.youtube.com/watch?v=3CCkeFShB3U) — Simplistics (QuantPsych), English. **xem trước**. Giải thích bản chất và cách nhận diện hiệu ứng tương tác so với mô hình cộng.
- [How to Interpret a Regression with an Interaction Term](https://www.youtube.com/watch?v=J8IHdu-oM64) — Econometrics, Causality, and Coding with Dr. HK, English. Hướng dẫn chi tiết cách đọc hiệu ứng chính và hạng tương tác từ bảng kết quả hồi quy.
- [Statistical Rethinking 2023 - 04 - Categories & Curves](https://www.youtube.com/watch?v=F0N4b7K_iYQ) — Richard McElreath, English. Minh họa cách mô hình hóa đường cong và khác biệt theo nhóm, mở rộng góc nhìn về tương tác trong mô hình sinh dữ liệu.

## Câu hỏi tự luyện

1. Hãy nêu một ví dụ thực tế trong đó tác động của một biến phụ thuộc rõ rệt vào giá trị của biến khác.
2. Vì sao các đường hồi quy không song song giữa các nhóm là dấu hiệu gợi ý sự tồn tại của hiệu ứng tương tác?
3. Trong ví dụ giờ học và trình độ đầu vào, hạng tương tác nắm bắt được thông tin gì mà mô hình cộng bỏ sót?
4. Nếu các biến liên tục không được dịch tâm (center), việc diễn giải các hiệu ứng chính trong mô hình có tương tác sẽ gặp khó khăn ở điểm nào?

## Tài liệu tham khảo

**Gelman, A., & Hill, J. (2006).** *Data Analysis Using Regression and Multilevel/Hierarchical Models*. Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

---

*Chương tiếp theo: [Chương 6: Mô hình Tuyến tính Tổng quát Bayes (GLM)]({{ site.baseurl }}/contents/vi/chapter06/)*
