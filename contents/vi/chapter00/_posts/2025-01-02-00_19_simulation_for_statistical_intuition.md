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

Sau bài này, bạn sẽ sử dụng mô phỏng như một công cụ suy luận thực thụ chứ không chỉ để minh họa, biết dùng mô phỏng để kiểm chứng công thức, phát hiện các điểm mù trực giác, và chuẩn bị nền tảng cho quy trình làm việc Bayesian dựa trên cơ chế sinh dữ liệu (generative story).

## Giới thiệu: Mô phỏng như phòng thí nghiệm của suy luận

Trong nhiều bài toán xác suất, suy đoán bằng lời dễ dẫn tới kết luận sai, còn công thức giải tích đôi khi khó hình dung trong bối cảnh thực tế. Mô phỏng đóng vai trò như một "phòng thí nghiệm" trung gian: ta phát biểu rõ giả định, sinh dữ liệu theo giả định đó, rồi đối chiếu hệ quả với điều mình kỳ vọng. Cách làm này giúp gắn chặt mô hình lý thuyết với hành vi thực tế của dữ liệu.

![Quy trình mô phỏng thống kê]({{ site.baseurl }}/img/chapter_img/chapter00/simulation_statistical_intuition_workflow.png)

*Hình 1: Quy trình mô phỏng 4 bước: xác định giả định mô hình -> chọn tham số -> sinh dữ liệu lặp lại -> so sánh với kỳ vọng và cập nhật.*

## 1) Vì sao cần mô phỏng?

Nhiều bài toán thống kê dễ gây nhầm lẫn về trực giác: ta có thể hiểu sai xác suất có điều kiện, đánh giá thấp mức độ bất định, hoặc tin vào một kết quả bề ngoài hợp lý mà chưa kiểm tra cơ chế sinh dữ liệu phía sau. Mô phỏng cho phép quan sát trực tiếp hệ quả của từng giả định.

## 2) Quy trình mô phỏng 4 bước

1. Phát biểu rõ cơ chế sinh dữ liệu (generative story).
2. Chọn bộ tham số đầu vào hợp lý.
3. Sinh dữ liệu lặp lại nhiều lần.
4. Tóm tắt kết quả mô phỏng và đối chiếu với kỳ vọng lý thuyết.

Khi kết quả mô phỏng mâu thuẫn với dự đoán ban đầu (và mã mô phỏng không có lỗi), thường chính trực giác của ta cần được hiệu chỉnh.

## 3) Khi nào nên mô phỏng?

Mô phỏng đặc biệt hữu ích khi công thức quá phức tạp để kiểm tra bằng tay, khi cần đánh giá độ nhạy của kết quả theo tham số, khi muốn trực quan hóa một khái niệm xác suất, hoặc khi cần kiểm tra nhanh (sanity check) cho mã nguồn suy luận Bayesian.

## 4) Ví dụ ngắn

Để thấy trực tiếp độ bất định của tỷ lệ mẫu $$\hat p$$ khi cỡ mẫu nhỏ, ta có thể cố định giá trị thật $$p=0.2$$, mô phỏng nhiều mẫu Binomial với $$n=20$$ và $$n=200$$, rồi so sánh mức dao động của $$\hat p$$ giữa hai trường hợp. Kết quả sẽ cho thấy ngay vì sao cỡ mẫu nhỏ dao động mạnh và vì sao thông tin tiên nghiệm (prior) đóng vai trò lớn hơn khi dữ liệu còn ít.

### 4.1) Quan sát 5 lần mô phỏng cụ thể

Với cùng giá trị thật $$p=0.2$$, năm lần mô phỏng điển hình có thể cho:

- Khi $$n=20$$: $$\hat p = 0.10, 0.15, 0.20, 0.30, 0.35$$.
- Khi $$n=200$$: $$\hat p = 0.17, 0.19, 0.20, 0.22, 0.24$$.

Cả hai dãy đều xoay quanh 0.2, nhưng nhóm $$n=20$$ phân tán rộng hơn nhiều. Chỉ vài lần mô phỏng cũng đủ tạo trực giác rõ ràng về ảnh hưởng của cỡ mẫu đến độ ổn định của ước lượng.

## 5) Liên hệ trực tiếp với thống kê Bayesian

Mô phỏng là "phòng thí nghiệm" cốt lõi của quy trình làm việc Bayesian (Bayesian workflow): nó cho phép thực hiện kiểm tra dự báo tiên nghiệm (prior predictive check), kiểm tra dự báo hậu nghiệm (posterior predictive check) và đánh giá độ ổn định của quyết định khi thay đổi giả định đầu vào. Nói gọn lại, mô phỏng rèn luyện tư duy "mô hình quy định dạng dữ liệu sinh ra" (model implies data).

## Tóm tắt nhanh

1. Mô phỏng là công cụ kiểm chứng suy luận, không chỉ là hình minh họa.
2. Quy trình chuẩn gồm bốn bước: đặt giả định -> chọn tham số -> sinh dữ liệu lặp -> tóm tắt và đối chiếu.
3. Mô phỏng rất hữu ích để kiểm tra nhanh (sanity check) các mô hình Bayesian.
4. Khi trực giác mâu thuẫn với mô phỏng, hãy kiểm tra lại mã nguồn rồi xem lại chính giả định và trực giác ban đầu.

## Video tham khảo

- [What is Monte Carlo Simulation?](https://www.youtube.com/watch?v=7TqhmX92P6U) — IBM Technology, English. **Xem trước.** Giải thích mô phỏng Monte Carlo như cách đặt giả định và sinh dữ liệu lặp lại để quan sát phân phối kết quả.
- [Law of Large Numbers - Explained and Visualized](https://www.youtube.com/watch?v=MntX3zWNWec) — Jeremy Blitz-Jones, English. Minh họa việc dùng mô phỏng để kiểm chứng trực quan một định lý xác suất.
- [But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) — 3Blue1Brown, English. Cho thấy quy trình sinh nhiều mẫu lặp lại để quan sát phân phối của trung bình mẫu.

## Câu hỏi tự luyện

1. Nêu một khái niệm xác suất mà bạn hay nhầm lẫn và thiết kế một thí nghiệm mô phỏng nhỏ để tự kiểm chứng.
2. Vì sao mô phỏng là cầu nối hiệu quả giữa công thức toán học và mã lập trình?
3. Khi kết quả mô phỏng khác xa kỳ vọng ban đầu, bạn nên kiểm tra những yếu tố nào trước tiên?

## Tài liệu tham khảo

- Downey, A. (2014). *Think Bayes*.
- McElreath, R. (2020). *Statistical Rethinking*.

---

*Bài học tiếp theo: [Chương 1: Cơ bản về Suy diễn Bayes]({{ site.baseurl }}/contents/vi/chapter01/)*
