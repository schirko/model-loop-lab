# Model Loop Lab: Site Milestones

**Project:** Model Loop Lab, a portfolio project on whether AI can build better AI.
**Lives at:** `B:\_Dev\Python\model-loop-lab` (PyCharm) and https://github.com/schirko/model-loop-lab
**Published at:** https://schirko.com/scott/model-loop-lab/ (through the Schirko repo)
**Maintained by:** Claude, updated whenever a milestone starts, changes or finishes.

## The goal

Build an AI-improving-AI loop, measure how much it improves, and show where that kind of loop breaks, then explain every step in plain language on a static project site linked from the portfolio.

Two experiments:

1. **The loop works.** An evolutionary search builds, scores, keeps and changes forest-cover models for 20 generations, then races Optuna and random guessing.
2. **Where loops break.** Model collapse: each generation learns only from the previous generation's synthetic data, and accuracy on real data falls.

Data: Forest Covertype (Roosevelt National Forest, Colorado), loaded with scikit-learn's `fetch_covtype`, sampled to 20,000 rows.

## Status key

- **Done**: finished, tested and committed
- **In progress**: being worked on now
- **Next**: the recommended next milestone
- **Planned**: agreed, not started

## Milestones

| # | Milestone | Status | Enhancement items |
|---|---|---|---|
| M0 | Project setup and front end | Done (waiting on first commit) | E-001 to E-006 |
| M1 | Baseline model and shared scoring | Next | E-007, E-008 |
| M2 | The evolution loop | Planned | E-009, E-010 |
| M3 | Racing Optuna and random guessing, and writing the findings | Planned | E-011, E-012 |
| M4 | Model collapse experiment | Planned | E-013, E-014 |
| M5 | Notebooks published as site pages | Planned | E-015 |
| M6 | Publish and add the portfolio card | Planned | E-016, E-017 |
| M7 | Live "run more generations" demo on the VPS (optional) | Planned | E-018 |

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

### M1. Baseline model and shared scoring

**Why:** Every later number is judged against the baseline. A fixed sample and a fixed test set make results comparable across all experiments.

**Plan:**
- `notebooks/01_baseline.ipynb`: load Covertype, take a fixed 20,000-row sample (fixed random seed), split train and held-out test, score a default decision tree
- `src/evaluate.py`: one shared function that trains a model and returns test accuracy, used by every notebook
- pytest tests for `src/evaluate.py`

**Done when:** the baseline accuracy is recorded and `evaluate.py` is tested.

### M2. The evolution loop

**Why:** This is the core claim: a program improves models without a person choosing settings.

**Plan:**
- `src/evolve.py`: population of 10, keep top 3, mutate, 20 generations, fixed seed
- `notebooks/02_evolution_loop.ipynb`: run it, log every model tried
- Write `results/web/evolution.json` with `"sample": false` so the site switches to real data

**Done when:** the generations chart and table on the site show real results.

### M3. Racing Optuna and random guessing, and writing the findings

**Why:** Improvement only matters if it beats simpler options. This is also where the "What it means" notes get written from real numbers.

**Plan:**
- `notebooks/03_optuna_compare.ipynb`: same 200-model budget for all three methods
- Write `results/web/search_compare.json`
- Replace the "Written from the real run" placeholders on The loop works page

### M4. Model collapse experiment

**Why:** Shows the limit of the idea, which is what separates this project from hype.

**Plan:**
- `src/collapse.py`: Gaussian mixture generator, 10 generations, classifier scored on real held-out data
- `notebooks/04_model_collapse.ipynb`
- Write `results/web/collapse.json` and the "What it means" notes on Where loops break

### M5. Notebooks published as site pages

**Why:** Lets employers read the full reasoning, code then result then explanation.

**Plan:** export each notebook to HTML into `site/notebooks/`, add the back bar and noindex tag, keep file sizes small, link from the Notebooks page.

### M6. Publish and add the portfolio card

**Why:** The project is only useful to employers once it is live and linked.

**Plan:** build, commit the Schirko repo, redeploy in Coolify, take the 16:9 screenshot, send the card details to the portfolio session.

### M7. Live demo on the VPS (optional)

**Why:** A visitor clicks "run 5 more generations" and watches the loop improve live. Memorable, but not needed for the project to be complete.

## Change history

| Date | Change |
|---|---|
| 2026-11-15 | Created. Plan moved from a Streamlit app to a static HTML site published under schirko.com/scott. M0 front end built. |
