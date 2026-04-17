#!/usr/bin/env python3
"""
run_waka_everywhere.py — Recursively runs WaKa.py on every file and folder in the repository, mirroring results into internet_2.9/ as an alien internet index.

- For each file/folder, runs WaKa.py and saves output (if any) in the corresponding internet_2.9/ path.
- Skips the internet_2.9/ folder itself to avoid recursion.
- Can be run anytime to refresh the alien internet.
"""
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INTERNET_ROOT = REPO_ROOT / "internet_2.9"
WAKA = REPO_ROOT / "WaKa.py"


def run_waka_on(path, outdir):
    """Run WaKa.py on a file or folder, save output to outdir. Overwrite WaKa.py with the latest version before each run."""
    try:
        # Overwrite WaKa.py with the latest version from the repo root (simulate rewrite each pass)
        waka_source = REPO_ROOT / "WaKa.py"
        waka_target = WAKA
        with open(waka_source, "r") as src, open(waka_target, "w") as dst:
            dst.write(src.read())
        # Ensure WaKa.py is executable
        try:
            os.chmod(waka_target, 0o755)
        except PermissionError:
            print(f"Warning: Could not set executable permission for {waka_target}")
        result = subprocess.run([
            str(WAKA), str(path)
        ], capture_output=True, text=True, check=True)
        outdir.mkdir(parents=True, exist_ok=True)
        outfile = outdir / (path.name + ".waka.txt")
        with open(outfile, "w") as f:
            f.write(result.stdout)
    except PermissionError as e:
        print(f"Permission error: {e} (path: {path})")
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e} (path: {path})")

def recurse_and_run_waka(current, outdir):
    if current.name == "internet_2.9":
        return
    if current.is_dir():
        for child in current.iterdir():
            recurse_and_run_waka(child, outdir / child.name)
    else:
        run_waka_on(current, outdir)

if __name__ == "__main__":
    recurse_and_run_waka(REPO_ROOT, INTERNET_ROOT)
    print("WaKa.py run on all files. Alien internet refreshed.")
