# Skrivi website

This folder contains the public Skrivi website at https://skrivi.no.

## Products and routes

- `/`: shared brand and two-app chooser.
- `/dictation/`: Skrivi Diktering / Skrivi Dictation, the existing Windows app.
  Its Store listing and installed name remain Skrivi. Downloads, release notes
  and technical details belong here.
- `/read-aloud/`: Skrivi Opplesing / Skrivi Read Aloud, a separate Windows x64 reader.
  Links to the full 0.2.1 setup executable in `workavoidance/Skrivi-TTS`, not the
  update-only ZIP or Dictation installer. Installed name: Skrivi TTS.
- `/schools/`: shared principles, current Dictation documents and a clearly
  labelled Read Aloud data flow and its own technical documentation. The existing
  bilingual school pack covers Dictation only; Read Aloud's technical docs are English.
- `/help/`: app-specific installation, feedback and release-note links.
- `/alpha/` and `/feedback/`: existing Dictation guides and feedback, kept at
  their original URLs. The home anchors `#download`, `#how`, `#schools` and
  `#technical` still lead to relevant content.

All pages are Norwegian by default. The shared script carries an explicit
English choice in internal links as `?lang=en`, including anchors. It also
switches document destinations, titles, descriptions and accessible labels.
No cookies or browser storage are used for language selection.

Read Aloud has no Microsoft Store listing yet. Keep its download, source and
feedback links separate from Dictation. The EXE bundles the published 0.2.1 app,
engines and voices; no cloud service or background update check is introduced.
Verify the exact release asset before updating version-pinned download links.

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
