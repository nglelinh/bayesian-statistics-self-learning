# Kế hoạch: explainer tương tác cho khóa Bayesian Statistics

## Hiện trạng
- Jekyll, `baseurl: /bayesian-statistics-self-learning`, hai ngôn ngữ `en`/`vi` (mặc định `en`); bài nằm ở `contents/{vi,en}/chapterNN/_posts/`.
  Nội dung tiếng Việt đầy đủ (chương 00–08+), tiếng Anh chỉ có phần chương 02 và một phần chương 00.
- Trước đây chỉ có widget thuần JS (`tools/dag-explorer/`); chưa có thư viện explainer, chưa có hub công cụ.
- Có cổng mật khẩu (`access_gate`) nên kiểm thử headless phải mở khóa phía client.

## Danh sách ưu tiên (theo nội dung bài thật)
| # | Khái niệm | Bài | Trạng thái |
|---|---|---|---|
| 1 | Định lý Bayes: cây tần suất tự nhiên + cập nhật tuần tự | 01_03 | Xong |
| 2 | Beta–Binomial, Gamma–Poisson, Normal–Normal từng quan sát | 02_03, 02_04, 02_05 | Xong |
| 3 | Xấp xỉ lưới (prior × likelihood → chuẩn hóa) | 02_06 | Xong |
| 4 | MCMC: Metropolis, Gibbs, HMC, R-hat | 04_02b | Xong |
| 5 | Khoảng tin cậy vs khoảng đáng tin (độ phủ) | 00_08, 01_04, 02_04 | Xong |
| 6 | Hồi quy Bayes, bó đường posterior | 04_01 | Xong |
| 7 | Posterior predictive check | 08_01 | Xong |
| 8 | Shrinkage / regularization (prior chuẩn = ridge) | 07_01 | Xong |
| 9 | LLN, CLT, sai số chuẩn | 00_14, 00_15 | Xong |
| 10 | WAIC / LOO, so sánh mô hình (pseudo-BMA) | 08_02, 08_03 | Xong |
| 11 | Quyết định: ngưỡng, hàm mất mát, EVSI | 08_04 | Xong |
| 12 | Hồi quy logistic, Poisson (posterior lưới) | 06_01, 06_02 | Xong |
| 13 | Hierarchical partial pooling | 04_06 (§7.3) | Xong |
| 14 | Confounding, collider, tương tác (bổ sung cho `tools/dag-explorer`) | 05_02, 05_04 | Xong |
| 15 | p-value, phân phối t, công suất mô phỏng | 00_08, 00_09 | Xong |
| 16 | Likelihood explorer, prior predictive | 02_02, 02_03 | Xong |
| 17 | Bayes factor / marginal likelihood, độ nhạy prior | 08_03 | Xong |
| 18 | Đa cộng tuyến (VIF, posterior hình dải chéo) | 05_03 | Xong |
| 19 | Bias–variance bằng mô phỏng | 07_02 | Xong |
| 20 | Horseshoe vs Laplace vs Gaussian (chọn biến) | 07_03 | Xong |
| 21 | Overdispersion: Poisson vs Negative Binomial | 06_02 | Xong |
| 22 | PPC cho GLM (logistic, Poisson số 0) | 06_03 | Xong |

## Kiến trúc
- `explainers/` (Svelte 5 + D3 + Vite, library mode, IIFE). **Một bundle cho cả khóa** vì hai bundle Svelte trên một trang xung đột.
- Số học thuần JS (`src/bayes/*.js`) với RNG có seed; UI chỉ hiển thị.
- `Stepper` dùng chung, nhãn VI/EN qua `lang`. Mỗi component có `data-lang`.
- Chèn vào bài chỉ bằng block `data-demo` + một `<script>` mỗi trang; không sửa nội dung có sẵn (bản sao lưu ở `/tmp/bayes-backups/`).

## Kiểm chứng
- Test số học (`npm test`: 36/36): hàm đặc biệt, lấy mẫu, cập nhật liên hợp vs lưới, Bayes rule, hội tụ lưới, Metropolis/Gibbs/HMC vs moment đã biết (seed cố định), R-hat, độ phủ khoảng, CLT/LLN, PPC, hồi quy vs lưới 2-D, ridge = posterior mean; đợt 2: digamma/phân phối t, WAIC vs LOO chính xác (+ p_waic vs khai triển bậc hai), EOL/EVSI dạng đóng vs tích phân và Monte Carlo, loss tối ưu vs cực tiểu số, GLM lưới vs công thức digamma và vs Newton MLE, phân cấp (giới hạn τ, p(τ|y) vs tích phân μ, Rao–Blackwell vs Monte Carlo), confounding/collider/interaction vs công thức giải tích, p-value đều/α/công suất, prior predictive vs Beta–Binomial và nhị thức âm; đợt 3: marginal likelihood vs Monte Carlo/lưới và Savage–Dickey, đa cộng tuyến (sd ∝ √VIF, corr ≈ −ρ), bias² + variance = tổng sai số chính xác, co rút Gaussian vs tích phân số và thứ tự MSE horseshoe < Laplace < Gaussian < MLE, Negative Binomial/Poisson–Gamma predictive và PPC phát hiện quá phân tán, PPC GLM bác mô hình sai nhưng không bác mô hình đúng.
- Jekyll build tạm + Chrome headless: 32 trang (45 instance VI, 11 instance EN), 56 instance, 0 lỗi console, không tràn ngang ở 390 px, không có NaN/undefined.
- Ghi chú: p_waic chỉ ≈ số tham số hiệu dụng khi mô hình đúng; với mô hình sai (đường thẳng cho dữ liệu sine) p_waic lớn hơn nhiều — test kiểm chứng cả hai trường hợp.
