## 1. Analysis
- [x] 1.1 Audit active references to Chapter 9 across lesson markdown, chapter indexes, sidebar navigation, and tracked generated lab HTML exports.
- [x] 1.2 Confirm post-removal learner flow from Chapter 8 so active pages do not point into retired Chapter 9 URLs.

## 2. Content And Navigation Updates
- [x] 2.1 Remove `contents/vi/chapter09/` from the active published course tree.
- [x] 2.2 Update `_includes/sidebar.html` and chapter-level navigation so Chapter 9 no longer appears.
- [x] 2.3 Revise Chapter 8 closing/next-step copy so it no longer links to `/vi/chapter09/` and instead ends cleanly or points to the intended active continuation.
- [x] 2.4 Update tracked practice-material references if any still link to retired Chapter 9 pages.

## 3. Validation
- [x] 3.1 Run search checks (for example with `rg`) to confirm active course content and tracked generated outputs no longer contain `/vi/chapter09/` links.
- [x] 3.2 Run `bundle exec jekyll build --verbose` and fix any rendering or broken-link regressions caused by Chapter 9 retirement.
- [x] 3.3 Run `openspec validate remove-chapter-9 --strict`.
