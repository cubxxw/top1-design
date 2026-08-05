import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/top1-design/scripts"))

import rank_candidates  # noqa: E402


class RankCandidatesTests(unittest.TestCase):
    def test_expected_winner_and_reversal_diagnostic(self):
        pairs = [
            {"a": "alpha", "b": "beta", "winner": "alpha", "confidence": 1.0},
            {"a": "beta", "b": "alpha", "winner": "alpha", "confidence": 1.0},
            {"a": "alpha", "b": "gamma", "winner": "alpha", "confidence": 0.8},
            {"a": "gamma", "b": "alpha", "winner": "alpha", "confidence": 0.8},
            {"a": "beta", "b": "gamma", "winner": "beta", "confidence": 0.7},
            {"a": "gamma", "b": "beta", "winner": "beta", "confidence": 0.7},
        ]
        result = rank_candidates.rank_pairs(pairs)
        self.assertEqual(result["ranking"][0]["candidate"], "alpha")
        self.assertEqual(result["diagnostics"]["unreversed_pairs"], [])

    def test_loader_rejects_invalid_winner(self):
        lines = ['{"a":"a","b":"b","winner":"c"}']
        with self.assertRaises(rank_candidates.PairError):
            rank_candidates.load_pairs(lines)


if __name__ == "__main__":
    unittest.main()
