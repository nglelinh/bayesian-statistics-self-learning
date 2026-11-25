---
layout: post
title: "Bài 0.13: Phân phối đồng thời (Joint Distribution)"
chapter: '00'
order: 13
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

Mọi mô hình Bayes trong suốt khóa học này thực chất đều quy về đúng một đối tượng trung tâm: **phân phối đồng thời (joint distribution) $$p(\theta, y)$$** trên tham số ẩn $$\theta$$ và dữ liệu quan sát $$y$$! Một khi bạn dựng xong mặt phân phối đồng thời đó bằng cách nhân tiên nghiệm $$p(\theta)$$ với hàm hợp lý $$p(y\mid\theta)$$, mọi phép toán suy diễn Bayes chỉ còn là hai thao tác cực kỳ trực quan: **cắt lát theo dữ liệu đã thấy (conditioning)** để lấy hậu nghiệm, hoặc **cộng/tích phân gộp một trục (marginalization)** để tính bằng chứng $$p(y)$$ và phân phối dự báo.

Bài học này rèn luyện phản xạ làm việc với bảng phân phối đồng thời, phân phối biên và phân phối có điều kiện để bạn nhìn thấy định lý Bayes hiện ra rõ mồn một ngay trên một bảng số $$2\times 2$$.

---

## Kiến thức cần nhớ: Ba phép toán nền tảng trên mọi Phân phối Đồng thời

1. **Phân phối đồng thời $$p(x, y)$$:** Lưu giữ *trọn vẹn* thông tin về cả hai biến cùng lúc (kể cả mối phụ thuộc giữa chúng); tổng (hoặc tích phân) trên toàn bộ không gian bằng đúng `1`.
2. **Biên hóa (Marginalization — Cộng/Tích phân gộp):** $$p(x) = \sum_y p(x, y)$$ loại bỏ một biến phụ để nhìn riêng phân phối của $$X$$ — đây chính là cơ chế tính bằng chứng $$p(y) = \int p(y,\theta)\,d\theta$$ và khử tham số nhiễu trong thống kê Bayes!
3. **Điều kiện hóa (Conditioning — Cắt lát & Chuẩn hóa lại):** Cố định $$X = x$$ cắt ra đúng một hàng/cột của bảng đồng thời rồi chia cho tổng biên của hàng/cột đó: $$p(y\mid x) = \frac{p(x, y)}{p(x)}$$ — chính là **định lý Bayes**!

---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu phân phối đồng thời là phần mở rộng tự nhiên của hàm phân phối một biến sang nhiều biến, biết cách rút ra phân phối biên và phân phối có điều kiện từ phân phối đồng thời, và thấy rõ vì sao cấu trúc này là nền tảng trực tiếp của suy luận Bayesian.

## 1) Động cơ: Một biến là chưa đủ

Ở các bài trước, ta đã làm việc với hàm phân phối của **một biến**: với biến rời rạc là $$p(x)=P(X=x)$$, còn với biến liên tục là hàm mật độ $$f(x)$$ kèm xác suất khoảng $$P(a\le X\le b)=\int_a^b f(x)\,dx$$.

Khi mở rộng từ một chiều sang hai chiều (và tổng quát là nhiều chiều), ta chuyển từ $$p(x)$$ hoặc $$f(x)$$ sang $$p(x,y)$$ hoặc $$f(x,y)$$. Phân phối đồng thời (joint distribution) vì thế không phải khái niệm tách biệt, mà là **bước mở rộng trực tiếp sang không gian nhiều biến**.

![Mở rộng từ 1 biến sang nhiều biến]({{ site.baseurl }}/img/chapter_img/chapter00/joint_distribution_marginalization.png)

*Hình 1: Minh họa mở rộng từ hàm phân phối 1 biến sang phân phối đồng thời 2 biến. Ở giữa là mật độ đồng thời $$f(x,y)$$; phía trên và bên phải là hai phân phối biên thu được bằng cách lấy tích phân theo trục còn lại; đường ngang nét đứt thể hiện một lát cắt giúp hình dung phân phối có điều kiện.*

Trong thực tế, ta thường quan tâm nhiều biến cùng lúc — chẳng hạn chiều cao $$H$$ và cân nặng $$W$$, thời gian học $$T$$ và điểm kiểm tra $$S$$, hay trạng thái bệnh $$D$$ và kết quả xét nghiệm $$X$$. Nếu chỉ mô tả riêng từng biến, ta sẽ bỏ sót mối liên hệ giữa chúng. Phân phối đồng thời cho phép trả lời các câu hỏi dạng: "xác suất để **đồng thời** $$H$$ nằm trong khoảng này và $$W$$ nằm trong khoảng kia là bao nhiêu?"

## 2) Định nghĩa phân phối đồng thời

### 2.1 Trường hợp rời rạc

Với hai biến rời rạc $$X, Y$$, phân phối đồng thời là:

$$p(x,y) = P(X=x, Y=y)$$

Để phân phối hợp lệ, cần có $$p(x,y) \ge 0$$ với mọi $$x,y$$ và tổng kép $$\sum_x\sum_y p(x,y)=1$$. Giá trị $$p(x,y)$$ chính là xác suất hai biến đồng thời nhận cặp giá trị $$(x, y)$$.

### 2.2 Trường hợp liên tục

Với hai biến liên tục $$X, Y$$, ta sử dụng hàm mật độ đồng thời $$f(x,y)$$ thỏa mãn:

$$P((X,Y)\in A)=\iint_A f(x,y)\,dx\,dy$$

và điều kiện chuẩn hóa:

$$\iint_{\mathbb{R}^2} f(x,y)\,dx\,dy=1$$

Tương tự bài PDF một biến, $$f(x,y)$$ không phải xác suất tại một điểm mà là mật độ xác suất trên mặt phẳng.

## 3) Từ đồng thời sang phân phối biên (marginal)

Phân phối biên mô tả phân phối của một biến khi ta "cộng gộp" (bỏ qua) biến còn lại. Với trường hợp rời rạc:

$$p_X(x)=\sum_y p(x,y),\qquad p_Y(y)=\sum_x p(x,y)$$

Với trường hợp liên tục:

$$f_X(x)=\int_{-\infty}^{\infty} f(x,y)\,dy,\qquad f_Y(y)=\int_{-\infty}^{\infty} f(x,y)\,dx$$

Về trực giác, phân phối biên thu được bằng cách lấy tổng hoặc tích phân dọc theo trục của biến còn lại.

## 4) Phân phối có điều kiện và quy tắc nhân

Khi đã biết $$Y=y$$ (với $$p_Y(y) > 0$$), phân phối có điều kiện của $$X$$ là:

$$p(x\mid y)=\frac{p(x,y)}{p_Y(y)}$$

(với biến liên tục, thay bằng các hàm mật độ tương ứng).

Từ định nghĩa này ta suy ra quy tắc nhân:

$$p(x,y)=p(x\mid y)p_Y(y)=p(y\mid x)p_X(x)$$

Đây chính là nền tảng trực tiếp của định lý Bayes:

$$p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}$$

trong đó điểm chính là phân tách phân phối đồng thời thành tích của hàm hợp lý và phân phối tiên nghiệm:

$$p(\theta,x)=p(x\mid\theta)p(\theta)$$

## 5) Độc lập và phụ thuộc

Hai biến $$X, Y$$ độc lập khi và chỉ khi với mọi $$x, y$$:

$$p(x,y)=p_X(x)p_Y(y)$$

(hoặc $$f(x,y)=f_X(x)f_Y(y)$$ trong trường hợp liên tục).

Nếu đẳng thức trên đúng, việc biết $$Y$$ không làm thay đổi phân phối của $$X$$. Ngược lại, khi hai biến phụ thuộc, thông tin về biến này sẽ làm thay đổi đánh giá về biến kia — và đây chính là tình huống trung tâm trong phần lớn mô hình Bayesian.

## 6) Ví dụ rời rạc ngắn

Xét hai biến nhị phân: $$X \in \{0,1\}$$ cho biết sinh viên có đi học đầy đủ hay không, và $$Y \in \{0,1\}$$ cho biết sinh viên có qua môn hay không, với bảng phân phối đồng thời:

$$
\begin{array}{c|cc}
 & y=0 & y=1 \\
\hline
x=0 & 0.30 & 0.10 \\
x=1 & 0.15 & 0.45
\end{array}
$$

Tổng bốn ô bằng 1 nên bảng hợp lệ. Từ bảng trên, ta tính được phân phối biên $$p_X(1)=0.15+0.45=0.60$$, $$p_Y(1)=0.10+0.45=0.55$$, và xác suất có điều kiện $$p(Y=1\mid X=1)=0.45/0.60=0.75$$. So với xác suất biên $$p_Y(1)=0.55$$, việc biết $$X=1$$ làm xác suất qua môn tăng lên rõ rệt, chứng tỏ hai biến có phụ thuộc.

### 6.1) Đọc bảng bằng số lượng cụ thể

Nếu quy đổi bảng trên sang một lớp 100 sinh viên:

- 45 sinh viên đi học đầy đủ và qua môn,
- 15 sinh viên đi học đầy đủ nhưng không qua môn,
- 10 sinh viên không đi học đầy đủ nhưng vẫn qua môn,
- 30 sinh viên không đi học đầy đủ và không qua môn.

Tỷ lệ qua môn ở nhóm đi học đầy đủ là $$45/(45+15)=75\%$$, còn ở nhóm không đi học đầy đủ chỉ là $$10/(10+30)=25\%$$. Cách đọc này cho thấy phân phối đồng thời không chỉ là bảng ký hiệu trừu tượng, mà phản ánh trực tiếp cấu trúc liên hệ giữa hai biến.

## 7) Liên hệ thực hành Bayesian

Trong mô hình Bayesian, ta thường xuất phát từ phân phối đồng thời của tham số và dữ liệu:

$$p(\theta, x)=p(x\mid\theta)p(\theta)$$

Sau đó biên hóa theo $$\theta$$ để thu được bằng chứng biên (evidence):

$$p(x)=\int p(x\mid\theta)p(\theta)\,d\theta$$

và chuẩn hóa để nhận phân phối hậu nghiệm:

$$p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}$$

Do đó, nắm vững mối liên hệ đồng thời – biên – có điều kiện là bước đệm thiết yếu cho các bài suy diễn Bayesian phía sau.

## Tóm tắt nhanh

1. Phân phối đồng thời mô tả xác suất (hoặc mật độ) của nhiều biến cùng lúc.
2. Phân phối biên thu được từ phân phối đồng thời bằng phép lấy tổng (rời rạc) hoặc tích phân (liên tục).
3. Phân phối có điều kiện bằng phân phối đồng thời chia cho phân phối biên.
4. Quy tắc nhân nối phân phối đồng thời với phân phối có điều kiện: $$p(x,y)=p(x\mid y)p(y)$$.
5. Hai biến độc lập khi và chỉ khi $$p(x,y)=p(x)p(y)$$.
6. Suy diễn Bayesian dựa trực tiếp vào bộ ba cấu trúc đồng thời – biên – có điều kiện.

---

### Ví dụ tính tay làm từng bước: Cắt lát và Biên hóa bảng đồng thời Thời tiết – Giao thông

Xét bảng phân phối đồng thời giữa **Thời tiết** ($$W \in \{\text{Mưa}, \text{Nắng}\}$$) và **Giao thông** ($$T \in \{\text{Tắc}, \text{Thông}\}$$) có tổng toàn bảng bằng $$1{,}00$$:

| Thời tiết \ Giao thông | Tắc đường ($$T=1$$) | Thông thoáng ($$T=0$$) | **Biên $$P(W)$$** |
| :--- | :--- | :--- | :--- |
| **Mưa ($$W=1$$)** | $$0{,}24$$ | $$0{,}06$$ | **$$0{,}30$$** |
| **Nắng ($$W=0$$)** | $$0{,}16$$ | $$0{,}54$$ | **$$0{,}70$$** |
| **Biên $$P(T)$$** | **$$0{,}40$$** | **$$0{,}60$$** | **$$1{,}00$$** |

1. **Kiểm tra độc lập:** $$P(W=1)\cdot P(T=1) = 0{,}30 \times 0{,}40 = 0{,}12 \neq 0{,}24$$ $$\implies$$ Mưa và Tắc đường **phụ thuộc mạnh** vào nhau!
2. **Cắt lát theo sự kiện "Đang tắc đường" ($$T=1$$):** Lấy cột `Tắc đường` `[0.24, 0.16]` chia cho tổng biên $$0{,}40$$:
   $$P(\text{Mưa} \mid \text{Tắc}) = \frac{0{,}24}{0{,}40} = \mathbf{0{,}60}, \qquad P(\text{Nắng} \mid \text{Tắc}) = \frac{0{,}16}{0{,}40} = \mathbf{0{,}40}.$$
   Trước khi mở bản đồ giao thông, xác suất tiên nghiệm trời mưa là $$30\%$$; chỉ cần thấy đường tắc, xác suất hậu nghiệm trời mưa lập tức tăng gấp đôi lên **$$60\%$$**!

### Giải thích: Bốn quy tắc vàng khi tư duy bằng phân phối đồng thời

1. **Định lý Bayes chỉ là hai cách tách tích của cùng một phân phối đồng thời:** $$p(\theta, y) = p(y\mid\theta)p(\theta) = p(\theta\mid y)p(y)$$.
2. **Tích phân biên bảo toàn trung thực độ bất định:** Thay vì chốt cứng một điểm ước lượng cho tham số phụ $$\sigma$$, thống kê Bayes lấy tích phân trên đồng thời $$p(\mu, \sigma\mid y)$$ để bất định của $$\sigma$$ phản ánh đúng vào khoảng tin cậy của $$\mu$$.
3. **Phân biệt bảng đồng thời với bảng điều kiện:** Bảng đồng thời có tổng *tất cả các ô* bằng 1; bảng điều kiện $$P(T\mid W)$$ có tổng *từng hàng* bằng 1.
4. **Độc lập là trường hợp rất đặc biệt:** Chỉ khi $$p(x,y) = p(x)p(y)$$ ở *mọi* ô bạn mới được nhân hai biên; trong mô hình Bayes phân cấp, các quan sát cùng nhóm luôn phụ thuộc nhau qua tham số chung!

**Kiểm tra nhanh.** Từ bảng Thời tiết – Giao thông ở trên, nếu bạn thấy đường đang **Thông thoáng** ($$T = 0$$), xác suất hậu nghiệm $$P(\text{Mưa} \mid \text{Thông})$$ bằng bao nhiêu?

---

## Video tham khảo

- [Joint Probability Distributions: Marginal and Conditional Densities](https://www.youtube.com/watch?v=pribJ8bUBzo) — Steve Brunton, English. **Xem trước.** Minh họa cách đi từ mật độ đồng thời sang phân phối biên và phân phối có điều kiện.
- [Marginal distribution and conditional distribution | AP Statistics | Khan Academy](https://www.youtube.com/watch?v=CAXQvTKP8sg) — Khan Academy, English. Trình bày trường hợp rời rạc từ bảng hai chiều sang phân phối biên và có điều kiện.
- [Covariance, Clearly Explained!!!](https://www.youtube.com/watch?v=qtaqvPAeEJY) — StatQuest with Josh Starmer, English. Giới thiệu hiệp phương sai như một thước đo tóm tắt sự phụ thuộc trong phân phối đồng thời.

## Bài tập

**Bài 1.** Từ bảng phân phối đồng thời ở Mục 6, hãy tính:

- $$p_X(0)$$ và $$p_X(1)$$.
- $$p_Y(0)$$ và $$p_Y(1)$$.
- $$p(X=1\mid Y=1)$$ và $$p(Y=1\mid X=1)$$.

**Bài 2.** Chứng minh từ định nghĩa rằng:

$$p(x,y)=p(x\mid y)p(y)=p(y\mid x)p(x)$$

**Bài 3.** Cho hai biến liên tục có hàm mật độ đồng thời $$f(x,y)=c(x+y)$$ trên miền $$0<x<1, 0<y<1$$ và bằng 0 ngoài miền đó.

- Tìm hằng số $$c$$ để $$f$$ là hàm mật độ hợp lệ.
- Tìm các hàm mật độ biên $$f_X(x)$$ và $$f_Y(y)$$.
- Kiểm tra xem $$X$$ và $$Y$$ có độc lập hay không.

## Tài liệu tham khảo

- Wasserman, L. (2004). *All of Statistics*. Springer.
- Gelman, A., et al. (2013). *Bayesian Data Analysis* (3rd ed.). CRC Press.
- Kruschke, J. K. (2015). *Doing Bayesian Data Analysis* (2nd ed.). Academic Press.

---

*Bài học tiếp theo: [0.14 Mô hình Thống kê là gì?]({{ site.baseurl }}/contents/vi/chapter00/00_12_statistical_model_definition/)*
