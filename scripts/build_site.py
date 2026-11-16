"""Publish the Model Loop Lab site into the portfolio folder.

Copies site/ into SITE_DIR (set in .env), then overlays any real results
the notebooks wrote to results/web/*.json on top of the sample data.
Finally checks every page carries the portfolio back bar and noindex tag.

Run from the project root:
    python scripts/build_site.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_SRC = ROOT / "site"
RESULTS_WEB = ROOT / "results" / "web"
SLUG = "model-loop-lab"

REQUIRED_MARKERS = {
    "back bar": "sx-backbar",
    "back bar stylesheet": "/scott/backbar.css",
    "noindex tag": '<meta name="robots" content="noindex, nofollow">',
    "favicon": "/scott/favicon.ico",
}


def read_env(path: Path) -> dict[str, str]:
    """Read simple KEY=value lines from a .env file. No extra package needed."""
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def check_target(site_dir: Path) -> None:
    """Refuse to wipe a folder that is not this project's portfolio folder."""
    if site_dir.name != SLUG:
        raise SystemExit(
            f"SITE_DIR must end in '{SLUG}' so the build never clears the wrong folder. Got: {site_dir}"
        )
    if not site_dir.parent.exists():
        raise SystemExit(f"The portfolio folder does not exist: {site_dir.parent}")


def missing_markers(html: str) -> list[str]:
    """Return the names of required portfolio markers a page is missing."""
    return [name for name, marker in REQUIRED_MARKERS.items() if marker not in html]


def check_pages(folder: Path) -> list[str]:
    """Check every HTML page in folder. Returns a list of problems found."""
    problems = []
    for page in sorted(folder.rglob("*.html")):
        missing = missing_markers(page.read_text(encoding="utf-8"))
        if missing:
            problems.append(f"{page.relative_to(folder)}: missing {', '.join(missing)}")
    return problems


def build(site_dir: Path) -> list[str]:
    """Copy the site, overlay real results, and return any page problems."""
    check_target(site_dir)
    if site_dir.exists():
        shutil.rmtree(site_dir)
    shutil.copytree(SITE_SRC, site_dir)

    overlaid = []
    if RESULTS_WEB.exists():
        for result in sorted(RESULTS_WEB.glob("*.json")):
            shutil.copy2(result, site_dir / "data" / result.name)
            overlaid.append(result.name)

    print(f"Published site/ to {site_dir}")
    print("Real results used: " + (", ".join(overlaid) if overlaid else "none yet (sample data)"))
    return check_pages(site_dir)


def main() -> int:
    env = read_env(ROOT / ".env")
    if "SITE_DIR" not in env:
        print("SITE_DIR is not set. Copy .env.example to .env and check the path.")
        return 1
    problems = build(Path(env["SITE_DIR"]))
    if problems:
        print("Pages that need fixing:")
        for p in problems:
            print("  " + p)
        return 1
    print("All pages have the back bar, favicon and noindex tag.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
