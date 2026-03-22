---
layout: post
title: "Bài 0.13: Giới thiệu Hàm Gamma và Beta"
chapter: '00'
order: 13
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu hàm Gamma là gì, vì sao nó là phần mở rộng tự nhiên của giai thừa sang số thực, và tại sao hàm này xuất hiện liên tục trong thống kê Bayesian (Beta, Gamma, Dirichlet, Student-t, ...).

## 1) Động cơ: Từ giai thừa đến số không nguyên

Với số nguyên dương, giai thừa được định nghĩa bởi:

$$n! = 1 \cdot 2 \cdot 3 \cdots n$$

Ví dụ: $$5! = 120$$.

Nhưng nếu ta hỏi $$\left(\frac{1}{2}\right)!$$ thì sao? Định nghĩa giai thừa thông thường không còn dùng được. Hàm Gamma được xây dựng để trả lời câu hỏi này một cách nhất quán.

Nói ngắn gọn và chính xác ở mức nhập môn: **hàm Gamma là mở rộng của giai thừa cho số không nguyên dương**. Cụ thể hơn, với mọi $$x>0$$ ta có thể viết:

$$x! = \Gamma(x+1)$$

## 2) Định nghĩa hàm Gamma

Với $$z > 0$$, hàm Gamma được định nghĩa:

$$\Gamma(z) = \int_0^{\infty} t^{z-1} e^{-t} \, dt$$

Đây là một tích phân luôn dương và hội tụ khi $$z > 0$$. Có thể xem $$\Gamma(z)$$ như một “hằng số chuẩn hóa” rất quan trọng trong nhiều phân phối xác suất.

## 3) Liên hệ cốt lõi với giai thừa

Tính chất nền tảng nhất:

$$\Gamma(z+1) = z\,\Gamma(z)$$

Nếu thế $$z=n$$ (số nguyên dương), ta có:

$$\Gamma(n+1) = n!$$

Ví dụ:

Chẳng hạn, ta có $$\Gamma(1)=1$$, $$\Gamma(2)=1!=1$$, $$\Gamma(3)=2!=2$$, và $$\Gamma(6)=5!=120$$.

Vì vậy, khi làm việc với số nguyên, Gamma “khớp” hoàn hảo với giai thừa quen thuộc.

## 4) Giá trị đặc biệt: $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$

Một kết quả nổi tiếng:

$$\Gamma\!\left(\frac{1}{2}\right)=\sqrt{\pi}$$

Từ đó:

$$\Gamma\!\left(\frac{3}{2}\right)=\frac{1}{2}\Gamma\!\left(\frac{1}{2}\right)=\frac{\sqrt{\pi}}{2}$$

$$\Gamma\!\left(\frac{5}{2}\right)=\frac{3}{2}\Gamma\!\left(\frac{3}{2}\right)=\frac{3\sqrt{\pi}}{4}$$

Điểm này giải thích vì sao $$\pi$$ xuất hiện trong nhiều công thức phân phối liên tục.

## 5) Hàm Beta: người bạn đi cùng hàm Gamma

Để đi từ Gamma đến các prior trên xác suất, ta cần thêm một nhân vật trung tâm: **hàm Beta**.

![Gamma va Beta relation]({{ site.baseurl }}/img/chapter_img/chapter00/gamma_beta_intro_illustration.png)
*Hình 1: Bên trái, $$\Gamma(x)$$ mở rộng giai thừa từ điểm nguyên sang trục số thực dương. Bên phải, hàm Beta là diện tích dưới đường $$t^{a-1}(1-t)^{b-1}$$ trên $$[0,1]$$, và diện tích này trở thành hằng số chuẩn hóa cho phân phối Beta.*

Với $$a,b>0$$, hàm Beta được định nghĩa bởi tích phân:

$$
B(a,b)=\int_0^1 t^{a-1}(1-t)^{b-1}\,dt
$$

Đây không phải là "phân phối Beta" ngay lập tức, mà là một **hằng số chuẩn hóa**. Phân phối Beta sẽ dùng chính hằng số này để bảo đảm mật độ tích phân bằng 1.

### 5.1 Cầu nối Gamma-Beta

Đẳng thức cốt lõi:

$$
B(a,b)=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}
$$

Công thức này rất quan trọng vì:

Nó biến một tích phân khó thành tỉ số các hàm Gamma đã biết, giúp việc tính toán trên máy trở nên gọn hơn, đồng thời làm lộ ra rất rõ cấu trúc liên hợp của cặp Beta-Binomial.

Một vài hệ quả cơ bản:

Hai hệ quả cơ bản đáng nhớ là tính **đối xứng** $$B(a,b)=B(b,a)$$ và dạng đặc biệt $$B(a,1)=\frac{1}{a}$$.

Ví dụ ngắn:

$$
B(2,3)=\frac{\Gamma(2)\Gamma(3)}{\Gamma(5)}=\frac{1!\,2!}{4!}=\frac{1}{12}
$$

### 5.2 Từ hàm Beta đến phân phối Beta

Với $$0<\theta<1$$:

$$
p(\theta\mid a,b)=\frac{1}{B(a,b)}\theta^{a-1}(1-\theta)^{b-1}
$$

Khi đó:

$$
\int_0^1 p(\theta\mid a,b)\,d\theta
=\frac{1}{B(a,b)}\int_0^1 \theta^{a-1}(1-\theta)^{b-1}d\theta
=1
$$

Điểm mấu chốt: hàm Beta không chỉ là ký hiệu toán học; nó chính là cơ chế chuẩn hóa để prior/posterior Beta trở thành mật độ hợp lệ.

### 5.3 Ví dụ số: 7 lần thành công trong 10 phép thử

Giả sử $$\theta$$ là xác suất thành công của một phép thử Bernoulli.

Ta đặt prior $$\theta \sim \text{Beta}(2,2)$$ và quan sát dữ liệu $$y=7$$ thành công trên $$n=10$$ phép thử.

Likelihood theo $$\theta$$ (bỏ hằng số theo tổ hợp):

$$
L(\theta) \propto \theta^{7}(1-\theta)^3
$$

Nhân prior với likelihood:

$$
p(\theta\mid y) \propto \theta^{2-1}(1-\theta)^{2-1}\cdot \theta^{7}(1-\theta)^3
=\theta^{8}(1-\theta)^4
$$

Đây là "hình dạng" của Beta$$\,(9,5)$$ nhưng vẫn chưa chuẩn hóa. Để thành posterior hợp lệ, ta cần chia cho hàm Beta:

$$
p(\theta\mid y)=\frac{1}{B(9,5)}\theta^{8}(1-\theta)^4
$$

![Beta-Binomial update 7 over 10]({{ site.baseurl }}/img/chapter_img/chapter00/beta_binomial_update_7of10.png)
*Hinh 2: Cap nhat tu prior Beta(2,2) voi du lieu 7/10. Duong cam la dang likelihood (da scale), duong xanh la posterior Beta(9,5). Hang so $$1/B(9,5)$$ bien bieu thuc ti le thanh mat do hop le.*

Trong đó:

$$
B(9,5)=\frac{\Gamma(9)\Gamma(5)}{\Gamma(14)}
$$

Nói cách khác, **hàm Beta chính là hằng số bảo đảm tổng xác suất hậu nghiệm bằng 1**. Không có nó, ta chỉ có một biểu thức tỉ lệ, chưa phải một phân phối posterior hoàn chỉnh.

### 5.4 Vì sao người ta "nghĩ ra" hàm Beta?

Ở mức trực giác, hàm Beta không xuất hiện do "sáng tác tùy ý", mà do một nhu cầu kỹ thuật rất cụ thể trong xác suất:

1. Với dữ liệu thành công/thất bại, biểu thức theo $$\theta$$ tự nhiên có dạng $$\theta^{u}(1-\theta)^{v}$$.
2. Dạng này mô tả tốt "hình dạng niềm tin", nhưng chưa chắc có diện tích bằng 1 trên $$[0,1]$$.
3. Muốn biến nó thành mật độ hợp lệ, ta phải chia cho đúng diện tích dưới đường cong đó.
4. Diện tích ấy chính là:

$$
\int_0^1 t^{a-1}(1-t)^{b-1}dt
$$

và được đặt tên là $$B(a,b)$$.

Vì vậy, ý nghĩa thực dụng của hàm Beta là: **đổi một biểu thức "đúng dạng" thành một phân phối xác suất hợp lệ**.

## 6) Vì sao hàm Gamma quan trọng trong Bayesian?

### 6.1 Chuẩn hóa phân phối

Nhiều mật độ xác suất trong thống kê thực ra xuất hiện ban đầu như một “hàm chưa chuẩn hóa”, và cần thêm một hằng số để tích phân bằng 1; trong rất nhiều trường hợp, hằng số này được viết bằng Gamma.

Ví dụ với phân phối Gamma (tham số shape $$\alpha$$, rate $$\beta$$):

$$p(x\mid \alpha,\beta)=\frac{\beta^{\alpha}}{\Gamma(\alpha)}x^{\alpha-1}e^{-\beta x},\quad x>0$$

### 6.2 Phân phối Beta

Phân phối Beta có hằng số chuẩn hóa:

$$B(a,b)=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$$

Do đó:

$$p(\theta\mid a,b)=\frac{1}{B(a,b)}\theta^{a-1}(1-\theta)^{b-1},\quad 0<\theta<1$$

### 6.3 Dirichlet và Student-t

Dirichlet là bản tổng quát nhiều chiều của Beta, và hằng số chuẩn hóa của nó cũng được viết bằng Gamma. Tương tự, phân phối Student-t có hệ số phía trước chứa tỉ số Gamma để bảo đảm mật độ hợp lệ.

Nói ngắn gọn: gặp Bayesian đủ lâu, bạn sẽ gặp Gamma liên tục.

## 7) Trực giác thực hành

Trong tính toán số, ta thường không làm việc trực tiếp với $$\Gamma(z)$$ khi $$z$$ lớn vì dễ tràn số. Thay vào đó dùng:

$$\log\Gamma(z)$$

Thư viện khoa học thường cung cấp sẵn các hàm này (`gammaln`, `betaln` trong SciPy), ổn định hơn cho tối ưu hóa và MCMC.

Ví dụ Python:

```python
from scipy.special import gamma, gammaln, beta, betaln

print(gamma(6))      # 120.0
print(gamma(0.5))    # ~1.7724538509 = sqrt(pi)
print(gammaln(100))  # log(Gamma(100))
print(beta(2, 3))    # 1/12 = 0.08333...
print(betaln(2, 3))  # log(Beta(2,3))
```

## 8) Tóm tắt nhanh

1. $$\Gamma(z)$$ mở rộng giai thừa từ số nguyên sang số thực dương.
2. Công thức đệ quy: $$\Gamma(z+1)=z\Gamma(z)$$.
3. Với $$n\in\mathbb{N}$$: $$\Gamma(n+1)=n!$$.
4. Giá trị nổi tiếng: $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$.
5. Hàm Beta $$B(a,b)$$ là tích phân chuẩn hóa trên $$[0,1]$$ và liên hệ trực tiếp với Gamma.
6. Trong Bayesian, Gamma và Beta xuất hiện liên tục như hằng số chuẩn hóa của nhiều phân phối.

## Bài tập

**Bài 1.** Dùng công thức đệ quy để tính $$\Gamma(4)$$ và $$\Gamma(5)$$, sau đó đối chiếu với $$3!$$ và $$4!$$.

**Bài 2.** Từ $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$, suy ra $$\Gamma\!\left(\tfrac{3}{2}\right)$$ và $$\Gamma\!\left(\tfrac{5}{2}\right)$$.

**Bài 3.** Viết lại hằng số chuẩn hóa của Beta($$a,b$$) bằng Gamma và giải thích tại sao cần hằng số này để mật độ tích phân bằng 1.

**Bài 4.** Trong Python, tính `gamma(10)` và `gammaln(10)`. Kiểm tra `np.log(gamma(10))` có gần `gammaln(10)` không.

**Bài 5.** Chứng minh nhanh $$B(a,1)=\frac{1}{a}$$ từ định nghĩa tích phân, rồi đối chiếu với công thức tỉ số Gamma.

## Tài liệu tham khảo

- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.
- SciPy Special Functions: `gamma`, `gammaln`.

---

*Bài học tiếp theo: [0.14 Phân phối đồng thời (Joint Distribution)](/vi/chapter00/joint-distribution/)*
