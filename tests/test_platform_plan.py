from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/paper-reconstruction/scripts/validate_platform_plan.py"
SPEC = importlib.util.spec_from_file_location("validate_platform_plan", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import cross-platform validator")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def psychopy_plan() -> dict:
    return {
        "schema_version": "1.0",
        "study_id": "synthetic-behavior-task",
        "study_type": "experiment",
        "implementation_level": "program",
        "target_platform": {
            "name": "PsychoPy",
            "version": "2026.x",
            "selection_source": "user-explicit",
        },
        "runtime_state": "buildable",
        "evidence_sources": [{"type": "paper", "status": "inspected"}],
        "phases": [
            {
                "id": "formal",
                "participant_event": "view stimulus and respond",
                "backend_action": "present randomized trial and log response",
                "component_ids": ["formal-routine", "formal-loop"],
                "output_fields": ["trial_id", "response_raw"],
            }
        ],
        "components": [
            {"id": "formal-routine", "native_type": "Routine", "phase_id": "formal"},
            {"id": "formal-loop", "native_type": "Loop", "phase_id": "formal"},
        ],
        "data_contract": {
            "stable_ids": ["participant_id", "trial_id"],
            "raw_fields": ["response_raw"],
            "derived_fields": [],
            "analysis_fields": ["response_raw"],
        },
        "analysis": {
            "required": True,
            "environment": "Python",
            "selection_source": "user-explicit",
            "artifacts": ["analysis.py", "pyproject.toml"],
        },
        "validation_tests": [
            {"id": "smoke", "target": "formal routine", "pass_criterion": "one synthetic session completes"}
        ],
    }


def longitudinal_plan() -> dict:
    value = psychopy_plan()
    value.update(
        {
            "study_id": "synthetic-three-wave-survey",
            "study_type": "longitudinal-survey",
            "target_platform": {
                "name": "Qualtrics",
                "version": "current export",
                "selection_source": "team-default",
            },
            "phases": [
                {
                    "id": "wave-survey",
                    "participant_event": "complete survey wave",
                    "backend_action": "route blocks and preserve anonymous key",
                    "component_ids": ["survey-block", "survey-flow", "survey-randomizer"],
                    "output_fields": ["participant_key", "wave_id", "item_id", "response_raw", "completion_status", "invitation_status"],
                }
            ],
            "components": [
                {"id": "survey-block", "native_type": "Block", "phase_id": "wave-survey"},
                {"id": "survey-flow", "native_type": "Survey Flow", "phase_id": "wave-survey"},
                {"id": "survey-randomizer", "native_type": "Randomizer", "phase_id": "wave-survey"},
            ],
            "waves": [
                {"id": "wave-1", "target_interval_days": 0},
                {"id": "wave-2", "target_interval_days": 30},
                {"id": "wave-3", "target_interval_days": 60},
            ],
            "data_contract": {
                "stable_ids": ["participant_key", "wave_id", "item_id"],
                "raw_fields": ["response_raw", "completion_status", "invitation_status"],
                "derived_fields": [],
                "analysis_fields": ["response_raw", "wave_id"],
            },
        }
    )
    return value


class PlatformPlanTests(unittest.TestCase):
    def test_accepts_psychopy_with_python_analysis(self) -> None:
        self.assertEqual([], MODULE.validate_plan(psychopy_plan()))

    def test_accepts_longitudinal_qualtrics_plan(self) -> None:
        self.assertEqual([], MODULE.validate_plan(longitudinal_plan()))

    def test_rejects_missing_platform_native_component(self) -> None:
        value = psychopy_plan()
        value["components"][0]["native_type"] = "generic-component"
        errors = MODULE.validate_plan(value)
        self.assertTrue(any("routine" in item.lower() for item in errors))

    def test_rejects_longitudinal_plan_without_wave_key(self) -> None:
        value = longitudinal_plan()
        value["data_contract"]["stable_ids"].remove("wave_id")
        value["data_contract"]["analysis_fields"].remove("wave_id")
        value["phases"][0]["output_fields"].remove("wave_id")
        errors = MODULE.validate_plan(value)
        self.assertTrue(any("wave_id" in item for item in errors))

    def test_rejects_unspecified_analysis_environment(self) -> None:
        value = psychopy_plan()
        value["analysis"]["environment"] = "unspecified"
        errors = MODULE.validate_plan(value)
        self.assertTrue(any("analysis.environment" in item for item in errors))

    def test_runtime_verified_requires_generic_runtime_evidence(self) -> None:
        value = psychopy_plan()
        value["runtime_state"] = "runtime-verified"
        errors = MODULE.validate_plan(value)
        self.assertTrue(any("runtime_evidence" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
