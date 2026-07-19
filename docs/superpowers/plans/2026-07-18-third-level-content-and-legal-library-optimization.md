# Implementation Plan: 三级内容、公开来源与法律法规库优化

- **Plan date:** 2026-07-19
- **Spec:** docs/superpowers/specs/2026-07-18-third-level-content-and-legal-library-optimization-design.md
- **Base commit:** 0e61ce0
- **Branch:** feat/third-level-content-legal-library-optimization

## Global Constraints

These apply to ALL tasks. Every implementer and reviewer must enforce them.

1. **No existing public URLs changed.** New regulation pages must register in `data/legacy-url-map.json`.
2. **Tests before migration.** Every task that adds or changes output must include or extend tests.
3. **No auto-scraping for legal texts.** All regulation texts sourced from official URLs, saved as structured data, verified by human. WebFetch/fetch is import aid only — version and completeness must be verified.
4. **Regulation full text must be static HTML.** Not loaded via JavaScript.
5. **Internal data stays internal.** `source_files` in content-inventory.json must NOT be deleted. Only public display is gated.
6. **No "官方全文入口" as substitute for full text.** Legal library pages must contain complete statute text.
7. **Quick-read cards must be human-distilled** from body content — not mechanically extracted from first paragraphs.
8. **All `<details>` must be native HTML elements.** No custom JS-only collapse components.
9. **Prohibited content never in collapsed `<details>`:** safety warnings, explicit prohibitions, enforcement authorization, applicability conditions, procedural prerequisites, rights/obligations affecting time/scope/approval/notification, and statute original text.
10. **Single source component per page.** Remove duplicate `.source-list` when unified `.source-list--public` is present.

## Tasks

### Task 1: Write Failing Tests for Public Content Policy
**Status:** pending

Write tests that:
- Assert no HTML file contains "巡防百科知识库内部资料"
- Assert no HTML file contains internal `.md` filenames or `F:\` absolute paths
- Assert every source `<li>` in `.source-list` has an `http://` or `https://` link
- Assert every source has title, publisher, and verification date
- Assert every learning-type third-level page has `.quick-read`, page nav, and exactly one public source section
- Assert no prohibited content (prohibitions, applicability conditions, legal basis) inside closed `<details>`
- Assert no page has both old `.source-list` AND new `.source-list--public`

Files: `tests/test_public_content_policy.py` (new)

**Expected: tests FAIL because 83 pages still show internal sources.**

### Task 2: Unified Public Source Data and Renderer
**Status:** pending

Migrate all internet sources from `content-inventory.json.public_sources` and existing HTML `.source-list` into `public-sources.json`. Then update `tools/public_source_index.py` to render only internet sources as unified `<section class="source-list source-list--public">` for ALL third-level pages.

Steps:
1. Parse `content-inventory.json` — extract all `public_sources` entries (87 articles). The current format stores URLs as direct strings; convert each to structured `{title, publisher, url, verified_at}` entries in `public-sources.json.pages`.
2. For pages with existing HTML `.source-list` having internet URLs not in the ledger, add them.
3. Extend `public-sources.json.pages` from 27 to cover all 87 articles.
4. For the 4 articles with zero public sources (zhuangbei/jiusheng-yi, jiusheng-sheng, sanshi-weidang, zhedieshi-weidang), search for verifiable public web pages via WebSearch or leave them as uncovered — the build MUST fail with a clear error listing these pages, per spec §6.2.
5. Update `tools/public_source_index.py`:
   - `render_page()` outputs ONLY `<section class="source-list source-list--public">`
   - Uses `<!-- source-citations:start/end -->` and `<!-- public-source-index:start/end -->` markers
   - Removes any fallback that would emit internal source names or local paths
   - Covers ALL third-level pages (not just current 27)
6. Run the renderer on all third-level HTML files (inject source blocks via marker comments).
7. Remove old `<section class="source-list">` from all HTML files that now have the unified block.
8. Run `python -m unittest tests/test_public_content_policy.py` — should now PASS for internal-source-exposure checks.
9. Run existing `tests/test_public_source_index.py` — all existing tests must still pass.

### Task 3: Learning Page Components — CSS + JS + One Representative Page
**Status:** pending

Build the CSS components and JavaScript behaviors for learning-type third-level pages, then migrate ONE representative long page (pick the longest jingqing page) to validate the template end-to-end.

Steps:
1. Add to `css/style.css` (using existing theme variables only):
   - `.quick-read` — 2×2 card grid desktop, single-column mobile; 3-4 cards
   - `.article-toc` — page nav with sticky sidebar on desktop (240-280px), horizontal scroll anchors on mobile
   - `.learning-section` / `.learning-section > summary` — native `<details>` with visual distinction from default
   - `.action-steps` — ordered list for sequential procedures
   - `.do-dont-grid` — 2-column do/don't comparison
   - `.key-warning` — high-risk/prohibition callout (max 1 per section)
   - `.legal-basis-card` — regulation name, article number, full text, applicability note
   - `.fact-list` — conditions, objects, time limits, record requirements
   - Print styles: expand all `<details>`, hide nav/expand controls
   - `content-visibility: auto` in @media queries
   - Responsive: max reading width 720-760px; desktop wider container for sidebar
2. Add to `js/main.js`:
   - "展开全部/收起全部" toggle for all `.learning-section` elements
   - Hash-based auto-expand: on page load, if URL hash points to content inside a collapsed `<details>`, expand it and scroll
   - Click on `.article-toc` anchor targeting a collapsed section: expand first, then scroll
   - Keyboard accessible (no custom focus management needed beyond native)
   - No-js fallback: every `<details>` independently operable
   - Do NOT save cross-page collapse state
3. Select and migrate ONE representative jingqing page to validate template:
   - Add `.quick-read` cards (3-4, human-distilled from body text)
   - Add `.article-toc`
   - Split body into default-visible (key content) and `<details class="learning-section">` (deep dives)
   - Convert applicable paragraphs to semantic components (`.action-steps`, `.key-warning`, etc.)
   - Ensure no prohibited content inside `<details>`
   - Add unified source block
4. Verify: desktop 1440px, mobile 390px, print, dark/light theme, no-JS baseline.
5. Run `tests/test_public_content_policy.py` and existing test suite.

### Task 4: Batch-Migrate Remaining Learning-Type Third-Level Pages
**Status:** pending

Migrate ~79 remaining learning-type third-level pages (jingqing, qinwu, xunlian, zhuangbei, zoufang, plus fagui non-law-library pages). Process module-by-module, one subagent per module batch.

For EACH page:
1. Add `.quick-read` with 3-4 human-distilled cards from body content.
2. Add `.article-toc` matching the page's section headings.
3. Split body into default-visible and `<details class="learning-section">` per spec §5.2 rules.
4. Convert applicable paragraphs to semantic components (`.action-steps`, `.do-dont-grid`, `.key-warning`, `.legal-basis-card`, `.fact-list`).
5. Ensure NO prohibited content inside collapsed `<details>`.
6. Add `<!-- source-citations:start -->...<!-- source-citations:end -->` markers.
7. Remove old `.source-list` block.

Run `tools/public_source_index.py render` after each module batch to inject source blocks.
Run test suite after each batch to catch regressions.

### Task 5: Legal Documents Data Model, Generator, and Tests
**Status:** pending

Create `data/legal-documents.json` and `tools/build_legal_pages.py`, plus comprehensive tests.

Steps:
1. Create `data/legal-documents.json` with schema per spec §9:
   - Top-level: version, documents[]
   - Each document: id, title, document_type, authority, document_number, status, promulgated_at, effective_at, version_label, source_url, verified_at, history[], chapters[]
   - Each chapter: number, title, articles[]
   - Each article: number, label, paragraphs[]
   - Start with ONE complete regulation (the shortest one) as validation data
2. Create `tools/build_legal_pages.py`:
   - Read `legal-documents.json`
   - Generate full-text HTML for each document per spec §4.2 template
   - Generate `.legal-basis-card` HTML snippets keyed by (document_id, article_number) for injection into enforcement pages
   - Generate a data structure consumable by `build_search_index.py`
   - Validate: article count, first/last article match, no duplicate numbers, sequential order
   - Output: `fagui/{id}.html` (overwrite existing stubs), plus card-snippet map
3. Create `tests/test_legal_documents.py`:
   - Schema validation (required fields present, article numbers unique and sequential)
   - Article count matches generator output
   - First/last article text matches source data
   - Card snippet text matches regulation text verbatim
   - Search index entries generated for all documents
4. Run `python -m unittest tests/test_legal_documents.py` — must pass with validation data.

### Task 6: Ingest and Build Complete Regulation Full Texts
**Status:** pending

Populate `legal-documents.json` with complete, structured text for all 6 regulations (+ index conversion). Then generate HTML.

Regulations to ingest:
- `zhian-guanli-chufa-fa`: 治安管理处罚法 (2025 revision, effective 2026-01-01)
- `renmin-jingcha-fa`: 人民警察法 (current)
- `jumin-shenfenzheng-fa`: 居民身份证法 (current)
- `xingzheng-anji-chengxu-guiding`: 公安机关办理行政案件程序规定 (current with amendments)
- `jingxie-wuqi-tiaoli`: 人民警察使用警械和武器条例 (current)
- `xianchang-zhizhi-guicheng`: 公安机关人民警察现场制止违法犯罪行为操作规程 (current, if verifiable)

Steps:
1. For each regulation, fetch from official source (e.g., flk.npc.gov.cn, gov.cn, mps.gov.cn).
2. Parse into structured JSON chapters/articles/paragraphs.
3. Verify: article count, first article, last article against official source.
4. Write to `legal-documents.json`.
5. Run `tools/build_legal_pages.py` to generate HTML.
6. Convert `fagui/qita-xiangguan-guifan.html` to index page (not single regulation).
7. Register all new/changed URLs in `data/legacy-url-map.json` if needed.
8. Run `python -m unittest tests/test_legal_documents.py` — all tests pass.
9. Run `tests/test_public_content_policy.py` — no regression.

### Task 7: Legal-Basis Cards in Enforcement Application Pages
**Status:** pending

Inject `.legal-basis-card` components into the 5 enforcement application pages using unified data from `legal-documents.json`.

Pages:
- `fagui/panwen-shenfenzheng.html` — 盘问检查
- `fagui/chuanhuan-qiangzhi-chuanhuan.html` — 传唤
- `fagui/jingxie-shiyong-chengxu.html` — 警械使用
- `fagui/xingzheng-anji-tiaocha.html` — 行政案件调查
- `fagui/zhifa-jilu-quanli.html` — 执法记录

Each card must contain: regulation full name, article number, complete original text (all paragraphs/items/provisos), current validity status + version date, "本页如何适用" brief explanation, deep link to full regulation article anchor, official source URL + verification date.

Steps:
1. Map each enforcement page to its applicable regulation articles using data from the spec and page content.
2. Generate `.legal-basis-card` HTML from `legal-documents.json` (using Task 5 generator).
3. Insert cards into each page after the relevant narrative section.
4. Verify each card's text matches `legal-documents.json` verbatim.
5. Run `tests/test_legal_documents.py` card-consistency tests.

### Task 8: Rebuild Search Index and Final Verification
**Status:** pending

Steps:
1. Update `tools/build_search_index.py`:
   - Include collapsed `<details>` content in search corpus
   - Include regulation titles, article numbers, and full text
   - Support article anchors (e.g., `#article-9`)
   - Verify no duplicate page entries
   - Verify legacy URLs all resolve
2. Run `build_search_index.py` to regenerate `search-index.json`.
3. Run full test suite:
   - `python -m unittest discover -s tests -p "test_*.py" -v`
   - `node --test tests/auth_core.test.js`
   - All 87+ existing tests must pass, plus all new tests from Tasks 1 and 5
4. Verify search for "第九条 人民警察法" returns correct page with article anchor.
5. Verify search for terms inside collapsed `<details>` returns the parent page.
6. Run `tools/check_site_links.py` — no broken links.

### Task 9: Visual Acceptance and Documentation
**Status:** pending

Steps:
1. Select representative pages:
   - One long jingqing page
   - One zhuangbei page
   - One enforcement procedure page (fagui)
   - One short regulation full text
   - One long regulation full text
2. For each, verify at 1440px and 390px:
   - Above-fold shows title, core conclusion, and at least 2 action priorities
   - Core flow and prohibition boundaries understandable without expanding details
   - Expanding details doesn't lose scroll position; TOC highlight correct
   - Regulation full text fully visible, any article searchable and copyable
   - No horizontal scroll on mobile
   - Print hides nav and expand controls, shows full regulation text
   - Dark/light theme contrast adequate on key cards, legal basis, source links
3. Update `docs/public-source-maintenance.md` with new workflow (if applicable).
4. Final checklist against spec §14 release gate — all 7 conditions must be true.

## Execution Order

Tasks 1-9 execute sequentially. Task 3 must complete before Task 4. Task 5 must complete before Tasks 6 and 7. Task 8 runs after all content tasks.
