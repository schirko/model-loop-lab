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
