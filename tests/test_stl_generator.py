from pathlib import Path

from PIL import Image, ImageDraw

from mtg_token_generator.models import Token, TokenStyle
from mtg_token_generator.stl_generator import render_stl


def test_render_stl_writes_ascii_stl_for_standard_card_size(tmp_path: Path):
    token = Token(
        scryfall_id="1",
        set_code="tdm",
        name="Goblin",
        type_line="Token Creature — Goblin",
        power="1",
        toughness="1",
    )

    stl_path = render_stl(token, TokenStyle(), tmp_path)
    text = stl_path.read_text(encoding="utf-8")

    assert stl_path.name == "tdm-goblin-1-1.stl"
    assert text.startswith("solid tdm-goblin-1-1")
    assert text.strip().endswith("endsolid tdm-goblin-1-1")
    assert "vertex 63.5000 88.9000 0.0000" in text
    assert "vertex 63.5000 88.9000 2.4000" in text


def test_render_stl_adds_bitmap_icon_relief_when_icon_path_is_provided(tmp_path: Path):
    token = Token(scryfall_id="1", set_code="tdm", name="Treasure", type_line="Token Artifact — Treasure")
    icon = tmp_path / "processed.png"
    image = Image.new("L", (16, 16), 255)
    draw = ImageDraw.Draw(image)
    draw.rectangle((6, 6, 9, 9), fill=0)
    image.save(icon)

    stl_path = render_stl(token, TokenStyle(), tmp_path, icon_path=icon)
    text = stl_path.read_text(encoding="utf-8")

    assert "relief tiles generated from processed icon" in text
    assert text.count("facet normal") > 24
    assert "vertex 27." in text or "vertex 29." in text
