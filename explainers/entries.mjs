// Danh sách bundle: key = mode của Vite, cũng là tên file đầu ra.
// Mỗi trang chỉ nạp MỘT bundle Svelte nên tất cả explainer Bayes nằm chung một bundle.
export const ENTRIES = {
  'bayes-explainer': { entry: 'src/bayes/main.js', name: 'BayesExplainer' }
};
