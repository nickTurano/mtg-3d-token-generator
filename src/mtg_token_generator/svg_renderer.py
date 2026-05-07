from __future__ import annotations

from html import escape
from pathlib import Path

from .models import Token, TokenStyle


def render_svg(token: Token, style: TokenStyle, output_dir: Path, icon_path: Path | None = None) -> Path:
    """Render a standard trading-card-size SVG layout for one token."""

    svg_dir = output_dir / "svg"
    svg_dir.mkdir(parents=True, exist_ok=True)
    output_path = svg_dir / f"{token.slug}.svg"
    width = style.width_mm
    height = style.height_mm
    icon_href = ""
    if icon_path is not None:
        try:
            icon_href = icon_path.relative_to(svg_dir).as_posix()
        except ValueError:
            icon_href = icon_path.name
    pt_text = f"{token.power}/{token.toughness}" if token.power and token.toughness else ""
    icon_markup = (
        f'<image href="{escape(icon_href)}" x="13.5" y="27" width="36.5" height="36.5" preserveAspectRatio="xMidYMid meet" />'
        if icon_href
        else '<path d="M31.75 29 L40 45 L31.75 61 L23.5 45 Z" fill="#111" />'
    )
    pt_markup = (
        f'<rect x="45" y="73" width="13" height="8" rx="2" fill="#fff" stroke="#111" stroke-width="0.7" />'
        f'<text x="51.5" y="78.7" text-anchor="middle" font-size="4.2" font-weight="700">{escape(pt_text)}</text>'
        if pt_text
        else ""
    )
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(token.name)} token">
  <rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="{style.corner_radius_mm}" fill="#f7f3e8" stroke="#111" stroke-width="1.5" />
  <rect x="4" y="4" width="{width - 8}" height="{height - 8}" rx="{max(style.corner_radius_mm - 0.75, 0)}" fill="none" stroke="#111" stroke-width="0.6" />
  <text x="31.75" y="12" text-anchor="middle" font-family="serif" font-size="6" font-weight="700">{escape(token.name)}</text>
  <line x1="7" y1="16" x2="56.5" y2="16" stroke="#111" stroke-width="0.5" />
  <text x="31.75" y="21.5" text-anchor="middle" font-family="sans-serif" font-size="3.2">{escape(token.type_line)}</text>
  {icon_markup}
  {pt_markup}
</svg>
'''
    output_path.write_text(svg, encoding="utf-8")
    return output_path
