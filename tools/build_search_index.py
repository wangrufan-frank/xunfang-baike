"""Build and verify search-index.json from the content inventory articles.

Each record keeps the superset of fields required by the task brief
(title/module/category/desc/keywords/path) and by the search UI
(js/search.js and the inline script in search.html), which additionally
renders ``module`` as a display name and iterates ``tags`` unguarded:

- ``title``: article ``<h1>`` text.
- ``module``: display title resolved from the page ``data-module`` slug
  via data/content-inventory.json (search.html prints it verbatim).
- ``category``: page ``data-category`` value.
- ``desc``: text of the ``.article-summary`` paragraph.
- ``tags``: category label list (search.html calls ``item.tags.map``).
- ``keywords``: ``<meta name="keywords">`` content, comma-split.
- ``path``: site-relative article path; records are sorted by it.

Pages without the ``.article-page`` marker (module indexes, auth pages,
redirect stubs) are never indexed, and the removed rumen/ module cannot
reappear because the inventory is the only source of paths.
"""

from argparse import ArgumentParser
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
INDEX_NAME = 'search-index.json'
FEATURED_DIRECTORY = 'meiyueyixue'
FEATURED_MODULE_TITLE = '本月精选'
_KEYWORD_SEPARATORS = re.compile(r'[,，;；]')
_VOID_TAGS = frozenset({
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
    'meta', 'param', 'source', 'track', 'wbr',
})


class _ArticleParser(HTMLParser):
    """Collect h1, data-module/category, summary, and meta keywords."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self.module = None
        self.category = None
        self.summary = None
        self.keywords = None
        self.has_article_page = False
        self._capture = None
        self._depth = 0
        self._parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = (attributes.get('class') or '').split()
        if (
            tag == 'meta'
            and (attributes.get('name') or '').lower() == 'keywords'
            and self.keywords is None
        ):
            self.keywords = attributes.get('content') or ''
        if 'article-page' in classes and not self.has_article_page:
            self.has_article_page = True
            self.module = attributes.get('data-module')
            self.category = attributes.get('data-category')

        target = None
        if tag == 'h1' and self.title is None:
            target = 'title'
        elif 'article-summary' in classes and self.summary is None:
            target = 'summary'

        if self._capture is not None:
            if tag not in _VOID_TAGS:
                self._depth += 1
        elif target is not None:
            self._capture = target
            self._depth = 1
            self._parts = []

    def handle_endtag(self, tag):
        if self._capture is None or tag in _VOID_TAGS:
            return
        self._depth -= 1
        if self._depth:
            return
        value = ' '.join(''.join(self._parts).split())
        if self._capture == 'title':
            self.title = value
        else:
            self.summary = value
        self._capture = None
        self._parts = []

    def handle_data(self, data):
        if self._capture is not None:
            self._parts.append(data)


def _parse_article(html: str) -> _ArticleParser:
    parser = _ArticleParser()
    parser.feed(html)
    parser.close()
    return parser


def _split_keywords(raw):
    if not raw:
        return []
    return [part.strip() for part in _KEYWORD_SEPARATORS.split(raw) if part.strip()]


def _load_inventory(root: Path) -> tuple[list[str], dict[str, str]]:
    inventory = json.loads(
        (root / 'data' / 'content-inventory.json').read_text(encoding='utf-8')
    )
    paths = []
    module_titles = {FEATURED_DIRECTORY: FEATURED_MODULE_TITLE}
    for module in inventory['modules']:
        module_titles[module['slug']] = module['title']
        for article in module['articles']:
            paths.append(article['path'])
    return paths, module_titles


def _featured_paths(root: Path, known: set[str]) -> list[str]:
    """Monthly-feature article pages: real .article-page files only."""
    featured_dir = root / FEATURED_DIRECTORY
    if not featured_dir.is_dir():
        return []
    paths = []
    for page in sorted(featured_dir.glob('*.html')):
        if page.name == 'index.html':
            continue
        relative = page.relative_to(root).as_posix()
        if relative in known:
            continue
        if _parse_article(page.read_text(encoding='utf-8')).has_article_page:
            paths.append(relative)
    return paths


def build_index(root: Path) -> list[dict]:
    """Return one search record per inventory (and featured) article."""
    root = Path(root)
    paths, module_titles = _load_inventory(root)
    paths = paths + _featured_paths(root, set(paths))
    records = []
    for relative in sorted(paths):
        parsed = _parse_article((root / relative).read_text(encoding='utf-8'))
        module_slug = parsed.module or relative.split('/', 1)[0]
        category = parsed.category or ''
        records.append({
            'title': parsed.title or '',
            'module': module_titles.get(module_slug, module_slug),
            'category': category,
            'desc': parsed.summary or '',
            'tags': [category] if category else [],
            'keywords': _split_keywords(parsed.keywords),
            'path': relative,
        })
    return records


def _record_errors(records: list[dict]) -> list[str]:
    errors = []
    seen_paths = set()
    seen_titles = {}
    for record in records:
        path = record.get('path', '')
        title = record.get('title', '')
        if path in seen_paths:
            errors.append(f'duplicate path: {path}')
        seen_paths.add(path)
        if title in seen_titles:
            errors.append(f'duplicate title: {title} ({seen_titles[title]} vs {path})')
        else:
            seen_titles[title] = path
        if not record.get('desc', '').strip():
            errors.append(f'missing desc: {path}')
    return errors


def check_index(root: Path, records: list[dict]) -> list[str]:
    """Validate records and compare them against search-index.json on disk."""
    root = Path(root)
    errors = _record_errors(records)
    index_path = root / INDEX_NAME
    if not index_path.is_file():
        errors.append(f'{INDEX_NAME} is missing; run python tools/build_search_index.py')
        return errors
    try:
        disk = json.loads(index_path.read_text(encoding='utf-8'))
    except (UnicodeError, json.JSONDecodeError) as error:
        errors.append(f'{INDEX_NAME} is not valid UTF-8 JSON: {error}')
        return errors
    if disk == records:
        return errors

    errors.append(
        f'{INDEX_NAME} is stale; run python tools/build_search_index.py'
    )
    disk_records = disk if isinstance(disk, list) else []
    disk_paths = {
        record.get('path'): record
        for record in disk_records
        if isinstance(record, dict)
    }
    rebuilt_paths = {record['path']: record for record in records}
    for path in sorted(disk_paths.keys() - rebuilt_paths.keys()):
        errors.append(f'{INDEX_NAME} lists removed page: {path}')
    for path in sorted(rebuilt_paths.keys() - disk_paths.keys()):
        errors.append(f'{INDEX_NAME} misses article: {path}')
    for path in sorted(disk_paths.keys() & rebuilt_paths.keys()):
        if disk_paths[path] != rebuilt_paths[path]:
            errors.append(f'{INDEX_NAME} record differs: {path}')
    return errors


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        '--check',
        action='store_true',
        help='compare search-index.json with a fresh build; write nothing',
    )
    args = parser.parse_args(argv)

    records = build_index(args.root)
    if args.check:
        errors = check_index(args.root, records)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print(f'OK: {INDEX_NAME} matches {len(records)} records.')
        return 0

    errors = _record_errors(records)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    index_path = Path(args.root) / INDEX_NAME
    with index_path.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    print(f'Wrote {len(records)} records to {INDEX_NAME}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
