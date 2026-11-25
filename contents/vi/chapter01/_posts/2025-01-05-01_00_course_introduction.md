---
layout: post
title: "Giới thiệu Khóa học: Phân tích Dữ liệu Bayes"
chapter: '01'
order: 0
owner: Nguyen Le Linh
lang: vi
categories:
- chapter01
lesson_type: required
---

Hầu hết chúng ta học thống kê lần đầu qua một danh sách dài các kiểm định rời rạc: kiểm định $$t$$, kiểm định $$\chi^2$$, ANOVA, từng công thức riêng cho từng bảng số liệu. Thống kê Bayes mở ra một con đường hoàn toàn khác: thay vì ghi nhớ hàng chục công thức chắp vá, bạn chỉ cần nắm vững **một nguyên lý duy nhất** — xây dựng mô hình sinh dữ liệu và cập nhật niềm tin theo định lý Bayes — rồi áp dụng nhất quán từ bài toán tung đồng xu đến hồi quy phân cấp và mô hình dự báo phức tạp.

Trang giới thiệu này là tấm bản đồ toàn khóa, giúp bạn hình dung rõ lộ trình học từ nền tảng xác suất, cập nhật liên hợp, MCMC cho tới đánh giá mô hình và ra quyết định thực tế.

---

## Chào mừng đến với Thống kê Bayes

Khóa học này được xây dựng với một mục tiêu rõ ràng: giúp bạn **tư duy bằng xác suất**, thay vì chỉ ghi nhớ các công thức thống kê một cách rời rạc. Trong thực tế, chúng ta liên tục đối diện với những câu hỏi như: một giả thuyết có đáng tin hay không, dữ liệu mới có làm thay đổi niềm tin ban đầu hay không, và nếu phải ra quyết định ngay lúc này thì rủi ro sai sót lớn đến mức nào. Thống kê Bayes (Bayesian statistics) đặc biệt phù hợp với những bài toán như vậy, bởi phương pháp này không dừng ở một “kết quả kiểm định” đơn lẻ mà cung cấp một khung tư duy nhất quán kết nối **niềm tin, dữ liệu, độ bất định và quyết định**.

> **Ví dụ mini.** Khi nghe dự báo “70% khả năng mưa”, bạn không cần tưởng tượng ngày mai được lặp lại vô hạn lần để hiểu con số đó. Bạn chỉ cần xem đó là mức độ tin cậy hiện tại để quyết định có mang ô hay không.
>
> **Câu hỏi tự kiểm tra.** Theo bạn, vì sao cách suy nghĩ “cập nhật niềm tin khi có thêm thông tin” lại gần với thực tế đời sống hơn nhiều công thức kiểm định rời rạc?

![Bayesian reasoning trong đời sống hằng ngày]({{ site.baseurl }}/img/chapter_img/chapter01/bayesian_daily_life_small.png)


## Kiến thức cần nhớ: Lộ trình 4 tầng của Tư duy Thống kê Bayes

Toàn bộ khóa học này được thiết kế như một hành trình gồm ba trụ cột liên kết chặt chẽ với nhau:

- **Tầng 1 — Nền tảng xác suất & Tư duy Bayes (Chương 0–2):** Xây dựng ngôn ngữ xác suất, trực giác prior–likelihood–posterior, họ liên hợp và xấp xỉ lưới để bạn nhìn thấy tường tận cơ chế cập nhật niềm tin bằng tay trước khi dùng phần mềm.
- **Tầng 2 — Tính toán hậu nghiệm & Mô hình hóa (Chương 3–7):** Vượt qua rào cản tích phân nhiều chiều bằng MCMC (Metropolis–Hastings, HMC/NUTS trong PyMC), sau đó xây dựng hồi quy tuyến tính, mô hình tuyến tính tổng quát (GLM), điều chuẩn bằng prior và mô hình phân cấp.
- **Tầng 3 — Phản biện mô hình & Ra quyết định (Chương 8–12):** Hoàn thiện chu trình khoa học bằng kiểm tra dự báo hậu nghiệm (PPC), tiêu chí thông tin (WAIC/PSIS-LOO), phân tích quyết định theo hàm chi phí và hệ thống bài lab thực hành xuyên suốt.

---

## Khóa học này sẽ giúp bạn học điều gì?

Khi hoàn thành khóa học này, bạn sẽ không chỉ nắm được định lý Bayes mà còn biết cách vận dụng tư duy Bayes vào các bài toán thực tế.

### 1. Hiểu xác suất như ngôn ngữ của mức độ tin cậy

Bạn sẽ thấy vì sao trong thống kê Bayes, xác suất không chỉ được hiểu là tần suất dài hạn mà còn là ngôn ngữ định lượng mức độ hợp lý của một giả thuyết, đặc biệt trong những tình huống mà độ bất định là điều không thể tránh khỏi.

### 2. Xây dựng mô hình sinh dữ liệu

Một mô hình Bayes tốt không bắt đầu từ việc viết mã, mà bắt đầu từ việc phân tích xem dữ liệu được sinh ra theo cơ chế nào, tham số nào chưa biết, và phân phối tiền nghiệm (prior) nào phản ánh hợp lý kiến thức sẵn có.

### 3. Cập nhật niềm tin bằng dữ liệu

Đây là trọng tâm của cả khóa học: **prior** biểu diễn niềm tin ban đầu, **likelihood** cho biết dữ liệu ủng hộ từng giả thuyết hay giá trị tham số đến mức nào, còn **posterior** là niềm tin đã được cập nhật sau khi kết hợp hai nguồn thông tin đó.

![Cỗ máy Bayes: từ prior đến posterior]({{ site.baseurl }}/img/chapter_img/chapter01/bayes_machine_small.png)

### 4. Sử dụng công cụ hiện đại cho suy luận Bayes

Sau phần nền tảng, khóa học sẽ giới thiệu các phương pháp tính toán như **xấp xỉ lưới (grid approximation)**, Monte Carlo và MCMC, tiếp đó là thư viện PyMC để triển khai các mô hình thực tế cùng các kỹ thuật chẩn đoán mô hình và kiểm tra dự báo.

### 5. Diễn giải kết quả một cách trung thực

Bạn sẽ học cách trả lời những câu hỏi mà người làm nghiên cứu, kinh doanh hay kỹ thuật thực sự quan tâm: xác suất một tham số lớn hơn 0 là bao nhiêu, vùng giá trị nào có khả năng cao, dự báo tương lai còn mức bất định ra sao, và mô hình có đang bỏ sót cấu trúc quan trọng nào không.

## Vì sao nên học thống kê Bayes ngay từ đầu?

Nhiều người tìm đến thống kê Bayes sau khi đã học thống kê tần suất (frequentist) và cảm thấy khó diễn giải các khái niệm như p-value, khoảng tin cậy (confidence interval) hay kiểm định giả thuyết. Cách tiếp cận Bayes trở nên hấp dẫn vì ba lý do chính.

### 1. Gần với trực giác học từ thông tin mới

Trong đời sống hằng ngày, chúng ta vốn suy nghĩ theo tinh thần Bayes: nghe dự báo thời tiết rồi điều chỉnh kế hoạch, xem kết quả xét nghiệm y khoa rồi cập nhật chẩn đoán, hay quan sát vài lượt mua hàng đầu tiên rồi điều chỉnh nhận định về nhu cầu thị trường. Ít ai suy nghĩ theo kiểu “bác bỏ giả thuyết ở mức ý nghĩa 5%”, bởi ngôn ngữ đời thực gắn với việc cập nhật niềm tin hơn là các quy tắc kiểm định hình thức.

### 2. Trung thực hơn về độ bất định

Thống kê Bayes không chỉ trả lời “ước lượng bằng bao nhiêu”, mà còn cho biết mức độ chắc chắn của ước lượng đó, những giá trị nào vẫn còn khả dĩ, và vùng rủi ro cần cân nhắc khi dự báo tương lai.

### 3. Phù hợp với khoa học dữ liệu hiện đại

Cách tiếp cận Bayes phát huy hiệu quả rõ rệt trong các bài toán có dữ liệu ít nhưng cần quyết định sớm, mô hình phân cấp, dự báo và hệ gợi ý (recommendation), phân tích y khoa, thử nghiệm A/B, cũng như học máy có **định lượng bất định (quantification of uncertainty)**.

## Tài liệu tham khảo trong suốt khóa học

### Tài liệu chính

**Richard McElreath (2020)** - *Statistical Rethinking* (2nd Edition)

Điểm mạnh của cuốn sách là trực giác mô hình hóa rõ ràng, cách giải thích dễ tiếp cận với người mới học và khả năng kết nối chặt chẽ giữa lý thuyết với thực hành mô hình.

### Tài liệu bổ sung

**Andrew Gelman et al. (2013)** - *Bayesian Data Analysis* (3rd Edition)

Cuốn sách cung cấp nền tảng toán học vững chắc, độ bao quát rộng và rất phù hợp khi bạn muốn đi sâu hơn sau khi đã có trực giác cơ bản.

**John K. Kruschke (2014)** - *Doing Bayesian Data Analysis*

Tài liệu có tính sư phạm cao, nhiều ví dụ minh họa và kết nối rõ ràng giữa khái niệm toán học với cách diễn giải kết quả.

## Thông tin môn học và đánh giá

### Tài liệu tham khảo cốt lõi

1. Gelman, A. et al. *Bayesian Data Analysis*.
2. Congdon, P. *Bayesian Statistical Modelling*.
3. Lee, P. M. *Bayesian Statistics: An Introduction*.

### Cấu phần đánh giá

Cấu phần đánh giá hiện tại gồm 20% thường kỳ, 30% giữa kỳ theo hướng thực hành và 50% cuối kỳ theo hướng thực hành.

## Bạn không cần giỏi toán mới học được Bayes

Bạn chỉ cần sự kiên nhẫn để chấp nhận ba nguyên tắc: độ bất định cần được mô hình hóa tường minh, dữ liệu không tự mang ý nghĩa nếu thiếu mô hình, và cập nhật niềm tin nhất quán là cốt lõi của suy luận. Khi nắm vững tinh thần đó, thống kê Bayes sẽ không còn là một chủ đề khó tiếp cận mà trở thành một cách tư duy tự nhiên.

> **3 ý cần nhớ.** Khóa học này không chỉ dạy công thức Bayes mà dạy cả một cách tư duy học từ dữ liệu; thống kê Bayes mạnh ở chỗ kết nối mô hình, độ bất định và ra quyết định trong cùng một quy trình; và để học tốt, bạn nên ưu tiên trực giác mô hình hóa trước rồi mới đến kỹ thuật tính toán.

## Đi tiếp từ đây

Bài tiếp theo là [1.1 Replication Crisis & P-values]({{ site.baseurl }}/contents/vi/chapter01/01_01_replication_crisis_pvalues/), nơi Chương 1 bắt đầu đặt câu hỏi: khi cách suy luận thống kê truyền thống bộc lộ nhiều giới hạn, ta có lựa chọn nào phù hợp hơn không? Nếu cần ôn lại nền tảng trước khi vào chương, bạn có thể xem [Chapter 00: Prerequisites](/vi/chapter00/).


## Giải thích: Chu trình làm việc Bayes 5 bước (Bayesian Workflow)

Suốt khóa học, dù bài toán đơn giản hay phức tạp, bạn sẽ luôn đi theo cùng một vòng lặp 5 bước:

1. **Kể câu chuyện sinh dữ liệu (Generative Story):** Viết rõ phân phối prior cho tham số và likelihood cho dữ liệu.
2. **Kiểm tra dự báo tiền nghiệm (Prior Predictive Check):** Sinh dữ liệu giả lập từ prior để đảm bảo mô hình chưa tạo ra kết quả phi lý.
3. **Cập nhật hậu nghiệm (Inference):** Tính hậu nghiệm bằng công thức liên hợp, lưới, hoặc MCMC (PyMC) và kiểm tra hội tụ ($$\hat R$$, ESS).
4. **Kiểm tra dự báo hậu nghiệm (Posterior Predictive Check):** So sánh dữ liệu mô phỏng từ hậu nghiệm với dữ liệu thật để tìm điểm yếu của mô hình.
5. **So sánh và ra quyết định:** Dùng WAIC/LOO để so sánh mô hình và tối thiểu hóa kỳ vọng tổn thất để đưa ra hành động cụ thể.

### Ví dụ tính toán làm từng bước: Bản thu nhỏ cả khóa học trong 3 dòng số

Giả sử bạn tung một đồng xu mới $$n = 5$$ lần và thấy $$4$$ mặt Ngửa. Với niềm tin ban đầu trung lập $$\text{Beta}(1, 1)$$ (kỳ vọng $$0.50$$), toàn bộ quy trình Bayes cho ra:

| Giai đoạn trong khóa học | Đại lượng tương ứng | Giá trị cụ thể |
| --- | --- | --- |
| Niềm tin ban đầu (Chương 1–2) | Prior $$\text{Beta}(1, 1)$$ | Kỳ vọng $$1/(1+1) = 0.500$$ |
| Bằng chứng dữ liệu (Chương 2) | Likelihood $$\text{Binomial}(5, p)$$ với $$k=4$$ | Tỷ lệ quan sát $$4/5 = 0.800$$ |
| Niềm tin cập nhật (Chương 2–3) | Posterior $$\text{Beta}(1+4, 1+1) = \text{Beta}(5, 2)$$ | Kỳ vọng $$5/(5+2) \approx 0.714$$ |
| Dự báo lần tung thứ 6 (Chương 8) | Posterior Predictive $$P(X_6 = 1 \mid y)$$ | Đúng bằng kỳ vọng hậu nghiệm $$5/7 \approx 0.714$$ |

Mọi mô hình lớn hơn ở các chương sau — từ hồi quy logistic đến mô hình phân cấp — đều vận hành theo đúng bốn dòng logic này, chỉ thay phân phối đơn giản bằng cấu trúc giàu thông tin hơn.

**Hiểu lầm cần tránh:** Nghĩ rằng phải thuộc lòng giải tích phức tạp mới bắt đầu học Bayes được. Trong khóa học này, trực giác xác suất và khả năng đọc phân phối luôn đi trước, còn phần tính tích phân nặng nhọc sẽ có mô phỏng và PyMC đảm nhiệm.

**Kiểm tra nhanh:** Nếu bạn quan sát thêm 5 lần nữa và thấy toàn mặt Sấp (tổng cộng 4 Ngửa, 6 Sấp trong 10 lần), hậu nghiệm tự động cập nhật thành $$\text{Beta}(5, 7)$$ với kỳ vọng $$5/12 \approx 0.417$$ — không cần bắt đầu lại từ đầu.

---

## Video tham khảo

- [The Bayesian Trap](https://www.youtube.com/watch?v=R13BD8qKeTg) — Veritasium, English. **xem trước**. Minh họa cái bẫy của tỷ lệ nền khi cập nhật niềm tin, gắn trực tiếp với mục tiêu tư duy bằng xác suất thay vì thuộc công thức.
- [Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM) — 3Blue1Brown, English. Giải thích định lý Bayes bằng trực giác hình học, hỗ trợ lộ trình đi từ prior, likelihood đến posterior.
- [Statistical Rethinking 2023 - 01 - The Golem of Prague](https://www.youtube.com/watch?v=FdnMWdICdRs) — Richard McElreath, English. Bài giảng mở đầu của *Statistical Rethinking* về việc xem mô hình như công cụ cần được giám sát, cùng tinh thần với khóa học này.
