from __future__ import annotations

from pathlib import Path

from PIL import Image

from .models import Token, TokenStyle

Point = tuple[float, float, float]
Triangle = tuple[Point, Point, Point]


def _box_triangles(x0: float, y0: float, z0: float, x1: float, y1: float, z1: float) -> list[Triangle]:
    p000 = (x0, y0, z0)
    p100 = (x1, y0, z0)
    p110 = (x1, y1, z0)
    p010 = (x0, y1, z0)
    p001 = (x0, y0, z1)
    p101 = (x1, y0, z1)
    p111 = (x1, y1, z1)
    p011 = (x0, y1, z1)
    return [
        (p000, p110, p100), (p000, p010, p110),
        (p001, p101, p111), (p001, p111, p011),
        (p000, p100, p101), (p000, p101, p001),
        (p100, p110, p111), (p100, p111, p101),
        (p110, p010, p011), (p110, p011, p111),
        (p010, p000, p001), (p010, p001, p011),
    ]


def _icon_relief_triangles(icon_path: Path, style: TokenStyle, max_samples: int = 32) -> list[Triangle]:
    with Image.open(icon_path) as image:
        gray = image.convert("L")
        gray.thumbnail((max_samples, max_samples), Image.Resampling.NEAREST)
        width_px, height_px = gray.size
        art_w = style.width_mm * 0.58
        art_h = style.height_mm * 0.40
        x_start = (style.width_mm - art_w) / 2
        y_start = style.height_mm * 0.31
        tile_w = art_w / width_px
        tile_h = art_h / height_px
        triangles: list[Triangle] = []
        for py in range(height_px):
            for px in range(width_px):
                if gray.getpixel((px, py)) < 128:
                    x0 = x_start + px * tile_w
                    x1 = x0 + tile_w * 0.92
                    y0 = y_start + py * tile_h
                    y1 = y0 + tile_h * 0.92
                    triangles += _box_triangles(
                        x0,
                        y0,
                        style.thickness_mm,
                        x1,
                        y1,
                        style.thickness_mm + style.icon_height_mm,
                    )
        return triangles


def _ascii_stl(name: str, triangles: list[Triangle], comments: list[str] | None = None) -> str:
    lines = [f"solid {name}"]
    for comment in comments or []:
        lines.append(f"  // {comment}")
    for tri in triangles:
        lines.append("  facet normal 0 0 0")
        lines.append("    outer loop")
        for x, y, z in tri:
            lines.append(f"      vertex {x:.4f} {y:.4f} {z:.4f}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append(f"endsolid {name}")
    return "\n".join(lines) + "\n"


def render_stl(token: Token, style: TokenStyle, output_dir: Path, icon_path: Path | None = None) -> Path:
    """Render an MVP printable standard-card-size rectangular STL plaque."""

    stl_dir = output_dir / "stl"
    stl_dir.mkdir(parents=True, exist_ok=True)
    output_path = stl_dir / f"{token.slug}.stl"
    triangles = _box_triangles(0, 0, 0, style.width_mm, style.height_mm, style.thickness_mm)
    comments: list[str] = []
    if icon_path is not None and icon_path.exists():
        triangles += _icon_relief_triangles(icon_path, style)
        comments.append("relief tiles generated from processed icon")
    else:
        margin_x = style.width_mm * 0.22
        margin_y = style.height_mm * 0.33
        triangles += _box_triangles(
            margin_x,
            margin_y,
            style.thickness_mm,
            style.width_mm - margin_x,
            style.height_mm - margin_y,
            style.thickness_mm + style.icon_height_mm,
        )
    output_path.write_text(_ascii_stl(token.slug, triangles, comments=comments), encoding="utf-8")
    return output_path
