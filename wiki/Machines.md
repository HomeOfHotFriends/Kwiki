# Machines

> *There are shit machines. There are shitting machines.*  
> *Shitting machines do not need to be shit machines.*  
> *There can be shit shitting machines.*

---

## Desiring-Machines (Deleuze & Guattari)

In *Anti-Oedipus*, everything is a machine. Machines connect to other machines. A mouth-machine connects to a breast-machine and produces a flow of milk. A hand-machine connects to a tool-machine and produces a cut. Desire is not lack — it is **production**. The desiring-machine produces by connecting and cutting flows.

Three syntheses define how machines work:

| Synthesis | Operation | Code analogue |
|---|---|---|
| **Connective** | `and-then`: production of production | Spawn event → bullet array |
| **Disjunctive** | `either-or`: recording, inscription | Behaviour enum, mode flags |
| **Conjunctive** | `so it's...`: consumption, identity | Frame result, player score |

The social body (*socius*) codes and overcodes these flows — captures them, assigns them names and purposes, makes them serve a hierarchy. **Anti-OOPedipus refuses the socius of OOP.**

---

## Machine Types in the Codebase

The indigenous proposal defines an explicit ontology drawn from Te Reo Māori and DOD logic:

### `zero_set` — The State Enum

```cpp
enum zero_set {
    pūwāhi_kau,      // empty space — the void, the unmarked
    pūtake_aukati,   // boundary suppression — the wall, the limit
    huinga_whakaputa,// output set — the producer, the emitter
    katinotoa,       // inert — present but not participating
    kauaeheahea,     // ethereal — phase-shifted, ghost state
    huinga_kōwhiringa// selection set — the query, the active filter
};
```

These are not "tile types." They are **machine states**. Each cell in `Te_Whariki_Pumotu` (the 19×19 world) is a machine that is currently in one of these states. State is not identity — it is present configuration.

---

### `Te_Whariki_Pumotu` — The World as Woven Mat

```cpp
struct Te_Whariki_Pumotu {
    static constexpr unsigned int whānui = 19;  // width
    static constexpr unsigned int teitei = 19;  // height
    std::array<zero_set, whānui * teitei> ngā_zero_set{};
    // ...
};
```

`Te Whariki` — the woven mat. In Māori culture: the foundation you lay before anything else is placed. Here: the spatial substrate of the world. A flat 19×19 array — no scene graph, no spatial hierarchy, no parent transforms. DOD. Flat. Woven.

The methods are Māori verbs:
- `whakawātea()` — to clear, to free (fill with `pūwāhi_kau`)
- `whakatakoto()` — to lay down, to place (set a cell's state)
- `pānui()` — to read, to announce (get a cell's state)
- `tāpiri()` — to add, to join (composite another mat onto this one with offset)

These aren't "set/get." They are **acts** with cultural weight.

---

### Gate Machines and Mode Machines

The system defines higher-level flow machines:

```
gates:    collapse | flow | deaf | blind
modes:    M_pair | M_pass | M_xiso | M_yiso | M_halt
```

```
bridge_eval:
  collapse → M_halt
  pass     → M_pass
  flow     → M_pair.FLOW
  deaf     → M_pair.DEAF
  blind    → M_pair.BLIND
  _        → M_pair.FULL
```

This is a **state machine for state machines** — the shit shitting machine. The `bridge_eval` function is the meta-production: it takes a gate condition and produces a mode, which governs how the X/Y plane data flows through a bytepair.

---

### The GrowingHome Machine (Rust)

From the `indigenous_proposal` — a circuit-builder named `GrowingHome`:

```rust
// Circuits grown from NAND:
// nand → nor (grown from nand)
// nand → xor (grown from nand)
```

The language is `.reo` (Te Reo shorthand). Circuits are not declared — they **grow**. This is the exact Anti-OOPedipus move: composition over inheritance. A NOR gate is not a child of NAND. It is NAND *applied to itself*. The genealogy is not descent — it is **self-application and recombination**.

The `CircuitLibrary` grows. It does not inherit.

---

## The Bullet as Pure Machine

From the esprade analysis: a bullet in EspRaDe is the purest machine in the design school.

```
bullet = { x, y, dx, dy }   // values locked at spawn
```

No curve. No acceleration after birth. Simple parts. But 200 of them, spawned in patterns that interact with movement, hitbox position, and other bullets — the *combinatory depth* is the product of their **relationship**, not their individual complexity.

> The connective synthesis: bullet connects to player-hitbox-machine → produces either collision event or miss-flow.

The desiring-machine doesn't care about category. The bullet machine connects or it doesn't. There is no Oedipal question here ("which class is this bullet?"). There is only: does this point intersect that box?

---

## Whakapapa

- Upstream: [Anti-OOPedipus](Anti-OOPedipus), [Whakapapa](Whakapapa)
- Downstream: [DOD](DOD), [Te Reo and Code](Te-Reo-and-Code), [Design Rules](Design-Rules)
- The Law applied: [The Law](The-Law)

<!-- BEGIN RECURSIVE_WEAVE -->
## Recursive Hub Weave

### Direct Connections
- [Anti-OOPedipus](Anti-OOPedipus.md)
- [Whakapapa — Genealogy of Ideas](Whakapapa.md)
- [DOD](DOD.md)
- [Te Reo and Code](Te-Reo-and-Code.md)
- [Design Rules](Design-Rules.md)
- [The Law](The-Law.md)

### Inbound Connections
- [Anti-OOPedipus](Anti-OOPedipus.md)
- [KELLS — Basic Units of Logic](Home.md)
- [Whakapapa — Genealogy of Ideas](Whakapapa.md)

### Lateral Bridges
#### [Anti-OOPedipus](Anti-OOPedipus.md)
- Connection strength: 8
- Shared motifs: machine, machines, whakapapa
#### [DOD](DOD.md)
- Connection strength: 7
- Shared motifs: pumotu, set, whakapapa, whariki, zero
#### [Te Reo and Code](Te-Reo-and-Code.md)
- Connection strength: 7
- Shared motifs: pumotu, set, whakapapa, whariki, zero
#### [Whakapapa — Genealogy of Ideas](Whakapapa.md)
- Connection strength: 6
- Shared motifs: whakapapa
#### [Rhizome](Rhizome.md)
- Connection strength: 5
- Shared motifs: desiring, machine, pumotu, whakapapa, whariki
#### [Te Whariki Pumotu](Te-Whariki-Pumotu.md)
- Connection strength: 5
- Shared motifs: pumotu, set, whakapapa, whariki, zero
#### [Production as Primary](Production-as-Primary.md)
- Connection strength: 4
- Shared motifs: desiring, machine, state, whakapapa
#### [Zero Set](Zero-Set.md)
- Connection strength: 4
- Shared motifs: pumotu, set, whariki, zero

### Recursive Prompt
- In each section above, add at least one sentence that names one direct and one lateral page together.
- Convert plain mentions of those pages into markdown links for tighter recursion.
<!-- END RECURSIVE_WEAVE -->

