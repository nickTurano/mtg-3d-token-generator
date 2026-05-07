from mtg_token_generator.models import Token, TokenStyle


def test_token_slug_includes_set_name_and_power_toughness():
    token = Token(
        scryfall_id="abc",
        set_code="tdm",
        name="Goblin Warrior",
        type_line="Token Creature — Goblin Warrior",
        power="1",
        toughness="1",
        colors=["R"],
        color_identity=["R"],
    )

    assert token.slug == "tdm-goblin-warrior-1-1"
    assert token.is_creature is True


def test_card_style_defaults_to_standard_mtg_card_size():
    style = TokenStyle()

    assert style.width_mm == 63.5
    assert style.height_mm == 88.9
    assert style.corner_radius_mm == 3.0
