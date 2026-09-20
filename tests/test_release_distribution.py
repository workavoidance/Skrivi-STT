from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAG = "v0.3.2"
SITE_TAG = "v0.3.0"
INSTALLER = f"Skrivi-{SITE_TAG}-windows-x64-setup.exe"
PUBLIC_INSTALLER_URL = (
    f"https://github.com/workavoidance/Skrivi-STT/releases/download/{SITE_TAG}/"
    f"Skrivi-{SITE_TAG}-windows-x64-setup.exe"
)
STORE_URL = "https://apps.microsoft.com/detail/9P42NBXD8W36"


def test_alpha_version_is_consistent_across_package_and_installer() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package = (ROOT / "src" / "whisper_dictate" / "__init__.py").read_text(
        encoding="utf-8"
    )
    installer = (ROOT / "build_installer.ps1").read_text(encoding="utf-8")
    preview = (ROOT / ".github" / "workflows" / "preview.yml").read_text(
        encoding="utf-8"
    )

    assert project["project"]["version"] == "0.3.2"
    assert '__version__ = "0.3.2"' in package
    assert '[string]$Version = "0.3.2"' in installer
    assert '-Version "0.3.2-pr.${{ github.event.pull_request.number }}"' in (preview)


def test_website_offers_the_accepted_store_release_and_current_installer() -> None:
    website = (ROOT / "website" / "dictation" / "index.html").read_text(
        encoding="utf-8"
    )
    testing = (ROOT / "website" / "alpha" / "index.html").read_text(encoding="utf-8")

    assert website.count(PUBLIC_INSTALLER_URL) == 2
    assert testing.count(PUBLIC_INSTALLER_URL) == 2
    assert "same version from GitHub" not in website
    assert "Microsoft Store may still show an older version" in website
    assert website.count(STORE_URL) == 2
    assert testing.count(STORE_URL) == 2


def test_readme_links_directly_to_current_alpha_installer() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    release_url = f"https://github.com/workavoidance/Skrivi-STT/releases/download/{SITE_TAG}/{INSTALLER}"

    assert release_url in readme
    assert "install the standard 64-bit Python" not in readme.casefold()


def test_tagged_release_uses_curated_notes_and_marks_alpha_as_prerelease() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(
        encoding="utf-8"
    )
    notes = ROOT / "docs" / "releases" / f"{TAG}.md"

    assert '"--notes-file", $notesFile' in workflow
    assert '$prereleaseArgs = @("--prerelease")' in workflow
    assert '--target "${{ github.sha }}"' in workflow
    assert "gh release upload $tag @assets --clobber" in workflow
    assert '$ErrorActionPreference = "SilentlyContinue"' in workflow
    assert '".github/workflows/release.yml"' not in workflow
    assert notes.is_file()
    assert "signed" in notes.read_text(encoding="utf-8")
    assert '$tag.StartsWith("v0.")' in workflow
    assert "publish-store-package:" in workflow


def test_release_version_file_matches_the_public_download() -> None:
    version = (ROOT / "release" / "VERSION").read_text(encoding="utf-8").strip()

    assert version == TAG
