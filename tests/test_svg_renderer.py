from pathlib import Path

from mtg_token_generator.models import Token, TokenStyle
from mtg_token_generator.svg_renderer import render_svg


def test_render_svg_uses_standard_card_dimensions_and_embeds_icon(tmp_path: Path):
    token = Token(
        scryfall_id="1",
        set_code="tdm",
        name="Treasure",
        type_line="Token Artifact — Treasure",
    )
    icon = tmp_path / "icon.png"
    icon.write_bytes(b"fake")

    svg_path = render_svg(token, TokenStyle(), tmp_path, icon_path=icon)
    text = svg_path.read_text(encoding="utf-8")

    assert svg_path.name == "tdm-treasure.svg"
    assert 'width="63.5mm"' in text
    assert 'height="88.9mm"' in text
    assert "Treasure" in text
    assert "Token Artifact" in text
    assert "icon.png" in text
