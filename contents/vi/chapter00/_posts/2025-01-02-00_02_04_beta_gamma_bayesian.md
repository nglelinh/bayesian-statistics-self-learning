---
layout: post
title: "Bài 0.5: Beta và Gamma - Phân phối cho Xác suất và Tham số Dương"
chapter: '00'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu phân phối Beta dùng để mô tả các đại lượng nằm trong đoạn $$[0,1]$$, nắm được ý nghĩa của các tham số $$\alpha,\beta$$, hiểu vai trò của phân phối Gamma cho tham số dương, và thấy rõ chức năng của hằng số chuẩn hóa trong việc tạo ra một hàm mật độ hợp lệ.

## 1) Bắt đầu từ vấn đề thực tế: mô tả một tỷ lệ chưa biết

Trong thực tế, ta thường gặp các đại lượng dạng tỷ lệ như tỷ lệ khách hàng nhấp chuột, tỷ lệ sản phẩm lỗi, hay tỷ lệ học viên hoàn thành khóa học. Các đại lượng này có chung một đặc điểm: giá trị luôn nằm giữa 0 và 1.

Để mô hình hóa chúng, ta cần một phân phối đủ linh hoạt trên đoạn $$[0,1]$$ — có thể lệch trái, lệch phải, hoặc tập trung quanh một vùng trung tâm. Đó là vai trò của phân phối Beta.

## 2) Phân phối Beta cho xác suất

Phân phối Beta được viết là:

$$
p\sim\text{Beta}(\alpha,\beta), \quad 0<p<1.
$$

Có thể hiểu nhanh rằng $$\alpha-1$$ gắn với phần nghiêng về "thành công", còn $$\beta-1$$ gắn với phần nghiêng về "thất bại". Kỳ vọng của phân phối là:

$$
\mathbb{E}[p]=\frac{\alpha}{\alpha+\beta}.
$$

Khi tổng $$\alpha+\beta$$ lớn, phân phối tập trung hẹp quanh trung bình; khi $$\alpha+\beta$$ nhỏ, phân phối dàn rộng hơn.

Hằng số chuẩn hóa của phân phối Beta là hàm Beta:

$$
B(\alpha,\beta)=\int_0^1 p^{\alpha-1}(1-p)^{\beta-1}\,dp
=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}.
$$

Do đó, hàm mật độ đầy đủ có dạng:

$$
f(p)=\frac{1}{B(\alpha,\beta)}p^{\alpha-1}(1-p)^{\beta-1},\quad 0<p<1.
$$

## 3) Hàm Gamma và cầu nối tới hàm Beta

Để biểu diễn hằng số chuẩn hóa của Beta, ta sử dụng hàm Gamma:

$$
\Gamma(z)=\int_0^{\infty} t^{z-1}e^{-t}\,dt,\quad z>0.
$$

Hàm Gamma mở rộng khái niệm giai thừa sang các số thực dương với tính chất đệ quy:

$$
\Gamma(z+1)=z\,\Gamma(z),\qquad \Gamma(n+1)=n!\;(n\in\mathbb{N}).
$$

Nhờ đó, hằng số chuẩn hóa của Beta được viết gọn thành tỷ số các hàm Gamma:

$$
B(\alpha,\beta)=\frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}.
$$

Về mặt thực hành, công thức này chuyển một tích phân chuẩn hóa khó tính trực tiếp thành tỷ số của các hàm Gamma, giúp việc tính toán ổn định và rõ cấu trúc hơn.

## 4) Phân phối Beta giải quyết vấn đề gì?

Phân phối Beta cung cấp một khuôn khổ có hệ thống để trả lời câu hỏi: "tỷ lệ thật nhiều khả năng nằm ở vùng nào trong đoạn $$[0,1]$$, và mức độ tập trung mạnh hay yếu ra sao?" Nói gọn lại:

- $$\alpha$$ và $$\beta$$ quyết định hình dạng phân phối,
- $$\frac{\alpha}{\alpha+\beta}$$ xác định vị trí trung tâm,
- $$\alpha+\beta$$ phản ánh mức độ tập trung quanh trung tâm.

Nhờ vậy, Beta không chỉ biểu diễn một con số tỷ lệ đơn lẻ mà còn thể hiện trọn vẹn độ bất định xung quanh tỷ lệ đó.

## 5) Ví dụ đọc hình dạng Beta

Nếu $$\alpha=2,\beta=5$$, mật độ nghiêng về phía gần 0; ngược lại, nếu $$\alpha=8,\beta=3$$, mật độ nghiêng về phía gần 1. Nói cách khác, cặp tham số $$\alpha,\beta$$ đồng thời kiểm soát cả vị trí lẫn độ tập trung của phân phối trên đoạn $$[0,1]$$.

![So sánh hình dạng Beta với các bộ tham số khác nhau]({{ site.baseurl }}/img/chapter_img/chapter00/beta_binomial_update_vi.png)

*Cách đọc hình: Biểu đồ cho thấy sự thay đổi của các tham số làm dịch chuyển vị trí đỉnh và co giãn độ rộng của phân phối Beta trên đoạn $$[0,1]$$.*

## 6) Phân phối Gamma cho tham số dương

Một cách tham số hóa phổ biến của phân phối Gamma là dạng shape–rate (hình dạng–tốc độ):

$$
\lambda\sim\text{Gamma}(\alpha,\beta), \quad
f(\lambda)=\frac{\beta^\alpha}{\Gamma(\alpha)}\lambda^{\alpha-1}e^{-\beta\lambda},\; \lambda>0.
$$

Kỳ vọng của phân phối là:

$$
\mathbb{E}[\lambda]=\frac{\alpha}{\beta}.
$$

Trong công thức trên, $$\frac{\beta^\alpha}{\Gamma(\alpha)}$$ là hằng số chuẩn hóa bảo đảm tổng xác suất bằng 1:

$$
\int_0^{\infty} f(\lambda)\,d\lambda=1.
$$

Nếu bỏ hệ số này, biểu thức $$\lambda^{\alpha-1}e^{-\beta\lambda}$$ mới chỉ mô tả hình dạng chứ chưa phải một hàm mật độ hợp lệ.

## 7) Ví dụ trực giác với Gamma

Với tham số hóa shape–rate:

- Khi giữ nguyên $$\alpha$$ và tăng $$\beta$$, phân phối dịch về gần 0 hơn.
- Khi tăng $$\alpha$$, phân phối có đỉnh rõ hơn và bớt lệch phải hơn.

Phân phối Gamma phù hợp để mô tả các đại lượng dương như thời gian chờ, cường độ xảy ra sự kiện, hoặc các biến có đuôi phải dài.

## 8) Dạng chưa chuẩn hóa và dạng chuẩn hóa

Trong thực hành, ta thường gặp phần lõi (kernel) của mật độ trước, chẳng hạn:

$$
g(p)=p^{\alpha-1}(1-p)^{\beta-1}.
$$

Biểu thức này chưa phải mật độ hợp lệ vì tích phân của nó trên $$[0,1]$$ không nhất thiết bằng 1. Để chuẩn hóa thành mật độ, ta chia cho hằng số chuẩn hóa tương ứng:

$$
f(p)=\frac{1}{B(\alpha,\beta)}g(p).
$$

Nguyên tắc tương tự áp dụng cho Gamma: phần lũy thừa và hàm mũ quy định hình dạng đường cong, còn hệ số phía trước bảo đảm tổng diện tích dưới đường cong bằng 1.

## 9) Mẹo thực hành

Khi sử dụng phân phối Gamma, luôn ghi rõ mình đang dùng tham số hóa shape–rate hay shape–scale. Khi đọc tài liệu khác, cần kiểm tra kỹ ký hiệu để tránh nhầm giữa tham số tốc độ (rate) $$\beta$$ và tham số tỷ lệ (scale) $$\theta=1/\beta$$.

## 10) Mở rộng từ giai thừa sang Gamma

Với số nguyên dương $$n$$, giai thừa được định nghĩa là:

$$
n!=1\cdot 2\cdot 3\cdots n.
$$

Hàm Gamma mở rộng khái niệm này sang tập số thực dương, nên ta có thể liên hệ nhanh với ký hiệu giai thừa mở rộng:

$$
x!=\Gamma(x+1),\quad x>0.
$$

Ví dụ với một số giá trị nguyên nhỏ:

$$
\Gamma(1)=1,\quad \Gamma(2)=1!,\quad \Gamma(3)=2!,\quad \Gamma(6)=5!.
$$

## 11) Giá trị đặc biệt thường gặp

Một giá trị đặc biệt rất hay gặp của hàm Gamma là:

$$
\Gamma\!\left(\frac{1}{2}\right)=\sqrt{\pi}.
$$

Áp dụng công thức đệ quy $$\Gamma(z+1)=z\,\Gamma(z)$$, ta suy ra:

$$
\Gamma\!\left(\frac{3}{2}\right)=\frac{\sqrt{\pi}}{2},
\qquad
\Gamma\!\left(\frac{5}{2}\right)=\frac{3\sqrt{\pi}}{4}.
$$

Đây cũng là lý do hằng số $$\pi$$ xuất hiện trong nhiều công thức phân phối liên tục.

## 12) Ví dụ tính hàm Beta

Với $$a,b>0$$:

$$
B(a,b)=\int_0^1 t^{a-1}(1-t)^{b-1}\,dt
=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}.
$$

Chẳng hạn, với $$a=2, b=3$$:

$$
B(2,3)=\frac{\Gamma(2)\Gamma(3)}{\Gamma(5)}=\frac{1!\,2!}{4!}=\frac{1}{12}.
$$

Ví dụ này minh họa trực tiếp vai trò của hàm Gamma trong việc tính hằng số chuẩn hóa cho phân phối Beta.

## 13) Ví dụ số cho hình dạng Beta (7/10)

Xét biểu thức theo $$\theta$$ trên đoạn $$[0,1]$$:

$$
g(\theta)=\theta^8(1-\theta)^4.
$$

Đây mới là dạng chưa chuẩn hóa. Khi chuẩn hóa, ta thu được mật độ của $$\text{Beta}(9,5)$$:

$$
f(\theta)=\frac{1}{B(9,5)}\theta^8(1-\theta)^4.
$$

![Beta-Binomial update 7 over 10]({{ site.baseurl }}/img/chapter_img/chapter00/beta_binomial_update_7of10.png)

*Cách đọc hình: Hai đường cong có cùng hình dạng tương đối; nhân thêm hệ số $$1/B(9,5)$$ chỉ điều chỉnh tỷ lệ trục tung để diện tích dưới đường cong bằng 1.*

## 14) Gợi ý tính toán số ổn định

Khi các tham số lớn, giá trị của hàm Gamma có thể vượt quá giới hạn biểu diễn số thực dấu phẩy động. Khi đó, nên tính trên thang log thay vì tính trực tiếp:

- Dùng `gammaln(z)` thay cho `log(gamma(z))`.
- Dùng `betaln(a,b)` thay cho `log(beta(a,b))`.

Trong SciPy, các hàm này nằm trong mô-đun `scipy.special` và cho độ ổn định số học cao hơn.

Ví dụ Python:

```python
from scipy.special import gamma, gammaln, beta, betaln

print(gamma(6))      # 120.0
print(gamma(0.5))    # ~1.7724538509 = sqrt(pi)
print(gammaln(100))  # log(Gamma(100))
print(beta(2, 3))    # 1/12 = 0.08333...
print(betaln(2, 3))  # log(Beta(2,3))
```

## 15) Tóm tắt nhanh

1. Phân phối Beta mô tả linh hoạt các đại lượng nằm trong $$[0,1]$$.
2. Phân phối Gamma mô tả các đại lượng nhận giá trị dương.
3. Hàm Gamma mở rộng khái niệm giai thừa: $$\Gamma(n+1)=n!$$.
4. Hàm Beta liên hệ trực tiếp với hàm Gamma qua tỷ số $$\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$$.
5. Hằng số chuẩn hóa biến một biểu thức "đúng hình dạng" thành hàm mật độ xác suất hợp lệ.

## Video tham khảo

- [The Beta distribution in 12 minutes!](https://www.youtube.com/watch?v=juF3r12nM5A) — Luis Serrano Academy, English. **Xem trước.** Giải thích cách đọc $$\alpha$$ và $$\beta$$ như số lần thành công và thất bại giả định trên đoạn $$[0,1]$$.
- [The Gamma Distribution](https://www.youtube.com/watch?v=9IIcHAJlcWc) — Steve Brunton, English. Minh họa hình dạng phân phối Gamma cho các đại lượng dương như tỷ lệ sự kiện và thời gian chờ.
- [How to Estimate Rates with a Gamma-Poisson Bayesian Model | Conjugate Priors](https://www.youtube.com/watch?v=m8roQUqmybg) — Drawing Distributions, English. Trình bày cặp liên hợp Gamma–Poisson khi ước lượng tốc độ sự kiện trong cập nhật Bayesian.

## Bài tập

**Bài 1.** Dùng công thức đệ quy để tính $$\Gamma(4)$$ và $$\Gamma(5)$$, sau đó đối chiếu với $$3!$$ và $$4!$$.

**Bài 2.** Từ $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$, suy ra $$\Gamma\!\left(\tfrac{3}{2}\right)$$ và $$\Gamma\!\left(\tfrac{5}{2}\right)$$.

**Bài 3.** Viết lại hằng số chuẩn hóa của $$\text{Beta}(a,b)$$ qua hàm Gamma và giải thích vì sao cần hằng số này để tích phân mật độ bằng 1.

**Bài 4.** Trong Python, tính `gamma(10)` và `gammaln(10)`, sau đó kiểm tra `np.log(gamma(10))` có khớp với `gammaln(10)` không.

**Bài 5.** Chứng minh nhanh $$B(a,1)=\frac{1}{a}$$ từ định nghĩa tích phân, rồi đối chiếu với công thức tỷ số hàm Gamma.

## Tài liệu tham khảo

- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. K. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.
- SciPy Special Functions: `gamma`, `gammaln`.

## Tổng kết

Beta và Gamma là hai họ phân phối nền tảng trong thống kê: Beta dành cho biến trên $$[0,1]$$, còn Gamma dành cho biến dương. Điểm cốt lõi cần nhớ là chọn đúng phân phối theo miền giá trị và hiểu vai trò của hằng số chuẩn hóa trong việc biến một phần lõi hàm thành phân phối hợp lệ.

---

*Bài học tiếp theo: [0.6 Thống kê Mô tả]({{ site.baseurl }}/contents/vi/chapter00/00_03_descriptive_statistics/)*
