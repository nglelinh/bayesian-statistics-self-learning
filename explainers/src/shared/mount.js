import { mount } from 'svelte';

export function attr(el, name, fallback = '') {
  const v = el.getAttribute('data-' + name);
  return v === null || v === '' ? fallback : v;
}

/** Gắn Component vào mọi phần tử khớp selector (mỗi phần tử một lần). */
export function mountAll(selector, Component, readProps = () => ({})) {
  const run = () => {
    document.querySelectorAll(selector).forEach((el) => {
      if (el.dataset.mounted === '1') return;
      el.dataset.mounted = '1';
      mount(Component, { target: el, props: readProps(el) });
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
}
