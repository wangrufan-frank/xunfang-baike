# Homepage and Legal Library Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a direct home navigation item, combine current and archived monthly learning on the homepage, expose two responsive priority-learning cards, and make generated legal pages chapter-collapsible with concise street-policing labels.

**Architecture:** Keep the site static and data-driven. `meiyueyixue/data.js` remains the only monthly issue source, while `data/legal-documents.json` becomes the only source for street-policing labels; render both through the existing JavaScript and Python generators. Use native links and `details`/`summary` for resilient, accessible interaction, with `js/main.js` only enhancing deep-link expansion.

**Tech Stack:** Static HTML, CSS custom properties, browser-native JavaScript, Python 3.12 `unittest`, Node.js 20 `node:test`.

**Spec:** `docs/superpowers/specs/2026-08-22-home-and-legal-library-redesign-design.md`

## Global Constraints

- Preserve the existing six module names, order, article content, authentication flow, and four themes.
- Keep monthly issue data only in `meiyueyixue/data.js`; do not copy issue metadata into `index.html`.
- Keep legal article text unchanged; only add optional `street_note` metadata.
- Every `street_note` must contain one four-to-six-character Chinese phrase and no sentence punctuation.
- Do not add a global draft, learning-only, or legal-disclaimer notice.
- Use existing CSS theme variables; do not hard-code a second palette for the new components.
- The floating priority cards appear on the homepage only and must never obscure primary content.
- Follow red-green-refactor for every behavior change and commit each independently reviewable task.

## File Map

- `js/nav.js`: global navigation model and active-home behavior.
- `js/monthly-hero.js`: pure archive selection plus homepage monthly rendering.
- `index.html`: semantic homepage priority links.
- `css/style.css`: monthly split panel, priority cards, legal accordion, badges, responsive and focus states.
- `data/legal-documents.json`: article-level `street_note` values; no duplicate document-level quick-nav list.
- `tools/build_legal_pages.py`: validation and HTML generation for street labels and chapter accordions.
- `js/main.js`: deep-link and legal TOC enhancement.
- `fagui/*.html`: generated legal pages; never hand-edit their generated chapter structure.
- `tests/test_site_structure.py`: navigation and homepage structural contracts.
- `tests/monthly_hero.test.js`: pure monthly archive selection behavior.
- `tests/test_legal_documents.py`: street-note schema, generator, and accordion contracts.
- `tests/test_brand_styles.py`: theme-token and responsive component contracts.

---

### Task 1: Add the global Home navigation item

**Files:**
- Modify: `tests/test_site_structure.py`
- Modify: `js/nav.js`

**Interfaces:**
- Consumes: existing `MODULES` records with `name`, `path`, and `emoji`.
- Produces: first record `{ name: '首页', path: 'index.html', emoji: '🏠' }`; existing `renderNav()` calculates root-relative links and the active state.

- [ ] **Step 1: Write the failing navigation test**

Add to `NavigationStructureTests`:

```python
def test_navigation_starts_with_direct_home_link(self):
    nav = (ROOT / "js" / "nav.js").read_text(encoding="utf-8")
    home = "{ name: '首页', path: 'index.html', emoji: '🏠' }"
    self.assertIn(home, nav)
    self.assertLess(nav.index(home), nav.index("{ name: '更新记录'"))
    self.assertIn("if (moduleDir === 'index.html')", nav)
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run:

```powershell
python -m unittest tests.test_site_structure.NavigationStructureTests.test_navigation_starts_with_direct_home_link -v
```

Expected: `FAIL` because the exact home record is absent.

- [ ] **Step 3: Add the minimal navigation record**

Insert this as the first `MODULES` item in `js/nav.js`:

```javascript
{ name: '首页', path: 'index.html', emoji: '🏠' },
```

Do not add special badge flags. Preserve the existing `moduleDir === 'index.html'` active-state branch and `moduleDirs` filtering.

- [ ] **Step 4: Run targeted navigation tests**

Run:

```powershell
python -m unittest tests.test_site_structure.NavigationStructureTests -v
```

Expected: all navigation structure tests pass.

- [ ] **Step 5: Commit the navigation change**

```powershell
git add -- tests/test_site_structure.py js/nav.js
git commit -m "feat: add direct home navigation"
```

---

### Task 2: Render the homepage monthly archive beside the current issue

**Files:**
- Create: `tests/monthly_hero.test.js`
- Modify: `js/monthly-hero.js`
- Modify: `css/style.css`
- Test: `tests/test_brand_styles.py`

**Interfaces:**
- Consumes: `monthlyData = { current: string, articles: Record<string, MonthlyArticle> }` from `meiyueyixue/data.js`.
- Produces: `getArchiveEntries(data, limit): Array<{ key, theme, file }>` and a `.monthly-hero-grid` containing `.monthly-current` and `.monthly-archive`.

- [ ] **Step 1: Write failing pure-data tests**

Create `tests/monthly_hero.test.js`:

```javascript
const test = require('node:test');
const assert = require('node:assert/strict');
const { getArchiveEntries } = require('../js/monthly-hero.js');

test('archive excludes current issue, sorts newest first, and limits results', () => {
  const data = {
    current: '2026-08',
    articles: {
      '2026-06': { theme: '六月', file: '2026-06.html' },
      '2026-08': { theme: '八月', file: 'index.html' },
      '2026-07': { theme: '七月', file: '2026-07.html' },
      '2026-05': { theme: '五月', file: '2026-05.html' }
    }
  };
  assert.deepEqual(
    getArchiveEntries(data, 2).map((entry) => entry.key),
    ['2026-07', '2026-06']
  );
});

test('archive returns an empty list when no past issue exists', () => {
  const data = { current: '2026-08', articles: { '2026-08': { theme: '八月' } } };
  assert.deepEqual(getArchiveEntries(data, 3), []);
});
```

- [ ] **Step 2: Run the Node test and verify the expected failure**

Run:

```powershell
node --test tests/monthly_hero.test.js
```

Expected: `FAIL` because `getArchiveEntries` is not exported.

- [ ] **Step 3: Add the pure archive selector and browser guard**

At the top of the existing IIFE in `js/monthly-hero.js`, define and export:

```javascript
function getArchiveEntries(data, limit) {
  if (!data || !data.articles) return [];
  return Object.keys(data.articles)
    .filter(function(key) { return key !== data.current; })
    .sort()
    .reverse()
    .slice(0, limit)
    .map(function(key) {
      var article = data.articles[key];
      return { key: key, theme: article.theme, file: article.file || (key + '.html') };
    });
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { getArchiveEntries: getArchiveEntries };
}
if (typeof document === 'undefined') return;
```

Keep `typeof monthlyData === 'undefined'` after the document guard so Node can require the file safely.

- [ ] **Step 4: Run the pure tests and verify green**

Run:

```powershell
node --test tests/monthly_hero.test.js
```

Expected: 2 tests pass.

- [ ] **Step 5: Write failing homepage markup and style-contract tests**

Add to `tests/test_brand_styles.py`:

```python
def test_monthly_home_panel_uses_shared_theme_tokens(self):
    script = (ROOT / "js" / "monthly-hero.js").read_text(encoding="utf-8")
    self.assertIn('class="monthly-hero-grid"', script)
    self.assertIn('class="monthly-current"', script)
    self.assertIn('class="monthly-archive"', script)
    self.assertIn("getArchiveEntries(monthlyData, 3)", script)
    self.assertIn("var(--police-blue-deep)", CSS)
    self.assertIn(".monthly-archive", CSS)
```

- [ ] **Step 6: Run the style test and verify the expected failure**

Run:

```powershell
python -m unittest tests.test_brand_styles.BrandStyleTests.test_monthly_home_panel_uses_shared_theme_tokens -v
```

Expected: `FAIL` because the split-panel classes are absent.

- [ ] **Step 7: Render the split panel and add responsive styles**

Replace the current one-column HTML assembly in `js/monthly-hero.js` with:

```javascript
var archiveEntries = getArchiveEntries(monthlyData, 3);
var currentHtml =
  '<div class="hero-label">' + label + '</div>' +
  '<div class="hero-theme">' + article.theme + '</div>' +
  '<div class="hero-summary">' + article.summary + '</div>' +
  '<a href="meiyueyixue/index.html" class="hero-link">查看全文 →</a>';
var archiveHtml = archiveEntries.length
  ? archiveEntries.map(function(entry) {
      return '<a class="monthly-archive-item" href="meiyueyixue/' + entry.file + '">' +
        '<span>' + entry.key.replace('-', '年') + '月</span>' +
        '<strong>' + entry.theme + '</strong></a>';
    }).join('')
  : '<p class="monthly-archive-empty">暂无往期内容</p>';

var html = '<section class="monthly-hero" aria-label="每月一学">' +
  '<div class="monthly-hero-grid">' +
    '<div class="monthly-current">' + currentHtml + '</div>' +
    '<aside class="monthly-archive"><div class="monthly-archive-heading">' +
      '<strong>往期回顾</strong><span>按月归档</span></div>' + archiveHtml +
      '<a class="monthly-archive-all" href="meiyueyixue/index.html#archiveGrid">查看全部往期 →</a>' +
    '</aside>' +
  '</div></section>';
```

In `css/style.css`, keep the existing police-blue gradient on `.monthly-hero-grid`; give `.monthly-archive` `background: rgba(255,255,255,.06)` and `border-left: 1px solid rgba(255,255,255,.18)`. At `max-width: 700px`, switch the grid to one column, set `border-left: 0`, and add `border-top: 1px solid rgba(255,255,255,.18)`.

- [ ] **Step 8: Run the monthly and brand tests**

Run:

```powershell
node --test tests/monthly_hero.test.js
python -m unittest tests.test_brand_styles -v
```

Expected: all tests pass.

- [ ] **Step 9: Commit the monthly panel**

```powershell
git add -- tests/monthly_hero.test.js tests/test_brand_styles.py js/monthly-hero.js css/style.css
git commit -m "feat: show monthly archive on homepage"
```

---

### Task 3: Add responsive homepage priority cards

**Files:**
- Modify: `tests/test_site_structure.py`
- Modify: `tests/test_brand_styles.py`
- Modify: `index.html`
- Modify: `css/style.css`

**Interfaces:**
- Consumes: the existing education pages `zoufang/neiwu-tiaoling.html` and `zoufang/tineng-kaohe.html`.
- Produces: `.home-priority-links` containing `.home-priority-card--internal` and `.home-priority-card--fitness` links.

- [ ] **Step 1: Write failing link and style tests**

Add to `NavigationStructureTests`:

```python
def test_home_exposes_two_priority_learning_links(self):
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    self.assertIn('class="home-priority-links"', home)
    self.assertIn('href="zoufang/neiwu-tiaoling.html"', home)
    self.assertIn('href="zoufang/tineng-kaohe.html"', home)
    self.assertEqual(2, home.count('class="home-priority-card '))
```

Add to `BrandStyleTests`:

```python
def test_home_priority_cards_are_theme_driven_and_responsive(self):
    for selector in (
        '.home-priority-links', '.home-priority-card',
        '.home-priority-card--internal', '.home-priority-card--fitness'
    ):
        self.assertIn(selector, CSS)
    self.assertIn('@media (min-width: 1520px)', CSS)
    self.assertIn('var(--police-blue)', CSS)
    self.assertIn('var(--amber)', CSS)
```

- [ ] **Step 2: Run both tests and verify the expected failures**

Run:

```powershell
python -m unittest tests.test_site_structure.NavigationStructureTests.test_home_exposes_two_priority_learning_links tests.test_brand_styles.BrandStyleTests.test_home_priority_cards_are_theme_driven_and_responsive -v
```

Expected: 2 failures because the priority links and styles are absent.

- [ ] **Step 3: Add semantic priority links to the homepage**

Insert immediately after `#monthly-hero-placeholder` in `index.html`:

```html
<aside class="home-priority-links" aria-label="当前重点学习">
  <a href="zoufang/neiwu-tiaoling.html" class="home-priority-card home-priority-card--internal">
    <span class="priority-kicker">重点学习</span>
    <strong>人民警察内务规范</strong>
    <span>着装警容 · 礼节礼仪 · 日常管理</span>
    <em>进入学习 →</em>
  </a>
  <a href="zoufang/tineng-kaohe.html" class="home-priority-card home-priority-card--fitness">
    <span class="priority-kicker">重点考核</span>
    <strong>体能考核要求</strong>
    <span>考核导向 · 训练参考 · 方案边界</span>
    <em>进入学习 →</em>
  </a>
</aside>
```

- [ ] **Step 4: Add theme-aware desktop, fallback, mobile, and focus styles**

Implement these layout states in `css/style.css`:

```css
.home-priority-links {
  max-width: var(--max-width);
  margin: 0 auto 24px;
  padding: 0 16px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

@media (min-width: 1520px) {
  .home-priority-links { display: contents; }
  .home-priority-card { position: fixed; top: 190px; width: 144px; z-index: 20; }
  .home-priority-card--internal { left: max(16px, calc(50% - 744px)); }
  .home-priority-card--fitness { right: max(16px, calc(50% - 744px)); }
}

@media (max-width: 600px) {
  .home-priority-links { grid-template-columns: 1fr; }
}
```

Use these concrete base rules before the media queries:

```css
.home-priority-card {
  display: grid;
  gap: 8px;
  padding: 18px 16px;
  overflow: hidden;
  color: var(--text);
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-top: 4px solid var(--police-blue);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  text-decoration: none;
}
.home-priority-card--internal { border-top-color: var(--amber); }
.home-priority-card--fitness { border-top-color: var(--accent-blue); }
.home-priority-card strong { color: var(--police-blue-deep); }
.home-priority-card > span:not(.priority-kicker) { color: var(--text-muted); }
.home-priority-card em { color: var(--police-blue); font-style: normal; font-weight: 700; }
.home-priority-card:focus-visible { outline: 3px solid var(--amber); outline-offset: 3px; }
```

Do not add floating animation.

- [ ] **Step 5: Run targeted structure, brand, and link tests**

Run:

```powershell
python -m unittest tests.test_site_structure.NavigationStructureTests.test_home_exposes_two_priority_learning_links tests.test_brand_styles -v
python tools/check_site_links.py
```

Expected: tests pass and the link checker reports no broken local links.

- [ ] **Step 6: Commit the priority cards**

```powershell
git add -- tests/test_site_structure.py tests/test_brand_styles.py index.html css/style.css
git commit -m "feat: highlight priority learning on homepage"
```

---

### Task 4: Add the reviewed street-note dataset and validation

**Files:**
- Modify: `tests/test_legal_documents.py`
- Modify: `tools/build_legal_pages.py`
- Modify: `data/legal-documents.json`

**Interfaces:**
- Consumes: article objects containing `number`, `label`, and `paragraphs`.
- Produces: optional `street_note: string`, validated against `^[\u4e00-\u9fff]{4,6}$`; removes all document-level `xunfang_articles` arrays.

- [ ] **Step 1: Add the exact expected mapping fixture**

Add this module-level constant to `tests/test_legal_documents.py`:

```python
EXPECTED_STREET_NOTES = {
    "jingxie-wuqi-tiaoli": {
        2: "强制手段层级", 3: "警械武器定义", 4: "使用基本原则",
        5: "依法使用边界", 6: "无关人员避让", 7: "驱逐警械条件",
        8: "约束警械条件", 9: "武器使用条件", 10: "武器禁用情形",
        11: "停止使用武器", 12: "伤亡现场处置", 13: "武器使用报告",
        14: "违法使用责任", 15: "无辜损害补偿",
    },
    "renmin-jingcha-fa": {
        5: "执行职务保护", 6: "公安法定职责", 7: "行政强制处罚",
        8: "强行带离措施", 9: "盘问检查条件", 10: "紧急使用武器",
        11: "警械使用授权", 12: "侦查强制措施", 13: "紧急优先通行",
        14: "保护约束措施", 17: "突发现场管制", 19: "非工作时履职",
        20: "文明执勤要求", 21: "危难立即救助", 22: "执法禁止行为",
        23: "着装证件要求", 33: "违法指令拒绝", 35: "阻碍执行职务",
        45: "治安案件回避", 50: "侵权损害赔偿",
    },
    "jumin-shenfenzheng-fa": {
        6: "身份信息保密", 13: "身份证明权利", 15: "证件查验条件",
        16: "禁止非法扣证", 20: "查验违法责任",
    },
    "xingzheng-anji-chengxu-guiding": {
        52: "口头传唤程序", 53: "询问查证要求",
        54: "证据收集要求", 55: "全程记录要求",
    },
    "zhian-guanli-chufa-fa": {
        9: "治安调解条件", 26: "公共秩序扰乱", 44: "活动安全疏散",
        45: "场所安全责任", 50: "人身侵害行为", 51: "殴打伤害处罚",
        61: "阻碍执行职务", 90: "报案立案处理", 91: "非法证据排除",
        94: "涉案信息保密", 96: "现场传唤程序", 97: "询问查证时限",
        98: "询问笔录要求", 99: "现场询问证人", 101: "特殊询问协助",
        102: "人身检查采样", 103: "当场检查程序", 104: "检查笔录要求",
        105: "涉案物品扣押", 108: "调查取证人数", 111: "处罚证据标准",
        112: "处罚告知申辩", 119: "当场处罚条件", 120: "当场处罚程序",
        121: "处罚救济途径", 123: "当场收缴条件", 125: "罚款票据要求",
        131: "文明执法要求", 132: "禁止打骂侮辱", 138: "个人信息保护",
        140: "违法执法赔偿",
    },
}
```

- [ ] **Step 2: Write failing schema and exact-selection tests**

Add to `LegalDocumentsSchemaTests`:

```python
def test_street_notes_match_reviewed_mapping_and_format(self):
    actual = {}
    for doc in self.documents:
        notes = {
            art["number"]: art["street_note"]
            for ch in doc.get("chapters", [])
            for art in ch.get("articles", [])
            if art.get("street_note")
        }
        if notes:
            actual[doc["id"]] = notes
        self.assertNotIn("xunfang_articles", doc)
    self.assertEqual(EXPECTED_STREET_NOTES, actual)
    for notes in actual.values():
        for note in notes.values():
            self.assertRegex(note, r"^[\u4e00-\u9fff]{4,6}$")
```

Add this focused method to `BuildScriptExecutionTests`:

```python
def test_validation_rejects_invalid_street_note(self):
    bad = {
        "id": "test", "title": "测试法", "document_type": "法律",
        "authority": "测试机关", "status": "现行有效", "partial": True,
        "chapters": [{
            "number": "第一章", "title": "测试",
            "articles": [{
                "number": 1, "label": "第一条",
                "street_note": "不合格。", "paragraphs": ["测试正文"]
            }]
        }]
    }
    errors, _ = MODULE.validate_all([bad])
    self.assertTrue(any("street_note" in error for error in errors), errors)
```

- [ ] **Step 3: Run the schema tests and verify the expected failures**

Run:

```powershell
python -m unittest tests.test_legal_documents.LegalDocumentsSchemaTests.test_street_notes_match_reviewed_mapping_and_format tests.test_legal_documents.BuildScriptExecutionTests.test_validation_rejects_invalid_street_note -v
```

Expected: failures because article-level notes and validation do not exist and the legacy array remains.

- [ ] **Step 4: Add validation to the generator**

In `_validate_document()`, after reading each article, validate the optional field:

```python
street_note = art.get('street_note')
if street_note is not None:
    if not isinstance(street_note, str) or not re.fullmatch(r'[\u4e00-\u9fff]{4,6}', street_note):
        errors.append(
            f'{prefix}: article {num} street_note must be 4-6 Chinese characters'
        )
```

Add `import re` at the top of `tools/build_legal_pages.py`.

- [ ] **Step 5: Apply the approved 74-note mapping to legal data**

For each document/article pair in `EXPECTED_STREET_NOTES`, add the exact `street_note` next to `label` in `data/legal-documents.json`. Remove the existing `xunfang_articles` property from `jingxie-wuqi-tiaoli`. Do not alter any `paragraphs`, version metadata, official URLs, or dates.

- [ ] **Step 6: Run schema and generator validation tests**

Run:

```powershell
python -m unittest tests.test_legal_documents.LegalDocumentsSchemaTests tests.test_legal_documents.BuildScriptExecutionTests -v
python tools/build_legal_pages.py --check
```

Expected: all tests pass; generator check reports zero validation errors.

- [ ] **Step 7: Commit the street-note data model**

```powershell
git add -- tests/test_legal_documents.py tools/build_legal_pages.py data/legal-documents.json
git commit -m "feat: classify street policing legal articles"
```

---

### Task 5: Generate collapsible legal chapters and street-note labels

**Files:**
- Modify: `tests/test_legal_documents.py`
- Modify: `tests/test_brand_styles.py`
- Modify: `tools/build_legal_pages.py`
- Modify: `js/main.js`
- Modify: `css/style.css`
- Regenerate: `fagui/jingxie-wuqi-tiaoli.html`
- Regenerate: `fagui/zhian-guanli-chufa-fa.html`
- Regenerate: `fagui/renmin-jingcha-fa.html`
- Regenerate: `fagui/jumin-shenfenzheng-fa.html`
- Regenerate: `fagui/xingzheng-anji-chengxu-guiding.html`
- Regenerate: `fagui/xianchang-zhizhi-guicheng.html`
- Regenerate: `fagui/qita-xiangguan-guifan.html`
- Regenerate: `data/legal-basis-cards.json`
- Regenerate: `data/legal-search-entries.json`

**Interfaces:**
- Consumes: article-level `street_note` from Task 4.
- Produces: `_street_articles(doc)`, chapter-only TOC `<details class="legal-toc-chapter">`, body `<details class="content-section chapter-block">`, `.street-common-badge`, `.street-note`, and legal TOC deep-link expansion.

- [ ] **Step 1: Write failing generator tests**

Add to `GeneratedPageTests`:

```python
def test_generated_page_uses_collapsible_chapter_toc_and_body(self):
    doc = next(d for d in self.documents if d["id"] == "renmin-jingcha-fa")
    html = MODULE._build_page(doc, [d["id"] for d in self.documents])
    self.assertIn('<details class="legal-toc-chapter">', html)
    self.assertIn('<summary class="legal-toc-chapter-heading">', html)
    self.assertIn('<details class="content-section chapter-block">', html)
    self.assertIn('<summary class="chapter-heading">', html)
    self.assertNotIn('<li class="toc-chapter"><strong>', html)

def test_street_note_renders_badge_phrase_and_derived_quick_link(self):
    doc = next(d for d in self.documents if d["id"] == "renmin-jingcha-fa")
    html = MODULE._build_page(doc, [d["id"] for d in self.documents])
    self.assertIn('<span class="street-common-badge">街面常用</span>', html)
    self.assertIn('<span class="street-note">盘问检查条件</span>', html)
    self.assertIn('<a href="#article-9">第九条 · 盘问检查条件</a>', html)
```

Add this test for empty chapter data:

```python
def test_document_without_chapters_has_no_empty_accordion_or_quick_nav(self):
    doc = next(d for d in self.documents if d["id"] == "xianchang-zhizhi-guicheng")
    html = MODULE._build_page(doc, [d["id"] for d in self.documents])
    self.assertNotIn('class="legal-toc-chapter"', html)
    self.assertNotIn('class="xunfang-quick-nav"', html)
    self.assertIn("法规正文待补充", html)
```

- [ ] **Step 2: Write failing interaction and style-contract tests**

Add to `GeneratedPageTests.test_generated_HTML_has_required_structure`:

```python
self.assertIn('js/main.js', html)
```

Add to `tests/test_theme_assets.py` or `tests/test_brand_styles.py`:

```python
def test_legal_accordion_and_street_badge_use_shared_tokens(self):
    for selector in (
        '.legal-toc-chapter', '.legal-toc-chapter-heading',
        '.chapter-block', '.street-common-badge', '.street-note'
    ):
        self.assertIn(selector, CSS)
    self.assertIn('var(--amber)', CSS)
    self.assertIn('var(--police-blue)', CSS)
```

Add this method to `BrandStyleTests`:

```python
def test_main_script_enhances_article_and_legal_toc_links(self):
    script = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
    self.assertIn('.article-toc a[href^="#"], .legal-toc a[href^="#"]', script)
    self.assertIn("expandAndScrollTo(target)", script)
```

- [ ] **Step 3: Run the new tests and verify the expected failures**

Run:

```powershell
python -m unittest tests.test_legal_documents.GeneratedPageTests tests.test_brand_styles -v
```

Expected: failures because the generator still emits flat lists and sections and the legal selectors are missing.

- [ ] **Step 4: Derive quick navigation from article metadata**

Add this helper and use it from `_xunfang_nav()`:

```python
def _street_articles(doc):
    return [
        art
        for chapter in doc.get('chapters', [])
        for art in chapter.get('articles', [])
        if art.get('street_note')
    ]
```

Render each quick link as `第九条 · 盘问检查条件`. Return an empty string when the helper returns no articles.

- [ ] **Step 5: Render native chapter accordions**

Change `_toc()` so each chapter is:

```html
<details class="legal-toc-chapter">
  <summary class="legal-toc-chapter-heading">第一章 总则</summary>
  <ul class="legal-toc-articles">…article links…</ul>
</details>
```

Change `_full_text()` so each chapter is:

```html
<details class="content-section chapter-block">
  <summary class="chapter-heading">第一章 总则</summary>
  <div class="chapter-articles">…article blocks…</div>
</details>
```

Keep every existing `id="article-N"` anchor unchanged.

- [ ] **Step 6: Render the street badge and four-to-six-character phrase**

In `_article_html()`, build the heading suffix only when `street_note` exists:

```python
note = _safe_str(art.get('street_note'))
note_html = ''
if note:
    note_html = (
        ' <span class="street-common-badge">街面常用</span>'
        f' <span class="street-note">{escape(note)}</span>'
    )
```

Append `note_html` after the escaped article label inside `.article-heading`. Do not emit explanatory sentences or disclaimers.

- [ ] **Step 7: Extend legal TOC deep-link enhancement**

In `js/main.js`, change the TOC selector to:

```javascript
var tocLinks = document.querySelectorAll(
  '.article-toc a[href^="#"], .legal-toc a[href^="#"]'
);
```

Reuse the existing `expandAndScrollTo()` function. It already opens the closest `details` before scrolling; do not add a second scrolling implementation.

- [ ] **Step 8: Add legal accordion, badge, focus, and print styles**

Add concrete theme-driven rules, retaining existing legal typography declarations where they do not conflict:

```css
.legal-toc-chapter,
.chapter-block { border: 1px solid var(--border); border-radius: var(--radius); background: var(--card-bg); }
.legal-toc-chapter + .legal-toc-chapter,
.chapter-block + .chapter-block { margin-top: 12px; }
.legal-toc-chapter-heading,
.chapter-heading { cursor: pointer; color: var(--text); font-weight: 700; }
.legal-toc-chapter-heading { padding: 12px 14px; }
.chapter-heading { padding: 18px 20px; }
.legal-toc-chapter-heading:focus-visible,
.chapter-heading:focus-visible { outline: 3px solid var(--amber); outline-offset: 3px; }
.legal-toc-articles { padding: 0 18px 14px 34px; }
.chapter-articles { padding: 0 20px 20px; }
.street-common-badge {
  display: inline-block;
  margin-left: 8px;
  padding: 2px 7px;
  color: var(--nav-text);
  background: var(--police-blue);
  border-radius: 999px;
  font-size: 11px;
}
.street-note { margin-left: 6px; color: var(--text-muted); font-size: 12px; font-weight: 600; }
@media print {
  details:not([open]) > *:not(summary) { display: block !important; }
}
```

The visible words “街面常用” ensure the badge does not rely on color alone. Do not add animation.

- [ ] **Step 9: Run generator tests before writing generated files**

Run:

```powershell
python -m unittest tests.test_legal_documents -v
python -m unittest tests.test_brand_styles -v
```

Expected: all tests pass against generated strings and CSS contracts.

- [ ] **Step 10: Regenerate legal pages and derived JSON**

Run:

```powershell
python tools/build_legal_pages.py
```

Expected: 7 pages generated, 240 articles reported, and derived card/search JSON rewritten without validation errors.

- [ ] **Step 11: Verify generated artifacts and deep links**

Run:

```powershell
python -m unittest tests.test_legal_documents tests.test_site_links -v
python tools/build_legal_pages.py --check
```

Expected: all tests pass, zero broken links, zero generator validation errors.

- [ ] **Step 12: Commit the legal library interaction**

```powershell
git add -- tests/test_legal_documents.py tests/test_brand_styles.py tools/build_legal_pages.py js/main.js css/style.css fagui data/legal-basis-cards.json data/legal-search-entries.json
git commit -m "feat: collapse legal chapters and mark street articles"
```

---

### Task 6: Full regression and visual acceptance

**Files:**
- Modify only if a verification failure directly identifies a defect in files changed by Tasks 1-5.

**Interfaces:**
- Consumes: completed homepage and legal-library changes.
- Produces: fresh automated and visual evidence that all four requested adjustments work together.

- [ ] **Step 1: Run the complete Python suite**

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: all tests pass; only pre-existing documented skips are allowed.

- [ ] **Step 2: Run all Node tests**

```powershell
node --test tests/auth_core.test.js tests/monthly_hero.test.js
```

Expected: authentication and monthly-hero tests pass with zero failures.

- [ ] **Step 3: Run repository maintenance checks**

```powershell
python tools/build_legal_pages.py --check
python tools/build_search_index.py --check
python tools/check_site_links.py
python tools/public_source_index.py check
git diff --check
```

Expected: every command exits 0; generator reports zero validation errors; link and source checks report no defects; Git reports no whitespace errors.

- [ ] **Step 4: Preview the static site over HTTP**

Start:

```powershell
python -m http.server 8000
```

Inspect `http://localhost:8000/` at approximately 1600 px, 1200 px, and 390 px widths. Check all four themes.

- [ ] **Step 5: Complete the visual checklist**

Confirm:

- “首页” is first in desktop and mobile navigation and is active on the root page.
- Monthly current and archive areas share one police-blue visual field; the archive does not appear as a white card.
- Both wide-screen priority cards sit outside primary content and never overlap it.
- Priority cards move into the document flow on narrower screens and stack on mobile.
- Legal TOCs initially show chapter names only.
- Opening a TOC chapter reveals its article links.
- Clicking `#article-9` opens the correct body chapter and positions the target.
- “街面常用” and its four-to-six-character phrase remain readable in every theme.
- Keyboard focus is visible on navigation, priority cards, archive links, and chapter summaries.
- Printed legal pages include complete chapter contents.

- [ ] **Step 6: Review the final diff against the approved spec**

```powershell
git status --short
git diff --stat 2b0dd0b..HEAD
```

Expected: only files named in this plan are changed, aside from generated legal outputs owned by `tools/build_legal_pages.py`. No unrelated cleanup is included.
