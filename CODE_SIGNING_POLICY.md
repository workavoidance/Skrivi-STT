# Code signing policy

## Current status

New Windows release builds are signed using the Certum Open Source Code Signing
in the Cloud certificate issued to **Open Source Developer Jonathan Wright**.
The private signing key remains in Certum's SimplySign cloud service.
Previously published unsigned releases remain unsigned.

## Project and responsibility

- **Project:** Skrivi Snakk
- **Repository:** <https://github.com/workavoidance/Skrivi-STT>
- **Licence:** [MIT](LICENSE)
- **Maintainer and release owner:** Jonathan Wright ([@workavoidance](https://github.com/workavoidance))
- **Official releases:** <https://github.com/workavoidance/Skrivi-STT/releases>

The maintainer reviews release changes and controls access to GitHub and Certum.
GitHub account access must use multi-factor authentication. Signing runs
automatically within the release workflow; it does not require approval on a phone.

## Signed artifacts

The release workflow signs and verifies:

- the portable `dist/Skrivi.exe` before creating the ZIP;
- the installed `dist/installed/Skrivi/Skrivi.exe` before compiling the installer;
- the final `Skrivi-<version>-windows-x64-setup.exe` installer;
- the Inno Setup uninstaller, checked after a disposable-runner installation.

Third-party binaries are not re-signed as project-owned code. The ZIP is not
Authenticode-signable. The Microsoft Store package follows its separate Store
process. Pull-request previews remain unsigned and receive no signing secrets.

## Build and publication

The source-controlled `.github/workflows/release.yml` runs on GitHub-hosted
Windows runners. Release changes are reviewed through pull requests and CI.
Changing `release/VERSION` on `main` triggers a signed release. Editing workflow
code alone does not republish an existing release.

Manual runs default to a non-publishing test: they produce downloadable signed
workflow artifacts. Publication requires `main` and an explicit `publish` input,
or the version-change push trigger. The isolated signing probe is diagnostic
only and is never published as a release.

Every signed executable must pass Windows Authenticode verification, match the
configured certificate thumbprint, and contain a timestamp. Any failure stops
the build before publication. SHA-256 checksums are calculated after signing.

## Signing credentials

The repository's Actions secrets are `CERTUM_USERNAME`, `CERTUM_KEY_ID` (the
certificate SHA-1 thumbprint), and `CERTUM_OTP_URI` (the full authentication URI
from activation). The authentication URI allows unattended login and must never
appear in source, logs, screenshots, or artifacts. It is not the private signing
key. The third-party SimplySign setup action is pinned to a reviewed commit;
diagnostic screenshots are disabled. Workflow changes require particular care
because workflows with access to these secrets can use the signing identity.

## Privacy and network access

Skrivi processes speech locally. It does not send recordings or transcripts to
a cloud transcription service and does not collect usage telemetry. The app
uses the network only to download a selected speech model from its published
Hugging Face source when that model is not already installed. The download host
can observe normal connection metadata such as the requesting IP address.

The complete data-handling description is in the
[privacy policy](docs/PRIVACY.md), and the model sources and integrity checks are
documented in the [local model guide](docs/MODELS.md).

## Installation and system changes

The installer installs Skrivi for the current Windows user, creates Start menu
and uninstall entries, and does not request administrator rights. An optional
desktop shortcut can be selected during installation. Automatic start at sign-in
is off by default and can be enabled or disabled in Skrivi's settings. Skrivi
can be removed through the standard Windows installed-apps interface.

## Verification and incident response

Use Windows file properties or `Get-AuthenticodeSignature` to inspect a release
executable. Its signature should be valid and identify
**Open Source Developer Jonathan Wright**. A SHA-256 checksum confirms the file
matches the published asset but does not replace signature verification.

Report suspected misuse privately as described in [SECURITY.md](SECURITY.md).
The maintainer will stop affected workflows, preserve evidence, contact Certum,
and rotate access credentials or request certificate revocation as appropriate.
