"""Provider-neutral synthesis boundary and deterministic offline fake."""

from __future__ import annotations

from typing import Any, Protocol

from . import __version__
from .retriever import RetrievedContext


class Synthesizer(Protocol):
    """Turn a profile plus retrieved knowledge into a contract-shaped report."""

    def synthesize(
        self,
        *,
        profile: dict[str, Any],
        synthesis_prompt: str,
        retrieved: RetrievedContext,
    ) -> dict[str, Any]:
        """Produce a report candidate; the pipeline validates it afterward."""


class FakeSynthesizer:
    """Return deterministic output for offline execution and automated tests."""

    def synthesize(
        self,
        *,
        profile: dict[str, Any],
        synthesis_prompt: str,
        retrieved: RetrievedContext,
    ) -> dict[str, Any]:
        if not synthesis_prompt.strip():
            raise ValueError("The synthesis prompt is empty.")

        constraints = profile.get("constraints", [])
        if not constraints:
            return _needs_constraints_report(profile)

        first_card = retrieved.cards[0]
        alternative_card = (
            retrieved.cards[1] if len(retrieved.cards) > 1 else first_card
        )
        first_constraint = constraints[0]
        constraint_id = first_constraint["id"]

        used = [
            {
                "constraint_id": constraint_id,
                "influence": (
                    "The deterministic fake cites the first supplied constraint."
                ),
            }
        ]
        unused = [
            {
                "constraint_id": constraint["id"],
                "reason": "The deterministic fake uses one constraint to prove wiring.",
            }
            for constraint in constraints[1:]
        ]

        return {
            "contract_version": "1.0",
            "status": "recommendation",
            "request_summary": profile["request"],
            "recommendations": [
                {
                    "id": "R-001",
                    "title": f"Apply {first_card.title}",
                    "description": (
                        "Deterministic offline output proving that a retrieved card "
                        "reaches the recommendation report."
                    ),
                    "rationale": (
                        "This is test-synthesized text, not a live model judgment."
                    ),
                    "card_citations": [first_card.card_id],
                    "constraint_citations": [constraint_id],
                }
            ],
            "rejected_alternatives": [
                {
                    "name": f"Apply {alternative_card.title} instead",
                    "reason": (
                        "Rejected by the deterministic fake to prove that an "
                        "alternative and its citations survive the pipeline."
                    ),
                    "card_citations": [alternative_card.card_id],
                    "constraint_citations": [constraint_id],
                }
            ],
            "constraint_analysis": {
                "used": used,
                "unused": unused,
                "unavailable": [],
            },
            "cost_estimate": {"status": "not_calculated", "estimate": None},
            "processing_feedback": _base_feedback(),
        }


def build_invalid_input_report(
    profile: dict[str, Any], invalid_information: list[dict[str, str]]
) -> dict[str, Any]:
    """Create a valid output report when the input contract is violated."""

    feedback = _base_feedback()
    feedback["invalid_information"] = invalid_information
    request = profile.get("request", "")
    return {
        "contract_version": "1.0",
        "status": "invalid_input",
        "request_summary": request if isinstance(request, str) else "",
        "recommendations": [],
        "rejected_alternatives": [],
        "constraint_analysis": {"used": [], "unused": [], "unavailable": []},
        "cost_estimate": {"status": "not_calculated", "estimate": None},
        "processing_feedback": feedback,
    }


def _needs_constraints_report(profile: dict[str, Any]) -> dict[str, Any]:
    feedback = _base_feedback()
    feedback["missing_information"] = [
        {
            "input_path": "/constraints",
            "description": "No decision-driving constraint was supplied.",
            "blocking": True,
            "impact": (
                "A recommendation cannot satisfy the required constraint citation."
            ),
        }
    ]
    feedback["clarifying_questions"] = [
        {
            "id": "Q-001",
            "question": (
                "Which consideration should drive the recommendation: delivery "
                "speed, cost, operational simplicity, latency, or something else?"
            ),
            "input_path": "/constraints",
            "blocking": True,
        }
    ]
    return {
        "contract_version": "1.0",
        "status": "needs_clarification",
        "request_summary": profile["request"],
        "recommendations": [],
        "rejected_alternatives": [],
        "constraint_analysis": {
            "used": [],
            "unused": [],
            "unavailable": [
                {
                    "input_path": "/constraints",
                    "impact": "No recommendation can cite a supplied constraint.",
                }
            ],
        },
        "cost_estimate": {"status": "not_calculated", "estimate": None},
        "processing_feedback": feedback,
    }


def _base_feedback() -> dict[str, Any]:
    return {
        "advisor_version": __version__,
        "synthesizer": {"kind": "fake", "provider": None, "model": None},
        "missing_information": [],
        "invalid_information": [],
        "unprocessed_input": [],
        "assumptions": [],
        "ambiguities": [],
        "clarifying_questions": [],
        "warnings": [],
        "quality_assessment": {
            "status": "not_measured",
            "recommendation_confidence": "not_assessed",
            "confidence_basis": [],
            "hallucination_risk": "not_assessed",
        },
    }
