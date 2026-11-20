# Model Loop Lab: Site Milestones

**Project:** Model Loop Lab, a portfolio project on whether AI can build better AI.
**Lives at:** `B:\Development\Python\model-loop-lab` (PyCharm) and https://github.com/schirko/model-loop-lab
**Published at:** https://schirko.com/scott/model-loop-lab/ (through the Schirko repo)
**Maintained by:** Claude, updated whenever a milestone starts, changes or finishes.

## The goal

Build an AI-improving-AI loop, measure how much it improves, and show where that kind of loop breaks, then explain every step in plain language on a static project site linked from the portfolio.

Two experiments:

1. **The loop works.** An evolutionary search builds, scores, keeps and changes forest-cover models for 20 generations, then races Optuna and random guessing.
2. **Where loops break.** Model collapse: each generation learns only from the previous generation's synthetic data, and accuracy on real data falls.

Data: Forest Covertype (Roosevelt National Forest, Colorado), loaded with scikit-learn's `fetch_covtype`, sampled to 20,000 rows.

## Notebooks

The four notebooks are the heart of the project. Each milestone from M1 to M4 delivers one notebook; the enhancements that build each one are listed under it in Enhancements-and-Bugs.md.

| # | Notebook | Milestone |
|---|---|---|
| 01 | `01_data_and_baseline.ipynb` | M1 |
| 02 | `02_evolution_loop.ipynb` | M2 |
| 03 | `03_search_race.ipynb` | M3 |
| 04 | `04_model_collapse.ipynb` | M4 |

## Status key

- **Done**: finished, tested and committed
- **In progress**: being worked on now
- **Next**: the recommended next milestone
- **Planned**: agreed, not started

## Milestones

| # | Milestone | Status | Enhancement items |
|---|---|---|---|
| M0 | Project setup and front end | Done | E-001 to E-006 |
| M1 | Notebook 01: data and baseline | Done (baseline 77.2%) | E-007, E-008, E-022 to E-024 |
| M2 | Notebook 02: the evolution loop | Next | E-009, E-010, E-025 |
| M3 | Notebook 03: racing Optuna and random guessing | Planned | E-011, E-012, E-021 |
| M4 | Notebook 04: model collapse | Planned | E-013, E-014 |
| M5 | Notebooks published as site pages | Done early: every run notebook is published by the build (E-015) | E-015 |
| M6 | Publish and add the portfolio card | In progress (live with sample data) | E-016, E-017, E-020 |
| M7 | Live "run more generations" demo on the VPS (optional) | Planned | E-018 |
| M8 | Presentation, growing with each notebook | In progress: part 1 (notebook 01) published | E-026 to E-029 |

### M0. Project setup and front end

**Why:** Gives every later milestone a visible place to land. Employers see the shape of the project from day one, and each notebook only has to write a small results file to fill in its chart.

**Delivered:**
- Four pages in `site/`: overview, The loop works, Where loops break, Notebooks
- Portfolio rules met on every page: back bar, favicons, noindex tag, absolute `/scott/` paths
- Charts in Plotly drawn from `site/data/*.json`, marked "Sample data" until real results arrive
- `scripts/build_site.py` publishes `site/` to the portfolio folder and checks every page
- pytest suite (16 tests) for the build script, page rules and data files
- The three project documents (this file, Enhancements-and-Bugs.md, Beginning-End-Development-Guide.md)

**Done when:** pages build into `Schirko\scott\model-loop-lab`, tests pass, and the first commit is pushed.

### M1. Notebook 01: data and baseline

**Why:** Every later number is judged against the baseline. A fixed sample and a fixed test set make results comparable across all experiments.

**Plan:**
- `src/evaluate.py`: shared loading, sample, split and scoring, with pytest tests (E-008) - done
- Notebook 01 walkthrough of the data, sample, split and scoring (E-022) - done
- Baseline steps: default decision tree, per-cover-type results (E-007) - done
- Baseline saved to the site (E-023) - done
- Notebook run on real data and notes written (E-024) - done

**Done when:** notebook 01 runs top to bottom in PyCharm and the site shows the real baseline.

### M2. Notebook 02: the evolution loop

**Why:** This is the core claim: a program improves models without a person choosing settings.

**Plan:**
- `src/evolve.py`: population of 10, keep top 3, mutate, 20 generations, fixed seed
- `02_evolution_loop.ipynb` runs it and logs every model tried
- Write `results/web/evolution.json` with `"sample": false` so the site switches to real data

**Done when:** the generations chart and table on the site show real results.

### M3. Notebook 03: racing Optuna and random guessing

**Why:** Improvement only matters if it beats simpler options. This is also where the "What it means" notes get written from real numbers.

**Plan:**
- `03_search_race.ipynb` gives all three methods the same 200-model budget
- Write `results/web/search_compare.json`
- Replace the "Written from the real run" placeholders on The loop works page

### M4. Notebook 04: model collapse

**Why:** Shows the limit of the idea, which is what separates this project from hype.

**Plan:**
- `src/collapse.py`: Gaussian mixture generator, 10 generations, classifier scored on real held-out data
- `04_model_collapse.ipynb` runs the collapse loop
- Write `results/web/collapse.json` and the "What it means" notes on Where loops break

### M5. Notebooks published as site pages

**Why:** Lets employers read the full reasoning, code then result then explanation.

**Plan:** export each notebook to HTML into `site/notebooks/`, add the back bar and noindex tag, keep file sizes small, link from the Notebooks page.

### M6. Publish and add the portfolio card

**Why:** The project is only useful to employers once it is live and linked.

**Plan:** build, commit the Schirko repo, redeploy in Coolify, take the 16:9 screenshot, send the card details to the portfolio session.

### M7. Live demo on the VPS (optional)

**Why:** A visitor clicks "run 5 more generations" and watches the loop improve live. Memorable, but not needed for the project to be complete.

### M8. Presentation

**Why:** A deck tells the whole story, notebook by notebook and step by step, in about 20 minutes, for an interview, a meeting or an email.

**How it grows:** Part 1 (13 slides: the opening and every step of notebook 01) is published now. As each notebook is finished, its slides are added from its real results, and all formats are rebuilt. Only real numbers ever go on a slide.

**The full slide-by-slide plan is in [`docs/PRESENTATION_PLAN.md`](docs/PRESENTATION_PLAN.md):** 30 slides plus a 4-slide appendix, a 12-minute core version, and for every slide its section label, headline, visual, callouts, source line and speaker notes. It is modeled on the Meat Price Explorer deck and the Life Expectancy Predictor's plain-English findings. Notebook 01's slides already carry its real numbers; notebooks 02 to 04's slides fill in as those notebooks are finished.

**Files**, in `scott/model-loop-lab/presentation/`, matching `scott/meat-prices/presentation/`:
- `model-loop-lab-story.html`: one self-contained web page that works offline
- `model-loop-lab-story.pptx`: editable PowerPoint with speaker notes
- `model-loop-lab-story.pdf`: for reading or printing
- `model-loop-lab-story-slides.zip`: every slide as a PNG
- `cover.png`: the cover slide, used as the thumbnail

A "The story, as a presentation" section on the project's overview page shows the cover thumbnail and slide count, a "View the presentation" button, and download links for PDF, PowerPoint, HTML and slide images, each with its size.

**Done when:** the full deck (about 30 slides plus appendix) is published in every format, no plan placeholders remain, and every number matches its notebook step.

## Change history

| Date | Change |
|---|---|
| 2026-11-20 | Presentation part 1 published (13 slides, all formats) and linked from the overview; the deck now grows with each notebook instead of waiting for M8. |
| 2026-11-20 | Overview page rebuilt to walk through the notebooks with real results only; notebooks and findings now published as web pages, so M5 is done early. |
| 2026-11-20 | M8 plan rewritten as a full slide-by-slide presentation plan, `docs/PRESENTATION_PLAN.md`, walking through every notebook and step. |
| 2026-11-19 | Added M8: a presentation in HTML, PowerPoint and PNG, built after all other milestones. |
| 2026-11-16 | M1 done. Baseline 77.2% (default decision tree, 100% on training plots). Weakest: Aspen 44%, Douglas-fir 52%. |
| 2026-11-16 | E-023 done: baseline saved for the site. Only E-024 (real run) left in M1. |
| 2026-11-16 | E-007 done: baseline steps added to notebook 01. |
| 2026-11-16 | Reorganized around four notebooks, one per milestone M1 to M4. Notebook 01 (data and baseline) started. |
| 2026-11-15 | M1 started: `src/evaluate.py` done and tested. |
| 2026-11-15 | Site live at schirko.com/scott/model-loop-lab with sample data, portfolio card added. |
| 2026-11-15 | M0 done: first commit pushed to GitHub on `master`. |
| 2026-11-15 | Created. Plan moved from a Streamlit app to a static HTML site published under schirko.com/scott. M0 front end built. |
