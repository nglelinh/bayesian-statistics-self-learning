---
layout: post
title: "Bài 8.3: Model Comparison Strategies"
chapter: '08'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter08
lesson_type: required
---

Sau khi có bảng điểm LOO/WAIC trong tay, phản xạ quen thuộc của hầu hết người làm dữ liệu là chọn lấy mô hình đứng hạng nhất và xóa sạch mọi mô hình còn lại. Nhưng điều gì xảy ra nếu Mô hình A và Mô hình B gần như ngang điểm nhau, mỗi mô hình lại nắm bắt một góc khác nhau của thực tế? Vứt bỏ Mô hình B đồng nghĩa với việc tự xóa đi phần **bất định về cấu trúc mô hình (model uncertainty)** và làm khoảng dự báo bị hẹp giả tạo.

Bài học này mở rộng tư duy từ "chọn một người thắng cuộc" sang ba chiến lược chiến lược chuẩn của thống kê Bayes hiện đại: **Chọn mô hình (Selection)**, **Kết hợp mô hình (Averaging / Stacking)** và **Mở rộng mô hình (Continuous Model Expansion)**.

---

## Mục tiêu học tập

Sau bài học này, bạn sẽ phân biệt rõ ba chiến lược so sánh mô hình trong thống kê Bayes: chọn một mô hình (selection), kết hợp nhiều mô hình (averaging) và mở rộng thành mô hình bao trùm (expansion). Trọng tâm là không xem so sánh mô hình như một thủ tục xếp hạng cơ học, mà như một bài toán ra quyết định dưới độ bất định về cấu trúc mô hình, trong đó chiến lược lựa chọn phụ thuộc vào mức độ tách biệt về hiệu năng dự báo và mục tiêu ứng dụng.


## Kiến thức cần nhớ: Chọn lọc, Kết hợp (BMA/Stacking) và Mở rộng Mô hình

Ba chiến lược xử lý đa mô hình tương ứng với ba bối cảnh thực tiễn rõ rệt:

- **Chọn mô hình (Model Selection):** Phù hợp khi một mô hình vượt trội rõ rệt ($$\Delta\text{elpd} \gg 2\,\mathrm{SE}$$) hoặc khi hệ thống vận hành đòi hỏi một mô hình đơn giản, gọn nhẹ duy nhất để triển khai và giải thích.
- **Kết hợp mô hình (BMA & Bayesian Stacking):** Thay vì chọn 1, ta trộn phân phối dự báo hậu nghiệm: $$p(\tilde y \mid y) = \sum_{k=1}^K w_k\, p(\tilde y \mid y, M_k)$$. Khác với BMA cổ điển (dễ nhạy với prior và giả định một trong các mô hình là mô hình thật — thế giới $$\mathcal{M}$$-closed), **Bayesian Stacking** (Yao et al., 2018) tối ưu hóa trực tiếp trọng số $$w_k$$ trên điểm LOO để tối đa hóa khả năng dự báo trong thế giới thực ($$\mathcal{M}$$-open).
- **Mở rộng mô hình (Model Expansion):** Thay vì coi hai mô hình rời rạc như hai đối thủ loại trừ nhau, ta nhúng cả hai vào một mô hình liên tục tổng quát hơn (ví dụ dùng phân phối Student-$$t$$ với bậc tự do $$\nu$$ học được thay vì chọn cứng giữa Gaussian và Cauchy).

---

## 1. So sánh mô hình không phải lúc nào cũng là chọn một mô hình thắng cuộc

Khi nhiều mô hình ứng viên có năng lực dự báo rất sát nhau, việc ép buộc phải chọn duy nhất một mô hình dễ tạo cảm giác chắc chắn giả tạo. Ngược lại, khi một mô hình vượt trội rõ rệt và ổn định qua các bước kiểm tra, duy trì nhiều mô hình chỉ làm tăng độ phức tạp mà không mang lại thêm giá trị dự báo. Do đó, câu hỏi đúng không phải là "mô hình nào đứng hạng nhất?", mà là "chiến lược nào tạo ra dự báo hữu ích nhất với mức độ bất định trung thực nhất?".

## 2. Chiến lược A — Chọn mô hình (Model Selection)

Chọn mô hình phù hợp khi khoảng cách về năng lực dự báo ngoài mẫu giữa mô hình tốt nhất và các mô hình còn lại đủ lớn so với độ bất định ước lượng. Khi đó, chi phí duy trì nhiều mô hình thường vượt quá lợi ích mang lại, còn một mô hình duy nhất giúp việc diễn giải, truyền đạt và triển khai trở nên gọn nhẹ hơn.

Tuy nhiên, điều kiện ngầm của chiến lược này là sự tách biệt phải đủ mạnh. Nếu chênh lệch giữa các chỉ số dự báo nhỏ và thiếu ổn định, việc chọn cứng một mô hình có thể khiến toàn bộ quy trình phụ thuộc vào dao động ngẫu nhiên của mẫu thay vì tín hiệu cấu trúc thật.

### Thử nghiệm: Hệ số Bayes là tỷ số hợp lý biên (marginal likelihood)

Tung đồng xu từng lần và quan sát $$BF_{10} = m_1(k)/m_0(k)$$ tích lũy; hợp lý biên tự động phạt các mô hình dàn trải xác suất quá rộng (hiệu ứng Occam).

<div class="interactive-demo" markdown="1">
<div data-demo="bf-explainer" data-lang="vi" data-tab="seq"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 3. Chiến lược B — Kết hợp mô hình (Model Averaging)

Kết hợp mô hình tuân theo nguyên tắc bảo toàn độ bất định giữa các mô hình bằng cách trộn các phân phối dự báo:

$$
p(\tilde y\mid y)=\sum_{k=1}^{K} w_k\,p_k(\tilde y\mid y),\qquad \sum_k w_k=1,\; w_k\ge 0.
$$

Trong thực hành hiện đại, trọng số stacking thường được ưu tiên vì chúng tối ưu trực tiếp năng lực dự báo của phân phối kết hợp, thay vì cố gán xác suất "đúng" hay "sai" tuyệt đối cho từng mô hình riêng lẻ.

### Thử nghiệm: Trung bình mô hình theo trọng số pseudo-BMA

Thêm từng mô hình vào tập ứng viên và quan sát sự thay đổi của trọng số $$w \propto \exp(\text{elpd}_{\text{loo}})$$ cùng dự báo trung bình.

<div class="interactive-demo" markdown="1">
<div data-demo="ic-explainer" data-lang="vi" data-tab="avg"></div>
</div>

### 3.1. Ví dụ định lượng ngắn

Giả sử tại một điểm dự báo mới, mô hình A cho trung bình 52, mô hình B cho trung bình 56, và trọng số stacking lần lượt là 0.58 và 0.42. Khi đó, dự báo trung bình của mô hình kết hợp là:

$$
0.58\times 52 + 0.42\times 56 = 53.68.
$$

Giá trị này phản ánh đồng thời tín hiệu từ cả hai mô hình lẫn độ bất định cấu trúc giữa chúng, thay vì cưỡng ép chọn 52 hoặc 56 như hai kịch bản loại trừ nhau.

![Selection vs Stacking predictive distributions]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_selection_vs_stacking.png)

### Thử nghiệm: Hệ số Bayes phụ thuộc vào độ rộng tiên nghiệm

Thay đổi tiên nghiệm $$\text{Beta}(c, c)$$ của $$M_1$$ và quan sát $$BF_{10}$$ biến thiên — lý do cần thực hiện phân tích độ nhạy.

<div class="interactive-demo" markdown="1">
<div data-demo="bf-explainer" data-lang="vi" data-tab="prior"></div>
</div>

## 4. Chiến lược C — Mở rộng mô hình (Model Expansion)

Mở rộng mô hình phù hợp khi các mô hình ứng viên phản ánh những mảnh ghép khác nhau của cùng một cơ chế sinh dữ liệu và có thể hợp nhất vào một mô hình lớn hơn — chẳng hạn bổ sung thành phần phi tuyến, hiệu ứng nhóm phân cấp hoặc các số hạng tương tác có điều chuẩn. Ưu điểm của hướng này là tạo ra một khung suy luận thống nhất thay vì duy trì nhiều mô hình rời rạc; rủi ro là tăng độ phức tạp tính toán và đòi hỏi kiểm tra chặt chẽ hơn để tránh quá khớp.

Có thể tóm tắt ngắn gọn: chọn mô hình xử lý sự cạnh tranh giữa các mô hình; kết hợp mô hình xử lý độ bất định giữa các mô hình; còn mở rộng mô hình xử lý sự thiếu hụt về cấu trúc của tập mô hình hiện có.

## 5. Quy tắc lựa chọn chiến lược trong thực hành

Ta có thể tóm lược một quy tắc thực hành như sau: nếu chênh lệch hiệu năng dự báo đủ lớn và ổn định, ưu tiên chọn mô hình (selection); nếu nhiều mô hình gần ngang sức, ưu tiên kết hợp mô hình (averaging) để bảo toàn độ bất định; nếu mọi mô hình đều bộc lộ sai lệch cơ chế trong PPC, ưu tiên mở rộng mô hình (expansion) thay vì tranh luận xem mô hình nào "ít sai nhất".

Quy tắc này cần luôn đi kèm bước kiểm tra chẩn đoán (chẳng hạn Pareto $$k$$ trong LOO) và kết quả phê bình mô hình. Một bảng xếp hạng gọn gàng không thể thay thế bằng chứng cho thấy mô hình vẫn đang bỏ sót cấu trúc quan trọng của dữ liệu.

## 6. Ví dụ tổng hợp: Cùng dữ liệu, ba quyết định khác nhau

Giả sử ta có ba mô hình M1, M2, M3 và kết quả LOO cho thấy M1 và M2 sát nhau trong phạm vi sai số chuẩn, còn M3 kém hơn rõ rệt. Khi mục tiêu là dự báo ngắn hạn ổn định, kết hợp giữa M1 và M2 thường hợp lý hơn chọn một mô hình. Nếu mục tiêu là giải thích cơ chế và M1 đơn giản hơn đáng kể, ta vẫn có thể chọn M1 với điều kiện báo cáo rõ độ bất định mô hình còn lại. Ngược lại, nếu PPC cho thấy cả M1 lẫn M2 đều sai lệch ở phần đuôi, quyết định đúng nhất không phải chọn hay trộn, mà là mở rộng mô hình để sửa trực tiếp cơ chế sinh dữ liệu.

Ví dụ này cho thấy so sánh mô hình là bài toán ra quyết định đa mục tiêu: cân bằng giữa dự báo, khả năng diễn giải, chi phí triển khai và tính trung thực với độ bất định.

## 7. Kết luận bài 8.3

Không tồn tại một chiến lược so sánh mô hình duy nhất đúng cho mọi tình huống. Selection, averaging và expansion là ba công cụ bổ sung lẫn nhau trong cùng một quy trình Bayes. Năng lực của người phân tích nằm ở việc nhận biết đúng lúc nào nên thu gọn bằng chọn mô hình, lúc nào nên bảo toàn độ bất định bằng kết hợp mô hình, và lúc nào cần tái thiết kế mô hình để khắc phục sai lệch cơ chế.

Bài tiếp theo: **Phân tích quyết định Bayes (Bayesian Decision Analysis)**, chuyển kết quả suy luận thành hành động tối ưu dưới một hàm mất mát cụ thể.


## Giải thích: Tính dự báo và phương sai khi Kết hợp mô hình (Stacking / BMA)

Khi hai mô hình ngang sức nhau (ví dụ $$\Delta\text{elpd} < 2\,\mathrm{SE}$$), hãy đi chậm qua 3 bước để kết hợp dự báo thay vì chọn cứng:

1. **Xác định trọng số $$w_1, \dots, w_K$$** ($$\sum w_k = 1, w_k \ge 0$$) từ Bayesian Stacking hoặc trọng số Akaike/Pseudo-BMA.
2. **Tính trung bình dự báo kết hợp:** $$\mu_{\text{comb}} = \sum_{k=1}^K w_k \mu_k$$.
3. **Tính phương sai dự báo kết hợp (cộng cả độ bất đồng giữa các mô hình!):**
   $$\sigma_{\text{comb}}^2 = \sum_{k=1}^K w_k \sigma_k^2 + \sum_{k=1}^K w_k (\mu_k - \mu_{\text{comb}})^2.$$

### Ví dụ tính toán làm từng bước: Trộn dự báo doanh số từ 2 mô hình theo trọng số Stacking

Giả sử hai mô hình dự báo doanh số quý tới (tỷ VNĐ) có điểm LOO rất sát nhau, với trọng số Stacking là $$w_1 = 0.60$$ và $$w_2 = 0.40$$:
- Mô hình 1 (tuyến tính): $$\mu_1 = 100$$, $$\sigma_1 = 5$$ ($$\sigma_1^2 = 25$$).
- Mô hình 2 (phi tuyến): $$\mu_2 = 110$$, $$\sigma_2 = 5$$ ($$\sigma_2^2 = 25$$).

| Thành phần | Công thức | Giá trị tính tay |
| --- | --- | --- |
| Trung bình kết hợp $$\mu_{\text{comb}}$$ | $$0.6(100) + 0.4(110)$$ | $$60 + 44 = 104.0\text{ tỷ}$$ |
| Phương sai nội mô hình | $$0.6(25) + 0.4(25)$$ | $$25.0$$ |
| Phương sai bất đồng giữa 2 mô hình | $$0.6(100 - 104)^2 + 0.4(110 - 104)^2$$ | $$0.6(16) + 0.4(36) = 9.6 + 14.4 = 24.0$$ |
| Tổng phương sai & Độ lệch chuẩn | $$\sigma_{\text{comb}}^2 = 25 + 24 = 49$$ | $$\sigma_{\text{comb}} = \sqrt{49} = 7.0\text{ tỷ}$$ |

Nhìn vào con số $$7.0\text{ tỷ}$$ so với $$5.0\text{ tỷ}$$: nếu chỉ chọn Mô hình 1, bạn sẽ báo cáo độ bất định $$\pm 5\text{ tỷ}$$ (quá tự tin). Kết hợp mô hình tự động mở rộng độ lệch chuẩn lên $$\pm 7\text{ tỷ}$$ để phản ánh trung thực sự bất đồng giữa hai giả định cấu trúc!

**Hiểu lầm cần tránh:** Nhầm rằng Stacking hay Model Averaging luôn cho ra dự báo có phương sai *nhỏ hơn* từng mô hình đơn lẻ. Khi các mô hình bất đồng mạnh về tâm dự báo, phương sai tổng có thể *lớn hơn* — và đó chính là dấu hiệu trung thực, giúp tránh bất ngờ ngoài mẫu.

**Kiểm tra nhanh:** Nếu hai mô hình hoàn toàn đồng ý về tâm dự báo ($$\mu_1 = \mu_2 = 104$$), số hạng bất đồng bằng $$0$$ và $$\sigma_{\text{comb}} = 5.0\text{ tỷ}$$.

---

## Video tham khảo

- [Statistical Rethinking 2023 - 20 - Horoscopes](https://www.youtube.com/watch?v=qwF-st2NGTU) — Richard McElreath, English. **Xem trước**. Giải thích vì sao bảng xếp hạng mô hình không phải lời tiên tri, củng cố lập luận không chọn kẻ thắng bằng mọi giá.
- [16a Prediction and Model Averaging](https://www.youtube.com/watch?v=707hT6qYghw) — Philip Ramsey, English. Minh họa phương pháp kết hợp dự báo giữa nhiều mô hình thay vì chỉ chọn một mô hình duy nhất.
- [Statistical Rethinking 2026 - Lecture B02 - Multilevel Model Expansion](https://www.youtube.com/watch?v=Nv2rm1s9q6I) — Richard McElreath, English. Trình bày chiến lược mở rộng mô hình nhiều tầng, đặt cạnh hai hướng selection và averaging.

## Câu hỏi tự luyện

1. Khi hai mô hình có chênh lệch LOO rất nhỏ so với sai số chuẩn, vì sao việc chọn cứng một mô hình có thể kém trung thực hơn kết hợp mô hình?
2. Trong tình huống nào chiến lược mở rộng mô hình (expansion) tốt hơn cả selection lẫn averaging?
3. Nếu mục tiêu chính là diễn giải nhân quả, thứ tự ưu tiên giữa các chiến lược sẽ thay đổi ra sao so với mục tiêu dự báo thuần túy?

## Tài liệu tham khảo

- Yao, Y., et al. (2018). "Using stacking to average Bayesian predictive distributions." *Bayesian Analysis*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition).

---

*Bài học tiếp theo: [8.4 Bayesian Decision Analysis]({{ site.baseurl }}/contents/vi/chapter08/08_04_decision_analysis/)*
