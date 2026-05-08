from __future__ import annotations

import requests

SCRYFALL_SEARCH_URL = "https://api.scryfall.com/cards/search"


def _fetch_search(query: str) -> list[dict] | None:
    """Fetch one Scryfall search query, returning None for no matches."""

    cards: list[dict] = []
    params = {"q": query, "unique": "cards"}
    url: str | None = SCRYFALL_SEARCH_URL
    while url:
        response = requests.get(url, params=params if url == SCRYFALL_SEARCH_URL else None, timeout=30)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        payload = response.json()
        cards.extend(payload.get("data", []))
        url = payload.get("next_page") if payload.get("has_more") else None
        params = None
    return cards


def fetch_tokens_for_set(set_code: str) -> list[dict]:
    """Fetch token records for a set from Scryfall, following pagination.

    Scryfall stores many set token printings in a sibling token set whose code is
    the main set code prefixed with ``t`` (for example, ``tdm`` -> ``ttdm``).
    Try the user-provided code first so direct token-set codes still work, then
    fall back to the sibling token set when the main set has no token results.
    """

    normalized_code = set_code.lower()
    queries = [f"e:{normalized_code} t:token", f"e:t{normalized_code} t:token"]

    for query in queries:
        cards = _fetch_search(query)
        if cards is not None:
            return cards
    return []
