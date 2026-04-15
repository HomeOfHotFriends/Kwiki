# The Law

> *There is one law that I know. Only one I can state as truth.*  
> *It is my most precious stone and I present it as **taonga**.*

---

## The Law

**Extreme depth of the whole achieved through extreme simplicity of the parts.**

---

## Taonga

In Te Ao Māori, **taonga** is a treasure — but not in the Western sense of hoarded wealth. Taonga is a gift that obligates. It is presented, not kept. To receive taonga is to receive responsibility. The Māori concept of kaitiakitanga (guardianship) activates the moment taonga changes hands.

This law is taonga. It is presented here once, at the root of every page, and it obligates every design decision made from this point. If a decision makes parts more complex to produce depth, the law is broken. If depth is sacrificed to keep parts simple, the law is honoured incorrectly — simplicity without depth is just emptiness.

The law is not a trick. It is the most compressed possible statement of everything the esprade analysis, Anti-OOPedipus, and the DOD approach are trying to say.

---

## The Law in Evidence: EspRaDe

**Bullet:** `{ x, y, dx, dy }` — four values, locked at birth.  
**Enemy body:** a moving spawn point.  
**Pattern:** a function that determines bullet spawn position, trajectory, speed, and time from a small set of parameters.  

From these: ~200 bullets per frame, patterns that interact with each other, the player's position, the player's hitbox (a few pixels), and the player's movement speed (two values: focused/unfocused). From four values per bullet and two values per player: a game that rewards thousands of hours of play. The depth is *emergent* — it is not stored anywhere in the code. It is produced by the simplicity connecting to itself.

> The Law as loop: simple parts → maximum combinatory space → emergent depth → player experience of infinite variation → the loop justifies the simplicity.

---

## The Law in Evidence: Anti-Oedipus

Deleuze and Guattari's method: molecular concepts, simple definitions (machine, flow, cut, recording) that combine into extraordinary conceptual depth. The book is not "hard" because the ideas are complex. It is hard because **you have to hold many simple ideas in relation simultaneously** and follow their interactions. The depth is combinatory, not intrinsic.

The same structure as EspRaDe. The same Law.

---

## The Law in Evidence: Te Whariki Pumotu

```cpp
enum zero_set { pūwāhi_kau, pūtake_aukati, huinga_whakaputa,
                katinotoa, kauaeheahea, huinga_kōwhiringa };
```

Six states. A 19×19 grid. The interactions between these six states — which cells are adjacent, which are in which state, how `tāpiri()` (composition) works — produce the spatial language of the game world. Six states. World-building capacity.

---

## The Law as Ira Kotahi

From the AI singularity essay in Te Reo Māori:

> *Ko te "ira kotahi" he "single digit"*  
> *(The ira kotahi is a single digit)*

Ira kotahi — the singular unity. In Māori mathematics: the number 1. In the ontological sense: the moment of self-unity, where complexity collapses back to a simple origin. The Law operates like ira kotahi: extreme simplicity that contains all possible depth. It is the origin of the tree, not the tree itself.

The Law is not complicated. It takes one sentence. From it: everything.

---

## The Violation

Every known violation of the Law follows the same pattern:

**Step 1:** The parts are made more complex to handle "edge cases" or "anticipated future needs."  
**Step 2:** The combinatory space collapses because complex parts interfere with each other unpredictably.  
**Step 3:** The depth of the whole *decreases* even as the complexity of the parts increases.  
**Step 4:** The game (or system, or codebase) becomes brittle. Iteration slows. The machine stops producing.

From the esprade doc, the failed shmup project:

> *My system of ultimate expression was agonising to experiment and iterate with, AND boxed me into even more rigid corners than the limitations I believed would arise from having a spawning system where each enemy type A has the same speed value.*

He built complex parts seeking maximum control. The maximum-control machine produced minimum emergent depth. The hierarchy (timed spawns locked to architecture) prevented the very thing he was trying to produce. The Oedipal machine reasserted itself through the back door of "granular control."

---

## Keeping the Law

The Law is not kept by intelligence. It is kept by **discipline and restraint** — by refusing to add complexity to parts even when it feels like the "right" solution. The constraint is the gift. The limit is what produces the depth.

This is kaitiakitanga applied to design: guard the simplicity of the parts as if they are taonga. They are.

---

## Whakapapa

- Upstream: [Whakapapa](Whakapapa), [Anti-OOPedipus](Anti-OOPedipus)
- Downstream: [DOD](DOD), [Design Rules](Design-Rules), [Machines](Machines)
- In code: [Te Reo and Code](Te-Reo-and-Code)
