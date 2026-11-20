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

1. In PyCharm, create a new project at `B:\Development\Python\model-loop-lab` with a new `.venv` virtual environment.
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
├── results/web/                  real results written by notebooks: *.json data, images/*.png charts
├── data/                         downloaded data, not committed
├── .env.example                  copy to .env and set SITE_DIR
├── .gitignore
├── pytest.ini
├── requirements.txt
├── presentation/
│   ├── build_deck.js             builds the deck as a PowerPoint (pptxgenjs)
│   ├── make_formats.py           makes the PDF, slide PNGs, zip, web page and cover from it
│   └── assets/                   images the deck uses (confusion chart)
├── docs/
│   ├── FINDINGS.md               every conclusion so far; published as docs/FINDINGS.html
│   └── PRESENTATION_PLAN.md       slide-by-slide plan for the M8 presentation
├── Site-Milestones.md
├── Enhancements-and-Bugs.md
└── Beginning-End-Development-Guide.md
```

### Step 3. Install packages and set the publish folder (M0)

Always call this project's own Python by its path, `.venv\Scripts\python`. On this PC a plain `python` can resolve to another project's environment even when the prompt shows `(.venv)` (bug B-006).

```
.venv\Scripts\python -m pip install -r requirements.txt
copy .env.example .env
```

`.env` holds `SITE_DIR=B:\Development\Python\Schirko\scott\model-loop-lab`. The build script refuses any folder that does not end in `model-loop-lab`, so it can never clear the wrong folder.

### Step 4. Test, build and preview (M0)

```
.venv\Scripts\python -m pytest
.venv\Scripts\python scripts/build_site.py
```

To preview, serve the Schirko folder so the `/scott/...` paths resolve, then open http://localhost:8000/scott/model-loop-lab/ in a browser:

```
cd B:\Development\Python\Schirko
python -m http.server 8000
```

### Step 5. Commit and publish (M0, then after every item)

Project repo, from `B:\Development\Python\model-loop-lab`:

```
git add .
git commit -m "Describe the change"
git push -u origin master
```

Portfolio repo, from `B:\Development\Python\Schirko`, then redeploy in Coolify:

```
git add scott
git commit -m "Publish Model Loop Lab project page"
git push
```

Never edit `scott/index.html` (the portfolio page). Send card details to the portfolio session instead.

---

## Part 3. How the pieces fit together

**Ownership in the portfolio folder (standing rule).** This project owns only:
- `Schirko\scott\model-loop-lab\` (everything the build writes)
- `Schirko\scott\images\screenshots\model-loop-lab.png` (its card screenshot)

It never writes `scott\index.html` or `scott\styles.css`; the portfolio project owns those. Card changes are sent to Scott as text, and he passes them to the portfolio project. `scripts/build_site.py` writes only inside `SITE_DIR`, refuses any `SITE_DIR` not named `model-loop-lab`, and `tests/test_build_site.py::test_build_never_touches_portfolio_files` checks that the portfolio's files are left untouched.

**What the build does** (`scripts/build_site.py`), in order:
1. Copies `site/` into `SITE_DIR`.
2. Copies `results/web/*.json` over the sample data in `data/`, and `results/web/images/*.png` into `images/`.
3. Publishes every notebook that has been run (`notebooks/NN_*.ipynb` with saved outputs) as `notebooks/NN_*.html`, using nbconvert's "lab" layout, with the portfolio head links and back bar added. Notebooks not yet run are skipped.
4. Publishes `docs/FINDINGS.md` as `docs/FINDINGS.html` (the `markdown` package), with the back bar.
5. Checks every page for the back bar, favicon and noindex tag.

**The overview page** follows the Life Expectancy and Meat Price Explorer pages: a label line, title, lede and buttons; four stat cards; the hero chart; "The project in plain English"; "Key findings so far" as one card per finding with its notebook step; the notebook charts with captions; "Words used on this page"; "How it was done" as numbered steps; "The analysis, step by step" as one numbered card per notebook (linked once published); and "More". It shows real results only. A test checks that it quotes the same baseline as `results/web/baseline.json`, and another that it carries no sample numbers. The two experiment pages keep their tagged sample charts until notebooks 02 to 04 replace them.

**The presentation.** `presentation/build_deck.js` builds the deck as a native PowerPoint (editable text and charts, speaker notes on every slide) following `docs/PRESENTATION_PLAN.md`. `presentation/make_formats.py` turns that one file into everything published in `site/presentation/`: the `.pptx`, a PDF, every slide as a PNG (zipped), a single-file web page with slide controls and speaker notes that works offline, `cover.png`, and `deck.json` (slide count and file sizes). The overview's "The story, as a presentation" section links them, and a test checks its slide count and sizes against `deck.json`. Rebuilding needs Node with `pptxgenjs`, LibreOffice and Poppler, so Claude rebuilds it as each notebook's slides are added; the published files are committed with the site.

**Charts.** Notebooks save charts with `save_web_chart(fig, name)` from `src/web_results.py` (150 dpi PNG, white background, site colors `SPRUCE`, `GRAY`, `AMBER`). The overview, the findings and the presentation all use these same files.

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

**Notebooks.** The project has four notebooks, one per milestone: `01_data_and_baseline`, `02_evolution_loop`, `03_search_race`, `04_model_collapse`. Many enhancements go into each one. Each notebook has: setup cell, then for every step a "What we're looking for" note, the code, its output, and "How to read it", "What it means", "What's next and why". To run one in PyCharm: open the `.ipynb`, pick the project's `.venv` as the kernel (top right), click **Run All**. To run a notebook from the terminal instead, saving every output into the file and stopping with a clear message at the first error: `.venv\Scripts\python -m nbconvert --to notebook --execute --inplace notebooks/<name>.ipynb`. The setup cell adds the project root to the import path, so `from src.evaluate import ...` works from inside `notebooks/`.

**Tests.** `python -m pytest` runs everything in `tests/`. `pytest.ini` puts the project root and `scripts/` on the import path. Current coverage: the build script, the portfolio rules on every page, the shape of every data file, and `src/evaluate.py` (sampling keeps class shares, splits don't overlap, scoring is repeatable and never changes the model passed in). The evaluate tests use a small made-up dataset, so they never download Covertype.

---

## Part 4. Development log

Newest first. Every addition, removal or change goes here.

### 2026-11-20: Presentation part 1 published

**Why:** the other portfolio projects let visitors view and download their presentation; this one now does too, from part 1 on, instead of waiting for the end.
**Added:** `presentation/build_deck.js` (13 slides: title, the two loops, word list, the four notebooks, notebook 01 opener, Steps 1 to 10 across seven slides, what's next; every slide with speaker notes), `presentation/make_formats.py`, `presentation/assets/confusion.png` (from notebook 01's real run), `site/presentation/` (pptx, pdf, slides zip, web page, cover, deck.json), the overview's "The story, as a presentation" section and its styles, and a test that the overview matches the deck (suite now 44). `presentation/out/` is git-ignored.
**Design:** Cambria headings and Calibri text (both ship with Office, so the PowerPoint looks the same on any PC), the site's spruce green with amber for "memorized" and weak spots, dark slides for the title and section openers.

### 2026-11-20: Overview rebuilt; notebooks and findings published as web pages

**Why:** the first overview was a placeholder built before any results: short, didn't walk through the notebooks, and showed sample numbers (86.7%, 46.0%) next to the real 77.2%. Rebuilt on the Life Expectancy Predictor and Meat Price Explorer pages.
**Changed:** `site/index.html` rewritten (see Part 3, "The overview page"); `site/assets/site.css` gained the matching styles (stat cards, panels, finding cards, numbered steps and notebook cards, docs pages); `site/notebooks/index.html` links notebook 01.
**Added:** `scripts/build_site.py` now copies chart images, publishes run notebooks (`publish_notebooks()`) and `docs/FINDINGS.md` (`publish_docs()`); `docs/FINDINGS.md`; notebook 01 now draws and saves five charts (`cover_types`, `baseline_scores`, `cover_type_recall`, `elevation_by_type`, `confusion`), including a new elevation-by-cover-type chart in Step 9; `save_web_chart()` in `src/web_results.py`; `markdown` in `requirements.txt`; 7 tests (suite now 41).
**Next run:** notebook 01 must be rerun to save its charts, then the build publishes everything.

### 2026-11-20: Presentation plan

**Added:** `docs/PRESENTATION_PLAN.md`, the slide-by-slide plan for the Milestone 8 deck: 30 slides plus a 4-slide appendix, walking through every notebook and its steps. Each slide has a section label (notebook and step), a one-sentence headline, a visual, up to three callouts, a source line and full speaker notes. Modeled on the Meat Price Explorer deck (`meat-prices/docs/PRESENTATION_PLAN.md`, `scott/meat-prices/presentation/`) and the Life Expectancy Predictor's plain-English findings and word list. Notebook 01's slides use its real numbers; later slides are marked with placeholders to fill from their notebooks.
**Added:** E-030, every notebook saves the charts the deck needs as PNG files.

### 2026-11-19: Projects folder moved to `B:\Development\Python`

**Changed:** the projects folder moved from `B:\_Dev\Python` to `B:\Development\Python`. Updated every path: `.env.example` and `.env` (`SITE_DIR=B:\Development\Python\Schirko\scott\model-loop-lab`), this guide, Site-Milestones.md, and the example path in `tests/test_build_site.py`. The code itself uses no fixed paths, so nothing else needed changing.
**Added:** Milestone 8, a presentation in HTML, PowerPoint and PNG, built after all other milestones (E-026 to E-029).

**PyCharm:** the moved project's `.venv` may still point at the old folder. If `.venv\Scripts\python` fails, rebuild it: delete `.venv`, create a new one in PyCharm, then reinstall with `.venv\Scripts\python -m pip install -r requirements.txt`.

### 2026-11-16: M1 complete (E-024)

**Result:** notebook 01 run on the real data. Baseline 77.2% (default decision tree; 100% on training plots, 33 levels, 2,341 leaves). Guessing the most common type: 48.8%. Weakest cover types: Aspen 44%, Douglas-fir 52%, Cottonwood/willow 65%. Biggest confusions: Spruce/fir and Lodgepole pine with each other, Aspen called Lodgepole pine, Douglas-fir and Cottonwood/willow called Ponderosa pine.
**Changed:** notebook 01's "What it means" notes rewritten from these real numbers.
**Fixed:** B-006, commands now call `.venv\Scripts\python` (plain `python` ran the Life Expectancy environment). B-007, file updates undone by PyCharm were rewritten. Notebooks are now run with `nbconvert` from the terminal, which saves every output into the file.

### 2026-11-16: Run notebooks from the terminal

**Added:** `nbconvert` to `requirements.txt`, so a notebook can be run top to bottom from the terminal with its outputs saved. Added after two PyCharm runs of notebook 01 stopped after Step 4 without recording an error.

### 2026-11-16: Portfolio ownership rule

**Rule:** this project never writes `scott/index.html` or `scott/styles.css`. It owns only `scott/model-loop-lab/` and `scott/images/screenshots/model-loop-lab.png`. Card changes go to Scott as text.
**Checked:** `scripts/build_site.py` had no step writing `index.html` or `styles.css` (it writes only inside `SITE_DIR`), so nothing was removed.
**Added:** test `test_build_never_touches_portfolio_files` (suite now 34).

### 2026-11-16: First real run of notebook 01; B-005 fixed

**Result:** first run on the real Covertype data: baseline 77.18% on held-out plots, 100% on training plots (33 levels, 2,341 leaves); guessing the most common type scores 48.8%.
**Fixed:** B-005, Step 8 used pandas `.style`, which needs the `jinja2` package. The table now formats recall and precision as text, so no extra package is needed.

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
