---
layout: post
title: "Bài 3.4: Hamiltonian Monte Carlo - MCMC Hiện đại và Mạnh mẽ"
chapter: '03'
order: 4
owner: Nguyen Le Linh
lang: vi
categories:
- chapter03
lesson_type: required
---

## Mục tiêu Học tập

Sau khi hoàn thành bài học này, bạn sẽ hiểu sâu sắc về **Hamiltonian Monte Carlo (HMC)** - thuật toán MCMC hiện đại và hiệu quả nhất hiện nay. Bạn sẽ không chỉ biết HMC hoạt động như thế nào, mà còn hiểu được ý tưởng thiên tài đằng sau nó: thay vì bước đi ngẫu nhiên như Metropolis-Hastings, HMC sử dụng **gradient** của posterior để di chuyển một cách thông minh và hiệu quả. Bạn sẽ nhận ra tại sao HMC là lựa chọn mặc định trong các công cụ Bayesian hiện đại như Stan và PyMC.

## Giới thiệu: Vấn đề của Random Walk

Metropolis-Hastings là một thuật toán elegant và mạnh mẽ, nhưng nó có một vấn đề lớn: **random walk behavior** (hành vi bước đi ngẫu nhiên).

Hãy tưởng tượng bạn đang tìm kiếm một kho báu trong một căn phòng tối. Metropolis-Hastings giống như việc bạn:
1. Đề xuất một bước đi ngẫu nhiên
2. Nếu bước đó đưa bạn đến nơi "tốt hơn" (posterior cao hơn), bạn đi
3. Nếu không, bạn có thể đi hoặc ở lại

Vấn đề là: **bạn không sử dụng bất kỳ thông tin nào về hướng đi**. Bạn chỉ bước đi ngẫu nhiên và hy vọng may mắn. Điều này dẫn đến:

- **Slow mixing**: Chuỗi di chuyển chậm trong không gian tham số
- **High autocorrelation**: Các mẫu liên tiếp rất giống nhau
- **Inefficiency**: Cần rất nhiều mẫu để có ước lượng tốt

Đặc biệt, khi posterior có **correlation** giữa các tham số hoặc có hình dạng phức tạp (ví dụ: hình elip dài và hẹp), random walk trở nên cực kỳ kém hiệu quả.

**Câu hỏi tự nhiên**: Liệu chúng ta có thể làm tốt hơn? Liệu chúng ta có thể sử dụng thông tin về **hướng đi** để di chuyển thông minh hơn?

Đây chính là lúc **Hamiltonian Monte Carlo** xuất hiện với một ý tưởng thiên tài: **sử dụng gradient của posterior để "lướt" qua không gian tham số một cách hiệu quả**.

## 1. Ý tưởng Cốt lõi: Từ Vật lý đến MCMC

HMC lấy cảm hứng từ **Hamiltonian dynamics** - một nhánh của vật lý cổ điển mô tả chuyển động của các hạt. Hãy xem ý tưởng này được chuyển đổi sang MCMC như thế nào.

### 1.1. Ẩn dụ Vật lý: Quả Bóng Lăn trên Đồi

Tưởng tượng posterior như một địa hình 3D (bề mặt), nơi độ cao tại mỗi điểm tỷ lệ với posterior density. Vùng có posterior cao là "thung lũng", vùng có posterior thấp là "đồi".

**Metropolis-Hastings**: Giống như một người đi bộ ngẫu nhiên trên địa hình này, không biết đường đi.

**Hamiltonian Monte Carlo**: Giống như một quả bóng được đẩy và lăn trên địa hình. Quả bóng:
- Có **động lượng** (momentum) - giúp nó di chuyển xa
- Chịu ảnh hưởng của **gradient** (độ dốc) - tự động đi theo hướng posterior cao
- **Lướt** qua không gian một cách mượt mà và hiệu quả

### 1.2. Hamiltonian Dynamics: Toán học Đằng sau

Trong vật lý Hamiltonian, một hệ thống được mô tả bởi:
- **Position** (vị trí) $$\theta$$: Tham số chúng ta quan tâm
- **Momentum** (động lượng) $$p$$: "Vận tốc" của tham số
- **Hamiltonian** (năng lượng toàn phần) $$H(\theta, p)$$: Tổng năng lượng của hệ

$$H(\theta, p) = U(\theta) + K(p)$$

Trong đó:
- $$U(\theta) = -\log P(\theta \mid D)$$: **Potential energy** (năng lượng thế) - càng thấp khi posterior càng cao
- $$K(p) = \frac{p^2}{2m}$$: **Kinetic energy** (động năng) - năng lượng từ chuyển động

**Phương trình Hamilton** mô tả cách hệ thống tiến hóa theo thời gian:

$$\frac{d\theta}{dt} = \frac{\partial H}{\partial p} = p$$

$$\frac{dp}{dt} = -\frac{\partial H}{\partial \theta} = -\frac{\partial U}{\partial \theta} = \frac{\partial \log P(\theta \mid D)}{\partial \theta}$$

**Ý nghĩa**: Gradient của posterior ($$\frac{\partial \log P(\theta \mid D)}{\partial \theta}$$) cho biết **hướng đi** để tăng posterior. HMC sử dụng thông tin này!

### 1.3. Tại sao Hamiltonian Dynamics Tốt cho MCMC?

Hamiltonian dynamics có hai tính chất quan trọng:

1. **Reversibility** (Tính khả nghịch): Nếu bạn đảo ngược momentum, hệ thống sẽ quay lại trạng thái ban đầu
2. **Volume preservation** (Bảo toàn thể tích): Thể tích trong không gian pha không thay đổi

Hai tính chất này đảm bảo rằng nếu chúng ta sử dụng Hamiltonian dynamics để propose trạng thái mới, **acceptance probability sẽ rất cao** (thường gần 100%)!

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Minh họa: So sánh Random Walk vs Hamiltonian Trajectory
np.random.seed(42)

# 2D Posterior: Bivariate Normal với correlation cao
mean = [0, 0]
cov = [[1, 0.95], [0.95, 1]]
posterior_2d = stats.multivariate_normal(mean, cov)

def log_posterior(theta):
    return posterior_2d.logpdf(theta)

def gradient_log_posterior(theta):
    # Gradient của log posterior cho Bivariate Normal
    inv_cov = np.linalg.inv(cov)
    return -inv_cov @ (theta - mean)

# Metropolis-Hastings trajectory (random walk)
def mh_trajectory(start, n_steps, step_size):
    trajectory = [start]
    current = start
        for _ in range(n_steps):
        proposed = current + np.random.normal(0, step_size, 2)
        log_r = log_posterior(proposed) - log_posterior(current)
        if np.log(np.random.uniform()) < log_r:
            current = proposed
        trajectory.append(current.copy())
    return np.array(trajectory)

# HMC-like trajectory (sử dụng gradient)
def hmc_like_trajectory(start, n_steps, step_size):
    trajectory = [start]
    theta = start.copy()
    momentum = np.random.normal(0, 1, 2)
    
    for _ in range(n_steps):
        # Leapfrog step (simplified)
        momentum = momentum + 0.5 * step_size * gradient_log_posterior(theta)
        theta = theta + step_size * momentum
        momentum = momentum + 0.5 * step_size * gradient_log_posterior(theta)
        trajectory.append(theta.copy())
    
    return np.array(trajectory)

# Generate trajectories
start_point = np.array([-2.0, -2.0])
mh_traj = mh_trajectory(start_point, 50, step_size=0.3)
hmc_traj = hmc_like_trajectory(start_point, 50, step_size=0.1)

# Vẽ
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Contour của posterior
x = np.linspace(-4, 4, 100)
y = np.linspace(-4, 4, 100)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))
Z = posterior_2d.pdf(pos)

for ax, traj, title, color in zip(axes, 
                                   [mh_traj, hmc_traj],
                                   ['Metropolis-Hastings: Random Walk', 
                                    'Hamiltonian MC: Gradient-guided'],
                                   ['blue', 'red']):
    ax.contour(X, Y, Z, levels=15, colors='gray', alpha=0.4)
    ax.plot(traj[:, 0], traj[:, 1], 'o-', color=color, linewidth=2, 
            markersize=4, alpha=0.7)
    ax.scatter(traj[0, 0], traj[0, 1], s=200, c='green', marker='o',
              edgecolors='black', linewidths=2, label='Start', zorder=5)
    ax.scatter(traj[-1, 0], traj[-1, 1], s=200, c='red', marker='*',
              edgecolors='black', linewidths=2, label='End', zorder=5)
    ax.set_xlabel('θ₁', fontsize=13, fontweight='bold')
    ax.set_ylabel('θ₂', fontsize=13, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)

plt.tight_layout()
plt.show()

print("=" * 70)
print("SO SÁNH METROPOLIS-HASTINGS VS HAMILTONIAN MC")
print("=" * 70)
print("\nMetropolis-Hastings (Random Walk):")
print("  - Bước đi ngẫu nhiên, không có hướng")
print("  - Di chuyển chậm, nhiều bước nhỏ")
print("  - Không hiệu quả với posterior có correlation")
print("\nHamiltonian MC (Gradient-guided):")
print("  - Sử dụng gradient để biết hướng đi")
print("  - Di chuyển xa và hiệu quả")
print("  - Khám phá không gian tham số nhanh hơn nhiều")
print("=" * 70)
```

## 2. Thuật toán HMC: Leapfrog Integration

Để implement HMC, chúng ta cần một cách để mô phỏng Hamiltonian dynamics. Phương pháp phổ biến nhất là **leapfrog integrator** - một thuật toán số để giải phương trình Hamilton.

### 2.1. Leapfrog Algorithm

Leapfrog integrator cập nhật position và momentum theo các bước "nhảy cóc":

```
For each leapfrog step:
    1. Half step for momentum:
       p ← p + (ε/2) × ∇log P(θ \mid D)
    
    2. Full step for position:
       θ ← θ + ε × p
    
    3. Half step for momentum:
       p ← p + (ε/2) × ∇log P(θ \mid D)
```

Trong đó $$\varepsilon$$ là **step size** (kích thước bước).

### 2.2. Thuật toán HMC Đầy đủ

**Input**:
- Current state: $$\theta^{(t)}$$
- Log posterior và gradient: $$\log P(\theta \mid D)$$ và $$\nabla \log P(\theta \mid D)$$
- Step size: $$\varepsilon$$
- Number of leapfrog steps: $$L$$

**Output**:
- Next state: $$\theta^{(t+1)}$$

**Quy trình**:

```
1. Sample momentum: p ~ N(0, I)

2. Simulate Hamiltonian dynamics (L leapfrog steps):
   For l = 1 to L:
       Apply leapfrog step
   
3. Compute acceptance probability:
   α = min(1, exp(H(θ⁽ᵗ⁾, p₀) - H(θ*, p*)))
   
4. Accept or reject:
   If u ~ Uniform(0,1) < α:
       θ⁽ᵗ⁺¹⁾ = θ*
   Else:
       θ⁽ᵗ⁺¹⁾ = θ⁽ᵗ⁾
```

**Lưu ý quan trọng**: Vì Hamiltonian dynamics bảo toàn năng lượng (lý tưởng), acceptance probability thường rất cao (>90%)!

## 3. NUTS: No-U-Turn Sampler

Một vấn đề của HMC cơ bản là phải chọn số bước leapfrog $$L$$. Quá ít: không khám phá đủ. Quá nhiều: lãng phí tính toán.

**NUTS** (No-U-Turn Sampler) là một phiên bản tự động của HMC, tự động chọn $$L$$ bằng cách:
- Tiếp tục chạy leapfrog cho đến khi trajectory bắt đầu "quay đầu" (U-turn)
- Dừng lại ngay khi phát hiện U-turn

NUTS là thuật toán mặc định trong **Stan** và **PyMC**, và nó hoạt động cực kỳ tốt trong thực tế mà không cần tuning nhiều.

## 4. Ưu điểm và Nhược điểm của HMC

### 4.1. Ưu điểm

✅ **Hiệu quả cao**: Di chuyển xa trong không gian tham số mỗi bước  
✅ **Low autocorrelation**: Các mẫu ít phụ thuộc nhau hơn  
✅ **Effective sample size cao**: Cần ít mẫu hơn để có ước lượng tốt  
✅ **Tốt với high-dimensional posterior**: Không bị curse of dimensionality như MH  
✅ **Tốt với correlated parameters**: Gradient giúp di chuyển theo hướng đúng  

### 4.2. Nhược điểm

❌ **Cần gradient**: Phải tính được $$\nabla \log P(\theta \mid D)$$  
❌ **Computational cost**: Mỗi iteration tốn nhiều tính toán hơn MH  
❌ **Tuning**: Cần chọn step size $$\varepsilon$$ phù hợp (nhưng NUTS giải quyết vấn đề này)  
❌ **Không phù hợp với discrete parameters**: HMC cần không gian liên tục  

## 5. So sánh Tổng thể: MH vs HMC

![HMC vs Metropolis-Hastings]({{ site.baseurl }}/img/chapter_img/chapter03/hmc_vs_mh.png)

| Khía cạnh | Metropolis-Hastings | Hamiltonian MC |
|-----------|---------------------|----------------|
| **Proposal** | Random walk | Gradient-guided |
| **Acceptance rate** | 20-50% (lý tưởng) | >90% (thường) |
| **Autocorrelation** | Cao | Thấp |
| **Efficiency** | Thấp (nhiều chiều) | Cao |
| **Cần gradient** | Không | Có |
| **Tuning** | Proposal SD | Step size, #steps |
| **Dễ implement** | Rất dễ | Phức tạp hơn |
| **Công cụ** | Tự code dễ | Dùng Stan/PyMC |

## 6. Khi nào Dùng HMC?

**Nên dùng HMC khi**:
- Posterior có nhiều chiều (>10 tham số)
- Các tham số có correlation
- Cần hiệu quả cao (ít mẫu hơn)
- Có thể tính gradient (hoặc dùng automatic differentiation)
- Dùng công cụ như Stan, PyMC

**Có thể dùng MH khi**:
- Posterior đơn giản, ít chiều
- Không tính được gradient
- Cần implement nhanh, đơn giản
- Học tập, nghiên cứu

## Tóm tắt và Kết nối

HMC là một bước nhảy vọt trong MCMC:

- **Ý tưởng**: Sử dụng gradient để di chuyển thông minh, không phải random walk
- **Hamiltonian dynamics**: Lấy cảm hứng từ vật lý, "lướt" qua posterior
- **Leapfrog integrator**: Cách mô phỏng Hamiltonian dynamics
- **NUTS**: Phiên bản tự động, không cần tuning nhiều
- **Hiệu quả**: Cao hơn MH nhiều lần, đặc biệt với nhiều chiều

HMC là lý do tại sao Bayesian statistics trở nên khả thi cho các mô hình phức tạp trong thực tế. Trong bài tiếp theo, chúng ta sẽ học cách **chẩn đoán** chất lượng mẫu MCMC và đảm bảo kết quả đáng tin cậy.

## Bài tập

**Bài tập 1: Hiểu Gradient**
Cho posterior: $$\log P(\theta \mid D) = -(\theta - 5)^2$$
(a) Tính gradient: $$\nabla \log P(\theta \mid D)$$
(b) Tại $$\theta = 3$$, gradient chỉ hướng nào? Giải thích.
(c) Tại $$\theta = 7$$, gradient chỉ hướng nào?
(d) Tại $$\theta = 5$$, gradient bằng bao nhiêu? Tại sao?

**Bài tập 2: So sánh Trajectories**
(a) Vẽ posterior 2D với correlation cao.
(b) Mô phỏng MH trajectory với 100 bước.
(c) Mô phỏng HMC-like trajectory (sử dụng gradient).
(d) So sánh: trajectory nào khám phá posterior tốt hơn?

**Bài tập 3: Acceptance Rate**
(a) Tại sao HMC có acceptance rate cao (>90%)?
(b) Điều gì xảy ra nếu step size quá lớn?
(c) NUTS giải quyết vấn đề gì của HMC cơ bản?

**Bài tập 4: Ưu nhược điểm**
Cho các tình huống sau, bạn sẽ chọn MH hay HMC? Giải thích.
(a) Posterior 1D đơn giản, Beta(5,2)
(b) Posterior 50D, các tham số có correlation
(c) Posterior có discrete parameters
(d) Cần kết quả nhanh, không quan tâm hiệu quả

**Bài tập 5: Suy ngẫm**
Viết một đoạn văn ngắn (200-300 từ):
(a) Tại sao HMC là "game changer" cho Bayesian statistics?
(b) Ẩn dụ vật lý (quả bóng lăn) giúp hiểu HMC như thế nào?
(c) Trong tương lai, bạn nghĩ MCMC sẽ phát triển theo hướng nào?

## Tài liệu Tham khảo

### Primary References:

**Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013).** *Bayesian Data Analysis* (3rd Edition). CRC Press.
- Chapter 12: Computationally efficient Markov chain simulation

**Kruschke, J. K. (2015).** *Doing Bayesian Data Analysis: A Tutorial with R, JAGS, and Stan* (2nd Edition). Academic Press.
- Chapter 14: Stan

### Supplementary Reading:

**Neal, R. M. (2011).** *MCMC using Hamiltonian dynamics*. Handbook of Markov Chain Monte Carlo, 2(11), 2.
- Bài báo kinh điển về HMC

**Hoffman, M. D., & Gelman, A. (2014).** *The No-U-Turn sampler: adaptively setting path lengths in Hamiltonian Monte Carlo*. Journal of Machine Learning Research, 15(1), 1593-1623.
- Bài báo giới thiệu NUTS

**Betancourt, M. (2017).** *A Conceptual Introduction to Hamiltonian Monte Carlo*. arXiv preprint arXiv:1701.02434.
- Giới thiệu conceptual xuất sắc về HMC

---

*Bài học tiếp theo: [3.5 MCMC Diagnostics - Kiểm tra Chất lượng Mẫu](/vi/chapter03/mcmc-diagnostics/)*
