---
layout: post
title: "Bài 0.15: Kỳ vọng, Phương sai, và Hiệp phương sai"
chapter: '00'
order: 15
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu kỳ vọng như "mức trung bình dài hạn", phương sai như "độ phân tán quanh trung bình", hiệp phương sai như "mức thay đổi cùng chiều hay ngược chiều" giữa hai biến, và biết vì sao ba khái niệm này xuất hiện liên tục trong mọi mô hình Bayesian.

## Giới thiệu: ba đại lượng mô tả trung tâm và bất định

Trong suy luận xác suất, không phải lúc nào ta cũng cần biết toàn bộ phân phối chi tiết. Nhiều quyết định thực hành bắt đầu từ ba câu hỏi cơ bản: giá trị điển hình nằm ở đâu, mức dao động lớn đến mức nào, và các biến có cùng biến thiên hay không. Kỳ vọng, phương sai, và hiệp phương sai là ba đại lượng trả lời trực tiếp ba câu hỏi đó.

## 1) Kỳ vọng: giá trị trung bình theo phân phối

Với biến rời rạc:

$$
\mathbb{E}[X] = \sum_x x\,p(x)
$$

Với biến liên tục:

$$
\mathbb{E}[X] = \int x f(x)\,dx
$$

Kỳ vọng không nhất thiết là giá trị ta quan sát trực tiếp nhiều nhất. Nó là "trọng tâm xác suất" của phân phối.

![Kỳ vọng như trọng tâm của phân phối]({{ site.baseurl }}/img/chapter_img/chapter00/expectation_center_histogram.png)

*Hình 1a: Kỳ vọng có thể được nhìn như trọng tâm của phân phối, chứ không nhất thiết là đỉnh cao nhất của histogram.*

## 2) Phương sai: độ bất định quanh trung bình

$$
\mathrm{Var}(X)=\mathbb{E}\big[(X-\mathbb{E}[X])^2\big]
$$

Viết lại dạng tính nhanh:

$$
\mathrm{Var}(X)=\mathbb{E}[X^2]-\mathbb{E}[X]^2
$$

Độ lệch chuẩn là:

$$
\mathrm{SD}(X)=\sqrt{\mathrm{Var}(X)}
$$

Về trực giác, phương sai lớn cho thấy dữ liệu phân tán mạnh, còn phương sai nhỏ cho thấy dữ liệu tập trung hơn quanh trung bình.

## 3) Hiệp phương sai: quan hệ cùng biến thiên

Với hai biến $$X, Y$$:

$$
\mathrm{Cov}(X,Y)=\mathbb{E}\big[(X-\mathbb{E}[X])(Y-\mathbb{E}[Y])\big]
$$

Khi $$\mathrm{Cov}>0$$, hai biến có xu hướng tăng cùng nhau; khi $$\mathrm{Cov}<0$$, một biến tăng thì biến kia thường giảm; còn khi hiệp phương sai gần 0, quan hệ tuyến tính giữa chúng yếu hoặc gần như không đáng kể.

![Hiệp phương sai dương giữa hai biến]({{ site.baseurl }}/img/chapter_img/chapter00/covariance_positive_scatter.png)

*Hình 1b: Hiệp phương sai dương xuất hiện khi hai biến có xu hướng tăng cùng nhau.*

![Hiệp phương sai âm giữa hai biến]({{ site.baseurl }}/img/chapter_img/chapter00/covariance_negative_scatter.png)

*Hình 1c: Hiệp phương sai âm xuất hiện khi một biến tăng thì biến kia có xu hướng giảm.*

Lưu ý: hiệp phương sai phụ thuộc đơn vị đo. Vì vậy thực hành thường dùng tương quan:

$$
\rho_{XY}=\frac{\mathrm{Cov}(X,Y)}{\mathrm{SD}(X)\mathrm{SD}(Y)}
$$

### 3.1) Một ví dụ quyết định rất ngắn

Giả sử có hai tuyến xe buýt đều có thời gian đi làm kỳ vọng là 30 phút.

- Tuyến A có các thời gian điển hình quanh $$28, 30, 32$$ phút.
- Tuyến B có các thời gian điển hình quanh $$20, 30, 40$$ phút.

Hai tuyến có thể có cùng kỳ vọng, nhưng tuyến B có phương sai lớn hơn nhiều nên rủi ro đi trễ cũng cao hơn hẳn. Nếu thêm vào đó ta thấy hôm nào mưa lớn thì thời gian đi làm cũng tăng mạnh, ta đang mô tả một hiệp phương sai dương giữa lượng mưa và thời gian di chuyển. Ví dụ này nhắc rằng chỉ nhìn trung bình là chưa đủ; quyết định thực tế thường phụ thuộc cả vào độ phân tán và cách các biến cùng biến thiên.

## 4) Các tính chất cần nhớ

1. $$\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$$
2. $$\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$$
3. $$\mathrm{Var}(X+Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)+2\mathrm{Cov}(X,Y)$$
4. Nếu $$X,Y$$ độc lập thì $$\mathrm{Cov}(X,Y)=0$$

Tính chất (4) chỉ đi một chiều: cov bằng 0 chưa chắc độc lập.

## 5) Liên hệ với Bayes

Trong Bayesian inference, posterior mean chính là kỳ vọng theo posterior, độ không chắc chắn thường được báo bằng posterior SD hoặc posterior variance, và khi có nhiều tham số thì covariance matrix cho biết mức phụ thuộc giữa các tham số đó.

Nói cách khác, học Bayes mà không chắc kỳ vọng/phương sai/hiệp phương sai thì rất khó diễn giải kết quả.

## Tóm tắt nhanh

1. Kỳ vọng là trung bình theo phân phối.
2. Phương sai đo mức phân tán quanh trung bình.
3. Hiệp phương sai đo mức thay đổi cùng chiều/ngược chiều của hai biến.
4. Ba đại lượng này là ngôn ngữ cơ bản để diễn giải posterior.

## Câu hỏi tự luyện

1. Vì sao kỳ vọng không luôn nằm ở đỉnh của phân phối?
2. Hãy nêu ví dụ hai biến có hiệp phương sai âm trong đời sống.
3. Tại sao nói cov bằng 0 chưa đủ kết luận độc lập?

## Tài liệu tham khảo

- Wasserman, L. (2004). *All of Statistics*. Springer.
- McElreath, R. (2020). *Statistical Rethinking* (2nd ed.). CRC Press.

---

*Bài học tiếp theo: [0.16 Luật số lớn và Định lý giới hạn trung tâm](/vi/chapter00/law-large-numbers-clt/)*
