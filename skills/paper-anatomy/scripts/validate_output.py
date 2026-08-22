#!/usr/bin/env python3
"""Validate the machine-checkable Paper Anatomy ABC output contract."""

from pathlib import Path
import re
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_output.py OUTPUT.md")
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"INVALID: file not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for letter in "ABC":
        if not re.search(rf"(?m)^#\s+{letter}\.", text):
            errors.append(f"missing section {letter}")
    for letter in "DEFG":
        if re.search(rf"(?m)^#\s+{letter}\.", text):
            errors.append(f"unexpected reconstruction section {letter}")

    required = {
        "material scope": r"(?m)^##\s+文献与材料范围",
        "B4 result-to-conclusion mapping": r"(?m)^##\s+B4\.",
        "C1 evidence-to-discussion closure": r"(?m)^##\s+C1\.",
        "final judgment": r"(?m)^##\s+最终判断",
    }
    for label, pattern in required.items():
        if not re.search(pattern, text):
            errors.append(f"missing {label}")

    source_limited = bool(re.search(r"定位模式\s*[：:]\s*`?source-limited`?", text, re.IGNORECASE))
    locator_pattern = r"\[(?:Paper|Supplement|OSF):[^\]]*PDF\s+p\.\s*\d+[^\]]*\]"
    limited_pattern = r"\[Source limited:[^\]]+\]"
    if source_limited:
        if not re.search(limited_pattern, text, re.IGNORECASE):
            errors.append("source-limited output missing [Source limited: ...] marker")
    else:
        for label, start, end in (
            ("B4", r"(?m)^##\s+B4\.", r"(?m)^##\s+B5\."),
            ("C1", r"(?m)^##\s+C1\.", r"(?m)^##\s+C2\."),
            ("final judgment", r"(?m)^##\s+最终判断", r"\Z"),
        ):
            begin = re.search(start, text)
            finish = re.search(end, text[begin.end():]) if begin else None
            segment = text[begin.end(): begin.end() + finish.start()] if begin and finish else text[begin.end():] if begin else ""
            if begin and not re.search(locator_pattern, segment, re.IGNORECASE):
                errors.append(f"{label} missing PDF page locator")

    if errors:
        print("INVALID: " + "; ".join(errors))
        return 1
    print("VALID: paper-anatomy ABC contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
