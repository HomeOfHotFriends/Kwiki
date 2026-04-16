#!/usr/bin/env python3
"""
fiap_parser.py — recursive descent parser for frog_in_a_pot.txt.

Philosophy (WaKa DOD):
  No classes. Flat parallel arrays.
  Functions consume data, produce data.
  Recursive structure mirrors the document structure.

The document has three levels:
  1. top-level blocks  (Chapter, Epilogue, Back Cover, Tabs, footnotes)
  2. sections          (doubled-title pattern within Chapter One)
  3. beats             (BPM-delineated segments within a section)

Each level is parsed recursively from the level above.
The output is a flat JSON lookup table (LUT) keyed by section_id.

Usage:
  python3 scripts/fiap_parser.py              # write scripts/fiap_lut.json
  python3 scripts/fiap_parser.py --print      # pretty-print summary to stdout
  python3 scripts/fiap_parser.py --concept <id>  # list entries tagged to that concept_id
"""

import json
import re
import sys
from pathlib import Path

ROOT   = Path(__file__).parent.parent
SOURCE = ROOT / "sources" / "text" / "frog_in_a_pot.txt"
OUT    = ROOT / "scripts" / "fiap_lut.json"

# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 1: top-level block boundaries
# A "block" is a named structural unit whose title appears as a lone line
# immediately followed by itself (the doubled-title pattern) OR is one of
# the hard-coded front/back matter labels.
# ─────────────────────────────────────────────────────────────────────────────

FRONT_MATTER_TITLES = {
    "Title", "Dedication", "Epigraph", "Acknowledgements",
    "Introduction",
    "Diagetic Title", "Diegetic Epigraph", "Diegetic Dedication",
    "Diegetic Author's Note",
}

BACK_MATTER_TITLES = {
    "Epilogue", "Back Cover", "Tab 31", "Tab 32",
}

# Type tags for each block
BLOCK_TYPES = {
    "Title":                "front_matter",
    "Dedication":           "front_matter",
    "Epigraph":             "front_matter",
    "Acknowledgements":     "front_matter",
    "Introduction":         "karl_frame",
    "Diagetic Title":       "diegetic_frame",
    "Diegetic Epigraph":    "diegetic_frame",
    "Diegetic Dedication":  "diegetic_frame",
    "Diegetic Author's Note": "diegetic_frame",
    "Chapter One":          "chapter",
    "Chapter Two":          "chapter",
    "Epilogue":             "karl_frame",
    "Back Cover":           "back_matter",
    "Tab 31":               "apparatus",
    "Tab 32":               "apparatus",
}

# Concept tags: which WaKa concept_ids does each block type connect to?
BLOCK_CONCEPT_MAP = {
    "front_matter":     ["frog_in_pot"],
    "karl_frame":       ["frog_in_pot", "content_vs_creative", "shitting_machine"],
    "diegetic_frame":   ["frog_in_pot", "desiring_machine"],
    "chapter":          ["frog_in_pot", "flow_state", "catch22", "content_vs_creative"],
    "back_matter":      ["frog_in_pot", "ira_kotahi"],
    "apparatus":        ["frog_in_pot", "the_law"],
    "section":          ["frog_in_pot", "flow_state", "desiring_machine"],
    "beat":             ["frog_in_pot", "positioning", "enemy_wave"],
    "ed_note":          ["frog_in_pot", "content_vs_creative", "anti_oopedipus"],
    "intercept":        ["frog_in_pot", "catch22", "determinism"],
    "footnote":         ["frog_in_pot", "content_vs_creative"],
}

# Characters in the diegetic layer
CHARACTERS = ["Space Dad", "Gharv Unkle", "Gharv", "Crime Flower",
              "Mr. Fish-With-Legs", "Hat Mang", "Lyle", "The Dicken",
              "Eahrl", "Karl Leisky"]


# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 1 PARSER: split raw lines into named top-level blocks
# ─────────────────────────────────────────────────────────────────────────────

def _slugify(title: str) -> str:
    """Human title → snake_case id."""
    s = re.sub(r"[^a-z0-9]+", "_", title.lower().strip())
    return s.strip("_")


def split_top_level(lines: list[str]) -> list[dict]:
    """
    Scan lines for doubled-title boundaries and front/back matter labels.
    Returns list of block dicts:
      { id, title, type, line_start, line_end, lines }
    line_start / line_end are 1-indexed (matching grep output).
    """
    boundaries = []  # (line_index_0based, title)

    all_known = FRONT_MATTER_TITLES | BACK_MATTER_TITLES | {"Chapter One", "Chapter Two"}

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        # Hard-coded known titles (single occurrence)
        if stripped in all_known:
            # Avoid double-counting if the next line is a duplicate (handled below)
            if i == 0 or lines[i - 1].strip() != stripped:
                boundaries.append((i, stripped))
            continue
        # Footnotes: [1], [2], … at line start
        m = re.match(r"^\[(\d+)\]\s", stripped)
        if m:
            boundaries.append((i, f"footnote_{m.group(1)}"))
            continue
        # Doubled-title: line N == line N+1 (non-empty)
        if i + 1 < len(lines) and lines[i + 1].strip() == stripped and stripped:
            # Only keep the first of the pair
            if not boundaries or boundaries[-1][0] != i - 1:
                boundaries.append((i, stripped))

    # Build block list
    blocks = []
    for idx, (start, title) in enumerate(boundaries):
        end = boundaries[idx + 1][0] - 1 if idx + 1 < len(boundaries) else len(lines) - 1
        btype = BLOCK_TYPES.get(title, "section" if "Chapter" not in title else "chapter")
        block_lines = lines[start: end + 1]
        blocks.append({
            "id":          _slugify(title) if not title.startswith("footnote_") else title,
            "title":       title,
            "type":        btype,
            "line_start":  start + 1,   # 1-indexed
            "line_end":    end + 1,
            "parent":      None,
            "lines":       block_lines,
        })

    return blocks


# ─────────────────────────────────────────────────────────────────────────────
# LEVEL 2 / 3 PARSER: extract beats, ed_notes, intercepts from a named block
# ─────────────────────────────────────────────────────────────────────────────

_BPM_RE      = re.compile(r"^BPM:\s*(.+)$")
_ED_RE       = re.compile(r"\[([^\]]+—Ed\..*?)\]", re.DOTALL)
_INTERCEPT_RE = re.compile(r"^\[(SURVEILLANCE|MAIL|REPORT|THE CENTRE|THE HALLWAY|Transmission)[^]]*\]", re.IGNORECASE)
_FOOTNOTE_RE = re.compile(r"^\[(\d+)\]\s+(.{0,120})")


def extract_beats(block: dict) -> list[dict]:
    """
    Split block lines at BPM markers.
    Returns list of beat dicts: { id, bpm, line_start, line_end, text }
    """
    lines       = block["lines"]
    base        = block["line_start"] - 1
    beats       = []
    current_bpm = None
    beat_start  = 0

    for i, line in enumerate(lines):
        m = _BPM_RE.match(line.strip())
        if m:
            if i > beat_start:
                beats.append({
                    "id":         f"{block['id']}__beat_{len(beats)}",
                    "parent":     block["id"],
                    "type":       "beat",
                    "bpm":        current_bpm,
                    "line_start": base + beat_start + 1,
                    "line_end":   base + i,
                    "text":       " ".join(l.strip() for l in lines[beat_start:i] if l.strip())[:400],
                })
            current_bpm = m.group(1).strip()
            beat_start  = i + 1

    # Trailing beat after last BPM
    if beat_start < len(lines):
        beats.append({
            "id":         f"{block['id']}__beat_{len(beats)}",
            "parent":     block["id"],
            "type":       "beat",
            "bpm":        current_bpm,
            "line_start": base + beat_start + 1,
            "line_end":   base + len(lines),
            "text":       " ".join(l.strip() for l in lines[beat_start:] if l.strip())[:400],
        })

    return beats


def extract_ed_notes(block: dict) -> list[dict]:
    """Extract [—Ed.] editorial asides from a block."""
    full_text = "\n".join(block["lines"])
    notes     = []
    for i, m in enumerate(_ED_RE.finditer(full_text)):
        notes.append({
            "id":     f"{block['id']}__ed_{i}",
            "parent": block["id"],
            "type":   "ed_note",
            "text":   m.group(1).strip()[:300],
        })
    return notes


def extract_intercepts(block: dict) -> list[dict]:
    """Extract [SURVEILLANCE / MAIL / REPORT / …] intercepts."""
    intercepts = []
    base       = block["line_start"] - 1
    for i, line in enumerate(block["lines"]):
        m = _INTERCEPT_RE.match(line.strip())
        if m:
            intercepts.append({
                "id":          f"{block['id']}__intercept_{len(intercepts)}",
                "parent":      block["id"],
                "type":        "intercept",
                "subtype":     m.group(1).upper(),
                "line_start":  base + i + 1,
                "text":        line.strip()[:300],
            })
    return intercepts


def extract_characters(block: dict) -> list[str]:
    """Return which CHARACTERS appear in this block."""
    full = "\n".join(block.get("lines", [])) or block.get("text", "")
    return [c for c in CHARACTERS if c in full]


def tag_concepts(block: dict) -> list[str]:
    """Assign concept_ids based on block type + character presence."""
    concepts = list(BLOCK_CONCEPT_MAP.get(block["type"], ["frog_in_pot"]))
    chars    = extract_characters(block)
    # Space Dad ↔ ira_kotahi (the singular presence)
    if "Space Dad" in chars and "ira_kotahi" not in concepts:
        concepts.append("ira_kotahi")
    # Crime Flower ↔ catch22 (destructive agent)
    if "Crime Flower" in chars and "catch22" not in concepts:
        concepts.append("catch22")
    return concepts


# ─────────────────────────────────────────────────────────────────────────────
# TOP-LEVEL RECURSIVE PARSE
# ─────────────────────────────────────────────────────────────────────────────

def assign_parents(blocks: list[dict]) -> list[dict]:
    """
    Assign each block's parent by line containment.
    Chapters own any section/diegetic block whose line range falls inside them.
    Tab 32 owns footnote blocks.
    Returns the same list with parent fields updated.
    """
    chapters = [b for b in blocks if b["type"] == "chapter"]
    tab32    = next((b for b in blocks if b["id"] == "tab_32"), None)

    for block in blocks:
        if block["type"] in ("section", "diegetic_frame", "apparatus"):
            # already has a parent if it's Tab 31/32 apparatus
            if block["parent"]:
                continue
        if block["id"].startswith("footnote_") and tab32:
            block["parent"] = "tab_32"
            continue
        if block["type"] in ("section", "diegetic_frame"):
            for ch in chapters:
                # section's mid-point falls inside chapter's range
                mid = (block["line_start"] + block["line_end"]) / 2
                # chapters are small (just title), extend them to next chapter start
                # use the chapter that starts immediately before this section
                if ch["line_start"] <= block["line_start"]:
                    block["parent"] = ch["id"]
                    # keep scanning; last matching chapter wins (latest chapter start ≤ section)
    return blocks


def parse_fiap(path: Path) -> dict:
    """
    Recursively parse frog_in_a_pot.txt.
    Returns a flat LUT dict:
      {
        "sections":     { id: entry, … },
        "by_type":      { type: [id, …], … },
        "by_bpm":       { bpm: [id, …], … },
        "by_concept":   { concept_id: [id, …], … },
        "by_character": { character: [id, …], … },
      }
    """
    raw   = path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()

    # Flat output arrays (DOD)
    all_entries  : dict[str, dict] = {}
    by_type      : dict[str, list] = {}
    by_bpm       : dict[str, list] = {}
    by_concept   : dict[str, list] = {}
    by_character : dict[str, list] = {}

    def _register(entry: dict):
        """Register an entry into all parallel indexes."""
        eid = entry["id"]
        if eid in all_entries:           # deduplicate
            entry["id"] = eid + "_b"
            eid         = entry["id"]
        all_entries[eid] = {k: v for k, v in entry.items() if k != "lines"}

        by_type.setdefault(entry.get("type", "unknown"), []).append(eid)

        bpm = entry.get("bpm")
        if bpm:
            by_bpm.setdefault(bpm, []).append(eid)

        for c in entry.get("concepts", []):
            by_concept.setdefault(c, []).append(eid)

        for ch in entry.get("characters", []):
            by_character.setdefault(ch, []).append(eid)

    # ── Level 1: top-level blocks ──
    top_blocks = split_top_level(lines)
    assign_parents(top_blocks)          # assign chapter parents by line containment

    for block in top_blocks:
        block["concepts"]   = tag_concepts(block)
        block["characters"] = extract_characters(block)
        _register(block)

        # ── Level 2 & 3: sub-entries within every named block ──
        # Sections get full beat decomposition; all blocks get ed_notes + intercepts.
        sub_entries: list[dict] = []
        if block["type"] in ("section", "chapter", "karl_frame", "apparatus"):
            sub_entries.extend(extract_beats(block))
        sub_entries.extend(extract_ed_notes(block))
        sub_entries.extend(extract_intercepts(block))

        for sub in sub_entries:
            sub["concepts"]   = tag_concepts(sub)
            sub["characters"] = extract_characters(sub)
            _register(sub)

    return {
        "sections":     all_entries,
        "by_type":      by_type,
        "by_bpm":       by_bpm,
        "by_concept":   by_concept,
        "by_character": by_character,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _print_summary(lut: dict):
    secs = lut["sections"]
    print(f"\nFIAP LUT  —  {len(secs)} entries\n")

    print("By type:")
    for t, ids in sorted(lut["by_type"].items()):
        print(f"  {t:<20} {len(ids):>4}")

    print("\nBy BPM:")
    for bpm, ids in sorted(lut["by_bpm"].items(), key=lambda x: x[0]):
        titles = [secs[i].get("title", i) for i in ids[:3] if i in secs]
        print(f"  {bpm:<30}  → {', '.join(titles)}")

    print("\nBy character:")
    for ch, ids in sorted(lut["by_character"].items(), key=lambda x: -len(x[1])):
        print(f"  {ch:<26} {len(ids):>4} entries")

    print("\nBy concept (top 10 by count):")
    by_c = sorted(lut["by_concept"].items(), key=lambda x: -len(x[1]))[:10]
    for cid, ids in by_c:
        print(f"  {cid:<28} {len(ids):>4} entries")


def main():
    args = sys.argv[1:]

    lut = parse_fiap(SOURCE)

    if "--concept" in args:
        idx = args.index("--concept")
        if idx + 1 < len(args):
            cid  = args[idx + 1]
            ids  = lut["by_concept"].get(cid, [])
            secs = lut["sections"]
            print(f"\nEntries tagged '{cid}'  ({len(ids)} total):\n")
            for eid in ids:
                e = secs.get(eid, {})
                print(f"  [{e.get('line_start','?'):>4}]  {e.get('type','?'):<14}  {e.get('title', eid)}")
        return

    if "--print" in args:
        _print_summary(lut)
        return

    # Default: write JSON
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(lut, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written: {OUT.relative_to(ROOT)}  ({len(lut['sections'])} entries)")
    _print_summary(lut)


if __name__ == "__main__":
    main()
