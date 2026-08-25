#!/usr/bin/env python3
"""Validate the machine-checkable Paper Reconstruction ABCDE contract."""

from pathlib import Path
import re
import sys


USAGE = "Usage: validate_output.py OUTPUT.md"


def strip_fenced_code(text: str) -> str:
    """Ignore example headings inside fenced code blocks."""
    kept: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if not in_fence:
            kept.append(line)
    return "\n".join(kept)


def validate_current(text: str) -> list[str]:
    errors: list[str] = []
    for letter in "ABCDE":
        if not re.search(rf"(?m)^#\s+{letter}\.", text):
            errors.append(f"missing section {letter}")
    required = {
        "A0 replication source ledger": r"(?m)^##\s+A0\.",
        "B0 task map": r"(?m)^##\s+B0\.",
        "C0 platform identification": r"(?m)^##\s+C0\.",
        "C5 paper analysis route": r"(?m)^##\s+C5\.",
        "D2 minimum data fields": r"(?m)^##\s+D2\.",
        "D3 validation and difference handling": r"(?m)^##\s+D3\.",
        "E2 theory and literature anchors": r"(?m)^##\s+E2\.",
        "E4 evidence-supported research ideas": r"(?m)^##\s+E4\.",
        "action order": r"(?m)^##\s+复现行动顺序",
        "feedback table": r"(?m)^##\s+可编辑反馈表",
    }
    for label, pattern in required.items():
        if not re.search(pattern, text):
            errors.append(f"missing {label}")
    if re.search(r"(?m)^##\s+A0\.", text) and not re.search(
        r"已读取|可访问未读取|发现但受限|未发现|链接失效", text
    ):
        errors.append("A0 source ledger missing an access-status value")
    e4_start = re.search(r"(?m)^##\s+E4\.", text)
    if e4_start:
        e4_segment = text[e4_start.end():]
        evidence_marker = r"证据起点|理论依据|理论命题|理论或相邻文献|evidence start|theoretical basis"
        status_marker = r"已检索确认|部分支持|待检索确认|evidence-supported|partially supported|search-verified"
        if not re.search(evidence_marker, e4_segment, re.IGNORECASE):
            errors.append("E4 research ideas missing an explicit evidence or theory marker")
        if not re.search(status_marker, e4_segment, re.IGNORECASE):
            errors.append("E4 research ideas missing an evidence-status marker")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print(USAGE)
        return 2
    path = Path(sys.argv[1])

    if not path.is_file():
        print(f"INVALID: file not found: {path}")
        return 1

    text = strip_fenced_code(path.read_text(encoding="utf-8"))
    errors = validate_current(text)
    if errors:
        print("INVALID: " + "; ".join(errors))
        return 1
    print("VALID: paper-reconstruction ABCDE contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
