# Hình ảnh Minh họa cho Chapter 01: Bayesian Inference Basics

## Danh sách Hình ảnh

### 1. bayes_theorem_visualization.png
**Mô tả**: Minh họa Định lý Bayes với Prior, Likelihood, và Posterior
- Ví dụ: Đồng xu với 7 Ngửa trong 10 lần toss
- Prior: Beta(2, 2) - niềm tin ban đầu
- Likelihood: Binomial - bằng chứng từ dữ liệu
- Posterior: Beta(9, 5) - niềm tin cập nhật
- So sánh Prior vs Posterior
- **Vị trí**: Bài 1.3 - Định lý Bayes

### 2. sequential_updating.png
**Mô tả**: Cập nhật tuần tự (Sequential Updating)
- Bước 0: Prior Beta(2, 2)
- Bước 1: Sau 5 lần toss (4 Ngửa) → Beta(6, 3)
- Bước 2: Sau thêm 5 lần (2 Ngửa) → Beta(8, 6)
- So sánh: Sequential vs Batch updating
- Minh họa: Thứ tự không quan trọng
- **Vị trí**: Bài 1.3 - Sequential Updating

### 3. prior_strength_comparison.png
**Mô tả**: So sánh Prior mạnh vs Prior yếu
- Weak Prior: Beta(2, 2) - không chắc chắn
- Strong Prior: Beta(20, 20) - rất chắc chắn
- Cùng dữ liệu: 7/10 Ngửa
- Weak prior bị ảnh hưởng nhiều bởi dữ liệu
- Strong prior kháng cự lại dữ liệu
- **Vị trí**: Bài 1.3 - Prior Strength

### 4. frequentist_vs_bayesian_philosophy.png
**Mô tả**: So sánh Triết lý Frequentist vs Bayesian
- Frequentist: θ cố định, data ngẫu nhiên
- Bayesian: data cố định, θ ngẫu nhiên
- Confidence Interval vs Credible Interval
- Diễn giải khác nhau hoàn toàn
- **Vị trí**: Bài 1.4 - Bayesian vs Frequentist

### 5. pvalue_vs_posterior_probability.png
**Mô tả**: So sánh P-value vs Posterior Probability
- P-value: P(data | H₀) - gián tiếp
- Posterior: P(H₀ | data) - trực tiếp
- Ví dụ: 8/10 thành công, H₀: θ = 0.5
- P-value ≈ 0.055 (borderline)
- P(θ > 0.5 | data) ≈ 0.945 (rõ ràng!)
- **Vị trí**: Bài 1.4 - P-value vs Posterior

## Thông tin Kỹ thuật

- **Độ phân giải**: 300 DPI
- **Định dạng**: PNG
- **Thư viện sử dụng**: 
  - matplotlib 3.10.6
  - scipy 1.16.3
  - seaborn 0.13.2
  - numpy 2.3.2
- **Ngày tạo**: 11/01/2026
- **Tổng dung lượng**: ~2.5 MB

## Mục đích Giáo dục

Các hình ảnh này được thiết kế để:
1. Minh họa trực quan Định lý Bayes
2. Làm rõ sự khác biệt Prior, Likelihood, Posterior
3. Giải thích Sequential Updating
4. So sánh Frequentist vs Bayesian
5. Làm rõ sự khác biệt giữa P-value và Posterior Probability

## Ghi chú

- Tất cả các hình ảnh đều có chú thích bằng tiếng Việt
- Màu sắc: Blue (Prior), Green (Likelihood), Red (Posterior)
- Các số liệu được tạo từ dữ liệu mô phỏng với seed cố định
- Font warnings về tiếng Việt có thể bỏ qua (không ảnh hưởng đến hình ảnh)
