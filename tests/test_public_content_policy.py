"""Tests for the public content policy.

These tests assert that the xunfang-baike static HTML site complies with the
public-content policy adopted during the 2026-07 content remediation:

- No internal-source labels ("巡防百科知识库内部资料").
- No internal .md filenames in source sections.
- No local absolute (drive-letter) paths.
- Every source <li> links to a public URL.
- Every source carries complete metadata.
- Learning-type third-level pages carry required structural sections.
- <details> elements do not hide prohibited content.
- No page mixes old .source-list with new .source-list--public.

Tests 1-5 and 8 are wired to FAIL initially because the current site still
contains internal source material in 83 pages.  Tests 6-7 are skipped --
the features they guard do not exist yet (no .quick-read sections, no
<details> elements).
"""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Directory helpers
# ---------------------------------------------------------------------------

# Directories whose .html files are treated as "content pages".
CONTENT_DIRS = [
    'jingqing', 'qinwu', 'xunlian', 'zhuangbei', 'zoufang', 'fagui',
    'meiyueyixue',
]

# fagui pages that belong to the "法律法规库" category -- they are reference
# pages, *not* learning-type third-level pages for the purpose of test 6.
LEGAL_LIBRARY_PATHS = {
    'fagui/zhian-guanli-chufa-fa.html',
    'fagui/renmin-jingcha-fa.html',
    'fagui/jumin-shenfenzheng-fa.html',
    'fagui/xingzheng-anji-chengxu-guiding.html',
    'fagui/jingxie-wuqi-tiaoli.html',
    'fagui/xianchang-zhizhi-guicheng.html',
    'fagui/qita-xiangguan-guifan.html',
}


def _content_html_files():
    """Yield every .html file inside one of the CONTENT_DIRS directories."""
    for dir_name in CONTENT_DIRS:
        dir_path = ROOT / dir_name
        if not dir_path.is_dir():
            continue
        yield from sorted(dir_path.glob('*.html'))


def _learning_third_level_pages():
    """Yield third-level learning-type pages.

    These are .html files under jingqing/, qinwu/, xunlian/, zhuangbei/,
    zoufang/ that are NOT index.html, plus fagui/ pages that are NOT in the
    legal-library list.
    """
    for html_file in _content_html_files():
        if html_file.name == 'index.html':
            continue
        relative = html_file.relative_to(ROOT).as_posix()
        if relative in LEGAL_LIBRARY_PATHS:
            continue
        yield html_file


# ---------------------------------------------------------------------------
# HTML scraping helpers
# ---------------------------------------------------------------------------

def _source_list_items(html):
    """Return each <li> text content found inside a bare .source-list section.

    ``bare`` means the class is exactly ``source-list`` (not
    ``source-list--public`` or any other compound class).
    """
    items = []
    for match in re.finditer(
        r'<section[^>]*\bclass="([^"]*)"[^>]*>(.*?)</section>',
        html, re.DOTALL,
    ):
        classes = match.group(1).split()
        if 'source-list' not in classes:
            continue
        if 'source-list--public' in classes:
            continue
        body = match.group(2)
        for li_match in re.finditer(r'<li>(.*?)</li>', body, re.DOTALL):
            items.append(li_match.group(1).strip())
    return items


def _violation(file_path, message=None):
    """Return a human-readable violation string for an assertion."""
    relative = file_path.relative_to(ROOT).as_posix()
    return f'{relative}: {message}' if message else relative


# ===================================================================
# Test cases
# ===================================================================

class PublicContentPolicyTests(unittest.TestCase):
    """Assert that every content page complies with the public-content policy."""

    # ------------------------------------------------------------------
    # Test 1 -- No internal source labels
    # ------------------------------------------------------------------

    def test_no_internal_source_labels(self):
        """No HTML file may contain the internal-source label."""
        violations = []
        for html_file in _content_html_files():
            source = html_file.read_text(encoding='utf-8')
            if '巡防百科知识库内部资料' in source:
                violations.append(_violation(html_file))
        self.assertEqual(
            violations, [],
            f'{len(violations)} file(s) still carry the internal-source label'
            f' "巡防百科知识库内部资料":\n' + '\n'.join(sorted(violations)),
        )

    # ------------------------------------------------------------------
    # Test 2 -- No internal .md filenames in source sections
    # ------------------------------------------------------------------

    def test_no_internal_md_filenames_in_sources(self):
        """No .source-list <li> may contain a bare .md filename."""
        violations = []
        for html_file in _content_html_files():
            source = html_file.read_text(encoding='utf-8')
            for item in _source_list_items(source):
                if re.search(r'\.md\s*[—–-]', item):
                    violations.append(_violation(html_file, item[:80]))
                    break  # one violation per file is sufficient
        self.assertEqual(
            violations, [],
            f'{len(violations)} file(s) still reference internal .md files'
            f' in their source sections:\n' + '\n'.join(sorted(violations)),
        )

    # ------------------------------------------------------------------
    # Test 3 -- No local absolute (drive-letter) paths
    # ------------------------------------------------------------------

    def test_no_local_absolute_paths(self):
        """No HTML file may contain a Windows drive-letter path (e.g. F:\\\\)."""
        violations = []
        for html_file in _content_html_files():
            source = html_file.read_text(encoding='utf-8')
            if re.search(r'[A-Za-z]:\\', source):
                violations.append(_violation(html_file))
        self.assertEqual(
            violations, [],
            f'{len(violations)} file(s) contain local absolute paths:\n'
            + '\n'.join(sorted(violations)),
        )

    # ------------------------------------------------------------------
    # Test 4 -- Every source <li> carries a public URL
    # ------------------------------------------------------------------

    def test_every_source_item_has_url(self):
        """Every <li> inside a .source-list must contain http:// or https://."""
        violations = []
        for html_file in _content_html_files():
            source = html_file.read_text(encoding='utf-8')
            for item in _source_list_items(source):
                if 'http://' not in item and 'https://' not in item:
                    violations.append(_violation(html_file, item[:80]))
                    break  # one violation per file is sufficient
        self.assertEqual(
            violations, [],
            f'{len(violations)} file(s) have source-list items without a'
            f' public URL:\n' + '\n'.join(sorted(violations)),
        )

    # ------------------------------------------------------------------
    # Test 5 -- Every source carries complete metadata
    # ------------------------------------------------------------------

    def test_every_source_has_metadata(self):
        """Each source-list <li> must include a dash-separated publisher and
        the string '核验日期' (verification date)."""
        violations = []
        for html_file in _content_html_files():
            source = html_file.read_text(encoding='utf-8')
            for item in _source_list_items(source):
                if '核验日期' not in item:
                    violations.append(
                        _violation(html_file,
                                   f'missing 核验日期: {item[:80]}')
                    )
                    break
                if not re.search(r'[—–-]', item):
                    violations.append(
                        _violation(html_file,
                                   f'missing title–publisher separator: {item[:80]}')
                    )
                    break
        self.assertEqual(
            violations, [],
            f'{len(violations)} file(s) have source-list items with'
            f' incomplete metadata:\n' + '\n'.join(sorted(violations)),
        )

    # ------------------------------------------------------------------
    # Test 6 -- Learning-type third-level pages carry required sections
    # ------------------------------------------------------------------

    @unittest.skip(
        'Feature not yet implemented: .quick-read sections and .article-toc '
        'do not exist yet.  Enable this test once the learning-page template '
        'is rolled out.'
    )
    def test_learning_pages_have_required_sections(self):
        """Every learning-type third-level page must include:

        * a .quick-read summary section,
        * page navigation (.article-toc or .page-nav), and
        * exactly one public source section (.source-list--public).
        """
        violations = []
        for html_file in _learning_third_level_pages():
            source = html_file.read_text(encoding='utf-8')
            relative = html_file.relative_to(ROOT).as_posix()

            has_quick_read = bool(re.search(
                r'<[^>]+\bclass="[^"]*\bquick-read\b[^"]*"', source
            ))
            has_toc = bool(re.search(
                r'<[^>]+\bclass="[^"]*\barticle-toc\b[^"]*"', source
            ))
            has_page_nav = bool(re.search(
                r'<[^>]+\bclass="[^"]*\bpage-nav\b[^"]*"', source
            ))
            public_source_count = len(re.findall(
                r'<section[^>]*\bclass="[^"]*\bsource-list--public\b[^"]*"',
                source,
            ))

            if not has_quick_read:
                violations.append(f'{relative}: missing .quick-read')
            if not has_toc and not has_page_nav:
                violations.append(f'{relative}: missing page navigation')
            if public_source_count != 1:
                violations.append(
                    f'{relative}: expected 1 .source-list--public,'
                    f' found {public_source_count}'
                )

        self.assertEqual(
            violations, [],
            f'{len(violations)} learning page(s) missing required'
            f' sections:\n' + '\n'.join(sorted(violations)),
        )

    # ------------------------------------------------------------------
    # Test 7 -- No prohibited content inside <details>
    # ------------------------------------------------------------------

    @unittest.skip(
        'Feature not yet implemented: no <details> elements exist in the '
        'current site.  Enable this test once collapsible sections are added.'
    )
    def test_no_prohibited_content_in_collapsed_details(self):
        """Content wrapped in <details> must not contain:

        * prohibitions (禁止 / 严禁 / 不得),
        * applicability conditions (适用条件 / 适用范围), or
        * legal-basis citations (法律依据 / 法条依据).
        """
        PROHIBITED = {
            'prohibition': r'禁止|严禁|不得',
            'applicability-condition': r'适用条件|适用范围',
            'legal-basis': r'法律依据|法条依据',
        }
        violations = []
        for html_file in _content_html_files():
            source = html_file.read_text(encoding='utf-8')
            for details_match in re.finditer(
                r'<details[^>]*>(.*?)</details>', source, re.DOTALL,
            ):
                body = details_match.group(1)
                found = [label for label, pattern in PROHIBITED.items()
                         if re.search(pattern, body)]
                if found:
                    violations.append(
                        _violation(html_file,
                                   f'<details> contains: {", ".join(found)}')
                    )
                    break
        self.assertEqual(
            violations, [],
            f'{len(violations)} file(s) have prohibited content inside'
            f' <details>:\n' + '\n'.join(sorted(violations)),
        )

    # ------------------------------------------------------------------
    # Test 8 -- No duplicate source sections
    # ------------------------------------------------------------------

    def test_no_duplicate_source_sections(self):
        """No page may carry both the old .source-list AND the new
        .source-list--public simultaneously."""
        violations = []
        for html_file in _content_html_files():
            source = html_file.read_text(encoding='utf-8')
            has_old = bool(re.search(
                r'<[^>]+\bclass="[^"]*\bsource-list\b(?!-)[^"]*"', source
            ))
            has_new = bool(re.search(
                r'<[^>]+\bclass="[^"]*\bsource-list--public\b[^"]*"', source
            ))
            if has_old and has_new:
                violations.append(_violation(html_file))
        self.assertEqual(
            violations, [],
            f'{len(violations)} file(s) have both .source-list (old) and'
            f' .source-list--public (new):\n' + '\n'.join(sorted(violations)),
        )


if __name__ == '__main__':
    unittest.main()
