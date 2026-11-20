/** Chọn chuỗi theo ngôn ngữ trang: tr(lang, 'tiếng Việt', 'English'). */
export const norm = (lang) => (lang === 'en' ? 'en' : 'vi');
export const tr = (lang, vi, en) => (lang === 'en' ? en : vi);
export const fmt = (x, d = 3) => (Number.isFinite(x) ? x.toFixed(d) : '—');
