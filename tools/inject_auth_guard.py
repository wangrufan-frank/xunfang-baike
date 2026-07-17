import re
import sys
from pathlib import Path


EXCLUDED_DIRS = {'.git', '.worktrees', '.superpowers', 'deliverables', 'docs'}
AUTH_SCRIPT_RE = re.compile(
    r'<script\b(?=[^>]*\bsrc=["\'][^"\']*js/auth-(?:config|core|guard)\.js["\'])'
    r'[^>]*>\s*</script>\s*',
    re.IGNORECASE,
)


def inject_html(html, root_prefix):
    scripts = (
        f'<script src="{root_prefix}js/auth-config.js"></script>\n'
        f'<script src="{root_prefix}js/auth-core.js"></script>\n'
        f'<script src="{root_prefix}js/auth-guard.js" data-root="{root_prefix}"></script>\n'
    )
    normalized = AUTH_SCRIPT_RE.sub('', html)
    return normalized.replace('</head>', scripts + '</head>', 1)


def runtime_html_pages(root):
    return sorted(
        path
        for path in root.rglob('*.html')
        if not any(part in EXCLUDED_DIRS for part in path.relative_to(root).parts)
    )


def inject_runtime_pages(root):
    changed = []
    for page in runtime_html_pages(root):
        if page.name == 'auth.html' and page.parent == root:
            continue
        root_prefix = '' if page.parent == root else '../'
        original = page.read_text(encoding='utf-8')
        injected = inject_html(original, root_prefix)
        if injected != original:
            page.write_text(injected, encoding='utf-8', newline='')
            changed.append(page)
    return changed


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]).resolve() if args else Path(__file__).resolve().parents[1]
    changed = inject_runtime_pages(root)
    for page in changed:
        print(page.relative_to(root))
    print(f'changed {len(changed)} page(s)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
