!
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
  Māori:           waka = vessel. whakapapa = WHAKAPAPA 
    tupuna = ancestor, source, origin, influence. not parent-child but lateral. āe = well ❤️‍🩹 

    yeesssss    
                   mauri = the l
                   life-force that makes a thing itself.
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
    python3 WaKa.py --inward <cid> [depth] [PageName]  # grow from core concept outward
  python3 WaKa.py --force            # overwrite existing page without prompting
  python3 WaKa.py --cross <A> <B>    # cross-generate A × B synthesis page
  python3 WaKa.py --rhizo <cA> <cB>  # print lateral whakapapa path between two concept_ids
    python3 WaKa.py --wowee-zowee      # run pages + inward + cross modes in parallel
"""

import json
import os
import re
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed
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
        "plantling",
        "rhizhome",
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
    "plantling":             "Plantling",
    "rhizhome":              "Rhizhome",
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
    "rhizome":             ["anti_oopedipus", "whakapapa", "te_whariki_pumotu", "desiring_machine", "plantling"],
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
    "plantling":           ["rhizome", "mauri", "rhizhome", "whakapapa", "anti_oopedipus"],
    "rhizhome":            ["plantling", "rhizome", "radiative", "content_vs_creative", "anti_oopedipus"],
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
    "plantling":           3,
    "rhizhome":            1,
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
    "plantling":           ["plantling", "Plantling", "blobbling", "Hot Friends", "Space Dad"],
    "rhizhome":            ["rhizhome", "Rhizhome", "alien internet", "utopian", "no currency", "community hub"],
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
    "Scripts":              ["dod", "zero_set", "whakapapa"],
    "Radiative":            ["radiative", "content_vs_creative", "the_law", "dod"],
    "Singularity":          ["singularity", "ira_kotahi", "tokotoko", "mauri"],
    "Genealogy-of-j":       ["esprade", "the_law", "whakapapa", "determinism", "simplicity_of_parts"],
    "The-Marae":            ["mauri", "whakapapa", "ira_kotahi", "taonga", "te_whariki_pumotu"],
    "Production-as-Primary":["desiring_machine", "shitting_machine", "content_vs_creative", "flow_state", "anti_oopedipus"],
    "Zero-Set":             ["zero_set", "te_whariki_pumotu", "dod", "simplicity_of_parts", "ira_kotahi"],
    "Enemy-Wave":           ["enemy_wave", "esprade", "positioning", "determinism", "simplicity_of_parts"],
    "Catch-22":             ["catch22", "content_vs_creative", "frog_in_pot", "flow_state", "anti_oopedipus"],
    "Plantling":            ["plantling", "rhizome", "mauri", "whakapapa", "anti_oopedipus"],
    "Rhizhome":             ["rhizhome", "plantling", "rhizome", "radiative", "content_vs_creative"],
    "Gamification-Lens":    ["rhizhome", "plantling", "radiative", "anti_oopedipus", "mauri", "the_law"],
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
    "inward_center": "",
    "inward_depth": 2,
    "voice_notes": "",
    "new_passage": ""
}

REBLESS_REFRAIN = "Rebless. Recurse. Rebless."

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
        for linked in WHAKAPAPA.get(cid, [])[:FIB_WHAKAPAPA_EXPAND]:
            if linked not in seen:
                seen.add(linked)
                ordered.append(linked)

    # user-supplied extras
    for e in extra:
        if e in CONCEPT_IDS and e not in seen:
            ordered.append(e)

    return ordered


def inward_distances(center: str, depth: int = 2) -> dict:
    """
    Breadth-first ring distances from a center concept.
    Returns {concept_id: ring_distance} where center is ring 0.
    """
    if center not in CONCEPT_IDS:
        return {}

    max_depth = max(0, int(depth))
    dist = {center: 0}
    frontier = [center]

    for ring in range(1, max_depth + 1):
        next_frontier = []
        for node in frontier:
            for linked in WHAKAPAPA.get(node, []):
                if linked in CONCEPT_IDS and linked not in dist:
                    dist[linked] = ring
                    next_frontier.append(linked)
        frontier = next_frontier
        if not frontier:
            break

    return dist


def build_inward_cluster(center: str, depth: int = 2, extra: list | None = None) -> list:
    """
    Build an inward-outward cluster:
    center first, then ring 1, ring 2, ... up to depth.
    Extra concepts (if valid) are appended last.
    """
    dist = inward_distances(center, depth)
    if not dist:
        return []

    ordered = [cid for cid, _ in sorted(dist.items(), key=lambda kv: (kv[1], kv[0]))]
    seen = set(ordered)

    for cid in (extra or []):
        if cid in CONCEPT_IDS and cid not in seen:
            ordered.append(cid)
            
            

    return ordered


def should_rebless(page: str, cluster: list) -> bool:
    """
    Apply the rebless-recurse-rebless refrain to Anti-OOPedipus pages and
    any page whose living cluster includes anti_oopedipus.
    """
    return page == "Anti-OOPedipus" or "anti_oopedipus" in set(cluster)


def select_passages(cluster: list, passages: dict, max_per: int = 2) -> list:
    """
    Select passages for the cluster.
    Returns [(concept_id, source_stem, passage_text), ...]

    Passage caps follow the Fibonacci sequence by cluster position:
      position 0 → fib_cap(0) = 3   (primary / mauri concept dominates)
      position 1 → fib_cap(1) = 2
      position 2 → fib_cap(2) = 1
      position 3+ → fib_cap(3) = 1

    The Fibonacci descent means the page's core concept has proportionally more
    text than supporting concepts — depth through simplicity, not uniformity.
    `max_per` acts as a hard ceiling above the fibonacci value.
    """
    selected = []
    for i, cid in enumerate(cluster):
        cap = min(max_per, fib_cap(i)) if max_per < fib_cap(0) else fib_cap(i)
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
    if should_rebless(page, cluster):
        lines.append(f"> *{REBLESS_REFRAIN}*\n")
    lines.append("---\n")

    # primary concept sections
    for cid in primary:
        if cid in CONCEPT_IDS:
            lines.append(build_section(cid, selected))
            if should_rebless(page, cluster):
                lines.append(f"> *{REBLESS_REFRAIN}*\n")
            lines.append("---\n")

    # whakapapa connections table
    if secondary:
        lines.append("## Whakapapa Connections\n")
        lines.append("| Concept | Tupuna |")
        lines.append("|---|---|")
        for cid in secondary[:FIB_SECONDARY_LIMIT]:
            name = CONCEPT_NAMES.get(cid, cid)
            parents = WHAKAPAPA.get(cid, [])
            parent_links = ", ".join(
                f"[{CONCEPT_NAMES.get(p, p)}]({slug(p)})" for p in parents[:FIB_WHAKAPAPA_EXPAND]
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


def generate_inward_page(
    center: str,
    depth: int,
    passages: dict,
    page_name: str = "",
    intent: str = "",
    voice_note: str = "",
) -> str:
    """
    Generate a page by growing from one core concept outward.
    Simple parts:
      center -> rings -> passages -> links.
    """
    cluster = build_inward_cluster(center, depth)
    if not cluster:
        return f"# Inward\n\nUnknown concept_id: {center}\n"

    selected = select_passages(cluster, passages, max_per=fib(4))  # center ring gets up to fib(4)=3
    distances = inward_distances(center, depth)
    title = page_name.replace("-", " ") if page_name else f"Inward {CONCEPT_NAMES.get(center, center)}"

    lines = [f"# {title}\n"]
    lead = intent or (
        f"Build inwards to get out: center on {CONCEPT_NAMES.get(center, center)}, "
        f"then move ring by ring."
    )
    lines.append(f"> *{lead}*\n")
    lines.append("---\n")

    # Keep the core visible: fib(6)=8 concept sections, closest rings first.
    for cid in cluster[:FIB_SECTION_LIMIT]:
        lines.append(build_section(cid, selected))
        lines.append("---\n")

    lines.append("## Simple Parts Map\n")
    lines.append("| Concept | Ring | Tupuna |")
    lines.append("|---|---:|---|")
    for cid in cluster[:FIB_MAP_LIMIT]:  # fib(7)=13
        ring = distances.get(cid, "?")
        linked = WHAKAPAPA.get(cid, [])[:FIB_WHAKAPAPA_EXPAND]
        tupuna = ", ".join(f"[{CONCEPT_NAMES.get(t, t)}]({slug(t)})" for t in linked) if linked else "—"
        lines.append(f"| [{CONCEPT_NAMES.get(cid, cid)}]({slug(cid)}) | {ring} | {tupuna} |")

    if voice_note:
        lines.append(f"\n\n> *{voice_note}*")

    lines.append("\n\n---\n")
    lines.append(
        "*Generated by [WaKa](../WaKa.py) in inward mode. "
        "Extreme depth through simple parts. Edit freely.*\n"
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
# GENERATIVE COMBINE FUNCTIONS
# Each function takes flat data in, produces flat data or Markdown out.
# No objects. No mutation. Pure combination.
#
# Five operations:
#   weave_passages    — interleave two passage lists sentence-by-sentence
#   rhizo_path        — find lateral whakapapa path between two concepts
#   merge_clusters    — union two page clusters, bias toward shared ancestors
#   combine_voices    — render a passage as two voices simultaneously
#   cross_generate    — generate a page synthesising two source pages
#
# Fibonacci weave ratios — consecutive Fibonacci pairs for natural interleaving:
#   FIB_WEAVE_TIGHT  (2,1)  fib(3):fib(2)  — source A dominates, brief B interjections
#   FIB_WEAVE_SPREAD (3,2)  fib(4):fib(3)  — A still leads, B has more voice
#   FIB_WEAVE_EVEN   (5,3)  fib(5):fib(4)  — near-equal, golden-ratio convergence
# ─────────────────────────────────────────────────────────────────────────────

FIB_WEAVE_TIGHT  = (2, 1)   # fib(3) : fib(2)
FIB_WEAVE_SPREAD = (3, 2)   # fib(4) : fib(3)
FIB_WEAVE_EVEN   = (5, 3)   # fib(5) : fib(4)

FIB_WHAKAPAPA_EXPAND = 3    # fib(4) — whakapapa links expanded per concept in get_cluster
FIB_RHIZO_MAX_DEPTH  = 5    # fib(5) — max BFS depth for rhizo_path
FIB_SECONDARY_LIMIT  = 5    # fib(5) — secondary concept rows in generate_page table
FIB_SECTION_LIMIT    = 8    # fib(6) — concept sections rendered in generate_inward_page
FIB_MAP_LIMIT        = 13   # fib(7) — rows in the Simple Parts Map table
#   cross_generate    — generate a page synthesising two source pages
# ─────────────────────────────────────────────────────────────────────────────

def weave_passages(passages_a: list, passages_b: list, ratio: tuple = FIB_WEAVE_TIGHT) -> list:
    """
    Interleave two passage lists.
    passages_a / passages_b: [(source_stem, text), ...]
    ratio (a, b): take `a` passages from A then `b` from B, repeat.
    Returns a new flat list in woven order.

    Default ratio is FIB_WEAVE_TIGHT = (2, 1) — a Fibonacci pair where source A
    contributes twice as many passages as B, mirroring the golden-ratio descent.
    Use FIB_WEAVE_SPREAD (3,2) for more balanced synthesis,
    or FIB_WEAVE_EVEN (5,3) for near-equal voices.

    Example with FIB_WEAVE_TIGHT:
        weave_passages(pa, pb)
        → [pa[0], pa[1], pb[0], pa[2], pa[3], pb[1], ...]
    """
    result = []
    ia, ib = 0, 0
    ra, rb = ratio
    while ia < len(passages_a) or ib < len(passages_b):
        for _ in range(ra):
            if ia < len(passages_a):
                result.append(passages_a[ia]); ia += 1
        for _ in range(rb):
            if ib < len(passages_b):
                result.append(passages_b[ib]); ib += 1
    return result


def rhizo_path(start: str, end: str, max_depth: int = FIB_RHIZO_MAX_DEPTH) -> list:
    """
    Find the shortest lateral whakapapa path between two concept_ids.
    Returns [start, ..., end] using BFS over WHAKAPAPA adjacency.
    Returns [] if no path found within max_depth.
    No objects — operates on WHAKAPAPA directly.
    """
    if start not in CONCEPT_IDS or end not in CONCEPT_IDS:
        return []
    if start == end:
        return [start]

    # BFS: queue of (current_node, path_so_far)
    queue = [(start, [start])]
    visited = {start}

    while queue:
        node, path = queue.pop(0)
        if len(path) > max_depth:
            continue
        for neighbour in WHAKAPAPA.get(node, []):
            if neighbour in visited:
                continue
            new_path = path + [neighbour]
            if neighbour == end:
                return new_path
            visited.add(neighbour)
            queue.append((neighbour, new_path))

    return []


def merge_clusters(cluster_a: list, cluster_b: list) -> list:
    """
    Merge two concept clusters into one ordered list.
    Concepts shared by both clusters rise to the front (shared tupuna first).
    Unique-to-A concepts follow, then unique-to-B.
    No duplicates. Order within each group is preserved from original lists.
    """
    set_a, set_b = set(cluster_a), set(cluster_b)
    shared    = [c for c in cluster_a if c in set_b]
    only_a    = [c for c in cluster_a if c not in set_b]
    only_b    = [c for c in cluster_b if c not in set_a]
    return shared + only_a + only_b


def combine_voices(voice_a: int, voice_b: int, text: str) -> str:
    """
    Render a single passage as two voices in parallel.
    voice_a / voice_b: integers 0–3 (see CONCEPT_VOICE).
    Produces a two-column Markdown table: | voice_a | voice_b |
    Each cell contains the passage rendered in its respective voice.
    """
    rendered_a = render_voice(voice_a, text).strip()
    rendered_b = render_voice(voice_b, text).strip()
    # sanitise newlines for table cells
    cell_a = rendered_a.replace("\n", " ").replace("|", "\\|")
    cell_b = rendered_b.replace("\n", " ").replace("|", "\\|")
    voice_labels = ["title", "body", "gloss", "raw"]
    label_a = voice_labels[voice_a] if voice_a < 4 else str(voice_a)
    label_b = voice_labels[voice_b] if voice_b < 4 else str(voice_b)
    return (
        f"| {label_a} | {label_b} |\n"
        f"|---|---|\n"
        f"| {cell_a} | {cell_b} |\n"
    )


def cross_generate(page_a: str, page_b: str, passages: dict, intent: str = "") -> str:
    """
    Generate a Markdown page synthesising two source pages.
    page_a, page_b: keys in PAGE_REGISTRY (or any concept cluster).
    passages: the full indexed passage pool.
    intent: optional framing sentence for the top of the page.

    Produces:
      — a merged cluster (shared concepts first)
      — woven passages from both pages
      — rhizo paths between each primary pair
      — a whakapapa bridge section
    """
    cluster_a = get_cluster(page_a, [])
    cluster_b = get_cluster(page_b, [])
    merged    = merge_clusters(cluster_a, cluster_b)

    title = f"{page_a} × {page_b}"
    lines = [f"# {title}\n"]
    if intent:
        lines.append(f"> *{intent}*\n")
    lines.append("---\n")

    # ── Shared core ──
    shared = [c for c in merged if c in set(cluster_a) and c in set(cluster_b)]
    if shared:
        lines.append("## Shared Tupuna\n")
        for cid in shared[:4]:
            raw_a = passages.get(cid, [])[:1]
            raw_b = passages.get(cid, [])[-1:]
            if raw_a and raw_b:
                woven = weave_passages(raw_a, raw_b, ratio=FIB_WEAVE_SPREAD)
            else:
                woven = raw_a or raw_b
            voice = CONCEPT_VOICE.get(cid, 1)
            lines.append(f"### {CONCEPT_NAMES.get(cid, cid)}\n")
            for src, passage in woven:
                lines.append(render_voice(voice, passage))
                lines.append(f"*— {src}*\n")
            # rhizo bridge between this shared concept and the primary of each page
            primary_a = cluster_a[0] if cluster_a else cid
            primary_b = cluster_b[0] if cluster_b else cid
            if primary_a != cid:
                path = rhizo_path(cid, primary_a)
                if path:
                    path_str = " → ".join(
                        f"[{CONCEPT_NAMES.get(p, p)}]({slug(p)})" for p in path
                    )
                    lines.append(f"\n*Path → {page_a}: {path_str}*\n")
            if primary_b != cid:
                path = rhizo_path(cid, primary_b)
                if path:
                    path_str = " → ".join(
                        f"[{CONCEPT_NAMES.get(p, p)}]({slug(p)})" for p in path
                    )
                    lines.append(f"\n*Path → {page_b}: {path_str}*\n")
        lines.append("---\n")

    # ── Divergent voices: one concept from each unique side ──
    only_a = [c for c in cluster_a if c not in set(cluster_b)]
    only_b = [c for c in cluster_b if c not in set(cluster_a)]
    if only_a and only_b:
        rep_a, rep_b = only_a[0], only_b[0]
        lines.append(f"## Divergence: {CONCEPT_NAMES.get(rep_a, rep_a)} vs {CONCEPT_NAMES.get(rep_b, rep_b)}\n")
        va = CONCEPT_VOICE.get(rep_a, 1)
        vb = CONCEPT_VOICE.get(rep_b, 1)
        ps_a = passages.get(rep_a, [])[:1]
        ps_b = passages.get(rep_b, [])[:1]
        if ps_a and ps_b:
            lines.append(combine_voices(va, vb, ps_a[0][1]))
            lines.append(f"*{CONCEPT_NAMES.get(rep_a, rep_a)}: {ps_a[0][0]} / "
                         f"{CONCEPT_NAMES.get(rep_b, rep_b)}: {ps_b[0][0]}*\n")
        # rhizo bridge between the two divergent concepts
        bridge = rhizo_path(rep_a, rep_b)
        if bridge:
            bridge_str = " → ".join(
                f"[{CONCEPT_NAMES.get(p, p)}]({slug(p)})" for p in bridge
            )
            lines.append(f"\n*Rhizo bridge: {bridge_str}*\n")
        lines.append("---\n")

    lines.append("\n---\n")
    lines.append(
        f"*Cross-generated by [WaKa](../WaKa.py) from `{page_a}` × `{page_b}`. "
        "All paths are lateral. Edit freely.*\n"
    )
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def fib(n: int) -> int:
    """
    Return the nth Fibonacci number (0-indexed: fib(0)=0, fib(1)=1, fib(2)=1, ...).
    Used throughout the generation engine to set passage caps and weave ratios.
    Fibonacci growth mirrors rhizomatic expansion: each step is the sum of the two before.
    """
    a, b = 0, 1
    for _ in range(max(0, n)):
        a, b = b, a + b
    return a


def fib_cap(position: int, base: int = 4) -> int:
    """
    Passage cap for concept at cluster position `position`.
    Descends the Fibonacci sequence from fib(base):
      position 0 → fib(base)     e.g. fib(4) = 3
      position 1 → fib(base-1)          fib(3) = 2
      position 2 → fib(base-2)          fib(2) = 1
      position 3+ → fib(1)              fib(1) = 1

    This lets the primary concept dominate the page,
    with each subsequent concept receiving proportionally fewer passages.
    """
    return fib(max(1, base - position))


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


def _write_markdown(path: Path, content: str, force: bool) -> tuple[bool, str]:
    """
    Write markdown content to a file.
    Returns (written, reason).
    """
    if path.exists() and not force:
        return (False, "exists")
    path.parent.mkdir(exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return (True, "written")


def _page_job(page: str, passages: dict, force: bool) -> dict:
    """Generate one registry page markdown file."""
    ui = dict(DEFAULT_USER_INPUT)
    ui["page"] = page
    ui["intent"] = f"Generate {page.replace('-', ' ')} through whakapapa links."

    md = generate_page(ui, passages)
    out = ROOT / "wiki" / f"{page}.md"
    written, reason = _write_markdown(out, md, force)

    return {
        "kind": "page",
        "name": page,
        "path": str(out.relative_to(ROOT)),
        "written": written,
        "reason": reason,
        "cluster": get_cluster(page, ui.get("extra_concepts", [])),
    }


def _inward_job(center: str, depth: int, passages: dict, force: bool) -> dict:
    """Generate one inward page from a center concept."""
    page_name = f"Inward-{slug(center).title()}"
    md = generate_inward_page(center, depth, passages, page_name=page_name)
    out = ROOT / "wiki" / f"{page_name}.md"
    written, reason = _write_markdown(out, md, force)

    return {
        "kind": "inward",
        "name": page_name,
        "path": str(out.relative_to(ROOT)),
        "written": written,
        "reason": reason,
        "cluster": build_inward_cluster(center, depth),
    }


def _cross_job(page_a: str, page_b: str, passages: dict, force: bool) -> dict:
    """Generate one cross page from two source pages."""
    out_name = f"{page_a}-x-{page_b}"
    md = cross_generate(page_a, page_b, passages)
    out = ROOT / "wiki" / f"{out_name}.md"
    written, reason = _write_markdown(out, md, force)

    cluster = merge_clusters(get_cluster(page_a, []), get_cluster(page_b, []))

    return {
        "kind": "cross",
        "name": out_name,
        "path": str(out.relative_to(ROOT)),
        "written": written,
        "reason": reason,
        "cluster": cluster,
    }


def run_wowee_zowee(passages: dict, force: bool = False, inward_depth: int = 2, workers: int = 8) -> dict:
    """
    Run three generation modes in parallel:
      1) all registry pages
      2) inward pages for all concepts
      3) cross pages for neighboring registry entries
    Returns a summary dict with counts and written paths.
    """
    page_names = list(PAGE_REGISTRY.keys())
    cross_pairs = list(zip(page_names, page_names[1:]))

    jobs = []
    for page in page_names:
        jobs.append(("page", page))
    for cid in CONCEPT_IDS:
        jobs.append(("inward", cid))
    for page_a, page_b in cross_pairs:
        jobs.append(("cross", (page_a, page_b)))

    results = []
    max_workers = max(2, min(workers, len(jobs)))

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {}
        for kind, payload in jobs:
            if kind == "page":
                fut = pool.submit(_page_job, payload, passages, force)
            elif kind == "inward":
                fut = pool.submit(_inward_job, payload, inward_depth, passages, force)
            else:
                page_a, page_b = payload
                fut = pool.submit(_cross_job, page_a, page_b, passages, force)
            future_map[fut] = kind

        for fut in as_completed(future_map):
            results.append(fut.result())

    written = [r for r in results if r.get("written")]
    skipped = [r for r in results if not r.get("written")]

    # Metadata updates stay sequential to avoid file write races.
    for item in written:
        if item.get("kind") in {"page", "inward", "cross"}:
            update_metadata(item["name"], item.get("cluster", []), ROOT)

    by_kind = {
        "page": len([r for r in written if r.get("kind") == "page"]),
        "inward": len([r for r in written if r.get("kind") == "inward"]),
        "cross": len([r for r in written if r.get("kind") == "cross"]),
    }

    return {
        "written_count": len(written),
        "skipped_count": len(skipped),
        "by_kind": by_kind,
        "written_paths": [r.get("path", "") for r in written],
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    # --force / -f: overwrite existing pages without prompting
    force = "--force" in args or "-f" in args
    args = [a for a in args if a not in ("--force", "-f")]

    # --wowee-zowee: run a set of modes simultaneously
    if args and args[0] == "--wowee-zowee":
        sources = load_sources(ROOT)
        passages = index_passages(sources)
        summary = run_wowee_zowee(passages, force=force)
        print("WaKa ── wowee-zowee complete")
        print(f"  written: {summary['written_count']} files")
        print(f"  skipped: {summary['skipped_count']} files")
        print(
            "  by kind: "
            f"pages={summary['by_kind']['page']} · "
            f"inward={summary['by_kind']['inward']} · "
            f"cross={summary['by_kind']['cross']}"
        )
        return

    # --cross <PageA> <PageB> [intent]: synthesise two pages
    if len(args) >= 3 and args[0] == "--cross":
        page_a, page_b = args[1], args[2]
        intent = " ".join(args[3:]) if len(args) > 3 else ""
        sources  = load_sources(ROOT)
        passages = index_passages(sources)
        md = cross_generate(page_a, page_b, passages, intent=intent)
        out_name = f"{page_a}-x-{page_b}.md"
        out_path = ROOT / "wiki" / out_name
        out_path.write_text(md, encoding="utf-8")
        print(f"Written: wiki/{out_name}")
        return

    # --rhizo <ConceptA> <ConceptB>: print lateral path
    if len(args) >= 3 and args[0] == "--rhizo":
        path = rhizo_path(args[1], args[2])
        if path:
            print(" → ".join(path))
        else:
            print(f"No path found between {args[1]} and {args[2]}")
        return

    # --inward <concept_id> [depth] [PageName]: grow page from center outward
    if len(args) >= 2 and args[0] == "--inward":
        center = args[1]
        if center not in CONCEPT_IDS:
            print(f"Unknown concept_id: {center}")
            print("Run --list to view valid concept IDs.")
            return

        depth = 2
        page_name = ""
        if len(args) >= 3:
            if args[2].isdigit():
                depth = int(args[2])
                if len(args) >= 4:
                    page_name = args[3]
            else:
                page_name = args[2]

        default_name = f"Inward-{slug(center).title()}"
        out_name = page_name or default_name

        sources = load_sources(ROOT)
        passages = index_passages(sources)

        md = generate_inward_page(center, depth, passages, page_name=out_name)
        out_path = ROOT / "wiki" / f"{out_name}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"Written: wiki/{out_name}.md")
        return

    # --list: print registry
    if args and args[0] == "--list":
        print_list()
        return

    # --new <PageName>: scaffold user_input.json
    if len(args) >= 2 and args[0] == "--new":
        scaffold_user_input(args[1], ROOT)
        return

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
