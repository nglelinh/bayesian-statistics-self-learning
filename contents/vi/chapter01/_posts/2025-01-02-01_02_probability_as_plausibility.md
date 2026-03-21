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

## Mục tiêu học tập

Sau bài này, bạn cần hiểu vì sao Bayesian statistics xem xác suất là **mức độ hợp lý của niềm tin** chứ không chỉ là tần suất dài hạn. Bạn cũng cần thấy được điểm mạnh của cách hiểu này trong những bài toán thật, nơi ta phải nói về các biến cố chỉ xảy ra một lần, về giả thuyết, và về tham số chưa biết.

> **Ví dụ mini.** Khi nghe “70% khả năng mưa ngày mai”, bạn hiểu đó là mức độ tin tưởng hiện tại để quyết định mang ô, chứ không phải tần số quan sát được từ vô số lần lặp của “ngày mai”.
>
> **Câu hỏi tự kiểm tra.** Vì sao câu “xác suất trời mưa ngày mai là 70%” lại khó diễn giải theo nghĩa tần suất nhưng rất tự nhiên theo nghĩa Bayes?

## 1. Một câu hỏi tưởng đơn giản: xác suất thật ra là gì?

Trong nhiều khóa thống kê truyền thống, xác suất thường được giới thiệu như:

- tần suất xảy ra của một sự kiện trong rất nhiều lần lặp lại.

Định nghĩa này hoạt động khá ổn với các ví dụ như:

- tung đồng xu,
- gieo xúc xắc,
- rút thẻ từ một bộ bài.

Nhưng nó bắt đầu gặp khó khi ta hỏi những câu rất đời thường như:

- xác suất trời mưa ngày mai là bao nhiêu,
- xác suất bệnh nhân này mắc bệnh A hay B là bao nhiêu,
- xác suất mô hình này đúng hơn mô hình kia là bao nhiêu.

Các sự kiện ấy không dễ được hiểu như “lặp lại vô hạn lần” theo nghĩa máy móc.

## 2. Quan điểm tần suất: xác suất là tần số dài hạn

Theo quan điểm frequentist, xác suất của một sự kiện là tần suất tương đối của nó khi số lần lặp đi tới rất lớn.

Ví dụ:

- nếu đồng xu cân bằng, thì khi tung rất nhiều lần, tỷ lệ mặt ngửa sẽ tiến gần tới 0.5.

Đây là một ý tưởng đẹp và quan trọng. Nhưng nó có hai giới hạn lớn.

### 2.1. Nó khó áp dụng cho sự kiện chỉ xảy ra một lần

Ví dụ:

- ngày mai mưa hay không,
- ca phẫu thuật này thành công hay không,
- thị trường tuần sau tăng hay giảm.

Bạn không thể “lặp lại vô hạn lần” đúng y hệt cùng một ngày mai để định nghĩa xác suất theo nghĩa thuần tần suất.

### 2.2. Nó không thoải mái khi nói về tham số chưa biết

Trong frequentist statistics:

- tham số $$\theta$$ được xem là cố định nhưng chưa biết,
- còn dữ liệu là ngẫu nhiên.

Vì vậy, họ không thích câu:

- “xác suất $$\theta$$ nằm giữa 0.4 và 0.6 là 95%”.

Với họ, $$\theta$$ đâu có ngẫu nhiên để mà gán xác suất.

## 3. Quan điểm Bayes: xác suất là độ hợp lý

Bayesian statistics đi theo một hướng tự nhiên hơn cho nhiều bài toán thực tế.

Xác suất không chỉ là tần số dài hạn. Nó còn là:

- mức độ tin tưởng,
- mức độ hợp lý,
- mức độ mà ta nên đặt cược vào một mệnh đề,

dựa trên thông tin hiện có.

Ví dụ:

- “70% khả năng mưa ngày mai” nghĩa là, với thông tin hiện tại, mệnh đề “ngày mai mưa” đáng tin ở mức 70%.

Đây không phải là một cách nói lỏng lẻo. Nó chính là nền tảng của Bayesian reasoning.

![Câu chuyện Linh và chiếc ô]({{ site.baseurl }}/img/chapter_img/chapter01/linh_umbrella_story.png)

## 4. Vì sao cách hiểu Bayesian lại gần đời sống hơn?

Bởi vì con người suy nghĩ như vậy gần như mỗi ngày.

### 4.1. Dự báo thời tiết

Khi nghe “70% khả năng mưa”, bạn:

- không suy nghĩ về vô số thế giới song song,
- mà nghĩ “trời khá dễ mưa, nên tốt hơn là mang ô”.

### 4.2. Chẩn đoán y khoa

Bác sĩ không chỉ nhìn triệu chứng hiện tại. Họ còn dùng:

- tần suất bệnh trong cộng đồng,
- tuổi tác, tiền sử bệnh,
- kết quả xét nghiệm trước đó.

Đó chính là tư duy cập nhật niềm tin dựa trên thông tin.

### 4.3. Kinh doanh

Một startup thấy 3 khách hàng đầu tiên đều mua hàng. Không ai kết luận ngay rằng tỷ lệ mua hàng thật là 100%. Ta giữ một mức bất định hợp lý, rồi tiếp tục cập nhật khi có thêm dữ liệu.

![Bayesian thinking trong đời sống hằng ngày]({{ site.baseurl }}/img/chapter_img/chapter01/bayesian_daily_life.png)

## 5. Ví dụ trực quan: đồng xu của người bạn

Giả sử bạn của bạn đưa một đồng xu và nói:

- “Tôi vừa tung 10 lần, ra 8 mặt ngửa.”

Bạn muốn trả lời câu hỏi:

- xác suất thực sự ra ngửa của đồng xu này có thể là bao nhiêu?

### Frequentist sẽ nói gì?

Họ sẽ nói đại loại:

- tham số thật là một hằng số,
- ta chỉ có thể ước lượng nó và dựng khoảng tin cậy.

### Bayesian sẽ nói gì?

Bayesian sẽ nói:

- trước dữ liệu, tôi có một prior về $$\theta$$,
- sau dữ liệu 8/10, tôi cập nhật prior đó thành posterior,
- và posterior nói vùng nào của $$\theta$$ đang hợp lý hơn.

![So sánh trực giác đồng xu giữa Frequentist và Bayes]({{ site.baseurl }}/img/chapter_img/chapter01/coin_flip_comparison.png)

Điểm mạnh ở đây là Bayes cho phép ta nói trực tiếp về:

- tham số chưa biết,
- mức độ tin tưởng của ta,
- và cách niềm tin đó thay đổi theo dữ liệu.

## 6. “Chủ quan” có phải là điểm yếu không?

Nhiều người nghe đến “degree of belief” thì lo rằng Bayes quá chủ quan. Nhưng cần phân biệt:

- **chủ quan có nguyên tắc**
- và **tùy tiện**.

Trong Bayes, bạn không được gán xác suất tùy ý vô lý. Các xác suất vẫn phải:

- nhất quán,
- tuân theo các quy tắc của xác suất,
- và có thể bị dữ liệu sửa lại.

Nói cách khác:

- Bayes cho phép niềm tin cá nhân xuất hiện,
- nhưng buộc niềm tin đó phải có cấu trúc logic và chịu trách nhiệm trước dữ liệu.

## 7. Dutch book trực giác: vì sao niềm tin phải nhất quán?

Một cách nghĩ rất hay là:

- nếu hệ thống xác suất của bạn không nhất quán,
- người khác có thể dàn xếp các cược khiến bạn thua chắc chắn.

Ý tưởng này được gọi là Dutch book argument.

Bạn không cần đào sâu phần triết học này ngay lập tức. Chỉ cần nhớ một điều:

**Bayesian probability không phải “muốn tin gì thì tin”. Nó là niềm tin có kỷ luật.**

![Dutch book cartoon]({{ site.baseurl }}/img/chapter_img/chapter01/dutch_book_cartoon.png)

## 8. Cox và ý tưởng “xác suất là logic mở rộng”

Một cách diễn đạt rất đẹp là:

- logic cổ điển xử lý những gì chắc chắn đúng hoặc chắc chắn sai,
- còn xác suất xử lý những gì chưa chắc chắn hoàn toàn.

Theo tinh thần đó, xác suất Bayesian có thể xem như một dạng **logic mở rộng cho thế giới bất định**.

Điều này giải thích vì sao Bayes thấy tự nhiên:

- khi chưa có dữ liệu, ta giữ một mức độ tin tưởng ban đầu,
- khi có dữ liệu mới, ta cập nhật nó.

## 9. Ai là ngẫu nhiên? Ai là cố định?

Đây là khác biệt cốt lõi giữa Frequentist và Bayesian.

### Frequentist

- tham số: cố định nhưng chưa biết,
- dữ liệu: ngẫu nhiên.

### Bayesian

- dữ liệu quan sát: đã cố định,
- tham số: chưa biết nên được mô tả bằng phân phối xác suất.

Điều này dẫn đến khác biệt rất lớn trong cách diễn giải kết quả.

![Khác biệt triết học giữa Frequentist và Bayesian]({{ site.baseurl }}/img/chapter_img/chapter01/frequentist_vs_bayesian_philosophy.png)

## 10. Vì sao chương này rất quan trọng cho phần sau?

Nếu bạn không chấp nhận được rằng:

- xác suất có thể mô tả niềm tin hợp lý,

thì toàn bộ Bayes phía sau sẽ trông rất lạ.

Nhưng một khi bạn thấy được điều này, các khái niệm như:

- prior,
- posterior,
- credible interval,
- xác suất giả thuyết,

sẽ trở nên rất tự nhiên.

## 11. Một cách nhớ ngắn gọn

Nếu phải tóm lại chỉ trong hai câu:

- Frequentist: xác suất gắn với tần suất dài hạn của dữ liệu có thể lặp lại.
- Bayesian: xác suất gắn với mức độ hợp lý của điều ta tin trong điều kiện thông tin hiện có.

Không phải một bên hoàn toàn sai và bên kia hoàn toàn đúng trong mọi tình huống. Nhưng Bayes linh hoạt hơn rất nhiều cho các câu hỏi khoa học thật sự.

> **3 ý cần nhớ.**
> 1. Frequentist và Bayesian khác nhau trước hết ở cách định nghĩa xác suất, không chỉ ở kỹ thuật tính toán.
> 2. Quan điểm Bayes xem xác suất như độ hợp lý nên áp dụng tự nhiên cho giả thuyết, tham số và các sự kiện chỉ xảy ra một lần.
> 3. “Chủ quan” trong Bayes không có nghĩa là tùy tiện, vì niềm tin vẫn phải tuân theo các quy tắc nhất quán của xác suất.

## Câu hỏi tự luyện

1. Vì sao dự báo “70% khả năng mưa ngày mai” là ví dụ rất tự nhiên cho cách hiểu Bayesian về xác suất?
2. Trong bài toán đồng xu 8/10 mặt ngửa, Frequentist và Bayesian khác nhau ở chỗ nào quan trọng nhất?
3. Hãy nêu một ví dụ trong công việc hoặc đời sống mà cách hiểu xác suất như độ hợp lý hữu ích hơn cách hiểu tần suất.
4. Vì sao Bayes vẫn có tính kỷ luật logic dù cho phép đưa niềm tin ban đầu vào mô hình?

## Tài liệu tham khảo

- Jaynes, E. T. *Probability Theory: The Logic of Science*.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 1.

---

*Bài học tiếp theo: [1.3 Định lý Bayes - Công cụ Cập nhật Niềm tin](/vi/chapter01/bayes-theorem-posterior/)*
