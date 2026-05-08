from __future__ import annotations

import os
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .models import Token

PREVIEW_WIDTH_PX = 635
PREVIEW_HEIGHT_PX = 889

_COLOR_MARKERS = {
    "W": ((245, 240, 214), (20, 20, 20), "W"),
    "U": ((74, 163, 223), (20, 20, 20), "U"),
    "B": ((59, 53, 47), (255, 255, 255), "B"),
    "R": ((227, 91, 54), (20, 20, 20), "R"),
    "G": ((89, 166, 90), (20, 20, 20), "G"),
}
_COLOR_TINTS = {
    "W": (247, 239, 210),
    "U": (184, 216, 235),
    "B": (203, 193, 190),
    "R": (235, 190, 170),
    "G": (190, 222, 185),
}


def _font(size: int, bold: bool = False, serif: bool = False):
    family = "DejaVuSerif" if serif else "DejaVuSans"
    name = f"{family}-Bold.ttf" if bold else f"{family}.ttf"
    path = f"/usr/share/fonts/truetype/dejavu/{name}"
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _fit_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = (text or "").replace("\n", " ").split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
            continue
        if current:
            lines.append(current)
        if draw.textbbox((0, 0), word, font=font)[2] > max_width:
            chunks = textwrap.wrap(word, width=18)
            lines.extend(chunks[:-1])
            current = chunks[-1] if chunks else ""
        else:
            current = word
    if current:
        lines.append(current)
    return lines


def _background_color(token: Token) -> tuple[int, int, int]:
    colors = token.color_identity or token.colors
    if not colors:
        return (230, 224, 211)
    tints = [_COLOR_TINTS.get(color, (230, 224, 211)) for color in colors]
    return tuple(sum(tint[i] for tint in tints) // len(tints) for i in range(3))


def _draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], text: str, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = xy[0] + (xy[2] - xy[0] - width) // 2
    y = xy[1] + (xy[3] - xy[1] - height) // 2 - 1
    draw.text((x, y), text, font=font, fill=fill)


def _draw_color_identity(draw: ImageDraw.ImageDraw, token: Token, font):
    colors = token.color_identity or token.colors or ["C"]
    radius = 16
    spacing = 38
    start_x = PREVIEW_WIDTH_PX - 64 - spacing * (len(colors) - 1)
    y = 74
    for index, color in enumerate(colors):
        fill, text_fill, label = _COLOR_MARKERS.get(color, ((217, 209, 191), (20, 20, 20), "C"))
        cx = start_x + spacing * index
        draw.ellipse((cx - radius, y - radius, cx + radius, y + radius), fill=fill, outline=(20, 20, 20), width=2)
        _draw_centered(draw, (cx - radius, y - radius, cx + radius, y + radius), label, font, text_fill)


def _paste_icon(card: Image.Image, icon_path: Path | None, art_box: tuple[int, int, int, int]):
    draw = ImageDraw.Draw(card)
    if icon_path is None or not icon_path.exists():
        cx = (art_box[0] + art_box[2]) // 2
        cy = (art_box[1] + art_box[3]) // 2
        draw.polygon([(cx, cy - 120), (cx + 95, cy), (cx, cy + 120), (cx - 95, cy)], fill=(35, 32, 28))
        return

    icon = Image.open(icon_path).convert("RGBA")
    bbox = icon.getbbox()
    if bbox:
        icon = icon.crop(bbox)
    max_art = (art_box[2] - art_box[0] - 54, art_box[3] - art_box[1] - 54)
    icon.thumbnail(max_art, Image.Resampling.LANCZOS)
    x = (art_box[0] + art_box[2] - icon.width) // 2
    y = (art_box[1] + art_box[3] - icon.height) // 2
    card.paste(icon, (x, y), icon)


def render_preview(token: Token, output_dir: Path, icon_path: Path | None = None) -> Path:
    """Render a PNG card mockup preview for one generated token."""

    preview_dir = output_dir / "previews"
    preview_dir.mkdir(parents=True, exist_ok=True)
    output_path = preview_dir / f"{token.slug}.png"

    title_font = _font(38, bold=True, serif=True)
    type_font = _font(23, bold=True)
    text_font = _font(24)
    pt_font = _font(30, bold=True)
    marker_font = _font(18, bold=True)

    card = Image.new("RGB", (PREVIEW_WIDTH_PX, PREVIEW_HEIGHT_PX), _background_color(token))
    draw = ImageDraw.Draw(card)

    margin = 28
    draw.rounded_rectangle((10, 10, PREVIEW_WIDTH_PX - 10, PREVIEW_HEIGHT_PX - 10), radius=36, fill=(35, 32, 28), outline=(15, 14, 12), width=4)
    draw.rounded_rectangle((margin, margin, PREVIEW_WIDTH_PX - margin, PREVIEW_HEIGHT_PX - margin), radius=26, fill=(238, 232, 218), outline=(70, 60, 48), width=3)

    title_box = (45, 45, PREVIEW_WIDTH_PX - 45, 104)
    draw.rounded_rectangle(title_box, radius=18, fill=(248, 244, 232), outline=(95, 80, 62), width=2)
    draw.text((62, 58), token.name, font=title_font, fill=(35, 28, 22))
    _draw_color_identity(draw, token, marker_font)

    art_box = (58, 126, PREVIEW_WIDTH_PX - 58, 564)
    draw.rounded_rectangle(art_box, radius=18, fill=(212, 205, 192), outline=(85, 72, 55), width=3)
    _paste_icon(card, icon_path, art_box)

    type_box = (45, 586, PREVIEW_WIDTH_PX - 45, 634)
    draw.rounded_rectangle(type_box, radius=14, fill=(248, 244, 232), outline=(95, 80, 62), width=2)
    type_lines = _fit_text(draw, token.type_line, type_font, type_box[2] - type_box[0] - 28)
    draw.text((62, 597), type_lines[0] if type_lines else token.type_line, font=type_font, fill=(35, 28, 22))

    text_box = (45, 654, PREVIEW_WIDTH_PX - 45, 820)
    draw.rounded_rectangle(text_box, radius=16, fill=(248, 244, 232), outline=(95, 80, 62), width=2)
    text_lines = _fit_text(draw, token.oracle_text or "", text_font, text_box[2] - text_box[0] - 32)
    y = 674
    for line in text_lines[:5]:
        draw.text((62, y), line, font=text_font, fill=(35, 28, 22))
        y += 32

    if token.power is not None and token.toughness is not None:
        pt_text = f"{token.power}/{token.toughness}"
        box = (PREVIEW_WIDTH_PX - 151, PREVIEW_HEIGHT_PX - 88, PREVIEW_WIDTH_PX - 45, PREVIEW_HEIGHT_PX - 38)
        draw.rounded_rectangle(box, radius=14, fill=(248, 244, 232), outline=(55, 45, 35), width=3)
        _draw_centered(draw, box, pt_text, pt_font, (25, 20, 15))

    card.save(output_path)
    return output_path
