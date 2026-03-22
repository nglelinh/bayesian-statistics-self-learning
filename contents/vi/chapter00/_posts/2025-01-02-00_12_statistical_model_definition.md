---
layout: post
title: "Bài 0.14: Mô hình Thống kê là gì?"
chapter: '00'
order: 14
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ nắm được định nghĩa thực dụng của mô hình thống kê như một mô tả xác suất cho cách dữ liệu được sinh ra, biết phân biệt dữ liệu quan sát với tham số chưa biết, và hiểu vì sao câu hỏi "mô hình này đang giả định điều gì?" luôn quan trọng hơn việc thuộc công thức.

## Giới thiệu: mô hình như ngôn ngữ trung gian của suy luận

Trong thống kê, dữ liệu quan sát chỉ là điểm khởi đầu. Để đi từ dữ liệu sang kết luận về cơ chế thật của thế giới, ta cần một cấu trúc trung gian có thể phát biểu giả định, tạo dự báo, và cho phép cập nhật khi có thêm thông tin. Cấu trúc đó chính là mô hình thống kê.

## 1) Động cơ: Dữ liệu không tự nói nếu thiếu mô hình

Khi nhìn một tập dữ liệu, ta có thể tính trung bình, độ lệch chuẩn, vẽ histogram. Nhưng những con số đó chưa tự trả lời câu hỏi suy luận như:

Tỷ lệ thật của hiện tượng trong quần thể là bao nhiêu, hiệu ứng có đủ lớn để quan tâm hay không, hay dự báo tương lai bất định đến mức nào đều là những câu hỏi vượt ra ngoài bản thân bảng số liệu thô.

Để trả lời, ta cần một cầu nối từ "tham số chưa biết" sang "dữ liệu có thể quan sát". Cầu nối đó chính là mô hình thống kê.

## 2) Định nghĩa cốt lõi

Một **mô hình thống kê** là một họ các phân phối xác suất cho dữ liệu $$x$$, được chỉ số hóa bởi tham số $$\theta$$:

$$
\mathcal{M} = \{p(x\mid \theta): \theta \in \Theta\}
$$

Trong đó, $$x$$ là dữ liệu ta quan sát được, $$\theta$$ là đại lượng chưa biết điều khiển cơ chế sinh dữ liệu, còn $$\Theta$$ là không gian tham số, tức tập các giá trị hợp lệ mà $$\theta$$ có thể nhận.

Nói ngắn gọn: mô hình thống kê là cách mã hóa "nếu tham số là thế này, dữ liệu có xu hướng trông ra sao".

## 3) Góc nhìn sinh dữ liệu (generative story)

Trong khóa học này, ta ưu tiên cách đọc mô hình theo câu chuyện sinh dữ liệu, nghĩa là tưởng tượng rằng trước hết có một tham số $$\theta$$ chưa biết, từ tham số đó dữ liệu $$x$$ được sinh ra theo $$p(x\mid\theta)$$, và nhiệm vụ của ta là so sánh dữ liệu quan sát được với những gì mô hình kỳ vọng dưới các giá trị khả dĩ của $$\theta$$.

Ví dụ đồng xu:

Ở đây, $$\theta$$ là xác suất ra ngửa, mỗi lần tung cho một quan sát $$y_i \sim \text{Bernoulli}(\theta)$$, và sau $$n$$ lần tung thì tổng số mặt ngửa $$k=\sum_i y_i$$ tuân theo phân phối $$\text{Binomial}(n,\theta)$$.

Điều quan trọng là mô hình ở đây không chỉ là công thức nhị thức, mà còn là tập giả định rằng mỗi lần tung có cùng xác suất $$\theta$$, các lần tung độc lập với nhau, và dữ liệu được tóm tắt bằng số lần ngửa trong $$n$$ phép thử.

![Mo hinh thong ke nhu cau noi giua tham so va du lieu]({{ site.baseurl }}/img/chapter_img/chapter00/statistical_model_definition_flow.png)

*Cách đọc hình: Hình này minh họa mo hinh thong ke nhu cau noi giua tham so va du lieu. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hinh 1: Mo hinh thong ke nhu cau noi giua tham so chua biet $$\theta$$ va du lieu quan sat $$x$$ thong qua co che sinh du lieu $$p(x\mid\theta)$$, roi cap nhat ve posterior $$p(\theta\mid x)$$.*

## 3.1) Mô hình và mô phỏng khác nhau thế nào?

Hai khái niệm này rất dễ bị trộn lẫn, nhưng vai trò của chúng khác nhau rõ rệt: mô hình là mô tả xác suất về cơ chế sinh dữ liệu, tức bản thiết kế khái niệm, còn mô phỏng là việc chạy bản thiết kế đó trên máy tính để sinh ra dữ liệu giả nhiều lần.

Ví dụ đồng xu:

Mô hình nói rằng mỗi lần tung $$y_i\sim\text{Bernoulli}(\theta)$$, còn mô phỏng là bước chọn một giá trị cụ thể của $$\theta$$, chẳng hạn 0.6, rồi sinh 10,000 lần tung để xem tỷ lệ ngửa dao động như thế nào.

Vì vậy, mô phỏng không thay thế mô hình; nó là công cụ để kiểm tra trực giác và hệ quả của mô hình.

## 4) Mô hình không phải "sự thật" mà là xấp xỉ có ích

Một hiểu lầm phổ biến là: có thể tìm được "mô hình đúng tuyệt đối". Trong thực tế:

Mô hình chỉ là bản đồ chứ không phải lãnh thổ, mọi mô hình đều buộc phải lược bỏ chi tiết, và giá trị của mô hình không nằm ở việc nó phản chiếu trọn vẹn thực tại mà ở chỗ nó giúp ta dự báo, giải thích, và hỗ trợ quyết định tốt đến mức nào.

Vì vậy, khi dùng mô hình, ta luôn phải hỏi:

Giả định nào đang được đưa vào, giả định đó có hợp lý với bối cảnh dữ liệu hay không, và nếu giả định sai thì kết luận của ta sẽ lệch đi theo hướng nào.

## 5) Liên hệ trực tiếp với Bayesian inference

Trong Bayes, mô hình thống kê đi vào công thức qua likelihood:

$$
p(\theta\mid x) \propto p(x\mid\theta)\,p(\theta)
$$

Ở đây:

$$p(x\mid\theta)$$ đến từ mô hình thống kê, $$p(\theta)$$ đóng vai trò prior, còn posterior $$p(\theta\mid x)$$ là kết quả của quá trình cập nhật niềm tin khi dữ liệu được quan sát.

Nếu định nghĩa mô hình không rõ, likelihood sẽ mơ hồ; khi đó posterior cũng mất ý nghĩa.

## 6) Một ví dụ mini: đo chiều cao sinh viên

Giả sử $$x_1,\dots,x_n$$ là chiều cao (cm) của sinh viên trong một lớp. Một mô hình đơn giản là:

$$
x_i \sim \mathcal{N}(\mu,\sigma^2),\quad i=1,\dots,n
$$

với $$\mu$$ là trung bình lớp và $$\sigma$$ là độ phân tán.

Mô hình này ngầm giả định rằng dữ liệu gần phân phối chuẩn, các quan sát độc lập có điều kiện theo tham số, và mọi quan sát đều đến từ cùng một cơ chế sinh dữ liệu.

Nhờ mô hình đó, ta có thể ước lượng và diễn giải $$\mu, \sigma$$, dự báo giá trị mới, đồng thời kiểm tra xem mô hình có đang bỏ sót cấu trúc quan trọng nào trong dữ liệu hay không.

## Tóm tắt nhanh

1. Mô hình thống kê là họ phân phối $$\{p(x\mid\theta)\}$$ cho dữ liệu.
2. Nó nối tham số chưa biết với dữ liệu quan sát qua cơ chế sinh dữ liệu.
3. Mô hình luôn đi kèm giả định; hiểu giả định quan trọng hơn nhớ công thức.
4. Trong Bayes, mô hình cung cấp likelihood để cập nhật từ prior sang posterior.

## Câu hỏi tự luyện

1. Với ví dụ đồng xu, hãy liệt kê ba giả định ngầm của mô hình Binomial.
2. Hãy nêu một tình huống mà giả định độc lập giữa các quan sát có thể sai.
3. Vì sao nói "mô hình là bản đồ, không phải lãnh thổ"?

## Tài liệu tham khảo

- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Wasserman, L. (2004). *All of Statistics*. Springer.

---

*Bài học tiếp theo: [0.15 Kỳ vọng, Phương sai, và Hiệp phương sai](/vi/chapter00/expectation-variance-covariance/)*
