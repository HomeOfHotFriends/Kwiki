#!/usr/bin/env python3
"""
WaKa.py — the generative vessel.

waka: a canoe. it carries what needs to be carried.
It has no opinion about the cargo. It knows the water.

Philosophy of this file:
  Anti-OOPedipus:  no tree. no hierarchy. no central organ.
                   concepts connect laterally, via whakapapa.
  DOD:             structs of arrays, not arrays of structs.
                   concepts live in flat parallel data indexed by id.
                   functions consume data, produce data. nothing is hidden.
  Māori:           waka = vessel. whakapapa = the graph.
                   mauri = the life-force that makes a thing itself.
                   ira kotahi = the singularity / the law.

The one law:
  EXTREME DEPTH OF THE WHOLE
  ACHIEVED THROUGH
  EXTREME SIMPLICITY OF THE PARTS.

Usage:
  python3 WaKa.py                    # generate page from scripts/user_input.json
  python3 WaKa.py <PageName>         # generate specific page
  python3 WaKa.py --list             # list all known pages and concepts
  python3 WaKa.py --index            # print passage index for all concepts
  python3 WaKa.py --new <PageName>   # scaffold a new user_input.json for a page
  python3 WaKa.py --force            # overwrite existing page without prompting
"""

import json
import os
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL METADATA
# ─────────────────────────────────────────────────────────────────────────────
# DOD: flat parallel arrays. No classes. concept_id is the index key.
# The data IS the model. Functions read it. Nothing is encapsulated.
# ─────────────────────────────────────────────────────────────────────────────

CONCEPT_IDS = [
    "the_law",
    "desiring_machine",
    "anti_oopedipus",
    "dod",
    "whakapapa",
    "rhizome",
    "ira_kotahi",
    "te_whariki_pumotu",
    "esprade",
    "frog_in_pot",
    "flow_state",
    "simplicity_of_parts",
    "enemy_wave",
    "positioning",
    "mauri",
    "tokotoko",
    "catch22",
    "content_vs_creative",
    "shitting_machine",
    "zero_set",
    "taonga",
    "determinism",
    "radiative",
    "singularity",
]

# Parallel array: human-readable name for each concept
CONCEPT_NAMES = {
    "the_law":               "The Law",
    "desiring_machine":      "Desiring-Machine",
    "anti_oopedipus":        "Anti-OOPedipus",
    "dod":                   "Data-Oriented Design",
    "whakapapa":             "Whakapapa",
    "rhizome":               "Rhizome",
    "ira_kotahi":            "Ira Kotahi",
    "te_whariki_pumotu":     "Te Whariki Pumotu",
    "esprade":               "Esp Ra De",
    "frog_in_pot":           "Frog In A Pot",
    "flow_state":            "Flow State",
    "simplicity_of_parts":   "Simplicity of Parts",
    "enemy_wave":            "Enemy Wave",
    "positioning":           "Positioning",
    "mauri":                 "Mauri",
    "tokotoko":              "Tokotoko",
    "catch22":               "Catch-22",
    "content_vs_creative":   "Content vs Creative Product",
    "shitting_machine":      "Shitting Machine",
    "zero_set":              "Zero Set",
    "taonga":                "Taonga",
    "determinism":           "Determinism",
    "radiative":             "Radiative",
    "singularity":           "Singularity / Ira Kotahi",
}

# Parallel array: whakapapa links (lateral, not hierarchical).
# These are NOT parent-child. They are tupuna — the concepts this one
# came from, reaches toward, or is inseparable from.
WHAKAPAPA = {
    "the_law":             ["simplicity_of_parts", "esprade", "dod", "taonga", "mauri"],
    "desiring_machine":    ["anti_oopedipus", "shitting_machine", "flow_state", "rhizome"],
    "anti_oopedipus":      ["desiring_machine", "rhizome", "catch22", "dod", "shitting_machine"],
    "dod":                 ["te_whariki_pumotu", "simplicity_of_parts", "zero_set", "enemy_wave", "the_law"],
    "whakapapa":           ["mauri", "ira_kotahi", "rhizome", "the_law"],
    "rhizome":             ["anti_oopedipus", "whakapapa", "te_whariki_pumotu", "desiring_machine"],
    "ira_kotahi":          ["mauri", "tokotoko", "whakapapa", "singularity"],
    "te_whariki_pumotu":   ["dod", "zero_set", "whakapapa", "mauri"],
    "esprade":             ["simplicity_of_parts", "enemy_wave", "positioning", "the_law", "determinism"],
    "frog_in_pot":         ["esprade", "flow_state", "content_vs_creative", "catch22"],
    "flow_state":          ["desiring_machine", "shitting_machine", "catch22", "esprade"],
    "simplicity_of_parts": ["the_law", "dod", "enemy_wave", "esprade"],
    "enemy_wave":          ["esprade", "positioning", "simplicity_of_parts", "dod"],
    "positioning":         ["esprade", "enemy_wave", "dod", "the_law"],
    "mauri":               ["ira_kotahi", "whakapapa", "te_whariki_pumotu", "taonga"],
    "tokotoko":            ["ira_kotahi", "mauri", "anti_oopedipus", "singularity"],
    "catch22":             ["flow_state", "content_vs_creative", "anti_oopedipus"],
    "content_vs_creative": ["catch22", "flow_state", "frog_in_pot", "radiative"],
    "shitting_machine":    ["desiring_machine", "flow_state", "anti_oopedipus"],
    "zero_set":            ["te_whariki_pumotu", "dod", "simplicity_of_parts"],
    "taonga":              ["the_law", "mauri", "whakapapa"],
    "determinism":         ["esprade", "dod", "positioning", "the_law"],
    "radiative":           ["content_vs_creative", "dod", "the_law"],
    "singularity":         ["ira_kotahi", "tokotoko", "mauri"],
}

# Parallel array: typographic voice (from source document)
# 0 = title    (Old Standard TT)  — declarations, the law, taonga
# 1 = body     (PT Serif)         — analysis, sustained thought
# 2 = gloss    (IBM Plex Mono)    — technical, code, annotation
# 3 = raw      (Arial)            — transcript voice, unedited
CONCEPT_VOICE = {
    "the_law":             0,
    "desiring_machine":    1,
    "anti_oopedipus":      0,
    "dod":                 2,
    "whakapapa":           1,
    "rhizome":             1,
    "ira_kotahi":          0,
    "te_whariki_pumotu":   2,
    "esprade":             3,
    "frog_in_pot":         3,
    "flow_state":          1,
    "simplicity_of_parts": 0,
    "enemy_wave":          2,
    "positioning":         2,
    "mauri":               1,
    "tokotoko":            1,
    "catch22":             3,
    "content_vs_creative": 1,
    "shitting_machine":    3,
    "zero_set":            2,
    "taonga":              0,
    "determinism":         2,
    "radiative":           1,
    "singularity":         0,
}

# Parallel array: keywords for passage extraction from source corpus
CONCEPT_KEYWORDS = {
    "the_law":             ["one law", "taonga", "most precious stone", "extreme depth", "extreme simplicity"],
    "desiring_machine":    ["desiring", "desire", "machine", "production", "product-cycle", "flow-state"],
    "anti_oopedipus":      ["anti-oedipus", "oedipus", "genealogical", "prohibition", "Deleuze", "Guattari"],
    "dod":                 ["data-oriented", "DOD", "spawning system", "design rules", "flat", "struct of arrays"],
    "whakapapa":           ["whakapapa", "genealogy", "tupuna", "ancestor"],
    "rhizome":             ["rhizome", "rhizomatic", "lateral", "flat hierarchy"],
    "ira_kotahi":          ["ira kotahi", "singularity", "motuhake", "mana motuhake"],
    "te_whariki_pumotu":   ["Te_Whariki_Pumotu", "namespace", "zero_set", "whakatakoto", "pānui"],
    "esprade":             ["esp ra de", "esprade", "CAVE", "DDP", "DoDonPachi", "shmup"],
    "frog_in_pot":         ["frog in a pot", "frog", "Chad Wife", "album"],
    "flow_state":          ["flow", "flow-state", "engagement", "focus", "ADHD"],
    "simplicity_of_parts": ["simplicity of the parts", "extreme simplicity", "simple programming", "simple parts"],
    "enemy_wave":          ["enemy wave", "wave", "spawn", "obstacle", "encounter"],
    "positioning":         ["positioning", "position", "x axis", "y axis", "pixel position"],
    "mauri":               ["mauri", "life force", "mauri tūturu"],
    "tokotoko":            ["tokotoko", "walking stick", "gap-filler"],
    "catch22":             ["catch 22", "catch-22", "Yossarian", "Heller"],
    "content_vs_creative": ["content", "creative product", "M-C-M", "bandcamp", "art"],
    "shitting_machine":    ["shitting machine", "shit machine", "shitting", "tautology"],
    "zero_set":            ["zero_set", "pūwāhi_kau", "pūtake_aukati", "enum"],
    "taonga":              ["taonga", "precious stone", "gift", "treasure"],
    "determinism":         ["deterministic", "determinism", "run-to-run", "seed"],
    "radiative":           ["radiative", "Radiative", "design thinking", "adaptive systems"],
    "singularity":         ["singularity", "ira kotahi", "singular", "te mutunga"],
}

# Page registry: page slug -> primary concept cluster
# ordered: first concept is the page's mauri (core identity)
PAGE_REGISTRY = {
    "The-Law":           ["the_law", "simplicity_of_parts", "taonga", "mauri", "ira_kotahi"],
    "Anti-OOPedipus":    ["anti_oopedipus", "desiring_machine", "rhizome", "dod"],
    "Machines":          ["desiring_machine", "shitting_machine", "flow_state", "te_whariki_pumotu"],
    "Whakapapa":         ["whakapapa", "catch22", "anti_oopedipus", "ira_kotahi"],
    "DOD":               ["dod", "zero_set", "te_whariki_pumotu", "simplicity_of_parts", "determinism"],
    "Te-Reo-and-Code":   ["te_whariki_pumotu", "zero_set", "whakapapa", "mauri"],
    "Shmup-Genealogy":   ["esprade", "enemy_wave", "positioning", "the_law", "frog_in_pot"],
    "Design-Rules":      ["simplicity_of_parts", "enemy_wave", "positioning", "dod", "the_law"],
    "Scripts":           ["dod", "zero_set", "whakapapa"],
    "Radiative":         ["radiative", "content_vs_creative", "the_law", "dod"],
    "Singularity":       ["singularity", "ira_kotahi", "tokotoko", "mauri"],
}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE INGESTION
# Raw corpus → flat passage pool indexed by concept_id.
# No objects. Text goes in, tagged chunks come out.
# ─────────────────────────────────────────────────────────────────────────────

def load_sources(root: Path) -> dict:
    """
    Load all .txt source files.
    Returns {stem: full_text}.
    """
    sources = {}
    txt_dir = root / "sources" / "text"
    if not txt_dir.exists():
        return sources
    for f in sorted(txt_dir.glob("*.txt")):
        sources[f.stem] = f.read_text(encoding="utf-8", errors="replace")
    return sources


def index_passages(sources: dict, window_words: int = 120) -> dict:
    """
    Passage indexer. DOD: no objects. Pure data transformation.
    sources: {stem: text}
    returns: {concept_id: [(source_stem, passage_text), ...]}

    Window = 120 words, stepped by 30.
    A passage is kept if ANY keyword for that concept appears in it.
    Deduplication by first 60 chars of passage.
    """
    passages = {cid: [] for cid in CONCEPT_IDS}
    seen = {cid: set() for cid in CONCEPT_IDS}

    for stem, text in sources.items():
        words = text.split()
        step = max(1, window_words // 4)
        # build overlapping windows
        starts = list(range(0, max(1, len(words) - window_words + 1), step))
        if not starts:
            starts = [0]
        for s in starts:
            chunk = " ".join(words[s: s + window_words])
            chunk_lower = chunk.lower()
            for cid in CONCEPT_IDS:
                for kw in CONCEPT_KEYWORDS.get(cid, []):
                    if kw.lower() in chunk_lower:
                        passage = _trim_to_sentences(chunk, kw)
                        key = passage[:60]
                        if key not in seen[cid]:
                            seen[cid].add(key)
                            passages[cid].append((stem, passage))
                        break   # one keyword match per chunk per concept is enough

    return passages


def _trim_to_sentences(text: str, keyword: str, max_chars: int = 340) -> str:
    """
    Find keyword in text. Expand to surrounding sentence boundaries.
    Returns clean passage ≤ max_chars.
    """
    lo = text.lower()
    idx = lo.find(keyword.lower())
    if idx < 0:
        return text[:max_chars].strip()

    # walk back to sentence start
    start = max(0, idx - 180)
    dot = text.rfind(". ", start, idx)
    if dot >= 0:
        start = dot + 2

    # walk forward to sentence end
    end_cap = min(len(text), idx + max_chars)
    dot2 = text.find(". ", idx + len(keyword))
    if 0 <= dot2 < end_cap:
        end_cap = dot2 + 1

    raw = text[start:end_cap].strip()
    raw = re.sub(r"\s+", " ", raw)
    return raw


# ─────────────────────────────────────────────────────────────────────────────
# USER INPUT
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_USER_INPUT = {
    "page": "The-Law",
    "intent": "Explain the one law. Connect it to taonga, DOD, and whakapapa.",
    "tone": "body",
    "extra_concepts": [],
    "voice_notes": "",
    "new_passage": ""
}

def load_user_input(root: Path) -> dict:
    p = root / "scripts" / "user_input.json"
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return dict(DEFAULT_USER_INPUT)

def save_user_input(root: Path, data: dict):
    p = root / "scripts" / "user_input.json"
    p.parent.mkdir(exist_ok=True)
    with open(p, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────────────────────────────────────
# GENERATION ENGINE
# Functions that consume data and produce Markdown.
# No state. No objects. inputs in, text out.
# ─────────────────────────────────────────────────────────────────────────────

def get_cluster(page: str, extra: list) -> list:
    """
    Build the full concept cluster for a page.
    Primary concepts come first (from PAGE_REGISTRY).
    Whakapapa expansions appended after.
    Extra concepts from user_input appended last.
    No duplicates.
    """
    primary = PAGE_REGISTRY.get(page, [])
    ordered = list(primary)
    seen = set(ordered)

    # expand one level via whakapapa
    for cid in list(ordered):
        for linked in WHAKAPAPA.get(cid, [])[:3]:
            if linked not in seen:
                seen.add(linked)
                ordered.append(linked)

    # user-supplied extras
    for e in extra:
        if e in CONCEPT_IDS and e not in seen:
            ordered.append(e)

    return ordered


def select_passages(cluster: list, passages: dict, max_per: int = 2) -> list:
    """
    Select passages for the cluster.
    Returns [(concept_id, source_stem, passage_text), ...]
    Primary concept gets 2 passages, secondaries get 1.
    """
    selected = []
    for i, cid in enumerate(cluster):
        cap = max_per if i < 5 else 1
        for source, text in passages.get(cid, [])[:cap]:
            selected.append((cid, source, text))
    return selected


def render_voice(voice: int, text: str) -> str:
    """
    Apply typographic voice to text.
    0 = title   → **bold**
    1 = body    → plain paragraph
    2 = gloss   → ```code block```
    3 = raw     → > blockquote italic
    """
    clean = re.sub(r"\s+", " ", text).strip()
    wrapped = textwrap.fill(clean, width=92)

    if voice == 0:
        return f"**{wrapped}**\n"
    elif voice == 1:
        return f"{wrapped}\n"
    elif voice == 2:
        return f"```\n{wrapped}\n```\n"
    elif voice == 3:
        lines = [l.strip() for l in clean.split(". ") if l.strip()]
        return "\n".join(f"> *{l.rstrip('.')}.*" for l in lines) + "\n"
    return wrapped + "\n"


def build_section(cid: str, all_selected: list) -> str:
    """
    Build the Markdown section for one concept.
    Pulls its passages from all_selected. Adds whakapapa links.
    """
    name = CONCEPT_NAMES.get(cid, cid)
    voice = CONCEPT_VOICE.get(cid, 1)
    linked = WHAKAPAPA.get(cid, [])
    cid_passages = [(src, p) for c, src, p in all_selected if c == cid]

    parts = [f"## {name}\n"]

    for src, passage in cid_passages[:2]:
        parts.append(render_voice(voice, passage))
        parts.append(f"*— {src}*\n")

    if linked:
        link_strs = [
            f"[{CONCEPT_NAMES.get(l, l)}]({slug(l)})"
            for l in linked[:5]
        ]
        parts.append(f"\n*Whakapapa: {' · '.join(link_strs)}*\n")

    return "\n".join(parts)


def generate_page(user_input: dict, passages: dict) -> str:
    """
    Main generation function.
    user_input + indexed passages → full Markdown wiki page.
    """
    page       = user_input.get("page", "New-Page")
    intent     = user_input.get("intent", "")
    extra      = user_input.get("extra_concepts", [])
    voice_note = user_input.get("voice_notes", "")
    new_pass   = user_input.get("new_passage", "")

    # inject any raw user-provided passage into the passage pool
    if new_pass:
        for cid in PAGE_REGISTRY.get(page, ["the_law"])[:1]:
            passages.setdefault(cid, []).insert(0, ("user_input", new_pass))

    cluster  = get_cluster(page, extra)
    selected = select_passages(cluster, passages)
    primary  = PAGE_REGISTRY.get(page, cluster[:4])
    secondary = [c for c in cluster if c not in set(primary)]

    title = page.replace("-", " ").replace("_", " ")

    lines = []
    lines.append(f"# {title}\n")
    if intent:
        lines.append(f"> *{intent}*\n")
    lines.append("---\n")

    # primary concept sections
    for cid in primary:
        if cid in CONCEPT_IDS:
            lines.append(build_section(cid, selected))
            lines.append("---\n")

    # whakapapa connections table
    if secondary:
        lines.append("## Whakapapa Connections\n")
        lines.append("| Concept | Tupuna |")
        lines.append("|---|---|")
        for cid in secondary[:6]:
            name = CONCEPT_NAMES.get(cid, cid)
            parents = WHAKAPAPA.get(cid, [])
            parent_links = ", ".join(
                f"[{CONCEPT_NAMES.get(p, p)}]({slug(p)})" for p in parents[:3]
            )
            lines.append(f"| [{name}]({slug(cid)}) | {parent_links} |")
        lines.append("\n---\n")

    if voice_note:
        lines.append(f"\n> *{voice_note}*\n")

    lines.append("\n---\n")
    lines.append(
        "*Generated by [WaKa](../WaKa.py). "
        "Old work is whakapapa, not gospel. Edit freely.*\n"
    )

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# METADATA
# Keeps a running record of all generated pages and their concept clusters.
# ─────────────────────────────────────────────────────────────────────────────

def update_metadata(page: str, cluster: list, root: Path):
    meta_path = root / "scripts" / "metadata.json"
    meta = {}
    if meta_path.exists():
        with open(meta_path) as f:
            meta = json.load(f)

    meta.setdefault("pages", {})[page] = {
        "concepts": cluster,
        "whakapapa_snapshot": {
            cid: WHAKAPAPA.get(cid, []) for cid in cluster
        },
    }
    meta["concept_count"] = len(CONCEPT_IDS)
    meta["page_count"]    = len(meta["pages"])

    meta_path.parent.mkdir(exist_ok=True)
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    return meta_path


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def slug(cid: str) -> str:
    """concept_id → wiki slug."""
    return cid.replace("_", "-")


def print_index(passages: dict):
    """Print the passage index: how many passages found per concept."""
    print("\nPassage Index:")
    print(f"  {'concept_id':<28} {'passages':>8}  {'sources'}")
    print(f"  {'─'*28}  {'─'*7}  {'─'*30}")
    for cid in CONCEPT_IDS:
        ps = passages.get(cid, [])
        sources = list({s for s, _ in ps})
        print(f"  {cid:<28} {len(ps):>8}  {', '.join(sources[:4])}")


def print_list():
    """Print all pages and their primary concepts."""
    print("\nPage Registry:")
    for page, concepts in PAGE_REGISTRY.items():
        print(f"  {page:<24}  {' · '.join(concepts)}")
    print()
    print("Concept IDs:")
    for cid in CONCEPT_IDS:
        print(f"  {cid:<28}  {CONCEPT_NAMES[cid]}")


def scaffold_user_input(page: str, root: Path):
    """Write a starter user_input.json for a given page."""
    primary = PAGE_REGISTRY.get(page, CONCEPT_IDS[:3])
    ui = {
        "page": page,
        "intent": f"Write the {page.replace('-', ' ')} page.",
        "tone": "body",
        "extra_concepts": [],
        "voice_notes": "",
        "new_passage": ""
    }
    save_user_input(root, ui)
    print(f"Scaffolded scripts/user_input.json for page: {page}")
    print(f"Primary concepts: {primary}")
    print("Edit intent, then run: python3 WaKa.py")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    # --list: print registry
    if args and args[0] == "--list":
        print_list()
        return

    # --new <PageName>: scaffold user_input.json
    if len(args) >= 2 and args[0] == "--new":
        scaffold_user_input(args[1], ROOT)
        return

    # --force / -f: overwrite existing pages without prompting
    force = "--force" in args or "-f" in args
    args = [a for a in args if a not in ("--force", "-f")]

    # ensure scripts/user_input.json exists
    ui_path = ROOT / "scripts" / "user_input.json"
    if not ui_path.exists():
        save_user_input(ROOT, dict(DEFAULT_USER_INPUT))
        print(f"Created {ui_path}")
        print("Edit scripts/user_input.json then run again.")
        return

    user_input = load_user_input(ROOT)

    # CLI page override
    if args and not args[0].startswith("--"):
        user_input["page"] = args[0]

    page = user_input.get("page", "New-Page")

    print(f"\nWaKa ── generating: {page}")
    print(f"  intent : {user_input.get('intent', '')[:72]}")

    # ingest sources
    sources = load_sources(ROOT)
    print(f"  sources: {list(sources.keys())}")

    # index passages
    passages = index_passages(sources)
    total_passages = sum(len(v) for v in passages.values())
    found_concepts = sum(1 for v in passages.values() if v)
    print(f"  indexed: {total_passages} passages across {found_concepts} concepts")

    # --index: print passage index and exit
    if args and args[0] == "--index":
        print_index(passages)
        return

    # generate
    output = generate_page(user_input, passages)

    # output path
    wiki_dir = ROOT / "wiki"
    wiki_dir.mkdir(exist_ok=True)
    out_path = wiki_dir / f"{page}.md"

    if out_path.exists() and not force:
        resp = input(f"  {out_path.name} already exists. Overwrite? [y/N] ").strip().lower()
        if resp != "y":
            print("  Aborted.")
            return

    out_path.write_text(output, encoding="utf-8")
    print(f"  written : {out_path.relative_to(ROOT)}")

    # update metadata
    cluster = get_cluster(page, user_input.get("extra_concepts", []))
    meta_path = update_metadata(page, cluster, ROOT)
    print(f"  metadata: {meta_path.relative_to(ROOT)}")

    print()
    print("  Next steps:")
    print("    Edit scripts/user_input.json and run again to iterate.")
    print("    python3 WaKa.py --new <PageName>   to scaffold a new page.")
    print("    python3 WaKa.py --list              to see all pages and concepts.")
    print()


if __name__ == "__main__":
    main()
āe āe capteā nflows  aplenty of room in this waka to carry more concepts, passages, and pages.