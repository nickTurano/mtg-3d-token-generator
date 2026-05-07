from mtg_token_generator.normalize import normalize_card


def test_normalize_simple_creature_token_card():
    raw = {
        "id": "scry-id",
        "set": "tdm",
        "name": "Goblin",
        "type_line": "Token Creature — Goblin",
        "power": "1",
        "toughness": "1",
        "colors": ["R"],
        "color_identity": ["R"],
        "layout": "token",
    }

    token = normalize_card(raw)

    assert token.scryfall_id == "scry-id"
    assert token.set_code == "tdm"
    assert token.name == "Goblin"
    assert token.is_creature is True
    assert token.slug == "tdm-goblin-1-1"


def test_normalize_prefers_first_card_face_for_faced_token():
    raw = {
        "id": "face-id",
        "set": "abc",
        "name": "Spirit // Treasure",
        "layout": "double_faced_token",
        "card_faces": [
            {
                "name": "Spirit",
                "type_line": "Token Creature — Spirit",
                "power": "1",
                "toughness": "1",
                "colors": ["W"],
                "oracle_text": "Flying",
            },
            {"name": "Treasure", "type_line": "Token Artifact — Treasure", "colors": []},
        ],
        "color_identity": ["W"],
    }

    token = normalize_card(raw)

    assert token.name == "Spirit"
    assert token.type_line == "Token Creature — Spirit"
    assert token.oracle_text == "Flying"
    assert token.color_identity == ["W"]
