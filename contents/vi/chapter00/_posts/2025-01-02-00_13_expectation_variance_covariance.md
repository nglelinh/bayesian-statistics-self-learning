---
layout: post
title: "Bài 0.15: Kỳ vọng, Phương sai, và Hiệp phương sai"
chapter: '00'
order: 15
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu kỳ vọng như "giá trị trung bình dài hạn", phương sai như "độ phân tán quanh trung bình", hiệp phương sai như "mức độ biến thiên cùng chiều hay ngược chiều" giữa hai biến, và nắm rõ vì sao ba đại lượng này xuất hiện xuyên suốt trong các mô hình Bayesian.

## Giới thiệu: Ba đại lượng mô tả trung tâm và độ bất định

Trong suy luận xác suất, không phải lúc nào ta cũng cần đọc toàn bộ dạng chi tiết của phân phối. Nhiều câu hỏi thực hành bắt đầu từ ba đặc trưng cơ bản: giá trị điển hình nằm ở đâu, mức dao động lớn đến mức nào, và các biến có biến thiên cùng nhau hay không. Kỳ vọng, phương sai và hiệp phương sai trả lời trực tiếp ba câu hỏi đó.

## 1) Kỳ vọng: Giá trị trung bình theo phân phối

Với biến ngẫu nhiên rời rạc:

$$
\mathbb{E}[X] = \sum_x x\,p(x)
$$

Với biến ngẫu nhiên liên tục:

$$
\mathbb{E}[X] = \int x f(x)\,dx
$$

Kỳ vọng không nhất thiết là giá trị xuất hiện nhiều nhất; nó đóng vai trò như "trọng tâm xác suất" của phân phối.

![Kỳ vọng như trọng tâm của phân phối]({{ site.baseurl }}/img/chapter_img/chapter00/expectation_center_histogram.png)

*Hình 1a: Kỳ vọng có thể được nhìn như trọng tâm của phân phối, không nhất thiết trùng với đỉnh cao nhất của histogram.*

## 2) Phương sai: Độ bất định quanh trung bình

Phương sai được định nghĩa là kỳ vọng của bình phương độ lệch so với trung bình:

$$
\mathrm{Var}(X)=\mathbb{E}\big[(X-\mathbb{E}[X])^2\big]
$$

Dạng khai triển thuận tiện khi tính toán:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2
$$

Độ lệch chuẩn là căn bậc hai của phương sai:

$$
\mathrm{SD}(X)=\sqrt{\mathrm{Var}(X)}
$$

Về trực giác, phương sai lớn cho thấy các giá trị phân tán rộng, còn phương sai nhỏ cho thấy phân phối tập trung chặt quanh kỳ vọng.

## 3) Hiệp phương sai: Mức độ cùng biến thiên

Với hai biến ngẫu nhiên $$X$$ và $$Y$$, hiệp phương sai được định nghĩa là:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}\big[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\big]
$$

Khi $$\mathrm{Cov}(X,Y) > 0$$, hai biến có xu hướng cùng tăng hoặc cùng giảm; khi $$\mathrm{Cov}(X,Y) < 0$$, biến này tăng thì biến kia có xu hướng giảm; còn khi hiệp phương sai gần 0, mối liên hệ tuyến tính giữa chúng yếu hoặc không đáng kể.

![Hiệp phương sai dương giữa hai biến]({{ site.baseurl }}/img/chapter_img/chapter00/covariance_positive_scatter.png)

*Hình 1b: Hiệp phương sai dương xuất hiện khi hai biến có xu hướng tăng cùng nhau.*

![Hiệp phương sai âm giữa hai biến]({{ site.baseurl }}/img/chapter_img/chapter00/covariance_negative_scatter.png)

*Hình 1c: Hiệp phương sai âm xuất hiện khi một biến tăng thì biến kia có xu hướng giảm.*

Lưu ý rằng hiệp phương sai phụ thuộc vào đơn vị đo của các biến. Để so sánh không phụ thuộc thang đo, thực hành thường chuẩn hóa thành hệ số tương quan:

$$
\rho_{XY}=\frac{\mathrm{Cov}(X,Y)}{\mathrm{SD}(X)\mathrm{SD}(Y)}
$$

### 3.1) Một ví dụ ngắn trong quyết định hằng ngày

Giả sử hai tuyến xe buýt đều có thời gian di chuyển kỳ vọng là 30 phút:

- Tuyến A thường mất quanh mức $$28, 30, 32$$ phút.
- Tuyến B thường dao động quanh mức $$20, 30, 40$$ phút.

Dù cùng kỳ vọng, tuyến B có phương sai lớn hơn nhiều nên rủi ro đến trễ cao hơn hẳn. Nếu nhận thấy những ngày mưa lớn thời gian di chuyển cũng kéo dài hơn, đó chính là hiệp phương sai dương giữa lượng mưa và thời gian đi lại. Ví dụ này cho thấy chỉ xem trung bình là chưa đủ; quyết định thực tế phụ thuộc cả vào độ phân tán và mối liên hệ giữa các biến.

## 4) Các tính chất cần nhớ

1. $$\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$$
2. $$\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$$
3. $$\mathrm{Var}(X+Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)+2\mathrm{Cov}(X,Y)$$
4. Nếu $$X,Y$$ độc lập thì $$\mathrm{Cov}(X,Y)=0$$

Lưu ý tính chất (4) chỉ đúng theo một chiều: hiệp phương sai bằng 0 chưa đủ kết luận hai biến độc lập.

## 5) Liên hệ với thống kê Bayesian

Trong suy diễn Bayesian, trung bình hậu nghiệm (posterior mean) chính là kỳ vọng theo phân phối hậu nghiệm; độ bất định thường được báo cáo qua độ lệch chuẩn hoặc phương sai hậu nghiệm; còn khi mô hình có nhiều tham số, ma trận hiệp phương sai hậu nghiệm cho biết mức độ phụ thuộc giữa các tham số đó. Vì vậy, nắm chắc kỳ vọng, phương sai và hiệp phương sai là điều kiện cần để diễn giải kết quả Bayesian.

## Tóm tắt nhanh

1. Kỳ vọng là trung bình có trọng số theo phân phối xác suất.
2. Phương sai đo mức độ phân tán quanh kỳ vọng.
3. Hiệp phương sai đo chiều hướng và mức độ cùng biến thiên tuyến tính của hai biến.
4. Ba đại lượng này là ngôn ngữ cơ bản để tóm tắt và diễn giải phân phối hậu nghiệm.

## Video tham khảo

- [Expected Values, Main Ideas!!!](https://www.youtube.com/watch?v=KLs_7b7SKi4) — StatQuest with Josh Starmer, English. **Xem trước.** Giải thích kỳ vọng như giá trị trung bình dài hạn của một biến ngẫu nhiên.
- [Covariance, Clearly Explained!!!](https://www.youtube.com/watch?v=qtaqvPAeEJY) — StatQuest with Josh Starmer, English. Minh họa trực quan hiệp phương sai dương, âm và bằng không.
- [Population and Estimated Parameters, Clearly Explained!!!](https://www.youtube.com/watch?v=vikkiwjQqfU) — StatQuest with Josh Starmer, English. Phân biệt tham số quần thể với đại lượng ước lượng từ mẫu.

## Câu hỏi tự luyện

1. Vì sao kỳ vọng không phải lúc nào cũng trùng với đỉnh cao nhất của phân phối?
2. Nêu một ví dụ thực tế về hai biến có hiệp phương sai âm.
3. Vì sao hiệp phương sai bằng 0 chưa đủ để kết luận hai biến độc lập?

## Tài liệu tham khảo

- Wasserman, L. (2004). *All of Statistics*. Springer.
- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.

---

*Bài học tiếp theo: [0.16 Luật số lớn và Định lý giới hạn trung tâm]({{ site.baseurl }}/contents/vi/chapter00/00_14_law_large_numbers_clt/)*
