---
layout: post
title: "Bài 8.4: Bayesian Decision Analysis - From Inference to Action"
chapter: '08'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter08
lesson_type: required
---

## Mục tiêu học tập

Sau bài học này, bạn sẽ biết cách chuyển kết quả suy luận Bayes thành hành động cụ thể dưới độ bất định thông qua hàm mất mát (loss function), mất mát kỳ vọng (expected loss) và giá trị thông tin (value of information). Trọng tâm của bài là phân biệt hai câu hỏi khác nhau: phân phối hậu nghiệm trả lời "ta tin điều gì?", còn lý thuyết quyết định trả lời "ta nên làm gì?" khi mỗi lựa chọn đi kèm chi phí sai lầm không đối xứng.

## 1. Suy luận không đồng nghĩa với quyết định

Một phân phối hậu nghiệm rất sắc nét vẫn chưa tự động xác định được hành động đúng, vì quyết định còn phụ thuộc vào hệ quả của từng loại sai lầm. Cùng một xác suất hậu nghiệm có thể dẫn tới hai hành động khác nhau khi cấu trúc thiệt hại thay đổi. Vì vậy, phân tích quyết định (decision analysis) là bước cuối cùng không thể thiếu của quy trình Bayes.

Khung chuẩn gồm bốn thành phần: tập hành động $$a\in\mathcal A$$, trạng thái thế giới $$\theta$$, phân phối hậu nghiệm $$p(\theta\mid y)$$ và hàm mất mát $$L(a,\theta)$$. Quy tắc hành động Bayes (Bayes action) chọn hành động tối thiểu hóa mất mát kỳ vọng hậu nghiệm:

$$
a^*(y)=\arg\min_{a\in\mathcal A} \mathbb E[L(a,\theta)\mid y]
=\arg\min_{a\in\mathcal A}\int L(a,\theta)p(\theta\mid y)\,d\theta.
$$

## 2. Quy tắc ngưỡng từ chi phí bất đối xứng

Xét bài toán cảnh báo rủi ro với hai hành động: phát cảnh báo ($$a_1$$) và không cảnh báo ($$a_0$$). Gọi $$q=P(H_1\mid y)$$ là xác suất hậu nghiệm xảy ra sự cố, $$L_{FP}$$ là chi phí báo động giả và $$L_{FN}$$ là chi phí bỏ sót sự cố. Khi đó, rủi ro kỳ vọng của mỗi hành động là:

$$
R(a_1\mid y)=L_{FP}(1-q),\qquad R(a_0\mid y)=L_{FN}q.
$$

Ta chọn phát cảnh báo khi $$R(a_1\mid y)<R(a_0\mid y)$$, tương đương:

$$
q>\frac{L_{FP}}{L_{FP}+L_{FN}}.
$$

Với $$L_{FP}=5$$ và $$L_{FN}=40$$, ngưỡng quyết định chỉ là $$q^*=5/45\approx 0.111$$. Điều này cho thấy quyết định tối ưu rất nhạy với cấu trúc chi phí, ngay cả khi phân phối hậu nghiệm không hề thay đổi.

![Expected loss threshold rule]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_expected_loss_threshold.png)

### 2.1. Ý nghĩa nghiệp vụ

Nếu tổn thất của việc bỏ sót sự cố lớn hơn nhiều lần so với báo động giả, tổ chức nên cảnh báo sớm hơn — tức sử dụng ngưỡng xác suất hậu nghiệm thấp hơn. Ngược lại, nếu báo động giả gây tốn kém lớn, ngưỡng hậu nghiệm cần được nâng cao để tránh can thiệp quá mức. Vì vậy, ngưỡng quyết định tối ưu không phải một hằng số phổ quát mà là hàm của cấu trúc mất mát trong từng bối cảnh cụ thể.

### Thử nghiệm: Ngưỡng quyết định trong thử nghiệm A/B

Thêm từng lô 150 người dùng, theo dõi $$\pi = P(p > p_0)$$ và so sánh với ngưỡng $$c_{fp}/(c_{fp} + c_{fn})$$.

<div class="interactive-demo" markdown="1">
<div data-demo="decision-explainer" data-lang="vi" data-tab="threshold"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Hàm mất mát và điểm tóm tắt hậu nghiệm

Trong bài toán ước lượng điểm, việc chọn trung bình (mean), trung vị (median) hay mốt (mode) không phải là sở thích trình bày, mà xuất phát trực tiếp từ hàm mất mát được giả định:

- Mất mát bình phương $$L(\hat\theta,\theta)=(\hat\theta-\theta)^2$$ → tối ưu là trung bình hậu nghiệm (posterior mean),
- Mất mát trị tuyệt đối $$L(\hat\theta,\theta)=|\hat\theta-\theta|$$ → tối ưu là trung vị hậu nghiệm (posterior median),
- Mất mát 0–1 (rời rạc) → tối ưu là mốt hậu nghiệm (posterior mode).

Như vậy, mọi báo cáo dưới dạng một "ước lượng điểm đại diện" đều ngầm mang theo một giả định về chi phí sai số, dù người phân tích có nêu rõ hay không.

### Thử nghiệm: Mỗi hàm mất mát cho một điểm tóm tắt tối ưu khác nhau

Mất mát bình phương → trung bình, trị tuyệt đối → trung vị, 0–1 → mốt, bất đối xứng → phân vị.

<div class="interactive-demo" markdown="1">
<div data-demo="decision-explainer" data-lang="vi" data-tab="loss"></div>
</div>

## 4. Từ bằng chứng đến hành động: Vai trò của hệ số Bayes

Với hai giả thuyết $$H_0,H_1$$, hệ số Bayes (Bayes factor) được định nghĩa:

$$
BF_{10}=\frac{p(D\mid H_1)}{p(D\mid H_0)}.
$$

Hệ số này cập nhật tỷ số odds qua biểu thức:

$$
\frac{P(H_1\mid D)}{P(H_0\mid D)}=BF_{10}\times\frac{P(H_1)}{P(H_0)}.
$$

Tuy nhiên, ngay cả khi $$BF_{10}$$ ủng hộ mạnh $$H_1$$, hành động cuối cùng vẫn phải đi qua mất mát kỳ vọng. Hệ số Bayes trả lời câu hỏi "dữ liệu ủng hộ giả thuyết nào hơn?", còn phân tích quyết định trả lời câu hỏi "trong cấu trúc chi phí hiện tại, hành động nào là tối ưu?".

## 5. Giá trị thông tin (Value of Information): Khi nào nên thu thập thêm dữ liệu

Không phải lúc nào thu thập thêm dữ liệu cũng mang lại lợi ích ròng. Giá trị thông tin được đo bằng mức giảm của mất mát kỳ vọng:

$$
\text{VOI}=\mathbb E[L\mid \text{quyết định ngay}] - \mathbb E[L\mid \text{có thêm thông tin}].
$$

Quy tắc hành động tương ứng là:

$$
\text{Thu thập thêm dữ liệu nếu } \text{VOI} > \text{chi phí thu thập}.
$$

Ví dụ, nếu mất mát kỳ vọng hiện tại là 12 và có thể giảm xuống 5 sau khi bổ sung thông tin, ta có $$\text{VOI} = 7$$. Nếu chi phí thu thập là 4, lợi ích ròng dương nên đáng thu thập thêm; nếu chi phí là 10, lợi ích ròng âm nên hợp lý hơn là quyết định ngay với thông tin sẵn có.

![Value of information decision curve]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_voi_decision_curve.png)

### Thử nghiệm: EVSI và cỡ mẫu tối ưu

So sánh giá trị kỳ vọng của thông tin mẫu bổ sung (EVSI) với chi phí thu thập để lựa chọn cỡ mẫu hợp lý.

<div class="interactive-demo" markdown="1">
<div data-demo="decision-explainer" data-lang="vi" data-tab="voi"></div>
</div>

## 6. Ví dụ tổng hợp: Quyết định trong A/B testing

Giả sử hai phiên bản sản phẩm A và B có phân phối hậu nghiệm cho tỷ lệ chuyển đổi lần lượt là $$p_A$$ và $$p_B$$. Bước suy luận cung cấp xác suất $$P(p_B>p_A\mid D)$$, nhưng quyết định triển khai không nên chỉ dựa cơ học vào con số này. Ta cần mô hình hóa hàm lợi ích hoặc mất mát kinh doanh: giá trị mỗi lượt chuyển đổi, chi phí triển khai, tổn thất nếu chọn sai và thời gian phản ứng. Hành động tối ưu là hành động tối đa hóa lợi ích kỳ vọng (hoặc tối thiểu hóa mất mát kỳ vọng), chứ không nhất thiết là hành động vượt qua một ngưỡng xác suất cố định.

Đây là điểm giao nhau trực tiếp giữa thống kê và quản trị: cùng một phân phối hậu nghiệm, hai doanh nghiệp có cấu trúc chi phí khác nhau hoàn toàn có thể đi đến hai quyết định tối ưu khác nhau.

## 7. Quy trình thực hành phân tích quyết định

Một quy trình chặt chẽ thường gồm bốn bước: (i) xác định tập hành động khả thi, (ii) xây dựng hàm mất mát hoặc lợi ích rõ ràng và hợp lý về mặt nghiệp vụ, (iii) tính mất mát kỳ vọng dựa trên phân phối hậu nghiệm hoặc dự báo hậu nghiệm, và (iv) kiểm tra độ nhạy của quyết định khi thay đổi giả định về chi phí. Bước thứ tư đặc biệt quan trọng vì nhiều quyết định có thể đảo chiều khi ước lượng chi phí thay đổi.

Dưới góc nhìn khoa học, một quyết định Bayes tốt không phải là quyết định chắc chắn đúng tuyệt đối, mà là quyết định tối ưu dựa trên thông tin hiện có và cấu trúc mất mát được khai báo minh bạch.

## 8. Kết luận bài 8.4

Phân tích quyết định Bayes khép lại chu trình của Chương 08: PPC giúp phát hiện sai lệch của mô hình, WAIC/LOO giúp so sánh năng lực dự báo, các chiến lược so sánh mô hình giúp xử lý độ bất định mô hình, và lý thuyết quyết định chuyển toàn bộ kết quả suy luận thành hành động cụ thể. Nếu suy luận là khoa học cập nhật niềm tin dưới bất định, thì phân tích quyết định là kỷ luật biến niềm tin đó thành lựa chọn có cơ sở.

Kết thúc Chương 08: phê bình mô hình → so sánh mô hình → ra quyết định.

## Video tham khảo

- [(ML 11.3) Frequentist risk, Bayesian expected loss, and Bayes risk](https://www.youtube.com/watch?v=b1GxZdFN6cY) — mathematicalmonk, English. **Xem trước**. Trình bày mất mát kỳ vọng và rủi ro Bayes, nối trực tiếp từ phân phối hậu nghiệm sang hành động tối ưu.
- [Decision Analysis 2: EMV & EVPI - Expected Value & Perfect Information](https://www.youtube.com/watch?v=tbv9E9D2BRQ) — Joshua Emmanuel, English. Giải thích giá trị kỳ vọng của thông tin hoàn hảo, hỗ trợ phần giá trị thông tin (VOI).
- [Decision Theory: Loss Functions & Bayes Criterion (Worked Example 3)](https://www.youtube.com/watch?v=c7_L0-0Bvs8) — StatsResource, English. Minh họa một bài toán quyết định với hàm mất mát cụ thể để thấy cùng một xác suất có thể dẫn tới các hành động khác nhau.

## Câu hỏi tự luyện

1. Vì sao hai tổ chức có cùng phân phối hậu nghiệm về rủi ro lại có thể đưa ra hai hành động tối ưu khác nhau?
2. Nếu chi phí báo động giả tăng gấp đôi, ngưỡng quyết định $$q^*$$ sẽ thay đổi theo chiều hướng nào?
3. Khi giá trị thông tin (VOI) dương nhưng rất sát chi phí thu thập, bạn cần kiểm tra thêm điều gì trước khi quyết định thu thập dữ liệu?

## Tài liệu tham khảo

- Berger, J. O. (1985). *Statistical Decision Theory and Bayesian Analysis*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition), Chapter 9.

---

*Chương tiếp theo: [Chapter 12: Labs Thực Hành Bayesian]({{ site.baseurl }}/vi/chapter12/)*
