"""Validate and render the generated learning-module catalog."""

from __future__ import annotations

import html
import json
import os
import re
import tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


ALLOWED_MODULE_SLUGS = {"rumen", "kaohe", "jilv"}
TOP_LEVEL_FIELDS = {"version", "verified_at", "sources", "modules"}
SOURCE_FIELDS = {"source_id", "title", "publisher", "platform", "published_at", "url"}
MODULE_FIELDS = {"slug", "title", "description", "articles"}
ARTICLE_FIELDS = {
    "slug", "number", "title", "stage", "summary", "reading_minutes", "tags",
    "keywords", "updated_at", "source_ids", "sections", "quiz",
}
SECTION_FIELDS = {"title", "lead", "body"}
QUIZ_FIELDS = {"question", "options", "answer_index", "explanation"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RAW_HTML_RE = re.compile(
    r"<\s*(?:/?\s*[A-Za-z][^>]*>|![^>]*(?:>|$)|\?[^>]*(?:\?>|>|$))"
)
INVALID_PERCENT_ESCAPE_RE = re.compile(r"%(?![0-9A-Fa-f]{2})")
MANIFEST_HTML_RE = re.compile(
    r"^(?:rumen|kaohe|jilv)/(?:index|[a-z0-9]+(?:-[a-z0-9]+)*)\.html$"
)


def load_catalog(path: Path) -> dict:
    """Load a UTF-8 JSON catalog, requiring an object at the top level."""
    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-standard JSON constant: {value}")

    catalog = json.loads(
        Path(path).read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    if not isinstance(catalog, dict):
        raise ValueError("catalog must be a JSON object")
    return catalog


def _field_error(value: object, fields: set[str], label: str) -> str | None:
    if not isinstance(value, dict) or set(value) != fields:
        actual = set(value) if isinstance(value, dict) else set()
        missing = sorted(fields - actual)
        unknown = sorted(actual - fields)
        return f"{label} fields must be exact; missing={missing}, unknown={unknown}"
    return None


def _valid_date(value: object, nullable: bool = False) -> bool:
    if nullable and value is None:
        return True
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _contains_raw_html(value: object) -> bool:
    if isinstance(value, str):
        return bool(RAW_HTML_RE.search(value))
    if isinstance(value, dict):
        return any(_contains_raw_html(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_raw_html(item) for item in value)
    return False


def _valid_string_list(value: object, *, allow_empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(_is_nonempty_string(item) for item in value)
    )


def _valid_https_url(value: object) -> bool:
    if not _is_nonempty_string(value):
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        return False
    if any(character.isspace() or ord(character) < 32 for character in value):
        return False
    if "\\" in value or INVALID_PERCENT_ESCAPE_RE.search(value):
        return False
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        parsed.port
    except (TypeError, ValueError):
        return False
    if hostname:
        try:
            hostname.encode("utf-8")
        except UnicodeEncodeError:
            return False
        if any(0xD800 <= ord(character) <= 0xDFFF for character in hostname):
            return False
    return bool(
        parsed.scheme == "https"
        and parsed.netloc
        and hostname
        and not parsed.username
        and not parsed.password
    )


def validate_catalog(catalog: dict) -> list[str]:
    """Return all schema and content errors without modifying the catalog."""
    errors: list[str] = []
    top_error = _field_error(catalog, TOP_LEVEL_FIELDS, "top-level")
    if top_error:
        return [top_error]

    if not isinstance(catalog["version"], int) or isinstance(catalog["version"], bool) or catalog["version"] < 1:
        errors.append("version must be a positive integer")
    if not _valid_date(catalog["verified_at"]):
        errors.append("verified_at must be a valid ISO date")
    if not isinstance(catalog["sources"], list):
        errors.append("sources must be a list")
        sources: list[object] = []
    else:
        sources = catalog["sources"]
    if not isinstance(catalog["modules"], list):
        errors.append("modules must be a list")
        modules: list[object] = []
    else:
        modules = catalog["modules"]

    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        label = f"sources[{index}]"
        field_error = _field_error(source, SOURCE_FIELDS, f"{label} source")
        if field_error:
            errors.append(field_error)
            continue
        for field in ("source_id", "title", "publisher", "platform", "url"):
            if not _is_nonempty_string(source[field]):
                errors.append(f"{label}.{field} must be a non-empty string")
        source_id = source["source_id"]
        if isinstance(source_id, str):
            if source_id in source_ids:
                errors.append(f"duplicate source_id: {source_id}")
            source_ids.add(source_id)
        if not _valid_https_url(source["url"]):
            errors.append(f"{label}.url must be an HTTPS URL")
        if not _valid_date(source["published_at"], nullable=True):
            errors.append(f"{label}.published_at must be a valid ISO date or null")
        if _contains_raw_html(source):
            errors.append(f"{label} contains raw HTML")

    module_slugs: set[str] = set()
    article_slugs: set[str] = set()
    for module_index, module in enumerate(modules):
        label = f"modules[{module_index}]"
        field_error = _field_error(module, MODULE_FIELDS, f"{label} module")
        if field_error:
            errors.append(field_error)
            continue
        slug = module["slug"]
        if not isinstance(slug, str) or slug not in ALLOWED_MODULE_SLUGS:
            errors.append(f"{label}.module slug must be one of {sorted(ALLOWED_MODULE_SLUGS)}")
        if isinstance(slug, str):
            if slug in module_slugs:
                errors.append(f"duplicate module slug: {slug}")
            module_slugs.add(slug)
        for field in ("title", "description"):
            if not _is_nonempty_string(module[field]):
                errors.append(f"{label}.{field} must be a non-empty string")
        if _contains_raw_html({key: module[key] for key in ("title", "description")}):
            errors.append(f"{label} contains raw HTML")
        if not isinstance(module["articles"], list):
            errors.append(f"{label}.articles must be a list")
            continue

        for article_index, article in enumerate(module["articles"]):
            article_label = f"{label}.articles[{article_index}]"
            field_error = _field_error(article, ARTICLE_FIELDS, f"{article_label} article")
            if field_error:
                errors.append(field_error)
                continue
            article_slug = article["slug"]
            if not isinstance(article_slug, str) or not SLUG_RE.fullmatch(article_slug):
                errors.append(f"{article_label}.slug must be a safe lowercase slug")
            elif article_slug in article_slugs:
                errors.append(f"duplicate article slug: {article_slug}")
            else:
                article_slugs.add(article_slug)
            for field in ("number", "title", "summary"):
                if not _is_nonempty_string(article[field]):
                    errors.append(f"{article_label}.{field} must be a non-empty string")
            for field in ("stage", "reading_minutes"):
                value = article[field]
                if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                    errors.append(f"{article_label}.{field} must be a positive integer")
            for field in ("tags", "keywords", "source_ids"):
                if not _valid_string_list(article[field]):
                    errors.append(f"{article_label}.{field} must be a non-empty string list")
            if isinstance(article["source_ids"], list):
                for source_id in article["source_ids"]:
                    if isinstance(source_id, str) and source_id not in source_ids:
                        errors.append(f"{article_label} references unknown source_id: {source_id}")
            if not _valid_date(article["updated_at"]):
                errors.append(f"{article_label}.updated_at must be a valid ISO date")

            sections = article["sections"]
            if not isinstance(sections, list) or not sections:
                errors.append(f"{article_label}.sections must be a non-empty list")
            else:
                for section_index, section in enumerate(sections):
                    section_label = f"{article_label}.sections[{section_index}]"
                    field_error = _field_error(section, SECTION_FIELDS, f"{section_label} section")
                    if field_error:
                        errors.append(field_error)
                        continue
                    for field in SECTION_FIELDS:
                        if not _is_nonempty_string(section[field]):
                            errors.append(f"{section_label}.{field} must be a non-empty string")

            quiz = article["quiz"]
            field_error = _field_error(quiz, QUIZ_FIELDS, f"{article_label} quiz")
            if field_error:
                errors.append(field_error)
            else:
                for field in ("question", "explanation"):
                    if not _is_nonempty_string(quiz[field]):
                        errors.append(f"{article_label}.quiz.{field} must be a non-empty string")
                if not _valid_string_list(quiz["options"]) or len(quiz["options"]) < 2:
                    errors.append(f"{article_label}.quiz.options must contain at least two strings")
                answer_index = quiz["answer_index"]
                if (
                    not isinstance(answer_index, int)
                    or isinstance(answer_index, bool)
                    or not isinstance(quiz["options"], list)
                    or not 0 <= answer_index < len(quiz["options"])
                ):
                    errors.append(f"{article_label}.quiz.answer_index is out of range")
            if _contains_raw_html(article):
                errors.append(f"{article_label} contains raw HTML")
    return errors


def _escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _page_start(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_escape(title)} — 巡防百科</title>
<link rel="stylesheet" href="../css/style.css">
<script src="../js/auth-config.js"></script>
<script src="../js/auth-core.js"></script>
<script src="../js/auth-guard.js" data-root="../"></script>
</head>
<body>
<header class="learning-header"><nav aria-label="主导航"><div id="nav-placeholder"></div></nav></header>"""


def _page_end() -> str:
    return """<footer class="learning-footer"><p>巡防百科 · 公开资料学习内容</p></footer>
<script src="../js/theme.js"></script>
<script src="../js/nav.js"></script>
<script src="../js/main.js"></script>
<script src="../js/search.js"></script>
</body>
</html>
"""


def render_module_index(module: dict) -> str:
    """Render a module index. All catalog-provided strings are escaped."""
    items = []
    for article in module.get("articles", []):
        tags = " · ".join(_escape(tag) for tag in article["tags"])
        items.append(
            f'<article class="learning-list-item"><a href="{_escape(article["slug"])}.html">'
            f'<span class="learning-number">{_escape(article["number"])}</span>'
            f'<h2>{_escape(article["title"])}</h2><p>{_escape(article["summary"])}</p>'
            f'<p class="meta">阶段 {_escape(article["stage"])} · {_escape(article["reading_minutes"])} 分钟 · {tags}</p>'
            "</a></article>"
        )
    empty = '<p class="empty-state">内容正在编制中。</p>' if not items else ""
    return (
        _page_start(module["title"])
        + f"""<main class="page-container learning-module">
<nav class="breadcrumb" aria-label="面包屑"><a href="../index.html">首页</a> &gt; <span>{_escape(module["title"])}</span></nav>
<section class="page-title"><h1>{_escape(module["title"])}</h1><p>{_escape(module["description"])}</p></section>
<section class="learning-list" aria-label="课程目录">{''.join(items)}{empty}</section>
</main>
"""
        + _page_end()
    )


def _render_sources(article: dict, sources: list[dict], verified_at: str | None) -> str:
    lookup = {source["source_id"]: source for source in sources}
    verification_date = verified_at or "目录未提供"
    cards = []
    for source_id in article["source_ids"]:
        source = lookup.get(source_id)
        if not source:
            continue
        published = source["published_at"] or "页面未标注"
        cards.append(
            '<article class="source-card">'
            f'<h3>{_escape(source["title"])}</h3>'
            f'<p>{_escape(source["publisher"])} / {_escape(source["platform"])}</p>'
            f'<p>发布日期：{_escape(published)}</p>'
            f'<p>核验日期：{_escape(verification_date)}</p>'
            f'<a href="{_escape(source["url"])}" target="_blank" rel="noopener noreferrer">查看公开原文</a>'
            "</article>"
        )
    return '<section class="source-disclosure"><h2>公开资料来源</h2>' + "".join(cards) + "</section>"


def render_article(
    module: dict,
    article: dict,
    previous: dict | None,
    next_: dict | None,
    *,
    sources: list[dict] | None = None,
    verified_at: str | None = None,
) -> str:
    """Render one article with source disclosure and ordered navigation."""
    sections = "".join(
        f'<section class="learning-section"><h2>{_escape(section["title"])}</h2>'
        f'<p class="lead">{_escape(section["lead"])}</p><p>{_escape(section["body"])}</p></section>'
        for section in article["sections"]
    )
    options = "".join(
        f'<li><label><input type="radio" name="quiz" value="{index}" disabled> {_escape(option)}</label></li>'
        for index, option in enumerate(article["quiz"]["options"])
    )
    previous_link = (
        f'<a class="previous" href="{_escape(previous["slug"])}.html">上一课：{_escape(previous["title"])}</a>'
        if previous else '<span class="previous disabled">已经是第一课</span>'
    )
    next_link = (
        f'<a class="next" href="{_escape(next_["slug"])}.html">下一课：{_escape(next_["title"])}</a>'
        if next_ else '<span class="next disabled">已经是最后一课</span>'
    )
    return (
        _page_start(article["title"])
        + f"""<main class="page-container learning-article">
<nav class="breadcrumb" aria-label="面包屑"><a href="../index.html">首页</a> &gt; <a href="index.html">{_escape(module["title"])}</a> &gt; <span>{_escape(article["title"])}</span></nav>
<article>
<header class="article-header"><p>第 {_escape(article["number"])} 课 · 阶段 {_escape(article["stage"])}</p><h1>{_escape(article["title"])}</h1><p>{_escape(article["summary"])}</p><p class="meta">更新时间：{_escape(article["updated_at"])} · 预计阅读 {_escape(article["reading_minutes"])} 分钟</p></header>
{sections}
<section class="quiz" data-answer-index="{_escape(article["quiz"]["answer_index"])}"><h2>学习自测</h2><fieldset><legend>{_escape(article["quiz"]["question"])}</legend><ol>{options}</ol></fieldset><p class="quiz-explanation">答案说明：{_escape(article["quiz"]["explanation"])}</p></section>
{_render_sources(article, sources or [], verified_at)}
<nav class="article-pagination" aria-label="课程翻页">{previous_link}{next_link}</nav>
</article>
</main>
"""
        + _page_end()
    )


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def _read_manifest(root: Path) -> set[str]:
    path = root / ".generated-learning-pages.json"
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return set()
    if not isinstance(entries, list):
        return set()
    return {entry for entry in entries if isinstance(entry, str)}


def _safe_generated_html(root: Path, relative: str) -> Path | None:
    if not MANIFEST_HTML_RE.fullmatch(relative):
        return None
    candidate = Path(relative)
    resolved_root = root.resolve()
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(resolved_root):
        return None
    return resolved


def build_pages(root: Path, catalog: dict) -> list[Path]:
    """Atomically write catalog pages and replace their generated-file manifest."""
    errors = validate_catalog(catalog)
    if errors:
        raise ValueError("invalid learning catalog:\n" + "\n".join(errors))
    root = Path(root)
    rendered: dict[str, str] = {}
    for module in catalog["modules"]:
        articles = module["articles"]
        if not articles:
            continue
        rendered[f'{module["slug"]}/index.html'] = render_module_index(module)
        for index, article in enumerate(articles):
            previous = articles[index - 1] if index else None
            next_ = articles[index + 1] if index + 1 < len(articles) else None
            rendered[f'{module["slug"]}/{article["slug"]}.html'] = render_article(
                module,
                article,
                previous,
                next_,
                sources=catalog["sources"],
                verified_at=catalog["verified_at"],
            )

    previous_manifest = _read_manifest(root)
    written: list[Path] = []
    for relative, content in sorted(rendered.items()):
        path = root / relative
        _atomic_write(path, content)
        written.append(path)
    for relative in previous_manifest - set(rendered):
        stale = _safe_generated_html(root, relative)
        if stale is not None:
            stale.unlink(missing_ok=True)
    manifest = json.dumps(sorted(rendered), ensure_ascii=False, indent=2) + "\n"
    _atomic_write(root / ".generated-learning-pages.json", manifest)
    return written


def generated_search_records(catalog: dict) -> list[dict]:
    """Create deterministic search-index records for catalog articles."""
    errors = validate_catalog(catalog)
    if errors:
        raise ValueError("invalid learning catalog:\n" + "\n".join(errors))
    records = []
    for module in catalog["modules"]:
        for article in module["articles"]:
            records.append({
                "title": article["title"],
                "module": module["title"],
                "path": f'{module["slug"]}/{article["slug"]}.html',
                "desc": article["summary"],
                "tags": list(article["tags"]),
                "keywords": list(article["keywords"]),
            })
    return records
