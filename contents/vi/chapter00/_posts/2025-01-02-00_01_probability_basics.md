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

Sau khi hoàn thành bài học này, bạn sẽ hiểu xác suất không chỉ là một tập hợp các công thức tính toán, mà là một ngôn ngữ toán học hoàn chỉnh để mô tả, định lượng, và suy luận về sự không chắc chắn. Bạn sẽ nắm vững các khái niệm cơ bản về không gian mẫu, biến cố, và các quy tắc xác suất, đồng thời hiểu được tại sao những khái niệm này lại là nền tảng không thể thiếu cho suy diễn Bayesian. Quan trọng hơn, bạn sẽ bắt đầu nhìn nhận xác suất như một cách để mã hóa niềm tin và cập nhật niềm tin đó khi có thêm thông tin mới.

## Giới thiệu: Tại sao chúng ta cần Xác suất?

Trong thế giới thực, chúng ta hiếm khi có thông tin hoàn hảo. Một bác sĩ chẩn đoán bệnh dựa trên các triệu chứng không rõ ràng. Một nhà khoa học cố gắng suy ra quy luật tự nhiên từ dữ liệu nhiễu. Một kỹ sư thiết kế hệ thống phải hoạt động tốt ngay cả khi điều kiện môi trường thay đổi không lường trước được. Trong tất cả những tình huống này, sự không chắc chắn không phải là một phiền toái cần loại bỏ, mà là một đặc điểm cơ bản của vấn đề cần được mô hình hóa và quản lý một cách có nguyên tắc.

Xác suất cung cấp cho chúng ta ngôn ngữ toán học để làm điều này. Nó cho phép chúng ta **định lượng mức độ tin tưởng** vào các mệnh đề khác nhau, kết hợp thông tin từ nhiều nguồn, và đưa ra quyết định hợp lý ngay cả khi chúng ta không thể chắc chắn về kết quả. **Trong khóa học này về phân tích dữ liệu Bayesian, xác suất không chỉ là công cụ tính toán mà còn là cách chúng ta tư duy về dữ liệu, mô hình, và suy luận.**

Trước khi chúng ta có thể sử dụng xác suất để suy diễn Bayesian, chúng ta cần hiểu rõ nền tảng của nó. Bài học này sẽ xây dựng các khái niệm cơ bản một cách cẩn thận, không chỉ để bạn có thể tính toán xác suất, mà còn để bạn hiểu được ý nghĩa của những con số đó và cách chúng liên kết với suy luận thống kê.

## Không gian Mẫu và Biến cố: Mô tả những gì có thể xảy ra

Mọi phân tích xác suất bắt đầu bằng việc xác định rõ ràng những gì có thể xảy ra. Chúng ta gọi tập hợp tất cả các kết quả có thể xảy ra của một thí nghiệm hoặc quá trình ngẫu nhiên là **không gian mẫu** (sample space), thường được ký hiệu là $$\Omega$$. Mỗi phần tử trong không gian mẫu đại diện cho một kết quả cụ thể, hoàn chỉnh, và có thể phân biệt được.

Hãy xem xét một ví dụ đơn giản: toss một đồng xu công bằng. Không gian mẫu ở đây là $$\Omega = \{\text{Sấp}, \text{Ngửa}\}$$. Mỗi lần toss, chúng ta quan sát được một trong hai kết quả này, và không có kết quả nào khác có thể xảy ra. Tính đơn giản của ví dụ này không nên che lấp tầm quan trọng của nó: việc xác định chính xác không gian mẫu là bước đầu tiên và quan trọng nhất trong mọi phân tích xác suất.

Trong nhiều tình huống thực tế, không gian mẫu có thể phức tạp hơn nhiều. Nếu chúng ta toss đồng xu hai lần, không gian mẫu trở thành $$\Omega = \{SS, SN, NS, NN\}$$, trong đó $$S$$ là Sấp và $$N$$ là Ngửa. Nếu chúng ta đo chiều cao của một người được chọn ngẫu nhiên, không gian mẫu là tập hợp tất cả các giá trị dương có thể (trong thực tế, bị giới hạn bởi các ràng buộc sinh học), và đây là một không gian liên tục chứ không phải rời rạc.

Một khi chúng ta đã xác định không gian mẫu, chúng ta có thể nói về các **biến cố** (events). Một biến cố là một tập hợp con của không gian mẫu, đại diện cho một tập hợp các kết quả mà chúng ta quan tâm. Ví dụ, trong thí nghiệm toss đồng xu hai lần, biến cố "ít nhất một lần ra Sấp" tương ứng với tập hợp $$\{SS, SN, NS\}$$. Biến cố "cả hai lần đều ra Sấp" tương ứng với tập hợp $$\{SS\}$$.

Việc định nghĩa biến cố như tập hợp con của không gian mẫu có vẻ trừu tượng, nhưng nó cho phép chúng ta sử dụng lý thuyết tập hợp để suy luận về xác suất. Chúng ta có thể nói về hợp của hai biến cố (ít nhất một trong hai xảy ra), giao của hai biến cố (cả hai cùng xảy ra), và phần bù của một biến cố (biến cố đó không xảy ra). Những phép toán này sẽ tương ứng trực tiếp với các quy tắc xác suất mà chúng ta sẽ thảo luận tiếp theo.

## Định nghĩa Xác suất: Từ Tần suất đến Niềm tin

**Có nhiều cách để hiểu xác suất là gì**, và cách chúng ta hiểu nó sẽ ảnh hưởng sâu sắc đến cách chúng ta sử dụng nó. Trong khóa học này, chúng ta sẽ chủ yếu làm việc với **quan điểm Bayesian về xác suất**, nhưng trước tiên hãy xem xét **quan điểm tần suất (frequentist)** truyền thống để hiểu sự khác biệt.

Theo quan điểm tần suất, xác suất của một biến cố được định nghĩa là tần suất tương đối mà biến cố đó xảy ra khi chúng ta lặp lại thí nghiệm vô số lần. Nếu chúng ta toss một đồng xu công bằng nhiều lần, tỷ lệ lần ra Sấp sẽ tiến gần đến $$0.5$$ khi số lần toss tăng lên. **Đây là một định nghĩa khách quan và dễ hiểu, nhưng nó có một hạn chế quan trọng: nó chỉ có ý nghĩa cho các sự kiện có thể lặp lại nhiều lần. Chúng ta không thể nói về "xác suất mưa ngày mai" hoặc "xác suất một giả thuyết khoa học là đúng" theo nghĩa tần suất, vì những sự kiện này không thể lặp lại trong điều kiện giống hệt nhau.**

**Quan điểm Bayesian về xác suất** rộng hơn và linh hoạt hơn. Trong quan điểm này, xác suất là một thước đo **mức độ tin tưởng** (degree of belief) hoặc **độ hợp lý** (plausibility) của một mệnh đề, dựa trên thông tin hiện có. Xác suất $$0$$ có nghĩa là chúng ta hoàn toàn chắc chắn rằng mệnh đề là sai, xác suất $$1$$ có nghĩa là chúng ta hoàn toàn chắc chắn rằng nó đúng, và các giá trị ở giữa thể hiện các mức độ không chắc chắn khác nhau. Quan trọng là, **xác suất Bayesian có thể thay đổi khi chúng ta thu thập thêm thông tin, và đây chính là cơ sở của suy diễn Bayesian.**

Dù chúng ta hiểu xác suất theo cách nào, nó phải tuân theo một số quy tắc toán học cơ bản để đảm bảo tính nhất quán. Những quy tắc này, được gọi là các tiên đề xác suất (probability axioms), là nền tảng của toàn bộ lý thuyết xác suất.

## Các Tiên đề Xác suất: Quy tắc của Trò chơi

Để xác suất là một công cụ toán học hữu ích, nó phải tuân theo một số quy tắc cơ bản. Các quy tắc này, được nhà toán học Nga Andrey Kolmogorov hình thức hóa vào năm 1933, định nghĩa những gì chúng ta có thể và không thể làm với xác suất.

**Tiên đề 1: Không âm (Non-negativity).** Xác suất của bất kỳ biến cố nào đều không âm. Với mọi biến cố $$A$$, chúng ta có $$P(A) \geq 0$$. Điều này có ý nghĩa trực quan: chúng ta không thể có "xác suất âm" cho một sự kiện. Xác suất bằng không có nghĩa là sự kiện chắc chắn không xảy ra.

**Tiên đề 2: Chuẩn hóa (Normalization).** Xác suất của toàn bộ không gian mẫu là $$1$$. Nói cách khác, $$P(\Omega) = 1$$. Điều này phản ánh thực tế là một trong các kết quả có thể phải xảy ra. Chúng ta hoàn toàn chắc chắn rằng *một cái gì đó* sẽ xảy ra, ngay cả khi chúng ta không chắc chắn *cái gì* sẽ xảy ra.

**Tiên đề 3: Tính cộng (Additivity).** Nếu hai biến cố $$A$$ và $$B$$ là **xung khắc** (mutually exclusive), nghĩa là chúng không thể cùng xảy ra ($$A \cap B = \emptyset$$), thì xác suất của hợp của chúng bằng tổng các xác suất riêng lẻ: $$P(A \cup B) = P(A) + P(B)$$. Điều này mở rộng cho bất kỳ tập hợp hữu hạn hoặc đếm được nào các biến cố xung khắc lẫn nhau.

Ba tiên đề này có vẻ đơn giản, nhưng chúng có những hệ quả sâu sắc. Từ chúng, chúng ta có thể suy ra tất cả các quy tắc xác suất khác mà chúng ta sẽ cần. Ví dụ, chúng ta có thể chứng minh rằng xác suất của biến cố bù $$A^c$$ (biến cố $$A$$ không xảy ra) là $$P(A^c) = 1 - P(A)$$. Để thấy điều này, lưu ý rằng $$A$$ và $$A^c$$ là xung khắc và hợp của chúng là toàn bộ không gian mẫu, vì vậy $$P(A) + P(A^c) = P(\Omega) = 1$$.

Một hệ quả quan trọng khác là **quy tắc cộng tổng quát** cho hai biến cố bất kỳ (không nhất thiết xung khắc):

$$P(A \cup B) = P(A) + P(B) - P(A \cap B)$$

Chúng ta phải trừ đi $$P(A \cap B)$$ vì nếu không, chúng ta sẽ đếm các kết quả trong cả $$A$$ và $$B$$ hai lần. Công thức này tương tự như nguyên lý bao hàm-loại trừ (inclusion-exclusion principle) trong lý thuyết tập hợp, và nó minh họa mối liên hệ sâu sắc giữa xác suất và lý thuyết tập hợp.

## Xác suất Có điều kiện: Cập nhật Niềm tin với Thông tin Mới

Một trong những khái niệm quan trọng nhất trong lý thuyết xác suất, và đặc biệt quan trọng cho suy diễn Bayesian, là **xác suất có điều kiện** (conditional probability). Đây là xác suất của một biến cố, với điều kiện chúng ta biết rằng một biến cố khác đã xảy ra.

Giả sử chúng ta quan tâm đến xác suất của biến cố $$A$$, nhưng chúng ta biết rằng biến cố $$B$$ đã xảy ra. Thông tin này thay đổi đánh giá của chúng ta về khả năng $$A$$ xảy ra như thế nào? Xác suất có điều kiện của $$A$$ cho $$B$$, ký hiệu là $$P(A \mid B)$$, được định nghĩa là:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$$

với điều kiện $$P(B) > 0$$.

Định nghĩa này có một trực giác rõ ràng. Khi chúng ta biết rằng $$B$$ đã xảy ra, không gian các kết quả có thể thu hẹp lại chỉ còn những kết quả trong $$B$$. Trong không gian thu hẹp này, xác suất của $$A$$ tỷ lệ với xác suất mà cả $$A$$ và $$B$$ cùng xảy ra, được chuẩn hóa bởi xác suất của $$B$$ để đảm bảo rằng tổng xác suất trong không gian mới vẫn bằng $$1$$.

Hãy xem xét một ví dụ cụ thể. Giả sử chúng ta toss một đồng xu công bằng hai lần. Không gian mẫu là $$\{SS, SN, NS, NN\}$$, và mỗi kết quả có xác suất $$1/4$$. Xác suất của biến cố "cả hai lần đều ra Sấp" ($$A = \{SS\}$$) là $$P(A) = 1/4$$. Nhưng giả sử chúng ta được biết rằng "ít nhất một lần ra Sấp" ($$B = \{SS, SN, NS\}$$). Với thông tin này, xác suất có điều kiện của $$A$$ cho $$B$$ là:

$$P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{P(\{SS\})}{P(\{SS, SN, NS\})} = \frac{1/4}{3/4} = \frac{1}{3}$$

Lưu ý rằng xác suất tăng từ $$1/4$$ lên $$1/3$$ khi chúng ta biết thêm thông tin. Đây là một ví dụ đơn giản của việc cập nhật niềm tin dựa trên bằng chứng mới, một ý tưởng trung tâm trong suy diễn Bayesian.

### Một biến thể rất dễ nhầm

Vẫn với hai lần tung đồng xu, hãy so sánh hai điều kiện khác nhau:

- Nếu biết **ít nhất một lần ra Sấp**, xác suất cả hai lần đều Sấp là $$1/3$$.
- Nhưng nếu biết **lần tung đầu tiên ra Sấp**, xác suất cả hai lần đều Sấp lại là $$1/2$$.

Hai bài toán nghe khá giống nhau, nhưng thông tin điều kiện không giống nhau nên xác suất có điều kiện cũng khác. Đây là bài học rất quan trọng: trong xác suất, ý nghĩa của “biết thêm thông tin” phụ thuộc hoàn toàn vào việc biến cố điều kiện đã loại bỏ những khả năng nào khỏi không gian mẫu.

Từ định nghĩa xác suất có điều kiện, chúng ta có thể suy ra **quy tắc nhân** (multiplication rule):

$$P(A \cap B) = P(A \mid B) \cdot P(B) = P(B \mid A) \cdot P(A)$$

Quy tắc này cho chúng ta hai cách khác nhau để tính xác suất của giao hai biến cố, và sự tương đương của chúng sẽ dẫn đến một trong những công thức quan trọng nhất trong thống kê: định lý Bayes.

## Độc lập: Khi Thông tin Không thay đổi Niềm tin

Hai biến cố $$A$$ và $$B$$ được gọi là **độc lập** (independent) nếu việc biết một biến cố xảy ra không thay đổi xác suất của biến cố kia. Hình thức hóa, $$A$$ và $$B$$ độc lập nếu và chỉ nếu:

$$P(A \mid B) = P(A)$$

hoặc tương đương:

$$P(A \cap B) = P(A) \cdot P(B)$$

Độc lập là một giả định mạnh và thường không đúng trong thực tế, nhưng nó đơn giản hóa đáng kể các tính toán xác suất và là nền tảng của nhiều mô hình thống kê. Ví dụ, khi chúng ta toss một đồng xu nhiều lần, chúng ta thường giả định rằng các lần toss là độc lập với nhau, nghĩa là kết quả của lần toss này không ảnh hưởng đến xác suất của các lần toss tiếp theo.

Tuy nhiên, trong nhiều tình huống thực tế, các biến cố không độc lập. Nếu chúng ta rút hai lá bài từ một bộ bài mà không hoàn lại, kết quả của lần rút thứ hai phụ thuộc vào lần rút thứ nhất. Nếu chúng ta quan sát nhiệt độ trong hai ngày liên tiếp, chúng có xu hướng tương quan với nhau. Việc nhận biết và mô hình hóa các phụ thuộc này là một phần quan trọng của phân tích dữ liệu Bayesian.

## Độc lập có điều kiện: Khi biết biến ẩn thì phụ thuộc biến mất

Có một tình huống tinh tế hơn độc lập thông thường: hai biến cố có thể **không độc lập khi nhìn toàn cục**, nhưng lại trở nên độc lập nếu ta biết thêm một biến ẩn $$C$$.

Ta nói $$A$$ và $$B$$ **độc lập có điều kiện theo $$C$$** nếu:

$$
P(A \cap B \mid C) = P(A \mid C)P(B \mid C).
$$

Trực giác là thế này:

Khi chưa biết $$C$$, ta đang trộn nhiều cơ chế sinh dữ liệu khác nhau vào chung một bức tranh; khi đã biết $$C$$, ta biết chính xác mình đang ở cơ chế nào; và trong từng cơ chế riêng lẻ đó, $$A$$ và $$B$$ có thể không còn ảnh hưởng lẫn nhau nữa.

Ví dụ, giả sử ta chọn ngẫu nhiên một trong hai đồng xu:

Đồng xu thứ nhất là công bằng, còn đồng xu thứ hai luôn ra ngửa.

Sau đó ta tung đồng xu đã chọn hai lần. Gọi:

Gọi $$C$$ là biến cố “đã chọn đồng xu 1”, $$A$$ là biến cố “lần tung thứ nhất ra ngửa”, và $$B$$ là biến cố “lần tung thứ hai ra ngửa”.

Nếu **biết trước đã chọn đồng xu nào**, hai lần tung là độc lập có điều kiện:

Dưới đồng xu công bằng, mỗi lần tung là độc lập với xác suất ngửa bằng $$1/2$$; dưới đồng xu luôn ngửa, hai lần tung vẫn độc lập theo nghĩa cả hai đều chắc chắn ra ngửa.

Nhưng nếu **không biết** đã chọn đồng xu nào, thì $$A$$ và $$B$$ không còn độc lập theo nghĩa thông thường nữa. Lý do là kết quả của lần tung đầu hé lộ thông tin về việc ta đang cầm loại đồng xu nào, và thông tin đó làm thay đổi niềm tin về lần tung thứ hai.

Đây là một ý rất quan trọng trong Bayes:

Phụ thuộc không phải lúc nào cũng đến từ việc các biến "tác động trực tiếp" lên nhau; đôi khi nó xuất hiện đơn giản vì ta chưa biết một biến ẩn đang đồng thời chi phối cả hai.

Khi học lên các mô hình hỗn hợp, mô hình phân cấp hay đồ thị nhân quả, bạn sẽ gặp lại ý tưởng này rất nhiều.

## Quy tắc Xác suất Toàn phần: Chia để Tính

Đôi khi, cách dễ nhất để tính xác suất của một biến cố là chia nó thành các trường hợp đơn giản hơn. **Quy tắc xác suất toàn phần** (law of total probability) cho phép chúng ta làm điều này một cách có hệ thống.

Giả sử chúng ta có một phân hoạch của không gian mẫu thành các biến cố xung khắc $$B_1, B_2, \ldots, B_n$$ sao cho $$\bigcup_{i=1}^n B_i = \Omega$$. Điều này có nghĩa là mỗi kết quả có thể thuộc về đúng một trong các $$B_i$$. Khi đó, xác suất của bất kỳ biến cố $$A$$ nào có thể được tính bằng:

$$P(A) = \sum_{i=1}^n P(A \mid B_i) \cdot P(B_i)$$

Công thức này nói rằng để tính $$P(A)$$, chúng ta có thể xem xét từng trường hợp $$B_i$$, tính xác suất của $$A$$ trong trường hợp đó ($$P(A \mid B_i)$$), nhân với xác suất của trường hợp đó ($$P(B_i)$$), và cộng tất cả lại.

Quy tắc này đặc biệt hữu ích trong các mô hình phân cấp, nơi chúng ta có các **biến tiềm ẩn (latent variables) không quan sát được trực tiếp**. Trong suy diễn Bayesian, chúng ta thường sử dụng quy tắc này để "loại trừ" (marginalize) các tham số không quan tâm, tập trung vào những gì chúng ta thực sự muốn suy luận.

## Ý nghĩa cho Suy diễn Bayesian

Tất cả các khái niệm chúng ta đã thảo luận trong bài học này không chỉ là lý thuyết trừu tượng. Chúng là nền tảng mà toàn bộ phân tích dữ liệu Bayesian được xây dựng trên đó.

**Trong suy diễn Bayesian, chúng ta sẽ sử dụng xác suất có điều kiện để cập nhật niềm tin về các tham số của mô hình khi chúng ta quan sát dữ liệu. Chúng ta sẽ sử dụng quy tắc xác suất toàn phần để loại trừ các tham số phiền nhiễu (nuisance parameters). Chúng ta sẽ sử dụng các tiên đề xác suất để đảm bảo rằng các suy luận của chúng ta là nhất quán và hợp lý.**

Quan trọng hơn, chúng ta sẽ áp dụng quan điểm Bayesian về xác suất như **mức độ tin tưởng**. Điều này cho phép chúng ta nói về "xác suất của một giả thuyết" hoặc "xác suất của một giá trị tham số", những khái niệm không có ý nghĩa trong thống kê tần suất nhưng lại rất tự nhiên và hữu ích trong thống kê Bayesian.

Khi bạn tiến xa hơn trong khóa học này, bạn sẽ thấy rằng mọi công cụ Bayesian, từ định lý Bayes đơn giản đến các mô hình phân cấp phức tạp, đều được xây dựng từ các nguyên tắc xác suất cơ bản mà chúng ta đã thảo luận ở đây. Việc hiểu sâu sắc những nền tảng này sẽ giúp bạn không chỉ áp dụng các phương pháp Bayesian một cách chính xác, mà còn hiểu được tại sao chúng hoạt động và khi nào chúng có thể thất bại.

## Bài tập

**Bài tập 1: Xác suất Cơ bản.** Một hộp chứa 5 viên bi đỏ, 3 viên bi xanh, và 2 viên bi vàng. Chúng ta rút ngẫu nhiên một viên bi. (a) Xác định không gian mẫu. (b) Tính xác suất rút được viên bi đỏ. (c) Tính xác suất rút được viên bi không phải màu vàng. Giải thích suy luận của bạn bằng lời, không chỉ công thức.

**Bài tập 2: Xác suất Có điều kiện.** Trong một lớp học, 60% sinh viên học Python, 40% học R, và 25% học cả hai. (a) Nếu một sinh viên được chọn ngẫu nhiên và biết rằng sinh viên đó học Python, xác suất để sinh viên đó cũng học R là bao nhiêu? (b) Hai biến cố "học Python" và "học R" có độc lập không? Giải thích bằng cả tính toán và trực giác.

**Bài tập 3: Quy tắc Xác suất Toàn phần.** Một công ty sản xuất sản phẩm tại ba nhà máy A, B, và C với tỷ lệ sản xuất lần lượt là 50%, 30%, và 20%. Tỷ lệ sản phẩm lỗi từ mỗi nhà máy lần lượt là 2%, 3%, và 5%. (a) Tính xác suất một sản phẩm được chọn ngẫu nhiên là lỗi. (b) Nếu một sản phẩm được phát hiện là lỗi, xác suất nó đến từ nhà máy C là bao nhiêu? (Gợi ý: Phần (b) yêu cầu định lý Bayes, mà chúng ta sẽ học trong bài tiếp theo, nhưng hãy thử suy luận bằng trực giác.)

**Bài tập 4: Nghịch lý Simpson.** Xem xét hai phương pháp điều trị A và B được thử nghiệm trên hai nhóm bệnh nhân: nhóm bệnh nhẹ và nhóm bệnh nặng. Trong nhóm bệnh nhẹ, A thành công 90/100 lần và B thành công 85/90 lần. Trong nhóm bệnh nặng, A thành công 20/100 lần và B thành công 15/110 lần. (a) Trong mỗi nhóm, phương pháp nào có tỷ lệ thành công cao hơn? (b) Tính tỷ lệ thành công tổng thể của mỗi phương pháp. (c) Giải thích tại sao kết quả có vẻ nghịch lý. Điều này dạy chúng ta gì về tầm quan trọng của việc xem xét các biến tiềm ẩn?

**Bài tập 5: Suy ngẫm về Xác suất.** Viết một đoạn văn ngắn (200-300 từ) giải thích sự khác biệt giữa quan điểm tần suất và quan điểm Bayesian về xác suất. Đưa ra một ví dụ về một tình huống mà quan điểm Bayesian có vẻ tự nhiên hơn, và giải thích tại sao. Suy ngẫm về việc cách chúng ta hiểu xác suất có thể ảnh hưởng đến cách chúng ta thiết kế thí nghiệm và diễn giải kết quả như thế nào.

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

*Bài học tiếp theo: [0.2 Bernoulli và Binomial](/vi/chapter00/00_02_01_bernoulli_binomial/)*
