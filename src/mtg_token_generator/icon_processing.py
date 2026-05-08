from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


def process_icon(raw_path: Path, processed_path: Path, size: int = 256, margin_px: int = 28, threshold: int = 200) -> Path:
    """Convert a raw icon into a centered black silhouette with transparent background."""

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(raw_path) as image:
        gray = ImageOps.grayscale(image)
        bw = gray.point(lambda pixel: 0 if pixel < threshold else 255, mode="L")
        # Find non-white content. Invert so black subject becomes bbox content.
        bbox = ImageOps.invert(bw).getbbox()
        if bbox is None:
            out_l = Image.new("L", (size, size), 255)
        else:
            cropped = bw.crop(bbox)
            max_dim = max(1, size - 2 * margin_px)
            cropped.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
            cropped = cropped.point(lambda pixel: 0 if pixel < 200 else 255, mode="L")
            out_l = Image.new("L", (size, size), 255)
            x = (size - cropped.width) // 2
            y = (size - cropped.height) // 2
            out_l.paste(cropped, (x, y))
        alpha = out_l.point(lambda pixel: 255 if pixel < 255 else 0, mode="L")
        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        out.putalpha(alpha)
        out.save(processed_path)
    return processed_path
