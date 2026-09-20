"""The school entry point covers both apps without losing language or old links."""

import re
from pathlib import Path

from test_website_navigation import Page

ROOT = Path(__file__).resolve().parents[1]


def test_reference_links_use_dark_text_on_light_cards() -> None:
    css = (ROOT / "website/styles.css").read_text(encoding="utf-8")
    rule = re.search(r"\.feature-card \.doc-links a\s*\{([^}]+)\}", css)
    assert rule is not None
    assert "color: var(--ink);" in rule[1]
    assert "border-color: var(--line);" in rule[1]
    assert ".doc-links a:focus-visible" in css


def test_shared_school_page_keeps_both_app_anchors_and_one_checklist() -> None:
    page = Page(ROOT / "website/schools/index.html")
    ids = [attrs.get("id") for _, attrs in page.elements]
    for anchor in ("dictation", "read-aloud", "assessment", "school-guide"):
        assert ids.count(anchor) == 1
    source = (ROOT / "website/schools/index.html").read_text(encoding="utf-8")
    assert "a dedicated school approval pack is not yet complete" not in source
    assert "Separate app. Separate assessment." not in source
    assert "temporary audio" in source
    assert "microphone" in source
    assert "examination use" in source


def test_shared_guide_link_follows_the_existing_language_switch() -> None:
    page = Page(ROOT / "website/schools/index.html")
    links = [
        attrs
        for tag, attrs in page.elements
        if tag == "a" and "SCHOOL_GUIDE" in (attrs.get("href") or "")
    ]
    assert len(links) == 1
    link = links[0]
    assert link["href"] == link["data-href-nb"]
    assert link["data-href-nb"].endswith("/SCHOOL_GUIDE_NB.md")
    assert link["data-href-en"].endswith("/SCHOOL_GUIDE.md")


def test_both_guides_have_matching_checklists_and_valid_local_links() -> None:
    guides = [
        ROOT / "docs" / name for name in ("SCHOOL_GUIDE.md", "SCHOOL_GUIDE_NB.md")
    ]
    contents = [path.read_text(encoding="utf-8") for path in guides]
    assert contents[0].count("- [ ]") == contents[1].count("- [ ]") == 10
    for path, source in zip(guides, contents, strict=True):
        for name in ("Snakk", "Lytt", "OCR", "Ctrl + Alt + Space"):
            assert name in source
        for link in re.findall(r"\]\(([^)]+)\)", source):
            if not link.startswith("https://"):
                assert (path.parent / link).is_file(), (path, link)
