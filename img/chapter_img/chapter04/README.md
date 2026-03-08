# Chapter 04 - Linear Regression - Hình ảnh Minh họa

## Tổng quan

Chapter này tập trung vào **Bayesian Linear Regression** - hiểu regression như một generative model thay vì chỉ "fitting a line".

## Danh sách Hình ảnh

### 1. `linear_regression_generative.png`
**Mô tả**: Data-generating process cho linear regression
- **Nội dung**:
  - Scatter plot với true regression line
  - Uncertainty bands (±1σ, ±2σ)
  - Generative story text box
  - Distribution cho specific x value
  - Residuals distribution
- **Sử dụng trong**: Bài 4.1 - Generative Model
- **Kích thước**: 16x12 inches
- **Ý nghĩa**: Minh họa cách dữ liệu được sinh ra từ model

### 2. `frequentist_vs_bayesian_regression.png`
**Mô tả**: So sánh Frequentist vs Bayesian approaches
- **Nội dung**:
  - Frequentist: Single OLS line với R², p-value
  - Bayesian: Posterior distribution of regression lines (100 samples)
  - Uncertainty quantification
- **Sử dụng trong**: Bài 4.1 - So sánh hai triết lý
- **Kích thước**: 16x6 inches
- **Ý nghĩa**: Thấy rõ sự khác biệt giữa point estimate và distribution

### 3. `parameter_interpretation.png`
**Mô tả**: Ý nghĩa của α, β, σ
- **Nội dung**:
  - Panel 1: Intercept (α) sau centering
  - Panel 2: Slope (β) - thay đổi y khi x tăng 1 unit
  - Panel 3: Noise (σ) - individual variability
- **Sử dụng trong**: Bài 4.1 - Parameter Interpretation
- **Kích thước**: 18x5 inches
- **Ý nghĩa**: Giúp hiểu rõ từng parameter

### 4. `standardization_comparison.png`
**Mô tả**: Raw vs Standardized data
- **Nội dung**:
  - Panel 1: Raw data (Height: 150-190 cm, Weight: 50-90 kg)
  - Panel 2: Standardized data (both mean=0, SD=1)
- **Sử dụng trong**: Bài 4.2 - Standardization
- **Kích thước**: 16x6 inches
- **Ý nghĩa**: Tại sao standardization quan trọng cho prior selection

### 5. `prior_selection.png`
**Mô tả**: Weakly informative priors cho α và β
- **Nội dung**:
  - 3 priors cho α: N(0,5) too wide, N(0,1) ✓, N(0,0.1) too narrow
  - 3 priors cho β: tương tự
- **Sử dụng trong**: Bài 4.2 - Prior Selection
- **Kích thước**: 18x10 inches
- **Ý nghĩa**: Chọn priors hợp lý, không quá wide/narrow

### 6. `prior_predictive_check.png`
**Mô tả**: Prior predictive distributions
- **Nội dung**:
  - Panel 1: β ~ N(0,1) - reasonable slopes ✓
  - Panel 2: β ~ N(0,5) - slopes quá extreme ✗
- **Sử dụng trong**: Bài 4.2 - Prior Predictive Check
- **Kích thước**: 16x6 inches
- **Ý nghĩa**: Kiểm tra priors có hợp lý trước khi fit model

## Thống kê

- **Tổng số hình**: 6
- **Định dạng**: PNG
- **Độ phân giải**: 300 DPI
- **Tổng dung lượng**: ~3.2 MB
- **Style**: Consistent với chapters trước

## Concepts Chính

1. **Generative Model**: Regression là câu chuyện về data-generating process
2. **Parameters**: α (intercept), β (slope), σ (noise)
3. **Frequentist vs Bayesian**: Point estimates vs Distributions
4. **Standardization**: Quan trọng cho prior selection
5. **Weakly Informative Priors**: N(0,1) cho α, β; HalfNormal(1) cho σ
6. **Prior Predictive Check**: Kiểm tra priors trước khi fit

## Tái tạo Hình ảnh

```bash
cd img/chapter_img/chapter04
python3 generate_chapter04_images.py
```

## Technical Details

- **Libraries**: numpy, matplotlib, scipy, seaborn
- **Seed**: 42 (reproducible)
- **Color scheme**:
  - Blue/Steelblue: Data points
  - Red: True values, regression lines
  - Green: Good/Recommended
  - Orange/Red: Bad/Not recommended

## Notes

- Tất cả hình ảnh sử dụng example về Height → Weight
- Data được generate với α=50, β=0.7, σ=5
- Standardization sử dụng z-score: (x - mean) / SD
- Priors recommendations: N(0,1) cho α, β; HalfNormal(1) cho σ

---

**Tác giả**: Nguyen Le Linh  
**Ngày tạo**: 11/01/2026  
**Chapter**: 04 - Linear Regression
