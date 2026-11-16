"""Tests for src/web_results.py."""

import json

import pytest

from src.web_results import save_web_result


def test_writes_real_data_with_date(tmp_path):
    path = save_web_result("baseline", {"score": 0.8, "label": "Tree"}, folder=tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert path.name == "baseline.json"
    assert data["sample"] is False
    assert data["score"] == 0.8
    assert len(data["recorded"]) == 10  # YYYY-MM-DD


def test_payload_cannot_mark_itself_as_sample(tmp_path):
    path = save_web_result("baseline", {"sample": True, "score": 0.5}, folder=tmp_path)
    assert json.loads(path.read_text(encoding="utf-8"))["sample"] is False


def test_rejects_names_the_site_does_not_read(tmp_path):
    with pytest.raises(ValueError):
        save_web_result("baselin", {"score": 0.8}, folder=tmp_path)


def test_creates_the_folder(tmp_path):
    target = tmp_path / "results" / "web"
    save_web_result("baseline", {"score": 0.8}, folder=target)
    assert (target / "baseline.json").exists()
