from __future__ import annotations

from .models import Token


def normalize_card(raw: dict) -> Token:
    """Normalize one Scryfall card/token record into a Token.

    For double-faced token records, the first face is normalized. Future versions
    can split faces into separate Token objects, but a single-token normalizer is
    useful for tests and one-at-a-time rendering.
    """

    face = raw.get("card_faces", [{}])[0] if raw.get("card_faces") else raw
    return Token(
        scryfall_id=raw["id"],
        set_code=raw["set"].lower(),
        name=face.get("name", raw["name"]),
        type_line=face.get("type_line", raw.get("type_line", "")),
        oracle_text=face.get("oracle_text", raw.get("oracle_text")),
        power=face.get("power", raw.get("power")),
        toughness=face.get("toughness", raw.get("toughness")),
        colors=list(face.get("colors", raw.get("colors", []))),
        color_identity=list(raw.get("color_identity", face.get("color_identity", []))),
        layout=raw.get("layout"),
    )


def normalize_cards(raw_cards: list[dict]) -> list[Token]:
    """Normalize Scryfall records, splitting card faces into individual tokens."""

    tokens: list[Token] = []
    for raw in raw_cards:
        faces = raw.get("card_faces") or []
        if faces:
            for face in faces:
                merged = {**raw, "card_faces": [face]}
                tokens.append(normalize_card(merged))
        else:
            tokens.append(normalize_card(raw))
    return tokens
