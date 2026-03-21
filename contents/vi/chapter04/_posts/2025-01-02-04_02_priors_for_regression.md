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

Sau bài này, bạn cần biết cách chọn prior cho regression một cách có nguyên tắc. Bạn cũng cần hiểu vì sao standardization rất quan trọng, vì sao weakly informative priors thường là điểm khởi đầu tốt, và vì sao prior predictive check là bước kiểm tra gần như bắt buộc trước khi fit model.

> **Ví dụ mini.** Nếu bạn đặt prior cho slope quá rộng, mô hình có thể ngầm cho phép những đường hồi quy điên rồ mà kiến thức miền nói ngay là vô lý. Prior cho regression không phải “điền đại cho đủ”, mà là cách giữ mô hình đứng trên mặt đất.
>
> **Câu hỏi tự kiểm tra.** Vì sao cùng một prior có thể trông hợp lý ở thang đo này nhưng vô lý ở thang đo khác?

## 1. Chọn prior cho regression khó ở đâu?

Trong regression, ta thường có ít nhất ba loại tham số:

- intercept $$\alpha$$,
- slope $$\beta$$,
- noise $$\sigma$$.

Nếu không cẩn thận, prior có thể:

- quá rộng và cho phép các giá trị vô lý,
- quá hẹp và bóp méo posterior,
- hoặc khiến sampler chạy khó.

Đây là lý do chọn prior cho regression vừa là chuyện thống kê, vừa là chuyện hiểu thang đo và bối cảnh của dữ liệu.

## 2. Standardization: bước rất nên làm trước khi nghĩ về prior

Một trong những cách đơn giản nhất để làm prior selection dễ hơn là standardize dữ liệu.

Ví dụ:

$$
x_{std} = \frac{x-\bar{x}}{\mathrm{SD}(x)}, \qquad
y_{std} = \frac{y-\bar{y}}{\mathrm{SD}(y)}.
$$

Sau bước này:

- biến có mean gần 0,
- độ lệch chuẩn gần 1,
- và các prior “chuẩn” trở nên dễ chọn hơn nhiều.

![So sánh trước và sau standardization]({{ site.baseurl }}/img/chapter_img/chapter04/standardization_comparison.png)

### Vì sao standardization giúp nhiều?

#### 1. Intercept dễ diễn giải hơn

Sau khi center hoặc standardize:

- intercept thường gần giá trị trung bình của $$y$$ tại $$x$$ trung bình.

#### 2. Prior không còn phụ thuộc quá mạnh vào đơn vị đo

Ví dụ:

- cm so với m,
- kg so với pound,

có thể làm prior “cùng chữ viết” trở nên hoàn toàn khác ý nghĩa nếu không chuẩn hóa.

#### 3. Sampler thường chạy ổn hơn

Khi các biến cùng scale tương đối giống nhau, posterior thường thân thiện hơn với HMC/NUTS.

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

Trực giác:

- quá rộng  $$\rightarrow$$ cho phép những giá trị không thực tế,
- quá hẹp  $$\rightarrow$$ ép mô hình quá mạnh,
- vừa phải  $$\rightarrow$$ giữ được tính regularization nhưng vẫn linh hoạt.

## 4. Prior cho slope $$\beta$$

Sau standardization, slope có ý nghĩa:

- $$x$$ tăng 1 độ lệch chuẩn thì $$y$$ thay đổi trung bình bao nhiêu độ lệch chuẩn.

Khi đó một prior như:

$$
\beta \sim \mathcal{N}(0,1)
$$

thường khá hợp lý cho nhiều bài toán.

Nó nói rằng:

- ta mong slope không quá cực đoan,
- nhưng vẫn mở cho cả hiệu ứng dương lẫn âm.

Nếu bạn chưa có kiến thức prior mạnh, đây là một lựa chọn weakly informative rất tốt.

![So sánh prior cho slope]({{ site.baseurl }}/img/chapter_img/chapter04/prior_slope_comparison.png)

## 5. Prior cho noise $$\sigma$$

Vì $$\sigma > 0$$, ta thường dùng các prior dương như:

- HalfNormal,
- Exponential,
- đôi khi HalfStudentT.

Một lựa chọn phổ biến sau standardization là:

$$
\sigma \sim \mathrm{HalfNormal}(1).
$$

![Prior cho noise sigma]({{ site.baseurl }}/img/chapter_img/chapter04/prior_noise_halfnormal.png)

Trực giác:

- ta mong noise ở mức vừa phải,
- nhưng vẫn cho mô hình không gian để chấp nhận dữ liệu nhiễu hơn nếu cần.

## 6. Weakly informative priors là gì và vì sao thường nên bắt đầu từ đó?

Weakly informative prior không có nghĩa là:

- “tôi không biết gì”.

Nó có nghĩa là:

- tôi không muốn áp một niềm tin quá mạnh,
- nhưng tôi vẫn muốn loại bớt những giá trị phi lý.

Trong regression, đây là cách rất hữu ích để:

- regularize,
- giúp posterior ổn định hơn,
- và giúp sampler đỡ đi vào các vùng vô nghĩa.

## 7. Prior predictive check: bước quan trọng nhất của bài này

Nếu chỉ nhìn prior trên tham số, nhiều khi ta khó biết nó có hợp lý không. Nhưng nếu dùng prior đó để sinh ra dữ liệu giả lập, mọi thứ trở nên rất rõ.

Ý tưởng:

1. lấy mẫu $$\alpha,\beta,\sigma$$ từ prior,
2. sinh ra nhiều đường hồi quy giả,
3. xem các đường đó có cho ra dữ liệu hợp lý về mặt thực tế không.

![Prior predictive slopes]({{ site.baseurl }}/img/chapter_img/chapter04/prior_predictive_slopes.png)

Ví dụ:

- nếu prior của slope cho ra các đường dốc phi lý,
- hoặc dự báo cân nặng âm, điểm thi 300 điểm, doanh thu nổ tung,

thì prior đang có vấn đề, dù về mặt toán học nó “hợp lệ”.

## 8. Một ví dụ trực quan: quảng cáo và doanh thu

Giả sử bạn mô hình hóa:

- $$x$$: chi phí quảng cáo,
- $$y$$: doanh thu.

Nếu prior cho slope quá rộng, mô hình có thể ngầm chấp nhận rằng:

- tăng rất ít ngân sách nhưng doanh thu tăng bùng nổ vô lý,
- hoặc tăng quảng cáo một chút mà doanh thu sụp rất mạnh.

Trước khi nhìn dữ liệu, bạn đã biết nhiều kịch bản trong số đó là phi thực tế. Prior cần phản ánh điều đó.

## 9. Prior sensitivity analysis

Sau khi fit model, một câu hỏi là:

**Nếu tôi đổi prior hợp lý khác đi một chút, posterior có đổi nhiều không?**

Nếu posterior thay đổi mạnh, điều đó có thể báo rằng:

- dữ liệu chưa đủ mạnh,
- prior đang ảnh hưởng đáng kể,
- và bạn cần minh bạch hơn khi báo cáo.

![Prior sensitivity analysis]({{ site.baseurl }}/img/chapter_img/chapter04/prior_sensitivity_analysis.png)

Sensitivity analysis không phải để tìm một prior “đúng tuyệt đối”. Nó là để hiểu:

- kết luận của bạn đang phụ thuộc vào prior đến mức nào.

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

Đây không phải chân lý cố định cho mọi bài toán, nhưng là một default rất lành mạnh để bắt đầu.

## 11. Sai lầm phổ biến khi chọn prior cho regression

### 11.1. Chọn prior mà quên nhìn thang đo dữ liệu

Đây là lỗi rất hay gặp.

### 11.2. Dùng prior cực rộng rồi gọi là “không thông tin”

Prior quá rộng nhiều khi lại gây hậu quả xấu:

- khó sampling,
- prior predictive vô lý,
- posterior khó đọc.

### 11.3. Không làm prior predictive check

Đây là mất đi một bước kiểm tra cực mạnh.

### 11.4. Không kiểm tra độ nhạy

Một prior có vẻ hợp lý nhưng vẫn nên được thử thách bằng vài lựa chọn lân cận.

> **3 ý cần nhớ.**
> 1. Standardization thường là bước tốt nhất để làm prior cho regression trở nên dễ chọn và dễ diễn giải hơn.
> 2. Weakly informative priors giúp loại bớt các giá trị phi lý mà vẫn để dữ liệu nói mạnh.
> 3. Prior predictive check và sensitivity analysis là hai công cụ quan trọng để đánh giá prior trong regression.

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
