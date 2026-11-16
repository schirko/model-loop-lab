# Model Loop Lab: Beginning-to-End Development Guide

This guide records everything needed to rebuild Model Loop Lab from nothing, and every addition, removal or change made along the way. Claude updates it at the end of every work item.

- **Part 1** lists the accounts, tools and outside services the project depends on.
- **Part 2** is the from-scratch rebuild, in order.
- **Part 3** explains how the pieces fit together.
- **Part 4** is the development log, newest entry first.

---

## Part 1. Accounts, tools and outside services

### Accounts

| Account | Used for | Notes |
|---|---|---|
| GitHub (`schirko`) | The `model-loop-lab` repository | Public repo |
| GitHub, Schirko repo | Publishing the site | The site is copied into `Schirko\scott\model-loop-lab` and deploys with schirko.com |
| VPS with Coolify | Hosting schirko.com | Coolify redeploys after the Schirko repo is pushed |

No database, Render or Neon account is needed. The site is static files only.

### Local tools

| Tool | Version used | Purpose |
|---|---|---|
| Windows PC | | Development machine |
| PyCharm | | Editor, terminal and Jupyter notebooks |
| Python | 3.14 (project `.venv`) | Analysis, tests and the build script |
| Git | | Version control |

### Outside services the pages load

| Service | What | Why |
|---|---|---|
| cdnjs | `plotly.js/2.35.3/plotly-basic.min.js` | Draws the charts (line and bar charts only, so the smaller "basic" bundle) |
| Google Fonts | Newsreader (headings), Public Sans (text) | Page typefaces; the pages fall back to system fonts if blocked |

### Data

| Dataset | Where it comes from | Licence |
|---|---|---|
| Forest Covertype | scikit-learn `fetch_covtype()`, originally UCI Machine Learning Repository (Blackard and Dean, U.S. Forest Service and Colorado State University) | CC BY 4.0 |

---

## Part 2. Rebuild from scratch

Follow these in order. Each step says which milestone added it.

### Step 1. Create the project (M0)

1. In PyCharm, create a new project at `B:\_Dev\Python\model-loop-lab` with a new `.venv` virtual environment.
2. On GitHub, create the repository `schirko/model-loop-lab`.
3. In the PyCharm terminal:

```
git init
git branch -M master
git remote add origin https://github.com/schirko/model-loop-lab.git
```

### Step 2. Add the project files (M0)

Create this layout:

```
model-loop-lab/
├── site/                         the published website (source)
│   ├── index.html                overview page
│   ├── loop/index.html           The loop works
│   ├── collapse/index.html       Where loops break
│   ├── notebooks/index.html      notebook list
│   ├── assets/site.css           page styles (never styles .sx- classes)
│   ├── assets/charts.js          shared chart helpers (MLL.*)
│   └── data/*.json               chart data: sample until real results replace it
├── scripts/build_site.py         publishes site/ into the portfolio folder
├── scripts/make_nb_01.py         regenerates notebook 01 from code
├── tests/                        pytest tests
├── notebooks/                    the four project notebooks
│   └── 01_data_and_baseline.ipynb  data, sample, split, scoring, baseline (M1)
├── src/                          shared Python code
│   ├── __init__.py               makes src importable (from src.evaluate import ...)
│   ├── evaluate.py               data loading, sample, split and scoring (M1)
│   └── web_results.py            save_web_result(): notebooks save results for the site
├── results/web/                  real chart data written by notebooks
├── data/                         downloaded data, not committed
├── .env.example                  copy to .env and set SITE_DIR
├── .gitignore
├── pytest.ini
├── requirements.txt
├── Site-Milestones.md
├── Enhancements-and-Bugs.md
└── Beginning-End-Development-Guide.md
```

### Step 3. Install packages and set the publish folder (M0)

```
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
```

`.env` holds `SITE_DIR=B:\_Dev\Python\Schirko\scott\model-loop-lab`. The build script refuses any folder that does not end in `model-loop-lab`, so it can never clear the wrong folder.

### Step 4. Test, build and preview (M0)

```
python -m pytest
python scripts/build_site.py
```

To preview, serve the Schirko folder so the `/scott/...` paths resolve, then open http://localhost:8000/scott/model-loop-lab/ in a browser:

```
cd B:\_Dev\Python\Schirko
python -m http.server 8000
```

### Step 5. Commit and publish (M0, then after every item)

Project repo, from `B:\_Dev\Python\model-loop-lab`:

```
git add .
git commit -m "Describe the change"
git push -u origin master
```

Portfolio repo, from `B:\_Dev\Python\Schirko`, then redeploy in Coolify:

```
git add scott
git commit -m "Publish Model Loop Lab project page"
git push
```

Never edit `scott/index.html` (the portfolio page). Send card details to the portfolio session instead.

---

## Part 3. How the pieces fit together

**Pages.** Plain HTML in `site/`. Every page carries, as the portfolio requires: the noindex meta tag, `/scott/backbar.css`, the four favicon links, and the `sx-backbar` block as the first thing in `<body>` with the crumb "Model Loop Lab". All links use absolute `/scott/` paths.

**Charts.** Each chart page loads Plotly, then `assets/charts.js`, then its own short script. The script calls `MLL.load("<name>")` to fetch `/scott/model-loop-lab/data/<name>.json` and `MLL.draw()` to render. Colors come from CSS variables, so light and dark mode both work.

**Sample data and the switch to real data.** Notebooks save results with `save_web_result(name, payload)` from `src/web_results.py`, which only accepts names the site reads (`baseline`, `evolution`, `search_compare`, `collapse`) and always marks the file `"sample": false` with today's date. Every data file has a `"sample"` field. While it is `true`, the page shows a "Sample data" notice next to the chart. Notebooks write real results to `results/web/<name>.json` with `"sample": false`. The build script copies those over the sample files, and the notice disappears. Nothing in the pages needs to change.

**Data file formats.**

| File | Read by | Main fields |
|---|---|---|
| `baseline.json` | overview, The loop works | `label`, `score`, `train_score`, `held_out_plots`, `training_plots`, `tree_depth`, `tree_leaves`, `seed`, `recorded` |
| `evolution.json` | overview, The loop works | `baseline {label, score}`, `generations [{gen, best, median, worst, top [{model, params, score}]}]` |
| `search_compare.json` | The loop works | `trials`, `evolution`, `optuna`, `random` (best-so-far accuracy after each model tried) |
| `collapse.json` | overview, Where loops break | `generations [{gen, real_test_accuracy, diversity, elevation_hist {bins, counts}}]` |

`tests/test_site_pages.py` checks these shapes, so a notebook that writes a bad file fails the tests.

**Shared scoring (`src/evaluate.py`).** Every experiment loads and scores data through this one file, so all numbers on the site are comparable:

| Function | What it does |
|---|---|
| `load_covertype()` | Downloads Covertype once into `data/` (about 11 MB), then returns a 20,000-plot sample, stratified so every cover type keeps its share |
| `make_split(X, y)` | 75% training plots, 25% held-out test plots, stratified, seed 42 |
| `evaluate(model, split)` | Trains a fresh copy of the model and returns accuracy on the held-out plots |
| `fit_predict(model, split)` | Same training, but returns the trained copy and its held-out predictions |
| `cover_type_report(y_true, y_pred)` | One row per cover type: plots, correct, recall, precision |
| `COVER_TYPES` | Names for cover types 1 to 7 (Spruce/fir, Lodgepole pine, ...) |

One seed (42) drives every random step, so rerunning a notebook gives the same numbers.

**Notebooks.** The project has four notebooks, one per milestone: `01_data_and_baseline`, `02_evolution_loop`, `03_search_race`, `04_model_collapse`. Many enhancements go into each one. Each notebook has: setup cell, then for every step a "What we're looking for" note, the code, its output, and "How to read it", "What it means", "What's next and why". To run one in PyCharm: open the `.ipynb`, pick the project's `.venv` as the kernel (top right), click **Run All**. The setup cell adds the project root to the import path, so `from src.evaluate import ...` works from inside `notebooks/`.

**Tests.** `python -m pytest` runs everything in `tests/`. `pytest.ini` puts the project root and `scripts/` on the import path. Current coverage: the build script, the portfolio rules on every page, the shape of every data file, and `src/evaluate.py` (sampling keeps class shares, splits don't overlap, scoring is repeatable and never changes the model passed in). The evaluate tests use a small made-up dataset, so they never download Covertype.

---

## Part 4. Development log

Newest first. Every addition, removal or change goes here.

### 2026-11-16: E-023 baseline saved for the site

**Added:** `src/web_results.py` (`save_web_result()`), `tests/test_web_results.py` (4 tests), `site/data/baseline.json` (sample stand-in), notebook 01 Step 10, a baseline shape test in `tests/test_site_pages.py` (suite now 33).
**Changed:** `site/assets/charts.js` gained `MLL.baseline()`, which loads `baseline.json` and, when it holds real data, replaces the copy inside `evolution.json`. The overview's figures now show one sample tag naming only the figures still on sample data.

**Decisions**
- The baseline gets its own file instead of living inside `evolution.json`: it is produced by notebook 01, long before notebook 02 writes the evolution results, so the site can show it as soon as it exists.
- `save_web_result()` refuses unknown names and forces `"sample": false`, so a typo can't create a file the site ignores and a notebook can never publish sample data by mistake.

### 2026-11-16: E-007 baseline steps in notebook 01

**Added:** notebook 01 Steps 7 to 9: the baseline (default decision tree) scored on held-out and training plots, a per-cover-type table, and a confusion chart (matplotlib). `src/evaluate.py` gained `fit_predict()` and `cover_type_report()`; `tests/test_evaluate.py` gained 2 tests (suite now 28).

**Decisions**
- Show the training score next to the held-out score: the gap shows overfitting, which is what the evolution loop can fix.
- Report recall and precision per cover type: overall accuracy is dominated by the two common types, and the rare types are where the loop has the most room to improve.
- `cover_type_report()` lives in `src/` because notebooks 02 and 03 will compare evolved models against the baseline the same way.

### 2026-11-16: Notebook 01 started (E-022); work reorganized around four notebooks

**Added:** `notebooks/01_data_and_baseline.ipynb`, steps 1 to 6 (setup, full dataset, stratified sample, split, guessing versus a decision tree, repeatability). `scripts/make_nb_01.py` regenerates it.
**Changed:** the project is organized around four notebooks (01 data and baseline, 02 evolution loop, 03 search race, 04 model collapse). Enhancements are the tasks that build each notebook and the site, grouped by notebook in Enhancements-and-Bugs.md. The site's Notebooks page lists the four notebooks.
**Tested:** every cell run top to bottom here on stand-in data (this workspace can't download Covertype); real outputs appear when it is run in PyCharm.

### 2026-11-15: E-008 shared scoring (`src/evaluate.py`)

**Added:** `src/__init__.py`, `src/evaluate.py`, `tests/test_evaluate.py` (10 tests; suite now 26).
**Changed:** `pytest.ini` now puts the project root on the path (`pythonpath = . scripts`) so tests import `src.evaluate`.
**Removed:** `src/.gitkeep` (the folder now has real files).

**Decisions**
- Stratified 20,000-plot sample: Cottonwood/willow is under 0.5% of plots, and a plain random sample could leave it with almost none.
- `evaluate()` trains a clone of the model: scoring the same settings twice gives the same answer, and nothing carries over between runs. The evolution loop depends on this.
- Accuracy as the score: easy to explain on the site ("correct on 86 of every 100 plots"). Per-class results can be added later if the rare cover types turn out to matter.

### 2026-11-15: First publish (sample data)

- Built into `Schirko\scott\model-loop-lab` and pushed with the Schirko repo; Coolify redeployed. Live at https://schirko.com/scott/model-loop-lab/.
- The portfolio session added the card (Data Science Projects, status "In progress") and the screenshot `scott/images/screenshots/model-loop-lab.png`. Neither file belongs to this project; changes to them go through the portfolio session.

### 2026-11-15: M0 project setup and front end

**Added**
- Site pages: `site/index.html`, `site/loop/index.html`, `site/collapse/index.html`, `site/notebooks/index.html`
- `site/assets/site.css`: spruce-green palette for Colorado forest data, Newsreader and Public Sans, light and dark mode, phone layout
- `site/assets/charts.js`: data loading, sample-data notices, theme-aware Plotly layouts, exact-size drawing
- Sample data: `site/data/evolution.json`, `search_compare.json`, `collapse.json` (made up, flagged `"sample": true`)
- `scripts/build_site.py` and tests in `tests/test_build_site.py` and `tests/test_site_pages.py` (16 tests)
- `.gitignore`, `.env.example`, `pytest.ini`, `requirements.txt`, empty `notebooks/`, `src/`, `results/web/`, `data/` folders
- The three project documents

**Decisions**
- Static HTML site under schirko.com/scott instead of a Streamlit app: no extra server, matches Meat Price Explorer, follows the portfolio's "Adding a project" guide.
- Plotly basic bundle 2.35.3 from cdnjs: the full bundle is several times larger and only line and bar charts are needed.
- Charts read JSON files instead of having numbers written into the pages, so notebooks can update the site without anyone editing HTML.

**Committed:** first push to `schirko/model-loop-lab` on the `master` branch. PyCharm's `.idea` folder was untracked (`git rm -r --cached .idea`) and is ignored from then on.

**Fixed during the render check:** B-001 to B-004 (see Enhancements-and-Bugs.md).
