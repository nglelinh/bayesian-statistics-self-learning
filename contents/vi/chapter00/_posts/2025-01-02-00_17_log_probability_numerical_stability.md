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

Trên bảng phấn, tích của 1.000 xác suất bằng $$0.1$$ chỉ là một dòng ký hiệu gọn gàng $$10^{-1000}$$. Nhưng ngay khi bạn gõ công thức ấy vào máy tính dấu phẩy động 64-bit chuẩn IEEE 754, con số đó lập tức biến mất thành đúng `0.0` vì vượt quá giới hạn dưới khoảng $$10^{-308}$$. Trong một lần chạy công thức Bayes, chỉ cần tử số và mẫu số cùng bị làm tròn về `0.0`, toàn bộ thuật toán lập tức sập với `0.0 / 0.0 = NaN`.

Bài học này bóc tách **cầu nối giữa toán học lý tưởng và tính toán số thực tế**: làm việc trên thang logarit và sử dụng thủ thuật `log-sum-exp` không phải mẹo lập trình vặt, mà là kỹ thuật quan trọng trong mọi phần mềm Bayes hiện đại như PyMC hay Stan.

---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao thực hành Bayesian gần như luôn thao tác trên thang log, nhận diện được các sự cố số học như underflow, overflow, `-inf` và `nan`, biết cách viết log-likelihood và log-posterior đúng chuẩn, đồng thời nắm kỹ thuật log-sum-exp để chuẩn hóa trọng số hậu nghiệm an toàn.


## Kiến thức cần nhớ: Số học dấu phẩy động, Đại số Logarit và Ổn định MCMC

Để hiểu vì sao mọi công cụ Bayes chuyên nghiệp đều tính hoàn toàn trong không gian log, hãy kết nối ba trụ cột:

- **Biểu diễn dấu phẩy động IEEE 754 (Floating-Point Arithmetic):** Số `float64` chỉ biểu diễn được các số dương lớn hơn khoảng $$2.2 \times 10^{-308}$$ (và nhỏ hơn $$1.8 \times 10^{308}$$). Khi nhân hàng trăm xác suất nhỏ hơn 1, hiện tượng tràn dưới (*underflow*) chắc chắn xảy ra.
- **Phép biến đổi đơn điệu Logarit (Log-Space Algebra):** Hàm $$\log$$ biến tích thành tổng ($$\log\prod p_i = \sum \log p_i$$), giữ nguyên thứ tự lớn nhỏ (nên $$\arg\max$$ không đổi) và thu gọn dải giá trị $$10^{-1000}$$ thành một con số hết sức bình thường là $$-2302.6$$.
- **Kỹ thuật Log-Sum-Exp & Cầu nối sang Bayes:** Khi chuẩn hóa phân phối hậu nghiệm trên lưới hay tính trọng số mô hình (WAIC/LOO), ta buộc phải cộng các xác suất từ thang log. Đẳng thức $$\log\sum_i e^{a_i} = m + \log\sum_i e^{a_i - m}$$ (với $$m = \max_i a_i$$) triệt tiêu cả tràn trên lẫn tràn dưới mà không làm mất một chữ số chính xác nào.

---

## Giới thiệu: Đúng về mặt toán chưa đủ, còn phải ổn định trên máy tính

Nhiều công thức xác suất hoàn toàn đúng trên giấy nhưng lại thất bại khi chạy trên máy tính. Nguyên nhân không nằm ở lý thuyết xác suất mà ở giới hạn biểu diễn số dấu phẩy động của máy tính. Trong tính toán Bayesian, hàm hợp lý và phân phối hậu nghiệm thường là tích của rất nhiều số dương nhỏ hơn 1; nếu nhân trực tiếp, kết quả dễ bị làm tròn thành 0. Ngược lại, một số phép lấy hàm mũ có thể tràn số thành `inf`. Khi đó, mô hình toán học vẫn đúng nhưng thuật toán đã hỏng.

Do đó, làm việc trên thang log (log-probability) không phải mẹo vặt lập trình, mà là chuẩn mực bắt buộc để tối ưu hóa, chuẩn hóa và lấy mẫu xác suất một cách ổn định.

## 1) Vấn đề thực sự nằm ở đâu?

Với chuẩn số thực `float64`, máy tính chỉ biểu diễn được một dải giá trị hữu hạn. Trong mô hình xác suất, giới hạn này bộc lộ ngay khi gặp ba tình huống:

1. Nhân rất nhiều xác suất nhỏ hơn 1 với nhau.
2. Lấy hàm mũ của các số có độ lớn quá lớn.
3. Chuẩn hóa bằng cách chia các số cực nhỏ cho tổng của các số cực nhỏ khác.

Xét ví dụ đơn giản:

$$
10^{-3}\times 10^{-3}\times \cdots \times 10^{-3}\quad \text{(1000 lần)} = 10^{-3000}
$$

Con số này hoàn toàn hợp lệ về mặt toán học, nhưng vượt dưới ngưỡng biểu diễn của `float64` nên máy tính làm tròn thành 0. Khi đó, ta mất toàn bộ thông tin về độ lớn tương đối của nó.

## 2) Log-probability là gì và vì sao nó giải quyết được bài toán?

Với mọi xác suất $$p > 0$$, ta chuyển sang làm việc với $$\log p$$ (trong thống kê mặc định là logarit tự nhiên). Tính chất quyết định là hàm log biến tích thành tổng:

$$
\log\left(\prod_{i=1}^n p(x_i\mid\theta)\right)=\sum_{i=1}^n \log p(x_i\mid\theta)
$$

Trong thực hành, làm việc trên thang log mang lại ba lợi ích chính:

1. Tránh underflow khi nhân nhiều xác suất nhỏ.
2. Chuyển tích thành tổng nên thuận tiện hơn cho đạo hàm và tối ưu hóa.
3. Kết hợp phân phối tiên nghiệm và hàm hợp lý thành phép cộng đơn giản trong định lý Bayes.

Lưu ý nhỏ về thuật ngữ: với biến liên tục, đại lượng chính xác là **log-density** (log của hàm mật độ), nhưng trong thực hành Bayesian thường được gọi gọn là **log-probability**.

### 2.1) Ví dụ quen thuộc khi chuyển sang thang log

Với phân phối Binomial:

$$
p(k\mid n,\theta)=\binom{n}{k}\theta^k(1-\theta)^{n-k}
$$

Lấy log hai vế ta thu được:

$$
\log p(k\mid n,\theta)=\log\binom{n}{k}+k\log\theta+(n-k)\log(1-\theta)
$$

Thay vì nhân các lũy thừa rất nhỏ như $$\theta^k$$ và $$(1-\theta)^{n-k}$$, ta chỉ cần cộng các hạng tử log tương ứng.

![Nhân trực tiếp nhiều xác suất nhỏ dễ gây underflow]({{ site.baseurl }}/img/chapter_img/chapter00/log_probability_direct_product.png)

*Hình 1a: Nhân trực tiếp nhiều xác suất nhỏ trên thang thường khiến tích nhanh chóng chạm 0 do underflow.*

### 2.2) Cực đại của hàm hợp lý không đổi khi lấy log

Vì hàm log tăng nghiêm ngặt trên $$(0, \infty)$$, điểm cực đại được bảo toàn:

$$
\arg\max_\theta L(\theta)=\arg\max_\theta \log L(\theta)
$$

Do đó, khi tìm MLE hay MAP, ta có thể tối ưu hóa trực tiếp trên thang log mà không làm thay đổi nghiệm.

## 3) Ví dụ số cụ thể: Đúng về toán học nhưng hỏng khi tính trực tiếp

Giả sử có 1,000 quan sát độc lập và tại một giá trị tham số nào đó, mỗi quan sát đóng góp xác suất xấp xỉ 0.01. Khi đó:

$$
L = 0.01^{1000} = 10^{-2000}
$$

Trên giấy đây là một số dương, nhưng trên máy tính nó bị làm tròn thành:

```python
0.0
```

— tức xảy ra **underflow**. Trong khi đó, log-likelihood vẫn hữu hạn và dễ xử lý:

$$
\log L = 1000\log(0.01)\approx -4605.17
$$

Hơn nữa, phần lớn thuật toán Bayesian chỉ cần so sánh độ lớn **tương đối** giữa các tham số. Nếu hai giá trị tham số cho:

$$
\log L_1=-4605,\qquad \log L_2=-4700
$$

ta biết ngay $$L_1 > L_2$$, dù nếu lấy hàm mũ trên máy tính thì cả hai đều bị đưa về `0.0`.

## 4) Underflow, overflow, `-inf` và `nan`

Đây là bốn tín hiệu số học thường gặp nhất khi lập trình mô hình xác suất:

- **Underflow**: số dương quá nhỏ bị làm tròn thành `0.0` (ví dụ nhân nhiều xác suất nhỏ hoặc tính `np.exp(-1000)`).
- **Overflow**: số quá lớn vượt giới hạn lưu trữ của `float64` và trở thành `inf` (ví dụ `np.exp(1000)`).
- **`-inf`**: thường xuất hiện khi tính $$\log(0)$$. Trong mô hình xác suất, đây đôi khi là kết quả hợp lệ khi mô hình gán xác suất bằng 0 cho một trạng thái không khả thi.
- **`nan`**: xuất hiện khi phép toán vô định về mặt số học, chẳng hạn `0/0`, `inf - inf`, hoặc chuẩn hóa một vector trọng số mà mọi phần tử đã underflow về 0.

Vì vậy, thang log giảm mạnh rủi ro số học nhưng không loại bỏ hoàn toàn; bạn vẫn cần kiểm tra `-inf`, `inf` và `nan` trong quá trình chạy mô hình.

## 5) Trong thống kê Bayesian, ta thường làm việc với log-posterior

Viết định lý Bayes ở dạng xác suất:

$$
p(\theta\mid x)=\frac{p(x\mid\theta)p(\theta)}{p(x)}
$$

Chuyển sang thang log:

$$
\log p(\theta\mid x)=\log p(x\mid\theta)+\log p(\theta)-\log p(x)
$$

Hay viết gọn:

$$
\log p(\theta\mid x)=\log p(x\mid\theta)+\log p(\theta)+C
$$

trong đó $$C$$ là hằng số không phụ thuộc vào $$\theta$$. Tính chất này đặc biệt hữu ích vì:

1. Để so sánh hai giá trị tham số, không cần tính hằng số chuẩn hóa $$p(x)$$.
2. Ước lượng MAP chỉ cần cực đại hóa log-posterior chưa chuẩn hóa.
3. Các thuật toán lấy mẫu và xấp xỉ hiện đại như MCMC, HMC, NUTS hay variational inference đều hoạt động trực tiếp trên hàm mật độ đồng thời ở thang log.

Nói cách khác, phần lõi mà các thư viện Bayesian tính toán thực chất là **log-likelihood** và **log-posterior chưa chuẩn hóa**.

## 6) Khi nào cần quay lại thang xác suất?

Ta buộc phải chuyển từ thang log về thang xác suất trong các tình huống như:

1. Chuẩn hóa trọng số sao cho tổng bằng 1.
2. Tính phân phối hậu nghiệm trên lưới (grid approximation).
3. Chuyển log-weight thành xác suất lấy mẫu.
4. Tính hàm softmax trong phân loại hoặc học máy.

Nếu các log-weight đều rất âm, việc tính trực tiếp:

$$
e^{a_i}
$$

có thể khiến mọi phần tử underflow về `0.0`, dẫn tới phép chia `0/0` và kết quả `nan`.

## 7) Kỹ thuật log-sum-exp

Khi cần tính:

$$
\log\sum_i e^{a_i}
$$

không nên tính hàm mũ trực tiếp mà dùng dạng ổn định số học:

$$
\log\sum_i e^{a_i}=m+\log\sum_i e^{a_i-m},\qquad m=\max_i a_i
$$

Bằng cách tách $$e^m$$ ra ngoài tổng, mọi số mũ $$a_i - m$$ đều nhỏ hơn hoặc bằng 0, tránh được overflow và giữ lại thành phần trội nhất để tránh underflow toàn phần.

### 7.1) Vì sao trừ `max` không làm đổi kết quả chuẩn hóa?

Khi chuẩn hóa trọng số, ta chỉ quan tâm tỷ lệ tương đối giữa các thành phần. Với mọi hằng số $$c$$:

$$
\frac{e^{a_i}}{\sum_j e^{a_j}}
=
\frac{e^{a_i-c}}{\sum_j e^{a_j-c}}
$$

Do đó, trừ cùng một hằng số khỏi toàn bộ log-weight không làm thay đổi xác suất cuối cùng, và chọn $$c=\max_j a_j$$ là cách an toàn nhất về mặt số học.

![Cộng trên thang log ổn định hơn với log-sum-exp]({{ site.baseurl }}/img/chapter_img/chapter00/log_probability_log_sum.png)

*Hình 1b: Kỹ thuật log-sum-exp dịch các số mũ về quanh giá trị lớn nhất để phép cộng và chuẩn hóa xác suất luôn ổn định.*

### 7.2) Ví dụ minh họa

Giả sử ba log-weight là:

$$
a=(-1000,\,-1001,\,-1005)
$$

Nếu lấy hàm mũ trực tiếp:

$$
e^{-1000},\ e^{-1001},\ e^{-1005}
$$

thì cả ba đều bị làm tròn thành `0.0` trên máy tính. Khi trừ đi giá trị lớn nhất $$\max(a) = -1000$$:

$$
a-\max(a)=(0,\,-1,\,-5)
$$

Ta thu được:

$$
(e^0,\ e^{-1},\ e^{-5}) \approx (1,\ 0.3679,\ 0.0067)
$$

Sau khi chuẩn hóa, ba trọng số xấp xỉ:

$$
(0.727,\ 0.268,\ 0.005)
$$

Như vậy thông tin xác suất vẫn hoàn toàn nguyên vẹn; chỉ cách tính trực tiếp mới làm mất thông tin đó.

## 8) Ví dụ Python ngắn

Đoạn mã dưới đây minh họa hai lỗi phổ biến: underflow khi nhân xác suất trực tiếp và lỗi `nan` khi chuẩn hóa log-weight chưa trừ `max`.

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

Bài học rút ra là: khi đã ở thang log, đừng lấy hàm mũ quá sớm; và khi cần chuẩn hóa, hãy trừ `max` hoặc dùng `log-sum-exp`.

## 9) Các sai lầm thực hành thường gặp

1. Dùng $$\log a + \log b$$ thay cho $$\log(a+b)$$: đây là nhầm lẫn cơ bản vì $$\log a + \log b = \log(ab)$$. Khi cần tính log của một tổng, phải dùng log-sum-exp.
2. Tính hàm hợp lý trên thang thường rồi mới lấy log: nếu hàm hợp lý đã underflow về 0 thì lấy log chỉ cho $$-\infty$$, không thể khôi phục thông tin đã mất.
3. Lấy hàm mũ cho log-posterior quá sớm chỉ để nhìn cho quen mắt, trong khi phần lớn bước tính không cần quay lại thang xác suất.
4. Mặc định mọi giá trị $$-\infty$$ đều là lỗi lập trình: đôi khi $$-\infty$$ là tín hiệu hợp lệ cho biết mô hình gán xác suất 0 cho một cấu hình cụ thể; cần phân biệt đó là tính chất mô hình hay lỗi số học.
5. Nhầm tưởng log-density của biến liên tục phải luôn âm: vì hàm mật độ có thể lớn hơn 1, log-density hoàn toàn có thể mang giá trị dương.

## 10) Thói quen tốt khi lập trình mô hình Bayesian

1. Viết hàm trả về log-likelihood hoặc log-posterior thay vì likelihood thô.
2. Cộng các đóng góp của từng quan sát trên thang log.
3. Chỉ lấy hàm mũ ở bước cuối cùng khi thực sự cần xác suất đã chuẩn hóa.
4. Dùng kỹ thuật trừ `max` hoặc `log-sum-exp` khi chuẩn hóa trọng số.
5. Kiểm tra `np.isfinite(...)` ở các bước tính quan trọng.

Nguyên tắc cốt lõi cần nhớ: **trong tính toán Bayesian, hãy giữ phép tính trên thang log lâu nhất có thể.**

## Tóm tắt nhanh

1. Công thức xác suất đúng về mặt toán học vẫn có thể hỏng trên máy tính do giới hạn biểu diễn số.
2. Log-probability biến tích thành tổng, tránh underflow và thuận lợi cho tối ưu hóa.
3. Tính toán Bayesian chủ yếu làm việc với log-likelihood và log-posterior chưa chuẩn hóa.
4. Khi cần cộng hoặc chuẩn hóa từ thang log, dùng log-sum-exp hoặc kỹ thuật trừ `max`.
5. Các giá trị `-inf`, `inf` và `nan` là tín hiệu chẩn đoán quan trọng trong quy trình tính toán.


## Giải thích: Ba bước chuẩn hóa hậu nghiệm an toàn bằng Log-Sum-Exp

Khi bạn có vectơ log-posterior chưa chuẩn hóa $$\mathbf{a} = (a_1, \dots, a_K)$$ gồm các số âm rất lớn, hãy luôn thực hiện đúng ba bước sau thay vì gọi `exp(a)` trực tiếp:

1. **Tìm điểm neo cực đại:** Đặt $$m = \max_k a_k$$.
2. **Dịch chuyển về gần 0 trước khi lấy mũ:** Tính $$b_k = a_k - m \le 0$$. Phần tử lớn nhất có $$b_{k^*} = 0 \implies e^{b_{k^*}} = 1$$, đảm bảo không bao giờ tràn trên (overflow) và mẫu số luôn $$\ge 1$$ (không bao giờ chia cho 0).
3. **Tính hằng số chuẩn hóa và xác suất hậu nghiệm:** $$\log Z = m + \log\sum_k e^{b_k}$$, rồi $$p_k = \exp(a_k - \log Z)$$.

### Ví dụ tính toán làm từng bước: Chuẩn hóa 3 mô hình có log-posterior bằng $$-1000$$

Giả sử sau khi quan sát tập dữ liệu lớn, ba giả thuyết $$H_1, H_2, H_3$$ có log-posterior chưa chuẩn hóa lần lượt là $$a_1 = -1000.0$$, $$a_2 = -1001.0$$, $$a_3 = -1002.0$$.

Nếu tính trực tiếp trên `float64`: $$\exp(-1000) = 0.0$$, nên tổng bằng `0.0` và tỷ số `0.0 / 0.0 = NaN`! Bây giờ áp dụng `log-sum-exp` với $$m = -1000.0$$:

| Giả thuyết | Log gốc $$a_k$$ | Dịch chuyển $$b_k = a_k - m$$ | $$e^{b_k}$$ | Xác suất chuẩn hóa $$p_k = e^{b_k} / \sum e^{b_j}$$ |
| --- | --- | --- | --- | --- |
| $$H_1$$ | $$-1000.0$$ | $$0.0$$ | $$1.0000$$ | $$1.0000 / 1.5032 \approx 0.6652$$ |
| $$H_2$$ | $$-1001.0$$ | $$-1.0$$ | $$0.3679$$ | $$0.3679 / 1.5032 \approx 0.2447$$ |
| $$H_3$$ | $$-1002.0$$ | $$-2.0$$ | $$0.1353$$ | $$0.1353 / 1.5032 \approx 0.0900$$ |
| **Tổng** | — | — | **$$1.5032$$** | **$$1.0000$$** |

Hằng số chuẩn hóa trên thang log là $$\log Z = -1000.0 + \ln(1.5032) \approx -999.5924$$. Kết quả chính xác tuyệt đối và hoàn toàn tránh được `NaN`.

**Hiểu lầm cần tránh:** Nhầm rằng trừ cùng một hằng số $$m$$ khỏi các giá trị log sẽ làm thay đổi xác suất cuối cùng. Thực tế trừ $$m$$ trên thang log tương đương chia cả tử và mẫu cho $$e^m$$ trên thang xác suất — tỷ số không hề thay đổi.

**Kiểm tra nhanh:** Nếu cộng thêm $$-5000$$ vào cả ba giá trị $$a_1, a_2, a_3$$ (thành $$-6000, -6001, -6002$$), các giá trị dịch chuyển $$b_k$$ vẫn là $$0, -1, -2$$, nên xác suất hậu nghiệm vẫn y hệt $$(0.6652, 0.2447, 0.0900)$$.

---

## Video tham khảo

- [Logs (logarithms), Clearly Explained!!!](https://www.youtube.com/watch?v=VSi0Z04fWj0) — StatQuest with Josh Starmer, English. **Xem trước.** Ôn lại tính chất biến tích thành tổng của logarit làm nền cho log-likelihood.
- [Why Log Probabilities Are Everywhere in AI - Underflow Error in HMMs and Viterbi Algorithm](https://www.youtube.com/watch?v=HghZrdnrNQY) — Algorithms and AI, English. Minh họa sự cố underflow khi nhân nhiều xác suất nhỏ trong thực tế.
- [The log-sum-exp trick (NLP817 5.12)](https://www.youtube.com/watch?v=MZ2VM32h37g) — Herman Kamper, English. Giải thích chi tiết kỹ thuật log-sum-exp để chuẩn hóa an toàn từ thang log.

## Câu hỏi tự luyện

1. Vì sao hai giá trị likelihood khác nhau có thể cùng bị làm tròn thành `0.0` trên máy tính, trong khi hai giá trị log-likelihood tương ứng vẫn so sánh được?
2. Giải thích bằng lời vì sao trừ đi `max` không làm thay đổi kết quả softmax cuối cùng.
3. Khi nào $$-\infty$$ là hệ quả hợp lệ của mô hình và khi nào nó là dấu hiệu lỗi số học?
4. Vì sao không thể thay $$\log(a+b)$$ bằng $$\log a + \log b$$?

## Tài liệu tham khảo

- Murphy, K. (2012). *Machine Learning: A Probabilistic Perspective*.
- Bishop, C. (2006). *Pattern Recognition and Machine Learning*.
- Gelman, A., et al. (2013). *Bayesian Data Analysis*.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*.

---

*Bài học tiếp theo: [0.20 Kiểm tra giả định mô hình cơ bản]({{ site.baseurl }}/contents/vi/chapter00/00_18_basic_model_assumption_checks/)*
