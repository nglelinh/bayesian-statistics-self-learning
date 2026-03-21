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

## Mục tiêu học tập

Sau bài này, bạn cần hiểu confounding (hiện tượng gây nhiễu) là gì và vì sao nó làm ta đọc sai dữ liệu. Bạn cũng cần biết DAG là công cụ để suy nghĩ về quan hệ nhân quả, từ đó quyết định khi nào nên điều chỉnh một biến và khi nào không nên. Đây là nền móng của causal inference (suy luận nhân quả).

> **Ví dụ mini.** Một bệnh viện thấy rằng bệnh nhân được điều trị mạnh hơn lại có tỷ lệ hồi phục thấp hơn. Kết luận "điều trị mạnh làm mọi chuyện tệ hơn" nghe rất hợp lý, nhưng có thể hoàn toàn sai nếu các ca nặng vốn dĩ đã được điều trị mạnh hơn. Mức độ nặng của bệnh lúc nhập viện có thể là biến gây nhiễu.
>
> **Câu hỏi tự kiểm tra.** Nếu một biến ảnh hưởng đồng thời tới cả treatment (can thiệp) và outcome (kết quả), chuyện gì có thể xảy ra nếu ta bỏ qua nó?

## 1. Correlation khác causation ở chỗ nào?

Trong dữ liệu thực tế, hai biến đi cùng nhau chưa chắc đã có quan hệ nhân quả trực tiếp.

Ví dụ rất nổi tiếng là doanh số kem tăng vào mùa hè, còn số vụ đuối nước cũng tăng vào mùa hè. Điều đó không có nghĩa kem gây đuối nước; cả hai cùng tăng vì **thời tiết nóng**. Vấn đề ở đây là ta nhìn thấy một tương quan, nhưng lại không nhìn thấy cấu trúc tạo ra tương quan đó.

Confounding chính là một trong những lý do phổ biến nhất khiến ta nhầm từ tương quan sang nhân quả.

## 2. Confounder là gì?

Một biến được gọi là **confounder** (biến gây nhiễu) nếu nó ảnh hưởng đến predictor hay treatment $$X$$, đồng thời ảnh hưởng đến outcome $$Y$$, nhưng lại không nằm trên con đường nhân quả từ $$X$$ đến $$Y$$.

### Ví dụ 1: cà phê và bệnh tim

Giả sử ta quan sát thấy người uống nhiều cà phê có nguy cơ bệnh tim cao hơn. Có thể ta vội kết luận cà phê là thủ phạm. Nhưng nếu những người căng thẳng hơn vừa uống nhiều cà phê hơn vừa có nguy cơ tim mạch cao hơn, thì **stress** có thể là confounder.

### Ví dụ 2: học thêm và điểm thi

Nếu học sinh yếu thường đi học thêm nhiều hơn, còn kết quả thi lại phụ thuộc mạnh vào năng lực ban đầu, thì **trình độ đầu vào** là một confounder khi ta nghiên cứu hiệu quả của học thêm.

![Confounding DAGs]({{ site.baseurl }}/img/chapter_img/chapter05/confounding_dags.png)

Điểm mấu chốt là confounding tạo ra một đường liên hệ phụ giữa $$X$$ và $$Y$$. Nếu không xử lý, ta dễ quy nhầm ảnh hưởng của confounder thành ảnh hưởng của treatment.

## 3. DAG là gì và vì sao nó hữu ích?

**DAG** là viết tắt của *Directed Acyclic Graph*, có thể hiểu là đồ thị có hướng và không có chu trình. Nói cụ thể hơn, *Directed* nghĩa là các mũi tên có hướng, *Acyclic* nghĩa là không có vòng lặp khép kín, còn *Graph* nghĩa là một sơ đồ biểu diễn quan hệ giữa các biến.

DAG giúp ta trả lời một câu rất thực tế:

> Trong câu hỏi nhân quả này, biến nào nên đưa vào mô hình, biến nào không nên?

Thay vì lao ngay vào chạy hồi quy, ta vẽ câu chuyện trước.

## 4. Ba cấu trúc cơ bản cần nhớ

![Causal basic structures]({{ site.baseurl }}/img/chapter_img/chapter05/causal_basic_structures.png)

Hầu hết DAG phức tạp đều được ghép từ ba cấu trúc cơ bản sau.

### 4.1. Fork: nguyên nhân chung

$$
Z \rightarrow X,\quad Z \rightarrow Y
$$

Đây là cấu trúc của confounding.

Ví dụ, tuổi ảnh hưởng đến mức độ tập luyện và đồng thời cũng ảnh hưởng đến huyết áp. Nếu đang muốn nghiên cứu tập luyện ảnh hưởng thế nào đến huyết áp, **tuổi** là biến nên điều chỉnh.

### 4.2. Chain: biến trung gian

$$
X \rightarrow M \rightarrow Y
$$

Đây là mediator (biến trung gian). Ví dụ, tập luyện làm giảm cân, còn giảm cân lại giúp cải thiện đường huyết.

Nếu ta muốn đo **tổng hiệu quả** của tập luyện lên đường huyết, không nên điều chỉnh cho cân nặng, vì như vậy ta chặn mất một phần đường tác động thật.

### 4.3. Collider: hai mũi tên cùng chụm vào một điểm

$$
X \rightarrow C \leftarrow Y
$$

Collider rất nguy hiểm vì khi ta điều kiện hóa lên nó, ta có thể tạo ra tương quan giả.

Ví dụ, năng lực và may mắn đều ảnh hưởng đến việc được tuyển dụng; nếu chỉ nhìn nhóm đã được tuyển, ta có thể thấy người "ít may mắn" lại thường "rất giỏi" và ngược lại.

Đó không phải quy luật thật của toàn bộ dân số, mà là hệ quả của việc chỉ nhìn vào collider.

## 5. Quy tắc thực hành: nên control hay không?

Một bản nhớ ngắn gọn là: **nên control cho confounders**, **không nên control cho mediators nếu mục tiêu là total effect (tổng hiệu ứng)**, và **không nên control cho colliders**. Quy tắc này nghe đơn giản, nhưng muốn áp dụng đúng thì phải có sơ đồ nhân quả đủ rõ.

## 6. Simpson's Paradox: ví dụ khiến nhiều người đổi cách nghĩ

![Simpson's paradox]({{ site.baseurl }}/img/chapter_img/chapter05/simpsons_paradox.png)

Simpson's Paradox xảy ra khi nhìn toàn bộ dữ liệu thì một xu hướng xuất hiện, nhưng khi tách theo nhóm quan trọng thì xu hướng ấy lại đảo chiều. Ví dụ trong y khoa, nhìn tổng thể thì nhóm điều trị tích cực có vẻ hồi phục kém hơn, nhưng khi tách bệnh nhân theo mức độ nặng nhẹ, trong từng nhóm mức độ bệnh thì điều trị tích cực lại tốt hơn. Nguyên nhân là vì các ca nặng được điều trị mạnh hơn, trong khi chính các ca nặng ấy vốn cũng khó hồi phục hơn.

Biến "mức độ nặng" đã làm méo quan hệ treatment-outcome khi bị bỏ qua.

![Simpson's paradox DAG]({{ site.baseurl }}/img/chapter_img/chapter05/simpsons_paradox_dag.png)

Đây là một ví dụ rất tốt để tự nhắc mình rằng:

> dữ liệu tổng hợp có thể kể một câu chuyện sai nếu ta không tách đúng cấu trúc.

## 7. Backdoor path là gì?

Một **backdoor path** có thể được hiểu là con đường phi nhân quả nối từ treatment $$X$$ tới outcome $$Y$$ thông qua các nguyên nhân chung. Mục tiêu của adjustment (điều chỉnh) là chặn các backdoor paths cần chặn, nhưng không chặn đường tác động nhân quả thật từ $$X$$ đến $$Y$$.

![Backdoor paths examples]({{ site.baseurl }}/img/chapter_img/chapter05/backdoor_paths_examples.png)

Ví dụ, nếu ta muốn biết học thêm $$X$$ ảnh hưởng thế nào tới điểm thi $$Y$$, trong khi năng lực ban đầu $$Z$$ ảnh hưởng cả việc đi học thêm lẫn điểm thi, thì đường $$X \leftarrow Z \rightarrow Y$$ chính là backdoor path. Điều chỉnh cho $$Z$$ sẽ giúp chặn đường này.

## 8. Điều chỉnh đủ và điều chỉnh sai khác nhau thế nào?

![Adjustment sets comparison]({{ site.baseurl }}/img/chapter_img/chapter05/adjustment_sets_comparison.png)

Một **adjustment set hợp lệ** là tập biến giúp chặn tất cả backdoor paths cần chặn, không mở ra các đường sai mới, và không vô tình chặn mất phần hiệu quả mà ta đang muốn đo. Vì thế, ta không cần điều chỉnh "càng nhiều càng tốt"; điều quan trọng là phải điều chỉnh **đúng biến**.

### Ví dụ thực tế

Trong một nghiên cứu về tác động của tập luyện lên sức khỏe tim mạch, **tuổi** và **thói quen ăn uống** có thể là confounders, **cân nặng hiện tại** có thể là mediator, còn **số lần nhập viện** có thể là collider nếu nó vừa chịu ảnh hưởng của sức khỏe vừa liên quan tới khả năng được theo dõi y tế. Nếu ta nhét tất cả vào một mô hình mà không suy nghĩ, ta rất dễ tự tạo bias (thiên lệch).

## 9. Collider bias: lỗi rất thường gặp khi "control cho mọi thứ"

![Collider bias Berkson]({{ site.baseurl }}/img/chapter_img/chapter05/collider_bias_berkson.png)

Collider bias thường xuất hiện khi ta chỉ nhìn một nhóm đã được chọn lọc.

Ví dụ, năng lực và may mắn đều ảnh hưởng đến việc đỗ vào một công ty cạnh tranh cao. Trong dân số chung, năng lực và may mắn có thể không liên quan, nhưng trong nhóm đã trúng tuyển, người kém may mắn hơn thường phải giỏi hơn để vẫn đỗ.

Kết quả là ta nhìn thấy một tương quan âm giả giữa năng lực và may mắn trong nhóm được chọn.

Bài học rất quan trọng:

> Không phải thêm biến nào vào mô hình cũng làm phân tích tốt hơn.

## 10. Một quy trình DAG rất thực tế

Khi gặp một câu hỏi nhân quả, bạn có thể đi theo bốn bước tương đối thực dụng sau.

### Bước 1. Xác định câu hỏi

Trước hết, hãy xác định xem bạn đang hỏi về ảnh hưởng của $$X$$ lên $$Y$$, hay chỉ đơn giản muốn dự đoán $$Y$$. Nếu mục tiêu là nhân quả, DAG trở nên đặc biệt quan trọng.

### Bước 2. Liệt kê các biến liên quan

Ở bước liệt kê biến, hãy nghĩ bằng ngôn ngữ đời thường: điều gì ảnh hưởng đến treatment, điều gì ảnh hưởng đến outcome, điều gì nằm ở giữa treatment và outcome, và điều gì là kết quả chung của hai thứ khác nhau.

### Bước 3. Vẽ mũi tên theo câu chuyện thực tế

Không cần vẽ đẹp ngay từ đầu. Điều quan trọng là vẽ đúng trực giác chuyên môn.

### Bước 4. Quyết định adjustment set

Ở bước cuối, hãy tự hỏi biến nào cần điều chỉnh để chặn backdoor paths, và biến nào không được điều chỉnh vì thực chất là mediator hoặc collider.

## 11. Công cụ tương tác để tự luyện DAG

Bạn có thể dùng công cụ DAG Explorer của website để tự vẽ các tình huống trong bài:

**[Mở Interactive DAG Explorer]({{ site.baseurl }}/tools/dag-explorer/standalone.html){:target="_blank"}**

Gợi ý nên thử là vẽ ví dụ kem và đuối nước, ví dụ học thêm và điểm thi, ví dụ exercise - weight loss - health, rồi thử đổi một biến từ confounder thành collider để xem logic thay đổi ra sao.

## 12. Điều quan trọng nhất của bài này

Confounding không phải là lỗi kỹ thuật nhỏ. Nó là vấn đề trung tâm của mọi phân tích muốn bàn đến nguyên nhân.

Nếu không suy nghĩ nhân quả trước, hồi quy có thể chạy rất đẹp, interval có thể trông rất thuyết phục, nhưng câu kết luận cuối cùng vẫn sai.

> **3 ý cần nhớ.** Confounder là biến ảnh hưởng đồng thời tới treatment và outcome, nên nếu bỏ qua nó ta dễ ước lượng sai hiệu quả mình quan tâm; DAG là công cụ để vẽ cấu trúc nhân quả trước khi chạy mô hình, nhờ đó quyết định biến nào nên và không nên điều chỉnh; và không nên "control cho mọi thứ", vì confounders thường cần điều chỉnh, còn mediators và colliders thì phải xử lý cẩn thận tùy câu hỏi.

## Câu hỏi tự luyện

1. Trong nghiên cứu hiệu quả học thêm lên điểm thi, biến nào có thể là confounder?
2. Vì sao mediator không nên luôn luôn bị control?
3. Hãy nghĩ ra một ví dụ collider trong đời sống hoặc công việc của bạn.
4. Simpson's Paradox dạy ta điều gì về việc đọc dữ liệu gộp?
5. Hãy thử vẽ một DAG đơn giản cho câu hỏi: "Tập thể dục có giúp ngủ ngon hơn không?"

## Tài liệu tham khảo

**Pearl, J. (2009).** *Causality: Models, Reasoning, and Inference* (2nd Edition). Cambridge University Press.

**McElreath, R. (2020).** *Statistical Rethinking* (2nd Edition). CRC Press.

**Hernan, M. A., & Robins, J. M. (2020).** *Causal Inference: What If*. Chapman & Hall/CRC.

---

*Bài học tiếp theo: [5.3 Multicollinearity](/vi/chapter05/multicollinearity/)*
