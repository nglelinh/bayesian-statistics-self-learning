---
layout: post
title: "Bài 1.1: Khủng hoảng Khoa học và Giới hạn của P-values"
chapter: '01'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu tại sao khoa học hiện đại đang đối mặt với một cuộc khủng hoảng về khả năng tái lập kết quả nghiên cứu, và vai trò của p-values trong cuộc khủng hoảng này. Bạn sẽ nhận ra rằng p-values không phải là công cụ "khách quan" và "chính xác" như nhiều người vẫn tin, mà chúng thường bị hiểu sai, dễ bị thao túng, và dẫn đến những kết luận sai lệch. Quan trọng hơn, bạn sẽ bắt đầu thấy rằng vấn đề không chỉ nằm ở cách chúng ta sử dụng p-values, mà còn ở chính bản chất của khung suy luận tần suất (frequentist) mà p-values dựa trên. Bài học này sẽ tạo động lực mạnh mẽ cho việc tìm kiếm một cách tiếp cận tốt hơn - phân tích Bayesian.

## Giới thiệu: Một Cuộc Khủng hoảng đang Diễn ra

Hãy tưởng tượng bạn là một nhà khoa học đọc một nghiên cứu mới được công bố trên một tạp chí uy tín. Nghiên cứu báo cáo một phát hiện thú vị: một loại thuốc mới có hiệu quả trong việc điều trị một bệnh hiểm nghèo, với p-value < 0.05. Bạn quyết định lặp lại thí nghiệm trong phòng thí nghiệm của mình với cùng phương pháp, cùng cỡ mẫu, và cùng mức độ cẩn thận. Nhưng khi kết quả ra, bạn không thấy hiệu quả gì cả. P-value của bạn là 0.42. Điều gì đã xảy ra?

Đây không phải là một trường hợp cá biệt. Trong những năm gần đây, khoa học đã đối mặt với một cuộc **khủng hoảng tái lập** (replication crisis) nghiêm trọng. Nhiều kết quả được công bố, đặc biệt trong tâm lý học, y học, và khoa học xã hội, không thể được tái lập khi các nhà nghiên cứu độc lập cố gắng lặp lại thí nghiệm. Các con số là đáng báo động: trong một nghiên cứu lớn của Open Science Collaboration năm 2015, chỉ 36% trong số 100 nghiên cứu tâm lý học được công bố có thể được tái lập thành công. Trong y học tiền lâm sàng, con số này thậm chí còn tồi tệ hơn: chỉ 11% theo một nghiên cứu của Begley và Ellis năm 2012.

![Thống kê Khủng hoảng Tái lập]({{ site.baseurl }}/img/chapter_img/chapter01/replication_crisis_stats.png)

Hình trên cho thấy tỷ lệ tái lập thành công trong các lĩnh vực khác nhau: Tâm lý học (36%), Y học tiền lâm sàng (11%), và Kinh tế học (61%). Những con số này cho thấy một cuộc khủng hoảng nghiêm trọng trong phương pháp khoa học hiện đại, đặc biệt trong các lĩnh vực phụ thuộc nhiều vào p-values và NHST.

Cuộc khủng hoảng này không phải là do các nhà khoa học gian lận hoặc thiếu cẩn thận. Nó là hệ quả của một vấn đề sâu xa hơn: cách chúng ta suy luận từ dữ liệu. Và ở trung tâm của vấn đề này là một công cụ thống kê được sử dụng rộng rãi nhất trong khoa học hiện đại: p-value.

## P-value là gì? Một Định nghĩa Chính xác (và Khó hiểu)

Trước khi chúng ta phê phán p-values, hãy đảm bảo rằng chúng ta hiểu chính xác chúng là gì. Đây là định nghĩa chính thức:

> **P-value là xác suất quan sát được dữ liệu ít nhất cực đoan như dữ liệu quan sát, giả sử rằng giả thuyết không (null hypothesis) là đúng.**

Hãy phân tích định nghĩa này từng phần. Giả sử chúng ta đang kiểm tra xem một loại thuốc mới có hiệu quả hay không. Giả thuyết không ($$H_0$$) là "thuốc không có hiệu quả", và giả thuyết thay thế ($$H_1$$) là "thuốc có hiệu quả". Chúng ta thu thập dữ liệu từ một thử nghiệm lâm sàng và tính toán một thống kê kiểm định, ví dụ như sự khác biệt trung bình giữa nhóm điều trị và nhóm đối chứng.

P-value trả lời câu hỏi: "Nếu thuốc thực sự không có hiệu quả ($$H_0$$ đúng), xác suất để chúng ta quan sát được một sự khác biệt ít nhất lớn như sự khác biệt chúng ta đã thấy là bao nhiêu?" Nếu p-value nhỏ (thường < 0.05), chúng ta kết luận rằng dữ liệu "không tương thích" với giả thuyết không, và chúng ta "bác bỏ" $$H_0$$.

Nhưng hãy chú ý đến những gì p-value **không** nói. Nó không nói "xác suất giả thuyết không là đúng". Nó không nói "xác suất thuốc có hiệu quả". Nó không đo lường độ lớn của hiệu ứng. Nó không nói gì về tầm quan trọng thực tế của kết quả. Tất cả những gì nó nói là: "Nếu giả thuyết không đúng, dữ liệu này sẽ khá bất thường."

Sự khác biệt tinh tế này - giữa $$P(\text{dữ liệu} \mid H_0)$$ (cái mà p-value đo lường) và $$P(H_0 \mid \text{dữ liệu})$$ (cái mà chúng ta thực sự quan tâm) - là nguồn gốc của vô số hiểu lầm.

## Những Hiểu lầm Phổ biến về P-values

Hãy xem xét một số hiểu lầm phổ biến nhất về p-values, ngay cả trong cộng đồng khoa học:

**Hiểu lầm 1: P-value là xác suất giả thuyết không là đúng.**  
Sai. P-value là $$P(\text{dữ liệu} \mid H_0)$$, không phải $$P(H_0 \mid \text{dữ liệu})$$. Trong khung tần suất, giả thuyết không được coi là cố định (đúng hoặc sai), không phải là một biến ngẫu nhiên có xác suất.

**Hiểu lầm 2: 1 - p-value là xác suất giả thuyết thay thế là đúng.**  
Sai. Ngay cả khi p-value nhỏ, điều này không tự động làm cho giả thuyết thay thế có khả năng cao. Có thể có nhiều giả thuyết thay thế khác nhau, hoặc có thể có vấn đề với thiết kế nghiên cứu.

**Hiểu lầm 3: P-value < 0.05 có nghĩa là kết quả "có ý nghĩa thống kê".**  
Đúng về mặt quy ước, nhưng ngưỡng 0.05 là hoàn toàn tùy ý. Không có gì kỳ diệu xảy ra khi p-value vượt qua ngưỡng này. Một p-value 0.049 không khác biệt về mặt thực chất so với 0.051, nhưng một cái được gọi là "có ý nghĩa" và cái kia thì không.

**Hiểu lầm 4: P-value nhỏ có nghĩa là hiệu ứng lớn hoặc quan trọng.**  
Sai. P-value phụ thuộc vào cả độ lớn của hiệu ứng và cỡ mẫu. Với cỡ mẫu đủ lớn, ngay cả một hiệu ứng rất nhỏ và không có ý nghĩa thực tế cũng có thể cho p-value rất nhỏ. Ngược lại, một hiệu ứng lớn và quan trọng có thể có p-value lớn nếu cỡ mẫu nhỏ.

**Hiểu lầm 5: Nếu p-value > 0.05, giả thuyết không là đúng.**  
Sai. Không bác bỏ được giả thuyết không không có nghĩa là nó đúng. Có thể chúng ta chỉ không có đủ dữ liệu (statistical power thấp) để phát hiện hiệu ứng.

Những hiểu lầm này không phải là vô hại. Chúng dẫn đến những quyết định sai lệch trong nghiên cứu, chính sách, và y học lâm sàng.

## P-hacking và Publication Bias: Khi Khoa học Trở thành Trò chơi

Vấn đề với p-values không chỉ nằm ở việc chúng bị hiểu sai, mà còn ở việc chúng dễ bị thao túng. Khi thành công nghề nghiệp của các nhà khoa học phụ thuộc vào việc công bố các kết quả "có ý nghĩa thống kê" (p < 0.05), một động lực mạnh mẽ được tạo ra để "tìm" các p-values nhỏ, ngay cả khi không có hiệu ứng thực sự.

**P-hacking** (còn gọi là data dredging hoặc fishing) là thực hành phân tích dữ liệu theo nhiều cách khác nhau cho đến khi tìm được một kết quả "có ý nghĩa". Các kỹ thuật p-hacking bao gồm:

- Thử nhiều biến phụ thuộc khác nhau và chỉ báo cáo cái cho p-value nhỏ nhất.
- Thử nhiều cách phân nhóm dữ liệu khác nhau.
- Thu thập dữ liệu cho đến khi p < 0.05, sau đó dừng lại.
- Loại bỏ các outliers một cách có chọn lọc.
- Thử nhiều phép kiểm định thống kê khác nhau.

Mỗi quyết định phân tích này có thể hợp lý khi được xem xét riêng lẻ, nhưng khi chúng được đưa ra sau khi nhìn thấy dữ liệu và với mục tiêu đạt được p < 0.05, chúng làm tăng đáng kể tỷ lệ phát hiện giả (false positive rate) lên xa trên 5%.

![Các Kỹ thuật P-hacking]({{ site.baseurl }}/img/chapter_img/chapter01/phacking_techniques.png)

Hình trên minh họa các kỹ thuật p-hacking phổ biến: (1) Optional stopping - dừng thu thập dữ liệu khi p < 0.05, (2) Cherry-picking - chỉ báo cáo biến phụ thuộc cho p-value nhỏ nhất, (3) Outlier removal - loại bỏ outliers một cách có chọn lọc, và (4) Subgroup analysis - thử nhiều cách phân nhóm khác nhau. Mỗi kỹ thuật này làm tăng tỷ lệ false positive lên xa trên 5% danh nghĩa.

Một vấn đề liên quan là **publication bias**: các tạp chí khoa học có xu hướng công bố các nghiên cứu với kết quả "dương tính" (p < 0.05) hơn là các nghiên cứu với kết quả "âm tính" (p > 0.05). Điều này tạo ra một bức tranh sai lệch về bằng chứng khoa học. Nếu 20 phòng thí nghiệm độc lập thử nghiệm một giả thuyết sai, chúng ta kỳ vọng 1 trong số đó (5%) sẽ có p < 0.05 chỉ do ngẫu nhiên. Nếu chỉ nghiên cứu này được công bố và 19 nghiên cứu còn lại bị "file drawer" (giấu trong ngăn kéo), văn học khoa học sẽ cho rằng giả thuyết được hỗ trợ, trong khi thực tế nó là sai.

![Publication Bias]({{ site.baseurl }}/img/chapter_img/chapter01/publication_bias.png)

Hình trên minh họa publication bias (file drawer problem): khi 20 lab độc lập thử nghiệm một giả thuyết SAI (không có hiệu ứng thực sự), chúng ta kỳ vọng khoảng 1 lab (5%) sẽ tìm thấy p < 0.05 chỉ do ngẫu nhiên. Nếu chỉ lab này được công bố và 19 lab còn lại bị "giấu trong ngăn kéo", văn học khoa học sẽ cho rằng giả thuyết được hỗ trợ, tạo ra một bức tranh sai lệch nghiêm trọng về bằng chứng khoa học.

## Tại sao P-values Không trả lời Câu hỏi Chúng ta Quan tâm

Vấn đề cơ bản nhất với p-values là chúng không trả lời câu hỏi mà các nhà khoa học thực sự quan tâm. Khi chúng ta tiến hành một nghiên cứu, chúng ta muốn biết:

- Giả thuyết của chúng ta có khả năng đúng không?
- Nếu có hiệu ứng, nó lớn đến mức nào?
- Chúng ta nên tin tưởng vào kết quả này đến mức nào?
- Dữ liệu hỗ trợ giả thuyết này hơn các giả thuyết thay thế khác như thế nào?

P-values không trả lời bất kỳ câu hỏi nào trong số này một cách trực tiếp. Thay vào đó, chúng trả lời một câu hỏi rất khác: "Nếu giả thuyết không đúng và chúng ta lặp lại thí nghiệm này vô số lần, tỷ lệ nào trong số các thí nghiệm đó sẽ cho kết quả ít nhất cực đoan như cái chúng ta đã thấy?"

Đây là một câu hỏi về **hành vi dài hạn của một quy trình** (long-run behavior of a procedure), không phải về **độ tin cậy của một giả thuyết cụ thể** (plausibility of a specific hypothesis) dựa trên dữ liệu hiện có. Sự khác biệt này là cơ bản và phản ánh sự khác biệt triết học sâu sắc giữa thống kê tần suất và thống kê Bayesian.

## Một Ví dụ Minh họa: Phát hiện Ngoại cảm

Hãy xem xét một ví dụ cụ thể để thấy rõ vấn đề. Năm 2011, nhà tâm lý học Daryl Bem công bố một nghiên cứu trên Journal of Personality and Social Psychology, một tạp chí uy tín, tuyên bố tìm thấy bằng chứng cho "ngoại cảm" (precognition) - khả năng dự đoán tương lai. Trong một trong các thí nghiệm của ông, người tham gia được yêu cầu dự đoán vị trí của một hình ảnh sẽ xuất hiện trên màn hình máy tính, và vị trí này được xác định ngẫu nhiên **sau khi** người tham gia đưa ra dự đoán. Bem báo cáo rằng người tham gia đoán đúng 53.1% thời gian, cao hơn đáng kể so với 50% kỳ vọng nếu họ chỉ đoán ngẫu nhiên, với p = 0.01.

Bây giờ, hãy suy nghĩ về điều này. Chúng ta có thực sự tin rằng con người có khả năng nhìn thấy tương lai không? Hầu hết các nhà khoa học sẽ nói không, vì điều này vi phạm mọi thứ chúng ta biết về vật lý và sinh học. Nhưng nếu chúng ta chỉ nhìn vào p-value, nó cho chúng ta biết rằng kết quả này "có ý nghĩa thống kê" và chúng ta nên "bác bỏ giả thuyết không" rằng không có ngoại cảm.

Vấn đề ở đây là p-value không tính đến **prior plausibility** (độ hợp lý tiên nghiệm) của giả thuyết. Nó xử lý giả thuyết "con người có ngoại cảm" giống như giả thuyết "aspirin làm giảm đau đầu" - cả hai đều chỉ cần p < 0.05 để được "chấp nhận". Nhưng trực giác của chúng ta nói rằng chúng ta cần bằng chứng mạnh hơn nhiều cho một tuyên bố phi thường hơn.

Đây chính xác là điều mà phân tích Bayesian làm. Nó cho phép chúng ta kết hợp kiến thức prior (những gì chúng ta đã biết trước khi thấy dữ liệu) với dữ liệu mới để đưa ra kết luận hợp lý. Nếu chúng ta bắt đầu với một prior rất hoài nghi về ngoại cảm (vì nó vi phạm vật lý), ngay cả dữ liệu của Bem cũng không đủ để làm chúng ta tin vào ngoại cảm. Chúng ta sẽ cần bằng chứng mạnh hơn nhiều.

## Con đường Phía trước: Tại sao chúng ta cần Bayesian

Cuộc khủng hoảng tái lập và các vấn đề với p-values đã dẫn đến một sự phản tư sâu sắc trong cộng đồng khoa học. Nhiều nhà thống kê và nhà khoa học phương pháp đã kêu gọi giảm bớt sự phụ thuộc vào p-values và NHST. Một số đề xuất các giải pháp trong khung tần suất, như sử dụng khoảng tin cậy, tính toán effect sizes, hoặc điều chỉnh ngưỡng p-value.

Nhưng những giải pháp này không giải quyết được vấn đề cơ bản: khung tần suất không trả lời trực tiếp các câu hỏi mà các nhà khoa học quan tâm. Chúng ta không muốn biết "Nếu giả thuyết không đúng, dữ liệu này sẽ hiếm đến mức nào?" Chúng ta muốn biết "Dựa trên dữ liệu này, giả thuyết nào có khả năng đúng nhất?"

Phân tích Bayesian cung cấp một khung suy luận khác, một khung trả lời trực tiếp các câu hỏi này. Thay vì tính $$P(\text{dữ liệu} \mid H_0)$$, Bayesian tính $$P(H \mid \text{dữ liệu})$$ - xác suất của giả thuyết cho trước dữ liệu. Thay vì quyết định nhị phân "bác bỏ" hoặc "không bác bỏ", Bayesian cung cấp một phân phối xác suất đầy đủ về các giá trị tham số có thể, định lượng sự không chắc chắn của chúng ta.

Trong các bài học tiếp theo, chúng ta sẽ khám phá chi tiết cách phân tích Bayesian hoạt động, tại sao nó tự nhiên và trực quan hơn, và làm thế nào nó giúp chúng ta tránh được các cạm bẫy của p-values. Nhưng trước tiên, chúng ta cần hiểu nền tảng triết học của Bayesian: xác suất như một thước đo độ tin cậy.

## Bài tập

**Bài tập 1: Diễn giải P-value.** Một nghiên cứu kiểm tra xem một loại thuốc mới có giảm huyết áp hay không. Giả thuyết không là "thuốc không có hiệu quả". Nghiên cứu báo cáo p = 0.03. Với mỗi phát biểu sau, hãy nói nó đúng hay sai và giải thích: (a) Xác suất giả thuyết không là đúng là 3%. (b) Xác suất thuốc có hiệu quả là 97%. (c) Nếu chúng ta lặp lại nghiên cứu này 100 lần và giả thuyết không đúng, chúng ta kỳ vọng thấy kết quả ít nhất cực đoan như thế này khoảng 3 lần. (d) Kết quả này có ý nghĩa lâm sàng quan trọng.

**Bài tập 2: P-hacking Simulation.** Sử dụng Python, mô phỏng tình huống sau: Bạn là một nhà nghiên cứu kiểm tra 20 giả thuyết khác nhau, tất cả đều sai (không có hiệu ứng thực sự). Với mỗi giả thuyết, bạn sinh dữ liệu ngẫu nhiên và tính p-value. (a) Bao nhiêu trong 20 p-values sẽ < 0.05? (b) Nếu bạn chỉ công bố các kết quả với p < 0.05, tỷ lệ false positive là bao nhiêu? (c) Lặp lại mô phỏng này 1000 lần và vẽ histogram của số lượng "phát hiện có ý nghĩa". Điều này dạy bạn gì về publication bias?

**Bài tập 3: Cỡ mẫu và P-value.** Xem xét hai nghiên cứu về cùng một hiệu ứng: (a) Nghiên cứu A: n = 50, hiệu ứng quan sát = 0.5, p = 0.08. (b) Nghiên cứu B: n = 500, hiệu ứng quan sát = 0.15, p = 0.02. Nghiên cứu nào "có ý nghĩa thống kê"? Nghiên cứu nào có hiệu ứng lớn hơn? Nếu bạn là một bác sĩ, bạn sẽ quan tâm đến nghiên cứu nào hơn? Điều này minh họa vấn đề gì với việc chỉ dựa vào p-values?

**Bài tập 4: Nghịch lý Ngoại cảm.** Giả sử xác suất prior của bạn cho "ngoại cảm tồn tại" là 0.0001 (rất hoài nghi). Bạn thấy một nghiên cứu với p = 0.01. (a) Điều này có làm bạn tin vào ngoại cảm không? Tại sao? (b) Nếu bạn thấy 10 nghiên cứu độc lập, tất cả đều cho p < 0.05, bạn có thay đổi ý kiến không? (c) Thảo luận về vai trò của prior plausibility trong đánh giá bằng chứng khoa học. Đây là một vấn đề mà thống kê tần suất không giải quyết được như thế nào?

**Bài tập 5: Suy ngẫm về Khủng hoảng Tái lập.** Viết một đoạn văn ngắn (300-400 từ) suy ngẫm về: (a) Tại sao khủng hoảng tái lập lại nghiêm trọng đến vậy? (b) Vai trò của p-values và NHST trong cuộc khủng hoảng này. (c) Những thay đổi nào trong thực hành khoa học có thể giúp cải thiện tình hình? (d) Phân tích Bayesian có thể giải quyết một số vấn đề này như thế nào?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 1: Probability and inference (critique of p-values)

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 11: Null Hypothesis Significance Testing

**McElreath, R. (2020).** *Statistical Rethinking: A Bayesian Course with Examples in R and Stan* (2nd Edition). CRC Press.
- Chapter 1: The Golem of Prague (critique of mechanical statistics)

### Supplementary Reading:

**Wasserstein, R. L., & Lazar, N. A. (2016).** The ASA Statement on p-Values: Context, Process, and Purpose. *The American Statistician*, 70(2), 129-133.

**Open Science Collaboration. (2015).** Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.

**Ioannidis, J. P. A. (2005).** Why Most Published Research Findings Are False. *PLoS Medicine*, 2(8), e124.

---

*Bài học tiếp theo: [1.2 Xác suất như Độ tin cậy - Quan điểm Bayes](/vi/chapter01/probability-as-plausibility/)*
