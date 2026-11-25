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

Nếu ai đó nói với bạn *"thời gian giao hàng trung bình là 30 phút"*, bạn vẫn chưa biết liệu đơn hàng sẽ luôn đến trong khoảng 28–32 phút hay lúc thì 10 phút lúc lại trễ hẳn 2 tiếng. Một con số trung bình đơn lẻ xóa sạch toàn bộ câu chuyện về rủi ro. Chính vì vậy, ngôn ngữ thực sự của thống kê Bayes không phải là **con số đơn**, mà là **phân phối xác suất** — đối tượng toán học ghi trọn vẹn cả vị trí trung tâm, độ phân tán lẫn hình dạng đuôi của sự không chắc chắn.

Bài mở đầu Chương 2 này giúp bạn nhìn các họ phân phối quen thuộc không như danh mục công thức phải thuộc, mà như những viên gạch để viết nên câu chuyện prior, likelihood và posterior.

---

## Mục tiêu học tập

Sau bài này, bạn cần nắm được ba nội dung chính. Thứ nhất, đọc một phân phối xác suất như cách mô tả mức độ chắc chắn. Thứ hai, phân biệt rõ khi nào nên dùng phân phối rời rạc và khi nào nên dùng phân phối liên tục. Thứ ba, hiểu vì sao thống kê Bayes luôn ưu tiên giữ **toàn bộ phân phối** thay vì chỉ rút gọn về một con số trung bình.

> **Ví dụ mini.** Hai lớp học đều có tỷ lệ qua môn là $$75\%$$, nhưng một lớp có 8 sinh viên còn lớp kia có 800 sinh viên. Cùng một tỷ lệ, nhưng mức độ chắc chắn về kết quả không hề giống nhau.
>
> **Câu hỏi tự kiểm tra.** Nếu chỉ báo cáo một con số $$75\%$$, bạn đã bỏ sót thông tin quan trọng nào?


## Kiến thức cần nhớ: PMF/PDF, Họ phân phối và Ba vai trò trong Suy diễn Bayes

Để đọc và chọn phân phối thành thạo trong mô hình hóa Bayes, hãy gắn kết ba trụ cột sau:

- **Rời rạc (PMF) và Liên tục (PDF):** Với biến rời rạc, $$P(X = x)$$ là xác suất thực sự tại điểm $$x$$. Với biến liên tục, hàm mật độ $$f(x)$$ có thể lớn hơn 1 (ví dụ $$\text{Uniform}(0, 0.5)$$ có $$f(x) = 2$$); chỉ có **tích phân trên một khoảng** $$\int_a^b f(x)\,dx$$ mới là xác suất.
- **Khớp miền giá trị (Support Matching):** Chọn phân phối trước hết là khớp miền giá trị của đại lượng cần mô hình hóa: $$[0, 1]$$ cho tỷ lệ (Beta), $$(0, \infty)$$ cho tốc độ/phương sai (Gamma, Exponential, Log-Normal), $$\{0, 1, 2, \dots\}$$ cho số đếm (Poisson, Negative Binomial) và $$(-\infty, \infty)$$ cho giá trị thực không chặn (Normal, Student-$$t$$).
- **Ba vai trò trong một mô hình Bayes:** Cùng một hệ phân phối có thể xuất hiện ở ba tầng: **Prior** (niềm tin về tham số), **Likelihood** (cơ chế sinh dữ liệu khi biết tham số) và **Posterior / Posterior Predictive** (niềm tin và dự báo sau khi thấy dữ liệu).

---

## Mở đầu: vì sao một con số thường là chưa đủ?

Giả sử bạn phụ trách theo dõi hiệu quả của một nút mua hàng mới trên website. Ở tuần 1, bạn ghi nhận 25 đơn hàng trên 100 lượt truy cập; ở tuần 2, bạn ghi nhận 250 đơn hàng trên 1000 lượt truy cập.

Cả hai tuần đều cho tỷ lệ chuyển đổi là $$25\%$$. Nếu chỉ nhìn vào **ước lượng điểm**, ta sẽ xem hai tuần là như nhau. Tuy nhiên, trực giác cho thấy điều đó không chính xác: ở tuần 2, ta chắc chắn hơn nhiều rằng tỷ lệ thực sự nằm gần $$25\%$$; còn ở tuần 1, cỡ mẫu nhỏ nên các giá trị lân cận như $$18\%$$ hay $$32\%$$ vẫn hoàn toàn khả dĩ. Chính vì vậy, thống kê Bayes không dừng lại ở câu “ước lượng là $$0.25$$”, mà làm việc với một đối tượng giàu thông tin hơn: **phân phối xác suất**.

![Bản đồ niềm tin của phân phối]({{ site.baseurl }}/img/chapter_img/chapter02/distribution_belief_map.png)

## 1. Phân phối xác suất là gì?

Nói một cách trực quan, phân phối xác suất là **bản đồ niềm tin** trên tập các giá trị có thể xảy ra. Khi một giá trị được gán xác suất hoặc mật độ cao, điều đó thể hiện rằng giá trị ấy phù hợp hơn với kiến thức sẵn có, được dữ liệu ủng hộ mạnh hơn, hoặc cả hai.

Trong thống kê Bayes, phân phối không chỉ mô tả dữ liệu mà còn biểu diễn độ bất định về tham số chưa biết (chẳng hạn $$\theta$$ là tỷ lệ khách mua hàng), về dữ liệu tương lai (như số đơn hàng tuần tới), hay về các đại lượng cần dự đoán (như chiều cao trung bình của một lớp học).

### Cách đọc một phân phối trong thực hành

Khi nhìn vào một phân phối, bạn có thể tự đặt ba câu hỏi: giá trị trung tâm hợp lý nhất nằm ở đâu, mức độ chắc chắn cao hay thấp, và các giá trị cực đoan có còn đáng kể hay không. Ba câu hỏi này biến một đồ thị xác suất thành công cụ hỗ trợ tư duy và ra quyết định.

## 2. Rời rạc và liên tục: hai dạng bất định phổ biến

### 2.1. Phân phối rời rạc

Ta dùng phân phối rời rạc khi đại lượng chỉ nhận một tập giá trị đếm được, chẳng hạn số sinh viên vắng học hôm nay, số thư rác nhận được trong 1 giờ, hay số mặt ngửa trong 10 lần tung đồng xu. Khi đó ta làm việc với hàm khối xác suất:

$$
P(X = x).
$$

Ví dụ, nếu $$X$$ là số lượt khách hàng nhấp vào quảng cáo, thì $$P(X=3)$$ là xác suất xảy ra đúng 3 lượt nhấp.

### 2.2. Phân phối liên tục

Ta dùng phân phối liên tục khi đại lượng có thể nhận vô số giá trị trên một khoảng, ví dụ như chiều cao, thời gian giao hàng, nhiệt độ, hay tỷ lệ chuyển đổi thực sự của một quảng cáo. Lúc này ta làm việc với hàm mật độ $$p(x)$$. Với biến ngẫu nhiên liên tục, xác suất tại đúng một điểm đơn lẻ bằng 0; đại lượng có ý nghĩa là xác suất rơi vào một khoảng:

$$
P(a < X < b) = \int_a^b p(x)\,dx.
$$

Ví dụ, thay vì hỏi “xác suất thời gian giao hàng đúng bằng 32.000 phút là bao nhiêu?”, ta hỏi “xác suất thời gian giao hàng nằm trong khoảng từ 30 đến 35 phút là bao nhiêu?”.

## 3. Cùng trung bình nhưng khác mức độ chắc chắn

Đây là điểm giúp người học thấy rõ giá trị của việc làm việc với cả phân phối. Giả sử hai người cùng nhận định: “Tôi cho rằng tỷ lệ khách hàng mua hàng khoảng $$0.25$$”, nhưng họ biểu diễn niềm tin bằng hai phân phối tiền nghiệm khác nhau: người A dùng Beta$$(3,9)$$ còn người B dùng Beta$$(30,90)$$.

Cả hai phân phối đều có cùng kỳ vọng:

$$
\frac{\alpha}{\alpha+\beta} = \frac{1}{4}.
$$

Tuy nhiên, ý nghĩa của chúng rất khác nhau. Beta$$(3,9)$$ trải khá rộng, tương ứng với phát biểu “tôi nghĩ trung tâm nằm quanh $$0.25$$, nhưng vẫn để ngỏ nhiều khả năng lân cận”; ngược lại, Beta$$(30,90)$$ tập trung hẹp hơn nhiều, thể hiện rằng “tôi khá chắc chắn giá trị thực không lệch xa $$0.25$$”. Một con số trung bình đơn lẻ không phản ánh được sự khác biệt này, còn phân phối xác suất thì thể hiện rất rõ.

![Phân phối hẹp thể hiện mức chắc chắn cao]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_narrow_distribution.png)

![Phân phối rộng thể hiện mức chưa chắc chắn cao hơn]({{ site.baseurl }}/img/chapter_img/chapter02/chapter02_wide_distribution.png)

## 4. Ba vai trò của phân phối trong thống kê Bayes

Trong Chương 2, bạn sẽ gặp phân phối xác suất ở ba vị trí chính.

### 4.1. Prior (Tiền nghiệm)

Prior $$P(\theta)$$ mô tả niềm tin về tham số **trước khi** quan sát dữ liệu hiện tại. Ví dụ, trước khi chạy chiến dịch quảng cáo mới, nhóm tiếp thị có thể tin rằng tỷ lệ mua hàng thường nằm trong khoảng $$2\%$$ đến $$5\%$$; hoặc trước khi kiểm thử dây chuyền mới, kỹ sư có thể tin rằng tỷ lệ lỗi khó vượt quá $$10\%$$.

### 4.2. Likelihood (Hàm hợp lý)

Likelihood $$P(D \mid \theta)$$ mô tả mức độ hợp lý của dữ liệu quan sát được nếu tham số thực sự bằng $$\theta$$. Ví dụ, nếu tỷ lệ mở email thực là $$0.4$$ thì việc quan sát 41 email được mở trên 100 email gửi đi là khá hợp lý; còn nếu tỷ lệ thực chỉ là $$0.05$$ thì dữ liệu đó rất khó xảy ra.

### 4.3. Posterior (Hậu nghiệm)

Posterior $$P(\theta \mid D)$$ là niềm tin **sau khi** kết hợp prior với dữ liệu thông qua định lý Bayes:

$$
P(\theta \mid D) = \frac{P(D \mid \theta)P(\theta)}{P(D)}.
$$

Nói gọn lại, prior là điểm xuất phát, likelihood là tiếng nói của dữ liệu, còn posterior là niềm tin đã được cập nhật sau khi kết hợp hai nguồn thông tin đó.

## 5. Cách đọc hình dạng của một phân phối

Khi quan sát đồ thị của một phân phối, bạn nên rèn thói quen kiểm tra bốn đặc trưng sau.

### 5.1. Trung tâm

Trung tâm cho biết vùng giá trị hợp lý nhất. Ví dụ, một phân phối tập trung quanh $$0.7$$ cho thấy tỷ lệ thành công khả dĩ nhất đang ở mức cao, còn phân phối tập trung quanh $$170$$ cho thấy chiều cao trung bình hợp lý nhất vào khoảng 170 cm.

### 5.2. Độ rộng

Độ rộng phản ánh mức độ bất định: phân phối hẹp cho thấy ta khá chắc chắn, còn phân phối rộng cho thấy độ mơ hồ vẫn còn lớn. Chẳng hạn, nếu 5 ngày đo nhiệt độ trong phòng máy chủ đều cho kết quả ổn định thì posterior sẽ hẹp; ngược lại, nếu mới đo trong 2 ngày đầu, posterior thường vẫn còn rộng.

### 5.3. Độ lệch

Phân phối có thể lệch trái hoặc lệch phải, đặc biệt thường gặp với xác suất, tỷ lệ hiếm hoặc dữ liệu đếm. Ví dụ, tỷ lệ khách trả hàng thường nhỏ nên phân phối hay lệch về phía gần 0; số cuộc gọi mỗi phút ở tổng đài cũng thường không đối xứng như phân phối chuẩn (Normal).

### 5.4. Phần đuôi

Phần đuôi cho biết các khả năng cực đoan còn đáng kể đến mức nào. Trong quyết định kinh doanh hay y khoa, phần đuôi có ý nghĩa lớn vì nó gắn với rủi ro xấu nhất. Ví dụ, một chiến dịch quảng cáo có thể có doanh thu kỳ vọng tốt nhưng đuôi trái dày, nghĩa là khả năng thua lỗ nặng chưa thể xem nhẹ; tương tự, một phác đồ điều trị có thể cho hiệu quả trung bình khá nhưng đuôi phải của tác dụng phụ lại lớn đến mức bác sĩ cần hết sức thận trọng.

## 6. Một số họ phân phối thường gặp

### 6.1. Beta: cho đại lượng nằm trong khoảng $$(0, 1)$$

Phân phối Beta phù hợp khi đại lượng cần mô tả là xác suất hoặc tỷ lệ, chẳng hạn tỷ lệ chuyển đổi, tỷ lệ qua môn, tỷ lệ sản phẩm lỗi, tỷ lệ bệnh nhân hồi phục, tỷ lệ nhấp quảng cáo hay xác suất đồng xu ra mặt ngửa.

![Họ phân phối Beta với nhiều hình dạng khác nhau]({{ site.baseurl }}/img/chapter_img/chapter02/beta_distribution_family.png)

### 6.2. Binomial (Nhị thức): đếm số lần thành công trong $$n$$ lần thử

Phân phối Binomial dùng khi có $$n$$ phép thử độc lập, mỗi phép thử chỉ có hai kết quả (thành công hoặc thất bại), và ta đếm tổng số lần thành công — ví dụ như số khách mua hàng trong $$n$$ lượt truy cập, số sinh viên qua môn trong lớp 40 người, hay số email được mở trong 100 email đã gửi.

### 6.3. Poisson: đếm số sự kiện trong một khoảng

Phân phối Poisson phù hợp với dữ liệu đếm như số cuộc gọi đến trong 1 giờ, số đơn hàng trong 10 phút, hay số lỗi hệ thống mỗi ngày. Họ phân phối này đặc biệt hữu ích khi ta quan tâm đến **tốc độ (cường độ) xảy ra sự kiện**.

### 6.4. Normal (Chuẩn): cho đại lượng liên tục xoay quanh một trung tâm

Phân phối Normal thường gặp với chiều cao, điểm số, sai số đo lường hay thời gian hoàn thành một tác vụ khi có nhiều nguồn dao động nhỏ cộng gộp lại.

### 6.5. Vai trò của hàm Gamma trong các phân phối liên hợp

Khi học về prior liên hợp ở Bài 2.5, bạn sẽ thấy hai họ Beta và Gamma xuất hiện rất thường xuyên. Cả hai đều có hằng số chuẩn hóa biểu diễn qua hàm Gamma:

$$
\Gamma(a)=\int_0^{\infty} x^{a-1}e^{-x}dx,
$$

trong đó với số nguyên dương $$n$$ thì $$\Gamma(n)=(n-1)!$$. Nhờ đó, ta viết được dạng tỉ lệ (hạt nhân):

$$
\text{Beta}(\alpha,\beta)\propto \theta^{\alpha-1}(1-\theta)^{\beta-1},\quad 0<\theta<1,
$$

$$
\text{Gamma}(\alpha,\beta)\propto \lambda^{\alpha-1}e^{-\beta\lambda},\quad \lambda>0,
$$

theo tham số hóa shape–rate (hình dạng – tốc độ). Điểm chính cần nhớ là hàm Gamma đóng vai trò chuẩn hóa giúp hai họ phân phối này có tích phân bằng 1 và cho phép cập nhật tham số gọn gàng trong các cặp liên hợp.

### 6.6. Bảng tóm tắt hằng số chuẩn hóa của các họ phân phối phổ biến

Trong thực hành, ta thường viết phần “hạt nhân” (kernel) trước rồi bổ sung hằng số chuẩn hóa để thu được phân phối hợp lệ.

| Họ phân phối | Miền giá trị | Dạng chuẩn hóa | Hằng số chuẩn hóa chính |
|---|---|---|---|
| Bernoulli$$(p)$$ | $$x\in\{0,1\}$$ | $$P(X=x)=p^x(1-p)^{1-x}$$ | Tổng trên $$x=0,1$$ tự bằng 1 |
| Binomial$$(n,p)$$ | $$k=0,\dots,n$$ | $$P(K=k)=\binom{n}{k}p^k(1-p)^{n-k}$$ | $$\binom{n}{k}$$ (đếm số cách) |
| Poisson$$(\lambda)$$ | $$k=0,1,2,\dots$$ | $$P(Y=k)=\frac{\lambda^k e^{-\lambda}}{k!}$$ | $$e^{-\lambda}$$ và $$k!$$ |
| Normal$$(\mu,\sigma^2)$$ | $$x\in\mathbb{R}$$ | $$f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$ | $$\frac{1}{\sigma\sqrt{2\pi}}$$ |
| Exponential$$(\lambda)$$ | $$t\ge 0$$ | $$f(t)=\lambda e^{-\lambda t}$$ | $$\lambda$$ |
| Gamma$$(\alpha,\beta)$$ (shape-rate) | $$\lambda>0$$ | $$f(\lambda)=\frac{\beta^\alpha}{\Gamma(\alpha)}\lambda^{\alpha-1}e^{-\beta\lambda}$$ | $$\frac{\beta^\alpha}{\Gamma(\alpha)}$$ |
| Beta$$(\alpha,\beta)$$ | $$\theta\in(0,1)$$ | $$f(\theta)=\frac{1}{B(\alpha,\beta)}\theta^{\alpha-1}(1-\theta)^{\beta-1}$$ | $$\frac{1}{B(\alpha,\beta)}$$, với $$B=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$$ |

Lưu ý: khi dùng ký hiệu $$\propto$$, ta đang làm việc với phần chưa chuẩn hóa; khi cần xác suất hoặc mật độ có tổng (hay tích phân) bằng 1, ta phải nhân thêm hằng số chuẩn hóa.

### 6.7. Miền tham số và quy ước tham số hóa

Để tránh nhầm lẫn khi đọc các công thức liên hợp:

- Beta dùng cho tham số xác suất $$\theta\in(0,1)$$.
- Gamma dùng cho tham số dương $$\lambda>0$$ (tốc độ hoặc cường độ).
- Normal thường dùng cho trung bình $$\mu\in\mathbb{R}$$ của dữ liệu liên tục.

Riêng với phân phối Gamma, cần luôn ghi rõ cách tham số hóa. Trong khóa học này, ta mặc định dùng tham số hóa shape–rate:

$$
E[\lambda]=\frac{\alpha}{\beta},\qquad \mathrm{Var}(\lambda)=\frac{\alpha}{\beta^2}.
$$

Nếu tham khảo tài liệu dùng tham số hóa shape–scale, bạn cần quy đổi tham số về cùng một hệ để tránh sai lệch kết quả số.

### 6.8. Lưu ý về xấp xỉ Normal

Trong thực hành, ta thường gặp xấp xỉ Normal cho tổng nhiều biến ngẫu nhiên hoặc cho một posterior đủ tập trung:

- **Hợp lý hơn** khi cỡ mẫu đủ lớn, phân phối không quá lệch và tham số không nằm sát biên.
- **Kém hợp lý** với tỷ lệ quá gần 0 hoặc 1, dữ liệu đếm rất nhỏ, hoặc posterior lệch mạnh.

Chẳng hạn với posterior Beta, xấp xỉ Normal thường chấp nhận được khi cả hai tham số hậu nghiệm đều không quá nhỏ (thực hành hay dùng quy tắc kinh nghiệm $$\alpha_{post},\beta_{post}>5$$) và khối lượng xác suất không dồn sát về 0 hoặc 1.

## 7. Vì sao Bayes giữ toàn bộ phân phối thay vì một con số?

Khi giữ lại toàn bộ phân phối, ta có thể trả lời nhiều câu hỏi thực tế hơn hẳn. Chẳng hạn, với posterior của tỷ lệ hoàn thành khóa học trực tuyến, ta có thể tính xác suất tỷ lệ hoàn thành vượt $$60\%$$, xác định khoảng giá trị hợp lý nhất của tỷ lệ đó, hoặc dự báo khoảng số người hoàn thành nếu mời thêm 100 học viên mới. Nếu chỉ có một ước lượng điểm duy nhất như $$0.58$$, ta không thể trả lời nghiêm túc các câu hỏi đó.

## 8. Minh họa qua ba bối cảnh thực tế

### 8.1. Kinh doanh

Một doanh nghiệp chạy thử nghiệm A/B cho hai phiên bản trang đích (landing page). Điều họ cần không chỉ là “phiên bản B cao hơn 1.2 điểm phần trăm”, mà còn là độ bất định của ước lượng đó, xác suất B thực sự tốt hơn A, và rủi ro còn lại nếu triển khai đại trà.

### 8.2. Giáo dục

Một giảng viên muốn đánh giá tỷ lệ sinh viên qua môn ở khóa mới. Khi lớp chỉ có 18 sinh viên, độ bất định là rất lớn; báo cáo một phân phối posterior sẽ trung thực hơn nhiều so với việc chỉ nêu con số “tỷ lệ qua môn là $$72\%$$”.

### 8.3. Y tế

Một bác sĩ theo dõi tỷ lệ đáp ứng của phác đồ điều trị mới. Với 12 bệnh nhân đầu tiên, mọi kết luận chắc chắn đều còn quá sớm; phân phối xác suất cho phép bác sĩ nêu rõ vùng giá trị hợp lý hiện tại thay vì một con số tạo cảm giác chính xác quá mức.

## 9. Những ngộ nhận phổ biến

### 9.1. “Phân phối chỉ là đồ thị minh họa”

Không đúng. Phân phối chứa toàn bộ thông tin về giá trị trung tâm, độ bất định, rủi ro ở hai đuôi và xác suất của các giả thuyết cụ thể mà ta quan tâm.

### 9.2. “Chỉ cần giá trị trung bình là đủ”

Không đúng. Hai phân phối có thể có cùng trung bình nhưng dẫn tới hai quyết định hoàn toàn khác nhau do độ rộng và phần đuôi khác nhau.

### 9.3. “Dữ liệu lớn rồi thì không cần phân phối”

Ngay cả khi dữ liệu rất lớn, phân phối vẫn cần thiết để diễn đạt mức độ chắc chắn, so sánh giả thuyết, dự báo dữ liệu mới và kiểm soát các rủi ro cực đoan vốn bị che khuất bởi một con số trung bình.

## Tóm tắt

**Phân phối xác suất là ngôn ngữ cốt lõi của thống kê Bayes.** Nó cho phép ta biểu diễn đồng thời giá trị hợp lý nhất, mức độ chắc chắn và khả năng xảy ra của các kịch bản cực đoan. Trong Chương 2, bạn cần ghi nhớ ba vai trò: prior là phân phối của niềm tin ban đầu, likelihood mô tả mức độ phù hợp của dữ liệu với từng giả thuyết, còn posterior là phân phối niềm tin sau khi đã cập nhật bằng dữ liệu. Nắm vững vai trò của phân phối sẽ giúp các bài học tiếp theo về likelihood, prior và posterior trở nên dễ tiếp thu hơn nhiều.

> **3 ý cần nhớ.** Phân phối luôn giàu thông tin hơn ước lượng điểm vì nó giữ lại toàn bộ độ bất định; hai phân phối có cùng trung tâm vẫn mang ý nghĩa rất khác nếu độ rộng khác nhau; và trong thống kê Bayes, prior, likelihood và posterior đều là những phân phối đảm nhận các vai trò riêng biệt trong suy luận.


## Giải thích: Đọc một phân phối qua 4 câu hỏi thay vì chỉ nhìn trung bình

Mỗi khi gặp một phân phối xác suất trong mô hình Bayes, hãy đọc chậm qua 4 câu hỏi sau:

1. **Miền giá trị (Support) là gì?** Tham số hay dữ liệu có bị chặn dương, chặn trong $$[0,1]$$, hay nhận giá trị nguyên không?
2. **Tâm phân phối ở đâu?** Trung bình, trung vị và mode có trùng nhau không (đối xứng hay lệch)?
3. **Độ phân tán và độ dày đuôi thế nào?** Hai phân phối cùng trung bình nhưng khác phương sai hoặc độ dày đuôi dẫn đến quyết định rủi ro rất khác nhau.
4. **Hàm mật độ có mang ý nghĩa vật lý/sinh dữ liệu gì?** Ví dụ: tổng $$n$$ phép thử Bernoulli sinh ra Binomial; thời gian chờ giữa các sự kiện Poisson sinh ra Exponential.

### Ví dụ tính toán làm từng bước: So sánh hai phân phối Beta có cùng trung bình $$0.5$$

Xét hai phân phối mô tả niềm tin về tỷ lệ chuyển đổi $$p \in [0, 1]$$: $$\text{Beta}(2, 2)$$ và $$\text{Beta}(20, 20)$$. Sử dụng công thức kỳ vọng $$\mu = \frac{\alpha}{\alpha+\beta}$$ và phương sai $$\sigma^2 = \frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$$:

| Phân phối | Kỳ vọng $$\mathbb{E}[p]$$ | Phương sai $$\mathrm{Var}(p)$$ | Độ lệch chuẩn $$\mathrm{SD}(p)$$ | Ý nghĩa mức độ tự tin |
| --- | --- | --- | --- | --- |
| $$\text{Beta}(2, 2)$$ | $$2 / 4 = 0.500$$ | $$\frac{4}{16 \times 5} = 0.0500$$ | $$\sqrt{0.0500} \approx 0.2236$$ | Rất mờ nhạt (tương đương chỉ 4 quan sát giả định) |
| $$\text{Beta}(20, 20)$$ | $$20 / 40 = 0.500$$ | $$\frac{400}{1600 \times 41} \approx 0.0061$$ | $$\sqrt{0.0061} \approx 0.0781$$ | Khá tập trung (tương đương 40 quan sát giả định) |

Cả hai đều có đúng trung bình $$0.500$$, nhưng độ lệch chuẩn của $$\text{Beta}(2, 2)$$ lớn gần gấp **3 lần** $$\text{Beta}(20, 20)$$. Đó là lý do chỉ báo cáo một con số trung bình là hoàn toàn không đủ trong thống kê Bayes.

**Hiểu lầm cần tránh:** Nhầm giá trị mật độ $$f(x)$$ của biến liên tục với xác suất $$P(X = x)$$. Với mọi biến liên tục, xác suất tại đúng một điểm đơn lẻ luôn bằng $$0$$, còn mật độ $$f(x)$$ hoàn toàn có thể lớn hơn $$1$$.

**Kiểm tra nhanh:** Với phân phối đều $$X \sim \text{Uniform}(0, 0.25)$$, mật độ trên đoạn $$[0, 0.25]$$ là $$f(x) = 1/0.25 = 4 > 1$$, nhưng xác suất rơi vào nửa đầu $$[0, 0.125]$$ là $$\int_0^{0.125} 4\,dx = 0.5 \in [0, 1]$$.

---

## Video tham khảo

- [The Main Ideas behind Probability Distributions](https://www.youtube.com/watch?v=oI3hZJqXJuc) — StatQuest with Josh Starmer, English. **xem trước**. Trình bày các ý tưởng cốt lõi của phân phối xác suất, phù hợp với mục tiêu đọc phân phối như một mô tả về độ bất định.
- [Random variables and probability distributions.](https://www.youtube.com/watch?v=pvkhK03aFDM) — Ben Lambert, English. Phân biệt rõ biến ngẫu nhiên rời rạc và liên tục, hỗ trợ phần lựa chọn họ phân phối.
- [Why “probability of 0” does not mean “impossible” | Probabilities of probabilities, part 2](https://www.youtube.com/watch?v=ZA4JkHKZM50) — 3Blue1Brown, English. Giải thích vì sao cần giữ toàn bộ hình dạng phân phối thay vì chỉ một điểm, gắn liền với tinh thần của thống kê Bayes.

## Câu hỏi tự luyện

1. Một lớp có 8 sinh viên và 6 người qua môn; lớp khác có 800 sinh viên và 600 người qua môn. Vì sao cùng tỷ lệ $$75\%$$ nhưng mức độ chắc chắn lại khác nhau?
2. Hãy nêu ba ví dụ biến rời rạc và ba ví dụ biến liên tục trong đời sống hoặc công việc của bạn.
3. Hai prior Beta$$(4,16)$$ và Beta$$(40,160)$$ có cùng trung bình. Chúng khác nhau ở điểm nào về mặt diễn giải?
4. Nếu bạn là quản lý một quán cà phê, đại lượng nào bạn muốn dự báo bằng **phân phối** thay vì chỉ một con số duy nhất?

## Tài liệu tham khảo

- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapter 1-2.
- Kruschke, J. *Doing Bayesian Data Analysis* (2nd ed.), Chapter 4-5.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 2.

---

*Bài học tiếp theo: [2.2 Likelihood - Câu chuyện về Dữ liệu và Mô hình]({{ site.baseurl }}/contents/vi/chapter02/02_02_likelihood/)*
