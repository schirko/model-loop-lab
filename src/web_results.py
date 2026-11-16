"""Save results where the website can read them.

Notebooks call save_web_result() to write a small JSON file into
results/web/. When scripts/build_site.py runs, those files replace the
sample files in site/data/, and the site's "Sample data" tags disappear
for every chart that now has real numbers.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_WEB = PROJECT_ROOT / "results" / "web"

# File names the site knows how to read. Anything else would never be shown.
SITE_FILES = {"baseline", "evolution", "search_compare", "collapse"}


def save_web_result(name: str, payload: dict, folder: Path | str = RESULTS_WEB) -> Path:
    """Write `payload` to <folder>/<name>.json, marked as real (not sample) data.

    Adds two fields: "sample": false and "recorded": today's date.
    Returns the path written.
    """
    if name not in SITE_FILES:
        raise ValueError(f"'{name}' is not a file the site reads. Use one of: {sorted(SITE_FILES)}")
    if not re.fullmatch(r"[a-z_]+", name):
        raise ValueError(f"Bad result name: {name!r}")
    data = {"sample": False, "recorded": date.today().isoformat(), **payload}
    data["sample"] = False  # a notebook can never publish sample data by accident
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}.json"
    path.write_text(json.dumps(data, indent=1), encoding="utf-8")
    return path
