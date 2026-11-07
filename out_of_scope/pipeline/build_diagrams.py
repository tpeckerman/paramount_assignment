#!/usr/bin/env python3
"""Render the process diagram in TASK2_SCALING.md to docs/ as a picture.

WHY THIS EXISTS

GitHub draws mermaid diagrams itself when it displays a markdown file, so the diagram is
already visible in TASK2_SCALING.md without this script. What GitHub does not give you is a
picture you can open on its own, drop in a slide, or send to someone who is not going to
browse the repo.

More importantly, it gives no warning when a diagram is broken. A mermaid block with a typo
renders as an error box or as nothing at all, and the markdown around it still looks fine.
Running the real renderer is the only way to find that out, so `--check` does exactly that and
fails the build. It is the same idea as the quote checker: the thing that silently looks fine
is the thing worth testing.

usage:
  python out_of_scope/pipeline/build_diagrams.py            write out_of_scope/docs/diagram_<n>_<slug>.svg
  python out_of_scope/pipeline/build_diagrams.py --check    render only, write nothing, fail on a broken one

Needs mermaid-cli, which comes from npm:  npx @mermaid-js/mermaid-cli
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import constants as C

CONFIG = pathlib.Path(__file__).resolve().parent / "mermaid.config.json"
SOURCE = C.TASK2_MD
OUT_DIR = C.DOCS_DIR


def blocks(text: str) -> list[tuple[str, str]]:
    """Each mermaid block, paired with the nearest heading above it for naming."""
    found = []
    for m in re.finditer(r"```mermaid\n(.*?)```", text, re.S):
        before = text[:m.start()]
        headings = re.findall(r"^#+ (.+)$", before, re.M)
        title = headings[-1] if headings else "diagram"
        slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:40]
        found.append((slug, m.group(1)))
    return found


def render(body: str, dest: pathlib.Path | None) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as td:
        src = pathlib.Path(td) / "d.mmd"
        src.write_text(body, encoding="utf-8")
        out = pathlib.Path(td) / "d.svg"
        # htmlLabels:false is the important one. With HTML labels mermaid puts the text in
        # a <foreignObject>, so the browser re-lays it out at display time using whatever
        # font it has. If that differs at all from the font used when the box was measured,
        # the text overflows a box sized for different metrics and gets clipped, usually by
        # a character or two at the end of a line. Real SVG <text> is measured and
        # positioned once, at render time, and cannot drift afterwards.
        proc = subprocess.run(
            ["npx", "--yes", "@mermaid-js/mermaid-cli",
             "-i", str(src), "-o", str(out), "-c", str(CONFIG)],
            capture_output=True, text=True, timeout=C.RENDER_TIMEOUT_SECONDS)
        if proc.returncode != 0 or not out.exists():
            return False, (proc.stderr or proc.stdout or "no output").strip()[-400:]
        if dest is not None:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(out, dest)
        return True, ""


VIEWER = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Diagrams</title>
<style>
  body {{ font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         margin: 0; padding: 1.5rem; color: #222; background: #fff; }}
  h1 {{ font-size: 1.4rem; margin: 0 0 .3rem; }}
  h2 {{ font-size: 1.1rem; margin: 2rem 0 .5rem; }}
  .hint {{ color: #666; font-size: 13px; margin-bottom: 1.5rem; }}
  .controls {{ position: sticky; top: 0; background: #fff; padding: .5rem 0;
               border-bottom: 1px solid #eee; z-index: 10; }}
  button {{ font: inherit; font-size: 13px; padding: .3rem .7rem; margin-right: .4rem;
            border: 1px solid #ccc; background: #f7f7f5; border-radius: 4px;
            cursor: pointer; }}
  button:hover {{ background: #efefec; }}
  .frame {{ overflow: auto; border: 1px solid #e3e3e0; border-radius: 6px;
            background: #fcfcfb; padding: 1rem; }}
  .frame svg {{ height: auto !important; max-width: none !important;
                width: calc(100% * var(--zoom, 1)); display: block; }}
  /* Most labels render as real SVG text. Mermaid still emits one HTML label per diagram
     inside a foreignObject, sized to the font it measured with. If the viewing font differs
     even slightly the text overflows a box cut to the old metrics and loses its last
     character. Pinning the same font and letting the box overflow removes both halves of
     that: the metrics match, and nothing is clipped if they ever stop matching. */
  .frame foreignObject {{ overflow: visible; }}
  .frame foreignObject div, .frame foreignObject span {{
      font-family: Helvetica, Arial, sans-serif !important;
      overflow: visible !important; }}
  .frame svg text, .frame svg tspan {{
      font-family: Helvetica, Arial, sans-serif !important; }}
</style></head><body>
<h1>How it works, diagrams</h1>
<p class="hint">Generated from the mermaid blocks in out_of_scope/HOW_IT_WORKS.md. Each diagram scrolls
inside its own frame. Use the buttons to change size, or just scroll.</p>
<div class="controls">
  <button onclick="z(0.25)">Bigger</button>
  <button onclick="z(-0.25)">Smaller</button>
  <button onclick="reset()">Fit width</button>
  <span class="hint" id="lvl" style="margin-left:.5rem"></span>
</div>
{body}
<script>
  let zoom = 1;
  function apply() {{
    document.querySelectorAll('.frame').forEach(f => f.style.setProperty('--zoom', zoom));
    document.getElementById('lvl').textContent = Math.round(zoom * 100) + '%';
  }}
  function z(d) {{ zoom = Math.min(6, Math.max(0.5, zoom + d)); apply(); }}
  function reset() {{ zoom = 1; apply(); }}
  apply();
</script>
</body></html>"""


def write_viewer(entries: list[tuple[str, str]]) -> pathlib.Path:
    """One scrollable page holding every diagram, so they can be read at any size.

    The SVGs are embedded rather than linked, so the page is a single file that works
    offline and survives being emailed. Mermaid is not loaded at runtime: the diagrams are
    already rendered, so nothing depends on a CDN being reachable.
    """
    blocks = []
    for title, svg in entries:
        # Strip the XML prolog; an inline <svg> must not carry one.
        svg = re.sub(r"^<\?xml[^>]*\?>\s*", "", svg).strip()
        # Let CSS drive the size instead of the renderer's fixed attributes.
        svg = re.sub(r'(<svg[^>]*?)\sstyle="[^"]*"', r"\1", svg, count=1)
        blocks.append(f"<h2>{title}</h2>\n<div class='frame'>{svg}</div>")
    dest = OUT_DIR / "diagrams.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(VIEWER.format(body="\n".join(blocks)), encoding="utf-8")
    return dest


def main() -> int:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    check_only = "--check" in sys.argv
    found = blocks(SOURCE.read_text(encoding="utf-8"))
    if not found:
        print(f"no mermaid blocks in {SOURCE.name}. Task 2 asks for a process diagram, so "
              f"its absence is a missing deliverable, not a style choice.")
        return 1

    if not check_only:
        # Diagram files are named after their heading, so renaming a heading would
        # otherwise leave the old file sitting in docs/ looking current.
        for stale in OUT_DIR.glob("diagram_*.svg"):
            stale.unlink()

    failures = []
    rendered: list[tuple[str, str]] = []
    for i, (slug, body) in enumerate(found, 1):
        name = f"diagram_{i}_{slug}.svg"
        dest = None if check_only else OUT_DIR / name
        ok, err = render(body, dest)
        if ok:
            print(f"  {'checked' if check_only else 'wrote  '} {name}")
            if dest is not None:
                rendered.append((slug.replace("_", " "),
                                 dest.read_text(encoding="utf-8")))
        else:
            failures.append((name, err))
            print(f"  BROKEN  {name}")

    if rendered:
        viewer = write_viewer(rendered)
        print(f"  wrote   {viewer.name}  (all {len(rendered)} on one scrollable page)")

    if failures:
        print(f"\n{len(failures)} diagram(s) do not render. A broken mermaid block shows as "
              f"an error box on GitHub and the markdown around it still looks fine, which is "
              f"why this is a build failure and not a warning.")
        for name, err in failures:
            print(f"\n  {name}:\n    {err}")
        return 1

    print(f"\n{len(found)} diagram(s) render.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
