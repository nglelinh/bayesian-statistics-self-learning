---
layout: post
title: "Bài 1.3: Định lý Bayes - Công cụ Cập nhật Niềm tin"
chapter: '01'
order: 3
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu định lý Bayes không chỉ là một công thức toán học, mà là một công cụ mạnh mẽ để cập nhật niềm tin một cách hợp lý khi có thêm bằng chứng. Bạn sẽ nắm vững ý nghĩa của từng thành phần trong công thức - prior, likelihood, và posterior - và hiểu cách chúng tương tác để tạo ra suy luận Bayesian. Quan trọng hơn, bạn sẽ phát triển trực giác về cách dữ liệu và kiến thức prior kết hợp với nhau, và tại sao điều này tự nhiên hơn nhiều so với các phương pháp thống kê truyền thống.


## Giới thiệu:

Hãy tưởng tượng bạn là một bác sĩ đang chẩn đoán một bệnh nhân. Bệnh nhân có các triệu chứng: sốt, ho, và mệt mỏi. Dựa trên kinh nghiệm và đào tạo của bạn, bạn biết rằng các triệu chứng này có thể do nhiều nguyên nhân: cảm cúm, COVID-19, hoặc viêm phổi vi khuẩn. Làm thế nào bạn quyết định chẩn đoán nào có khả năng nhất?

![Chẩn đoán Y tế với Bayes]({{ site.baseurl }}/img/chapter_img/chapter01/doctor_diagnosis_bayes.png)

Hình trên minh họa một bác sĩ sử dụng tư duy Bayesian trong chẩn đoán: (1) Bắt đầu với prior - tỷ lệ phổ biến của các bệnh trong mùa này, (2) Quan sát triệu chứng của bệnh nhân (likelihood), và (3) Cập nhật niềm tin để có posterior - chẩn đoán cuối cùng. Đây chính xác là cách định lý Bayes hoạt động trong thực tế!

Bạn bắt đầu với kiến thức prior: bạn biết rằng trong mùa này, cảm cúm rất phổ biến (giả sử 50% các trường hợp có triệu chứng tương tự), COVID-19 ít phổ biến hơn (30%), và viêm phổi vi khuẩn hiếm (20%). Đây là **prior** của bạn - niềm tin ban đầu trước khi xem xét chi tiết triệu chứng của bệnh nhân cụ thể này.

Sau đó, bạn xem xét các triệu chứng cụ thể. Bạn biết rằng nếu bệnh nhân có cảm cúm, xác suất họ có cả ba triệu chứng này là 60%. Nếu họ có COVID-19, xác suất là 80%. Nếu họ có viêm phổi vi khuẩn, xác suất là 40%. Đây là **likelihood** - xác suất quan sát được dữ liệu (triệu chứng) cho mỗi chẩn đoán có thể.

Bây giờ, làm thế nào bạn kết hợp prior và likelihood để đưa ra chẩn đoán cuối cùng? Đây chính xác là điều mà định lý Bayes làm. Nó cho bạn một công thức chính xác để cập nhật niềm tin ban đầu (prior) dựa trên bằng chứng mới (likelihood) để có được niềm tin cập nhật (**posterior**).

Định lý Bayes không chỉ áp dụng cho chẩn đoán y học. Nó là nguyên tắc cơ bản của mọi học tập và suy luận hợp lý. Mỗi khi chúng ta cập nhật niềm tin dựa trên bằng chứng mới, chúng ta đang áp dụng định lý Bayes, dù chúng ta có ý thức về điều đó hay không.

## Định lý Bayes: Công thức và Ý nghĩa

Định lý Bayes có thể được phát biểu đơn giản như sau. Giả sử chúng ta có một tham số hoặc giả thuyết $$\theta$$ mà chúng ta quan tâm, và chúng ta quan sát dữ liệu $$D$$. Định lý Bayes cho chúng ta biết:

$$P(\theta \mid D) = \frac{P(D \mid \theta) \cdot P(\theta)}{P(D)}$$

Hãy phân tích từng thành phần:

**$$P(\theta \mid D)$$ - Posterior (Phân phối Hậu nghiệm):** Đây là xác suất của $$\theta$$ cho trước dữ liệu $$D$$. Nó thể hiện niềm tin cập nhật của chúng ta về $$\theta$$ sau khi quan sát dữ liệu. Đây là điều chúng ta muốn tính toán - câu trả lời cho câu hỏi "Dựa trên dữ liệu này, giá trị nào của $$\theta$$ có khả năng nhất?"

**$$P(D \mid \theta)$$ - Likelihood (Hàm hợp lý):** Đây là xác suất quan sát được dữ liệu $$D$$ nếu $$\theta$$ có giá trị cụ thể. Nó thể hiện mức độ "tương thích" giữa dữ liệu và giá trị tham số. Lưu ý rằng trong likelihood, chúng ta coi dữ liệu là cố định và $$\theta$$ là biến - ngược lại với cách chúng ta thường nghĩ về xác suất.

**$$P(\theta)$$ - Prior (Phân phối Tiên nghiệm):** Đây là xác suất của $$\theta$$ trước khi quan sát dữ liệu. Nó thể hiện kiến thức, niềm tin, hoặc giả định ban đầu của chúng ta về $$\theta$$. Prior có thể đến từ nghiên cứu trước, lý thuyết, hoặc kiến thức chuyên môn.

**$$P(D)$$ - Evidence (Bằng chứng) hoặc Marginal Likelihood:** Đây là xác suất quan sát được dữ liệu, tích phân qua tất cả các giá trị có thể của $$\theta$$. Nó đóng vai trò như một hằng số chuẩn hóa để đảm bảo posterior là một phân phối xác suất hợp lệ (tích phân bằng 1).

Định lý Bayes thường được viết ở dạng tỷ lệ, bỏ qua hằng số chuẩn hóa:

$$P(\theta \mid D) \propto P(D \mid \theta) \cdot P(\theta)$$

Điều này nói rằng: **Posterior tỷ lệ với Likelihood nhân Prior**. Đây là trái tim của suy diễn Bayesian.

## Suy ra Định lý Bayes: Một Hệ quả Đơn giản

Định lý Bayes không phải là một nguyên lý mới hoặc sâu sắc. Nó là một hệ quả trực tiếp của định nghĩa xác suất có điều kiện. Hãy xem cách suy ra nó.

Từ định nghĩa xác suất có điều kiện, chúng ta có:

$$P(\theta \mid D) = \frac{P(\theta, D)}{P(D)}$$

và

$$P(D \mid \theta) = \frac{P(\theta, D)}{P(\theta)}$$

Từ phương trình thứ hai, chúng ta có $$P(\theta, D) = P(D \mid \theta) \cdot P(\theta)$$. Thay vào phương trình đầu tiên:

$$P(\theta \mid D) = \frac{P(D \mid \theta) \cdot P(\theta)}{P(D)}$$

Đó là định lý Bayes! Nó chỉ là một cách viết lại định nghĩa xác suất có điều kiện. Nhưng đừng để sự đơn giản của suy ra này che lấp tầm quan trọng của nó. Định lý Bayes cung cấp một công thức chính xác để cập nhật niềm tin, và đây là nền tảng của toàn bộ thống kê Bayesian.

## Một Ví dụ Cụ thể: Đồng xu Thiên lệch

Hãy xem xét một ví dụ đơn giản để thấy định lý Bayes hoạt động như thế nào trong thực tế. Giả sử chúng ta có một đồng xu, và chúng ta muốn ước lượng xác suất nó ra Ngửa, ký hiệu là $$\theta$$.

**Prior:** Trước khi toss đồng xu, chúng ta tin rằng nó có thể công bằng ($$\theta = 0.5$$) hoặc có thể thiên lệch một chút, nhưng chúng ta không chắc chắn. Chúng ta mã hóa niềm tin này bằng một phân phối Beta với tham số $$\alpha = 2, \beta = 2$$. Phân phối này tập trung xung quanh 0.5 nhưng cho phép một số biến thiên.

**Dữ liệu:** Chúng ta toss đồng xu 10 lần và quan sát 7 lần ra Ngửa và 3 lần ra Sấp.

**Likelihood:** Với mỗi giá trị có thể của $$\theta$$, chúng ta có thể tính xác suất quan sát được 7 Ngửa trong 10 lần toss. Đây là phân phối Binomial:

$$P(D \mid \theta) = \binom{10}{7} \theta^7 (1-\theta)^3$$

**Posterior:** Áp dụng định lý Bayes, posterior cũng là một phân phối Beta với tham số $$\alpha' = 2 + 7 = 9, \beta' = 2 + 3 = 5$$. (Đây là một ví dụ của phân phối liên hợp - chúng ta sẽ thảo luận về điều này sau.)

Posterior này cho chúng ta biết rằng sau khi quan sát dữ liệu, niềm tin của chúng ta về $$\theta$$ đã thay đổi. Trung bình của posterior là $$\frac{9}{9+5} = 0.64$$, cao hơn prior mean là 0.5. Dữ liệu đã "kéo" niềm tin của chúng ta về phía các giá trị $$\theta$$ lớn hơn, phù hợp với việc chúng ta thấy nhiều Ngửa hơn Sấp.

![Định lý Bayes: Prior × Likelihood = Posterior]({{ site.baseurl }}/img/chapter_img/chapter01/bayes_theorem_visualization.png)

Hình trên minh họa cách định lý Bayes hoạt động với ví dụ đồng xu: (1) Prior (màu xanh) - niềm tin ban đầu tập trung xung quanh θ=0.5, (2) Likelihood (màu cam) - dữ liệu 7 Ngửa/10 lần toss hỗ trợ mạnh cho θ cao hơn, và (3) Posterior (màu tím) - kết quả của việc kết hợp prior và likelihood, dịch chuyển về phía θ≈0.64. Đây là "thỏa hiệp" giữa kiến thức prior và bằng chứng từ dữ liệu.

![Visualizing Bayes' Theorem with Coin Flips]({{ site.baseurl }}/img/chapter_img/chapter01/coin_bayes_visualization.png)

Hình trên cho thấy chi tiết hơn về cách posterior thay đổi khi có thêm dữ liệu: bắt đầu với prior (0 lần toss), sau đó cập nhật tuần tự sau mỗi lần quan sát (1, 3, 5, 7, 10 lần toss). Lưu ý rằng posterior càng lúc càng "hẹp" (ít không chắc chắn hơn) và dịch chuyển về giá trị θ phù hợp với dữ liệu quan sát được.

## Prior, Likelihood, và Posterior: Một Cuộc Đối thoại

Một cách hữu ích để nghĩ về định lý Bayes là như một cuộc đối thoại giữa prior và likelihood, với posterior là sự thỏa hiệp giữa chúng.

**Prior nói:** "Dựa trên kiến thức trước đó, tôi nghĩ $$\theta$$ có khả năng nằm trong khoảng này."

**Likelihood nói:** "Nhưng nhìn vào dữ liệu! Nếu $$\theta$$ có giá trị đó, dữ liệu này sẽ rất bất thường. Các giá trị $$\theta$$ khác phù hợp với dữ liệu tốt hơn."

**Posterior nói:** "OK, hãy thỏa hiệp. Tôi sẽ xem xét cả kiến thức prior và dữ liệu mới. Dựa trên cả hai, đây là niềm tin cập nhật của tôi về $$\theta$$."

Mức độ mà posterior nghiêng về prior hay likelihood phụ thuộc vào **độ mạnh** của mỗi cái. Nếu prior rất mạnh (chắc chắn) và dữ liệu ít, posterior sẽ gần với prior. Nếu prior yếu (không chắc chắn) và dữ liệu nhiều, posterior sẽ chủ yếu được xác định bởi likelihood.

Đây là một đặc điểm đẹp đẽ của suy diễn Bayesian: nó tự động cân bằng giữa kiến thức prior và bằng chứng mới. Khi dữ liệu tích lũy, ảnh hưởng của prior giảm dần, và posterior hội tụ về giá trị thực của tham số (với điều kiện mô hình đúng).

![So sánh Prior Mạnh vs Prior Yếu]({{ site.baseurl }}/img/chapter_img/chapter01/prior_strength_comparison.png)

Hình trên so sánh hai trường hợp: (1) Prior yếu (Beta(2,2) - phẳng, không chắc chắn) dễ bị "kéo" bởi dữ liệu, posterior gần với likelihood, và (2) Prior mạnh (Beta(20,20) - nhọn, rất chắc chắn về θ=0.5) "kháng cự" lại dữ liệu, cần nhiều bằng chứng hơn mới thay đổi. Đây là một tính năng, không phải bug - cho phép chúng ta mã hóa mức độ tin tưởng vào kiến thức trước đó.

![Prior Strength Chi tiết]({{ site.baseurl }}/img/chapter_img/chapter01/prior_strength_detailed.png)

Hình trên minh họa chi tiết hơn về ảnh hưởng của độ mạnh prior: với cùng dữ liệu (7/10), prior yếu cho posterior mean = 0.64 (gần với dữ liệu 0.7), trong khi prior mạnh cho posterior mean = 0.54 (vẫn gần với prior 0.5). Khi dữ liệu tích lũy (ví dụ 70/100), cả hai posterior đều hội tụ về giá trị thật, nhưng prior mạnh hội tụ chậm hơn.

## Evidence: Hằng số Chuẩn hóa và Hơn thế nữa

Thành phần $$P(D)$$ trong định lý Bayes, được gọi là evidence hoặc marginal likelihood, thường bị bỏ qua vì nó chỉ là một hằng số chuẩn hóa. Nhưng nó thực sự có ý nghĩa quan trọng, đặc biệt trong so sánh mô hình.

Evidence được tính bằng cách tích phân likelihood qua tất cả các giá trị có thể của tham số, có trọng số bởi prior:

$$P(D) = \int P(D \mid \theta) P(\theta) d\theta$$

Đây là xác suất quan sát được dữ liệu, trung bình hóa qua sự không chắc chắn về $$\theta$$. Nó trả lời câu hỏi: "Nếu chúng ta không biết $$\theta$$ chính xác là gì, nhưng chúng ta có prior về nó, xác suất chúng ta sẽ thấy dữ liệu này là bao nhiêu?"

Evidence có hai vai trò quan trọng:

**Chuẩn hóa Posterior:** Nó đảm bảo rằng posterior là một phân phối xác suất hợp lệ (tích phân bằng 1).

**So sánh Mô hình:** Khi chúng ta có nhiều mô hình khác nhau (với các prior và likelihood khác nhau), chúng ta có thể so sánh evidence của chúng để xem mô hình nào phù hợp với dữ liệu tốt hơn. Tỷ số của hai evidence được gọi là **Bayes factor**, một công cụ mạnh mẽ cho so sánh mô hình Bayesian.

Trong thực hành, evidence thường khó tính toán vì nó liên quan đến tích phân qua không gian tham số, có thể có nhiều chiều. Đây là một trong những thách thức tính toán của phân tích Bayesian, và chúng ta sẽ thảo luận về các phương pháp để giải quyết nó (như MCMC) trong các bài học sau.

## Sequential Updating: Học tập như một Quá trình

Một đặc điểm đẹp đẽ của định lý Bayes là nó cho phép **cập nhật tuần tự** (sequential updating). Posterior từ một lần cập nhật có thể trở thành prior cho lần cập nhật tiếp theo khi có thêm dữ liệu mới.

Giả sử chúng ta bắt đầu với prior $$P(\theta)$$, quan sát dữ liệu $$D_1$$, và tính posterior:

$$P(\theta \mid D_1) = \frac{P(D_1 \mid \theta) P(\theta)}{P(D_1)}$$

Sau đó, chúng ta quan sát thêm dữ liệu $$D_2$$. Chúng ta có thể sử dụng $$P(\theta \mid D_1)$$ như prior mới:

$$P(\theta \mid D_1, D_2) = \frac{P(D_2 \mid \theta) P(\theta \mid D_1)}{P(D_2 \mid D_1)}$$

Điều thú vị là, kết quả cuối cùng giống như nếu chúng ta đã cập nhật một lần với tất cả dữ liệu $$D_1$$ và $$D_2$$ cùng lúc (với điều kiện các quan sát độc lập). Thứ tự mà chúng ta quan sát dữ liệu không quan trọng - chỉ có tổng bằng chứng mới quan trọng.

Điều này phản ánh cách chúng ta học trong thực tế. Chúng ta không bắt đầu từ đầu mỗi khi có thông tin mới. Chúng ta cập nhật niềm tin hiện tại dựa trên bằng chứng mới. Định lý Bayes cung cấp một công thức chính xác cho quá trình học tập tự nhiên này.

![Sequential Updating: Cập nhật Tuần tự]({{ site.baseurl }}/img/chapter_img/chapter01/sequential_updating.png)

## Ý nghĩa Triết học: Suy luận như Cập nhật Niềm tin

Định lý Bayes không chỉ là một công cụ tính toán. Nó thể hiện một quan điểm triết học về bản chất của suy luận khoa học.

Trong quan điểm Bayesian, suy luận không phải là quá trình "chấp nhận" hoặc "bác bỏ" giả thuyết dựa trên một ngưỡng tùy ý (như p < 0.05). Nó là quá trình **cập nhật niềm tin một cách liên tục và định lượng** dựa trên bằng chứng tích lũy.

Chúng ta không bao giờ "chứng minh" một giả thuyết là đúng hoặc sai một cách tuyệt đối. Chúng ta chỉ có thể nói rằng dựa trên bằng chứng hiện có, một giả thuyết có độ hợp lý cao hơn hoặc thấp hơn. Khi có thêm bằng chứng, chúng ta cập nhật đánh giá của mình.

Quan điểm này phù hợp hơn nhiều với cách khoa học thực sự hoạt động. Các lý thuyết khoa học không được "chứng minh" một lần và mãi mãi. Chúng được hỗ trợ ngày càng mạnh mẽ (hoặc yếu đi) khi bằng chứng tích lũy. Định lý Bayes cung cấp một khung toán học chính xác cho quá trình này.

## Ý nghĩa cho Phân tích Dữ liệu

Trong các bài học tiếp theo, chúng ta sẽ thấy định lý Bayes được áp dụng vào nhiều vấn đề khác nhau: ước lượng tham số, kiểm định giả thuyết, dự đoán, và so sánh mô hình. Nhưng ý tưởng cơ bản luôn giống nhau: bắt đầu với prior, quan sát dữ liệu, tính likelihood, và cập nhật để có posterior.

Trong thực hành, chúng ta thường không thể tính posterior một cách giải tích (bằng công thức đóng) vì tích phân trong evidence quá phức tạp. Thay vào đó, chúng ta sử dụng các phương pháp tính toán như Markov Chain Monte Carlo (MCMC) để lấy mẫu từ posterior. Nhưng nguyên tắc cơ bản vẫn là định lý Bayes.

Định lý Bayes cũng làm rõ vai trò của prior trong phân tích Bayesian. Prior không phải là "thiên kiến" cần tránh, mà là một phần cần thiết và hữu ích của suy luận. Nó cho phép chúng ta kết hợp kiến thức trước đó với dữ liệu mới một cách có nguyên tắc. Và như chúng ta đã thấy, khi dữ liệu tích lũy, ảnh hưởng của prior giảm dần.

## Bài tập

**Bài tập 1: Áp dụng Định lý Bayes.** Một xét nghiệm y tế cho một bệnh hiếm có độ nhạy 99% (nếu có bệnh, xét nghiệm dương tính 99% thời gian) và độ đặc hiệu 95% (nếu không có bệnh, xét nghiệm âm tính 95% thời gian). Bệnh này xuất hiện ở 1% dân số. (a) Một người được xét nghiệm dương tính. Xác suất họ thực sự có bệnh là bao nhiêu? (b) Sử dụng định lý Bayes để tính toán. (c) Kết quả có ngạc nhiên không? Giải thích tại sao prior (tỷ lệ bệnh trong dân số) quan trọng.

**Bài tập 2: Prior, Likelihood, Posterior.** Giả sử $$\theta$$ có thể nhận ba giá trị: 0.3, 0.5, 0.7. Prior của bạn là $$P(\theta = 0.3) = 0.2$$, $$P(\theta = 0.5) = 0.5$$, $$P(\theta = 0.7) = 0.3$$. Bạn quan sát 3 thành công trong 5 lần thử. (a) Tính likelihood cho mỗi giá trị $$\theta$$. (b) Tính posterior (unnormalized và normalized). (c) Vẽ biểu đồ prior, likelihood, và posterior. (d) Giá trị $$\theta$$ nào có posterior cao nhất? Tại sao?

**Bài tập 3: Sequential Updating.** Bắt đầu với prior Beta(2, 2) cho xác suất một đồng xu ra Ngửa. (a) Bạn toss đồng xu 5 lần và thấy 4 Ngửa. Tính posterior. (b) Sử dụng posterior này như prior mới, bạn toss thêm 5 lần và thấy 2 Ngửa. Tính posterior mới. (c) So sánh với posterior nếu bạn đã cập nhật một lần với tất cả 10 lần toss (6 Ngửa, 4 Sấp). Chúng có giống nhau không?

**Bài tập 4: Prior Strength.** Xem xét hai prior khác nhau cho cùng một vấn đề: (a) Prior 1: Beta(2, 2) - weakly informative. (b) Prior 2: Beta(20, 20) - strongly informative. Với cùng dữ liệu (7 thành công trong 10 thử), tính posterior cho mỗi prior. So sánh chúng. Prior nào bị ảnh hưởng nhiều hơn bởi dữ liệu? Tại sao?

**Bài tập 5: Suy ngẫm về Prior.** Viết một đoạn văn ngắn (300-400 từ) suy ngẫm về: (a) Prior có phải là "thiên kiến" không? (b) Làm thế nào chúng ta nên chọn prior trong thực hành? (c) Điều gì xảy ra nếu prior của chúng ta sai? (d) Tại sao việc minh bạch về prior lại quan trọng trong phân tích Bayesian?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 1: Probability and inference
- Chapter 2: Single-parameter models

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 5: Bayes' Rule
- Chapter 6: Inferring a Binomial Probability via Exact Mathematical Analysis

**McElreath, R. (2020).** *Statistical Rethinking: A Bayesian Course with Examples in R and Stan* (2nd Edition). CRC Press.
- Chapter 2: Small Worlds and Large Worlds
- Chapter 3: Sampling the Imaginary

### Supplementary Reading:

**Jaynes, E. T. (2003).** *Probability Theory: The Logic of Science*. Cambridge University Press.
- Chapter 4: Elementary hypothesis testing

---

*Bài học tiếp theo: [1.4 Bayesian vs. Frequentist - So sánh Hai Paradigm](/vi/chapter01/bayesian-vs-frequentist/)*
