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
                self.assertIn('js/search.js', html)

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


if __name__ == '__main__':
    unittest.main()
