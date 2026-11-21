"""Builds notebooks/02_evolution_loop.ipynb (kept so the notebook can be regenerated).

E-009 adds Steps 1 to 4: setup, the settings the loop can change, how a child is
made, and generation 1 scored against the baseline. E-010 adds the full run.
"""

from pathlib import Path

import nbformat as nbf

md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell

cells = [
    md("""# 02. The evolution loop

**Notebook:** 02 of 4 · **Milestone:** M2 · **Code:** `src/evolve.py` · **Enhancements:** E-009 (Steps 1–4), E-010 and E-025 (to come)

Notebook 01 ended with a brief: a plain decision tree gets **77.2%** of held-out plots right, it memorizes its training plots (100% on those), and it confuses neighboring cover types. This notebook asks whether a program can do better **on its own**, with no person choosing the settings.

The loop works like evolution in miniature:

| Stage | What happens |
|---|---|
| **Build** | A population of 10 models, each with its own settings |
| **Score** | Every model on the same 5,000 held-out plots as notebook 01 |
| **Keep** | The best 3 survive unchanged |
| **Change** | The other 7 places go to copies of the survivors with one small random change each |

Then back to Build, for 20 generations. The only thing guiding the loop is the score.

**To run in PyCharm:** open this file, choose the project's `.venv` as the kernel, then click **Run All**. Or from the terminal: `.venv\\Scripts\\python -m nbconvert --to notebook --execute --inplace notebooks/02_evolution_loop.ipynb`."""),

    md("""## Step 1. Setup

### What we're looking for
The same data, sample and split as notebook 01, so every score here is directly comparable with the 77.2% baseline, which is read from the file notebook 01 saved."""),
    code("""import json
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import matplotlib.pyplot as plt

from src.evaluate import SEED, load_covertype, make_split
from src.evolve import (MODEL_NAMES, SEARCH_SPACE, SETTING_MEANINGS, evolve, generation_summary,
                        mutate, random_settings)
from src.web_results import AMBER, GRAY, SPRUCE, save_web_chart

plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "font.size": 11})
pd.set_option("display.max_colwidth", 90)

X, y = load_covertype()
split = make_split(X, y)
baseline = json.loads((PROJECT_ROOT / "results" / "web" / "baseline.json").read_text(encoding="utf-8"))

print(f"Training plots: {len(split.X_train):,}   Held-out plots: {len(split.X_test):,}")
print(f"Baseline to beat: {baseline['label']}, {baseline['score']:.2%}")"""),
    md("""### How to read it
The plot counts should match notebook 01 exactly (15,000 and 5,000), and the baseline should read 77.18%.

### What it means
Same plots, same split, same scoring function. Any model in this notebook that scores above 77.2% is genuinely better than the plain tree, not luckier.

### What's next and why
Before running the loop, it helps to see exactly which settings it is allowed to change."""),

    md("""## Step 2. The settings the loop can change

### What we're looking for
The "genes" of each model: the five settings the loop chooses, and the values each one can take. Two of them speak directly to notebook 01's main weakness, memorizing."""),
    code("""space = pd.DataFrame({
    "setting": list(SEARCH_SPACE),
    "values it can take": [", ".join("no limit" if v is None else MODEL_NAMES.get(v, str(v)) for v in vals)
                           for vals in SEARCH_SPACE.values()],
    "what it means": [SETTING_MEANINGS[k] for k in SEARCH_SPACE],
}).set_index("setting")
combos = 1
for vals in SEARCH_SPACE.values():
    combos *= len(vals)
print(f"Possible combinations of settings: {combos:,}")
space"""),
    md("""### How to read it
One row per setting. The middle column lists every value the loop can choose, in order from smallest to largest; the right column says what the setting does. The line above the table counts every possible combination.

### What it means
* **`max_depth`** and **`min_samples_leaf`** limit memorizing. Notebook 01's plain tree had no depth limit and a leaf size of 1, which is how it built 2,341 final answers and scored 100% on its own training plots.
* **`model`** can swap the single tree for a **random forest** or **extra trees**, which average many trees. Averaging smooths out the quirks any one tree memorizes.
* **`max_features`** makes trees look at different features, so the trees in a forest disagree in useful ways.

There are 5,670 combinations. The loop will try around 150 of them, so it has to search, not test everything. That is the point of the experiment: can a simple rule (keep the best, change them a little) find good settings in a space too large to try exhaustively?

### What's next and why
The "change them a little" part is the heart of the loop, so the next step shows exactly what a change looks like."""),

    md("""## Step 3. How a child is made

### What we're looking for
What one **mutation** does: a survivor is copied, and exactly one of its settings moves one step to a neighboring value (or, for the model type, switches to a different type)."""),
    code("""rng = random.Random(SEED)
parent = random_settings(rng)
children = []
while len(children) < 6:            # six different children of the same parent
    c = mutate(parent, rng)
    if c not in children:
        children.append(c)

def changed(child):
    keys = [k for k in SEARCH_SPACE if getattr(child, k) != getattr(parent, k)]
    return ", ".join(f"{k}: {getattr(parent, k)} \\u2192 {getattr(child, k)}" for k in keys)

family = pd.DataFrame(
    [{"who": "Parent", "settings": parent.label(), "change": ""}] +
    [{"who": f"Child {i}", "settings": c.label(), "change": changed(c)} for i, c in enumerate(children, 1)]
).set_index("who")
family"""),
    md("""### How to read it
The first row is a parent with random settings. Each child below it is one possible copy with a single change, and the last column names which setting moved and from what to what.

### What it means
Children look like their parents. Because each step is small, a good model's children are usually good too, and the loop refines what works instead of starting over. Occasionally a change switches the model type, which lets the loop jump to a different kind of model when that pays off.

### What's next and why
With the rules clear, the next step builds and scores generation 1: ten models with completely random settings."""),

    md("""## Step 4. Generation 1: ten random models

### What we're looking for
Where the loop starts. Generation 1 has no history, so its ten models have random settings. How do they compare with the 77.2% baseline, and how far apart are the best and the worst?

This is exactly generation 1 of the full run in the next steps: same seed, same ten models."""),
    code("""gen1 = evolve(split, population=10, keep=3, generations=1)
show = gen1[["rank", "kept", "score", "label"]].copy()
show["vs baseline"] = ((show["score"] - baseline["score"]) * 100).map("{:+.1f} pts".format)
show["score"] = show["score"].map("{:.1%}".format)
show.set_index("rank")"""),
    code("""fig, ax = plt.subplots(figsize=(8, 4.2))
s = gen1.sort_values("score").reset_index(drop=True)
colors = [SPRUCE if k else GRAY for k in s["kept"]]
ax.axvline(baseline["score"], color=AMBER, linestyle="--", linewidth=2, zorder=1)
ax.scatter(s["score"], range(len(s)), s=90, color=colors, zorder=3)
for i, v in enumerate(s["score"]):
    left = v < baseline["score"]          # labels stay on the dot's side of the baseline line
    ax.text(v - 0.004 if left else v + 0.004, i, f"{v:.1%}", va="center", ha="right" if left else "left")
ax.set_yticks(range(len(s)), [f"Model {r}" for r in s["rank"]])
ax.set_ylim(-1.2, len(s) - 0.4)
ax.text(baseline["score"] + 0.003, -0.95, f"baseline {baseline['score']:.1%}", color=AMBER, va="center")
lo = min(s["score"].min(), baseline["score"]) - 0.035
ax.set_xlim(lo, max(s["score"].max(), baseline["score"]) + 0.03)
ax.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
ax.grid(axis="y", color="#e6e9e5", linewidth=0.8)
ax.set_axisbelow(True)
ax.set_xlabel("Accuracy on the 5,000 held-out plots")
ax.set_title("Generation 1: ten random models against the baseline", loc="left")
save_web_chart(fig, "generation_1")
plt.show()"""),
    md("""### How to read it
The table lists generation 1's ten models from best (rank 1) to worst, with each one's full settings and how many percentage points above or below the baseline it scored. In the chart, each dot is one model: green dots are the three survivors that become parents of generation 2, gray dots are dropped, and the dashed amber line is the baseline. Dots to the right of the line beat the plain tree. The chart is saved as `generation_1.png`.

### What it means
*Written from the real run (E-010): how many random models already beat 77.2%, which kinds of settings top the table, and how wide the spread is.*

### What's next and why
Generation 1 is pure chance. The next steps (E-010) run all 20 generations and show whether keeping the best and changing them a little climbs steadily above where chance starts."""),
]

nb = nbf.v4.new_notebook(cells=cells, metadata={
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
})
out = Path(__file__).resolve().parent.parent / "notebooks" / "02_evolution_loop.ipynb"
nbf.write(nb, out)
print(f"Wrote {out}")
