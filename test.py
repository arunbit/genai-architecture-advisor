"""Run the offline walking skeleton: profile JSON in, JSON and Markdown reports out."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from genai_architecture_advisor.contracts import ContractValidator  # noqa: E402
from genai_architecture_advisor.pipeline import AdvisorPipeline  # noqa: E402
from genai_architecture_advisor.render import render_markdown  # noqa: E402
from genai_architecture_advisor.retriever import (  # noqa: E402
    StuffEverythingRetriever,
)
from genai_architecture_advisor.synthesizer import FakeSynthesizer  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path, help="Input profile JSON path")
    parser.add_argument("--cards-dir", type=Path, default=PROJECT_ROOT / "cards")
    parser.add_argument(
        "--prompt", type=Path, default=PROJECT_ROOT / "prompts" / "synthesis.md"
    )
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "reports")
    args = parser.parse_args()

    if not args.prompt.is_file():
        parser.error(
            "The Arun-authored prompt is missing. Create prompts/synthesis.md first."
        )

    with args.profile.open(encoding="utf-8") as file:
        profile = json.load(file)
    if not isinstance(profile, dict):
        parser.error("The profile root must be a JSON object.")

    pipeline = AdvisorPipeline(
        contracts=ContractValidator.from_project_root(PROJECT_ROOT),
        retriever=StuffEverythingRetriever(args.cards_dir),
        synthesizer=FakeSynthesizer(),
    )
    result = pipeline.run(profile, args.prompt.read_text(encoding="utf-8"))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_stem = args.profile.stem
    json_path = args.output_dir / f"{output_stem}.json"
    markdown_path = args.output_dir / f"{output_stem}.md"
    json_path.write_text(
        json.dumps(result.report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    markdown_path.write_text(render_markdown(result.report), encoding="utf-8")

    print(f"JSON report: {json_path}")
    print(f"Markdown report: {markdown_path}")
    print("Synthesizer: fake (offline; no live LLM call)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
