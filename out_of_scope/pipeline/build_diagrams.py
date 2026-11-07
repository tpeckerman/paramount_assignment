#!/usr/bin/env python3
"""Draw the Task 2 process diagram as an SVG and a one-page viewer.

The diagram is drawn by hand-placed coordinates, not by a layout tool. An automatic layout
(mermaid) kept routing arrows around the outside of the lanes and crossing them, which made
the flow unreadable. Placing the boxes ourselves keeps each lane in one row.

  python out_of_scope/pipeline/build_diagrams.py            write docs/process_diagram.svg and docs/diagrams.html
  python out_of_scope/pipeline/build_diagrams.py --check    build in memory, fail if the SVG is not valid XML
"""
from __future__ import annotations

import pathlib
import re
import sys
import xml.dom.minidom as minidom
from xml.sax.saxutils import escape

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import constants as C  # noqa: E402

OUT_DIR = C.DOCS_DIR
W, H = 1400, 1010

STYLE = {
    "llm": ("#eaf0ff", "#2f5fe0", 2.5),
    "code": ("#ffffff", "#9aa0ab", 1.5),
    "person": ("#ffffff", "#111318", 2.5),
    "store": ("#f4f5f7", "#6b7280", 1.5),
    "out": ("#ffffff", "#2f5fe0", 2.5),
}


def build_svg() -> str:
    o: list[str] = []

    def text(x, y, lines, size=13, anchor="middle", weight="normal", fill="#1f2328"):
        lines = lines if isinstance(lines, list) else [lines]
        y0 = y - (len(lines) - 1) * (size + 3) / 2
        for i, ln in enumerate(lines):
            o.append(f'<text x="{x}" y="{y0 + i * (size + 3) + size * 0.35:.1f}" '
                     f'text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" '
                     f'fill="{fill}">{escape(ln)}</text>')

    def box(cx, cy, w, h, lines, kind, rounded=False):
        f, s, sw = STYLE[kind]
        r = 18 if rounded else 2
        o.append(f'<rect x="{cx - w/2}" y="{cy - h/2}" width="{w}" height="{h}" rx="{r}" '
                 f'fill="{f}" stroke="{s}" stroke-width="{sw}"/>')
        text(cx, cy, lines)

    def diamond(cx, cy, hw, hh, lines, kind):
        f, s, sw = STYLE[kind]
        o.append(f'<polygon points="{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}" '
                 f'fill="{f}" stroke="{s}" stroke-width="{sw}"/>')
        text(cx, cy, lines)

    def lane(x, y, w, h, title):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fcfcfb" '
                 f'stroke="#c4c7cc" stroke-width="1.2"/>')
        text(x + 14, y + 20, title, size=13, anchor="start", weight="bold", fill="#444")

    def line(points, label=None, lx=None, ly=None, arrow=True, anchor="middle"):
        d = "M " + " L ".join(f"{px},{py}" for px, py in points)
        mk = ' marker-end="url(#a)"' if arrow else ""
        o.append(f'<path d="{d}" fill="none" stroke="#5b6068" stroke-width="1.6"{mk}/>')
        if label:
            text(lx, ly, label, size=12, anchor=anchor, fill="#333")

    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
             f'font-family="Helvetica, Arial, sans-serif">')
    o.append('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
             'markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
             'fill="#5b6068"/></marker></defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')

    # lanes
    lane(20, 20, 1360, 230, "1. KEEP THE RULES CURRENT: a law changes or a regulator publishes a decision")
    lane(20, 270, 1040, 210, "2. DESCRIBE A NEW PROGRAM")
    lane(20, 510, 1040, 300, "3. DECIDE")

    # lane 1
    box(135, 130, 190, 70, ["Signal: a source file", "changed (fingerprint check)"], "code")
    diamond(370, 130, 115, 72, ["Does it change a rule", "or add a precedent?", "(small model)"], "llm")
    box(640, 130, 200, 80, ["Model drafts the rule", "update, or logs", "the decision"], "llm")
    box(910, 130, 220, 80, ["Check: quote matches source.", "Expert signs off", "judgment rules"], "person")
    box(370, 228, 70, 28, ["End"], "store", rounded=True)
    line([(230, 130), (255, 130)])
    line([(485, 130), (540, 130)], "yes", 512, 118)
    line([(740, 130), (800, 130)])
    line([(1020, 130), (1090, 130)])
    line([(370, 202), (370, 214)], "no", 384, 208, anchor="start")

    # rules store
    o.append('<path d="M1090,85 L1090,175 A140,16 0 0 0 1370,175 L1370,85 A140,16 0 0 0 1090,85 '
             'A140,16 0 0 0 1370,85" fill="#f4f5f7" stroke="#6b7280" stroke-width="1.5"/>')
    text(1230, 128, ["RULES TABLE, DECISIONS TABLE,", "TIMELINE", "approved entries only, numbered versions"])

    # lane 2
    box(105, 375, 130, 70, ["Program", "comes in"], "code")
    box(315, 375, 190, 80, ["Split into segments", "at scene changes,", "about 10 minutes at most"], "code")
    box(565, 375, 210, 90, ["Model watches each segment", "and writes a description", "with timecodes"], "llm")
    diamond(860, 375, 130, 82, ["Embed it. Close match", "in the cache?", "(cosine + ROUGE-L,", "high bar)"], "code")
    line([(170, 375), (220, 375)])
    line([(410, 375), (460, 375)])
    line([(670, 375), (730, 375)])

    # cache column
    o.append('<rect x="1090" y="270" width="280" height="520" rx="10" fill="#f4f5f7" '
             'stroke="#6b7280" stroke-width="1.5"/>')
    text(1230, 296, "DECISION CACHE", size=14, weight="bold")
    text(1108, 410, ["Key: embedding of the description,", "plus country and channel",
                     "", "Match: cosine similarity and", "ROUGE-L, both above a high bar",
                     "", "Each row stores the answer and the", "rules and past decisions it used",
                     "", "A row is removed when any of those", "changes or is replaced"],
         size=12.5, anchor="start")
    line([(990, 375), (1090, 375)], "look up", 1040, 362)
    line([(1330, 190), (1330, 270)], "removes cache rows that", 1318, 222, anchor="end")
    text(1318, 238, "used a changed rule or decision", size=12, anchor="end", fill="#333")

    # lane 3
    diamond(150, 620, 120, 76, ["Contains sex, violence or", "another category that", "needs checking?"], "code")
    box(425, 620, 210, 90, ["Code gathers the relevant", "rules and similar past", "regulator decisions"], "code")
    box(695, 620, 230, 90, ["Model answers: when it can", "be shown, with reasoning", "and a confidence score"], "llm")
    diamond(930, 620, 90, 66, ["Confidence", "below X?"], "code")
    box(930, 740, 180, 70, ["Compliance reviewer", "decides"], "person")
    line([(270, 620), (320, 620)], "yes", 295, 608)
    line([(530, 620), (580, 620)])
    line([(810, 620), (840, 620)])
    line([(930, 686), (930, 705)], "yes", 944, 696, anchor="start")

    # flows between lanes
    line([(860, 457), (860, 492), (150, 492), (150, 544)], "no match", 500, 484)
    line([(1090, 165), (1040, 165), (1040, 535), (425, 535), (425, 575)],
         "rules and past decisions", 760, 528)

    # answer
    box(1230, 900, 280, 80, ["ANSWER", "rating, hours, conditions,", "each with its rule"], "out")
    line([(150, 696), (150, 905), (1090, 905)], "no", 164, 760, anchor="start")
    line([(1020, 620), (1050, 620), (1050, 905)], "no", 1062, 640, anchor="start")
    line([(1020, 740), (1050, 740)], arrow=False)
    line([(1150, 860), (1150, 790)], "store answer", 1138, 828, anchor="end")
    line([(1310, 790), (1310, 860)], ["match:", "reuse answer"], 1322, 828, anchor="start")
    o.append('<circle cx="1050" cy="740" r="3.5" fill="#5b6068"/>')

    # legend
    lx, ly = 40, 975
    for i, (kind, label) in enumerate([("llm", "Model"), ("code", "Code"), ("person", "Person")]):
        f, s, sw = STYLE[kind]
        o.append(f'<rect x="{lx + i*110}" y="{ly-10}" width="22" height="16" fill="{f}" '
                 f'stroke="{s}" stroke-width="{sw}"/>')
        text(lx + i*110 + 30, ly - 2, label, size=13, anchor="start")
    o.append("</svg>")
    return "\n".join(o)


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
<p class="hint">Drawn by out_of_scope/pipeline/build_diagrams.py. Each diagram scrolls
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
    svg = build_svg()
    try:
        minidom.parseString(svg)
    except Exception as e:  # noqa: BLE001
        print(f"process diagram is not valid SVG: {e}")
        return 1
    if "--check" in sys.argv:
        print("1 diagram(s) build.")
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale in OUT_DIR.glob("diagram_*.svg"):
        stale.unlink()
    dest = OUT_DIR / "diagram_1_process.svg"
    dest.write_text(svg, encoding="utf-8")
    viewer = write_viewer([("process diagram", svg)])
    print(f"  wrote   {dest.name}\n  wrote   {viewer.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
