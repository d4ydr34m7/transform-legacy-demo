#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

DOC_EXTS = {".md", ".txt"}

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def short_summary(text: str, max_lines: int = 12) -> str:
    """
    Cheap summary: pulls headings + first useful lines.
    (Later we can swap in an LLM summary.)
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    picks = []
    for ln in lines:
        if ln.startswith("#") or ln.startswith("##") or ln.lower().startswith(("summary", "overview", "purpose")):
            picks.append(ln)
        if len(picks) >= max_lines:
            break
    if not picks:
        picks = lines[:max_lines]
    return "\n".join(picks)

def main() -> None:
    # You will point this at Transform’s generated documentation folder later
    in_dir = Path(os.environ.get("TRANSFORM_DOCS_DIR", "docs/transform-docs")).resolve()
    out_dir = Path("docs/phase1/out").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not in_dir.exists():
        print(f"[WARN] Input folder not found: {in_dir}")
        print("Set env var TRANSFORM_DOCS_DIR to Transform's documentation output folder.")
        return

    files = [p for p in in_dir.rglob("*") if p.is_file() and p.suffix.lower() in DOC_EXTS]
    if not files:
        print(f"[WARN] No .md/.txt found under: {in_dir}")
        return

    index_lines = ["# Phase 1 Summaries", f"Source: `{in_dir}`", ""]
    for p in sorted(files)[:200]:  # cap to avoid giant runs
        rel = p.relative_to(in_dir)
        text = read_text(p)
        if not text.strip():
            continue
        summ = short_summary(text)
        out_file = out_dir / f"{rel.as_posix().replace('/', '__')}.summary.md"
        out_file.write_text(f"# Summary: {rel}\n\n{summ}\n", encoding="utf-8")
        index_lines.append(f"- {rel} → `{out_file.relative_to(Path.cwd())}`")

    (out_dir / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"[OK] Wrote summaries to: {out_dir}")

if __name__ == "__main__":
    main()
