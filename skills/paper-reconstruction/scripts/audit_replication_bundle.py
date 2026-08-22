#!/usr/bin/env python3
"""Audit cross-artifact semantic consistency in a replication bundle."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ALLOWED_RELATIONS = {
    "serial",
    "serial-repeat",
    "interleaved-repeat",
    "nested-repeat",
    "conditional",
    "parallel-external",
}
ALLOWED_LIST_ORDERS = {
    "Sequential",
    "Random",
    "RandomWithReplacement",
    "Counterbalance",
    "Offset",
    "Permutation",
}
RUNTIME_STATES = {"design-only", "buildable", "generated", "runtime-verified"}
REQUIRED_STABLE_IDS = {"Subject", "Session", "StudyID", "BlockIndex", "TrialIndex", "TrialUID"}


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def load_json(path: Path, audit: Audit) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - aggregate malformed artifacts.
        audit.error(f"cannot read JSON {path.name}: {exc}")
        return {}


def load_table(path: Path, audit: Audit) -> list[dict[str, str]]:
    try:
        delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle, delimiter=delimiter))
    except Exception as exc:  # noqa: BLE001 - aggregate malformed artifacts.
        audit.error(f"cannot read table {path.name}: {exc}")
        return []


def unique_named(items: list[dict[str, Any]], label: str, audit: Audit) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        name = str(item.get("name", "")).strip()
        if not name:
            audit.error(f"{label}[{index}] missing name")
        elif name in result:
            audit.error(f"duplicate {label} name: {name}")
        else:
            result[name] = item
    return result


def resolve_artifacts(root: Path, artifacts: dict[str, Any], audit: Audit) -> dict[str, Path]:
    resolved: dict[str, Path] = {}
    for name, value in artifacts.items():
        relative = value.get("path") if isinstance(value, dict) else value
        if not isinstance(relative, str) or not relative.strip():
            audit.error(f"artifact {name} missing path")
            continue
        path = (root / relative).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            audit.error(f"artifact {name} escapes bundle directory: {relative}")
            continue
        resolved[name] = path
        if not path.is_file():
            audit.error(f"artifact {name} not found: {relative}")
    return resolved


def audit_sources(manifest: dict[str, Any], artifacts: dict[str, Any], audit: Audit) -> set[str]:
    sources = manifest.get("sources", [])
    source_ids: set[str] = set()
    allowed_status = {"已读取", "可访问未读取", "发现但受限", "未发现", "链接失效", "复现建议"}
    for index, source in enumerate(sources):
        source_id = str(source.get("id", "")).strip()
        if not source_id:
            audit.error(f"sources[{index}] missing id")
            continue
        if source_id in source_ids:
            audit.error(f"duplicate source id: {source_id}")
        source_ids.add(source_id)
        if source.get("status") not in allowed_status:
            audit.error(f"source {source_id} has invalid access status: {source.get('status')!r}")

    for artifact_name, value in artifacts.items():
        if not isinstance(value, dict):
            continue
        for source_id in value.get("source_ids", []):
            if source_id not in source_ids:
                audit.error(f"artifact {artifact_name} references unknown source id: {source_id}")
    return source_ids


def audit_execution(
    root: Path,
    manifest: dict[str, Any],
    artifact_paths: dict[str, Path],
    audit: Audit,
) -> tuple[set[str], set[str], set[str]]:
    execution = manifest.get("execution", {})
    procedures = unique_named(execution.get("procedures", []), "procedure", audit)
    lists = unique_named(execution.get("lists", []), "list", audit)
    conditions = {str(value) for value in manifest.get("conditions", [])}
    if not conditions:
        audit.error("manifest conditions must not be empty")

    entry = execution.get("entry_procedure")
    if entry not in procedures:
        audit.error(f"entry procedure is not defined: {entry!r}")

    for name, procedure in procedures.items():
        caller = procedure.get("called_by")
        if name == entry:
            if caller not in (None, ""):
                audit.error(f"entry procedure {name} must not be called_by a List")
        elif caller not in lists:
            audit.error(f"procedure {name} is not called by a defined List: {caller!r}")
        elif name not in lists[caller].get("calls", []):
            audit.error(f"procedure {name} says called_by {caller}, but that List does not call it")
        timeline = procedure.get("timeline", [])
        if not timeline or len(timeline) != len(set(timeline)):
            audit.error(f"procedure {name} timeline must be non-empty with unique object names")

    all_nodes = set(procedures) | set(lists)
    serial_edges: list[tuple[str, str]] = []
    for index, relation in enumerate(execution.get("relations", [])):
        origin = relation.get("from")
        target = relation.get("to")
        relation_type = relation.get("type")
        if origin not in all_nodes or target not in all_nodes:
            audit.error(f"relation[{index}] references unknown node: {origin!r} -> {target!r}")
        if relation_type not in ALLOWED_RELATIONS:
            audit.error(f"relation[{index}] has invalid type {relation_type!r}; do not use ambiguous 'parallel'")
        if relation_type == "parallel-external" and not relation.get("synchronization_contract"):
            audit.error(f"parallel-external relation {origin!r}->{target!r} lacks synchronization_contract")
        if relation_type == "serial":
            serial_edges.append((str(origin), str(target)))

    adjacency: dict[str, list[str]] = {node: [] for node in all_nodes}
    for origin, target in serial_edges:
        if origin in adjacency and target in adjacency:
            adjacency[origin].append(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            audit.error(f"serial execution cycle detected at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for child in adjacency[node]:
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for node in adjacency:
        visit(node)

    for name, list_spec in lists.items():
        order = list_spec.get("order")
        relation_type = list_spec.get("relation_type")
        if order not in ALLOWED_LIST_ORDERS:
            audit.error(f"List {name} has unsupported Order: {order!r}")
        if relation_type not in ALLOWED_RELATIONS:
            audit.error(f"List {name} has invalid relation_type: {relation_type!r}")
        for called in list_spec.get("calls", []):
            if called not in procedures:
                audit.error(f"List {name} calls undefined procedure {called}")

        table_path = (root / str(list_spec.get("file", ""))).resolve()
        if not table_path.is_file():
            audit.error(f"List {name} table not found: {list_spec.get('file')!r}")
            continue
        rows = load_table(table_path, audit)
        if list_spec.get("rows") != len(rows):
            audit.error(f"List {name} declares {list_spec.get('rows')} rows but file contains {len(rows)}")
        if rows and "Procedure" not in rows[0]:
            audit.error(f"List {name} table missing Procedure column")
        if relation_type == "interleaved-repeat" and rows:
            trial_kinds = {row.get("TrialKind", "") for row in rows}
            if len(trial_kinds - {""}) < 2:
                audit.error(f"interleaved-repeat List {name} needs at least two TrialKind values")
        for row_index, row in enumerate(rows, start=2):
            called = row.get("Procedure", "")
            if called not in list_spec.get("calls", []):
                audit.error(f"{table_path.name}:{row_index} Procedure {called!r} is not declared in List {name}.calls")
            condition = row.get("Condition", "")
            if condition and condition not in conditions:
                audit.error(f"{table_path.name}:{row_index} unknown Condition {condition!r}")
            weight = row.get("Weight", "1")
            try:
                if float(weight) <= 0:
                    raise ValueError
            except ValueError:
                audit.error(f"{table_path.name}:{row_index} Weight must be positive: {weight!r}")

    map_path = artifact_paths.get("procedure_map")
    object_names: set[str] = set()
    if map_path and map_path.is_file():
        rows = load_table(map_path, audit)
        mapped: dict[str, list[tuple[int, str]]] = {name: [] for name in procedures}
        for row_index, row in enumerate(rows, start=2):
            name = row.get("Procedure", "")
            if name not in procedures:
                audit.error(f"{map_path.name}:{row_index} unknown Procedure {name!r}")
                continue
            try:
                order = int(row.get("TimelineIndex", ""))
            except ValueError:
                audit.error(f"{map_path.name}:{row_index} invalid TimelineIndex")
                continue
            object_name = row.get("ObjectName", "")
            if object_name in object_names:
                audit.error(f"duplicate E-Prime object name: {object_name}")
            object_names.add(object_name)
            mapped[name].append((order, object_name))
        for name, procedure in procedures.items():
            actual = [value for _, value in sorted(mapped.get(name, []))]
            if actual != procedure.get("timeline", []):
                audit.error(f"procedure_map timeline mismatch for {name}: manifest={procedure.get('timeline', [])}, table={actual}")

    return set(procedures), set(lists), object_names


def audit_data_contract(
    manifest: dict[str, Any],
    artifact_paths: dict[str, Path],
    object_names: set[str],
    audit: Audit,
) -> None:
    event_path = artifact_paths.get("event_log_schema")
    dictionary_path = artifact_paths.get("data_dictionary")
    analysis_path = artifact_paths.get("analysis_contract")
    if not all((event_path, dictionary_path, analysis_path)):
        return

    event_data = load_json(event_path, audit)
    event_fields = unique_named(event_data.get("fields", []), "event field", audit)
    dictionary_rows = load_table(dictionary_path, audit)
    dictionary = {row.get("VariableName", ""): row for row in dictionary_rows if row.get("VariableName")}
    if len(dictionary) != len(dictionary_rows):
        audit.error("data dictionary has blank or duplicate VariableName values")

    stable_ids = set(manifest.get("logging", {}).get("stable_id_fields", []))
    missing_ids = REQUIRED_STABLE_IDS - stable_ids
    if missing_ids:
        audit.error(f"logging.stable_id_fields missing {sorted(missing_ids)}")

    for name, field in event_fields.items():
        if name not in dictionary:
            audit.error(f"event field {name} missing from data dictionary")
        source_object = field.get("source_object")
        if source_object not in object_names and source_object not in {"Context", "Derived"}:
            audit.error(f"event field {name} references unknown source_object {source_object!r}")
    for name in stable_ids:
        if name not in event_fields:
            audit.error(f"stable ID {name} missing from event log schema")

    analysis = load_json(analysis_path, audit)
    for name in analysis.get("required_fields", []):
        if name not in dictionary:
            audit.error(f"analysis requires field {name} missing from data dictionary")
    for derived in analysis.get("derived_fields", []):
        name = derived.get("name")
        inputs = derived.get("inputs", [])
        if not name or not derived.get("formula"):
            audit.error("derived analysis field requires name and formula")
        if name not in dictionary:
            audit.error(f"derived analysis field {name!r} missing from data dictionary")
        for source in inputs:
            if source not in dictionary:
                audit.error(f"derived field {name!r} uses unknown input {source!r}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_runtime(root: Path, manifest: dict[str, Any], audit: Audit) -> None:
    platform = manifest.get("platform", {})
    state = platform.get("runtime_state")
    if state not in RUNTIME_STATES:
        audit.error(f"platform.runtime_state must be one of {sorted(RUNTIME_STATES)}, got {state!r}")
        return
    if state != "runtime-verified":
        audit.note(f"runtime state is {state}; do not describe this bundle as runtime-verified")
        return
    runtime = platform.get("runtime_artifacts", {})
    for label, expected_suffix in (("experiment", ".es3"), ("generated_script", ".ebs3"), ("smoke_log", ".txt")):
        item = runtime.get(label, {})
        path = (root / str(item.get("path", ""))).resolve()
        if not path.is_file() or path.suffix.lower() != expected_suffix:
            audit.error(f"runtime-verified bundle missing {label} {expected_suffix} artifact")
            continue
        expected_hash = item.get("sha256")
        if not expected_hash or sha256(path) != expected_hash:
            audit.error(f"runtime artifact hash mismatch: {label}")
    if not platform.get("eprime_version") or not platform.get("smoke_tested_at"):
        audit.error("runtime-verified bundle requires eprime_version and smoke_tested_at")


def audit_bundle(root: Path) -> Audit:
    audit = Audit()
    root = root.resolve()
    manifest_path = root / "bundle_manifest.json"
    if not manifest_path.is_file():
        audit.error("bundle_manifest.json not found")
        return audit
    manifest = load_json(manifest_path, audit)
    if manifest.get("schema_version") != "1.0":
        audit.error("bundle schema_version must be 1.0")
    if not manifest.get("study_id"):
        audit.error("bundle study_id is required")
    artifacts = manifest.get("artifacts", {})
    artifact_paths = resolve_artifacts(root, artifacts, audit)
    audit_sources(manifest, artifacts, audit)
    _, _, objects = audit_execution(root, manifest, artifact_paths, audit)
    audit_data_contract(manifest, artifact_paths, objects, audit)
    audit_runtime(root, manifest, audit)
    return audit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit semantic consistency across a replication bundle.")
    parser.add_argument("bundle", type=Path, help="Directory containing bundle_manifest.json")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable JSON result")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = audit_bundle(args.bundle)
    valid = not audit.errors and not (args.strict and audit.warnings)
    if args.json:
        print(json.dumps({"valid": valid, "errors": audit.errors, "warnings": audit.warnings, "notes": audit.notes}, ensure_ascii=False, indent=2))
    else:
        print("REPLICATION BUNDLE VALID" if valid else "REPLICATION BUNDLE INVALID")
        for label, messages in (("ERROR", audit.errors), ("WARNING", audit.warnings), ("NOTE", audit.notes)):
            for message in messages:
                print(f"- {label}: {message}")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
