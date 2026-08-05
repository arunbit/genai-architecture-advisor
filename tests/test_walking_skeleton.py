from __future__ import annotations

import copy
import json
from pathlib import Path

from genai_architecture_advisor.contracts import ContractValidator
from genai_architecture_advisor.pipeline import AdvisorPipeline
from genai_architecture_advisor.render import render_markdown
from genai_architecture_advisor.retriever import StuffEverythingRetriever
from genai_architecture_advisor.synthesizer import FakeSynthesizer

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_walking_skeleton_produces_valid_cited_report(tmp_path: Path) -> None:
    profile = _example_profile()
    pipeline = _pipeline(tmp_path)

    result = pipeline.run(profile, "Arun-authored test prompt.")

    assert result.report["status"] == "recommendation"
    assert result.report["recommendations"][0]["card_citations"] == ["CARD-001"]
    assert result.report["recommendations"][0]["constraint_citations"] == ["C-001"]
    assert result.report["rejected_alternatives"]
    assert "CARD-001 CONTENT" in result.synthesis_input
    assert "CARD-002 CONTENT" in result.synthesis_input
    assert "Synthesizer: `fake`" in render_markdown(result.report)


def test_empty_constraints_request_clarification(tmp_path: Path) -> None:
    profile = _example_profile()
    profile["constraints"] = []

    result = _pipeline(tmp_path).run(profile, "Arun-authored test prompt.")

    assert result.report["status"] == "needs_clarification"
    assert result.report["recommendations"] == []
    assert result.report["processing_feedback"]["clarifying_questions"]


def test_invalid_input_returns_contract_shaped_feedback(tmp_path: Path) -> None:
    profile = _example_profile()
    profile["context"]["team_size"] = -1

    result = _pipeline(tmp_path).run(profile, "Arun-authored test prompt.")

    assert result.report["status"] == "invalid_input"
    assert result.report["processing_feedback"]["invalid_information"]
    assert result.synthesis_input == ""


def test_nested_unknown_field_is_reported_without_echoing_value(
    tmp_path: Path,
) -> None:
    profile = _example_profile()
    profile["context"]["budget"]["private_note"] = "do not echo this value"

    result = _pipeline(tmp_path).run(profile, "Arun-authored test prompt.")

    unprocessed = result.report["processing_feedback"]["unprocessed_input"]
    assert unprocessed == [
        {
            "input_path": "/context/budget/private_note",
            "reason": (
                "The field is allowed for forward compatibility but unused in v1."
            ),
        }
    ]
    assert "do not echo this value" not in json.dumps(result.report)


def _pipeline(tmp_path: Path) -> AdvisorPipeline:
    cards_dir = tmp_path / "cards"
    cards_dir.mkdir()
    (cards_dir / "one.md").write_text(
        "# First test pattern\n\n**Card ID:** CARD-001\n\nCARD-001 CONTENT\n",
        encoding="utf-8",
    )
    (cards_dir / "two.md").write_text(
        "# Second test pattern\n\n**Card ID:** CARD-002\n\nCARD-002 CONTENT\n",
        encoding="utf-8",
    )
    return AdvisorPipeline(
        contracts=ContractValidator.from_project_root(PROJECT_ROOT),
        retriever=StuffEverythingRetriever(cards_dir),
        synthesizer=FakeSynthesizer(),
    )


def _example_profile() -> dict:
    with (PROJECT_ROOT / "profiles" / "example1.json").open(encoding="utf-8") as file:
        return copy.deepcopy(json.load(file))
