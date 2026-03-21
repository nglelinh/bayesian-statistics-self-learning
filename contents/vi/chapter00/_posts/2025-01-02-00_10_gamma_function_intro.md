---
layout: post
title: "Bài 0.10: Giới thiệu Hàm Gamma"
chapter: '00'
order: 10
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

- $$\Gamma(1)=1$$
- $$\Gamma(2)=1!=1$$
- $$\Gamma(3)=2!=2$$
- $$\Gamma(6)=5!=120$$

Vì vậy, khi làm việc với số nguyên, Gamma “khớp” hoàn hảo với giai thừa quen thuộc.

## 4) Giá trị đặc biệt: $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$

Một kết quả nổi tiếng:

$$\Gamma\!\left(\frac{1}{2}\right)=\sqrt{\pi}$$

Từ đó:

$$\Gamma\!\left(\frac{3}{2}\right)=\frac{1}{2}\Gamma\!\left(\frac{1}{2}\right)=\frac{\sqrt{\pi}}{2}$$

$$\Gamma\!\left(\frac{5}{2}\right)=\frac{3}{2}\Gamma\!\left(\frac{3}{2}\right)=\frac{3\sqrt{\pi}}{4}$$

Điểm này giải thích vì sao $$\pi$$ xuất hiện trong nhiều công thức phân phối liên tục.

## 5) Vì sao hàm Gamma quan trọng trong Bayesian?

### 5.1 Chuẩn hóa phân phối

Nhiều mật độ xác suất có dạng “hàm chưa chuẩn hóa”, và cần một hằng số để tích phân bằng 1. Hằng số đó thường viết bằng Gamma.

Ví dụ với phân phối Gamma (tham số shape $$\alpha$$, rate $$\beta$$):

$$p(x\mid \alpha,\beta)=\frac{\beta^{\alpha}}{\Gamma(\alpha)}x^{\alpha-1}e^{-\beta x},\quad x>0$$

### 5.2 Phân phối Beta

Phân phối Beta có hằng số chuẩn hóa:

$$B(a,b)=\frac{\Gamma(a)\Gamma(b)}{\Gamma(a+b)}$$

Do đó:

$$p(\theta\mid a,b)=\frac{1}{B(a,b)}\theta^{a-1}(1-\theta)^{b-1},\quad 0<\theta<1$$

### 5.3 Dirichlet và Student-t

- Dirichlet là tổng quát nhiều chiều của Beta, và hằng số chuẩn hóa cũng dùng Gamma.
- Student-t có hệ số phía trước chứa tỉ số Gamma, giúp bảo đảm mật độ hợp lệ.

Nói ngắn gọn: gặp Bayesian đủ lâu, bạn sẽ gặp Gamma liên tục.

## 6) Trực giác thực hành

Trong tính toán số, ta thường không làm việc trực tiếp với $$\Gamma(z)$$ khi $$z$$ lớn vì dễ tràn số. Thay vào đó dùng:

$$\log\Gamma(z)$$

Thư viện khoa học thường cung cấp sẵn hàm này (`gammaln` trong SciPy), ổn định hơn cho tối ưu hóa và MCMC.

Ví dụ Python:

```python
from scipy.special import gamma, gammaln

print(gamma(6))      # 120.0
print(gamma(0.5))    # ~1.7724538509 = sqrt(pi)
print(gammaln(100))  # log(Gamma(100))
```

## 7) Tóm tắt nhanh

1. $$\Gamma(z)$$ mở rộng giai thừa từ số nguyên sang số thực dương.
2. Công thức đệ quy: $$\Gamma(z+1)=z\Gamma(z)$$.
3. Với $$n\in\mathbb{N}$$: $$\Gamma(n+1)=n!$$.
4. Giá trị nổi tiếng: $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$.
5. Trong Bayesian, Gamma chủ yếu xuất hiện như hằng số chuẩn hóa của nhiều phân phối.

## Bài tập

**Bài 1.** Dùng công thức đệ quy để tính $$\Gamma(4)$$ và $$\Gamma(5)$$, sau đó đối chiếu với $$3!$$ và $$4!$$.

**Bài 2.** Từ $$\Gamma\!\left(\tfrac{1}{2}\right)=\sqrt{\pi}$$, suy ra $$\Gamma\!\left(\tfrac{3}{2}\right)$$ và $$\Gamma\!\left(\tfrac{5}{2}\right)$$.

**Bài 3.** Viết lại hằng số chuẩn hóa của Beta($$a,b$$) bằng Gamma và giải thích tại sao cần hằng số này để mật độ tích phân bằng 1.

**Bài 4.** Trong Python, tính `gamma(10)` và `gammaln(10)`. Kiểm tra `np.log(gamma(10))` có gần `gammaln(10)` không.

## Tài liệu tham khảo

- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.
- SciPy Special Functions: `gamma`, `gammaln`.

---

*Bài học tiếp theo: [Chương 1: Cơ bản về Suy diễn Bayes](/vi/chapter01/)*
