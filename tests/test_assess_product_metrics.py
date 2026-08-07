import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/top1-design/scripts"))

import assess_product_metrics  # noqa: E402


def record(
    run_id,
    audited=20,
    clean=19,
    released=True,
    wins=7,
    losses=2,
    ties=1,
    baseline=200,
    engine=90,
):
    return {
        "run_id": run_id,
        "eligible": True,
        "audited_units": audited,
        "severe_defect_free_units": clean,
        "release_bar_met": released,
        "blind_comparisons": {
            "taste_engine_wins": wins,
            "control_wins": losses,
            "ties": ties,
        },
        "human_edit_minutes": {
            "baseline": baseline,
            "taste_engine": engine,
        },
    }


class AssessProductMetricsTests(unittest.TestCase):
    def test_all_four_targets_must_pass(self):
        cohort = {
            "schema_version": "1.0",
            "cohort_id": "pilot",
            "records": [
                record("one"),
                record("two", clean=20, wins=8, losses=2, ties=0),
            ],
        }
        result = assess_product_metrics.assess_product_metrics(cohort)
        self.assertTrue(result["product_success"])
        self.assertEqual(result["metrics"]["release_bar_rate"]["value"], 1.0)
        self.assertEqual(
            result["metrics"]["human_edit_time_reduction"]["value"],
            0.55,
        )

    def test_ties_remain_in_blind_preference_denominator(self):
        cohort = {
            "schema_version": "1.0",
            "records": [record("one", wins=7, losses=0, ties=3)],
        }
        result = assess_product_metrics.assess_product_metrics(cohort)
        self.assertEqual(result["metrics"]["blind_preference_rate"]["value"], 0.7)
        self.assertTrue(result["metrics"]["blind_preference_rate"]["passed"])

    def test_one_failed_target_blocks_product_success(self):
        cohort = {
            "schema_version": "1.0",
            "records": [record("one", released=False)],
        }
        result = assess_product_metrics.assess_product_metrics(cohort)
        self.assertFalse(result["product_success"])
        self.assertFalse(result["metrics"]["release_bar_rate"]["passed"])

    def test_clean_units_cannot_exceed_audited_units(self):
        cohort = {
            "schema_version": "1.0",
            "records": [record("one", audited=1, clean=2)],
        }
        with self.assertRaises(assess_product_metrics.MetricsError):
            assess_product_metrics.assess_product_metrics(cohort)


if __name__ == "__main__":
    unittest.main()
