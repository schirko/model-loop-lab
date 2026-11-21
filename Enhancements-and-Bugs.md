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
| 01 | `01_data_and_baseline.ipynb` | What does the data look like, and how good is a plain model? | M1 | Done: baseline 77.2% |
| 02 | `02_evolution_loop.ipynb` | Can a program find better models on its own? | M2 | In progress: Steps 1–4 written |
| 03 | `03_search_race.ipynb` | Does the loop beat Optuna and random guessing? | M3 | Planned |
| 04 | `04_model_collapse.ipynb` | What happens when models learn only from other models? | M4 | Planned |

Every notebook follows the same layout for each step: what we're looking for, the code, its result, then how to read it, what it means, and what's next and why.

## Bugs

### Open

None.

### Closed

| ID | Bug | Found | Fixed | How it was fixed |
|---|---|---|---|---|
| B-006 | Commands typed as `python` ran the Life Expectancy project's environment, not this one: packages went to the wrong place and `jupyter` could not find a kernel | 2026-11-16 | 2026-11-16 | Every command now calls `.venv\Scripts\python` directly; the guide says so |
| B-007 | Some of Claude's file updates were undone on the PC (PyCharm saved its older open copies over them) | 2026-11-16 | 2026-11-16 | Files rewritten and sizes checked; when PyCharm reports a file changed on disk, choose Load File System Changes |
| B-005 | Notebook 01 Step 8 stopped with "The '.style' accessor requires jinja2" | 2026-11-16 | 2026-11-16 | Formatted the recall and precision columns as text instead of using pandas `.style`, so no extra package is needed |
| B-001 | Chart x-axis titles drew over the bottom edge of the chart box | 2026-11-15 | 2026-11-15 | Removed padding from `.mll-chart` so Plotly's own margins fit the box |
| B-002 | Charts ran off the right edge on phone screens | 2026-11-15 | 2026-11-15 | `MLL.draw()` passes the box's exact width and height to Plotly |
| B-003 | End-of-line labels were cut off on phones | 2026-11-15 | 2026-11-15 | Labels are hidden below 520 px wide; the legend names the lines instead |
| B-004 | Two end labels overlapped on the search-race chart | 2026-11-15 | 2026-11-15 | Removed those labels; the legend carries the three names |

## Enhancements: open

### Notebook 01: Data and baseline

All done.

### Notebook 02: Evolution loop

| ID | Enhancement | Priority | Status |
|---|---|---|---|
| E-010 | Notebook 02: run all 20 generations, write `results/web/evolution.json`, and write the "What it means" notes from the real run (Steps 4 onward) | P1 | Open |
| E-025 | Notebook 02 charts (best and median per generation, winning settings, winner vs baseline by cover type, training vs held-out gap); add the feature-share column to the site's generation table | P2 | Open |

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
| E-021 | Change the portfolio card status from "In progress" once real results replace the sample data | M3 | P2 | Open |
| E-018 | Live "run more generations" demo on the VPS | M7 | P3 | Open |
| E-026 | Presentation: add each notebook's slides (plan slides 13 to 30) to `presentation/build_deck.js` when it is finished, then rerun `make_formats.py` | M2–M4 | P2 | Open |
| E-030 | Every notebook saves its charts as PNG files for the site and the deck (done for notebook 01; repeat for 02 to 04) | M2–M4 | P2 | Open |
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
| E-009 | `src/evolve.py`: five settings (model type, trees, depth, leaf size, feature share; 5,670 combinations), mutation by one small step, population 10, keep 3, survivors never retrained, `to_web()` for the site; 12 pytest tests. Notebook 02 Steps 1–4: setup, the settings, how a child is made, generation 1 scored with a dot chart | Notebook 02 | 2026-11-20 |
| E-027 | Presentation part 1 (13 slides: opening and every step of notebook 01) built as native PowerPoint with speaker notes (`presentation/build_deck.js`) | Presentation | 2026-11-20 |
| E-028 | PDF, slide PNGs (zipped), one-file offline web page with speaker notes, and cover, all made from the one PowerPoint (`presentation/make_formats.py`), published in `site/presentation/` | Presentation | 2026-11-20 |
| E-029 | "The story, as a presentation" section on the overview: cover thumbnail with slide count, View button, four downloads with sizes; a test checks they match the deck | Site | 2026-11-20 |
| E-031 | Overview page rebuilt on the Life Expectancy / meat-prices pattern: label line, four stat cards, hero chart, plain English, key-findings cards, five charts with captions, word list, numbered "How it was done", numbered notebook cards, More; no sample numbers on the overview | Site | 2026-11-20 |
| E-015 | Build publishes every run notebook as a web page in `notebooks/`, with the back bar (`publish_notebooks()`), and skips notebooks not yet run | Site | 2026-11-20 |
| E-032 | `docs/FINDINGS.md` (Life Expectancy pattern: start here, word list, short version, one section per finding) published as `docs/FINDINGS.html` | Site | 2026-11-20 |
| E-033 | Notebook 01 draws and saves five charts (cover types, baseline scores, recall by cover type, elevation by cover type, confusion); `save_web_chart()` with 2 tests; build copies them to the site | Notebook 01 | 2026-11-20 |
| E-020 | Sample-data version published to schirko.com/scott/model-loop-lab | Site | 2026-11-15 |
| E-008 | `src/evaluate.py`: shared loading, 20,000-plot stratified sample, train/test split, accuracy scoring; 10 pytest tests | Notebook 01 | 2026-11-15 |
| E-024 | Notebook 01 run on the real data; "What it means" notes written from the actual numbers (baseline 77.2%, weakest Aspen 44%) | Notebook 01 | 2026-11-16 |
| E-023 | Notebook 01 Step 10 saves `results/web/baseline.json`; overview and The loop works read it; sample tag on the overview names only figures still on sample data; `src/web_results.py` with 4 tests | Notebook 01 | 2026-11-16 |
| E-007 | Notebook 01 Steps 7 to 9: baseline score with training-score comparison, per-cover-type table, confusion chart; `fit_predict()` and `cover_type_report()` added to `src/evaluate.py` with 2 tests | Notebook 01 | 2026-11-16 |
| E-022 | Notebook 01 started: setup, full dataset, sample, split, guessing versus a tree, repeatability check | Notebook 01 | 2026-11-16 |

## Change history

| Date | Change |
|---|---|
| 2026-11-20 | E-009 done: evolution loop code and notebook 02 Steps 1–4. Recall chart now marks amber only for cover types more than 5 points below the overall score, matching the deck. Tests now 56. |
| 2026-11-20 | Presentation part 1 published in all formats and linked from the overview (E-027 to E-029). The deck now grows with each notebook (E-026). Tests now 44. |
| 2026-11-20 | Overview rebuilt (E-031), notebooks and findings published as web pages (E-015, E-032), notebook 01 charts (E-033). E-015 moved forward from M5. Tests now 41. |
| 2026-11-20 | Full presentation plan written (`docs/PRESENTATION_PLAN.md`); added E-030. |
| 2026-11-19 | Added E-026 to E-029 for the M8 presentation. |
| 2026-11-16 | Notebook 01 done (E-024): M1 complete. B-006 and B-007 found and fixed. |
| 2026-11-16 | First real run of notebook 01: baseline 77.18%. B-005 found and fixed. |
| 2026-11-16 | E-023 done. Test suite now 33 tests. |
| 2026-11-16 | E-007 done. Test suite now 28 tests. |
| 2026-11-16 | Reorganized around four notebooks. Enhancements are now the tasks that build each notebook and the site, grouped by notebook. Notebook 01 renamed `01_data_and_baseline.ipynb`; the baseline (E-007) goes into it instead of a separate notebook. Added E-022 to E-025. |
| 2026-11-15 | E-008 done. Test suite now 26 tests. |
| 2026-11-15 | Site published with sample data; portfolio card and screenshot added by the portfolio session (E-016, E-017, E-020). Added E-021. |
| 2026-11-15 | E-006 done (first push). Publishing to the Schirko repo split out as E-020. |
| 2026-11-15 | Created with the M0 front end. B-001 to B-004 found and fixed during the first render check. |
