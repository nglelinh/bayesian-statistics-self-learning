## Context
The repository already implements a static browser-side password gate intended for whole-site protection. The requested behavior is narrower: only Chapter 12 content must require a new password.

## Goals / Non-Goals
- Goals:
  - Protect `contents/vi/chapter12/` routes with a dedicated password flow.
  - Preserve existing behavior for pages outside Chapter 12.
  - Keep solution compatible with static GitHub Pages hosting.
- Non-Goals:
  - Strong server-side security (not possible in pure static hosting).
  - Per-user accounts or role-based authorization.
  - Protecting downloadable assets outside the page-gate UX.

## Decisions
- Decision: Extend the existing access gate with path-scoped protection rules (e.g., configured protected path prefixes) instead of introducing a second independent gate system.
  - Why: Minimal surface-area change, reuses existing UI/JS/session patterns, and stays aligned with current architecture.
- Decision: Use a chapter-specific password hash/session key for the scoped gate.
  - Why: Avoids accidental unlock overlap with any site-wide gate credentials.

## Alternatives Considered
- Keep site-wide gate and rotate password globally.
  - Rejected because it blocks all chapters, which is broader than requested.
- Build a separate Chapter 12-only custom gate implementation.
  - Rejected to avoid duplicate logic in layout and JavaScript.

## Risks / Trade-offs
- Static gates are obfuscation/access-friction, not true backend authorization.
  - Mitigation: Keep this explicitly documented in capability requirements.
- Path matching errors could over-block or under-block pages.
  - Mitigation: Add explicit scenarios for Chapter 12 pages and non-Chapter-12 pages.

## Migration Plan
1. Add scoped-gate configuration for Chapter 12 and new password value.
2. Update plugin/layout/JS to evaluate gate enablement per page route.
3. Validate Chapter 12 routes prompt for password; other routes remain open.
4. Run full Jekyll build verification.

## Open Questions
- None for this proposal (scope confirmed: Chapter 12 only).
