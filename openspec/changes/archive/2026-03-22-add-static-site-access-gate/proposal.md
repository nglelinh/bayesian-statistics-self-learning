## Why
The course site is currently published as a public static Jekyll site on GitHub Pages, so it cannot enforce HTTP Basic Auth at the hosting layer. The repository still needs a lightweight access gate that can be turned on from configuration without changing the content structure.

## What Changes
- Add a static-site access gate capability that can be enabled from `_config.yml`
- Hash the configured password during the Jekyll build so the raw password is not emitted into generated HTML
- Inject a client-side gate into the shared layout so learners must enter configured credentials before using the site
- Persist authenticated state in browser storage for the current browser session
- Document the limitation that this is not true server-side HTTP Basic Auth on GitHub Pages

## Impact
- Affected specs: `build-multilingual-site`, `protect-site-access`
- Affected code: `_config.yml`, `_layouts/default.html`, `_includes/head.html`, `public/js/*`, `public/css/*`, `_plugins/*`
