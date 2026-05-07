from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from .models import TokenStyle
from .normalize import normalize_cards
from .pipeline import generate_from_tokens
from .scryfall import fetch_tokens_for_set

app = typer.Typer(help="Generate standard-card-size 3D printable tabletop token assets.")


@app.command()
def generate_all(
    set_code: str = typer.Option(..., "--set-code", help="Magic set code, e.g. tdm."),
    output: Path | None = typer.Option(None, "--output", help="Output directory."),
    limit: int | None = typer.Option(None, "--limit", help="Limit number of tokens for test runs."),
    width_mm: float = typer.Option(63.5, help="Card/token width in millimeters."),
    height_mm: float = typer.Option(88.9, help="Card/token height in millimeters."),
    thickness_mm: float = typer.Option(2.4, help="Base thickness in millimeters."),
    generate_icons: bool = typer.Option(True, "--generate-icons/--no-generate-icons", help="Generate placeholder/raw icons and processed printable silhouettes."),
    regen_icons: bool = typer.Option(False, "--regen-icons", help="Regenerate raw icon files even when cached files already exist."),
):
    """Fetch token metadata and generate prompts, SVGs, and MVP STLs."""

    out = output or Path("output") / set_code.lower()
    raw_cards = fetch_tokens_for_set(set_code)
    tokens = normalize_cards(raw_cards)
    if limit is not None:
        tokens = tokens[:limit]
    style = TokenStyle(width_mm=width_mm, height_mm=height_mm, thickness_mm=thickness_mm)
    outputs = generate_from_tokens(tokens, out, style, generate_icons=generate_icons, regen_icons=regen_icons)
    print(f"[green]Generated {len(tokens)} tokens in {out}[/green]")
    for key, value in outputs.items():
        count = len(value) if isinstance(value, list) else 1
        print(f"  {key}: {count}")


if __name__ == "__main__":
    app()
