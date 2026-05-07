# Standard-card-size MTG token generator plan

Approved MVP v0.1:

- Python CLI project in `src/mtg_token_generator`.
- GitHub repo: `nickTurano/mtg-3d-token-generator`.
- Standard trading-card physical dimensions by default: 63.5mm × 88.9mm.
- Fetch token metadata from Scryfall by set code.
- Normalize metadata into reusable `Token` objects and `tokens.json`.
- Generate original AI icon prompts with strict guardrails:
  - no official Magic artwork,
  - no mana symbols,
  - no card frames,
  - no set symbols,
  - no logos,
  - no copyrighted characters.
- Cache AI icon prompt files under `icons/prompts/`.
- Render SVG layouts at standard card size.
- Render MVP STL card/plaque geometry with a raised relief placeholder.

Future phases:

- Actual image generation integration.
- Icon threshold/cleanup.
- AI icon to STL relief/vector conversion.
- Better card-front aesthetics.
- Shopify CSV/API export.
- HueForge/heightmap companion mode.
