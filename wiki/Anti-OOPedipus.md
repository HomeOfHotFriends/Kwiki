# Anti-OOPedipus

> *Welcoming Anti-Oedipus. Welcoming Anti-Œdipus. Welcoming Anti-O^O.P.-dipus.*

> *On the prohibition and the refusal of genealogical machines.*

---

## The Argument

**Deleuze and Guattari** wrote *Anti-Oedipus* to destroy a specific machine: the Oedipal triangle. Psychoanalysis takes the infinite productive force of desire — flows, connections, assemblages — and reduces it to a family drama. Mummy. Daddy. Me. Every desire coded back to lack, to prohibition, to the Father's law.

**Anti-OOPedipus** makes the same argument about Object-Oriented Programming.

OOP takes the productive capacity of data and behaviour — flows, arrays, transformations — and forces it into a family drama. Every object must have a class. Every class must have a parent. Every behaviour must descend from a hierarchy. The Gang of Four are the psychoanalysts. The inheritance tree is the Oedipal triangle. The `virtual override` is the law of the father.

The question is not "is OOP bad?" The question is: **what gets prohibited when you commit to hierarchy as the default?**

---

## The Oedipal Machine in Code

In classical OOP inheritance:

```
Entity
  └── Actor
        └── Enemy
              └── Boss
                    └── FinalBoss
```

This is not a natural structure produced by the problem. It is a *social coding* of the problem — the insistence that everything must have a parent, that relationship must be expressed as descent, that the identity of a thing is produced by what it came from rather than what it *does*.

The pathology:

- **Fragile base class problem** — changing the parent breaks the children; the father's law reaches forward through time
- **Diamond problem** — when two parents conflict, the hierarchy produces contradiction it cannot resolve
- **Deep call stacks** — to understand what anything does, you must climb the genealogical tree
- **God classes** — the hierarchical pressure to centralise produces the Oedipal father: one class that everything depends on, that must not be touched

---

## What DOD Refuses

Data-Oriented Design does not begin with objects. It begins with **what data exists and how it changes**.

```c
// OOP (genealogical machine)
class Enemy {
    virtual void update() = 0;  // the father demands you implement
};

// DOD (desiring-machine)
struct BulletData { float x, y, dx, dy; };
BulletData bullets[MAX_BULLETS];  // flat. no parent. flows.
```

The DOD approach says: the machine is the array and the transform. The identity of a bullet is not its class — it is its position, velocity, and what happens to them each frame. The "type" of a bullet is its data, not its genealogy.

This is the desiring-machine: it produces through connection and flow, not through descent and prohibition.

---

## The Shitting Machines Passage

> *h okay. on the shitting. on the shit machines. Āe, yes.*  
> *There are shit machines. There are shitting machines.*  
> *Shitting machines do not need to be shit machines.*  
> *The flow-state permits the meta-function:*  
> *There can be shit shitting machines.*  
> *A tautology of the production/product-cycle.*

`IBM Plex Mono gloss:` This is the DOD loop stated in Anti-Oedipus language. A *shitting machine* is a system that produces output through a transform applied to input data — a process-machine. A *shit machine* is a system defined by its product — an output-machine. The insight: **a process-machine does not need to be an output-machine.** The bullet spawner does not care about bullets — it cares about spawn events. The bullets care about position. Neither is a parent of the other.

The "shit shitting machine" is the meta-system: a machine that produces other machines. This is DOD architecture — a data pipeline that produces transforms that produce outputs. No hierarchy. Only flow.

---

## The Prohibition

The refusal in the title refers to a specific machine Karl refuses to build: **the genealogical machine** — the system that codes every new idea or component by reducing it to its parent, its origin, its Oedipal position.

In OOP: every new class must find its parent.  
In design: every new mechanic must fit the existing hierarchy.  
In philosophy: every new thought must be grounded in an authoritative lineage.

Anti-OOPedipus is not chaos. It is not "no rules." The Law still exists:

> *Extreme depth of the whole achieved through extreme simplicity of the parts.*

But the law generates complexity through **relationship and flow**, not through **descent and inheritance**.

---

## Whakapapa

- Upstream: [Whakapapa](Whakapapa), Deleuze & Guattari *Anti-Oedipus* (1972)
- Downstream: [Machines](Machines), [DOD](DOD), [The Law](The-Law)
- Code manifestation: [Te Reo and Code](Te-Reo-and-Code)

<!-- BEGIN RECURSIVE_WEAVE -->
## Recursive Hub Weave

### Direct Connections
- [Whakapapa — Genealogy of Ideas](Whakapapa.md)
- [Machines](Machines.md)
- [DOD](DOD.md)
- [The Law](The-Law.md)
- [Te Reo and Code](Te-Reo-and-Code.md)

### Inbound Connections
- [Content vs Creative](Content-vs-Creative.md)
- [Desiring Machine](Desiring-Machine.md)
- [Flow State](Flow-State.md)
- [Frog In A Pot](Frog-In-A-Pot.md)
- [KELLS — Basic Units of Logic](Home.md)
- [Ira Kotahi](Ira-Kotahi.md)
- [Machines](Machines.md)
- [Oedipal Machine](Oedipal-Machine.md)

### Lateral Bridges
#### [Machines](Machines.md)
- Connection strength: 8
- Shared motifs: machine, machines, whakapapa
#### [Production as Primary](Production-as-Primary.md)
- Connection strength: 8
- Shared motifs: anti, machine, oopedipus, shitting, whakapapa
#### [Desiring Machine](Desiring-Machine.md)
- Connection strength: 7
- Shared motifs: anti, machine, oopedipus, shitting
#### [Oedipal Machine](Oedipal-Machine.md)
- Connection strength: 7
- Shared motifs: anti, machine, oedipal, oopedipus
#### [Rhizome](Rhizome.md)
- Connection strength: 7
- Shared motifs: anti, machine, oopedipus, whakapapa
#### [Shitting Machine](Shitting-Machine.md)
- Connection strength: 7
- Shared motifs: anti, machine, oopedipus, shitting
#### [Te Reo and Code](Te-Reo-and-Code.md)
- Connection strength: 7
- Shared motifs: code, whakapapa
#### [Whakapapa — Genealogy of Ideas](Whakapapa.md)
- Connection strength: 7
- Shared motifs: code, whakapapa

### Recursive Prompt
- In each section above, add at least one sentence that names one direct and one lateral page together.
- Convert plain mentions of those pages into markdown links for tighter recursion.
<!-- END RECURSIVE_WEAVE -->

