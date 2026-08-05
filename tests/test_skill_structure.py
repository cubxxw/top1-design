import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/top1-design/SKILL.md"


class SkillStructureTests(unittest.TestCase):
    def test_frontmatter_and_no_placeholders(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: top1-design$")
        self.assertRegex(frontmatter, r"(?m)^description: .{100,}$")
        self.assertNotIn("TODO", text)

    def test_referenced_local_files_exist(self):
        text = SKILL.read_text(encoding="utf-8")
        refs = re.findall(r"`(references/[^`]+)`", text)
        for relative in refs:
            self.assertTrue((SKILL.parent / relative).exists(), relative)


if __name__ == "__main__":
    unittest.main()
