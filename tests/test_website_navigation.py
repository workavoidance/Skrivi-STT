from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "website"


class Page(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.elements: list[tuple[str, dict[str, str | None]]] = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.elements.append((tag, dict(attrs)))


def test_internal_page_links_assets_and_anchors_resolve() -> None:
    pages = {path.resolve(): Page(path) for path in ROOT.rglob("*.html")}
    for path, page in pages.items():
        for tag, attrs in page.elements:
            for key in ("href", "src"):
                link = attrs.get(key)
                if not link or urlsplit(link).scheme or link.startswith("//"):
                    continue
                url = urlsplit(link)
                target = (
                    (path.parent / unquote(url.path)).resolve() if url.path else path
                )
                if target.is_dir():
                    target /= "index.html"
                assert target.is_file(), (path, tag, link)
                if url.fragment and target in pages:
                    ids = {a.get("id") for _, a in pages[target].elements}
                    assert unquote(url.fragment) in ids, (path, link)


def test_pages_share_bilingual_navigation_and_norwegian_default() -> None:
    for path in ROOT.rglob("*.html"):
        page = Page(path)
        assert ("html", {"lang": "nb"}) in page.elements
        for _, attrs in page.elements:
            for nb, en in (
                ("data-nb", "data-en"),
                ("data-href-nb", "data-href-en"),
                ("data-aria-nb", "data-aria-en"),
                ("data-alt-nb", "data-alt-en"),
            ):
                assert bool(attrs.get(nb)) == bool(attrs.get(en)), (path, attrs)
        sources = [a.get("src", "") for tag, a in page.elements if tag == "script"]
        assert any(source.endswith("/script.js") for source in sources)


def test_read_aloud_is_not_presented_as_released() -> None:
    page = (ROOT / "read-aloud" / "index.html").read_text(encoding="utf-8")
    assert "Under utvikling" in page
    assert "In development" in page
    assert "apps.microsoft.com" not in page
    assert ".exe" not in page
