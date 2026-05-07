from mtg_token_generator.ai_icons import build_icon_prompt
from mtg_token_generator.models import Token


def test_icon_prompt_is_original_printable_and_excludes_mtg_symbols():
    token = Token(
        scryfall_id="1",
        set_code="tdm",
        name="Goblin",
        type_line="Token Creature — Goblin",
        power="1",
        toughness="1",
        colors=["R"],
        color_identity=["R"],
    )

    prompt = build_icon_prompt(token)

    assert "Goblin" in prompt
    assert "black icon on pure white background" in prompt
    assert "3D printing" in prompt
    assert "no Magic: The Gathering symbols" in prompt
    assert "no mana symbols" in prompt
    assert "no card frame" in prompt
