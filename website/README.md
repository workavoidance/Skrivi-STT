# Skrivi website

This folder contains the public Skrivi website at https://skrivi.no.

## Products and routes

- `/`: shared brand and two-app chooser.
- `/dictation/`: Skrivi Diktering / Skrivi Dictation, the existing Windows app.
  Its Store listing and installed name remain Skrivi. Downloads, release notes
  and technical details belong here.
- `/read-aloud/`: Skrivi Opplesing / Skrivi Read Aloud, in development. No public
  download, supported voice/language list or release date is promised yet.
- `/schools/`: shared principles, current Dictation documents and a clearly
  labelled planned Read Aloud data flow. Existing documents cover Dictation only.
- `/help/`: app-specific help routes and development status.
- `/alpha/` and `/feedback/`: existing Dictation guides and feedback, kept at
  their original URLs. The home anchors `#download`, `#how`, `#schools` and
  `#technical` still lead to relevant content.

All pages are Norwegian by default. The shared script carries an explicit
English choice in internal links as `?lang=en`, including anchors. It also
switches document destinations, titles, descriptions and accessible labels.
No cookies or browser storage are used for language selection.

When Read Aloud ships, give it its own Store ID, installer, release notes,
help guide, campaign IDs and reviewed privacy/data-flow documents. Do not reuse
Dictation downloads or imply its technical documentation covers both apps.

It is intentionally a simple static site: plain HTML, CSS and a small language-switching script. There is no framework, build step, database, analytics package, account system or external font dependency.

Download links remain measurable without adding browser tracking. Microsoft
Store links use `skrivi-website-home`, `skrivi-website-dictation` and
`skrivi-website-testing` campaign IDs; their results appear in Partner Center's
Acquisitions report. GitHub's
release asset API supplies the cumulative `download_count` for each conventional
installer file.

## Design direction

The site follows `docs/BRAND_GUIDELINES.md`:

- Norwegian first, English second
- warm paper-white, charcoal and strong orange
- clean, generous spacing
- product-first rather than documentation-first
- student value and school reassurance given equal weight
- local/private/free/non-generative positioning

## Preview locally

Open `index.html` directly in a browser, or serve this folder with any basic static web server.

## Publishing

`.github/workflows/pages.yml` publishes this folder with GitHub Pages when changes under `website/` are pushed to `main`.

GitHub Pages must be enabled for the repository with **GitHub Actions** selected as the Pages source. Once enabled, the site should be available at the repository's GitHub Pages URL.

The existing custom domain is `skrivi.no`, configured by `CNAME`.
