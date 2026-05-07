from pathlib import Path

from mtg_token_generator.pipeline import generate_from_tokens
from mtg_token_generator.models import Token


def test_generate_from_tokens_writes_metadata_prompts_svg_and_stl(tmp_path: Path):
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

    outputs = generate_from_tokens([token], tmp_path)

    assert (tmp_path / "tokens.json").exists()
    assert (tmp_path / "icons" / "prompts" / "tdm-goblin-1-1.txt").exists()
    assert (tmp_path / "svg" / "tdm-goblin-1-1.svg").exists()
    assert (tmp_path / "stl" / "tdm-goblin-1-1.stl").exists()
    assert outputs["svg"] == [tmp_path / "svg" / "tdm-goblin-1-1.svg"]
