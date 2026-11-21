"""The evolution loop: a program that searches for better forest-cover models.

Each round (a "generation"):
1. Build:  a population of models, each with its own settings.
2. Score:  every model on the same held-out plots, with src.evaluate.evaluate().
3. Keep:   the best few ("survivors") carry over unchanged.
4. Change: the rest of the next population are copies of survivors with small
           random changes ("mutations").

No person chooses the settings. The only thing guiding the loop is the score.

Typical use in a notebook:

    from src.evolve import evolve, generation_summary
    log = evolve(split, population=10, keep=3, generations=20)
    generation_summary(log)
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from src.evaluate import SEED, Split, evaluate

# ---------------------------------------------------------------------------
# The settings the loop is allowed to change, and the values each can take.
# Ordered lists, so a small mutation can step to a neighboring value.
# ---------------------------------------------------------------------------
MODEL_TYPES = ["decision_tree", "random_forest", "extra_trees"]
MODEL_NAMES = {"decision_tree": "Decision tree", "random_forest": "Random forest", "extra_trees": "Extra trees"}
N_ESTIMATORS = [25, 50, 100, 150, 200, 300]            # trees in a forest (ignored for a single tree)
MAX_DEPTH = [6, 10, 14, 18, 22, 26, 30, 40, None]       # how many questions deep a tree may go; None = no limit
MIN_SAMPLES_LEAF = [1, 2, 3, 4, 6, 8, 12]               # fewest plots a final answer must cover
MAX_FEATURES = ["sqrt", 0.3, 0.5, 0.8, 1.0]             # share of map features each split may look at

SEARCH_SPACE = {
    "model": MODEL_TYPES,
    "n_estimators": N_ESTIMATORS,
    "max_depth": MAX_DEPTH,
    "min_samples_leaf": MIN_SAMPLES_LEAF,
    "max_features": MAX_FEATURES,
}

# What each setting means, in plain English (used in notebook 02 and on the site).
SETTING_MEANINGS = {
    "model": "The kind of model: one decision tree, or a forest that averages many trees",
    "n_estimators": "How many trees a forest averages (a single decision tree ignores this)",
    "max_depth": "How many yes/no questions deep a tree may go; no limit lets it memorize",
    "min_samples_leaf": "The fewest plots a final answer must cover; 1 lets it fit single plots",
    "max_features": "The share of the 54 map features each question may choose from",
}


@dataclass(frozen=True)
class Settings:
    """One model's settings: one value for each entry in SEARCH_SPACE."""

    model: str
    n_estimators: int
    max_depth: int | None
    min_samples_leaf: int
    max_features: str | float

    def as_dict(self) -> dict:
        return {k: getattr(self, k) for k in SEARCH_SPACE}

    def label(self) -> str:
        """Short readable description, e.g. 'Random forest, 200 trees, depth 26, leaf 1, features 0.5'."""
        depth = "no depth limit" if self.max_depth is None else f"depth {self.max_depth}"
        trees = "" if self.model == "decision_tree" else f", {self.n_estimators} trees"
        return f"{MODEL_NAMES[self.model]}{trees}, {depth}, leaf {self.min_samples_leaf}, features {self.max_features}"


def random_settings(rng: random.Random) -> Settings:
    """Pick every setting at random. This is how generation 1 starts."""
    return Settings(**{k: rng.choice(v) for k, v in SEARCH_SPACE.items()})


def _step(values: list, current, rng: random.Random):
    """Move one position up or down an ordered list of values (stays in range)."""
    i = values.index(current)
    j = min(len(values) - 1, max(0, i + rng.choice([-1, 1])))
    if j == i:  # at an end: step the only way possible
        j = i - 1 if i == len(values) - 1 else i + 1
    return values[j]


def mutate(parent: Settings, rng: random.Random, changes: int = 1) -> Settings:
    """Copy a survivor and change `changes` of its settings a little.

    Numeric settings step to a neighboring value. The model type, when picked,
    switches to a different type. Small steps mean children resemble their
    parents, so good settings are refined rather than thrown away.
    """
    new = parent.as_dict()
    for key in rng.sample(list(SEARCH_SPACE), k=changes):
        if key == "model":
            new[key] = rng.choice([m for m in MODEL_TYPES if m != parent.model])
        else:
            new[key] = _step(SEARCH_SPACE[key], new[key], rng)
    child = Settings(**new)
    return child if child != parent else mutate(parent, rng, changes)


def make_model(settings: Settings, seed: int = SEED):
    """Turn settings into an untrained scikit-learn model."""
    common = dict(max_depth=settings.max_depth, min_samples_leaf=settings.min_samples_leaf,
                  max_features=settings.max_features, random_state=seed)
    if settings.model == "decision_tree":
        return DecisionTreeClassifier(**common)
    forest = RandomForestClassifier if settings.model == "random_forest" else ExtraTreesClassifier
    return forest(n_estimators=settings.n_estimators, n_jobs=-1, **common)


def evolve(
    split: Split,
    population: int = 10,
    keep: int = 3,
    generations: int = 20,
    seed: int = SEED,
    scorer: Callable | None = None,
    on_generation: Callable[[int, pd.DataFrame], None] | None = None,
) -> pd.DataFrame:
    """Run the loop and return a log with one row per model per generation.

    Columns: generation, rank (1 = best that generation), kept (a survivor),
    new (first time these settings were scored), score, label, and one column
    per setting.

    Settings already scored are not retrained: survivors keep their score, and
    a child that happens to repeat earlier settings reuses its score. That is
    why the best score can never go down from one generation to the next.
    `scorer(model, split)` defaults to src.evaluate.evaluate.
    """
    if not 0 < keep < population:
        raise ValueError("keep must be at least 1 and smaller than population")
    score_model = scorer or evaluate
    rng = random.Random(seed)
    scores: dict[Settings, float] = {}

    current: list[Settings] = []
    while len(current) < population:          # generation 1: all random, no repeats
        s = random_settings(rng)
        if s not in current:
            current.append(s)

    rows = []
    for gen in range(1, generations + 1):
        gen_rows = []
        for s in current:
            new = s not in scores
            if new:
                scores[s] = float(score_model(make_model(s, seed), split))
            gen_rows.append({"generation": gen, "score": scores[s], "new": new, "label": s.label(), **s.as_dict(), "_s": s})
        gen_rows.sort(key=lambda r: r["score"], reverse=True)
        for rank, r in enumerate(gen_rows, 1):
            r["rank"] = rank
            r["kept"] = rank <= keep
        rows.extend(gen_rows)
        if on_generation:
            on_generation(gen, pd.DataFrame(gen_rows).drop(columns="_s"))

        survivors = [r["_s"] for r in gen_rows[:keep]]
        children: list[Settings] = []
        k = 0
        while len(survivors) + len(children) < population:   # children from each survivor in turn
            child = mutate(survivors[k % keep], rng)
            if child not in survivors and child not in children:
                children.append(child)
            k += 1
        current = survivors + children

    cols = ["generation", "rank", "kept", "new", "score", "label", *SEARCH_SPACE]
    return pd.DataFrame(rows)[cols]


def generation_summary(log: pd.DataFrame) -> pd.DataFrame:
    """Best, median and worst score per generation, and how many models were new."""
    g = log.groupby("generation")
    return pd.DataFrame({
        "best": g["score"].max(),
        "median": g["score"].median(),
        "worst": g["score"].min(),
        "new_models": g["new"].sum(),
    })


def to_web(log: pd.DataFrame, baseline: dict, keep: int, sample_size: int) -> dict:
    """Shape the log for the website's evolution.json (see site/data/evolution.json)."""
    summary = generation_summary(log)
    gens = []
    for gen, row in summary.iterrows():
        top = log[(log.generation == gen) & (log["rank"] <= keep)].sort_values("rank")
        gens.append({
            "gen": int(gen),
            "best": round(float(row.best), 4),
            "median": round(float(row["median"]), 4),
            "worst": round(float(row.worst), 4),
            "top": [{
                "model": MODEL_NAMES[r.model],
                "params": {
                    "n_estimators": "—" if r.model == "decision_tree" else int(r.n_estimators),
                    "max_depth": "None" if pd.isna(r.max_depth) else int(r.max_depth),
                    "min_samples_leaf": int(r.min_samples_leaf),
                    "max_features": r.max_features,
                },
                "score": round(float(r.score), 4),
            } for r in top.itertuples()],
        })
    population = int(log[log.generation == 1].shape[0])
    return {
        "dataset": f"Forest Covertype (stratified sample of {sample_size:,} plots)",
        "metric": "Accuracy on held-out plots",
        "baseline": {"label": baseline["label"], "score": baseline["score"]},
        "population": population,
        "keep": keep,
        "models_trained": int(log["new"].sum()),
        "generations": gens,
    }
