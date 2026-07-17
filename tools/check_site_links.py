"""Check internal links, anchors, and asset references across site HTML.

Scans every runtime HTML page (excluding VCS, tooling, and documentation
directories), collects ``href``/``src`` attributes plus ``meta`` refresh
targets, and reports:

- local references whose target file does not exist (exact case, so the
  check also holds on case-sensitive static hosting),
- ``#fragment`` references whose target page lacks a matching ``id=`` or
  ``<a name=>`` anchor,
- external URLs that do not even parse as absolute http(s) URLs
  (format check only; no network access).
"""

from argparse import ArgumentParser
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {
    '.git', '.worktrees', '.superpowers', 'deliverables', 'docs',
    'miniprogram', 'node_modules', '__pycache__', 'tests', 'tools', 'data',
}
TARGET_EXCLUDED_DIRS = {'.git', '.worktrees', 'node_modules', '__pycache__'}
SKIPPED_SCHEMES = {'mailto', 'tel', 'javascript', 'data'}
_REFRESH_URL = re.compile(r'url\s*=\s*[\'"]?([^\'"]+)', re.IGNORECASE)


class _LinkParser(HTMLParser):
    """Collect link-like attributes and anchor targets from one page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        identifier = attributes.get('id')
        if identifier:
            self.anchors.add(identifier)
        if tag == 'a' and attributes.get('name'):
            self.anchors.add(attributes['name'])
        for attribute in ('href', 'src'):
            value = attributes.get(attribute)
            if value is not None:
                self.references.append(value)
        if tag == 'meta' and (attributes.get('http-equiv') or '').lower() == 'refresh':
            match = _REFRESH_URL.search(attributes.get('content') or '')
            if match:
                self.references.append(match.group(1).strip())


def _parse_page(path: Path) -> _LinkParser:
    parser = _LinkParser()
    parser.feed(path.read_text(encoding='utf-8'))
    parser.close()
    return parser


def _walk_files(root: Path, excluded: set[str]) -> set[str]:
    """Exact-case relative POSIX paths of every file below ``root``."""
    files = set()
    for current, directories, names in os.walk(root):
        directories[:] = sorted(set(directories) - excluded)
        relative = Path(current).relative_to(root)
        for name in names:
            files.add((relative / name).as_posix().removeprefix('./'))
    return files


def discover_pages(root: Path) -> list[Path]:
    """Runtime HTML pages to scan, sorted for stable reports."""
    root = Path(root)
    return sorted(
        (
            page for page in root.rglob('*.html')
            if not EXCLUDED_DIRS.intersection(page.relative_to(root).parts)
        ),
        key=lambda page: page.relative_to(root).as_posix(),
    )


def check_site(root: Path) -> list[str]:
    """Return one error string per broken reference; empty when clean."""
    root = Path(root)
    existing = _walk_files(root, TARGET_EXCLUDED_DIRS)
    pages = discover_pages(root)
    parsed = {page.relative_to(root).as_posix(): _parse_page(page) for page in pages}
    anchor_cache = {
        relative: parser.anchors for relative, parser in parsed.items()
    }

    def anchors_of(relative: str) -> set[str]:
        if relative not in anchor_cache:
            anchor_cache[relative] = _parse_page(root / relative).anchors
        return anchor_cache[relative]

    errors = []
    for relative, parser in sorted(parsed.items()):
        page_dir = Path(relative).parent
        for value in parser.references:
            reference = value.strip()
            if not reference:
                continue
            parts = urlsplit(reference)
            if parts.scheme in SKIPPED_SCHEMES:
                continue
            if parts.scheme in ('http', 'https') or (not parts.scheme and parts.netloc):
                if not (parts.scheme and parts.netloc):
                    errors.append(f'{relative}: invalid external URL -> {reference}')
                continue
            if parts.scheme:
                errors.append(f'{relative}: unsupported URL scheme -> {reference}')
                continue

            path_part = unquote(parts.path)
            if not path_part:
                target = relative
            else:
                combined = (page_dir / path_part).as_posix()
                segments = []
                escaped = False
                for segment in combined.split('/'):
                    if segment in ('', '.'):
                        continue
                    if segment == '..':
                        if not segments:
                            escaped = True
                            break
                        segments.pop()
                    else:
                        segments.append(segment)
                if escaped:
                    errors.append(f'{relative}: reference escapes site root -> {reference}')
                    continue
                target = '/'.join(segments)
                if path_part.endswith('/') or not target:
                    target = f'{target}/index.html'.lstrip('/')
                if target not in existing:
                    errors.append(f'{relative}: broken link -> {reference}')
                    continue
            if parts.fragment and target.endswith('.html'):
                if parts.fragment not in anchors_of(target):
                    errors.append(
                        f'{relative}: missing anchor #{parts.fragment} -> {target}'
                    )
    return errors


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args(argv)

    errors = check_site(args.root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f'{len(errors)} broken reference(s) found.', file=sys.stderr)
        return 1
    pages = discover_pages(args.root)
    print(f'OK: {len(pages)} pages checked; no broken links or anchors.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
