---
layout: post
title: "Giới thiệu Khóa học: Phân tích Dữ liệu Bayes"
chapter: '01'
order: 0
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

## Chào mừng đến với Bayesian Statistics

Khóa học này được xây dựng cho một mục tiêu rất rõ: giúp bạn học cách **nghĩ bằng xác suất**, thay vì chỉ ghi nhớ các công thức thống kê như những mảnh rời rạc. Trong thực tế, chúng ta liên tục phải đối diện với những câu hỏi như một giả thuyết có đáng tin hay không, dữ liệu mới có làm thay đổi niềm tin cũ hay không, và nếu phải ra quyết định ngay hôm nay thì rủi ro sai là bao nhiêu. Bayesian statistics đặc biệt mạnh ở chính những câu hỏi như vậy, bởi nó không chỉ đưa ra một “kết quả kiểm định”, mà cung cấp một cách suy nghĩ thống nhất về **niềm tin, dữ liệu, bất định và quyết định**.

> **Ví dụ mini.** Khi nghe dự báo “70% khả năng mưa”, bạn không cần lặp lại ngày mai vô hạn lần để hiểu ý nghĩa của nó. Bạn chỉ cần biết mức độ tin tưởng hiện tại để quyết định có mang ô hay không.
>
> **Câu hỏi tự kiểm tra.** Theo bạn, vì sao kiểu suy nghĩ “cập nhật niềm tin khi có thêm thông tin” lại gần với đời sống thực hơn nhiều công thức thống kê rời rạc?

![Bayesian reasoning trong đời sống hằng ngày]({{ site.baseurl }}/img/chapter_img/chapter01/bayesian_daily_life_small.png)

## Khóa học này sẽ giúp bạn học điều gì?

Nếu học tốt khóa này, bạn sẽ không chỉ biết “Bayes theorem là gì”, mà còn biết cách dùng tư duy Bayes trong các bài toán thật.

### 1. Hiểu xác suất như một ngôn ngữ của mức độ tin tưởng

Bạn sẽ thấy vì sao trong Bayes, xác suất không chỉ được hiểu như tần suất dài hạn mà còn như một ngôn ngữ mô tả mức độ hợp lý của một giả thuyết, đặc biệt trong những tình huống mà bất định là điều không thể tránh khỏi.

### 2. Hiểu cách xây mô hình sinh dữ liệu

Một mô hình Bayes tốt không bắt đầu từ code. Nó bắt đầu từ câu hỏi dữ liệu được sinh ra như thế nào, tham số nào còn chưa biết, và prior nào phản ánh hợp lý điều ta đã biết từ trước.

### 3. Hiểu cách cập nhật niềm tin bằng dữ liệu

Đây là trái tim của cả khóa học: **prior** là điều ta tin ban đầu, **likelihood** là cách dữ liệu lên tiếng dưới từng giả thuyết hay giá trị tham số, còn **posterior** là niềm tin đã được cập nhật sau khi hai phần đó gặp nhau.

![Cỗ máy Bayes: từ prior đến posterior]({{ site.baseurl }}/img/chapter_img/chapter01/bayes_machine_small.png)

### 4. Biết dùng công cụ hiện đại để làm suy luận Bayes

Sau phần nền tảng, khóa học sẽ đi vào các công cụ như **grid approximation**, Monte Carlo và MCMC, rồi đến PyMC để triển khai những mô hình thực sự, cũng như các kỹ thuật chẩn đoán mô hình và kiểm tra dự báo.

### 5. Biết diễn giải kết quả một cách trung thực

Bạn sẽ học cách trả lời những câu hỏi mà người làm nghiên cứu, kinh doanh hay kỹ thuật thật sự quan tâm, chẳng hạn xác suất một tham số lớn hơn 0 là bao nhiêu, vùng giá trị nào còn hợp lý, dự báo tương lai còn bất định ra sao, và mô hình có đang bỏ sót một cấu trúc quan trọng nào không.

## Vì sao nên học Bayes ngay từ đầu?

Nhiều người đến với Bayes sau khi đã học thống kê tần suất và cảm thấy có gì đó “khó nuốt” ở p-values, confidence intervals hay kiểm định giả thuyết. Điều đó rất bình thường.

Bayes hấp dẫn vì ba lý do lớn.

### 1. Nó gần với trực giác học từ thông tin mới

Trong đời sống, ta vốn đã suy nghĩ theo cách rất Bayesian: nghe dự báo thời tiết rồi cập nhật kế hoạch, thấy xét nghiệm y khoa rồi cập nhật chẩn đoán, hay xem vài lượt mua hàng đầu tiên rồi điều chỉnh niềm tin về nhu cầu thị trường. Ta hầu như không suy nghĩ theo kiểu “tôi bác bỏ giả thuyết ở mức ý nghĩa 5%”, bởi ngôn ngữ đời thực gần với cập nhật niềm tin hơn là với các nghi thức kiểm định hình thức.

### 2. Nó trung thực hơn về bất định

Bayes không chỉ trả lời “ước lượng là bao nhiêu”, mà còn cho biết ta chắc đến đâu, những giá trị nào vẫn còn có khả năng, và nếu phải dự báo tương lai thì vùng rủi ro nên được hiểu như thế nào.

### 3. Nó rất hợp với data science hiện đại

Bayes đặc biệt mạnh trong những bối cảnh như dữ liệu ít nhưng vẫn cần quyết định nhanh, mô hình phân cấp, dự báo và recommendation, phân tích y khoa, A/B testing, hay machine learning có **quantification of uncertainty** (định lượng bất định).

## Tài liệu nên tham khảo trong suốt khóa học

### Tài liệu chính

**Richard McElreath (2020)** - *Statistical Rethinking* (2nd Edition)

Điểm mạnh của tài liệu này là trực giác mô hình hóa rất tốt, cách giải thích gần với người mới học, và khả năng kết nối chặt giữa lý thuyết với mô hình thực hành.

### Tài liệu bổ sung

**Andrew Gelman et al. (2013)** - *Bayesian Data Analysis* (3rd Edition)

Điểm mạnh của tài liệu này là nền tảng rất vững, độ bao quát rộng, và sự phù hợp cao khi bạn muốn đi sâu hơn sau khi đã có trực giác ban đầu.

**John K. Kruschke (2014)** - *Doing Bayesian Data Analysis*

Điểm mạnh của tài liệu này là tính sư phạm rất cao, nhiều ví dụ minh họa, và khả năng kết nối khái niệm với diễn giải rất tốt.

## Thông tin môn học và đánh giá

### Tài liệu tham khảo cốt lõi

1. Gelman, A. et al. *Bayesian Data Analysis*.
2. Congdon, P. *Bayesian Statistical Modelling*.
3. Lee, P. M. *Bayesian Statistics: An Introduction*.

### Cấu phần đánh giá

Cấu phần đánh giá hiện tại gồm 20% thường kỳ, 30% giữa kỳ theo hướng thực hành, và 50% cuối kỳ cũng theo hướng thực hành.

## Bạn không cần giỏi toán mới học được Bayes

Bạn chỉ cần đủ kiên nhẫn để chấp nhận rằng bất định là thứ phải được mô hình hóa, dữ liệu không tự nói nếu không có mô hình, và việc cập nhật niềm tin một cách nhất quán là cốt lõi của suy luận. Nếu giữ được tinh thần đó, Bayes sẽ không còn là một chương thống kê khó, mà trở thành một cách tư duy rất tự nhiên.

> **3 ý cần nhớ.** Khóa học này không chỉ dạy công thức Bayes mà dạy cả một cách suy nghĩ về học từ dữ liệu; Bayesian statistics mạnh ở chỗ kết nối mô hình, bất định và ra quyết định trong cùng một workflow; và để học tốt khóa này, bạn nên luôn ưu tiên trực giác mô hình hóa trước rồi mới đến kỹ thuật tính toán.

## Đi tiếp từ đây

Bài tiếp theo là [1.1 Replication Crisis & P-values](/vi/chapter01/replication-crisis-pvalues/). Đây là nơi Chapter 1 bắt đầu đặt câu hỏi: nếu cách suy luận thống kê truyền thống có quá nhiều giới hạn, ta có lựa chọn nào tốt hơn không?

Nếu cần ôn lại nền tảng trước khi vào chương, bạn có thể xem [Chapter 00: Prerequisites](/vi/chapter00/).
