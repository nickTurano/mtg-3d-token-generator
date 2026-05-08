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
        assert out.mode == "RGBA"
        alpha_values = set(out.getchannel("A").getdata())
        assert alpha_values <= {0, 255}
        assert out.getpixel((0, 0))[3] == 0
        assert out.getchannel("A").getbbox() is not None
        opaque_pixels = [pixel for pixel in out.getdata() if pixel[3] == 255]
        assert opaque_pixels
        assert all(pixel[:3] == (0, 0, 0) for pixel in opaque_pixels)
