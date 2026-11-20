# Explainers — minh họa tương tác từng bước (Svelte + D3 + Vite)

Thư mục này chứa các "explainer": widget có nút **Bước tiếp / Lùi / Play**, thanh trượt và
biểu đồ SVG, nhúng vào bài học Jekyll bằng một thẻ `<div data-demo="...">`.
Toàn bộ explainer của khóa học nằm trong **một bundle duy nhất**: `public/js/explainers/bayes-explainer.js`.

## Build

```bash
cd explainers
npm install          # lần đầu
npm run build        # tạo ../public/js/explainers/bayes-explainer.js (đã đính kèm CSS)
npm test             # kiểm tra số học (node --test)
npm run dev          # Vite dev server (tuỳ chọn)
```

Bundle build ra được commit cùng repo (GitHub Pages không chạy npm). `explainers/` bị loại khỏi site
(`exclude` trong `_config.yml`) và `explainers/node_modules/` nằm trong `.gitignore`.

## Chạy thử site

> **Cảnh báo: phải serve từ thư mục gốc của repo** (hoặc từ thư mục cha của site đã build) vì `baseurl` là
> `/bayesian-statistics-self-learning`. Mở file HTML trực tiếp, hoặc serve từ `explainers/`, sẽ làm
> đường dẫn `/public/js/explainers/...` bị 404.

```bash
# Cách 1: Jekyll (từ gốc repo)
bundle exec jekyll serve --port 4010
# -> http://127.0.0.1:4010/bayesian-statistics-self-learning/

# Cách 2: build tạm rồi serve từ thư mục cha
bundle exec jekyll build -d /tmp/site/bayesian-statistics-self-learning
cd /tmp/site && python3 -m http.server 4018 --bind 127.0.0.1
```

Site có cổng mật khẩu (`access_gate`); khi kiểm thử tự động cần mở khóa lớp này (xem `check-pages.mjs` ghi chú).

## Kiểm tra bằng Chrome headless

```bash
cd explainers
PORT=9391 node check-pages.mjs http://127.0.0.1:4018/bayesian-statistics-self-learning \
  /contents/vi/chapter02/02_05_conjugate_priors/ /contents/vi/chapter04/04_02b_mcmc_theory/
```

Script mở từng trang, bấm mọi nút, đổi mọi select và báo lỗi console. Mọi `data-demo` phải kết thúc bằng `-explainer`.

## Nhúng vào bài học

```html
### Thử nghiệm: tiêu đề

Mô tả ngắn.

<div class="interactive-demo" markdown="1">
<div data-demo="conjugate-explainer" data-lang="vi" data-tab="betabinom"></div>
</div>
<script src="{{ '/public/js/explainers/bayes-explainer.js' | relative_url }}"></script>
```

**Chỉ một thẻ `<script>` cho mỗi trang** (đặt ở block đầu tiên). Nạp hai bundle Svelte trên cùng một trang sẽ xung đột.

## Ngôn ngữ (VI / EN)

Mọi component nhận `data-lang="vi|en"` (mặc định lấy từ `<html lang>`, nếu không phải `en` thì dùng `vi`).
Bài tiếng Anh (hiện có `contents/en/chapter02/02_03–02_06`) phải ghi `data-lang="en"`.

## Các explainer và thuộc tính

| `data-demo` | Nội dung | Thuộc tính |
|---|---|---|
| `bayesrule-explainer` | Cây tần suất tự nhiên; cập nhật tuần tự 3 đồng xu | `data-tab` tree\|sequential, `data-preset` disease\|common\|spam |
| `conjugate-explainer` | Beta–Binomial, Gamma–Poisson, Normal–Normal từng quan sát, đối chiếu lưới | `data-tab` betabinom\|gammapoisson\|normalnormal, `data-a`, `data-b`, `data-theta` |
| `grid-explainer` | Xấp xỉ lưới từng bước | `data-prior` flat\|beta22\|beta55\|tri\|bimodal, `data-k`, `data-n`, `data-points` |
| `mcmc-explainer` | Metropolis (4 chuỗi, R-hat), Gibbs, HMC (leapfrog) | `data-tab` metropolis\|gibbs\|hmc, `data-target` beta\|normal\|bimodal |
| `interval-explainer` | Độ phủ của khoảng tin cậy vs khoảng đáng tin | — |
| `clt-explainer` | LLN và CLT | `data-tab` clt\|lln, `data-dist` uniform\|exponential\|bernoulli\|bimodal |
| `ppc-explainer` | Kiểm tra dự đoán posterior | `data-data` iid\|streaky\|alternating, `data-stat` total\|switches\|longestRun |
| `regression-explainer` | Hồi quy tuyến tính Bayes, bó đường posterior | `data-a`, `data-b` |
| `shrink-explainer` | Prior chuẩn = ridge, co hệ số đa thức | `data-degree` 1–12 |
| `ic-explainer` | WAIC / LOO chính xác theo bậc đa thức; trung bình mô hình pseudo-BMA | `data-tab` waic\|avg |
| `decision-explainer` | Ngưỡng quyết định A/B, hàm mất mát → điểm tóm tắt, EVSI/EVPI | `data-tab` threshold\|loss\|voi |
| `glm-explainer` | Hồi quy logistic / Poisson Bayes (posterior lưới 2-D) | `data-tab` logistic\|poisson |
| `pooling-explainer` | Partial pooling phân cấp (8 trường), posterior của τ | `data-data` schools\|equal |
| `confound-explainer` | Confounder (fork, Simpson), collider, interaction bằng mô phỏng | `data-tab` fork\|collider\|interaction |
| `pvalue-explainer` | p-value đều dưới H₀, phân phối t, công suất | `data-tab` pnull\|tdist\|power |
| `likelihood-explainer` | Likelihood nhị thức/Poisson từng quan sát, prior predictive | `data-tab` binom\|poisson\|predictive |
| `bf-explainer` | Bayes factor, marginal likelihood, độ nhạy prior | `data-tab` seq\|prior |
| `collinear-explainer` | Đa cộng tuyến: VIF, posterior dải chéo | |
| `biasvar-explainer` | Bias–variance theo bậc đa thức | `data-tau` 100\|3\|0.5 |
| `horseshoe-explainer` | Gaussian vs Laplace vs Horseshoe | |
| `overdisp-explainer` | Poisson vs Negative Binomial, PPC | `data-data` nb\|poisson |
| `glmppc-explainer` | PPC cho logistic và Poisson | `data-tab` logistic\|poisson |

## Cấu trúc

```
explainers/
  build.mjs  vite.config.js  entries.mjs  check-pages.mjs
  src/shared/   Stepper.svelte  Plot.svelte  mount.js  ui.css  theme.css  i18n.js
  src/bayes/    *Explainer.svelte  (UI)   *.js  (số học thuần, có test)   main.js
  tests/        bayes1.test.js  bayes2.test.js  bayes3.test.js  bayes4.test.js
```

Thêm explainer mới: viết module số học + test trong `src/bayes/`, viết component `.svelte`, đăng ký trong `main.js`,
`npm run build`, rồi chèn block vào bài.
