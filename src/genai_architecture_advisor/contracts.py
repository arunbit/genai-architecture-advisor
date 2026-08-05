"""Load and enforce the frozen JSON contracts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


@dataclass(frozen=True)
class InputIssue:
    """One input-validation problem at a precise JSON Pointer path."""

    input_path: str
    message: str


@dataclass(frozen=True)
class ProfileInspection:
    """Validation errors and tolerated fields that the MVP does not process."""

    invalid: tuple[InputIssue, ...]
    unprocessed_paths: tuple[str, ...]


class ReportContractError(ValueError):
    """Raised when pipeline output violates the frozen report contract."""


class ContractValidator:
    """Validate profiles and reports against the version-1 JSON Schemas."""

    def __init__(self, profile_schema: dict[str, Any], report_schema: dict[str, Any]):
        Draft202012Validator.check_schema(profile_schema)
        Draft202012Validator.check_schema(report_schema)
        self._profile_schema = profile_schema
        self._profile_validator = Draft202012Validator(profile_schema)
        self._report_validator = Draft202012Validator(report_schema)

    @classmethod
    def from_project_root(cls, project_root: Path) -> ContractValidator:
        """Load both frozen schemas from the public project tree."""

        schema_dir = project_root / "schemas"
        profile_schema = _load_json(schema_dir / "profile.schema.json")
        report_schema = _load_json(schema_dir / "report.schema.json")
        return cls(profile_schema, report_schema)

    def inspect_profile(self, profile: dict[str, Any]) -> ProfileInspection:
        """Return all invalid and tolerated-but-unprocessed input paths."""

        errors = sorted(
            self._profile_validator.iter_errors(profile),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        invalid = tuple(
            InputIssue(_json_pointer(error.absolute_path), error.message)
            for error in errors
        )
        unprocessed = tuple(
            sorted(_find_unprocessed_paths(profile, self._profile_schema))
        )
        return ProfileInspection(invalid=invalid, unprocessed_paths=unprocessed)

    def validate_report(self, report: dict[str, Any]) -> None:
        """Fail loudly when generated output violates the frozen report schema."""

        errors = sorted(
            self._report_validator.iter_errors(report),
            key=lambda error: tuple(str(part) for part in error.absolute_path),
        )
        if not errors:
            return

        details = "; ".join(
            f"{_json_pointer(error.absolute_path)}: {error.message}" for error in errors
        )
        raise ReportContractError(details)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, dict):
        raise TypeError(f"Expected a JSON object in {path}")
    return value


def _json_pointer(path_parts: Any) -> str:
    parts = [str(part).replace("~", "~0").replace("/", "~1") for part in path_parts]
    return "/" + "/".join(parts) if parts else "/"


def _find_unprocessed_paths(
    value: Any, schema: dict[str, Any], path: tuple[str | int, ...] = ()
) -> list[str]:
    """Find keys accepted by `additionalProperties` but unknown to the MVP."""

    paths: list[str] = []
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key, child in value.items():
            child_path = (*path, key)
            child_schema = properties.get(key)
            if child_schema is None:
                paths.append(_json_pointer(child_path))
                continue
            paths.extend(_find_unprocessed_paths(child, child_schema, child_path))
    elif isinstance(value, list):
        item_schema = schema.get("items", {})
        for index, child in enumerate(value):
            paths.extend(_find_unprocessed_paths(child, item_schema, (*path, index)))
    return paths
