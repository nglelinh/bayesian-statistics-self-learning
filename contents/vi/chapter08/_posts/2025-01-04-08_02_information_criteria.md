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

## Mục tiêu học tập

Sau bài học này, bạn cần hiểu WAIC và LOO như các công cụ xấp xỉ năng lực dự báo ngoài mẫu của mô hình Bayes, đồng thời biết đọc kết quả theo bất định ước lượng thay vì theo tư duy "xếp hạng cứng". Trọng tâm của bài là lập luận phương pháp: vì sao phải ưu tiên tiêu chí dự báo ngoài mẫu, khi nào chênh lệch giữa các mô hình đủ lớn để kết luận, và khi nào nên chuyển từ model selection sang model averaging.

## 1. Từ training fit sang out-of-sample prediction

Vấn đề cổ điển của model comparison là mô hình càng linh hoạt càng dễ đạt training fit tốt, nhưng chính tính linh hoạt đó lại có thể làm giảm năng lực dự báo trên dữ liệu mới. Vì vậy, đại lượng đáng quan tâm không phải lỗi trong mẫu mà là log predictive density ngoài mẫu. Trong ngôn ngữ pointwise, ta quan tâm tổng

$$
\text{elpd} = \sum_{i=1}^n \log p(y_i\mid y_{-i}),
$$

trong đó mỗi quan sát được đánh giá như một điểm chưa từng thấy khi mô hình đã học từ phần dữ liệu còn lại.

Ý tưởng này rất mạnh về mặt khái niệm nhưng đắt đỏ về tính toán nếu phải refit mô hình nhiều lần; WAIC và PSIS-LOO xuất hiện như hai lối đi thực dụng để xấp xỉ cùng mục tiêu.

## 2. WAIC: một xấp xỉ Bayes hoàn toàn cho predictive accuracy

WAIC có thể viết dưới dạng

$$
\text{WAIC}=-2\,(\text{lppd}-p_{\text{WAIC}}),
$$

trong đó lppd phản ánh độ khớp dự báo pointwise, còn $$p_{\text{WAIC}}$$ đóng vai trò độ phức tạp hiệu dụng để phạt overfitting. Khi so sánh nhiều mô hình trên cùng dữ liệu, WAIC thấp hơn tương ứng với predictive performance tốt hơn (hoặc, tương đương, elpd lớn hơn).

Điều cần nhấn mạnh là WAIC không phải một "điểm số tuyệt đối" của mô hình; nó chỉ có ý nghĩa trong tương quan với các mô hình cạnh tranh và phải đi kèm sai số chuẩn của chênh lệch.

## 3. PSIS-LOO: gần chuẩn tham chiếu hơn cho thực hành

LOO-CV lý tưởng yêu cầu bỏ từng quan sát rồi refit mô hình, còn PSIS-LOO dùng importance sampling được Pareto-smoothed để xấp xỉ quy trình đó mà không cần refit toàn bộ. Vì gần với định nghĩa ngoài mẫu trực tiếp hơn, LOO thường được ưu tiên trong workflow hiện đại, với điều kiện diagnostic Pareto $$k$$ cho thấy xấp xỉ đủ tin cậy.

Một cách đọc ngắn gọn nhưng đúng bản chất là: WAIC thường nhanh và tiện; PSIS-LOO thường đáng tin hơn; cả hai đều phải được diễn giải cùng bất định ước lượng.

![WAIC and LOO comparison with uncertainty]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_waic_loo_comparison.png)

## 4. Đọc bảng so sánh mô hình: chênh lệch và độ bất định

Giả sử ba mô hình cho kết quả theo thang elpd như sau (giá trị càng cao càng tốt):

- Mô hình A: elpd = -221, SE = 5
- Mô hình B: elpd = -220, SE = 5.5
- Mô hình C: elpd = -229, SE = 6

Kết luận hợp lý là C kém hơn rõ rệt so với A và B, nhưng A và B gần như hòa vì chênh lệch 1 điểm nhỏ hơn đáng kể so với mức bất định đi kèm. Trong tình huống này, việc tuyên bố "B thắng" là diễn giải quá tay; lựa chọn trưởng thành hơn là xem A và B như một tập mô hình cạnh tranh gần ngang nhau, rồi cân nhắc averaging hoặc ưu tiên mô hình dễ diễn giải hơn nếu mục tiêu truyền thông quan trọng.

## 5. Pareto k: điều kiện tin cậy của PSIS-LOO

Với PSIS-LOO, chỉ số Pareto $$k$$ trả lời câu hỏi: trọng số importance sampling có ổn định không. Một ngưỡng thực hành thường dùng là:

- $$k<0.5$$: rất ổn,
- $$0.5\le k\le 0.7$$: dùng được nhưng cần cẩn trọng,
- $$k>0.7$$: xấp xỉ có thể kém tin cậy, cần kiểm tra kỹ và cân nhắc biện pháp thay thế.

Điểm quan trọng là Pareto $$k$$ không phải một chi tiết phụ. Nếu diagnostic thất bại, bảng xếp hạng LOO có thể nhìn đẹp nhưng không còn nền tảng đủ vững để ra quyết định.

## 6. Ví dụ phương pháp luận: khi nào "đủ bằng chứng" để chọn mô hình

Giả sử mô hình tốt nhất có elpd cao hơn mô hình đứng thứ hai 6 điểm, trong khi sai số chuẩn của chênh lệch khoảng 2. Khi đó ta có thể xem là có khoảng cách đủ thuyết phục để chọn mô hình tốt nhất cho mục tiêu dự báo. Ngược lại, nếu chênh lệch chỉ 1.5 với sai số chuẩn 2.2, kết luận khoa học nên là "chưa phân biệt được rõ", và chiến lược hợp lý hơn thường là averaging hoặc giữ nhiều mô hình cho các mục tiêu khác nhau.

Nói cách khác, model comparison trong Bayes là bài toán suy luận dưới bất định, không phải cuộc thi điểm số với một con số duy nhất.

## 7. Thực hành tốt khi dùng WAIC/LOO

Thực hành tốt có thể tóm lược thành ba nguyên tắc. Thứ nhất, luôn so sánh trên cùng một dữ liệu và cùng biến mục tiêu để đảm bảo ý nghĩa của chênh lệch. Thứ hai, đọc đồng thời estimate và SE thay vì chỉ nhìn rank. Thứ ba, nếu nhiều mô hình sát nhau, chuyển từ logic "winner-takes-all" sang logic kết hợp dự báo.

Từ góc nhìn workflow, WAIC/LOO không thay thế PPC: một mô hình có điểm dự báo tốt hơn vẫn có thể sai cơ chế ở những vùng mà bài toán quan tâm đặc biệt, do đó model criticism và model comparison phải được dùng bổ sung, không dùng thay thế.

## 8. Kết luận bài 8.2

WAIC và LOO cung cấp ngôn ngữ định lượng để so sánh mô hình theo năng lực dự báo ngoài mẫu, nhưng giá trị lớn nhất của chúng nằm ở cách diễn giải có kỷ luật: luôn đọc chênh lệch cùng bất định, luôn kiểm tra diagnostic của phép xấp xỉ, và luôn gắn quyết định chọn mô hình với mục tiêu dự báo cụ thể thay vì với thói quen chọn hạng nhất.

Bài tiếp theo: **Model Comparison Strategies**, nơi ta đi sâu vào lựa chọn giữa selection, averaging, và expansion.

## Câu hỏi tự luyện

1. Vì sao chênh lệch WAIC/LOO nhỏ hơn sai số chuẩn của chênh lệch không đủ để tuyên bố mô hình thắng?
2. Nếu một mô hình đứng hạng nhất nhưng có nhiều điểm Pareto $$k>0.7$$, bạn sẽ xử lý kết quả đó thế nào?
3. Khi nào bạn ưu tiên model averaging thay vì chọn một mô hình duy nhất?

## Tài liệu tham khảo

- Vehtari, A., Gelman, A., & Gabry, J. (2017). "Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC." *Statistics and Computing*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition), Chapter 7.

---

*Bài học tiếp theo: [8.3 Model Comparison Strategies](/vi/chapter08/model-comparison/)*
