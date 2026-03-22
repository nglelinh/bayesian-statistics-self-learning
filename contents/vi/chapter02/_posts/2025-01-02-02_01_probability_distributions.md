---
layout: post
title: "Bài 2.1: Phân phối Xác suất - Ngôn ngữ của Sự Không chắc chắn"
chapter: '02'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter02
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn nên làm được ba việc. Thứ nhất, đọc một phân phối như đọc một câu chuyện về mức độ chắc chắn. Thứ hai, phân biệt rõ khi nào nên dùng phân phối rời rạc và khi nào nên dùng phân phối liên tục. Thứ ba, hiểu vì sao trong Bayes ta luôn muốn giữ cả **phân phối đầy đủ**, thay vì chỉ giữ một con số trung bình.

> **Ví dụ mini.** Hai lớp đều có tỷ lệ qua môn là $$75\%$$, nhưng một lớp có 8 sinh viên còn lớp kia có 800 sinh viên. Cùng một tỷ lệ, nhưng mức độ chắc chắn không hề giống nhau.
>
> **Câu hỏi tự kiểm tra.** Nếu chỉ báo cáo một con số $$75\%$$, bạn đã bỏ mất thông tin quan trọng nào?

## Mở đầu: vì sao một con số thường là chưa đủ?

Giả sử bạn phụ trách theo dõi hiệu quả của một nút mua hàng mới trên website.

Ở tuần 1, bạn thấy 25 đơn hàng trên 100 lượt truy cập; ở tuần 2, bạn lại cũng thấy 25 đơn hàng, nhưng lần này trên 1000 lượt truy cập.

Cả hai tuần đều cho tỷ lệ $$25\%$$. Nếu chỉ nhìn **ước lượng điểm**, ta sẽ nói hai tuần là như nhau. Nhưng trực giác cho thấy điều đó không đúng. Ở tuần 2, ta **chắc hơn** rất nhiều rằng tỷ lệ thật sự đang ở gần $$25\%$$. Ở tuần 1, dữ liệu còn ít nên nhiều giá trị lân cận như $$18\%$$ hay $$32\%$$ vẫn khá hợp lý.

Đó là lý do thống kê Bayes không dừng ở câu “ước lượng là $$0.25$$”. Ta muốn một đối tượng giàu thông tin hơn: **phân phối xác suất**.

![Bản đồ niềm tin của phân phối]({{ site.baseurl }}/img/chapter_img/chapter02/distribution_belief_map.png)

## 1. Phân phối xác suất là gì?

Nói thật đơn giản, một phân phối xác suất là **bản đồ niềm tin** về những giá trị có thể xảy ra.

Nếu một giá trị được gán mật độ hoặc xác suất cao, điều đó có nghĩa là:

giá trị đó phù hợp hơn với điều ta biết, hoặc dữ liệu đang ủng hộ nó mạnh hơn, hoặc đồng thời cả hai điều ấy cùng xảy ra.

Trong Bayes, phân phối không chỉ dùng cho dữ liệu. Nó còn dùng để mô tả sự không chắc chắn về tham số chưa biết, chẳng hạn $$\theta$$ là tỷ lệ khách hàng mua hàng, về dữ liệu tương lai như số đơn hàng trong tuần sau, hoặc về các dự đoán như chiều cao trung bình của một lớp học.

### Một cách đọc rất đời thường

Trong thực hành, bạn có thể đọc một phân phối bằng cách tự hỏi ba câu rất đời thường: giá trị nào là trung tâm hợp lý nhất, mình đang chắc đến mức nào, và những giá trị cực đoan có còn khả thi hay không. Chính ba câu hỏi này biến một đồ thị xác suất thành một công cụ để suy nghĩ và ra quyết định.

## 2. Rời rạc và liên tục: hai kiểu không chắc chắn phổ biến

### 2.1. Phân phối rời rạc

Ta dùng phân phối rời rạc khi đại lượng chỉ nhận một tập giá trị đếm được.

Ví dụ:

số sinh viên vắng học trong hôm nay, số email spam nhận được trong 1 giờ, hay số mặt ngửa trong 10 lần tung đồng xu.

Khi đó ta làm việc với xác suất kiểu:

$$
P(X = x).
$$

Ví dụ, nếu $$X$$ là số lần khách hàng bấm vào quảng cáo, thì $$P(X=3)$$ là xác suất có đúng 3 lượt bấm.

### 2.2. Phân phối liên tục

Ta dùng phân phối liên tục khi đại lượng có thể nhận vô số giá trị trên một khoảng.

Ví dụ:

chiều cao, thời gian giao hàng, nhiệt độ, hay tỷ lệ chuyển đổi thật sự của một quảng cáo.

Lúc này ta làm việc với mật độ $$p(x)$$. Với biến liên tục, xác suất tại đúng một điểm thường bằng 0. Điều có ý nghĩa là xác suất nằm trong một khoảng:

$$
P(a < X < b) = \int_a^b p(x)\,dx.
$$

Ví dụ, thay vì hỏi “xác suất thời gian giao hàng đúng bằng 32.000 phút là bao nhiêu?”, ta hỏi “xác suất nằm trong khoảng từ 30 đến 35 phút là bao nhiêu?”.

## 3. Cùng trung bình, nhưng không cùng mức chắc chắn

Đây là chỗ người mới học Bayes thường “ngộ” ra giá trị của phân phối.

Giả sử hai người cùng nói: “Tôi nghĩ tỷ lệ khách hàng mua hàng khoảng $$0.25$$.” Nhưng họ dùng hai prior khác nhau:

Người A dùng Beta$$(3,9)$$ còn người B dùng Beta$$(30,90)$$.

Cả hai đều có trung bình:

$$
\frac{\alpha}{\alpha+\beta} = \frac{1}{4}.
$$

Nhưng chúng không mang cùng một ý nghĩa.

Beta$$(3,9)$$ khá rộng, nên nó giống với phát biểu “tôi nghĩ trung tâm là $$0.25$$, nhưng tôi vẫn còn khá mở với nhiều khả năng lân cận”; ngược lại, Beta$$(30,90)$$ hẹp hơn nhiều, nên nó giống với phát biểu “tôi không chỉ nghĩ trung tâm là $$0.25$$, tôi còn tin khá chắc là giá trị thật không đi quá xa”.

![Phân phối hẹp và rộng thể hiện mức chắc chắn khác nhau]({{ site.baseurl }}/img/chapter_img/chapter02/narrow_vs_wide.png)

Một con số trung bình không cho bạn thấy sự khác biệt này. Phân phối thì có.

## 4. Ba vai trò của phân phối trong Bayes

Trong Chapter 2, bạn sẽ gặp phân phối ở ba vị trí chính.

### 4.1. Prior

Prior $$P(\theta)$$ mô tả điều ta tin về tham số **trước khi** thấy dữ liệu hiện tại.

Ví dụ:

trước khi chạy quảng cáo mới, nhóm marketing có thể tin rằng tỷ lệ mua hàng thường nằm quanh $$2\%$$ đến $$5\%$$, còn trước khi kiểm thử dây chuyền mới, kỹ sư có thể tin rằng tỷ lệ lỗi khó mà vượt $$10\%$$.

### 4.2. Likelihood

Likelihood $$P(D \mid \theta)$$ mô tả dữ liệu sẽ hợp lý ra sao nếu tham số thật là $$\theta$$.

Ví dụ:

nếu tỷ lệ mở email thật sự là $$0.4$$ thì quan sát 41 email mở trên 100 email là khá hợp lý, còn nếu tỷ lệ thật sự chỉ là $$0.05$$ thì dữ liệu đó sẽ trở nên rất khó xảy ra.

### 4.3. Posterior

Posterior $$P(\theta \mid D)$$ là điều ta tin **sau khi** kết hợp prior với dữ liệu.

Đây là nơi Bayes thực sự vận hành:

$$
P(\theta \mid D) = \frac{P(D \mid \theta)P(\theta)}{P(D)}.
$$

Nói ngắn gọn nhưng đủ chính xác, prior là điểm xuất phát, likelihood là tiếng nói của dữ liệu, còn posterior là niềm tin đã được cập nhật sau khi hai nguồn thông tin ấy được kết hợp.

## 5. Đọc hình dạng của một phân phối như thế nào?

Khi nhìn đồ thị một phân phối, bạn nên tập thói quen đọc bốn thứ sau.

### 5.1. Trung tâm

Trung tâm cho biết vùng giá trị hợp lý nhất.

Ví dụ:

một phân phối tập trung quanh $$0.7$$ cho thấy tỷ lệ thành công hợp lý nhất đang ở mức cao, còn một phân phối tập trung quanh $$170$$ cho thấy chiều cao trung bình hợp lý nhất vào khoảng 170 cm.

### 5.2. Độ rộng

Độ rộng cho biết mức độ không chắc chắn.

Một phân phối hẹp cho biết ta khá chắc, còn một phân phối rộng cho biết ta vẫn còn mơ hồ đáng kể. Chẳng hạn, nếu 5 ngày đo nhiệt độ trong phòng server đều cho kết quả rất ổn định thì posterior sẽ hẹp; nhưng nếu ta mới chỉ đo trong 2 ngày đầu, posterior thường vẫn còn rộng.

### 5.3. Độ lệch

Phân phối có thể lệch trái hoặc lệch phải. Điều này hay gặp với xác suất, tỷ lệ hiếm, hoặc dữ liệu đếm.

Ví dụ:

tỷ lệ khách trả hàng thường khá nhỏ nên phân phối có thể lệch về phía gần 0, còn số cuộc gọi mỗi phút ở tổng đài cũng thường không đối xứng đẹp như phân phối Normal.

### 5.4. Đuôi

Đuôi cho biết các khả năng cực đoan còn đáng kể đến mức nào.

Trong quyết định kinh doanh hoặc y khoa, phần đuôi rất quan trọng vì nó liên quan tới rủi ro xấu nhất.

Ví dụ:

một chiến dịch quảng cáo có thể có doanh thu trung bình tốt nhưng đuôi trái dày, nghĩa là khả năng lỗ nặng vẫn chưa thể xem nhẹ; tương tự, một điều trị có thể có hiệu quả trung bình khá nhưng đuôi phải của tác dụng phụ lại lớn đến mức khiến bác sĩ phải giữ thái độ thận trọng.

## 6. Một số họ phân phối bạn sẽ gặp rất thường xuyên

### 6.1. Beta: dành cho đại lượng nằm giữa 0 và 1

Beta rất phù hợp khi đại lượng là:

xác suất, tỷ lệ, phần trăm chuyển đổi, tỷ lệ đậu môn, hay tỷ lệ máy lỗi.

Ví dụ:

tỷ lệ bệnh nhân hồi phục, tỷ lệ khách hàng nhấn vào quảng cáo, hay xác suất đồng xu ra ngửa.

![Họ phân phối Beta với nhiều hình dạng khác nhau]({{ site.baseurl }}/img/chapter_img/chapter02/beta_distribution_family.png)

### 6.2. Binomial: đếm số lần thành công trong $$n$$ lần thử

Dùng khi bạn có:

một tình huống trong đó có $$n$$ khách hàng nhìn thấy trang web, mỗi người hoặc mua hoặc không, và cuối cùng bạn đếm được bao nhiêu người thật sự mua hàng.

Các ví dụ khác:

số sinh viên đậu trong một lớp 40 người, hay số email được mở trong 100 email đã gửi.

### 6.3. Poisson: đếm số sự kiện xảy ra trong một khoảng

Phù hợp với:

số cuộc gọi đến trong 1 giờ, số đơn hàng trong 10 phút, hay số lỗi hệ thống mỗi ngày.

Poisson đặc biệt hữu ích khi ta quan tâm đến **tốc độ xảy ra sự kiện**.

### 6.4. Normal: dành cho đại lượng liên tục xoay quanh một trung tâm

Thường gặp trong:

chiều cao, điểm số, sai số đo lường, hay thời gian hoàn thành một tác vụ khi có nhiều nguồn dao động nhỏ cộng lại.

### 6.5. Vai trò của hàm Gamma trong các phân phối liên hợp

Khi học liên hợp ở Buổi 4, bạn sẽ thấy Beta và Gamma xuất hiện dày đặc. Hai họ này đều có hằng số chuẩn hóa dùng hàm Gamma:

$$
\Gamma(a)=\int_0^{\infty} x^{a-1}e^{-x}dx,
$$

và với số nguyên dương $$n$$ thì $$\Gamma(n)=(n-1)!$$.

Nhờ đó, ta viết được:

$$
\text{Beta}(\alpha,\beta)\propto \theta^{\alpha-1}(1-\theta)^{\beta-1},\quad 0<\theta<1,
$$

$$
\text{Gamma}(\alpha,\beta)\propto \lambda^{\alpha-1}e^{-\beta\lambda},\quad \lambda>0,
$$

trong tham số hóa shape-rate. Điểm chính cần nhớ: hàm Gamma là "keo nối" giúp các phân phối này chuẩn hóa đúng và cập nhật tham số gọn trong các cặp liên hợp.

### 6.6. Bảng nhanh hằng số chuẩn hóa của các họ thường gặp

Trong thực hành, ta thường viết trước dạng "hạt nhân" (kernel) rồi thêm hằng số chuẩn hóa để thành phân phối hợp lệ.

| Họ phân phối | Miền giá trị | Dạng chuẩn hóa | Hằng số chuẩn hóa chính |
|---|---|---|---|
| Bernoulli$$(p)$$ | $$x\in\{0,1\}$$ | $$P(X=x)=p^x(1-p)^{1-x}$$ | Tổng trên $$x=0,1$$ tự bằng 1 |
| Binomial$$(n,p)$$ | $$k=0,\dots,n$$ | $$P(K=k)=\binom{n}{k}p^k(1-p)^{n-k}$$ | $$\binom{n}{k}$$ (đếm số cách) |
| Poisson$$(\lambda)$$ | $$k=0,1,2,\dots$$ | $$P(Y=k)=\frac{\lambda^k e^{-\lambda}}{k!}$$ | $$e^{-\lambda}$$ và $$k!$$ |
| Normal$$(\mu,\sigma^2)$$ | $$x\in\mathbb{R}$$ | $$f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$ | $$\frac{1}{\sigma\sqrt{2\pi}}$$ |
| Exponential$$(\lambda)$$ | $$t\ge 0$$ | $$f(t)=\lambda e^{-\lambda t}$$ | $$\lambda$$ |
| Gamma$$(\alpha,\beta)$$ (shape-rate) | $$\lambda>0$$ | $$f(\lambda)=\frac{\beta^\alpha}{\Gamma(\alpha)}\lambda^{\alpha-1}e^{-\beta\lambda}$$ | $$\frac{\beta^\alpha}{\Gamma(\alpha)}$$ |
| Beta$$(\alpha,\beta)$$ | $$\theta\in(0,1)$$ | $$f(\theta)=\frac{1}{B(\alpha,\beta)}\theta^{\alpha-1}(1-\theta)^{\beta-1}$$ | $$\frac{1}{B(\alpha,\beta)}$$, với $$B=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$$ |

Ghi nhớ ngắn: khi chỉ viết dấu $$\propto$$, bạn đang làm việc với phần chưa chuẩn hóa; khi cần xác suất/mật độ hợp lệ để tích phân (hoặc tổng) bằng 1, phải thêm hằng số chuẩn hóa.

### 6.7. Nhắc nhanh miền tham số và tham số hóa

Để tránh nhầm khi đọc công thức liên hợp:

- Beta dùng cho tham số xác suất $$\theta\in(0,1)$$.
- Gamma dùng cho tham số dương $$\lambda>0$$ (tốc độ/cường độ).
- Normal thường dùng cho trung bình $$\mu\in\mathbb{R}$$ của dữ liệu liên tục.

Riêng Gamma, cần luôn ghi rõ tham số hóa. Trong tài liệu này, mặc định là shape-rate:

$$
E[\lambda]=\frac{\alpha}{\beta},\qquad \mathrm{Var}(\lambda)=\frac{\alpha}{\beta^2}.
$$

Nếu một nguồn khác dùng shape-scale thì kết quả số có thể khác nếu bạn không đổi tham số về cùng hệ.

### 6.8. Lưu ý xấp xỉ Normal: khi nào hợp lý, khi nào không

Trong thực hành, ta hay nghe "xấp xỉ Normal" cho tổng nhiều biến ngẫu nhiên hoặc cho posterior khá tập trung. Gợi ý nhanh:

- **Hợp lý hơn** khi cỡ mẫu đủ lớn, phân phối không quá lệch, và tham số không dính sát biên.
- **Kém hợp lý** với tỷ lệ rất gần 0/1, dữ liệu đếm rất nhỏ, hoặc posterior lệch mạnh.

Ví dụ với posterior Beta, xấp xỉ Normal thường tạm ổn khi cả hai tham số hậu nghiệm đều không nhỏ (thực hành hay dùng ngưỡng như $$\alpha_{post},\beta_{post}>5$$) và khối lượng xác suất không dồn sát 0 hoặc 1.

## 7. Vì sao Bayes thích giữ cả phân phối thay vì chỉ giữ một số?

Khi giữ cả phân phối, ta trả lời được nhiều câu hỏi thực tế hơn hẳn.

Ví dụ với một posterior cho tỷ lệ hoàn thành khóa học online, ta có thể hỏi:

xác suất tỷ lệ hoàn thành vượt $$60\%$$ là bao nhiêu, vùng giá trị hợp lý nhất của tỷ lệ đó là gì, và nếu mời thêm 100 học viên mới thì số người hoàn thành có thể nằm trong khoảng nào.

Nếu chỉ có một con số như $$0.58$$, ta gần như không trả lời được các câu hỏi này một cách nghiêm túc.

## 8. Minh họa nhanh bằng ba bối cảnh đời thường

### 8.1. Kinh doanh

Một startup chạy A/B test cho hai phiên bản landing page. Điều họ cần không chỉ là “phiên bản B tốt hơn 1.2 điểm phần trăm”, mà còn là:

mức bất định của kết luận đó lớn tới đâu, xác suất B thực sự tốt hơn A là bao nhiêu, và rủi ro còn lại nếu triển khai toàn bộ là gì.

### 8.2. Giáo dục

Một giảng viên muốn biết tỷ lệ sinh viên qua môn của khóa mới. Nếu lớp chỉ có 18 sinh viên, thì sự không chắc chắn phải được thể hiện rõ. Một posterior sẽ trung thực hơn nhiều so với chỉ báo cáo “tỷ lệ đậu hiện là $$72\%$$”.

### 8.3. Y tế

Một bác sĩ muốn biết tỷ lệ đáp ứng của một phác đồ mới. Với 12 bệnh nhân đầu tiên, kết luận chắc chắn là quá sớm. Phân phối cho phép bác sĩ nói “vùng giá trị hợp lý hiện tại là gì” thay vì đưa ra một con số trông có vẻ chính xác quá mức.

## 9. Những ngộ nhận phổ biến

### 9.1. “Phân phối chỉ là đồ thị đẹp”

Không. Phân phối là nơi chứa toàn bộ thông tin về giá trị trung tâm, độ bất định, rủi ro ở hai đuôi, và cả xác suất của những giả thuyết cụ thể mà ta quan tâm.

### 9.2. “Chỉ cần trung bình là đủ”

Không. Hai phân phối có thể có cùng trung bình nhưng gợi ra hai quyết định hoàn toàn khác nhau vì độ rộng của chúng khác nhau.

### 9.3. “Nhiều dữ liệu thì khỏi cần phân phối”

Ngay cả khi dữ liệu lớn, phân phối vẫn cần thiết để truyền đạt mức độ chắc chắn, so sánh các giả thuyết, dự đoán tương lai, và kiểm tra những rủi ro cực đoan mà một con số trung bình thường che khuất.

## Tóm tắt

**Phân phối xác suất là ngôn ngữ cốt lõi của thống kê Bayes.** Nó cho phép ta mô tả không chỉ “giá trị nào hợp lý”, mà còn “ta chắc đến đâu” và “các khả năng khác còn đáng kể không”.

Khi học Chapter 2, bạn nên luôn nhớ rằng prior là phân phối của niềm tin ban đầu, likelihood là phân phối mô tả mức độ dữ liệu phù hợp với từng giả thuyết, còn posterior là phân phối của niềm tin đã được cập nhật sau khi tiếp nhận dữ liệu.

Nếu nắm chắc vai trò của phân phối, các bài sau về likelihood, prior và posterior sẽ dễ hiểu hơn rất nhiều.

> **3 ý cần nhớ.** Phân phối luôn giàu thông tin hơn một ước lượng điểm vì nó giữ lại cả mức độ bất định; cùng một giá trị trung tâm chưa chắc nói cùng một điều nếu độ rộng của phân phối khác nhau; và trong Bayes, prior, likelihood, và posterior đều là những phân phối đóng các vai trò khác nhau trong suy luận.

## Câu hỏi tự luyện

1. Một lớp có 8 sinh viên và 6 người qua môn. Một lớp khác có 800 sinh viên và 600 người qua môn. Vì sao cùng tỷ lệ $$75\%$$ nhưng mức chắc chắn lại khác nhau?
2. Hãy cho ba ví dụ rời rạc và ba ví dụ liên tục trong đời sống hoặc công việc của bạn.
3. Prior Beta$$(4,16)$$ và Beta$$(40,160)$$ có cùng trung bình. Chúng khác nhau ở điểm nào về mặt diễn giải?
4. Nếu bạn là quản lý một quán cà phê, bạn muốn dự báo gì bằng **phân phối**, chứ không chỉ bằng một con số duy nhất?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1-2.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 4-5.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2.

---

*Bài học tiếp theo: [2.2 Likelihood - Câu chuyện về Dữ liệu và Mô hình](/vi/chapter02/likelihood/)*
