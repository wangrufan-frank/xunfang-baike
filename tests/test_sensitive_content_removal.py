from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]

# Detail pages removed during the 2026-07 content remediation. They must stay
# deleted: the rebuilt modules cover these topics only through the approved
# replacement articles listed in data/content-inventory.json.
DELETED_PATHS = {
    'qinwu/yanchanghui-zhifa.html',
    'qinwu/xiaoyuan-jinrong.html',
    'qinwu/yuqing-zhanshu.html',
    'qinwu/chuzhi-yuan.html',
    'qinwu/kongzhi-daili.html',
    'qinwu/shewen-yanlian.html',
    'qinwu/xuanchuan-quzheng.html',
    'qinwu/yuqing-daokong.html',
    'xunlian/zhudong-hengyi.html',
    'xunlian/xunlian-jiaoxuefa.html',
    'xunlian/shizi-fangyu.html',
    'xunlian/sinengli-yaosu.html',
    'xunlian/gaishu-yuanze.html',
    'xunlian/wuli-shengji.html',
    'jingqing/chidao-jingqing.html',
    'jingqing/chidao-leiqing.html',
    'jingqing/dajia-douou.html',
    'jingqing/jizhi-liucheng.html',
    'jingqing/keyi-cheliang.html',
    'jingqing/renyuan-pancha.html',
    'jingqing/zuijiu-naoshi.html',
    'zoufang/xianchang-chuzhi.html',
    'zoufang/zhengzhi-hexinqu.html',
    'zoufang/daxing-huodong.html',
}

# Titles of removed pages that must not resurface as page or module names.
# Terms that became approved category or article vocabulary in the rebuilt
# site (for example the qinwu category 大型活动安保) are intentionally not
# listed here any more.
FORBIDDEN_RUNTIME_TERMS = {
    '训练教学法',
    '快反技能',
    '反恐基础理论',
    '现场处置执法规范',
    '政治核心区处置',
}

RUNTIME_SUFFIXES = {'.html', '.js', '.json', '.wxml', '.wxss'}
EXCLUDED_PARTS = {
    '.git',
    '.worktrees',
    '.superpowers',
    'deliverables',
    'docs',
    'node_modules',
    'tests',
}


def runtime_files():
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix not in RUNTIME_SUFFIXES:
            continue
        relative = path.relative_to(ROOT)
        if EXCLUDED_PARTS.intersection(relative.parts):
            continue
        yield path


class SensitiveContentRemovalTests(unittest.TestCase):
    def test_parse_html_targets_the_current_repository(self):
        source = (ROOT / 'parse_html.py').read_text(encoding='utf-8')
        self.assertIn("BASE = os.path.dirname(os.path.abspath(__file__))", source)
        self.assertNotIn("BASE = r'F:\\frank第二大脑\\xunfang-baike'", source)

    def test_restricted_detail_files_are_deleted(self):
        remaining = sorted(path for path in DELETED_PATHS if (ROOT / path).exists())
        self.assertEqual(remaining, [])

    def test_restricted_terms_are_absent_from_runtime_files(self):
        hits = []
        for path in runtime_files():
            source = path.read_text(encoding='utf-8')
            for term in FORBIDDEN_RUNTIME_TERMS:
                if term in source:
                    hits.append((path.relative_to(ROOT).as_posix(), term))
        self.assertEqual(sorted(hits), [])

    def test_deleted_paths_are_not_referenced_by_runtime_files(self):
        forbidden_references = DELETED_PATHS | {
            Path(path).name for path in DELETED_PATHS
        }
        hits = []
        for path in runtime_files():
            source = path.read_text(encoding='utf-8')
            for reference in forbidden_references:
                if reference in source:
                    hits.append((path.relative_to(ROOT).as_posix(), reference))
        self.assertEqual(sorted(hits), [])

    def test_search_index_excludes_deleted_pages(self):
        records = json.loads((ROOT / 'search-index.json').read_text(encoding='utf-8'))
        indexed_paths = {record['path'] for record in records}
        self.assertEqual(sorted(indexed_paths.intersection(DELETED_PATHS)), [])

    def test_jingqing_miniprogram_still_shows_remediation_state(self):
        mini = (
            ROOT / 'miniprogram' / 'pages' / 'jingqing' / 'index' / 'index.wxml'
        ).read_text(encoding='utf-8')
        self.assertIn('内容整改中', mini)

    def test_jingqing_miniprogram_data_is_empty(self):
        source = (
            ROOT / 'miniprogram' / 'data' / 'jingqing.js'
        ).read_text(encoding='utf-8').strip()
        self.assertEqual(source, 'module.exports = [];')

    def test_qinwu_miniprogram_still_shows_remediation_shell(self):
        mini_home = (
            ROOT / 'miniprogram' / 'pages' / 'index' / 'index.wxml'
        ).read_text(encoding='utf-8')
        mini_section = (
            ROOT / 'miniprogram' / 'pages' / 'qinwu' / 'index' / 'index.wxml'
        ).read_text(encoding='utf-8')
        mini_data = (
            ROOT / 'miniprogram' / 'data' / 'qinwu.js'
        ).read_text(encoding='utf-8').strip()

        self.assertIn('巡防勤务', mini_home)
        self.assertIn('内容整改中', mini_section)
        self.assertEqual(mini_data, 'module.exports = [];')

    def test_miniprogram_home_does_not_repeat_removed_jingqing_cases(self):
        source = (
            ROOT / 'miniprogram' / 'pages' / 'index' / 'index.js'
        ).read_text(encoding='utf-8')
        self.assertNotIn('醉酒闹事处置', source)
        self.assertNotIn('家暴警情', source)

    def test_html_links_do_not_target_deleted_pages(self):
        hits = []
        for page in ROOT.rglob('*.html'):
            relative = page.relative_to(ROOT)
            if EXCLUDED_PARTS.intersection(relative.parts):
                continue
            source = page.read_text(encoding='utf-8')
            for href in re.findall(r'href=["\']([^"\']+\.html)(?:[#?][^"\']*)?["\']', source):
                if href.startswith(('http://', 'https://', '//')):
                    continue
                target = (page.parent / href).resolve()
                try:
                    target_relative = target.relative_to(ROOT).as_posix()
                except ValueError:
                    continue
                if target_relative in DELETED_PATHS:
                    hits.append((relative.as_posix(), target_relative))
        self.assertEqual(sorted(hits), [])


if __name__ == '__main__':
    unittest.main()
