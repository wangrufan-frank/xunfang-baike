import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "data" / "content-inventory.json"
EXPECTED_COUNTS = {
    "zhuangbei": 28,
    "qinwu": 13,
    "xunlian": 15,
    "jingqing": 6,
    "fagui": 17,
    "zoufang": 14,
}

DISPLAY_MODULES = [
    ("jingqing", "警情处置"),
    ("qinwu", "勤务须知"),
    ("fagui", "执法规范"),
    ("zhuangbei", "装备操作"),
    ("zoufang", "教育学习"),
    ("xunlian", "实战训练"),
]

RENAMED_MODULES = {
    "qinwu": ("勤务保障", "勤务须知"),
    "zhuangbei": ("装备介绍", "装备操作"),
    "zoufang": ("教育培训", "教育学习"),
    "xunlian": ("警务训练", "实战训练"),
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
        self.assertEqual(93, len(paths))
        self.assertEqual(93, len(set(paths)))

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
        self.assertEqual(28, len(records))
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
        self.assertEqual(15, len(records))
        self.assertEqual(7, sum(record["category"] == "单兵技能训练" for record in records))
        self.assertEqual(6, sum(record["category"] == "小组协同训练" for record in records))
        self.assertEqual(2, sum(record["category"] == "伤员救助" for record in records))
        for record in records:
            assert_article_contract(self, record)


class IncidentContentTests(unittest.TestCase):
    def test_all_incident_pages_follow_article_contract(self):
        records = article_records("jingqing")
        self.assertEqual(6, len(records))
        for record in records:
            assert_article_contract(self, record)
            html = (ROOT / record["path"]).read_text(encoding="utf-8")
            if record["slug"] == "jiuzhu-lei-jingqing-chuzhi":
                # 处置流程文章采用环节式结构，不套用基础处置模板
                for heading in ["处置原则", "舆情管控", "现场评估", "呼救", "先期救助", "现场保护", "交接记录"]:
                    self.assertIn(heading, html, record["path"])
                continue
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
        self.assertEqual(14, len(records))
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


class HostingConfigTests(unittest.TestCase):
    def test_github_pages_bypasses_jekyll_for_static_site(self):
        marker = ROOT / ".nojekyll"
        self.assertTrue(marker.is_file(), ".nojekyll must exist at the site root")
        self.assertEqual("", marker.read_text(encoding="utf-8").strip())


class NavigationStructureTests(unittest.TestCase):
    def test_home_exposes_two_priority_learning_links(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="home-priority-links"', home)
        self.assertIn('href="zoufang/neiwu-tiaoling.html"', home)
        self.assertIn('href="zoufang/tineng-kaohe.html"', home)
        self.assertEqual(2, home.count('class="home-priority-card '))

    def test_navigation_starts_with_direct_home_link(self):
        nav = (ROOT / "js" / "nav.js").read_text(encoding="utf-8")
        home = "{ name: '首页', path: 'index.html', emoji: '🏠' }"
        self.assertIn(home, nav)
        self.assertLess(nav.index(home), nav.index("{ name: '更新记录'"))
        self.assertIn("if (moduleDir === 'index.html')", nav)

    def test_monthly_issue_keeps_july_archive_and_selects_august(self):
        data = (ROOT / "meiyueyixue" / "data.js").read_text(encoding="utf-8")
        current = (ROOT / "meiyueyixue" / "index.html").read_text(encoding="utf-8")
        archive = ROOT / "meiyueyixue" / "2026-07.html"

        self.assertIn('current: "2026-08"', data)
        self.assertIn('"2026-07"', data)
        self.assertIn('"2026-08"', data)
        self.assertIn('2026-07.html', data)
        self.assertTrue(archive.is_file())
        self.assertIn('data-monthly-issue="2026-08"', current)
        self.assertIn('汛期高温叠加：巡防现场风险识别', current)
        self.assertIn('data-monthly-issue="2026-07"', archive.read_text(encoding="utf-8"))

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

    def test_module_display_names_are_consistent_across_runtime_sources(self):
        inventory = load_inventory()
        inventory_by_slug = {module["slug"]: module for module in inventory["modules"]}
        search_records = json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
        search_fallbacks = (ROOT / "js" / "search.js").read_text(encoding="utf-8")

        for slug, title in DISPLAY_MODULES:
            module = inventory_by_slug[slug]
            self.assertEqual(title, module["title"])
            self.assertTrue(all(article["module_title"] == title for article in module["articles"]))
            self.assertTrue(all(
                record["module"] == title
                for record in search_records
                if record["path"].startswith(f"{slug}/")
            ))
            self.assertIn(f"'{slug}': '{title}'", search_fallbacks)

            index_html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
            self.assertIn(f"<title>{title} — 巡防百科</title>", index_html)
            self.assertIn(f'<span class="current">{title}</span>', index_html)
            self.assertIn(title, index_html)

    def test_old_names_are_absent_from_module_label_contexts(self):
        explicit_reference_patterns = [
            "{old}模块",
            "返回{old}",
            "进入{old}",
            ">{old}<",
        ]
        runtime_pages = [
            path
            for slug, _ in DISPLAY_MODULES
            for path in (ROOT / slug).glob("*.html")
        ]
        runtime_pages.extend([ROOT / "index.html", ROOT / "search.html"])

        for path in runtime_pages:
            text = path.read_text(encoding="utf-8")
            for old, _ in RENAMED_MODULES.values():
                for pattern in explicit_reference_patterns:
                    self.assertNotIn(pattern.format(old=old), text, str(path))

    def test_verbatim_legal_education_training_quote_is_preserved(self):
        legal_documents = (ROOT / "data" / "legal-documents.json").read_text(encoding="utf-8")
        legal_cards = (ROOT / "data" / "legal-basis-cards.json").read_text(encoding="utf-8")
        statutory_text = "警察业务等教育培训"
        self.assertIn(statutory_text, legal_documents)
        self.assertIn(statutory_text, legal_cards)
