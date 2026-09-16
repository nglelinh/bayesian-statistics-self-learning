---
layout: post
title: "Bài 2.7: Ứng dụng hiện đại của prior liên hợp và cập nhật Bayes"
chapter: '02'
order: 7
owner: Nguyen Le Linh
lang: vi
categories:
- chapter02
lesson_type: optional
---

## Mục tiêu học tập

Sau bài tùy chọn này, bạn nhìn prior liên hợp (conjugate prior) và xấp xỉ lưới (grid approximation) như những lựa chọn thiết kế công nghiệp, không còn như mẹo làm bài. Bạn có thể chỉ vào một sản phẩm đang chạy—quảng cáo, xếp hạng, hoặc giám sát tần suất sự kiện—và nói likelihood đang giả định gì, họ prior nào giữ cho phép cập nhật đủ rẻ, và khi nào đại số phải nhường chỗ cho mô phỏng.

## Kiến thức cần có

Các bài 2.1–2.6 đã dựng bộ khung bốn phần: phân phối, likelihood, prior, posterior. Bài này không chứng minh lại liên hợp Beta–Binomial hay Gamma–Poisson. Nó hỏi vì sao các cặp ấy vẫn xuất hiện trong hệ thống khoa học máy tính lớn, và vì sao empirical Bayes thường là cách prior nhận được một con số.

## Mở đầu

Khi bạn đã cập nhật được một Beta bằng cách đếm số thành công, một nghi ngờ tự nhiên xuất hiện. Vì sao một công ty với hàng triệu người dùng vẫn cần posterior dạng đóng? Câu trả lời là độ trễ và tính nhiều nhiệm vụ. Một hệ quảng cáo hay xếp hạng có thể cần xác suất chuyển đổi cho mọi mục, mỗi phút. Một chuỗi MCMC cho từng mục thường quá chậm; một phép cập nhật liên hợp cộng số đếm vào $$(\alpha,\beta)$$ thì không. Căng thẳng trí tuệ vì thế vừa kinh tế vừa thống kê. Đại số chính xác sống sót ở những nơi nó *đủ nhanh để còn trung thực ở quy mô lớn*.

## Phát triển khái niệm

Prior liên hợp là một họ phân phối đứng yên trong chính nó sau khi nhân với likelihood. Với xác suất chuyển đổi $$\theta$$ và dữ liệu nhị thức, prior Beta cho

$$
\theta\mid y \sim \mathrm{Beta}(\alpha+y,\ \beta+n-y).
$$

Cùng phép cộng số đếm ấy, một bảng điều khiển gọi là “làm mượt”. Empirical Bayes chọn $$\alpha$$ và $$\beta$$ từ cả tập hợp các mục thay vì từ một chuyên gia đơn lẻ, nên một mục hiếm được vay sức từ toàn chợ. Khi likelihood rời họ mũ, hoặc prior phải phân cấp theo cách phá vỡ liên hợp, lưới bạn gặp ở bài 2.6 trở thành bức tranh đúng cuối cùng trước Hamiltonian Monte Carlo.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Tỷ lệ Beta–Binomial trong quảng cáo và xếp hạng

Hãy tưởng tượng mỗi mẫu quảng cáo, mỗi cặp truy vấn–mục, hay mỗi ghim gợi ý có một xác suất nhấp hoặc chuyển đổi chưa biết $$\theta_i$$. Câu chuyện dữ liệu rất trần: $$n_i$$ cơ hội, $$y_i$$ thành công. Một prior Beta chung, với siêu tham số khớp bằng empirical Bayes, kéo các mục ồn về phía trung bình của chợ. Đó là lý do một mục mới với một nhấp trên hai lần hiển thị không bị coi là chuyển đổi 50%. Trung bình hậu nghiệm

$$
\hat\theta_i=\frac{\alpha+y_i}{\alpha+\beta+n_i}
$$

là điểm xếp hạng có thể làm mới bằng phép cộng số nguyên. PinnerFormer của Pinterest (Pancha et al., 2022) là mô hình chuỗi cho biểu diễn người dùng, nhưng tầng phục vụ vẫn cần các tỷ lệ mục đứng vững; làm mượt liên hợp vẫn là bước Bayes rẻ đầu tiên dưới các ranker phức tạp hơn.

### 2. Thompson sampling như lấy mẫu posterior để quyết định

Russo et al. (2018) sắp xếp một sự thật mà các nền tảng vẫn cài mỗi ngày: nếu bạn lấy được mẫu từ $$p(\theta\mid y)$$, bạn có thể chọn hành động bằng cách giả bộ mẫu ấy là đúng. Với bandit Beta–Binomial, mẫu đó là một dòng mã. Câu chuyện sinh là tuần tự. Posterior hôm nay trở thành prior ngày mai; khám phá không phải heuristic mà là hệ quả của bề rộng posterior còn lại. Các contextual bandit hiện đại thay Beta bằng posterior hồi quy, nhưng quy tắc quyết định—lấy mẫu rồi hành động—vẫn là phép cập nhật bạn đã làm trên lưới.

### 3. Giám sát số đếm bằng Gamma–Poisson

Sự kiện hạ tầng, sụt chất lượng luồng, và số sự cố thường được mô hình hóa Poisson với prior Gamma trên cường độ. Posterior vẫn là Gamma sau một đêm đếm, nên hệ thống trực canh có thể báo một khoảng dự báo hậu nghiệm mà không cần bộ lấy mẫu. Khi phương sai vượt quá trung bình, câu chuyện phải đổi sang Negative Binomial và liên hợp không còn là bữa trưa miễn phí. Đó là lúc bài 2.6 đã chuẩn bị: vẽ lưới, thấy posterior méo đi, và thừa nhận dạng đóng đã hết.

### 4. Khi liên hợp thất bại: từ lưới đến lập trình xác suất

Stan, PyMC và NumPyro đều viết các mô hình liên hợp như những trường hợp bạn *không* nên phí một sampler, và các mô hình không liên hợp như lý do NUTS tồn tại. Lưới vẫn là hình dung đúng. Nó cho thấy tích chưa chuẩn hóa $$p(y\mid\theta)p(\theta)$$ như một phong cảnh. Hamiltonian Monte Carlo, sẽ vào Chương 4, là việc bạn làm khi phong cảnh ấy có quá nhiều tọa độ cho một lưới. Pathfinder (Zhang, Carpenter, Gelman và Vehtari, 2022) sau đó dùng một đường quasi-Newton để đặt một Gaussian rẻ gần cùng phong cảnh, thường để khởi động ấm. Các đối tượng Chương 2 không bị thay; chúng được cấp trình biên dịch.

## Diễn giải và nhận định

Một tỷ lệ bị co (shrinkage) không phải “CTR thật”. Nó là trung bình hậu nghiệm dưới một câu chuyện phân cấp, và câu chuyện ấy sai nếu các mục không trao đổi được với nhau—mẫu quảng cáo khác nước, hay truy vấn khác ý định. Thompson sampling không xóa regret; nó tiêu bất định posterior. Một khoảng Gamma bỏ qua điểm gãy sẽ trông sắc và đến muộn. Hãy đọc mọi dạng đóng như một giả định rằng quan sát kế tiếp vẫn cùng một loại.

## Ứng dụng

Quảng cáo, xếp hạng, độ tin cậy hệ thống, và thí nghiệm tuần tự là bốn nơi Chương 2 đã vào sản xuất. Chúng cũng chỉ ra ranh giới: liên hợp cho vòng trong, mô phỏng cho mô hình không còn viết vừa một bảng.

## Giới hạn và hướng mở rộng

Empirical Bayes ước lượng điểm các siêu tham số nên thường đánh giá thấp bất định về chính prior. Bayes phân cấp đầy đủ, vốn được tư duy đa mức ở Chương 5 bắt đầu thúc đẩy, đặt posterior lên $$(\alpha,\beta)$$. Xấp xỉ lưới chết khi số chiều lớn hơn vài đơn vị. Công cụ trung thực tiếp theo không phải bảng liên hợp dày hơn mà là một sampler, điều Chương 4 xây dựng.

## Bài tập

1. Hai mục có dữ liệu nhấp $$(y,n)=(1,2)$$ và $$(40,100)$$. Với prior $$\mathrm{Beta}(2,98)$$, trung bình hậu nghiệm nào dịch nhiều hơn, và quyết định sản phẩm nào được biện minh?
2. Viết câu chuyện sinh của Thompson sampling trên ba tiêu đề email. Cái gì quan sát được, cái gì ẩn, và khi nào nên dừng khám phá?
3. Một monitor Poisson–Gamma báo cường độ rất hẹp sau cuối tuần yên. Lưu lượng thứ Hai cao gấp mười. Giả định nào vừa vỡ?
4. Mở trang bắt đầu của PyMC hoặc Stan, tìm một ví dụ liên hợp và một ví dụ không liên hợp. Với ví dụ thứ hai, nói vì sao lưới sẽ thất bại.

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 2–3.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 6.
- Russo, D., Van Roy, B., Kazerouni, A., Osband, I., & Wen, Z. (2018). A tutorial on Thompson sampling. *Foundations and Trends in Machine Learning*, 11(1), 1–96.
- Pancha, N., Zhai, A., Leskovec, J., & Rosenberg, C. (2022). PinnerFormer: Sequence modeling for user representation at Pinterest. *KDD*. [arXiv:2205.04507](https://arxiv.org/abs/2205.04507).
- Zhang, L., Carpenter, B., Gelman, A., & Vehtari, A. (2022). Pathfinder: Parallel quasi-Newton variational inference. *JMLR*, 23(306), 1–49. [arXiv:2108.03782](https://arxiv.org/abs/2108.03782).
- [Stan User’s Guide](https://mc-stan.org/docs/stan-users-guide/index.html).
- [PyMC overview](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
- [NumPyro getting started](https://num.pyro.ai/en/stable/getting_started.html).
