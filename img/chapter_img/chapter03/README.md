# Hình ảnh Minh họa cho Chapter 03: MCMC

## Danh sách Hình ảnh

### 1. markov_chain_basics.png
**Mô tả**: Markov Chain Basics
- Trajectory của 3-state Markov chain
- Hội tụ về stationary distribution
- Transition matrix
- Phân phối empirical vs stationary
- **Vị trí**: Bài 3.2 - Markov Chain

### 2. metropolis_hastings.png
**Mô tả**: Metropolis-Hastings Algorithm
- Trace plot (500 iterations đầu)
- Histogram vs target distribution
- Autocorrelation plot
- Algorithm explanation
- Proposal width tuning
- Running mean convergence
- **Vị trí**: Bài 3.3 - Metropolis-Hastings

### 3. mcmc_diagnostics.png
**Mô tả**: MCMC Diagnostics - Good vs Bad
- Good trace plot ("fuzzy caterpillar")
- Bad trace plot (stuck, poor mixing)
- Good vs Bad distributions
- Good vs Bad autocorrelation
- **Vị trí**: Bài 3.5 - MCMC Diagnostics

### 4. convergence_diagnostics.png
**Mô tả**: Convergence Diagnostics - R-hat và ESS
- Multiple chains converging (good)
- Multiple chains not converging (bad)
- Gelman-Rubin R̂ diagnostic explanation
- Effective Sample Size (ESS) explanation
- **Vị trí**: Bài 3.5 - MCMC Diagnostics

### 5. hmc_vs_mh.png
**Mô tả**: HMC vs Metropolis-Hastings
- MH trajectory (random walk, slow)
- HMC trajectory (directed, efficient)
- Comparison table
- Khi nào dùng MH vs HMC
- **Vị trí**: Bài 3.4 - Hamiltonian Monte Carlo

### 6. mcmc_workflow.png
**Mô tả**: MCMC Workflow
- 6 bước workflow: Setup, Warmup, Sampling, Diagnostics, Analysis, Checking
- Common issues & solutions
- Tools (PyMC, Stan, ArviZ)
- Best practices
- **Vị trí**: Bài 3.6 - PyMC Implementation

## Thông tin Kỹ thuật

- **Độ phân giải**: 300 DPI
- **Định dạng**: PNG
- **Thư viện sử dụng**: 
  - matplotlib 3.10.6
  - scipy 1.16.3
  - seaborn 0.13.2
  - numpy 2.3.2
- **Ngày tạo**: 11/01/2026
- **Tổng dung lượng**: ~3.5 MB

## Mục đích Giáo dục

Các hình ảnh này được thiết kế để:
1. Giải thích Markov Chain property và stationary distribution
2. Minh họa Metropolis-Hastings algorithm
3. Dạy cách đọc và diễn giải MCMC diagnostics
4. Giải thích R-hat và ESS
5. So sánh HMC vs Metropolis-Hastings
6. Cung cấp workflow thực tế cho MCMC

## Ghi chú

- Tất cả các hình ảnh đều có chú thích bằng tiếng Việt
- Màu sắc: Green (Good), Red (Bad)
- Minh họa cả good và bad examples để học từ sai lầm
- Workflow bao gồm troubleshooting tips
