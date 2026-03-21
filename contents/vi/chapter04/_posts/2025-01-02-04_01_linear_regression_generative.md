---
layout: post
title: "Bài 4.1: Bayesian Linear Regression - Mô hình Sinh dữ liệu"
chapter: '04'
order: 1
owner: Nguyen Le Linh
lang: vi
categories:
- chapter04
lesson_type: required
---

## Mục tiêu học tập

Sau bài này, bạn cần nhìn hồi quy tuyến tính Bayes như một **câu chuyện sinh dữ liệu**, chứ không chỉ là bài toán “fit một đường thẳng”. Bạn cũng cần hiểu vai trò của intercept, slope và noise trong mô hình, và vì sao Bayesian regression luôn giữ lại bất định của tham số lẫn dự đoán.

> **Ví dụ mini.** Bạn muốn mô tả mối liên hệ giữa chiều cao và cân nặng. Cách nhìn cũ là “tìm đường thẳng tốt nhất”. Cách nhìn Bayes là “mỗi người có cân nặng được sinh ra quanh một xu hướng trung bình, và ta chưa chắc chắn về xu hướng đó”.
>
> **Câu hỏi tự kiểm tra.** Vì sao regression theo tinh thần Bayes không nên được hiểu đơn giản là tìm một đường thẳng duy nhất?

## 1. Regression không chỉ là vẽ đường thẳng

Khi mới học hồi quy, nhiều người được dạy:

- chọn một đường thẳng $$y = \alpha + \beta x$$,
- rồi tìm đường làm sai số bình phương nhỏ nhất.

Cách đó hữu ích, nhưng nó dễ khiến ta nghĩ regression chỉ là một kỹ thuật fitting hình học.

Trong Bayesian regression, ta nhìn sâu hơn:

- dữ liệu đến từ đâu,
- tại sao các điểm không nằm đúng trên một đường,
- và ta bất định đến mức nào về các tham số.

![Frequentist vs Bayesian regression]({{ site.baseurl }}/img/chapter_img/chapter04/frequentist_vs_bayesian_regression.png)

## 2. Câu chuyện sinh dữ liệu của hồi quy tuyến tính

Giả sử ta muốn mô hình hóa mối quan hệ giữa:

- chiều cao $$x$$,
- và cân nặng $$y$$.

Câu chuyện sinh dữ liệu có thể kể như sau.

### Bước 1. Có một xu hướng trung bình

Người cao hơn thường nặng hơn. Ta mô tả xu hướng đó bằng:

$$
\mu_i = \alpha + \beta x_i.
$$

Ở đây:

- $$\alpha$$ là intercept,
- $$\beta$$ là slope.

### Bước 2. Mỗi cá nhân dao động quanh xu hướng đó

Không ai nằm chính xác trên đường trung bình, vì còn nhiều yếu tố khác như:

- khối cơ,
- chế độ ăn,
- giới tính,
- mức độ vận động,
- sai số đo lường.

Vì vậy ta viết:

$$
y_i \sim \mathcal{N}(\mu_i,\sigma).
$$

Ở đây $$\sigma$$ là độ nhiễu quanh đường hồi quy.

### Bước 3. Ta chưa biết chính xác các tham số

Ta không biết thật sự:

- intercept là bao nhiêu,
- slope là bao nhiêu,
- noise là bao nhiêu.

Nên ta đặt prior cho chúng, rồi dùng dữ liệu để suy luận posterior.

![Regression như một generative story]({{ site.baseurl }}/img/chapter_img/chapter04/regression_generative_story.png)

## 3. Ba tham số cần hiểu thật chắc

### 3.1. Intercept $$\alpha$$

Intercept là giá trị trung bình của $$y$$ khi $$x = 0$$.

Về mặt toán học, nó rất tiện. Nhưng về mặt thực tế, nó không phải lúc nào cũng dễ diễn giải.

Ví dụ:

- nếu $$x$$ là chiều cao tính bằng cm, thì $$x=0$$ là không có ý nghĩa thực tế.

Vì thế trong regression Bayes, ta thường:

- center hoặc standardize biến đầu vào,
- để intercept có ý nghĩa dễ đọc hơn.

### 3.2. Slope $$\beta$$

Slope cho biết:

- trung bình $$y$$ thay đổi bao nhiêu khi $$x$$ tăng 1 đơn vị.

Ví dụ:

- nếu $$\beta = 0.7$$ kg/cm, thì mỗi cm chiều cao tăng tương ứng với mức tăng trung bình 0.7 kg cân nặng.

### 3.3. Noise $$\sigma$$

Noise cho biết mức độ các điểm dữ liệu phân tán quanh đường hồi quy.

- $$\sigma$$ nhỏ  $$\rightarrow$$ dữ liệu bám sát đường hơn,
- $$\sigma$$ lớn  $$\rightarrow$$ dữ liệu phân tán mạnh hơn.

![Ý nghĩa của các tham số regression]({{ site.baseurl }}/img/chapter_img/chapter04/regression_parameter_interpretation.png)

## 4. Bayesian regression khác OLS ở đâu?

### OLS thường trả lời

- đường thẳng “tốt nhất” là gì?

### Bayesian regression trả lời

- những đường thẳng nào còn hợp lý sau khi thấy dữ liệu,
- mức độ bất định của slope và intercept là bao nhiêu,
- dự đoán cho quan sát mới bất định đến đâu.

Nói cách khác:

- OLS cho bạn một đường trung tâm,
- Bayes cho bạn một **phân phối của các đường có thể**.

## 5. Vì sao “generative” là một từ rất quan trọng?

Nếu bạn xem regression như generative model, bạn sẽ tự hỏi đúng câu hỏi hơn:

- dữ liệu được sinh ra từ quá trình nào,
- giả định Normal cho residual có hợp lý không,
- noise có đồng nhất theo mọi giá trị của $$x$$ không,
- và mô hình này có tạo ra dữ liệu giống với dữ liệu thật không.

Đây là khác biệt rất quan trọng giữa:

- “fit xong là xong”,
- và “mô hình hóa rồi kiểm tra”.

## 6. Viết mô hình Bayes đầy đủ

Một Bayesian linear regression tối giản có dạng:

$$
\alpha \sim p(\alpha)
$$

$$
\beta \sim p(\beta)
$$

$$
\sigma \sim p(\sigma)
$$

$$
y_i \sim \mathcal{N}(\alpha + \beta x_i,\sigma)
$$

Từ đó ta suy ra posterior:

$$
p(\alpha,\beta,\sigma \mid x,y).
$$

Điều quan trọng không phải là thuộc công thức này, mà là hiểu:

- prior nói điều gì trước dữ liệu,
- likelihood nói dữ liệu đến từ đâu,
- posterior là câu trả lời sau khi ghép cả hai lại.

## 7. Một ví dụ thực tế khác ngoài chiều cao - cân nặng

Regression Bayes xuất hiện ở rất nhiều nơi:

### Giá nhà và diện tích

- $$x$$: diện tích,
- $$y$$: giá nhà.

### Điểm thi và số giờ học

- $$x$$: số giờ ôn tập,
- $$y$$: điểm thi.

### Doanh thu và chi phí quảng cáo

- $$x$$: ngân sách ads,
- $$y$$: doanh thu.

Trong mọi ví dụ đó, tư duy generative vẫn giống nhau:

- có một xu hướng trung bình,
- dữ liệu thật dao động quanh xu hướng,
- và ta bất định về các tham số của xu hướng ấy.

## 8. Regression Bayes cho dự đoán như thế nào?

Giả sử bạn muốn dự đoán cân nặng của một người cao 175 cm.

Regression Bayes không chỉ cho một con số duy nhất. Nó cho:

- một giá trị trung bình dự đoán,
- bất định do chưa chắc về $$\alpha$$ và $$\beta$$,
- bất định do noise cá thể $$\sigma$$.

Đây là một điểm rất mạnh:

- ta không chỉ dự đoán,
- mà còn biết nên tự tin đến đâu vào dự đoán đó.

## 9. Một thói quen quan trọng từ bài này

Mỗi khi thấy regression, hãy tự hỏi:

1. dữ liệu đang được sinh ra như thế nào?
2. đâu là xu hướng trung bình?
3. đâu là phần noise?
4. tham số nào đang chưa biết?
5. dự đoán mới cần giữ lại những bất định nào?

Nếu làm được như vậy, bạn đã bắt đầu nghĩ như người làm Bayesian modeling chứ không chỉ như người chạy hồi quy.

> **3 ý cần nhớ.**
> 1. Bayesian linear regression là một generative model: dữ liệu được sinh quanh một xu hướng trung bình với nhiễu.
> 2. Intercept, slope và noise đều là các đại lượng chưa biết và phải được suy luận, không chỉ ước lượng bằng một con số điểm.
> 3. Regression Bayes mạnh ở chỗ giữ lại bất định của tham số lẫn dự đoán, thay vì chỉ đưa ra một đường thẳng duy nhất.

## Câu hỏi tự luyện

1. Hãy kể generative story cho mối quan hệ giữa số giờ học và điểm thi.
2. Vì sao $$\sigma$$ là một tham số rất quan trọng chứ không chỉ là “phần dư” phụ thêm?
3. Khác biệt lớn nhất giữa “fit a line” và “model a process” là gì?
4. Trong công việc của bạn, bài toán regression nào nên được nhìn theo tinh thần generative?

## Tài liệu tham khảo

- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4.
- Gelman, A. et al. *Regression and Other Stories*.
- Gelman, A. et al. *Bayesian Data Analysis* (3rd ed.), Chapters on regression.

---

*Bài học tiếp theo: [4.2 Priors for Regression - Chọn Prior có Nguyên tắc](/vi/chapter04/priors-for-regression/)*
