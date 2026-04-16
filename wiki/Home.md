# KELLS — Basic Units of Logic

> *Welcoming Anti-OOPedipus.*  
> *On the prohibition and the refusal of genealogical machines.*

**By Your mom.**  
**Biology Period 1. MS. WENDY WRITER.**

---

This wiki is the **living whakapapa** of the project.  
Not documentation. Not a manual. A genealogy — a map of which ideas gave birth to which, and which machines are shitting which machines.

Old work here is **whakapapa, not gospel**. It is the root system, not the tree.

---

## Pages

| Page | What it is |
|---|---|
| [Whakapapa](Whakapapa) | The genealogy of all ideas here. Read this first. |
| [Anti-OOPedipus](Anti-OOPedipus) | The philosophy. OOP as Oedipal law. DOD as desire. |
| [Machines](Machines) | Desiring-machines, shitting machines, data machines. |
| [The Law](The-Law) | The one law. Presented as taonga. |
| [DOD](DOD) | Data-Oriented Design principles and design rules. |
| [Te Reo and Code](Te-Reo-and-Code) | The Māori-named codebase. `Te_Whariki_Pumotu`. |
| [Shmup Genealogy](Shmup-Genealogy) | DonPachi → DDP → EspRaDe → j. |
| [Design Rules](Design-Rules) | The rules Karl follows. Not mechanics — design rules. |
| [Scripts](Scripts) | How to use the generation scripts to grow new pages. |
| [User Profile](User-Profile.md) | Whakapapa of the creator — intellectual, musical, philosophical lineage. |
| [Rhizhome](Rhizhome) | The master lens: simulating a utopian alien internet. |
| [Plantlings](Plantlings) | The people of Rhizhome — entities that grow sideways. |

---

## The Law (stated once, here, so it is never lost)

> *There is one law that I know. Only one I can state as truth.*  
> *It is my most precious stone and I present it as **taonga**.*

**Extreme depth of the whole achieved through extreme simplicity of the parts.**

Every page here is a fractal of that law.

---

## Generated Indexes

| Index | What it is |
|---|---|
| [All Pages](All-Pages.md) | Every wiki page, alphabetical, with link counts |
| [Connections](Connections.md) | Cross-synthesis pages + most-connected hubs |
| [Orphans](Orphans.md) | Pages not yet linked from anywhere |
| [Tags](Tags.md) | Tag → page map (add frontmatter tags to populate) |
| [Timeline](Timeline.md) | Pages sorted by last edit date |

---

## How This Wiki Grows

This wiki is **iteratively generated** from:

1. **Source docs** in `sources/text/` — old work, whakapapa material
2. **Internal metadata** in `scripts/metadata.json` — concept graph, page registry, whakapapa links
3. **User input** in `scripts/user_input.json` — your intent, tone, new concepts to introduce
4. **`WaKa.py`** — reads both, pulls relevant source passages, outputs a new wiki page

To grow a new page:

```bash
# Edit your intent
nano scripts/user_input.json

# Generate a page
python3 WaKa.py

# Rebuild all indexes + refresh weave blocks (one command does both)
python3 scripts/wiki_index.py
```

---

## Tone

This wiki has four voices, inherited from the source typography:

| Voice | Font (source) | Use |
|---|---|---|
| **Title / Law** | Old Standard TT | Declarations, the law, taonga |
| *Body* | PT Serif | Analysis, sustained thought |
| `gloss` | IBM Plex Mono | Technical terms, code, annotations |
| raw | Arial | Transcript voice, unedited thought |

In Markdown: headings = title voice, blockquotes = body, `inline code` = gloss, plain paragraphs = raw.

---

*Palette: `#fff9ed` parchment · `#00a797` teal · `#000000` black · `#666666` ghost*

<!-- BEGIN RECURSIVE_WEAVE -->
## Recursive Hub Weave

### Direct Connections
- [Whakapapa — Genealogy of Ideas](Whakapapa.md)
- [Anti-OOPedipus](Anti-OOPedipus.md)
- [Machines](Machines.md)
- [The Law](The-Law.md)
- [DOD](DOD.md)
- [Te Reo and Code](Te-Reo-and-Code.md)
- [Shmup Genealogy](Shmup-Genealogy.md)
- [Design Rules](Design-Rules.md)

### Inbound Connections
- No inbound links detected yet.

### Lateral Bridges
#### [Design Rules](Design-Rules.md)
- Connection strength: 3
- Shared motifs: law
#### [Shmup Genealogy](Shmup-Genealogy.md)
- Connection strength: 3
- Shared motifs: law
#### [The Law](The-Law.md)
- Connection strength: 3
- Shared motifs: law
#### [Whakapapa — Genealogy of Ideas](Whakapapa.md)
- Connection strength: 3
- Shared motifs: wiki
#### [Anti-OOPedipus](Anti-OOPedipus.md)
- Connection strength: 2
- Shared motifs: link-graph affinity
#### [DOD](DOD.md)
- Connection strength: 2
- Shared motifs: link-graph affinity
#### [Machines](Machines.md)
- Connection strength: 2
- Shared motifs: link-graph affinity
#### [Scripts](Scripts.md)
- Connection strength: 2
- Shared motifs: link-graph affinity

### Recursive Prompt
- In each section above, add at least one sentence that names one direct and one lateral page together.
- Convert plain mentions of those pages into markdown links for tighter recursion.
<!-- END RECURSIVE_WEAVE -->

