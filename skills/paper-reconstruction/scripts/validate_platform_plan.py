#!/usr/bin/env python3
"""Validate a platform-native reconstruction plan across implementation and analysis layers."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any


IMPLEMENTATION_LEVELS = {"conceptual", "program", "statistical", "direct-copy"}
RUNTIME_STATES = {"design-only", "buildable", "generated", "runtime-verified"}
SOURCE_STATUSES = {"inspected", "accessible-not-read", "restricted", "missing", "broken-link"}
SELECTION_SOURCES = {"user-explicit", "team-default", "paper-original", "neutral-default"}

ALIASES = {
    "e-prime": "e-prime",
    "e-prime-3": "e-prime",
    "e-prime-3.0": "e-prime",
    "psychopy": "psychopy",
    "matlab": "matlab-psychtoolbox",
    "psychtoolbox": "matlab-psychtoolbox",
    "matlab-psychtoolbox": "matlab-psychtoolbox",
    "jspsych": "jspsych",
    "qualtrics": "qualtrics",
    "sosci": "sosci",
    "sosci-survey": "sosci",
    "otree": "otree",
    "inquisit": "inquisit",
    "gorilla": "gorilla",
    "field-protocol": "field-protocol",
    "platform-neutral": "platform-neutral",
}

PLATFORM_COMPONENTS = {
    "psychopy": [{"routine"}],
    "matlab-psychtoolbox": [{"entry-point", "main-script"}, {"screen"}, {"response-handler", "kbqueue"}],
    "jspsych": [{"timeline"}, {"plugin"}],
    "qualtrics": [{"block"}, {"survey-flow"}],
    "sosci": [{"question-page", "questionnaire-page"}],
    "otree": [{"subsession"}, {"player"}, {"page"}],
    "inquisit": [{"script"}, {"trial"}],
    "gorilla": [{"task"}],
    "field-protocol": [{"protocol-step"}, {"experimenter-log"}],
}


def normalized(value: Any) -> str:
    return re.sub(r"\s+", "-", str(value or "").strip().lower())


def unique_values(items: list[dict[str, Any]], key: str, label: str, errors: list[str]) -> set[str]:
    values: set[str] = set()
    for index, item in enumerate(items):
        value = str(item.get(key, "")).strip()
        if not value:
            errors.append(f"{label}[{index}] missing {key}")
        elif value in values:
            errors.append(f"{label} duplicate {key}: {value}")
        values.add(value)
    return values


def validate_plan(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if plan.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if not str(plan.get("study_id", "")).strip():
        errors.append("study_id is required")

    level = normalized(plan.get("implementation_level"))
    if level not in IMPLEMENTATION_LEVELS:
        errors.append(f"implementation_level must be one of {sorted(IMPLEMENTATION_LEVELS)}")

    platform = plan.get("target_platform") or {}
    raw_platform = normalized(platform.get("name"))
    platform_name = ALIASES.get(raw_platform, raw_platform)
    selection_source = normalized(platform.get("selection_source"))
    if selection_source not in SELECTION_SOURCES:
        errors.append(f"target_platform.selection_source must be one of {sorted(SELECTION_SOURCES)}")
    if level in {"program", "direct-copy"} and platform_name in {"", "unspecified", "platform-neutral"}:
        errors.append("program/direct-copy plan requires a concrete target platform")

    runtime_state = normalized(plan.get("runtime_state"))
    if runtime_state not in RUNTIME_STATES:
        errors.append(f"runtime_state must be one of {sorted(RUNTIME_STATES)}")

    sources = plan.get("evidence_sources") or []
    if not sources:
        errors.append("evidence_sources must not be empty")
    for index, source in enumerate(sources):
        if normalized(source.get("status")) not in SOURCE_STATUSES:
            errors.append(f"evidence_sources[{index}].status is invalid")

    phases = plan.get("phases") or []
    components = plan.get("components") or []
    phase_ids = unique_values(phases, "id", "phases", errors)
    component_ids = unique_values(components, "id", "components", errors)
    native_types = {normalized(item.get("native_type")) for item in components}

    if level in {"program", "direct-copy"} and (not phases or not components):
        errors.append("program/direct-copy plan requires phases and native components")
    for component in components:
        if component.get("phase_id") not in phase_ids:
            errors.append(f"component {component.get('id', '<missing>')} references unknown phase_id")
    for phase in phases:
        for component_id in phase.get("component_ids", []):
            if component_id not in component_ids:
                errors.append(f"phase {phase.get('id', '<missing>')} references unknown component {component_id}")

    for group in PLATFORM_COMPONENTS.get(platform_name, []):
        if not native_types.intersection(group):
            errors.append(f"{platform_name} plan missing native component type from {sorted(group)}")

    data = plan.get("data_contract") or {}
    stable_ids = set(data.get("stable_ids") or [])
    raw_fields = set(data.get("raw_fields") or [])
    derived_fields = set(data.get("derived_fields") or [])
    analysis_fields = set(data.get("analysis_fields") or [])
    declared_fields = stable_ids | raw_fields | derived_fields
    for phase in phases:
        for field in phase.get("output_fields", []):
            if field not in declared_fields:
                errors.append(f"phase {phase.get('id', '<missing>')} emits undeclared field {field}")
    for field in analysis_fields:
        if field not in declared_fields:
            errors.append(f"analysis field {field} is not logged or derived")

    study_type = normalized(plan.get("study_type"))
    if study_type in {"survey", "longitudinal-survey"}:
        for field in {"item_id", "response_raw", "completion_status"} - declared_fields:
            errors.append(f"survey data contract missing {field}")
    if study_type == "longitudinal-survey":
        for field in {"participant_key", "wave_id", "invitation_status"} - declared_fields:
            errors.append(f"longitudinal data contract missing {field}")
        waves = plan.get("waves") or []
        wave_ids = unique_values(waves, "id", "waves", errors)
        if len(wave_ids) < 2:
            errors.append("longitudinal plan requires at least two waves")

    analysis = plan.get("analysis") or {}
    if analysis.get("required"):
        environment = normalized(analysis.get("environment"))
        if environment in {"", "unspecified"}:
            errors.append("analysis.environment must be explicit or platform-neutral")
        if normalized(analysis.get("selection_source")) not in SELECTION_SOURCES:
            errors.append(f"analysis.selection_source must be one of {sorted(SELECTION_SOURCES)}")
        if not analysis.get("artifacts"):
            errors.append("analysis.artifacts must not be empty when analysis is required")

    tests = plan.get("validation_tests") or []
    if level in {"program", "direct-copy"} and not tests:
        errors.append("program/direct-copy plan requires validation_tests")
    for index, test in enumerate(tests):
        if not test.get("id") or not test.get("target") or not test.get("pass_criterion"):
            errors.append(f"validation_tests[{index}] requires id, target, and pass_criterion")

    if runtime_state == "runtime-verified":
        evidence = plan.get("runtime_evidence") or {}
        for key in ("environment_record", "smoke_test", "artifact_hashes"):
            if not evidence.get(key):
                errors.append(f"runtime-verified plan missing runtime_evidence.{key}")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_platform_plan.py PLAN.json")
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"INVALID: file not found: {path}")
        return 1
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"INVALID: cannot read JSON: {exc}")
        return 1
    errors = validate_plan(plan)
    if errors:
        print("INVALID: " + "; ".join(errors))
        return 1
    print("VALID: cross-platform reconstruction plan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
