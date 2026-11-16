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
git branch -M main
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
├── tests/                        pytest tests
├── notebooks/                    Jupyter notebooks (M1 onward)
├── src/                          shared Python code (M1 onward)
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
git push -u origin main
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

**Sample data and the switch to real data.** Every data file has a `"sample"` field. While it is `true`, the page shows a "Sample data" notice next to the chart. Notebooks write real results to `results/web/<name>.json` with `"sample": false`. The build script copies those over the sample files, and the notice disappears. Nothing in the pages needs to change.

**Data file formats.**

| File | Read by | Main fields |
|---|---|---|
| `evolution.json` | overview, The loop works | `baseline {label, score}`, `generations [{gen, best, median, worst, top [{model, params, score}]}]` |
| `search_compare.json` | The loop works | `trials`, `evolution`, `optuna`, `random` (best-so-far accuracy after each model tried) |
| `collapse.json` | overview, Where loops break | `generations [{gen, real_test_accuracy, diversity, elevation_hist {bins, counts}}]` |

`tests/test_site_pages.py` checks these shapes, so a notebook that writes a bad file fails the tests.

**Tests.** `python -m pytest` runs everything in `tests/`. Current coverage: the build script, the portfolio rules on every page, and the shape of every data file.

---

## Part 4. Development log

Newest first. Every addition, removal or change goes here.

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

**Fixed during the render check:** B-001 to B-004 (see Enhancements-and-Bugs.md).
