import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "data" / "content-inventory.json"
EXPECTED_COUNTS = {
    "zhuangbei": 26,
    "qinwu": 13,
    "xunlian": 13,
    "jingqing": 5,
    "fagui": 17,
    "zoufang": 13,
}


def load_inventory():
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def article_records(module=None):
    records = [
        article
        for group in load_inventory()["modules"]
        for article in group["articles"]
    ]
    return [record for record in records if record["module"] == module] if module else records


def assert_article_contract(testcase, record):
    path = ROOT / record["path"]
    testcase.assertTrue(path.is_file(), record["path"])
    html = path.read_text(encoding="utf-8")
    testcase.assertIn(f'data-module="{record["module"]}"', html)
    testcase.assertIn(f'data-category="{record["category"]}"', html)
    testcase.assertIn(record["title"], html)
    testcase.assertIn("article-summary", html)
    testcase.assertIn("source-list", html)
    testcase.assertIn("related-links", html)
    testcase.assertIn("page-nav", html)


class ContentInventoryTests(unittest.TestCase):
    def test_inventory_has_exact_module_and_article_counts(self):
        inventory = load_inventory()
        counts = {
            module["slug"]: len(module["articles"])
            for module in inventory["modules"]
        }
        self.assertEqual(EXPECTED_COUNTS, counts)
        paths = [record["path"] for record in article_records()]
        self.assertEqual(87, len(paths))
        self.assertEqual(87, len(set(paths)))

    def test_inventory_records_have_required_fields(self):
        required = {
            "module", "module_title", "category", "category_anchor",
            "title", "slug", "path", "source_files", "public_sources",
            "images", "related_pages",
        }
        for record in article_records():
            self.assertEqual(set(), required.difference(record), record["path"])
            self.assertRegex(record["path"], r"^[a-z0-9-]+/[a-z0-9-]+\.html$")
            self.assertTrue(
                record["source_files"] or record["public_sources"],
                record["path"],
            )
