# Model Loop Lab: Enhancements and Bugs

The working list for this project, maintained by Claude.

**How the work is organized.** The four notebooks are the heart of the project. Each one takes many enhancements to finish. An enhancement is any single task, large or small: importing data, writing a function, adding a chart, changing a color. Some enhancements belong to a notebook. Others belong to the site or the project as a whole.

**Picking the next item:** the highest-priority open bug first, then the highest-priority open enhancement, favoring the notebook currently in progress.

**Priority:** P1 needed now · P2 needed to finish its notebook or milestone · P3 nice to have
**Status:** Open · In progress · Done · Won't do
**Testing rule:** any Python written for an enhancement gets pytest tests in `tests/`, and `python -m pytest` must pass before it is marked Done.

## Notebooks

| # | Notebook | What it answers | Milestone | Status |
|---|---|---|---|---|
| 01 | `01_data_and_baseline.ipynb` | What does the data look like, and how good is a plain model? | M1 | In progress |
| 02 | `02_evolution_loop.ipynb` | Can a program find better models on its own? | M2 | Planned |
| 03 | `03_search_race.ipynb` | Does the loop beat Optuna and random guessing? | M3 | Planned |
| 04 | `04_model_collapse.ipynb` | What happens when models learn only from other models? | M4 | Planned |

Every notebook follows the same layout for each step: what we're looking for, the code, its result, then how to read it, what it means, and what's next and why.

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

## Enhancements: open

### Notebook 01: Data and baseline

| ID | Enhancement | Priority | Status |
|---|---|---|---|
| E-024 | Run notebook 01 in PyCharm on the real data and write the "What it means" notes from the actual numbers | P1 | Open |

### Notebook 02: Evolution loop

| ID | Enhancement | Priority | Status |
|---|---|---|---|
| E-009 | `src/evolve.py`: population of 10, keep top 3, mutate, 20 generations, with pytest tests | P2 | Open |
| E-010 | Run the loop in notebook 02 and write `results/web/evolution.json` | P2 | Open |
| E-025 | Generation chart and table in notebook 02, with the four reading notes | P2 | Open |

### Notebook 03: Search race

| ID | Enhancement | Priority | Status |
|---|---|---|---|
| E-011 | Race the loop, Optuna and random guessing on the same 200-model budget; write `results/web/search_compare.json` | P2 | Open |
| E-012 | Write the "What it means" notes on The loop works page from the real results | P2 | Open |

### Notebook 04: Model collapse

| ID | Enhancement | Priority | Status |
|---|---|---|---|
| E-013 | `src/collapse.py`: Gaussian mixture generator, 10 generations, with pytest tests | P2 | Open |
| E-014 | Run the collapse loop in notebook 04, write `results/web/collapse.json`, and the "What it means" notes on Where loops break | P2 | Open |

### Site and project

| ID | Enhancement | Milestone | Priority | Status |
|---|---|---|---|---|
| E-015 | Publish the notebooks as web pages under `site/notebooks/` with back bar and noindex tag | M5 | P2 | Open |
| E-021 | Change the portfolio card status from "In progress" once real results replace the sample data | M3 | P2 | Open |
| E-018 | Live "run more generations" demo on the VPS | M7 | P3 | Open |
| E-019 | Host the Plotly script and fonts locally instead of from cdnjs and Google Fonts | — | P3 | Open |

## Enhancements: done

| ID | Enhancement | Belongs to | Done |
|---|---|---|---|
| E-001 | Site pages: overview, The loop works, Where loops break, Notebooks | Site | 2026-11-15 |
| E-002 | Portfolio rules on every page: back bar, favicons, noindex, absolute `/scott/` paths | Site | 2026-11-15 |
| E-003 | Plotly charts drawn from `site/data/*.json`, with a "Sample data" notice that turns off when real results arrive | Site | 2026-11-15 |
| E-004 | `scripts/build_site.py` publishes to `SITE_DIR` and overlays `results/web/*.json`, with pytest tests | Site | 2026-11-15 |
| E-005 | Light and dark mode, and phone-width layout | Site | 2026-11-15 |
| E-006 | First commit and push of the project repo (`master` branch, `.idea` untracked) | Project | 2026-11-15 |
| E-016 | Portfolio screenshot `model-loop-lab.png` (made by the portfolio session) | Site | 2026-11-15 |
| E-017 | Portfolio card added, status "In progress" (made by the portfolio session) | Site | 2026-11-15 |
| E-020 | Sample-data version published to schirko.com/scott/model-loop-lab | Site | 2026-11-15 |
| E-008 | `src/evaluate.py`: shared loading, 20,000-plot stratified sample, train/test split, accuracy scoring; 10 pytest tests | Notebook 01 | 2026-11-15 |
| E-023 | Notebook 01 Step 10 saves `results/web/baseline.json`; overview and The loop works read it; sample tag on the overview names only figures still on sample data; `src/web_results.py` with 4 tests | Notebook 01 | 2026-11-16 |
| E-007 | Notebook 01 Steps 7 to 9: baseline score with training-score comparison, per-cover-type table, confusion chart; `fit_predict()` and `cover_type_report()` added to `src/evaluate.py` with 2 tests | Notebook 01 | 2026-11-16 |
| E-022 | Notebook 01 started: setup, full dataset, sample, split, guessing versus a tree, repeatability check | Notebook 01 | 2026-11-16 |

## Change history

| Date | Change |
|---|---|
| 2026-11-16 | E-023 done. Test suite now 33 tests. |
| 2026-11-16 | E-007 done. Test suite now 28 tests. |
| 2026-11-16 | Reorganized around four notebooks. Enhancements are now the tasks that build each notebook and the site, grouped by notebook. Notebook 01 renamed `01_data_and_baseline.ipynb`; the baseline (E-007) goes into it instead of a separate notebook. Added E-022 to E-025. |
| 2026-11-15 | E-008 done. Test suite now 26 tests. |
| 2026-11-15 | Site published with sample data; portfolio card and screenshot added by the portfolio session (E-016, E-017, E-020). Added E-021. |
| 2026-11-15 | E-006 done (first push). Publishing to the Schirko repo split out as E-020. |
| 2026-11-15 | Created with the M0 front end. B-001 to B-004 found and fixed during the first render check. |
