# MTG 3D Token Generator

Generate standard trading-card-size, 3D-printable tabletop token assets from Magic token metadata.

This project is intended to create original tabletop accessory designs. It does not use official Magic artwork, mana symbols, card frames, set symbols, logos, or other Wizards of the Coast-owned visual identity.

## MVP goals

- Fetch token metadata from Scryfall by set code.
- Normalize token records into reusable JSON.
- Generate AI icon prompts and cache generated icons.
- Produce standard-card-size SVG layouts: 63.5mm × 88.9mm.
- Produce standard-card-size STL relief plaques/tokens.

## Development

```bash
uv venv ~/venvs/mtg-token-generator --python python3
uv pip install --python ~/venvs/mtg-token-generator/bin/python -e '.[dev]'
~/venvs/mtg-token-generator/bin/pytest
```
