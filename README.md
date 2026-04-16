# HOME: Design Bible

This file is auto-generated from the recursive JSON meta-structure in `Json to build internet 2 from`.

## Project Overview
- **ID:** home_ttrpg
- **Title:** HOME
- **Subtitle:** A Campaign of Rhizomes, Redistribution, and Singing Distance
- **Version:** 0.1-recursive
- **Status:** living_system

## Design Principles
- no_dice
- position_over_probability
- terrain_as_logic
- characters_as_multivalued_systems
- paired_authorship
- memory_box_fermentation
- recursive_growth
- redistribution_over_loot
- ambiguity_with_structure
- framing_before_resolution

## Core Laws
- dual_terrain_covenant: true
- player_set_and_gm_set_are_sovereign: true
- every_encounter_is_a_braid_of_one_player_terrain_and_one_gm_terrain: true
- core_rules_are_externalized_to_other_books: true
- all_elements_must_support_recursive_generation: true

---

This file is the top-level design bible. All other content is generated to match this schema and its recursive hooks.

```bash
# Full pass: regenerate all index pages + refresh per-page weave blocks
python3 scripts/wiki_index.py

# Index pages only (faster)
python3 scripts/wiki_index.py --indexes

# Per-page weave blocks only
python3 scripts/wiki_index.py --weave

# Preview without writing anything
python3 scripts/wiki_index.py --dry-run

# Check for broken internal links
python3 scripts/wiki_index.py --check-links

# Generate a new content page from user_input.json
python3 WaKa.py
```

---

## Generated index pages

| Page | What it contains |
|---|---|
| `wiki/All-Pages.md` | Every wiki page alphabetically, with inbound/outbound link counts |
| `wiki/Connections.md` | Cross-synthesis pages (`A-x-B`) + most-connected hub pages |
| `wiki/Orphans.md` | Pages that no other page links to — candidates for integration |
| `wiki/Tags.md` | Tag → page map built from YAML frontmatter |
| `wiki/Timeline.md` | Pages sorted by last git commit date |

All index pages are regenerated deterministically by `scripts/wiki_index.py`.

---

## Naming conventions

| Pattern | Meaning |
|---|---|
| `Concept-Name.md` | Content page |
| `A-x-B.md` | Cross-synthesis of two concepts |
| `_template.md` | Page template (not indexed) |
| `Home.md` | Landing page (not indexed as a content page) |

---

## Repository layout

```
Kwiki/
├── wiki/                  ← all wiki pages + generated indexes
│   ├── Home.md            ← landing page
│   ├── _template.md       ← copy this to start a new page
│   ├── All-Pages.md       ← generated
│   ├── Connections.md     ← generated
│   ├── Orphans.md         ← generated
│   ├── Tags.md            ← generated
│   ├── Timeline.md        ← generated
│   └── *.md               ← content pages
├── scripts/
│   ├── wiki_index.py      ← unified index + weave generator (run this)
│   ├── batch_grow.py      ← batch-generate content pages via WaKa.py
│   ├── metadata.json      ← concept graph
│   └── user_input.json    ← intent for next WaKa.py generation
├── sources/               ← source material ingested by WaKa.py
├── WaKa.py                ← page generator
└── README.md              ← this file
```
