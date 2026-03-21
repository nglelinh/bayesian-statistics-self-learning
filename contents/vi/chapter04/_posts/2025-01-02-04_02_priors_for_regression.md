---
layout: post
title: "Bài 4.2: Priors for Regression - Chọn Prior có Nguyên tắc"
chapter: '04'
order: 2
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần biết cách chọn prior (phân phối tiên nghiệm) cho regression một cách có nguyên tắc. Bạn cũng cần hiểu vì sao standardization (chuẩn hóa) rất quan trọng, vì sao weakly informative priors (các prior thông tin yếu) thường là điểm khởi đầu tốt, và vì sao prior predictive check (kiểm tra dự báo từ prior) là bước kiểm tra gần như bắt buộc trước khi fit model.

> **Ví dụ mini.** Nếu bạn đặt prior cho slope quá rộng, mô hình có thể ngầm cho phép những đường hồi quy điên rồ mà kiến thức miền nói ngay là vô lý. Prior cho regression không phải “điền đại cho đủ”, mà là cách giữ mô hình đứng trên mặt đất.
>
> **Câu hỏi tự kiểm tra.** Vì sao cùng một prior có thể trông hợp lý ở thang đo này nhưng vô lý ở thang đo khác?

## 1. Chọn prior cho regression khó ở đâu?

Trong regression, ta thường có ít nhất ba loại tham số là intercept (hệ số chặn) $$\alpha$$, slope (hệ số dốc) $$\beta$$, và noise (độ nhiễu) $$\sigma$$. Nếu không cẩn thận, prior có thể quá rộng và cho phép các giá trị vô lý, quá hẹp và bóp méo posterior (phân phối hậu nghiệm), hoặc đơn giản là khiến sampler (bộ lấy mẫu) chạy khó khăn hơn mức cần thiết.

Đây là lý do chọn prior cho regression vừa là chuyện thống kê, vừa là chuyện hiểu thang đo và bối cảnh của dữ liệu.

## 2. Standardization (chuẩn hóa): bước rất nên làm trước khi nghĩ về prior

Một trong những cách đơn giản nhất để làm prior selection (việc chọn prior) dễ hơn là standardize (chuẩn hóa) dữ liệu. Chẳng hạn, ta có thể viết:

$$
x_{std} = \frac{x-\bar{x}}{\mathrm{SD}(x)}, \qquad
y_{std} = \frac{y-\bar{y}}{\mathrm{SD}(y)}.
$$

Sau bước này, biến có mean gần 0, độ lệch chuẩn gần 1, và vì thế các prior “chuẩn” cũng trở nên dễ chọn hơn nhiều.

![So sánh trước và sau standardization]({{ site.baseurl }}/img/chapter_img/chapter04/standardization_comparison.png)

### Vì sao standardization (chuẩn hóa) giúp nhiều?

#### 1. Intercept dễ diễn giải hơn

Sau khi center (đưa về quanh trung tâm) hoặc standardize (chuẩn hóa), intercept thường gần giá trị trung bình của $$y$$ tại mức $$x$$ trung tâm, nên việc diễn giải nó trở nên tự nhiên hơn.

#### 2. Prior không còn phụ thuộc quá mạnh vào đơn vị đo

Ví dụ, cm so với m, hoặc kg so với pound, có thể làm prior “cùng chữ viết” trở nên hoàn toàn khác ý nghĩa nếu không chuẩn hóa.

#### 3. Sampler thường chạy ổn hơn

Khi các biến cùng scale tương đối giống nhau, posterior thường thân thiện hơn với HMC/NUTS, tức các thuật toán lấy mẫu Hamiltonian thường dùng trong Bayes hiện đại.

## 3. Prior cho intercept $$\alpha$$

Sau khi chuẩn hóa, intercept thường nên nằm quanh 0 với độ bất định vừa phải. Vì vậy một prior kiểu:

$$
\alpha \sim \mathcal{N}(0,1)
$$

hoặc

$$
\alpha \sim \mathcal{N}(0,2)
$$

thường là khởi đầu hợp lý.

![So sánh prior cho intercept]({{ site.baseurl }}/img/chapter_img/chapter04/prior_intercept_comparison.png)

Trực giác ở đây khá đơn giản: prior quá rộng sẽ cho phép những giá trị không thực tế, prior quá hẹp sẽ ép mô hình quá mạnh, còn một prior vừa phải sẽ giữ được tính regularization nhưng vẫn đủ linh hoạt để cho dữ liệu lên tiếng.

## 4. Prior cho slope $$\beta$$

Sau standardization, slope có ý nghĩa rất rõ: $$x$$ tăng 1 độ lệch chuẩn thì $$y$$ thay đổi trung bình bao nhiêu độ lệch chuẩn.

Khi đó một prior như:

$$
\beta \sim \mathcal{N}(0,1)
$$

thường khá hợp lý cho nhiều bài toán.

Prior này nói rằng ta mong slope không quá cực đoan, nhưng vẫn mở cho cả hiệu ứng dương lẫn âm.

Nếu bạn chưa có kiến thức prior mạnh, đây là một lựa chọn weakly informative rất tốt.

![So sánh prior cho slope]({{ site.baseurl }}/img/chapter_img/chapter04/prior_slope_comparison.png)

## 5. Prior cho noise $$\sigma$$

Vì $$\sigma > 0$$, ta thường dùng các prior dương như HalfNormal, Exponential, hoặc đôi khi HalfStudentT.

Một lựa chọn phổ biến sau standardization là:

$$
\sigma \sim \mathrm{HalfNormal}(1).
$$

![Prior cho noise sigma]({{ site.baseurl }}/img/chapter_img/chapter04/prior_noise_halfnormal.png)

Trực giác ở đây là ta mong noise ở mức vừa phải, nhưng vẫn muốn để mô hình còn đủ không gian để chấp nhận dữ liệu nhiễu hơn nếu điều đó thực sự được quan sát.

## 6. Weakly informative priors là gì và vì sao thường nên bắt đầu từ đó?

Weakly informative prior không có nghĩa là “tôi không biết gì”. Điều nó thực sự có nghĩa là tôi không muốn áp một niềm tin quá mạnh, nhưng tôi vẫn muốn loại bớt những giá trị phi lý mà kiến thức miền có thể bác bỏ ngay từ đầu.

Trong regression, đây là cách rất hữu ích để regularize (ổn định hóa) mô hình, giúp posterior ổn định hơn, và khiến sampler ít bị kéo vào những vùng tham số vô nghĩa.

## 7. Prior predictive check (kiểm tra dự báo từ prior): bước quan trọng nhất của bài này

Nếu chỉ nhìn prior trên tham số, nhiều khi ta khó biết nó có hợp lý không. Nhưng nếu dùng prior đó để sinh ra dữ liệu giả lập, mọi thứ trở nên rất rõ.

Ý tưởng là lấy mẫu $$\alpha,\beta,\sigma$$ từ prior, sinh ra nhiều đường hồi quy giả từ các mẫu ấy, rồi xem những đường đó có tạo ra dữ liệu hợp lý về mặt thực tế hay không.

![Prior predictive slopes]({{ site.baseurl }}/img/chapter_img/chapter04/prior_predictive_slopes.png)

Ví dụ, nếu prior của slope cho ra các đường dốc phi lý, hoặc sinh ra những dự báo như cân nặng âm, điểm thi 300 điểm, hay doanh thu tăng bùng nổ vô lý, thì prior đang có vấn đề, dù về mặt toán học nó “hợp lệ”.

## 8. Một ví dụ trực quan: quảng cáo và doanh thu

Giả sử bạn mô hình hóa $$x$$ là chi phí quảng cáo còn $$y$$ là doanh thu. Nếu prior cho slope quá rộng, mô hình có thể ngầm chấp nhận rằng tăng rất ít ngân sách nhưng doanh thu tăng bùng nổ một cách vô lý, hoặc ngược lại, chỉ tăng quảng cáo một chút mà doanh thu lại sụp xuống rất mạnh.

Trước khi nhìn dữ liệu, bạn đã biết nhiều kịch bản trong số đó là phi thực tế. Prior cần phản ánh điều đó.

## 9. Prior sensitivity analysis (phân tích độ nhạy của prior)

Sau khi fit model, một câu hỏi rất nên đặt ra là: **Nếu tôi đổi prior hợp lý khác đi một chút, posterior có đổi nhiều không?** Nếu posterior thay đổi mạnh, điều đó có thể báo rằng dữ liệu chưa đủ mạnh, prior đang ảnh hưởng đáng kể, và vì thế bạn cần minh bạch hơn khi báo cáo kết luận.

![Prior sensitivity analysis]({{ site.baseurl }}/img/chapter_img/chapter04/prior_sensitivity_analysis.png)

Sensitivity analysis (phân tích độ nhạy) không phải để tìm một prior “đúng tuyệt đối”. Mục tiêu của nó là để hiểu kết luận của bạn đang phụ thuộc vào prior đến mức nào.

## 10. Một bộ prior khởi đầu rất thực dụng

Với dữ liệu đã standardize, một bộ prior khởi đầu tốt cho hồi quy tuyến tính đơn giản thường là:

$$
\alpha \sim \mathcal{N}(0,1)
$$

$$
\beta \sim \mathcal{N}(0,1)
$$

$$
\sigma \sim \mathrm{HalfNormal}(1)
$$

Đây không phải chân lý cố định cho mọi bài toán, nhưng là một default (lựa chọn mặc định khởi đầu) rất lành mạnh để bắt đầu.

## 11. Sai lầm phổ biến khi chọn prior cho regression

### 11.1. Chọn prior mà quên nhìn thang đo dữ liệu

Đây là lỗi rất hay gặp.

### 11.2. Dùng prior cực rộng rồi gọi là “không thông tin”

Prior quá rộng nhiều khi lại gây hậu quả xấu như khó sampling (lấy mẫu), prior predictive vô lý, và posterior cũng trở nên khó đọc hơn.

### 11.3. Không làm prior predictive check

Đây là mất đi một bước kiểm tra cực mạnh.

### 11.4. Không kiểm tra độ nhạy

Một prior có vẻ hợp lý nhưng vẫn nên được thử thách bằng vài lựa chọn lân cận.

> **3 ý cần nhớ.** Standardization thường là bước tốt nhất để làm prior cho regression trở nên dễ chọn và dễ diễn giải hơn; weakly informative priors giúp loại bớt các giá trị phi lý mà vẫn để dữ liệu nói mạnh; và prior predictive check cùng sensitivity analysis là hai công cụ quan trọng để đánh giá prior trong regression.

## Câu hỏi tự luyện

1. Vì sao standardization lại giúp prior selection dễ hơn?
2. Hãy giải thích bằng lời một prior weakly informative cho slope đang nói điều gì.
3. Prior predictive check đang kiểm tra điều gì mà nhìn prior trên tham số chưa chắc cho ta thấy?
4. Trong một bài toán regression của bạn, tham số nào là nơi cần prior cẩn thận nhất?

## Tài liệu tham khảo

- Gelman, A., Simpson, D., & Betancourt, M. (2017). The prior can often only be understood in the context of the likelihood.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4.
- Gelman, A. et al. *Regression and Other Stories*.

---

*Bài học tiếp theo: [4.3 Posterior Inference với PyMC - Từ Theory đến Practice](/vi/chapter04/posterior-inference-pymc/)*
