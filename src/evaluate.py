"""Shared data loading and scoring for every Model Loop Lab experiment.

Every notebook gets its data and its scores from here, so all results on
the site are measured the same way:

* the same 20,000-plot sample of the Forest Covertype data,
* the same split into training plots and held-out test plots,
* the same score: accuracy on the held-out plots.

Typical use in a notebook:

    from src.evaluate import load_covertype, make_split, evaluate
    X, y = load_covertype()
    split = make_split(X, y)
    score = evaluate(DecisionTreeClassifier(random_state=42), split)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.base import clone
from sklearn.datasets import fetch_covtype
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_HOME = PROJECT_ROOT / "data"

SEED = 42            # one seed for every random step, so results repeat exactly
SAMPLE_SIZE = 20_000  # plots used by the experiments (the full set has 581,012)
TEST_SIZE = 0.25      # share of the sample held out for scoring

# The seven forest cover types, by the number the dataset uses for each.
COVER_TYPES = {
    1: "Spruce/fir",
    2: "Lodgepole pine",
    3: "Ponderosa pine",
    4: "Cottonwood/willow",
    5: "Aspen",
    6: "Douglas-fir",
    7: "Krummholz",
}


@dataclass(frozen=True)
class Split:
    """Training plots and held-out test plots, kept together."""

    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def stratified_sample(
    X: pd.DataFrame, y: pd.Series, size: int = SAMPLE_SIZE, seed: int = SEED
) -> tuple[pd.DataFrame, pd.Series]:
    """Take `size` rows while keeping each cover type's share the same.

    Stratifying matters here because some cover types are rare. A plain
    random sample could leave the rarest one with almost no rows.
    """
    if size >= len(X):
        return X.reset_index(drop=True), y.reset_index(drop=True)
    X_s, _, y_s, _ = train_test_split(
        X, y, train_size=size, stratify=y, random_state=seed
    )
    return X_s.reset_index(drop=True), y_s.reset_index(drop=True)


def load_covertype(
    sample_size: int | None = SAMPLE_SIZE,
    seed: int = SEED,
    data_home: Path | str = DATA_HOME,
) -> tuple[pd.DataFrame, pd.Series]:
    """Load the Forest Covertype data as a table of features and a label column.

    The first call downloads about 11 MB into the project's data/ folder.
    Later calls read the saved copy. Pass sample_size=None for all 581,012 plots.
    """
    bunch = fetch_covtype(data_home=str(data_home), as_frame=True)
    X = bunch.data
    y = bunch.target.rename("cover_type")
    if sample_size is None:
        return X, y
    return stratified_sample(X, y, size=sample_size, seed=seed)


def make_split(
    X: pd.DataFrame, y: pd.Series, test_size: float = TEST_SIZE, seed: int = SEED
) -> Split:
    """Split plots into training and held-out test sets, stratified by cover type."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=seed
    )
    return Split(X_train, X_test, y_train, y_test)


def evaluate(model, split: Split) -> float:
    """Train a fresh copy of `model` on the training plots and return its
    accuracy on the held-out plots (0 to 1).

    A copy is trained so the model passed in is never changed. That lets the
    same settings be scored again and again without results leaking between runs.
    """
    fitted = clone(model).fit(split.X_train, split.y_train)
    return float(accuracy_score(split.y_test, fitted.predict(split.X_test)))
