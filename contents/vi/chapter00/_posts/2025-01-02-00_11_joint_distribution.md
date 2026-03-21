---
layout: post
title: "Bài 0.11: Phân phối đồng thời (Joint Distribution)"
chapter: '00'
order: 11
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu rằng phân phối đồng thời là phần mở rộng tự nhiên của hàm phân phối một biến sang nhiều biến, biết cách lấy phân phối biên và phân phối có điều kiện từ joint, và thấy rõ vì sao cấu trúc này là nền tảng trực tiếp cho suy luận Bayesian.

## 1) Động cơ: Một biến là chưa đủ

Ở các bài trước, ta đã dùng hàm phân phối cho **một biến**:

- rời rạc: $$p(x)=P(X=x)$$,
- liên tục: $$f(x)$$ với $$P(a\le X\le b)=\int_a^b f(x)\,dx$$.

Đây là mô tả một chiều. Bây giờ ta mở rộng sang hai chiều (và tổng quát là nhiều chiều): từ $$p(x)$$ hoặc $$f(x)$$ sang $$p(x,y)$$ hoặc $$f(x,y)$$. Vì vậy, joint distribution không phải khái niệm tách rời, mà là **bước mở rộng trực tiếp của hàm phân phối nhiều biến**.

![Mo rong tu 1 bien sang nhieu bien](/bayesian-statistics-self-learning/img/chapter_img/chapter00/joint_distribution_marginalization.png)
*Hinh 1: Minh hoa mo rong tu ham phan phoi 1 bien sang phan phoi dong thoi 2 bien. O giua la joint density $$f(x,y)$$; phia tren va ben phai la phan phoi bien thu duoc bang tich phan theo truc con lai; duong ngang dut the hien mot lat cat de hinh dung phan phoi co dieu kien.*

Trong thực tế, ta thường quan tâm nhiều biến cùng lúc. Ví dụ:

- chiều cao $$H$$ và cân nặng $$W$$,
- thời gian học $$T$$ và điểm kiểm tra $$S$$,
- trạng thái bệnh $$D$$ và kết quả xét nghiệm $$X$$.

Nếu chỉ mô tả từng biến riêng lẻ, ta có thể bỏ lỡ mối liên hệ quan trọng giữa chúng. Phân phối đồng thời giúp trả lời các câu hỏi kiểu: "xác suất để **đồng thời** xảy ra $$H$$ trong khoảng này và $$W$$ trong khoảng kia là bao nhiêu?"

## 2) Định nghĩa phân phối đồng thời

### 2.1 Trường hợp rời rạc

Với hai biến rời rạc $$X, Y$$, phân phối đồng thời là:

$$p(x,y) = P(X=x, Y=y)$$

Điều kiện hợp lệ:

1. $$p(x,y) \ge 0$$ với mọi $$x,y$$
2. $$\sum_x\sum_y p(x,y)=1$$

Ở đây, $$p(x,y)$$ là xác suất để cả hai biến nhận giá trị cụ thể cùng lúc.

### 2.2 Trường hợp liên tục

Với hai biến liên tục $$X, Y$$, ta dùng mật độ đồng thời:

$$f(x,y)$$

Sao cho:

$$P((X,Y)\in A)=\iint_A f(x,y)\,dx\,dy$$

và:

$$\iint_{\mathbb{R}^2} f(x,y)\,dx\,dy=1$$

Lưu ý như bài PDF: $$f(x,y)$$ không phải là xác suất tại một điểm, mà là mật độ trên mặt phẳng.

## 3) Từ đồng thời sang biên (marginal)

Phân phối biên cho biết hành vi của một biến khi "bỏ qua" biến còn lại.

- Rời rạc:

$$p_X(x)=\sum_y p(x,y),\qquad p_Y(y)=\sum_x p(x,y)$$

- Liên tục:

$$f_X(x)=\int_{-\infty}^{\infty} f(x,y)\,dy,\qquad f_Y(y)=\int_{-\infty}^{\infty} f(x,y)\,dx$$

Trực giác: phân phối biên là tổng/tích phân "cộng dồn" theo trục còn lại.

## 4) Phân phối có điều kiện và quy tắc nhân

Khi đã biết $$Y=y$$, phân phối của $$X$$ là:

$$p(x\mid y)=\frac{p(x,y)}{p_Y(y)}$$

(rời rạc; với liên tục thay bằng mật độ tương ứng).

Từ đây có quy tắc nhân:

$$p(x,y)=p(x\mid y)p_Y(y)=p(y\mid x)p_X(x)$$

Đây chính là công cụ nền cho Bayes:

$$p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}$$

Trong đó, "hạt nhân" quan trọng là liên hệ giữa đồng thời và có điều kiện:

$$p(\theta,x)=p(x\mid\theta)p(\theta)$$

## 5) Độc lập và phụ thuộc

Hai biến $$X, Y$$ độc lập khi và chỉ khi:

$$p(x,y)=p_X(x)p_Y(y)$$

Cho mọi $$x,y$$ (hoặc $$f(x,y)=f_X(x)f_Y(y)$$ trong trường hợp liên tục).

- Nếu đẳng thức đúng: biết $$Y$$ không làm thay đổi niềm tin về $$X$$.
- Nếu không đúng: tồn tại phụ thuộc, và thông tin về một biến sẽ cập nhật biến còn lại.

Trong Bayesian, phần lớn mô hình thú vị nằm ở trường hợp **không độc lập**.

## 6) Ví dụ rời rạc ngắn

Giả sử:

- $$X \in \{0,1\}$$ (đi học hay không)
- $$Y \in \{0,1\}$$ (qua môn hay không)

và bảng đồng thời:

$$
\begin{array}{c|cc}
 & y=0 & y=1 \\
\hline
x=0 & 0.30 & 0.10 \\
x=1 & 0.15 & 0.45
\end{array}
$$

Kiểm tra nhanh:

- Tổng bằng 1.
- Biên của $$X$$: $$p_X(1)=0.15+0.45=0.60$$.
- Biên của $$Y$$: $$p_Y(1)=0.10+0.45=0.55$$.
- Có điều kiện: $$p(Y=1\mid X=1)=0.45/0.60=0.75$$.

So với $$p_Y(1)=0.55$$, ta thấy biết $$X=1$$ làm xác suất qua môn tăng rõ rệt, tức là có phụ thuộc.

## 7) Liên hệ thực hành Bayesian

Trong mô hình Bayesian, ta làm việc thường xuyên với phân phối đồng thời:

$$p(\theta, x)=p(x\mid\theta)p(\theta)$$

Sau đó lấy biên theo $$\theta$$ để được evidence:

$$p(x)=\int p(x\mid\theta)p(\theta)\,d\theta$$

và chuẩn hóa để ra posterior:

$$p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}$$

Vì vậy, nắm chắc joint/marginal/conditional là bước đệm bắt buộc trước khi học suy diễn Bayes sâu hơn.

## Tóm tắt nhanh

1. Phân phối đồng thời mô tả xác suất (hoặc mật độ) của nhiều biến cùng lúc.
2. Phân phối biên lấy từ joint bằng cách tổng (rời rạc) hoặc tích phân (liên tục).
3. Phân phối có điều kiện lấy từ joint chia cho biên.
4. Quy tắc nhân nối joint với conditional: $$p(x,y)=p(x\mid y)p(y)$$.
5. Độc lập tương đương với $$p(x,y)=p(x)p(y)$$.
6. Bayes dựa trực tiếp trên cấu trúc joint-marginal-conditional.

## Bài tập

**Bài 1.** Cho bảng joint ở Mục 6, hãy tính:

- $$p_X(0), p_X(1)$$
- $$p_Y(0), p_Y(1)$$
- $$p(X=1\mid Y=1)$$ và $$p(Y=1\mid X=1)$$

**Bài 2.** Chứng minh từ định nghĩa rằng:

$$p(x,y)=p(x\mid y)p(y)=p(y\mid x)p(x)$$

**Bài 3.** Cho hai biến liên tục có joint $$f(x,y)=c(x+y)$$ trên miền $$0<x<1, 0<y<1$$ và 0 ngoài miền đó.

- Tìm hằng số $$c$$ để $$f$$ hợp lệ.
- Tìm $$f_X(x)$$ và $$f_Y(y)$$.
- Kiểm tra $$X, Y$$ có độc lập không.

## Tài liệu tham khảo

- Wasserman, L. (2004). *All of Statistics*. Springer.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.

---

*Bài học tiếp theo: [Chương 1: Cơ bản về Suy diễn Bayes](/vi/chapter01/)*
