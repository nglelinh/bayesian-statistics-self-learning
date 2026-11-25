---
layout: post
title: "Bài 8.2: Information Criteria - WAIC và LOO"
chapter: '08'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter08
lesson_type: required
---

Thêm tham số vào mô hình hầu như lúc nào cũng làm tăng độ khớp trên tập dữ liệu hiện có, nhưng lại có thể phá hỏng khả năng dự báo trên dữ liệu mới. Làm sao ước lượng được **độ chính xác dự báo ngoài mẫu (out-of-sample predictive accuracy)** mà không phải chạy lại MCMC hàng trăm lần như kiểm định chéo *leave-one-out* thủ công?

Công trình đột phá của Sumio Watanabe (2010, WAIC) và Aki Vehtari, Andrew Gelman, Jonah Gabry (2017, PSIS-LOO) đã giải quyết trọn vẹn bài toán này: chỉ từ **một** lần chạy MCMC duy nhất, ta có thể ước lượng chính xác hiệu năng dự báo ngoài mẫu kèm cả sai số chuẩn và tín hiệu cảnh báo chẩn đoán (chỉ số Pareto $$k$$).

---

## Mục tiêu học tập

Sau bài học này, bạn sẽ hiểu WAIC và LOO như những công cụ xấp xỉ năng lực dự báo ngoài mẫu của mô hình Bayes, đồng thời biết đọc kết quả kèm theo độ bất định ước lượng thay vì xếp hạng một cách cứng nhắc. Trọng tâm của bài là lập luận phương pháp: vì sao cần ưu tiên tiêu chí dự báo ngoài mẫu, khi nào chênh lệch giữa các mô hình đủ lớn để đưa ra kết luận, và khi nào nên chuyển từ chọn một mô hình sang kết hợp nhiều mô hình (model averaging).


## Kiến thức cần nhớ: ELPD, WAIC, PSIS-LOO và Chẩn đoán Pareto $$k$$

So sánh mô hình Bayes hiện đại xoay quanh ba trụ cột toán học cốt lõi:

- **Mật độ dự báo log kỳ vọng (ELPD — Expected Log Pointwise Predictive Density):** Thước đo mục tiêu cho khả năng dự báo ngoài mẫu: $$\text{elpd} = \sum_{i=1}^n \mathbb{E}_{\tilde y_i}[\log p(\tilde y_i \mid y)]$$. Điểm ELPD càng **cao** (càng ít âm) thì mô hình dự báo càng tốt (khác với thang deviance/AIC càng thấp càng tốt).
- **WAIC (Widely Applicable Information Criterion):** Tách ELPD thành độ khớp trong mẫu (**lppd**) trừ đi số tham số hiệu dụng (**$$p_{\text{WAIC}}$$** — tính bằng tổng phương sai của log-likelihood hậu nghiệm từng điểm). Khác với AIC hay DIC, WAIC tận dụng toàn bộ phân phối hậu nghiệm thay vì chỉ một ước lượng điểm.
- **PSIS-LOO & Chỉ số Pareto $$k$$:** Xấp xỉ kiểm định chéo bỏ-từng-điểm (*leave-one-out*) bằng lấy mẫu quan trọng làm mượt theo phân phối Pareto tổng quát (*Pareto Smoothed Importance Sampling*). Chỉ số $$\hat k_i$$ là công cụ chẩn đoán cực kỳ quý giá: $$\hat k_i < 0.5$$ là rất tin cậy, $$0.5 \le \hat k_i \le 0.7$$ chấp nhận được, còn $$\hat k_i > 0.7$$ cảnh báo điểm dữ liệu $$i$$ có ảnh hưởng quá lớn — cần tính LOO trực tiếp hoặc xem lại mô hình.

---

## 1. Từ độ khớp trong mẫu sang dự báo ngoài mẫu

Vấn đề kinh điển của so sánh mô hình là mô hình càng linh hoạt càng dễ đạt độ khớp tốt trên tập huấn luyện, nhưng chính sự linh hoạt đó có thể làm suy giảm khả năng dự báo trên dữ liệu mới. Do đó, đại lượng đáng quan tâm không phải sai số trong mẫu mà là mật độ dự báo dạng log ngoài mẫu (expected log predictive density). Ở dạng từng điểm quan sát (pointwise), ta xét tổng:

$$
\text{elpd} = \sum_{i=1}^n \log p(y_i\mid y_{-i}),
$$

trong đó mỗi quan sát $$y_i$$ được đánh giá như một điểm dữ liệu mới khi mô hình đã học từ toàn bộ phần dữ liệu còn lại $$y_{-i}$$.

Ý tưởng này chặt chẽ về mặt lý thuyết nhưng rất tốn kém nếu phải khớp lại mô hình nhiều lần; WAIC và PSIS-LOO ra đời như hai phương pháp thực dụng để xấp xỉ cùng mục tiêu đó.

## 2. WAIC: Xấp xỉ hoàn toàn theo hướng Bayes cho độ chính xác dự báo

WAIC được viết dưới dạng:

$$
\text{WAIC}=-2\,(\text{lppd}-p_{\text{WAIC}}),
$$

trong đó $$\text{lppd}$$ đo độ khớp dự báo trên từng điểm dữ liệu, còn $$p_{\text{WAIC}}$$ là số tham số hiệu dụng đóng vai trò phạt độ phức tạp để hạn chế quá khớp. Khi so sánh các mô hình trên cùng tập dữ liệu, giá trị WAIC thấp hơn tương ứng với năng lực dự báo tốt hơn (tương đương với $$\text{elpd}$$ lớn hơn).

Cần lưu ý rằng WAIC không phải một thang điểm tuyệt đối: nó chỉ có ý nghĩa khi đặt trong tương quan giữa các mô hình cạnh tranh và phải đi kèm sai số chuẩn của độ chênh lệch.

## 3. PSIS-LOO: Chuẩn tham chiếu gần thực tế hơn

Kiểm định chéo loại từng phần tử (LOO-CV) lý tưởng đòi hỏi bỏ lần lượt từng quan sát và khớp lại mô hình, trong khi PSIS-LOO dùng kỹ thuật lấy mẫu trọng số có làm mượt Pareto (Pareto-smoothed importance sampling) để xấp xỉ quy trình đó mà không cần khớp lại toàn bộ. Vì bám sát định nghĩa dự báo ngoài mẫu hơn, PSIS-LOO thường được ưu tiên trong quy trình Bayes hiện đại, với điều kiện chỉ số chẩn đoán Pareto $$k$$ cho thấy phép xấp xỉ đủ tin cậy.

Tóm lại: WAIC nhanh và thuận tiện; PSIS-LOO thường đáng tin cậy hơn; và cả hai đều phải được diễn giải cùng độ bất định ước lượng.

![WAIC and LOO comparison with uncertainty]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_waic_loo_comparison.png)

### Thử nghiệm: WAIC và LOO ước lượng chất lượng dự báo ngoài mẫu

Tăng bậc đa thức từng bước để quan sát $$\text{lppd}$$ trong mẫu luôn tăng, còn $$\text{elpd}$$ theo WAIC và LOO (bám sát $$\text{elpd}$$ trên dữ liệu mới) đạt đỉnh rồi giảm. Bảng kết quả hiển thị $$p_{\text{waic}}$$, $$\Delta\text{elpd}$$ và sai số chuẩn.

<div class="interactive-demo" markdown="1">
<div data-demo="ic-explainer" data-lang="vi" data-tab="waic"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 4. Đọc bảng so sánh mô hình: Chênh lệch và độ bất định

Giả sử ba mô hình cho kết quả theo thang $$\text{elpd}$$ như sau (giá trị càng cao càng tốt):

- Mô hình A: $$\text{elpd} = -221$$, $$\text{SE} = 5$$
- Mô hình B: $$\text{elpd} = -220$$, $$\text{SE} = 5.5$$
- Mô hình C: $$\text{elpd} = -229$$, $$\text{SE} = 6$$

Kết luận hợp lý là C kém hơn rõ rệt so với A và B, còn A và B gần như tương đương vì chênh lệch 1 điểm nhỏ hơn nhiều so với độ bất định đi kèm. Trong trường hợp này, tuyên bố "B thắng" là kết luận quá mức; cách xử lý hợp lý hơn là xem A và B như nhóm mô hình ngang sức, sau đó cân nhắc kết hợp mô hình (averaging) hoặc ưu tiên mô hình dễ diễn giải hơn nếu mục tiêu truyền đạt là quan trọng.

## 5. Chỉ số Pareto $$k$$: Điều kiện tin cậy của PSIS-LOO

Với PSIS-LOO, chỉ số Pareto $$k$$ cho biết các trọng số lấy mẫu quan trọng có ổn định hay không. Ngưỡng thực hành thường dùng gồm:

- $$k<0.5$$: phép xấp xỉ ổn định,
- $$0.5\le k\le 0.7$$: có thể sử dụng nhưng cần thận trọng,
- $$k>0.7$$: phép xấp xỉ có thể kém tin cậy, cần kiểm tra lại các điểm ảnh hưởng lớn và cân nhắc phương án thay thế.

Pareto $$k$$ không phải chi tiết phụ: nếu bước chẩn đoán này không đạt, bảng xếp hạng LOO dù trông gọn gàng vẫn không đủ cơ sở vững chắc để ra quyết định.

## 6. Ví dụ phương pháp luận: Khi nào đủ bằng chứng để chọn mô hình

Giả sử mô hình đứng đầu có $$\text{elpd}$$ cao hơn mô hình thứ hai 6 điểm, với sai số chuẩn của chênh lệch khoảng 2. Khi đó ta có khoảng cách đủ thuyết phục để chọn mô hình đứng đầu cho mục tiêu dự báo. Ngược lại, nếu chênh lệch chỉ là 1.5 trong khi sai số chuẩn là 2.2, kết luận hợp lý nên là "chưa đủ bằng chứng phân biệt rõ", và nên cân nhắc kết hợp dự báo hoặc giữ nhiều mô hình cho các mục tiêu khác nhau.

Nói cách khác, so sánh mô hình trong thống kê Bayes là bài toán suy luận dưới bất định, không phải cuộc thi chấm điểm dựa trên một con số duy nhất.

## 7. Thực hành tốt khi dùng WAIC và LOO

Có ba nguyên tắc thực hành cốt lõi. Thứ nhất, luôn so sánh các mô hình trên cùng một tập dữ liệu và cùng biến mục tiêu để chênh lệch có ý nghĩa. Thứ hai, luôn đọc đồng thời giá trị ước lượng và sai số chuẩn thay vì chỉ nhìn thứ hạng. Thứ ba, khi nhiều mô hình đạt hiệu năng sát nhau, hãy chuyển từ tư duy "chọn duy nhất mô hình đứng đầu" sang tư duy kết hợp dự báo.

Trong tổng thể quy trình Bayes, WAIC và LOO không thay thế PPC: một mô hình có điểm dự báo tốt hơn vẫn có thể sai lệch cơ chế ở những vùng quan trọng của bài toán. Vì vậy, phê bình mô hình (PPC) và so sánh mô hình (WAIC/LOO) cần được sử dụng bổ trợ cho nhau.

## 8. Kết luận bài 8.2

WAIC và LOO cung cấp thước đo định lượng để so sánh năng lực dự báo ngoài mẫu giữa các mô hình, nhưng giá trị lớn nhất của chúng nằm ở kỷ luật diễn giải: luôn đọc chênh lệch kèm độ bất định, luôn kiểm tra chẩn đoán của phép xấp xỉ, và luôn gắn lựa chọn mô hình với mục tiêu dự báo thay vì chọn máy móc theo thứ hạng.

Bài tiếp theo: **Các chiến lược so sánh mô hình (Model Comparison Strategies)**, đi sâu vào lựa chọn giữa chọn mô hình (selection), kết hợp mô hình (averaging) và mở rộng mô hình (expansion).


## Giải thích: Tự tính WAIC bằng tay và đọc bảng chênh lệch ELPD có sai số chuẩn

Để thực sự hiểu WAIC và LOO đang tính gì bên dưới hàm `az.compare()`, hãy đi chậm qua 4 bước:

1. **Lập ma trận log-likelihood** cỡ $$S \times n$$ (hàng là mẫu hậu nghiệm $$s$$, cột là điểm dữ liệu $$i$$).
2. **Tính $$\text{lppd}_i = \log\!\left(\frac{1}{S}\sum_{s=1}^S p(y_i \mid \theta^{(s)})\right)$$** cho từng điểm rồi cộng lại.
3. **Tính phạt độ phức tạp $$p_{\text{WAIC}} = \sum_{i=1}^n \mathrm{Var}_{s}(\log p(y_i \mid \theta^{(s)}))$$:** Điểm nào có log-likelihood dao động mạnh qua các mẫu hậu nghiệm thì đóng góp phạt lớn.
4. **Tính $$\widehat{\text{elpd}}_{\text{WAIC}} = \text{lppd} - p_{\text{WAIC}}$$** và khi so hai mô hình, luôn đối chiếu $$\Delta\text{elpd}$$ với sai số chuẩn $$\mathrm{SE}(\Delta\text{elpd})$$!

### Ví dụ tính toán làm từng bước: Tính $$\text{lppd}_i$$ và $$p_{\text{WAIC},i}$$ cho 1 điểm dữ liệu với $$S = 2$$ mẫu hậu nghiệm

Giả sử tại điểm dữ liệu $$i$$, hai mẫu hậu nghiệm $$\theta^{(1)}, \theta^{(2)}$$ cho xác suất hợp lý là $$p_1 = 0.20$$ và $$p_2 = 0.40$$ (tương ứng $$\log p_1 \approx -1.6094$$ và $$\log p_2 \approx -0.9163$$):

| Bước tính | Công thức | Giá trị tính tay |
| --- | --- | --- |
| Độ khớp điểm $$\text{lppd}_i$$ | $$\ln\!\left(\frac{0.20 + 0.40}{2}\right) = \ln(0.30)$$ | $$-1.2040$$ |
| Trung bình log-likelihood | $$\frac{-1.6094 + (-0.9163)}{2}$$ | $$-1.2629$$ |
| Phạt độ phức tạp $$p_{\text{WAIC}, i}$$ (phương sai mẫu $$S-1=1$$) | $$\frac{(-1.6094+1.2629)^2 + (-0.9163+1.2629)^2}{2-1}$$ | $$0.2402$$ |
| Đóng góp ELPD của điểm $$i$$ | $$\text{lppd}_i - p_{\text{WAIC}, i}$$ | $$-1.2040 - 0.2402 = -1.4442$$ |

Khi so sánh hai mô hình trên cả tập dữ liệu: giả sử Mô hình A có $$\text{elpd}_{\text{LOO}} = -120.5$$ và Mô hình B có $$\text{elpd}_{\text{LOO}} = -124.0$$ (chênh lệch $$\Delta\text{elpd} = 3.5$$) với $$\mathrm{SE}(\Delta\text{elpd}) = 4.2$$. Vì $$\Delta\text{elpd} < 2\,\mathrm{SE}$$, sự chênh lệch này **chưa đủ bằng chứng mạnh** để loại bỏ Mô hình B!

**Hiểu lầm cần tránh:** Nhìn thấy Mô hình A có ELPD cao hơn Mô hình B dù chỉ $$0.8$$ điểm (trong khi $$\mathrm{SE} = 3.0$$) rồi vội tuyên bố "Mô hình A thắng tuyệt đối". Chênh lệch nhỏ hơn $$2\,\mathrm{SE}$$ thường nằm trong vùng nhiễu lấy mẫu.

**Kiểm tra nhanh:** Nếu $$\Delta\text{elpd} = 18.0$$ và $$\mathrm{SE}(\Delta\text{elpd}) = 4.5$$, tỷ số $$z = 18.0 / 4.5 = 4.0$$ — đây là bằng chứng rất rõ ràng cho thấy mô hình đứng đầu vượt trội về dự báo ngoài mẫu.

---

## Video tham khảo

- [Evaluating model fit through AIC, DIC, WAIC and LOO-CV](https://www.youtube.com/watch?v=xS4jDHQfP2o) — Ben Lambert, English. **Xem trước**. Đặt AIC, DIC, WAIC và LOO-CV cạnh nhau để so sánh các cách ước lượng năng lực dự báo ngoài mẫu.
- [BDA 2019 Lecture 9.1 PSIS-LOO and K-fold cross-validation](https://www.youtube.com/watch?v=D0kVMie93Yk) — Aki Vehtari, English. Trình bày PSIS-LOO và kiểm định chéo K-fold, củng cố lý do ưu tiên LOO hơn độ khớp trong mẫu.
- [31- Pareto k diagnostics in R](https://www.youtube.com/watch?v=h4g5KUWRzyg) — Horizon 2 Reach, English. Giải thích chẩn đoán Pareto $$k$$ — điều kiện cần kiểm tra trước khi tin tưởng ước lượng PSIS-LOO.

## Câu hỏi tự luyện

1. Vì sao chênh lệch WAIC/LOO nhỏ hơn sai số chuẩn của chênh lệch không đủ cơ sở để khẳng định một mô hình vượt trội hơn?
2. Nếu một mô hình đứng hạng nhất nhưng có nhiều điểm dữ liệu mang chỉ số Pareto $$k>0.7$$, bạn sẽ xử lý kết quả đó như thế nào?
3. Trong những tình huống nào bạn nên ưu tiên kết hợp mô hình (model averaging) thay vì chọn một mô hình duy nhất?

## Tài liệu tham khảo

- Vehtari, A., Gelman, A., & Gabry, J. (2017). "Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC." *Statistics and Computing*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition), Chapter 7.

---

*Bài học tiếp theo: [8.3 Model Comparison Strategies]({{ site.baseurl }}/contents/vi/chapter08/08_03_model_comparison/)*
