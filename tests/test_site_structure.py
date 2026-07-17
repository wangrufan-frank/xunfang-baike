import json
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


class EquipmentContentTests(unittest.TestCase):
    def test_all_equipment_pages_follow_article_contract(self):
        records = article_records("zhuangbei")
        self.assertEqual(26, len(records))
        for record in records:
            assert_article_contract(self, record)

    def test_three_nine_piece_items_are_not_inventory_articles(self):
        paths = {record["path"] for record in article_records("zhuangbei")}
        self.assertNotIn("zhuangbei/shensuo-jinggun.html", paths)
        self.assertNotIn("zhuangbei/cuilei-pensheqi.html", paths)
        self.assertNotIn("zhuangbei/shoukao.html", paths)


class DutyContentTests(unittest.TestCase):
    def test_all_duty_pages_follow_article_contract(self):
        records = article_records("qinwu")
        self.assertEqual(13, len(records))
        for record in records:
            assert_article_contract(self, record)

    def test_duty_runtime_uses_new_labels(self):
        for path in (ROOT / "qinwu").glob("*.html"):
            html = path.read_text(encoding="utf-8")
            self.assertNotIn("巡防勤务", html)
            self.assertNotIn("群体性事件", html)
            self.assertNotIn("警卫任务", html)


class NavigationStructureTests(unittest.TestCase):
    def test_home_and_nav_use_exact_six_modules(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        nav = (ROOT / "js" / "nav.js").read_text(encoding="utf-8")
        for title in ["装备介绍", "勤务保障", "警务训练", "警情处置", "执法规范", "教育培训"]:
            self.assertIn(title, home)
            self.assertIn(title, nav)
        for old_title in ["巡防勤务", "法条规范", "走访送教", "入门指南"]:
            self.assertNotIn(old_title, home)
            self.assertNotIn(old_title, nav)

    def test_module_indexes_expose_exact_category_anchors(self):
        for module in load_inventory()["modules"]:
            html = (ROOT / module["slug"] / "index.html").read_text(encoding="utf-8")
            for article in module["articles"]:
                self.assertIn(f'id="{article["category_anchor"]}"', html)
                self.assertIn(article["path"].split("/")[-1], html)
