---
layout: post
title: "Bài 1.4: Bayesian vs Frequentist - So Sánh và Lựa Chọn"
chapter: '01'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu sự khác nhau giữa hai trường phái không chỉ ở công cụ tính toán, mà ở chính câu hỏi mà mỗi bên chọn để trả lời. Bạn cũng cần biết vì sao Bayesian thường cho diễn giải trực tiếp hơn, nhưng frequentist vẫn có vai trò trong nhiều bối cảnh thực tế.

> **Ví dụ mini.** Cùng dữ liệu 7 ngửa trong 10 lần tung, một frequentist hỏi “nếu đồng xu công bằng thì dữ liệu này lạ đến mức nào?”, còn một Bayesian hỏi “sau khi thấy dữ liệu này, xác suất thật sự có khả năng nằm ở đâu?”.
>
> **Câu hỏi tự kiểm tra.** Hai trường phái này khác nhau chủ yếu ở công thức tính toán, hay ở chính câu hỏi mà họ chọn để trả lời?

## 1. Vì sao cần so sánh hai trường phái này?

Rất nhiều người học thống kê cảm thấy bối rối vì frequentist và Bayesian đôi khi dùng cùng dữ liệu, cùng mô hình, thậm chí cùng một số công cụ toán, nhưng lại diễn giải kết quả rất khác. Sự khác biệt nằm sâu hơn mức kỹ thuật. Nó nằm ở cách hiểu xác suất, ở việc tham số được xem là gì, và ở loại câu trả lời cuối cùng mà mỗi bên muốn nhắm tới.

## 2. Cùng một bài toán, hai cách hỏi khác nhau

Xét lại ví dụ đồng xu: ta tung 10 lần, thấy 7 mặt ngửa, và muốn biết đồng xu có thiên lệch hay không.

### Frequentist thường hỏi:

Nếu đồng xu thật sự cân bằng, dữ liệu như thế này có lạ không?

### Bayesian thường hỏi:

Sau khi thấy dữ liệu này, vùng giá trị hợp lý của xác suất ra ngửa là gì?

Chỉ riêng khác biệt trong câu hỏi đã dẫn tới khác biệt lớn trong diễn giải.

![So sánh Frequentist và Bayesian]({{ site.baseurl }}/img/chapter_img/chapter01/frequentist_vs_bayesian_comparison.png)

## 3. Khác nhau ở định nghĩa xác suất

### Frequentist

Với frequentist, xác suất là tần suất dài hạn của một kết quả trong nhiều lần lặp lại.

### Bayesian

Với Bayesian, xác suất là mức độ tin tưởng hợp lý vào một mệnh đề, dựa trên thông tin hiện có.

Điều này kéo theo một khác biệt rất quan trọng.

### Với Frequentist

Tham số là cố định nhưng chưa biết, còn dữ liệu là ngẫu nhiên.

### Với Bayesian

Dữ liệu quan sát đã cố định, còn tham số chưa biết được mô tả bằng phân phối xác suất.

![So sánh nền tảng triết học]({{ site.baseurl }}/img/chapter_img/chapter01/frequentist_vs_bayesian_philosophy.png)

## 4. Confidence interval và credible interval khác nhau thế nào?

Đây là điểm gây nhầm nhất cho người học.

Giả sử bạn có một khoảng $$[0.46, 0.86]$$.

### Frequentist confidence interval

Diễn giải đúng là nếu ta lặp lại quy trình này rất nhiều lần thì 95% các khoảng được tạo ra sẽ chứa giá trị thật. Điều này **không** có nghĩa là “có 95% xác suất tham số nằm trong khoảng đó”.

### Bayesian credible interval

Diễn giải Bayesian lại nói trực tiếp hơn: với dữ liệu hiện tại và prior hiện tại, có 95% xác suất tham số nằm trong khoảng đó.

Điều này gần đúng với kiểu câu hỏi mà người dùng thật sự muốn hỏi.

## 5. P-value và posterior probability khác nhau thế nào?

### Frequentist

P-value hỏi nếu giả thuyết không đúng, thì dữ liệu này lạ đến mức nào.

### Bayesian

Posterior probability lại nói về việc sau khi thấy dữ liệu, giả thuyết hoặc tham số có khả năng ở đâu.

Đây là khác biệt giữa việc nói về **độ lạ của dữ liệu** và việc nói về **độ tin cậy của giả thuyết**.

![P-value so với posterior probability]({{ site.baseurl }}/img/chapter_img/chapter01/pvalue_vs_posterior_probability.png)

## 6. Một ví dụ y khoa để thấy khác biệt rõ hơn

Giả sử một xét nghiệm cho kết quả dương tính.

### Frequentist style

Người ta có thể nói: nếu bệnh nhân không mắc bệnh, xác suất có kết quả dương tính là bao nhiêu?

### Bayesian style

Người ta hỏi trực tiếp hơn: sau khi có kết quả dương tính, xác suất bệnh nhân thực sự mắc bệnh là bao nhiêu?

Trong y khoa, rõ ràng câu hỏi thứ hai gần với nhu cầu của bác sĩ và bệnh nhân hơn.

![So sánh trong bối cảnh thử nghiệm lâm sàng và y khoa]({{ site.baseurl }}/img/chapter_img/chapter01/clinical_trial_comparison.png)

## 7. Frequentist mạnh ở đâu?

Sẽ không công bằng nếu xem frequentist như “sai hoàn toàn”.

Frequentist mạnh trong các bối cảnh như thiết kế thử nghiệm chuẩn hóa với quy tắc quyết định cố định, các bài toán có cỡ mẫu rất lớn, những ngành hoặc cơ quan quản lý quen với ngôn ngữ kiểm định truyền thống, và các thủ tục cần bảo đảm tính chất dài hạn của quy trình. Những ví dụ điển hình là nhiều clinical trial giai đoạn cuối, kiểm soát chất lượng sản xuất, hay những tình huống mà quy trình ra quyết định phải được chuẩn hóa rất chặt.

## 8. Bayesian mạnh ở đâu?

Bayesian đặc biệt mạnh khi cần diễn giải trực tiếp về tham số hoặc giả thuyết, khi có kiến thức prior đáng tin, khi dữ liệu còn ít, khi cần cập nhật tuần tự, khi mô hình có cấu trúc phân cấp hoặc phức tạp, hay khi cần dự báo đi kèm bất định. Những ví dụ rất tiêu biểu là startup làm A/B test với traffic chưa lớn, bác sĩ ra quyết định dựa trên nhiều nguồn thông tin, các hệ recommendation, dự báo time series, hay những phân tích khoa học có prior từ nghiên cứu trước.

## 9. Điểm yếu điển hình của mỗi bên

### Frequentist thường gặp khó ở:

Frequentist thường gặp khó ở việc diễn giải p-value và confidence interval, trong việc kết hợp kiến thức prior, trong việc nói trực tiếp về xác suất của tham số, và trong việc cập nhật tự nhiên khi dữ liệu tới theo từng đợt.

### Bayesian thường gặp khó ở:

Bayesian thường gặp khó ở chỗ phải chọn prior, tính toán đôi khi nặng hơn, và cần người đọc chấp nhận cách diễn giải xác suất như degree of belief.

Nhưng với công cụ hiện đại như PyMC và Stan, rào cản tính toán đã giảm đi rất nhiều.

## 10. Không phải lúc nào cũng là “chiến tranh”

Trong thực hành hiện đại, nhiều nhà phân tích dùng tư duy frequentist cho một số kiểm tra hay baseline, nhưng dùng Bayesian cho mô hình chính và diễn giải kết quả. Điều quan trọng không phải là chọn phe một cách giáo điều, mà là xem bạn có đang dùng công cụ phù hợp với câu hỏi hay không, và việc diễn giải kết quả có trung thực với chính phương pháp đã chọn hay không.

![Cây quyết định: khi nào nghĩ theo Frequentist, khi nào theo Bayes]({{ site.baseurl }}/img/chapter_img/chapter01/decision_tree_freq_vs_bayes.png)

## 11. Vì sao khóa học này chọn trọng tâm là Bayes?

Vì trong phần lớn các bài toán hiện đại mà người học khóa này quan tâm, Bayes trả lời trực tiếp hơn các câu hỏi như tham số có khả năng nằm ở đâu, bất định còn lại là bao nhiêu, xác suất giả thuyết này lớn hơn giả thuyết kia là bao nhiêu, và dự báo tương lai nên được hiểu thế nào.

Nói ngắn gọn, Bayes thường nói đúng thứ mà người dùng cuối, nhà nghiên cứu, bác sĩ, kỹ sư hay product analyst muốn nghe.

## 12. Một cách kết luận dễ nhớ

Nếu phải nhớ thật ngắn, thì frequentist thường đánh giá dữ liệu dưới một giả thuyết, còn Bayesian thường đánh giá giả thuyết sau khi thấy dữ liệu.

Đó là lý do vì sao Bayesian thường có cảm giác “tự nhiên hơn” đối với câu hỏi thực tế.

> **3 ý cần nhớ.**
> 1. Frequentist và Bayesian khác nhau từ nền tảng triết học: ai là ngẫu nhiên, ai là cố định, và xác suất đang nói về điều gì.
> 2. Frequentist thường trả lời câu hỏi về dữ liệu giả định dưới một giả thuyết, còn Bayesian trả lời trực tiếp về tham số hoặc giả thuyết sau khi thấy dữ liệu.
> 3. Trong nhiều bài toán thực tế, câu trả lời Bayesian thường gần hơn với câu hỏi mà người dùng thật sự muốn hỏi.

## Câu hỏi tự luyện

1. Hãy giải thích bằng lời sự khác nhau giữa confidence interval và credible interval.
2. Trong ví dụ đồng xu 7/10, frequentist và Bayesian đang hỏi hai câu khác nhau như thế nào?
3. Với một bài toán chẩn đoán y khoa, vì sao cách diễn giải Bayesian thường tự nhiên hơn?
4. Hãy nêu một tình huống mà frequentist vẫn là lựa chọn hợp lý.

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1-4.
- Dienes, Z. (2011). Bayesian versus orthodox statistics.
- Wasserstein, R. L., & Lazar, N. A. (2016). ASA Statement on p-values.

---

*Kết thúc Chapter 1. Bài học tiếp theo: [Chapter 2 - Cơ bản về Phân tích Dữ liệu Bayesian](/vi/chapter02/)*
