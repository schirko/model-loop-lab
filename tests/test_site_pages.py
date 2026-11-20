"""Checks on the real site/ folder: every page meets the portfolio rules,
and every chart data file has the fields its page reads."""

import json
from pathlib import Path

import pytest

import build_site

SITE = Path(__file__).resolve().parent.parent / "site"
PAGES = sorted(SITE.rglob("*.html"))


@pytest.mark.parametrize("page", PAGES, ids=lambda p: str(p.relative_to(SITE)))
def test_page_has_portfolio_markers(page):
    html = page.read_text(encoding="utf-8")
    assert build_site.missing_markers(html) == []
    assert html.index("sx-backbar") < html.index("<main"), "back bar must come first in <body>"


@pytest.mark.parametrize("page", PAGES, ids=lambda p: str(p.relative_to(SITE)))
def test_crumb_matches_card_name(page):
    assert '<span class="sx-crumb">Model Loop Lab</span>' in page.read_text(encoding="utf-8")


def load(name):
    return json.loads((SITE / "data" / f"{name}.json").read_text(encoding="utf-8"))


def test_evolution_data_shape():
    d = load("evolution")
    assert {"sample", "baseline", "generations"} <= d.keys()
    for g in d["generations"]:
        assert g["worst"] <= g["median"] <= g["best"] <= 1
        assert len(g["top"]) >= 1


def test_search_compare_lines_never_go_down():
    d = load("search_compare")
    for key in ("evolution", "optuna", "random"):
        line = d[key]
        assert len(line) == d["trials"]
        assert all(a <= b for a, b in zip(line, line[1:])), f"{key} best-so-far dropped"


def test_collapse_data_shape():
    d = load("collapse")
    gens = d["generations"]
    assert gens[0]["gen"] == 0
    for g in gens:
        assert 0 <= g["real_test_accuracy"] <= 1
        assert len(g["elevation_hist"]["bins"]) == len(g["elevation_hist"]["counts"])


def test_baseline_data_shape():
    d = load("baseline")
    assert {"sample", "label", "score", "train_score"} <= d.keys()
    assert 0 < d["score"] <= d["train_score"] <= 1



def test_overview_quotes_the_saved_baseline():
    """The overview's baseline must match notebook 01's saved result, when it exists."""
    saved = SITE.parent / "results" / "web" / "baseline.json"
    if not saved.exists():
        pytest.skip("notebook 01 has not saved its baseline yet")
    score = json.loads(saved.read_text(encoding="utf-8"))["score"]
    page = (SITE / "index.html").read_text(encoding="utf-8")
    assert f"{score:.1%}" in page, f"overview should quote the saved baseline {score:.1%}"


def test_overview_has_no_sample_numbers():
    """The overview shows real results only; sample data stays on the experiment pages."""
    page = (SITE / "index.html").read_text(encoding="utf-8")
    assert "data-sample-for" not in page
    assert "86.7%" not in page and "46.0%" not in page



def test_overview_presentation_matches_the_deck():
    """The overview's slide count and download sizes must match the published deck."""
    info_path = SITE / "presentation" / "deck.json"
    if not info_path.exists():
        pytest.skip("presentation not built yet")
    info = json.loads(info_path.read_text(encoding="utf-8"))
    page = (SITE / "index.html").read_text(encoding="utf-8")
    assert f"{info['slides']} slides" in page
    for size in info["sizes"].values():
        assert size in page, f"overview should show the file size {size}"
    for name in ["cover.png", "model-loop-lab-story.pdf", "model-loop-lab-story.pptx",
                 "model-loop-lab-story.html", "model-loop-lab-story-slides.zip"]:
        assert (SITE / "presentation" / name).exists(), name
