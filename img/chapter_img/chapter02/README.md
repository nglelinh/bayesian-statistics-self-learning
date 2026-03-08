# Hình ảnh Minh họa cho Chapter 02: Probability Updating

## Danh sách Hình ảnh

### 1. beta_distribution_family.png
**Mô tả**: Họ phân phối Beta với các tham số khác nhau
- 6 biến thể của Beta distribution
- Beta(2,2) - Đồng nhất yếu
- Beta(5,2) - Lệch phải
- Beta(2,5) - Lệch trái
- Beta(10,10) - Tập trung
- Beta(0.5,0.5) - U-shaped
- Beta(1,1) - Đồng nhất hoàn toàn
- **Vị trí**: Bài 2.1 - Phân phối Xác suất

### 2. conjugate_prior_beta_binomial.png
**Mô tả**: Conjugate Prior - Beta-Binomial
- Prior: Beta(2, 2)
- Likelihood: Binomial (7/10 thành công)
- Posterior: Beta(9, 5)
- So sánh Prior, Likelihood, Posterior
- Minh họa conjugacy property
- **Vị trí**: Bài 2.5 - Conjugate Priors

### 3. grid_approximation.png
**Mô tả**: Grid Approximation với các grid sizes khác nhau
- 6 grid sizes: 5, 10, 20, 50, 100, 1000
- So sánh với true posterior (Beta)
- Minh họa trade-off giữa độ chính xác và tính toán
- **Vị trí**: Bài 2.6 - Grid Approximation

### 4. prior_data_tradeoff.png
**Mô tả**: Prior-Data Tradeoff
- 4 scenarios:
  - Weak prior + Ít dữ liệu → Posterior rất không chắc chắn
  - Weak prior + Nhiều dữ liệu → Data chi phối
  - Strong prior + Ít dữ liệu → Prior chi phối
  - Strong prior + Nhiều dữ liệu → Thỏa hiệp
- **Vị trí**: Bài 2.3 - Prior, Bài 2.4 - Posterior

### 5. posterior_predictive.png
**Mô tả**: Posterior Predictive Distribution
- Posterior sau quan sát
- Posterior predictive cho dữ liệu mới
- So sánh với point estimate prediction
- Minh họa uncertainty propagation
- **Vị trí**: Bài 2.4 - Posterior

### 6. conjugate_families.png
**Mô tả**: Các Conjugate Families phổ biến
- Beta-Binomial
- Normal-Normal
- Gamma-Poisson
- Tại sao conjugacy quan trọng
- Khi nào dùng/không dùng
- **Vị trí**: Bài 2.5 - Conjugate Priors

## Thông tin Kỹ thuật

- **Độ phân giải**: 300 DPI
- **Định dạng**: PNG
- **Thư viện sử dụng**: 
  - matplotlib 3.10.6
  - scipy 1.16.3
  - seaborn 0.13.2
  - numpy 2.3.2
- **Ngày tạo**: 11/01/2026
- **Tổng dung lượng**: ~3 MB

## Mục đích Giáo dục

Các hình ảnh này được thiết kế để:
1. Minh họa họ phân phối Beta và tính linh hoạt của nó
2. Làm rõ conjugate prior property
3. Giải thích grid approximation method
4. Minh họa prior-data tradeoff
5. Giải thích posterior predictive distribution
6. Tổng hợp các conjugate families phổ biến

## Ghi chú

- Tất cả các hình ảnh đều có chú thích bằng tiếng Việt
- Màu sắc: Blue (Prior), Green (Likelihood), Red (Posterior)
- Các ví dụ sử dụng Beta-Binomial vì dễ hiểu và trực quan
- Grid approximation minh họa từ thô đến mịn
