## Why
The course owner wants Chapter 12 to be password-protected with a new password, while keeping the rest of the site accessible as it is today. The current access gate is site-wide, so it cannot target only one chapter.

## What Changes
- Add a Chapter-scoped access-gate mode so protection can be applied only to `contents/vi/chapter12/**` routes.
- Support a dedicated Chapter 12 password configuration separate from the current site-wide password setting.
- Ensure users are prompted for password when opening Chapter 12 landing page or any Chapter 12 lesson URL directly.
- Keep non-Chapter-12 pages unaffected (no new password prompt outside the protected scope).

## Impact
- Affected specs: `protect-site-access`
- Affected implementation areas (expected):
  - `_config.yml`
  - `_plugins/access_gate.rb`
  - `_layouts/default.html`
  - `public/js/access-gate.js`
- User-visible outcome: Chapter 12 requires the new password before content is visible; all other chapters continue current behavior.
