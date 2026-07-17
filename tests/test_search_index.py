import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_search_index", ROOT / "tools" / "build_search_index.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SearchIndexTests(unittest.TestCase):
    def test_index_matches_all_inventory_articles(self):
        records = MODULE.build_index(ROOT)
        self.assertEqual(87, len(records))
        self.assertEqual(87, len({record["path"] for record in records}))
        self.assertFalse(any(record["path"].startswith("rumen/") for record in records))
        self.assertEqual([], MODULE.check_index(ROOT, records))


if __name__ == "__main__":
    unittest.main()
