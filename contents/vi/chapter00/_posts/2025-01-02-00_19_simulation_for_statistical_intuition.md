---
layout: post
title: "Bài 0.21: Mô phỏng để kiểm tra trực giác thống kê"
chapter: '00'
order: 21
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ xem mô phỏng như một công cụ suy luận chứ không chỉ là minh họa, biết dùng mô phỏng để kiểm tra công thức, phát hiện hiểu sai trực giác, và chuẩn bị tốt cho workflow Bayesian dựa trên generative story.

## Giới thiệu: mô phỏng như phòng thí nghiệm của suy luận

Trong nhiều bài toán xác suất, trực giác bằng lời dễ dẫn đến kết luận sai, còn công thức đóng đôi khi khó kiểm tra nhanh trong bối cảnh thực tế. Mô phỏng cung cấp một "phòng thí nghiệm" trung gian: ta phát biểu giả định, sinh dữ liệu theo giả định đó, rồi đối chiếu hệ quả với điều mình tin là đúng. Cách làm này giúp học sâu hơn vì nó buộc ta nối chặt mô hình lý thuyết với hành vi dữ liệu quan sát được.

![Quy trinh mo phong thong ke]({{ site.baseurl }}/img/chapter_img/chapter00/simulation_statistical_intuition_workflow.png)

*Cách đọc hình: Hình này minh họa quy trinh mo phong thong ke. Hãy đọc nhãn trục/chú thích trước, rồi so sánh xu hướng chính giữa các đường, cột hoặc nhóm điểm thay vì chỉ nhìn từng điểm lẻ.*
*Hinh 1: Quy trinh mo phong 4 buoc: gia dinh mo hinh -> dat tham so -> sinh du lieu -> so sanh va cap nhat.*

## 1) Vì sao cần mô phỏng?

Nhiều bài toán thống kê khó vì trực giác dễ sai:

Ta có thể nhầm xác suất có điều kiện, đánh giá sai mức bất định, hoặc tin vào một kết quả "đẹp" mà không kiểm tra cơ chế sinh dữ liệu đứng sau nó.

Mô phỏng giúp ta nhìn trực tiếp hệ quả của giả định.

## 2) Quy trình mô phỏng 4 bước

1. Viết rõ cơ chế sinh dữ liệu (generative story).
2. Chọn tham số đầu vào hợp lý.
3. Sinh dữ liệu lặp nhiều lần.
4. Tóm tắt kết quả và so với kỳ vọng lý thuyết.

Nếu kết quả mô phỏng mâu thuẫn trực giác, thường trực giác của ta cần sửa.

## 3) Khi nào nên mô phỏng?

Mô phỏng đặc biệt hữu ích khi công thức quá phức tạp hoặc khó kiểm tra tay, khi ta muốn kiểm tra độ nhạy theo tham số, khi cần dạy hay học một khái niệm xác suất bằng trực quan, hoặc khi cần sanity check cho code suy luận Bayesian.

## 4) Ví dụ ngắn

Muốn hiểu khoảng bất định của tỷ lệ $$p$$ khi $$n$$ nhỏ:

Ta có thể giả sử giá trị thật $$p=0.2$$, mô phỏng nhiều mẫu Binomial với $$n=20$$ và $$n=200$$, rồi so sánh độ dao động của $$\hat p$$ giữa hai bối cảnh đó.

Bạn sẽ thấy ngay vì sao dữ liệu nhỏ dễ dao động lớn và vì sao prior có thể quan trọng trong bối cảnh ít dữ liệu.

## 5) Liên hệ trực tiếp với Bayes

Mô phỏng là "phòng thí nghiệm" của Bayesian workflow:

Nó cho phép ta kiểm tra prior predictive, posterior predictive, và cả độ ổn định của quyết định khi các giả định đầu vào thay đổi.

Nói cách khác, mô phỏng giúp ta học tư duy "model implies data".

## Tóm tắt nhanh

1. Mô phỏng là công cụ suy luận, không chỉ là hình minh họa.
2. Quy trình chuẩn: giả định -> sinh dữ liệu -> lặp -> tóm tắt.
3. Mô phỏng đặc biệt hữu ích để sanity check mô hình Bayes.
4. Khi trực giác và mô phỏng mâu thuẫn, hãy tin dữ liệu mô phỏng trước rồi xem lại giả định.

## Câu hỏi tự luyện

1. Hãy nêu một khái niệm xác suất mà bạn thường dễ hiểu sai và đề xuất cách mô phỏng để kiểm tra.
2. Vì sao mô phỏng là cầu nối tốt giữa toán và code?
3. Khi mô phỏng cho kết quả bất ngờ, bạn nên kiểm tra điều gì đầu tiên?

## Tài liệu tham khảo

- Downey, A. (2014). *Think Bayes*.
- McElreath, R. (2020). *Statistical Rethinking*.

---

*Bài học tiếp theo: [Chương 1: Cơ bản về Suy diễn Bayes](/vi/chapter01/)*
