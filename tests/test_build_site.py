"""Tests for scripts/build_site.py."""

from pathlib import Path

import pytest

import build_site


def test_read_env_skips_comments_and_quotes(tmp_path):
    env = tmp_path / ".env"
    env.write_text('# comment\nSITE_DIR="B:\\Development\\x\\model-loop-lab"\n\nOTHER=1\n', encoding="utf-8")
    values = build_site.read_env(env)
    assert values["SITE_DIR"] == "B:\\Development\\x\\model-loop-lab"
    assert values["OTHER"] == "1"


def test_read_env_missing_file_is_empty(tmp_path):
    assert build_site.read_env(tmp_path / "nope.env") == {}


def test_check_target_refuses_wrong_folder(tmp_path):
    with pytest.raises(SystemExit):
        build_site.check_target(tmp_path / "scott")


def test_build_copies_site_and_overlays_results(tmp_path, monkeypatch):
    src = tmp_path / "site"
    (src / "data").mkdir(parents=True)
    good = "\n".join(build_site.REQUIRED_MARKERS.values())
    (src / "index.html").write_text(good, encoding="utf-8")
    (src / "data" / "evolution.json").write_text('{"sample": true}', encoding="utf-8")
    results = tmp_path / "results" / "web"
    results.mkdir(parents=True)
    (results / "evolution.json").write_text('{"sample": false}', encoding="utf-8")
    monkeypatch.setattr(build_site, "SITE_SRC", src)
    monkeypatch.setattr(build_site, "RESULTS_WEB", results)

    target = tmp_path / "scott" / "model-loop-lab"
    target.parent.mkdir()
    problems = build_site.build(target)

    assert problems == []
    assert (target / "index.html").exists()
    assert '"sample": false' in (target / "data" / "evolution.json").read_text(encoding="utf-8")


def test_check_pages_reports_missing_back_bar(tmp_path):
    (tmp_path / "page.html").write_text("<html></html>", encoding="utf-8")
    problems = build_site.check_pages(tmp_path)
    assert len(problems) == 1 and "back bar" in problems[0]


def test_build_never_touches_portfolio_files(tmp_path, monkeypatch):
    """Standing rule: the build writes only inside scott/model-loop-lab/.
    The portfolio's own index.html and styles.css must be left exactly as they were."""
    src = tmp_path / "site"
    (src / "data").mkdir(parents=True)
    (src / "index.html").write_text("\n".join(build_site.REQUIRED_MARKERS.values()), encoding="utf-8")
    monkeypatch.setattr(build_site, "SITE_SRC", src)
    monkeypatch.setattr(build_site, "RESULTS_WEB", tmp_path / "no-results")

    scott = tmp_path / "scott"
    scott.mkdir()
    (scott / "index.html").write_text("PORTFOLIO PAGE", encoding="utf-8")
    (scott / "styles.css").write_text("PORTFOLIO STYLES", encoding="utf-8")
    before = {p.relative_to(scott) for p in scott.rglob("*")}

    build_site.build(scott / "model-loop-lab")

    assert (scott / "index.html").read_text(encoding="utf-8") == "PORTFOLIO PAGE"
    assert (scott / "styles.css").read_text(encoding="utf-8") == "PORTFOLIO STYLES"
    new = {p.relative_to(scott) for p in scott.rglob("*")} - before
    assert all(p.parts[0] == "model-loop-lab" for p in new), f"wrote outside its folder: {new}"
