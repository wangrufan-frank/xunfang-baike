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

DISPLAY_MODULES = [
    ("jingqing", "警情处置"),
    ("qinwu", "勤务须知"),
    ("fagui", "执法规范"),
    ("zhuangbei", "装备操作"),
    ("zoufang", "教育学习"),
    ("xunlian", "实战训练"),
]


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
    testcase.assertIn("public-source-index", html)
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


class TrainingContentTests(unittest.TestCase):
    def test_all_training_pages_follow_article_contract(self):
        records = article_records("xunlian")
        self.assertEqual(13, len(records))
        self.assertEqual(7, sum(record["category"] == "单兵技能训练" for record in records))
        self.assertEqual(6, sum(record["category"] == "小组协同训练" for record in records))
        for record in records:
            assert_article_contract(self, record)


class IncidentContentTests(unittest.TestCase):
    def test_all_incident_pages_follow_article_contract(self):
        records = article_records("jingqing")
        self.assertEqual(5, len(records))
        for record in records:
            assert_article_contract(self, record)
            html = (ROOT / record["path"]).read_text(encoding="utf-8")
            for heading in ["任务确认", "风险分析", "到场", "人员保护", "法律边界", "记录报告", "禁止性事项"]:
                self.assertIn(heading, html, record["path"])


class LegalContentTests(unittest.TestCase):
    def test_all_legal_pages_follow_article_contract(self):
        records = article_records("fagui")
        self.assertEqual(17, len(records))
        for record in records:
            assert_article_contract(self, record)

    def test_law_library_pages_show_effective_date_and_official_link(self):
        records = [record for record in article_records("fagui") if record["category"] == "法律法规库"]
        self.assertEqual(7, len(records))
        for record in records:
            html = (ROOT / record["path"]).read_text(encoding="utf-8")
            # Single-statute pages show 施行日期; index/compilation pages use
            # 核验日期 in the version-meta-card instead.
            has_effective_date = "施行日期" in html or "核验日期" in html
            self.assertTrue(has_effective_date,
                            f'{record["path"]} missing effective/review date marker')
            self.assertRegex(html, r'https://[^"\s]+')


class EducationContentTests(unittest.TestCase):
    def test_all_education_pages_follow_article_contract(self):
        records = article_records("zoufang")
        self.assertEqual(13, len(records))
        for record in records:
            assert_article_contract(self, record)

    def test_onboarding_module_is_removed_from_web_runtime(self):
        self.assertFalse((ROOT / "rumen").exists())
        self.assertFalse((ROOT / ".generated-learning-pages.json").exists())
        for path in [ROOT / "index.html", ROOT / "js" / "nav.js", ROOT / "search-index.json"]:
            self.assertNotIn("rumen", path.read_text(encoding="utf-8"))


class MediaAndCrossReferenceTests(unittest.TestCase):
    def test_inventory_images_and_related_pages_exist(self):
        valid_paths = {record["path"] for record in article_records()}
        for record in article_records():
            for image in record["images"]:
                self.assertTrue((ROOT / image["path"]).is_file(), image["path"])
                self.assertTrue(image["alt"].strip(), image["path"])
                self.assertTrue(image["source"].strip(), image["path"])
            for related in record["related_pages"]:
                self.assertIn(related, valid_paths, (record["path"], related))


class NavigationStructureTests(unittest.TestCase):
    def test_home_and_nav_use_exact_six_modules_in_display_order(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        nav = (ROOT / "js" / "nav.js").read_text(encoding="utf-8")
        expected_titles = [title for _, title in DISPLAY_MODULES]
        expected_paths = [f"{slug}/index.html" for slug, _ in DISPLAY_MODULES]
        for source in (home, nav):
            self.assertEqual(
                sorted(source.index(title) for title in expected_titles),
                [source.index(title) for title in expected_titles],
            )
            self.assertEqual(
                sorted(source.index(path) for path in expected_paths),
                [source.index(path) for path in expected_paths],
            )

        for old_title in [
            "装备介绍", "勤务保障", "警务训练", "教育培训",
            "巡防勤务", "法条规范", "走访送教", "入门指南",
        ]:
            self.assertNotIn(old_title, home)
            self.assertNotIn(old_title, nav)

        monthly_position = nav.index("本月精选")
        self.assertGreater(monthly_position, nav.index("实战训练"))
        self.assertIn("special: true", nav)

    def test_module_indexes_expose_exact_category_anchors(self):
        for module in load_inventory()["modules"]:
            html = (ROOT / module["slug"] / "index.html").read_text(encoding="utf-8")
            for article in module["articles"]:
                self.assertIn(f'id="{article["category_anchor"]}"', html)
                self.assertIn(article["path"].split("/")[-1], html)
