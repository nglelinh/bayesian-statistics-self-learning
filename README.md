# Bayesian Statistics - Self Learning Course

Khóa học **Bayesian Statistics** hoàn chỉnh bằng Tiếng Việt, được xây dựng dựa trên **Statistical Rethinking** của Richard McElreath.

**🎯 Mục tiêu**: Dạy Bayesian reasoning như một framework nhất quán để suy luận thống kê, thay thế NHST bằng probabilistic modeling.

**📚 33 bài học chi tiết** | **400+ biểu đồ minh họa** | **150+ bài tập thực hành** | **Python/PyMC**

## 🎯 Tính năng chính

- ✅ **33 bài học** chi tiết từ cơ bản đến nâng cao
- ✅ **400+ biểu đồ** minh họa concepts
- ✅ **150+ bài tập** thực hành với Jupyter notebooks
- ✅ **Python/PyMC** - Công cụ hiện đại
- ✅ **Tiếng Việt** - Dễ hiểu, dễ học
- ✅ **Complete Bayesian workflow** - Từ model đến interpretation
- ✅ **Real-world examples** - A/B testing, regression, GLM
- ✅ **Causal inference** - DAGs và confounding

## 📚 Cấu trúc Khóa học

### Chapter 00: Prerequisites (7 bài)
Kiến thức nền tảng: Probability, Distributions, Python, Linear Algebra, Calculus

### Chapter 01: Bayesian Inference (4 bài)
Replication crisis, P-values critique, Bayes' Theorem, Bayesian vs Frequentist

### Chapter 02: Probability & Updating (6 bài)
Likelihood, Prior, Posterior, Conjugate Priors, Grid Approximation (64 charts!)

### Chapter 03: MCMC (6 bài)
Monte Carlo, Markov Chain, Metropolis-Hastings, HMC, NUTS, PyMC, Diagnostics

### Chapter 04: Bayesian Linear Regression (4 bài)
Generative model, Priors, Posterior inference, Model checking, Predictions

### Chapter 05: Multivariate Regression (3 bài)
Multiple predictors, Confounding, DAGs, Multicollinearity

### Chapter 06: Bayesian GLM (2 bài)
Logistic Regression, Poisson Regression

### Chapter 07: Priors & Regularization (1 bài)
Regularization thông qua priors, Overfitting prevention

**📊 Tổng cộng**: 33 bài học | 400+ charts | 12-14 tuần

---

## 🚀 Bắt đầu Học

### Cho Sinh viên

1. **Clone repository**:
```bash
git clone https://github.com/your-username/bayesian-statistics-self-learning.git
cd bayesian-statistics-self-learning
```

2. **Cài đặt môi trường**:
```bash
pip install numpy matplotlib scipy seaborn pymc arviz pandas jupyter
```

3. **Bắt đầu học**:
- Đọc lecture notes trong `contents/vi/chapter00/`
- Làm bài tập trong `exercises/Chapter00_Prerequisites_Exercises.ipynb`
- Xem [COURSE_SUMMARY.md](./COURSE_SUMMARY.md) để biết lộ trình chi tiết

### Cho Giảng viên

1. **Review course structure**: [COURSE_SUMMARY.md](./COURSE_SUMMARY.md)
2. **Check lecture schedule**: [LECTURE_SCHEDULE.md](./LECTURE_SCHEDULE.md)
3. **Assign exercises**: `exercises/` folder
4. **Customize** theo nhu cầu lớp học

---

## 💻 Bài Tập & Labs

### **Exercises** (8 notebooks - 150+ problems)

Thư mục `exercises/` chứa **8 Jupyter notebooks** với **150+ bài tập**:

| Notebook | Topics | Time |
|----------|--------|------|
| Chapter00 | Prerequisites | 2-3h |
| Chapter01 | Bayesian Inference | 3-4h |
| Chapter02 | Probability & Updating | 4-5h |
| Chapter03 | MCMC | 5-6h |
| Chapter04 | Linear Regression | 4-5h |
| Chapter05 | Multivariate Regression | 4-5h |
| Chapter06 | GLM | 4-5h |
| Chapter07 | Regularization | 3-4h |

**Xem chi tiết**: [exercises/README.md](./exercises/README.md)

### **Labs** (7 labs - Complete solutions)

Thư mục `labs/` chứa **7 lab exercises** với **solutions đầy đủ** (2 formats):

| Lab | Topics | Solutions |
|-----|--------|-----------|
| Lab 1 | Conditional Probability & Bayes | ✅ .py + .ipynb |
| Lab 2 | Simulation & Inference | ✅ .py + .ipynb |
| Lab 3 | Continuous Distributions | ✅ .py + .ipynb |
| Lab 4 | Conjugate Priors | ✅ .py + .ipynb |
| Lab 5 | Normal Conjugacy | ✅ .py + .ipynb |
| Lab 6 | Point Estimation | ✅ .py + .ipynb |
| Lab 7 | Bayesian Regression | ✅ .py + .ipynb |

**Features:**
- ✅ **2 formats**: Python scripts (.py) + Jupyter notebooks (.ipynb)
- ✅ **Theory mapping**: Explicit links to lecture chapters
- ✅ **3000+ lines**: Production-quality code
- ✅ **Step-by-step**: Detailed solutions with visualizations

**Xem chi tiết**: [labs/README.md](./labs/README.md) | [labs/solutions/NOTEBOOKS_README.md](./labs/solutions/NOTEBOOKS_README.md)

---

## 🛠️ Công cụ

### Bắt buộc
- **Python** 3.8+
- **PyMC** 5.0+ (Bayesian modeling)
- **ArviZ** (Visualization & diagnostics)
- **NumPy, Matplotlib, SciPy**

### Tùy chọn
- **Jupyter Notebook** (Interactive learning)
- **Seaborn, Pandas**

### Installation
```bash
pip install pymc arviz numpy matplotlib scipy jupyter seaborn pandas
```

## 📁 Cấu trúc Thư mục

```
.
├── contents/vi/             # 📚 Lecture notes (Tiếng Việt)
│   ├── chapter00/           # Prerequisites (7 bài)
│   ├── chapter01/           # Bayesian Inference (4 bài)
│   ├── chapter02/           # Probability & Updating (6 bài)
│   ├── chapter03/           # MCMC (6 bài)
│   ├── chapter04/           # Linear Regression (4 bài)
│   ├── chapter05/           # Multivariate Regression (3 bài)
│   ├── chapter06/           # GLM (2 bài)
│   └── chapter07/           # Regularization (1 bài)
│
├── exercises/               # 💻 Jupyter notebooks bài tập
│   ├── Chapter00_Prerequisites_Exercises.ipynb
│   ├── Chapter01_Bayesian_Inference_Exercises.ipynb
│   ├── Chapter02_Probability_Updating_Exercises.ipynb
│   ├── Chapter03_MCMC_Exercises.ipynb
│   ├── Chapter04_Linear_Regression_Exercises.ipynb
│   ├── Chapter05_Multivariate_Regression_Exercises.ipynb
│   ├── Chapter06_GLM_Exercises.ipynb
│   ├── Chapter07_Regularization_Exercises.ipynb
│   ├── README.md
│   └── EXERCISES_OVERVIEW.md
│
├── img/chapter_img/         # 📊 Hình ảnh minh họa
│
├── COURSE_SUMMARY.md        # 📖 Tổng quan khóa học
├── LECTURE_SCHEDULE.md      # 📅 Lịch giảng 14 tuần
├── README.md                # Hướng dẫn này
│
└── [Jekyll files]           # Website infrastructure
    ├── _config.yml
    ├── _includes/
    ├── _layouts/
    ├── _plugins/
    └── public/
```

## 📖 Tài liệu Tham khảo

### Primary (Bắt buộc)
- **Richard McElreath (2020)** - *Statistical Rethinking* (2nd Edition)
- **Video lectures**: https://www.youtube.com/playlist?list=PLDcUM9US4XdM9_N6XUUFrhghGJ4K25bFc

### Secondary (Tham khảo)
- **Andrew Gelman et al.** - *Bayesian Data Analysis* (3rd Edition)
- **John K. Kruschke** - *Doing Bayesian Data Analysis*
- **PyMC Documentation**: https://www.pymc.io/
- **ArviZ Documentation**: https://arviz-devs.github.io/

---

## 🎯 Learning Outcomes

Sau khi hoàn thành khóa học, bạn sẽ:

- ✅ **Hiểu Bayesian reasoning** - Không chỉ công thức
- ✅ **Critique p-values** - Biết tại sao NHST có vấn đề
- ✅ **Implement MCMC** - Từ Metropolis-Hastings đến NUTS
- ✅ **Sử dụng PyMC** - Fit models thực tế
- ✅ **Check diagnostics** - R-hat, ESS, trace plots, divergences
- ✅ **Interpret posteriors** - Uncertainty quantification
- ✅ **Make predictions** - Với credible intervals
- ✅ **Causal thinking** - DAGs, confounding, colliders
- ✅ **Model comparison** - LOO, WAIC (preview)
- ✅ **Regularization** - Priors để ngăn overfitting

---

## 🎓 Đối tượng Học viên

### Phù hợp cho:
- ✅ Graduate students (Data Science, Statistics, ML)
- ✅ Researchers cần Bayesian methods
- ✅ Data scientists muốn nâng cao
- ✅ Anyone có background toán/thống kê cơ bản

### Yêu cầu tiên quyết:
- Probability & Statistics cơ bản
- Linear algebra cơ bản
- Python programming
- Calculus cơ bản (derivatives, integrals)

## 🛠️ Development (Website)

### Chạy Jekyll local server

```bash
# Cài đặt Ruby dependencies
bundle install

# Chạy server
bundle exec jekyll serve

# Truy cập tại
http://127.0.0.1:4000/bayesian-statistics-self-learning/
```

### Deploy to GitHub Pages

1. Push to GitHub
2. GitHub Actions tự động build và deploy
3. Truy cập tại: `https://nglelinh.github.io/bayesian-statistics-self-learning/`

---

## 💡 Tips Học Tập

### Cho Sinh viên

1. **Đọc lecture notes trước** - Hiểu concepts
2. **Làm bài tập** - Practice makes perfect
3. **Chạy code** - Don't just read
4. **Visualize** - Plots giúp hiểu
5. **Interpret** - Không chỉ numbers
6. **Ask questions** - Discussion forum

### Cho Giảng viên

1. **1 chapter/week** - Sustainable pace
2. **Live coding** - Demo trong class
3. **Office hours** - Support students
4. **Peer review** - Students learn from each other
5. **Real data** - Make it relevant
6. **Emphasize interpretation** - Not just mechanics

## 🤝 Đóng góp

Contributions are welcome! Để đóng góp:

1. Fork repository
2. Tạo branch: `git checkout -b feature/improvement`
3. Commit: `git commit -am 'Add improvement'`
4. Push: `git push origin feature/improvement`
5. Tạo Pull Request

**Areas for contribution**:
- Thêm examples
- Improve explanations
- Fix typos
- Add visualizations
- Translate to English

---

## 📄 License

Course content: Educational use  
Code: MIT License  
Theme: Lanyon by Mark Otto

---

## 🙏 Acknowledgments

- **Richard McElreath** - Statistical Rethinking
- **PyMC Development Team**
- **ArviZ Development Team**
- **Bayesian Statistics Community**

---

## 📞 Contact

**Giảng viên**: Nguyen Le Linh  
**Email**: [Your email]  
**Issues**: [GitHub Issues](../../issues)

---

## 🎉 Course Status

**✅ COMPLETE AND READY TO USE**

### **Theory:**
- ✅ **43 lecture notes** (11 chapters)
- ✅ **400+ illustrations**
- ✅ **Narrative style** - Pedagogical approach
- ✅ **Vietnamese** - Full translation

### **Practice:**
- ✅ **8 exercise notebooks** (150+ problems)
- ✅ **7 lab exercises** with complete solutions
- ✅ **14 solution files** (7 .py + 7 .ipynb)
- ✅ **3000+ lines** of production code
- ✅ **Theory mapping** - Labs ↔ Chapters

### **Documentation:**
- ✅ **Complete guides** - All aspects covered
- ✅ **Quick references** - Easy lookup
- ✅ **Student guide** - Learning pathway
- ✅ **12-15 week curriculum**

**Start learning Bayesian Statistics today! 🚀**

**Quick links:**
- 📚 [Course Index](./COURSE_INDEX.md) - Complete overview
- 🎓 [Student Guide](./STUDENT_GUIDE.md) - How to learn
- 💻 [Lab Solutions](./labs/solutions/NOTEBOOKS_README.md) - Interactive notebooks
- 📊 [Final Summary](./FINAL_COMPLETE_SUMMARY.md) - What we built

---

**Last updated**: January 2025  
**Version**: 1.0  
**Status**: Production-ready

---

**Happy Learning! 🎓📊🐍**
