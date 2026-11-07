#!/usr/bin/env python3
"""Render the diagrams in HOW_IT_WORKS.md to docs/ as pictures.

WHY THIS EXISTS

GitHub draws mermaid diagrams itself when it displays a markdown file, so the diagrams are
already visible in HOW_IT_WORKS.md without this script. What GitHub does not give you is a
picture you can open on its own, drop in a slide, or send to someone who is not going to
browse the repo.

More importantly, it gives no warning when a diagram is broken. A mermaid block with a typo
renders as an error box or as nothing at all, and the markdown around it still looks fine.
Running the real renderer is the only way to find that out, so `--check` does exactly that and
fails the build. It is the same idea as the quote checker: the thing that silently looks fine
is the thing worth testing.

usage:
  python pipeline/build_diagrams.py            write docs/diagram_<n>_<slug>.svg
  python pipeline/build_diagrams.py --check    render only, write nothing, fail on a broken one

Needs mermaid-cli, which comes from npm:  npx @mermaid-js/mermaid-cli
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "HOW_IT_WORKS.md"
OUT_DIR = ROOT / "docs"


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
        proc = subprocess.run(
            ["npx", "--yes", "@mermaid-js/mermaid-cli", "-i", str(src), "-o", str(out)],
            capture_output=True, text=True, timeout=300)
        if proc.returncode != 0 or not out.exists():
            return False, (proc.stderr or proc.stdout or "no output").strip()[-400:]
        if dest is not None:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(out, dest)
        return True, ""


def main() -> int:
    check_only = "--check" in sys.argv
    found = blocks(SOURCE.read_text(encoding="utf-8"))
    if not found:
        print(f"no mermaid blocks in {SOURCE.name}, which is itself suspicious")
        return 1

    failures = []
    for i, (slug, body) in enumerate(found, 1):
        name = f"diagram_{i}_{slug}.svg"
        dest = None if check_only else OUT_DIR / name
        ok, err = render(body, dest)
        if ok:
            print(f"  {'checked' if check_only else 'wrote  '} {name}")
        else:
            failures.append((name, err))
            print(f"  BROKEN  {name}")

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
