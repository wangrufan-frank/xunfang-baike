"""Build full-text legal pages from data/legal-documents.json.

Generates:
- fagui/{id}.html — complete statute text pages replacing existing stubs
- data/legal-basis-cards.json — HTML card snippets for injection into enforcement pages

Usage:
  python tools/build_legal_pages.py              # generate all pages
  python tools/build_legal_pages.py --check      # dry-run, validate only
  python tools/build_legal_pages.py --output-dir fagui/  # custom output dir
"""

from argparse import ArgumentParser
from html import escape
import json
import os
import sys
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = 'fagui'


# ---- Template fragments ----

def _safe_str(value):
    """Return '' for None, otherwise str(value)."""
    if value is None:
        return ''
    return str(value)


def _format_date(value):
    """Format a YYYY-MM-DD date for display, or return empty string."""
    if not value:
        return ''
    return value


def _meta_keywords(doc):
    """Comma-separated keywords for <meta name="keywords">."""
    kws = doc.get('keywords', [])
    if not kws:
        return ''
    return '，'.join(str(k) for k in kws)


def _status_badge(status):
    """Return a small status tag HTML snippet."""
    if not status:
        return ''
    cls = 'status-valid' if status in ('现行有效',) else 'status-other'
    return f'<span class="status-tag {cls}">{escape(status)}</span>'


def _breadcrumb(title):
    return f'''  <a href="../index.html">首页</a> &gt;
  <a href="index.html">执法规范</a> &gt;
  <a href="index.html#legal-library">法律法规库</a> &gt;
  <span class="current">{escape(title)}</span>'''


def _title_block(doc):
    doc_type = _safe_str(doc.get('document_type'))
    status = _safe_str(doc.get('status'))
    summary = _safe_str(doc.get('description'))
    return f'''  <header class="page-title">
    <div class="title-tags">
      <span class="doc-type-tag">{escape(doc_type)}</span>
      {_status_badge(status)}
    </div>
    <h1>{escape(doc['title'])}</h1>
    <p class="article-summary">{escape(summary)}</p>
  </header>'''


def _version_card(doc):
    """Render the version metadata card."""
    lines = []
    authority = _safe_str(doc.get('authority'))
    doc_number = _safe_str(doc.get('document_number'))
    promulgated = _format_date(doc.get('promulgated_at'))
    effective = _format_date(doc.get('effective_at'))
    version_label = _safe_str(doc.get('version_label'))
    source_url = _safe_str(doc.get('source_url'))
    source_title = _safe_str(doc.get('source_title'))
    verified = _format_date(doc.get('verified_at'))

    if authority:
        lines.append(f'<li><strong>发布主体：</strong>{escape(authority)}</li>')
    if doc_number:
        lines.append(f'<li><strong>文号：</strong>{escape(doc_number)}</li>')
    if promulgated:
        lines.append(f'<li><strong>公布日期：</strong>{escape(promulgated)}</li>')
    if effective:
        lines.append(f'<li><strong>施行日期：</strong>{escape(effective)}</li>')
    if version_label:
        lines.append(f'<li><strong>版本：</strong>{escape(version_label)}</li>')
    if source_url:
        lines.append(
            f'<li><strong>官方来源：</strong>'
            f'<a href="{escape(source_url, quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{escape(source_title or "原文链接")}</a></li>'
        )
    if verified:
        lines.append(f'<li><strong>核验日期：</strong>{escape(verified)}</li>')

    return f'''  <section class="version-meta-card">
    <h2>版本与效力信息</h2>
    <ul>
      {''.join(f'      {line}\n' for line in lines) if lines else ''}    </ul>
  </section>'''


def _xunfang_nav(doc):
    """Render quick-nav to articles relevant to xunfang (patrol duty)."""
    article_nums = doc.get('xunfang_articles', [])
    if not article_nums:
        return ''
    items = []
    for num in article_nums:
        # Find the article label
        label = f'第{num}条'
        items.append(
            f'      <li><a href="#article-{num}">{label}</a></li>'
        )
    return f'''  <section class="xunfang-quick-nav">
    <h2>巡防常用条款</h2>
    <ul class="xunfang-nav-list">
{''.join(f'{item}\n' for item in items)}    </ul>
  </section>'''


def _toc(doc):
    """Render a table of contents from chapters and articles."""
    chapters = doc.get('chapters', [])
    if not chapters:
        return ''
    items = []
    for ch in chapters:
        ch_num = _safe_str(ch.get('number'))
        ch_title = _safe_str(ch.get('title'))
        items.append(
            f'<li class="toc-chapter"><strong>{escape(ch_num)} {escape(ch_title)}</strong>'
        )
        for art in ch.get('articles', []):
            art_num = art.get('number')
            art_label = _safe_str(art.get('label'))
            items.append(
                f'<ul><li class="toc-article">'
                f'<a href="#article-{art_num}">{escape(art_label)}</a>'
                f'</li></ul>'
            )
        items.append('</li>')
    return f'''  <section class="legal-toc">
    <h2>目录</h2>
    <ol class="legal-toc-list">
      {''.join(f'      {item}\n' for item in items)}    </ol>
  </section>'''


def _article_html(art):
    """Render a single article as an HTML block with a stable anchor."""
    num = art.get('number')
    label = _safe_str(art.get('label'))
    paragraphs = art.get('paragraphs', [])
    paras_html = '\n'.join(
        f'      <p>{escape(p)}</p>' for p in paragraphs
    )
    return (
        f'    <div class="legal-article" id="article-{num}">\n'
        f'      <h3 class="article-heading">{escape(label)}</h3>\n'
        f'{paras_html}\n'
        f'    </div>'
    )


def _full_text(doc):
    """Render complete statute text with chapters and articles."""
    chapters = doc.get('chapters', [])
    if not chapters:
        return '''  <section class="content-section">
    <h2>法规全文</h2>
    <p>法规正文待补充。参见官方来源获取完整文本。</p>
  </section>'''
    sections = []
    for ch in chapters:
        ch_num = _safe_str(ch.get('number'))
        ch_title = _safe_str(ch.get('title'))
        articles = ch.get('articles', [])
        arts_html = '\n'.join(_article_html(a) for a in articles)
        sections.append(
            f'  <section class="content-section chapter-block">\n'
            f'    <h2 class="chapter-heading">{escape(ch_num)} {escape(ch_title)}</h2>\n'
            f'{arts_html}\n'
            f'  </section>'
        )
    return '\n'.join(sections)


def _source_index(doc):
    """Render the public-source-index block."""
    source_url = _safe_str(doc.get('source_url'))
    if not source_url:
        return ''
    title = doc['title']
    authority = _safe_str(doc.get('authority'))
    source_title = _safe_str(doc.get('source_title', '原文链接'))
    promulgated = _format_date(doc.get('promulgated_at'))
    verified = _format_date(doc.get('verified_at'))
    doc_num = _safe_str(doc.get('document_number'))

    published_span = ''
    if promulgated:
        published_span = f'<span class="public-source-published">发布日期：{escape(promulgated)}</span>'

    cite_title = escape(title)
    if doc_num:
        cite_title = f'{cite_title}（{escape(doc_num)}）'

    note_parts = ['行政法规正文']
    if doc_num:
        note_parts.append(f'文号{escape(doc_num)}')
    note_text = '规定警械使用条件、武器使用情形和法律责任。'

    return f'''<!-- public-source-index:start -->
<section class="public-source-index" aria-labelledby="public-source-index-title">
<h2 id="public-source-index-title">公开资料对照</h2>
<p class="public-source-note">本索引用于说明核验日期时互联网上存在与本页知识点相似的公开资料，不表示本站内容均转载自所列网页，也不构成保密审查、法律审查或业务主管部门审核结论。公开发布仍须执行本单位规定的先审查、后公开程序。</p>
<ol class="public-source-list">
<li class="public-source-item" id="public-source-{escape(doc['id'])}"><span class="public-source-number">[1]</span> <cite>{cite_title}</cite><span class="public-source-publisher">发布主体：{escape(authority)}</span><span class="public-source-platform">平台：{escape(source_title)}</span>{published_span}<span class="public-source-verified">核验日期：{escape(verified)}</span><a href="{escape(source_url, quote=True)}" target="_blank" rel="noopener noreferrer">原文链接</a><p>相似内容说明：{note_text}</p></li>
</ol>
</section>
<!-- public-source-index:end -->'''


def _related_links(doc):
    """Render related enforcement page links."""
    related = doc.get('related_pages', [])
    if not related:
        return ''
    links = []
    for path in related:
        # Extract filename for display, use as link text if simple
        fname = path.split('/')[-1].replace('.html', '')
        # We need a display name — use the filename for now
        links.append(f'      <li><a href="../{path}">{escape(fname)}</a></li>')
    return f'''
  <nav class="related-links" aria-label="相关内容">
    <h2>相关内容</h2>
    <ul>
{''.join(f'{link}\n' for link in links)}    </ul>
  </nav>'''


def _prev_next(doc, doc_order):
    """Render prev/next page nav based on document order list."""
    idx = doc_order.index(doc['id']) if doc['id'] in doc_order else -1
    if idx < 0:
        return ''
    prev_id = doc_order[idx - 1] if idx > 0 else None
    next_id = doc_order[idx + 1] if idx < len(doc_order) - 1 else None

    prev_html = ''
    next_html = ''
    if prev_id:
        prev_html = f'    <a href="{prev_id}.html">← 上一篇</a>'
    else:
        prev_html = '    <a href="index.html">← 返回执法规范</a>'
    if next_id:
        next_html = f'    <a href="{next_id}.html">下一篇 →</a>'
    else:
        next_html = '    <a href="index.html">↑ 返回执法规范</a>'

    return f'''
  <nav class="page-nav" aria-label="文章导航">
{prev_html}
{next_html}
  </nav>'''


def _page_head(doc):
    """Render <head> section for a legal page."""
    title = escape(doc['title'])
    kws = _meta_keywords(doc)
    desc = escape(_safe_str(doc.get('description')))
    kw_meta = f'\n<meta name="keywords" content="{escape(kws, quote=True)}">' if kws else ''
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">{kw_meta}
<meta name="description" content="{escape(desc, quote=True)}">
<title>{title} — 巡防百科</title>
<link rel="stylesheet" href="../css/style.css">
<script src="../js/auth-config.js"></script>
<script src="../js/auth-core.js"></script>
<script src="../js/auth-guard.js" data-root="../"></script>
</head>'''


def _page_foot():
    return '''
<script src="../js/theme.js"></script>
<script src="../js/nav.js"></script>
<script src="../js/main.js"></script>
<script src="../js/search.js"></script>
</body>
</html>'''


def _build_page(doc, doc_order):
    """Assemble a complete HTML page for one legal document."""
    parts = [
        _page_head(doc),
        '<body>',
        '',
        '<div id="nav-placeholder"></div>',
        '',
        '<div class="breadcrumb">',
        _breadcrumb(doc['title']),
        '</div>',
        '',
        f'<main class="page-container article-page" data-module="fagui" data-category="法律法规库">',
        _title_block(doc),
        '',
        '<article class="article-content">',
    ]

    # Quick nav for xunfang-relevant articles
    xnav = _xunfang_nav(doc)
    if xnav:
        parts.append(xnav)
        parts.append('')

    # Version metadata
    parts.append(_version_card(doc))
    parts.append('')

    # Table of contents
    toc = _toc(doc)
    if toc:
        parts.append(toc)
        parts.append('')

    # Full text
    parts.append(_full_text(doc))
    parts.append('')

    # Source index
    si = _source_index(doc)
    if si:
        parts.append(si)
        parts.append('')

    parts.append('</article>')
    parts.append('')

    # Related links
    rl = _related_links(doc)
    if rl:
        parts.append(rl)
        parts.append('')

    # Page nav
    pn = _prev_next(doc, doc_order)
    if pn:
        parts.append(pn)
        parts.append('')

    parts.append('</main>')
    parts.append(_page_foot())

    return '\n'.join(parts)


# ---- Card snippet generation ----

def _build_card(doc, art):
    """Generate a .legal-basis-card HTML snippet for one article."""
    title = doc['title']
    doc_id = doc['id']
    doc_num = _safe_str(doc.get('document_number'))
    source_url = _safe_str(doc.get('source_url'))
    source_title = _safe_str(doc.get('source_title'))
    verified = _format_date(doc.get('verified_at'))

    art_label = _safe_str(art.get('label'))
    art_num = art.get('number')
    paragraphs = art.get('paragraphs', [])
    text = '\n'.join(
        f'      <p>{escape(p)}</p>' for p in paragraphs
    )

    source_line = ''
    source_parts = []
    if source_url:
        source_parts.append(
            f'来源：<a href="{escape(source_url, quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">{escape(source_title or "官方原文")}</a>'
        )
    if verified:
        source_parts.append(f'核验日期：{escape(verified)}')
    if source_parts:
        source_line = f'    <p class="legal-source">{escape(" | ").join(source_parts)}</p>\n'

    deep_link = f'    <p class="legal-deep-link"><a href="{escape(doc_id)}.html#article-{art_num}">查看{escape(title)}全文</a></p>\n'

    return (
        f'<div class="legal-basis-card">\n'
        f'  <h3>法律依据</h3>\n'
        f'  <p class="legal-title">《{escape(title)}》{escape(art_label)}</p>\n'
        f'  <blockquote class="legal-text">\n'
        f'{text}\n'
        f'  </blockquote>\n'
        f'  <p class="legal-note"><!-- applicability-note --></p>\n'
        f'{source_line}'
        f'{deep_link}'
        f'</div>'
    )


def _build_cards_map(documents):
    """Build the card snippet map for all documents that have chapters."""
    cards = {}
    for doc in documents:
        for ch in doc.get('chapters', []):
            for art in ch.get('articles', []):
                key = f'{doc["id"]}/{art["number"]}'
                cards[key] = _build_card(doc, art)
    return cards


# ---- Validation ----

def _validate_document(doc, index):
    """Validate a single document; returns list of error strings."""
    errors = []
    prefix = f'doc[{index}] ({doc.get("id", "?")})'
    required = [
        'id', 'title', 'document_type', 'authority', 'status',
    ]
    for field in required:
        if not doc.get(field):
            errors.append(f'{prefix}: missing required field "{field}"')
    if 'chapters' not in doc:
        errors.append(f'{prefix}: missing "chapters"')
        return errors

    chapters = doc['chapters']
    if not chapters:
        return errors

    # Collect article numbers across all chapters
    article_numbers = []
    for ch in chapters:
        for art in ch.get('articles', []):
            num = art.get('number')
            if num is None:
                continue
            article_numbers.append(num)
            label = art.get('label', '')
            paras = art.get('paragraphs', [])
            if not isinstance(paras, list) or len(paras) == 0:
                errors.append(
                    f'{prefix}: article {num} ({label}) has no paragraphs'
                )

    # Check duplicates
    seen = set()
    dups = []
    for n in article_numbers:
        if n in seen:
            dups.append(n)
        seen.add(n)
    if dups:
        errors.append(f'{prefix}: duplicate article numbers: {dups}')

    # Check sequential (skip for partial documents)
    if article_numbers and not doc.get('partial'):
        expected = list(range(article_numbers[0], article_numbers[-1] + 1))
        if article_numbers != expected:
            errors.append(
                f'{prefix}: article numbers not sequential. '
                f'Got {article_numbers[0]}..{article_numbers[-1]} '
                f'({len(article_numbers)} articles), '
                f'expected {expected[0]}..{expected[-1]} ({len(expected)} articles)'
            )

        # Check first and last
        if article_numbers[0] != 1:
            errors.append(
                f'{prefix}: first article is {article_numbers[0]}, expected 1'
            )

    return errors


def validate_all(documents):
    """Validate all documents; returns (list of errors, total_articles)."""
    errors = []
    total = 0
    for i, doc in enumerate(documents):
        errs = _validate_document(doc, i)
        errors.extend(errs)
        for ch in doc.get('chapters', []):
            total += len(ch.get('articles', []))
    return errors, total


# ---- Search index data generation ----

def build_search_entries(documents):
    """Generate records consumable by build_search_index.py.

    Each record: title, module, category, desc, tags, keywords, path
    """
    entries = []
    for doc in documents:
        entries.append({
            'title': doc['title'],
            'module': 'fagui',
            'category': '法律法规库',
            'desc': doc.get('description', ''),
            'tags': ['法律法规库'],
            'keywords': doc.get('keywords', []),
            'path': f'fagui/{doc["id"]}.html',
        })
    return entries


# ---- Main ----

def _write_atomic(path, content):
    """Write content to path atomically using a temp file."""
    tmp = path.with_suffix(path.suffix + '.tmp')
    try:
        with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        os.replace(str(tmp), str(path))
    finally:
        if tmp.exists():
            tmp.unlink()


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='dry-run: validate only, do not write files')
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT,
                        help='project root directory')
    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
                        help='output directory relative to root (default: fagui/)')
    args = parser.parse_args(argv)

    root = Path(args.root)
    data_file = root / 'data' / 'legal-documents.json'

    if not data_file.is_file():
        print(f'ERROR: {data_file} not found', file=sys.stderr)
        return 1

    try:
        data = json.loads(data_file.read_text(encoding='utf-8'))
    except (UnicodeError, json.JSONDecodeError) as e:
        print(f'ERROR: cannot parse {data_file}: {e}', file=sys.stderr)
        return 1

    if not isinstance(data, dict) or data.get('version') != 1:
        print('ERROR: legal-documents.json must have version=1', file=sys.stderr)
        return 1

    documents = data.get('documents', [])
    if not isinstance(documents, list) or not documents:
        print('ERROR: documents must be a non-empty list', file=sys.stderr)
        return 1

    # Validate
    errors, total_articles = validate_all(documents)
    if errors:
        for e in errors:
            print(f'VALIDATION ERROR: {e}', file=sys.stderr)

    # Document order for prev/next nav
    doc_order = [d['id'] for d in documents]
    doc_with_chapters = sum(1 for d in documents if d.get('chapters'))

    if args.check:
        print(f'CHECK: {len(documents)} documents, {doc_with_chapters} with chapters, '
              f'{total_articles} articles')
        print(f'CHECK: {len(errors)} validation errors')
        if errors:
            return 1
        print('CHECK: all validations passed.')
        return 0

    if errors:
        print(f'\n{len(errors)} validation errors — aborting build.',
              file=sys.stderr)
        return 1

    # Generate pages
    output_dir = root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    for doc in documents:
        html = _build_page(doc, doc_order)
        path = output_dir / f'{doc["id"]}.html'
        _write_atomic(path, html)
        generated += 1

    # Generate card snippets
    cards = _build_cards_map(documents)
    cards_file = root / 'data' / 'legal-basis-cards.json'
    with open(cards_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(cards, ensure_ascii=False, indent=2) + '\n')

    # Generate search entries
    search_entries = build_search_entries(documents)
    search_file = root / 'data' / 'legal-search-entries.json'
    with open(search_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(search_entries, ensure_ascii=False, indent=2) + '\n')

    print(f'Generated {generated} pages, {total_articles} articles, '
          f'{len(cards)} cards')
    print(f'  Pages: {output_dir}/')
    print(f'  Cards: data/legal-basis-cards.json')
    print(f'  Search entries: data/legal-search-entries.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
