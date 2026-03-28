## 1. Configuration and scope setup
- [ ] 1.1 Add Chapter 12 scoped access-gate configuration in `_config.yml` with a dedicated password field and protected path prefix for `contents/vi/chapter12/` routes.
- [ ] 1.2 Keep existing gate defaults backward-compatible for projects that still use site-wide mode.

## 2. Access-gate runtime updates
- [ ] 2.1 Update `_plugins/access_gate.rb` to emit route-aware gate payload data (enabled state, hash, session key, protected-path rules) without exposing plaintext passwords.
- [ ] 2.2 Update `_layouts/default.html` to render the gate only when the current page route matches protected Chapter 12 scope.
- [ ] 2.3 Update `public/js/access-gate.js` to enforce session-scoped unlock for the Chapter 12 gate and preserve current behavior on unprotected pages.

## 3. Verification
- [ ] 3.1 Verify Chapter 12 landing page and Chapter 12 lesson URLs are locked until correct password is entered.
- [ ] 3.2 Verify non-Chapter-12 pages render without password prompt.
- [ ] 3.3 Run `bundle exec jekyll build --verbose` and resolve any build/render regressions.
