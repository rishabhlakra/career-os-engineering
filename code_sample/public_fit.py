from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


PresentationTier = Literal["match", "reachable_reach", "aspirational"]


@dataclass(frozen=True, slots=True)
class InternalFitAssessment:
    """Small stand-in for the private ranker's output.

    The numeric fields are useful inside the service, but should never cross the
    API boundary.
    """

    tier: PresentationTier
    explanation: str
    matched: tuple[str, ...]
    gaps: tuple[str, ...]
    language: str | None
    similarity: float
    ranking_weight: float
    seniority_label: str


@dataclass(frozen=True, slots=True)
class PublicFitPayload:
    tier: PresentationTier
    explanation: str
    matched: tuple[str, ...]
    gap: str | None
    gaps: tuple[str, ...]
    language: str | None

    def as_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["matched"] = list(self.matched)
        payload["gaps"] = list(self.gaps)
        return payload


def to_public_payload(assessment: InternalFitAssessment) -> PublicFitPayload:
    """Return the allow-listed fit fields used by the product interface."""
    explanation = assessment.explanation.strip()
    if not explanation:
        raise ValueError("A public fit payload needs an explanation")

    matched = _unique_non_empty(assessment.matched)
    gaps = _unique_non_empty(assessment.gaps)

    return PublicFitPayload(
        tier=assessment.tier,
        explanation=explanation,
        matched=matched,
        gap=gaps[0] if gaps else None,
        gaps=gaps,
        language=assessment.language,
    )


def _unique_non_empty(values: tuple[str, ...]) -> tuple[str, ...]:
    cleaned = (value.strip() for value in values)
    return tuple(dict.fromkeys(value for value in cleaned if value))
