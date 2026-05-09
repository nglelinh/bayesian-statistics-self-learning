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

## Mục tiêu học tập

Sau bài học này, bạn cần phân biệt rõ ba chiến lược so sánh mô hình trong Bayes: chọn một mô hình (selection), kết hợp nhiều mô hình (averaging), và mở rộng mô hình theo hướng bao trùm (expansion). Điểm trọng tâm là không xem model comparison như một thủ tục xếp hạng cơ học, mà như một bài toán ra quyết định dưới bất định mô hình, nơi lựa chọn chiến lược phụ thuộc vào độ tách biệt về predictive performance và mục tiêu ứng dụng.

## 1. So sánh mô hình không phải lúc nào cũng là chọn kẻ thắng

Khi nhiều mô hình cạnh tranh có năng lực dự báo rất sát nhau, việc buộc phải chọn đúng một mô hình dễ tạo cảm giác chắc chắn giả tạo. Ngược lại, khi một mô hình vượt trội rõ rệt và ổn định qua các kiểm tra, việc giữ nhiều mô hình chỉ làm tăng độ phức tạp mà không mang thêm giá trị dự báo. Vì vậy, câu hỏi đúng không phải là "model nào hạng nhất", mà là "chiến lược nào tạo dự báo hữu ích nhất với mức bất định trung thực nhất".

## 2. Strategy A - Model selection

Model selection phù hợp khi khoảng cách dự báo ngoài mẫu giữa mô hình tốt nhất và phần còn lại đủ lớn so với bất định ước lượng. Khi đó, chi phí nhận thức của việc duy trì nhiều mô hình thường cao hơn lợi ích, và một mô hình duy nhất cho phép diễn giải, giao tiếp, và triển khai đơn giản hơn.

Tuy nhiên, điều kiện ngầm của selection là sự tách biệt đủ mạnh. Nếu chênh lệch chỉ số dự báo nhỏ và không ổn định, selection có thể khiến toàn bộ pipeline phụ thuộc vào dao động mẫu ngẫu nhiên thay vì tín hiệu cấu trúc thật.

## 3. Strategy B - Model averaging

Model averaging đi theo nguyên tắc "bảo toàn bất định mô hình" bằng cách kết hợp predictive distributions:

$$
p(\tilde y\mid y)=\sum_{k=1}^{K} w_k\,p_k(\tilde y\mid y),\qquad \sum_k w_k=1,\; w_k\ge 0.
$$

Trong thực hành hiện đại, trọng số stacking thường được ưu tiên vì chúng tối ưu trực tiếp năng lực dự báo của phân phối kết hợp, thay vì cố gán một xác suất "đúng/sai" tuyệt đối cho từng mô hình.

### 3.1. Ví dụ định lượng ngắn

Giả sử ở một điểm dự báo mới, mô hình A cho trung bình 52, mô hình B cho 56, và stacking weights lần lượt là 0.58 và 0.42. Khi đó dự báo trung bình của mô hình kết hợp là

$$
0.58\times 52 + 0.42\times 56 = 53.68.
$$

Giá trị này phản ánh cả tín hiệu của hai mô hình lẫn bất định cấu trúc đang tồn tại giữa chúng, thay vì cưỡng bức chọn 52 hoặc 56 như hai kịch bản loại trừ nhau.

![Selection vs Stacking predictive distributions]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_selection_vs_stacking.png)

## 4. Strategy C - Model expansion

Model expansion phù hợp khi các mô hình ứng viên đại diện cho các mảnh khác nhau của cùng một cơ chế sinh dữ liệu và có thể được hợp nhất vào một mô hình lớn hơn, ví dụ bằng cách thêm thành phần phi tuyến, hiệu ứng nhóm phân cấp, hoặc tương tác có regularization. Lợi điểm của expansion là tạo một khung suy luận nhất quán thay vì duy trì nhiều mô hình rời rạc; rủi ro là tăng độ phức tạp tính toán và đòi hỏi kiểm tra mạnh hơn để tránh overfitting.

Một cách đọc hữu ích là: selection giải quyết cạnh tranh giữa mô hình; averaging giải quyết bất định giữa mô hình; expansion giải quyết thiếu hụt cấu trúc của tập mô hình hiện có.

## 5. Quy tắc lựa chọn chiến lược trong thực hành

Một quy tắc làm việc có thể được phát biểu như sau. Nếu chênh lệch predictive performance đủ lớn và ổn định, ưu tiên selection. Nếu nhiều mô hình gần ngang nhau, ưu tiên averaging để bảo toàn bất định. Nếu tất cả mô hình đều bộc lộ sai lệch cơ chế trong PPC, ưu tiên expansion thay vì tiếp tục tranh luận ai là "ít sai nhất".

Điểm quan trọng là quy tắc này phải luôn đi cùng kiểm tra diagnostic (ví dụ Pareto $$k$$ trong LOO) và kết quả model criticism. Một bảng rank đẹp không thể thay thế bằng chứng rằng mô hình còn bỏ sót cấu trúc dữ liệu quan trọng.

## 6. Ví dụ tổng hợp: cùng dữ liệu, ba quyết định khác nhau

Giả sử ta có ba mô hình M1, M2, M3 và kết quả LOO cho thấy M1 và M2 sát nhau trong sai số chuẩn, còn M3 kém hơn rõ rệt. Khi mục tiêu là dự báo ngắn hạn ổn định, averaging giữa M1 và M2 thường hợp lý hơn selection. Nếu mục tiêu là giải thích cơ chế và M1 đơn giản hơn đáng kể, selection có thể vẫn được chọn với điều kiện báo cáo rõ bất định mô hình còn lại. Ngược lại, nếu PPC chỉ ra cả M1 lẫn M2 đều sai ở tail, quyết định tốt nhất không phải chọn hoặc trộn, mà là expansion để sửa đúng cơ chế sinh dữ liệu.

Qua ví dụ này, ta thấy model comparison là một quyết định đa mục tiêu: dự báo, diễn giải, chi phí triển khai, và trung thực với bất định.

## 7. Kết luận bài 8.3

Không có một chiến lược so sánh mô hình đúng cho mọi bối cảnh. Selection, averaging, và expansion là ba công cụ bổ sung nhau trong cùng một workflow Bayesian. Năng lực của người phân tích không nằm ở việc nhớ tên công cụ, mà ở chỗ biết khi nào nên giảm bất định bằng chọn mô hình, khi nào nên giữ bất định bằng kết hợp mô hình, và khi nào phải tái thiết kế mô hình để sửa sai lệch cơ chế.

Bài tiếp theo: **Bayesian Decision Analysis**, nơi kết quả mô hình được chuyển thành lựa chọn hành động tối ưu dưới loss cụ thể.

## Câu hỏi tự luyện

1. Trong tình huống hai mô hình chênh lệch LOO rất nhỏ so với SE, vì sao selection có thể kém trung thực hơn averaging?
2. Khi nào expansion tốt hơn cả selection lẫn averaging?
3. Nếu mục tiêu chính là diễn giải nhân quả, bạn sẽ thay đổi ưu tiên chiến lược thế nào so với mục tiêu dự báo thuần túy?

## Tài liệu tham khảo

- Yao, Y., et al. (2018). "Using stacking to average Bayesian predictive distributions." *Bayesian Analysis*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition).

---

*Bài học tiếp theo: [8.4 Bayesian Decision Analysis](/vi/chapter08/decision-analysis/)*
