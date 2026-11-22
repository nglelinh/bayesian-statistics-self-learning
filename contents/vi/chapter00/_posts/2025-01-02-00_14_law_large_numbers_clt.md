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

## Mục tiêu học tập

Sau bài này, bạn sẽ hiểu vì sao trung bình mẫu trở nên ổn định khi cỡ mẫu tăng lên (Luật số lớn — LLN), vì sao tổng hoặc trung bình của nhiều biến ngẫu nhiên có xu hướng tiến gần phân phối chuẩn (Định lý giới hạn trung tâm — CLT), và vì sao hai định lý này là nền tảng cho mô phỏng, ước lượng và kiểm định thống kê.

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
