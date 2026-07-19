#!/usr/bin/env python3
"""Phase C: Remove old .source-list from HTML files and inject renderer markers.

1. Removes <section class="source-list">...</section> blocks from all third-level HTML
2. Before .page-nav (or before </article>/</main>), injects:
   - <!-- source-citations:start --><!-- source-citations:end -->
   - <!-- public-source-index:start -->
   - <!-- public-source-index:end -->
3. Runs the renderer to inject actual source blocks
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIRS = ('fagui', 'xunlian', 'zhuangbei', 'zoufang', 'jingqing', 'qinwu', 'meiyueyixue')

# Pattern to match old .source-list sections (not .source-list--public)
OLD_SOURCE_LIST = re.compile(
    r'[ \t]*<section[^>]*\bclass="(?:[^"]*\s)?source-list(?:\s[^"]*)?"[^>]*>'
    r'.*?'
    r'</section>\s*',
    re.DOTALL,
)

# Pattern to find insertion point
PAGE_NAV_RE = re.compile(r'(<nav[^>]*\bclass="[^"]*\bpage-nav\b)', re.DOTALL)


def discover_pages(root: Path) -> list[Path]:
    root = Path(root)
    pages = []
    for directory in CONTENT_DIRS:
        content_dir = root / directory
        if not content_dir.is_dir():
            continue
        pages.extend(
            path for path in content_dir.glob('*.html')
            if path.name != 'index.html'
        )
    return sorted(pages, key=lambda path: path.relative_to(root).as_posix())


def has_markers(html: str) -> bool:
    return ('<!-- public-source-index:start -->' in html and
            '<!-- public-source-index:end -->' in html)


def inject_markers(html: str) -> str:
    """Inject source markers before .page-nav, or before </article>/</main>."""
    if '<!-- public-source-index:start -->' in html:
        return html  # Already has markers

    # Try .page-nav first
    match = PAGE_NAV_RE.search(html)
    if match:
        pos = match.start()
        # Find the beginning of the line containing .page-nav
        line_start = html.rfind('\n', 0, pos) + 1
        # Check if there's whitespace before it on the line
        if html[line_start:pos].strip() == '':
            insert_pos = line_start
        else:
            insert_pos = pos
    else:
        # Fall back to before </article> or </main>
        for tag in ('</article>', '</main>'):
            idx = html.find(tag)
            if idx != -1:
                insert_pos = idx
                break
        else:
            return html  # No insertion point found

    marker_block = (
        '<!-- source-citations:start -->'
        '<!-- source-citations:end -->\n'
        '<!-- public-source-index:start -->\n'
        '<!-- public-source-index:end -->\n'
    )
    return html[:insert_pos] + marker_block + html[insert_pos:]


def main():
    root = ROOT
    pages = discover_pages(root)
    print(f'Found {len(pages)} third-level HTML pages')

    # Step 1: Remove old .source-list sections
    removed_count = 0
    failed = []
    for page_path in pages:
        original = page_path.read_text(encoding='utf-8')
        modified = OLD_SOURCE_LIST.sub('\n', original)

        # Step 2: Inject markers if not present
        modified = inject_markers(modified)

        if modified != original:
            try:
                page_path.write_text(modified, encoding='utf-8')
                if OLD_SOURCE_LIST.search(original):
                    removed_count += 1
                    print(f'  FIXED: {page_path.relative_to(root).as_posix()}')
            except OSError as e:
                failed.append(str(page_path))
                print(f'  ERROR writing {page_path}: {e}', file=sys.stderr)

    print(f'\nRemoved .source-list from {removed_count} pages')
    if failed:
        print(f'WARNING: {len(failed)} files failed to write')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
