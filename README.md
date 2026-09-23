# Talks and lectures

Research presentations and teaching material by **Roi Naveiro**.

**[Browse the talks](https://roinaveiro.github.io/talks/)** · [Personal website](https://roinaveiro.github.io/)

Latest: **[Secure Machine Learning: a Bayesian perspective](https://roinaveiro.github.io/talks/cristalera/secure-ml.html)**, AIHUB CSIC Summer School, September 2026. The [technical appendix](https://roinaveiro.github.io/talks/cristalera/secure-ml-appendix.html) accompanies the lecture.

## Repository layout

```text
site/                   Landing-page template, styles, search, and talk catalog
scripts/                Catalog build and publication checks
docs/                   GitHub Pages website, published from main
  index.html            Generated talks catalog
  assets/               Catalog styles and JavaScript
  cristalera/           Secure Machine Learning source, assets, slides, and notes
  <talk>/               Earlier talks and their required resources
```

Talks keep their existing folders so shared URLs continue to work. The website groups related versions instead of listing every file. Earlier presentations retain their original Quarto or xaringan format; rebuilding the catalog does not rebuild them.

Local manuscript drafts, backups, Python environments, execution logs, duplicate exports, and old PDF snapshots are not part of a new talk's publication. The root `.gitignore` keeps this working material out of Git.

## Update the catalog

Edit `site/catalog.json` to add a talk or change its description and links. Keep links relative to `docs/`. Then run:

```bash
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 scripts/check_site.py
```

Only Python 3.9 or later is needed. The generated page works without JavaScript; JavaScript adds topic filters and search. No external fonts, analytics, frameworks, or build services are required.

## Edit Secure Machine Learning

The main source is `docs/cristalera/secure-ml.qmd`. Its appendix, styling, figures, and notes live in the same folder. With Quarto installed:

```bash
cd docs/cristalera
quarto render
```

Both HTML decks embed their presentation resources. Citations live in speaker notes, and the main deck retains its final bibliography. The reference filter preserves manuscript titles while omitting links to unpublished local drafts. See the [talk README](docs/cristalera/README.md) for editing and presenting instructions.

## Publish

GitHub Pages serves `docs/` from the `main` branch. After rendering any changed talk and rebuilding the catalog, review and commit the intended files, then push `main`. Pages publishes the update automatically. The repository check verifies the catalog and the current Secure Machine Learning decks.

Do not add the whole working directory without reviewing it. New talks should include only the presentation, its editable sources and required resources; keep draft papers and computational environments local.
