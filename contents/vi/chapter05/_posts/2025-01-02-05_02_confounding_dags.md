---
layout: post
title: "Bài 5.2: Confounding và DAGs - Causal Inference Basics"
chapter: '05'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter05
lesson_type: required
---

Mùa thu năm 1973, Đại học UC Berkeley đối diện một cáo buộc nghiêm trọng về phân biệt giới tính trong tuyển sinh sau đại học: nhìn vào bảng tổng hợp toàn trường, 44% ứng viên nam trúng tuyển trong khi con số ở nữ chỉ là 35%. Thế nhưng khi nhà thống kê Peter Bickel cùng cộng sự tách số liệu theo từng khoa, một kết quả gây chấn động xuất hiện: ở hầu hết các khoa, tỷ lệ trúng tuyển của nữ thậm chí còn nhỉnh hơn nam! Nguyên nhân là ứng viên nữ nộp nhiều hơn vào các khoa có tỷ lệ chọi khắt khe nhất. Câu chuyện kinh điển ấy là lời nhắc sắc bén nhất về lý do dữ liệu thuần túy không bao giờ tự nói lên quan hệ nhân quả nếu thiếu một **đồ thị nhân quả (DAG)**.

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu hiện tượng gây nhiễu (confounding) là gì và vì sao nó dễ khiến ta rút ra kết luận sai từ dữ liệu quan sát. Bạn cũng sẽ biết cách sử dụng đồ thị nhân quả có hướng không chu trình (DAG) để quyết định biến nào cần điều chỉnh và biến nào không nên đưa vào mô hình — nền tảng cốt lõi của suy luận nhân quả (causal inference).

> **Ví dụ ngắn.** Một bệnh viện ghi nhận nhóm bệnh nhân được điều trị tích cực có tỷ lệ hồi phục thấp hơn nhóm điều trị chuẩn. Kết luận rằng "điều trị tích cực làm bệnh nặng hơn" có thể hoàn toàn sai nếu các ca vốn nặng hơn ngay từ lúc nhập viện mới được chỉ định điều trị tích cực. Khi đó, mức độ nặng ban đầu của bệnh chính là biến gây nhiễu.
>
> **Câu hỏi tự kiểm tra.** Điều gì có thể xảy ra nếu ta bỏ qua một biến ảnh hưởng đồng thời tới cả biến can thiệp (treatment) lẫn biến kết quả (outcome)?


## Kiến thức cần nhớ: Mô hình cấu trúc nhân quả, Toán tử do() và Quy tắc d-separation

Suy luận nhân quả hiện đại (theo trường phái Judea Pearl) nâng cấp hồi quy thống kê bằng ba khái niệm nền tảng:

- **Quan sát $$P(Y \mid X=x)$$ khác can thiệp $$P(Y \mid \mathrm{do}(X=x))$$:** Phân phối có điều kiện thông thường chỉ lọc những người *tự nhiên* có $$X=x$$ (nên bị trộn lẫn với các nguyên nhân chung dẫn họ đến $$X=x$$). Ngược lại, toán tử $$\mathrm{do}(X=x)$$ biểu diễn hành động cắt đứt mọi mũi tên đi vào $$X$$ và ép $$X=x$$ cho toàn bộ quần thể.
- **Ba nguyên tử đồ thị và quy tắc d-separation:** Mọi dòng thông tin thống kê trong một DAG đều truyền qua ba cấu trúc sơ cấp: **Fork** ($$X \leftarrow Z \rightarrow Y$$, mở sẵn và đóng khi điều chỉnh $$Z$$), **Chain** ($$X \rightarrow M \rightarrow Y$$, mở sẵn và đóng khi điều chỉnh $$M$$), và **Collider** ($$X \rightarrow C \leftarrow Y$$, đóng sẵn nhưng *mở ra* khi điều chỉnh $$C$$).
- **Công thức điều chỉnh đường cửa sau (Backdoor Adjustment):** Nếu tập biến $$Z$$ chặn mọi đường cửa sau giữa $$X$$ và $$Y$$ mà không chứa hậu duệ của $$X$$, ta tính được phân phối can thiệp thuần túy từ dữ liệu quan sát qua công thức trung bình trọng số:
  $$P(Y \mid \mathrm{do}(X=x)) = \sum_z P(Y \mid X=x, Z=z)\,P(Z=z).$$
## 1. Tương quan khác quan hệ nhân quả ở chỗ nào?

Trong dữ liệu thực tế, hai biến cùng tăng hoặc cùng giảm không đồng nghĩa với việc biến này gây ra biến kia. Ví dụ kinh điển là doanh số kem và số vụ đuối nước đều tăng vào mùa hè: kem không gây đuối nước, mà cả hai cùng chịu tác động từ một nguyên nhân chung là **thời tiết nóng**. Khi chỉ nhìn vào hệ số tương quan mà bỏ qua cấu trúc sinh dữ liệu phía sau, ta rất dễ nhầm lẫn tương quan thành nhân quả — và hiện tượng gây nhiễu (confounding) là nguyên nhân phổ biến nhất dẫn đến nhầm lẫn này.

## 2. Biến gây nhiễu (Confounder) là gì?

Một biến $$Z$$ được gọi là **biến gây nhiễu (confounder)** nếu nó tác động đồng thời lên biến can thiệp $$X$$ và biến kết quả $$Y$$, đồng thời không nằm trên con đường nhân quả đi từ $$X$$ đến $$Y$$.

- **Ví dụ 1 – Cà phê và bệnh tim:** Nếu quan sát thấy người uống nhiều cà phê có tỷ lệ mắc bệnh tim cao hơn, ta chưa thể vội kết luận cà phê gây bệnh tim. Nếu người chịu áp lực cao vừa uống nhiều cà phê hơn vừa có nguy cơ tim mạch cao hơn, thì **mức độ căng thẳng (stress)** là biến gây nhiễu.
- **Ví dụ 2 – Học thêm và điểm thi:** Nếu học sinh có học lực yếu thường đi học thêm nhiều hơn, trong khi điểm thi phụ thuộc mạnh vào năng lực ban đầu, thì **trình độ đầu vào** là biến gây nhiễu khi đánh giá hiệu quả của việc học thêm.

![Sơ đồ confounding tổng quan]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_confounding_dag_overview.png)

Điểm cốt lõi là biến gây nhiễu tạo ra một đường liên hệ phi nhân quả giữa $$X$$ và $$Y$$. Nếu không kiểm soát biến này, mô hình sẽ quy nhầm ảnh hưởng của nó thành tác động của $$X$$.

## 3. Đồ thị nhân quả DAG là gì?

**DAG** là viết tắt của *Directed Acyclic Graph* (đồ thị có hướng và không có chu trình): các mũi tên có hướng biểu diễn chiều tác động nhân quả giữa các biến và không tạo thành vòng lặp khép kín. DAG giúp trả lời trực tiếp câu hỏi thực hành trước khi chạy hồi quy:

> Với câu hỏi nhân quả đang xét, biến nào cần đưa vào mô hình để điều chỉnh và biến nào không nên đưa vào?

## 4. Ba cấu trúc cơ bản trong DAG

Hầu hết các sơ đồ nhân quả phức tạp đều được ghép từ ba cấu trúc nền tảng sau.

### 4.1. Cấu trúc chạc (Fork): nguyên nhân chung

$$
Z \rightarrow X,\quad Z \rightarrow Y
$$

Đây chính là cấu trúc của hiện tượng gây nhiễu. Ví dụ, độ tuổi ảnh hưởng đến cả mức độ tập luyện lẫn huyết áp. Khi muốn đo tác động của tập luyện lên huyết áp, ta **cần điều chỉnh cho độ tuổi** để đóng đường liên hệ phi nhân quả này.

![Cấu trúc fork: nguyên nhân chung gây confounding]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_fork_structure.png)

### 4.2. Cấu trúc chuỗi (Chain): biến trung gian (Mediator)

$$
X \rightarrow M \rightarrow Y
$$

Ở đây $$M$$ là **biến trung gian (mediator)** nằm trên chính con đường tác động từ $$X$$ đến $$Y$$. Chẳng hạn, tập luyện giúp giảm cân, và giảm cân giúp cải thiện đường huyết. Nếu mục tiêu là ước lượng **tổng hiệu ứng** (total effect) của tập luyện lên đường huyết, ta **không nên điều chỉnh cho cân nặng**, vì làm vậy sẽ chặn mất một phần tác động thực sự của tập luyện.

![Cấu trúc chain: mediator nằm trên đường tác động]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_chain_structure.png)

![Tổng quan mediation trong câu chuyện nhân quả]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_mediation_overview.png)

### 4.3. Cấu trúc hội tụ (Collider): hệ quả chung

$$
X \rightarrow C \leftarrow Y
$$

**Collider** là biến chịu tác động từ cả $$X$$ và $$Y$$. Khác với fork, đường qua collider vốn tự đóng; nhưng nếu ta điều kiện hóa (hoặc lọc dữ liệu) theo $$C$$, ta sẽ vô tình **mở đường** và tạo ra tương quan giả giữa $$X$$ và $$Y$$. Ví dụ, cả năng lực và may mắn đều ảnh hưởng đến khả năng trúng tuyển; trong toàn bộ dân số hai yếu tố này có thể độc lập, nhưng nếu chỉ xét riêng nhóm đã trúng tuyển, người kém may mắn hơn thường phải có năng lực cao hơn, tạo ra tương quan âm giả tạo.

![Cấu trúc collider: điều kiện hóa có thể mở ra tương quan giả]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_collider_structure.png)

![Tổng quan collider bias trong sơ đồ nhân quả]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_collider_bias_overview.png)

### Thử nghiệm: biến gây nhiễu làm lệch hệ số và điều chỉnh $$Z$$ khắc phục

Mô phỏng cấu trúc fork $$Z \rightarrow X, Z \rightarrow Y$$: so sánh ước lượng bỏ qua $$Z$$, phân tầng theo $$Z$$ (nghịch lý Simpson) và hồi quy có điều chỉnh $$Z$$.

<div class="interactive-demo" markdown="1">
<div data-demo="confound-explainer" data-lang="vi" data-tab="fork"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 5. Quy tắc thực hành: khi nào nên điều chỉnh một biến?

Nguyên tắc rút gọn cần ghi nhớ là: **nên điều chỉnh cho biến gây nhiễu (confounder)**, **không điều chỉnh cho biến trung gian (mediator)** nếu mục tiêu là tổng hiệu ứng, và **không điều chỉnh cho collider**. Tuy ngắn gọn, quy tắc này chỉ áp dụng chính xác khi ta đã phác thảo rõ cấu trúc nhân quả bằng DAG.

## 6. Nghịch lý Simpson (Simpson's Paradox)

![Minh họa nhanh Simpson's Paradox]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_paradox_overview.png)

![Dữ liệu gộp tạo ra kết luận sai về treatment]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_aggregate_bias.png)

![Tách theo severity cho thấy hiệu quả thật của treatment]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_stratified_effect.png)

**Nghịch lý Simpson** xảy ra khi một xu hướng xuất hiện rõ rệt trên dữ liệu gộp, nhưng lại đảo chiều hoàn toàn khi tách dữ liệu theo một biến phân tầng quan trọng. Trong ví dụ y khoa, nhìn gộp toàn bộ bệnh nhân thì điều trị tích cực có tỷ lệ hồi phục thấp hơn, nhưng khi tách riêng nhóm ca nặng và nhóm ca nhẹ thì điều trị tích cực đều cho kết quả tốt hơn ở cả hai nhóm. Nguyên nhân là nhóm điều trị tích cực tiếp nhận tỷ lệ ca nặng cao hơn nhiều, khiến biến "mức độ nặng" làm đảo ngược xu hướng khi gộp chung.

![DAG của Simpson's Paradox khi chưa điều chỉnh confounder]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_dag_unadjusted.png)

![DAG sau khi điều chỉnh severity để lộ causal effect]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_simpsons_dag_adjusted.png)

### 6.1. Bảng số minh họa nghịch lý Simpson

Giả sử bệnh viện so sánh hai phác đồ **điều trị tích cực** và **điều trị chuẩn** trên hai nhóm **ca nặng** và **ca nhẹ**:

| Nhóm bệnh nhân | Điều trị tích cực | Điều trị chuẩn |
|---|---:|---:|
| Ca nặng | 24/80 hồi phục = 30% | 6/30 hồi phục = 20% |
| Ca nhẹ | 54/60 hồi phục = 90% | 144/180 hồi phục = 80% |

Trong **cả hai nhóm**, điều trị tích cực đều có tỷ lệ hồi phục cao hơn 10 điểm phần trăm. Tuy nhiên, khi gộp chung toàn bộ bệnh nhân:

- Điều trị tích cực: $$78/140 \approx 55.7\%$$ hồi phục.
- Điều trị chuẩn: $$150/210 \approx 71.4\%$$ hồi phục.

Tỷ lệ gộp bị đảo ngược không phải vì phác đồ tích cực kém hiệu quả, mà vì phần lớn ca nặng được phân bổ vào nhóm này.

### Giải thích: Tính tay công thức Backdoor Adjustment trên bảng Nghịch lý Simpson

Ở mục 6.1, số liệu gộp cho thấy điều trị tích cực ($$X=1$$) chỉ đạt tỷ lệ hồi phục $$55.7\%$$, kém hơn điều trị chuẩn ($$X=0$$) ở mức $$71.4\%$$. Hãy dùng công thức Backdoor Adjustment với biến gây nhiễu mức độ nặng $$Z \in \{\text{nặng}, \text{nhẹ}\}$$ để tính hiệu quả **can thiệp thật sự**:

1. **Tính phân phối biên $$P(Z)$$ của toàn bộ $$N = 140 + 210 = 350$$ bệnh nhân:**
   - Tổng số ca nặng: $$80 + 30 = 110 \implies P(Z=\text{nặng}) = \frac{110}{350} = \frac{11}{35} \approx 31.43\%$$.
   - Tổng số ca nhẹ: $$60 + 180 = 240 \implies P(Z=\text{nhẹ}) = \frac{240}{350} = \frac{24}{35} \approx 68.57\%$$.
2. **Tính xác suất hồi phục nếu can thiệp cho MỌI bệnh nhân dùng điều trị tích cực ($$\mathrm{do}(X=1)$$):**
   $$P(Y=1 \mid \mathrm{do}(X=1)) = 0.30 \times \frac{11}{35} + 0.90 \times \frac{24}{35} = \frac{3.3 + 21.6}{35} = \frac{24.9}{35} \approx 71.14\%.$$
3. **Tính xác suất hồi phục nếu can thiệp cho MỌI bệnh nhân dùng điều trị chuẩn ($$\mathrm{do}(X=0)$$):**
   $$P(Y=1 \mid \mathrm{do}(X=0)) = 0.20 \times \frac{11}{35} + 0.80 \times \frac{24}{35} = \frac{2.2 + 19.2}{35} = \frac{21.4}{35} \approx 61.14\%.$$
4. **Kết luận nhân quả (Average Treatment Effect — ATE):**
   $$\text{ATE} = 71.14\% - 61.14\% = +10.0\%.$$

Chỉ bằng hai dòng cộng nhân, công thức Backdoor đã lật ngược hoàn toàn con số gộp gây hiểu lầm ($$-15.7\%$$) và trả về đúng lợi ích thật sự ($$+10\%$$) của phác đồ tích cực.

## 7. Đường cửa sau (Backdoor Path) là gì?

**Đường cửa sau (backdoor path)** là mọi đường nối phi nhân quả giữa biến can thiệp $$X$$ và biến kết quả $$Y$$ bắt đầu bằng một mũi tên đi vào $$X$$ (thông qua các nguyên nhân chung). Mục tiêu của việc điều chỉnh (adjustment) là chặn toàn bộ các đường cửa sau đang mở mà không chặn đường tác động nhân quả từ $$X$$ đến $$Y$$ và không vô tình mở ra đường sai mới.

Bốn hình dưới minh họa các tình huống điển hình: đường cửa sau đơn giản, nhiều đường cửa sau cần chặn cùng lúc, đường cửa sau vốn đã bị collider chặn sẵn và cấu trúc M-bias (nơi điều chỉnh nhầm một collider sẽ mở đường cửa sau).

![Ví dụ backdoor path đơn giản]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_backdoor_simple.png)

![Ví dụ có nhiều backdoor paths cần chặn cùng lúc]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_backdoor_multiple.png)

![Backdoor path bị collider chặn tự nhiên]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_backdoor_blocked_by_collider.png)

![M-bias: điều chỉnh sai có thể mở backdoor path]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_backdoor_m_bias.png)

Chẳng hạn, khi đánh giá tác động của học thêm ($$X$$) lên điểm thi ($$Y$$) với năng lực ban đầu ($$Z$$) tác động lên cả hai, đường $$X \leftarrow Z \rightarrow Y$$ là một đường cửa sau và sẽ được đóng lại khi ta điều chỉnh cho $$Z$$.

## 8. Tập biến điều chỉnh hợp lệ và sai lệch khi điều chỉnh nhầm

Bốn sơ đồ dưới đối chiếu sự khác biệt giữa tập điều chỉnh hợp lệ, tập điều chỉnh chặn nhầm biến trung gian (chỉ còn hiệu ứng trực tiếp), tập điều chỉnh nhầm collider và trường hợp không điều chỉnh.

![Adjustment set hợp lệ chặn các backdoor paths cần chặn]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_adjustment_valid_z1_z2.png)

![Adjustment set hợp lệ nhưng chỉ còn direct effect]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_adjustment_valid_but_mediator.png)

![Adjustment set sai vì điều chỉnh collider]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_adjustment_invalid_collider.png)

![Không điều chỉnh khiến backdoor paths vẫn mở]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_adjustment_invalid_none.png)

Một **tập điều chỉnh hợp lệ (valid adjustment set)** chặn được mọi đường cửa sau đang mở, không mở đường giả mới và không cắt ngang con đường tác động ta muốn đo. Vì vậy, mục tiêu không phải điều chỉnh càng nhiều biến càng tốt, mà là điều chỉnh **đúng biến**.

### Ví dụ thực tế

Trong nghiên cứu tác động của tập luyện lên sức khỏe tim mạch, `tuổi` và `thói quen ăn uống` có thể là biến gây nhiễu, `cân nặng hiện tại` có thể là biến trung gian, còn `số lần nhập viện` có thể là collider nếu nó vừa chịu ảnh hưởng của tình trạng tim mạch vừa liên quan đến mức độ theo dõi y tế. Khi mục tiêu là tổng hiệu ứng của tập luyện, ta cần điều chỉnh cho `tuổi` và `thói quen ăn uống`, tránh điều chỉnh cho `cân nặng hiện tại` và tuyệt đối không thêm `số lần nhập viện` chỉ vì biến này có sẵn trong tập dữ liệu.

## 9. Thiên lệch collider (Collider Bias): rủi ro của thói quen "kiểm soát mọi thứ"

![Trong dân số chung, hai nguyên nhân của collider có thể độc lập]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_collider_general_population.png)

![Khi condition lên collider, tương quan giả xuất hiện]({{ site.baseurl }}/img/chapter_img/chapter05/chapter05_collider_conditioned_sample.png)

Thiên lệch collider thường phát sinh khi phân tích chỉ giới hạn trên một tập mẫu đã qua chọn lọc hoặc khi đưa một hệ quả chung vào mô hình hồi quy. Trong ví dụ tuyển dụng, dù năng lực và may mắn độc lập ở dân số chung, việc chỉ quan sát nhóm trúng tuyển tạo ra tương quan âm giả giữa hai biến này. Bài học thực hành rất rõ: thêm biến vào mô hình không phải lúc nào cũng giúp ước lượng chính xác hơn.

### Thử nghiệm: điều kiện hóa theo collider tạo tương quan giả

$$X$$ và $$Y$$ độc lập nhưng cùng tác động vào $$C$$; chỉ cần lọc theo $$C$$ là hai biến xuất hiện tương quan âm giả.

<div class="interactive-demo" markdown="1">
<div data-demo="confound-explainer" data-lang="vi" data-tab="collider"></div>
</div>

## 10. Quy trình bốn bước khi làm việc với DAG

1. **Xác định rõ mục tiêu:** bạn muốn ước lượng tác động nhân quả của $$X$$ lên $$Y$$ hay chỉ dự đoán $$Y$$? Khi mục tiêu là nhân quả, việc vẽ DAG là bước bắt buộc.
2. **Liệt kê các biến liên quan:** xác định các yếu tố ảnh hưởng đến can thiệp, các yếu tố ảnh hưởng đến kết quả, các biến nằm giữa can thiệp và kết quả, cũng như các hệ quả chung.
3. **Vẽ mũi tên theo kiến thức chuyên môn:** tập trung thể hiện đúng giả định về chiều tác động thực tế trước khi chạy mô hình.
4. **Chọn tập điều chỉnh (adjustment set):** giữ các biến cần thiết để chặn đường cửa sau và loại trừ các biến trung gian hoặc collider không phù hợp với câu hỏi nghiên cứu.

## 11. Công cụ tương tác để tự luyện DAG

Bạn có thể sử dụng công cụ DAG Explorer của trang web để tự vẽ và kiểm tra các cấu trúc trong bài:

**[Mở Interactive DAG Explorer]({{ site.baseurl }}/tools/dag-explorer/standalone.html){:target="_blank"}**

Bạn nên thử vẽ ví dụ doanh số kem – đuối nước, ví dụ học thêm – điểm thi, ví dụ tập luyện – giảm cân – sức khỏe, rồi thử đảo chiều mũi tên để biến một confounder thành collider và quan sát sự thay đổi của tập điều chỉnh.

## 12. Tổng kết bài học

Hiện tượng gây nhiễu là vấn đề cốt lõi của mọi phân tích hướng đến nguyên nhân – kết quả. Nếu bỏ qua bước tư duy nhân quả, mô hình hồi quy vẫn có thể chạy hội tụ và cho khoảng hậu nghiệm rất hẹp, nhưng kết luận cuối cùng vẫn sai lệch hoàn toàn.

> **3 ý cần nhớ.** Biến gây nhiễu ảnh hưởng đồng thời tới cả biến can thiệp và biến kết quả nên cần được điều chỉnh để tránh ước lượng sai; DAG giúp tường minh hóa cấu trúc nhân quả trước khi chạy hồi quy; và nguyên tắc chọn biến là điều chỉnh đúng biến gây nhiễu, tránh kiểm soát tùy tiện biến trung gian hay collider.

## Video tham khảo

- [Statistical Rethinking 2023 - 05 - Elemental Confounds](https://www.youtube.com/watch?v=mBEA7PKDmiY) — Richard McElreath, English. **xem trước**. Biểu diễn các cấu trúc gây nhiễu cơ bản bằng đồ thị mũi tên, khớp với phần phân biệt tương quan và nhân quả trong bài.
- [Statistical Rethinking 2023 - 06 - Good & Bad Controls](https://www.youtube.com/watch?v=uanZZLlzKHw) — Richard McElreath, English. Phân tích các biến kiểm soát nên dùng và nên tránh, hỗ trợ quy tắc chọn biến điều chỉnh.
- [4.6 - The Backdoor Adjustment](https://www.youtube.com/watch?v=U1S8Rq8IcrY) — Brady Neal - Causal Inference, English. Trình bày tiêu chuẩn điều chỉnh đường cửa sau (backdoor adjustment), củng cố mục 7 và 8.

## Câu hỏi tự luyện

1. Trong nghiên cứu hiệu quả của việc học thêm lên điểm thi, những biến nào có thể đóng vai trò biến gây nhiễu?
2. Vì sao không phải lúc nào cũng nên điều chỉnh cho biến trung gian (mediator)?
3. Hãy nêu một ví dụ về collider trong đời sống hoặc công việc của bạn.
4. Nghịch lý Simpson nhắc nhở ta điều gì khi đọc số liệu gộp?
5. Hãy phác thảo một DAG đơn giản cho câu hỏi: "Tập thể dục có giúp ngủ ngon hơn không?"

## Tài liệu tham khảo

**Pearl, J. (2009).** *Causality: Models, Reasoning, and Inference* (2nd Edition). Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

**Hernan, M. A., & Robins, J. M. (2020).** *Causal Inference: What If*. Chapman & Hall/CRC.

---

*Bài học tiếp theo: [5.3 Multicollinearity]({{ site.baseurl }}/contents/vi/chapter05/05_03_multicollinearity/)*
