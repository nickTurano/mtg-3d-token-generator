from __future__ import annotations

from pathlib import Path

from .models import Token


_COLOR_MOODS = {
    "W": "orderly, luminous, protective",
    "U": "mysterious, arcane, flowing",
    "B": "ominous, shadowy, macabre",
    "R": "aggressive, fiery, energetic",
    "G": "natural, wild, organic",
}


def build_icon_prompt(token: Token) -> str:
    """Build a guardrailed prompt for an original printable token icon."""

    colors = token.color_identity or token.colors
    mood = ", ".join(_COLOR_MOODS.get(color, color) for color in colors) or "neutral tabletop fantasy"
    subject = token.name
    return f"""Create an original monochrome icon for a tabletop gaming token.

Subject: {subject}
Token type: {token.type_line}
Mood inspiration: {mood}

Design requirements:
- black icon on pure white background
- centered composition
- simple bold silhouette
- thick connected shapes
- no text
- no numbers
- no border
- no card frame
- no logos
- no Magic: The Gathering symbols
- no mana symbols
- no set symbols
- no copyrighted characters
- readable when printed as a raised 3D printing relief at standard trading-card size
- minimal fine detail
- suitable for thresholding, vectorization, and 3D printing
""".strip()


def write_icon_prompt(token: Token, output_dir: Path) -> Path:
    prompt_dir = output_dir / "icons" / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    path = prompt_dir / f"{token.slug}.txt"
    path.write_text(build_icon_prompt(token), encoding="utf-8")
    return path
