from copy import deepcopy
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'public_source_index', ROOT / 'tools' / 'public_source_index.py'
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PublicSourceIndexUnitTests(unittest.TestCase):
    @staticmethod
    def fixture_ledger(verification_status='verified', coverage_status='verified'):
        return {
            'version': 1,
            'pages': [{
                'page_id': 'fagui-dubo-zhifa',
                'path': 'fagui/dubo-zhifa.html',
                'title': '赌博类警情执法标准',
                'review_status': 'pending',
                'reviewed_by': None,
                'reviewed_at': None,
                'points': [{
                    'point_id': 'fagui-dubo-zhifa-01',
                    'position': 1,
                    'label': '核心要点',
                    'source_ids': ['official-secrecy-law-2024'],
                    'coverage_status': coverage_status,
                    'coverage_note': '核对公开与保密审查边界。',
                }],
            }],
            'sources': [{
                'source_id': 'official-secrecy-law-2024',
                'title': '中华人民共和国保守国家秘密法（2024修订）',
                'publisher': '全国人民代表大会常务委员会',
                'platform': '工业和信息化部政府网站',
                'url': 'https://gdca.miit.gov.cn/zwgk/zcwj/flfg/art/2024/art_4870c40a6f8249389684d03786d41639.html',
                'published_at': '2024-02-27',
                'verified_at': '2026-07-14',
                'verification_status': verification_status,
                'similarity_note': '公开法律文本说明公开与保密义务的边界。',
                'source_level': 1,
                'last_checked_at': '2026-07-14',
            }],
        }

    def test_discovery_matches_current_site_inventory(self):
        pages = MODULE.discover_pages(ROOT)
        self.assertEqual(len(pages), 27)
        counts = {'fagui': 0, 'xunlian': 0, 'zhuangbei': 0, 'zoufang': 0}
        point_counts = {'fagui': 0, 'xunlian': 0, 'zhuangbei': 0, 'zoufang': 0}
        point_count = 0
        for page in pages:
            counts[page.parent.name] += 1
            page_point_count = len(
                MODULE.extract_points(page.read_text(encoding='utf-8'))
            )
            point_counts[page.parent.name] += page_point_count
            point_count += page_point_count
        self.assertEqual(
            counts,
            {'fagui': 6, 'xunlian': 11, 'zhuangbei': 7, 'zoufang': 3},
        )
        self.assertEqual(
            point_counts,
            {'fagui': 33, 'xunlian': 67, 'zhuangbei': 31, 'zoufang': 22},
        )
        self.assertEqual(point_count, 153)

    def test_discovery_is_limited_to_named_directories_and_non_index_html(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('fagui', 'xunlian', 'zhuangbei', 'zoufang', 'jingqing'):
                (root / name).mkdir()
                (root / name / 'page.html').write_text('<h1>title</h1>', encoding='utf-8')
                (root / name / 'index.html').write_text('<h1>index</h1>', encoding='utf-8')
            (root / 'fagui' / 'note.txt').write_text('not html', encoding='utf-8')

            pages = MODULE.discover_pages(root)

        self.assertEqual(
            [page.relative_to(root).as_posix() for page in pages],
            ['fagui/page.html', 'xunlian/page.html', 'zhuangbei/page.html', 'zoufang/page.html'],
        )

    def test_extract_points_decodes_entities_and_ignores_other_elements(self):
        html = (
            '<h1>页面 &amp; 标题</h1>'
            '<div class="step-title">第一 &amp; 要点</div>'
            '<span class="other step-title-extra">不应提取</span>'
            '<div class="step-title"><strong>第二</strong>要点</div>'
        )
        self.assertEqual(MODULE.extract_points(html), ['第一 & 要点', '第二要点'])

    def test_load_ledger_reads_utf8_json(self):
        ledger = self.fixture_ledger()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'ledger.json'
            path.write_text(json.dumps(ledger, ensure_ascii=False), encoding='utf-8')
            self.assertEqual(MODULE.load_ledger(path), ledger)

    def test_pending_or_search_snippet_source_is_rejected_in_strict_mode(self):
        ledger = self.fixture_ledger(
            verification_status='needs_review', coverage_status='pending'
        )
        errors = MODULE.validate_schema(ledger)
        self.assertTrue(any('verification_status' in error for error in errors))
        self.assertTrue(any('coverage_status' in error for error in errors))

    def test_allow_pending_relaxes_only_verification_requirements(self):
        ledger = self.fixture_ledger('needs_review', 'pending')
        self.assertEqual(MODULE.validate_schema(ledger, allow_pending=True), [])
        ledger['sources'][0]['url'] = 'http://example.com/source'
        self.assertTrue(MODULE.validate_schema(ledger, allow_pending=True))

    def test_schema_rejects_bad_version_duplicates_and_dangling_references(self):
        ledger = self.fixture_ledger()
        ledger['version'] = 2
        ledger['pages'].append(deepcopy(ledger['pages'][0]))
        ledger['sources'].append(deepcopy(ledger['sources'][0]))
        ledger['pages'][0]['points'].append(deepcopy(ledger['pages'][0]['points'][0]))
        ledger['pages'][0]['points'][0]['source_ids'].append('missing-source')

        errors = MODULE.validate_schema(ledger)

        self.assertTrue(any('version' in error for error in errors))
        self.assertTrue(any('duplicate page path' in error for error in errors))
        self.assertTrue(any('duplicate source_id' in error for error in errors))
        self.assertTrue(any('duplicate point_id' in error for error in errors))
        self.assertTrue(any('missing-source' in error for error in errors))

    def test_strict_schema_requires_sources_and_verified_coverage(self):
        ledger = self.fixture_ledger()
        point = ledger['pages'][0]['points'][0]
        point['source_ids'] = []
        point['coverage_status'] = 'pending'
        errors = MODULE.validate_schema(ledger)
        self.assertTrue(any('source_ids' in error for error in errors))
        self.assertTrue(any('coverage_status' in error for error in errors))

    def test_source_fields_https_and_dates_are_validated(self):
        required = (
            'title', 'publisher', 'platform', 'url', 'verified_at',
            'similarity_note', 'source_level', 'last_checked_at',
        )
        for field in required:
            with self.subTest(field=field):
                ledger = self.fixture_ledger()
                ledger['sources'][0][field] = ''
                self.assertTrue(
                    any(field in error for error in MODULE.validate_schema(ledger))
                )

        ledger = self.fixture_ledger()
        ledger['sources'][0]['url'] = 'http://example.com/source'
        ledger['sources'][0]['verified_at'] = '2026/07/14'
        ledger['sources'][0]['last_checked_at'] = '2026-02-30'
        errors = MODULE.validate_schema(ledger)
        self.assertTrue(any('https://' in error for error in errors))
        self.assertTrue(any('verified_at' in error for error in errors))
        self.assertTrue(any('last_checked_at' in error for error in errors))

    def test_identifier_fields_reject_non_string_values_without_type_error(self):
        locations = {
            'source_id': 'source[1].source_id',
            'path': 'page[1].path',
            'point_id': 'page[1].point[1].point_id',
            'source_ids': 'page[1].point[1].source_ids[1]',
        }
        for field in locations:
            for value in ({}, []):
                with self.subTest(field=field, value_type=type(value).__name__):
                    ledger = self.fixture_ledger()
                    if field == 'source_id':
                        ledger['sources'][0][field] = value
                    elif field == 'path':
                        ledger['pages'][0][field] = value
                    elif field == 'point_id':
                        ledger['pages'][0]['points'][0][field] = value
                    else:
                        ledger['pages'][0]['points'][0][field] = [value]

                    errors = MODULE.validate_schema(ledger)

                    self.assertTrue(
                        any(
                            error == f'{locations[field]} must be a non-empty string'
                            for error in errors
                        ),
                        errors,
                    )

    def test_review_status_is_not_inferred_from_verified_sources(self):
        ledger = self.fixture_ledger()
        before = deepcopy(ledger)
        self.assertEqual(ledger['pages'][0]['review_status'], 'pending')
        self.assertTrue(MODULE.publish_errors(ledger))
        self.assertEqual(ledger, before)

    def test_publish_requires_approval_reviewer_and_review_date(self):
        ledger = self.fixture_ledger()
        page = ledger['pages'][0]
        page.update(review_status='approved', reviewed_by='reviewer', reviewed_at='2026-07-14')
        self.assertEqual(MODULE.publish_errors(ledger), [])
        for field in ('reviewed_by', 'reviewed_at'):
            with self.subTest(field=field):
                changed = deepcopy(ledger)
                changed['pages'][0][field] = ''
                self.assertTrue(any(field in error for error in MODULE.publish_errors(changed)))

    def test_new_html_point_missing_from_ledger_is_reported(self):
        ledger = self.fixture_ledger()
        html = (ROOT / 'fagui' / 'dubo-zhifa.html').read_text(encoding='utf-8')
        changed = html.replace(
            '<div class="page-nav">',
            '<div class="step-card step-blue"><div class="step-title">新增知识点</div>'
            '<div class="step-lead">新增摘要</div></div><div class="page-nav">',
        )
        errors = MODULE.compare_page_points(changed, ledger['pages'][0])
        self.assertTrue(any('新增知识点' in error for error in errors))

    def test_compare_page_points_reports_added_removed_and_renamed_labels(self):
        page = {
            'path': 'fagui/example.html',
            'points': [
                {'position': 1, 'label': '要点一'},
                {'position': 2, 'label': '要点二'},
                {'position': 3, 'label': '已删除要点'},
            ],
        }
        html = (
            '<h1>页面</h1>'
            '<div class="step-title">要点一</div>'
            '<div class="step-title">要点二已改名</div>'
            '<div class="step-title">新增要点</div>'
        )
        errors = MODULE.compare_page_points(html, page)
        combined = '\n'.join(errors)
        for label in ('要点二已改名', '新增要点', '要点二', '已删除要点'):
            self.assertIn(label, combined)

    def test_compare_page_points_reports_only_middle_insertion(self):
        page = self._comparison_page('A', 'B')
        html = self._comparison_html('A', 'NEW', 'B')
        self.assertEqual(
            MODULE.compare_page_points(html, page),
            ['example.html: HTML added point at position 2: NEW'],
        )

    def test_compare_page_points_reports_only_middle_deletion(self):
        page = self._comparison_page('A', 'B', 'C')
        html = self._comparison_html('A', 'C')
        self.assertEqual(
            MODULE.compare_page_points(html, page),
            ['example.html: HTML removed point at position 2: B'],
        )

    def test_compare_page_points_reports_equal_length_replacement_as_rename(self):
        page = self._comparison_page('A', 'OLD', 'C')
        html = self._comparison_html('A', 'NEW', 'C')
        self.assertEqual(
            MODULE.compare_page_points(html, page),
            ['example.html: point renamed at position 2: OLD -> NEW'],
        )

    @staticmethod
    def _comparison_page(*labels):
        return {
            'path': 'example.html',
            'points': [
                {'position': position, 'label': label}
                for position, label in enumerate(labels, 1)
            ],
        }

    @staticmethod
    def _comparison_html(*labels):
        return ''.join(
            f'<div class="step-title">{label}</div>' for label in labels
        )

    def test_validate_ledger_reports_inventory_and_html_drift(self):
        ledger = self.fixture_ledger()
        ledger['pages'][0]['path'] = 'fagui/page.html'
        ledger['pages'][0]['points'][0]['label'] = '台账要点'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'fagui').mkdir()
            (root / 'fagui' / 'page.html').write_text(
                '<h1>页面</h1><div class="step-title">HTML 要点</div>',
                encoding='utf-8',
            )
            (root / 'xunlian').mkdir()
            (root / 'xunlian' / 'extra.html').write_text('<h1>新页面</h1>', encoding='utf-8')

            errors = MODULE.validate_ledger(root, ledger)

        combined = '\n'.join(errors)
        self.assertIn('xunlian/extra.html', combined)
        self.assertIn('HTML 要点', combined)
        self.assertIn('台账要点', combined)


class PublicSourceLedgerInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = MODULE.load_ledger(ROOT / 'data' / 'public-sources.json')

    def test_ledger_covers_every_current_page_and_point(self):
        errors = MODULE.validate_ledger(ROOT, self.ledger, allow_pending=True)
        self.assertEqual(errors, [])
        self.assertEqual(len(self.ledger['pages']), 27)
        self.assertEqual(
            sum(len(page['points']) for page in self.ledger['pages']), 153
        )


class PublicSourceRenderTests(unittest.TestCase):
    def setUp(self):
        self.html = (
            '<div class="step-card step-blue">\n'
            '  <div class="step-title">第一点</div><div class="step-lead">摘要一</div>\n'
            '</div>\n'
            '<div class="step-card step-green">\n'
            '  <div class="step-title">第二点</div><div class="step-lead">摘要二</div>\n'
            '</div>\n'
            '<div class="page-nav"></div>\n'
        )
        self.source = deepcopy(
            PublicSourceIndexUnitTests.fixture_ledger('verified', 'verified')['sources'][0]
        )
        self.source['source_id'] = 'source-law'
        self.source_map = {'source-law': self.source}
        self.page = {
            'page_id': 'fixture-page',
            'path': 'fixture/page.html',
            'title': '测试页',
            'review_status': 'pending',
            'reviewed_by': None,
            'reviewed_at': None,
            'points': [
                {
                    'point_id': 'point-01', 'position': 1, 'label': '第一点',
                    'source_ids': ['source-law'], 'coverage_status': 'verified',
                    'coverage_note': '第一点与公开资料的相似边界。',
                },
                {
                    'point_id': 'point-02', 'position': 2, 'label': '第二点',
                    'source_ids': ['source-law'], 'coverage_status': 'verified',
                    'coverage_note': '第二点与公开资料的相似边界。',
                },
            ],
        }

    def test_render_page_adds_reusable_citations_and_complete_source_index(self):
        rendered = MODULE.render_page(self.html, self.page, self.source_map)

        self.assertIn('id="source-ref-point-01-source-law"', rendered)
        self.assertIn('id="source-ref-point-02-source-law"', rendered)
        self.assertEqual(rendered.count('href="#public-source-source-law"'), 2)
        self.assertEqual(rendered.count('id="public-source-source-law"'), 1)
        self.assertIn('class="public-source-index"', rendered)
        self.assertLess(rendered.index('public-source-index'), rendered.index('page-nav'))
        for value in (
            self.source['title'], self.source['publisher'], self.source['platform'],
            self.source['published_at'], self.source['verified_at'],
            self.source['similarity_note'],
            'target="_blank" rel="noopener noreferrer"',
            'href="#source-ref-point-01-source-law"',
            '本索引用于说明核验日期时互联网上存在与本页知识点相似的公开资料，不表示本站内容均转载自所列网页，也不构成保密审查、法律审查或业务主管部门审核结论。公开发布仍须执行本单位规定的先审查、后公开程序。',
        ):
            self.assertIn(value, rendered)
        self.assertEqual(MODULE.render_page(rendered, self.page, self.source_map), rendered)

    def test_render_page_rejects_bad_page_structure_and_dangling_sources(self):
        cases = []
        renamed = self.html.replace('第一点', '标题不符', 1)
        cases.append(('标题不符', renamed, self.page, self.source_map))
        cases.append(('数量', self.html.replace(
            '<div class="step-card step-green">', '<div class="other">', 1
        ), self.page, self.source_map))
        cases.append(('source-law', self.html, self.page, {}))
        cases.append(('.page-nav', self.html.replace('page-nav', 'other-nav'), self.page, self.source_map))
        for expected, html, page, sources in cases:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, 'fixture/page.html.*' + expected):
                    MODULE.render_page(html, page, sources)


class PublicSourceIndexCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / 'tools' / 'public_source_index.py'), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=False,
        )

    def test_inventory_command_reports_current_counts(self):
        result = self.run_cli('inventory')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('27 pages, 153 points', result.stdout)
        self.assertIn('fagui: 6 pages, 33 points', result.stdout)
        self.assertIn('xunlian: 11 pages, 67 points', result.stdout)
        self.assertIn('zhuangbei: 7 pages, 31 points', result.stdout)
        self.assertIn('zoufang: 3 pages, 22 points', result.stdout)

    def test_inventory_output_writes_pending_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'public-sources.json'
            result = self.run_cli('inventory', '--output', str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            ledger = MODULE.load_ledger(output)

        self.assertIn(
            'Wrote 27 pages and 153 points; all coverage statuses are pending.',
            result.stdout,
        )
        self.assertEqual(MODULE.validate_ledger(ROOT, ledger, allow_pending=True), [])
        self.assertEqual(ledger['sources'], [])
        self.assertTrue(
            all(
                page['review_status'] == 'pending'
                and page['reviewed_by'] is None
                and page['reviewed_at'] is None
                for page in ledger['pages']
            )
        )
        self.assertTrue(
            all(
                point['source_ids'] == []
                and point['coverage_status'] == 'pending'
                and point['coverage_note'] == ''
                for page in ledger['pages']
                for point in page['points']
            )
        )

    def test_check_allow_pending_reports_production_ledger_summary(self):
        result = self.run_cli('check', '--allow-pending')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            'PASS: 27 pages, 153 points; '
            '153 points pending source verification.',
            result.stdout,
        )

    def test_unknown_command_is_usage_error(self):
        result = self.run_cli('unknown')
        self.assertEqual(result.returncode, 2)

    def test_check_failure_uses_data_error_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger_path = Path(directory) / 'ledger.json'
            ledger_path.write_text(
                json.dumps(PublicSourceIndexUnitTests.fixture_ledger(
                    'needs_review', 'pending'
                ), ensure_ascii=False),
                encoding='utf-8',
            )
            result = self.run_cli('check', str(ledger_path))
        self.assertEqual(result.returncode, 1)
        self.assertIsInstance(result.stderr, str)
        self.assertIn('verification_status', result.stderr)

    def test_check_invalid_identifier_types_returns_data_error_without_traceback(self):
        ledger = PublicSourceIndexUnitTests.fixture_ledger()
        ledger['sources'][0]['source_id'] = {}
        ledger['pages'][0]['path'] = {}
        ledger['pages'][0]['points'][0]['point_id'] = []
        ledger['pages'][0]['points'][0]['source_ids'] = [{}]
        with tempfile.TemporaryDirectory() as directory:
            ledger_path = Path(directory) / 'ledger.json'
            ledger_path.write_text(
                json.dumps(ledger, ensure_ascii=False),
                encoding='utf-8',
            )
            result = self.run_cli('check', str(ledger_path))

        self.assertEqual(result.returncode, 1)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('source[1].source_id must be a non-empty string', result.stderr)
        self.assertIn('page[1].path must be a non-empty string', result.stderr)
        self.assertIn('page[1].point[1].point_id must be a non-empty string', result.stderr)
        self.assertIn(
            'page[1].point[1].source_ids[1] must be a non-empty string',
            result.stderr,
        )

    def test_production_write_rejects_pending_ledger_without_changing_html(self):
        pages = MODULE.discover_pages(ROOT)
        before = {page: page.read_bytes() for page in pages}
        result = self.run_cli('write')
        self.assertEqual(result.returncode, 1)
        self.assertEqual({page: page.read_bytes() for page in pages}, before)

    def test_write_check_reports_changes_without_writing(self):
        fixture = PublicSourceRenderTests()
        fixture.setUp()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'fagui').mkdir()
            page_path = root / 'fagui' / 'page.html'
            page_path.write_text('<h1>测试页</h1>' + fixture.html, encoding='utf-8')
            page = deepcopy(fixture.page)
            page['path'] = 'fagui/page.html'
            ledger = {'version': 1, 'pages': [page], 'sources': [fixture.source]}
            ledger_path = root / 'ledger.json'
            ledger_path.write_text(json.dumps(ledger, ensure_ascii=False), encoding='utf-8')
            before = page_path.read_bytes()

            result = self.run_cli(
                'write', str(ledger_path), '--root', str(root), '--check'
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn('CHANGED: fagui/page.html', result.stdout)
            self.assertIn('CHECK: 1 of 1 pages would change.', result.stdout)
            self.assertEqual(page_path.read_bytes(), before)

    def test_write_check_is_dry_run_and_render_failure_is_atomic(self):
        fixture = PublicSourceRenderTests()
        fixture.setUp()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'fagui').mkdir()
            first = root / 'fagui' / 'first.html'
            second = root / 'fagui' / 'second.html'
            first.write_text('<h1>测试页</h1>' + fixture.html, encoding='utf-8')
            second.write_text(
                '<h1>第二页</h1>' + fixture.html.replace('page-nav', 'other-nav'),
                encoding='utf-8',
            )
            ledger = {'version': 1, 'pages': [], 'sources': [fixture.source]}
            for index, path in enumerate((first, second), 1):
                page = deepcopy(fixture.page)
                page['page_id'] = f'fixture-{index}'
                page['path'] = path.relative_to(root).as_posix()
                page['title'] = '测试页' if index == 1 else '第二页'
                page['points'] = deepcopy(fixture.page['points'])
                for point_index, point in enumerate(page['points'], 1):
                    point['point_id'] = f'page-{index}-{point_index:02d}'
                ledger['pages'].append(page)
            ledger_path = root / 'ledger.json'
            ledger_path.write_text(json.dumps(ledger, ensure_ascii=False), encoding='utf-8')
            first_before = first.read_bytes()

            checked = self.run_cli(
                'write', str(ledger_path), '--root', str(root), '--check'
            )
            failed = self.run_cli('write', str(ledger_path), '--root', str(root))

            self.assertEqual(checked.returncode, 1)
            self.assertEqual(failed.returncode, 1)
            self.assertIn('second.html', failed.stderr)
            self.assertEqual(first.read_bytes(), first_before)


if __name__ == '__main__':
    unittest.main()
