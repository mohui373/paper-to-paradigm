from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/paper-anatomy/scripts/prepare_paper.py"
GENERATOR = ROOT / "tests/fixtures/generate_synthetic_paper.py"
FIXTURE = ROOT / "tests/fixtures/synthetic_paper.pdf"
RECONSTRUCTION_SKILL = ROOT / "skills/paper-reconstruction/SKILL.md"
RECONSTRUCTION_CONTRACT = ROOT / "skills/paper-reconstruction/references/output-contract.md"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PREPARE = load_module("prepare_paper", SCRIPT)
FIXTURE_GENERATOR = load_module("generate_synthetic_paper", GENERATOR)


class PreparePaperTests(unittest.TestCase):
    def test_reconstruction_reuses_index_without_exposing_it_in_output(self) -> None:
        skill_text = RECONSTRUCTION_SKILL.read_text(encoding="utf-8")
        contract_text = RECONSTRUCTION_CONTRACT.read_text(encoding="utf-8")
        self.assertIn("../paper-anatomy/scripts/prepare_paper.py", skill_text)
        self.assertIn("未指定时默认处理索引中的全部论文", skill_text)
        self.assertIn("仅作为本地导航侧车，不进入 ABCDE 正文", contract_text)

    def test_inline_abstract_prefix_is_a_heading(self) -> None:
        lines = [{"text": "Abstract. This sentence begins on the heading line.", "bbox": [10, 20, 300, 35]}]
        headings, _, _ = PREPARE.detect_page_items(lines, 7)
        self.assertEqual("Abstract", headings[0]["title"])
        self.assertEqual("inline_prefix", headings[0]["detected_from"])

    def test_standalone_abstract_with_period_is_a_heading(self) -> None:
        lines = [{"text": "Abstract.", "bbox": [10, 20, 80, 35]}]
        headings, _, _ = PREPARE.detect_page_items(lines, 7)
        self.assertEqual("Abstract.", headings[0]["title"])

    def test_fixture_is_programmatically_rebuildable(self) -> None:
        self.assertTrue(FIXTURE.is_file())
        with tempfile.TemporaryDirectory(prefix="paper-to-paradigm-pdf-") as temp_dir:
            generated = Path(temp_dir) / "synthetic_paper.pdf"
            FIXTURE_GENERATOR.build_pdf(generated)
            self.assertGreater(generated.stat().st_size, 1000)
            self.assertEqual(3, len(PREPARE.prepare(generated, include_text=False, render_dir=None)["pages"]))

    def test_extracts_sections_figures_tables_links_and_image(self) -> None:
        bundle = PREPARE.prepare(FIXTURE, include_text=True, render_dir=None)
        self.assertEqual(3, bundle["source"]["page_count"])
        self.assertEqual("page-grounded", bundle["locator_mode"])
        self.assertEqual("Synthetic Behavioral Study for PDF Grounding Tests", bundle["source"]["title"])
        self.assertIn("10.12345/paper-to-paradigm.synthetic-fixture", bundle["identifiers"]["doi_candidates"])
        section_titles = {item["title"] for item in bundle["sections"]}
        for title in {"Abstract", "1. Introduction", "2. Methods", "3. Results", "4. Discussion", "Appendix"}:
            self.assertIn(title, section_titles)
        self.assertIn("Figure 1", {item["id"] for item in bundle["figures"]})
        self.assertIn("Table 1", {item["id"] for item in bundle["tables"]})
        self.assertGreaterEqual(len(bundle["embedded_images"]), 1)
        urls = {item["url"] for item in bundle["links"]}
        self.assertIn("https://example.org/synthetic-supplement.pdf", urls)
        index = bundle["document_index"]
        self.assertEqual("single_paper", index["document_type"])
        self.assertEqual(1, index["paper_count"])
        self.assertEqual("all_default", index["selection"]["mode"])
        categories = {item["category"]: item["status"] for item in index["papers"][0]["canonical_sections"]}
        self.assertTrue(all(status == "detected" for status in categories.values()))

    def test_indexes_and_selects_papers_in_a_proceedings_pdf(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-to-paradigm-proceedings-") as temp_dir:
            proceedings = Path(temp_dir) / "proceedings.pdf"
            FIXTURE_GENERATOR.build_proceedings_pdf(proceedings)
            bundle = PREPARE.prepare(proceedings, include_text=False, render_dir=None)
            index = bundle["document_index"]
            self.assertEqual("multi_paper_collection", index["document_type"])
            self.assertEqual(2, index["paper_count"])
            self.assertEqual(["paper-001", "paper-002"], index["selection"]["selected_paper_ids"])
            self.assertEqual((1, 2), (index["papers"][0]["start_pdf_page"], index["papers"][0]["end_pdf_page"]))
            self.assertEqual((3, 4), (index["papers"][1]["start_pdf_page"], index["papers"][1]["end_pdf_page"]))
            self.assertEqual({"start_pdf_page": 5, "end_pdf_page": 5}, index["back_matter"])
            self.assertIn("First Synthetic Proceedings Paper", index["papers"][0]["title"])

            selected = PREPARE.prepare(
                proceedings,
                include_text=False,
                render_dir=None,
                article_selectors=["Second Synthetic"],
            )["document_index"]["selection"]
            self.assertEqual("explicit", selected["mode"])
            self.assertEqual(["paper-002"], selected["selected_paper_ids"])

    def test_article_selector_must_match_uniquely(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-to-paradigm-proceedings-") as temp_dir:
            proceedings = Path(temp_dir) / "proceedings.pdf"
            FIXTURE_GENERATOR.build_proceedings_pdf(proceedings)
            with self.assertRaisesRegex(ValueError, "not found"):
                PREPARE.prepare(
                    proceedings,
                    include_text=False,
                    render_dir=None,
                    article_selectors=["Missing paper"],
                )

    def test_cli_no_text_writes_preview_bundle(self) -> None:
        with tempfile.TemporaryDirectory(prefix="paper-to-paradigm-pdf-cli-") as temp_dir:
            output = Path(temp_dir) / "bundle.json"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURE), "--no-text", "-o", str(output)],
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            value = json.loads(output.read_text(encoding="utf-8"))
            self.assertTrue(all("text_preview" in page and "text" not in page for page in value["pages"]))


if __name__ == "__main__":
    unittest.main()
