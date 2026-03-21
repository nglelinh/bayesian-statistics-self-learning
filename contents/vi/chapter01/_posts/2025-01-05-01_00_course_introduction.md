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

Khóa học này được xây dựng cho một mục tiêu rất rõ: giúp bạn học cách **nghĩ bằng xác suất**, thay vì chỉ nhớ các công thức thống kê. Trong thực tế, chúng ta liên tục phải trả lời những câu hỏi như:

- Một giả thuyết có đáng tin không?
- Dữ liệu mới có làm thay đổi niềm tin cũ không?
- Nếu phải ra quyết định ngay hôm nay, rủi ro sai là bao nhiêu?

Bayesian statistics mạnh ở đúng những câu hỏi như vậy. Nó không chỉ cho bạn một “kết quả kiểm định”, mà cho bạn một cách suy nghĩ thống nhất về **niềm tin, dữ liệu, bất định và quyết định**.

> **Ví dụ mini.** Khi nghe dự báo “70% khả năng mưa”, bạn không cần lặp lại ngày mai vô hạn lần để hiểu ý nghĩa của nó. Bạn chỉ cần biết mức độ tin tưởng hiện tại để quyết định có mang ô hay không.
>
> **Câu hỏi tự kiểm tra.** Theo bạn, vì sao kiểu suy nghĩ “cập nhật niềm tin khi có thêm thông tin” lại gần với đời sống thực hơn nhiều công thức thống kê rời rạc?

![Bayesian reasoning trong đời sống hằng ngày]({{ site.baseurl }}/img/chapter_img/chapter01/bayesian_daily_life.png)

## Khóa học này sẽ giúp bạn học điều gì?

Nếu học tốt khóa này, bạn sẽ không chỉ biết “Bayes theorem là gì”, mà còn biết cách dùng tư duy Bayes trong các bài toán thật.

### 1. Hiểu xác suất như một ngôn ngữ của mức độ tin tưởng

Bạn sẽ thấy vì sao trong Bayes:

- xác suất không chỉ là tần suất dài hạn,
- mà còn là cách mô tả mức độ hợp lý của một giả thuyết,
- đặc biệt khi ta không chắc chắn.

### 2. Hiểu cách xây mô hình sinh dữ liệu

Một mô hình Bayes tốt không bắt đầu từ code. Nó bắt đầu từ câu hỏi:

- dữ liệu được sinh ra như thế nào,
- tham số nào chưa biết,
- và prior nào phản ánh điều ta biết từ trước.

### 3. Hiểu cách cập nhật niềm tin bằng dữ liệu

Đây là trái tim của cả khóa học:

- prior là điều ta tin ban đầu,
- likelihood là phần dữ liệu lên tiếng,
- posterior là niềm tin đã cập nhật.

![Cỗ máy Bayes: từ prior đến posterior]({{ site.baseurl }}/img/chapter_img/chapter01/bayes_machine.png)

### 4. Biết dùng công cụ hiện đại để làm suy luận Bayes

Sau phần nền tảng, khóa học sẽ đi vào:

- grid approximation,
- Monte Carlo và MCMC,
- PyMC để triển khai mô hình thật,
- chẩn đoán mô hình và kiểm tra dự báo.

### 5. Biết diễn giải kết quả một cách trung thực

Bạn sẽ học cách trả lời những câu hỏi mà người làm nghiên cứu, kinh doanh hay kỹ thuật thật sự quan tâm:

- xác suất tham số lớn hơn 0 là bao nhiêu,
- vùng giá trị hợp lý nhất là gì,
- dự báo tương lai bất định ra sao,
- và mô hình có đang bỏ sót điều gì không.

## Vì sao nên học Bayes ngay từ đầu?

Nhiều người đến với Bayes sau khi đã học thống kê tần suất và cảm thấy có gì đó “khó nuốt” ở p-values, confidence intervals hay kiểm định giả thuyết. Điều đó rất bình thường.

Bayes hấp dẫn vì ba lý do lớn.

### 1. Nó gần với trực giác học từ thông tin mới

Trong đời sống, ta vẫn suy nghĩ rất Bayesian:

- nghe dự báo thời tiết rồi cập nhật kế hoạch,
- thấy xét nghiệm y khoa rồi cập nhật chẩn đoán,
- xem vài lượt mua hàng đầu tiên rồi cập nhật niềm tin về nhu cầu thị trường.

Ta gần như không suy nghĩ theo kiểu:

- “Tôi bác bỏ giả thuyết ở mức ý nghĩa 5%”.

### 2. Nó trung thực hơn về bất định

Bayes không chỉ trả lời “ước lượng là bao nhiêu”, mà còn cho biết:

- ta chắc đến đâu,
- giá trị nào còn có khả năng,
- và nếu dự đoán tương lai thì vùng rủi ro là gì.

### 3. Nó rất hợp với data science hiện đại

Bayes đặc biệt mạnh trong các bối cảnh như:

- dữ liệu ít nhưng cần quyết định nhanh,
- mô hình phân cấp,
- dự báo và recommendation,
- phân tích y khoa,
- A/B testing,
- machine learning có quantification of uncertainty.

## Lộ trình của Chapter 1

Chapter 1 không dạy bạn công thức nặng. Nó làm một việc quan trọng hơn: **đổi cách nhìn**.

### Bài 1.1

Ta bắt đầu từ một câu hỏi lớn: vì sao khoa học hiện đại lại gặp khủng hoảng tái lập, và p-values có vai trò gì trong chuyện đó?

### Bài 1.2

Ta quay về nền tảng triết học: xác suất thực ra là gì? Tần suất dài hạn hay độ hợp lý của niềm tin?

### Bài 1.3

Ta học định lý Bayes như một quy tắc cập nhật niềm tin khi có thêm bằng chứng.

### Bài 1.4

Ta đặt Bayes và Frequentist cạnh nhau để xem mỗi bên đang trả lời câu hỏi gì, mạnh ở đâu, và giới hạn ở đâu.

## Cách học khóa này để hiệu quả hơn

Nếu bạn muốn học nhanh mà vẫn chắc, hãy giữ ba thói quen sau.

### 1. Luôn hỏi “bài toán thật ở đây là gì?”

Trước mọi công thức, hãy hỏi:

- tham số chưa biết là gì,
- dữ liệu đến từ đâu,
- và quyết định cuối cùng là gì.

### 2. Ưu tiên trực giác trước kỹ thuật

Nếu bạn hiểu:

- prior là gì,
- likelihood nói gì,
- posterior dùng để làm gì,

thì phần tính toán sau này sẽ nhẹ hơn rất nhiều.

### 3. Đừng cố học Bayes như học thuộc lòng

Bayes không hiệu quả nếu chỉ học theo kiểu:

- công thức nào đi với công thức nào.

Nó hiệu quả khi bạn nhìn thấy một workflow thống nhất:

- đặt câu hỏi,
- mô hình hóa,
- cập nhật,
- kiểm tra,
- và ra quyết định.

## Tài liệu nên tham khảo trong suốt khóa học

### Tài liệu chính

**Richard McElreath (2020)** - *Statistical Rethinking* (2nd Edition)

Điểm mạnh:

- cực kỳ tốt về trực giác mô hình hóa,
- cách giải thích gần với người mới học,
- kết nối tốt giữa lý thuyết và mô hình thực hành.

### Tài liệu bổ sung

**Andrew Gelman et al. (2013)** - *Bayesian Data Analysis* (3rd Edition)

Điểm mạnh:

- nền tảng vững,
- bao quát rộng,
- rất phù hợp khi bạn muốn đi sâu hơn sau khi đã có trực giác.

**John K. Kruschke (2014)** - *Doing Bayesian Data Analysis*

Điểm mạnh:

- cực kỳ sư phạm,
- nhiều ví dụ minh họa,
- rất tốt cho việc kết nối khái niệm với diễn giải.

## Bạn không cần giỏi toán mới học được Bayes

Bạn cần đủ kiên nhẫn để chấp nhận rằng:

- bất định là thứ phải được mô hình hóa,
- dữ liệu không tự nói nếu không có mô hình,
- và việc cập nhật niềm tin một cách nhất quán là cốt lõi của suy luận.

Nếu giữ được tinh thần đó, Bayes sẽ không còn là một chương thống kê khó, mà trở thành một cách tư duy rất tự nhiên.

> **3 ý cần nhớ.**
> 1. Khóa học này không chỉ dạy công thức Bayes mà dạy cả một cách suy nghĩ về học từ dữ liệu.
> 2. Bayesian statistics mạnh ở chỗ kết nối mô hình, bất định và ra quyết định trong cùng một workflow.
> 3. Để học tốt khóa này, bạn nên luôn ưu tiên trực giác mô hình hóa trước rồi mới đến kỹ thuật tính toán.

## Đi tiếp từ đây

Bài tiếp theo là [1.1 Replication Crisis & P-values](/vi/chapter01/replication-crisis-pvalues/). Đây là nơi Chapter 1 bắt đầu đặt câu hỏi: nếu cách suy luận thống kê truyền thống có quá nhiều giới hạn, ta có lựa chọn nào tốt hơn không?

Nếu cần ôn lại nền tảng trước khi vào chương, bạn có thể xem [Chapter 00: Prerequisites](/vi/chapter00/).
