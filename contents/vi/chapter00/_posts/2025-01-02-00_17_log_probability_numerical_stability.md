---
layout: post
title: "Bài 0.19: Log-probability và Ổn định số"
chapter: '00'
order: 19
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao thực hành Bayesian gần như luôn làm việc trên thang log, nhận diện được underflow, overflow, `-inf`, `nan` trong tính toán xác suất, biết viết log-likelihood và log-posterior đúng cách, đồng thời nắm kỹ thuật log-sum-exp để chuẩn hóa posterior weights một cách an toàn.

## Giới thiệu: đúng về mặt toán chưa đủ, còn phải ổn định trên máy

Nhiều công thức xác suất hoàn toàn đúng trên giấy nhưng lại thất bại khi đưa vào máy tính. Lý do không nằm ở thống kê, mà ở chỗ máy tính chỉ lưu được số với độ chính xác hữu hạn. Trong Bayesian computation, likelihood và posterior thường chứa tích của rất nhiều số nhỏ hơn 1; nếu tính trực tiếp, chúng dễ bị làm tròn thành 0. Ở chiều ngược lại, một số phép mũ có thể phình ra thành `inf`. Khi đó, mô hình lý thuyết vẫn đúng nhưng thuật toán đã hỏng.

Vì vậy, log-probability không chỉ là một mẹo lập trình. Nó là cách chuẩn để biến mô hình xác suất thành phép tính ổn định, có thể tối ưu hóa, chuẩn hóa, và lấy mẫu một cách đáng tin cậy.

## 1) Vấn đề thật sự nằm ở đâu?

Máy tính không lưu số thực với độ chính xác vô hạn. Với kiểu `float64`, chỉ có một miền giá trị hữu hạn có thể biểu diễn được. Trong mô hình xác suất, điều này trở thành vấn đề ngay khi ta làm việc với:

1. Tích của rất nhiều xác suất nhỏ hơn 1.
2. Hàm mũ của các số có độ lớn rất lớn.
3. Phép chuẩn hóa yêu cầu chia các số cực nhỏ cho tổng của các số cực nhỏ khác.

Ví dụ rất đơn giản:

$$
10^{-3}\times 10^{-3}\times \cdots \times 10^{-3}\quad \text{(1000 lần)} = 10^{-3000}
$$

Con số này hoàn toàn hợp lệ về mặt toán học, nhưng trên máy tính nó gần như chắc chắn bị làm tròn thành 0. Khi đó, ta không còn biết giá trị thật nhỏ đến mức nào; ta chỉ biết nó đã "rơi khỏi miền biểu diễn".

## 2) Log-probability là gì và vì sao nó cứu được bài toán?

Nếu $$p>0$$, ta có thể làm việc với $$\log p$$ thay vì $$p$$. Trong thống kê, mặc định ở đây là log tự nhiên.

Điểm quan trọng nhất là:

$$
\log\left(\prod_{i=1}^n p(x_i\mid\theta)\right)=\sum_{i=1}^n \log p(x_i\mid\theta)
$$

Tức là log biến tích thành tổng. Đây là lý do cốt lõi khiến log-domain ổn định hơn.

Trong thực hành, làm việc trên thang log có ba lợi ích lớn:

1. Tránh underflow do nhân quá nhiều số nhỏ.
2. Biến tích thành tổng nên dễ tối ưu hóa và dễ kiểm tra hơn.
3. Ghép prior với likelihood rất tự nhiên trong Bayes.

Một lưu ý nhỏ về ngôn ngữ: với biến liên tục, chính xác hơn ta đang làm việc với **log-density** chứ không phải xác suất tại một điểm. Tuy nhiên trong thực hành Bayes, người ta thường gọi gọn là **log-probability**.

### 2.1) Một công thức quen thuộc khi lên thang log

Với mô hình Binomial:

$$
p(k\mid n,\theta)=\binom{n}{k}\theta^k(1-\theta)^{n-k}
$$

lấy log cho ta:

$$
\log p(k\mid n,\theta)=\log\binom{n}{k}+k\log\theta+(n-k)\log(1-\theta)
$$

Thay vì nhân các số rất nhỏ như $$\theta^k$$ và $$(1-\theta)^{n-k}$$, ta chỉ cần cộng các log-term tương ứng.

![Nhân trực tiếp nhiều xác suất nhỏ dễ gây underflow]({{ site.baseurl }}/img/chapter_img/chapter00/log_probability_direct_product.png)

*Hình 1a: Tính trực tiếp trên thang xác suất khiến tích của nhiều số nhỏ nhanh chóng chạm về 0 trên máy tính.*

### 2.2) Cực đại likelihood không đổi khi lấy log

Vì hàm log tăng đơn điệu, nên:

$$
\arg\max_\theta L(\theta)=\arg\max_\theta \log L(\theta)
$$

Điều này có nghĩa: nếu mục tiêu của ta là tìm MLE hay MAP, ta có thể tối ưu hóa trên log-scale mà không làm thay đổi nghiệm tối ưu.

## 3) Ví dụ số rất cụ thể: đúng toán nhưng sai số học

Giả sử ta có 1000 quan sát độc lập, và với một giá trị tham số nào đó, mỗi quan sát đóng góp một xác suất cỡ 0.01. Khi đó:

$$
L = 0.01^{1000} = 10^{-2000}
$$

Trên giấy, đây là một số dương. Nhưng trên máy tính, giá trị này thường thành:

```python
0.0
```

Tức là **underflow**.

Trong khi đó, log-likelihood vẫn hoàn toàn hữu dụng:

$$
\log L = 1000\log(0.01)\approx -4605.17
$$

Đây là một số âm lớn, nhưng vẫn hữu hạn và vẫn so sánh được.

Điểm quan trọng là: thuật toán Bayes thường không cần biết xác suất tuyệt đối là bao nhiêu. Nó chỉ cần biết giá trị nào **lớn hơn tương đối**. Nếu hai tham số cho:

$$
\log L_1=-4605,\qquad \log L_2=-4700
$$

thì ta vẫn biết ngay $$L_1 > L_2$$, dù nếu exponentiate cả hai lên máy tính thì có thể đều thành 0.

## 4) Underflow, overflow, `-inf`, và `nan`

Đây là bốn tín hiệu bạn sẽ gặp rất thường xuyên khi code mô hình xác suất:

**Underflow**

Một số dương quá nhỏ bị làm tròn thành 0.

Ví dụ điển hình là tích của rất nhiều likelihood term nhỏ, hoặc `np.exp(-1000)` gần như bằng 0 trên máy.

**Overflow**

Một số quá lớn vượt khỏi khả năng biểu diễn của máy và trở thành `inf`.

Ví dụ điển hình là `np.exp(1000)`, vốn vượt quá khả năng lưu trữ của `float64`.

**`-inf`**

Thường xuất hiện khi lấy $$\log(0)$$. Trong mô hình xác suất, điều này đôi khi là hợp lý: nếu mô hình gán xác suất 0 cho dữ liệu quan sát được, thì log-probability của trạng thái đó thật sự là $$-\infty$$.

**`nan`**

Xuất hiện khi phép tính đã mất nghĩa số học, ví dụ `0/0`, `inf - inf`, hoặc chuẩn hóa một vector trọng số mà tất cả đều đã underflow về 0.

Vì vậy, log-domain không làm mọi thứ "an toàn tuyệt đối". Nó chỉ đẩy rủi ro xuống thấp hơn rất nhiều. Bạn vẫn phải kiểm tra `-inf`, `inf`, và `nan` trong pipeline.

## 5) Trong Bayes, ta gần như luôn làm việc với log-posterior

Công thức Bayes viết theo xác suất là:

$$
p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}
$$

Lấy log:

$$
\log p(\theta\mid x)=\log p(x\mid\theta)+\log p(\theta)-\log p(x)
$$

Hay viết gọn hơn:

$$
\log p(\theta\mid x)=\log p(x\mid\theta)+\log p(\theta)+C
$$

trong đó $$C$$ là hằng số không phụ thuộc vào $$\theta$$.

Điều này cực kỳ quan trọng vì:

1. Để so sánh hai giá trị tham số, ta không cần chuẩn hóa posterior đầy đủ.
2. MAP chỉ cần cực đại hóa log-posterior chưa chuẩn hóa.
3. Nhiều thuật toán MCMC, HMC, NUTS, variational inference đều vận hành dựa trên joint log-probability.

Nói cách khác: trong thực hành Bayesian hiện đại, thứ thư viện nội bộ thật sự tính thường là **log-likelihood** hoặc **log-posterior chưa chuẩn hóa**, chứ không phải posterior ở thang xác suất thông thường.

## 6) Khi nào ta buộc phải quay lại thang xác suất?

Không phải lúc nào cũng có thể ở yên trên log-scale. Ta thường phải quay lại thang xác suất khi:

1. Cần chuẩn hóa các trọng số để tổng bằng 1.
2. Cần tính posterior trên lưới (grid approximation).
3. Cần chuyển log-weights thành xác suất lấy mẫu.
4. Cần tính softmax trong machine learning hoặc phân loại Bayes.

Vấn đề là nếu các log-weight rất âm, phép tính trực tiếp

$$
e^{a_i}
$$

có thể underflow về 0 cho mọi $$i$$. Khi đó, bước chuẩn hóa sau đó sẽ thành `0/0`, sinh `nan`.

## 7) Log-sum-exp: kỹ thuật chuẩn hóa bắt buộc phải biết

Khi cần tính:

$$
\log\sum_i e^{a_i}
$$

ta không nên tính thẳng. Công thức ổn định là:

$$
\log\sum_i e^{a_i}=m+\log\sum_i e^{a_i-m},\qquad m=\max_i a_i
$$

Ý tưởng rất đơn giản: tách $$e^m$$ ra ngoài tổng. Vì mọi số $$a_i-m\le 0$$, nên các số mũ mới sẽ không còn bùng nổ.

### 7.1) Vì sao trừ `max` lại hợp lý?

Khi chuẩn hóa trọng số, điều ta cần là **tỉ lệ tương đối** giữa các giá trị. Với mọi hằng số $$c$$:

$$
\frac{e^{a_i}}{\sum_j e^{a_j}}
=
\frac{e^{a_i-c}}{\sum_j e^{a_j-c}}
$$

Tức là ta có thể trừ cùng một hằng số khỏi tất cả log-weights mà không làm thay đổi xác suất cuối cùng. Chọn $$c=\max_j a_j$$ là lựa chọn an toàn nhất.

![Cộng trên thang log ổn định hơn với log-sum-exp]({{ site.baseurl }}/img/chapter_img/chapter00/log_probability_log_sum.png)

*Hình 1b: Log-sum-exp giữ phép cộng xác suất ổn định hơn bằng cách kéo mọi số mũ về quanh giá trị lớn nhất.*

### 7.2) Ví dụ nhỏ nhưng rất quan trọng

Giả sử ba log-weights là:

$$
a=(-1000,\,-1001,\,-1005)
$$

Nếu tính trực tiếp:

$$
e^{-1000},\ e^{-1001},\ e^{-1005}
$$

thì trên máy tính cả ba có thể cùng thành 0.

Nhưng nếu trừ max, ta được:

$$
a-\max(a)=(0,\,-1,\,-5)
$$

Khi đó:

$$
(e^0,\ e^{-1},\ e^{-5}) \approx (1,\ 0.3679,\ 0.0067)
$$

và sau chuẩn hóa, trọng số xấp xỉ là:

$$
(0.727,\ 0.268,\ 0.005)
$$

Tức là thông tin xác suất thật ra vẫn còn nguyên; chỉ có cách tính trực tiếp là đã làm mất nó.

## 8) Ví dụ Python ngắn

Đoạn code sau minh họa hai lỗi rất điển hình: underflow khi nhân likelihood trực tiếp và lỗi `nan` khi chuẩn hóa log-weights sai cách.

```python
import numpy as np

# Ví dụ 1: nhân xác suất trực tiếp
p = 0.01
n = 1000

likelihood = p ** n
log_likelihood = n * np.log(p)

print(likelihood)      # 0.0  -> underflow
print(log_likelihood)  # -4605.170185988091

# Ví dụ 2: chuẩn hóa log-weights sai cách
log_weights = np.array([-1000.0, -1001.0, -1005.0])

bad_weights = np.exp(log_weights)
bad_weights = bad_weights / bad_weights.sum()
print(bad_weights)     # [nan nan nan]

# Cách ổn định: trừ max trước khi exponentiate
m = np.max(log_weights)
good_weights = np.exp(log_weights - m)
good_weights = good_weights / good_weights.sum()
print(good_weights)    # [0.727..., 0.268..., 0.0049...]
```

Điều nên rút ra không phải là "Python khó chịu", mà là:

1. Nếu đã ở thang log, đừng exponentiate quá sớm.
2. Khi cần chuẩn hóa, hãy trừ `max` hoặc dùng `log-sum-exp`.

## 9) Các sai lầm thực hành rất hay gặp

1. Có $$\log a$$ và $$\log b$$ nhưng lại dùng $$\log a + \log b$$ để thay cho $$\log(a+b)$$. Đây là sai khác bản chất: $$\log a + \log b = \log(ab)$$, không phải log của tổng. Khi cần cộng xác suất trong log-domain, phải dùng log-sum-exp.
2. Tính likelihood ở thang thường trước, rồi mới lấy log sau. Nếu likelihood đã underflow về 0 thì lấy log chỉ cho ra $$-\infty$$; thông tin đã mất không cứu lại được.
3. Exponentiate log-posterior quá sớm chỉ để "nhìn cho quen". Nhiều bước suy luận không cần phải quay lại thang xác suất.
4. Thấy $$-\infty$$ thì coi như luôn là bug. Thực ra $$-\infty$$ đôi khi là tín hiệu hợp lệ cho biết mô hình đang gán xác suất 0 cho một cấu hình nào đó. Điều cần làm là kiểm tra xem đó là hệ quả mô hình hay lỗi số học.
5. Quên rằng với biến liên tục, log-density có thể dương nếu density lớn hơn 1. Đây không nhất thiết là sai.

## 10) Thói quen tốt khi code mô hình Bayes

1. Viết hàm trả về log-likelihood hoặc log-posterior, không phải likelihood thô.
2. Cộng các đóng góp likelihood ở thang log.
3. Chỉ exponentiate ở bước cuối cùng, khi thật sự cần xác suất đã chuẩn hóa.
4. Dùng kỹ thuật `subtract max` hoặc log-sum-exp khi chuẩn hóa weights.
5. Luôn kiểm tra `np.isfinite(...)` ở các bước quan trọng.

Nếu phải nhớ đúng một câu sau bài này, hãy nhớ câu sau:

**Trong Bayes, hãy ở lại thang log lâu nhất có thể.**

## Tóm tắt nhanh

1. Nhiều phép tính xác suất đúng trên giấy nhưng không ổn định trên máy tính.
2. Log-probability biến tích thành tổng, giúp tránh underflow và dễ tối ưu hóa hơn.
3. Trong Bayes, ta thường làm việc với log-likelihood và log-posterior chưa chuẩn hóa.
4. Khi cần cộng hoặc chuẩn hóa xác suất ở log-domain, phải dùng log-sum-exp hoặc kỹ thuật trừ `max`.
5. `-inf`, `inf`, và `nan` không phải chi tiết phụ; chúng là tín hiệu chẩn đoán rất quan trọng.

## Câu hỏi tự luyện

1. Vì sao hai giá trị likelihood khác nhau có thể cùng hiện thành `0.0` trên máy, nhưng hai log-likelihood tương ứng vẫn so sánh được?
2. Hãy giải thích bằng lời vì sao trừ `max` không làm thay đổi softmax cuối cùng.
3. Khi nào $$-\infty$$ là tín hiệu hợp lệ của mô hình, và khi nào nó có thể là bug số học?
4. Vì sao $$\log a + \log b$$ không thể thay cho $$\log(a+b)$$?

## Tài liệu tham khảo

- Murphy, K. (2012). *Machine Learning: A Probabilistic Perspective*.
- Bishop, C. (2006). *Pattern Recognition and Machine Learning*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis*.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*.

---

*Bài học tiếp theo: [0.20 Kiểm tra giả định mô hình cơ bản](/vi/chapter00/basic-model-assumption-checks/)*
