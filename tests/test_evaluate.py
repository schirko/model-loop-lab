"""Tests for src/evaluate.py.

These use a small made-up dataset so they run in a second and never
download the real Covertype data.
"""

import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier

from src import evaluate as ev


@pytest.fixture
def small_data():
    """1,000 rows, 3 classes with one rare class, shaped like Covertype."""
    X, y = make_classification(
        n_samples=1000, n_features=8, n_informative=5, n_classes=3,
        weights=[0.6, 0.35, 0.05], random_state=0,
    )
    X = pd.DataFrame(X, columns=[f"f{i}" for i in range(8)])
    y = pd.Series(y + 1, name="cover_type")
    return X, y


def test_sample_has_requested_size_and_keeps_class_shares(small_data):
    X, y = small_data
    X_s, y_s = ev.stratified_sample(X, y, size=400, seed=1)
    assert len(X_s) == len(y_s) == 400
    full = y.value_counts(normalize=True)
    part = y_s.value_counts(normalize=True)
    for cls in full.index:
        assert part[cls] == pytest.approx(full[cls], abs=0.01)


def test_sample_is_repeatable_with_same_seed(small_data):
    X, y = small_data
    a, _ = ev.stratified_sample(X, y, size=300, seed=7)
    b, _ = ev.stratified_sample(X, y, size=300, seed=7)
    c, _ = ev.stratified_sample(X, y, size=300, seed=8)
    assert a.equals(b)
    assert not a.equals(c)


def test_sample_larger_than_data_returns_everything(small_data):
    X, y = small_data
    X_s, y_s = ev.stratified_sample(X, y, size=5000)
    assert len(X_s) == len(X)


def test_split_sizes_and_no_overlap(small_data):
    X, y = small_data
    split = ev.make_split(X, y, test_size=0.25, seed=3)
    assert len(split.X_test) == 250
    assert len(split.X_train) == 750
    assert set(split.X_train.index).isdisjoint(split.X_test.index)
    assert split.y_test.nunique() == 3, "rare class must appear in the test set"


def test_evaluate_returns_accuracy_between_0_and_1(small_data):
    split = ev.make_split(*small_data)
    score = ev.evaluate(DecisionTreeClassifier(random_state=0), split)
    assert 0.0 <= score <= 1.0
    assert isinstance(score, float)


def test_evaluate_beats_guessing_the_most_common_class(small_data):
    split = ev.make_split(*small_data)
    tree = ev.evaluate(DecisionTreeClassifier(random_state=0), split)
    guess = ev.evaluate(DummyClassifier(strategy="most_frequent"), split)
    assert tree > guess


def test_evaluate_does_not_change_the_model_passed_in(small_data):
    split = ev.make_split(*small_data)
    model = DecisionTreeClassifier(random_state=0)
    ev.evaluate(model, split)
    assert not hasattr(model, "tree_"), "the original model should stay unfitted"


def test_evaluate_is_repeatable(small_data):
    split = ev.make_split(*small_data)
    model = DecisionTreeClassifier(random_state=0)
    assert ev.evaluate(model, split) == ev.evaluate(model, split)


def test_load_covertype_samples_and_names_label(monkeypatch, small_data, tmp_path):
    X, y = small_data

    class FakeBunch:
        data = X
        target = y.rename("Cover_Type")

    calls = {}

    def fake_fetch(data_home, as_frame):
        calls["data_home"] = data_home
        return FakeBunch()

    monkeypatch.setattr(ev, "fetch_covtype", fake_fetch)
    X_s, y_s = ev.load_covertype(sample_size=200, data_home=tmp_path)
    assert len(X_s) == 200
    assert y_s.name == "cover_type"
    assert calls["data_home"] == str(tmp_path)

    X_all, _ = ev.load_covertype(sample_size=None, data_home=tmp_path)
    assert len(X_all) == len(X)


def test_cover_type_names_cover_all_seven():
    assert sorted(ev.COVER_TYPES) == [1, 2, 3, 4, 5, 6, 7]


def test_fit_predict_matches_evaluate(small_data):
    split = ev.make_split(*small_data)
    model = DecisionTreeClassifier(random_state=0)
    fitted, preds = ev.fit_predict(model, split)
    assert len(preds) == len(split.y_test)
    assert (preds == split.y_test).mean() == pytest.approx(ev.evaluate(model, split))
    assert not hasattr(model, "tree_")


def test_cover_type_report_counts_and_rates():
    y_true = pd.Series([1, 1, 1, 2, 2, 7])
    y_pred = pd.Series([1, 1, 2, 2, 1, 7])
    report = ev.cover_type_report(y_true, y_pred)
    assert list(report.index) == list(ev.COVER_TYPES.values())
    spruce = report.loc["Spruce/fir"]
    assert spruce["plots"] == 3 and spruce["correct"] == 2
    assert spruce["recall"] == pytest.approx(2 / 3)
    assert spruce["precision"] == pytest.approx(2 / 3)
    assert report.loc["Krummholz", "recall"] == 1.0
    assert report["correct"].sum() == 4
    # a type with no plots and no predictions has no rates, not an error
    assert pd.isna(report.loc["Aspen", "recall"])
