from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

from .models import Token


_COLOR_MOODS = {
    "W": "orderly, luminous, protective",
    "U": "mysterious, arcane, flowing",
    "B": "ominous, shadowy, macabre",
    "R": "aggressive, fiery, energetic",
    "G": "natural, wild, organic",
}


@dataclass(frozen=True)
class IconPaths:
    prompt: Path
    raw: Path
    processed: Path


def icon_paths(token: Token, output_dir: Path) -> IconPaths:
    return IconPaths(
        prompt=output_dir / "icons" / "prompts" / f"{token.slug}.txt",
        raw=output_dir / "icons" / "raw" / f"{token.slug}.png",
        processed=output_dir / "icons" / "processed" / f"{token.slug}.png",
    )


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
    paths = icon_paths(token, output_dir)
    paths.prompt.parent.mkdir(parents=True, exist_ok=True)
    paths.prompt.write_text(build_icon_prompt(token), encoding="utf-8")
    return paths.prompt


def generate_placeholder_icon(token: Token, path: Path, force: bool = False, size: int = 1024) -> Path:
    """Generate a deterministic local icon placeholder.

    This is intentionally not marketed as final art; it gives the v0.2 pipeline
    real raster silhouettes to process, embed, and convert into STL relief while
    a real image-generation provider is wired in later.
    """

    if path.exists() and not force:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(image)
    lower = f"{token.name} {token.type_line}".lower()
    if "treasure" in lower:
        draw.polygon([(512, 190), (810, 470), (512, 835), (214, 470)], fill="black")
        draw.polygon([(512, 290), (690, 470), (512, 720), (334, 470)], fill="white")
    elif "clue" in lower:
        draw.ellipse((235, 210, 675, 650), outline="black", width=90)
        draw.line((640, 620, 830, 810), fill="black", width=95)
    elif "food" in lower:
        draw.pieslice((210, 260, 814, 880), start=0, end=180, fill="black")
        draw.rectangle((230, 560, 794, 705), fill="black")
    elif "blood" in lower:
        draw.polygon([(512, 145), (745, 530), (512, 870), (279, 530)], fill="black")
        draw.ellipse((298, 435, 726, 895), fill="black")
    elif token.is_creature:
        draw.ellipse((320, 255, 704, 690), fill="black")
        draw.polygon([(370, 310), (245, 175), (470, 250)], fill="black")
        draw.polygon([(654, 310), (779, 175), (554, 250)], fill="black")
        draw.ellipse((415, 430, 465, 480), fill="white")
        draw.ellipse((559, 430, 609, 480), fill="white")
    else:
        draw.polygon([(512, 170), (600, 410), (850, 410), (645, 555), (730, 805), (512, 650), (294, 805), (379, 555), (174, 410), (424, 410)], fill="black")
    image.save(path)
    return path
