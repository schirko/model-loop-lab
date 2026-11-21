"""Tests for src/evolve.py.

Most tests use a stand-in scorer (a made-up score computed from the settings),
so they run in a moment and never train real models. One test runs the real
loop on a small made-up dataset.
"""

import random

import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from src import evaluate as ev
from src import evolve as evo


def fake_scorer(model, split):
    """A made-up score: deeper limits and more trees score higher, plus noise from the settings."""
    p = model.get_params()
    depth = p.get("max_depth") or 50
    trees = p.get("n_estimators", 1)
    return 0.5 + depth / 200 + trees / 2000 - p["min_samples_leaf"] / 100


@pytest.fixture
def split():
    X, y = make_classification(n_samples=600, n_features=8, n_informative=5, n_classes=3, random_state=0)
    X = pd.DataFrame(X, columns=[f"f{i}" for i in range(8)])
    return ev.make_split(X, pd.Series(y + 1), seed=1)


def test_random_settings_stay_in_the_search_space():
    rng = random.Random(0)
    for _ in range(200):
        s = evo.random_settings(rng)
        for key, values in evo.SEARCH_SPACE.items():
            assert getattr(s, key) in values


def test_mutation_changes_exactly_one_setting_by_a_small_step():
    rng = random.Random(1)
    for _ in range(300):
        parent = evo.random_settings(rng)
        child = evo.mutate(parent, rng)
        changed = [k for k in evo.SEARCH_SPACE if getattr(child, k) != getattr(parent, k)]
        assert len(changed) == 1
        key = changed[0]
        values = evo.SEARCH_SPACE[key]
        assert getattr(child, key) in values
        if key != "model":
            assert abs(values.index(getattr(child, key)) - values.index(getattr(parent, key))) == 1


@pytest.mark.parametrize("model, cls", [
    ("decision_tree", DecisionTreeClassifier),
    ("random_forest", RandomForestClassifier),
    ("extra_trees", ExtraTreesClassifier),
])
def test_make_model_builds_the_right_kind(model, cls):
    s = evo.Settings(model=model, n_estimators=50, max_depth=10, min_samples_leaf=2, max_features="sqrt")
    m = evo.make_model(s, seed=3)
    assert isinstance(m, cls)
    assert m.get_params()["max_depth"] == 10 and m.get_params()["min_samples_leaf"] == 2


def test_log_has_one_row_per_model_per_generation(split):
    log = evo.evolve(split, population=6, keep=2, generations=4, scorer=fake_scorer)
    assert len(log) == 6 * 4
    assert (log.groupby("generation")["kept"].sum() == 2).all()
    assert (log.groupby("generation")["rank"].max() == 6).all()


def test_best_score_never_goes_down(split):
    log = evo.evolve(split, population=6, keep=2, generations=8, scorer=fake_scorer)
    best = evo.generation_summary(log)["best"].tolist()
    assert all(a <= b for a, b in zip(best, best[1:]))


def test_survivors_are_not_retrained(split):
    calls = []
    def counting(model, s):
        calls.append(1)
        return fake_scorer(model, s)
    log = evo.evolve(split, population=6, keep=2, generations=5, scorer=counting)
    assert len(calls) == log["new"].sum()
    assert len(calls) <= 6 + 4 * (6 - 2)  # generation 1, then at most the children of each later generation


def test_same_seed_gives_the_same_run(split):
    a = evo.evolve(split, population=5, keep=2, generations=3, seed=7, scorer=fake_scorer)
    b = evo.evolve(split, population=5, keep=2, generations=3, seed=7, scorer=fake_scorer)
    c = evo.evolve(split, population=5, keep=2, generations=3, seed=8, scorer=fake_scorer)
    assert a.equals(b)
    assert not a.equals(c)


def test_keep_must_be_smaller_than_population(split):
    with pytest.raises(ValueError):
        evo.evolve(split, population=3, keep=3, generations=1, scorer=fake_scorer)


def test_real_loop_runs_and_beats_its_first_generation(split):
    log = evo.evolve(split, population=4, keep=2, generations=3)
    summary = evo.generation_summary(log)
    assert 0 < summary["best"].iloc[-1] <= 1
    assert summary["best"].iloc[-1] >= summary["best"].iloc[0]


def test_to_web_matches_the_site_format(split):
    log = evo.evolve(split, population=6, keep=3, generations=4, scorer=fake_scorer)
    web = evo.to_web(log, {"label": "Default decision tree", "score": 0.772}, keep=3, sample_size=20000)
    assert web["baseline"]["score"] == 0.772 and web["population"] == 6 and web["keep"] == 3
    assert len(web["generations"]) == 4
    for g in web["generations"]:
        assert g["worst"] <= g["median"] <= g["best"] <= 1.5
        assert len(g["top"]) == 3
        assert {"n_estimators", "max_depth", "min_samples_leaf"} <= g["top"][0]["params"].keys()
