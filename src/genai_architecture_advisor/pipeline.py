"""End-to-end orchestration for the walking skeleton."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .contracts import ContractValidator
from .retriever import Retriever
from .synthesizer import Synthesizer, build_invalid_input_report


@dataclass(frozen=True)
class PipelineResult:
    """Validated machine report plus the exact stuffed synthesis input."""

    report: dict[str, Any]
    synthesis_input: str


class AdvisorPipeline:
    """Validate, retrieve, synthesize, enrich feedback, and validate again."""

    def __init__(
        self,
        *,
        contracts: ContractValidator,
        retriever: Retriever,
        synthesizer: Synthesizer,
    ):
        self._contracts = contracts
        self._retriever = retriever
        self._synthesizer = synthesizer

    def run(self, profile: dict[str, Any], base_prompt: str) -> PipelineResult:
        inspection = self._contracts.inspect_profile(profile)
        if inspection.invalid:
            invalid_information = [
                {
                    "input_path": issue.input_path,
                    "issue": issue.message,
                    "expected": "A value accepted by profile contract version 1.0.",
                }
                for issue in inspection.invalid
            ]
            report = build_invalid_input_report(profile, invalid_information)
            _add_unprocessed_feedback(report, inspection.unprocessed_paths)
            self._contracts.validate_report(report)
            return PipelineResult(report=report, synthesis_input="")

        retrieved = self._retriever.retrieve(profile)
        synthesis_input = _compose_synthesis_input(
            base_prompt, profile, retrieved.stuffed_text
        )
        report = self._synthesizer.synthesize(
            profile=profile,
            synthesis_prompt=synthesis_input,
            retrieved=retrieved,
        )
        _add_unprocessed_feedback(report, inspection.unprocessed_paths)
        self._contracts.validate_report(report)
        return PipelineResult(report=report, synthesis_input=synthesis_input)


def _compose_synthesis_input(
    base_prompt: str, profile: dict[str, Any], stuffed_cards: str
) -> str:
    """Mechanical framing around Arun's synthesis instructions."""

    return (
        f"{base_prompt.strip()}\n\n"
        "## Input profile\n\n"
        f"```json\n{json.dumps(profile, indent=2, sort_keys=True)}\n```\n\n"
        "## Pattern cards\n\n"
        f"{stuffed_cards}\n"
    )


def _add_unprocessed_feedback(
    report: dict[str, Any], unprocessed_paths: tuple[str, ...]
) -> None:
    report["processing_feedback"]["unprocessed_input"] = [
        {
            "input_path": path,
            "reason": (
                "The field is allowed for forward compatibility but unused in v1."
            ),
        }
        for path in unprocessed_paths
    ]
