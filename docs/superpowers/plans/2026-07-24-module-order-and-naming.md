# Website Module Order and Naming Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorder the six website modules and consistently rename four of them across all user-facing website surfaces without changing existing URLs.

**Architecture:** Keep the current static-site structure and module slugs intact. Treat `index.html` and `js/nav.js` as the two ordering sources, `data/content-inventory.json` as the module-display-name source for search generation, and update contextual module labels in HTML without altering legal quotations or generic uses of the same words.

**Tech Stack:** Static HTML, vanilla JavaScript, JSON, Python `unittest`/`pytest`, Python search-index generator.

## Global Constraints

- The exact module order is: 警情处置, 勤务须知, 执法规范, 装备操作, 教育学习, 实战训练.
- Rename 勤务保障 to 勤务须知, 装备介绍 to 装备操作, 教育培训 to 教育学习, and 警务训练 to 实战训练.
- Keep the existing `jingqing/`, `qinwu/`, `fagui/`, `zhuangbei/`, `zoufang/`, and `xunlian/` paths unchanged.
- Keep 本月精选 after the six main modules and retain its existing special styling.
- Do not modify historical docs, deliverables, screenshots, reports, or `miniprogram/`.
- Preserve verbatim legal quotations and generic prose uses such as the statutory phrase “警察业务等教育培训”; only module labels and explicit module references are renamed.
- Preserve all unrelated dirty-worktree changes and stage only files changed by each task.

---

## File Structure

- `tests/test_site_structure.py`: owns module order, display-name, inventory, and contextual stale-label checks.
- `index.html`: owns homepage card order and homepage module labels.
- `js/nav.js`: owns global navigation order and global module labels.
- `js/search.js`: owns the client-side slug-to-display-name fallback mapping.
- `data/content-inventory.json`: owns module titles and per-article `module_title` values used by tooling.
- `search-index.json`: generated user-facing search records; rebuilt from the inventory and article HTML.
- `jingqing/*.html`, `qinwu/*.html`, `fagui/*.html`, `zhuangbei/*.html`, `zoufang/*.html`, `xunlian/*.html`: module indexes and article pages containing page titles, headings, breadcrumbs, return links, and cross-module references.

### Task 1: Homepage and global navigation order

**Files:**
- Modify: `tests/test_site_structure.py`
- Modify: `index.html`
- Modify: `js/nav.js`

**Interfaces:**
- Consumes: Existing module card markup in `index.html` and the `MODULES` array in `js/nav.js`.
- Produces: One canonical `DISPLAY_MODULES` test constant and matching homepage/navigation order.

- [ ] **Step 1: Write the failing order-and-name test**

Add this constant near `EXPECTED_COUNTS` in `tests/test_site_structure.py`:

```python
DISPLAY_MODULES = [
    ("jingqing", "警情处置"),
    ("qinwu", "勤务须知"),
    ("fagui", "执法规范"),
    ("zhuangbei", "装备操作"),
    ("zoufang", "教育学习"),
    ("xunlian", "实战训练"),
]
```

Replace `NavigationStructureTests.test_home_and_nav_use_exact_six_modules` with:

```python
def test_home_and_nav_use_exact_six_modules_in_display_order(self):
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    nav = (ROOT / "js" / "nav.js").read_text(encoding="utf-8")

    expected_titles = [title for _, title in DISPLAY_MODULES]
    expected_paths = [f"{slug}/index.html" for slug, _ in DISPLAY_MODULES]
    for source in (home, nav):
        self.assertEqual(
            sorted(source.index(title) for title in expected_titles),
            [source.index(title) for title in expected_titles],
        )
        self.assertEqual(
            sorted(source.index(path) for path in expected_paths),
            [source.index(path) for path in expected_paths],
        )

    for old_title in [
        "装备介绍", "勤务保障", "警务训练", "教育培训",
        "巡防勤务", "法条规范", "走访送教", "入门指南",
    ]:
        self.assertNotIn(old_title, home)
        self.assertNotIn(old_title, nav)

    monthly_position = nav.index("本月精选")
    self.assertGreater(monthly_position, nav.index("实战训练"))
    self.assertIn("special: true", nav)
```

- [ ] **Step 2: Run the focused test and confirm it fails**

Run:

```powershell
python -m pytest tests/test_site_structure.py::NavigationStructureTests::test_home_and_nav_use_exact_six_modules_in_display_order -q
```

Expected: `FAILED` because the current homepage/navigation start with 装备介绍 and contain the four old names.

- [ ] **Step 3: Update the homepage cards**

In `index.html`, move the six existing `.module-card` blocks without changing their icon, accent class, count, description, or href. Set their order and label text to:

```html
<a href="jingqing/index.html" class="module-card accent-red">
  <div class="name">警情处置</div>
  <div class="hot-links">进入警情处置 →</div>
</a>
<a href="qinwu/index.html" class="module-card accent-green">
  <div class="name">勤务须知</div>
  <div class="hot-links">进入勤务须知 →</div>
</a>
<a href="fagui/index.html" class="module-card accent-red">
  <div class="name">执法规范</div>
  <div class="hot-links">进入执法规范 →</div>
</a>
<a href="zhuangbei/index.html" class="module-card accent-blue">
  <div class="name">装备操作</div>
  <div class="hot-links">进入装备操作 →</div>
</a>
<a href="zoufang/index.html" class="module-card accent-teal">
  <div class="name">教育学习</div>
  <div class="hot-links">进入教育学习 →</div>
</a>
<a href="xunlian/index.html" class="module-card accent-purple">
  <div class="name">实战训练</div>
  <div class="hot-links">进入实战训练 →</div>
</a>
```

Retain each card’s existing icon, count, and description elements between the shown `name` and `hot-links` elements.

- [ ] **Step 4: Update the navigation data**

Replace the first six entries of `MODULES` in `js/nav.js` with:

```javascript
var MODULES = [
  { name: '警情处置', path: 'jingqing/index.html', emoji: '🚨' },
  { name: '勤务须知', path: 'qinwu/index.html', emoji: '📋' },
  { name: '执法规范', path: 'fagui/index.html', emoji: '📕' },
  { name: '装备操作', path: 'zhuangbei/index.html', emoji: '🛡️' },
  { name: '教育学习', path: 'zoufang/index.html', emoji: '🎓' },
  { name: '实战训练', path: 'xunlian/index.html', emoji: '⚔️' },
  { name: '本月精选', path: 'meiyueyixue/index.html', emoji: '⭐', special: true }
];
```

- [ ] **Step 5: Run the focused test and confirm it passes**

Run:

```powershell
python -m pytest tests/test_site_structure.py::NavigationStructureTests::test_home_and_nav_use_exact_six_modules_in_display_order -q
```

Expected: `1 passed`.

- [ ] **Step 6: Commit the ordering change**

```powershell
git add -- tests/test_site_structure.py index.html js/nav.js
git commit -m "feat: reorder and rename website modules"
```

### Task 2: Module pages, inventory, and search consistency

**Files:**
- Modify: `tests/test_site_structure.py`
- Modify: `js/search.js`
- Modify: `data/content-inventory.json`
- Modify: `search-index.json`
- Modify: `qinwu/index.html` and `qinwu/*.html`
- Modify: `zhuangbei/index.html` and `zhuangbei/*.html`
- Modify: `zoufang/index.html` and `zoufang/*.html`
- Modify: `xunlian/index.html` and `xunlian/*.html`
- Modify where explicit renamed-module references occur: `jingqing/*.html`
- Modify where explicit renamed-module references occur: `fagui/*.html`

**Interfaces:**
- Consumes: `DISPLAY_MODULES` from Task 1, article `data-module` slugs, and `tools/build_search_index.py`.
- Produces: Consistent module display names in HTML, inventory records, client-side search fallback names, and generated search records.

- [ ] **Step 1: Write failing module-surface and source-integrity tests**

Add these constants after `DISPLAY_MODULES` in `tests/test_site_structure.py`:

```python
RENAMED_MODULES = {
    "qinwu": ("勤务保障", "勤务须知"),
    "zhuangbei": ("装备介绍", "装备操作"),
    "zoufang": ("教育培训", "教育学习"),
    "xunlian": ("警务训练", "实战训练"),
}
```

Add these tests to `NavigationStructureTests`:

```python
def test_module_display_names_are_consistent_across_runtime_sources(self):
    inventory = load_inventory()
    inventory_by_slug = {module["slug"]: module for module in inventory["modules"]}
    search_records = json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
    search_fallbacks = (ROOT / "js" / "search.js").read_text(encoding="utf-8")

    for slug, title in DISPLAY_MODULES:
        module = inventory_by_slug[slug]
        self.assertEqual(title, module["title"])
        self.assertTrue(all(article["module_title"] == title for article in module["articles"]))
        self.assertTrue(all(
            record["module"] == title
            for record in search_records
            if record["path"].startswith(f"{slug}/")
        ))
        self.assertIn(f"'{slug}': '{title}'", search_fallbacks)

        index_html = (ROOT / slug / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"<title>{title} — 巡防百科</title>", index_html)
        self.assertIn(f'<span class="current">{title}</span>', index_html)
        self.assertIn(title, index_html)

def test_old_names_are_absent_from_module_label_contexts(self):
    explicit_reference_patterns = [
        "{old}模块",
        "返回{old}",
        "进入{old}",
        ">{old}<",
    ]
    runtime_pages = [
        path
        for slug, _ in DISPLAY_MODULES
        for path in (ROOT / slug).glob("*.html")
    ]
    runtime_pages.extend([ROOT / "index.html", ROOT / "search.html"])

    for path in runtime_pages:
        text = path.read_text(encoding="utf-8")
        for old, _ in RENAMED_MODULES.values():
            for pattern in explicit_reference_patterns:
                self.assertNotIn(pattern.format(old=old), text, str(path))

def test_verbatim_legal_education_training_quote_is_preserved(self):
    legal_documents = (ROOT / "data" / "legal-documents.json").read_text(encoding="utf-8")
    legal_cards = (ROOT / "data" / "legal-basis-cards.json").read_text(encoding="utf-8")
    statutory_text = "警察业务等教育培训"
    self.assertIn(statutory_text, legal_documents)
    self.assertIn(statutory_text, legal_cards)
```

- [ ] **Step 2: Run the new tests and confirm they fail**

Run:

```powershell
python -m pytest tests/test_site_structure.py::NavigationStructureTests::test_module_display_names_are_consistent_across_runtime_sources tests/test_site_structure.py::NavigationStructureTests::test_old_names_are_absent_from_module_label_contexts tests/test_site_structure.py::NavigationStructureTests::test_verbatim_legal_education_training_quote_is_preserved -q
```

Expected: the first two tests fail on current module labels; the legal-quotation preservation test passes.

- [ ] **Step 3: Update module labels in HTML**

Apply the following contextual replacements in the six module directories:

```text
勤务保障 → 勤务须知
装备介绍 → 装备操作
教育培训 → 教育学习
警务训练 → 实战训练
```

Change the text when it is a page title, heading, breadcrumb, exact link label, return label, metadata keyword identifying the module, or an explicit phrase ending in “模块”. Also update cross-module phrases such as `参见警务训练模块` to `参见实战训练模块`.

Do not replace quoted statutes or generic prose where the phrase is not a module name. In particular, retain `警察业务等教育培训` in `data/legal-documents.json`, `data/legal-basis-cards.json`, and any rendered statutory quotation.

- [ ] **Step 4: Update inventory module display names**

In `data/content-inventory.json`, update both each affected module’s top-level `title` and every affected article’s `module_title`:

```json
{
  "qinwu": "勤务须知",
  "zhuangbei": "装备操作",
  "zoufang": "教育学习",
  "xunlian": "实战训练"
}
```

Do not change `slug`, `module`, `path`, article ordering, categories, sources, images, or related-page paths.

- [ ] **Step 5: Update the search fallback map**

In `js/search.js`, set `MODULE_NAMES` to:

```javascript
var MODULE_NAMES = {
  'zhuangbei': '装备操作',
  'qinwu': '勤务须知',
  'xunlian': '实战训练',
  'jingqing': '警情处置',
  'fagui': '执法规范',
  'zoufang': '教育学习',
  'meiyueyixue': '本月精选'
};
```

- [ ] **Step 6: Regenerate the search index**

Run:

```powershell
python tools/build_search_index.py
```

Expected: `Wrote 87 records to search-index.json`.

- [ ] **Step 7: Run module consistency and search-index tests**

Run:

```powershell
python -m pytest tests/test_site_structure.py::NavigationStructureTests tests/test_search_index.py -q
```

Expected: all selected tests pass and `search-index.json` matches a fresh build.

- [ ] **Step 8: Review the diff for scope and source integrity**

Run:

```powershell
git diff --check
git diff --stat
git diff -- data/legal-documents.json data/legal-basis-cards.json miniprogram
```

Expected: no whitespace errors; no changes to legal source JSON or `miniprogram/`; changes are limited to runtime module HTML, inventory/search data, tests, and the two JavaScript files.

- [ ] **Step 9: Commit the sitewide naming change**

Stage only the files changed for this task, excluding pre-existing deliverable changes:

```powershell
git add -- tests/test_site_structure.py js/search.js data/content-inventory.json search-index.json jingqing qinwu fagui zhuangbei zoufang xunlian
git commit -m "feat: align module names across website"
```

### Task 3: Full website regression verification

**Files:**
- Verify only; no planned source changes.

**Interfaces:**
- Consumes: Completed Tasks 1 and 2.
- Produces: Evidence that structure, search generation, links, auth integration, and content contracts still pass.

- [ ] **Step 1: Run the focused structure and search suite**

```powershell
python -m pytest tests/test_site_structure.py tests/test_search_index.py tests/test_site_links.py -q
```

Expected: all tests pass.

- [ ] **Step 2: Verify the generated search index directly**

```powershell
python tools/build_search_index.py --check
```

Expected: `OK: search-index.json matches 87 records.`

- [ ] **Step 3: Run the complete automated test suite**

```powershell
python -m pytest tests -q
```

Expected: all tests pass. If an unrelated environment-only presentation verification test requires unavailable desktop software, record it separately and still require every website test to pass.

- [ ] **Step 4: Confirm paths and unrelated worktree changes are preserved**

```powershell
git status --short
git diff HEAD~2 --name-status
```

Expected: no module directory was renamed or deleted; existing unrelated `deliverables/` changes remain unstaged and uncommitted; implementation commits contain only the planned website files.
