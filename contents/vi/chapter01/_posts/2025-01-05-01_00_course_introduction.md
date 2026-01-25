---
layout: post
title: "Giới thiệu Khóa học: Phân tích Dữ liệu Bayes"
chapter: '01'
order: 0
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

## Chào mừng đến với Bayesian Statistics!

Chào mừng bạn đến với khóa học **Phân tích Dữ liệu Bayes (Bayesian Data Analysis – 2101595)**. Đây là một hành trình khám phá cách tiếp cận hiện đại và mạnh mẽ nhất trong thống kê và khoa học dữ liệu – **Bayesian Statistics**.

Khác với thống kê truyền thống (frequentist statistics) mà bạn có thể đã học, phương pháp Bayes không chỉ là một tập hợp các công thức tính toán, mà là một **triết lý hoàn chỉnh** về cách chúng ta học hỏi từ dữ liệu, cập nhật niềm tin, và đưa ra quyết định dưới sự không chắc chắn.

---

## 🎯 Mục tiêu Khóa học

Sau khi hoàn thành khóa học này, bạn sẽ có khả năng:

### 1. **Tư duy Bayesian**
- Hiểu sâu sắc triết lý Bayesian về xác suất như "mức độ tin tưởng" (plausibility)
- Phê phán những hạn chế của p-values và hypothesis testing truyền thống
- Áp dụng Bayesian reasoning vào các vấn đề thực tế

### 2. **Xây dựng Mô hình**
- Xây dựng probabilistic models như **data-generating processes**
- Hiểu vai trò của likelihood, prior, và posterior trong suy diễn Bayesian
- Chọn priors phù hợp và kiểm tra tính nhạy cảm (sensitivity)

### 3. **Tính toán Bayesian**
- Thành thạo MCMC (Markov Chain Monte Carlo) sampling
- Sử dụng PyMC để implement Bayesian models
- Chẩn đoán và đánh giá convergence của MCMC chains

### 4. **Mô hình Nâng cao**
- Áp dụng Bayesian linear regression và GLM (Generalized Linear Models)
- Xây dựng hierarchical/multilevel models
- Sử dụng Gaussian Processes và mixture models cho các vấn đề phức tạp

### 5. **Model Checking & Decision Making**
- Kiểm tra mô hình với posterior predictive checks
- So sánh models với information criteria (WAIC, LOO)
- Áp dụng Bayesian decision analysis cho ra quyết định tối ưu

### 6. **Thực hành Chuyên nghiệp**
- Báo cáo kết quả Bayesian một cách rõ ràng và chính xác
- Thực hiện complete Bayesian workflow từ đầu đến cuối
- Áp dụng vào các bài toán thực tế trong nghiên cứu và công nghiệp

---

## 📖 Tài liệu Tham khảo

Khóa học này kết hợp **dual references framework** - lấy điểm mạnh từ nhiều nguồn:

### Primary Reference (Implementation):

**Richard McElreath (2020)** - *Statistical Rethinking* (2nd Edition)
- Triết lý modeling rõ ràng, dễ hiểu
- Intuitive explanations
- Video lectures miễn phí: [YouTube Playlist](https://www.youtube.com/playlist?list=PLDcUM9US4XdM9_N6XUUFrhghGJ4K25bFc)

### Secondary References (Theory):

**Andrew Gelman et al. (2013)** - *Bayesian Data Analysis* (3rd Edition)
- Nền tảng toán học vững chắc
- Comprehensive coverage
- Official syllabus reference

**John K. Kruschke (2014)** - *Doing Bayesian Data Analysis*
- Pedagogical approach xuất sắc
- Visual explanations
- Beginner-friendly

### Additional Resources:

- **Gelman & Hill (2006)**: *Data Analysis Using Regression and Multilevel/Hierarchical Models*
- **Rasmussen & Williams (2006)**: *Gaussian Processes for Machine Learning*
- **PyMC Documentation**: https://www.pymc.io/
- **ArviZ Documentation**: https://python.arviz.org/

---

## 🚀 Tại sao Học Bayesian Statistics?

Nếu bạn đã quen với thống kê tần suất - với p-values, confidence intervals, và hypothesis testing - bạn có thể tự hỏi: tại sao phải học một cách tiếp cận hoàn toàn khác? Có năm lý do chính.

### 1. Trực Quan và Tự Nhiên

Bayesian phản ánh cách chúng ta tự nhiên suy nghĩ. Khi bạn học được thông tin mới, bạn cập nhật niềm tin của mình - bạn không "bác bỏ" hay "không bác bỏ" một giả thuyết dựa trên một con số như 0.05. 

Ví dụ: Bạn nghĩ một đồng xu cân bằng. Tung 10 lần được 8 mặt ngửa. Bạn sẽ nghĩ "có lẽ đồng xu hơi lệch", không phải "bác bỏ giả thuyết đồng xu cân bằng ở mức ý nghĩa 5%". Bayesian làm chính xác điều đó - cập nhật niềm tin dựa trên dữ liệu.

Hơn nữa, khi nói "95% credible interval là [0.6, 0.8]", điều này có nghĩa đơn giản là: có 95% khả năng tham số nằm trong khoảng đó. Rất dễ hiểu, không cần diễn giải phức tạp.

### 2. Linh Hoạt

Bayesian cho phép bạn xây dựng model phức tạp phù hợp với thực tế:

- **Tích hợp kiến thức sẵn có**: Nếu bạn biết trước một tham số phải dương, bạn có thể nói điều đó trực tiếp trong model
- **Xử lý missing data**: Không cần kỹ thuật phức tạp - model tự học các giá trị thiếu
- **Hierarchical models**: Khi dữ liệu có cấu trúc nhóm (học sinh trong lớp, bệnh nhân trong bệnh viện), Bayesian xử lý rất tốt

### 3. Trung Thực về Sự Không Chắc Chắn

Thay vì cho một con số ("trung bình là 5.2"), Bayesian cho bạn cả một phân phối xác suất về tham số. Điều này cho phép trả lời:

- "Xác suất hiệu ứng lớn hơn 0.5 là bao nhiêu?" → 78%
- "Khoảng nào chứa 95% khả năng?" → [0.4, 0.7]
- "Nếu quyết định dựa trên con số này, rủi ro sai là bao nhiêu?" → Tính được

Không chắc chắn được lan truyền tự nhiên qua model. Nếu không chắc về A, và A ảnh hưởng đến B, thì không chắc chắn về B cũng tự động được tính.

### 4. Được Dùng Rộng Rãi trong Thực Tế

Bayesian không chỉ là lý thuyết - nó được dùng thật:

- **Google, Netflix**: Tối ưu hóa search, gợi ý phim
- **Ngân hàng, tài chính**: Đo rủi ro, quản lý danh mục đầu tư
- **Y tế**: Thử nghiệm lâm sàng (FDA chấp nhận), y học cá nhân hóa
- **AI/Machine Learning**: Neural networks với uncertainty, tự động tune parameters

Nếu bạn làm data science, machine learning, hay nghiên cứu, biết Bayesian là một lợi thế lớn.

### 5. Đang Trở Thành Chuẩn Mực

Trong nhiều lĩnh vực, Bayesian đang thay thế p-values:

- Các tạp chí khoa học khuyến khích dùng Bayesian thay vì chỉ p-values
- American Statistical Association cảnh báo về lạm dụng p-values, đề xuất Bayesian
- Causal inference (trả lời "X gây ra Y?") dùng Bayesian là chuẩn
- Nhiều công ty tech yêu cầu Bayesian trong job requirements

**Tóm lại**: Học Bayesian không phải học thêm một công cụ - nó là học một cách tư duy mới về dữ liệu và sự không chắc chắn, một cách tư duy đang ngày càng trở thành thiết yếu.

---

## 🚀 Bắt đầu Ngay!

**Bài học tiếp theo**: [1.1 Replication Crisis & P-values](/vi/chapter01/replication-crisis-pvalues/)

Hoặc nếu bạn cần ôn lại kiến thức nền tảng:  
**Prerequisites**: [Chapter 00: Prerequisites](/vi/chapter00/)

---

**Chúc bạn học tốt và enjoy the journey! 🎉**

*"In God we trust, all others must bring data."* - W. Edwards Deming  
*"But with Bayesian statistics, we update our trust based on the data!"* - Modern statistician

