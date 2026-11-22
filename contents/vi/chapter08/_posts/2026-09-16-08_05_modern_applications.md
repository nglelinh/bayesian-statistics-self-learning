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

Sau bài học tùy chọn này, bạn sẽ nhìn nhận PPC, LOO/WAIC và phân tích quyết định như một quy trình vận hành thực tế, thay vì phần phụ lục sau khi khớp mô hình. Bạn sẽ kết nối được kiểm tra hậu nghiệm với hiệu chuẩn dựa trên mô phỏng (simulation-based calibration), so sánh mô hình với độ bất định của chính hiệu chênh LOO, và quy tắc hành động Bayes với tối ưu hóa Bayes (Bayesian optimization) cùng bài toán bandit.

## Kiến thức cần có

Các bài 8.1–8.4 đã trình bày PPC, các tiêu chí thông tin, chiến lược so sánh mô hình và ra quyết định dưới hàm mất mát. Bài học này không định nghĩa lại ELPD, mà cho thấy các công cụ đó đang được hoàn thiện như thế nào trong nghiên cứu giai đoạn 2022–2025 và trong các thư viện tối ưu hóa hiện đại.

## Mở đầu

Chương 8 xuất phát từ một thói quen phổ biến nhưng dễ gây sai lầm: thấy chuỗi MCMC hội tụ là dừng lại. Trong môi trường kỹ thuật phần mềm và dữ liệu, thói quen đó thường biến thành tâm lý yên tâm chỉ vì các chỉ báo hội tụ đều hiển thị trạng thái đạt. Tuy nhiên, một thuật toán lấy mẫu có thể lấy mẫu chính xác từ một mô hình sai, hoặc lấy mẫu sai từ một mô hình đúng; và một hiệu chênh $$\Delta\mathrm{ELPD}$$ có thể đảo dấu khi tính lại sai số. Trọng tâm của bài học này là tách bạch ba câu hỏi mà các nhóm sản phẩm thường trộn lẫn: mô hình có sinh được dữ liệu giống thực tế không, mô hình nào dự báo tốt hơn khi tính cả độ bất định của phép so sánh, và cuối cùng ta nên *hành động* ra sao?

## Phát triển khái niệm

PPC đặt câu hỏi liệu dữ liệu mô phỏng $$y^{\mathrm{rep}}$$ sinh từ $$p(y\mid\theta)$$ với $$\theta\sim p(\theta\mid y)$$ có tái tạo được cấu trúc của dữ liệu quan sát $$y$$ hay không. LOO ước lượng kỳ vọng mật độ dự báo dạng log trên một điểm dữ liệu mới. Lý thuyết quyết định chọn hành động tối ưu:

$$
a^*(y)=\arg\min_a\int L(a,\theta)\,p(\theta\mid y)\,d\theta.
$$

Ba công cụ này không thay thế nhau. Một mô hình có điểm LOO tốt hơn vẫn có thể thất bại ở PPC phần đuôi; và một hành động tối ưu vẫn có thể dựa trên mô hình có điểm log score thấp hơn nếu hàm mất mát mang tính bất đối xứng.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Hiệu chuẩn dựa trên mô phỏng (SBC) như kiểm thử phần mềm và suy luận

Modrák et al. (2025) hoàn thiện khung hiệu chuẩn dựa trên mô phỏng (simulation-based calibration — SBC): rút $$\theta$$ từ tiên nghiệm, sinh dữ liệu $$y$$, khớp lại mô hình rồi kiểm tra phân bố thứ hạng của các đại lượng kiểm định trong hậu nghiệm. Nhóm tác giả chỉ ra rằng nếu chỉ kiểm tra thứ hạng của riêng tham số, ta có thể bỏ sót cả một lớp lỗi — kể cả trường hợp hậu nghiệm trùng với tiên nghiệm — trong khi hàm hợp lý đồng thời là một đại lượng kiểm định rất nhạy. Trong công nghiệp, SBC đóng vai trò như kiểm thử đơn vị (unit test) cho mô hình PyMC hoặc Stan trước khi đưa vào thử nghiệm A/B hay định giá. PPC của bài 8.1 kiểm tra mô hình trên dữ liệu thật, còn SBC kiểm tra *chính thuật toán suy luận* trên dữ liệu sinh từ mô hình đó.

### 2. Độ bất định của bản thân phép so sánh LOO

Sivula, Magnusson, Matamoros và Vehtari (2025) chỉ ra rằng xấp xỉ chuẩn cho hiệu chênh LOO thường bị lệch khi hai mô hình dự báo gần giống nhau, khi mô hình bị đặc tả sai hoặc khi cỡ mẫu nhỏ. Độ lệch (skewness) của sai số ước lượng thậm chí có thể không triệt tiêu khi $$n\to\infty$$ trong một số trường hợp. Hệ quả thực tế rất rõ: không nên công bố bảng xếp hạng mô hình như một thứ tự tuyệt đối nếu sai số chuẩn của $$\Delta\mathrm{ELPD}$$ lấn át bản thân độ chênh lệch. Bài 8.3 đã nhấn mạnh so sánh mô hình là ra quyết định dưới độ bất định; nghiên cứu này định lượng trực tiếp phần độ bất định đó.

### 3. Tối ưu hóa Bayes (Bayesian optimization) như lý thuyết quyết định trên hàm tốn kém

Khi $$\theta$$ là một cấu hình siêu tham số hoặc một thí nghiệm phòng lab, mỗi lần đánh giá hàm mục tiêu $$f(\theta)$$ đều rất tốn kém. Tối ưu hóa Bayes đặt một phân phối hậu nghiệm — thường là quá trình Gauss (Gaussian process) — lên hàm $$f$$, rồi chọn điểm đánh giá tiếp theo bằng cách tối thiểu hóa mất mát kỳ vọng (ví dụ qua tiêu chí expected improvement). Đây chính là nguyên lý của bài 8.4 áp dụng cho không gian hành động liên tục. Thư viện BoTorch (Balandat et al., 2020; hệ sinh thái 2022–2026) triển khai quy tắc này bằng mô phỏng Monte Carlo trên hậu nghiệm, hỗ trợ tối ưu đa mục tiêu và có ràng buộc. AutoML nhờ vậy là một ứng dụng trực tiếp của hành động Bayes để chọn mô hình và siêu tham số thay cho tìm kiếm lưới mù quáng.

### 4. Bài toán bandit và thí nghiệm thích nghi

Thompson sampling — từng xuất hiện như ứng dụng của tiên nghiệm liên hợp ở Chương 2 — được đặt đúng vào vị trí của nó: một cách xấp xỉ tuần tự cho hành động Bayes khi hàm mất mát là độ hối tiếc (regret). Các nền tảng nội dung, quảng cáo và thử nghiệm lâm sàng thích nghi liên tục cập nhật $$p(\theta\mid y)$$ rồi chọn phương án (arm) tiếp theo. Quyết định ở đây không phải "bác bỏ $$H_0$$", mà là tiếp tục thử nghiệm, dừng lại hay điều chỉnh tỷ lệ phân bổ lưu lượng. PPC vẫn giữ vai trò thiết yếu: nếu mô hình tỷ lệ chuyển đổi sai ở phần đuôi, thuật toán bandit có thể dồn lưu lượng vào một phương án kém hiệu quả.

## Diễn giải và nhận định

Một kết quả PPC tốt không đồng nghĩa với bằng chứng nhân quả. Một hiệu chênh LOO lớn hơn hai lần sai số chuẩn vẫn có thể chỉ là so sánh giữa hai mô hình cùng bị đặc tả sai. Giá trị expected improvement cao không bảo đảm điểm đánh giá kế tiếp chắc chắn tốt hơn, mà chỉ có nghĩa rằng *dưới phân phối hậu nghiệm hiện tại*, giá trị thông tin dự kiến vượt chi phí đánh giá. Cần giữ tách bạch ba lớp diễn giải: phê bình cơ chế sinh dữ liệu, so sánh năng lực dự báo và lựa chọn hành động.

## Ứng dụng

Kiểm thử mô hình trước khi đưa vào vận hành, lựa chọn mô hình dự báo cho dữ liệu bảng và chuỗi thời gian, tinh chỉnh siêu tham số và phân bổ thí nghiệm là bốn mảng ứng dụng nổi bật của Chương 8 trong khoa học máy tính và khoa học dữ liệu hiện nay.

## Giới hạn và hướng mở rộng

SBC đòi hỏi khớp lại mô hình rất nhiều lần nên tốn chi phí tính toán. LOO giả định đóng góp của các quan sát có thể tách tích gần như độc lập. Tối ưu hóa Bayes phụ thuộc mạnh vào tiên nghiệm trên hàm $$f$$ và dễ đưa ra lựa chọn thiếu thận trọng nếu mô hình nhiễu bị đặc tả sai. Khóa học không có chương riêng về quá trình Gauss, nên bài này chỉ sử dụng GP như một phân phối hậu nghiệm phục vụ ra quyết định; khi mở rộng sang thống kê phi tham số, bạn sẽ thấy hạt nhân của tối ưu hóa Bayes chính là mô hình này.

## Video tham khảo

- [#164 Bayesian Workflow, with Andrew Gelman, Aki Vehtari & Richard McElreath](https://www.youtube.com/watch?v=ysITaNRUQUU) — Learning Bayesian Statistics, English. **Xem trước**. Cuộc thảo luận của Andrew Gelman, Aki Vehtari và Richard McElreath về quy trình Bayes, kết nối kiểm tra mô hình với so sánh và ra quyết định.
- [BITESIZE | Understanding Simulation-Based Calibration, with Teemu Säilynoja](https://www.youtube.com/watch?v=EC1bvP65rjs) — Learning Bayesian Statistics, English. Giải thích hiệu chuẩn dựa trên mô phỏng (SBC), bổ trợ cho phần kiểm thử thuật toán suy luận.
- [Uncertainty in Bayesian leave-one-out cross-validation based model comparison](https://www.youtube.com/watch?v=vLx6lUlZ0fc) — Aki Vehtari, English. Phân tích độ bất định khi so sánh mô hình bằng LOO, làm rõ vì sao không nên đọc hiệu chênh ELPD như một bảng xếp hạng cứng.

## Bài tập

1. Trên một mô hình định giá, hãy phân biệt trường hợp không đạt ở PPC phần đuôi phải với trường hợp không đạt ở SBC. Trường hợp nào buộc bạn sửa *mã suy luận*, trường hợp nào buộc bạn sửa *câu chuyện sinh dữ liệu*?
2. Hai mô hình có $$\Delta\mathrm{ELPD}=1.2$$ với sai số chuẩn 1.5. Dựa trên Sivula et al. (2025), bạn sẽ trình bày kết luận như thế nào trên slide báo cáo cho giám đốc sản phẩm?
3. Viết hàm mất mát cho một vòng tối ưu hóa Bayes khi mỗi thí nghiệm tiêu tốn một ngân sách cố định và bạn chỉ còn năm lần đánh giá. Tập hành động và trạng thái thế giới trong bài toán này là gì?
4. Một thuật toán bandit nội dung khai thác quá sớm một tiêu đề giật gân (clickbait). Phép kiểm tra PPC nào sẽ phát hiện sai lệch của mô hình phần thưởng, và quy tắc quyết định nào sẽ thận trọng hơn Thompson sampling thuần túy?

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 6–7, 9.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 10, 13.
- Modrák, M., et al. (2025). Simulation-based calibration checking for Bayesian computation. *Bayesian Analysis*, 20(2), 461–488. [arXiv:2211.02383](https://arxiv.org/abs/2211.02383).
- Sivula, T., Magnusson, M., Matamoros, A. A., & Vehtari, A. (2025). Uncertainty in Bayesian leave-one-out cross-validation based model comparison. *Bayesian Analysis*. [arXiv:2008.10296](https://arxiv.org/abs/2008.10296).
- Balandat, M., et al. (2020). BoTorch: A framework for efficient Monte-Carlo Bayesian optimization. *NeurIPS*. [arXiv:1910.06403](https://arxiv.org/abs/1910.06403).
- Russo, D., et al. (2018). A tutorial on Thompson sampling. *Foundations and Trends in Machine Learning*.
- [ArviZ posterior predictive checks](https://python.arviz.org/en/stable/api/generated/arviz.plot_ppc.html).
- [Stan Workflow / SBC notes](https://mc-stan.org/docs/stan-users-guide/posterior-predictive-checks.html).
