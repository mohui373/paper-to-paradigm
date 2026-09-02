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
ABSTRACT_PREFIX_RE = re.compile(r"^(?P<title>abstract|摘要|概要)\s*[\.:：]\s*\S+", re.IGNORECASE)
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
    "author index",
    "subject index",
    "作者索引",
    "主题索引",
}

CANONICAL_SECTION_ORDER = (
    ("abstract", "摘要 / Abstract"),
    ("introduction_theory", "前言与理论 / Introduction & Theory"),
    ("research_design", "研究设计 / Research Design"),
    ("results_analysis", "结果与数据处理 / Results & Analysis"),
    ("discussion_value", "讨论与文章价值 / Discussion & Value"),
)

CANONICAL_SECTION_PATTERNS = {
    "abstract": re.compile(r"^(?:abstract|summary|摘要|概要)$", re.IGNORECASE),
    "introduction_theory": re.compile(
        r"^(?:introduction|background|theoretical background|theoretical framework|"
        r"conceptual framework|literature review|前言|引言|研究背景|理论背景|理论基础|理论框架|文献综述)\b",
        re.IGNORECASE,
    ),
    "research_design": re.compile(
        r"^(?:materials? and methods?|methods?|methodology|research design|study design|"
        r"participants?|sample|procedure|materials?|measures?|measurement|data and methods|"
        r"方法|研究方法|研究设计|参与者|被试|样本|程序|实验材料|测量)\b",
        re.IGNORECASE,
    ),
    "results_analysis": re.compile(
        r"^(?:results?|findings|data analysis|analyses|analysis|statistical analysis|"
        r"结果|研究结果|数据处理|数据分析|统计分析)\b",
        re.IGNORECASE,
    ),
    "discussion_value": re.compile(
        r"^(?:discussion|general discussion|conclusions?|implications?|contributions?|"
        r"limitations?|future research|讨论|总讨论|结论|总结|启示|理论贡献|实践意义|研究价值|"
        r"局限|未来研究)\b",
        re.IGNORECASE,
    ),
}

END_MATTER_RE = re.compile(
    r"^(?:references|bibliography|acknowledgements?|appendix|supplementary materials?|"
    r"参考文献|致谢|附录|补充材料)\b",
    re.IGNORECASE,
)

COLLECTION_BACK_MATTER_RE = re.compile(
    r"^(?:author index|subject index|name index|作者索引|主题索引|人名索引)$",
    re.IGNORECASE,
)


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
        words = plumber_page.extract_words(
            keep_blank_chars=False,
            use_text_flow=True,
            extra_attrs=["size", "fontname"],
        )
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
                "font_size_max": round(max(float(item.get("size", 0) or 0) for item in row), 2),
                "font_bold": any("bold" in str(item.get("fontname", "")).lower() for item in row),
            }
        )
    return lines


def looks_like_heading(text: str) -> bool:
    compact = re.sub(r"\s+", " ", text).strip()
    lowered = compact.lower().rstrip(".:：。")
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
        abstract_prefix = ABSTRACT_PREFIX_RE.match(value)
        if abstract_prefix:
            headings.append(
                {
                    "title": abstract_prefix.group("title").title() if abstract_prefix.group("title").isascii() else abstract_prefix.group("title"),
                    "pdf_page": pdf_page,
                    "bbox": line["bbox"],
                    "detected_from": "inline_prefix",
                }
            )
        elif looks_like_heading(value):
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


def normalize_heading(text: str) -> str:
    value = re.sub(r"\s+", " ", text).strip().rstrip(".:：。")
    value = re.sub(r"^(?:\d+(?:\.\d+){0,3}|[IVX]+)[.)]?\s+", "", value, flags=re.IGNORECASE)
    return value.strip()


def canonical_section(text: str) -> str | None:
    normalized = normalize_heading(text)
    for category, pattern in CANONICAL_SECTION_PATTERNS.items():
        if pattern.match(normalized):
            return category
    return None


def title_before_abstract(page: dict[str, Any], abstract_heading: dict[str, Any]) -> str | None:
    """Choose the most title-like line above an Abstract heading."""
    abstract_top = float((abstract_heading.get("bbox") or [0, 10_000])[1])
    candidates = []
    for line in page.get("layout_lines", []):
        value = re.sub(r"\s+", " ", line.get("text", "")).strip()
        top = float((line.get("bbox") or [0, 10_000])[1])
        if not value or top >= abstract_top or len(value) < 8:
            continue
        lowered = value.lower()
        if DOI_RE.search(value) or URL_RE.search(value):
            continue
        if lowered.startswith(("abstract", "keywords", "chapter ", "©", "http")):
            continue
        if re.fullmatch(r"[\d\s|–—-]+", value):
            continue
        candidates.append(line)
    if not candidates:
        return None
    largest = max(float(item.get("font_size_max", 0) or 0) for item in candidates)
    title_lines = [
        item
        for item in candidates
        if float(item.get("font_size_max", 0) or 0) >= max(12.0, largest - 0.75)
    ]
    if not title_lines:
        title_lines = [max(candidates, key=lambda item: float(item.get("font_size_max", 0) or 0))]
    title_lines.sort(key=lambda item: float((item.get("bbox") or [0, 0])[1]))
    title = " ".join(re.sub(r"\s+", " ", item["text"]).strip() for item in title_lines)
    return title[:500] or None


def build_canonical_index(
    headings: list[dict[str, Any]], start_page: int, end_page: int
) -> list[dict[str, Any]]:
    relevant = [item for item in headings if start_page <= item["pdf_page"] <= end_page]
    major = []
    for item in relevant:
        category = canonical_section(item["title"])
        if category:
            major.append({**item, "category": category})
        elif END_MATTER_RE.match(normalize_heading(item["title"])):
            major.append({**item, "category": "end_matter"})

    ranges_by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, item in enumerate(major):
        category = item["category"]
        if category == "end_matter":
            continue
        next_page = end_page + 1
        if index + 1 < len(major):
            next_page = major[index + 1]["pdf_page"]
        range_item = {
            "start_pdf_page": item["pdf_page"],
            "end_pdf_page": max(item["pdf_page"], next_page - 1),
            "heading_titles": [item["title"]],
        }
        existing = ranges_by_category[category]
        if existing and range_item["start_pdf_page"] <= existing[-1]["end_pdf_page"] + 1:
            existing[-1]["end_pdf_page"] = max(existing[-1]["end_pdf_page"], range_item["end_pdf_page"])
            existing[-1]["heading_titles"].extend(range_item["heading_titles"])
        else:
            existing.append(range_item)

    result = []
    for category, label in CANONICAL_SECTION_ORDER:
        ranges = ranges_by_category.get(category, [])
        result.append(
            {
                "category": category,
                "label": label,
                "status": "detected" if ranges else "not_detected",
                "ranges": ranges,
            }
        )
    return result


def detect_papers(
    pages: list[dict[str, Any]], headings: list[dict[str, Any]], metadata_title: str | None
) -> tuple[str, list[dict[str, Any]], dict[str, Any] | None, dict[str, Any] | None]:
    abstract_starts: list[dict[str, Any]] = []
    for page in pages:
        for heading in page["section_headings"]:
            if canonical_section(heading["title"]) == "abstract":
                abstract_starts.append(
                    {
                        "pdf_page": page["pdf_page"],
                        "heading": heading,
                        "title": title_before_abstract(page, heading),
                    }
                )
                break

    # Multiple distinct Abstract openings are the strongest layout-level signal
    # available without depending on publisher-specific proceedings metadata.
    distinct_starts = []
    seen_pages: set[int] = set()
    for item in abstract_starts:
        if item["pdf_page"] not in seen_pages:
            seen_pages.add(item["pdf_page"])
            distinct_starts.append(item)

    page_count = len(pages)
    if len(distinct_starts) >= 2:
        document_type = "multi_paper_collection"
        starts = distinct_starts
        front_matter = None
        if starts[0]["pdf_page"] > 1:
            front_matter = {"start_pdf_page": 1, "end_pdf_page": starts[0]["pdf_page"] - 1}
        back_matter_start = next(
            (
                heading["pdf_page"]
                for heading in headings
                if heading["pdf_page"] > starts[-1]["pdf_page"]
                and COLLECTION_BACK_MATTER_RE.match(normalize_heading(heading["title"]))
            ),
            None,
        )
        back_matter = (
            {"start_pdf_page": back_matter_start, "end_pdf_page": page_count}
            if back_matter_start is not None
            else None
        )
    else:
        document_type = "single_paper"
        starts = [
            {
                "pdf_page": 1,
                "heading": distinct_starts[0]["heading"] if distinct_starts else None,
                "title": metadata_title or (distinct_starts[0]["title"] if distinct_starts else None),
            }
        ]
        front_matter = None
        back_matter = None

    papers = []
    for index, item in enumerate(starts):
        start_page = item["pdf_page"]
        if index + 1 < len(starts):
            end_page = starts[index + 1]["pdf_page"] - 1
        else:
            end_page = (back_matter["start_pdf_page"] - 1) if back_matter else page_count
        paper_headings = [entry for entry in headings if start_page <= entry["pdf_page"] <= end_page]
        paper_pages = pages[start_page - 1 : end_page]
        paper_dois = unique(
            doi for page in paper_pages for doi in page.get("doi_candidates", [])
        )
        papers.append(
            {
                "paper_id": f"paper-{index + 1:03d}",
                "ordinal": index + 1,
                "title": item.get("title") or f"Untitled paper {index + 1}",
                "start_pdf_page": start_page,
                "end_pdf_page": end_page,
                "doi_candidates": paper_dois,
                "canonical_sections": build_canonical_index(paper_headings, start_page, end_page),
                "raw_sections": section_ranges(paper_headings, end_page),
            }
        )
    return document_type, papers, front_matter, back_matter


def select_papers(papers: list[dict[str, Any]], selectors: list[str] | None) -> dict[str, Any]:
    if not selectors:
        return {
            "mode": "all_default",
            "requested": [],
            "selected_paper_ids": [paper["paper_id"] for paper in papers],
            "selected_page_ranges": [
                {"paper_id": paper["paper_id"], "start_pdf_page": paper["start_pdf_page"], "end_pdf_page": paper["end_pdf_page"]}
                for paper in papers
            ],
        }

    selected: list[dict[str, Any]] = []
    for raw_selector in selectors:
        selector = raw_selector.strip().casefold()
        matches = []
        for paper in papers:
            exact_keys = {
                paper["paper_id"].casefold(),
                str(paper["ordinal"]),
                *(doi.casefold() for doi in paper["doi_candidates"]),
            }
            title = str(paper.get("title") or "").casefold()
            if selector in exact_keys or (selector and selector in title):
                matches.append(paper)
        if len(matches) != 1:
            reason = "not found" if not matches else "ambiguous"
            raise ValueError(f"Article selector {raw_selector!r} is {reason}; use a paper ID, ordinal, DOI, or a unique title phrase.")
        if matches[0] not in selected:
            selected.append(matches[0])

    return {
        "mode": "explicit",
        "requested": selectors,
        "selected_paper_ids": [paper["paper_id"] for paper in selected],
        "selected_page_ranges": [
            {"paper_id": paper["paper_id"], "start_pdf_page": paper["start_pdf_page"], "end_pdf_page": paper["end_pdf_page"]}
            for paper in selected
        ],
    }


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


def prepare(
    pdf: Path,
    include_text: bool,
    render_dir: Path | None,
    article_selectors: list[str] | None = None,
) -> dict[str, Any]:
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
        page_urls = [clean_token(item) for item in URL_RE.findall(text)]
        page_dois = [normalize_doi(item) for item in DOI_RE.findall(text)]
        urls.extend(page_urls)
        urls.extend(clean_token(item) for item in annotation_urls(page))
        dois.extend(page_dois)
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
            "doi_candidates": unique(page_dois),
            "url_candidates": unique(page_urls),
            "layout_lines": lines,
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
    metadata_title = str(metadata.get("/Title") or "") or None
    document_type, papers, front_matter, back_matter = detect_papers(pages, all_headings, metadata_title)
    selection = select_papers(papers, article_selectors)
    # Layout lines are temporary title-detection features, not part of the public
    # sidecar schema. Keeping them would duplicate page text and inflate the index.
    for page in pages:
        page.pop("layout_lines", None)
    return {
        "schema_version": "1.1",
        "prepared_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "file_name": pdf.name,
            "sha256": sha256(pdf),
            "page_count": page_count,
            "title": metadata_title,
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
        "document_index": {
            "document_type": document_type,
            "paper_count": len(papers),
            "front_matter": front_matter,
            "back_matter": back_matter,
            "selection": selection,
            "papers": papers,
        },
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
    parser.add_argument(
        "--article",
        action="append",
        help="Select one paper in a multi-paper PDF by ordinal, paper ID, DOI, or unique title phrase; repeat to select several. Default: all papers.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf = args.pdf.resolve()
    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        print(f"ERROR: not a readable PDF: {args.pdf}", file=sys.stderr)
        return 2
    output = args.output or pdf.with_suffix(".source_bundle.json")
    try:
        bundle = prepare(
            pdf,
            include_text=not args.no_text,
            render_dir=args.render_pages,
            article_selectors=args.article,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should provide one clear failure boundary.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Prepared {bundle['source']['page_count']} pages -> {output}")
    print(f"Locator mode: {bundle['locator_mode']}")
    index = bundle["document_index"]
    print(f"Document type: {index['document_type']}; papers: {index['paper_count']}")
    for paper in index["papers"]:
        marker = "*" if paper["paper_id"] in index["selection"]["selected_paper_ids"] else " "
        print(f"{marker} {paper['paper_id']} | PDF pp. {paper['start_pdf_page']}-{paper['end_pdf_page']} | {paper['title']}")
    if bundle["extraction_warnings"]:
        for warning in bundle["extraction_warnings"]:
            print(f"WARNING: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
