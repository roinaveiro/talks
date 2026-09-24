# Secure Machine Learning

A three-hour, English-language Quarto lecture for a mixed postdoctoral audience.

## Present

Open **[secure-ml.html](secure-ml.html)** in a browser. Images, styles, scripts, fonts, and mathematics are embedded for presentation without a network connection.

- Arrow keys or Space: advance, including progressive reveals.
- **S**: open presenter view with speaker notes and a timer.
- **O** or Escape: slide overview.
- **F**: full screen.
- Use the slide menu to jump to a section.

The main deck ends with the AIHUB template closing slide. Additional technical material is in **[secure-ml-appendix.html](secure-ml-appendix.html)**, linked from the reading slide.

The HTML decks are the current version. Export fresh PDFs for sharing or printing after edits; older PDF snapshots may exist locally and are not included in the website.

## Edit and render with Quarto

Install [Quarto](https://quarto.org/docs/get-started/), then open a terminal in this folder. Quarto is the only software needed to render the slides; the project includes all figures, fonts, and mathematics libraries. Tested with Quarto 1.10.18.

Preview the main deck while editing; save `secure-ml.qmd` to refresh the browser:

```bash
quarto preview secure-ml.qmd
```

Render both the main deck and appendix:

```bash
quarto render
```

Or render either deck separately:

```bash
quarto render secure-ml.qmd
quarto render secure-ml-appendix.qmd
```

The results are `secure-ml.html` and `secure-ml-appendix.html` in this folder. Each embeds its images, styles, fonts, scripts, and mathematics. Keep both HTML files together for the links between decks to work. The optional `bash scripts/render.sh` command is just a wrapper around `quarto render`.

### Where to edit

| File | What to change |
|---|---|
| [secure-ml.qmd](secure-ml.qmd) | All main slides, their order, and speaker notes, including the opening, break, and closing |
| [secure-ml-appendix.qmd](secure-ml-appendix.qmd) | All technical appendix slides and their notes |
| [_quarto.yml](_quarto.yml) | Shared Quarto settings for both decks |
| [deck.css](deck.css) | Fonts, colors, spacing, and slide layouts |
| [deck.js](deck.js) | Section labels; hide numbering and navigation on the opening and closing slides |
| [assets/](assets/) | Figures used in the slides |

Each deck has one `.qmd` source containing its complete slide content. Edit `secure-ml.qmd` for the main talk; use `quarto preview secure-ml-appendix.qmd` when editing the appendix. Generated HTML is overwritten on the next render.

To find a section in the main source, search for its slide ID prefix:

| Search for | Section |
|---|---|
| `{#motivation-` | Opening template slide and motivation |
| `{#bayes-` | Bayesian inference and decision theory |
| `{#poison-` | Poisoning, microcredit, spatial analysis, and radon |
| `{#evasion-start` | Evasion divider, held during the ten-minute break |
| `{#evasion-` | Evasion and image attacks |
| `{#defense-` | Bayesian defenses |
| `{#sequential-` | Sequential play, EWA opponent learning, particle filtering, and the car merge |
| `{#llm-` | Extending sequential interaction to language agents |
| `{#conclusions-` | Open research questions, CUNEF vacancies, bibliography, and closing template slide |

### Add or change a slide

Each `##` heading starts a slide. Keep slide identifiers unique; use the existing prefixes to keep the source easy to navigate, for example `bayes-` or `poison-`. A minimal example:

```markdown
## What decision would you make? {#bayes-new-example}

- Describe the situation.
- Give the audience one decision to consider.

**What would an error cost?**

::: {.notes}
Your explanation, timing, and discussion prompts go here.
:::
```

Use `$p(\theta \mid D)$` for inline maths and `$$ ... $$` for display equations. Images use ordinary Quarto syntax, for example `![](assets/digit-clean.png){width=220 fig-alt="Clean handwritten digit"}`. Existing slides provide examples of columns, progressive reveals (`.fragment`), and prompts. Put citations in the slide’s speaker notes; the bibliography remains at the end of the main deck.

The first and last slides use editable text over the supplied PowerPoint artwork. Their composition is controlled by the `.template-*` rules in `deck.css`. The small `deck.js` script adds section labels and hides slide numbering and navigation on these two slides.

### PDF after editing

Render the HTML, open it in Chrome or Chromium, press **E** to enter **PDF Export Mode**, and print to **Save as PDF** with background graphics enabled and margins set to none. This preserves the Reveal slide design. The supplied PDFs are snapshots and need exporting again after edits.

### Optional maintenance tools

All assets needed for rendering are included. To regenerate teaching plots and refresh copies of original figures, see [assets/README.md](assets/README.md) and `scripts/build_figures.py`; that optional script requires Python, NumPy, SciPy, Matplotlib, and PyMuPDF, plus the original source papers/talks.

`scripts/check_deck.cjs` is an optional browser audit and PDF exporter. It requires Node.js and Playwright with Chromium. It checks image loading, mathematics, speaker notes, and slide overflow, and captures screenshots. None of these tools is needed for ordinary Quarto editing or HTML rendering.

Quarto embeds the vendored KaTeX library directly through `self-contained-math: true`. The `filters/local-references.lua` filter preserves manuscript citation text while omitting links to unpublished local drafts. There are no pre-render or post-render scripts. See the official [Quarto project guide](https://quarto.org/docs/projects/quarto-projects.html) and [Reveal format reference](https://quarto.org/docs/reference/formats/presentations/revealjs.html) for additional settings.

## Teaching material

- **[Speaker guide](speaker-guide.md):** timing, examples, exercise answers, optional cuts.
- **[Technical appendix source](secure-ml-appendix.qmd):** mathematical detours and extra results.
- **[Source notes](sources-and-design-notes.md):** paper selection, current-news attribution, limitations.
- **[Teaching structure](talk-structure.md):** current narrative and progression.

The main deck has **122 slides**, including cover, section dividers, and closing; the appendix has **11**. The session is designed for **180 minutes**; see the speaker guide for rehearsal targets. The sequence runs from agent coordination and decisions under uncertainty through Bayesian foundations, poisoning, moment targets, spatial and radon decisions, evasion, protection, Bayesian sequential play, and open questions about AI opponents. A CUNEF vacancies announcement follows the questions, and the bibliography immediately precedes the thanks slide.

## Visual style and pacing

The previous design has been restored. Language is only lightly condensed; the stories and mathematical steps have more room. Use each plot to explain what changes and why, then return to the decision.

The two graphical models in the defense section are original vector panels from the manuscript. Full explanations, source references, qualifications, and timing remain in speaker notes. Source footers are omitted from the projected slides.

Earlier versions may be kept locally in `backups/`; that working directory is excluded from the published repository.

## Scientific and editorial choices

- Each major section starts with a concrete problem. The main cases are Mexico microcredit, Meuse spatial analysis, MNIST images, Minnesota radon, and a simulated two-car lane merge.
- Newly plotted teaching examples are labelled as illustrations. Original scientific images are preserved; provenance is documented.
- The radon utility feature fails the current draft's stated finite-second-moment assumption. Its run is presented empirically, with the qualification in the notes.
- The radon slides use the original manuscript figures and their annotations. Their numerical differences from the draft prose are recorded in the notes. The Meuse story adds an explicit illustrative planning rule and distinguishes MMD deletion from the BA coordinate attack.
- The defenses paper unifies proactive and reactive **evasion** defenses. The slides preserve this scope and distinguish empirical predictive results from proposed decision protection.
- The ending uses the local sequential-play manuscript: the original interaction diagram defines the game, EWA models the opponent, a particle filter updates beliefs, and posterior samples support myopic decisions, horizon simulation, or approximate dynamic programming. Original MC, H2S, and ADP driving figures are preserved. The extension to language agents is a research direction.
- The first and last slides reuse the PowerPoint's exact network artwork and reproduce its colors, rule, stripe, and text placement. Only the opening and closing use that template composition.
