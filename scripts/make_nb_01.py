"""Builds notebooks/01_data_and_baseline.ipynb (kept so the notebook can be regenerated)."""

from pathlib import Path

import nbformat as nbf

md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell

cells = [
    md("""# 01. Data and baseline

**Notebook:** 01 of 4 · **Milestone:** M1 · **Code:** `src/evaluate.py` · **Enhancements:** E-008, E-022, E-007 (done), E-023, E-024 (to come)

This notebook answers two questions: what does the Colorado forest data look like, and how good is a plain model with no tuning? The second answer is the baseline, the number every later notebook has to beat.

Every experiment in Model Loop Lab gets its data and its scores from one file, `src/evaluate.py`. Steps 1 to 6 walk through that file and check each piece on the real Forest Covertype data. Steps 7 to 9 record the baseline and show where it goes wrong.

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
    cover_type_report, evaluate, fit_predict, load_covertype, make_split,
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
* **A plain decision tree** with default settings. This is a preview of the baseline, recorded properly in the steps that follow."""),
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
The shared pieces work on the real data. Now they can be trusted to record the official baseline."""),

    md("""## Step 7. Record the baseline

### What we're looking for
The **baseline**: the accuracy of a decision tree with every setting left at its default. Nobody chose its settings, so it shows how well a model does with zero tuning. Every improvement the evolution loop claims in notebook 02 is measured against this number.

We also score the tree on the plots it trained on. Comparing the two scores shows whether the tree learned general patterns or just memorized its training plots."""),
    code("""baseline_model = DecisionTreeClassifier(random_state=SEED)
fitted, predictions = fit_predict(baseline_model, split)

baseline = evaluate(baseline_model, split)
train_score = fitted.score(split.X_train, split.y_train)

print(f"Baseline accuracy on held-out plots: {baseline:.2%}")
print(f"Accuracy on its own training plots:  {train_score:.2%}")
print(f"Tree size: {fitted.get_depth()} levels deep, {fitted.get_n_leaves():,} leaves")
print(f"Wrong on {int(round((1 - baseline) * len(split.y_test))):,} of {len(split.y_test):,} held-out plots")"""),
    md("""### How to read it
The first line is the baseline. The second is the same tree scored on the 15,000 plots it learned from. The third line gives the tree's size: each level is one more yes/no question, and each leaf is a final answer. The last line turns the baseline into a count of mistakes.

### What it means
A default tree keeps splitting until every training plot is sorted perfectly, which is why its training score is at or near 100%. It grows thousands of leaves, many of them fitted to single, unusual plots. The drop from that near-perfect training score to the held-out score is **overfitting**: the tree memorized details that don't carry over to new plots.

That gap is exactly what the evolution loop can work on. Settings such as maximum depth and minimum leaf size stop a tree from memorizing, and other model types average many trees together. The loop's job is to find the combination that closes the gap.

### What's next and why
A single accuracy number hides where the mistakes are. With cover types this uneven, the tree could be strong on the common types and weak on the rare ones."""),

    md("""## Step 8. Which cover types does the baseline get right?

### What we're looking for
For each cover type: how many held-out plots it has, how many the tree got right (**recall**), and how trustworthy the tree's answer is when it names that type (**precision**). Rare cover types are where a model is most likely to struggle."""),
    code("""report = cover_type_report(split.y_test, predictions)
report.style.format({"recall": "{:.1%}", "precision": "{:.1%}"})"""),
    md("""### How to read it
* **plots**: how many of the 5,000 held-out plots really are this cover type
* **correct**: how many of those the tree labeled correctly
* **recall**: correct ÷ plots. "Of the real Aspen plots, how many did the tree find?"
* **precision**: of every plot the tree *called* this type, the share that really were. "When the tree says Aspen, how often is it right?"

### What it means
Look at whether the low recall rates line up with the small plot counts. If they do, the baseline is weakest on the cover types it saw the fewest examples of. That's normal for an untuned tree, and it means the overall accuracy is carried mostly by Lodgepole pine and Spruce/fir.

### What's next and why
The table says how often each type is missed but not what it gets mistaken for. The next chart shows that."""),

    md("""## Step 9. What gets confused with what?

### What we're looking for
Patterns in the mistakes. Cover types that grow in similar places, at similar elevations and on similar soils, should be the ones the tree mixes up."""),
    code("""import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

names = list(COVER_TYPES.values())
fig, ax = plt.subplots(figsize=(8, 7))
ConfusionMatrixDisplay.from_predictions(
    split.y_test, predictions,
    labels=list(COVER_TYPES), display_labels=names,
    normalize="true", values_format=".0%", cmap="Greens", colorbar=False, ax=ax,
)
ax.set_xlabel("Tree's answer")
ax.set_ylabel("Real cover type")
ax.set_title("Baseline decision tree: share of each real cover type by answer")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.show()"""),
    md("""### How to read it
Each row is a real cover type and adds up to 100% across. Each column is the tree's answer. The diagonal from top left to bottom right shows correct answers, the same numbers as the recall column in Step 8. Any other shaded square is a mistake: the row's cover type was called the column's.

### What it means
The biggest off-diagonal squares show which cover types look alike from the map features. Expect Spruce/fir and Lodgepole pine to be confused with each other, since they share the middle elevations, and the lower-elevation types (Ponderosa pine, Douglas-fir, Cottonwood/willow) to be confused among themselves. Those mix-ups are where a better model has the most to gain.

### What's next and why
The baseline is recorded. Next, the baseline gets saved where the website can read it (E-023), so the site's "Starting accuracy" shows this real number. Then notebook 02 starts the evolution loop and tries to beat it."""),

    md("""## Summary

| Check | Result |
|---|---|
| Full dataset | 581,012 plots, 54 features, 7 cover types |
| Sample | 20,000 plots, cover-type shares kept |
| Split | 15,000 training / 5,000 held-out, no overlap |
| Scoring | Repeatable, never changes the model passed in |
| Baseline | Default decision tree, scored in Step 7 |
| Weak spots | Rare cover types and look-alike pairs, Steps 8 and 9 |

The data and scoring checks also run automatically in `tests/test_evaluate.py` every time `python -m pytest` runs, on a small made-up dataset so they don't need the download."""),
]

nb = nbf.v4.new_notebook(cells=cells, metadata={
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
})
out = Path(__file__).resolve().parent.parent / "notebooks" / "01_data_and_baseline.ipynb"
nbf.write(nb, out)
print(f"Wrote {out}")
