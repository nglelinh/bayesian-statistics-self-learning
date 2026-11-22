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

Sau bài này, bạn sẽ biết cách lựa chọn phân phối tiên nghiệm (prior) cho mô hình hồi quy một cách có nguyên tắc. Bạn cũng sẽ hiểu vì sao chuẩn hóa dữ liệu (standardization) là bước nền quan trọng, vì sao phân phối tiên nghiệm thông tin yếu (weakly informative prior) thường là điểm khởi đầu phù hợp, và vì sao kiểm tra dự báo tiên nghiệm (prior predictive check) cần được thực hiện trước khi khớp mô hình.

> **Ví dụ ngắn.** Nếu đặt phân phối tiên nghiệm cho hệ số dốc quá rộng, mô hình có thể ngầm chấp nhận những đường hồi quy hoàn toàn phi thực tế theo kiến thức chuyên môn. Chọn phân phối tiên nghiệm cho hồi quy không phải là thao tác hình thức, mà là cách đặt ra biên giới hợp lý cho mô hình ngay từ đầu.
>
> **Câu hỏi tự kiểm tra.** Vì sao cùng một phân phối tiên nghiệm có thể hợp lý ở thang đo này nhưng lại bất hợp lý ở thang đo khác?

## 1. Khó khăn khi chọn phân phối tiên nghiệm cho hồi quy

Trong hồi quy tuyến tính cơ bản, ta có ít nhất ba tham số cần đặt phân phối tiên nghiệm: hệ số chặn $$\alpha$$, hệ số dốc $$\beta$$ và độ nhiễu $$\sigma$$. Nếu chọn thiếu cân nhắc, phân phối tiên nghiệm có thể quá rộng và cho phép những giá trị vô lý, quá hẹp và làm sai lệch phân phối hậu nghiệm, hoặc khiến bộ lấy mẫu (sampler) hoạt động kém ổn định. Do đó, chọn phân phối tiên nghiệm vừa đòi hỏi hiểu biết thống kê, vừa đòi hỏi nắm vững thang đo và bối cảnh thực tế của dữ liệu.

## 2. Chuẩn hóa dữ liệu: bước nên thực hiện trước khi đặt tiên nghiệm

Một trong những cách đơn giản và hiệu quả nhất để việc chọn phân phối tiên nghiệm trở nên nhất quán hơn là chuẩn hóa (standardize) các biến đầu vào và đầu ra:

$$
x_{std} = \frac{x-\bar{x}}{\mathrm{SD}(x)}, \qquad
y_{std} = \frac{y-\bar{y}}{\mathrm{SD}(y)}.
$$

Sau phép biến đổi này, các biến đều có trung bình bằng 0 và độ lệch chuẩn bằng 1, giúp việc chọn phân phối tiên nghiệm theo thang đo chuẩn trở nên trực quan hơn nhiều.

![Dữ liệu ở thang đo gốc trước khi standardize]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_standardization_raw_data.png)

![Dữ liệu sau khi standardize về mean 0 và SD 1]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_standardization_standardized_data.png)

### Ba lợi ích chính của chuẩn hóa dữ liệu

1. **Hệ số chặn dễ diễn giải hơn.** Sau khi dịch tâm hoặc chuẩn hóa, hệ số chặn tương ứng với giá trị kỳ vọng của $$y$$ tại mức trung bình của $$x$$, thay vì tại mốc $$x = 0$$ vốn có thể vô nghĩa.
2. **Phân phối tiên nghiệm ít phụ thuộc vào đơn vị đo.** Cùng một công thức tiên nghiệm có thể mang ý nghĩa rất khác nhau nếu đổi đơn vị từ cm sang m hoặc từ kg sang pound. Chuẩn hóa loại bỏ sự lệ thuộc này.
3. **Bộ lấy mẫu hội tụ ổn định hơn.** Khi các biến nằm trên cùng một thang đo, hình dạng phân phối hậu nghiệm thường cân đối hơn, giúp các thuật toán lấy mẫu như HMC/NUTS hoạt động hiệu quả hơn.

### 2.1. Ví dụ minh họa: cùng một tiên nghiệm trước và sau khi chuẩn hóa

Giả sử $$x$$ là chiều cao tính bằng cm (chủ yếu trong khoảng 150–190 cm) và $$y$$ là cân nặng tính bằng kg (khoảng 45–90 kg). Nếu chưa chuẩn hóa mà đặt trực tiếp:

$$
\alpha \sim \mathcal{N}(0,1), \qquad \beta \sim \mathcal{N}(0,1),
$$

thì hai phân phối này tuy gọn về mặt ký hiệu nhưng bất hợp lý về mặt ngữ nghĩa:

- Tiên nghiệm $$\alpha \sim \mathcal{N}(0,1)$$ ngầm cho rằng khi $$x = 0$$ cm, cân nặng trung bình nằm quanh 0 kg — một phát biểu không có ý nghĩa thực tế.
- Tiên nghiệm $$\beta \sim \mathcal{N}(0,1)$$ có khoảng 95% xấp xỉ $$[-2, 2]$$ kg/cm. Nghĩa là chỉ cần chênh lệch 20 cm chiều cao, mô hình đã cho phép mức chênh cân nặng trung bình từ $$-40$$ đến $$40$$ kg, quá rộng so với thực tế.

Ngược lại, sau khi chuẩn hóa $$x$$ và $$y$$ thành $$x_{std}$$ và $$y_{std}$$, cùng cặp phân phối tiên nghiệm:

$$
\alpha \sim \mathcal{N}(0,1), \qquad \beta \sim \mathcal{N}(0,1)
$$

lại mang ý nghĩa rõ ràng và hợp lý hơn nhiều:

- $$\alpha$$ quanh 0 có nghĩa là tại mức chiều cao trung bình, cân nặng kỳ vọng cũng nằm quanh mức trung bình của tập dữ liệu.
- $$\beta$$ quanh 0 với độ lệch chuẩn 1 có nghĩa là khi $$x$$ tăng thêm 1 độ lệch chuẩn, $$y$$ thường thay đổi trong phạm vi vài độ lệch chuẩn — đủ linh hoạt cho dữ liệu nhưng loại bỏ được các giá trị cực đoan.

Như vậy, chuẩn hóa không chỉ là kỹ thuật tính toán mà còn giúp ta diễn giải phân phối tiên nghiệm một cách trực quan.

## 3. Phân phối tiên nghiệm cho hệ số chặn $$\alpha$$

Sau khi chuẩn hóa dữ liệu, hệ số chặn thường nằm gần 0 với mức độ bất định vừa phải. Vì vậy, những lựa chọn như:

$$
\alpha \sim \mathcal{N}(0,1)
$$

hoặc

$$
\alpha \sim \mathcal{N}(0,2)
$$

thường là điểm khởi đầu phù hợp. Ba biểu đồ dưới đây minh họa sự khác biệt giữa phân phối tiên nghiệm quá rộng, thông tin yếu (vừa phải) và quá hẹp cho hệ số chặn.

![Prior quá rộng cho intercept]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_intercept_too_wide.png)

![Prior weakly informative cho intercept]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_intercept_weakly_informative.png)

![Prior quá hẹp cho intercept]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_intercept_too_narrow.png)

Nguyên tắc chung ở đây khá rõ: tiên nghiệm quá rộng cho phép các giá trị thiếu thực tế, tiên nghiệm quá hẹp áp đặt ràng buộc quá mạnh lên ước lượng, còn tiên nghiệm vừa phải vừa có tác dụng điều chuẩn (regularization) vừa để dữ liệu đóng vai trò chính.

## 4. Phân phối tiên nghiệm cho hệ số dốc $$\beta$$

Trên thang đo chuẩn hóa, hệ số dốc $$\beta$$ biểu thị mức thay đổi trung bình của $$y$$ (tính theo độ lệch chuẩn) khi $$x$$ tăng thêm 1 độ lệch chuẩn. Khi chưa có thông tin chuyên sâu về độ lớn của tác động, một phân phối tiên nghiệm thông tin yếu như:

$$
\beta \sim \mathcal{N}(0,1)
$$

thường là lựa chọn hợp lý. Phân phối này cho phép cả mối quan hệ dương lẫn âm, đồng thời hạn chế các hệ số dốc quá cực đoan. Ba hình dưới đây so sánh trực quan ba mức độ rộng khác nhau của tiên nghiệm cho hệ số dốc.

![Prior quá rộng cho slope]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_slope_too_wide.png)

![Prior weakly informative cho slope]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_slope_weakly_informative.png)

![Prior quá hẹp cho slope]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_slope_too_narrow.png)

## 5. Phân phối tiên nghiệm cho độ nhiễu $$\sigma$$

Do $$\sigma > 0$$, ta cần chọn các phân phối chỉ nhận giá trị dương như HalfNormal, Exponential hoặc HalfStudentT. Sau khi chuẩn hóa dữ liệu, một lựa chọn phổ biến là:

$$
\sigma \sim \mathrm{HalfNormal}(1).
$$

![Đường prior HalfNormal cho noise sigma]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_noise_halfnormal_curve.png)

Lựa chọn này phản ánh kỳ vọng rằng độ nhiễu nằm ở mức vừa phải trên thang chuẩn hóa, đồng thời vẫn đủ mở để mô hình thích ứng nếu dữ liệu thực tế có độ phân tán lớn hơn.

![Tóm tắt cách đọc prior cho noise sigma]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_noise_halfnormal_summary.png)

## 6. Phân phối tiên nghiệm thông tin yếu là gì và vì sao nên bắt đầu từ đó?

Phân phối tiên nghiệm thông tin yếu (weakly informative prior) không mang nghĩa "hoàn toàn không có thông tin". Ngược lại, nó thể hiện mục tiêu không áp đặt niềm tin quá chặt lên mô hình, nhưng vẫn loại bỏ được những vùng tham số phi lý mà kiến thức chuyên môn có thể bác bỏ ngay từ đầu. Trong hồi quy, loại tiên nghiệm này giúp điều chuẩn mô hình, ổn định phân phối hậu nghiệm và giảm nguy cơ bộ lấy mẫu đi vào những vùng tham số không có ý nghĩa.

## 7. Kiểm tra dự báo tiên nghiệm (prior predictive check)

Nếu chỉ quan sát biểu đồ mật độ trên không gian tham số, đôi khi rất khó đánh giá một phân phối tiên nghiệm có hợp lý hay không. Cách kiểm tra hiệu quả hơn là dùng chính các phân phối tiên nghiệm đó để mô phỏng dữ liệu giả lập: rút nhiều mẫu $$(\alpha, \beta, \sigma)$$ từ tiên nghiệm, vẽ các đường hồi quy tương ứng và xem liệu dữ liệu được sinh ra có phù hợp với thực tế hay không.

![Prior predictive với slope weakly informative]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_predictive_weakly_informative.png)

Nếu phân phối tiên nghiệm sinh ra các đường hồi quy có độ dốc cực đoan hoặc tạo ra những dự đoán vô lý như cân nặng âm, điểm thi 300 điểm hay doanh thu tăng giảm phi thực tế, thì phân phối tiên nghiệm cần được điều chỉnh lại — dù về mặt toán học nó hoàn toàn hợp lệ.

![Prior predictive với slope quá rộng]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_predictive_too_wide.png)

## 8. Ví dụ trực quan: chi phí quảng cáo và doanh thu

Giả sử $$x$$ là chi phí quảng cáo và $$y$$ là doanh thu. Nếu phân phối tiên nghiệm của hệ số dốc quá rộng, mô hình sẽ ngầm cho phép kịch bản tăng rất ít ngân sách nhưng doanh thu tăng đột biến phi thực tế, hoặc ngược lại, tăng nhẹ ngân sách nhưng doanh thu sụt giảm nghiêm trọng. Trước khi nhìn vào dữ liệu, kiến thức thực tế đã cho thấy những kịch bản đó không hợp lý, và phân phối tiên nghiệm cần phản ánh điều này.

### 8.1. Đọc kết quả kiểm tra dự báo tiên nghiệm bằng con số

Giả sử dữ liệu quảng cáo và doanh thu đã được chuẩn hóa, và bạn đang cân nhắc giữa hai phân phối tiên nghiệm cho hệ số dốc:

$$
\beta \sim \mathcal{N}(0,3)
$$

hoặc

$$
\beta \sim \mathcal{N}(0,0.5).
$$

Với lựa chọn thứ nhất, khoảng 95% của $$\beta$$ xấp xỉ $$[-6, 6]$$. Khi một chiến dịch có chi phí ở mức $$x_{std} = 2$$ (cao hơn trung bình 2 độ lệch chuẩn), chỉ riêng giá trị trung bình dự đoán:

$$
\mu = \alpha + \beta x_{std}
$$

đã có thể dao động quanh khoảng $$-12$$ đến $$12$$ độ lệch chuẩn của $$y$$, chưa kể phần nhiễu. Trong hầu hết bối cảnh kinh doanh, biên độ này rộng một cách phi thực tế.

Ngược lại, với

$$
\beta \sim \mathcal{N}(0,0.5),
$$

khoảng 95% của hệ số dốc thu gọn về xấp xỉ $$[-1, 1]$$. Tại cùng mức $$x_{std} = 2$$, giá trị trung bình dự đoán chủ yếu nằm trong phạm vi $$-2$$ đến $$2$$ độ lệch chuẩn quanh mức trung tâm — vẫn đủ linh hoạt nhưng sát với thực tế hơn nhiều. Ví dụ này cho thấy kiểm tra dự báo tiên nghiệm hữu ích hơn việc chỉ nhìn vào tham số vì nó chuyển đổi phân phối tiên nghiệm sang chính ngôn ngữ của dữ liệu quan sát.

## 9. Phân tích độ nhạy của phân phối tiên nghiệm (prior sensitivity analysis)

Sau khi ước lượng mô hình, một bước kiểm tra quan trọng là đặt câu hỏi: **Nếu thay đổi phân phối tiên nghiệm sang một vài phương án hợp lý lân cận, phân phối hậu nghiệm có biến đổi đáng kể không?** Nếu kết quả thay đổi mạnh, điều đó cho thấy dữ liệu chưa đủ mạnh để áp đảo tiên nghiệm và kết luận chịu ảnh hưởng rõ rệt từ giả định ban đầu — một thông tin cần được trình bày minh bạch khi báo cáo.

![Posterior khi thay đổi các prior hợp lý khác nhau]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_sensitivity_posterior_overlay.png)

Phân tích độ nhạy không nhằm tìm ra một phân phối tiên nghiệm "duy nhất đúng", mà nhằm đo lường mức độ phụ thuộc của kết luận vào lựa chọn tiên nghiệm.

![Tóm tắt cách đọc prior sensitivity analysis]({{ site.baseurl }}/img/chapter_img/chapter04/chapter04_prior_sensitivity_summary.png)

## 10. Bộ phân phối tiên nghiệm khởi đầu thực dụng

Với dữ liệu đã được chuẩn hóa, một bộ phân phối tiên nghiệm khởi đầu hợp lý cho hồi quy tuyến tính đơn giản thường là:

$$
\alpha \sim \mathcal{N}(0,1)
$$

$$
\beta \sim \mathcal{N}(0,1)
$$

$$
\sigma \sim \mathrm{HalfNormal}(1)
$$

Đây không phải công thức cố định cho mọi bài toán, nhưng là điểm xuất phát an toàn để bắt đầu và điều chỉnh tiếp theo bối cảnh cụ thể.

## 11. Những sai lầm phổ biến khi chọn phân phối tiên nghiệm

- **Bỏ qua thang đo dữ liệu:** đặt tiên nghiệm theo thói quen mà không kiểm tra đơn vị đo là lỗi thường gặp nhất.
- **Dùng tiên nghiệm quá rộng và xem là "không thông tin":** tiên nghiệm trải quá phẳng thường gây khó khăn cho bộ lấy mẫu, tạo dự báo tiên nghiệm phi thực tế và làm giảm độ ổn định của ước lượng.
- **Bỏ qua bước kiểm tra dự báo tiên nghiệm:** nếu không mô phỏng dữ liệu từ tiên nghiệm, ta rất dễ bỏ sót các giả định vô lý ẩn sau công thức.
- **Không thực hiện phân tích độ nhạy:** ngay cả khi tiên nghiệm ban đầu có vẻ hợp lý, vẫn nên đối chiếu với một vài lựa chọn lân cận để đánh giá độ vững của kết luận.

> **3 ý cần nhớ.** Chuẩn hóa dữ liệu giúp việc chọn và diễn giải phân phối tiên nghiệm trong hồi quy trở nên đơn giản và nhất quán hơn; phân phối tiên nghiệm thông tin yếu giúp loại bỏ các giá trị phi thực tế mà vẫn để dữ liệu đóng vai trò quyết định; và kiểm tra dự báo tiên nghiệm cùng phân tích độ nhạy là hai công cụ cốt lõi để thẩm định lựa chọn tiên nghiệm.

## Video tham khảo

- [Bayesian Priors Explained | Prior Modelling & Prior Predictive Checks](https://www.youtube.com/watch?v=G3ludfAUAng) — stats 4 good, English. **xem trước**. Trình bày cách xây dựng phân phối tiên nghiệm và kiểm tra bằng dự báo tiên nghiệm, khớp với quy trình thực hành trong bài.
- [Keynote 2: Weakly Informative Priors -- Andrew Gelman](https://www.youtube.com/watch?v=UH6-9FU6bRg) — AISTATS 2014, English. Giải thích cơ sở của phân phối tiên nghiệm thông tin yếu, bổ trợ cho phần lấy tiên nghiệm loại này làm điểm khởi đầu.
- [Standardized variables in a simple regression](https://www.youtube.com/watch?v=RTFnrK5ZZ8E) — Jos Dornschneider-Elkink, English. Minh họa sự thay đổi ý nghĩa của các hệ số hồi quy sau khi chuẩn hóa biến, làm rõ lý do nên chuẩn hóa trước khi đặt tiên nghiệm.

## Câu hỏi tự luyện

1. Vì sao chuẩn hóa dữ liệu giúp việc lựa chọn phân phối tiên nghiệm trở nên dễ dàng hơn?
2. Hãy diễn giải bằng lời ý nghĩa của một phân phối tiên nghiệm thông tin yếu đặt cho hệ số dốc.
3. Kiểm tra dự báo tiên nghiệm giúp phát hiện điều gì mà việc chỉ quan sát phân phối tiên nghiệm trên tham số có thể bỏ sót?
4. Trong một bài toán hồi quy thuộc lĩnh vực của bạn, tham số nào đòi hỏi phải chọn phân phối tiên nghiệm cẩn thận nhất?

## Tài liệu tham khảo

- Gelman, A., Simpson, D., & Betancourt, M. (2017). The prior can often only be understood in the context of the likelihood.
- McElreath, R. *Statistical Rethinking* (2nd ed.), Chapter 4.
- Gelman, A. et al. *Regression and Other Stories*.

---

*Bài học tiếp theo: [4.3 Posterior Inference với PyMC - Từ Theory đến Practice]({{ site.baseurl }}/contents/vi/chapter04/04_03_posterior_inference_pymc/)*
