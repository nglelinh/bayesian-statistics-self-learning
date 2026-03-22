## Context
The repository builds a static Jekyll site and deploys it to GitHub Pages. GitHub Pages serves already-built files and does not provide a runtime hook for HTTP Basic Auth. Any protection implemented only in this repository must therefore run in the generated static site.

## Goals
- Add an optional site-wide access gate controlled from `_config.yml`
- Keep the implementation minimal and compatible with the current Jekyll/GitHub Pages deployment flow
- Avoid emitting the plaintext configured password into generated HTML
- Prevent visible content flash before the gate is evaluated

## Non-Goals
- Providing true server-enforced HTTP Basic Auth
- Hiding page source or built HTML from a determined visitor
- Adding an external identity provider or backend session service

## Decision
Use a static client-side access gate injected into the shared layout. The site configuration will store the fixed credentials, but a build-time plugin will convert the configured password into a SHA-256 digest and expose only the digest plus non-sensitive metadata to templates. Browser-side JavaScript will prompt for credentials, compare the submitted digest through Web Crypto, and unlock the page for the current browser session.

## Consequences
- This provides a lightweight deterrent suitable for low-sensitivity staging or classroom sharing
- This does not provide real HTTP Basic Auth and should not be treated as strong protection for sensitive material
- If true HTTP Basic Auth is required, deployment must move behind a host or proxy that supports server-side auth
