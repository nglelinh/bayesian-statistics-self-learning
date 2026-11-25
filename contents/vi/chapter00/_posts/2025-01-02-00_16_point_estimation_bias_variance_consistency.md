---
layout: post
title: "Bài 0.18: Ước lượng điểm, Bias-Variance, Consistency"
chapter: '00'
order: 18
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

Trong phần lớn thế kỷ 20, thống kê học xoay quanh một câu hỏi tưởng như hiển nhiên: làm sao nén toàn bộ dữ liệu thành *một con số tốt nhất* đại diện cho tham số chưa biết — và "tốt nhất" nghĩa là gì? Ronald Fisher đặt nền móng cho ước lượng hợp lý cực đại (MLE), nhưng năm 1956 Charles Stein gây chấn động giới toán học khi chứng minh rằng ở từ 3 chiều trở lên, một bộ ước lượng *có chệch nhẹ* (co về gốc tọa độ) lại đạt sai số bình phương trung bình thấp hơn mọi bộ ước lượng không chệch cổ điển.

Câu chuyện của Stein chính là cánh cửa tự nhiên dẫn sang tư duy Bayes: chấp nhận một chút độ chệch có kiểm soát (từ phân phối prior) để đổi lấy sự sụt giảm mạnh của phương sai khi dữ liệu còn ít.

---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu ba tiêu chí cốt lõi để đánh giá một bộ ước lượng (estimator): độ chệch (bias), phương sai (variance) và tính nhất quán (consistency), đồng thời nắm được sự đánh đổi độ chệch – phương sai (bias–variance tradeoff) như một nguyên lý thực hành khi thiết kế mô hình.


## Kiến thức cần nhớ: Lý thuyết ước lượng điểm, Phân rã MSE và Cầu nối sang Co cụm Bayes

Bốn khái niệm trong bài này tạo thành ngôn ngữ đánh giá chuẩn cho mọi bộ ước lượng (từ MLE, OLS đến Posterior Mean và MAP):

- **Độ chệch và Phương sai (Bias & Variance):** Độ chệch $$\mathrm{Bias}(\hat\theta) = \mathbb{E}[\hat\theta] - \theta$$ đo sai lệch hệ thống, còn phương sai $$\mathrm{Var}(\hat\theta)$$ đo mức dao động của ước lượng theo mẫu.
- **Sai số bình phương trung bình (MSE Decomposition):** Mọi sai số bình phương trung bình đều tách gọn thành $$\mathrm{MSE}(\hat\theta) = \mathrm{Bias}(\hat\theta)^2 + \mathrm{Var}(\hat\theta)$$. Đây là nền toán học cho đánh đổi độ chệch – phương sai trong học máy và điều chuẩn.
- **Tính nhất quán (Consistency) & Tiệm cận Bayes:** Một ước lượng nhất quán hội tụ về giá trị thật $$\theta$$ khi $$n \to \infty$$. Trong thống kê Bayes, định lý Bernstein–von Mises khẳng định rằng dưới điều kiện chính quy, phân phối hậu nghiệm cũng hội tụ về giá trị thật và thu hẹp quanh MLE khi dữ liệu đủ lớn — tức ước lượng Bayes vừa nhất quán vừa tối ưu hơn khi cỡ mẫu nhỏ.

---

## Giới thiệu: Đánh giá ước lượng không thể chỉ nhìn một mẫu duy nhất

Một bộ ước lượng tốt không chỉ cho kết quả "gần đúng" trong một lần lấy mẫu ngẫu nhiên. Ta cần xem xét hành vi của nó trên nhiều mẫu khả dĩ: có lệch có hệ thống không, có dao động quá mạnh giữa các mẫu không, và khi cỡ mẫu tăng lên thì có hội tụ về giá trị thật không. Ba tiêu chí bias, variance và consistency được xây dựng để trả lời ba câu hỏi này.

![Bias variance tradeoff]({{ site.baseurl }}/img/chapter_img/chapter00/bias_variance_tradeoff_curve.png)

*Hình 1: Khi độ phức tạp mô hình tăng, độ chệch (bias) giảm dần nhưng phương sai (variance) tăng lên, khiến sai số bình phương trung bình (MSE) đạt cực tiểu tại một điểm cân bằng.*

## 1) Ước lượng điểm là gì?

Ước lượng điểm (point estimator) là một hàm của dữ liệu $$\hat\theta=g(x_1,\dots,x_n)$$ dùng để đưa ra một giá trị ước lượng cụ thể cho tham số chưa biết $$\theta$$. Ví dụ, ta dùng trung bình mẫu $$\bar X$$ để ước lượng $$\mu$$, tỷ lệ mẫu $$\hat p$$ để ước lượng $$p$$, hoặc hệ số hồi quy mẫu để ước lượng độ dốc thật.

## 2) Độ chệch (Bias)

Độ chệch đo sai lệch có hệ thống của bộ ước lượng so với giá trị thật:

$$
\mathrm{Bias}(\hat\theta)=\mathbb{E}[\hat\theta]-\theta
$$

Nếu $$\mathrm{Bias}(\hat\theta) = 0$$, bộ ước lượng được gọi là không chệch (unbiased); nếu khác 0, bộ ước lượng có xu hướng lệch hệ thống về một phía.

## 3) Phương sai (Variance) của bộ ước lượng

Ngay cả một bộ ước lượng không chệch vẫn có thể dao động mạnh từ mẫu này sang mẫu khác. Mức độ dao động đó được đo bằng phương sai $$\mathrm{Var}(\hat\theta)$$. Vì vậy, một bộ ước lượng tốt không chỉ cần ít chệch mà còn cần phương sai đủ nhỏ.

## 4) MSE và phân rã độ chệch – phương sai

Sai số bình phương trung bình (Mean Squared Error — MSE):

$$
\mathrm{MSE}(\hat\theta)=\mathbb{E}[(\hat\theta-\theta)^2]
$$

được phân rã thành hai thành phần:

$$
\mathrm{MSE}(\hat\theta)=\mathrm{Bias}(\hat\theta)^2+\mathrm{Var}(\hat\theta)
$$

Đẳng thức này là nền tảng cho tư duy điều chuẩn (regularization): chấp nhận một chút độ chệch để đổi lấy mức giảm phương sai lớn hơn, qua đó hạ tổng sai số dự báo.

### 4.1) Một ví dụ cụ thể về đánh đổi bias – variance

Giả sử cần ước lượng tham số thật $$\theta = 10$$ bằng hai bộ ước lượng:

- Bộ ước lượng A không chệch ($$\mathrm{Bias}=0$$) nhưng có phương sai bằng $$9$$.
- Bộ ước lượng B chệch lên 1 đơn vị ($$\mathrm{Bias}=1$$) nhưng có phương sai chỉ bằng $$4$$.

Khi đó:

$$
\mathrm{MSE}(A) = 0^2 + 9 = 9,
\qquad
\mathrm{MSE}(B) = 1^2 + 4 = 5.
$$

Dù có độ chệch, bộ ước lượng B vẫn đạt MSE thấp hơn vì giảm được phương sai đáng kể. Đây chính là nguyên lý đứng sau các kỹ thuật co rút (shrinkage) và điều chuẩn (regularization).

## 5) Tính nhất quán (Consistency)

Bộ ước lượng $$\hat\theta_n$$ được gọi là nhất quán (consistent) nếu nó hội tụ theo xác suất về giá trị thật khi cỡ mẫu tiến ra vô cùng:

$$
\hat\theta_n \xrightarrow[]{P} \theta \quad \text{khi } n\to\infty
$$

Nói đơn giản, khi lượng dữ liệu ngày càng lớn, ước lượng sẽ càng tiến sát tham số thật.

## 6) Liên hệ với thống kê Bayesian

Trong thống kê Bayesian, ta làm việc với toàn bộ phân phối hậu nghiệm thay vì chỉ một ước lượng điểm. Dù vậy, góc nhìn bias–variance vẫn rất hữu ích: một phân phối tiên nghiệm mạnh thường giúp giảm phương sai ước lượng nhưng có thể kéo theo độ chệch nếu tiên nghiệm đặt lệch; ngược lại, tiên nghiệm yếu ít gây chệch nhưng có thể khiến phương sai lớn khi dữ liệu còn ít.

## Tóm tắt nhanh

1. Độ chệch (bias) đo sai lệch hệ thống của bộ ước lượng.
2. Phương sai (variance) đo độ dao động của bộ ước lượng giữa các mẫu.
3. $$\mathrm{MSE} = \mathrm{Bias}^2 + \mathrm{Var}$$.
4. Tính nhất quán (consistency) mô tả sự hội tụ về giá trị thật khi cỡ mẫu lớn.


## Giải thích: Khi nào một ước lượng "có chệch" lại đánh bại ước lượng "không chệch"?

Hãy đọc chậm bốn bước sau để thấy vì sao "không chệch" không phải lúc nào cũng là mục tiêu tối thượng:

1. **Đặt thước đo tổng sai số là MSE:** Một ước lượng tốt phải ở gần $$\theta$$ nhất có thể về trung bình bình phương: $$\mathrm{MSE} = \mathrm{Bias}^2 + \mathrm{Var}$$.
2. **So sánh MLE (không chệch) với ước lượng co cụm Bayes (có chệch nhẹ):** Khi $$n$$ nhỏ, MLE bám sát dữ liệu nhiễu nên phương sai lớn.
3. **Tính toán cụ thể phần đánh đổi:** Nếu thêm một độ chệch nhỏ $$b$$ (đóng góp $$b^2$$ vào MSE) giúp giảm phương sai đi nhiều hơn $$b^2$$, tổng MSE sẽ giảm ròng.
4. **Kiểm tra giới hạn $$n \to \infty$$:** Trọng số của prior giảm theo $$1/n$$, nên độ chệch tiến về 0 và tính nhất quán vẫn được bảo toàn.

### Ví dụ tính toán làm từng bước: So sánh MLE và Posterior Mean với $$n = 4$$

Giả sử xác suất thật là $$\theta = 0.4$$ và ta tung đồng xu $$n = 4$$ lần ($$K \sim \text{Binomial}(4, 0.4)$$). So sánh hai bộ ước lượng:
- **MLE (không chệch):** $$\hat\theta_{\text{MLE}} = K / 4$$.
- **Posterior Mean với prior $$\text{Beta}(1, 1)$$:** $$\hat\theta_{\text{Bayes}} = \frac{K + 1}{4 + 2} = \frac{K + 1}{6}$$.

Ta có $$\mathbb{E}[K] = 4 \times 0.4 = 1.6$$ và $$\mathrm{Var}(K) = 4 \times 0.4 \times 0.6 = 0.96$$. Tính tay từng thành phần:

| Bộ ước lượng | Kỳ vọng $$\mathbb{E}[\hat\theta]$$ | $$\mathrm{Bias}$$ | $$\mathrm{Bias}^2$$ | $$\mathrm{Var}(\hat\theta)$$ | $$\mathrm{MSE} = \mathrm{Bias}^2 + \mathrm{Var}$$ |
| --- | --- | --- | --- | --- | --- |
| $$\hat\theta_{\text{MLE}} = K/4$$ | $$1.6 / 4 = 0.4000$$ | $$0.0000$$ | $$0.0000$$ | $$0.96 / 16 = 0.0600$$ | $$0.0600$$ |
| $$\hat\theta_{\text{Bayes}} = (K+1)/6$$ | $$2.6 / 6 \approx 0.4333$$ | $$+0.0333$$ | $$0.0011$$ | $$0.96 / 36 \approx 0.0267$$ | $$0.0278$$ |

Chỉ bằng cách chấp nhận độ chệch rất nhỏ ($$+0.0333$$, bình phương chỉ $$0.0011$$), bộ ước lượng Bayes đã cắt giảm hơn **một nửa** tổng sai số MSE (từ $$0.0600$$ xuống $$0.0278$$)!

**Hiểu lầm cần tránh:** Nghĩ rằng ước lượng không chệch luôn tốt hơn ước lượng có chệch. Khi cỡ mẫu nhỏ hoặc số tham số lớn, phương sai mới là kẻ thù chính làm hỏng dự báo.

**Kiểm tra nhanh:** Nếu tăng cỡ mẫu lên $$n = 400$$, độ chệch của $$\hat\theta_{\text{Bayes}} = (K+1)/402$$ chỉ còn $$(161/402) - 0.4 \approx +0.0005$$ — tiến sát về 0 đúng như tính nhất quán.

---

## Video tham khảo

- [Unbiasedness vs consistency of estimators - an example](https://www.youtube.com/watch?v=6i7mqDJICzQ) — Ben Lambert, English. **Xem trước.** Minh họa sự khác nhau giữa tính không chệch và tính nhất quán của bộ ước lượng.
- [[Proof] MSE = Variance + Bias²](https://www.youtube.com/watch?v=qmVT35gFW-Q) — math et al, English. Trình bày phép chứng minh phân rã MSE thành bình phương độ chệch cộng phương sai.
- [Population and Estimated Parameters, Clearly Explained!!!](https://www.youtube.com/watch?v=vikkiwjQqfU) — StatQuest with Josh Starmer, English. Giải thích mối liên hệ giữa tham số quần thể và ước lượng mẫu khi cỡ mẫu thay đổi.

## Câu hỏi tự luyện

1. Một bộ ước lượng có độ chệch nhỏ nhưng MSE lớn có thể xảy ra không? Vì sao?
2. Vì sao điều chuẩn (regularization) có thể cải thiện chất lượng dự báo dù làm xuất hiện độ chệch?
3. Tính nhất quán có bảo đảm bộ ước lượng hoạt động tốt trên mẫu nhỏ không?

## Tài liệu tham khảo

- Casella, G., & Berger, R. (2002). *Statistical Inference*.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*.

---

*Bài học tiếp theo: [0.19 Log-probability và Ổn định số]({{ site.baseurl }}/contents/vi/chapter00/00_17_log_probability_numerical_stability/)*
