#!/usr/bin/env python3
"""
scripts/wiki_index.py — unified wiki maintenance tool for Kwiki.

One command keeps the whole wiki whole.

Usage (from repo root):

    python3 scripts/wiki_index.py            # regenerate index pages + update weave blocks
    python3 scripts/wiki_index.py --indexes  # index pages only
    python3 scripts/wiki_index.py --weave    # per-page weave blocks only
    python3 scripts/wiki_index.py --dry-run  # show what would change, write nothing

Generated index pages (wiki/):
    All-Pages.md   — alphabetical list of every content page
    Connections.md — cross-synthesis pages (-x-) + most-connected pages
    Orphans.md     — pages that receive no inbound links
    Tags.md        — tag → page map (reads YAML frontmatter; instructions if absent)
    Timeline.md    — pages sorted by last git commit date (fallback: alphabetical)

Per-page weave blocks:
    Injects/replaces <!-- BEGIN RECURSIVE_WEAVE --> ... <!-- END RECURSIVE_WEAVE -->
    blocks in every content page with direct links, inbound links, and lateral bridges.
    (Replaces the old wiki/recursive_weave.py — same output, shared data model.)

Design: flat data, no classes, DOD style — mirrors WaKa.py and the original
recursive_weave.py so the codebase stays coherent.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# ── paths ──────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent
WIKI = ROOT / "wiki"

# Slugs of generated / structural files — excluded from content analysis
INDEX_SLUGS = {
    "all-pages", "connections", "orphans", "tags", "timeline",
    "home", "readme", "_template",
}

STOPWORDS = {
    "the", "and", "of", "to", "in", "a", "for", "as", "on", "is", "are", "by", "or",
    "with", "from", "at", "this", "that", "it", "be", "not", "into", "all", "one", "vs",
    "you", "your", "their", "our", "an", "we", "they", "them", "its", "can", "was", "were",
}

WEAVE_BEGIN = "<!-- BEGIN RECURSIVE_WEAVE -->"
WEAVE_END   = "<!-- END RECURSIVE_WEAVE -->"

# ── helpers ────────────────────────────────────────────────────────────────────

def slug_from_name(name: str) -> str:
    return name.replace(".md", "").strip().lower()


def human_title(path: Path, text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    slug = slug_from_name(path.name)
    return " ".join(p.capitalize() for p in re.split(r"[-_]+", slug) if p)


def normalize_link_target(target: str) -> str:
    t = target.strip().split("#", 1)[0].strip()
    t = t.replace(".md", "").replace("./", "").strip("/")
    return t.lower()


def extract_links(text: str) -> list[str]:
    links: list[str] = []
    for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = normalize_link_target(m.group(1))
        if target and not target.startswith("http") and not target.startswith("../"):
            links.append(target)
    for m in re.finditer(r"\[\[([^\]]+)\]\]", text):
        target = normalize_link_target(m.group(1))
        if target:
            links.append(target)
    return links


def extract_headings(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^##+\s+(.+)$", text, flags=re.MULTILINE)]


def extract_tokens(title: str, headings: list[str]) -> set[str]:
    combined = " ".join([title] + headings).lower()
    words = re.findall(r"[a-z0-9]+", combined)
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def parse_frontmatter_tags(text: str) -> list[str]:
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not fm:
        return []
    m = re.search(r"^tags\s*:\s*(.+)$", fm.group(1), re.MULTILINE | re.IGNORECASE)
    if not m:
        return []
    raw = m.group(1).strip().strip("[]")
    return [t.strip().strip("\"'") for t in raw.split(",") if t.strip()]


# ── git timestamps ─────────────────────────────────────────────────────────────

def git_timestamps(wiki_dir: Path) -> dict[str, datetime]:
    result: dict[str, datetime] = {}
    for path in wiki_dir.glob("*.md"):
        try:
            ts_raw = subprocess.check_output(
                ["git", "log", "-1", "--format=%aI", "--", str(path.relative_to(ROOT))],
                cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
            ).strip()
            if ts_raw:
                dt = datetime.fromisoformat(ts_raw)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                result[slug_from_name(path.name)] = dt
        except Exception:
            pass
    return result


# ── data model ─────────────────────────────────────────────────────────────────

def load_pages(wiki_dir: Path) -> dict[str, dict]:
    """
    Returns {slug: {file, title, text, links, headings, tokens, tags, is_cross}}
    Skips generated index files.
    """
    pages: dict[str, dict] = {}
    for path in sorted(wiki_dir.glob("*.md")):
        slug = slug_from_name(path.name)
        if slug in INDEX_SLUGS:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        title = human_title(path, text)
        headings = extract_headings(text)
        pages[slug] = {
            "file":     path,
            "title":    title,
            "text":     text,
            "links":    extract_links(text),
            "headings": headings,
            "tokens":   extract_tokens(title, headings),
            "tags":     parse_frontmatter_tags(text),
            "is_cross": "-x-" in path.name,
        }
    return pages


def build_inbound(pages: dict[str, dict]) -> dict[str, set[str]]:
    inbound: dict[str, set[str]] = defaultdict(set)
    for src, item in pages.items():
        for target in item["links"]:
            if target in pages and target != src:
                inbound[target].add(src)
    return inbound


# ── index generators ───────────────────────────────────────────────────────────

_HEADER = "*Generated by `scripts/wiki_index.py`. Re-run to update. Do not edit manually.*\n\n---\n\n"


def gen_all_pages(pages: dict[str, dict], inbound: dict[str, set[str]]) -> str:
    lines = [f"# All Pages\n\n{_HEADER}"]
    lines.append(f"**{len(pages)} pages** — alphabetical, content and cross-synthesis.\n\n")
    lines.append("| Page | Inbound | Outbound |\n|---|---|---|\n")
    for slug in sorted(pages):
        item = pages[slug]
        out_c = len([t for t in item["links"] if t in pages and t != slug])
        in_c  = len(inbound.get(slug, set()))
        mark  = " ✕" if item["is_cross"] else ""
        lines.append(f"| [{item['title']}]({item['file'].name}){mark} | {in_c} | {out_c} |\n")
    lines.append("\n> ✕ = cross-synthesis page (`A-x-B.md`)\n")
    return "".join(lines)


def gen_connections(pages: dict[str, dict], inbound: dict[str, set[str]]) -> str:
    cross = {s: p for s, p in pages.items() if p["is_cross"]}
    rich = sorted(
        pages.items(),
        key=lambda kv: (
            len(inbound.get(kv[0], set())) +
            len([t for t in kv[1]["links"] if t in pages and t != kv[0]])
        ),
        reverse=True,
    )[:10]

    lines = [f"# Connections\n\n{_HEADER}"]

    lines.append("## Cross-Synthesis Pages\n\n")
    lines.append("Created by combining two concepts (`A-x-B.md` naming).\n\n")
    if cross:
        lines.append("| Page | Left | Right |\n|---|---|---|\n")
        for slug in sorted(cross):
            item = cross[slug]
            parts = slug.split("-x-", 1)
            left  = parts[0].replace("-", " ").title() if len(parts) == 2 else "—"
            right = parts[1].replace("-", " ").title() if len(parts) == 2 else "—"
            lines.append(f"| [{item['title']}]({item['file'].name}) | {left} | {right} |\n")
    else:
        lines.append("*No cross-synthesis pages found yet.*\n")

    lines.append("\n## Most-Connected Pages\n\n")
    lines.append("Highest combined inbound + outbound link count.\n\n")
    lines.append("| Page | Inbound | Outbound | Total |\n|---|---|---|---|\n")
    for slug, item in rich:
        out_c = len([t for t in item["links"] if t in pages and t != slug])
        in_c  = len(inbound.get(slug, set()))
        lines.append(f"| [{item['title']}]({item['file'].name}) | {in_c} | {out_c} | {in_c+out_c} |\n")
    return "".join(lines)


def gen_orphans(pages: dict[str, dict], inbound: dict[str, set[str]]) -> str:
    orphans = sorted(
        slug for slug, item in pages.items()
        if not inbound.get(slug) and not item["is_cross"]
    )
    lines = [f"# Orphans\n\n{_HEADER}"]
    lines.append("Pages with **no inbound links** from other wiki pages.\n")
    lines.append("These are candidates for linking in from related pages.\n\n")
    if orphans:
        lines.append(f"**{len(orphans)} orphan(s):**\n\n")
        for slug in orphans:
            item = pages[slug]
            lines.append(f"- [{item['title']}]({item['file'].name})\n")
    else:
        lines.append("*No orphans — every page is reachable. 🎉*\n")
    lines.append("\n> Cross-synthesis (`-x-`) and generated index files are excluded.\n")
    return "".join(lines)


def gen_tags(pages: dict[str, dict]) -> str:
    tag_map: dict[str, list[str]] = defaultdict(list)
    for slug, item in pages.items():
        for tag in item["tags"]:
            tag_map[tag].append(slug)

    lines = [f"# Tags\n\n{_HEADER}"]
    if tag_map:
        lines.append(f"**{len(tag_map)} tag(s)** across wiki pages.\n\n")
        for tag in sorted(tag_map):
            lines.append(f"## `{tag}`\n\n")
            for slug in sorted(tag_map[tag]):
                item = pages[slug]
                lines.append(f"- [{item['title']}]({item['file'].name})\n")
            lines.append("\n")
    else:
        lines.append("*No frontmatter tags found yet.*\n\n")
        lines.append("## How to add tags\n\n")
        lines.append("Add a YAML frontmatter block at the **top** of any wiki page:\n\n")
        lines.append("```markdown\n---\ntags: dod, maori, design\nstatus: draft\n"
                     "summary: One-sentence summary.\nupdated: 2026-04-16\n---\n\n"
                     "# Page Title\n...\n```\n\n")
        lines.append("Re-run `python3 scripts/wiki_index.py` to rebuild this page.\n")
    return "".join(lines)


def gen_timeline(pages: dict[str, dict], timestamps: dict[str, datetime]) -> str:
    if timestamps:
        ordered = sorted(
            pages.keys(),
            key=lambda s: timestamps.get(s) or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
        method = "Sorted by **last git commit date** (most recent first)."
    else:
        ordered = sorted(pages.keys())
        method = "Git timestamps unavailable — sorted **alphabetically** as fallback."

    lines = [f"# Timeline\n\n{_HEADER}"]
    lines.append(f"{method}\n\n")
    lines.append("| Page | Last Updated | Type |\n|---|---|---|\n")
    for slug in ordered:
        item   = pages[slug]
        ts     = timestamps.get(slug)
        date   = ts.strftime("%Y-%m-%d") if ts else "—"
        kind   = "cross-synthesis" if item["is_cross"] else "content"
        lines.append(f"| [{item['title']}]({item['file'].name}) | {date} | {kind} |\n")
    return "".join(lines)


# ── weave block (merged from recursive_weave.py) ──────────────────────────────

def score_related(current: str, pages: dict[str, dict],
                  inbound: dict[str, set[str]]) -> list[tuple[str, int, set[str]]]:
    cur_tokens = pages[current]["tokens"]
    cur_links  = set(pages[current]["links"])
    scores: list[tuple[str, int, set[str]]] = []
    for other, item in pages.items():
        if other == current:
            continue
        shared  = cur_tokens & item["tokens"]
        link_sc = 0
        if other in cur_links:
            link_sc += 2
        if current in set(item["links"]):
            link_sc += 2
        if other in inbound.get(current, set()):
            link_sc += 1
        score = link_sc + len(shared)
        if score > 0:
            scores.append((other, score, shared))
    scores.sort(key=lambda x: (-x[1], x[0]))
    return scores


def make_weave_block(current: str, pages: dict[str, dict],
                     inbound: dict[str, set[str]]) -> str:
    related  = score_related(current, pages, inbound)[:8]
    direct   = list(dict.fromkeys(
        t for t in pages[current]["links"] if t in pages and t != current
    ))[:8]
    inbound_pages = sorted(inbound.get(current, set()))[:8]

    lines = [WEAVE_BEGIN, "## Recursive Hub Weave", ""]
    lines.append("### Direct Connections")
    if direct:
        for slug in direct:
            lines.append(f"- [{pages[slug]['title']}]({pages[slug]['file'].name})")
    else:
        lines.append("- No direct markdown links detected yet.")

    lines += ["", "### Inbound Connections"]
    if inbound_pages:
        for slug in inbound_pages:
            lines.append(f"- [{pages[slug]['title']}]({pages[slug]['file'].name})")
    else:
        lines.append("- No inbound links detected yet.")

    lines += ["", "### Lateral Bridges"]
    if related:
        for slug, score, shared in related:
            shared_str = ", ".join(sorted(shared)[:5]) if shared else "link-graph affinity"
            lines.append(f"#### [{pages[slug]['title']}]({pages[slug]['file'].name})")
            lines.append(f"- Connection strength: {score}")
            lines.append(f"- Shared motifs: {shared_str}")
    else:
        lines.append("- No bridge candidates yet.")

    lines += [
        "",
        "### Recursive Prompt",
        "- In each section above, add at least one sentence that names one direct and one lateral page together.",
        "- Convert plain mentions of those pages into markdown links for tighter recursion.",
        WEAVE_END,
        "",
    ]
    return "\n".join(lines)


def replace_or_append_weave(text: str, weave: str) -> str:
    pattern = re.compile(
        r"\n?<!-- BEGIN RECURSIVE_WEAVE -->.*?<!-- END RECURSIVE_WEAVE -->\n?",
        re.DOTALL,
    )
    if pattern.search(text):
        return (pattern.sub("\n" + weave + "\n", text).rstrip() + "\n")
    return text.rstrip() + "\n\n" + weave + "\n"


# ── write helper ───────────────────────────────────────────────────────────────

def write_file(path: Path, content: str, dry_run: bool) -> bool:
    """Returns True if a change would be / was made."""
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    changed  = existing != content
    if dry_run:
        status = "would write" if changed else "unchanged  "
        print(f"  {status}: {path.name}")
    else:
        if changed:
            path.write_text(content, encoding="utf-8")
            print(f"  wrote    : {path.name}")
        else:
            print(f"  unchanged: {path.name}")
    return changed


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--indexes", action="store_true",
                   help="Only regenerate index pages (skip per-page weave blocks).")
    g.add_argument("--weave",   action="store_true",
                   help="Only update per-page weave blocks (skip index pages).")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would change without writing anything.")
    p.add_argument("--strict",  action="store_true",
                   help="Weave: only update pages that already have at least one internal link.")
    p.add_argument("--limit",   type=int, default=None,
                   help="Weave: only update the top N hub pages by degree.")
    return p.parse_args()


# ── main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    args       = parse_args()
    do_indexes = not args.weave
    do_weave   = not args.indexes
    dry        = args.dry_run

    print(f"\nwiki_index.py — scanning {WIKI}/\n")

    pages      = load_pages(WIKI)
    inbound    = build_inbound(pages)
    timestamps = git_timestamps(WIKI)

    content_count = sum(1 for p in pages.values() if not p["is_cross"])
    cross_count   = sum(1 for p in pages.values() if p["is_cross"])
    orphan_count  = sum(
        1 for slug, item in pages.items()
        if not inbound.get(slug) and not item["is_cross"]
    )
    has_tags = any(p["tags"] for p in pages.values())

    print(f"  pages   : {len(pages)} total ({content_count} content, {cross_count} cross-synthesis)")
    print(f"  orphans : {orphan_count}")
    print(f"  tags    : {'yes' if has_tags else 'none yet'}")
    print(f"  git ts  : {'available' if timestamps else 'unavailable (alpha fallback)'}\n")

    # ── index pages ───────────────────────────────────────────────────────────
    if do_indexes:
        print("Index pages:")
        write_file(WIKI / "All-Pages.md",   gen_all_pages(pages, inbound),   dry)
        write_file(WIKI / "Connections.md", gen_connections(pages, inbound), dry)
        write_file(WIKI / "Orphans.md",     gen_orphans(pages, inbound),     dry)
        write_file(WIKI / "Tags.md",        gen_tags(pages),                 dry)
        write_file(WIKI / "Timeline.md",    gen_timeline(pages, timestamps), dry)
        print()

    # ── per-page weave blocks ─────────────────────────────────────────────────
    if do_weave:
        slugs = list(pages.keys())

        if args.strict:
            slugs = [
                s for s in slugs
                if any(t in pages and t != s for t in pages[s]["links"])
            ]

        ranked = sorted(
            slugs,
            key=lambda s: -(
                len([t for t in pages[s]["links"] if t in pages and t != s]) +
                len(inbound.get(s, set()))
            ),
        )
        if args.limit is not None:
            ranked = ranked[:max(0, args.limit)]

        print(f"Weave blocks ({len(ranked)} pages):")
        updated = 0
        for slug in ranked:
            item    = pages[slug]
            weave   = make_weave_block(slug, pages, inbound)
            new_txt = replace_or_append_weave(item["text"], weave)
            if write_file(item["file"], new_txt, dry):
                updated += 1
                if not dry:
                    item["text"] = new_txt   # keep in-memory state consistent

        mode_parts = []
        if args.strict:
            mode_parts.append("strict")
        if args.limit is not None:
            mode_parts.append(f"limit={args.limit}")
        mode_label = ", ".join(mode_parts) or "default"
        print(f"\n  {updated} page(s) updated ({mode_label})\n")

    suffix = " (dry run)" if dry else ""
    print(f"Done{suffix}.\n")


if __name__ == "__main__":
    main()
