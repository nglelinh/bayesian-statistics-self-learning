---
layout: post
title: "Bài 3.6: PyMC - Bayesian Modeling trong Thực tế"
chapter: '03'
order: 6
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu PyMC như một công cụ thực hành cho toàn bộ những gì đã học trong chương: prior, likelihood, posterior, sampler và diagnostics. Bạn không cần xem PyMC như black box, mà như một lớp trừu tượng giúp ta mô tả mô hình rõ ràng hơn và dùng các sampler hiện đại như NUTS một cách an toàn hơn.

> **Ví dụ mini.** Thay vì tự viết lại Metropolis-Hastings hay HMC cho mỗi mô hình mới, bạn chỉ cần mô tả prior, likelihood và dữ liệu trong PyMC. Thư viện sẽ giúp bạn lấy mẫu posterior và cung cấp diagnostics cần thiết.
>
> **Câu hỏi tự kiểm tra.** Nếu dùng PyMC rồi, vì sao ta vẫn cần hiểu sampling, HMC và diagnostics về mặt khái niệm?

## 1. Tại sao từ chương này trở đi ta cần công cụ?

Nếu bài toán chỉ có một vài tham số đơn giản, ta còn có thể:

- tính tay,
- grid approximation,
- hoặc tự viết sampler cơ bản.

Nhưng khi mô hình thực tế bắt đầu có:

- nhiều tham số,
- nhiều tầng,
- dữ liệu thật,
- cấu trúc không còn conjugate,

thì việc tự triển khai mọi thứ từ đầu trở nên:

- dễ lỗi,
- khó mở rộng,
- tốn thời gian,
- và khó chẩn đoán.

Đó là lúc PyMC trở nên rất giá trị.

## 2. PyMC thật ra làm gì?

PyMC cho phép bạn:

1. mô tả mô hình bằng ngôn ngữ gần với toán học,
2. để thư viện chọn và chạy sampler phù hợp,
3. dùng ArviZ để đọc posterior và diagnostics.

Nói ngắn gọn:

- bạn tập trung vào **mô hình**,
- PyMC lo nhiều phần của **máy lấy mẫu**.

Điều này cực hợp với tinh thần Bayesian workflow:

- suy nghĩ về generative story trước,
- code hóa nó rõ ràng,
- rồi kiểm tra chất lượng suy luận sau.

![MCMC workflow trong thực hành]({{ site.baseurl }}/img/chapter_img/chapter03/mcmc_workflow.png)

## 3. PyMC không phải black box nếu bạn hiểu chương này

Một người chưa học Chapter 3 có thể xem PyMC như:

- “viết vài dòng rồi posterior tự hiện ra”.

Nhưng sau khi học chương này, bạn biết đằng sau các dòng code đó là:

- prior,
- likelihood,
- posterior,
- sampler,
- warm-up,
- diagnostics,
- ESS,
- R-hat,
- và posterior predictive.

Nói cách khác, PyMC không thay thế tư duy Bayesian. Nó chỉ giúp bạn triển khai tư duy đó hiệu quả hơn.

## 4. Cách nghĩ đúng khi viết model trong PyMC

Khi mở PyMC, đừng nghĩ:

- “mình phải gọi API nào?”

Hãy nghĩ:

- tham số chưa biết là gì,
- prior hợp lý là gì,
- dữ liệu được sinh ra như thế nào,
- và mình muốn trả lời câu hỏi posterior nào.

Ví dụ, với bài toán đồng xu:

- tham số là xác suất ngửa $$\theta$$,
- prior có thể là Beta,
- likelihood là Binomial,
- dữ liệu là số lần ngửa quan sát được.

Khi suy nghĩ theo trình tự này, code PyMC sẽ trở thành bản dịch của mô hình, không phải mẹo lập trình.

## 5. Một mô hình Bayes trong PyMC thường có ba lớp

### 5.1. Khai báo prior

Đây là nơi bạn viết ra điều tin trước dữ liệu.

### 5.2. Khai báo likelihood

Đây là nơi bạn kể câu chuyện sinh dữ liệu.

### 5.3. Gọi sampler

Đây là nơi PyMC dùng NUTS hoặc sampler phù hợp để lấy mẫu posterior.

Nếu học kỹ Chapter 2 và Chapter 3, bạn sẽ thấy ba bước này rất quen.

## 6. NUTS là lý do lớn khiến PyMC mạnh

Trong nhiều mô hình liên tục, PyMC mặc định dùng NUTS:

- một phiên bản tự động hóa rất mạnh của HMC.

Điều này giúp bạn:

- không phải tự chỉnh số bước leapfrog,
- có warm-up/tuning hợp lý hơn,
- thường thu được chain tốt hơn so với tự viết MH ngây thơ.

Tuy nhiên, đừng vì vậy mà bỏ qua diagnostics. Dùng NUTS không đồng nghĩa với:

- “mọi thứ tự động đúng”.

## 7. Workflow tối thiểu khi dùng PyMC

Một workflow lành mạnh thường là:

1. xác định bài toán và generative story,
2. chọn prior có lý do,
3. viết model trong PyMC,
4. lấy mẫu posterior,
5. kiểm tra diagnostics,
6. xem posterior summary,
7. làm posterior predictive nếu cần,
8. quay lại chỉnh mô hình nếu có vấn đề.

Đây là điều quan trọng:

- chạy được model chưa phải là kết thúc,
- đọc được model mới là năng lực thực sự.

## 8. Những sai lầm phổ biến khi mới dùng PyMC

### 8.1. Chạy được là tin ngay

Sai. Bạn vẫn phải xem:

- trace plot,
- R-hat,
- ESS,
- warning của sampler.

### 8.2. Chọn prior qua loa

Sai. Prior không phải dòng code trang trí.

### 8.3. Không chuẩn hóa hoặc tham số hóa kém

Nhiều mô hình chạy khó không phải vì PyMC yếu, mà vì:

- dữ liệu scale quá lệch,
- mô hình tham số hóa chưa tốt,
- posterior có hình dạng xấu.

### 8.4. Quên posterior predictive

Có posterior chưa đủ. Bạn vẫn cần hỏi:

- mô hình này dự đoán dữ liệu mới ra sao,
- có hợp với dữ liệu quan sát không.

## 9. PyMC đặc biệt hữu ích cho loại bài toán nào?

PyMC rất hợp khi bạn làm:

- hồi quy Bayes,
- logistic regression,
- hierarchical models,
- mixture models,
- time series có uncertainty,
- và các mô hình mà code tay sampler là không thực tế.

Trong khóa học này, PyMC sẽ là cánh tay thực hành cho phần lý thuyết.

## 10. Một tư duy rất quan trọng khi làm việc với PyMC

Đừng hỏi:

- “PyMC cho ra kết quả gì?”

Hãy hỏi:

- “Mô hình mình đã viết đang giả định điều gì?”
- “Sampler có thực sự khám phá tốt posterior chưa?”
- “Posterior này có trả lời đúng câu hỏi mình quan tâm không?”
- “Mô hình dự đoán dữ liệu có ổn không?”

Nếu bạn giữ được bốn câu hỏi đó, PyMC sẽ là công cụ cực mạnh. Nếu không, nó dễ biến thành black box.

## 11. Chapter 3 khép lại ở đâu?

Sau chương này, bạn đã đi qua một đường rất quan trọng:

- từ tích phân khó,
- tới Monte Carlo,
- tới chuỗi Markov,
- tới MH,
- tới HMC/NUTS,
- rồi tới diagnostics và công cụ thực hành.

Đó chính là nền móng để bước sang các mô hình Bayes thực thụ ở các chương sau.

> **3 ý cần nhớ.**
> 1. PyMC giúp ta triển khai mô hình Bayes thực tế bằng cách mô tả prior, likelihood và dữ liệu một cách gần với ngôn ngữ toán học.
> 2. Dùng PyMC không miễn cho ta trách nhiệm hiểu sampler, diagnostics và posterior predictive.
> 3. Giá trị thật của PyMC không nằm ở việc “chạy được model”, mà ở chỗ nó giúp ta thực hiện Bayesian workflow đầy đủ và minh bạch.

## Câu hỏi tự luyện

1. Vì sao PyMC nên được xem là công cụ triển khai mô hình chứ không phải máy “bấm nút ra posterior”?
2. NUTS trong PyMC liên hệ thế nào với HMC mà bạn đã học?
3. Sau khi chạy xong một model PyMC, ba kiểm tra đầu tiên bạn nên làm là gì?
4. Trong một bài toán thực tế của bạn, model nào sẽ là ứng viên tốt để triển khai bằng PyMC?

## Tài liệu tham khảo

- PyMC Documentation.
- ArviZ Documentation.
- McElreath, R. *Statistical Rethinking* (2nd ed.), later chapters for applied modeling.

---

*Kết thúc Chapter 3. Bài học tiếp theo: [Chapter 4 - Bayesian Regression](/vi/chapter04/)*
