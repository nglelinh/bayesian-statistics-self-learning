---
layout: post
title: "Bài 8.5: Ứng dụng hiện đại của kiểm tra mô hình và ra quyết định Bayes"
chapter: '08'
order: 5
owner: Nguyen Le Linh
lang: vi
categories:
- chapter08
lesson_type: optional
---

## Mục tiêu học tập

Sau bài tùy chọn này, bạn nhìn PPC, LOO/WAIC và decision analysis như một workflow sản xuất, không như chương “phụ lục sau khi đã fit”. Bạn sẽ nối được kiểm tra hậu nghiệm với simulation-based calibration, so sánh mô hình với bất định của chính hiệu chênh LOO, và quy tắc Bayes action với Bayesian optimization cùng bandit.

## Kiến thức cần có

Các bài 8.1–8.4 đã xây PPC, information criteria, so sánh mô hình, và quyết định dưới loss. Bài này không định nghĩa lại ELPD. Nó cho thấy các đối tượng ấy đang được siết chặt trong nghiên cứu 2022–2025 và trong các thư viện tối ưu hóa.

## Mở đầu

Chương 8 được viết vì một thói quen xấu: xem chuỗi MCMC hội tụ rồi dừng. Trong khoa học máy tính, thói quen ấy biến thành dashboard xanh. Một sampler có thể lấy đúng mẫu từ sai mô hình, hoặc lấy sai mẫu từ đúng mô hình. Một hiệu $$\Delta\mathrm{ELPD}$$ có thể đổi dấu khi bạn tính lại sai số. Căng thẳng của bài này là phân biệt ba câu hỏi mà sản phẩm hay trộn: mô hình có sinh được dữ liệu kiểu này không, mô hình nào dự báo tốt hơn dưới bất định của chính sự so sánh, và ta nên *làm gì*?

## Phát triển khái niệm

PPC hỏi liệu $$y^{\mathrm{rep}}$$ sinh từ $$p(y\mid\theta)$$ với $$\theta\sim p(\theta\mid y)$$ có tái tạo được cấu trúc của $$y$$. LOO ước lượng kỳ vọng log predictive density trên một điểm mới. Decision theory chọn

$$
a^*(y)=\arg\min_a\int L(a,\theta)\,p(\theta\mid y)\,d\theta.
$$

Ba đối tượng ấy không thay thế nhau. Một mô hình thắng LOO vẫn có thể thất bại PPC ở đuôi. Một hành động tối ưu có thể chọn mô hình *xấu hơn về log score* nếu loss không đối xứng.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Simulation-based calibration như kiểm tra phần mềm và suy luận

Modrák et al. (2025) siết lại simulation-based calibration: lấy $$\theta$$ từ prior, sinh $$y$$, khớp lại, rồi xét thứ hạng của đại lượng kiểm tra trong posterior. Họ chỉ ra rằng chỉ xếp hạng tham số sẽ bỏ sót cả một lớp lỗi—kể cả trường hợp posterior trùng prior—và rằng likelihood đồng thời là một test quantity nhạy. Trong công nghiệp, đây là unit test cho một mô hình PyMC/Stan trước khi nó vào A/B hoặc vào định giá. PPC của bài 8.1 kiểm tra mô hình trên dữ liệu thật; SBC kiểm tra *công cụ suy luận* trên dữ liệu sinh ra từ chính mô hình.

### 2. Bất định của chính cuộc so sánh LOO

Sivula, Magnusson, Matamoros và Vehtari (2025) cho thấy xấp xỉ chuẩn của hiệu LOO thường lệch khi hai mô hình dự báo gần nhau, khi mô hình sai đặc tả, hoặc khi mẫu nhỏ. Skewness của sai số có thể không tắt khi $$n\to\infty$$ trong một số tình huống. Hệ quả sản phẩm rất cụ thể: một leaderboard mô hình không được công bố như một thứ hạng cứng nếu sai số của $$\Delta\mathrm{ELPD}$$ nuốt mất hiệu. Bài 8.3 đã nói so sánh là quyết định dưới bất định mô hình; giấy này đo chính bất định ấy.

### 3. Bayesian optimization như decision theory trên hàm đắt

Khi $$\theta$$ là một cấu hình siêu tham số hoặc một thí nghiệm phòng lab, mỗi đánh giá $$f(\theta)$$ rất đắt. Bayesian optimization đặt một posterior—thường là quá trình Gauss—lên $$f$$, rồi chọn điểm kế tiếp bằng cách tối thiểu hóa expected loss, ví dụ expected improvement. Đó là bài 8.4 viết cho không gian hành động liên tục. BoTorch (Balandat et al., 2020; hệ sinh thái 2022–2026) biến quy tắc ấy thành Monte Carlo trên posterior, đủ để tối ưu nhiều mục tiêu và ràng buộc. AutoML là ứng dụng, không phải lý thuyết mới: chọn mô hình và siêu tham số bằng Bayes action, không bằng một lưới mù.

### 4. Bandit và thí nghiệm thích nghi

Thompson sampling, đã xuất hiện như ứng dụng conjugate ở Chương 2, nay được đọc đúng chỗ của nó: một xấp xỉ tuần tự của Bayes action khi loss là regret. Nền tảng nội dung, quảng cáo, và thử nghiệm lâm sàng thích nghi đều cập nhật $$p(\theta\mid y)$$ rồi chọn tay đòn. Quyết định không phải “bác bỏ $$H_0$$”; quyết định là tiếp tục, dừng, hay đổi tỷ lệ phân bổ. PPC vẫn cần: nếu mô hình chuyển đổi sai đuôi, bandit sẽ khai thác một ảo ảnh.

## Diễn giải và nhận định

Một PPC đẹp không cấp giấy phép nhân quả. Một hiệu LOO lớn hơn hai sai số chuẩn vẫn có thể là so sánh giữa hai mô hình cùng misspecify. Expected improvement cao không có nghĩa điểm kế tiếp sẽ tốt; nó có nghĩa *dưới posterior hiện tại* giá trị thông tin vượt chi phí. Hãy giữ ba lớp diễn giải tách bạch: phê bình sinh dữ liệu, so sánh dự báo, và hành động.

## Ứng dụng

Kiểm thử mô hình trước khi lên production, chọn mô hình dự báo cho bảng và cho chuỗi thời gian, tinh chỉnh siêu tham số, và phân bổ thí nghiệm là bốn mặt của Chương 8 trong CS/DS hiện nay.

## Giới hạn và hướng mở rộng

SBC tốn nhiều lần khớp mô hình. LOO giả định các quan sát đóng góp gần như nhân tử hóa được. Bayesian optimization phụ thuộc mạnh vào prior trên $$f$$ và sẽ nhẹ dạ nếu nhiễu bị hiểu sai. Khóa học không có chương Gaussian process riêng, nên bài này chỉ dùng GP như một posterior phục vụ quyết định. Nếu chương sau mở nonparametric, bạn sẽ thấy nhân của BO chính là mô hình ấy.

## Bài tập

1. Phân biệt, trên một mô hình giá, một thất bại PPC ở đuôi phải với một thất bại SBC. Cái nào buộc bạn sửa *mã suy luận*, cái nào buộc bạn sửa *câu chuyện sinh*?
2. Hai mô hình có $$\Delta\mathrm{ELPD}=1.2$$ và sai số 1.5. Dựa trên Sivula et al. (2025), bạn sẽ viết gì trên slide cho giám đốc sản phẩm?
3. Viết loss của một vòng Bayesian optimization khi mỗi thí nghiệm tốn một ngân sách cố định và bạn còn năm lần đánh giá. Hành động là gì, trạng thái thế giới là gì?
4. Một bandit nội dung khai thác sớm một tiêu đề.clickbait. PPC nào sẽ tố cáo mô hình thưởng, và decision rule nào sẽ thận trọng hơn Thompson sampling thuần?

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 6–7, 9.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 10, 13.
- Modrák, M., et al. (2025). Simulation-based calibration checking for Bayesian computation. *Bayesian Analysis*, 20(2), 461–488. [arXiv:2211.02383](https://arxiv.org/abs/2211.02383).
- Sivula, T., Magnusson, M., Matamoros, A. A., & Vehtari, A. (2025). Uncertainty in Bayesian leave-one-out cross-validation based model comparison. *Bayesian Analysis*. [arXiv:2008.10296](https://arxiv.org/abs/2008.10296).
- Balandat, M., et al. (2020). BoTorch: A framework for efficient Monte-Carlo Bayesian optimization. *NeurIPS*. [arXiv:1910.06403](https://arxiv.org/abs/1910.06403).
- Russo, D., et al. (2018). A tutorial on Thompson sampling. *Foundations and Trends in Machine Learning*.
- [ArviZ posterior predictive checks](https://python.arviz.org/en/stable/api/generated/arviz.plot_ppc.html).
- [Stan Workflow / SBC notes](https://mc-stan.org/docs/stan-users-guide/posterior-predictive-checks.html).
