#!/usr/bin/env python3
"""Build the talks landing page using only Python's standard library."""
import argparse
from datetime import date
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DOCS = ROOT / "docs"


def escape(value):
    return html.escape(value, quote=True)


def link(url, label, css=""):
    path = (DOCS / url).resolve()
    if not path.is_relative_to(DOCS) or not path.is_file():
        raise ValueError(f"Missing talk in catalog: {url}")
    cls = f' class="{escape(css)}"' if css else ""
    return f'<a href="{escape(url)}"{cls}>{escape(label)}</a>'


def build():
    catalog = json.loads((SITE / "catalog.json").read_text())
    featured = catalog["featured"]
    feature = f'''<section class="featured" aria-labelledby="featured-title">
      <p class="feature-label">Latest lecture · {escape(featured["date"])}</p>
      <h2 id="featured-title">{link(featured["url"], featured["title"])}</h2>
      <p class="subtitle">{escape(featured["subtitle"])}</p>
      <p class="description">{escape(featured["description"])}</p>
      <p class="featured-event">{escape(featured["event"])} · {escape(featured["details"])}</p>
      <p class="featured-links">
        {link(featured["url"], "Open slides")}
        {link(featured["appendix"], "Technical appendix")}
      </p>
    </section>'''
    sections = []
    count = 1
    ids = set()
    for group in catalog["groups"]:
        group_id = group["id"]
        if group_id in ids:
            raise ValueError(f"Duplicate topic: {group_id}")
        ids.add(group_id)
        rows = []
        for talk in group["talks"]:
            links = "\n".join(link(item["url"], item["label"]) for item in talk["links"])
            event = f'<p class="talk-event">{escape(talk["event"])}</p>' if talk.get("event") else ""
            rows.append(f'''<article class="talk-row">
              <div><h4>{link(talk["links"][0]["url"], talk["title"])}</h4>
                <p class="talk-description">{escape(talk["description"])}</p>{event}</div>
              <div class="talk-links">{links}</div>
            </article>''')
            count += 1
        sections.append(f'''<section class="talk-group" data-topic="{escape(group_id)}" aria-labelledby="topic-{escape(group_id)}">
          <h3 id="topic-{escape(group_id)}">{escape(group["title"])}</h3>
          {chr(10).join(rows)}
        </section>''')
    page = (SITE / "index.html").read_text().replace("{{FEATURED}}", feature).replace("{{CATALOG}}", "\n".join(sections)).replace("{{TALK_COUNT}}", str(count)).replace("{{YEAR}}", str(date.today().year))
    return {
        DOCS / "index.html": page,
        DOCS / "assets/catalog.css": (SITE / "catalog.css").read_text(),
        DOCS / "assets/catalog.js": (SITE / "catalog.js").read_text(),
        DOCS / ".nojekyll": "",
    }, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check that catalog outputs match their sources without writing files.")
    args = parser.parse_args()
    outputs, count = build()
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f"Outdated catalog output: {path.relative_to(ROOT)}. Run python3 scripts/build_catalog.py")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print(f"{'Checked' if args.check else 'Built'} catalog: {count} talks and lectures; all slide links exist.")


if __name__ == "__main__":
    main()
