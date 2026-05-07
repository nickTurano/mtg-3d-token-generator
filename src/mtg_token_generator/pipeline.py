from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from .ai_icons import write_icon_prompt
from .models import Token, TokenStyle
from .stl_generator import render_stl
from .svg_renderer import render_svg


def write_tokens_json(tokens: list[Token], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    set_code = tokens[0].set_code if tokens else None
    payload = {
        "set_code": set_code,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "scryfall/manual",
        "tokens": [token.to_dict() for token in tokens],
    }
    path = output_dir / "tokens.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def generate_from_tokens(tokens: list[Token], output_dir: Path, style: TokenStyle | None = None) -> dict[str, list[Path] | Path]:
    style = style or TokenStyle()
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = write_tokens_json(tokens, output_dir)
    prompt_paths: list[Path] = []
    svg_paths: list[Path] = []
    stl_paths: list[Path] = []
    for token in tokens:
        prompt_paths.append(write_icon_prompt(token, output_dir))
        processed_icon = output_dir / "icons" / "processed" / f"{token.slug}.png"
        icon_arg = processed_icon if processed_icon.exists() else None
        svg_paths.append(render_svg(token, style, output_dir, icon_path=icon_arg))
        stl_paths.append(render_stl(token, style, output_dir))
    return {"metadata": metadata_path, "prompts": prompt_paths, "svg": svg_paths, "stl": stl_paths}
