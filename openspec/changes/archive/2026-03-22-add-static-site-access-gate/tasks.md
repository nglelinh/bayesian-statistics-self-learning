## 1. Implementation
- [x] 1.1 Add a Jekyll plugin helper that derives a safe access-gate payload from `_config.yml`
- [x] 1.2 Add a shared access-gate UI and bootstrap data to the default layout
- [x] 1.3 Add client-side logic to verify credentials and hold the session state
- [x] 1.4 Add styling so protected pages do not flash visible content before the gate loads
- [x] 1.5 Add configuration documentation and sensible disabled-by-default defaults

## 2. Validation
- [x] 2.1 Run `bundle exec jekyll build --verbose`
- [x] 2.2 Verify the generated site includes the access gate only when enabled
