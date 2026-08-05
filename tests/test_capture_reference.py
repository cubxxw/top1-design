import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/top1-design/scripts"))

import capture_reference  # noqa: E402


class CaptureReferenceTests(unittest.TestCase):
    def test_safe_slug(self):
        self.assertEqual(capture_reference.safe_slug("Granola Home!"), "granola-home")
        with self.assertRaises(ValueError):
            capture_reference.safe_slug("---")

    def test_card_separates_observation_from_interpretation(self):
        card = capture_reference.build_card(
            slug="granola-home",
            requested_url="https://www.granola.ai/",
            captured_at="2026-08-05T00:00:00+00:00",
            page={
                "url": "https://www.granola.ai/",
                "title": "Granola",
                "viewport": {"width": 1280, "height": 720},
            },
            screenshot_path=Path("capture.png"),
            session="test",
            role="positive-reference",
        )
        self.assertEqual(card["observed"], [])
        self.assertEqual(card["interpretation"], [])
        self.assertEqual(card["rights"], "link-only")


if __name__ == "__main__":
    unittest.main()
