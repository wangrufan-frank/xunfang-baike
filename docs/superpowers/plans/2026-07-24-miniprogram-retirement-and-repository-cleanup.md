# Miniprogram Retirement and Repository Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the obsolete WeChat miniprogram implementation and its active dependencies while preserving the static website, historical documentation, and every existing `deliverables/` worktree change.

**Architecture:** Treat the static website as the only runtime product. Retire the miniprogram through a Git deletion commit, replace miniprogram-specific tests with a durable absence contract, then remove the remaining active tooling references without rewriting historical records or regenerating deliverables.

**Tech Stack:** Static HTML/CSS/JavaScript, Python `unittest`/`pytest`, Node.js syntax checking, GitHub Pages.

## Global Constraints

- Delete the complete tracked `miniprogram/` tree and root `parse_html.py`.
- Preserve all static website runtime files, URLs, module paths, content, authentication, search, images, and video.
- Preserve `.nojekyll`, `CNAME`, and the GitHub Pages publishing model.
- Preserve all historical files under `docs/`; only this feature's design and plan documents may be added.
- Do not modify, delete, stage, commit, or regenerate anything under `deliverables/`.
- Remove only miniprogram-specific tests; retain sensitive-content, deleted-page, search-index, and internal-link coverage.
- Update the active presentation generator copy from `微信小程序迁移` to `移动端体验优化`; do not regenerate a presentation.
- Do not rewrite Git history. The removed miniprogram must remain recoverable from the parent commit.
- Before implementation, capture `git -c core.quotepath=false status --short -- deliverables`; after integration the output must be byte-for-byte equivalent.

---

## File Structure

- `miniprogram/`: obsolete WeChat miniprogram runtime; delete the entire tracked tree.
- `parse_html.py`: obsolete website-to-miniprogram data generator; delete.
- `tests/test_sensitive_content_removal.py`: retain website remediation tests, replace miniprogram behavior tests with retirement contracts.
- `tools/check_site_links.py`: remove the obsolete miniprogram scan exclusion.
- `tools/generate_demo_ppt.js`: replace the active future-plan copy; do not run the generator.

### Task 1: Retire the miniprogram implementation

**Files:**
- Modify: `tests/test_sensitive_content_removal.py`
- Delete: `parse_html.py`
- Delete: `miniprogram/app.js`
- Delete: `miniprogram/app.json`
- Delete: `miniprogram/app.wxss`
- Delete: `miniprogram/components/nav-bar/nav-bar.js`
- Delete: `miniprogram/components/nav-bar/nav-bar.json`
- Delete: `miniprogram/components/nav-bar/nav-bar.wxml`
- Delete: `miniprogram/components/nav-bar/nav-bar.wxss`
- Delete: `miniprogram/custom-tab-bar/index.js`
- Delete: `miniprogram/custom-tab-bar/index.json`
- Delete: `miniprogram/custom-tab-bar/index.wxml`
- Delete: `miniprogram/custom-tab-bar/index.wxss`
- Delete: `miniprogram/data/fagui.js`
- Delete: `miniprogram/data/jingqing.js`
- Delete: `miniprogram/data/qinwu.js`
- Delete: `miniprogram/data/xunlian.js`
- Delete: `miniprogram/data/zhuangbei.js`
- Delete: `miniprogram/data/zoufang.js`
- Delete: `miniprogram/pages/auth/auth.js`
- Delete: `miniprogram/pages/auth/auth.json`
- Delete: `miniprogram/pages/auth/auth.wxml`
- Delete: `miniprogram/pages/auth/auth.wxss`
- Delete: `miniprogram/pages/fagui/detail/detail.js`
- Delete: `miniprogram/pages/fagui/detail/detail.json`
- Delete: `miniprogram/pages/fagui/detail/detail.wxml`
- Delete: `miniprogram/pages/fagui/index/index.js`
- Delete: `miniprogram/pages/fagui/index/index.json`
- Delete: `miniprogram/pages/fagui/index/index.wxml`
- Delete: `miniprogram/pages/index/index.js`
- Delete: `miniprogram/pages/index/index.json`
- Delete: `miniprogram/pages/index/index.wxml`
- Delete: `miniprogram/pages/jingqing/detail/detail.js`
- Delete: `miniprogram/pages/jingqing/detail/detail.json`
- Delete: `miniprogram/pages/jingqing/detail/detail.wxml`
- Delete: `miniprogram/pages/jingqing/index/index.js`
- Delete: `miniprogram/pages/jingqing/index/index.json`
- Delete: `miniprogram/pages/jingqing/index/index.wxml`
- Delete: `miniprogram/pages/more/more.js`
- Delete: `miniprogram/pages/more/more.json`
- Delete: `miniprogram/pages/more/more.wxml`
- Delete: `miniprogram/pages/qinwu/detail/detail.js`
- Delete: `miniprogram/pages/qinwu/detail/detail.json`
- Delete: `miniprogram/pages/qinwu/detail/detail.wxml`
- Delete: `miniprogram/pages/qinwu/index/index.js`
- Delete: `miniprogram/pages/qinwu/index/index.json`
- Delete: `miniprogram/pages/qinwu/index/index.wxml`
- Delete: `miniprogram/pages/xunlian/detail/detail.js`
- Delete: `miniprogram/pages/xunlian/detail/detail.json`
- Delete: `miniprogram/pages/xunlian/detail/detail.wxml`
- Delete: `miniprogram/pages/xunlian/index/index.js`
- Delete: `miniprogram/pages/xunlian/index/index.json`
- Delete: `miniprogram/pages/xunlian/index/index.wxml`
- Delete: `miniprogram/pages/zhuangbei/detail/detail.js`
- Delete: `miniprogram/pages/zhuangbei/detail/detail.json`
- Delete: `miniprogram/pages/zhuangbei/detail/detail.wxml`
- Delete: `miniprogram/pages/zhuangbei/index/index.js`
- Delete: `miniprogram/pages/zhuangbei/index/index.json`
- Delete: `miniprogram/pages/zhuangbei/index/index.wxml`
- Delete: `miniprogram/pages/zoufang/detail/detail.js`
- Delete: `miniprogram/pages/zoufang/detail/detail.json`
- Delete: `miniprogram/pages/zoufang/detail/detail.wxml`
- Delete: `miniprogram/pages/zoufang/index/index.js`
- Delete: `miniprogram/pages/zoufang/index/index.json`
- Delete: `miniprogram/pages/zoufang/index/index.wxml`
- Delete: `miniprogram/project.config.json`
- Delete: `miniprogram/project.private.config.json`
- Delete: `miniprogram/sitemap.json`

**Interfaces:**
- Consumes: Existing `SensitiveContentRemovalTests` and Git-tracked miniprogram files.
- Produces: A repository contract in which `miniprogram/` and `parse_html.py` remain absent while all website remediation tests remain active.

- [ ] **Step 1: Replace miniprogram behavior tests with a failing retirement contract**

In `tests/test_sensitive_content_removal.py`, remove:

- `test_parse_html_targets_the_current_repository`
- `test_jingqing_miniprogram_still_shows_remediation_state`
- `test_jingqing_miniprogram_data_is_empty`
- `test_qinwu_miniprogram_still_shows_remediation_shell`
- `test_miniprogram_home_does_not_repeat_removed_jingqing_cases`

Add this test at the start of `SensitiveContentRemovalTests`:

```python
def test_miniprogram_implementation_is_retired(self):
    self.assertFalse((ROOT / 'miniprogram').exists())
    self.assertFalse((ROOT / 'parse_html.py').exists())
```

- [ ] **Step 2: Run the retirement test and verify RED**

Run:

```powershell
python -m pytest -p no:cacheprovider tests/test_sensitive_content_removal.py::SensitiveContentRemovalTests::test_miniprogram_implementation_is_retired -q
```

Expected: `FAILED` because `miniprogram/` and `parse_html.py` still exist.

- [ ] **Step 3: Delete the obsolete implementation**

Use `apply_patch` to delete `parse_html.py` and every exact `miniprogram/` file listed in this task's **Files** section. Empty directories disappear after their last file is removed. Do not delete or modify any other root directory.

- [ ] **Step 4: Run the retirement and retained remediation tests**

Run:

```powershell
python -m pytest -p no:cacheprovider tests/test_sensitive_content_removal.py -q
```

Expected: all tests in `tests/test_sensitive_content_removal.py` pass.

- [ ] **Step 5: Verify deletion scope**

Run:

```powershell
git diff --name-status -- miniprogram parse_html.py tests/test_sensitive_content_removal.py
git diff --check
```

Expected: all 66 miniprogram files and `parse_html.py` are deleted; only `tests/test_sensitive_content_removal.py` is modified; no whitespace errors.

- [ ] **Step 6: Commit the retired implementation**

```powershell
git add -- tests/test_sensitive_content_removal.py
git commit -m "refactor: retire miniprogram implementation"
```

### Task 2: Remove active miniprogram references

**Files:**
- Modify: `tests/test_sensitive_content_removal.py`
- Modify: `tools/check_site_links.py`
- Modify: `tools/generate_demo_ppt.js`

**Interfaces:**
- Consumes: The absence contract from Task 1.
- Produces: Active maintenance tooling that no longer excludes or plans for a miniprogram.

- [ ] **Step 1: Write the failing active-tooling test**

Add this test to `SensitiveContentRemovalTests`:

```python
def test_active_tooling_no_longer_targets_miniprogram(self):
    link_checker = (ROOT / 'tools' / 'check_site_links.py').read_text(encoding='utf-8')
    presentation_generator = (
        ROOT / 'tools' / 'generate_demo_ppt.js'
    ).read_text(encoding='utf-8')

    self.assertNotIn("'miniprogram'", link_checker)
    self.assertNotIn('微信小程序迁移', presentation_generator)
    self.assertIn('移动端体验优化', presentation_generator)
```

- [ ] **Step 2: Run the active-tooling test and verify RED**

Run:

```powershell
python -m pytest -p no:cacheprovider tests/test_sensitive_content_removal.py::SensitiveContentRemovalTests::test_active_tooling_no_longer_targets_miniprogram -q
```

Expected: `FAILED` because the link checker still excludes `miniprogram` and the presentation generator still contains `微信小程序迁移`.

- [ ] **Step 3: Remove the obsolete link-check exclusion**

Change `EXCLUDED_DIRS` in `tools/check_site_links.py` from:

```python
EXCLUDED_DIRS = {
    '.git', '.worktrees', '.superpowers', 'deliverables', 'docs',
    'miniprogram', 'node_modules', '__pycache__', 'tests', 'tools', 'data',
}
```

to:

```python
EXCLUDED_DIRS = {
    '.git', '.worktrees', '.superpowers', 'deliverables', 'docs',
    'node_modules', '__pycache__', 'tests', 'tools', 'data',
}
```

- [ ] **Step 4: Replace the active future-plan copy**

In `tools/generate_demo_ppt.js`, replace the miniprogram plan tuple:

```javascript
['微信小程序迁移', '将成熟内容逐步适配至移动端使用场景。']
```

with:

```javascript
['移动端体验优化', '持续优化手机端浏览、搜索与内容阅读体验。']
```

Do not run `tools/generate_demo_ppt.js` and do not modify generated presentation files.

- [ ] **Step 5: Run focused tests and syntax checks**

Run:

```powershell
python -m pytest -p no:cacheprovider tests/test_sensitive_content_removal.py -q
python tools/check_site_links.py
node --check tools/generate_demo_ppt.js
```

Expected: all sensitive-content tests pass; link checker exits `0`; Node syntax check exits `0`.

- [ ] **Step 6: Audit active references**

Run:

```powershell
git -c core.quotepath=false grep -n -I -e 'miniprogram' -e '微信小程序迁移' -- ':!docs/**' ':!deliverables/**'
```

Expected: the only `miniprogram` matches are the retirement contract and its test name in `tests/test_sensitive_content_removal.py`; no active code, generator, or configuration match remains; `微信小程序迁移` has no match outside historical `docs/` and `deliverables/`.

- [ ] **Step 7: Commit active-reference cleanup**

```powershell
git add -- tests/test_sensitive_content_removal.py tools/check_site_links.py tools/generate_demo_ppt.js
git commit -m "refactor: remove active miniprogram references"
```

### Task 3: Repository and deployment verification

**Files:**
- Verify only; no planned source changes.

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces: Evidence that website behavior, repository scope, deployment, and pre-existing deliverable changes are preserved.

- [ ] **Step 1: Run focused website tests**

```powershell
python -m pytest -p no:cacheprovider tests/test_sensitive_content_removal.py tests/test_site_structure.py tests/test_search_index.py tests/test_site_links.py -q
```

Expected: all selected tests pass.

- [ ] **Step 2: Verify generated search and internal links**

```powershell
python tools/build_search_index.py --check
python tools/check_site_links.py
```

Expected: search index matches 87 records and the link checker reports no broken site links.

- [ ] **Step 3: Run the complete suite**

Use a writable task-specific temporary directory because the legal-page generation test writes generated data:

```powershell
$testTemp = Join-Path (Get-Location) '.test-tmp'
New-Item -ItemType Directory -Force -Path $testTemp | Out-Null
$env:TEMP = $testTemp
$env:TMP = $testTemp
python -m pytest -p no:cacheprovider tests -q
```

Expected: all tests pass; only the repository's intentional skips remain.

- [ ] **Step 4: Verify protected scope**

With `BASE_SHA` set to the commit immediately before Task 1:

```powershell
git diff --name-status $BASE_SHA..HEAD -- deliverables
git diff --name-status $BASE_SHA..HEAD -- docs
git status --short
```

Expected: no `deliverables/` or `docs/` path in the Task 1–2 commit range; the approved design and implementation plan were committed before `BASE_SHA`; the working tree contains no task-created uncommitted files.

- [ ] **Step 5: Verify retirement and recovery point**

```powershell
Test-Path -LiteralPath 'miniprogram'
Test-Path -LiteralPath 'parse_html.py'
git ls-tree -r --name-only $BASE_SHA -- miniprogram parse_html.py
```

Expected: both `Test-Path` results are `False`; the base commit lists the removed files, proving they remain recoverable through Git history.

- [ ] **Step 6: Integrate and verify the main worktree**

After approved review, merge the feature branch into `master`. Compare the main worktree's captured pre-implementation `deliverables/` status with:

```powershell
git -c core.quotepath=false status --short -- deliverables
```

Expected: byte-for-byte equivalent output.

- [ ] **Step 7: Push and verify GitHub Pages**

Push `master`, monitor the GitHub Pages workflow until it reaches `completed/success`, then request cache-busted production URLs for `/`, `/jingqing/`, and `/search.html`.

Expected: HTTP `200` for all three pages; homepage contains `勤务须知`, `装备操作`, `教育学习`, and `实战训练`.
