from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


Confidence = Literal["high", "medium", "low"]


@dataclass(frozen=True, slots=True)
class NormalizedLocation:
    country: str | None
    city: str | None
    is_remote: bool
    confidence: Confidence

    @property
    def is_clearly_outside_germany(self) -> bool:
        return self.country not in (None, "Germany") and self.confidence == "high"


_GERMAN_CITIES = {
    "berlin": "Berlin",
    "bremen": "Bremen",
    "hamburg": "Hamburg",
    "hannover": "Hannover",
    "hanover": "Hannover",
    "köln": "Cologne",
    "koeln": "Cologne",
    "cologne": "Cologne",
    "münchen": "Munich",
    "muenchen": "Munich",
    "munich": "Munich",
    "oldenburg": "Oldenburg",
}

_REMOTE_GERMANY = (
    "remote germany",
    "remote - germany",
    "remote (germany)",
    "remote in germany",
    "home office germany",
    "homeoffice germany",
    "deutschlandweit",
    "bundesweit",
)

_REMOTE = ("remote", "home office", "homeoffice", "hybrid", "work from home")
_AMBIGUOUS_REGIONS = ("emea", "europe", "worldwide", "global", "international")

_FOREIGN_LOCATIONS = {
    "Austria": re.compile(r"\b(?:austria|vienna|wien|österreich)\b", re.IGNORECASE),
    "Switzerland": re.compile(
        r"\b(?:switzerland|zürich|zurich|bern|schweiz)\b", re.IGNORECASE
    ),
    "United Kingdom": re.compile(
        r"\b(?:united kingdom|london|uk|u\.k\.)\b", re.IGNORECASE
    ),
    "United States": re.compile(
        r"\b(?:united states|new york|usa|u\.s\.)\b", re.IGNORECASE
    ),
}

_GERMANY_TOKEN = re.compile(r"\b(?:de|ger)\b", re.IGNORECASE)


def normalize_location(raw: str | None) -> NormalizedLocation:
    """Conservatively normalize job-board location text.

    Unknown locations remain unknown. They are not silently treated as German or
    rejected as foreign, which lets a later stage ask for stronger evidence.
    """
    text = (raw or "").strip().casefold()
    if not text:
        return NormalizedLocation(None, None, False, "low")

    if any(signal in text for signal in _REMOTE_GERMANY):
        return NormalizedLocation("Germany", None, True, "high")

    is_remote = any(signal in text for signal in _REMOTE)
    city = _find_german_city(text)
    foreign_country = _find_foreign_country(text)

    if foreign_country:
        return NormalizedLocation(foreign_country, None, is_remote, "high")

    explicit_germany = (
        "germany" in text
        or "deutschland" in text
        or bool(_GERMANY_TOKEN.search(text))
    )
    if city or explicit_germany:
        confidence: Confidence = "high" if city or "germany" in text or "deutschland" in text else "medium"
        return NormalizedLocation("Germany", city, is_remote, confidence)

    if any(region in text for region in _AMBIGUOUS_REGIONS):
        return NormalizedLocation(None, None, is_remote, "low")

    return NormalizedLocation(None, None, is_remote, "low")


def _find_german_city(text: str) -> str | None:
    for alias, canonical_name in _GERMAN_CITIES.items():
        if re.search(rf"\b{re.escape(alias)}\b", text):
            return canonical_name
    return None


def _find_foreign_country(text: str) -> str | None:
    for country, pattern in _FOREIGN_LOCATIONS.items():
        if pattern.search(text):
            return country
    return None
