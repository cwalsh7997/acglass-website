"""The hygiene cap must preserve exact approved copy and reject other debt."""
import importlib.util
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("metadata_limits", ROOT / ".github/site-checks/_metadata_limits.py")
limits = importlib.util.module_from_spec(spec)
spec.loader.exec_module(limits)


class ApprovedDescriptionTests(unittest.TestCase):
    def approved(self):
        source = (ROOT / "euro-wall.html").read_text()
        return re.search(r'<meta name="description" content="([^"]+)"', source)[1]

    def test_existing_approved_sentence_is_preserved(self):
        description = self.approved()
        self.assertEqual(len(description), 158)
        self.assertFalse(limits.description_over_limit("euro-wall.html", description))

    def test_one_character_change_loses_the_exception(self):
        self.assertTrue(limits.description_over_limit("euro-wall.html", self.approved() + "."))

    def test_exception_cannot_be_reused_on_another_page(self):
        self.assertTrue(limits.description_over_limit("unapproved.html", self.approved()))

    def test_normal_cap_still_applies(self):
        self.assertFalse(limits.description_over_limit("new.html", "a" * 155))
        self.assertTrue(limits.description_over_limit("new.html", "a" * 156))
