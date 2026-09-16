---
layout: post
title: "Bài 6.4: Ứng dụng hiện đại của GLM Bayes"
chapter: '06'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter06
lesson_type: optional
---

## Mục tiêu học tập

Sau bài tùy chọn này, bạn chọn được một GLM Bayes vì *câu chuyện sinh của outcome*, không vì thói quen gọi mọi bài toán là hồi quy tuyến tính. Bạn sẽ nhận ra logistic, Poisson và các họ gần kề đang chạy trong tín dụng, dịch tễ, và đo lường marketing, và biết posterior của một xác suất hay một cường độ đếm phải được đọc cùng chi phí quyết định.

## Kiến thức cần có

Các bài 6.1–6.3 đã xây logistic, Poisson, và đánh giá GLM. Bài này không viết lại link function. Nó chỉ nối cùng những mô hình ấy với các hệ thống 2022–2026.

## Mở đầu

Chương 6 sinh ra vì giả định Gaussian của Chương 4 không chịu được nhị phân và số đếm. Trong sản phẩm, sự không chịu ấy xuất hiện ngay: giao dịch vỡ nợ hoặc không, số đơn hàng trong giờ, số ca bệnh bị trễ khai báo. Nếu ta vẫn tối ưu bình phương tối thiểu, ta đang kể một câu chuyện sinh mà dữ liệu không thể đã sống. Căng thẳng của bài này là chọn đúng họ quan sát trước khi bàn mạng sâu hay feature store.

## Phát triển khái niệm

Một GLM Bayes giữ cấu trúc tuyến tính trên một thang phù hợp,

$$
g(\mathbb E[y_i\mid x_i])=x_i^\top\beta,
$$

rồi đặt prior trên $$\beta$$ và lấy posterior. Với logistic, $$g$$ là logit và $$y$$ là Bernoulli. Với Poisson, $$g$$ là log và $$y$$ là đếm. Posterior không trả về “lớp dự đoán”; nó trả về một phân phối trên xác suất hoặc trên cường độ. Ngưỡng phân loại chỉ xuất hiện sau, khi một hàm mất mát nói rõ false positive đắt hơn false negative bao nhiêu.

## Mô hình như câu chuyện sinh dữ liệu

### 1. Logistic Bayes cho tín dụng, gian lận và rủi ro lâm sàng

Câu chuyện sinh: mỗi hồ sơ có một xác suất sự kiện hiếm, $$\theta(x)=\mathrm{logit}^{-1}(x^\top\beta)$$, rồi nhãn được tung như một đồng xu lệch. Prior trên $$\beta$$ giữ cho xác suất không bị đẩy về 0 hoặc 1 khi một tổ hợp feature chưa từng xuất hiện—đúng tinh thần regularization sẽ được nhấn ở Chương 7. Điều công nghiệp cần từ posterior không phải độ chính xác tối đa, mà một xác suất đã hiệu chỉnh để đặt hạn mức, bảo hiểm, hoặc ngưỡng duyệt. Grinsztajn, Oyallon và Varoquaux (2022) cho thấy trên nhiều bảng dị thể, mô hình “nông” vẫn thắng mạng sâu; một logistic Bayes được đặc tả tốt vì thế không phải bước lùi.

### 2. Poisson và Negative Binomial cho nhu cầu và nowcasting

Số đơn, số cuộc gọi, số ca theo ngày là đếm. Câu chuyện Poisson nói phương sai bằng trung bình; thực tế dịch tễ và thương mại thường cần Negative Binomial khi quá phân tán. Trong đại dịch, nowcasting phải vừa ước lượng cường độ vừa sửa độ trễ khai báo. Hierarchical Bayes trên các nhóm địa lý là GLM Chương 6 viết thành nhiều chặn. Posterior predictive của tuần tới không phải một điểm; nó là một quạt bất định mà kho và bệnh viện phải mua.

### 3. Media mix modeling như GLM nhân quả có prior

Google Meridian (2024) là một khung marketing mix Bayesian: doanh số được kể như hàm của kênh truyền thông đã biến đổi bằng adstock và lợi suất giảm dần, cộng các yếu tố không phải media, với prior có thể hiệu chỉnh bằng thí nghiệm. Suy luận dùng MCMC/NUTS. Likelihood gần với hồi quy, nhưng tinh thần là GLM đã được mở cho biến đổi phi tuyến của phơi nhiễm. Tài liệu Meridian nhấn mạnh mục tiêu là suy luận nhân quả về ROI, không phải tối thiểu hóa lỗi dự báo hold-out—một cảnh báo thẳng từ Chương 5 và 6: cùng một họ mô hình phục vụ hai câu hỏi khác nhau.

### 4. Đánh giá GLM: hiệu chỉnh trước nhãn cứng

Bài 6.3 đã cảnh báo confusion matrix không trung tính về chi phí. Trong tín dụng, bỏ sót vỡ nợ đắt hơn từ chối nhầm. Trong dịch tễ, bỏ sót cụm đắt hơn cảnh báo thừa. Vì thế posterior của $$\theta(x)$$ phải được kiểm bằng reliability diagram, không chỉ bằng accuracy. Một GLM “kém sắc” nhưng thẳng trên biểu đồ hiệu chỉnh vẫn có thể là mô hình quyết định đúng.

## Diễn giải và nhận định

Một hệ số logistic là thay đổi log-odds, không phải thay đổi xác suất không đổi. Một hệ số Poisson là thay đổi log-cường độ. Khoảng hậu nghiệm trên ROI media đã gộp bất định của adstock, của confounder, và của sampler. Không khoảng nào tự trở thành quyết định cho đến khi loss được viết.

## Ứng dụng

Phê duyệt tín dụng, phát hiện gian lận, dự báo nhu cầu, nowcasting, và phân bổ ngân sách quảng cáo là bốn nơi GLM Bayes đã là hạ tầng, không phải ví dụ sách.

## Giới hạn và hướng mở rộng

Meridian cảnh báo rằng hold-out tốt không chứng minh hiệu ứng media đúng. Poisson sẽ vỡ với zero-inflation. Logistic tuyến tính không bắt tương tác sâu trừ khi bạn viết chúng ra. Chương 7 sẽ hỏi prior nào giữ GLM khỏi quá khớp khi số cột tăng.

## Bài tập

1. Một mô hình vỡ nợ đạt accuracy 98% vì chỉ 2% hồ sơ vỡ nợ. Posterior mean của $$\theta(x)$$ trên nhóm rủi ro cao là 0.15. Vì sao accuracy đang giấu đúng đối tượng mà GLM Bayes quan tâm?
2. Viết câu chuyện sinh cho số đơn mỗi giờ ở một kho. Khi nào bạn rời Poisson sang Negative Binomial, và posterior predictive sẽ đổi hình dạng ra sao?
3. Meridian khuyên không lấy dự báo hold-out làm tiêu chí chính. Nối câu ấy với sự khác nhau giữa dự báo và suy luận nhân quả ở Chương 5.
4. Chọn một ngưỡng logistic khi false negative đắt gấp mười false positive. Bạn cần thêm đối tượng nào của posterior, không chỉ $$\hat\beta$$?

## Tài liệu tham khảo

- Gelman et al. *Bayesian Data Analysis* (3rd ed.), Ch. 16.
- Kruschke, J. K. *Doing Bayesian Data Analysis* (2nd ed.), Ch. 21–22.
- Grinsztajn, L., Oyallon, E., & Varoquaux, G. (2022). Why do tree-based models still outperform deep learning on typical tabular data? *NeurIPS*.
- Google. (2024). *Meridian*: Bayesian marketing mix modeling. [Bayesian inference](https://developers.google.com/meridian/docs/causal-inference/bayesian-inference); [GitHub](https://github.com/google/meridian).
- [Stan User’s Guide, GLM chapters](https://mc-stan.org/docs/stan-users-guide/index.html).
- [PyMC GLM examples](https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/GLM_linear.html).
