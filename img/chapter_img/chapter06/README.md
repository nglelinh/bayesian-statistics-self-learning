# Chapter 06 - Generalized Linear Models (GLM) - Hình ảnh Minh họa

## Tổng quan

Chapter này giới thiệu **Generalized Linear Models (GLM)** - mở rộng linear regression cho các outcome types khác nhau: binary (logistic), count (Poisson), và các link functions.

## Danh sách Hình ảnh

### 1. `logistic_regression_basics.png`
**Mô tả**: Logistic Regression cơ bản
- **Nội dung**:
  - Panel 1: Logistic function (sigmoid curve)
  - Panel 2: Binary data với probability curve
  - Panel 3: Interpretation text box
  - Panel 4: Odds ratio visualization
- **Sử dụng trong**: Bài 6.1 - Logistic Regression
- **Kích thước**: 16x12 inches
- **Ý nghĩa**: Hiểu logistic function và odds ratio

### 2. `poisson_regression_basics.png`
**Mô tả**: Poisson Regression cơ bản
- **Nội dung**:
  - Panel 1: Poisson distributions (λ = 1, 3, 5, 10)
  - Panel 2: Log link function
  - Panel 3: Count data example
  - Panel 4: Interpretation text box
- **Sử dụng trong**: Bài 6.2 - Poisson Regression
- **Kích thước**: 16x12 inches
- **Ý nghĩa**: Hiểu count data và log link

### 3. `link_functions_comparison.png`
**Mô tả**: So sánh Link Functions
- **Nội dung**:
  - Panel 1: Identity link (Linear) - Range: (-∞, +∞)
  - Panel 2: Logit link (Logistic) - Range: [0, 1]
  - Panel 3: Log link (Poisson) - Range: [0, +∞)
  - Panel 4: Summary table
- **Sử dụng trong**: Bài 6.1, 6.2 - Link Functions
- **Kích thước**: 16x12 inches
- **Ý nghĩa**: Thấy rõ sự khác biệt giữa các link functions

### 4. `model_evaluation_glm.png`
**Mô tả**: Model Evaluation cho GLM
- **Nội dung**:
  - Panel 1: ROC Curve (AUC = 0.85)
  - Panel 2: Confusion Matrix
  - Panel 3: Residual plot (Poisson)
  - Panel 4: Evaluation metrics text box
- **Sử dụng trong**: Bài 6.3 - Model Evaluation
- **Kích thước**: 16x12 inches
- **Ý nghĩa**: Cách đánh giá GLM models

## Thống kê

- **Tổng số hình**: 4
- **Định dạng**: PNG
- **Độ phân giải**: 300 DPI
- **Tổng dung lượng**: ~2.6 MB
- **Style**: Consistent với chapters trước

## Concepts Chính

1. **Logistic Regression**: Binary outcomes, logit link
2. **Odds Ratio**: exp(β) interpretation
3. **Poisson Regression**: Count data, log link
4. **Link Functions**: Transform outcome space to linear predictor space
5. **ROC Curve**: Classifier performance
6. **Confusion Matrix**: TP, TN, FP, FN
7. **Model Evaluation**: Accuracy, Precision, Recall, F1, AUC

## Tái tạo Hình ảnh

```bash
cd img/chapter_img/chapter06
python3 generate_chapter06_images.py
```

## Technical Details

- **Libraries**: numpy, matplotlib, scipy, seaborn, scipy.special.expit
- **Seed**: 42 (reproducible)
- **Color scheme**:
  - Blue: Logistic curves, Good models
  - Green: Success, Good practices
  - Red: Failure, Random classifier
  - Orange: Poisson distributions

## Notes

- Logistic regression: P(y=1|x) bounded [0,1]
- Poisson regression: λ = E[y|x] bounded [0,+∞)
- Link functions map outcome space → linear predictor space
- ROC curve: Trade-off between TPR and FPR
- Confusion matrix: Essential for classification evaluation
- Residual plots: Check model assumptions

## GLM Framework

```
Outcome Type    Link Function    Model
─────────────────────────────────────────
Continuous      Identity         Linear Regression
Binary          Logit            Logistic Regression
Count           Log              Poisson Regression
```

---

**Tác giả**: Nguyen Le Linh  
**Ngày tạo**: 11/01/2026  
**Chapter**: 06 - Generalized Linear Models (GLM)
