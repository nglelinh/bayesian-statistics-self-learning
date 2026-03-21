# Hình ảnh Minh họa cho Chapter 00: Prerequisites

## Danh sách Hình ảnh

### Bài 0.3: Thống kê Mô tả (MỚI!)

1. **descriptive_mean_vs_median.png** - So sánh trung bình và trung vị dưới phân phối đối xứng và lệch phải
   - Panel trái: phân phối gần đối xứng, mean và median gần nhau
   - Panel phải: phân phối lệch phải, mean bị kéo về phía đuôi dài
   - Minh họa trực quan cách phát hiện độ lệch trước khi mô hình hóa

2. **descriptive_spread_and_boxplot.png** - Minh họa độ phân tán và box plot / IQR
   - Panel trái: hai tập dữ liệu cùng trung bình nhưng khác độ lệch chuẩn
   - Panel phải: box plot với Q1, median, Q3, IQR và outlier tiềm năng
   - Nhấn mạnh rằng biết giá trị trung tâm là chưa đủ

3. **descriptive_correlation_patterns.png** - Ba mẫu hình scatter plot quan trọng
   - Tuyến tính dương: Pearson r hoạt động tốt
   - Phi tuyến: r có thể gần 0 dù vẫn có cấu trúc rõ
   - Tương quan do nhóm ẩn: nhắc lại rằng correlation không ngụ ý causation

### Bài 0.8: P-values và Kiểm định Giả thuyết

1. **pvalue_ttest_illustration.png** - Minh họa phân phối t và vùng p-value trong kiểm định t hai phía
   - Cho thấy phân phối t với df=24
   - Vùng đỏ thể hiện p-value (hai đuôi)
   - Giá trị t quan sát = 2.02, p-value ≈ 0.054

2. **effect_size_vs_sample_size.png** - So sánh ảnh hưởng của kích thước hiệu ứng và kích thước mẫu
   - Bên trái: Hiệu ứng nhỏ (0.5 cm) với mẫu lớn (n=1000) → p < 0.05
   - Bên phải: Hiệu ứng lớn (5 cm) với mẫu nhỏ (n=20) → p có thể > 0.05
   - Minh họa: "Ý nghĩa thống kê" ≠ "Ý nghĩa thực tiễn"

3. **pvalue_misinterpretations.png** - Bốn hiểu lầm phổ biến về p-values
   - P(data|H₀) ≠ P(H₀|data)
   - P-value nhỏ không có nghĩa là hiệu ứng lớn
   - P-value lớn không chứng minh H₀ đúng
   - Ngưỡng α = 0.05 là tùy ý

4. **multiple_testing_problem.png** - Vấn đề multiple testing (p-hacking)
   - 20 kiểm định độc lập khi H₀ đúng
   - Kỳ vọng tìm thấy ~1 kết quả "có ý nghĩa" do ngẫu nhiên
   - Minh họa false positive rate

5. **confidence_vs_credible_intervals.png** - So sánh Confidence Intervals (Frequentist) và Credible Intervals (Bayesian)
   - Phần trên: 50 confidence intervals 95% từ các thí nghiệm khác nhau
   - Phần dưới: Một credible interval 95% với phân phối posterior
   - Minh họa sự khác biệt trong diễn giải

6. **sample_size_calculation.png** - Kích thước mẫu cần thiết để phát hiện hiệu ứng
   - Mối quan hệ giữa effect size và sample size
   - Power = 0.80, α = 0.05, σ = 7 cm
   - Hiệu ứng nhỏ cần mẫu rất lớn

### Bài 0.9: T-test và Phân phối T (MỚI!)

7. **t_vs_normal_distribution.png** - So sánh phân phối T với Normal
   - T-distribution với df = 2, 5, 10, 30
   - So với phân phối chuẩn (df = ∞)
   - Minh họa đuôi dày hơn khi mẫu nhỏ

8. **t_value_interpretation.png** - Cách diễn giải các t-value khác nhau
   - 4 scenarios: t = 0.5, 2.0, 3.0, và -0.70 (chocolate example)
   - Mỗi panel hiển thị p-value tương ứng
   - Giúp sinh viên hiểu quan hệ giữa t-value và p-value

9. **t_test_types.png** - Ba loại t-test với ví dụ cụ thể
   - One-sample: Chocolate weight test
   - Independent two-sample: So sánh chiều cao hai khoa
   - Paired: Cân nặng trước/sau dùng thuốc
   - Bảng tóm tắt công thức và df

## Scripts

- `generate_images.py` - Script gốc tạo hình ảnh cho bài 0.8
- `generate_images_professional.py` - Script cải tiến với style chuyên nghiệp cho bài 0.8
- `generate_descriptive_statistics_images.py` - Script tạo hình minh họa cho bài 0.3 (MỚI!)
- `generate_t_test_images.py` - Script tạo hình ảnh cho bài 0.9 (MỚI!)

## Usage

Để tái tạo tất cả hình ảnh:

```bash
# Bài 0.3: Thống kê mô tả
python3 generate_descriptive_statistics_images.py

# Bài 0.8: P-values
python3 generate_images_professional.py

# Bài 0.9: T-test
python3 generate_t_test_images.py
```

## Image Quality

- **Resolution**: 300 DPI (publication quality)
- **Format**: PNG with transparency support
- **Color scheme**: Professional, modern, consistent palette
- **Style**: Clean, educational, accessible
- **Size**: 200-700KB per image (optimized)
