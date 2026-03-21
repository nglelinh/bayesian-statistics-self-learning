---
layout: post
title: "Bài 0.12: Mô hình Thống kê là gì?"
chapter: '00'
order: 12
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ nắm được định nghĩa thực dụng của mô hình thống kê như một mô tả xác suất cho cách dữ liệu được sinh ra, biết phân biệt dữ liệu quan sát với tham số chưa biết, và hiểu vì sao câu hỏi "mô hình này đang giả định điều gì?" luôn quan trọng hơn việc thuộc công thức.

## 1) Động cơ: Dữ liệu không tự nói nếu thiếu mô hình

Khi nhìn một tập dữ liệu, ta có thể tính trung bình, độ lệch chuẩn, vẽ histogram. Nhưng những con số đó chưa tự trả lời câu hỏi suy luận như:

- tỷ lệ thật của hiện tượng trong quần thể là bao nhiêu,
- hiệu ứng có đủ lớn để quan tâm hay không,
- dự báo tương lai bất định đến mức nào.

Để trả lời, ta cần một cầu nối từ "tham số chưa biết" sang "dữ liệu có thể quan sát". Cầu nối đó chính là mô hình thống kê.

## 2) Định nghĩa cốt lõi

Một **mô hình thống kê** là một họ các phân phối xác suất cho dữ liệu $$x$$, được chỉ số hóa bởi tham số $$\theta$$:

$$
\mathcal{M} = \{p(x\mid \theta): \theta \in \Theta\}
$$

Trong đó:

- $$x$$: dữ liệu ta quan sát được,
- $$\theta$$: đại lượng chưa biết điều khiển cơ chế sinh dữ liệu,
- $$\Theta$$: không gian tham số (những giá trị hợp lệ của $$\theta$$).

Nói ngắn gọn: mô hình thống kê là cách mã hóa "nếu tham số là thế này, dữ liệu có xu hướng trông ra sao".

## 3) Góc nhìn sinh dữ liệu (generative story)

Trong khóa học này, ta ưu tiên cách đọc mô hình theo câu chuyện sinh dữ liệu:

1. Chọn tham số $$\theta$$ (chưa biết).
2. Từ $$\theta$$, sinh dữ liệu $$x$$ theo $$p(x\mid\theta)$$.
3. So sánh dữ liệu quan sát được với những gì mô hình kỳ vọng.

Ví dụ đồng xu:

- $$\theta$$ là xác suất ra ngửa,
- mỗi lần tung: $$y_i \sim \text{Bernoulli}(\theta)$$,
- sau $$n$$ lần: $$k=\sum_i y_i \sim \text{Binomial}(n,\theta)$$.

Mô hình ở đây không chỉ là công thức nhị thức. Nó là giả định rằng:

- mỗi lần tung có cùng xác suất $$\theta$$,
- các lần tung độc lập,
- và dữ liệu là số lần ngửa trong $$n$$ phép thử.

![Mo hinh thong ke nhu cau noi giua tham so va du lieu]({{ site.baseurl }}/img/chapter_img/chapter00/statistical_model_definition_flow.png)
*Hinh 1: Mo hinh thong ke nhu cau noi giua tham so chua biet $$\theta$$ va du lieu quan sat $$x$$ thong qua co che sinh du lieu $$p(x\mid\theta)$$, roi cap nhat ve posterior $$p(\theta\mid x)$$.*

## 3.1) Mô hình và mô phỏng khác nhau thế nào?

Hai khái niệm này dễ bị trộn lẫn, nhưng vai trò khác nhau:

- **Mô hình** là mô tả xác suất về cơ chế sinh dữ liệu (bản thiết kế).
- **Mô phỏng** là chạy bản thiết kế đó để sinh dữ liệu giả nhiều lần bằng máy tính.

Ví dụ đồng xu:

- mô hình: mỗi lần tung $$y_i\sim\text{Bernoulli}(\theta)$$,
- mô phỏng: chọn một $$\theta$$ cụ thể (ví dụ 0.6), rồi sinh 10,000 lần tung để xem tỷ lệ ngửa dao động ra sao.

Vì vậy, mô phỏng không thay thế mô hình; nó là công cụ để kiểm tra trực giác và hệ quả của mô hình.

## 4) Mô hình không phải "sự thật" mà là xấp xỉ có ích

Một hiểu lầm phổ biến là: có thể tìm được "mô hình đúng tuyệt đối". Trong thực tế:

- mô hình là bản đồ, không phải lãnh thổ,
- mọi mô hình đều lược bỏ chi tiết,
- giá trị của mô hình nằm ở khả năng dự báo, giải thích và hỗ trợ quyết định.

Vì vậy, khi dùng mô hình, ta luôn phải hỏi:

- giả định nào đang được đưa vào,
- giả định đó có hợp lý với bối cảnh dữ liệu không,
- và nếu giả định sai, kết luận lệch đi theo hướng nào.

## 5) Liên hệ trực tiếp với Bayesian inference

Trong Bayes, mô hình thống kê đi vào công thức qua likelihood:

$$
p(\theta\mid x) \propto p(x\mid\theta)\,p(\theta)
$$

Ở đây:

- $$p(x\mid\theta)$$ đến từ mô hình thống kê,
- $$p(\theta)$$ là prior,
- posterior $$p(\theta\mid x)$$ là kết quả cập nhật niềm tin.

Nếu định nghĩa mô hình không rõ, likelihood sẽ mơ hồ; khi đó posterior cũng mất ý nghĩa.

## 6) Một ví dụ mini: đo chiều cao sinh viên

Giả sử $$x_1,\dots,x_n$$ là chiều cao (cm) của sinh viên trong một lớp. Một mô hình đơn giản là:

$$
x_i \sim \mathcal{N}(\mu,\sigma^2),\quad i=1,\dots,n
$$

với $$\mu$$ là trung bình lớp và $$\sigma$$ là độ phân tán.

Mô hình này ngầm giả định:

- dữ liệu gần phân phối chuẩn,
- các quan sát độc lập có điều kiện theo tham số,
- mỗi quan sát đến từ cùng một cơ chế sinh dữ liệu.

Nhờ mô hình, ta có thể:

- ước lượng và diễn giải $$\mu, \sigma$$,
- dự báo giá trị mới,
- kiểm tra mô hình có bỏ sót cấu trúc quan trọng không.

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

*Bài học tiếp theo: [Bài 0.13: Kỳ vọng, Phương sai, và Hiệp phương sai](/vi/chapter00/expectation-variance-covariance/)*
