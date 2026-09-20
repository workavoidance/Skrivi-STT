# Skrivi Snakk 0.3.1 — local acceptance build

Prepared for user testing before publication. The shared Skrivi interface adds
consistent settings, immediate preference saving, shortcut controls, model
maintenance, manual update checks and error recovery. Existing data and internal
installation identities remain unchanged.

The signed PC installer is `Skrivi-Snakk-0.3.1-windows-x64-setup.exe`.
The separate `Skrivi-Snakk-0.3.1-windows-x64.msix` is for Store submission.
Do not publish, change website links or submit to Microsoft until the user has
tested the installers and explicitly approved continuing.

Signed build passed: https://github.com/workavoidance/Skrivi-STT/actions/runs/35525721348
Built source: `e461f1f98e597b4d8953b00007def1b225690d0e`.
215 tests passed; signed installation, shortcut migration, product metadata,
reinstall, startup cleanup and data-preserving uninstall passed on the runner.
The local installer signature and timestamp are valid. SHA-256:
`28f7652730a1c99f9143e112c71b5678e41828e0032e54385fac11a21bf36c27`.
Store identity remains `Skrivi.Skrivi`, package version `1.3.11.0`.

Local files: `../output/test-builds/snakk-0.3.1/` and `../output/test-builds/snakk-store/`.
Shared acceptance checklist and verification records are in `../output/test-builds/`.
The initial run 35525292614 failed on a relative metadata path; it is superseded.
No GitHub release, website update, local installation or Store submission performed.
