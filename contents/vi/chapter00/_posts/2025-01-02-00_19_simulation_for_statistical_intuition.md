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

Năm 1946, khi nằm dưỡng bệnh và chơi trò xếp bài Solitaire, nhà toán học Stanislaw Ulam nảy ra một ý tưởng làm thay đổi toàn bộ khoa học tính toán: thay vì cố giải bài toán tổ hợp cực khó bằng công thức đóng, tại sao không chơi thử hàng trăm ván trên máy tính rồi đếm tỷ lệ thắng? Cùng với John von Neumann, ông gọi kỹ thuật đó là **phương pháp Monte Carlo** — đặt theo sòng bạc nổi tiếng ở Monaco.

Đối với người học thống kê Bayes, mô phỏng không chỉ là công cụ kiểm chứng bài tập mà là **phòng thí nghiệm tư duy**: bất cứ khi nào một công thức trông mờ ảo hoặc một mô hình phức tạp khó đoán hành vi, bạn luôn có thể sinh dữ liệu giả lập với tham số đã biết để nhìn tận mắt điều gì xảy ra.

---

## Mục tiêu học tập

Sau bài này, bạn sẽ sử dụng mô phỏng như một công cụ suy luận thực thụ chứ không chỉ để minh họa, biết dùng mô phỏng để kiểm chứng công thức, phát hiện các điểm mù trực giác, và chuẩn bị nền tảng cho quy trình làm việc Bayesian dựa trên cơ chế sinh dữ liệu (generative story).


## Bản đồ kiến thức nền: Mô hình sinh dữ liệu, Monte Carlo và Kiểm chứng quy trình Bayes

Mô phỏng kết nối ba trụ cột quan trọng của khoa học dữ liệu định lượng:

- **Mô hình sinh dữ liệu (Generative Modeling):** Muốn mô phỏng, bạn buộc phải viết rõ ràng từng bước dữ liệu được tạo ra như thế nào (từ tham số đến quan sát). Nếu viết được hàm sinh dữ liệu, bạn đã hiểu trọn vẹn cấu trúc xác suất của bài toán.
- **Tích phân Monte Carlo (Monte Carlo Integration):** Mọi xác suất $$P(A)$$ hay kỳ vọng $$\mathbb{E}[g(X)]$$ đều có thể xấp xỉ bằng tần suất thực nghiệm trên $$M$$ lần mô phỏng độc lập, với sai số giảm theo $$1/\sqrt{M}$$.
- **Cầu nối sang Thống kê Bayes (Prior & Posterior Predictive Checks):** Toàn bộ quy trình Bayes hiện đại xoay quanh mô phỏng: *Prior predictive simulation* kiểm tra xem prior có sinh ra dữ liệu hợp lý không, *Simulation-Based Calibration (SBC)* kiểm tra thuật toán suy diễn có khôi phục được tham số thật không, và *Posterior predictive simulation* kiểm tra mô hình sau khi khớp có tái tạo được dữ liệu thực tế không.

---

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


## Khung giải thích (nên đọc chậm): Bốn bước kiểm chứng trực giác bằng mô phỏng

Khi gặp một câu hỏi xác suất khó hoặc nghi ngờ một bộ ước lượng, hãy dùng quy trình mô phỏng 4 bước:

1. **Cố định "chân lý ẩn" (Ground truth):** Tự chọn giá trị tham số thật biết trước (ví dụ $$\theta_{\text{true}} = 0.30$$) để có mốc đối chiếu tuyệt đối.
2. **Sinh $$M$$ tập dữ liệu giả lập:** Dùng bộ sinh số ngẫu nhiên (cố định `seed` để tái lập) tạo ra $$M$$ kịch bản độc lập theo đúng giả định mô hình.
3. **Áp dụng đúng quy trình suy diễn lên từng kịch bản:** Tính thống kê quan tâm (trung bình mẫu, khoảng tin cậy, xác suất sự kiện).
4. **Đo sai số Monte Carlo:** Kiểm tra $$\mathrm{MCSE} = \sqrt{\hat p(1-\hat p)/M}$$ để chắc chắn số lần mô phỏng $$M$$ đủ lớn nhằm kết luận đáng tin cậy.

### Ví dụ tính toán cầm tay chỉ việc: Đo độ chính xác ước lượng xác suất bằng Monte Carlo

Giả sử bạn mô phỏng bài toán kiểm tra xem tổng của 2 viên xúc xắc công bằng có lớn hơn hoặc bằng 10 hay không (giá trị lý thuyết chính xác là $$p = 6/36 = 1/6 \approx 0.1667$$). Hãy theo dõi sai số chuẩn Monte Carlo $$\mathrm{MCSE} = \sqrt{p(1-p)/M}$$ khi tăng số lần chạy $$M$$:

| Số lần mô phỏng $$M$$ | $$\mathrm{MCSE} = \sqrt{0.1667 \times 0.8333 / M}$$ | Biên sai số 95% ($$\pm 1.96\,\mathrm{MCSE}$$) | Mức độ tin cậy |
| --- | --- | --- | --- |
| $$M = 100$$ | $$\sqrt{0.1389 / 100} \approx 0.0373$$ | $$\pm 0.0731$$ | Rất thô (dao động từ 9% đến 24%) |
| $$M = 1\,000$$ | $$\sqrt{0.1389 / 1000} \approx 0.0118$$ | $$\pm 0.0231$$ | Khá ổn để xem trực giác |
| $$M = 10\,000$$ | $$\sqrt{0.1389 / 10000} \approx 0.0037$$ | $$\pm 0.0073$$ | Chính xác tới dưới 1 điểm phần trăm |

**Hiểu lầm cần tránh:** Chạy mô phỏng chỉ $$M = 50$$ lần rồi kết luận thuật toán bị sai chỉ vì kết quả lệch vài phần trăm so với lý thuyết. Luôn tính nhanh $$\mathrm{MCSE}$$ trước khi phán xét.

**Kiểm tra nhanh:** Nếu bạn muốn ước lượng một xác suất quanh $$0.5$$ với sai số chuẩn Monte Carlo nhỏ hơn $$0.005$$, ta cần $$\sqrt{0.25/M} \le 0.005 \implies M \ge 0.25 / 0.000025 = 10\,000$$ lần mô phỏng.

---

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
