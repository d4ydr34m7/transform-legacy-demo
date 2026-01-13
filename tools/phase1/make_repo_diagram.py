#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

def main() -> None:
    # Simple module diagram for now; later we can generate deeper call graphs.
    text = """# Repo Diagram (Simple)

```mermaid
flowchart LR
  A[legacy-app] --> B[legacy-wrappers]
  A --> C[JDO annotations]
  B --> D[com.verafin.commons.jdo]
"""
    out = Path("docs/phase1/out/REPO_DIAGRAM.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"[OK] Wrote: {out}")

if __name__ == "__main__":
    main()