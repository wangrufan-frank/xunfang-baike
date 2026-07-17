import copy
import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "learning_modules.py"
SPEC = importlib.util.spec_from_file_location("learning_modules", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def valid_source():
    return {
        "source_id": "official-example",
        "title": "公开规范",
        "publisher": "发布机关",
        "platform": "政府网站",
        "published_at": "2024-01-02",
        "url": "https://example.gov.cn/rule.html",
    }


def valid_article(slug="01-example"):
    return {
        "slug": slug,
        "number": "01",
        "title": "第一课",
        "stage": 1,
        "summary": "了解基本要求。",
        "reading_minutes": 5,
        "tags": ["入门"],
        "keywords": ["规范", "边界"],
        "updated_at": "2026-07-16",
        "source_ids": ["official-example"],
        "sections": [
            {"title": "学习目标", "lead": "先理解原则。", "body": "依法、规范、协作。"}
        ],
        "quiz": {
            "question": "遇到不明确事项应当如何处理？",
            "options": ["自行扩大权限", "及时请示"],
            "answer_index": 1,
            "explanation": "不确定时应当依规请示。",
        },
    }


def valid_module(article=None, slug="rumen"):
    return {
        "slug": slug,
        "title": "巡防入门指南",
        "description": "五阶段基础学习。",
        "articles": [article or valid_article()],
    }


def valid_catalog():
    return {
        "version": 1,
        "verified_at": "2026-07-16",
        "sources": [valid_source()],
        "modules": [valid_module()],
    }


class LearningCatalogValidationTests(unittest.TestCase):
    def assert_invalid(self, catalog, fragment):
        errors = MODULE.validate_catalog(catalog)
        self.assertTrue(errors, "catalog should be invalid")
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_catalog_has_no_errors(self):
        self.assertEqual([], MODULE.validate_catalog(valid_catalog()))

    def test_load_catalog_reads_utf8_json_object(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(json.dumps(valid_catalog(), ensure_ascii=False), encoding="utf-8")
            self.assertEqual(valid_catalog(), MODULE.load_catalog(path))

    def test_load_catalog_rejects_duplicate_keys_and_nonstandard_constants(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            for payload in ('{"version": 1, "version": 2}', '{"version": NaN}'):
                with self.subTest(payload=payload):
                    path.write_text(payload, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        MODULE.load_catalog(path)

    def test_rejects_missing_required_top_level_field(self):
        catalog = valid_catalog()
        del catalog["verified_at"]
        self.assert_invalid(catalog, "verified_at")

    def test_rejects_unknown_and_missing_article_fields(self):
        catalog = valid_catalog()
        del catalog["modules"][0]["articles"][0]["summary"]
        catalog["modules"][0]["articles"][0]["html"] = "<b>bad</b>"
        self.assert_invalid(catalog, "article fields")

    def test_rejects_non_https_source(self):
        catalog = valid_catalog()
        catalog["sources"][0]["url"] = "http://example.gov.cn/rule.html"
        self.assert_invalid(catalog, "HTTPS")

    def test_validation_reports_non_string_slugs_and_malformed_urls(self):
        cases = (
            (lambda c: c["modules"][0].update(slug=[]), "module slug"),
            (lambda c: c["modules"][0]["articles"][0].update(slug=7), "safe lowercase slug"),
            (lambda c: c["sources"][0].update(url=None), "HTTPS"),
            (lambda c: c["sources"][0].update(url="https://[::1"), "HTTPS"),
            (lambda c: c["sources"][0].update(url="https://example.gov.cn:bad/rule"), "HTTPS"),
            (lambda c: c["sources"][0].update(url=json.loads('"https://\\ud800"')), "HTTPS"),
        )
        for mutate, fragment in cases:
            with self.subTest(fragment=fragment):
                catalog = valid_catalog()
                mutate(catalog)
                self.assert_invalid(catalog, fragment)

    def test_rejects_duplicate_source_ids(self):
        catalog = valid_catalog()
        catalog["sources"].append(copy.deepcopy(catalog["sources"][0]))
        self.assert_invalid(catalog, "duplicate source_id")

    def test_rejects_duplicate_module_slugs(self):
        catalog = valid_catalog()
        catalog["modules"].append(valid_module(slug="rumen"))
        self.assert_invalid(catalog, "duplicate module slug")

    def test_rejects_duplicate_article_slugs_across_modules(self):
        catalog = valid_catalog()
        catalog["modules"].append(valid_module(slug="kaohe"))
        self.assert_invalid(catalog, "duplicate article slug")

    def test_rejects_dangling_source_ids(self):
        catalog = valid_catalog()
        catalog["modules"][0]["articles"][0]["source_ids"] = ["missing"]
        self.assert_invalid(catalog, "unknown source_id")

    def test_rejects_invalid_iso_dates_but_allows_absent_publication_date(self):
        catalog = valid_catalog()
        catalog["verified_at"] = "2026-02-30"
        catalog["modules"][0]["articles"][0]["updated_at"] = "16/07/2026"
        self.assert_invalid(catalog, "date")
        catalog = valid_catalog()
        catalog["sources"][0]["published_at"] = None
        self.assertEqual([], MODULE.validate_catalog(catalog))

    def test_rejects_empty_sections(self):
        catalog = valid_catalog()
        catalog["modules"][0]["articles"][0]["sections"] = []
        self.assert_invalid(catalog, "sections")

    def test_rejects_raw_html_in_any_content_string(self):
        for mutate in (
            lambda c: c["modules"][0].update(title="<em>bad</em>"),
            lambda c: c["modules"][0]["articles"][0]["sections"][0].update(body="text <b>bad</b>"),
            lambda c: c["sources"][0].update(title="<script>bad</script>"),
        ):
            with self.subTest(mutate=mutate):
                catalog = valid_catalog()
                mutate(catalog)
                self.assert_invalid(catalog, "raw HTML")

    def test_rejects_raw_html_comments_declarations_and_processing_instructions(self):
        for payload in (
            "before <!-- hidden --> after",
            "<!DOCTYPE html>",
            "<?xml version='1.0'?>",
            "<!ENTITY example 'value'>",
        ):
            with self.subTest(payload=payload):
                catalog = valid_catalog()
                catalog["modules"][0]["articles"][0]["summary"] = payload
                self.assert_invalid(catalog, "raw HTML")

    def test_rejects_unknown_module_slug(self):
        catalog = valid_catalog()
        catalog["modules"][0]["slug"] = "secret"
        self.assert_invalid(catalog, "module slug")


class LearningCatalogInventoryTests(unittest.TestCase):
    def test_onboarding_has_five_ordered_stages(self):
        catalog = MODULE.load_catalog(ROOT / "data" / "learning-modules.json")
        module = next(module for module in catalog["modules"] if module["slug"] == "rumen")
        articles = module["articles"]

        self.assertEqual(5, len(articles))
        self.assertEqual(["01", "02", "03", "04", "05"], [article["number"] for article in articles])
        self.assertEqual([1, 2, 3, 4, 5], [article["stage"] for article in articles])
        self.assertEqual(
            [
                "01-gangwei-renshi",
                "02-zhize-bianjie",
                "03-jilv-baomi",
                "04-qinwu-goutong",
                "05-fuxi-zice",
            ],
            [article["slug"] for article in articles],
        )
        self.assertEqual(
            [
                "认识巡防岗位",
                "明确职责与权限边界",
                "纪律要求与保密意识",
                "勤务基础与群众沟通",
                "综合复习与入门自测",
            ],
            [article["title"] for article in articles],
        )
        expected_sections = ["学习目标", "核心要点", "常见误区", "请示与正式培训边界"]
        for index, article in enumerate(articles):
            with self.subTest(slug=article["slug"]):
                self.assertTrue(article["quiz"])
                self.assertTrue(article["source_ids"])
                self.assertEqual(expected_sections, [section["title"] for section in article["sections"]])
                previous = articles[index - 1] if index else None
                next_ = articles[index + 1] if index + 1 < len(articles) else None
                html = MODULE.render_article(
                    module,
                    article,
                    previous,
                    next_,
                    sources=catalog["sources"],
                    verified_at=catalog["verified_at"],
                )
                if previous:
                    self.assertIn(f'href="{previous["slug"]}.html"', html)
                else:
                    self.assertIn(
                        '<span class="previous disabled">已经是第一课</span>',
                        html,
                    )
                if next_:
                    self.assertIn(f'href="{next_["slug"]}.html"', html)
                else:
                    self.assertIn(
                        '<span class="next disabled">已经是最后一课</span>',
                        html,
                    )

        review_body = articles[-1]["sections"][1]["body"]
        self.assertEqual(5, review_body.count("理由："))


class LearningRendererTests(unittest.TestCase):
    def setUp(self):
        self.source = valid_source()
        self.module = valid_module()

    def render_article(self, article, previous=None, next_=None):
        return MODULE.render_article(
            self.module,
            article,
            previous,
            next_,
            sources=[self.source],
            verified_at="2026-07-16",
        )

    def test_renderer_escapes_catalog_text_and_adds_source_disclosure(self):
        article = valid_article()
        article["summary"] = "<script>alert(1)</script>"
        html = self.render_article(article)
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("公开资料来源", html)
        self.assertIn('target="_blank" rel="noopener noreferrer"', html)

    def test_pages_use_semantic_landmarks_and_existing_auth_contract(self):
        for html in (
            MODULE.render_module_index(self.module),
            self.render_article(valid_article()),
        ):
            for tag in ("header", "nav", "main", "footer"):
                self.assertIn(f"<{tag}", html)
            head = html.split("</head>", 1)[0]
            auth_scripts = re.findall(
                r'<script\b[^>]*\bsrc="\.\./js/auth-(?:config|core|guard)\.js"[^>]*></script>',
                head,
            )
            self.assertEqual(
                [
                    '<script src="../js/auth-config.js"></script>',
                    '<script src="../js/auth-core.js"></script>',
                    '<script src="../js/auth-guard.js" data-root="../"></script>',
                ],
                auth_scripts,
            )
            for script in auth_scripts:
                self.assertIsNone(
                    re.search(r'\s(?:async|defer)(?:\s|=|>)', script),
                    script,
                )
            expected_head_assets = [
                '../css/style.css',
                '../js/auth-config.js',
                '../js/auth-core.js',
                '../js/auth-guard.js',
            ]
            positions = [head.index(value) for value in expected_head_assets]
            self.assertEqual(sorted(positions), positions)
            self.assertIn('data-root="../"', head)
            body_end = html.rsplit("</body>", 1)[0]
            scripts = ["theme.js", "nav.js", "main.js", "search.js"]
            positions = [body_end.index(script) for script in scripts]
            self.assertEqual(sorted(positions), positions)

    def test_article_has_breadcrumb_update_quiz_sources_and_previous_next(self):
        article = valid_article("02-current")
        previous = valid_article("01-previous")
        previous["title"] = "上一课"
        next_ = valid_article("03-next")
        next_["title"] = "下一课"
        html = self.render_article(article, previous, next_)
        for text in ("首页", "巡防入门指南", "更新时间：2026-07-16", "学习自测", "上一课", "下一课"):
            self.assertIn(text, html)
        self.assertIn('href="01-previous.html"', html)
        self.assertIn('href="03-next.html"', html)
        self.assertIn("公开规范", html)
        self.assertIn("发布机关 / 政府网站", html)
        self.assertIn("核验日期：2026-07-16", html)

    def test_source_without_publication_date_has_disclosure(self):
        self.source["published_at"] = None
        html = self.render_article(valid_article())
        self.assertIn("发布日期：页面未标注", html)

    def test_module_index_lists_escaped_articles(self):
        self.module["articles"][0]["title"] = "A & B"
        html = MODULE.render_module_index(self.module)
        self.assertIn("A &amp; B", html)
        self.assertIn('href="01-example.html"', html)


class LearningBuildTests(unittest.TestCase):
    def test_build_skips_modules_without_articles(self):
        catalog = valid_catalog()
        catalog["modules"].append({
            "slug": "kaohe",
            "title": "考核标准",
            "description": "待后续任务建设。",
            "articles": [],
        })
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            written = MODULE.build_pages(root, catalog)
            relative = sorted(path.relative_to(root).as_posix() for path in written)
            manifest = json.loads(
                (root / ".generated-learning-pages.json").read_text(encoding="utf-8")
            )

            self.assertEqual(["rumen/01-example.html", "rumen/index.html"], relative)
            self.assertEqual(relative, manifest)
            self.assertFalse((root / "kaohe" / "index.html").exists())

    def test_current_catalog_builds_only_the_six_onboarding_pages(self):
        catalog = MODULE.load_catalog(ROOT / "data" / "learning-modules.json")
        expected = [
            "rumen/01-gangwei-renshi.html",
            "rumen/02-zhize-bianjie.html",
            "rumen/03-jilv-baomi.html",
            "rumen/04-qinwu-goutong.html",
            "rumen/05-fuxi-zice.html",
            "rumen/index.html",
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            written = MODULE.build_pages(root, catalog)
            relative = sorted(path.relative_to(root).as_posix() for path in written)
            manifest = json.loads(
                (root / ".generated-learning-pages.json").read_text(encoding="utf-8")
            )

            self.assertEqual(expected, relative)
            self.assertEqual(expected, manifest)

    def test_build_writes_pages_and_manifest_and_only_removes_manifested_stale_html(self):
        catalog = valid_catalog()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            module_dir = root / "rumen"
            module_dir.mkdir()
            stale = module_dir / "stale.html"
            stale.write_text("old", encoding="utf-8")
            preserved = module_dir / "manual.html"
            preserved.write_text("manual", encoding="utf-8")
            (root / ".generated-learning-pages.json").write_text(
                json.dumps(["rumen/stale.html"]), encoding="utf-8"
            )
            written = MODULE.build_pages(root, catalog)
            relative = {path.relative_to(root).as_posix() for path in written}
            self.assertEqual({"rumen/index.html", "rumen/01-example.html"}, relative)
            self.assertFalse(stale.exists())
            self.assertTrue(preserved.exists())
            manifest = json.loads((root / ".generated-learning-pages.json").read_text(encoding="utf-8"))
            self.assertEqual(sorted(relative), manifest)
            self.assertFalse(list(root.rglob("*.tmp")))

    def test_manifest_cleanup_rejects_noncanonical_and_impossible_paths(self):
        invalid = (
            "rumen/nested/stale.html",
            "rumen/./manual.html",
            "rumen/../kaohe/stale.html",
            r"rumen\stale.html",
            "rumen/-bad.html",
            "rumen/UPPER.html",
            "rumen/stale.htm",
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in invalid:
                self.assertIsNone(MODULE._safe_generated_html(root, relative), relative)
            self.assertEqual(
                (root / "rumen" / "index.html").resolve(),
                MODULE._safe_generated_html(root, "rumen/index.html"),
            )
            self.assertEqual(
                (root / "jilv" / "01-valid-slug.html").resolve(),
                MODULE._safe_generated_html(root, "jilv/01-valid-slug.html"),
            )

    def test_build_passes_explicit_source_context_to_article_renderer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            MODULE.build_pages(root, valid_catalog())
            rendered = (root / "rumen" / "01-example.html").read_text(encoding="utf-8")
            self.assertIn(valid_source()["title"], rendered)
            self.assertIn("2026-07-16", rendered)

    def test_build_rejects_invalid_catalog_before_writing(self):
        catalog = valid_catalog()
        catalog["verified_at"] = "bad"
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                MODULE.build_pages(Path(directory), catalog)
            self.assertEqual([], list(Path(directory).iterdir()))

    def test_generated_search_records_match_article_pages(self):
        records = MODULE.generated_search_records(valid_catalog())
        self.assertEqual(
            [{
                "title": "第一课",
                "module": "巡防入门指南",
                "path": "rumen/01-example.html",
                "desc": "了解基本要求。",
                "tags": ["入门"],
                "keywords": ["规范", "边界"],
            }],
            records,
        )


if __name__ == "__main__":
    unittest.main()
