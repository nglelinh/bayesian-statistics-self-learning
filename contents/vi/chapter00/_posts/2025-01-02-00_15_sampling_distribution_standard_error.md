---
layout: post
title: "Bài 0.17: Sampling Distribution và Standard Error"
chapter: '00'
order: 17
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

Đầu thế kỷ 20, William Sealy Gosset làm việc tại nhà máy bia Guinness ở Dublin với một bài toán hết sức thực tế: ông chỉ có thể thử nghiệm trên vài mẻ lúa mạch nhỏ, nhưng vẫn cần biết trung bình mẫu của mình dao động mạnh đến mức nào nếu lặp lại thí nghiệm. Công trình ký bút danh "Student" của ông đã làm rõ khái niệm **phân phối lấy mẫu (sampling distribution)** — chiếc cầu nối giữa một mẫu hữu hạn ta cầm trên tay và quần thể ẩn phía sau.

Dù thống kê Bayes sử dụng phân phối hậu nghiệm thay cho phân phối lấy mẫu tần suất để suy luận trực tiếp về tham số, việc hiểu rạch ròi sự khác biệt giữa độ lệch chuẩn của dữ liệu (SD), sai số chuẩn của ước lượng (SE) và độ lệch chuẩn hậu nghiệm là điều kiện bắt buộc để đọc đúng mọi bảng kết quả thống kê.

---

## Mục tiêu học tập

Sau bài này, bạn sẽ phân biệt rõ phân phối của dữ liệu gốc với phân phối của ước lượng, hiểu sai số chuẩn (standard error) là độ bất định của bộ ước lượng chứ không phải độ phân tán của dữ liệu, và vận dụng trực giác này để đọc kết quả suy luận thống kê chính xác hơn.


## Kiến thức cần nhớ: Biến thiên dữ liệu, Phân phối lấy mẫu và Độ bất định ước lượng

Để không bao giờ nhầm lẫn giữa các loại "độ lệch chuẩn" trong thống kê, hãy đặt bài học này trên ba trụ cột:

- **Thống kê mẫu như biến ngẫu nhiên (Sampling Distribution):** Một thống kê như $$\bar X$$ hay $$\hat p$$ là hàm của dữ liệu ngẫu nhiên, nên bản thân nó cũng có phân phối xác suất riêng khi lặp lại quá trình lấy mẫu.
- **Độ lệch chuẩn (SD) so với Sai số chuẩn (SE):** SD đo mức độ phân tán giữa *các cá thể* trong dữ liệu ($$\sigma$$), còn SE đo mức độ dao động của *bản thân ước lượng* qua các lần lấy mẫu lặp lại ($$\sigma/\sqrt{n}$$).
- **Cầu nối sang Thống kê Bayes:** Trong Bayes, ta không cần giả định lấy mẫu lặp vô hạn để đo bất định của tham số; thay vào đó, ta đọc trực tiếp độ lệch chuẩn hậu nghiệm $$\mathrm{SD}(\theta \mid y)$$ và sai số chuẩn Monte Carlo (MCSE) của chuỗi MCMC — hai đại lượng song hành với tư duy SE nhưng trả lời trực tiếp câu hỏi về tham số.

---

## Giới thiệu: Từ một mẫu dữ liệu đến độ ổn định của ước lượng

Trong thực tế, ta thường chỉ quan sát được một mẫu dữ liệu duy nhất, nhưng vẫn cần đánh giá: "nếu lặp lại quy trình lấy mẫu nhiều lần, ước lượng hiện tại sẽ dao động mạnh đến mức nào?" Phân phối lấy mẫu (sampling distribution) và sai số chuẩn (standard error) là ngôn ngữ để định lượng câu hỏi đó.

## 1) Phân phối lấy mẫu (Sampling distribution) là gì?

Giả sử ta lặp lại cùng một quy trình lấy mẫu nhiều lần và ở mỗi lần đều tính một ước lượng $$\hat\theta$$ (chẳng hạn trung bình mẫu $$\bar X$$). Tập hợp các giá trị $$\hat\theta$$ thu được qua các lần lặp tạo thành **phân phối lấy mẫu (sampling distribution)**.

Điểm mấu chốt cần nhớ: phân phối lấy mẫu là phân phối của **ước lượng**, không phải phân phối của từng quan sát đơn lẻ.

![Sampling distribution của trung bình mẫu với n = 20]({{ site.baseurl }}/img/chapter_img/chapter00/sampling_distribution_n20.png)

*Hình 1a: Khi cỡ mẫu còn nhỏ ($$n = 20$$), phân phối lấy mẫu của trung bình mẫu khá rộng.*

## 2) Sai số chuẩn (Standard Error — SE)

Sai số chuẩn là độ lệch chuẩn của phân phối lấy mẫu:

$$
\mathrm{SE}(\hat\theta)=\sqrt{\mathrm{Var}(\hat\theta)}
$$

Đối với trung bình mẫu:

$$
\mathrm{SE}(\bar X)=\frac{\sigma}{\sqrt{n}}\approx\frac{s}{\sqrt{n}}
$$

Như vậy, độ lệch chuẩn (SD) của dữ liệu đo mức phân tán giữa các cá thể trong mẫu, còn sai số chuẩn (SE) đo mức độ bất định của chính ước lượng.

### Thử nghiệm: sampling distribution và sai số chuẩn

Tăng cỡ mẫu n và xem độ lệch chuẩn của trung bình mẫu giảm theo σ/√n.

<div class="interactive-demo" markdown="1">
<div data-demo="clt-explainer" data-lang="vi" data-tab="clt"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3) Nhầm lẫn phổ biến: SD và SE

Hai tập dữ liệu có cùng độ lệch chuẩn (SD) nhưng khác cỡ mẫu sẽ có sai số chuẩn (SE) khác nhau: cỡ mẫu $$n$$ càng lớn thì SE càng nhỏ và ước lượng càng ổn định; ngược lại, $$n$$ càng nhỏ thì SE càng lớn và kết luận càng kém chắc chắn.

![Sampling distribution của trung bình mẫu với n = 200]({{ site.baseurl }}/img/chapter_img/chapter00/sampling_distribution_n200.png)

*Hình 1b: Khi tăng cỡ mẫu lên $$n = 200$$, phân phối lấy mẫu thu hẹp rõ rệt, tương ứng với sai số chuẩn nhỏ hơn.*

### 3.1) Ví dụ phân biệt SD và SE

Giả sử cân nặng của một nhóm người có độ lệch chuẩn khoảng 12 kg:

- Với mẫu $$n=25$$ người, sai số chuẩn của trung bình là $$12/\sqrt{25}=2.4$$ kg.
- Với mẫu $$n=100$$ người, sai số chuẩn của trung bình là $$12/\sqrt{100}=1.2$$ kg.

Trong cả hai trường hợp, độ lệch chuẩn (SD) giữa các cá nhân vẫn là 12 kg; đại lượng thay đổi là độ bất định của **ước lượng trung bình**. Do đó không thể dùng SD và SE thay thế cho nhau.

## 4) Liên hệ giữa SE và khoảng bất định

Theo xấp xỉ chuẩn, khoảng bất định của ước lượng thường có dạng:

$$
\hat\theta \pm c\cdot \mathrm{SE}(\hat\theta)
$$

trong đó hệ số $$c$$ phụ thuộc vào mức độ tin cậy mong muốn (như 95% hay 90%). Dù khung suy luận là tần suất hay Bayesian, quy luật trực giác "SE càng lớn thì khoảng bất định càng rộng" vẫn giữ nguyên.

## 5) Liên hệ với quy trình Bayesian

Trong thống kê Bayesian, độ lệch chuẩn hậu nghiệm (posterior SD) của tham số đóng vai trò tương tự SE: nó phản ánh mức độ bất định còn lại về tham số sau khi đã kết hợp thông tin tiên nghiệm với dữ liệu. Nắm vững phân phối lấy mẫu và SE giúp việc đọc các khoảng hậu nghiệm trở nên tự nhiên hơn nhiều.

## Tóm tắt nhanh

1. Phân phối lấy mẫu là phân phối của bộ ước lượng qua các lần lấy mẫu lặp lại.
2. Sai số chuẩn (SE) là độ lệch chuẩn của bộ ước lượng.
3. Độ lệch chuẩn dữ liệu (SD) và sai số chuẩn (SE) đo hai đại lượng khác nhau.
4. Khi cỡ mẫu tăng, SE giảm theo tỷ lệ $$1/\sqrt{n}$$.


## Giải thích: Tách bạch ba tầng độ bất định

Khi đọc một báo cáo có ghi "trung bình $$50 \pm 2$$", hãy dừng lại và hỏi con số $$2$$ đó thuộc tầng nào trong ba tầng sau:

1. **Tầng dữ liệu (SD = $$s$$):** Phản ánh khoảng chênh lệch tự nhiên giữa các cá thể. Lấy thêm dữ liệu chỉ giúp ước lượng $$s$$ chính xác hơn chứ không làm $$s$$ tiến về 0.
2. **Tầng ước lượng (SE = $$s/\sqrt{n}$$):** Phản ánh độ ổn định của trung bình mẫu $$\bar x$$. Khi $$n$$ tăng gấp 4 lần, SE giảm đi một nửa và tiến về 0 khi $$n \to \infty$$.
3. **Tầng dự báo cá thể mới:** Khi dự đoán một quan sát mới $$X_{\text{new}}$$, độ bất định gộp cả hai nguồn: $$\sqrt{s^2 + s^2/n}$$ — luôn lớn hơn hoặc bằng SD.

### Ví dụ tính toán làm từng bước: Khảo sát chiều cao sinh viên

Giả sử đo chiều cao của $$n = 36$$ sinh viên, ta thu được trung bình mẫu $$\bar x = 168.0\text{ cm}$$ và độ lệch chuẩn mẫu $$s = 6.0\text{ cm}$$.

| Đại lượng | Công thức | Giá trị tính tay | Ý nghĩa thực tế |
| --- | --- | --- | --- |
| Độ lệch chuẩn mẫu (SD) | $$s$$ | $$6.0\text{ cm}$$ | Chênh lệch điển hình giữa các sinh viên trong lớp |
| Sai số chuẩn (SE) | $$s / \sqrt{n}$$ | $$6.0 / \sqrt{36} = 1.0\text{ cm}$$ | Độ dao động dự kiến của trung bình mẫu $$\bar x$$ |
| Biên sai số 95% của $$\bar x$$ | $$1.96 \times \mathrm{SE}$$ | $$1.96 \times 1.0 = 1.96\text{ cm}$$ | Khoảng tin cậy 95% cho chiều cao trung bình: $$[166.04,\; 169.96]\text{ cm}$$ |

**Hiểu lầm cần tránh:** Nhìn thấy khoảng $$168.0 \pm 1.96\text{ cm}$$ rồi kết luận "95% sinh viên cao từ 166 cm đến 170 cm". Thực tế đó là khoảng bất định cho *trung bình quần thể*, còn 95% sinh viên cá lẻ sẽ trải rộng quanh $$\bar x \pm 1.96 s \approx [156.2,\; 179.8]\text{ cm}$$.

**Kiểm tra nhanh:** Nếu tăng cỡ mẫu từ $$n = 36$$ lên $$n = 144$$ (gấp 4 lần), SD vẫn xoay quanh $$6.0\text{ cm}$$, còn SE giảm một nửa từ $$1.0\text{ cm}$$ xuống $$6.0 / \sqrt{144} = 0.5\text{ cm}$$.

---

## Video tham khảo

- [Standard Deviation vs Standard Error, Clearly Explained!!!](https://www.youtube.com/watch?v=A82brFpdr9g) — StatQuest with Josh Starmer, English. **Xem trước.** Phân biệt rõ độ phân tán của dữ liệu (SD) với độ bất định của ước lượng (SE).
- [Introduction to sampling distributions | Sampling distributions | AP Statistics | Khan Academy](https://www.youtube.com/watch?v=z0Ry_3_qhDw) — Khan Academy, English. Giới thiệu khái niệm phân phối lấy mẫu của một thống kê khi lặp lại quy trình lấy mẫu.
- [Standard error of the mean | Inferential statistics | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=J1twbrHel3o) — Khan Academy, English. Giải thích cách sai số chuẩn của trung bình mẫu thu nhỏ khi cỡ mẫu tăng.

## Câu hỏi tự luyện

1. Giải thích vì sao SD lớn không nhất thiết kéo theo SE lớn trong mọi trường hợp.
2. Nếu tăng cỡ mẫu từ 100 lên 400, sai số chuẩn thay đổi ra sao?
3. Phân phối lấy mẫu của trung vị (median) có giống phân phối lấy mẫu của trung bình (mean) không? Vì sao?

## Tài liệu tham khảo

- Rice, J. (2006). *Mathematical Statistics and Data Analysis*.
- Wasserman, L. (2004). *All of Statistics*.

---

*Bài học tiếp theo: [0.18 Ước lượng điểm, Bias-Variance, Consistency]({{ site.baseurl }}/contents/vi/chapter00/00_16_point_estimation_bias_variance_consistency/)*
