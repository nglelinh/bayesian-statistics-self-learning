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

Thực chất một **mô hình thống kê (statistical model)** là gì? Nó không phải là một hàm hộp đen `model.fit()` vô hồn — mà là **một câu chuyện toán học mô tả cách dữ liệu được sinh ra (generative story)!** Trong tư duy Bayes, viết một mô hình thống kê nghĩa là nêu tường minh hai mảnh ghép: quy luật sinh dữ liệu khi biết tham số (**hàm hợp lý** $$p(y\mid\theta)$$) và những giá trị tham số khả dĩ trước khi nhìn dữ liệu (**tiên nghiệm** $$p(\theta)$$).

Bài học này giúp bạn đọc và viết lưu loát ký hiệu mô hình sinh, phân biệt rạch ròi **tham số**, **dữ liệu** và **siêu tham số**, đồng thời biết kiểm tra mô hình bằng mô phỏng tiên nghiệm trước khi chạm vào dữ liệu thật.

---

## Bản đồ kiến thức nền: Bốn thành phần của một Mô hình Thống kê Sinh (Generative Model)

1. **Cấu trúc sinh dữ liệu (Hàm hợp lý $$p(y\mid\theta)$$):** Họ phân phối xác suất mô tả cách tín hiệu và nhiễu kết hợp để tạo ra quan sát $$y$$.
2. **Phân phối tiên nghiệm $$p(\theta\mid\phi)$$:** Mã hóa miền hợp lệ và thang đo hợp lý của tham số $$\theta$$, được điều khiển bởi các **siêu tham số** $$\phi$$.
3. **Mô phỏng chiều thuận (Prior Predictive):** Vì mô hình Bayes có tính sinh hoàn chỉnh, ta có thể rút $$\theta \sim p(\theta)$$ rồi sinh dữ liệu giả $$y_{\text{sim}} \sim p(y\mid\theta)$$ *trước khi* khớp dữ liệu — phát hiện ngay những tiên nghiệm vô lý (như dự báo điểm thi âm!).
4. **"Mọi mô hình đều sai, nhưng có những mô hình hữu ích" (George Box):** Mô hình là sự đơn giản hóa có chủ đích; giá trị của nó nằm ở khả năng giải thích cấu trúc, định lượng bất định và dự báo tốt trên dữ liệu mới.

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

---

### Ví dụ tính tay cầm tay chỉ việc: Kiểm tra mô hình điểm thi qua Phân phối Dự báo Tiên nghiệm

Giả sử bạn mô hình hóa điểm thi $$Y$$ với nhiễu đo lường đã biết $$\sigma = 10$$ và điểm trung bình lớp chưa biết $$\mu$$:

$$\mu \sim \mathcal{N}(70,\; 5^2), \qquad Y \mid \mu \sim \mathcal{N}(\mu,\; 10^2).$$

Trước khi chấm bất kỳ bài thi nào, một điểm thi tương lai $$Y = \mu + \varepsilon$$ tuân theo phân phối dự báo tiên nghiệm nào? Vì $$\mu$$ và $$\varepsilon$$ độc lập:
1. **Kỳ vọng dự báo tiên nghiệm:** $$\mathbb{E}[Y] = 70 + 0 = \mathbf{70}$$.
2. **Phương sai dự báo tiên nghiệm (phương sai hai nguồn độc lập cộng nhau!):**
   $$\mathrm{Var}(Y) = \mathrm{Var}(\mu) + \mathrm{Var}(\varepsilon) = 5^2 + 10^2 = 25 + 100 = \mathbf{125} \implies \mathrm{SD}(Y) = \sqrt{125} \approx \mathbf{11{,}18}.$$
3. **Khoảng 95% dự báo tiên nghiệm:** $$70 \pm 1{,}96(11{,}18) = \mathbf{[48{,}1;\; 91{,}9]}$$ — nằm gọn gàng trong thang điểm 0–100! *(Trái lại, một tiên nghiệm "phẳng" cẩu thả $$\mu \sim \mathcal{N}(70, 1000^2)$$ sẽ dự báo điểm thi từ $$-1890$$ đến $$+2030$$!)*

### Khung giải thích: Bốn nguyên tắc xây dựng mô hình thống kê chuẩn mực (nên đọc chậm)

1. **Luôn viết mô hình bằng 2–3 dòng ký hiệu toán trước khi gõ code:** Ký hiệu giúp mọi giả định ẩn hiện ra công khai để đồng nghiệp phản biện.
2. **Tách bất định tham số (epistemic) khỏi nhiễu dữ liệu (aleatoric):** Thu thêm dữ liệu làm $$\mathrm{Var}(\mu\mid y) \to 0$$, nhưng không bao giờ làm biến mất nhiễu cá thể $$\sigma^2 = 100$$.
3. **Luôn chạy kiểm tra dự báo tiên nghiệm (Prior Predictive Check):** Một biểu đồ 5 giây cứu bạn khỏi hàng giờ gỡ lỗi MCMC vô ích.
4. **Bắt đầu đơn giản rồi mở rộng dần:** Dựng mô hình nền tối giản trước, kiểm tra chỗ nào nó không khớp thực tế (PPC), rồi mới thêm phân cấp hoặc đuôi nặng Student-$$t$$.

**Kiểm tra nhanh.** Trong mô hình điểm thi ở trên, nếu bạn đã biết chắc chắn điểm trung bình lớp $$\mu = 70$$ (tức $$\mathrm{SD}(\mu) = 0$$), thì độ lệch chuẩn dự báo của một bài thi mới $$Y$$ sẽ còn lại bằng bao nhiêu?

---

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
