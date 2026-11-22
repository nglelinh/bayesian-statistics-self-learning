---
layout: post
title: "Bài 0.1: Nền tảng Xác suất - Ngôn ngữ của Sự Không chắc chắn"
chapter: '00'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu xác suất không chỉ là tập hợp các công thức tính toán mà là một ngôn ngữ toán học hoàn chỉnh để mô tả, định lượng và suy luận về sự không chắc chắn. Bạn sẽ nắm vững các khái niệm cơ bản về không gian mẫu, biến cố và các quy tắc xác suất, đồng thời thấy rõ vì sao chúng là nền tảng của suy diễn Bayesian. Quan trọng hơn, bạn sẽ tiếp cận xác suất như một cách mã hóa mức độ tin tưởng và cập nhật niềm tin đó khi có thêm thông tin mới.

## Giới thiệu: Tại sao chúng ta cần Xác suất?

Trong thực tế, chúng ta hiếm khi có thông tin hoàn hảo. Một bác sĩ chẩn đoán bệnh từ những triệu chứng chưa rõ ràng; một nhà khoa học tìm cách suy ra quy luật tự nhiên từ dữ liệu có nhiễu; một kỹ sư thiết kế hệ thống sao cho vẫn vận hành ổn định khi điều kiện môi trường biến động khó lường. Trong mọi tình huống như vậy, sự không chắc chắn không phải là phiền toái cần gạt bỏ, mà là đặc tính vốn có của bài toán cần được mô hình hóa và xử lý một cách có nguyên tắc.

Xác suất cung cấp ngôn ngữ toán học cho việc này. Nó cho phép chúng ta **định lượng mức độ tin tưởng** vào các mệnh đề khác nhau, kết hợp thông tin từ nhiều nguồn và đưa ra quyết định hợp lý ngay cả khi chưa biết chắc kết quả. **Trong khóa học phân tích dữ liệu Bayesian này, xác suất không chỉ là công cụ tính toán mà còn là cách tư duy về dữ liệu, mô hình và suy luận.**

Trước khi áp dụng xác suất vào suy diễn Bayesian, chúng ta cần nắm chắc các khái niệm nền tảng. Bài học này trình bày từng khái niệm cơ bản một cách hệ thống, giúp bạn vừa tính toán được xác suất vừa hiểu rõ ý nghĩa của các con số đó trong suy luận thống kê.

## Không gian Mẫu và Biến cố: Mô tả những gì có thể xảy ra

Mọi phân tích xác suất đều bắt đầu từ việc xác định rõ những kết quả nào có thể xảy ra. Tập hợp tất cả các kết quả có thể có của một thí nghiệm hay quá trình ngẫu nhiên được gọi là **không gian mẫu** (sample space), thường ký hiệu là $$\Omega$$. Mỗi phần tử của không gian mẫu biểu diễn một kết quả cụ thể, đầy đủ và phân biệt được với các kết quả khác.

Xét ví dụ đơn giản: tung một đồng xu công bằng. Không gian mẫu là $$\Omega = \{\text{Sấp}, \text{Ngửa}\}$$. Ở mỗi lần tung, ta quan sát được một trong hai mặt này và không có kết quả nào khác. Dù rất đơn giản, ví dụ này cho thấy một điểm cốt lõi: xác định đúng không gian mẫu luôn là bước đầu tiên và quan trọng nhất của mọi phân tích xác suất.

Trong thực tế, không gian mẫu thường phức tạp hơn nhiều. Nếu tung đồng xu hai lần, không gian mẫu là $$\Omega = \{SS, SN, NS, NN\}$$, trong đó $$S$$ là Sấp và $$N$$ là Ngửa. Nếu đo chiều cao của một người được chọn ngẫu nhiên, không gian mẫu là tập hợp các số thực dương có thể có (trong thực tế nằm trong giới hạn sinh học); đây là không gian liên tục chứ không phải rời rạc.

Khi đã có không gian mẫu, ta định nghĩa **biến cố** (event) là một tập hợp con của không gian mẫu, đại diện cho nhóm kết quả ta quan tâm. Ví dụ, khi tung đồng xu hai lần, biến cố "ít nhất một lần ra Sấp" là tập hợp $$\{SS, SN, NS\}$$, còn biến cố "cả hai lần đều ra Sấp" là tập hợp $$\{SS\}$$.

Định nghĩa biến cố như tập hợp con của không gian mẫu nghe có vẻ trừu tượng, nhưng nhờ đó ta có thể dùng lý thuyết tập hợp để suy luận về xác suất: hợp của hai biến cố (ít nhất một trong hai xảy ra), giao của hai biến cố (cả hai cùng xảy ra) và phần bù của một biến cố (biến cố đó không xảy ra). Các phép toán tập hợp này tương ứng trực tiếp với các quy tắc xác suất dưới đây.

## Định nghĩa Xác suất: Từ Tần suất đến Niềm tin

**Có nhiều cách hiểu về bản chất của xác suất**, và cách hiểu đó ảnh hưởng trực tiếp đến cách chúng ta áp dụng nó. Trong khóa học này, ta chủ yếu làm việc theo **quan điểm Bayesian**, nhưng trước hết hãy điểm qua **quan điểm tần suất (frequentist)** truyền thống để thấy rõ sự khác biệt.

Theo quan điểm tần suất, xác suất của một biến cố là tần suất tương đối mà biến cố đó xảy ra khi lặp lại thí nghiệm vô số lần trong điều kiện như nhau. Khi tung một đồng xu công bằng nhiều lần, tỷ lệ lần ra Sấp sẽ tiến gần đến $$0.5$$ khi số lần tung tăng lên. **Định nghĩa này khách quan và dễ hiểu, nhưng có một hạn chế lớn: nó chỉ áp dụng được cho những hiện tượng có thể lặp lại nhiều lần. Ta không thể nói về "xác suất ngày mai trời mưa" hay "xác suất một giả thuyết khoa học là đúng" theo nghĩa tần suất, vì những sự kiện này không thể lặp lại trong điều kiện giống hệt nhau.**

**Quan điểm Bayesian về xác suất** rộng và linh hoạt hơn. Theo cách hiểu này, xác suất là thước đo **mức độ tin tưởng** (degree of belief) hay **độ hợp lý** (plausibility) của một mệnh đề dựa trên thông tin hiện có. Xác suất bằng $$0$$ biểu thị sự chắc chắn rằng mệnh đề sai, xác suất bằng $$1$$ biểu thị sự chắc chắn rằng mệnh đề đúng, còn các giá trị nằm giữa phản ánh những mức độ không chắc chắn khác nhau. Quan trọng là **xác suất Bayesian thay đổi khi có thêm thông tin mới, và đây chính là nền tảng của suy diễn Bayesian.**

Dù hiểu xác suất theo quan điểm nào, nó vẫn phải tuân theo một số quy tắc toán học cơ bản để bảo đảm tính nhất quán. Các quy tắc này được gọi là các tiên đề xác suất (probability axioms) và là cơ sở của toàn bộ lý thuyết xác suất.

## Các Tiên đề Xác suất: Quy tắc của Trò chơi

Để xác suất trở thành một công cụ toán học chặt chẽ, nó phải thỏa mãn một số quy tắc nền tảng. Các quy tắc này do nhà toán học Nga Andrey Kolmogorov hệ thống hóa vào năm 1933, xác định những gì hợp lệ và không hợp lệ khi thao tác với xác suất.

**Tiên đề 1: Tính không âm (Non-negativity).** Xác suất của mọi biến cố đều không âm: với mọi biến cố $$A$$, ta có $$P(A) \geq 0$$. Về mặt trực giác, không thể tồn tại "xác suất âm"; xác suất bằng $$0$$ ứng với trường hợp biến cố chắc chắn không xảy ra.

**Tiên đề 2: Tính chuẩn hóa (Normalization).** Xác suất của toàn bộ không gian mẫu bằng $$1$$, tức $$P(\Omega) = 1$$. Điều này phản ánh thực tế rằng chắc chắn *một kết quả nào đó* trong không gian mẫu sẽ xảy ra, dù ta chưa biết cụ thể là kết quả nào.

**Tiên đề 3: Tính cộng (Additivity).** Nếu hai biến cố $$A$$ và $$B$$ **xung khắc** (mutually exclusive), tức không thể cùng xảy ra ($$A \cap B = \emptyset$$), thì xác suất của hợp hai biến cố bằng tổng các xác suất riêng lẻ: $$P(A \cup B) = P(A) + P(B)$$. Quy tắc này mở rộng cho mọi họ hữu hạn hoặc đếm được các biến cố đôi một xung khắc.

Ba tiên đề này tuy ngắn gọn nhưng tạo ra nhiều hệ quả quan trọng, từ đó suy ra toàn bộ các quy tắc tính xác suất khác. Chẳng hạn, xác suất của biến cố bù $$A^c$$ (biến cố $$A$$ không xảy ra) là $$P(A^c) = 1 - P(A)$$, vì $$A$$ và $$A^c$$ xung khắc và hợp của chúng là toàn bộ không gian mẫu, nên $$P(A) + P(A^c) = P(\Omega) = 1$$.

Một hệ quả quan trọng khác là **quy tắc cộng tổng quát** cho hai biến cố bất kỳ (không nhất thiết xung khắc):

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

Ta phải trừ đi $$P(A \cap B)$$ để tránh đếm hai lần những kết quả thuộc cả $$A$$ lẫn $$B$$. Công thức này tương ứng với nguyên lý bao hàm - loại trừ (inclusion-exclusion principle) trong lý thuyết tập hợp, thể hiện mối liên hệ chặt chẽ giữa xác suất và lý thuyết tập hợp.

## Xác suất Có điều kiện: Cập nhật Niềm tin với Thông tin Mới

Một trong những khái niệm trung tâm của lý thuyết xác suất — và đặc biệt quan trọng đối với suy diễn Bayesian — là **xác suất có điều kiện** (conditional probability). Đây là xác suất của một biến cố khi ta đã biết một biến cố khác xảy ra.

Giả sử ta quan tâm đến xác suất của biến cố $$A$$, nhưng đã biết biến cố $$B$$ xảy ra. Thông tin này làm thay đổi đánh giá của ta về khả năng xảy ra của $$A$$ như thế nào? Xác suất có điều kiện của $$A$$ khi biết $$B$$, ký hiệu là $$P(A \mid B)$$, được định nghĩa là:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$$

với điều kiện $$P(B) > 0$$.

Định nghĩa này có ý nghĩa trực quan rõ ràng. Khi biết $$B$$ đã xảy ra, không gian các kết quả có thể bị thu hẹp lại chỉ còn các phần tử thuộc $$B$$. Trong không gian thu hẹp đó, xác suất của $$A$$ tỷ lệ với xác suất cả $$A$$ và $$B$$ cùng xảy ra, rồi chia cho $$P(B)$$ để chuẩn hóa sao cho tổng xác suất trong không gian mới vẫn bằng $$1$$.

Xét một ví dụ cụ thể: tung một đồng xu công bằng hai lần. Không gian mẫu là $$\{SS, SN, NS, NN\}$$, mỗi kết quả có xác suất $$1/4$$. Xác suất của biến cố "cả hai lần đều ra Sấp" ($$A = \{SS\}$$) là $$P(A) = 1/4$$. Tuy nhiên, nếu biết thêm rằng "ít nhất một lần ra Sấp" ($$B = \{SS, SN, NS\}$$), xác suất có điều kiện của $$A$$ khi biết $$B$$ trở thành:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{P(\{SS\})}{P(\{SS, SN, NS\})} = \frac{1/4}{3/4} = \frac{1}{3}$$

Xác suất tăng từ $$1/4$$ lên $$1/3$$ khi có thêm thông tin. Đây là ví dụ đơn giản về việc cập nhật niềm tin theo bằng chứng mới — ý tưởng cốt lõi của suy diễn Bayesian.

### Một biến thể rất dễ nhầm

Vẫn với hai lần tung đồng xu, hãy so sánh hai điều kiện khác nhau:

- Nếu biết **ít nhất một lần ra Sấp**, xác suất cả hai lần đều Sấp là $$1/3$$.
- Nếu biết **lần tung đầu tiên ra Sấp**, xác suất cả hai lần đều Sấp là $$1/2$$.

Hai phát biểu nghe tương đối giống nhau, nhưng thông tin điều kiện khác nhau dẫn đến xác suất có điều kiện khác nhau. Điểm cần nhớ là trong xác suất, ý nghĩa của việc "biết thêm thông tin" phụ thuộc hoàn toàn vào việc biến cố điều kiện đã loại bỏ những khả năng nào khỏi không gian mẫu.

Từ định nghĩa xác suất có điều kiện, ta suy ra **quy tắc nhân** (multiplication rule):

$$P(A \cap B) = P(A \mid B) \cdot P(B) = P(B \mid A) \cdot P(A)$$

Quy tắc này cho hai cách tương đương để tính xác suất giao của hai biến cố, và chính sự tương đương này dẫn trực tiếp đến định lý Bayes.

## Độc lập: Khi Thông tin Không thay đổi Niềm tin

Hai biến cố $$A$$ và $$B$$ được gọi là **độc lập** (independent) nếu việc biết một biến cố xảy ra không làm thay đổi xác suất của biến cố kia. Một cách hình thức, $$A$$ và $$B$$ độc lập khi và chỉ khi:

$$P(A \mid B) = P(A)$$

hoặc tương đương:

$$P(A \cap B) = P(A) \cdot P(B)$$

Độc lập là một giả định mạnh và thường không hoàn toàn đúng ngoài thực tế, nhưng nó giúp đơn giản hóa đáng kể việc tính toán và làm nền tảng cho nhiều mô hình thống kê. Chẳng hạn, khi tung đồng xu nhiều lần, ta thường giả định các lần tung độc lập với nhau, tức kết quả của một lần tung không ảnh hưởng đến xác suất của các lần tung tiếp theo.

Ngược lại, nhiều tình huống thực tế không có tính độc lập. Nếu rút hai lá bài từ một bộ bài mà không hoàn lại, kết quả lần rút thứ hai phụ thuộc vào lần rút thứ nhất. Nếu quan sát nhiệt độ trong hai ngày liên tiếp, hai giá trị thường tương quan với nhau. Nhận diện và mô hình hóa các mối phụ thuộc như vậy là một phần quan trọng của phân tích dữ liệu Bayesian.

## Độc lập có điều kiện: Khi biết biến ẩn thì phụ thuộc biến mất

Có một tình huống tinh tế hơn độc lập thông thường: hai biến cố có thể **không độc lập khi xét tổng thể**, nhưng lại trở nên độc lập khi ta biết thêm một biến ẩn $$C$$. Ta nói $$A$$ và $$B$$ **độc lập có điều kiện theo $$C$$** nếu:

$$
P(A \cap B \mid C) = P(A \mid C)P(B \mid C).
$$

Về mặt trực giác, khi chưa biết $$C$$, ta đang gộp chung nhiều cơ chế sinh dữ liệu khác nhau vào cùng một bức tranh; khi đã biết $$C$$, ta xác định rõ mình đang ở cơ chế nào, và bên trong từng cơ chế riêng lẻ đó, $$A$$ và $$B$$ có thể không còn ảnh hưởng lẫn nhau nữa.

Ví dụ, giả sử ta chọn ngẫu nhiên một trong hai đồng xu: đồng xu thứ nhất công bằng, còn đồng xu thứ hai luôn ra Ngửa. Sau đó ta tung đồng xu đã chọn hai lần. Gọi $$C$$ là biến cố "đã chọn đồng xu 1", $$A$$ là biến cố "lần tung thứ nhất ra Ngửa", và $$B$$ là biến cố "lần tung thứ hai ra Ngửa". Nếu **biết trước đã chọn đồng xu nào**, hai lần tung là độc lập có điều kiện: với đồng xu công bằng, mỗi lần tung độc lập với xác suất ra Ngửa bằng $$1/2$$; với đồng xu luôn ra Ngửa, hai lần tung vẫn độc lập theo nghĩa cả hai đều chắc chắn ra Ngửa. Nhưng nếu **không biết** đã chọn đồng xu nào, $$A$$ và $$B$$ không còn độc lập theo nghĩa thông thường, vì kết quả lần tung đầu tiết lộ thông tin về loại đồng xu đang dùng và từ đó làm thay đổi đánh giá về lần tung thứ hai.

Đây là một ý tưởng quan trọng trong thống kê Bayesian: sự phụ thuộc không nhất thiết xuất phát từ việc hai biến tác động trực tiếp lên nhau; đôi khi nó chỉ xuất hiện vì ta chưa biết một biến ẩn đang đồng thời chi phối cả hai. Bạn sẽ gặp lại cơ chế này thường xuyên khi học mô hình hỗn hợp, mô hình phân cấp và đồ thị nhân quả.

## Quy tắc Xác suất Toàn phần: Chia để Tính

Đôi khi cách thuận tiện nhất để tính xác suất của một biến cố là tách bài toán thành các trường hợp đơn giản hơn. **Quy tắc xác suất toàn phần** (law of total probability) cho phép thực hiện việc này một cách có hệ thống.

Giả sử không gian mẫu được phân hoạch thành các biến cố đôi một xung khắc $$B_1, B_2, \ldots, B_n$$ sao cho $$\bigcup_{i=1}^n B_i = \Omega$$, nghĩa là mỗi kết quả có thể thuộc về đúng một biến cố $$B_i$$. Khi đó, xác suất của một biến cố $$A$$ bất kỳ được tính bằng:

$$P(A) = \sum_{i=1}^n P(A \mid B_i) \cdot P(B_i)$$

Công thức này cho biết để tính $$P(A)$$, ta xét từng trường hợp $$B_i$$, lấy xác suất của $$A$$ trong trường hợp đó ($$P(A \mid B_i)$$) nhân với xác suất xảy ra trường hợp đó ($$P(B_i)$$), rồi cộng toàn bộ lại.

Quy tắc này đặc biệt hữu ích trong các mô hình phân cấp có **biến tiềm ẩn (latent variables)** không quan sát trực tiếp được. Trong suy diễn Bayesian, ta thường dùng quy tắc xác suất toàn phần để biên hóa (marginalize) — tức lấy tổng hoặc tích phân nhằm loại bỏ các tham số không trực tiếp quan tâm và tập trung vào đại lượng cần suy luận.

## Ý nghĩa cho Suy diễn Bayesian

Các khái niệm trong bài học này không chỉ là phần mở đầu lý thuyết mà là khung xương trực tiếp của phân tích dữ liệu Bayesian. **Trong suy diễn Bayesian, ta dùng xác suất có điều kiện để cập nhật niềm tin về tham số mô hình khi quan sát dữ liệu, dùng quy tắc xác suất toàn phần để biên hóa các tham số phiền nhiễu (nuisance parameters), và dựa vào các tiên đề xác suất để bảo đảm mọi suy luận đều nhất quán.**

Hơn nữa, việc nhìn nhận xác suất như **mức độ tin tưởng** cho phép ta phát biểu trực tiếp về "xác suất của một giả thuyết" hay "xác suất của một giá trị tham số" — những phát biểu không hợp lệ trong khuôn khổ tần suất nhưng lại tự nhiên và hữu ích trong thống kê Bayesian.

Trong các bài học tiếp theo, mọi công cụ Bayesian — từ định lý Bayes cơ bản đến các mô hình phân cấp phức tạp — đều được xây dựng từ những nguyên tắc này. Nắm chắc nền tảng ngay từ đầu sẽ giúp bạn áp dụng phương pháp đúng chỗ, đồng thời hiểu rõ vì sao một mô hình hoạt động tốt hoặc gặp hạn chế.

## Video tham khảo

- [The Main Ideas behind Probability Distributions](https://www.youtube.com/watch?v=oI3hZJqXJuc) — StatQuest with Josh Starmer, English. **Xem trước.** Giúp hình dung phân phối xác suất như cách biểu diễn mức độ chắc chắn, khớp với phần mở đầu của bài.
- [Conditional Probabilities, Clearly Explained!!!](https://www.youtube.com/watch?v=_IgyaD7vOOA) — StatQuest with Josh Starmer, English. Trình bày trực quan về xác suất có điều kiện, phép tính nền tảng để cập nhật suy luận khi có thông tin mới.
- [Random variables | Probability and Statistics | Khan Academy](https://www.youtube.com/watch?v=3v9w79NhsfI) — Khan Academy, English. Giới thiệu cách định nghĩa biến ngẫu nhiên, hỗ trợ phân biệt kết quả quan sát với đại lượng chưa biết.

## Bài tập

**Bài tập 1: Xác suất Cơ bản.** Một hộp chứa 5 viên bi đỏ, 3 viên bi xanh và 2 viên bi vàng. Rút ngẫu nhiên một viên bi. (a) Xác định không gian mẫu. (b) Tính xác suất rút được viên bi đỏ. (c) Tính xác suất rút được viên bi không phải màu vàng. Giải thích lập luận bằng lời, không chỉ ghi công thức.

**Bài tập 2: Xác suất Có điều kiện.** Trong một lớp học, 60% sinh viên học Python, 40% học R và 25% học cả hai. (a) Nếu chọn ngẫu nhiên một sinh viên và biết người đó học Python, xác suất người đó cũng học R là bao nhiêu? (b) Hai biến cố "học Python" và "học R" có độc lập không? Giải thích bằng cả tính toán và trực giác.

**Bài tập 3: Quy tắc Xác suất Toàn phần.** Một công ty sản xuất sản phẩm tại ba nhà máy A, B và C với tỷ lệ sản lượng lần lượt là 50%, 30% và 20%. Tỷ lệ sản phẩm lỗi của mỗi nhà máy lần lượt là 2%, 3% và 5%. (a) Tính xác suất một sản phẩm chọn ngẫu nhiên bị lỗi. (b) Nếu một sản phẩm được phát hiện bị lỗi, xác suất nó đến từ nhà máy C là bao nhiêu? (Gợi ý: phần (b) liên quan đến định lý Bayes sẽ học ở bài sau, nhưng bạn có thể thử suy luận trước bằng xác suất có điều kiện.)

**Bài tập 4: Nghịch lý Simpson.** Xét hai phương pháp điều trị A và B được thử nghiệm trên hai nhóm bệnh nhân: nhóm bệnh nhẹ và nhóm bệnh nặng. Trong nhóm bệnh nhẹ, A thành công 90/100 ca và B thành công 85/90 ca. Trong nhóm bệnh nặng, A thành công 20/100 ca và B thành công 24/110 ca. (a) Trong mỗi nhóm, phương pháp nào có tỷ lệ thành công cao hơn? (b) Tính tỷ lệ thành công tổng thể của mỗi phương pháp. (c) Giải thích vì sao kết quả có vẻ nghịch lý và điều này cho thấy gì về vai trò của các biến tiềm ẩn.

**Bài tập 5: Suy ngẫm về Xác suất.** Viết một đoạn văn ngắn (200–300 từ) giải thích sự khác biệt giữa quan điểm tần suất và quan điểm Bayesian về xác suất. Nêu một ví dụ mà quan điểm Bayesian tỏ ra tự nhiên hơn và giải thích lý do. Phân tích ngắn gọn cách hiểu về xác suất ảnh hưởng ra sao đến việc thiết kế thí nghiệm và diễn giải kết quả.

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 1: Probability and inference
- Appendix A: Standard probability distributions

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 4: What is This Stuff Called Probability?

### Supplementary Reading:

**Jaynes, E. T. (2003).** *Probability Theory: The Logic of Science*. Cambridge University Press.
- Chapters 1-2: Plausible reasoning and quantitative rules

---

*Bài học tiếp theo: [0.2 Bernoulli và Binomial]({{ site.baseurl }}/contents/vi/chapter00/00_02_01_bernoulli_binomial/)*
