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

Sau bài học này, bạn cần chuyển được kết quả suy luận Bayes thành hành động cụ thể dưới bất định, thông qua loss function, expected loss và value of information. Trọng tâm của bài là hiểu rằng posterior trả lời câu hỏi "ta tin điều gì", còn decision theory trả lời câu hỏi khác hẳn: "ta nên làm gì" khi mỗi lựa chọn mang chi phí không đối xứng.

## 1. Inference không đồng nghĩa với decision

Một posterior rất sắc nét vẫn chưa tự động sinh ra quyết định đúng, bởi quyết định luôn phụ thuộc thêm vào hệ quả của sai lầm. Cùng một mức xác suất hậu nghiệm có thể dẫn đến hai hành động khác nhau nếu cấu trúc thiệt hại thay đổi. Đây là lý do decision analysis là chặng cuối bắt buộc của Bayesian workflow, không phải phần phụ trang trí sau suy luận.

Khung chuẩn gồm bốn thành phần: tập hành động $$a\in\mathcal A$$, trạng thái thế giới $$\theta$$, posterior $$p(\theta\mid y)$$ và loss $$L(a,\theta)$$. Quy tắc Bayes action là chọn

$$
a^*(y)=\arg\min_{a\in\mathcal A} \mathbb E[L(a,\theta)\mid y]
=\arg\min_{a\in\mathcal A}\int L(a,\theta)p(\theta\mid y)\,d\theta.
$$

## 2. Quy tắc ngưỡng từ chi phí bất đối xứng

Xét bài toán cảnh báo rủi ro với hai hành động: cảnh báo ($$a_1$$) và không cảnh báo ($$a_0$$). Gọi $$q=P(H_1\mid y)$$ là xác suất hậu nghiệm có sự cố, $$L_{FP}$$ là chi phí báo động giả, và $$L_{FN}$$ là chi phí bỏ sót sự cố. Khi đó

$$
R(a_1\mid y)=L_{FP}(1-q),\qquad R(a_0\mid y)=L_{FN}q.
$$

Ta chọn cảnh báo nếu $$R(a_1\mid y)<R(a_0\mid y)$$, tương đương

$$
q>\frac{L_{FP}}{L_{FP}+L_{FN}}.
$$

Với $$L_{FP}=5$$ và $$L_{FN}=40$$, ngưỡng quyết định chỉ là $$q^*=5/45\approx 0.111$$. Điều này cho thấy một điểm quan trọng về mặt phương pháp: quyết định tối ưu có thể rất "nhạy" theo chi phí, ngay cả khi posterior không thay đổi.

![Expected loss threshold rule]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_expected_loss_threshold.png)

### 2.1. Ví dụ ý nghĩa nghiệp vụ

Nếu bỏ sót sự cố gây tổn thất lớn hơn nhiều lần so với cảnh báo nhầm, tổ chức hợp lý sẽ cảnh báo sớm hơn, tức dùng ngưỡng posterior thấp hơn. Ngược lại, nếu cảnh báo nhầm rất đắt đỏ, ngưỡng posterior cần cao hơn để tránh hành động quá mức. Quy tắc tối ưu vì vậy không bao giờ là một con số "phổ quát"; nó là hàm của cấu trúc mất mát trong bối cảnh cụ thể.

## 3. Loss function và điểm tóm tắt posterior

Trong bài toán ước lượng điểm, lựa chọn mean, median hay mode không phải sở thích trình bày, mà được quyết định bởi loss:

- squared loss $$L(\hat\theta,\theta)=(\hat\theta-\theta)^2$$ -> tối ưu là posterior mean,
- absolute loss $$L(\hat\theta,\theta)=|\hat\theta-\theta|$$ -> tối ưu là posterior median,
- 0-1 loss (rời rạc) -> tối ưu là posterior mode.

Kết luận phương pháp ở đây là: bất kỳ báo cáo "điểm ước lượng đại diện" nào cũng ngầm chứa một quan điểm về chi phí sai số, dù ta có ý thức điều đó hay không.

## 4. Từ bằng chứng đến hành động: vai trò của Bayes factor

Với hai giả thuyết $$H_0,H_1$$, Bayes factor được định nghĩa:

$$
BF_{10}=\frac{p(D\mid H_1)}{p(D\mid H_0)}.
$$

Nó cập nhật odds thông qua

$$
\frac{P(H_1\mid D)}{P(H_0\mid D)}=BF_{10}\times\frac{P(H_1)}{P(H_0)}.
$$

Tuy nhiên, ngay cả khi $$BF_{10}$$ nghiêng mạnh về $$H_1$$, hành động cuối cùng vẫn phải đi qua expected loss. Bayes factor trả lời câu hỏi "dữ liệu ủng hộ giả thuyết nào"; decision analysis trả lời câu hỏi khác: "trong cấu trúc chi phí hiện tại, hành động nào tối ưu".

## 5. Value of Information: khi nào nên thu thập thêm dữ liệu

Không phải lúc nào thêm dữ liệu cũng đáng. Giá trị thông tin được đo bằng mức giảm expected loss:

$$
\text{VOI}=\mathbb E[L\mid \text{quyết định ngay}] - \mathbb E[L\mid \text{có thêm thông tin}].
$$

Quy tắc hành động rất rõ:

$$
\text{Thu thập thêm dữ liệu nếu } \text{VOI} > \text{chi phí thu thập}.
$$

Ví dụ, nếu expected loss hiện tại là 12 và sau khi bổ sung thông tin có thể giảm xuống 5, ta có VOI = 7. Nếu chi phí lấy thêm thông tin là 4, lợi ích ròng dương và nên thu thập; nếu chi phí là 10, lợi ích ròng âm và nên quyết định ngay với thông tin hiện có.

![Value of information decision curve]({{ site.baseurl }}/img/chapter_img/chapter08/chapter08_voi_decision_curve.png)

## 6. Ví dụ tổng hợp: quyết định A/B testing

Giả sử hai phiên bản sản phẩm A và B có posterior conversion rates $$p_A$$ và $$p_B$$. Phần suy luận cho ta xác suất $$P(p_B>p_A\mid D)$$, nhưng quyết định triển khai không nên dựa trên xác suất này một cách cơ học. Ta cần mô hình hóa utility/loss kinh doanh: giá trị mỗi conversion, chi phí triển khai, rủi ro tổn thất nếu chọn sai, và thời gian cần phản ứng. Khi đó hành động tối ưu là hành động có expected utility cao nhất (hoặc expected loss thấp nhất), không nhất thiết là hành động có posterior probability cao nhất theo một ngưỡng cố định.

Đây là điểm giao quan trọng giữa thống kê và quản trị: cùng một posterior, doanh nghiệp có cấu trúc chi phí khác nhau sẽ có quyết định tối ưu khác nhau.

## 7. Khuôn mẫu workflow cho decision analysis

Một quy trình thực hành chặt chẽ thường đi qua bốn bước: (i) xác định tập hành động có thể thực thi, (ii) định nghĩa loss/utility rõ ràng và có khả năng bảo vệ về nghiệp vụ, (iii) tính expected loss dựa trên posterior/predictive, và (iv) kiểm tra độ nhạy của quyết định khi thay đổi loss assumptions. Bước (iv) đặc biệt quan trọng vì nhiều quyết định có thể đảo chiều khi chi phí được đánh giá lại.

Từ góc nhìn khoa học, một quyết định Bayes tốt không phải quyết định "chắc chắn đúng", mà là quyết định tối ưu theo thông tin hiện có và cấu trúc mất mát đã khai báo minh bạch.

## 8. Kết luận bài 8.4

Bayesian decision analysis hoàn tất chu trình của chapter 08: PPC giúp phát hiện mô hình sai ở đâu, WAIC/LOO giúp so sánh năng lực dự báo, model comparison strategies giúp xử lý bất định mô hình, và decision theory biến toàn bộ thông tin đó thành hành động cụ thể. Nếu inference là khoa học của niềm tin dưới bất định, thì decision analysis là kỷ luật biến niềm tin đó thành lựa chọn có trách nhiệm.

**Chapter 08 Complete**: model criticism -> model comparison -> decision.

## Câu hỏi tự luyện

1. Vì sao hai tổ chức có cùng posterior về rủi ro có thể đưa ra hai hành động tối ưu khác nhau?
2. Nếu chi phí báo động giả tăng gấp đôi, ngưỡng $$q^*$$ thay đổi theo hướng nào?
3. Khi VOI dương nhưng rất gần chi phí thu thập, bạn cần kiểm tra gì trước khi quyết định thu thêm dữ liệu?

## Tài liệu tham khảo

- Berger, J. O. (1985). *Statistical Decision Theory and Bayesian Analysis*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd Edition), Chapter 9.

---

*Chương tiếp theo: [Chapter 12: Labs Thực Hành Bayesian](/vi/chapter12/)*
