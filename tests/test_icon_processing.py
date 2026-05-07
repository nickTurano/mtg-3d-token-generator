from pathlib import Path

from PIL import Image, ImageDraw

from mtg_token_generator.icon_processing import process_icon


def test_process_icon_outputs_square_black_white_silhouette_with_margin(tmp_path: Path):
    raw = tmp_path / "raw.png"
    processed = tmp_path / "processed.png"
    image = Image.new("RGB", (100, 100), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((20, 30, 80, 70), fill=(20, 20, 20))
    image.save(raw)

    result = process_icon(raw, processed, size=64, margin_px=8)

    assert result == processed
    with Image.open(processed) as out:
        assert out.size == (64, 64)
        values = set(out.convert("L").getdata())
        assert values <= {0, 255}
        assert out.convert("L").getpixel((0, 0)) == 255
        assert out.convert("L").getbbox() == (0, 0, 64, 64)
