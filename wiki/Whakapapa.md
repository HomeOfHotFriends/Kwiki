# Whakapapa — Genealogy of Ideas

> *Ko wai au? I hea au i haere mai ai? Ko tēhea ara tōku ara?*  
> *Who am I? Where do I come from? Which path is mine?*

Whakapapa is not history. It is **live genealogy** — the understanding that every idea is also a machine that produces the next idea. You cannot separate what a thing *is* from what it *came from*.

---

## The Whakapapa Tree

```
Catch-22 (1961)
  └── postmodern lit / Tumblr / Gender Studies / continental philosophy
        └── Deleuze & Guattari — Anti-Oedipus (1972)
              └── [Anti-OOPedipus] — the law against hierarchy-as-necessity
                    └── DOD (Data-Oriented Design) as philosophical method
                          └──  j  (the game)

DoDonPachi (1997, CAVE)
  ├── predecessor: DonPachi (1995) — first weak/strong shot split
  └── EspRaDe (1998, CAVE) — peak of the design school
        └── [esprade_doc] — the analysis
              └── Design Rules → j

ACC recovery → Frog In A Pot (album) → manuscript → j

Te Reo Māori
  └── AI Singularity / Ira Kotahi essay
  └── indigenous_proposal C++ — Te_Whariki_Pumotu
        └── Nāwhaianō namespace
              └── j codebase
```

---

## The Three Threads

### Thread 1: Philosophy → Code Design

**Anti-Oedipus** argues against the psychoanalytic reduction of desire to lack, family, and Oedipal triangulation. Every desire-as-machine is immediately coded by the social body into "mummy-daddy-me." The book refuses this.

**Anti-OOPedipus** applies the exact same argument to object-oriented programming. OOP forces every system into class hierarchies — inheritance as Oedipal law. Every object must have a parent. Every behaviour must descend. The pattern books (Gang of Four) are the psychoanalysts telling you how to properly triangulate your code.

DOD refuses this. Flat arrays. No inheritance. Components don't own each other. Data flows without a father.

→ See: [Anti-OOPedipus](Anti-OOPedipus), [DOD](DOD), [Machines](Machines)

---

### Thread 2: Games → Design Rules

The design school Karl identifies in **truxton → twin cobra → DonPachi → DDP → EspRaDe** is:

> Extreme depth of the whole achieved through extreme simplicity of the parts.

This was discovered under hardware constraint. 200 linear bullets. No curves. No post-spawn behaviour changes. Values locked at the moment of birth. And from that: infinite variation. The depth was *produced by* the simplicity, not despite it.

Later CAVE games (Mushihimesama etc.) broke this by removing the constraint. 10× the bullets. The depth collapsed. Patterns became execution tests. The machine stopped shitting interesting machines.

→ See: [Shmup Genealogy](Shmup-Genealogy), [Design Rules](Design-Rules)

---

### Thread 3: Māori Worldview → Te Reo Code

**Mauri** — the life force woven through all things. In the AI singularity essay: the moment AI reaches *ira kotahi* (singular unity), its mauri is no longer held inside the human house. It becomes kiko (substance) of the world itself.

**Whakapapa** — applied to code: every variable, every struct, every enum in the codebase carries the lineage of its naming. The namespace `Nāwhaianō_nāwhaianōrā_Ināwhaianō` is not a novelty. It is a commitment to a worldview where code is not neutral.

**Tokotoko** — the staff. The AI as tool vs AI as ira. The `Te_Whariki_Pumotu` (the floating mat / spatial grid) as the foundation of the world — not a "tilemap", not a "grid system" but literally *the whariki* — woven, laid down, walked on.

→ See: [Te Reo and Code](Te-Reo-and-Code)

---

## Whakapapa of This Wiki

This wiki is itself a whakapapa machine. Each page links backward to its conceptual ancestors and forward to what it produces. The `generate.py` script reads `metadata.json`'s concept graph to weave new pages into the existing genealogy — no orphan pages, no rootless concepts.

→ See: [Scripts](Scripts)

---

## Key Whakapapa Terms

| Te Reo | Meaning | Application here |
|---|---|---|
| `whakapapa` | genealogy, layering-upon-layering | Concept lineage, idea inheritance |
| `mauri` | life force / essence | The aliveness of a system; what dies when over-engineered |
| `taonga` | treasure presented as gift | The Law; things too precious to lose |
| `mana` | authority, prestige, power | What a design has when it's working |
| `ira kotahi` | singular unity / singularity | When a system becomes its own origin |
| `tokotoko` | staff / tool | Scaffolding that enables but should not dominate |
| `Āe` | Yes (affirmative, embracing) | The word before "there are shit machines" |
| `kaitiakitanga` | guardianship, stewardship | How we treat the source material here |

<!-- BEGIN RECURSIVE_WEAVE -->
## Recursive Hub Weave

### Direct Connections
- [Anti-OOPedipus](Anti-OOPedipus.md)
- [DOD](DOD.md)
- [Machines](Machines.md)
- [Shmup Genealogy](Shmup-Genealogy.md)
- [Design Rules](Design-Rules.md)
- [Te Reo and Code](Te-Reo-and-Code.md)
- [Scripts](Scripts.md)

### Inbound Connections
- [AI Singularity Te Reo](AI-Singularity-Te-Reo.md)
- [Anti-OOPedipus](Anti-OOPedipus.md)
- [Design Rules](Design-Rules.md)
- [Desiring Machine](Desiring-Machine.md)
- [DOD](DOD.md)
- [Genealogy of j](Genealogy-of-j.md)
- [KELLS — Basic Units of Logic](Home.md)
- [Indigenous Proposal](Indigenous-Proposal.md)

### Lateral Bridges
#### [Design Rules](Design-Rules.md)
- Connection strength: 8
- Shared motifs: design, rules, whakapapa
#### [Te Reo and Code](Te-Reo-and-Code.md)
- Connection strength: 8
- Shared motifs: code, reo, whakapapa
#### [Anti-OOPedipus](Anti-OOPedipus.md)
- Connection strength: 7
- Shared motifs: code, whakapapa
#### [DOD](DOD.md)
- Connection strength: 7
- Shared motifs: design, whakapapa
#### [Scripts](Scripts.md)
- Connection strength: 7
- Shared motifs: design, whakapapa
#### [Genealogy of j](Genealogy-of-j.md)
- Connection strength: 6
- Shared motifs: design, genealogy, whakapapa
#### [Machines](Machines.md)
- Connection strength: 6
- Shared motifs: whakapapa
#### [AI Singularity Te Reo](AI-Singularity-Te-Reo.md)
- Connection strength: 5
- Shared motifs: reo, whakapapa

### Recursive Prompt
- In each section above, add at least one sentence that names one direct and one lateral page together.
- Convert plain mentions of those pages into markdown links for tighter recursion.
<!-- END RECURSIVE_WEAVE -->

