---
layout: post
title: "Bài 1.4: Bayesian vs Frequentist - So Sánh và Lựa Chọn"
chapter: '01'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu rõ sự khác biệt triết học và thực hành giữa hai trường phái thống kê chính: **Frequentist** và **Bayesian**. Bạn sẽ nhận ra rằng sự khác biệt không chỉ là về kỹ thuật tính toán, mà là về cách chúng ta **định nghĩa xác suất, diễn giải kết quả, và trả lời các câu hỏi khoa học**. Quan trọng hơn, bạn sẽ phát triển khả năng đánh giá khi nào nên dùng phương pháp nào, và hiểu tại sao Bayesian thường cung cấp câu trả lời trực tiếp và tự nhiên hơn cho các vấn đề thực tế.

## Giới thiệu: Hai Cách Nhìn về Thống Kê

Hãy tưởng tượng bạn tung một đồng xu 10 lần và được 7 lần ngửa. Bạn muốn biết: đồng xu này có thiên lệch hay không? Và nếu có, xác suất ra ngửa thực sự là bao nhiêu?

Hai nhà thống kê - một người theo trường phái Frequentist, một người theo Bayesian - sẽ tiếp cận câu hỏi này hoàn toàn khác nhau, không chỉ về mặt tính toán mà còn về mặt **triết học cơ bản**.

**Nhà thống kê Frequentist** sẽ nói: "Nếu đồng xu cân bằng (xác suất thực sự là 0.5), xác suất để quan sát được 7 ngửa hoặc cực đoan hơn là bao nhiêu?" Anh ta tính ra p-value = 0.344, và kết luận: "Không đủ bằng chứng để bác bỏ giả thuyết đồng xu cân bằng."

**Nhà thống kê Bayesian** sẽ hỏi một câu khác: "Cho trước dữ liệu này (7 ngửa trong 10 lần), xác suất thực sự ra ngửa có khả năng nằm ở đâu?" Cô ấy tính toán posterior distribution và trả lời: "Có 95% khả năng xác suất thực nằm trong khoảng [0.46, 0.86]. Giá trị có khả năng nhất là 0.65."

Bạn thấy sự khác biệt không? Frequentist trả lời về **dữ liệu giả định** (nếu giả thuyết đúng, dữ liệu sẽ như thế nào), trong khi Bayesian trả lời về **tham số thực** (cho trước dữ liệu, tham số có khả năng là gì). Câu hỏi của Bayesian chính là câu hỏi mà hầu hết chúng ta thực sự quan tâm!

## Sự Khác Biệt Triết Học Cơ Bản

### Xác Suất Là Gì?

Đây là nền tảng của mọi sự khác biệt.

**Quan điểm Frequentist: Xác suất = Tần suất Dài Hạn**

Với Frequentist, xác suất là tỷ lệ mà một sự kiện xảy ra trong vô số lần lặp lại. Khi nói "xác suất tung đồng xu ra ngửa là 0.5", họ có nghĩa là: nếu tung đồng xu vô hạn lần, 50% sẽ là ngửa.

Định nghĩa này có hệ quả quan trọng: **tham số θ không có xác suất**. Trong thí nghiệm tung đồng xu, tham số θ (xác suất thực ra ngửa) là một con số cố định - nó chỉ có một giá trị thực duy nhất, dù chúng ta không biết giá trị đó là gì. Vì nó không thể "lặp lại", nó không có "tần suất", và do đó không có "xác suất" theo nghĩa Frequentist.

Điều này nghe có vẻ kỳ lạ, nhưng nó nhất quán với định nghĩa của họ. Đối với Frequentist, chỉ có **dữ liệu** mới có thể ngẫu nhiên (vì chúng ta có thể tưởng tượng lặp lại thí nghiệm), còn **tham số** thì cố định.

**Quan điểm Bayesian: Xác suất = Mức Độ Tin Tưởng (Degree of Belief)**

Với Bayesian, xác suất đo lường **mức độ tin tưởng hoặc độ hợp lý** về một mệnh đề. Khi nói "xác suất θ = 0.7 là 30%", họ có nghĩa là: dựa trên những gì tôi biết, tôi tin 30% rằng θ có giá trị 0.7.

Định nghĩa này cho phép chúng ta gán xác suất cho **bất cứ thứ gì** mà chúng ta không chắc chắn - kể cả các tham số cố định. Trong thí nghiệm đồng xu, dù θ có một giá trị thực duy nhất, nhưng vì **chúng ta không biết** giá trị đó là gì, chúng ta có thể - và nên - dùng xác suất để biểu diễn sự không chắc chắn của mình.

Đối với Bayesian, **tham số** là biến ngẫu nhiên (phản ánh sự không biết của chúng ta), còn **dữ liệu** thì cố định (đã quan sát).

### Ai Là Ngẫu Nhiên? Ai Là Cố Định?

Đây là điểm then chốt:

| Khía cạnh | Frequentist | Bayesian |
|-----------|-------------|----------|
| **Tham số θ** | Cố định (nhưng không biết) | Biến ngẫu nhiên |
| **Dữ liệu** | Ngẫu nhiên (có thể lặp lại) | Cố định (đã quan sát) |
| **Xác suất** | Về dữ liệu chưa quan sát | Về tham số chưa biết |

Hệ quả:
- **Frequentist** có thể nói: $$P(\text{data} \mid \theta)$$ - "xác suất của dữ liệu cho trước tham số"
- **Bayesian** có thể nói: $$P(\theta \mid \text{data})$$ - "xác suất của tham số cho trước dữ liệu"

Câu nào là câu trả lời cho câu hỏi khoa học "tham số có khả năng là gì?"  Rõ ràng là câu thứ hai!

## Sự Khác Biệt trong Diễn Giải

### Confidence Interval vs Credible Interval

Hãy xem một ví dụ cụ thể. Bạn tính toán và được khoảng [0.46, 0.86]. Bạn diễn giải như thế nào?

**Diễn Giải Frequentist (95% Confidence Interval)**

"Nếu chúng ta lặp lại thí nghiệm này nhiều lần, và mỗi lần tính một khoảng tin cậy 95%, thì 95% các khoảng đó sẽ chứa giá trị θ thật."

Bạn **KHÔNG THỂ** nói: "Có 95% khả năng θ nằm trong khoảng [0.46, 0.86]."

Tại sao? Vì θ là cố định! Nó hoặc nằm trong khoảng (xác suất = 1), hoặc không nằm trong khoảng (xác suất = 0). Chúng ta chỉ không biết cái nào đúng.

Điều mà "95%" đề cập đến là **tính chất của phương pháp**, không phải của θ. Phương pháp này, khi áp dụng nhiều lần, sẽ tạo ra các khoảng mà 95% trong số chúng chứa θ.

Này nghe có vẻ phức tạp và gián tiếp, đúng không? Đó là vì nó *là* phức tạp và gián tiếp. Nó không trả lời câu hỏi "θ có khả năng ở đâu?" mà trả lời câu hỏi "phương pháp này đáng tin cậy thế nào?"

**Diễn Giải Bayesian (95% Credible Interval)**

"Có 95% khả năng θ nằm trong khoảng [0.46, 0.86]."

Hoặc chính xác hơn: "$$P(\theta \in [0.46, 0.86] \mid \text{data}) = 0.95$$"

Đơn giản, trực tiếp, và chính xác là câu trả lời bạn muốn. Bạn có thể nói điều này vì trong Bayesian, θ có phân phối xác suất - posterior distribution.

### P-value vs Posterior Probability

**P-value (Frequentist)**

Giả sử bạn muốn test xem θ có lớn hơn 0.5 hay không. Với dữ liệu 7/10, bạn tính p-value = 0.344.

Diễn giải đúng: "Nếu θ = 0.5 (giả thuyết không), xác suất quan sát được 7 ngửa hoặc cực đoan hơn là 34.4%."

Bạn **KHÔNG THỂ** nói: "Có 34.4% khả năng θ = 0.5" hay "Có 65.6% khả năng θ ≠ 0.5".

P-value là $$P(\text{data or more extreme} \mid H_0)$$, không phải $$P(H_0 \mid \text{data})$$.

**Posterior Probability (Bayesian)**

Với cùng dữ liệu, bạn tính posterior và được: $$P(\theta > 0.5 \mid \text{data}) = 0.89$$

Diễn giải: "Có 89% khả năng θ lớn hơn 0.5."

Đây chính xác là câu trả lời cho câu hỏi "θ có lớn hơn 0.5 không?" - một câu trả lời trực tiếp và có nghĩa.

## Ưu và Nhược Điểm

### Ưu Điểm của Frequentist

1. **Không cần prior**: Không phải chọn prior distribution, tránh tranh cãi về "chủ quan"
2. **Đảm bảo tần suất**: Confidence intervals và tests có tính chất tần suất được đảm bảo
3. **Được dạy rộng rãi**: Hầu hết người làm khoa học đều biết
4. **Công cụ sẵn có**: Nhiều software và packages

### Nhược Điểm của Frequentist

1. **Diễn giải phức tạp**: CI và p-values rất khó diễn giải đúng, thường bị hiểu sai
2. **Không trả lời câu hỏi quan tâm**: $$P(\text{data} \mid H_0)$$ thay vì $$P(H_0 \mid \text{data})$$
3. **Phụ thuộc vào ý định**: Kết quả thay đổi tùy vào "stopping rule" (khi nào dừng thu thập dữ liệu)
4. **Không cập nhật được**: Không có cách tự nhiên để kết hợp kiến thức trước hoặc cập nhật khi có dữ liệu mới

### Ưu Điểm của Bayesian

1. **Diễn giải tự nhiên**: Posterior probabilities và credible intervals dễ hiểu và trực tiếp
2. **Trả lời đúng câu hỏi**: $$P(\theta \mid \text{data})$$ - chính xác là điều bạn quan tâm
3. **Cập nhật tuần tự**: Dễ dàng kết hợp dữ liệu mới: posterior hôm nay là prior ngày mai
4. **Kết hợp kiến thức trước**: Prior cho phép tích hợp nghiên cứu trước, lý thuyết, expert knowledge
5. **Xử lý tốt mẫu nhỏ**: Prior giúp regularization, ổn định estimates
6. **Tự nhiên với hierarchical models**: Bayesian framework hoàn hảo cho partial pooling

### Nhược Điểm của Bayesian

1. **Cần chọn prior**: Phải quyết định prior distribution (nhưng có thể dùng weakly informative priors)
2. **Tính toán phức tạp**: Thường cần MCMC, mất thời gian (nhưng PyMC, Stan rất tốt)
3. **Ít được dạy**: Ít người học, ít hiểu (nhưng đang thay đổi!)

## Khi Nào Dùng Phương Pháp Nào?

### Dùng Frequentist khi:

- **Clinical trials với quy định**: FDA và các cơ quan quản lý thường yêu cầu p-values và kiểm soát Type I error
- **Mẫu lớn, vấn đề đơn giản**: Khi không cần prior và asymptotic theory đủ tốt
- **Báo cáo cho audience không biết Bayes**: Khi người đọc quen với p-values (dù hiểu sai!)
- **Không có prior information**: Hoàn toàn mới, không có nghiên cứu trước

### Dùng Bayesian khi:

- **Mẫu nhỏ**: Prior giúp ổn định estimates, regularization tự nhiên
- **Cần diễn giải trực tiếp**: "Xác suất tham số lớn hơn 0 là bao nhiêu?"
- **Có prior information**: Nghiên cứu trước, expert knowledge, lý thuyết
- **Sequential learning**: Cập nhật model khi có dữ liệu mới (online learning)
- **Hierarchical/multilevel data**: Học sinh trong lớp, bệnh nhân trong bệnh viện
- **Complex models**: Flexible priors, many parameters, missing data

### Ví Dụ Thực Tế

**Frequentist phù hợp:**
- A/B testing với traffic lớn (hàng triệu visitors)
- Clinical trial phase III
- Quality control manufacturing
- National surveys với n > 10,000

**Bayesian phù hợp:**
- A/B testing với traffic nhỏ (startup sớm)
- Medical diagnosis (kết hợp prior knowledge)
- Recommendation systems
- Machine learning với uncertainty
- Time series forecasting
- Meta-analysis (kết hợp nhiều studies)

**Cả hai đều tốt:**
- Linear regression với n lớn
- Simple hypothesis tests với assumptions đủ
- Descriptive statistics

## Xu Hướng Hiện Đại

Bayesian đang ngày càng trở nên phổ biến vì ba lý do chính:

### 1. Công Cụ Tốt Hơn

Các tools như **PyMC**, **Stan**, và **TensorFlow Probability** làm cho Bayesian inference trở nên accessible. Bạn không cần viết MCMC từ đầu nữa - chỉ cần specify model và library sẽ lo phần còn lại.

### 2. Tính Toán Rẻ Hơn

GPUs, cloud computing, và các thuật toán MCMC hiệu quả (như NUTS trong PyMC) làm cho models phức tạp có thể fit trong vài phút thay vì vài ngày.

### 3. Nhu Cầu Thực Tế

Tech companies (Google, Facebook, Netflix) sử dụng Bayesian rộng rãi. Machine learning cần uncertainty quantification. AI safety đòi hỏi Bayesian decision theory.

**American Statistical Association** (2016) đã công khai cảnh báo về lạm dụng p-values và khuyến nghị alternatives - trong đó Bayesian là một lựa chọn hàng đầu.

Nhiều journals, đặc biệt trong psychology và medicine, giờ khuyến khích hoặc yêu cầu Bayesian analysis cùng với hoặc thay vì p-values.

## Tóm Tắt: Bayesian vs Frequentist

| Khía cạnh | Frequentist | Bayesian |
|-----------|-------------|----------|
| **Xác suất** | Tần suất dài hạn | Mức độ tin tưởng |
| **Tham số θ** | Cố định | Biến ngẫu nhiên |
| **Dữ liệu** | Ngẫu nhiên | Cố định |
| **Prior** | Không có | Bắt buộc |
| **Kết quả** | Point estimate + CI | Posterior distribution |
| **Diễn giải** | Phức tạp, gián tiếp | Đơn giản, trực tiếp |
| **Câu trả lời** | $$P(\text{data} \mid \theta)$$ | $$P(\theta \mid \text{data})$$ |

**Kết luận**: Bayesian cung cấp một framework nhất quán và trực quan cho suy luận thống kê. Với công cụ hiện đại, Bayesian là lựa chọn ưu tiên cho hầu hết các bài toán trong khoa học dữ liệu, machine learning, và nghiên cứu khoa học hiện đại.

## Bài Tập

**Bài tập 1: Diễn giải Confidence Interval.** Cho 95% CI = [0.3, 0.7] cho tỷ lệ ủng hộ một chính sách. (a) Viết diễn giải **đúng** theo quan điểm Frequentist. (b) Giải thích tại sao **không thể** nói "có 95% khả năng tỷ lệ thực nằm trong [0.3, 0.7]". (c) Nếu dùng Bayesian với prior uninformative, credible interval sẽ gần giống CI. Viết diễn giải Bayesian và so sánh với Frequentist.

**Bài tập 2: P-value.** Trong một thí nghiệm y học, p-value = 0.03 cho test "thuốc có hiệu quả". (a) Viết diễn giải **đúng** của p-value này. (b) Liệt kê 3 diễn giải **SAI** phổ biến. (c) Giải thích tại sao không thể dùng p-value để nói về xác suất giả thuyết đúng.

**Bài tập 3: Bayesian Posterior.** Với dữ liệu 12 thành công trong 15 thử, và prior Beta(2,2): (a) Tính posterior Beta(α', β'). (b) Tính $$P(\theta > 0.5 \mid \text{data})$$. (c) Tính 95% credible interval. (d) So sánh với p-value cho $$H_0: \theta = 0.5$$ và giải thích sự khác biệt.

**Bài tập 4: Khi nào dùng gì?** Với mỗi tình huống sau, chọn Frequentist hoặc Bayesian và giải thích tại sao: (a) Startup test hai versions của landing page với 500 visitors. (b) FDA approval cho thuốc mới với 10,000 patients. (c) Dự đoán sales tháng tới dựa trên 2 năm dữ liệu history. (d) Kiểm tra quality control với 1 triệu sản phẩm mỗi ngày.

**Bài tập 5: Mô phỏng.** Viết code Python để: (a) Mô phỏng 1000 experiments với θ thật = 0.6, n = 20. (b) Cho mỗi experiment, tính 95% CI (Frequentist) và 95% credible interval (Bayesian với prior Beta(2,2)). (c) Tính tỷ lệ intervals chứa θ thật. (d) Vẽ histogram của độ rộng của các intervals. So sánh và giải thích.

## Tài Liệu Tham Khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 1: Probability and inference
- Chapter 4: Asymptotics and connections to non-Bayesian approaches

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 11: Null Hypothesis Significance Testing
- Chapter 12: Bayesian Approaches to Testing a Point ("Null") Value

**McElreath, R. (2020).** *Statistical Rethinking: A Bayesian Course with Examples in R and Stan* (2nd Edition). CRC Press.
- Chapter 1: The Golem of Prague (fundamental differences)
- Chapter 2: Small worlds and large worlds

### Supplementary Reading:

**Wasserstein, R. L., & Lazar, N. A. (2016).** The ASA's statement on p-values: Context, process, and purpose. *The American Statistician*, 70(2), 129-133.
- ASA's official statement cảnh báo về p-values

**Dienes, Z. (2011).** Bayesian versus orthodox statistics: Which side are you on? *Perspectives on Psychological Science*, 6(3), 274-290.
- So sánh triết học rất rõ ràng

**Morey, R. D., Hoekstra, R., Rouder, J. N., Lee, M. D., & Wagenmakers, E. J. (2016).** The fallacy of placing confidence in confidence intervals. *Psychonomic Bulletin & Review*, 23(1), 103-123.
- Giải thích tại sao CI khó diễn giải

---

*Chúc mừng! Bạn đã hoàn thành Chapter 01 - Bayesian Inference Fundamentals.*  
*Tiếp theo: Chapter 02 - Building Blocks of Bayesian Models*
