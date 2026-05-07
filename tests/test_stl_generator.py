from pathlib import Path

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
