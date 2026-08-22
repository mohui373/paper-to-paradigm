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
