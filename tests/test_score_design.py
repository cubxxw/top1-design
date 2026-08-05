import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/top1-design/scripts"))

import score_design  # noqa: E402


def node(
    node_id="root",
    depth=0,
    confidence=1.0,
    value=96,
    gates=None,
    evidence=None,
    parent_id=None,
):
    return {
        "id": node_id,
        "parent_id": parent_id,
        "scope": node_id,
        "depth": depth,
        "required": True,
        "confidence": confidence,
        "scores": {name: value for name in score_design.MODE_WEIGHTS["persuade"]},
        "hard_gates": gates or {"functional": True},
        "evidence": evidence or ["capture.png"],
    }


def report(nodes, required_depth=0, threshold=95):
    return {
        "schema_version": "1.0",
        "mode": "persuade",
        "required_depth": required_depth,
        "threshold": threshold,
        "required_hard_gates": ["functional"],
        "nodes": nodes,
    }


class ScoreDesignTests(unittest.TestCase):
    def test_high_parent_promotes_when_depth_remains(self):
        result = score_design.score_report(report([node()], required_depth=2))
        self.assertEqual(result["nodes"][0]["status"], "promote")
        self.assertEqual(result["release_status"], "not_releasable")

    def test_failed_gate_blocks_high_score(self):
        target = node(gates={"functional": False})
        result = score_design.score_report(report([target]))
        self.assertEqual(result["nodes"][0]["status"], "blocked")
        self.assertEqual(result["release_status"], "not_releasable")

    def test_confidence_caps_score(self):
        target = node(confidence=0.5, value=100)
        result = score_design.score_report(report([target], threshold=95))
        self.assertEqual(result["nodes"][0]["effective_score"], 90)
        self.assertEqual(result["nodes"][0]["status"], "repair")

    def test_all_required_terminal_children_control_release(self):
        nodes = [
            node("root", depth=0),
            node("left", depth=1, parent_id="root"),
            node("right", depth=1, parent_id="root"),
        ]
        result = score_design.score_report(report(nodes, required_depth=1))
        self.assertEqual(set(result["required_terminal_nodes"]), {"left", "right"})
        self.assertEqual(result["release_status"], "release_candidate")

    def test_missing_metric_is_invalid(self):
        target = node()
        del target["scores"]["copy"]
        with self.assertRaises(score_design.EvaluationError):
            score_design.score_report(report([target]))


if __name__ == "__main__":
    unittest.main()
