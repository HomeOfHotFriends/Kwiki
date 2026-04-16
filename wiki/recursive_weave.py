#!/usr/bin/env python3
"""
recursive_weave.py — compatibility shim.

The weave logic has been merged into scripts/wiki_index.py.
Run from the repo root:

    python3 scripts/wiki_index.py --weave [--strict] [--limit N] [--dry-run]

This shim forwards all arguments so existing invocations keep working.
"""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Map old flags to new unified script flags (all are identical)
result = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "wiki_index.py"), "--weave"] + sys.argv[1:],
    cwd=ROOT,
)
sys.exit(result.returncode)
