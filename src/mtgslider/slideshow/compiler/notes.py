"""Speaker notes generators. One function per preset's notes_mode.

These are deterministic — they read from packet data, not from any LLM.
The voice differences are real (different prose, different emphases) but bounded:
the generator can only restate facts already in the packet.
"""
from __future__ import annotations

from typing import Any


def for_unit(unit_content: dict, slide_type: str, *, mode: str, theme: dict) -> str:
    if mode == "rich":
        return _rich(unit_content, slide_type, theme)
    if mode == "terse":
        return _terse(unit_content, slide_type, theme)
    if mode == "heuristic":
        return _heuristic(unit_content, slide_type, theme)
    return ""


# ---------- rich (Rhystic-voice) ----------

def _rich(c: dict, slide_type: str, theme: dict) -> str:
    name = theme["canonical_name"]
    if slide_type == "thesis":
        return (
            f"Open by setting the scope. We're surveying {name} — not as a tournament archetype, "
            "but as a thread you can pull through Magic's history. Pause after the title. "
            "Let the audience ask 'what counts?' before you answer it."
        )
    if slide_type == "definition":
        examples = c.get("examples") or []
        ex_str = (" Aliases include: " + ", ".join(examples) + ".") if examples else ""
        return (
            f"Define the boundary. {c.get('definition','')}{ex_str} "
            "The point isn't to be exhaustive — it's to give the audience a yardstick they can apply themselves."
        )
    if slide_type == "card_spotlight":
        card = c.get("card", {})
        cname = card.get("card_name", "")
        why = c.get("claim") or card.get("link_reason") or ""
        return (
            f"Sit with this one. {cname} matters here because: {why}. "
            "Don't just narrate the rules text — name what makes the card belong to this thread."
        )
    if slide_type == "visual_motif":
        return (
            "Read the artwork as evidence. What recurs across these images — colors, postures, objects, "
            "settings? The motif is doing work even when the rules text doesn't mention it."
        )
    if slide_type == "conclusion":
        return (
            "Close on the question, not the inventory. What did this survey teach us about how Magic "
            "uses this thread? Where would the next slide go if we kept walking?"
        )
    return ""


# ---------- terse (Sierkovitz-voice) ----------

def _terse(c: dict, slide_type: str, theme: dict) -> str:
    if slide_type == "thesis":
        return f"Scope: {theme['canonical_name']}. Curated, not exhaustive. Move briskly."
    if slide_type == "data":
        stats = c.get("stats", {})
        return (
            f"{stats.get('card_count', 0)} cards in the included set. "
            f"Color distribution and type breakdown shown. Don't read the table — point at the outliers."
        )
    if slide_type == "card_spotlight":
        card = c.get("card", {})
        return f"{card.get('card_name','')}: {c.get('claim','')[:120]}"
    if slide_type == "cluster":
        cards = c.get("cards") or []
        return f"{len(cards)} cards. Two sentences max — they speak for themselves."
    if slide_type == "conclusion":
        return "State the takeaway. Move to Q&A."
    return ""


# ---------- heuristic (teaching voice) ----------

def _heuristic(c: dict, slide_type: str, theme: dict) -> str:
    if slide_type == "thesis":
        return (
            f"Frame what students will learn: how to recognize {theme['canonical_name']} cards "
            "when they see one in a draft, a binder, or a deck list."
        )
    if slide_type == "definition":
        return (
            "Give them the working definition, then the test: 'when you see this kind of card, "
            "ask yourself — does it belong to the thread?' Repeat the definition once, slowly."
        )
    if slide_type == "card_spotlight":
        card = c.get("card", {})
        cname = card.get("card_name", "")
        return (
            f"Walk through {cname} as an example. Point at the specific text or art that makes it qualify. "
            "Then ask: what's a near-miss card that wouldn't qualify, and why?"
        )
    if slide_type == "key_takeaways":
        return (
            "Summarize the heuristics they should leave with. Three is plenty. "
            "If you find yourself wanting four, the third is probably weak — cut it."
        )
    if slide_type == "conclusion":
        return "Quick recap. Invite questions about edge cases — that's where the learning lives."
    return ""
