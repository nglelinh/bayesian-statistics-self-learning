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

Sau bài này, bạn cần hiểu rằng sự khác nhau giữa hai trường phái không chỉ nằm ở kỹ thuật tính toán mà nằm ở chính câu hỏi mỗi bên lựa chọn để trả lời. Bạn cũng cần nhận ra vì sao cách tiếp cận Bayes thường cho diễn giải trực tiếp hơn, đồng thời hiểu rõ những bối cảnh mà phương pháp tần suất vẫn giữ vai trò quan trọng.

> **Ví dụ mini.** Với cùng dữ liệu 7 mặt ngửa trong 10 lần tung, nhà thống kê tần suất hỏi: “Nếu đồng xu cân bằng thì dữ liệu này bất thường đến mức nào?”, còn nhà thống kê Bayes hỏi: “Sau khi quan sát dữ liệu này, xác suất ra ngửa thực sự có khả năng nằm ở đâu?”.
>
> **Câu hỏi tự kiểm tra.** Hai trường phái này khác nhau chủ yếu ở công thức tính toán, hay ở chính câu hỏi mà họ đặt ra?

## 1. Vì sao cần so sánh hai trường phái này?

Nhiều người học thống kê cảm thấy lúng túng vì trường phái tần suất (frequentist) và trường phái Bayes (Bayesian) đôi khi sử dụng cùng dữ liệu, cùng mô hình, thậm chí cùng một số công cụ toán học, nhưng lại diễn giải kết quả rất khác nhau. Sự khác biệt này nằm sâu hơn mức kỹ thuật: nó xuất phát từ cách định nghĩa xác suất, cách nhìn nhận tham số và loại câu trả lời cuối cùng mà mỗi bên hướng tới.

## 2. Cùng một bài toán, hai cách đặt câu hỏi

Xét lại ví dụ tung đồng xu 10 lần thu được 7 mặt ngửa để kiểm tra xem đồng xu có thiên lệch hay không.

### Câu hỏi theo hướng Frequentist

Nếu đồng xu thực sự cân bằng, dữ liệu như thế này có bất thường không?

### Câu hỏi theo hướng Bayesian

Sau khi thấy dữ liệu này, vùng giá trị hợp lý của xác suất ra ngửa là gì?

Chỉ riêng sự khác biệt trong cách đặt câu hỏi đã dẫn đến cách diễn giải hoàn toàn khác nhau.

![Góc nhìn Frequentist trong so sánh tổng quát]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_frequentist_vs_bayesian_frequentist.png)

![Góc nhìn Bayesian trong so sánh tổng quát]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_frequentist_vs_bayesian_bayesian.png)

## 3. Khác biệt ở định nghĩa xác suất và vai trò của tham số

### Trường phái Frequentist

Xác suất được hiểu là tần suất dài hạn của một kết quả qua nhiều lần lặp lại. Do đó, tham số được xem là cố định nhưng chưa biết, còn dữ liệu là đại lượng ngẫu nhiên.

### Trường phái Bayesian

Xác suất được hiểu là mức độ tin cậy hợp lý đối với một mệnh đề dựa trên thông tin hiện có. Do đó, dữ liệu đã quan sát được xem là cố định, còn tham số chưa biết được mô tả bằng phân phối xác suất.

![Frequentist: tham số cố định, dữ liệu ngẫu nhiên]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_philosophy_frequentist.png)

![Bayesian: dữ liệu đã thấy, tham số còn bất định]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_philosophy_bayesian.png)

## 4. Khoảng tin cậy (Confidence interval) và khoảng tin cậy Bayes (Credible interval)

Đây là điểm dễ gây nhầm lẫn nhất với người học. Giả sử ta thu được một khoảng $$[0.46, 0.86]$$.

### Frequentist confidence interval

Diễn giải đúng là nếu lặp lại quy trình lấy mẫu và dựng khoảng rất nhiều lần, thì 95% các khoảng được tạo ra sẽ chứa giá trị tham số thực. Điều này **không** có nghĩa là “có 95% xác suất tham số nằm trong khoảng cụ thể đang có”.

### Bayesian credible interval

Diễn giải Bayes trực tiếp hơn: với dữ liệu hiện tại và prior đã chọn, xác suất để tham số nằm trong khoảng đó là 95%. Cách phát biểu này sát với câu hỏi mà người dùng thực sự muốn đặt ra.

### Thử nghiệm: khoảng tin cậy và khoảng đáng tin khi lặp thí nghiệm

Mỗi hàng là một thí nghiệm; xem khoảng tin cậy 95% phủ μ cố định đúng 95% số lần, còn khoảng đáng tin phụ thuộc prior.

<div class="interactive-demo" markdown="1">
<div data-demo="interval-explainer" data-lang="vi"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 5. P-value và xác suất hậu nghiệm (Posterior probability)

### Theo góc nhìn Frequentist

P-value đánh giá rằng nếu giả thuyết không là đúng thì dữ liệu quan sát được bất thường đến mức nào.

### Theo góc nhìn Bayesian

Xác suất hậu nghiệm cho biết sau khi thấy dữ liệu, giả thuyết hoặc tham số có khả năng nằm ở đâu.

Đây là khác biệt giữa việc đánh giá **độ bất thường của dữ liệu** và việc đánh giá **độ tin cậy của giả thuyết**.

![P-value ở góc nhìn Frequentist]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_vs_posterior_frequentist.png)

![Posterior probability ở góc nhìn Bayesian]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_pvalue_vs_posterior_bayesian.png)

## 6. Ví dụ y khoa minh họa sự khác biệt

Giả sử một xét nghiệm trả về kết quả dương tính.

### Theo góc nhìn Frequentist

Câu hỏi thường đặt ra là: nếu bệnh nhân không mắc bệnh, xác suất xét nghiệm vẫn cho kết quả dương tính là bao nhiêu?

### Theo góc nhìn Bayesian

Câu hỏi trực tiếp hơn: sau khi nhận kết quả dương tính, xác suất bệnh nhân thực sự mắc bệnh là bao nhiêu?

Trong thực hành y khoa, câu hỏi thứ hai sát với nhu cầu của cả bác sĩ lẫn bệnh nhân hơn.

### Một ví dụ bằng con số

Giả sử tỷ lệ mắc bệnh trong dân số là $$1\%$$, xét nghiệm có độ nhạy $$99\%$$ và tỷ lệ dương tính giả là $$5\%$$. Khi một người có kết quả dương tính, theo định lý Bayes:

$$
P(\text{bệnh}\mid +)
=\frac{0.99\times 0.01}{0.99\times 0.01 + 0.05\times 0.99}
\approx 0.167.
$$

Nghĩa là sau khi có kết quả dương tính, xác suất thực sự mắc bệnh mới chỉ vào khoảng $$16.7\%$$ chứ không phải gần $$99\%$$. Ví dụ này cho thấy rõ: phương pháp tần suất thường báo cáo đặc tính của xét nghiệm dưới một giả thuyết cho trước, còn phương pháp Bayes trả lời trực tiếp xác suất mắc bệnh mà bác sĩ và bệnh nhân cần biết.

![Phân tích thử nghiệm lâm sàng theo Frequentist]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_clinical_trial_frequentist.png)

![Phân tích thử nghiệm lâm sàng theo Bayesian]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_clinical_trial_bayesian.png)

## 7. Thế mạnh của trường phái Frequentist

Sẽ không công bằng nếu coi thống kê tần suất là “sai hoàn toàn”. Trường phái này có ưu thế rõ rệt trong các thiết kế thử nghiệm chuẩn hóa với quy tắc quyết định cố định, các bài toán có cỡ mẫu rất lớn, những lĩnh vực hay cơ quan quản lý đã quen với khung kiểm định truyền thống, và các quy trình đòi hỏi bảo đảm tính chất thống kê dài hạn. Các ví dụ tiêu biểu gồm thử nghiệm lâm sàng giai đoạn cuối, kiểm soát chất lượng sản xuất hay những quy trình ra quyết định cần chuẩn hóa nghiêm ngặt.

## 8. Thế mạnh của trường phái Bayesian

Thống kê Bayes đặc biệt phù hợp khi cần diễn giải trực tiếp về tham số hoặc giả thuyết, khi có kiến thức ban đầu (prior) đáng tin cậy, khi cỡ mẫu còn nhỏ, khi cần cập nhật tuần tự theo từng đợt dữ liệu, khi mô hình có cấu trúc phân cấp hoặc phức tạp, hay khi cần dự báo đi kèm định lượng bất định. Những ứng dụng tiêu biểu gồm thử nghiệm A/B ở các doanh nghiệp mới có lưu lượng chưa lớn, hỗ trợ quyết định y khoa từ nhiều nguồn thông tin, hệ gợi ý, dự báo chuỗi thời gian và các phân tích khoa học có prior từ nghiên cứu trước.

## 9. Hạn chế thường gặp của mỗi bên

### Hạn chế của Frequentist

Thống kê tần suất thường gặp khó khăn trong việc diễn giải đúng p-value và khoảng tin cậy, khó tích hợp kiến thức ban đầu, không cho phép phát biểu trực tiếp về xác suất của tham số, và không thuận tiện khi cập nhật liên tục theo từng đợt dữ liệu.

### Hạn chế của Bayesian

Thống kê Bayes đòi hỏi phải lựa chọn prior, chi phí tính toán đôi khi cao hơn và cần người đọc chấp nhận cách hiểu xác suất như mức độ tin cậy. Tuy vậy, với các công cụ hiện đại như PyMC và Stan, rào cản tính toán đã giảm đi đáng kể.

## 10. Lựa chọn theo bài toán thay vì theo phe phái

Trong thực hành hiện đại, nhiều nhà phân tích kết hợp cả hai cách tiếp cận: dùng tư duy tần suất cho một số kiểm tra nhanh hoặc mốc so sánh cơ sở, và dùng Bayes cho mô hình chính cũng như phần diễn giải kết quả. Điều quan trọng không phải là chọn phe một cách cứng nhắc, mà là dùng đúng công cụ cho câu hỏi đặt ra và diễn giải kết quả trung thực với phương pháp đã chọn.

![Cây quyết định: khi nào nghĩ theo Frequentist, khi nào theo Bayes]({{ site.baseurl }}/img/chapter_img/chapter01/decision_tree_freq_vs_bayes.png)

## 11. Vì sao khóa học này tập trung vào Bayes?

Trong phần lớn các bài toán hiện đại mà người học quan tâm, thống kê Bayes trả lời trực tiếp hơn những câu hỏi cốt lõi: tham số có khả năng nằm ở đâu, độ bất định còn lại lớn đến mức nào, xác suất giả thuyết này vượt trội hơn giả thuyết kia là bao nhiêu, và dự báo tương lai nên được hiểu ra sao. Nói gọn lại, kết quả Bayes thường sát với thông tin mà nhà nghiên cứu, bác sĩ, kỹ sư hay chuyên viên phân tích sản phẩm thực sự cần.

## 12. Tóm lược dễ nhớ

Nếu cần một cách phân biệt ngắn gọn: trường phái tần suất đánh giá dữ liệu dưới một giả thuyết cho trước, còn trường phái Bayes đánh giá giả thuyết sau khi đã quan sát dữ liệu. Chính điểm này khiến cách diễn giải Bayes thường tự nhiên hơn trong các bài toán thực tế.

> **3 ý cần nhớ.**
> 1. Frequentist và Bayesian khác nhau từ nền tảng triết học: đại lượng nào ngẫu nhiên, đại lượng nào cố định và xác suất biểu thị điều gì.
> 2. Frequentist thường trả lời câu hỏi về dữ liệu giả định dưới một giả thuyết, còn Bayesian trả lời trực tiếp về tham số hoặc giả thuyết sau khi thấy dữ liệu.
> 3. Trong nhiều bài toán thực tế, câu trả lời theo hướng Bayes gần hơn với câu hỏi mà người dùng thực sự muốn đặt ra.

## Video tham khảo

- [Bayesian vs. Frequentist Statistics ... MADE EASY!!!](https://www.youtube.com/watch?v=qJcv7VHwqcA) — Stats with Brian, English. **xem trước**. Minh họa cách hai trường phái đặt hai câu hỏi khác nhau trên cùng một tập dữ liệu, đúng trọng tâm so sánh của bài.
- [Are you Bayesian or Frequentist?](https://www.youtube.com/watch?v=GEFxFVESQXc) — Cassie Kozyrkov, English. Trình bày cách chọn ngôn ngữ xác suất dựa trên quyết định cần đưa ra, củng cố quan điểm không biến khác biệt phương pháp thành phe phái.
- [Bayesian Statistics: Credible vs Confidence Intervals](https://www.youtube.com/watch?v=YPceDssQFWo) — Academia Elevated, English. Phân biệt rõ cách đọc khoảng tin cậy (confidence interval) và khoảng tin cậy Bayes (credible interval), bổ trợ cho phần diễn giải kết quả.

## Câu hỏi tự luyện

1. Hãy giải thích bằng lời sự khác nhau giữa confidence interval và credible interval.
2. Trong ví dụ đồng xu 7/10, trường phái Frequentist và Bayesian đang đặt hai câu hỏi khác nhau như thế nào?
3. Với một bài toán chẩn đoán y khoa, vì sao cách diễn giải theo hướng Bayes thường tự nhiên hơn?
4. Hãy nêu một tình huống mà cách tiếp cận Frequentist vẫn là lựa chọn hợp lý.

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1-4.
- Dienes, Z. (2011). Bayesian versus orthodox statistics.
- Wasserstein, R. L., & Lazar, N. A. (2016). ASA Statement on p-values.

---

*Kết thúc Chapter 1. Bài học tiếp theo: [Chapter 2 - Cơ bản về Phân tích Dữ liệu Bayesian]({{ site.baseurl }}/contents/vi/chapter02/)*
