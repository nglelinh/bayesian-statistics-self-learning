# Chapter 05 - Multivariate Regression - Hình ảnh Minh họa

## Tổng quan

Chapter này tập trung vào **Multivariate Regression** - mở rộng từ một predictor sang nhiều predictors, và các vấn đề phức tạp như confounding, multicollinearity, và interaction effects.

## Danh sách Hình ảnh

### 1. `multiple_predictors_visualization.png`
**Mô tả**: Visualization cho multiple predictors
- **Nội dung**:
  - Panel 1: Weight vs Height (colored by Age)
  - Panel 2: Weight vs Age (colored by Height)
  - Panel 3: 3D visualization (Height, Age, Weight)
- **Sử dụng trong**: Bài 5.1 - Multiple Predictors
- **Kích thước**: 18x6 inches
- **Ý nghĩa**: Thấy rõ mối quan hệ giữa nhiều biến

### 2. `confounding_dags.png`
**Mô tả**: DAGs và Causal Inference
- **Nội dung**:
  - Panel 1: Confounding DAG (Z → X, Z → Y)
  - Panel 2: Simpson's Paradox visualization
  - Panel 3: Collider Bias DAG
  - Panel 4: Mediation DAG
- **Sử dụng trong**: Bài 5.2 - Confounding and DAGs
- **Kích thước**: 16x12 inches
- **Ý nghĩa**: Hiểu causal relationships và khi nào control variables

### 3. `multicollinearity_effects.png`
**Mô tả**: Effects của Multicollinearity
- **Nội dung**:
  - Panel 1: Low correlation (r=0.2) ✓
  - Panel 2: High correlation (r=0.95) ✗
  - Panel 3: Posterior với low correlation (narrow, independent)
  - Panel 4: Posterior với high correlation (wide, correlated)
- **Sử dụng trong**: Bài 5.3 - Multicollinearity
- **Kích thước**: 16x12 inches
- **Ý nghĩa**: Tại sao multicollinearity là vấn đề

### 4. `interaction_effects.png`
**Mô tả**: Interaction Effects
- **Nội dung**:
  - Panel 1: No interaction (parallel slopes)
  - Panel 2: With interaction (different slopes)
  - Panel 3: Model comparison text box
  - Panel 4: Continuous interaction
- **Sử dụng trong**: Bài 5.4 - Interaction Effects
- **Kích thước**: 16x12 inches
- **Ý nghĩa**: Khi nào effect của X phụ thuộc vào Z

## Thống kê

- **Tổng số hình**: 4
- **Định dạng**: PNG
- **Độ phân giải**: 300 DPI
- **Tổng dung lượng**: ~2.8 MB
- **Style**: Consistent với chapters trước

## Concepts Chính

1. **Multiple Predictors**: Nhiều biến độc lập cùng lúc
2. **"Holding Others Constant"**: Ý nghĩa của coefficients trong multiple regression
3. **Confounding**: Biến gây nhiễu cần control
4. **Simpson's Paradox**: Trend đảo ngược khi aggregate
5. **Collider Bias**: Khi KHÔNG nên control
6. **Multicollinearity**: Predictors tương quan cao → posterior uncertainty tăng
7. **Interaction**: Effect của X phụ thuộc vào Z

## Tái tạo Hình ảnh

```bash
cd img/chapter_img/chapter05
python3 generate_chapter05_images.py
```

## Technical Details

- **Libraries**: numpy, matplotlib, scipy, seaborn, mpl_toolkits.mplot3d
- **Seed**: 42 (reproducible)
- **Color scheme**:
  - Blue/Steelblue: Data points, Good practices
  - Red: Bad practices, High correlation
  - Green: Good practices, Low correlation
  - Viridis/Plasma: Colormaps for 3D

## Notes

- 3D visualization giúp hiểu multiple predictors
- DAGs rất quan trọng cho causal inference
- Simpson's Paradox là ví dụ kinh điển về confounding
- Multicollinearity không bias estimates nhưng tăng uncertainty
- Interaction effects cần test explicitly

---

**Tác giả**: Nguyen Le Linh  
**Ngày tạo**: 11/01/2026  
**Chapter**: 05 - Multivariate Regression
