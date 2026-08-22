from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/paper-reconstruction/scripts/audit_replication_bundle.py"
STARTER = ROOT / "skills/paper-reconstruction/assets/eprime-starter"

SPEC = importlib.util.spec_from_file_location("audit_replication_bundle", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import semantic audit script")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SemanticAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="paper-to-paradigm-test-")
        self.bundle = Path(self.temp.name) / "bundle"
        shutil.copytree(STARTER, self.bundle)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def manifest(self) -> dict:
        return json.loads((self.bundle / "bundle_manifest.json").read_text(encoding="utf-8"))

    def save_manifest(self, value: dict) -> None:
        (self.bundle / "bundle_manifest.json").write_text(
            json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def test_valid_starter(self) -> None:
        result = MODULE.audit_bundle(self.bundle)
        self.assertEqual([], result.errors)

    def test_rejects_undefined_proc_call(self) -> None:
        value = self.manifest()
        value["execution"]["lists"][0]["calls"] = ["UndefinedProc"]
        self.save_manifest(value)
        result = MODULE.audit_bundle(self.bundle)
        self.assertTrue(any("UndefinedProc" in item for item in result.errors))

    def test_rejects_timeline_drift(self) -> None:
        value = self.manifest()
        value["execution"]["procedures"][0]["timeline"] = ["Welcome", "Goodbye"]
        self.save_manifest(value)
        result = MODULE.audit_bundle(self.bundle)
        self.assertTrue(any("timeline mismatch" in item for item in result.errors))

    def test_rejects_analysis_field_missing_from_dictionary(self) -> None:
        path = self.bundle / "analysis_contract.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value["required_fields"].append("MissingAnalysisField")
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
        result = MODULE.audit_bundle(self.bundle)
        self.assertTrue(any("MissingAnalysisField" in item for item in result.errors))

    def test_rejects_ambiguous_parallel_relation(self) -> None:
        value = self.manifest()
        value["execution"]["relations"][0]["type"] = "parallel"
        self.save_manifest(value)
        result = MODULE.audit_bundle(self.bundle)
        self.assertTrue(any("ambiguous 'parallel'" in item for item in result.errors))

    def test_runtime_verified_requires_runtime_artifacts(self) -> None:
        value = self.manifest()
        value["platform"]["runtime_state"] = "runtime-verified"
        self.save_manifest(value)
        result = MODULE.audit_bundle(self.bundle)
        self.assertTrue(any("runtime-verified bundle missing" in item for item in result.errors))


if __name__ == "__main__":
    unittest.main()
