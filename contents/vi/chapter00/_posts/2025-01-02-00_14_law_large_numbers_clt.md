---
layout: post
title: "Bài 0.16: Luật số lớn và Định lý giới hạn trung tâm"
chapter: '00'
order: 16
owner: Nguyen Le Linh
lang: vi
categories:
- chapter00
lesson_type: required
---

Cuối thế kỷ 17, Jacob Bernoulli tự hỏi một câu vừa giản dị vừa sâu sắc: nếu một biến cố có xác suất thật $$p$$ ẩn giấu sau màn sương ngẫu nhiên, liệu ta có thể "nhìn thấy" $$p$$ chỉ bằng cách lặp đi lặp lại thí nghiệm đủ nhiều lần? Ông mất hơn hai mươi năm để chứng minh câu trả lời — Luật số lớn. Một thế kỷ sau, Pierre-Simon Laplace và Abraham de Moivre còn đi xa hơn: không chỉ biết trung bình mẫu tiến về đâu, họ phát hiện mọi dao động quanh điểm hội tụ đó đều mang chung một hình bóng kỳ lạ — đường cong chuông chuẩn.

Trong thống kê Bayes hiện đại, hai định lý kinh điển này là xương sống của **phương pháp Monte Carlo và MCMC**: mỗi khi ta rút hàng nghìn mẫu từ phân phối hậu nghiệm, chính Luật số lớn đảm bảo trung bình mẫu hội tụ về kỳ vọng hậu nghiệm, còn Định lý giới hạn trung tâm cho phép đo chính xác sai số tính toán (MCSE).

---

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao trung bình mẫu trở nên ổn định khi cỡ mẫu tăng lên (Luật số lớn — LLN), vì sao tổng hoặc trung bình của nhiều biến ngẫu nhiên có xu hướng tiến gần phân phối chuẩn (Định lý giới hạn trung tâm — CLT), và vì sao hai định lý này là nền tảng cho mô phỏng, ước lượng và kiểm định thống kê.


## Bản đồ kiến thức nền: Hội tụ xác suất, Phân phối tiệm cận và Monte Carlo Bayes gặp nhau ở đâu?

Để hiểu hai định lý này ở tầm đại học – sau đại học thay vì chỉ thuộc phát biểu, hãy đặt chúng trên ba trụ cột:

- **Lý thuyết hội tụ của biến ngẫu nhiên (Convergence Modes):** Luật số lớn yếu (WLLN) phát biểu sự hội tụ theo xác suất ($$\bar X_n \xrightarrow{P} \mu$$), còn Luật số lớn mạnh (SLLN) phát biểu hội tụ hầu chắc chắn ($$\bar X_n \xrightarrow{\text{a.s.}} \mu$$). Đây là cơ sở lý thuyết giải thích vì sao ước lượng trung bình không bị trôi vô định khi cỡ mẫu tăng.
- **Tiệm cận phân phối (Asymptotic Distribution & CLT):** Định lý giới hạn trung tâm mô tả hội tụ theo phân phối của đại lượng chuẩn hóa $$\sqrt{n}(\bar X_n - \mu)/\sigma \xrightarrow{d} \mathcal{N}(0,1)$$. Điều kỳ diệu là tính chuẩn tiệm cận không đòi hỏi dữ liệu gốc phải chuẩn, miễn phương sai hữu hạn.
- **Cầu nối sang Thống kê Bayes & MCMC:** Trong thực hành Bayes, tích phân hậu nghiệm $$\mathbb{E}[g(\theta) \mid y]$$ thường không có công thức đóng. Ta thay tích phân bằng trung bình mẫu $$\frac{1}{S}\sum_{s=1}^S g(\theta^{(s)})$$ (nhờ LLN / định lý Ergodic cho chuỗi Markov) và đánh giá sai số chuẩn Monte Carlo $$\text{MCSE} = \hat{\sigma}_g / \sqrt{S_{\text{eff}}}$$ (nhờ CLT).

---

## Giới thiệu: Vì sao ngẫu nhiên vẫn tạo ra quy luật ổn định?

Một ý tưởng trung tâm của thống kê là từng quan sát đơn lẻ có thể nhiễu mạnh, nhưng khi gộp đủ nhiều quan sát, các quy luật ổn định lại hiện ra rõ rệt. Luật số lớn (LLN) và Định lý giới hạn trung tâm (CLT) mô tả chính xác hai khía cạnh của hiện tượng này, đồng thời giải thích vì sao có thể dùng ước lượng mẫu để suy luận về quần thể.

## 1) Luật số lớn (LLN): Trung bình mẫu hội tụ

Cho $$X_1,\dots,X_n$$ là các biến ngẫu nhiên độc lập, cùng phân phối (i.i.d.) với kỳ vọng hữu hạn $$\mu$$. Xét trung bình mẫu:

$$
\bar X_n = \frac{1}{n}\sum_{i=1}^n X_i
$$

Luật số lớn khẳng định rằng khi $$n\to\infty$$, $$\bar X_n$$ hội tụ về $$\mu$$ (theo xác suất). Về mặt trực giác, các sai lệch ngẫu nhiên dương và âm dần bù trừ cho nhau khi ta lấy trung bình trên số lượng quan sát ngày càng lớn.

![Trung bình chạy hội tụ dần về kỳ vọng]({{ site.baseurl }}/img/chapter_img/chapter00/lln_running_mean_convergence.png)

*Hình 1a: Luật số lớn cho thấy trung bình trượt (running mean) dần ổn định và hội tụ về kỳ vọng thật khi số quan sát tăng.*

### Thử nghiệm: luật số lớn

Trung bình chạy của năm chuỗi mô phỏng hội tụ về μ.

<div class="interactive-demo" markdown="1">
<div data-demo="clt-explainer" data-lang="vi" data-tab="lln"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>

## 2) Định lý giới hạn trung tâm (CLT): Phân phối của trung bình mẫu gần chuẩn

Với điều kiện phương sai $$\sigma^2$$ hữu hạn, ta có hội tụ theo phân phối:

$$
\frac{\bar X_n-\mu}{\sigma/\sqrt{n}} \Rightarrow \mathcal N(0,1)
$$

Hệ quả thực hành khi $$n$$ đủ lớn là:

$$
\bar X_n \approx \mathcal N\left(\mu,\frac{\sigma^2}{n}\right)
$$

ngay cả khi phân phối gốc của từng quan sát $$X_i$$ không phải phân phối chuẩn.

![Phân phối của trung bình mẫu gần chuẩn]({{ site.baseurl }}/img/chapter_img/chapter00/clt_sample_means_histogram.png)

*Hình 1b: Định lý giới hạn trung tâm cho thấy phân phối của trung bình mẫu tiến gần dạng chuẩn dù phân phối gốc không nhất thiết chuẩn.*

### Thử nghiệm: định lý giới hạn trung tâm

Histogram của trung bình mẫu tiến tới phân phối chuẩn khi n tăng, dù phân phối gốc lệch.

<div class="interactive-demo" markdown="1">
<div data-demo="clt-explainer" data-lang="vi" data-tab="clt"></div>
</div>

## 3) LLN và CLT khác nhau ở điểm nào?

**LLN** trả lời câu hỏi trung bình mẫu có hội tụ về giá trị thật hay không, còn **CLT** mô tả tốc độ hội tụ và hình dạng độ bất định quanh giá trị thật đó. Nói ngắn gọn, LLN giải thích "hội tụ về đâu", còn CLT giải thích "dao động ra sao quanh điểm hội tụ".

## 4) Liên hệ với sai số chuẩn

Từ CLT, độ rộng dao động của $$\bar X_n$$ tỷ lệ với $$1/\sqrt{n}$$. Vì vậy sai số chuẩn giảm chậm theo cỡ mẫu: muốn giảm sai số đi một nửa, cần tăng cỡ mẫu lên khoảng 4 lần. Đây là nguyên tắc quan trọng khi thiết kế thí nghiệm và đánh giá độ chính xác của ước lượng.

### 4.1) Một ví dụ bằng con số: Tăng cỡ mẫu 4 lần thì sao?

Giả sử ta ước lượng một tỷ lệ thật quanh mức $$0.6$$. Sai số chuẩn của tần suất mẫu xấp xỉ:

$$
\mathrm{SE}(\hat p)\approx \sqrt{\frac{0.6\times 0.4}{n}}.
$$

- Với $$n=25$$, $$\mathrm{SE}\approx 0.098$$.
- Với $$n=100$$, $$\mathrm{SE}\approx 0.049$$.
- Với $$n=400$$, $$\mathrm{SE}\approx 0.024$$.

Khi tăng cỡ mẫu từ 25 lên 100 rồi lên 400 (mỗi bước gấp 4 lần), sai số chuẩn giảm đi một nửa mỗi lần, thay vì giảm tỷ lệ thuận với $$n$$. Ví dụ này minh họa trực tiếp quy luật $$1/\sqrt{n}$$ trong thực hành.

## 5) Liên hệ với thống kê Bayesian và mô phỏng

Trong thống kê Bayesian, các ước lượng Monte Carlo cũng dựa trên trung bình mẫu: số lượng mẫu rút từ phân phối hậu nghiệm càng lớn thì ước lượng càng ổn định, và nhiều tiêu chí đánh giá độ bất định tính toán (như sai số chuẩn Monte Carlo) đều bắt nguồn từ trực giác của LLN và CLT.

## Tóm tắt nhanh

1. LLN: trung bình mẫu hội tụ về kỳ vọng thật khi cỡ mẫu tăng.
2. CLT: phân phối của trung bình mẫu tiến gần phân phối chuẩn với phương sai $$\sigma^2/n$$.
3. LLN nói về điểm hội tụ; CLT nói về hình dạng và độ rộng dao động quanh điểm đó.
4. Cả hai định lý là nền tảng cho suy luận thống kê và phương pháp mô phỏng.


## Khung giải thích (nên đọc chậm): Bốn bước đọc tốc độ hội tụ và sai số chuẩn

Nhiều người học nhớ mang máng "cỡ mẫu lớn thì chính xác hơn", nhưng lại lúng túng khi phải định lượng *cần bao nhiêu mẫu là đủ*. Hãy đọc chậm chuỗi bốn bước sau:

1. **Xác định kỳ vọng và độ lệch chuẩn của một quan sát đơn lẻ ($$\mu, \sigma$$):** Một mẫu đơn lẻ $$X_i$$ có độ bất định bằng $$\sigma$$ — con số này phản ánh bản chất biến thiên của dữ liệu và không giảm khi lấy thêm mẫu.
2. **Tính kỳ vọng và độ lệch chuẩn của trung bình mẫu ($$\bar X_n$$):** Trung bình mẫu vẫn có kỳ vọng $$\mu$$, nhưng phương sai giảm theo tỷ lệ $$1/n$$ thành $$\sigma^2/n$$, kéo theo sai số chuẩn $$\mathrm{SE} = \sigma/\sqrt{n}$$.
3. **Áp dụng xấp xỉ chuẩn CLT:** Khi $$n$$ đủ lớn, khoảng $$\mu \pm 1.96\,\sigma/\sqrt{n}$$ chứa xấp xỉ $$95\%$$ các giá trị khả dĩ của $$\bar X_n$$.
4. **Đánh đổi chi phí – độ chính xác:** Vì căn bậc hai $$\sqrt{n}$$ tăng chậm, muốn giảm một nửa bề rộng sai số phải tăng cỡ mẫu gấp $$4$$ lần; muốn giảm $$10$$ lần phải tăng cỡ mẫu gấp $$100$$ lần.

### Ví dụ tính toán cầm tay chỉ việc: Ước lượng thời gian phản hồi máy chủ lệch phải

Giả sử thời gian phản hồi của một API tuân theo phân phối mũ (rất lệch phải, hoàn toàn không phải phân phối chuẩn) với trung bình thật $$\mu = 200\text{ ms}$$ và độ lệch chuẩn $$\sigma = 200\text{ ms}$$. Ta lấy mẫu $$n$$ yêu cầu độc lập và tính trung bình mẫu $$\bar X_n$$.

| Cỡ mẫu $$n$$ | Kỳ vọng $$\mathbb{E}[\bar X_n]$$ | Sai số chuẩn $$\mathrm{SE} = 200/\sqrt{n}$$ | Khoảng 95% theo CLT ($$\mu \pm 1.96\,\mathrm{SE}$$) |
| --- | --- | --- | --- |
| $$n = 25$$ | $$200\text{ ms}$$ | $$200 / 5 = 40.0\text{ ms}$$ | $$[121.6,\; 278.4]\text{ ms}$$ |
| $$n = 100$$ | $$200\text{ ms}$$ | $$200 / 10 = 20.0\text{ ms}$$ | $$[160.8,\; 239.2]\text{ ms}$$ |
| $$n = 400$$ | $$200\text{ ms}$$ | $$200 / 20 = 10.0\text{ ms}$$ | $$[180.4,\; 219.6]\text{ ms}$$ |

Ta tính thử xác suất $$\bar X_{100}$$ vượt quá $$230\text{ ms}$$ theo CLT:

$$
z = \frac{230 - 200}{20} = 1.5 \implies P(\bar X_{100} > 230) \approx 1 - \Phi(1.5) \approx 1 - 0.9332 = 0.0668 \quad (6.68\%).
$$

**Hiểu lầm cần tránh:** Nghĩ rằng CLT làm cho *từng quan sát* $$X_i$$ trở thành phân phối chuẩn khi $$n$$ lớn. Thực tế dữ liệu gốc vẫn lệch phải (vẫn là phân phối mũ); chỉ có phân phối của **trung bình mẫu** $$\bar X_n$$ mới tiến gần dạng chuông chuẩn.

**Kiểm tra nhanh:** Nếu muốn sai số chuẩn của $$\bar X_n$$ giảm xuống đúng $$5\text{ ms}$$, ta giải $$200/\sqrt{n} = 5 \implies \sqrt{n} = 40 \implies n = 1600$$ yêu cầu.

---

## Video tham khảo

- [Law of Large Numbers - Explained and Visualized](https://www.youtube.com/watch?v=MntX3zWNWec) — Jeremy Blitz-Jones, English. **Xem trước.** Trực quan hóa cách trung bình mẫu ổn định dần khi số quan sát tăng lên.
- [But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) — 3Blue1Brown, English. Giải thích vì sao phân phối của trung bình mẫu tiến dần về dạng chuông chuẩn.
- [Định lý giới hạn trung tâm (Central limit theorem)](https://www.youtube.com/watch?v=Sm2yBx3Jn6c) — Bài Học 10 Phút, Tiếng Việt. Tóm tắt ngắn gọn bằng tiếng Việt để đối chiếu với các nội dung về ước lượng và mô phỏng trong bài.

## Câu hỏi tự luyện

1. Vì sao chỉ riêng Luật số lớn không đủ để xây dựng khoảng bất định cho $$\bar X_n$$?
2. Giải thích bằng lời vì sao sai số chuẩn giảm theo tỷ lệ $$1/\sqrt{n}$$.
3. Định lý giới hạn trung tâm có đòi hỏi dữ liệu gốc phải tuân theo phân phối chuẩn không?

## Tài liệu tham khảo

- Casella, G., & Berger, R. (2002). *Statistical Inference*.
- Wasserman, L. (2004). *All of Statistics*.

---

*Bài học tiếp theo: [0.17 Sampling Distribution và Standard Error]({{ site.baseurl }}/contents/vi/chapter00/00_15_sampling_distribution_standard_error/)*
