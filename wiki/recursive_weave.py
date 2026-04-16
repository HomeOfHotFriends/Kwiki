#!/usr/bin/env python3
"""
recursive_weave.py

Run this from the wiki folder. It updates existing Markdown files in place by
adding a generated recursive hub block with cross-page connections.
It does not create any new Markdown files.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

BEGIN = "<!-- BEGIN RECURSIVE_WEAVE -->"
END = "<!-- END RECURSIVE_WEAVE -->"

STOPWORDS = {
    "the", "and", "of", "to", "in", "a", "for", "as", "on", "is", "are", "by", "or",
    "with", "from", "at", "this", "that", "it", "be", "not", "into", "all", "one", "vs",
    "you", "your", "their", "our", "an", "we", "they", "them", "its", "can", "was", "were",
}


def slug_from_name(name: str) -> str:
    return name.replace(".md", "").strip().lower()


def human_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", slug) if part)


def normalize_link_target(target: str) -> str:
    t = target.strip()
    t = t.split("#", 1)[0].strip()
    t = t.replace(".md", "")
    t = t.replace("./", "")
    t = t.strip("/")
    return t.lower()


def extract_headings(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^##+\s+(.+)$", text, flags=re.MULTILINE)]


def extract_links(text: str) -> list[str]:
    links = []
    for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = normalize_link_target(m.group(1))
        if target and not target.startswith("http") and not target.startswith("../"):
            links.append(target)
    return links


def extract_tokens(title: str, headings: list[str]) -> set[str]:
    text = " ".join([title] + headings).lower()
    words = re.findall(r"[a-z0-9]+", text)
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def score_related(current: str, meta: dict, inbound: dict[str, set[str]]) -> list[tuple[str, int, set[str]]]:
    current_tokens = meta[current]["tokens"]
    current_links = set(meta[current]["links"])

    scores = []
    for other in meta:
        if other == current:
            continue

        other_tokens = meta[other]["tokens"]
        shared_tokens = current_tokens & other_tokens

        mutual_links = 0
        if other in current_links:
            mutual_links += 2
        if current in set(meta[other]["links"]):
            mutual_links += 2
        if other in inbound[current]:
            mutual_links += 1

        token_score = len(shared_tokens)
        score = mutual_links + token_score
        if score > 0:
            scores.append((other, score, shared_tokens))

    scores.sort(key=lambda x: (-x[1], x[0]))
    return scores


def make_weave_block(current: str, meta: dict, inbound: dict[str, set[str]]) -> str:
    related = score_related(current, meta, inbound)
    top_related = related[:8]

    direct = [t for t in meta[current]["links"] if t in meta and t != current]
    direct = list(dict.fromkeys(direct))[:8]

    inbound_pages = sorted(inbound[current])[:8]

    lines = []
    lines.append(BEGIN)
    lines.append("## Recursive Hub Weave")
    lines.append("")
    lines.append("### Direct Connections")
    if direct:
        for slug in direct:
            lines.append(f"- [{meta[slug]['title']}]({meta[slug]['file'].name})")
    else:
        lines.append("- No direct markdown links detected yet.")

    lines.append("")
    lines.append("### Inbound Connections")
    if inbound_pages:
        for slug in inbound_pages:
            lines.append(f"- [{meta[slug]['title']}]({meta[slug]['file'].name})")
    else:
        lines.append("- No inbound links detected yet.")

    lines.append("")
    lines.append("### Lateral Bridges")
    if top_related:
        for slug, score, shared in top_related:
            shared_list = ", ".join(sorted(shared)[:5]) if shared else "link-graph affinity"
            lines.append(f"#### [{meta[slug]['title']}]({meta[slug]['file'].name})")
            lines.append(f"- Connection strength: {score}")
            lines.append(f"- Shared motifs: {shared_list}")
    else:
        lines.append("- No bridge candidates yet.")

    lines.append("")
    lines.append("### Recursive Prompt")
    lines.append("- In each section above, add at least one sentence that names one direct and one lateral page together.")
    lines.append("- Convert plain mentions of those pages into markdown links for tighter recursion.")
    lines.append(END)
    lines.append("")
    return "\n".join(lines)


def replace_or_append_weave(text: str, weave: str) -> str:
    pattern = re.compile(r"\n?<!-- BEGIN RECURSIVE_WEAVE -->.*?<!-- END RECURSIVE_WEAVE -->\n?", re.DOTALL)
    if pattern.search(text):
        updated = pattern.sub("\n" + weave + "\n", text).rstrip() + "\n"
        return updated

    # Append near end without deleting any authored content.
    return text.rstrip() + "\n\n" + weave + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively weave connection blocks into existing markdown files."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Only update pages that already have at least one internal markdown link.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only update top N hub pages ranked by direct+inbound connection degree.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show selection and counts without writing files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    root = Path.cwd()
    files = sorted(p for p in root.glob("*.md") if p.is_file())
    if not files:
        print("No .md files found in current directory.")
        return

    meta: dict[str, dict] = {}
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        slug = slug_from_name(path.name)

        top_heading = None
        m = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
        if m:
            top_heading = m.group(1).strip()

        title = top_heading or human_title(slug)
        headings = extract_headings(text)
        links = extract_links(text)
        tokens = extract_tokens(title, headings)

        meta[slug] = {
            "file": path,
            "title": title,
            "headings": headings,
            "links": links,
            "tokens": tokens,
            "text": text,
        }

    inbound: dict[str, set[str]] = defaultdict(set)
    for src_slug, item in meta.items():
        for target in item["links"]:
            if target in meta and target != src_slug:
                inbound[target].add(src_slug)

    selected = list(meta.keys())
    if args.strict:
        selected = [
            slug for slug in selected
            if any(target in meta and target != slug for target in meta[slug]["links"])
        ]

    ranked = sorted(
        selected,
        key=lambda slug: (
            -(len([t for t in meta[slug]["links"] if t in meta and t != slug]) + len(inbound[slug])),
            slug,
        ),
    )

    if args.limit is not None:
        if args.limit < 0:
            print("--limit must be >= 0")
            return
        ranked = ranked[:args.limit]

    if args.dry_run:
        print(f"Dry run: selected {len(ranked)} of {len(meta)} markdown files.")
        print("Selected hubs:")
        for slug in ranked:
            degree = len([t for t in meta[slug]["links"] if t in meta and t != slug]) + len(inbound[slug])
            print(f"  - {meta[slug]['file'].name} (degree={degree})")
        return

    updated_count = 0
    for slug in ranked:
        item = meta[slug]
        weave = make_weave_block(slug, meta, inbound)
        new_text = replace_or_append_weave(item["text"], weave)
        if new_text != item["text"]:
            item["file"].write_text(new_text, encoding="utf-8")
            updated_count += 1

    mode = []
    if args.strict:
        mode.append("strict")
    if args.limit is not None:
        mode.append(f"limit={args.limit}")
    mode_label = ", ".join(mode) if mode else "default"

    print(
        f"Updated {updated_count} markdown files with recursive weave blocks "
        f"({mode_label}; selected {len(ranked)} of {len(meta)})."
    )


if __name__ == "__main__":
    main()
