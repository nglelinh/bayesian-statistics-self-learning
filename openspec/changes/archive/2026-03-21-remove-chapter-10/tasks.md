## 1. Analysis
- [x] 1.1 Audit all active references to Chapter 10 across lesson markdown, chapter indexes, sidebar/navigation includes, and tracked generated lab HTML exports.
- [x] 1.2 Confirm the post-removal learner flow after Chapter 9 so active pages do not point into retired Chapter 10 URLs.

## 2. Content And Navigation Updates
- [x] 2.1 Remove `contents/vi/chapter10/` from the active published course tree.
- [x] 2.2 Update global and local navigation (`_includes/sidebar.html` and chapter-level next-step links) so Chapter 10 no longer appears.
- [x] 2.3 Revise Chapter 9 closing/next-step copy so it no longer links to `/vi/chapter10/` and instead ends the sequence cleanly or points to the intended active continuation.
- [x] 2.4 Update practice-material references and tracked generated lab HTML files that still link to retired Chapter 10 pages.

## 3. Validation
- [x] 3.1 Run search checks (for example with `rg`) to confirm active course content and tracked generated lab outputs no longer contain `/vi/chapter10/` links.
- [x] 3.2 Run `bundle exec jekyll build --verbose` and fix any rendering or broken-link regressions caused by Chapter 10 retirement.
- [x] 3.3 Run `openspec validate remove-chapter-10 --strict`.
