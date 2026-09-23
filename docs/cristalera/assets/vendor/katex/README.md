# KaTeX 0.13.11

This folder vendors KaTeX 0.13.11 for reproducible offline rendering of the
slides. Quarto embeds this local copy directly into each output HTML file.

- Package: `katex@0.13.11`
- Source: <https://registry.npmjs.org/katex/-/katex-0.13.11.tgz>
- Project: <https://github.com/KaTeX/KaTeX>
- License: MIT; see the unchanged `LICENSE` file.
- Contents: unchanged `dist/katex.min.js`, `dist/katex.min.css`, all 60 files in
  `dist/fonts/`, and the package license. `provenance.json` records the tarball
  and individual file SHA-256 checksums.

The shared `_quarto.yml` configuration uses:

```yaml
format:
  revealjs:
    html-math-method:
      method: katex
      url: assets/vendor/katex/
    embed-resources: true
    self-contained-math: true
```

Run `quarto render` from the project root. Quarto embeds the JavaScript, CSS,
and font resources itself; no postprocessing step is needed. The output HTML
does not need this vendor directory or a network connection to display maths.
Keep this folder in the editable project for future renders and attribution.
