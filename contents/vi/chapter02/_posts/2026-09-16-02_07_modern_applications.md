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

Dù các mô hình học sâu ngày nay có hàng tỷ tham số, những cặp liên hợp giản dị như Beta–Binomial hay Gamma–Poisson vẫn đang chạy trong trái tim của nhiều hệ thống công nghiệp khổng lồ: từ thuật toán *Thompson Sampling* phân bổ quảng cáo theo thời gian thực, hệ thống ước lượng tỷ lệ lỗi vi dịch vụ (microservices) đến các bộ lọc dự báo nhu cầu bán lẻ có hàng triệu mã hàng.

Bài tổng kết Chương 2 này kết nối các khái niệm cốt lõi — prior, likelihood, posterior, liên hợp và xấp xỉ lưới — với cách kỹ sư dữ liệu ứng dụng chúng để ra quyết định nhanh, ổn định và có kiểm soát bất định trong thực tế.

---

## Mục tiêu học tập

Sau bài học tùy chọn này, bạn sẽ nhìn nhận prior liên hợp (conjugate prior) và xấp xỉ lưới (grid approximation) như những lựa chọn thiết kế hệ thống thực tế chứ không chỉ là kỹ thuật làm bài tập. Bạn có thể quan sát một hệ thống đang vận hành — như quảng cáo, xếp hạng hay giám sát sự cố — và chỉ ra likelihood đang giả định điều gì, họ prior nào giữ chi phí cập nhật ở mức thấp, và khi nào phép tính giải tích phải nhường chỗ cho mô phỏng.


## Bản đồ kiến thức nền: Cập nhật liên hợp trong hệ thống trực tuyến và Thử nghiệm thích nghi

Ba trụ cột ứng dụng dưới đây giải thích vì sao kiến thức Chương 2 có sức sống bền bỉ trong kỹ thuật hiện đại:

- **Cập nhật trực tuyến chi phí $$O(1)$$ (Streaming Conjugate Updates):** Trong các hệ thống thời gian thực xử lý hàng triệu sự kiện mỗi giây, không thể chạy MCMC lại từ đầu mỗi khi có một lượt nhấp chuột mới. Mô hình Beta–Binomial và Gamma–Poisson cho phép cập nhật hậu nghiệm tức thì chỉ bằng phép cộng số đếm.
- **Thompson Sampling (Multi-Armed Bandits):** Thay vì chia đều lưu lượng 50/50 trong suốt thí nghiệm A/B, thuật toán rút ngẫu nhiên một mẫu $$\tilde p_a \sim \text{Beta}(\alpha_a, \beta_a)$$ từ hậu nghiệm của mỗi phương án và chọn phương án có mẫu lớn nhất — tự động giảm thiểu tổn thất cơ hội (*regret*).
- **Làm trơn dữ liệu thưa (Empirical Bayes Shrinkage):** Khi xếp hạng hàng nghìn sản phẩm hay bài viết mới chỉ có vài lượt đánh giá, thay tỷ lệ thô bằng kỳ vọng hậu nghiệm giúp chống nhiễu mẫu nhỏ cực kỳ hiệu quả.

---

## Kiến thức cần có

Các bài 2.1–2.6 đã xây dựng bộ khung gồm bốn thành phần: phân phối, likelihood, prior và posterior. Bài viết này không chứng minh lại tính liên hợp của Beta–Binomial hay Gamma–Poisson, mà tập trung trả lời vì sao các cặp này vẫn xuất hiện trong các hệ thống khoa học máy tính quy mô lớn và vì sao empirical Bayes thường được dùng để chọn tham số cho prior.

## Mở đầu

Khi đã quen với việc cập nhật phân phối Beta bằng cách đếm số lần thành công, một câu hỏi tự nhiên nảy ra: vì sao một nền tảng có hàng triệu người dùng vẫn cần đến posterior dạng đóng? Câu trả lời nằm ở yêu cầu độ trễ thấp và số lượng thực thể rất lớn. Một hệ thống quảng cáo hay xếp hạng có thể phải cập nhật xác suất chuyển đổi cho hàng triệu mục sau mỗi phút. Chạy chuỗi MCMC cho từng mục là quá chậm, trong khi phép cập nhật liên hợp chỉ cần cộng số đếm vào $$(\alpha,\beta)$$ nên chạy gần như tức thời. Bài toán đặt ra vì thế vừa mang tính hiệu năng vừa mang tính thống kê: các công thức giải tích vẫn giữ vị trí quan trọng ở những nơi chúng đủ nhanh để duy trì suy luận trung thực ở quy mô lớn.

## Phát triển khái niệm

Prior liên hợp là họ phân phối đóng dưới phép nhân với likelihood: posterior thu được vẫn thuộc cùng họ đó. Với xác suất chuyển đổi $$\theta$$ và dữ liệu nhị thức, prior Beta cho:

$$
\theta\mid y \sim \mathrm{Beta}(\alpha+y,\ \beta+n-y).
$$

Trên các bảng điều khiển phân tích, chính phép cộng số đếm này thường được gọi là “làm mượt” (smoothing). Phương pháp **empirical Bayes** ước lượng $$\alpha$$ và $$\beta$$ từ toàn bộ tập hợp các mục thay vì chỉ hỏi một chuyên gia đơn lẻ, nhờ đó một mục mới hoặc hiếm dữ liệu có thể mượn thông tin từ toàn hệ thống. Khi likelihood không còn thuộc họ mũ hoặc khi cấu trúc prior phân cấp phá vỡ tính liên hợp, xấp xỉ lưới ở Bài 2.6 là trực giác hình học cuối cùng trước khi chuyển sang Hamiltonian Monte Carlo.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Ước lượng tỷ lệ Beta–Binomial trong quảng cáo và xếp hạng

Xét mỗi mẫu quảng cáo, mỗi cặp truy vấn–mục, hoặc mỗi nội dung gợi ý có một xác suất nhấp hay chuyển đổi chưa biết $$\theta_i$$. Cấu trúc dữ liệu rất gọn: $$n_i$$ lượt hiển thị và $$y_i$$ lượt thành công. Một prior Beta dùng chung — với siêu tham số được ước lượng bằng empirical Bayes — sẽ kéo ước lượng của các mục ít dữ liệu, nhiều nhiễu về gần mức trung bình chung của hệ thống. Nhờ vậy, một mục mới chỉ có 1 lượt nhấp trên 2 lượt hiển thị sẽ không bị đánh giá là có tỷ lệ chuyển đổi 50%. Trung bình hậu nghiệm:

$$
\hat\theta_i=\frac{\alpha+y_i}{\alpha+\beta+n_i}
$$

đóng vai trò điểm xếp hạng có thể cập nhật liên tục chỉ bằng phép cộng số nguyên. Chẳng hạn, PinnerFormer của Pinterest (Pancha et al., 2022) là mô hình tuần tự biểu diễn hành vi người dùng, nhưng tầng phục vụ (serving layer) vẫn cần các ước lượng tỷ lệ ổn định cho từng mục; làm mượt liên hợp vì thế vẫn là lớp suy luận Bayes chi phí thấp đứng nền cho các bộ xếp hạng phức tạp hơn.

### 2. Thompson sampling: lấy mẫu từ posterior để ra quyết định

Russo et al. (2018) hệ thống hóa một nguyên lý đang được triển khai hằng ngày trên nhiều nền tảng: nếu có thể lấy mẫu từ $$p(\theta\mid y)$$, bạn có thể chọn hành động tối ưu bằng cách hành động như thể giá trị vừa lấy mẫu là tham số thực. Với bài toán bandit Beta–Binomial, thao tác lấy mẫu này chỉ tốn một dòng mã. Cơ chế sinh dữ liệu diễn ra tuần tự: posterior hôm nay trở thành prior ngày mai, còn hoạt động thăm dò (exploration) không phải quy tắc cảm tính mà là hệ quả tự nhiên của độ rộng posterior còn lại. Các hệ thống contextual bandit hiện đại thay phân phối Beta bằng posterior của mô hình hồi quy, nhưng nguyên tắc quyết định — lấy mẫu rồi hành động — vẫn xuất phát từ chính cơ chế cập nhật ở Chương 2.

### 3. Giám sát số đếm bằng Gamma–Poisson

Các sự kiện hạ tầng, suy giảm chất lượng luồng dữ liệu và số lượng sự cố thường được mô hình hóa bằng Poisson với prior Gamma trên cường độ. Sau mỗi chu kỳ đếm, posterior vẫn là phân phối Gamma, giúp hệ thống trực canh tính ngay khoảng dự báo hậu nghiệm mà không cần bộ lấy mẫu. Tuy nhiên, khi phương sai vượt quá trung bình (overdispersion), mô hình cần chuyển sang Negative Binomial và không còn giữ được dạng đóng liên hợp thuận tiện nữa. Khi đó, tư duy của Bài 2.6 phát huy tác dụng: quan sát posterior trên lưới, nhận ra phân phối bị lệch và chấp nhận rằng lời giải giải tích đã đạt giới hạn.

### 4. Khi tính liên hợp không còn đáp ứng: từ lưới đến lập trình xác suất

Các thư viện lập trình xác suất như Stan, PyMC và NumPyro đều coi mô hình liên hợp là trường hợp không cần tiêu tốn tài nguyên cho bộ lấy mẫu, còn các mô hình không liên hợp chính là lý do thuật toán NUTS ra đời. Xấp xỉ lưới vẫn giữ vai trò hình dung cốt lõi: nó cho thấy tích chưa chuẩn hóa $$p(y\mid\theta)p(\theta)$$ như một bề mặt mật độ trên không gian tham số. Hamiltonian Monte Carlo (trình bày ở Chương 4) là công cụ dùng khi bề mặt đó có quá nhiều chiều để dựng lưới. Sau đó, Pathfinder (Zhang, Carpenter, Gelman và Vehtari, 2022) sử dụng quỹ đạo tối ưu quasi-Newton để dựng nhanh một xấp xỉ Gaussian quanh vùng mật độ cao đó, thường dùng làm bước khởi tạo (warm start). Các khái niệm của Chương 2 không bị thay thế, mà được tự động hóa bằng các công cụ tính toán hiện đại.

## Diễn giải và nhận định

Một tỷ lệ đã qua phép co về trung bình (shrinkage) không phải là “CTR thực”, mà là trung bình hậu nghiệm dưới một giả định phân cấp; giả định này sẽ sai lệch nếu các mục không tương đương để chia sẻ thông tin (chẳng hạn mẫu quảng cáo thuộc các thị trường khác nhau hoặc truy vấn có mục đích khác nhau). Thompson sampling không triệt tiêu hoàn toàn độ hối tiếc (regret), mà giảm dần nó khi độ bất định của posterior thu hẹp. Tương tự, một khoảng dự báo Gamma bỏ qua điểm chuyển chế độ (changepoint) sẽ trông rất hẹp nhưng phản ứng chậm khi hệ thống thay đổi đột ngột. Mọi công thức dạng đóng đều ngầm giả định rằng quan sát kế tiếp vẫn tuân theo cùng một quy luật sinh dữ liệu.

## Ứng dụng

Quảng cáo, hệ xếp hạng, giám sát độ tin cậy hệ thống và thử nghiệm tuần tự là bốn lĩnh vực đưa kiến thức Chương 2 trực tiếp vào vận hành thực tế. Chúng cũng vạch rõ ranh giới thiết kế: dùng prior liên hợp cho vòng tính toán lõi đòi hỏi tốc độ cao, và dùng mô phỏng cho những mô hình không còn biểu diễn gọn bằng công thức đóng.

## Giới hạn và hướng mở rộng

Empirical Bayes chỉ ước lượng điểm các siêu tham số nên thường đánh giá thấp độ bất định của chính prior. Cách tiếp cận Bayes phân cấp đầy đủ — được mở ra qua tư duy đa mức ở Chương 5 — đặt phân phối hậu nghiệm lên chính $$(\alpha,\beta)$$. Trong khi đó, xấp xỉ lưới nhanh chóng mất khả thi khi số chiều vượt quá vài tham số. Bước tiến trung thực tiếp theo không phải là mở rộng bảng công thức liên hợp mà là sử dụng bộ lấy mẫu — trọng tâm của Chương 4.


## Khung giải thích (nên đọc chậm): Giải bài toán "5 sao nhưng chỉ có 1 lượt đánh giá" bằng co cụm Bayes

Trong thương mại điện tử, một sản phẩm có 1/1 đánh giá tốt (100%) có thực sự đáng tin hơn sản phẩm có 90/100 đánh giá tốt (90%) không? Hãy đi qua 3 bước xử lý bằng prior liên hợp:

1. **Ước lượng mức nền toàn sàn làm Prior:** Giả sử trung bình toàn sàn có tỷ lệ đánh giá tốt là $$80\%$$, chọn prior $$\text{Beta}(8, 2)$$ (cỡ mẫu ảo $$M = 10$$).
2. **Cập nhật hậu nghiệm cho từng sản phẩm:** Cộng số đánh giá tốt vào $$\alpha = 8$$ và số đánh giá xấu vào $$\beta = 2$$.
3. **Xếp hạng theo kỳ vọng hậu nghiệm (hoặc cận dưới 5% của hậu nghiệm):** Sản phẩm ít dữ liệu bị kéo về mức nền toàn sàn, còn sản phẩm nhiều dữ liệu giữ sát tỷ lệ thực tế của chính nó.

### Ví dụ tính toán cầm tay chỉ việc: Xếp hạng 2 sản phẩm với Prior $$\text{Beta}(8, 2)$$

| Sản phẩm | Dữ liệu $$(k / n)$$ | Tỷ lệ thô (MLE) | Hậu nghiệm | Kỳ vọng hậu nghiệm $$\mathbb{E}[p \vert y]$$ |
| --- | --- | --- | --- | --- |
| Sản phẩm A (mới) | $$1 / 1$$ | $$100.0\%$$ | $$\text{Beta}(9, 2)$$ | $$9 / 11 \approx 81.8\%$$ |
| Sản phẩm B (uy tín) | $$90 / 100$$ | $$90.0\%$$ | $$\text{Beta}(98, 12)$$ | $$98 / 110 \approx 89.1\%$$ |

Thứ tự xếp hạng lập tức trở nên hợp lý: Sản phẩm B ($$89.1\%$$) đứng trên Sản phẩm A ($$81.8\%$$), khắc phục triệt để lỗi "nhiễu mẫu nhỏ" mà không cần đặt các luật lọc cứng nhắc tùy tiện.

**Hiểu lầm cần tránh:** Dùng cùng một prior toàn cục cho các danh mục hàng hóa có chất lượng nền hoàn toàn khác nhau — khi đó nên nâng cấp lên mô hình phân cấp (Chương 5) để mỗi danh mục có prior riêng.

**Kiểm tra nhanh:** Nếu Sản phẩm A tiếp tục nhận thêm 19 đánh giá tốt nữa (tổng 20/20), hậu nghiệm trở thành $$\text{Beta}(28, 2)$$ với kỳ vọng $$28/30 \approx 93.3\%$$ — lúc này bằng chứng đã đủ mạnh để vượt lên trên Sản phẩm B.

---

## Video tham khảo

- [What is a conjugate prior?](https://www.youtube.com/watch?v=aPNrhR0dFi8) — Ben Lambert, English. **xem trước**. Ôn lại điều kiện để prior liên hợp mang lại phép cập nhật gọn, phù hợp với góc nhìn thiết kế hệ thống trong bài.
- [How to Estimate Rates with a Gamma-Poisson Bayesian Model | Conjugate Priors](https://www.youtube.com/watch?v=m8roQUqmybg) — Drawing Distributions, English. Minh họa cách mô hình Gamma–Poisson ước lượng tốc độ sự kiện, hỗ trợ ví dụ giám sát tần suất.
- [Bayesian Updates and Conjugate Priors](https://www.youtube.com/watch?v=GqSX-8AQL90) — Steve Brunton, English. Trình bày quá trình cập nhật liên hợp lặp lại khi dữ liệu đến liên tục, gắn với các hệ thống vận hành thời gian thực.

## Bài tập

1. Hai mục có dữ liệu lượt nhấp $$(y,n)=(1,2)$$ và $$(40,100)$$. Với prior $$\mathrm{Beta}(2,98)$$, trung bình hậu nghiệm của mục nào dịch chuyển mạnh hơn so với tỷ lệ thô, và quyết định sản phẩm nào được rút ra từ đó?
2. Viết câu chuyện sinh dữ liệu cho Thompson sampling với ba tiêu đề email: đại lượng nào quan sát được, đại lượng nào ẩn, và khi nào nên dừng giai đoạn thăm dò?
3. Một bộ giám sát Poisson–Gamma cho ước lượng cường độ rất hẹp sau một cuối tuần yên ắng, nhưng sang thứ Hai lưu lượng tăng gấp mười lần. Giả định nào của mô hình vừa bị phá vỡ?
4. Mở trang tài liệu khởi đầu của PyMC hoặc Stan, tìm một ví dụ liên hợp và một ví dụ không liên hợp; với ví dụ thứ hai, giải thích vì sao xấp xỉ lưới sẽ không khả thi.

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 2–3.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 6.
- Russo, D., Van Roy, B., Kazerouni, A., Osband, I., & Wen, Z. (2018). A tutorial on Thompson sampling. *Foundations and Trends in Machine Learning*, 11(1), 1–96.
- Pancha, N., Zhai, A., Leskovec, J., & Rosenberg, C. (2022). PinnerFormer: Sequence modeling for user representation at Pinterest. *KDD*. [arXiv:2205.04507](https://arxiv.org/abs/2205.04507).
- Zhang, L., Carpenter, B., Gelman, A., & Vehtari, A. (2022). Pathfinder: Parallel quasi-Newton variational inference. *JMLR*, 23(306), 1–49. [arXiv:2108.03782](https://arxiv.org/abs/2108.03782).
- [Stan User’s Guide](https://mc-stan.org/docs/stan-users-guide/index.html).
- [PyMC overview](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/pymc_overview.html).
- [NumPyro getting started](https://num.pyro.ai/en/stable/getting_started.html).
