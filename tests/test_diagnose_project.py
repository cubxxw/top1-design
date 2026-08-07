import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/top1-design/scripts"))

import diagnose_project  # noqa: E402


class DiagnoseProjectTests(unittest.TestCase):
    def make_project(self, package):
        temporary = tempfile.TemporaryDirectory()
        project = Path(temporary.name)
        (project / "package.json").write_text(
            json.dumps(package),
            encoding="utf-8",
        )
        (project / "src/components").mkdir(parents=True)
        (project / "src/components/Button.tsx").write_text(
            "export function Button() { return null }\n",
            encoding="utf-8",
        )
        self.addCleanup(temporary.cleanup)
        return project

    def test_declared_rescue_next_tailwind_is_supported(self):
        project = self.make_project(
            {
                "scripts": {"dev": "next dev", "build": "next build", "test": "test"},
                "dependencies": {
                    "next": "1",
                    "react": "1",
                    "tailwindcss": "1",
                },
            }
        )
        result = diagnose_project.diagnose(
            project,
            profile={
                "schema_version": "1.0",
                "declared_stage": "middle",
                "runtime": {"start_verified": True},
            },
        )
        self.assertEqual(result["strategy"]["mode"], "rescue")
        self.assertEqual(
            result["capability"]["automatic_modification"]["status"],
            "supported",
        )
        self.assertEqual(result["change_policy"]["recommended_level"], 2)
        self.assertEqual(result["change_policy"]["maximum_without_new_authority"], 4)

    def test_unknown_stack_is_review_only_but_browser_review_can_be_ready(self):
        project = self.make_project({"scripts": {"build": "echo build"}})
        result = diagnose_project.diagnose(
            project,
            profile={"schema_version": "1.0", "declared_stage": "early"},
            target_url="http://localhost:3000/",
        )
        self.assertEqual(result["capability"]["review"]["status"], "ready")
        self.assertEqual(
            result["capability"]["automatic_modification"]["status"],
            "review_only",
        )
        self.assertEqual(result["change_policy"]["recommended_level"], 0)
        self.assertEqual(result["change_policy"]["maximum_without_new_authority"], 0)

    def test_conditional_adapter_caps_change_level(self):
        project = self.make_project(
            {
                "scripts": {"dev": "vite", "build": "vite build"},
                "dependencies": {"react": "1"},
            }
        )
        result = diagnose_project.diagnose(
            project,
            profile={"schema_version": "1.0", "declared_stage": "early"},
            target_url="http://localhost:5173/",
        )
        self.assertEqual(
            result["capability"]["automatic_modification"]["status"],
            "conditional",
        )
        self.assertEqual(result["change_policy"]["recommended_level"], 1)
        self.assertEqual(result["change_policy"]["maximum_without_new_authority"], 2)


if __name__ == "__main__":
    unittest.main()
