from pathlib import Path

from PIL import Image

from mtg_token_generator.ai_icons import build_icon_prompt, generate_placeholder_icon, icon_paths
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


def test_icon_paths_are_grouped_by_artifact_type(tmp_path: Path):
    token = Token(scryfall_id="1", set_code="tdm", name="Treasure", type_line="Token Artifact — Treasure")

    paths = icon_paths(token, tmp_path)

    assert paths.prompt == tmp_path / "icons" / "prompts" / "tdm-treasure.txt"
    assert paths.raw == tmp_path / "icons" / "raw" / "tdm-treasure.png"
    assert paths.processed == tmp_path / "icons" / "processed" / "tdm-treasure.png"


def test_generate_placeholder_icon_writes_square_png_and_reuses_cache(tmp_path: Path):
    token = Token(scryfall_id="1", set_code="tdm", name="Goblin", type_line="Token Creature — Goblin")
    path = tmp_path / "raw.png"

    first = generate_placeholder_icon(token, path)
    mtime = first.stat().st_mtime_ns
    second = generate_placeholder_icon(token, path, force=False)

    assert first == second == path
    assert path.stat().st_mtime_ns == mtime
    with Image.open(path) as image:
        assert image.size == (1024, 1024)
        assert image.mode == "RGB"
