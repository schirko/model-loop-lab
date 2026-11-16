# Model Loop Lab: Enhancements and Bugs

The working list for this project. Maintained by Claude. The next item to work on is the highest-priority open bug, then the highest-priority open enhancement.

**Priority:** P1 needed now · P2 needed for the milestone · P3 nice to have
**Status:** Open · In progress · Done · Won't do
**Testing rule:** any Python written for an item gets pytest tests in `tests/`, and `python -m pytest` must pass before the item is marked Done.

## Bugs

### Open

None.

### Closed

| ID | Bug | Found | Fixed | How it was fixed |
|---|---|---|---|---|
| B-001 | Chart x-axis titles drew over the bottom edge of the chart box | 2026-11-15 | 2026-11-15 | Removed padding from `.mll-chart` so Plotly's own margins fit the box |
| B-002 | Charts ran off the right edge on phone screens | 2026-11-15 | 2026-11-15 | `MLL.draw()` passes the box's exact width and height to Plotly |
| B-003 | End-of-line labels were cut off on phones | 2026-11-15 | 2026-11-15 | Labels are hidden below 520 px wide; the legend names the lines instead |
| B-004 | Two end labels overlapped on the search-race chart | 2026-11-15 | 2026-11-15 | Removed those labels; the legend carries the three names |

## Enhancements

### Open

| ID | Enhancement | Milestone | Priority | Status |
|---|---|---|---|---|
| E-006 | First commit of the project repo, and first publish into the Schirko repo | M0 | P1 | Open |
| E-007 | `notebooks/01_baseline.ipynb`: fixed 20,000-row sample, train/test split, default decision tree score | M1 | P1 | Open |
| E-008 | `src/evaluate.py` shared scoring function, with pytest tests | M1 | P1 | Open |
| E-009 | `src/evolve.py` evolution loop (population 10, keep 3, mutate, 20 generations), with pytest tests | M2 | P2 | Open |
| E-010 | `notebooks/02_evolution_loop.ipynb` writes `results/web/evolution.json` | M2 | P2 | Open |
| E-011 | `notebooks/03_optuna_compare.ipynb` writes `results/web/search_compare.json` | M3 | P2 | Open |
| E-012 | Write the "What it means" notes on The loop works page from real results | M3 | P2 | Open |
| E-013 | `src/collapse.py` model-collapse loop, with pytest tests | M4 | P2 | Open |
| E-014 | `notebooks/04_model_collapse.ipynb` writes `results/web/collapse.json`, plus the "What it means" notes | M4 | P2 | Open |
| E-015 | Export notebooks to HTML pages under `site/notebooks/` with back bar and noindex tag | M5 | P2 | Open |
| E-016 | Portfolio screenshot `model-loop-lab.png`, 16:9, into `scott/images/screenshots/` | M6 | P2 | Open |
| E-017 | Send card details to the portfolio session (name, section, status, URLs, description, tags) | M6 | P2 | Open |
| E-018 | Live "run more generations" demo on the VPS | M7 | P3 | Open |
| E-019 | Host the Plotly script and fonts locally instead of from cdnjs and Google Fonts, if the portfolio ever needs no outside requests | — | P3 | Open |

### Done

| ID | Enhancement | Milestone | Done |
|---|---|---|---|
| E-001 | Site pages: overview, The loop works, Where loops break, Notebooks | M0 | 2026-11-15 |
| E-002 | Portfolio rules on every page: back bar, favicons, noindex, absolute `/scott/` paths | M0 | 2026-11-15 |
| E-003 | Plotly charts drawn from `site/data/*.json`, with a "Sample data" notice that turns off when real results arrive | M0 | 2026-11-15 |
| E-004 | `scripts/build_site.py` publishes to `SITE_DIR` and overlays `results/web/*.json`, with pytest tests | M0 | 2026-11-15 |
| E-005 | Light and dark mode, and phone-width layout | M0 | 2026-11-15 |

## Change history

| Date | Change |
|---|---|
| 2026-11-15 | Created with the M0 front end. B-001 to B-004 found and fixed during the first render check. |
