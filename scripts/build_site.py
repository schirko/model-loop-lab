"""Publish the Model Loop Lab site into the portfolio folder.

Steps, in order:
1. Copy site/ into SITE_DIR (set in .env).
2. Overlay real results the notebooks wrote: results/web/*.json replace the
   sample data in data/, and results/web/images/*.png go into images/.
3. Publish every notebook that has been run (notebooks/*.ipynb with saved
   outputs) as a web page in notebooks/, with the portfolio back bar.
4. Publish docs/FINDINGS.md as docs/FINDINGS.html, with the back bar.
5. Check every page carries the back bar, favicon and noindex tag.

It writes only inside SITE_DIR and never touches the portfolio's own
index.html or styles.css.

Run from the project root:
    .venv\\Scripts\\python scripts/build_site.py
"""

from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_SRC = ROOT / "site"
RESULTS_WEB = ROOT / "results" / "web"
NOTEBOOKS = ROOT / "notebooks"
DOCS = ROOT / "docs"
SLUG = "model-loop-lab"
PROJECT_NAME = "Model Loop Lab"

REQUIRED_MARKERS = {
    "back bar": "sx-backbar",
    "back bar stylesheet": "/scott/backbar.css",
    "noindex tag": '<meta name="robots" content="noindex, nofollow">',
    "favicon": "/scott/favicon.ico",
}

# The portfolio's shared head links and back bar, exactly as its
# "Adding a project to the portfolio" guide gives them.
HEAD_LINKS = """<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="/scott/backbar.css">
<link rel="icon" href="/scott/favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" sizes="16x16" href="/scott/favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/scott/favicon-32.png">
<link rel="apple-touch-icon" href="/scott/apple-touch-icon.png">"""

BACKBAR = f"""<div class="sx-backbar">
  <a class="sx-back" href="/scott/">
    <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>
    Portfolio
  </a>
  <span class="sx-crumb">{PROJECT_NAME}</span>
  <span class="sx-links"><a href="/scott/{SLUG}/">Overview</a><a href="/scott/{SLUG}/notebooks/">Notebooks</a><a href="https://github.com/schirko/{SLUG}">Code</a></span>
</div>"""


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


def missing_markers(page_html: str) -> list[str]:
    """Return the names of required portfolio markers a page is missing."""
    return [name for name, marker in REQUIRED_MARKERS.items() if marker not in page_html]


def check_pages(folder: Path) -> list[str]:
    """Check every HTML page in folder. Returns a list of problems found."""
    problems = []
    for page in sorted(folder.rglob("*.html")):
        missing = missing_markers(page.read_text(encoding="utf-8"))
        if missing:
            problems.append(f"{page.relative_to(folder)}: missing {', '.join(missing)}")
    return problems


def add_portfolio_chrome(page_html: str) -> str:
    """Put the portfolio head links in <head> and the back bar first in <body>."""
    page_html = re.sub(r"(<head[^>]*>)", lambda m: m.group(1) + "\n" + HEAD_LINKS, page_html, count=1)
    page_html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + BACKBAR, page_html, count=1)
    return page_html


def has_outputs(notebook_path: Path) -> bool:
    """True if the notebook has been run (at least one code cell has output)."""
    nb = json.loads(notebook_path.read_text(encoding="utf-8"))
    return any(c.get("outputs") for c in nb.get("cells", []) if c.get("cell_type") == "code")


def publish_notebooks(site_dir: Path, notebooks: Path = NOTEBOOKS) -> list[str]:
    """Turn every run notebook into a web page in site_dir/notebooks/.

    Notebooks that have not been run yet are skipped, so the site never shows
    a notebook without its results. Returns the names published.
    """
    from nbconvert import HTMLExporter  # only needed here

    exporter = HTMLExporter(template_name="lab")
    out_dir = site_dir / "notebooks"
    out_dir.mkdir(parents=True, exist_ok=True)
    published = []
    for nb_path in sorted(notebooks.glob("[0-9][0-9]_*.ipynb")):
        if not has_outputs(nb_path):
            continue
        body, _ = exporter.from_filename(str(nb_path))
        (out_dir / f"{nb_path.stem}.html").write_text(add_portfolio_chrome(body), encoding="utf-8")
        published.append(nb_path.stem)
    return published


DOC_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - {project}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/scott/{slug}/assets/site.css">
</head>
<body>
<main class="mll-wrap mll-doc">
{body}
</main>
<footer class="mll-foot"><div class="mll-wrap"><p>{project} by Scott Schirkofsky. Part of my <a href="/scott/">project portfolio</a>.</p></div></footer>
</body>
</html>
"""


def publish_docs(site_dir: Path, docs: Path = DOCS) -> list[str]:
    """Turn docs/FINDINGS.md into a web page at site_dir/docs/FINDINGS.html."""
    import markdown  # only needed here

    published = []
    for name in ("FINDINGS",):
        src = docs / f"{name}.md"
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        first = re.search(r"^#\s+(.+)$", text, flags=re.M)
        title = first.group(1).strip() if first else name.title()
        body = markdown.markdown(text, extensions=["tables"])
        page = DOC_PAGE.format(title=html.escape(title), project=PROJECT_NAME, slug=SLUG, body=body)
        out = site_dir / "docs" / f"{name}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(add_portfolio_chrome(page), encoding="utf-8")
        published.append(name)
    return published


def build(site_dir: Path) -> list[str]:
    """Copy the site, overlay real results, publish notebooks and docs,
    and return any page problems."""
    check_target(site_dir)
    if site_dir.exists():
        shutil.rmtree(site_dir)
    shutil.copytree(SITE_SRC, site_dir)

    overlaid = []
    if RESULTS_WEB.exists():
        for result in sorted(RESULTS_WEB.glob("*.json")):
            shutil.copy2(result, site_dir / "data" / result.name)
            overlaid.append(result.name)
    images = []
    if (RESULTS_WEB / "images").exists():
        (site_dir / "images").mkdir(exist_ok=True)
        for png in sorted((RESULTS_WEB / "images").glob("*.png")):
            shutil.copy2(png, site_dir / "images" / png.name)
            images.append(png.name)

    print(f"Published site/ to {site_dir}")
    print("Real results used: " + (", ".join(overlaid) if overlaid else "none yet (sample data)"))
    print("Charts copied: " + (", ".join(images) if images else "none yet"))
    if NOTEBOOKS.exists():
        nbs = publish_notebooks(site_dir)
        print("Notebooks published: " + (", ".join(nbs) if nbs else "none yet (run them first)"))
    if DOCS.exists():
        docs = publish_docs(site_dir)
        print("Docs published: " + (", ".join(docs) if docs else "none"))
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
