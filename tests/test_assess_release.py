import sys
import unittest
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/top1-design/scripts"))

import assess_release  # noqa: E402
import score_design  # noqa: E402


def evaluation():
    return {
        "schema_version": "1.0",
        "run_id": "test-run",
        "mode": "persuade",
        "required_depth": 0,
        "threshold": 95,
        "required_hard_gates": ["functional", "accessibility", "responsive"],
        "nodes": [
            {
                "id": "root",
                "parent_id": None,
                "depth": 0,
                "confidence": 1,
                "scores": {
                    name: 97 for name in score_design.MODE_WEIGHTS["persuade"]
                },
                "hard_gates": {
                    "functional": True,
                    "accessibility": True,
                    "responsive": True,
                },
                "evidence": ["target.png"],
            }
        ],
    }


def check(check_id, family, **dimensions):
    return {
        "id": check_id,
        "family": family,
        "status": "pass",
        "required": True,
        "evidence": [f"{check_id}.json"],
        **dimensions,
    }


def manifest():
    return {
        "schema_version": "1.0",
        "run_id": "test-run",
        "evaluation": evaluation(),
        "coverage": {
            "required_check_families": [
                "visual",
                "interaction",
                "responsive",
                "accessibility",
                "functional",
            ],
            "required_viewports": ["desktop", "mobile"],
            "required_flows": ["primary"],
            "required_states": ["default", "focus"],
            "required_accessibility_methods": ["automated", "keyboard"],
        },
        "checks": [
            check("visual", "visual"),
            check("default", "interaction", state="default"),
            check("focus", "interaction", state="focus"),
            check("desktop", "responsive", viewport="desktop"),
            check("mobile", "responsive", viewport="mobile"),
            check("axe", "accessibility", method="automated"),
            check("keyboard", "accessibility", method="keyboard"),
            check("primary", "functional", flow="primary"),
        ],
        "defects": [],
        "change_control": {
            "within_authority": True,
            "tests_passed": True,
            "blast_radius_reviewed": True,
            "rollback_ready": True,
        },
    }


class AssessReleaseTests(unittest.TestCase):
    def test_complete_evidence_meets_release_bar(self):
        result = assess_release.assess_release(manifest())
        self.assertTrue(result["release_bar_met"])
        self.assertEqual(result["release_status"], "release_candidate")

    def test_unresolved_severe_defect_blocks_even_if_accepted(self):
        candidate = manifest()
        candidate["defects"] = [
            {
                "id": "RESP-001",
                "family": "responsive",
                "severity": "severe",
                "status": "accepted_risk",
                "evidence": ["mobile.png"],
            }
        ]
        result = assess_release.assess_release(candidate)
        self.assertFalse(result["release_bar_met"])
        self.assertIn("severe_defects", result["blocking_reasons"][0])

    def test_missing_required_viewport_blocks(self):
        candidate = manifest()
        candidate["checks"] = [
            item for item in candidate["checks"] if item["id"] != "mobile"
        ]
        result = assess_release.assess_release(candidate)
        self.assertFalse(result["release_bar_met"])
        responsive = next(
            gate
            for gate in result["gate_results"]
            if gate["gate"] == "responsive_evidence"
        )
        self.assertFalse(responsive["passed"])
        self.assertIn("viewport=mobile", " ".join(responsive["reasons"]))

    def test_failed_recursive_score_blocks_release(self):
        candidate = deepcopy(manifest())
        candidate["evaluation"]["nodes"][0]["scores"]["goal_fit"] = 20
        result = assess_release.assess_release(candidate)
        self.assertFalse(result["release_bar_met"])
        self.assertEqual(result["score_release_status"], "not_releasable")


if __name__ == "__main__":
    unittest.main()
