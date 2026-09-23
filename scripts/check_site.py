#!/usr/bin/env python3
"""Check the published catalog, slide links and current lecture outputs."""
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links = []
        self.resources = []
        self.ids = set()
        self.slide_count = 0
        self.source_count = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        classes = attrs.get("class", "").split()
        if tag == "section" and "slide" in classes:
            self.slide_count += 1
        if "source" in classes:
            self.source_count += 1
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in {"script", "img", "source", "video", "audio"}:
            for key in ["src", "data-src", "poster"]:
                if attrs.get(key):
                    self.resources.append(attrs[key])
        if tag == "link" and attrs.get("href"):
            self.resources.append(attrs["href"])


def check_target(page_path, href, pages, errors):
    url = urlsplit(href)
    if url.scheme or url.netloc or href.startswith("//"):
        return
    target = (page_path.parent / unquote(url.path)).resolve() if url.path else page_path
    if not target.exists():
        errors.append(f"{page_path.relative_to(ROOT)}: missing {href}")
        return
    anchor = unquote(url.fragment).lstrip("/")
    if anchor and target.suffix == ".html":
        if target not in pages:
            pages[target] = Page(target)
        if anchor not in pages[target].ids:
            errors.append(f"{page_path.relative_to(ROOT)}: missing anchor {href}")


def main():
    subprocess.run([sys.executable, str(ROOT / "scripts/build_catalog.py"), "--check"], check=True)
    catalog = json.loads((ROOT / "site/catalog.json").read_text())
    paths = {DOCS / "index.html", DOCS / catalog["featured"]["url"], DOCS / catalog["featured"]["appendix"]}
    for group in catalog["groups"]:
        for talk in group["talks"]:
            paths.update(DOCS / item["url"] for item in talk["links"])
    pages = {p: Page(p) for p in paths}
    errors = []
    for path, page in list(pages.items()):
        for resource in page.resources:
            check_target(path, resource, pages, errors)
        if path == DOCS / "index.html" or path.parent.name == "cristalera":
            for href in page.links:
                check_target(path, href, pages, errors)
    for name in ["secure-ml", "secure-ml-appendix"]:
        path = DOCS / "cristalera" / f"{name}.html"
        qmd = path.with_suffix(".qmd").read_text()
        expected = len(re.findall(r"^## ", qmd, re.MULTILINE))
        page = pages[path]
        if page.slide_count != expected:
            errors.append(f"{name}: expected {expected} slides, found {page.slide_count}")
        if page.source_count or "{.source}" in qmd:
            errors.append(f"{name}: source footers still present")
        if any(href.startswith("context/") for href in page.links):
            errors.append(f"{name}: links to unpublished local manuscripts")
        print(f"{name}: {page.slide_count} slides; no source footers")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(paths)} pages: presentation resources and current site links resolve.")


if __name__ == "__main__":
    main()
