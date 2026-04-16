# Kwiki

A living wiki for the **j** project — philosophy, code, design, whakapapa.

This is not documentation. It is a **genealogy**: a map of which ideas gave birth to which, and how concepts machine each other into existence.

---

## Purpose

The wiki holds concepts that span code, culture, and design:

- **Data-Oriented Design** (DOD) and why it matters
- **Te reo Māori** naming as structural, not decorative
- **Desiring-machines**, rhizomes, and the Deleuzian frame for the project
- The **one law** — *extreme depth of the whole through extreme simplicity of the parts*

Old work is whakapapa, not gospel. It is the root system, not the tree.

---

## How to add a new page

1. Copy the template:
   ```bash
   cp wiki/_template.md wiki/Your-Page-Name.md
   ```
2. Fill in the title, frontmatter, and content.
3. Add links to related pages using `[Display Text](Page-Slug.md)`.
4. Regenerate indexes:
   ```bash
   python3 scripts/wiki_index.py
   ```

**Naming convention:** `Title-Case-Hyphenated.md`  
Cross-synthesis pages: `Page-A-x-Page-B.md`

---

## How to run the generator

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
