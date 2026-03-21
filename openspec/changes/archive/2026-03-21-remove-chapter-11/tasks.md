## 1. Analysis
- [x] 1.1 Audit every active reference to Chapter 11 across lesson content, chapter indexes, sidebar navigation, labs, and generated HTML exports.
- [x] 1.2 Confirm the post-removal learner flow from Chapter 10 to the remaining lab track in Chapter 12.

## 2. Content And Navigation Updates
- [x] 2.1 Remove `contents/vi/chapter11/` from the published curriculum tree.
- [x] 2.2 Update `_includes/sidebar.html` and any chapter-level navigation so Chapter 11 no longer appears in global or local navigation.
- [x] 2.3 Revise Chapter 10 closing copy so it no longer points to Chapter 11 and instead ends the lecture track cleanly or points learners to Chapter 12 labs.
- [x] 2.4 Update lesson/lab references that still link to Chapter 11 content.
- [x] 2.5 Regenerate tracked lab HTML exports if their notebook sources changed.

## 3. Validation
- [x] 3.1 Run `rg` to confirm no active course pages or tracked generated lab outputs still link to `/chapter11/`.
- [x] 3.2 Run `bundle exec jekyll build --verbose` and fix any rendering or broken-link regressions caused by the retirement.
- [x] 3.3 Run `openspec validate remove-chapter-11 --strict`.
