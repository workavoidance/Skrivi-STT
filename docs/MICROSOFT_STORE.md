# Microsoft Store distribution

Skrivi Snakk's Microsoft Store product identity is:

- Store ID: `9P42NBXD8W36`
- Package name: `Skrivi.Skrivi`
- Publisher: `CN=EF3D997F-87B2-4AD0-B65B-877EE1632E65`
- Publisher display name: `Skrivi`

The Store package is an additional distribution channel. The existing Inno
Setup installer and portable archive remain the primary GitHub release assets.
A failure or delay in Store packaging or certification must not block their
publication.

## Submit the current test release

1. Let the release workflow build the unsigned `.msix` artifact.
2. Download `Skrivi-v0.3.0-windows-x64.msix` and its `.sha256` from the
   [0.3.0 release](https://github.com/workavoidance/Skrivi-STT/releases/tag/v0.3.0).
   The `Skrivi-<version>-Microsoft-Store` workflow artifact is also available.
3. In Partner Center, open Skrivi Snakk and start an MSIX submission.
4. Complete pricing, availability, properties, age ratings, Store listings and
   submission options.
5. Upload the `.msix` and submit it for
   certification.

Microsoft signs the package after certification. The unsigned `.msix` is a
maintainer submission asset, not the installer offered on the public website.
Do not publish the unsigned package as a normal PC installation download.
Use the signed `.exe` to try the GitHub test release on a PC. The Store version
advances independently of GitHub publication and may still be older.

Before each public submission, verify microphone capture, global push-to-talk,
text insertion, model download, settings persistence and automatic startup from
an installed Store package. The Store package declares a `windows.startupTask`
and Skrivi Snakk controls it through Windows' packaged `StartupTask` API. Users and
organisation policies remain able to control Skrivi Snakk through Windows Startup
settings. Also avoid installing the Store and website editions together; they
are separate installations and may keep separate application data.

After the first submission is accepted, automate future free-app updates with
the Microsoft Store Developer CLI. Store credentials belong in GitHub Actions
secrets and must never be committed to this repository.

The public Store page will use:

`https://apps.microsoft.com/detail/9P42NBXD8W36`

## Automated updates

The `Microsoft Store submission` workflow uses these repository Actions secrets:
`AZURE_AD_TENANT_ID`, `AZURE_AD_APPLICATION_CLIENT_ID`,
`AZURE_AD_APPLICATION_SECRET`, and `SELLER_ID`. The Entra application must have
Manager (Windows) access in Partner Center. Save the secret expiry date and
replace the GitHub secret before it expires. Never include keys in screenshots.

Run `Microsoft Store submission` manually to check authentication, package
identity and whether a published or pending submission exists. This manual run
is read-only. It checks that SELLER_ID is present; it does not independently
validate that value with the MSIX API.

After a publishing run of `Windows release` succeeds, the reusable workflow
submits that run's MSIX for certification using Microsoft's CLI. Non-publishing
builds do not submit. Only main can submit. Store submissions are serialized,
and Store failures do not retract the signed GitHub release.

The first submission must be completed in Partner Center. Automatic updates
require a published submission and stop if there is any pending draft or review,
because the CLI would otherwise replace a draft. Resolve existing submissions in
Partner Center before the next release. The CLI preserves the previously
published listing and delivery settings; certification and final publication
remain controlled by Microsoft and those settings. A successful upload does not
mean certification has finished.

References:
- https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/github-actions
- https://learn.microsoft.com/en-us/windows/apps/publish/msstore-dev-cli/commands
