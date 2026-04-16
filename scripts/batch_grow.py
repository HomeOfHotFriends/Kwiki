#!/usr/bin/env python3
"""
batch_grow.py — grow 30 new hub nodes through WaKa.py in one pass.
Usage: python3 scripts/batch_grow.py
"""

import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
UI   = ROOT / "scripts" / "user_input.json"

PAGES = [
    {
        "page": "DOD",
        "intent": "Lay out the full Data-Oriented Design philosophy. Connect to te_whariki_pumotu, zero_set, simplicity_of_parts, and the_law.",
        "tone": "body",
        "extra_concepts": ["zero_set", "simplicity_of_parts", "determinism"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Te-Reo-and-Code",
        "intent": "Show how te reo Māori names the codebase. Te_Whariki_Pumotu, zero_set as pūwāhi_kau. Code as whakapapa.",
        "tone": "body",
        "extra_concepts": ["mauri", "whakapapa", "ira_kotahi"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Shmup-Genealogy",
        "intent": "Trace the genealogy: DonPachi → DDP → EspRaDe → j. Each ancestor feeds the law of simplicity.",
        "tone": "body",
        "extra_concepts": ["frog_in_pot", "the_law", "positioning"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Design-Rules",
        "intent": "State the design rules Karl follows. Not mechanics — the rules below the mechanics. DOD, simplicity, enemy wave.",
        "tone": "body",
        "extra_concepts": ["determinism", "positioning", "zero_set"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Scripts",
        "intent": "Document how to use WaKa.py to grow this wiki. The generator is itself a machine shitting machines.",
        "tone": "body",
        "extra_concepts": ["dod", "whakapapa", "zero_set"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Radiative",
        "intent": "Radiative design: systems that expand outward from a simple seed. Not reactive — generative.",
        "tone": "body",
        "extra_concepts": ["the_law", "dod", "content_vs_creative", "singularity"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Singularity",
        "intent": "Ira Kotahi — the singularity. The one point that contains all directions. Tokotoko as proof.",
        "tone": "body",
        "extra_concepts": ["ira_kotahi", "tokotoko", "mauri", "whakapapa"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Frog-In-A-Pot",
        "intent": "The album. The frog. The slow boil of content-as-capture. Escape through creative product.",
        "tone": "body",
        "extra_concepts": ["content_vs_creative", "catch22", "flow_state", "esprade"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Flow-State",
        "intent": "Flow as the desiring-machine at full production. ADHD, focus, and the corridor of the game.",
        "tone": "body",
        "extra_concepts": ["desiring_machine", "shitting_machine", "catch22", "esprade"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Rhizome",
        "intent": "Deleuze and Guattari's rhizome as the underlying map of this entire wiki. No root, no crown.",
        "tone": "body",
        "extra_concepts": ["anti_oopedipus", "whakapapa", "desiring_machine", "te_whariki_pumotu"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Desiring-Machine",
        "intent": "The desiring-machine: production as primary. No lack. No law. Only flow and breakdowns.",
        "tone": "body",
        "extra_concepts": ["anti_oopedipus", "shitting_machine", "rhizome", "flow_state"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Shitting-Machine",
        "intent": "The shitting machine — what the desiring-machine produces. Product, not waste. Output as mauri.",
        "tone": "body",
        "extra_concepts": ["desiring_machine", "flow_state", "anti_oopedipus", "the_law"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Catch-22",
        "intent": "Catch-22 as the structure of content capture. You can't leave the system that's consuming you.",
        "tone": "body",
        "extra_concepts": ["content_vs_creative", "frog_in_pot", "flow_state", "anti_oopedipus"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Content-vs-Creative",
        "intent": "M-C-M prime. Content as extraction. Creative product as rupture. Bandcamp vs the algorithm.",
        "tone": "body",
        "extra_concepts": ["catch22", "frog_in_pot", "radiative", "flow_state"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Mauri",
        "intent": "Mauri as life-force and structural integrity. What makes a thing itself. Connects everything.",
        "tone": "body",
        "extra_concepts": ["ira_kotahi", "whakapapa", "taonga", "te_whariki_pumotu"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Taonga",
        "intent": "Taonga: precious things that carry mauri. The law as taonga. Code as taonga. Not metaphor.",
        "tone": "body",
        "extra_concepts": ["the_law", "mauri", "whakapapa", "ira_kotahi"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Tokotoko",
        "intent": "The walking stick. The gap-filler. The probe that confirms ground before weight is committed.",
        "tone": "body",
        "extra_concepts": ["ira_kotahi", "mauri", "singularity", "anti_oopedipus"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Ira-Kotahi",
        "intent": "Ira Kotahi: the singular breath. One life. One law. Everything that radiates from the centre.",
        "tone": "body",
        "extra_concepts": ["singularity", "mauri", "whakapapa", "tokotoko"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Zero-Set",
        "intent": "Zero_set: the empty base state all entities begin from. DOD's concept zero. pūwāhi_kau.",
        "tone": "body",
        "extra_concepts": ["te_whariki_pumotu", "dod", "simplicity_of_parts", "determinism"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Enemy-Wave",
        "intent": "The enemy wave as design unit. Spawn, position, destroy. Simplicity at the micro produces depth at the macro.",
        "tone": "body",
        "extra_concepts": ["esprade", "positioning", "simplicity_of_parts", "dod"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Positioning",
        "intent": "Position as the primary variable. X, Y, and the law. The whole game is a positioning problem.",
        "tone": "body",
        "extra_concepts": ["enemy_wave", "esprade", "dod", "the_law"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Determinism",
        "intent": "Deterministic systems: same seed, same run. Freedom through constraint. Esprade as proof.",
        "tone": "body",
        "extra_concepts": ["esprade", "dod", "positioning", "the_law", "zero_set"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Te-Whariki-Pumotu",
        "intent": "Te Whariki Pumotu: the woven floor. The namespace as marae. Every identifier placed with intention.",
        "tone": "body",
        "extra_concepts": ["dod", "zero_set", "whakapapa", "mauri", "te_whariki_pumotu"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Oedipal-Machine",
        "intent": "The Oedipal machine: the law that prohibits. OOP as Oedipus. Inheritance as genealogical capture.",
        "tone": "body",
        "extra_concepts": ["anti_oopedipus", "desiring_machine", "rhizome", "catch22"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Simplicity-of-Parts",
        "intent": "The deepest part of the law. Extreme simplicity of the parts. One struct. One function. One wave.",
        "tone": "body",
        "extra_concepts": ["the_law", "dod", "enemy_wave", "esprade", "zero_set"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Indigenous-Proposal",
        "intent": "The indigenous design proposal: sovereignty over the codebase. Māori concepts as structural, not decorative.",
        "tone": "body",
        "extra_concepts": ["whakapapa", "mauri", "taonga", "ira_kotahi", "te_whariki_pumotu"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "AI-Singularity-Te-Reo",
        "intent": "AI and te reo Māori: the singularity coming, and what Māori knowledge brings to it. Ira kotahi as frame.",
        "tone": "body",
        "extra_concepts": ["singularity", "ira_kotahi", "whakapapa", "mauri", "radiative"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Genealogy-of-j",
        "intent": "The genealogy of project j. What fed it. DonPachi, EspRaDe, DOD, the law, the album.",
        "tone": "body",
        "extra_concepts": ["esprade", "frog_in_pot", "the_law", "dod", "whakapapa"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "Production-as-Primary",
        "intent": "Production precedes the product. The machine produces before it knows what it's making. Anti-lack.",
        "tone": "body",
        "extra_concepts": ["desiring_machine", "shitting_machine", "flow_state", "anti_oopedipus", "the_law"],
        "voice_notes": "",
        "new_passage": ""
    },
    {
        "page": "The-Marae",
        "intent": "The wiki as marae. Every page a whare. Whakapapa as the meeting ground. No random links.",
        "tone": "body",
        "extra_concepts": ["whakapapa", "mauri", "taonga", "te_whariki_pumotu", "ira_kotahi"],
        "voice_notes": "",
        "new_passage": ""
    },
]


def run(ui: dict) -> bool:
    UI.write_text(json.dumps(ui, indent=2, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "WaKa.py"), "--force"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    ok = result.returncode == 0
    status = "✓" if ok else "✗"
    print(f"  {status}  {ui['page']}")
    if not ok:
        print(result.stderr[:200])
    return ok


if __name__ == "__main__":
    print(f"\nBatch growing {len(PAGES)} hub nodes via WaKa.py\n")
    ok_count = 0
    for ui in PAGES:
        if run(ui):
            ok_count += 1
    print(f"\nDone: {ok_count}/{len(PAGES)} pages written to wiki/\n")
