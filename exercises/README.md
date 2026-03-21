# Bài Tập - Bayesian Statistics Course

Thư mục này chứa **Jupyter notebooks bài tập** cho từng chapter của course.

---

## 📚 Danh sách Notebooks

| Chapter | Notebook | Nội dung | Thời gian |
|---------|----------|----------|-----------|
| 00 | `Chapter00_Prerequisites_Exercises.ipynb` | Probability, Distributions, Statistics, Python, Linear Algebra, Calculus | 2-3 giờ |
| 01 | `Chapter01_Bayesian_Inference_Exercises.ipynb` | P-values, Bayes' Theorem, Bayesian vs Frequentist | 3-4 giờ |
| 02 | `Chapter02_Probability_Updating_Exercises.ipynb` | Likelihood, Prior, Posterior, Conjugate Priors, Grid Approximation | 4-5 giờ |
| 04 | `Chapter04_Linear_Regression_Exercises.ipynb` | Bayesian Linear Regression, Model Checking, Predictions | 4-5 giờ |
| 05 | `Chapter05_Multivariate_Regression_Exercises.ipynb` | Multiple Predictors, Confounding, DAGs, Multicollinearity | 4-5 giờ |
| 06 | `Chapter06_GLM_Exercises.ipynb` | Logistic Regression, Poisson Regression, Overdispersion | 4-5 giờ |
| 07 | `Chapter07_Regularization_Exercises.ipynb` | Overfitting, Regularization, Prior Choice | 3-4 giờ |

**Tổng thời gian**: ~30-40 giờ

---

## 🎯 Cấu trúc Mỗi Notebook

Mỗi notebook bao gồm:

1. **Import libraries** - Setup môi trường
2. **Bài tập lý thuyết** - Câu hỏi conceptual
3. **Coding exercises** - Implement từ đầu
4. **Real data analysis** - Áp dụng thực tế
5. **Tự đánh giá** - Checklist kiến thức

---

## 🛠️ Cài đặt

### Requirements

```bash
pip install numpy matplotlib scipy seaborn pymc arviz pandas jupyter
```

### Kiểm tra

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import pymc as pm
import arviz as az
import pandas as pd

print("✅ All libraries installed!")
```

---

## 📖 Cách Sử dụng

### Cho Sinh viên

1. **Đọc lecture notes** trước
2. **Mở notebook** tương ứng
3. **Làm bài tập** từ trên xuống
4. **Chạy code** và kiểm tra kết quả
5. **Tự đánh giá** ở cuối notebook

### Cho Giảng viên

- Assign notebooks như homework
- Students submit completed notebooks
- Auto-grading có thể dùng `nbgrader`
- Hoặc manual grading

---

## 💡 Tips

### Khi Làm Bài

- ✅ Đọc kỹ đề bài
- ✅ Thử tự làm trước khi xem hints
- ✅ Run code từng cell
- ✅ Visualize để hiểu
- ✅ Interpret results, không chỉ code

### Khi Gặp Khó khăn

1. Review lecture notes
2. Check PyMC/ArviZ documentation
3. Google error messages
4. Ask in discussion forum
5. Office hours

---

## 📝 Đánh giá

### Tự đánh giá

Mỗi notebook có checklist cuối:
- [ ] Hiểu concepts
- [ ] Code chạy được
- [ ] Interpret đúng
- [ ] Apply được

### Nộp bài (nếu là homework)

```bash
# Rename với tên của bạn
mv Chapter01_Bayesian_Inference_Exercises.ipynb \
   Chapter01_NguyenVanA_Exercises.ipynb

# Hoặc export to HTML
jupyter nbconvert --to html Chapter01_Bayesian_Inference_Exercises.ipynb
```

---

## 🎓 Learning Objectives

Sau khi hoàn thành tất cả notebooks, bạn sẽ:

- ✅ Thành thạo Bayesian reasoning
- ✅ Implement Bayesian models từ đầu
- ✅ Sử dụng PyMC cho real problems
- ✅ Fit và interpret Bayesian models
- ✅ Check diagnostics và model assumptions
- ✅ Make predictions với uncertainty
- ✅ Understand causal inference basics
- ✅ Handle overfitting với regularization

---

## 📚 Tài liệu Tham khảo

### Primary
- **Statistical Rethinking** (McElreath) - Chapters tương ứng
- **PyMC Documentation**: https://www.pymc.io/
- **ArviZ Documentation**: https://arviz-devs.github.io/

### Supplementary
- **Bayesian Data Analysis** (Gelman et al.)
- **Doing Bayesian Data Analysis** (Kruschke)
- **PyMC Examples**: https://www.pymc.io/projects/examples/

---

## 🐛 Troubleshooting

### Common Issues

**1. Import errors**
```bash
pip install --upgrade pymc arviz
```

**2. Sampling too slow**
- Reduce iterations
- Simplify model
- Check for divergences

**3. Divergences**
- Increase `target_accept`
- Reparameterize model
- Check priors

**4. Notebook won't open**
```bash
jupyter notebook Chapter01_Bayesian_Inference_Exercises.ipynb
```

---

## 📧 Support

- **Giảng viên**: [Your email]
- **Discussion forum**: [Link]
- **Office hours**: [Schedule]

---

## 🎉 Chúc Bạn Học Tốt!

**Remember**: Bayesian statistics là về **reasoning under uncertainty**, không chỉ là công thức!

---

**Last updated**: January 2025  
**Version**: 1.0


