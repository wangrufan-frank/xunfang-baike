"""Tests for legal documents data model, generator, and validation."""

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_STREET_NOTES = {
    "jingxie-wuqi-tiaoli": {
        2: "强制手段层级", 3: "警械武器定义", 4: "使用基本原则",
        5: "依法使用边界", 6: "无关人员避让", 7: "驱逐警械条件",
        8: "约束警械条件", 9: "武器使用条件", 10: "武器禁用情形",
        11: "停止使用武器", 12: "伤亡现场处置", 13: "武器使用报告",
        14: "违法使用责任", 15: "无辜损害补偿",
    },
    "renmin-jingcha-fa": {
        5: "执行职务保护", 6: "公安法定职责", 7: "行政强制处罚",
        8: "强行带离措施", 9: "盘问检查条件", 10: "紧急使用武器",
        11: "警械使用授权", 12: "侦查强制措施", 13: "紧急优先通行",
        14: "保护约束措施", 17: "突发现场管制", 19: "非工作时履职",
        20: "文明执勤要求", 21: "危难立即救助", 22: "执法禁止行为",
        23: "着装证件要求", 33: "违法指令拒绝", 35: "阻碍执行职务",
        45: "治安案件回避", 50: "侵权损害赔偿",
    },
    "jumin-shenfenzheng-fa": {
        6: "身份信息保密", 13: "身份证明权利", 15: "证件查验条件",
        16: "禁止非法扣证", 20: "查验违法责任",
    },
    "xingzheng-anji-chengxu-guiding": {
        52: "口头传唤程序", 53: "询问查证要求",
        54: "证据收集要求", 55: "全程记录要求",
    },
    "zhian-guanli-chufa-fa": {
        9: "治安调解条件", 26: "公共秩序扰乱", 44: "活动安全疏散",
        45: "场所安全责任", 50: "人身侵害行为", 51: "殴打伤害处罚",
        61: "阻碍执行职务", 90: "报案立案处理", 91: "非法证据排除",
        94: "涉案信息保密", 96: "现场传唤程序", 97: "询问查证时限",
        98: "询问笔录要求", 99: "现场询问证人", 101: "特殊询问协助",
        102: "人身检查采样", 103: "当场检查程序", 104: "检查笔录要求",
        105: "涉案物品扣押", 108: "调查取证人数", 111: "处罚证据标准",
        112: "处罚告知申辩", 119: "当场处罚条件", 120: "当场处罚程序",
        121: "处罚救济途径", 123: "当场收缴条件", 125: "罚款票据要求",
        131: "文明执法要求", 132: "禁止打骂侮辱", 138: "个人信息保护",
        140: "违法执法赔偿",
    },
}

# Load the build_legal_pages module dynamically
SPEC = importlib.util.spec_from_file_location(
    'build_legal_pages', ROOT / 'tools' / 'build_legal_pages.py'
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _load_data():
    """Load legal-documents.json."""
    path = ROOT / 'data' / 'legal-documents.json'
    return json.loads(path.read_text(encoding='utf-8'))


def _collect_articles(documents):
    """Return flat list of (doc_index, doc, ch_index, art_index, article) tuples."""
    result = []
    for di, doc in enumerate(documents):
        for ci, ch in enumerate(doc.get('chapters', [])):
            for ai, art in enumerate(ch.get('articles', [])):
                result.append((di, doc, ci, ch, ai, art))
    return result


class LegalDocumentsSchemaTests(unittest.TestCase):
    """Test schema validity of legal-documents.json."""

    @classmethod
    def setUpClass(cls):
        cls.data = _load_data()
        cls.documents = cls.data['documents']

    def test_version_is_1(self):
        self.assertEqual(1, self.data.get('version'))

    def test_documents_is_non_empty_list(self):
        self.assertIsInstance(self.documents, list)
        self.assertGreater(len(self.documents), 0)

    def test_every_document_has_required_fields(self):
        required = ['id', 'title', 'document_type', 'authority', 'status']
        for i, doc in enumerate(self.documents):
            with self.subTest(doc_index=i, doc_id=doc.get('id', '?')):
                for field in required:
                    self.assertIn(field, doc, f'doc[{i}] missing {field}')
                    self.assertTrue(doc[field], f'doc[{i}].{field} is empty')

    def test_document_ids_are_unique(self):
        ids = [d['id'] for d in self.documents]
        self.assertEqual(len(ids), len(set(ids)))

    def test_document_status_valid_values(self):
        valid = {'现行有效', '已废止', '已修订'}
        for doc in self.documents:
            with self.subTest(doc_id=doc['id']):
                self.assertIn(doc['status'], valid,
                              f'{doc["id"]}: invalid status "{doc["status"]}"')

    def test_every_article_has_required_fields(self):
        articles = _collect_articles(self.documents)
        for di, doc, ci, ch, ai, art in articles:
            with self.subTest(doc_id=doc['id'], article_num=art.get('number', '?')):
                self.assertIsNotNone(art.get('number'),
                                     f'{doc["id"]} art has no number')
                self.assertTrue(art.get('label', '').strip(),
                                f'{doc["id"]} art {art.get("number")} missing label')
                self.assertIsInstance(art.get('paragraphs'), list,
                                      f'{doc["id"]} art {art.get("number")} paragraphs not list')
                self.assertGreater(len(art.get('paragraphs', [])), 0,
                                   f'{doc["id"]} art {art.get("number")} has empty paragraphs')

    def test_at_least_one_document_has_full_chapters(self):
        """Verify the validation data (jingxie-wuqi-tiaoli) has complete chapters."""
        complete_docs = [d for d in self.documents if d.get('chapters')]
        self.assertGreaterEqual(len(complete_docs), 1,
                                'Expected at least 1 document with full chapters')
        jingxie = next((d for d in self.documents if d['id'] == 'jingxie-wuqi-tiaoli'), None)
        self.assertIsNotNone(jingxie, 'jingxie-wuqi-tiaoli document not found')
        self.assertGreaterEqual(len(jingxie['chapters']), 1,
                                'jingxie-wuqi-tiaoli must have chapters')
        total_arts = sum(len(ch.get('articles', [])) for ch in jingxie['chapters'])
        self.assertGreaterEqual(total_arts, 15,
                                f'jingxie-wuqi-tiaoli only has {total_arts} articles, expected 15+')

    def test_skelton_documents_have_empty_chapters(self):
        """Documents not yet ingested should be marked partial=True."""
        SKELETON_IDS = {'xingzheng-anji-chengxu-guiding', 'xianchang-zhizhi-guicheng'}
        for doc in self.documents:
            if doc['id'] in SKELETON_IDS:
                # These docs are expected to be incomplete — must be marked partial
                self.assertTrue(
                    doc.get('partial'),
                    f'{doc["id"]}: incomplete document should be marked partial=True'
                )
                continue
            # All other documents should have real chapters
            if doc['id'] == 'qita-xiangguan-guifan':
                continue  # index page, not a single law
            ch = doc.get('chapters', [])
            article_count = sum(len(c.get('articles', [])) for c in ch)
            self.assertGreater(article_count, 0,
                               f'{doc["id"]}: should have articles in chapters')

    def test_street_notes_match_reviewed_mapping_and_format(self):
        actual = {}
        for doc in self.documents:
            notes = {
                art["number"]: art["street_note"]
                for ch in doc.get("chapters", [])
                for art in ch.get("articles", [])
                if art.get("street_note")
            }
            if notes:
                actual[doc["id"]] = notes
            self.assertNotIn("xunfang_articles", doc)
        self.assertEqual(EXPECTED_STREET_NOTES, actual)
        for notes in actual.values():
            for note in notes.values():
                self.assertRegex(note, r"^[\u4e00-\u9fff]{4,6}$")


class ArticleNumberingTests(unittest.TestCase):
    """Test article numbering: unique, sequential, starting at 1."""

    @classmethod
    def setUpClass(cls):
        cls.data = _load_data()
        cls.documents = cls.data['documents']

    def test_article_numbers_unique_and_sequential(self):
        for doc in self.documents:
            if not doc.get('chapters'):
                continue
            if doc.get('partial'):
                continue
            nums = []
            for ch in doc['chapters']:
                for art in ch.get('articles', []):
                    nums.append(art['number'])
            if not nums:
                continue
            with self.subTest(doc_id=doc['id']):
                self.assertEqual(len(nums), len(set(nums)),
                                 f'{doc["id"]}: duplicate article numbers in {nums}')
                expected = list(range(1, len(nums) + 1))
                self.assertEqual(expected, nums,
                                 f'{doc["id"]}: article numbers {nums} not sequential 1..{len(nums)}')

    def test_first_article_is_1(self):
        for doc in self.documents:
            if not doc.get('chapters'):
                continue
            if doc.get('partial'):
                continue
            first_art = None
            for ch in doc['chapters']:
                arts = ch.get('articles', [])
                if arts:
                    first_art = arts[0]
                    break
            if first_art is None:
                continue
            with self.subTest(doc_id=doc['id']):
                self.assertEqual(1, first_art['number'],
                                 f'{doc["id"]}: first article is #{first_art["number"]}, expected 1')


class GeneratedPageTests(unittest.TestCase):
    """Test generated HTML pages match source data."""

    @classmethod
    def setUpClass(cls):
        cls.data = _load_data()
        cls.documents = cls.data['documents']

    def test_build_page_contains_all_articles(self):
        """For each document with chapters, generated HTML has correct article count."""
        doc_order = [d['id'] for d in self.documents]
        for doc in self.documents:
            if not doc.get('chapters'):
                continue
            expected_count = sum(
                len(ch.get('articles', [])) for ch in doc['chapters']
            )
            html = MODULE._build_page(doc, doc_order)
            # Count article anchors
            import re
            anchor_count = len(re.findall(r'id="article-\d+"', html))
            with self.subTest(doc_id=doc['id']):
                self.assertEqual(expected_count, anchor_count,
                                 f'{doc["id"]}: HTML has {anchor_count} article anchors, '
                                 f'expected {expected_count}')

    def test_first_article_text_in_HTML(self):
        """First article's first paragraph appears in generated HTML."""
        doc_order = [d['id'] for d in self.documents]
        for doc in self.documents:
            if not doc.get('chapters'):
                continue
            first_art = doc['chapters'][0]['articles'][0]
            first_text = first_art['paragraphs'][0][:30]  # first 30 chars
            html = MODULE._build_page(doc, doc_order)
            with self.subTest(doc_id=doc['id']):
                self.assertIn(first_text, html,
                              f'{doc["id"]}: first article text not found in HTML')

    def test_last_article_text_in_HTML(self):
        """Last article's first paragraph appears in generated HTML."""
        doc_order = [d['id'] for d in self.documents]
        for doc in self.documents:
            if not doc.get('chapters'):
                continue
            last_ch = doc['chapters'][-1]
            last_art = last_ch['articles'][-1]
            last_text = last_art['paragraphs'][0][:30]
            html = MODULE._build_page(doc, doc_order)
            with self.subTest(doc_id=doc['id']):
                self.assertIn(last_text, html,
                              f'{doc["id"]}: last article text not found in HTML')

    def test_generated_HTML_has_required_structure(self):
        """Verify HTML has breadcrumb, title block, module attributes, footer scripts."""
        doc_order = [d['id'] for d in self.documents]
        for doc in self.documents:
            html = MODULE._build_page(doc, doc_order)
            with self.subTest(doc_id=doc['id']):
                self.assertIn('data-module="fagui"', html)
                self.assertIn('data-category="法律法规库"', html)
                self.assertIn('<title>' + doc['title'], html)
                self.assertIn('class="article-summary"', html)
                self.assertIn('class="breadcrumb"', html)
                self.assertIn('class="page-nav"', html)
                self.assertIn('js/main.js', html)
                self.assertIn('js/search.js', html)

    def test_generated_page_uses_collapsible_chapter_toc_and_body(self):
        doc = next(d for d in self.documents if d["id"] == "renmin-jingcha-fa")
        html = MODULE._build_page(doc, [d["id"] for d in self.documents])
        self.assertIn('<details class="legal-toc-chapter">', html)
        self.assertIn('<summary class="legal-toc-chapter-heading">', html)
        self.assertIn('<details class="content-section chapter-block">', html)
        self.assertIn('<summary class="chapter-heading">', html)
        self.assertNotIn('<li class="toc-chapter"><strong>', html)

    def test_street_note_renders_badge_phrase_and_derived_quick_link(self):
        doc = next(d for d in self.documents if d["id"] == "renmin-jingcha-fa")
        html = MODULE._build_page(doc, [d["id"] for d in self.documents])
        self.assertIn('<span class="street-common-badge">街面常用</span>', html)
        self.assertIn('<span class="street-note">盘问检查条件</span>', html)
        self.assertIn('<a href="#article-9">第九条 · 盘问检查条件</a>', html)

    def test_related_links_render_chinese_titles_instead_of_filename_slugs(self):
        doc = next(d for d in self.documents if d["id"] == "renmin-jingcha-fa")
        html = MODULE._build_page(doc, [d["id"] for d in self.documents])
        self.assertIn(
            '<a href="../fagui/panwen-shenfenzheng.html">盘问检查与身份证查验</a>',
            html,
        )
        self.assertNotIn('>panwen-shenfenzheng</a>', html)

    def test_all_legal_pages_render_data_driven_learning_visuals(self):
        visual_docs = [doc for doc in self.documents if doc.get("learning_visual")]
        self.assertEqual(7, len(visual_docs))
        for doc in visual_docs:
            visual = doc["learning_visual"]
            html = MODULE._build_page(doc, [d["id"] for d in self.documents])
            with self.subTest(doc_id=doc["id"]):
                self.assertEqual({"title", "src", "alt", "caption"}, set(visual))
                self.assertIn('class="content-section learning-visual-section"', html)
                self.assertIn(f'src="{visual["src"]}"', html)
                self.assertIn(f'alt="{visual["alt"]}"', html)
                self.assertIn(f'<figcaption>{visual["caption"]}</figcaption>', html)

    def test_document_without_chapters_has_no_empty_accordion_or_quick_nav(self):
        doc = next(d for d in self.documents if d["id"] == "xianchang-zhizhi-guicheng")
        html = MODULE._build_page(doc, [d["id"] for d in self.documents])
        self.assertNotIn('class="legal-toc-chapter"', html)
        self.assertNotIn('class="xunfang-quick-nav"', html)
        self.assertIn("法规正文待补充", html)

    def test_no_empty_documents_without_chapters_produce_empty_text(self):
        """Skeleton documents produce proper skeleton pages with placeholder."""
        doc_order = [d['id'] for d in self.documents]
        for doc in self.documents:
            if doc.get('chapters'):
                continue
            html = MODULE._build_page(doc, doc_order)
            with self.subTest(doc_id=doc['id']):
                self.assertIn('法规正文待补充', html,
                              f'{doc["id"]}: skeleton page should have placeholder text')


class CardSnippetTests(unittest.TestCase):
    """Test .legal-basis-card snippets match source data."""

    def test_card_snippets_match_source(self):
        """Each card's text matches the corresponding article text verbatim."""
        data = _load_data()
        documents = data['documents']
        # Only test documents that have full chapters (jingxie-wuqi-tiaoli)
        for doc in documents:
            if not doc.get('chapters'):
                continue
            for ch in doc['chapters']:
                for art in ch['articles']:
                    card_key = f'{doc["id"]}/{art["number"]}'
                    card_html = MODULE._build_card(doc, art)
                    with self.subTest(card_key=card_key):
                        # Each paragraph text should appear in the card
                        for para in art['paragraphs']:
                            self.assertIn(para, card_html,
                                          f'{card_key}: paragraph text missing from card')

    def test_card_has_all_css_classes(self):
        """Each card uses the correct CSS class structure."""
        data = _load_data()
        for doc in data['documents']:
            if not doc.get('chapters'):
                continue
            for ch in doc['chapters']:
                for art in ch['articles']:
                    card_html = MODULE._build_card(doc, art)
                    self.assertIn('class="legal-basis-card"', card_html)
                    self.assertIn('class="legal-title"', card_html)
                    self.assertIn('class="legal-text"', card_html)
                    self.assertIn('class="legal-note"', card_html)
                    self.assertIn('class="legal-source"', card_html)
                    self.assertIn('class="legal-deep-link"', card_html)


class SearchIndexEntriesTests(unittest.TestCase):
    """Test the search index data generated for legal documents."""

    @classmethod
    def setUpClass(cls):
        cls.data = _load_data()
        cls.documents = cls.data['documents']
        cls.entries = MODULE.build_search_entries(cls.documents)

    def test_one_entry_per_document(self):
        self.assertEqual(len(self.documents), len(self.entries))

    def test_all_entries_have_required_fields(self):
        required = ['title', 'module', 'category', 'desc', 'tags', 'keywords', 'path']
        for i, entry in enumerate(self.entries):
            with self.subTest(entry_index=i):
                for field in required:
                    self.assertIn(field, entry, f'entry[{i}] missing {field}')

    def test_module_is_fagui(self):
        for entry in self.entries:
            with self.subTest(path=entry['path']):
                self.assertEqual('fagui', entry['module'])

    def test_category_is_law_library(self):
        for entry in self.entries:
            with self.subTest(path=entry['path']):
                self.assertEqual('法律法规库', entry['category'])

    def test_tags_contains_category(self):
        for entry in self.entries:
            with self.subTest(path=entry['path']):
                self.assertIn('法律法规库', entry['tags'])

    def test_path_pattern(self):
        for entry in self.entries:
            with self.subTest(path=entry['path']):
                self.assertTrue(
                    entry['path'].startswith('fagui/') and entry['path'].endswith('.html'),
                    f'bad path: {entry["path"]}'
                )

    def test_title_is_non_empty(self):
        for entry in self.entries:
            with self.subTest(path=entry['path']):
                self.assertTrue(entry['title'].strip(),
                                f'empty title for {entry["path"]}')


class BuildScriptExecutionTests(unittest.TestCase):
    """Test the build_legal_pages.py script execution."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmp = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_check_flag_passes_with_valid_data(self):
        """--check should succeed against current legal-documents.json."""
        rc = MODULE.main(['--check', '--root', str(ROOT)])
        self.assertEqual(0, rc, '--check should pass on valid data')

    def test_generate_pages_to_temp_dir(self):
        """Generate pages to a temp dir and verify files are created."""
        rc = MODULE.main(['--root', str(ROOT), '--output-dir', str(self.tmp)])
        self.assertEqual(0, rc)
        # Verify HTML files exist
        data = _load_data()
        for doc in data['documents']:
            html_path = self.tmp / f'{doc["id"]}.html'
            self.assertTrue(html_path.is_file(),
                            f'{html_path} was not created')

    def test_real_root_build_renders_formal_public_source_ledger(self):
        rc = MODULE.main(['--root', str(ROOT), '--output-dir', str(self.tmp)])
        self.assertEqual(0, rc)
        html = (self.tmp / 'qita-xiangguan-guifan.html').read_text(encoding='utf-8')
        self.assertIn('id="public-source-official-police-firearm-rules"', html)
        self.assertIn(
            'id="public-source-official-fuxin-police-patrol-equipment-standards"',
            html,
        )
        self.assertNotIn('id="public-source-qita-xiangguan-guifan"', html)

    def test_temporary_root_without_public_source_ledger_uses_fallback(self):
        root = self.tmp / 'root'
        (root / 'data').mkdir(parents=True)
        (root / 'data' / 'legal-documents.json').write_text(
            json.dumps(_load_data(), ensure_ascii=False),
            encoding='utf-8',
        )
        rc = MODULE.main(['--root', str(root)])
        self.assertEqual(0, rc)
        html = (root / 'fagui' / 'renmin-jingcha-fa.html').read_text(encoding='utf-8')
        self.assertIn('id="public-source-renmin-jingcha-fa"', html)

    def test_validation_catches_bad_data(self):
        """Validation should catch document with duplicate article numbers."""
        bad = {
            'version': 1,
            'documents': [{
                'id': 'test',
                'title': 'Test',
                'document_type': '法律',
                'authority': 'Test',
                'status': '现行有效',
                'chapters': [{
                    'number': '第一章',
                    'title': '测试',
                    'articles': [
                        {'number': 1, 'label': '第一条', 'paragraphs': ['test']},
                        {'number': 1, 'label': '第一条', 'paragraphs': ['test dup']},
                    ]
                }]
            }]
        }
        errors, total = MODULE.validate_all(bad['documents'])
        self.assertGreater(len(errors), 0, 'should catch duplicate article numbers')

    def test_validation_catches_gaps(self):
        """Validation should catch non-sequential article numbers."""
        bad = {
            'version': 1,
            'documents': [{
                'id': 'test',
                'title': 'Test',
                'document_type': '法律',
                'authority': 'Test',
                'status': '现行有效',
                'chapters': [{
                    'number': '第一章',
                    'title': '测试',
                    'articles': [
                        {'number': 1, 'label': '第一条', 'paragraphs': ['test']},
                        {'number': 3, 'label': '第三条', 'paragraphs': ['test gap']},
                    ]
                }]
            }]
        }
        errors, total = MODULE.validate_all(bad['documents'])
        self.assertGreater(len(errors), 0, 'should catch non-sequential article numbers')

    def test_validation_catches_missing_first_article(self):
        """Validation should catch when first article is not 1."""
        bad = {
            'version': 1,
            'documents': [{
                'id': 'test',
                'title': 'Test',
                'document_type': '法律',
                'authority': 'Test',
                'status': '现行有效',
                'chapters': [{
                    'number': '第一章',
                    'title': '测试',
                    'articles': [
                        {'number': 2, 'label': '第二条', 'paragraphs': ['test']},
                    ]
                }]
            }]
        }
        errors, total = MODULE.validate_all(bad['documents'])
        self.assertGreater(len(errors), 0, 'should catch non-1 first article')

    def test_validation_catches_empty_paragraphs(self):
        """Validation should catch articles with empty paragraphs."""
        bad = {
            'version': 1,
            'documents': [{
                'id': 'test',
                'title': 'Test',
                'document_type': '法律',
                'authority': 'Test',
                'status': '现行有效',
                'chapters': [{
                    'number': '第一章',
                    'title': '测试',
                    'articles': [
                        {'number': 1, 'label': '第一条', 'paragraphs': []},
                    ]
                }]
            }]
        }
        errors, total = MODULE.validate_all(bad['documents'])
        self.assertGreater(len(errors), 0, 'should catch empty paragraphs')

    def test_validation_rejects_invalid_street_note(self):
        bad = {
            "id": "test", "title": "测试法", "document_type": "法律",
            "authority": "测试机关", "status": "现行有效", "partial": True,
            "chapters": [{
                "number": "第一章", "title": "测试",
                "articles": [{
                    "number": 1, "label": "第一条",
                    "street_note": "不合格。", "paragraphs": ["测试正文"]
                }]
            }]
        }
        errors, _ = MODULE.validate_all([bad])
        self.assertTrue(any("street_note" in error for error in errors), errors)

    def test_validation_rejects_filename_slug_as_related_title(self):
        bad = {
            "id": "test", "title": "测试法", "document_type": "法律",
            "authority": "测试机关", "status": "现行有效", "partial": True,
            "related_pages": [{
                "path": "fagui/panwen-shenfenzheng.html",
                "title": "panwen-shenfenzheng",
            }],
            "chapters": [],
        }
        errors, _ = MODULE.validate_all([bad])
        self.assertTrue(any("related_pages" in error for error in errors), errors)


if __name__ == '__main__':
    unittest.main()
