---
layout: post
title: "Bài 1.2: Xác suất như Độ hợp lý - Nền tảng Triết học của Bayesian"
chapter: '01'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sự khác biệt cơ bản giữa hai cách diễn giải xác suất: **quan điểm tần suất (frequentist) và quan điểm Bayesian**. Bạn sẽ nhận ra rằng đây không chỉ là sự khác biệt kỹ thuật, mà là **sự khác biệt triết học sâu sắc về bản chất của xác suất và suy luận khoa học**. Quan trọng hơn, bạn sẽ thấy rằng quan điểm Bayesian - xem xác suất như một thước đo độ hợp lý hoặc độ tin cậy - tự nhiên và trực quan hơn nhiều cho hầu hết các vấn đề khoa học thực tế. Bài học này sẽ đặt nền tảng triết học cho toàn bộ khóa học về phân tích Bayesian. Cox đã chỉ ra rằng nếu chúng ta muốn gán

## Giới thiệu: Xác suất có nghĩa là gì?

Hãy bắt đầu với một câu hỏi đơn giản nhưng sâu sắc: "Xác suất trời mưa ngày mai là 70%" có nghĩa là gì?

Nếu bạn hỏi một nhà thống kê tần suất, họ sẽ gặp khó khăn trong việc trả lời. Theo định nghĩa tần suất, xác suất là tần số dài hạn của một sự kiện trong vô số lần lặp lại giống hệt nhau. Nhưng "ngày mai" chỉ xảy ra một lần. Chúng ta không thể lặp lại "ngày mai" vô số lần để đếm tần suất trời mưa. Vậy thì "xác suất 70%" có nghĩa là gì trong ngữ cảnh này?

Nếu bạn hỏi một người bình thường trên đường phố, họ sẽ nói: "Điều đó có nghĩa là tôi khá chắc chắn trời sẽ mưa, nhưng không hoàn toàn chắc chắn. Tôi nên mang theo ô." Đây là một diễn giải hoàn toàn tự nhiên và hữu ích. Xác suất 70% thể hiện **mức độ tin tưởng** hoặc **độ hợp lý** của sự kiện "trời mưa ngày mai" dựa trên thông tin hiện có (dự báo thời tiết, mùa, vị trí địa lý, v.v.).

![Câu chuyện Linh và Chiếc Ô]({{ site.baseurl }}/img/chapter_img/chapter01/linh_umbrella_story.png)

Hình trên minh họa cách chúng ta tự nhiên sử dụng xác suất Bayesian trong cuộc sống hàng ngày: khi nghe dự báo "70% xác suất mưa", chúng ta hiểu đó là mức độ tin tưởng và quyết định mang ô, không phải nghĩ về tần số dài hạn trong vô số vũ trụ song song!

Đây chính xác là quan điểm Bayesian về xác suất. **Xác suất không phải là một tính chất khách quan của thế giới (tần số dài hạn), mà là một thước đo chủ quan của kiến thức và sự không chắc chắn của chúng ta. Và đây không phải là điểm yếu, mà là điểm mạnh, vì nó cho phép chúng ta áp dụng xác suất vào mọi loại vấn đề, không chỉ những vấn đề có thể lặp lại.**

## Quan điểm Tần suất: Xác suất như Tần số Dài hạn

Trước khi chúng ta đi sâu vào quan điểm Bayesian, hãy hiểu rõ quan điểm tần suất để thấy sự khác biệt.

Theo quan điểm tần suất, xác suất của một sự kiện $$A$$ được định nghĩa là giới hạn của tần số tương đối khi số lần lặp lại tiến đến vô cùng:

$$P(A) = \lim_{n \to \infty} \frac{\text{số lần } A \text{ xảy ra}}{n}$$

Ví dụ, nếu chúng ta toss một đồng xu công bằng vô số lần, tỷ lệ lần ra Ngửa sẽ tiến gần đến 0.5. Đây là xác suất tần suất của sự kiện "ra Ngửa".

Định nghĩa này có một số hệ quả quan trọng:

**Xác suất là khách quan.** Nó không phụ thuộc vào kiến thức hoặc niềm tin của chúng ta. Đồng xu có xác suất 0.5 ra Ngửa bất kể chúng ta biết điều đó hay không.

**Xác suất chỉ áp dụng cho sự kiện có thể lặp lại.** Chúng ta không thể nói về "xác suất Einstein là thiên tài" hoặc "xác suất vũ trụ bắt đầu từ Big Bang" theo nghĩa tần suất, vì những sự kiện này không thể lặp lại.

**Tham số là cố định nhưng không biết.** Trong thống kê tần suất, các tham số của mô hình (như trung bình của một phân phối) được coi là các hằng số cố định, không phải là các biến ngẫu nhiên. Chúng ta không thể nói "xác suất tham số $$\theta = 0.5$$" vì $$\theta$$ không phải là ngẫu nhiên - nó hoặc là 0.5 hoặc không phải.

Những hạn chế này làm cho quan điểm tần suất khó áp dụng vào nhiều vấn đề khoa học thực tế. Trong hầu hết các tình huống, chúng ta không thể lặp lại thí nghiệm vô số lần, và chúng ta thực sự muốn đưa ra các phát biểu xác suất về các tham số hoặc giả thuyết.

## Quan điểm Bayesian: Xác suất như Độ hợp lý

Quan điểm Bayesian về xác suất rất khác. Xác suất không phải là tần số dài hạn, mà là **thước đo độ hợp lý** (plausibility) hoặc **độ tin cậy** (degree of belief) của một mệnh đề, dựa trên thông tin hiện có.

Theo quan điểm này:

**Xác suất là chủ quan (nhưng có nguyên tắc).** Hai người có thể gán các xác suất khác nhau cho cùng một sự kiện nếu họ có thông tin khác nhau. Nhưng điều này không có nghĩa là "bất cứ điều gì cũng được". Xác suất Bayesian phải tuân theo các quy tắc của lý thuyết xác suất (các tiên đề Kolmogorov) để đảm bảo tính nhất quán.

**Xác suất áp dụng cho bất kỳ mệnh đề nào.** Chúng ta có thể nói về "xác suất một giả thuyết là đúng", "xác suất một tham số nằm trong một khoảng", hoặc "xác suất trời mưa ngày mai". Tất cả những điều này đều có ý nghĩa như các thước đo độ tin cậy.

**Tham số là biến ngẫu nhiên.** Trong thống kê Bayesian, các tham số không được coi là cố định mà không biết, mà là các biến ngẫu nhiên có phân phối xác suất. Phân phối này thể hiện sự không chắc chắn của chúng ta về giá trị thực của tham số.

**Xác suất có thể thay đổi khi có thêm thông tin.** Khi chúng ta quan sát dữ liệu mới, chúng ta cập nhật xác suất của mình. Đây là bản chất của suy diễn Bayesian: bắt đầu với một niềm tin ban đầu (prior), quan sát dữ liệu, và cập nhật niềm tin (posterior).

## Một Ví dụ Minh họa: Đồng xu của Bạn bè

Hãy xem xét một ví dụ cụ thể để thấy rõ sự khác biệt giữa hai quan điểm.

Giả sử một người bạn đưa cho bạn một đồng xu và nói: "Tôi vừa toss đồng xu này 10 lần và thấy 8 lần ra Ngửa. Xác suất đồng xu này ra Ngửa là bao nhiêu?"

**Quan điểm Tần suất:** Một nhà thống kê tần suất sẽ nói: "Chúng ta không thể nói về 'xác suất' của tham số (xác suất thực của đồng xu ra Ngửa). Tham số là một hằng số cố định. Những gì chúng ta có thể làm là ước lượng nó và cung cấp một khoảng tin cậy. Ước lượng điểm là 8/10 = 0.8. Khoảng tin cậy 95% là [0.49, 0.95]." Nhưng khoảng tin cậy này **không** có nghĩa là "có 95% xác suất tham số nằm trong khoảng này". Nó có nghĩa là "nếu chúng ta lặp lại quy trình này vô số lần, 95% các khoảng được tạo ra sẽ chứa giá trị thực của tham số".

**Quan điểm Bayesian:** Một nhà thống kê Bayesian sẽ nói: "Trước khi thấy dữ liệu, tôi tin rằng đồng xu có thể là công bằng (xác suất 0.5) hoặc không công bằng, nhưng tôi không chắc chắn. Đây là prior của tôi. Sau khi thấy 8 Ngửa trong 10 lần toss, tôi cập nhật niềm tin của mình. Posterior của tôi cho thấy xác suất cao nhất là khoảng 0.7, và có 95% xác suất tham số nằm trong khoảng [0.5, 0.9]." Khoảng này **thực sự** có nghĩa là "dựa trên dữ liệu và prior của tôi, tôi tin 95% rằng tham số nằm trong khoảng này".

Bạn thấy sự khác biệt không? Diễn giải Bayesian trực tiếp trả lời câu hỏi chúng ta quan tâm: "Dựa trên dữ liệu này, tham số có khả năng là bao nhiêu?" Diễn giải tần suất trả lời một câu hỏi khác về hành vi dài hạn của một quy trình.

## Cox's Theorem: Xác suất như Logic Mở rộng

Bạn có thể hỏi: "Nếu xác suất Bayesian là chủ quan, làm sao nó có thể là khoa học? Khoa học không phải là khách quan sao?"

Câu trả lời nằm trong một kết quả toán học đẹp đẽ được gọi là **Cox's Theorem** (1946). Richard Cox đã chứng minh rằng nếu chúng ta muốn một hệ thống để suy luận hợp lý về các mệnh đề không chắc chắn, và nếu hệ thống này phải tuân theo một số quy tắc tối thiểu về tính nhất quán, thì hệ thống đó **phải** là lý thuyết xác suất.

Cụ thể, Cox đã chỉ ra rằng nếu chúng ta muốn gán các "mức độ tin cậy" (degree of belief) cho các mệnh đề sao cho:

1. Mức độ tin cậy được biểu diễn bằng số thực.
2. Mức độ tin cậy phụ thuộc vào thông tin hiện có.
3. Các quy tắc kết hợp mức độ tin cậy phải nhất quán (ví dụ, nếu $$A$$ ngụ ý $$B$$, thì mức độ tin cậy của $$A$$ không thể lớn hơn mức độ tin cậy của $$B$$).

Thì các quy tắc này **bắt buộc** phải là các quy tắc của lý thuyết xác suất: quy tắc cộng, quy tắc nhân, và định lý Bayes.

Điều này có nghĩa là xác suất Bayesian không phải là một lựa chọn tùy ý. Nó là cách duy nhất nhất quán để suy luận về sự không chắc chắn. Xác suất là **logic mở rộng** - một cách để mở rộng logic nhị phân (đúng/sai) sang logic liên tục (mức độ tin cậy từ 0 đến 1).

## Tại sao Quan điểm Bayesian Tự nhiên hơn?

Trong thực tế, hầu hết mọi người tự nhiên suy nghĩ theo cách Bayesian, ngay cả khi họ không biết về thống kê Bayesian. Khi bạn nghe dự báo thời tiết nói "70% xác suất mưa", bạn không nghĩ về tần số dài hạn trong vô số vũ trụ song song. Bạn nghĩ: "Tôi khá chắc chắn trời sẽ mưa, nhưng không hoàn toàn chắc."

Khi một bác sĩ nói "có 80% xác suất bạn bị cảm cúm", họ không có nghĩa là nếu chúng ta lặp lại cuộc sống của bạn vô số lần trong cùng điều kiện, 80% các lần bạn sẽ bị cảm cúm. Họ có nghĩa là dựa trên các triệu chứng và kiến thức y học, cảm cúm là chẩn đoán có khả năng cao nhất.

![Bayesian trong Cuộc sống Hàng ngày]({{ site.baseurl }}/img/chapter_img/chapter01/bayesian_daily_life.png)

Hình trên minh họa ba tình huống hàng ngày mà chúng ta tự nhiên sử dụng tư duy Bayesian: (1) Dự báo thời tiết - "70% mưa" là mức độ tin tưởng, (2) Chẩn đoán y tế - bác sĩ cập nhật niềm tin dựa trên triệu chứng, và (3) Đoán người gõ cửa - chúng ta kết hợp thông tin prior (ai thường đến) với dữ liệu (tiếng bước chân) để đưa ra kết luận.

Khi một nhà khoa học nói "dữ liệu này hỗ trợ mạnh mẽ cho giả thuyết X", họ đang đưa ra một phát biểu về độ hợp lý của giả thuyết cho trước dữ liệu - **một phát biểu Bayesian**.

Quan điểm Bayesian phù hợp với cách chúng ta tự nhiên suy nghĩ về sự không chắc chắn. Nó cho phép chúng ta:

1. **Kết hợp kiến thức prior.** Chúng ta không bắt đầu mỗi phân tích từ con số không. Chúng ta có kiến thức từ nghiên cứu trước, lý thuyết, và kinh nghiệm. Bayesian cho phép chúng ta mã hóa kiến thức này như prior và cập nhật nó với dữ liệu mới.

2. **Đưa ra phát biểu trực tiếp về các tham số.** Chúng ta có thể nói "có 95% xác suất hiệu ứng điều trị nằm giữa 0.2 và 0.5" - một phát biểu rõ ràng và hữu ích. Trong khung tần suất, chúng ta chỉ có thể nói về khoảng tin cậy với diễn giải phức tạp về hành vi dài hạn.

3. **Định lượng sự không chắc chắn một cách tự nhiên.** Thay vì quyết định nhị phân "bác bỏ" hoặc "không bác bỏ", chúng ta có một phân phối xác suất đầy đủ thể hiện mức độ không chắc chắn của chúng ta về mọi giá trị tham số có thể.

4. **So sánh các mô hình và giả thuyết.** Chúng ta có thể tính xác suất tương đối của các mô hình khác nhau cho trước dữ liệu, giúp chúng ta chọn mô hình phù hợp nhất.

## Phản biện Phổ biến và Trả lời

**Phản biện 1: "Xác suất chủ quan không khoa học."**  
Trả lời: Khoa học không yêu cầu khách quan tuyệt đối. Nó yêu cầu tính minh bạch, có thể tái lập, và tự sửa chữa. Trong Bayesian, chúng ta minh bạch về prior của mình, và khi dữ liệu tích lũy, các posterior sẽ hội tụ bất kể prior ban đầu (với điều kiện prior không quá cực đoan). Hơn nữa, "khách quan" trong thống kê tần suất cũng là một ảo tưởng - nhiều quyết định chủ quan được đưa ra trong việc chọn kiểm định, mức ý nghĩa, và cách xử lý dữ liệu.

**Phản biện 2: "Prior là tùy ý."**  
Trả lời: Prior không cần phải tùy ý. Chúng có thể dựa trên nghiên cứu trước, lý thuyết, hoặc kiến thức chuyên môn. Và chúng ta có thể kiểm tra độ nhạy cảm của kết quả đối với prior. Nếu kết quả thay đổi đáng kể với các prior hợp lý khác nhau, điều này cho chúng ta biết rằng dữ liệu không đủ mạnh để đưa ra kết luận chắc chắn - một thông tin hữu ích!

**Phản biện 3: "Bayesian phức tạp hơn."**  
Trả lời: Về mặt khái niệm, Bayesian thực sự đơn giản hơn - nó trả lời trực tiếp các câu hỏi chúng ta quan tâm. Về mặt tính toán, đúng là Bayesian có thể phức tạp hơn, nhưng với các công cụ hiện đại như PyMC, Stan, và JAGS, điều này không còn là rào cản lớn.

## Ý nghĩa cho Phân tích Dữ liệu

Sự khác biệt triết học giữa quan điểm tần suất và Bayesian không chỉ là tranh luận học thuật. Nó có những hệ quả thực tế sâu sắc cho cách chúng ta phân tích dữ liệu và diễn giải kết quả.

Trong các bài học tiếp theo, chúng ta sẽ thấy cách quan điểm Bayesian dẫn đến các phương pháp phân tích cụ thể: **định lý Bayes, phân phối prior và posterior, posterior predictive checks, và so sánh mô hình Bayesian**. Tất cả những công cụ này đều xuất phát tự nhiên từ ý tưởng cơ bản rằng xác suất là một thước đo độ hợp lý, và suy luận là quá trình cập nhật niềm tin khi có thêm bằng chứng.

Nhưng trước tiên, chúng ta cần hiểu công cụ toán học cốt lõi của suy diễn Bayesian: định lý Bayes.

## Bài tập

**Bài tập 1: Diễn giải Xác suất.** Với mỗi phát biểu sau, hãy nói nó có ý nghĩa theo quan điểm tần suất, Bayesian, hoặc cả hai, và giải thích: (a) "Xác suất đồng xu này ra Ngửa là 0.5." (b) "Xác suất trời mưa ngày mai là 0.7." (c) "Xác suất giả thuyết Einstein đúng là 0.99." (d) "Xác suất tham số $$\theta$$ lớn hơn 0 là 0.95." (e) "Nếu chúng ta lặp lại thí nghiệm này 100 lần, chúng ta kỳ vọng thấy kết quả này khoảng 5 lần."

**Bài tập 2: Cập nhật Niềm tin.** Bạn tin rằng một đồng xu có thể công bằng (xác suất 0.5) hoặc thiên về Ngửa (xác suất 0.7), và ban đầu bạn nghĩ hai khả năng này có khả năng như nhau. (a) Đây là prior của bạn. Vẽ hoặc mô tả nó. (b) Bạn toss đồng xu 10 lần và thấy 7 lần ra Ngửa. Bạn nghĩ niềm tin của bạn nên thay đổi như thế nào? (c) Nếu bạn thấy 10 lần ra Ngửa trong 10 lần toss, niềm tin của bạn sẽ thay đổi như thế nào? (d) Thảo luận về cách dữ liệu mạnh hơn ảnh hưởng đến posterior nhiều hơn.

**Bài tập 3: So sánh Khoảng.** Một nghiên cứu báo cáo: (a) "Khoảng tin cậy 95% cho hiệu ứng điều trị là [0.2, 0.5]." (b) "Khoảng tin cậy Bayesian 95% cho hiệu ứng điều trị là [0.2, 0.5]." Viết hai đoạn văn ngắn giải thích ý nghĩa của mỗi khoảng theo cách mà một bác sĩ không chuyên về thống kê có thể hiểu. Khoảng nào dễ diễn giải hơn? Tại sao?

**Bài tập 4: Dutch Book.** Giả sử bạn gán các xác suất sau: $$P(A) = 0.6$$, $$P(B) = 0.5$$, $$P(A \cap B) = 0.4$$, $$P(A \cup B) = 0.6$$. (a) Kiểm tra xem các xác suất này có nhất quán với các quy tắc xác suất không. (b) Nếu không nhất quán, chỉ ra quy tắc nào bị vi phạm. (c) Giải thích bằng lời tại sao các xác suất không nhất quán này có thể dẫn đến các quyết định tồi.

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 1: Probability and inference (Bayesian vs. frequentist)

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 2: Introduction: Credibility, Models, and Parameters

**McElreath, R. (2020).** *Statistical Rethinking: A Bayesian Course with Examples in R and Stan* (2nd Edition). CRC Press.
- Chapter 1: The Golem of Prague
- Chapter 2: Small Worlds and Large Worlds

### Supplementary Reading:

**Jaynes, E. T. (2003).** *Probability Theory: The Logic of Science*. Cambridge University Press.
- Chapters 1-2: Plausible reasoning and Cox's theorem

**Lindley, D. V. (2000).** The Philosophy of Statistics. *Journal of the Royal Statistical Society: Series D*, 49(3), 293-337.

---

*Bài học tiếp theo: [1.3 Định lý Bayes và Phân phối Posterior](/vi/chapter01/bayes-theorem-posterior/)*
