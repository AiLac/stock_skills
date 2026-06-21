#!/usr/bin/env python3
"""Validate report section cross-references in the single-stock-analyze skill.

Every cross-reference of the form  第 N 节「TITLE」  (in SKILL.md, references/*.md,
examples/*.md) must point at the right section: the Nth "## " heading in
assets/stock-verdict-template.md must have a title matching TITLE (compared after
stripping emoji / spaces / punctuation, with substring tolerance for abbreviations).

Run from anywhere:  python scripts/check_section_refs.py
Exit 0 = all consistent; exit 1 = mismatches printed.
"""
from __future__ import annotations
import glob
import os
import re
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(SKILL_DIR, "assets", "stock-verdict-template.md")
REF_RE = re.compile(r"第\s*(\d+)\s*节「([^」]+)」")  # 第 N 节「TITLE」


def norm(s: str) -> str:
    """Keep CJK, latin letters, digits and slash; drop emoji/space/punctuation."""
    return re.sub(r"[^0-9A-Za-z一-鿿/]", "", s)


def canonical_titles(path: str) -> list[str]:
    return [ln[3:].strip() for ln in open(path, encoding="utf-8") if ln.startswith("## ")]


def main() -> int:
    titles = canonical_titles(TEMPLATE)
    canon = [norm(t) for t in titles]
    files = (
        [os.path.join(SKILL_DIR, "SKILL.md")]
        + sorted(glob.glob(os.path.join(SKILL_DIR, "references", "*.md")))
        + sorted(glob.glob(os.path.join(SKILL_DIR, "examples", "*.md")))
    )
    problems = []
    for f in files:
        for ln, line in enumerate(open(f, encoding="utf-8"), 1):
            for m in REF_RE.finditer(line):
                n = int(m.group(1))
                t = norm(m.group(2))
                rel = os.path.relpath(f, SKILL_DIR)
                if not (1 <= n <= len(titles)):
                    problems.append(f"{rel}:{ln} 第{n}节 out of range (1..{len(titles)})")
                elif t not in canon[n - 1] and canon[n - 1] not in t:
                    problems.append(
                        f"{rel}:{ln} 第{n}节「{m.group(2)}」 != template "
                        f"§{n} 「{titles[n - 1]}」"
                    )
    if problems:
        print("SECTION-REF MISMATCHES:")
        for p in problems:
            print("  " + p)
        return 1
    print(f"OK: all 第N节「标题」 refs match the {len(titles)}-section template")
    return 0


if __name__ == "__main__":
    sys.exit(main())
