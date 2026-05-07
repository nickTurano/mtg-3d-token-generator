from __future__ import annotations

from dataclasses import dataclass, field
import re


_CARD_WIDTH_MM = 63.5
_CARD_HEIGHT_MM = 88.9


@dataclass(frozen=True)
class TokenStyle:
    """Physical and visual settings for generated standard-card-size tokens."""

    name: str = "minimal-card"
    width_mm: float = _CARD_WIDTH_MM
    height_mm: float = _CARD_HEIGHT_MM
    thickness_mm: float = 2.4
    corner_radius_mm: float = 3.0
    border_width_mm: float = 2.0
    border_height_mm: float = 0.4
    icon_height_mm: float = 0.6


@dataclass(frozen=True)
class Token:
    """Normalized token metadata used by every generation stage."""

    scryfall_id: str
    set_code: str
    name: str
    type_line: str
    oracle_text: str | None = None
    power: str | None = None
    toughness: str | None = None
    colors: list[str] = field(default_factory=list)
    color_identity: list[str] = field(default_factory=list)
    layout: str | None = None

    @property
    def is_creature(self) -> bool:
        return "creature" in self.type_line.lower()

    @property
    def is_artifact(self) -> bool:
        return "artifact" in self.type_line.lower()

    @property
    def is_emblem(self) -> bool:
        return "emblem" in self.type_line.lower() or "emblem" in self.name.lower()

    @property
    def slug(self) -> str:
        parts = [self.set_code.lower(), self.name]
        if self.power and self.toughness:
            parts.append(f"{self.power}-{self.toughness}")
        raw = "-".join(parts).lower()
        raw = raw.replace("/", "-")
        raw = re.sub(r"[^a-z0-9]+", "-", raw)
        return re.sub(r"-+", "-", raw).strip("-")

    def to_dict(self) -> dict:
        return {
            "scryfall_id": self.scryfall_id,
            "set_code": self.set_code,
            "name": self.name,
            "type_line": self.type_line,
            "oracle_text": self.oracle_text,
            "power": self.power,
            "toughness": self.toughness,
            "colors": list(self.colors),
            "color_identity": list(self.color_identity),
            "layout": self.layout,
            "is_creature": self.is_creature,
            "is_artifact": self.is_artifact,
            "is_emblem": self.is_emblem,
            "slug": self.slug,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Token":
        return cls(
            scryfall_id=data["scryfall_id"],
            set_code=data["set_code"],
            name=data["name"],
            type_line=data["type_line"],
            oracle_text=data.get("oracle_text"),
            power=data.get("power"),
            toughness=data.get("toughness"),
            colors=list(data.get("colors", [])),
            color_identity=list(data.get("color_identity", [])),
            layout=data.get("layout"),
        )
