from __future__ import annotations

import requests

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search"


def fetch_tokens_for_set(set_code: str) -> list[dict]:
    """Fetch token records for a set from Scryfall, following pagination."""

    cards: list[dict] = []
    params = {"q": f"e:{set_code.lower()} t:token", "unique": "cards"}
    url: str | None = SCRYFALL_SEARCH_URL
    while url:
        response = requests.get(url, params=params if url == SCRYFALL_SEARCH_URL else None, timeout=30)
        if response.status_code == 404:
            return []
        response.raise_for_status()
        payload = response.json()
        cards.extend(payload.get("data", []))
        url = payload.get("next_page") if payload.get("has_more") else None
        params = None
    return cards
