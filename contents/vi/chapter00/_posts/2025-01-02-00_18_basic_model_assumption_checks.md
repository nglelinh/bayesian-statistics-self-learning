---
layout: post
title: "Bài 0.18: Kiểm tra giả định mô hình cơ bản"
chapter: '00'
order: 18
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ biết cách kiểm tra nhanh những giả định cốt lõi của mô hình (dạng phân phối, tính độc lập, cấu trúc sai số), nhận diện dấu hiệu sai mô hình (misspecification), và hiểu vì sao kiểm tra giả định là một phần của suy luận chứ không phải bước trang trí.

![Kiem tra gia dinh mo hinh co ban]({{ site.baseurl }}/img/chapter_img/chapter00/basic_model_assumption_checks.png)
*Hinh 1: Minh hoa fit va residual de nhin nhanh outlier, xu huong phan du, va dau hieu misspecification.*

## 1) Giả định mô hình là gì?

Mỗi mô hình thống kê ngầm nói rằng:

- dữ liệu sinh từ một cơ chế cụ thể,
- nhiễu có cấu trúc nào đó,
- quan hệ giữa biến đầu vào và đầu ra có dạng nhất định.

Nếu giả định sai nghiêm trọng, suy luận có thể lệch dù code chạy hoàn hảo.

## 2) Các kiểm tra cơ bản nên làm

1. **Kiểm tra phân phối**: histogram, density, QQ-style trực giác.
2. **Kiểm tra phần dư**: residual có cấu trúc hay không?
3. **Kiểm tra outlier/influence**: vài điểm có chi phối kết quả không?
4. **Kiểm tra phụ thuộc**: dữ liệu theo thời gian/nhóm có vi phạm độc lập không?

## 3) Ví dụ trực giác

Nếu dữ liệu đếm có nhiều số 0 nhưng ta dùng Gaussian model, mô hình có thể dự báo giá trị âm hoặc sai uncertainty. Đây là dấu hiệu nên đổi likelihood (ví dụ Poisson/Negative Binomial).

## 4) Sai mô hình không phải thất bại, mà là tín hiệu cập nhật

Trong tư duy Bayesian workflow:

1. Đề xuất mô hình,
2. Fit mô hình,
3. Kiểm tra hệ quả dự báo và giả định,
4. Cải tiến mô hình.

Mục tiêu không phải "chứng minh mô hình đúng", mà là làm mô hình phù hợp hơn với dữ liệu và câu hỏi thực tế.

## 5) Liên hệ với các chương sau

Các kỹ thuật kiểm tra sâu hơn như posterior predictive checks, WAIC, LOO sẽ xuất hiện ở chương sau. Bài này giúp bạn có nền trực giác để hiểu chúng không chỉ là chỉ số, mà là công cụ phát hiện sai lệch mô hình.

## Tóm tắt nhanh

1. Mô hình luôn đi kèm giả định.
2. Giả định sai có thể làm kết luận sai.
3. Kiểm tra giả định là bước trung tâm của workflow.
4. Misspecification là thông tin để cải thiện mô hình.

## Câu hỏi tự luyện

1. Nêu một tình huống vi phạm giả định độc lập trong dữ liệu thực.
2. Vì sao kiểm tra residual giúp phát hiện thiếu biến hoặc sai dạng hàm?
3. Nếu có outlier mạnh, bạn sẽ làm gì trước khi kết luận?

## Tài liệu tham khảo

- Gelman, A., et al. (2013). *Bayesian Data Analysis*.
- McElreath, R. (2020). *Statistical Rethinking*.

---

*Bài học tiếp theo: [Bài 0.19: Mô phỏng để kiểm tra trực giác thống kê](/vi/chapter00/simulation-for-statistical-intuition/)*
