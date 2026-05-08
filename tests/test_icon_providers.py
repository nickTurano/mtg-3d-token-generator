from pathlib import Path

import pytest
from PIL import Image

from mtg_token_generator.icon_providers import PlaceholderIconProvider, create_icon_provider
from mtg_token_generator.models import Token


class RecordingProvider:
    def __init__(self):
        self.calls = []

    def generate(self, token: Token, prompt: str, output_path: Path, force: bool = False) -> Path:
        self.calls.append((token, prompt, output_path, force))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (32, 32), "white").save(output_path)
        return output_path


def test_create_icon_provider_returns_placeholder_provider_by_default():
    provider = create_icon_provider("placeholder")

    assert isinstance(provider, PlaceholderIconProvider)


def test_create_icon_provider_rejects_unknown_provider_name():
    with pytest.raises(ValueError, match="Unknown icon provider"):
        create_icon_provider("bogus")


def test_pipeline_uses_supplied_icon_provider(tmp_path: Path):
    from mtg_token_generator.pipeline import generate_from_tokens

    token = Token(scryfall_id="1", set_code="tdm", name="Goblin", type_line="Token Creature — Goblin")
    provider = RecordingProvider()

    outputs = generate_from_tokens([token], tmp_path, generate_icons=True, icon_provider=provider)

    raw_path = tmp_path / "icons" / "raw" / "tdm-goblin.png"
    assert outputs["raw_icons"] == [raw_path]
    assert provider.calls[0][0] == token
    assert "Subject: Goblin" in provider.calls[0][1]
    assert provider.calls[0][2] == raw_path
    assert provider.calls[0][3] is False


def test_openai_provider_writes_base64_png_from_client(tmp_path: Path):
    from mtg_token_generator.icon_providers import OpenAIIconProvider

    class FakeImage:
        b64_json = "iVBORw0KGgo="
        url = None

    class FakeImages:
        def __init__(self):
            self.kwargs = None

        def generate(self, **kwargs):
            self.kwargs = kwargs
            return type("Result", (), {"data": [FakeImage()]})()

    class FakeClient:
        def __init__(self):
            self.images = FakeImages()

    client = FakeClient()
    provider = OpenAIIconProvider(client=client, model="gpt-image-2", quality="low", size="1024x1024")
    out = tmp_path / "raw.png"

    result = provider.generate(
        Token(scryfall_id="1", set_code="tdm", name="Goblin", type_line="Token Creature — Goblin"),
        "prompt text",
        out,
    )

    assert result == out
    assert out.read_bytes() == b"\x89PNG\r\n\x1a\n"
    assert client.images.kwargs == {
        "model": "gpt-image-2",
        "prompt": "prompt text",
        "size": "1024x1024",
        "quality": "low",
        "n": 1,
    }
