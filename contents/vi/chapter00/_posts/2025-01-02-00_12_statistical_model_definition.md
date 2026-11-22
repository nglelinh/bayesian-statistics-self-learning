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

Sau bài này, bạn sẽ hiểu định nghĩa thực dụng của mô hình thống kê như một mô tả xác suất về cách dữ liệu được sinh ra, phân biệt rõ dữ liệu quan sát với tham số chưa biết, và thấy vì sao việc nắm rõ giả định của mô hình luôn quan trọng hơn việc thuộc công thức.

## Giới thiệu: Mô hình như ngôn ngữ trung gian của suy luận

Trong thống kê, dữ liệu quan sát mới chỉ là điểm khởi đầu. Để đi từ dữ liệu đến kết luận về cơ chế thực tế đằng sau nó, ta cần một cấu trúc trung gian giúp phát biểu giả định, tạo dự báo và cập nhật hiểu biết khi có thêm thông tin. Cấu trúc đó chính là mô hình thống kê.

## 1) Động cơ: Dữ liệu không tự trả lời nếu thiếu mô hình

Từ một tập dữ liệu, ta có thể tính trung bình, độ lệch chuẩn hay vẽ histogram. Tuy nhiên, những con số mô tả đó chưa tự trả lời được các câu hỏi suy luận như tỷ lệ thật trong quần thể là bao nhiêu, hiệu ứng có đủ lớn về mặt thực tiễn hay không, hoặc dự báo tương lai bất định đến mức nào. Để giải quyết các câu hỏi này, ta cần cầu nối từ "tham số chưa biết" sang "dữ liệu có thể quan sát" — đó chính là mô hình thống kê.

## 2) Định nghĩa cốt lõi

Một **mô hình thống kê** là một họ các phân phối xác suất cho dữ liệu $$x$$, được chỉ số hóa bởi tham số $$\theta$$:

$$
\mathcal{M} = \{p(x\mid \theta): \theta \in \Theta\}
$$

Trong đó, $$x$$ là dữ liệu quan sát được, $$\theta$$ là đại lượng chưa biết chi phối cơ chế sinh dữ liệu, và $$\Theta$$ là không gian tham số — tập tất cả các giá trị hợp lệ mà $$\theta$$ có thể nhận. Nói ngắn gọn, mô hình thống kê mô tả "nếu tham số nhận giá trị $$\theta$$, dữ liệu sẽ có xu hướng phân bố như thế nào".

## 3) Góc nhìn sinh dữ liệu (generative story)

Trong khóa học này, ta ưu tiên đọc mô hình theo cơ chế sinh dữ liệu: trước hết tồn tại một tham số $$\theta$$ chưa biết, từ $$\theta$$ dữ liệu $$x$$ được sinh ra theo $$p(x\mid\theta)$$, và nhiệm vụ của phân tích là đối chiếu dữ liệu quan sát được với những gì mô hình dự kiến dưới các giá trị khả dĩ của $$\theta$$.

Xét ví dụ tung đồng xu: $$\theta$$ là xác suất ra Ngửa, mỗi lần tung cho một quan sát $$y_i \sim \text{Bernoulli}(\theta)$$, và sau $$n$$ lần tung thì tổng số lần ra Ngửa $$k=\sum_i y_i$$ tuân theo $$\text{Binomial}(n,\theta)$$. Ở đây, mô hình không chỉ là công thức nhị thức, mà còn bao gồm các giả định: mỗi lần tung có cùng xác suất $$\theta$$, các lần tung độc lập nhau, và thông tin được tóm tắt qua số lần ra Ngửa trong $$n$$ phép thử.

![Mô hình thống kê như cầu nối giữa tham số và dữ liệu]({{ site.baseurl }}/img/chapter_img/chapter00/statistical_model_definition_flow.png)

*Hình 1: Mô hình thống kê đóng vai trò cầu nối giữa tham số chưa biết $$\theta$$ và dữ liệu quan sát $$x$$ thông qua cơ chế sinh dữ liệu $$p(x\mid\theta)$$, từ đó cập nhật thành phân phối hậu nghiệm $$p(\theta\mid x)$$.*

## 3.1) Mô hình và mô phỏng khác nhau thế nào?

Hai khái niệm này dễ bị nhầm lẫn nhưng giữ vai trò khác nhau: **mô hình** là bản thiết kế khái niệm mô tả cơ chế xác suất sinh ra dữ liệu, còn **mô phỏng** là việc chạy bản thiết kế đó trên máy tính với tham số cụ thể để tạo dữ liệu giả nhiều lần.

Với ví dụ đồng xu, mô hình phát biểu $$y_i\sim\text{Bernoulli}(\theta)$$, còn mô phỏng là chọn một giá trị cụ thể như $$\theta = 0.6$$ rồi lặp lại việc tung nhiều lần để quan sát sự dao động của tỷ lệ ra Ngửa.

Ví dụ mô phỏng ngắn bằng Python:

```python
import numpy as np

np.random.seed(42)

theta = 0.6
n_tosses = 20
n_simulations = 10_000

heads_counts = np.random.binomial(n_tosses, theta, size=n_simulations)
head_rates = heads_counts / n_tosses

print(heads_counts[:10])
print(head_rates.mean(), head_rates.std())
```

Trong đoạn mã này, mô hình là $$K \sim \text{Binomial}(20, 0.6)$$. Bước mô phỏng giúp ta thấy nếu mô hình đó đúng, số mặt Ngửa trong 20 lần tung thường nằm quanh mức nào và dao động bao nhiêu giữa các lần lặp. Trung bình của `head_rates` sẽ tiến sát 0.6, nhưng từng mẫu riêng lẻ vẫn biến thiên quanh giá trị đó — minh họa rằng mô hình sinh ra một phân phối kết quả chứ không phải một con số cố định. Như vậy, mô phỏng không thay thế mô hình mà là công cụ kiểm tra trực giác và hệ quả của mô hình.

## 4) Mô hình không phải "sự thật" mà là xấp xỉ hữu ích

Một hiểu lầm phổ biến là tin rằng tồn tại một "mô hình đúng tuyệt đối". Trên thực tế, mô hình chỉ là bản đồ chứ không phải lãnh thổ: mọi mô hình đều lược bỏ một phần chi tiết, và giá trị của nó nằm ở khả năng dự báo, giải thích và hỗ trợ quyết định. Do đó, khi xây dựng mô hình, ta luôn cần tự hỏi những giả định nào đang được đặt ra, chúng có phù hợp với bối cảnh dữ liệu không, và kết luận sẽ lệch theo hướng nào nếu giả định bị vi phạm.

## 5) Liên hệ trực tiếp với suy diễn Bayesian

Trong thống kê Bayesian, mô hình thống kê đi vào định lý Bayes qua hàm hợp lý (likelihood):

$$
p(\theta\mid x) \propto p(x\mid\theta)\,p(\theta)
$$

Trong đó, $$p(x\mid\theta)$$ xuất phát từ mô hình thống kê, $$p(\theta)$$ là phân phối tiên nghiệm (prior), và $$p(\theta\mid x)$$ là phân phối hậu nghiệm (posterior) sau khi cập nhật dữ liệu. Nếu mô hình được đặc tả thiếu rõ ràng, hàm hợp lý sẽ mơ hồ và phân phối hậu nghiệm cũng mất ý nghĩa.

## 6) Một ví dụ ngắn: Đo chiều cao sinh viên

Giả sử $$x_1,\dots,x_n$$ là chiều cao (cm) của sinh viên trong một lớp. Một mô hình đơn giản là:

$$
x_i \sim \mathcal{N}(\mu,\sigma^2),\quad i=1,\dots,n
$$

với $$\mu$$ là chiều cao trung bình và $$\sigma$$ là độ lệch chuẩn. Mô hình này ngầm giả định dữ liệu gần phân phối chuẩn, các quan sát độc lập có điều kiện khi biết tham số, và tất cả quan sát đều phát sinh từ cùng một cơ chế. Từ đó ta có thể ước lượng $$\mu, \sigma$$, dự báo quan sát mới và kiểm tra xem mô hình có bỏ sót cấu trúc nào trong dữ liệu hay không.

### 6.1) Chọn mô hình theo bản chất dữ liệu

Nếu dữ liệu không phải chiều cao mà là số cuộc gọi đến tổng đài mỗi giờ ($$0, 1, 3, 2, 4, \dots$$), mô hình Poisson sẽ hợp lý hơn vì tôn trọng bản chất đếm nguyên không âm. Nếu ép dùng mô hình Normal, ta vẫn tính được trung bình và độ lệch chuẩn nhưng mô hình lại ngầm gán xác suất dương cho các giá trị âm vốn vô nghĩa trong thực tế. Vì thế, chọn mô hình là chọn một câu chuyện hợp lý về cơ chế sinh dữ liệu, và lựa chọn đó quyết định loại suy luận nào có ý nghĩa.

## Tóm tắt nhanh

1. Mô hình thống kê là họ phân phối $$\{p(x\mid\theta)\}$$ cho dữ liệu.
2. Nó kết nối tham số chưa biết với dữ liệu quan sát qua cơ chế sinh dữ liệu.
3. Mọi mô hình đều gắn với giả định; hiểu rõ giả định quan trọng hơn thuộc công thức.
4. Trong thống kê Bayesian, mô hình cung cấp hàm hợp lý để cập nhật từ tiên nghiệm sang hậu nghiệm.

## Video tham khảo

- [What is a statistical model?](https://www.youtube.com/watch?v=3d5ivs_8amQ) — Very Normal, English. **Xem trước.** Giải thích định nghĩa mô hình thống kê như mô tả xác suất về cách dữ liệu được sinh ra.
- [Statistical Rethinking 2023 - 01 - The Golem of Prague](https://www.youtube.com/watch?v=FdnMWdICdRs) — Richard McElreath, English. Phân tích vai trò của giả định và vì sao mô hình cần được kiểm soát thay vì dùng máy móc.
- [Regression and Other Stories: Generative models and statistical inference (ros02 4)](https://www.youtube.com/watch?v=kn8fyNzvcPo) — Data Science Learning Community Videos, English. Minh họa mối liên hệ giữa mô hình sinh dữ liệu và suy luận thống kê.

## Câu hỏi tự luyện

1. Với ví dụ tung đồng xu, hãy liệt kê ba giả định ngầm của mô hình Binomial.
2. Nêu một tình huống thực tế mà giả định độc lập giữa các quan sát bị vi phạm.
3. Vì sao nói "mô hình là bản đồ, không phải lãnh thổ"?

## Tài liệu tham khảo

- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Wasserman, L. (2004). *All of Statistics*. Springer.

---

*Bài học tiếp theo: [0.15 Kỳ vọng, Phương sai, và Hiệp phương sai]({{ site.baseurl }}/contents/vi/chapter00/00_13_expectation_variance_covariance/)*
