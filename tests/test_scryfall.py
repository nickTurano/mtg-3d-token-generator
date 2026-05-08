from mtg_token_generator import scryfall


class FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise AssertionError(f"unexpected HTTP error {self.status_code}")

    def json(self):
        return self._payload


def test_fetch_tokens_for_set_uses_token_set_when_main_set_has_no_token_results(monkeypatch):
    calls = []

    def fake_get(url, params=None, timeout=30):
        calls.append((url, params))
        if url == scryfall.SCRYFALL_SEARCH_URL:
            query = params["q"]
            if query == "e:tdm t:token":
                return FakeResponse(status_code=404)
            if query == "e:ttdm t:token":
                return FakeResponse(payload={"data": [{"id": "token-id", "name": "Goblin"}], "has_more": False})
        raise AssertionError(f"unexpected request: {url=} {params=}")

    monkeypatch.setattr(scryfall.requests, "get", fake_get)

    cards = scryfall.fetch_tokens_for_set("tdm")

    assert cards == [{"id": "token-id", "name": "Goblin"}]
    assert calls[0][1]["q"] == "e:tdm t:token"
    assert calls[1][1]["q"] == "e:ttdm t:token"
