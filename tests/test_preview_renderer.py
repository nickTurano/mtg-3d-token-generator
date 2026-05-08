from pathlib import Path

from PIL import Image, ImageDraw

from mtg_token_generator.models import Token
from mtg_token_generator.preview_renderer import render_preview


def test_render_preview_writes_card_mockup_with_transparent_icon_and_color_marker(tmp_path: Path):
    token = Token(
        scryfall_id="1",
        set_code="tdm",
        name="Goblin",
        type_line="Token Creature — Goblin",
        oracle_text="Haste",
        power="1",
        toughness="1",
        colors=["R"],
        color_identity=["R"],
    )
    icon = tmp_path / "icons" / "processed" / "tdm-goblin-1-1.png"
    icon.parent.mkdir(parents=True)
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 56, 56), fill=(0, 0, 0, 255))
    image.save(icon)

    preview_path = render_preview(token, tmp_path, icon_path=icon)

    assert preview_path == tmp_path / "previews" / "tdm-goblin-1-1.png"
    with Image.open(preview_path) as preview:
        assert preview.size == (635, 889)
        assert preview.mode == "RGB"
        # The art panel background should show through transparent icon corners.
        assert preview.getpixel((75, 145)) != (255, 255, 255)
        # Red color identity marker should be present near top-right.
        redish_pixels = [
            pixel for pixel in preview.crop((520, 40, 610, 120)).getdata()
            if pixel[0] > 180 and pixel[1] < 120 and pixel[2] < 100
        ]
        assert redish_pixels


def test_render_preview_handles_missing_icon(tmp_path: Path):
    token = Token(scryfall_id="1", set_code="tdm", name="Treasure", type_line="Token Artifact — Treasure")

    preview_path = render_preview(token, tmp_path)

    assert preview_path.exists()
