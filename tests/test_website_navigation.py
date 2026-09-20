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


def test_read_aloud_links_to_full_setup_not_store_or_update_zip() -> None:
    installer = (
        "https://github.com/workavoidance/Skrivi-TTS/releases/download/v0.4.1/"
        "Skrivi-TTS-0.4.1-windows-x64-setup.exe"
    )
    for route in ("index.html", "read-aloud/index.html", "help/index.html"):
        page = (ROOT / route).read_text(encoding="utf-8")
        assert installer in page
        assert "No download yet" not in page
        assert "Ingen nedlasting ennå" not in page
    page = (ROOT / "read-aloud/index.html").read_text(encoding="utf-8")
    assert "apps.microsoft.com" not in page
    assert "App-Update-Windows-x64.zip" not in page
    assert "code-signed" in page
    assert "not code-signed" not in page
    assert "kodesignert" in page
    assert "Ctrl + Alt + Shift + Space" in page
    assert "Ctrl + Alt + Space" in page
    assert "https://github.com/workavoidance/Skrivi-TTS/issues" in page


def test_product_names_are_consistent_in_both_languages() -> None:
    for path in ROOT.rglob("*.html"):
        page = Page(path)
        text = path.read_text(encoding="utf-8")
        for old_name in ("Diktering", "Opplesing", "Dictation", "Read Aloud"):
            assert old_name not in text, (path, old_name)
        for name in ("Snakk", "Lytt"):
            assert any(
                tag == "a"
                and attrs.get("data-nb") == name
                and attrs.get("data-en") == name
                for tag, attrs in page.elements
            ), (path, name)
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    for name in ("Skrivi Snakk", "Skrivi Lytt"):
        assert f'data-nb="{name}" data-en="{name}"' in home
