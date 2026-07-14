"""Inventory HTML knowledge points and validate the public-source ledger."""

from argparse import ArgumentParser
from datetime import datetime
from difflib import SequenceMatcher
from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tempfile


CONTENT_DIRECTORIES = ('fagui', 'xunlian', 'zhuangbei', 'zoufang')
DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = DEFAULT_ROOT / 'data' / 'public-sources.json'
SOURCE_REQUIRED_FIELDS = (
    'title',
    'publisher',
    'platform',
    'url',
    'verified_at',
    'similarity_note',
    'source_level',
    'last_checked_at',
)
SOURCE_NOTICE = (
    '本索引用于说明核验日期时互联网上存在与本页知识点相似的公开资料，'
    '不表示本站内容均转载自所列网页，也不构成保密审查、法律审查或业务主管部门审核结论。'
    '公开发布仍须执行本单位规定的先审查、后公开程序。'
)
_DIV_TAG = re.compile(r'</?div\b[^>]*>', re.IGNORECASE)
_MANAGED_CITATIONS = re.compile(
    r'<!--\s*source-citations:start\s*-->.*?'
    r'<!--\s*source-citations:end\s*-->',
    re.DOTALL,
)
_MANAGED_INDEX = re.compile(
    r'\n?[ \t]*<!--\s*public-source-index:start\s*-->.*?'
    r'<!--\s*public-source-index:end\s*-->[ \t]*\n?',
    re.DOTALL,
)


class _PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self.points = []
        self._capture = None
        self._depth = 0
        self._parts = []

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get('class', '').split()
        target = None
        if tag == 'h1' and self.title is None:
            target = 'title'
        elif 'step-title' in classes:
            target = 'point'

        if self._capture is not None:
            self._depth += 1
        elif target is not None:
            self._capture = target
            self._depth = 1
            self._parts = []

    def handle_endtag(self, tag):
        if self._capture is None:
            return
        self._depth -= 1
        if self._depth:
            return
        value = ' '.join(''.join(self._parts).split())
        if self._capture == 'title':
            self.title = value
        else:
            self.points.append(value)
        self._capture = None
        self._parts = []

    def handle_data(self, data):
        if self._capture is not None:
            self._parts.append(data)


def _parse_page(html):
    parser = _PageParser()
    parser.feed(html)
    parser.close()
    return parser


def discover_pages(root: Path) -> list[Path]:
    """Return sorted content HTML pages in the four published directories."""
    root = Path(root)
    pages = []
    for directory in CONTENT_DIRECTORIES:
        content_dir = root / directory
        if not content_dir.is_dir():
            continue
        pages.extend(
            path for path in content_dir.glob('*.html')
            if path.name != 'index.html'
        )
    return sorted(pages, key=lambda path: path.relative_to(root).as_posix())


def extract_points(html: str) -> list[str]:
    """Extract visible labels from elements whose class is ``step-title``."""
    return _parse_page(html).points


def _classes(tag):
    match = re.search(r'\bclass\s*=\s*(["\'])(.*?)\1', tag, re.IGNORECASE)
    return match.group(2).split() if match else []


def _div_elements(html, class_name):
    elements = []
    stack = []
    for match in _DIV_TAG.finditer(html):
        if match.group(0).lower().startswith('</'):
            if not stack:
                continue
            opening = stack.pop()
            if class_name in opening['classes']:
                elements.append((opening['start'], opening['end'], match.start(), match.end()))
        else:
            stack.append({
                'start': match.start(),
                'end': match.end(),
                'classes': _classes(match.group(0)),
            })
    return sorted(elements)


def _visible_text(fragment):
    parser = _PageParser()
    parser.feed(f'<div class="step-title">{fragment}</div>')
    parser.close()
    return parser.points[0] if parser.points else ''


def _set_point_attributes(opening_tag, point_id):
    opening_tag = re.sub(
        r'\s+(?:id|data-source-point)\s*=\s*(["\']).*?\1',
        '',
        opening_tag,
        flags=re.IGNORECASE,
    )
    suffix = ' /' if opening_tag.endswith('/>') else ''
    base = opening_tag[:-2] if suffix else opening_tag[:-1]
    return (
        f'{base} id="point-{escape(point_id, quote=True)}" '
        f'data-source-point="{escape(point_id, quote=True)}"{suffix}>'
    )


def render_page(html: str, page: dict, sources: dict[str, dict]) -> str:
    """Render managed citations and a static source index into one HTML page."""
    path = page.get('path', '<unknown>')
    clean = _MANAGED_INDEX.sub('\n', _MANAGED_CITATIONS.sub('', html))
    cards = _div_elements(clean, 'step-card')
    points = sorted(page.get('points', []), key=lambda point: point.get('position', 0))
    if len(cards) != len(points):
        raise ValueError(
            f'{path}: knowledge point 数量 mismatch: HTML {len(cards)}, ledger {len(points)}'
        )

    navs = _div_elements(clean, 'page-nav')
    if len(navs) != 1:
        raise ValueError(f'{path}: expected exactly one .page-nav, found {len(navs)}')

    source_numbers = {}
    source_order = []
    first_refs = {}
    edits = []
    for card, point in zip(cards, points):
        card_start, card_open_end, card_close_start, _ = card
        card_html = clean[card_open_end:card_close_start]
        titles = _div_elements(card_html, 'step-title')
        leads = _div_elements(card_html, 'step-lead')
        if len(titles) != 1 or len(leads) != 1:
            raise ValueError(
                f'{path}: point {point.get("point_id", "<unknown>")} requires one '
                '.step-title and one .step-lead'
            )
        title = titles[0]
        actual_title = _visible_text(card_html[title[1]:title[2]])
        expected_title = point.get('label', '')
        if actual_title != expected_title:
            raise ValueError(
                f'{path}: point title mismatch: {expected_title} -> {actual_title}'
            )

        point_id = point['point_id']
        opening = clean[card_start:card_open_end]
        edits.append((card_start, card_open_end, _set_point_attributes(opening, point_id)))
        citation_links = []
        for source_id in point.get('source_ids', []):
            source = sources.get(source_id)
            if source is None:
                raise ValueError(f'{path}: point {point_id} references missing source {source_id}')
            if source_id not in source_numbers:
                source_numbers[source_id] = len(source_order) + 1
                source_order.append(source_id)
            reference_id = f'source-ref-{point_id}-{source_id}'
            first_refs.setdefault(source_id, reference_id)
            citation_links.append(
                f'<a class="source-citation" id="{escape(reference_id, quote=True)}" '
                f'href="#public-source-{escape(source_id, quote=True)}">'
                f'[{source_numbers[source_id]}]</a>'
            )
        marker = (
            '<!-- source-citations:start -->'
            '<span class="source-citations">' + ' '.join(citation_links) + '</span>'
            '<!-- source-citations:end -->'
        )
        lead_close = card_open_end + leads[0][2]
        edits.append((lead_close, lead_close, marker))

    entries = []
    for source_id in source_order:
        source = sources[source_id]
        published = (
            f'<span class="public-source-published">发布日期：{escape(source["published_at"])}</span>'
            if source.get('published_at') else ''
        )
        entries.append(
            f'<li class="public-source-item" '
            f'id="public-source-{escape(source_id, quote=True)}">'
            f'<span class="public-source-number">[{source_numbers[source_id]}]</span> '
            f'<cite>{escape(source["title"])}</cite>'
            f'<span class="public-source-publisher">发布主体：{escape(source["publisher"])}</span>'
            f'<span class="public-source-platform">平台：{escape(source["platform"])}</span>'
            f'{published}'
            f'<span class="public-source-verified">核验日期：{escape(source["verified_at"])}</span>'
            f'<a href="{escape(source["url"], quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">原文链接</a>'
            f'<p>相似内容说明：{escape(source["similarity_note"])}</p>'
            f'<a href="#{escape(first_refs[source_id], quote=True)}">返回引用位置</a>'
            '</li>'
        )
    source_index = (
        '<!-- public-source-index:start -->\n'
        '<section class="public-source-index" aria-labelledby="public-source-index-title">\n'
        '<h2 id="public-source-index-title">公开资料对照</h2>\n'
        f'<p class="public-source-note">{SOURCE_NOTICE}</p>\n'
        '<ol class="public-source-list">\n' + '\n'.join(entries) + '\n</ol>\n'
        '</section>\n'
        '<!-- public-source-index:end -->\n'
    )
    nav_start = navs[0][0]
    line_start = clean.rfind('\n', 0, nav_start) + 1
    insertion_start = (
        line_start if clean[line_start:nav_start].strip() == '' else nav_start
    )
    edits.append((insertion_start, nav_start, source_index))
    rendered = clean
    for start, end, replacement in sorted(edits, reverse=True):
        rendered = rendered[:start] + replacement + rendered[end:]
    return rendered


def load_ledger(path: Path) -> dict:
    """Load a UTF-8 JSON ledger."""
    with Path(path).open(encoding='utf-8') as stream:
        return json.load(stream)


def _is_empty(value):
    return value is None or value == '' or value == []


def _is_non_empty_string(value):
    return isinstance(value, str) and bool(value.strip())


def _valid_date(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        return False
    return parsed.strftime('%Y-%m-%d') == value


def validate_schema(ledger: dict, allow_pending: bool = False) -> list[str]:
    """Validate ledger structure, identities, references, and source metadata."""
    errors = []
    if not isinstance(ledger, dict):
        return ['ledger must be a JSON object']
    if ledger.get('version') != 1:
        errors.append('version must equal 1')

    pages = ledger.get('pages')
    sources = ledger.get('sources')
    if not isinstance(pages, list):
        errors.append('pages must be a list')
        pages = []
    if not isinstance(sources, list):
        errors.append('sources must be a list')
        sources = []

    source_ids = set()
    for index, source in enumerate(sources, 1):
        prefix = f'source[{index}]'
        if not isinstance(source, dict):
            errors.append(f'{prefix} must be an object')
            continue
        source_id = source.get('source_id')
        if not _is_non_empty_string(source_id):
            errors.append(f'{prefix}.source_id must be a non-empty string')
        elif source_id in source_ids:
            errors.append(f'duplicate source_id: {source_id}')
        else:
            source_ids.add(source_id)

        for field in SOURCE_REQUIRED_FIELDS:
            if _is_empty(source.get(field)):
                errors.append(f'{prefix}.{field} must be non-empty')
        url = source.get('url')
        if not _is_empty(url) and (
            not isinstance(url, str) or not url.startswith('https://')
        ):
            errors.append(f'{prefix}.url must start with https://')
        for field in ('verified_at', 'last_checked_at'):
            value = source.get(field)
            if not _is_empty(value) and not _valid_date(value):
                errors.append(f'{prefix}.{field} must be a valid YYYY-MM-DD date')
        if not allow_pending and source.get('verification_status') != 'verified':
            errors.append(f'{prefix}.verification_status must be verified')

    page_paths = set()
    point_ids = set()
    referenced_ids = []
    for page_index, page in enumerate(pages, 1):
        page_prefix = f'page[{page_index}]'
        if not isinstance(page, dict):
            errors.append(f'{page_prefix} must be an object')
            continue
        path = page.get('path')
        if not _is_non_empty_string(path):
            errors.append(f'{page_prefix}.path must be a non-empty string')
        elif path in page_paths:
            errors.append(f'duplicate page path: {path}')
        else:
            page_paths.add(path)

        points = page.get('points')
        if not isinstance(points, list):
            errors.append(f'{page_prefix}.points must be a list')
            continue
        for point_index, point in enumerate(points, 1):
            prefix = f'{page_prefix}.point[{point_index}]'
            if not isinstance(point, dict):
                errors.append(f'{prefix} must be an object')
                continue
            point_id = point.get('point_id')
            if not _is_non_empty_string(point_id):
                errors.append(f'{prefix}.point_id must be a non-empty string')
            elif point_id in point_ids:
                errors.append(f'duplicate point_id: {point_id}')
            else:
                point_ids.add(point_id)

            ids = point.get('source_ids')
            if not isinstance(ids, list):
                errors.append(f'{prefix}.source_ids must be a list')
                ids = []
            valid_ids = []
            for source_index, source_id in enumerate(ids, 1):
                if not _is_non_empty_string(source_id):
                    errors.append(
                        f'{prefix}.source_ids[{source_index}] must be a '
                        'non-empty string'
                    )
                    continue
                valid_ids.append(source_id)
            referenced_ids.extend((prefix, source_id) for source_id in valid_ids)
            if not allow_pending:
                if point.get('coverage_status') != 'verified':
                    errors.append(f'{prefix}.coverage_status must be verified')
                if not valid_ids:
                    errors.append(f'{prefix}.source_ids must contain at least one source')

    for prefix, source_id in referenced_ids:
        if source_id not in source_ids:
            errors.append(f'{prefix}.source_ids references missing source_id: {source_id}')
    return errors


def compare_page_points(html: str, page: dict) -> list[str]:
    """Report ledger labels that differ from HTML labels at each position."""
    html_points = extract_points(html)
    ledger_points = page.get('points', []) if isinstance(page, dict) else []
    ledger_entries = sorted(
        (point.get('position'), point.get('label', ''))
        for point in ledger_points
        if isinstance(point, dict)
    )
    ledger_labels = [label for _, label in ledger_entries]
    errors = []
    path = page.get('path', '<unknown>') if isinstance(page, dict) else '<unknown>'
    matcher = SequenceMatcher(None, ledger_labels, html_points, autojunk=False)
    for tag, ledger_start, ledger_end, html_start, html_end in matcher.get_opcodes():
        if tag == 'equal':
            continue
        ledger_chunk = ledger_entries[ledger_start:ledger_end]
        html_chunk = html_points[html_start:html_end]
        if tag == 'replace' and len(ledger_chunk) == len(html_chunk):
            for (position, old_label), new_label in zip(ledger_chunk, html_chunk):
                errors.append(
                    f'{path}: point renamed at position {position}: '
                    f'{old_label} -> {new_label}'
                )
            continue
        if tag in ('delete', 'replace'):
            for position, label in ledger_chunk:
                errors.append(
                    f'{path}: HTML removed point at position {position}: {label}'
                )
        if tag in ('insert', 'replace'):
            for offset, label in enumerate(html_chunk, html_start + 1):
                errors.append(
                    f'{path}: HTML added point at position {offset}: {label}'
                )
    return errors


def validate_ledger(
    root: Path, ledger: dict, allow_pending: bool = False
) -> list[str]:
    """Validate schema and ensure ledger pages match the current HTML inventory."""
    root = Path(root)
    errors = validate_schema(ledger, allow_pending=allow_pending)
    discovered = {
        page.relative_to(root).as_posix(): page
        for page in discover_pages(root)
    }
    ledger_pages = {}
    pages = ledger.get('pages', []) if isinstance(ledger, dict) else []
    for page in pages if isinstance(pages, list) else []:
        if isinstance(page, dict) and _is_non_empty_string(page.get('path')):
            ledger_pages.setdefault(page['path'], page)

    for path in sorted(discovered.keys() - ledger_pages.keys()):
        errors.append(f'HTML page missing from ledger: {path}')
    for path in sorted(ledger_pages.keys() - discovered.keys()):
        errors.append(f'ledger page missing from HTML inventory: {path}')
    for path in sorted(discovered.keys() & ledger_pages.keys()):
        html = discovered[path].read_text(encoding='utf-8')
        page = ledger_pages[path]
        parsed = _parse_page(html)
        if parsed.title != page.get('title'):
            errors.append(
                f'{path}: page title differs: {page.get("title", "")} -> '
                f'{parsed.title or ""}'
            )
        errors.extend(compare_page_points(html, page))
    return errors


def publish_errors(ledger: dict) -> list[str]:
    """Return publication-review errors without changing the ledger."""
    errors = []
    pages = ledger.get('pages', []) if isinstance(ledger, dict) else []
    for index, page in enumerate(pages if isinstance(pages, list) else [], 1):
        if not isinstance(page, dict):
            errors.append(f'page[{index}] must be an object for publication')
            continue
        prefix = f'page[{index}]'
        if page.get('review_status') != 'approved':
            errors.append(f'{prefix}.review_status must be approved')
        for field in ('reviewed_by', 'reviewed_at'):
            if _is_empty(page.get(field)):
                errors.append(f'{prefix}.{field} must be non-empty')
    return errors


def _print_errors(errors):
    for error in errors:
        print(error, file=sys.stderr)


def _build_parser():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        'command',
        choices=('inventory', 'check', 'check-publish', 'write', 'report'),
    )
    parser.add_argument('ledger', nargs='?', type=Path)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--allow-pending', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', type=Path)
    return parser


def _write_text_atomic(path, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf-8', newline='', dir=path.parent,
            prefix=f'.{path.name}.', suffix='.tmp', delete=False,
        ) as stream:
            stream.write(content)
            temporary = Path(stream.name)
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    args = _build_parser().parse_args(argv)
    if args.command == 'inventory':
        pages = discover_pages(args.root)
        ledger_pages = []
        category_counts = {
            directory: {'pages': 0, 'points': 0}
            for directory in CONTENT_DIRECTORIES
        }
        for page in pages:
            parsed = _parse_page(page.read_text(encoding='utf-8'))
            counts = category_counts[page.parent.name]
            counts['pages'] += 1
            counts['points'] += len(parsed.points)
            page_id = f'{page.parent.name}-{page.stem}'
            ledger_pages.append({
                'page_id': page_id,
                'path': page.relative_to(args.root).as_posix(),
                'title': parsed.title,
                'review_status': 'pending',
                'reviewed_by': None,
                'reviewed_at': None,
                'points': [
                    {
                        'point_id': f'{page_id}-{position:02d}',
                        'position': position,
                        'label': label,
                        'source_ids': [],
                        'coverage_status': 'pending',
                        'coverage_note': '',
                    }
                    for position, label in enumerate(parsed.points, 1)
                ],
            })
        points = sum(counts['points'] for counts in category_counts.values())
        if args.output:
            ledger = {'version': 1, 'pages': ledger_pages, 'sources': []}
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(ledger, ensure_ascii=False, indent=2) + '\n',
                encoding='utf-8',
            )
            print(
                f'Wrote {len(pages)} pages and {points} points; '
                'all coverage statuses are pending.'
            )
            return 0
        print(f'{len(pages)} pages, {points} points')
        for directory, counts in category_counts.items():
            print(
                f'{directory}: {counts["pages"]} pages, '
                f'{counts["points"]} points'
            )
        return 0

    ledger_path = args.ledger or DEFAULT_LEDGER
    try:
        ledger = load_ledger(ledger_path)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f'cannot load ledger {ledger_path}: {error}', file=sys.stderr)
        return 1

    allow_pending = args.allow_pending and args.command != 'write'
    errors = validate_ledger(args.root, ledger, allow_pending=allow_pending)
    if args.command == 'check-publish':
        errors.extend(publish_errors(ledger))
    if errors:
        _print_errors(errors)
        return 1

    if args.command == 'check':
        pages = ledger['pages']
        point_count = sum(len(page['points']) for page in pages)
        pending_count = sum(
            point.get('coverage_status') == 'pending'
            for page in pages
            for point in page['points']
        )
        print(
            f'PASS: {len(pages)} pages, {point_count} points; '
            f'{pending_count} points pending source verification.'
        )
    elif args.command == 'write':
        sources = {source['source_id']: source for source in ledger['sources']}
        rendered_pages = []
        try:
            for page in ledger['pages']:
                path = args.root / page['path']
                original = path.read_text(encoding='utf-8')
                rendered = render_page(original, page, sources)
                rendered_pages.append((path, page['path'], original, rendered))
        except (OSError, UnicodeError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1

        changed = [item for item in rendered_pages if item[2] != item[3]]
        for _, relative, _, _ in changed:
            print(f'CHANGED: {relative}')
        if args.check:
            print(f'CHECK: {len(changed)} of {len(rendered_pages)} pages would change.')
            return 1 if changed else 0
        try:
            for path, _, _, rendered in changed:
                _write_text_atomic(path, rendered)
        except OSError as error:
            print(f'cannot write generated HTML: {error}', file=sys.stderr)
            return 1
        print(f'WROTE: {len(changed)} of {len(rendered_pages)} pages changed.')
    elif args.command == 'report':
        point_count = sum(len(page.get('points', [])) for page in ledger['pages'])
        print(
            f'{len(ledger["pages"])} pages, {point_count} points, '
            f'{len(ledger["sources"])} sources'
        )
    return 0


if __name__ == '__main__':
    sys.exit(main())
