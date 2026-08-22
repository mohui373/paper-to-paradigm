#!/usr/bin/env python3
"""Prepare a page-grounded source bundle for Paper Anatomy.

The generated JSON is a sidecar index. It keeps page text and locator metadata
outside the ABC report so conclusions can cite compact pointers such as
``[Paper: PDF p. 7, Fig. 2]`` without turning the report into a page dump.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any


DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>\]\[(){}\"']+", re.IGNORECASE)
CAPTION_RE = re.compile(
    r"^(?P<kind>fig(?:ure)?|table|图|表)\s*[\.:：]?\s*(?P<label>[A-Za-z]?\d+[A-Za-z]?)\b(?P<rest>.*)$",
    re.IGNORECASE,
)
NUMBERED_HEADING_RE = re.compile(r"^(?:\d+(?:\.\d+){0,3}|[IVX]+)[.)]?\s+\S+", re.IGNORECASE)
CANONICAL_HEADINGS = {
    "abstract",
    "introduction",
    "background",
    "method",
    "methods",
    "materials and methods",
    "results",
    "discussion",
    "conclusion",
    "conclusions",
    "references",
    "acknowledgements",
    "appendix",
    "supplementary materials",
    "摘要",
    "引言",
    "方法",
    "研究方法",
    "结果",
    "讨论",
    "结论",
    "参考文献",
    "附录",
    "补充材料",
}


def clean_token(value: str) -> str:
    return value.strip().rstrip(".,;:)]}，。；：")


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_doi(raw: str) -> str:
    return clean_token(raw).lower()


def classify_url(url: str) -> str:
    lowered = url.lower()
    if "doi.org/" in lowered:
        return "doi"
    if "osf.io" in lowered:
        return "osf"
    if any(token in lowered for token in ("supp", "appendix", "supporting-information", "mmc")):
        return "supplement"
    if any(token in lowered for token in ("prereg", "aspredicted.org", "clinicaltrials.gov")):
        return "preregistration"
    if any(token in lowered for token in ("github.com", "gitlab.com", "codeberg.org")):
        return "code"
    if any(token in lowered for token in ("zenodo.org", "figshare.com", "dataverse", "dryad", "datadryad")):
        return "repository"
    return "other"


def page_label(reader: Any, index: int) -> str | None:
    try:
        labels = reader.page_labels
        if labels and index < len(labels):
            return str(labels[index])
    except Exception:  # PDF page labels are optional and inconsistently encoded.
        pass
    return None


def annotation_urls(page: Any) -> list[str]:
    urls: list[str] = []
    try:
        annotations = page.get("/Annots") or []
        for annotation_ref in annotations:
            annotation = annotation_ref.get_object()
            action = annotation.get("/A")
            if action and action.get("/URI"):
                urls.append(str(action.get("/URI")))
    except Exception:
        pass
    return urls


def text_lines_with_boxes(plumber_page: Any) -> list[dict[str, Any]]:
    """Group extracted words into approximate visual lines with PDF bboxes."""
    try:
        words = plumber_page.extract_words(keep_blank_chars=False, use_text_flow=True)
    except Exception:
        return []
    groups: dict[float, list[dict[str, Any]]] = defaultdict(list)
    for word in words:
        groups[round(float(word.get("top", 0)), 1)].append(word)
    lines: list[dict[str, Any]] = []
    for top in sorted(groups):
        row = sorted(groups[top], key=lambda item: float(item.get("x0", 0)))
        text = " ".join(str(item.get("text", "")) for item in row).strip()
        if not text:
            continue
        lines.append(
            {
                "text": text,
                "bbox": [
                    round(min(float(item.get("x0", 0)) for item in row), 2),
                    round(min(float(item.get("top", 0)) for item in row), 2),
                    round(max(float(item.get("x1", 0)) for item in row), 2),
                    round(max(float(item.get("bottom", 0)) for item in row), 2),
                ],
            }
        )
    return lines


def looks_like_heading(text: str) -> bool:
    compact = re.sub(r"\s+", " ", text).strip()
    lowered = compact.lower().rstrip(":：")
    if lowered in CANONICAL_HEADINGS:
        return True
    if len(compact) > 120 or len(compact.split()) > 16:
        return False
    return bool(NUMBERED_HEADING_RE.match(compact))


def detect_page_items(lines: list[dict[str, Any]], pdf_page: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    headings: list[dict[str, Any]] = []
    figures: list[dict[str, Any]] = []
    tables: list[dict[str, Any]] = []
    for line in lines:
        value = re.sub(r"\s+", " ", line["text"]).strip()
        if looks_like_heading(value):
            headings.append({"title": value, "pdf_page": pdf_page, "bbox": line["bbox"]})
        match = CAPTION_RE.match(value)
        if not match:
            continue
        kind_raw = match.group("kind").lower()
        item = {
            "id": f"{'Table' if kind_raw in {'table', '表'} else 'Figure'} {match.group('label')}",
            "caption": value,
            "pdf_page": pdf_page,
            "caption_bbox": line["bbox"],
        }
        (tables if kind_raw in {"table", "表"} else figures).append(item)
    return headings, figures, tables


def section_ranges(headings: list[dict[str, Any]], page_count: int) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        end_page = page_count
        if index + 1 < len(headings):
            end_page = max(heading["pdf_page"], headings[index + 1]["pdf_page"] - 1)
        sections.append(
            {
                "title": heading["title"],
                "start_pdf_page": heading["pdf_page"],
                "end_pdf_page": end_page,
                "heading_bbox": heading.get("bbox"),
            }
        )
    return sections


def render_pages(pdf: Path, target: Path, warnings: list[str]) -> list[str]:
    executable = shutil.which("pdftoppm")
    if not executable:
        warnings.append("Page rendering skipped: pdftoppm was not found on PATH.")
        return []
    target.mkdir(parents=True, exist_ok=True)
    prefix = target / "page"
    result = subprocess.run(
        [executable, "-png", "-r", "144", str(pdf), str(prefix)],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        warnings.append(f"Page rendering failed: {result.stderr.strip() or 'unknown pdftoppm error'}")
        return []
    return [path.name for path in sorted(target.glob("page-*.png"))]


def prepare(pdf: Path, include_text: bool, render_dir: Path | None) -> dict[str, Any]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf is required: python -m pip install pypdf") from exc

    try:
        import pdfplumber
    except ImportError:
        pdfplumber = None

    reader = PdfReader(str(pdf))
    plumber_document = pdfplumber.open(str(pdf)) if pdfplumber else None
    warnings: list[str] = []
    if reader.is_encrypted:
        warnings.append("The PDF is encrypted; extraction may be incomplete.")
    if plumber_document is None:
        warnings.append("pdfplumber is unavailable; bounding boxes and embedded-image inventory are limited.")

    pages: list[dict[str, Any]] = []
    all_headings: list[dict[str, Any]] = []
    all_figures: list[dict[str, Any]] = []
    all_tables: list[dict[str, Any]] = []
    all_images: list[dict[str, Any]] = []
    urls: list[str] = []
    dois: list[str] = []
    pages_with_text = 0

    for index, page in enumerate(reader.pages):
        number = index + 1
        text = page.extract_text() or ""
        urls.extend(clean_token(item) for item in URL_RE.findall(text))
        urls.extend(clean_token(item) for item in annotation_urls(page))
        dois.extend(normalize_doi(item) for item in DOI_RE.findall(text))
        if text.strip():
            pages_with_text += 1

        lines: list[dict[str, Any]] = []
        images: list[dict[str, Any]] = []
        if plumber_document is not None:
            plumber_page = plumber_document.pages[index]
            lines = text_lines_with_boxes(plumber_page)
            for image_index, image in enumerate(plumber_page.images, start=1):
                entry = {
                    "id": f"PDF-image-p{number}-{image_index}",
                    "pdf_page": number,
                    "bbox": [
                        round(float(image.get("x0", 0)), 2),
                        round(float(image.get("top", 0)), 2),
                        round(float(image.get("x1", 0)), 2),
                        round(float(image.get("bottom", 0)), 2),
                    ],
                    "width": image.get("width"),
                    "height": image.get("height"),
                }
                images.append(entry)
                all_images.append(entry)

        headings, figures, tables = detect_page_items(lines, number)
        all_headings.extend(headings)
        all_figures.extend(figures)
        all_tables.extend(tables)
        page_record: dict[str, Any] = {
            "pdf_page": number,
            "printed_page_label": page_label(reader, index),
            "char_count": len(text),
            "section_headings": headings,
            "figure_captions": figures,
            "table_captions": tables,
            "embedded_images": images,
        }
        if include_text:
            page_record["text"] = text
        else:
            page_record["text_preview"] = re.sub(r"\s+", " ", text).strip()[:500]
        pages.append(page_record)

    if plumber_document is not None:
        plumber_document.close()

    page_count = len(reader.pages)
    ratio = pages_with_text / page_count if page_count else 0
    if ratio >= 0.7:
        locator_mode = "page-grounded"
    elif ratio > 0:
        locator_mode = "mixed-page-grounded"
        warnings.append("Some pages have no extractable text; inspect rendered pages or apply OCR before interpreting them.")
    else:
        locator_mode = "image-page-grounded"
        warnings.append("No extractable text was found; OCR is required for section- and claim-level analysis.")

    rendered_pages: list[str] = []
    if render_dir is not None:
        rendered_pages = render_pages(pdf, render_dir, warnings)

    links = []
    for url in unique(urls):
        links.append({"url": url, "category": classify_url(url), "access_status": "not_checked"})
        if "doi.org/" in url.lower():
            dois.extend(normalize_doi(item) for item in DOI_RE.findall(url))

    metadata = reader.metadata or {}
    return {
        "schema_version": "1.0",
        "prepared_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "file_name": pdf.name,
            "sha256": sha256(pdf),
            "page_count": page_count,
            "title": str(metadata.get("/Title") or "") or None,
            "author": str(metadata.get("/Author") or "") or None,
        },
        "locator_mode": locator_mode,
        "material_scope": {
            "inspected": ["main_pdf"],
            "not_implied_as_inspected": ["supplement", "appendix", "osf", "data", "code", "preregistration"],
            "pages_with_extractable_text": pages_with_text,
            "text_coverage_ratio": round(ratio, 3),
            "rendered_page_directory": render_dir.name if render_dir and rendered_pages else None,
            "rendered_pages": rendered_pages,
        },
        "identifiers": {"doi_candidates": unique(dois)},
        "links": links,
        "sections": section_ranges(all_headings, page_count),
        "figures": all_figures,
        "tables": all_tables,
        "embedded_images": all_images,
        "pages": pages,
        "extraction_warnings": warnings,
        "locator_examples": [
            "[Paper: PDF p. 7]",
            "[Paper: PDF p. 7, Fig. 2]",
            "[Paper: PDF p. 9, Table 1]",
            "[Supplement: PDF p. 3, Appendix A]",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a page/section/figure/table source bundle from a paper PDF.")
    parser.add_argument("pdf", type=Path, help="Input paper PDF")
    parser.add_argument("-o", "--output", type=Path, help="Output JSON path (default: <paper>.source_bundle.json)")
    parser.add_argument("--no-text", action="store_true", help="Store page previews instead of full extracted page text")
    parser.add_argument("--render-pages", type=Path, help="Optional directory for 144-DPI page PNGs (requires pdftoppm)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf = args.pdf.resolve()
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        print(f"ERROR: not a readable PDF: {args.pdf}", file=sys.stderr)
        return 2
    output = args.output or pdf.with_suffix(".source_bundle.json")
    try:
        bundle = prepare(pdf, include_text=not args.no_text, render_dir=args.render_pages)
    except Exception as exc:  # noqa: BLE001 - CLI should provide one clear failure boundary.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Prepared {bundle['source']['page_count']} pages -> {output}")
    print(f"Locator mode: {bundle['locator_mode']}")
    if bundle["extraction_warnings"]:
        for warning in bundle["extraction_warnings"]:
            print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
