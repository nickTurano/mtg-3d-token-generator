from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from .ai_icons import generate_placeholder_icon, icon_paths, write_icon_prompt
from .icon_processing import process_icon
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


def generate_from_tokens(
    tokens: list[Token],
    output_dir: Path,
    style: TokenStyle | None = None,
    generate_icons: bool = False,
    regen_icons: bool = False,
) -> dict[str, list[Path] | Path]:
    style = style or TokenStyle()
    output_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = write_tokens_json(tokens, output_dir)
    prompt_paths: list[Path] = []
    raw_icon_paths: list[Path] = []
    processed_icon_paths: list[Path] = []
    svg_paths: list[Path] = []
    stl_paths: list[Path] = []
    for token in tokens:
        paths = icon_paths(token, output_dir)
        prompt_paths.append(write_icon_prompt(token, output_dir))
        icon_arg = paths.processed if paths.processed.exists() else None
        if generate_icons:
            raw_icon_paths.append(generate_placeholder_icon(token, paths.raw, force=regen_icons))
            processed_icon_paths.append(process_icon(paths.raw, paths.processed))
            icon_arg = paths.processed
        svg_paths.append(render_svg(token, style, output_dir, icon_path=icon_arg))
        stl_paths.append(render_stl(token, style, output_dir, icon_path=icon_arg))
    return {
        "metadata": metadata_path,
        "prompts": prompt_paths,
        "raw_icons": raw_icon_paths,
        "processed_icons": processed_icon_paths,
        "svg": svg_paths,
        "stl": stl_paths,
    }
