---
layout: post
title: "Bài 0.4: Normal và Trực giác CLT - Khi nào Dữ liệu có dạng Chuông?"
chapter: '00'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

Tại sao chiều cao của hàng nghìn sinh viên, sai số đo đạc thiên văn của Carl Friedrich Gauss năm 1809, và nhiễu nhiệt trong mạch điện tử — ba hiện tượng hoàn toàn không liên quan — lại cùng vẽ nên đúng một đường cong hình chuông? Câu trả lời không phải là sự trùng hợp ngẫu nhiên, mà là **Định lý Giới hạn Trung tâm (CLT)**: bất cứ khi nào một đại lượng là tổng của nhiều tác động nhỏ, độc lập, phân phối của nó sẽ tự động bị "hút" về phân phối Chuẩn (*Normal*).

Trong thống kê Bayes, phân phối Chuẩn giữ hai vai trò tối quan trọng: vừa là mô hình chuẩn mực cho dữ liệu liên tục và prior liên hợp Normal–Normal, vừa là đích đến tiệm cận của hầu hết phân phối hậu nghiệm khi cỡ mẫu lớn (định lý Bernstein–von Mises và xấp xỉ Laplace).

---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vai trò của phân phối Normal, diễn giải chính xác hai tham số $$\mu$$ và $$\sigma$$, đồng thời vận dụng trực giác của định lý giới hạn trung tâm (CLT) để giải thích vì sao nhiều đại lượng tổng hợp có dạng gần chuẩn.

## Kiến thức cần nhớ: Entropy cực đại, Định lý Giới hạn Trung tâm và Cập nhật Normal–Normal

Nhìn ở bậc đại học trở lên, sự thống trị của phân phối Chuẩn đến từ ba trụ cột lý thuyết:

- **Lý thuyết thông tin (Maximum Entropy):** Trong tất cả các phân phối liên tục trên $$(-\infty, +\infty)$$ có cùng trung bình $$\mu$$ và phương sai $$\sigma^2$$, phân phối Chuẩn có **entropy lớn nhất** — tức là phân phối "ít giả định thừa nhất" khi bạn chỉ biết trung tâm và độ phân tán.
- **Lý thuyết giới hạn (CLT & Laplace Approximation):** Không chỉ tổng các biến ngẫu nhiên hội tụ về Chuẩn, mà ngay cả log-posterior $$\log p(	heta \mid y)$$ quanh đỉnh cực đại (MAP) khi khai triển Taylor bậc 2 cũng cho một parabol úp ngược — đồng nghĩa posterior gần đỉnh xấp xỉ một phân phối Chuẩn. Đây là nền tảng của xấp xỉ Laplace và nhiều biến thể Variational Inference.
- **Cầu nối sang Prior liên hợp (Normal–Normal):** Khi dữ liệu tuân theo $$y_i \sim \mathcal{N}(\mu, \sigma^2)$$ (biết $$\sigma^2$$) và prior là $$\mu \sim \mathcal{N}(\mu_0, 	au_0^2)$$, hậu nghiệm của $$\mu$$ vẫn là phân phối Chuẩn với **độ chính xác cộng dồn** (precision $$= 1/	ext{variance}$$).

---

## 1) Phân phối Normal là gì?

Với một biến ngẫu nhiên liên tục $$X$$ tuân theo phân phối Normal:

$$
X\sim\mathcal{N}(\mu,\sigma^2),
$$

hàm mật độ xác suất có dạng:

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

Trong đó, $$\mu$$ xác định vị trí trung tâm của phân phối, còn $$\sigma$$ đo độ phân tán quanh trung tâm đó. Một quy tắc ước lượng nhanh thường dùng là khoảng $$\mu\pm\sigma$$ chứa xấp xỉ 68% khối lượng xác suất, khoảng $$\mu\pm 2\sigma$$ chứa xấp xỉ 95%, và khoảng $$\mu\pm 3\sigma$$ chứa xấp xỉ 99.7%.

![Quy tắc 68-95-99.7 của phân phối Normal]({{ site.baseurl }}/img/chapter_img/chapter00/normal_distribution_rule.png)

*Cách đọc hình: Đường cong chuông minh họa quy tắc 68–95–99.7 quanh giá trị trung tâm $$\mu$$; mỗi dải màu thể hiện phần diện tích xác suất ứng với 1, 2 và 3 độ lệch chuẩn $$\sigma$$.*

## 2) Vì sao Normal xuất hiện nhiều?

Định lý giới hạn trung tâm (CLT) cho biết khi cộng hoặc lấy trung bình nhiều thành phần nhiễu độc lập, đại lượng tổng hợp thường tiến gần dạng phân phối chuẩn, ngay cả khi từng thành phần riêng lẻ không có dạng chuẩn. Nhờ tính chất này, nhiều đại lượng trong thực tế như sai số đo lường, điểm trung bình hay tổng tác động của nhiều yếu tố nhỏ thường phân bố gần dạng Normal.

![CLT làm phân phối của trung bình mẫu dần trở nên tròn và hẹp hơn]({{ site.baseurl }}/img/chapter_img/chapter00/clt_sample_means_overlay.png)

*Cách đọc hình: Các đường cong chồng lớp cho thấy khi cỡ mẫu tăng lên, phân phối của trung bình mẫu dần đối xứng dạng chuông và thu hẹp quanh kỳ vọng chung.*

## 3) Hằng số chuẩn hóa của Normal đến từ đâu?

Xét lại hàm mật độ Normal:

$$
f(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).
$$

Hệ số $$\frac{1}{\sigma\sqrt{2\pi}}$$ là hằng số chuẩn hóa bảo đảm tổng diện tích dưới đường cong bằng 1:

$$
\int_{-\infty}^{\infty} f(x)\,dx=1.
$$

Đặt biến chuẩn hóa $$z=\frac{x-\mu}{\sigma}$$, ta có:

$$
\int_{-\infty}^{\infty} f(x)\,dx
=\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz
=1.
$$

Nhờ hệ số này, toàn bộ khối lượng xác suất dưới đường cong chuông bằng đúng 1, giúp $$f(x)$$ trở thành một hàm mật độ hợp lệ.

## 4) Ví dụ trực giác

Giả sử điểm kiểm tra cuối kỳ chịu tác động đồng thời của nhiều yếu tố nhỏ như chất lượng giấc ngủ, mức độ ôn tập, độ khó từng câu hỏi và trạng thái tâm lý khi làm bài. Mỗi yếu tố chỉ gây biến thiên nhỏ, nhưng khi cộng gộp lại, phân phối điểm tổng thường có dạng gần hình chuông. Vì lý do đó, dùng mô hình Normal cho sai số hoặc cho điểm tổng hợp là lựa chọn hợp lý trong nhiều bối cảnh.

### 4.1) Một cách đọc nhanh bằng độ lệch chuẩn

Giả sử chiều cao của một nhóm người được xấp xỉ bởi:

$$
X \sim \mathcal{N}(170, 6^2).
$$

Ta có thể ước lượng nhanh mà chưa cần tra bảng hay tính tích phân:

- Khoảng $$164$$ đến $$176$$ cm tương ứng $$\mu \pm 1\sigma$$, chứa xấp xỉ 68% quan sát.
- Khoảng $$158$$ đến $$182$$ cm tương ứng $$\mu \pm 2\sigma$$, chứa xấp xỉ 95% quan sát.

Do đó, một người cao $$182$$ cm không phải trường hợp quá bất thường, mà chỉ nằm gần biên trên của vùng 95%.

## 5) Khi nào không nên dùng Normal?

Phân phối Normal không phù hợp khi dữ liệu bị giới hạn miền (chẳng hạn xác suất nằm trong $$[0,1]$$ hoặc thời gian chờ luôn dương), khi dữ liệu là số đếm nguyên không âm, hoặc khi phân phối bị lệch mạnh, có đuôi dày hay chứa nhiều giá trị ngoại lai (outlier). Trong các trường hợp này, giả định Normal có thể làm sai lệch đáng kể khoảng bất định.

## 6) Liên hệ Bayesian

Trong mô hình hóa Bayesian, phân phối Normal xuất hiện ở nhiều vai trò khác nhau: làm hàm hợp lý (likelihood) cho dữ liệu liên tục, làm phân phối tiên nghiệm (prior) cho các hệ số hồi quy, hoặc đóng vai trò xấp xỉ tiện lợi cho phân phối hậu nghiệm (posterior) khi cỡ mẫu đủ lớn. Tuy vậy, quy trình phân tích Bayesian luôn yêu cầu kiểm tra lại giả định mô hình thay vì mặc định gán Normal cho mọi dữ liệu liên tục.

## Giải thích: Cơ chế "cộng độ chính xác" trong cập nhật Normal–Normal bằng tay

Nếu bạn đã quen viết phân phối Chuẩn theo phương sai $$\sigma^2$$, cập nhật Bayes trông khá rắc rối. Bí quyết để mọi thứ trở nên trong suốt là chuyển sang **độ chính xác (*precision*)** — nghịch đảo của phương sai:

1. **Định nghĩa độ chính xác:** Prior có độ chính xác $$\lambda_0 = rac{1}{	au_0^2}$$; trung bình mẫu $$ar{y}$$ từ $$n$$ quan sát có phương sai $$\sigma^2/n$$, nên độ chính xác của dữ liệu là $$\lambda_{	ext{data}} = rac{n}{\sigma^2}$$.
2. **Độ chính xác hậu nghiệm là phép cộng đơn thuần:** $$\lambda_{	ext{post}} = \lambda_0 + \lambda_{	ext{data}}$$. Có thêm dữ liệu luôn làm độ chính xác tăng lên (phương sai hậu nghiệm thu nhỏ lại).
3. **Trung bình hậu nghiệm là trung bình có trọng số theo độ chính xác:**
   $$\mu_{	ext{post}} = rac{\lambda_0 \mu_0 + \lambda_{	ext{data}} ar{y}}{\lambda_0 + \lambda_{	ext{data}}}.$$
4. **Trực giác kéo co:** Ai có độ chính xác cao hơn (phương sai nhỏ hơn) sẽ kéo trung bình hậu nghiệm về phía mình mạnh hơn.

### Ví dụ tính toán làm từng bước: Đo tốc độ phản ứng của một cảm biến mới

Nhà sản xuất cho biết thời gian trễ trung bình $$\mu$$ của dòng cảm biến này quanh mức $$\mu_0 = 50	ext{ ms}$$ với độ lệch chuẩn tiên nghiệm $$	au_0 = 4	ext{ ms}$$ ($$	au_0^2 = 16$$). Sai số đo mỗi lần thử đã biết là $$\sigma = 6	ext{ ms}$$ ($$\sigma^2 = 36$$). Bạn đo $$n = 9$$ lần và thu được trung bình mẫu $$ar{y} = 44	ext{ ms}$$.

- **Bước 1 — Tính độ chính xác của prior và dữ liệu:**
  - Prior: $$\lambda_0 = rac{1}{4^2} = rac{1}{16} = 0.0625$$.
  - Dữ liệu: $$\lambda_{	ext{data}} = rac{n}{\sigma^2} = rac{9}{36} = rac{1}{4} = 0.2500$$.
- **Bước 2 — Độ chính xác và phương sai hậu nghiệm:**
  - $$\lambda_{	ext{post}} = 0.0625 + 0.2500 = 0.3125 = rac{5}{16}$$.
  - Phương sai hậu nghiệm: $$	au_{	ext{post}}^2 = rac{1}{0.3125} = 3.2 \implies 	au_{	ext{post}} = \sqrt{3.2} pprox 1.79	ext{ ms}$$.
- **Bước 3 — Trung bình hậu nghiệm:**
  $$\mu_{	ext{post}} = rac{0.0625 	imes 50 + 0.2500 	imes 44}{0.3125} = rac{3.125 + 11.0}{0.3125} = rac{14.125}{0.3125} = 45.2	ext{ ms}.$$
  Nhận xét: Vì $$\lambda_{	ext{data}}$$ gấp 4 lần $$\lambda_0$$, dữ liệu chiếm trọng số $$4/5 = 80\%$$ và prior chiếm $$1/5 = 20\%$$: $$0.2 	imes 50 + 0.8 	imes 44 = 10 + 35.2 = 45.2	ext{ ms}$$!

**Hiểu lầm cần tránh:** Giả định mọi dữ liệu đều chuẩn khi phân phối thực tế có **đuôi nặng** (*heavy tails*, nhiều ngoại lai). Với dữ liệu có ngoại lai, likelihood Chuẩn sẽ bị kéo lệch mạnh; trong Bayes ta thường thay bằng phân phối Student-$$t$$.

**Kiểm tra nhanh:** Khoảng tin cậy Bayes 95% (95% credible interval) của $$\mu$$ trong ví dụ trên là $$45.2 \pm 1.96 	imes 1.79 pprox [41.7, 48.7]	ext{ ms}$$, hẹp hơn hẳn khoảng tiên nghiệm $$50 \pm 1.96 	imes 4 = [42.2, 57.8]	ext{ ms}$$.

---

## Video tham khảo

- [The Normal Distribution, Clearly Explained!!!](https://www.youtube.com/watch?v=rzFX5NWojp0) — StatQuest with Josh Starmer, English. **Xem trước.** Giải thích trực quan cách đọc $$\mu$$ và $$\sigma$$ trên đường cong chuông.
- [But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) — 3Blue1Brown, English. Minh họa trực giác vì sao trung bình của nhiều biến độc lập tiến gần phân phối chuẩn.
- [Định lý giới hạn trung tâm (Central limit theorem)](https://www.youtube.com/watch?v=Sm2yBx3Jn6c) — Bài Học 10 Phút, Tiếng Việt. Video tiếng Việt ngắn gọn giúp đối chiếu trực tiếp với lập luận CLT trong bài.

## Câu hỏi tự luyện

1. Nêu một đại lượng liên tục phù hợp để mô hình hóa bằng phân phối Normal và giải thích lý do.
2. Nêu một đại lượng liên tục nhưng không nên dùng phân phối Normal, đồng thời đề xuất phân phối thay thế.
3. Định lý giới hạn trung tâm (CLT) giúp ích gì cho trực giác về phân phối của trung bình mẫu?

---

*Bài học tiếp theo: [0.5 Beta và Gamma]({{ site.baseurl }}/contents/vi/chapter00/00_02_04_beta_gamma_bayesian/)*
