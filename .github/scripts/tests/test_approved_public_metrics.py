"""Approved copy must not permit a changed statistic or a wider exemption."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHECKS = ROOT / ".github/site-checks"
sys.path.insert(0, str(CHECKS))
from approved_claims import REGISTRY, approved, load_registry

spec = importlib.util.spec_from_file_location("safety_claims", CHECKS / "_safety_claims.py")
safety = importlib.util.module_from_spec(spec)
spec.loader.exec_module(safety)


class ApprovedPublicMetricsTests(unittest.TestCase):
    def setUp(self):
        self.rows = load_registry(ROOT)
        self.emr = next(r for r in self.rows if r["kind"] == "safety:EMR")

    def test_current_copy_is_bound_and_safety_copy_is_cleared(self):
        self.assertEqual(len(self.rows), 7)
        safety.APPROVAL_USES.clear()
        for path in ("index.html", "about.html", "qualifications.html"):
            self.assertEqual(safety.scan(str(ROOT / path)), [])

    def test_changed_number_is_not_approved(self):
        text = self.emr["source_text"].replace("1.0", "0.8")
        self.assertFalse(approved(self.rows, self.emr["kind"], self.emr["path"], text, {}))

    def test_same_copy_on_another_page_is_not_approved(self):
        self.assertFalse(approved(self.rows, self.emr["kind"], "new.html", self.emr["source_text"], {}))

    def test_duplicate_occurrence_is_not_approved(self):
        used = {}
        self.assertTrue(approved(self.rows, self.emr["kind"], self.emr["path"], self.emr["source_text"], used))
        self.assertFalse(approved(self.rows, self.emr["kind"], self.emr["path"], self.emr["source_text"], used))

    def test_other_safety_statistics_still_fail_detection(self):
        self.assertTrue(list(safety.candidates("ACG reports 0 OSHA recordable incidents.")))
        self.assertTrue(list(safety.candidates("ACG reports an EMR of 0.8, three-year average.")))
        self.assertFalse(approved(self.rows, "safety:recordable", self.emr["path"], self.emr["source_text"], {}))

    def test_missing_registry_grants_no_exception(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(load_registry(d), [])

    def test_modified_approval_source_fails_closed(self):
        data = json.loads((ROOT / REGISTRY).read_text())
        data["approved_source_surfaces"][0]["source_text"] += " changed"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / REGISTRY
            p.parent.mkdir(parents=True)
            p.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                load_registry(d)

    def test_unapproved_volume_copy_does_not_match(self):
        row = next(r for r in self.rows if r["kind"] == "volume:350+")
        self.assertFalse(approved(self.rows, row["kind"], row["path"], row["source_text"].replace("350+", "500+"), {}))
