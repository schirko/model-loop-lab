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
    monkeypatch.setattr(build_site, "NOTEBOOKS", tmp_path / "no-notebooks")
    monkeypatch.setattr(build_site, "DOCS", tmp_path / "no-docs")

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
    monkeypatch.setattr(build_site, "NOTEBOOKS", tmp_path / "no-notebooks")
    monkeypatch.setattr(build_site, "DOCS", tmp_path / "no-docs")

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


def test_add_portfolio_chrome_puts_bar_first_in_body():
    page = "<html><head><title>x</title></head><body class='a'><p>hi</p></body></html>"
    out = build_site.add_portfolio_chrome(page)
    assert build_site.missing_markers(out) == []
    assert out.index("sx-backbar") < out.index("<p>hi</p>")
    assert out.index("/scott/backbar.css") < out.index("</head>")
    assert '<span class="sx-crumb">Model Loop Lab</span>' in out


def _write_notebook(path, with_output):
    import nbformat
    cell = nbformat.v4.new_code_cell("print('hello')")
    if with_output:
        cell.outputs = [nbformat.v4.new_output("stream", name="stdout", text="hello\n")]
    nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell("# Title"), cell])
    nbformat.write(nb, path)


def test_publish_notebooks_skips_unrun_notebooks(tmp_path):
    nbs = tmp_path / "notebooks"
    nbs.mkdir()
    _write_notebook(nbs / "01_run.ipynb", with_output=True)
    _write_notebook(nbs / "02_not_run.ipynb", with_output=False)
    site = tmp_path / "model-loop-lab"
    published = build_site.publish_notebooks(site, notebooks=nbs)
    assert published == ["01_run"]
    page = (site / "notebooks" / "01_run.html").read_text(encoding="utf-8")
    assert build_site.missing_markers(page) == []
    assert "hello" in page
    assert not (site / "notebooks" / "02_not_run.html").exists()


def test_publish_docs_renders_findings(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "FINDINGS.md").write_text("# Findings\n\n| a | b |\n|---|---|\n| 1 | 2 |\n", encoding="utf-8")
    site = tmp_path / "model-loop-lab"
    assert build_site.publish_docs(site, docs=docs) == ["FINDINGS"]
    page = (site / "docs" / "FINDINGS.html").read_text(encoding="utf-8")
    assert build_site.missing_markers(page) == []
    assert "<table>" in page and "<title>Findings - Model Loop Lab</title>" in page
