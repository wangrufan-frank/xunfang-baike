# Learning Handbook Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first offline-demonstration version of “巡防入门学习手册” as a new, independent, clean-history static-site project with nine learning sections, a five-stage learning path, source cards, review-aware publication gates, search, and self-tests.

**Architecture:** Author structured UTF-8 JSON content and generate a fully static `dist/` site with a Python standard-library build pipeline. The generator has separate `demo` and `public` modes: demo mode visibly marks unreviewed demonstration content, while public mode emits only content whose business, confidentiality, publicity/copyright, and technical reviews are all approved. Browser JavaScript handles local search and quiz interactions; no server-side account, hidden internal area, or client-side password gate exists.

**Tech Stack:** Python 3 standard library, `unittest`, semantic HTML5, CSS, vanilla JavaScript, Git

## Global Constraints

- New project root: `F:\frank第二大脑\xunfang-learning-handbook`.
- Initialize a new independent Git repository; do not copy `xunfang-baike\.git` or its history.
- Do not copy old articles, attachments, search indexes, authentication code, deployment settings, or hidden internal content.
- Display name: `巡防入门学习手册`.
- Subtitle: `面向新警、辅警的公开型基础知识与职业素养学习平台`.
- The first phase is an offline demonstration and must show a persistent demo-status notice.
- Public mode must include only records with all four reviews marked `approved`.
- Use only publicly releasable, newly written demonstration text; no tactical actions, deployment patterns, internal procedures, sensitive equipment details, or non-public cases.
- Use lowercase hyphen-separated filenames, UTF-8, four-space JavaScript indentation, single quotes, and semicolons.
- Use no third-party runtime libraries, remote fonts, analytics, trackers, or external scripts.
- `dist/`, local caches, review records, credentials, and environment files must not be committed.

---

### Task 1: Independent project and content contract

**Files:**
- Create: `F:\frank第二大脑\xunfang-learning-handbook\.gitignore`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\README.md`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\handbook\__init__.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\handbook\content.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\tests\test_content.py`

**Interfaces:**
- Consumes: JSON dictionaries loaded from `content/`.
- Produces: `validate_article(article: dict) -> list[str]`, `load_articles(path: Path) -> list[dict]`, and `is_publishable(article: dict, mode: str) -> bool`.

- [ ] **Step 1: Initialize the directory and independent repository**

Run:

```powershell
New-Item -ItemType Directory -Path 'F:\frank第二大脑\xunfang-learning-handbook'
git -C 'F:\frank第二大脑\xunfang-learning-handbook' init
```

Expected: the new root has its own `.git` directory and `git rev-list --all --count` returns `0`.

- [ ] **Step 2: Write failing content-contract tests**

Create tests asserting that a valid article has these exact keys: `id`, `slug`, `title`, `category`, `stage`, `content_type`, `status`, `summary`, `sections`, `sources`, `media`, `quiz`, `reviews`, and `updated_at`. Assert rejection of missing sources, non-HTTPS sources, duplicate source URLs, unknown categories, tactical/internal tags, and a `public` record lacking four approved reviews.

```python
def test_public_article_requires_four_approved_reviews(self):
    article = valid_article()
    article['status'] = 'approved'
    article['reviews']['confidentiality'] = 'pending'
    self.assertFalse(is_publishable(article, 'public'))

def test_demo_article_is_visible_only_in_demo_mode(self):
    article = valid_article()
    article['status'] = 'demo'
    self.assertTrue(is_publishable(article, 'demo'))
    self.assertFalse(is_publishable(article, 'public'))
```

- [ ] **Step 3: Run tests and verify RED**

Run: `python -m unittest tests.test_content -v`

Expected: import failure because `handbook.content` does not exist.

- [ ] **Step 4: Implement the minimal content contract**

Define immutable category slugs `first-look`, `professional-conduct`, `legal-basics`, `public-communication`, `duty-basics`, `risk-awareness`, `equipment-awareness`, `scenario-classroom`, and `learning-center`. Return human-readable validation errors; never silently drop an invalid article.

```python
REVIEW_KEYS = ('business', 'confidentiality', 'publicity_copyright', 'technical')

def is_publishable(article, mode):
    if validate_article(article):
        return False
    if mode == 'demo':
        return article['status'] in {'demo', 'approved'}
    if mode == 'public':
        return article['status'] == 'approved' and all(
            article['reviews'].get(key) == 'approved' for key in REVIEW_KEYS
        )
    raise ValueError('mode must be demo or public')
```

- [ ] **Step 5: Run tests and verify GREEN**

Run: `python -m unittest tests.test_content -v`

Expected: all content-contract tests pass.

- [ ] **Step 6: Commit**

```powershell
git add .gitignore README.md handbook tests
git commit -m "feat: establish handbook content contract"
```

### Task 2: Static build and publication gate

**Files:**
- Create: `F:\frank第二大脑\xunfang-learning-handbook\handbook\build.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\handbook\render.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\tools\build.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\tests\test_build.py`

**Interfaces:**
- Consumes: validated content records and a mode of `demo` or `public`.
- Produces: `build_site(project_root: Path, output_dir: Path, mode: str) -> BuildResult`, where `BuildResult` contains `article_count`, `category_count`, and `search_count`.

- [ ] **Step 1: Write failing build tests**

Use a temporary project with one demo record and one fully approved record. Assert that demo mode emits both, public mode emits only the approved record, every build recreates the output directory, and invalid content aborts before writing partial output.

```python
def test_public_build_excludes_demo_records(self):
    result = build_site(self.root, self.output, 'public')
    self.assertEqual(result.article_count, 1)
    self.assertFalse((self.output / 'learn' / 'demo-record.html').exists())
    self.assertTrue((self.output / 'learn' / 'approved-record.html').exists())
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m unittest tests.test_build -v`

Expected: import failure because `handbook.build` does not exist.

- [ ] **Step 3: Implement atomic static builds**

Build into a sibling temporary directory, validate all records first, and replace `dist/` only after all pages and indexes are written. `tools/build.py` accepts `--mode demo|public` and `--output <path>`.

```python
@dataclass(frozen=True)
class BuildResult:
    article_count: int
    category_count: int
    search_count: int
```

- [ ] **Step 4: Run tests and verify GREEN**

Run: `python -m unittest tests.test_build -v`

Expected: all build and publication-gate tests pass.

- [ ] **Step 5: Commit**

```powershell
git add handbook tools tests
git commit -m "feat: add review-gated static build"
```

### Task 3: Semantic page rendering and source cards

**Files:**
- Modify: `F:\frank第二大脑\xunfang-learning-handbook\handbook\render.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\tests\test_render.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\site\assets\css\style.css`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\site\assets\js\main.js`

**Interfaces:**
- Produces: `render_home(context: dict) -> str`, `render_category(context: dict) -> str`, and `render_article(article: dict, mode: str) -> str`.

- [ ] **Step 1: Write failing render tests**

Assert UTF-8 Chinese title, skip link, `header`, `nav`, `main`, `footer`, five-stage learning path, nine category links, persistent demo notice in demo mode, platform-boundary notice, source publisher/title/date/access date/link, media guide card, and quiz markup.

```python
def test_demo_article_has_status_and_source_disclosures(self):
    html = render_article(valid_article(), 'demo')
    self.assertIn('离线演示内容，未经正式发布审核', html)
    self.assertIn('不能替代单位正式培训', html)
    self.assertIn('来源与延伸学习', html)
```

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m unittest tests.test_render -v`

Expected: failures for missing semantic templates and disclosures.

- [ ] **Step 3: Implement minimal accessible templates**

Escape all content with `html.escape`; allow no raw HTML in content JSON. External links use `rel="noopener noreferrer"`. Video records render as official-platform link cards rather than downloaded players. Include visible focus states and a text-only fallback for icon elements.

- [ ] **Step 4: Add responsive CSS and progressive JS**

Use system fonts, a warm police-blue palette, CSS grid with one-column fallback below `720px`, minimum 44px interactive targets, and `prefers-reduced-motion`. JavaScript only enhances navigation and quiz controls; reading remains possible with JavaScript disabled.

- [ ] **Step 5: Run tests and verify GREEN**

Run: `python -m unittest tests.test_render -v`

Expected: all semantic, disclosure, and source-card tests pass.

- [ ] **Step 6: Commit**

```powershell
git add handbook site tests
git commit -m "feat: render accessible learning pages"
```

### Task 4: Search and self-test behavior

**Files:**
- Create: `F:\frank第二大脑\xunfang-learning-handbook\handbook\search.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\site\assets\js\search.js`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\site\assets\js\quiz.js`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\tests\test_search.py`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\tests\test_frontend_contract.py`

**Interfaces:**
- Produces: `create_search_records(articles: list[dict]) -> list[dict]` and `dist/search-index.json` containing only emitted articles.

- [ ] **Step 1: Write failing search tests**

Assert deterministic ordering, Chinese title and summary preservation, category/stage metadata, no review notes or non-public fields, and exact equality between emitted article slugs and search-index slugs.

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m unittest tests.test_search tests.test_frontend_contract -v`

Expected: import or asset-contract failures.

- [ ] **Step 3: Implement the search index**

```python
def create_search_records(articles):
    return [
        {
            'slug': article['slug'],
            'title': article['title'],
            'summary': article['summary'],
            'category': article['category'],
            'stage': article['stage'],
            'url': f"learn/{article['slug']}.html",
        }
        for article in sorted(articles, key=lambda item: (item['category'], item['title']))
    ]
```

- [ ] **Step 4: Implement browser search and quiz enhancement**

Search normalizes whitespace and performs local title/summary matching without network requests. Quiz buttons reveal the selected answer, correct answer, and explanation; no scores or personal data leave the browser.

- [ ] **Step 5: Run tests and verify GREEN**

Run: `python -m unittest tests.test_search tests.test_frontend_contract -v`

Expected: all search and frontend-contract tests pass.

- [ ] **Step 6: Commit**

```powershell
git add handbook site tests
git commit -m "feat: add local search and self-tests"
```

### Task 5: Nine-section demonstration content

**Files:**
- Create: `F:\frank第二大脑\xunfang-learning-handbook\site\site.json`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\content\demo\*.json`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\tests\test_demo_content.py`

**Interfaces:**
- Consumes: the content contract from Task 1.
- Produces: nine category introductions, three representative foundation lessons, and one monthly-learning issue, all marked `demo`.

- [ ] **Step 1: Write failing demonstration-content tests**

Assert exactly nine category introductions, at least one record for every category, three foundation lessons, one monthly issue, HTTPS source metadata for every factual lesson, no empty section, no external media without publisher/title/URL, and no status other than `demo`.

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m unittest tests.test_demo_content -v`

Expected: failure because `site.json` and demonstration records do not exist.

- [ ] **Step 3: Add newly written demonstration records**

Create concise, non-operational records for all nine sections. The three foundation lessons are `保密意识：公开不等于可以随意汇编`, `程序意识是规范履职的基础`, and `与群众沟通先从倾听开始`. The monthly issue is `入门第一课：岗位、边界与学习方法`. Every page shows that it is demonstration text pending formal review.

- [ ] **Step 4: Run tests and verify GREEN**

Run: `python -m unittest tests.test_demo_content -v`

Expected: all nine-section coverage and safety-structure tests pass.

- [ ] **Step 5: Commit**

```powershell
git add site content tests
git commit -m "docs: add handbook demonstration content"
```

### Task 6: Governance documentation and repository safeguards

**Files:**
- Create: `F:\frank第二大脑\xunfang-learning-handbook\EDITORIAL.md`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\SECURITY.md`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\templates\source-record-template.json`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\templates\review-ledger-template.csv`
- Create: `F:\frank第二大脑\xunfang-learning-handbook\tests\test_repository_safety.py`

**Interfaces:**
- Produces: documented source intake, three-review-and-one-check workflow, takedown process, and machine-checked repository safety rules.

- [ ] **Step 1: Write failing repository-safety tests**

Assert that tracked files contain no `.env`, old domain, `auth.html`, old search index, absolute local source paths, or files copied from the backup directory. Assert that the blank review template contains business, confidentiality, publicity/copyright, technical, decision, reviewer, date, and notes columns but no real review record.

- [ ] **Step 2: Run tests and verify RED**

Run: `python -m unittest tests.test_repository_safety -v`

Expected: failure because governance documents and templates are missing.

- [ ] **Step 3: Write governance documents and templates**

Document source levels, original explanation/short quotation/link guide/authorized republication, aggregation-risk checks, media licensing, metadata checks, correction and takedown, and the rule that review records stay outside the public repository.

- [ ] **Step 4: Run tests and verify GREEN**

Run: `python -m unittest tests.test_repository_safety -v`

Expected: all repository-safety tests pass.

- [ ] **Step 5: Commit**

```powershell
git add EDITORIAL.md SECURITY.md templates tests
git commit -m "docs: define public content governance"
```

### Task 7: End-to-end build and offline handoff

**Files:**
- Modify: `F:\frank第二大脑\xunfang-learning-handbook\README.md`
- Generate but do not commit: `F:\frank第二大脑\xunfang-learning-handbook\dist\`

**Interfaces:**
- Produces: a verified offline demo reachable with `python -m http.server 8000 --directory dist`.

- [ ] **Step 1: Run the complete test suite**

Run: `python -m unittest discover -s tests -v`

Expected: all tests pass with zero failures and zero errors.

- [ ] **Step 2: Build demo and public modes**

Run:

```powershell
python tools/build.py --mode demo --output dist
python tools/build.py --mode public --output public-check
```

Expected: demo mode emits all demonstration records with a visible banner; public mode emits zero articles because no record has completed formal review.

- [ ] **Step 3: Verify output safety**

Search generated output for the old domain, old authentication hash, local absolute paths, review notes, and forbidden source filenames. Verify direct pages, search JSON, source links, mobile viewport, keyboard focus, reduced-motion behavior, and JavaScript-disabled reading.

- [ ] **Step 4: Remove `public-check` and retain `dist` for offline review**

Resolve the exact `public-check` path inside the new project before removal. Do not remove `dist`.

- [ ] **Step 5: Update README and commit source changes**

Document build, test, preview, publication-mode, review, and content-authoring commands. Commit only source files and tests; confirm `dist/` remains ignored.

```powershell
git add README.md
git commit -m "docs: add handbook build and review guide"
git status --short
```

Expected: working tree is clean except ignored `dist/`, and the repository has no remote or deployment configuration.
