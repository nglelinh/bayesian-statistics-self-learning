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

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vai trò của phân phối Normal, diễn giải chính xác hai tham số $$\mu$$ và $$\sigma$$, đồng thời vận dụng trực giác của định lý giới hạn trung tâm (CLT) để giải thích vì sao nhiều đại lượng tổng hợp có dạng gần chuẩn.

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
