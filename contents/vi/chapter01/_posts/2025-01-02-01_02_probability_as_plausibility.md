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

Năm 1946, nhà vật lý Richard Cox đặt ra một câu hỏi tưởng thuộc về triết học thuần túy: nếu ta muốn mở rộng logic đúng/sai của Aristotle sang thế giới không chắc chắn — sao cho mức độ hợp lý của các mệnh đề luôn nhất quán — thì bộ quy tắc toán học nào là duy nhất? Kết quả chứng minh của ông gây kinh ngạc: bất kỳ hệ thống suy luận hợp lý nhất quán nào cũng *bắt buộc* phải đẳng cấu với các quy tắc xác suất (quy tắc cộng và quy tắc nhân), từ đó kéo theo định lý Bayes.

Trước đó ít lâu, Frank Ramsey và Bruno de Finetti cũng đi tới đúng kết luận ấy từ một hướng khác hoàn toàn: nếu niềm tin của bạn vi phạm tiên đề xác suất, đối thủ có thể lập một tổ hợp kèo cược (*Dutch book*) khiến bạn chắc chắn thua tiền bất kể thực tế diễn ra thế nào.

---

## Mục tiêu học tập

Sau bài này, bạn cần hiểu vì sao thống kê Bayes xem xác suất là **mức độ hợp lý của niềm tin** chứ không chỉ là tần suất dài hạn. Bạn cũng cần thấy được lợi thế của cách hiểu này trong những bài toán thực tế, nơi ta cần đánh giá các biến cố chỉ xảy ra một lần, các giả thuyết và các tham số chưa biết.

> **Ví dụ mini.** Khi nghe “70% khả năng mưa ngày mai”, bạn hiểu đó là mức độ tin cậy hiện tại để quyết định có mang ô hay không, chứ không phải tần suất thu được từ vô số lần lặp lại của “ngày mai”.
>
> **Câu hỏi tự kiểm tra.** Vì sao câu “xác suất trời mưa ngày mai là 70%” khó diễn giải theo nghĩa tần suất nhưng lại rất tự nhiên theo quan điểm Bayes?


## Bản đồ kiến thức nền: Diễn giải xác suất, Định lý Cox và Tính nhất quán Dutch Book

Bài học này đặt nền móng triết học – toán học cho toàn bộ khóa học thông qua ba trụ cột:

- **Tần suất dài hạn so với Độ hợp lý (Frequentist vs. Epistemic Probability):** Trường phái tần suất định nghĩa xác suất qua giới hạn của thí nghiệm lặp vô hạn, nên không thể gán xác suất cho sự kiện đơn lẻ hay tham số cố định. Trường phái Bayes xem xác suất là **độ hợp lý có điều kiện trên thông tin hiện có**, áp dụng thống nhất cho cả dữ liệu lẫn tham số chưa biết.
- **Định lý Cox & Lập luận Dutch Book:** Chứng minh rằng xác suất Bayes không phải sự tùy tiện chủ quan, mà là hệ quả logic duy nhất của yêu cầu nhất quán (*coherence*).
- **Cầu nối sang Mô hình hóa Bayes:** Khi xem tham số $$\theta$$ cũng có phân phối xác suất biểu diễn trạng thái tri thức, mọi bài toán suy luận, dự báo và kiểm định đều quy về một phép toán duy nhất: tính xác suất có điều kiện và biên hóa.

---

## 1. Một câu hỏi tưởng đơn giản: xác suất thực chất là gì?

Trong nhiều khóa thống kê truyền thống, xác suất thường được giới thiệu là tần suất xuất hiện của một sự kiện qua rất nhiều lần lặp lại. Định nghĩa này hoạt động tốt với những ví dụ như tung đồng xu, gieo xúc xắc hay rút thẻ từ bộ bài. Tuy nhiên, nó bắt đầu bộc lộ giới hạn khi ta đặt ra các câu hỏi rất thực tế như: xác suất trời mưa ngày mai là bao nhiêu, xác suất bệnh nhân này mắc bệnh A hay B là bao nhiêu, hay xác suất mô hình này đúng hơn mô hình kia là bao nhiêu. Những sự kiện như vậy khó có thể hiểu theo nghĩa “lặp lại vô hạn lần” một cách cơ học.

## 2. Quan điểm tần suất: xác suất là tần suất dài hạn

Theo quan điểm tần suất (frequentist), xác suất của một sự kiện là tần suất tương đối của nó khi số lần lặp tiến tới rất lớn. Ví dụ, với một đồng xu cân bằng, khi tung rất nhiều lần thì tỷ lệ mặt ngửa sẽ tiến gần về 0.5. Đây là một ý tưởng chặt chẽ và có vai trò quan trọng, nhưng nó có hai giới hạn lớn.

### 2.1. Khó áp dụng cho sự kiện chỉ xảy ra một lần

Những biến cố như ngày mai có mưa hay không, ca phẫu thuật này có thành công hay không, hay thị trường tuần tới tăng hay giảm đều là các sự kiện đơn lẻ. Ta không thể “lặp lại vô hạn lần” đúng cùng một ngày mai để định nghĩa xác suất theo nghĩa tần suất thuần túy.

### 2.2. Khó phát biểu trực tiếp về tham số chưa biết

Trong thống kê tần suất, tham số $$\theta$$ được xem là một hằng số cố định nhưng chưa biết, còn dữ liệu mới là đại lượng ngẫu nhiên. Vì vậy, trường phái này tránh nói “xác suất để $$\theta$$ nằm giữa 0.4 và 0.6 là 95%”, bởi theo quan điểm của họ, $$\theta$$ không phải biến ngẫu nhiên để có thể gán xác suất.

## 3. Quan điểm Bayes: xác suất là độ hợp lý

Thống kê Bayes đi theo một hướng phù hợp hơn với nhiều bài toán thực tế: xác suất không chỉ là tần suất dài hạn, mà còn là mức độ tin cậy, mức độ hợp lý hay mức độ sẵn sàng đặt cược vào một mệnh đề dựa trên thông tin hiện có. Nhờ đó, phát biểu “70% khả năng mưa ngày mai” được hiểu một cách tự nhiên là: với thông tin hiện tại, mệnh đề “ngày mai có mưa” đáng tin ở mức 70%. Đây không phải cách nói cảm tính, mà là nền tảng của suy luận Bayes.

![Câu chuyện Linh và chiếc ô]({{ site.baseurl }}/img/chapter_img/chapter01/linh_umbrella_story.png)

## 4. Vì sao cách hiểu Bayes gần với đời sống hơn?

Cách hiểu này phản ánh đúng cách con người suy luận hằng ngày trong nhiều tình huống quen thuộc.

### 4.1. Dự báo thời tiết

Khi nghe “70% khả năng mưa”, bạn không nghĩ về vô số thế giới song song, mà đơn giản hiểu rằng khả năng mưa khá cao nên mang theo ô là hợp lý.

### 4.2. Chẩn đoán y khoa

Bác sĩ không chỉ nhìn vào triệu chứng trước mắt, mà còn kết hợp tỷ lệ mắc bệnh trong cộng đồng, tuổi tác, tiền sử bệnh và các kết quả xét nghiệm trước đó. Quá trình ấy chính là cập nhật niềm tin dựa trên thông tin.

### 4.3. Kinh doanh

Một công ty khởi nghiệp thấy 3 khách hàng đầu tiên đều mua hàng. Không ai kết luận ngay rằng tỷ lệ mua hàng thực sự là 100%; thay vào đó, ta giữ một mức bất định hợp lý và tiếp tục cập nhật khi có thêm dữ liệu.

![Nghe tiếng động lạ rồi cập nhật giả thuyết nguyên nhân]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayesian_daily_life_night_noise.png)

![Đọc review nhà hàng rồi cập nhật đánh giá]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayesian_daily_life_restaurant.png)

![Dự báo thời tiết như một quá trình cập nhật niềm tin]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayesian_daily_life_weather.png)

![Chẩn đoán y khoa như một quá trình cập nhật niềm tin]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_bayesian_daily_life_medical.png)

## 5. Ví dụ trực quan: đồng xu của người bạn

Giả sử bạn của bạn đưa một đồng xu và nói: “Tôi vừa tung 10 lần, ra 8 mặt ngửa.” Câu hỏi bạn thực sự muốn trả lời là xác suất ra ngửa của đồng xu này có thể nằm ở mức nào.

### Theo quan điểm tần suất

Nhà thống kê tần suất xem tham số thực là một hằng số cố định; ta chỉ có thể ước lượng nó từ mẫu và dựng khoảng tin cậy.

### Theo quan điểm Bayes

Nhà thống kê Bayes đặt một phân phối tiền nghiệm (prior) cho $$\theta$$ trước khi thấy dữ liệu; sau khi quan sát 8/10 mặt ngửa, prior đó được cập nhật thành phân phối hậu nghiệm (posterior), cho biết vùng giá trị nào của $$\theta$$ hiện đang hợp lý hơn.

![Cách nhà thống kê tần suất nhìn bài toán đồng xu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_coin_flip_frequentist.png)

![Cách nhà thống kê Bayesian nhìn bài toán đồng xu]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_coin_flip_bayesian.png)

Điểm mạnh của cách tiếp cận Bayes là cho phép phát biểu trực tiếp về tham số chưa biết, mức độ tin cậy hiện tại và cách niềm tin đó dịch chuyển theo dữ liệu.

### Cách đọc bằng con số

Nếu bắt đầu với prior đều Beta$$(1,1)$$ và quan sát 8 mặt ngửa trong 10 lần tung, posterior sẽ là Beta$$(9,3)$$. Trung bình hậu nghiệm lúc này là:

$$
\frac{9}{9+3}=0.75.
$$

Ta cũng có thể hỏi trực tiếp: “xác suất đồng xu thiên về mặt ngửa cao hơn mức cân bằng là bao nhiêu?”, tức $$P(\theta>0.5\mid D)$$, và giá trị này vào khoảng $$0.97$$. Đây chính là tinh thần xem xác suất như độ hợp lý: nó cho phép định lượng trực tiếp mức độ hợp lý của các giá trị tham số sau khi đã quan sát dữ liệu.

## 6. Tính “chủ quan” có phải là điểm yếu không?

Nhiều người khi nghe đến “mức độ tin cậy” (degree of belief) thường lo ngại rằng thống kê Bayes quá chủ quan. Tuy nhiên, cần phân biệt giữa **chủ quan có nguyên tắc** và sự tùy tiện. Trong thống kê Bayes, bạn không được gán xác suất một cách vô căn cứ; các xác suất phải nhất quán, tuân thủ các tiên đề xác suất và chịu sự điều chỉnh của dữ liệu. Nói cách khác, Bayes cho phép đưa kiến thức ban đầu vào mô hình, nhưng buộc niềm tin đó phải có cấu trúc logic rõ ràng và sẵn sàng thay đổi trước bằng chứng mới.

## 7. Trực giác Dutch book: vì sao niềm tin phải nhất quán?

Một lập luận nổi tiếng gọi là **Dutch book argument** chỉ ra rằng nếu hệ thống xác suất của bạn không nhất quán, người khác có thể thiết kế một tổ hợp kèo cược khiến bạn chắc chắn thua bất kể kết quả nào xảy ra. Bạn chưa cần đi sâu vào khía cạnh triết học này ngay lúc đầu; điều quan trọng cần nhớ là **xác suất Bayes không phải “muốn tin gì thì tin”, mà là niềm tin có kỷ luật logic**.

![Dutch book cartoon]({{ site.baseurl }}/img/chapter_img/chapter01/dutch_book_cartoon.png)

## 8. Cox và ý tưởng “xác suất là logic mở rộng”

Logic cổ điển xử lý các mệnh đề chắc chắn đúng hoặc chắc chắn sai, trong khi xác suất xử lý những mệnh đề chưa chắc chắn hoàn toàn. Theo tinh thần đó, xác suất Bayes có thể được xem như một dạng **logic mở rộng cho thế giới có bất định**. Điều này giải thích vì sao cách tiếp cận Bayes trở nên tự nhiên: khi chưa có dữ liệu, ta giữ một mức độ tin cậy ban đầu; khi dữ liệu mới xuất hiện, ta cập nhật niềm tin ấy một cách nhất quán.

## 9. Đại lượng nào ngẫu nhiên, đại lượng nào cố định?

Đây là khác biệt cốt lõi giữa hai trường phái Frequentist và Bayesian.

### Trường phái Frequentist

Tham số là đại lượng cố định nhưng chưa biết, còn dữ liệu là đại lượng ngẫu nhiên.

### Trường phái Bayesian

Dữ liệu đã quan sát là cố định, còn tham số chưa biết được mô tả bằng phân phối xác suất.

Sự khác biệt nền tảng này dẫn đến hai cách diễn giải kết quả rất khác nhau.

![Frequentist nhìn xác suất theo dữ liệu lặp lại]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_philosophy_frequentist.png)

![Bayesian nhìn xác suất như bất định về tham số]({{ site.baseurl }}/img/chapter_img/chapter01/chapter01_philosophy_bayesian.png)

## 10. Vì sao bài học này quan trọng cho các phần sau?

Nếu chưa chấp nhận rằng xác suất có thể biểu diễn mức độ hợp lý của niềm tin, toàn bộ các khái niệm Bayes ở những chương sau sẽ trở nên khó hiểu. Ngược lại, khi đã nắm rõ quan điểm này, những khái niệm như prior, posterior, khoảng tin cậy Bayes (credible interval) hay xác suất của giả thuyết sẽ trở nên mạch lạc và tự nhiên.

## 11. Tóm lược ngắn gọn

Nếu tóm gọn trong một câu: trường phái tần suất gắn xác suất với tần suất dài hạn của dữ liệu có thể lặp lại, còn trường phái Bayes gắn xác suất với mức độ hợp lý của niềm tin dựa trên thông tin hiện có. Không phải một bên hoàn toàn sai và bên kia hoàn toàn đúng trong mọi bối cảnh, nhưng cách hiểu Bayes linh hoạt hơn nhiều đối với các câu hỏi khoa học thực tế.

> **3 ý cần nhớ.** Frequentist và Bayesian khác nhau trước hết ở cách định nghĩa xác suất chứ không chỉ ở kỹ thuật tính toán; quan điểm Bayes xem xác suất là độ hợp lý nên áp dụng tự nhiên cho giả thuyết, tham số và các sự kiện chỉ xảy ra một lần; và tính “chủ quan” trong Bayes không đồng nghĩa với tùy tiện vì mọi niềm tin đều phải tuân thủ quy tắc nhất quán của xác suất.


## Khung giải thích (nên đọc chậm): Chứng minh bằng con số vì sao niềm tin bất nhất sẽ bị "Dutch Book"

Nhiều người nghĩ tính nhất quán xác suất chỉ là lý thuyết suông. Hãy đọc chậm ví dụ đặt cược 4 bước sau để thấy bất kỳ sự vi phạm tiên đề cộng nào cũng dẫn đến thua lỗ chắc chắn:

1. **Liên hệ niềm tin với giá cược công bằng:** Nếu bạn tin biến cố $$A$$ có độ hợp lý $$q$$, bạn sẵn sàng mua/bán một vé trả $$100\text{ nghìn}$$ khi $$A$$ xảy ra với giá $$100q\text{ nghìn}$$.
2. **Giả sử niềm tin bị bất nhất:** Bạn gán xác suất đội X thắng là $$0.60$$ và đội X không thắng là $$0.50$$ — tổng bằng $$1.10 > 1$$ (vi phạm tiên đề chuẩn hóa).
3. **Đối thủ thiết lập bộ kèo Dutch Book:** Đối thủ bán cho bạn cả hai vé (một vé "đội X thắng" giá $$60\text{ nghìn}$$, một vé "đội X không thắng" giá $$50\text{ nghìn}$$).
4. **Kiểm tra mọi kịch bản thực tế:** Tổng tiền bạn bỏ ra là $$110\text{ nghìn}$$, nhưng dù kết quả trận đấu thế nào bạn cũng chỉ thắng đúng một vé và nhận lại $$100\text{ nghìn}$$ — lỗ chắc chắn $$10\text{ nghìn}$$!

### Ví dụ tính toán cầm tay chỉ việc: Bảng kết quả của một Dutch Book

| Kịch bản thực tế | Tiền bạn bỏ ra mua 2 vé | Tiền nhận về từ vé thắng | Lãi / Lỗ ròng của bạn |
| --- | --- | --- | --- |
| Đội X thắng ($$A$$) | $$60 + 50 = 110\text{ nghìn}$$ | $$100\text{ nghìn}$$ | $$-10\text{ nghìn}$$ |
| Đội X không thắng ($$A^c$$) | $$60 + 50 = 110\text{ nghìn}$$ | $$100\text{ nghìn}$$ | $$-10\text{ nghìn}$$ |

Để không bao giờ rơi vào tình huống thua chắc chắn như vậy (dù ở vai người mua hay người bán vé), bộ niềm tin $$q(A)$$ bắt buộc phải thỏa mãn đúng ba tiên đề Kolmogorov và quy tắc cập nhật Bayes khi có thêm thông tin!

**Hiểu lầm cần tránh:** Nghĩ rằng "xác suất chủ quan" trong Bayes nghĩa là ai muốn bịa số nào cũng được. Thực chất "chủ quan" có nghĩa là *phụ thuộc vào thông tin hiện có*, và mọi bước cập nhật từ thông tin đó đều bị ràng buộc chặt chẽ bởi toán học.

**Kiểm tra nhanh:** Nếu bạn gán $$q(A) = 0.45$$ và $$q(A^c) = 0.45$$ (tổng $$0.90 < 1$$), đối thủ chỉ cần *mua lại* cả hai vé từ bạn với tổng giá $$90\text{ nghìn}$$ và chắc chắn thu về $$100\text{ nghìn}$$ từ bạn — bạn vẫn lỗ chắc chắn $$10\text{ nghìn}$$.

---

## Video tham khảo

- [The Bayesian Trap](https://www.youtube.com/watch?v=R13BD8qKeTg) — Veritasium, English. **xem trước**. Minh họa cách dùng xác suất như mức độ tin vào giả thuyết, làm rõ bước chuyển từ tần suất dài hạn sang độ hợp lý.
- [Bayes' Theorem (with Example!)](https://www.youtube.com/watch?v=akClB1J6b28) — Steve Brunton, English. Trình bày định lý Bayes như bài toán suy luận ngược từ dấu hiệu về nguyên nhân, hỗ trợ các tình huống xảy ra một lần trong bài.
- [Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM) — 3Blue1Brown, English. Trực quan hóa quá trình cập nhật niềm tin bằng diện tích, giúp hình dung rõ xác suất theo nghĩa độ hợp lý (plausibility).

## Câu hỏi tự luyện

1. Vì sao dự báo “70% khả năng mưa ngày mai” là ví dụ tự nhiên cho cách hiểu Bayes về xác suất?
2. Trong bài toán đồng xu 8/10 mặt ngửa, điểm khác biệt quan trọng nhất giữa Frequentist và Bayesian là gì?
3. Hãy nêu một ví dụ trong công việc hoặc đời sống mà cách hiểu xác suất như độ hợp lý hữu ích hơn cách hiểu tần suất.
4. Vì sao thống kê Bayes vẫn giữ được tính kỷ luật logic dù cho phép đưa niềm tin ban đầu vào mô hình?

## Tài liệu tham khảo

- Jaynes, E. T. *Probability Theory: The Logic of Science*.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 1.

---

*Bài học tiếp theo: [1.3 Định lý Bayes - Công cụ Cập nhật Niềm tin]({{ site.baseurl }}/contents/vi/chapter01/01_03_bayes_theorem_posterior/)*
