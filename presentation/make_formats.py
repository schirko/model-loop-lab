"""Turn the PowerPoint deck into the other published formats.

Input:  presentation/out/model-loop-lab-story.pptx  (from presentation/build_deck.js)
Output, in site/presentation/ (the build publishes this folder with the site):
    model-loop-lab-story.pptx          editable PowerPoint with speaker notes
    model-loop-lab-story.pdf           for reading or printing
    model-loop-lab-story-slides.zip    every slide as a PNG
    model-loop-lab-story.html          one self-contained web page that works offline
    cover.png                          the first slide, for the overview page thumbnail
    deck.json                          slide count and file sizes, read by the overview page

Needs LibreOffice and Poppler (pdftoppm). Every format comes from the one .pptx,
so they always match.

Run from the project root:
    python presentation/make_formats.py
"""

from __future__ import annotations

import base64
import html
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "presentation" / "out" / "model-loop-lab-story.pptx"
OUT = ROOT / "site" / "presentation"
STEM = "model-loop-lab-story"
sys.path.insert(0, str(ROOT / "scripts"))
from build_site import add_portfolio_chrome  # noqa: E402  (same back bar as every page)


def speaker_notes(pptx: Path) -> list[str]:
    from pptx import Presentation
    deck = Presentation(str(pptx))
    return [s.notes_slide.notes_text_frame.text if s.has_notes_slide else "" for s in deck.slides]


def to_pdf(pptx: Path, out_dir: Path) -> Path:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    helper = Path(__import__("os").environ.get("SOFFICE_HELPER", ""))
    cmd = ([sys.executable, str(helper)] if helper.is_file() else [soffice])
    subprocess.run(cmd + ["--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(pptx)],
                   check=True, capture_output=True)
    return out_dir / f"{pptx.stem}.pdf"


def to_pngs(pdf: Path, out_dir: Path) -> list[Path]:
    subprocess.run(["pdftoppm", "-png", "-scale-to-x", "1920", "-scale-to-y", "-1", str(pdf), str(out_dir / "slide")], check=True)
    pngs = sorted(out_dir.glob("slide-*.png"))
    for i, p in enumerate(pngs, 1):
        p.rename(out_dir / f"slide-{i:02d}.png")
    return sorted(out_dir.glob("slide-*.png"))


HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Can AI build better AI? - Model Loop Lab presentation</title>
<style>
  :root {{ --bg: #141916; --panel: #1c231f; --ink: #eef1ec; --ink2: #c1c9c2; --accent: #7cc39d; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
  .deck {{ max-width: 1200px; margin: 0 auto; padding: 16px; }}
  .stage {{ position: relative; aspect-ratio: 16 / 9; background: #000; border-radius: 8px; overflow: hidden; }}
  .stage img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; display: none; }}
  .stage img.on {{ display: block; }}
  .bar {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 12px 0; }}
  button {{ background: var(--panel); color: var(--ink); border: 1px solid #304038; border-radius: 6px; padding: 8px 14px; font: inherit; cursor: pointer; }}
  button:hover {{ border-color: var(--accent); }}
  button:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; }}
  .count {{ color: var(--ink2); font-variant-numeric: tabular-nums; margin-right: auto; }}
  .notes {{ background: var(--panel); border-radius: 8px; padding: 14px 18px; color: var(--ink2); line-height: 1.6; max-width: 80ch; }}
  .notes[hidden] {{ display: none; }}
  .notes strong {{ color: var(--accent); display: block; margin-bottom: 4px; font-size: 0.85rem; }}
  .help {{ color: #8f9a92; font-size: 0.85rem; }}
</style>
</head>
<body>
<main class="deck">
  <div class="stage" id="stage" aria-live="polite">
{slides}
  </div>
  <div class="bar">
    <span class="count" id="count"></span>
    <button id="prev" type="button">Previous</button>
    <button id="next" type="button">Next</button>
    <button id="toggle" type="button" aria-pressed="true">Hide speaker notes</button>
  </div>
  <div class="notes" id="notes"><strong>Speaker notes</strong><span id="note"></span></div>
  <p class="help">Arrow keys move between slides. Press N to show or hide the speaker notes.</p>
</main>
<script>
const notes = {notes};
const imgs = [...document.querySelectorAll("#stage img")];
let i = 0;
function show(k) {{
  i = Math.max(0, Math.min(imgs.length - 1, k));
  imgs.forEach((im, j) => im.classList.toggle("on", j === i));
  document.getElementById("count").textContent = "Slide " + (i + 1) + " of " + imgs.length;
  document.getElementById("note").textContent = notes[i];
}}
document.getElementById("prev").onclick = () => show(i - 1);
document.getElementById("next").onclick = () => show(i + 1);
const box = document.getElementById("notes"), tog = document.getElementById("toggle");
function toggleNotes() {{
  box.hidden = !box.hidden;
  tog.textContent = box.hidden ? "Show speaker notes" : "Hide speaker notes";
  tog.setAttribute("aria-pressed", String(!box.hidden));
}}
tog.onclick = toggleNotes;
document.addEventListener("keydown", (e) => {{
  if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") {{ e.preventDefault(); show(i + 1); }}
  if (e.key === "ArrowLeft" || e.key === "PageUp") {{ e.preventDefault(); show(i - 1); }}
  if (e.key === "n" || e.key === "N") toggleNotes();
}});
show(0);
</script>
</body>
</html>
"""


def to_html(pngs: list[Path], notes: list[str]) -> str:
    slides = "\n".join(
        f'    <img alt="Slide {k}" src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}">'
        for k, p in enumerate(pngs, 1)
    )
    page = HTML.format(slides=slides, notes=json.dumps(notes))
    return add_portfolio_chrome(page)


def human_size(n: int) -> str:
    return f"{n / 1_000_000:.1f} MB" if n >= 1_000_000 else f"{round(n / 1000)} KB"


def main() -> int:
    if not SRC.exists():
        print(f"Build the deck first: node presentation/build_deck.js  (missing {SRC})")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pdf = to_pdf(SRC, tmp)
        pngs = to_pngs(pdf, tmp)
        notes = speaker_notes(SRC)
        if len(notes) != len(pngs):
            print(f"Slide count mismatch: {len(pngs)} images, {len(notes)} notes")
            return 1
        shutil.copy2(SRC, OUT / f"{STEM}.pptx")
        shutil.copy2(pdf, OUT / f"{STEM}.pdf")
        with zipfile.ZipFile(OUT / f"{STEM}-slides.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for p in pngs:
                z.write(p, arcname=f"{STEM}-{p.name}")
        from PIL import Image
        Image.open(pngs[0]).convert("RGB").resize((1200, 675)).save(OUT / "cover.png", optimize=True)
        (OUT / f"{STEM}.html").write_text(to_html(pngs, notes), encoding="utf-8")

    info = {"slides": len(pngs), "sizes": {ext: human_size((OUT / name).stat().st_size) for ext, name in {
        "pdf": f"{STEM}.pdf", "pptx": f"{STEM}.pptx", "html": f"{STEM}.html", "zip": f"{STEM}-slides.zip"}.items()}}
    (OUT / "deck.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print(f"Wrote {len(pngs)} slides to {OUT}")
    print(json.dumps(info["sizes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
