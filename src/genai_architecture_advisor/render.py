"""Render a validated JSON report as human-readable Markdown."""

from __future__ import annotations

from typing import Any


def render_markdown(report: dict[str, Any]) -> str:
    """Render the contract's important fields without introducing new facts."""

    lines = [
        "# Architecture Recommendation Report",
        "",
        f"**Status:** `{report['status']}`",
        "",
        "## Request",
        "",
        report["request_summary"] or "No valid request summary was available.",
        "",
        "## Recommendations",
        "",
    ]

    if report["recommendations"]:
        for recommendation in report["recommendations"]:
            lines.extend(
                [
                    f"### {recommendation['title']}",
                    "",
                    recommendation["description"],
                    "",
                    f"**Rationale:** {recommendation['rationale']}",
                    "",
                    "**Card citations:** "
                    + ", ".join(recommendation["card_citations"]),
                    "",
                    "**Constraint citations:** "
                    + ", ".join(recommendation["constraint_citations"]),
                    "",
                ]
            )
    else:
        lines.extend(["No recommendation was produced.", ""])

    lines.extend(["## Rejected alternatives", ""])
    if report["rejected_alternatives"]:
        for alternative in report["rejected_alternatives"]:
            lines.extend(
                [
                    f"### {alternative['name']}",
                    "",
                    alternative["reason"],
                    "",
                    "**Card citations:** " + ", ".join(alternative["card_citations"]),
                    "",
                    "**Constraint citations:** "
                    + ", ".join(alternative["constraint_citations"]),
                    "",
                ]
            )
    else:
        lines.extend(["No rejected alternative was produced.", ""])

    lines.extend(_render_constraint_analysis(report["constraint_analysis"]))
    lines.extend(_render_processing_feedback(report["processing_feedback"]))
    lines.extend(
        [
            "## Cost estimate",
            "",
            (
                f"Status: `{report['cost_estimate']['status']}`. "
                "No numeric cost was generated."
            ),
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _render_constraint_analysis(analysis: dict[str, Any]) -> list[str]:
    lines = ["## Constraint analysis", ""]
    if analysis["used"]:
        lines.extend(["### Used", ""])
        for item in analysis["used"]:
            lines.append(f"- `{item['constraint_id']}` — {item['influence']}")
        lines.append("")
    if analysis["unused"]:
        lines.extend(["### Unused", ""])
        for item in analysis["unused"]:
            lines.append(f"- `{item['constraint_id']}` — {item['reason']}")
        lines.append("")
    if analysis["unavailable"]:
        lines.extend(["### Unavailable", ""])
        for item in analysis["unavailable"]:
            lines.append(f"- `{item['input_path']}` — {item['impact']}")
        lines.append("")
    if not any(analysis.values()):
        lines.extend(["No constraint analysis was available.", ""])
    return lines


def _render_processing_feedback(feedback: dict[str, Any]) -> list[str]:
    lines = [
        "## Processing feedback",
        "",
        f"Advisor version: `{feedback['advisor_version']}`",
        "",
        f"Synthesizer: `{feedback['synthesizer']['kind']}`",
        "",
        "Quality measurement: "
        f"`{feedback['quality_assessment']['status']}`; hallucination risk: "
        f"`{feedback['quality_assessment']['hallucination_risk']}`.",
        "",
    ]
    sections = (
        ("Missing information", "missing_information", "description"),
        ("Invalid information", "invalid_information", "issue"),
        ("Unprocessed input", "unprocessed_input", "reason"),
        ("Assumptions", "assumptions", "reason"),
        ("Ambiguities", "ambiguities", "description"),
        ("Clarifying questions", "clarifying_questions", "question"),
    )
    for title, key, text_key in sections:
        if not feedback[key]:
            continue
        lines.extend([f"### {title}", ""])
        for item in feedback[key]:
            lines.append(f"- `{item['input_path']}` — {item[text_key]}")
        lines.append("")
    if feedback["warnings"]:
        lines.extend(["### Warnings", ""])
        lines.extend(f"- {warning}" for warning in feedback["warnings"])
        lines.append("")
    return lines
