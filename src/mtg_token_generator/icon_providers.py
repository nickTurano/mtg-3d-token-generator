from __future__ import annotations

import base64
import os
from pathlib import Path
from typing import Protocol
from urllib.request import urlopen

from .ai_icons import generate_placeholder_icon
from .models import Token


class IconProvider(Protocol):
    def generate(self, token: Token, prompt: str, output_path: Path, force: bool = False) -> Path: ...


class PlaceholderIconProvider:
    def generate(self, token: Token, prompt: str, output_path: Path, force: bool = False) -> Path:
        return generate_placeholder_icon(token, output_path, force=force)


class OpenAIIconProvider:
    def __init__(
        self,
        client=None,
        model: str = "gpt-image-2",
        quality: str = "low",
        size: str = "1024x1024",
    ):
        self.client = client or self._default_client()
        self.model = model
        self.quality = quality
        self.size = size

    @staticmethod
    def _default_client():
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("OpenAI icon provider requires the 'openai' package to be installed.") from exc
        return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def generate(self, token: Token, prompt: str, output_path: Path, force: bool = False) -> Path:
        if output_path.exists() and not force:
            return output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result = self.client.images.generate(
            model=self.model,
            prompt=prompt,
            size=self.size,
            quality=self.quality,
            n=1,
        )
        image = result.data[0]
        if getattr(image, "b64_json", None):
            output_path.write_bytes(base64.b64decode(image.b64_json))
        elif getattr(image, "url", None):
            with urlopen(image.url, timeout=60) as response:
                output_path.write_bytes(response.read())
        else:
            raise RuntimeError("OpenAI image response did not include b64_json or url data.")
        return output_path


def create_icon_provider(name: str | IconProvider = "placeholder") -> IconProvider:
    if not isinstance(name, str):
        return name
    normalized = name.lower().strip()
    if normalized == "placeholder":
        return PlaceholderIconProvider()
    if normalized == "openai":
        return OpenAIIconProvider()
    raise ValueError(f"Unknown icon provider: {name}")
