"""Builds notebooks/01_shared_scoring.ipynb (kept so the notebook can be regenerated)."""

from pathlib import Path

import nbformat as nbf

md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell

cells = [
    md("""# 01. Shared data loading and scoring

**Notebook:** 01 · **Item:** E-008 · **Milestone:** M1 (Baseline model and shared scoring) · **Code:** `src/evaluate.py`

Every experiment in Model Loop Lab, from the evolution loop to model collapse, gets its data and its scores from one file, `src/evaluate.py`. This notebook walks through that file one piece at a time and checks each piece on the real Forest Covertype data.

**Why one shared file?** If each notebook loaded data and scored models its own way, a better score might only mean a luckier split of the data. Sharing the code means every model on the site is judged on exactly the same plots, so the comparisons are fair.

The four pieces:

| Piece | Job |
|---|---|
| `load_covertype()` | Get the data and take a 20,000-plot sample |
| `make_split()` | Hold back 25% of the plots for testing |
| `evaluate()` | Train a model and score it on the held-out plots |
| `SEED` | One number that fixes every random step |

**To run in PyCharm:** open this file, choose the project's `.venv` as the kernel (top right of the notebook), then click **Run All**. The first run downloads about 11 MB of data into `data/`."""),

    md("## Step 1. Setup"),
    code("""import sys
from pathlib import Path

# Let the notebook import from src/ (the project root is one folder up).
PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier

from src.evaluate import (
    COVER_TYPES, SAMPLE_SIZE, SEED, TEST_SIZE,
    evaluate, load_covertype, make_split,
)

pd.set_option("display.max_columns", 12)
print(f"Seed: {SEED}   Sample size: {SAMPLE_SIZE:,}   Test share: {TEST_SIZE:.0%}")"""),
    md("""This prints the three settings every experiment shares. They live in `src/evaluate.py`, so changing one there changes it everywhere at once."""),

    md("""## Step 2. Load the full dataset

### What we're looking for
How big the full dataset is, what a row looks like, and how common each of the seven forest cover types is. The last point matters for Step 3."""),
    code("""X_full, y_full = load_covertype(sample_size=None)
print(f"Plots: {len(X_full):,}   Features: {X_full.shape[1]}")
X_full.iloc[:5, :10]"""),
    md("""### How to read it
Each row is one 30 by 30 meter plot of the Roosevelt National Forest. The first ten columns are map measurements: elevation in meters, aspect (compass direction the slope faces), slope in degrees, distances to water, roads and past fire points, and hillshade (how much sun the plot gets at 9am, noon and 3pm). The remaining 44 columns are yes/no flags: 4 for wilderness area and 40 for soil type."""),

    code("""full_counts = (
    y_full.value_counts().sort_index()
    .rename(index=COVER_TYPES).rename("plots").to_frame()
)
full_counts["share"] = (full_counts["plots"] / len(y_full)).map("{:.2%}".format)
full_counts"""),
    md("""### How to read it
One row per cover type: how many plots have it and what share of all plots that is.

### What it means
The classes are very uneven. Two cover types, Lodgepole pine and Spruce/fir, take up most of the forest, while Cottonwood/willow is a tiny sliver. A model can look good by getting the two big ones right and ignoring the rest, which is worth remembering whenever we read an accuracy number later.

### What's next and why
581,012 plots is too many to train models on over and over in a loop. The next step takes a smaller sample without losing the rare cover types."""),

    md("""## Step 3. Take the 20,000-plot sample

### What we're looking for
Whether the sample keeps each cover type's share. `load_covertype()` uses a **stratified** sample: it draws from each cover type in proportion to its size, instead of drawing 20,000 plots blindly. A blind draw could leave the rarest type with almost nothing."""),
    code("""X, y = load_covertype()   # default: 20,000 plots, seed 42
sample_counts = y.value_counts().sort_index().rename(index=COVER_TYPES)

compare = pd.DataFrame({
    "full share": (full_counts["plots"] / len(y_full)).map("{:.2%}".format),
    "sample plots": sample_counts,
    "sample share": (sample_counts / len(y)).map("{:.2%}".format),
})
print(f"Sample: {len(X):,} plots")
compare"""),
    md("""### How to read it
The first column is each cover type's share of the full forest. The next two are its count and share in the sample.

### What it means
The two share columns should match to within a few hundredths of a percent. That's what stratifying buys us: the sample is a small but faithful copy of the forest, rare cover types included.

### What's next and why
Now the sample has to be split, so models can be trained on some plots and tested on plots they have never seen."""),

    md("""## Step 4. Split into training and held-out plots

### What we're looking for
A 75/25 split where no plot appears on both sides, and where both sides keep the same cover-type shares."""),
    code("""split = make_split(X, y)
overlap = set(split.X_train.index) & set(split.X_test.index)

shares = pd.DataFrame({
    "train share": split.y_train.value_counts(normalize=True).sort_index(),
    "test share": split.y_test.value_counts(normalize=True).sort_index(),
}).rename(index=COVER_TYPES).map("{:.2%}".format)

print(f"Training plots: {len(split.X_train):,}   Held-out plots: {len(split.X_test):,}   Plots in both: {len(overlap)}")
shares"""),
    md("""### How to read it
The first line gives the size of each side and how many plots appear in both. The table compares cover-type shares in the training and held-out sets.

### What it means
15,000 plots to learn from, 5,000 to be tested on, and zero overlap. Testing on unseen plots is what makes a score honest. A model scored on plots it trained on can simply memorize them and look far better than it really is. Every score on the site comes from these same 5,000 held-out plots.

### What's next and why
With data and split fixed, the last piece is the scoring function itself."""),

    md("""## Step 5. Score models with `evaluate()`

### What we're looking for
Two scores that frame everything that follows:

* **Guessing**: a "model" that always predicts the most common cover type. Any real model has to beat this to be worth anything.
* **A plain decision tree** with default settings. This is a preview of the baseline that E-007 records properly."""),
    code("""guess = evaluate(DummyClassifier(strategy="most_frequent"), split)
tree = evaluate(DecisionTreeClassifier(random_state=SEED), split)

print(f"Always guess the most common type: {guess:.1%}")
print(f"Plain decision tree:               {tree:.1%}")"""),
    md("""### How to read it
Each number is accuracy: the share of the 5,000 held-out plots where the predicted cover type was right.

### What it means
Guessing scores about the same as the largest cover type's share, because that's the only type it ever predicts. The decision tree, which actually looks at elevation, soil and the rest, should do far better. The gap between the two is how much the map features tell us about which trees grow where.

### What's next and why
Before trusting `evaluate()` inside a loop that calls it hundreds of times, we need to know it gives the same answer every time and has no side effects."""),

    md("""## Step 6. Check that scoring is repeatable

### What we're looking for
Two things the evolution loop depends on: scoring the same settings twice gives the identical number, and the model passed in is left untouched (`evaluate()` trains a copy)."""),
    code("""model = DecisionTreeClassifier(random_state=SEED)
first = evaluate(model, split)
second = evaluate(model, split)

print(f"First score:  {first:.4f}")
print(f"Second score: {second:.4f}")
print(f"Identical: {first == second}")
print(f"Original model still untrained: {not hasattr(model, 'tree_')}")"""),
    md("""### How to read it
Both scores, whether they match exactly, and whether the model object we passed in was changed.

### What it means
Identical scores and an untrained original mean any difference between two models in the loop comes from their settings, not from chance or from one run leaking into the next.

### What's next and why
The shared pieces work on the real data. The next notebook, **02_baseline** (E-007), uses them to record the official baseline, the plain decision tree's score, and writes it to the site as the number the evolution loop has to beat."""),

    md("""## Summary

| Check | Result |
|---|---|
| Full dataset | 581,012 plots, 54 features, 7 cover types |
| Sample | 20,000 plots, cover-type shares kept |
| Split | 15,000 training / 5,000 held-out, no overlap |
| Scoring | Repeatable, never changes the model passed in |

The same checks run automatically in `tests/test_evaluate.py` every time `python -m pytest` runs, on a small made-up dataset so they don't need the download."""),
]

nb = nbf.v4.new_notebook(cells=cells, metadata={
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
})
out = Path(__file__).resolve().parent.parent / "notebooks" / "01_shared_scoring.ipynb"
nbf.write(nb, out)
print(f"Wrote {out}")
