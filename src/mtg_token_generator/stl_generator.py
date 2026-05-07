from __future__ import annotations

from pathlib import Path

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
        (p000, p110, p100), (p000, p010, p110),  # bottom
        (p001, p101, p111), (p001, p111, p011),  # top
        (p000, p100, p101), (p000, p101, p001),  # front
        (p100, p110, p111), (p100, p111, p101),  # right
        (p110, p010, p011), (p110, p011, p111),  # back
        (p010, p000, p001), (p010, p001, p011),  # left
    ]


def _ascii_stl(name: str, triangles: list[Triangle]) -> str:
    lines = [f"solid {name}"]
    for tri in triangles:
        lines.append("  facet normal 0 0 0")
        lines.append("    outer loop")
        for x, y, z in tri:
            lines.append(f"      vertex {x:.4f} {y:.4f} {z:.4f}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append(f"endsolid {name}")
    return "\n".join(lines) + "\n"


def render_stl(token: Token, style: TokenStyle, output_dir: Path) -> Path:
    """Render an MVP printable standard-card-size rectangular STL plaque.

    This intentionally starts as simple ASCII STL geometry. Later versions can
    replace this with CadQuery/contour relief while keeping the public interface.
    """

    stl_dir = output_dir / "stl"
    stl_dir.mkdir(parents=True, exist_ok=True)
    output_path = stl_dir / f"{token.slug}.stl"
    triangles = _box_triangles(0, 0, 0, style.width_mm, style.height_mm, style.thickness_mm)
    # Raised inner artwork plate placeholder: proves relief layers in MVP.
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
    output_path.write_text(_ascii_stl(token.slug, triangles), encoding="utf-8")
    return output_path
