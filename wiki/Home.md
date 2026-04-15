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

---

## The Law (stated once, here, so it is never lost)

> *There is one law that I know. Only one I can state as truth.*  
> *It is my most precious stone and I present it as **taonga**.*

**Extreme depth of the whole achieved through extreme simplicity of the parts.**

Every page here is a fractal of that law.

---

## How This Wiki Grows

This wiki is **iteratively generated** from:

1. **Source docs** in `sources/text/` — old work, whakapapa material
2. **Internal metadata** in `scripts/metadata.json` — concept graph, page registry, whakapapa links
3. **User input** in `scripts/user_input.json` — your intent, tone, new concepts to introduce
4. **`scripts/generate.py`** — reads both, pulls relevant source passages, outputs a new wiki page

To grow a new page:

```bash
# Edit your intent
nano scripts/user_input.json

# Generate
python3 scripts/generate.py

# Push to wiki
bash scripts/push.sh
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
