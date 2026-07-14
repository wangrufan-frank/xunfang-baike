# 巡防勤务整改栏目壳恢复实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在网站和微信小程序恢复“巡防勤务”栏目入口，并统一显示“内容整改中”，同时保持所有已删除内容不可访问。

**Architecture:** 在现有敏感内容删除回归测试上增加栏目壳断言，先确认测试失败，再恢复网站和小程序的安全占位入口。数据层继续保持空数组，搜索索引不新增记录，旧详情页继续不存在。

**Tech Stack:** 静态 HTML、微信小程序 JavaScript/WXML、Python `unittest`

## Global Constraints

- 不恢复任何已删除 HTML、文章数据、摘要、热词、搜索记录或旧详情链接。
- `miniprogram/data/qinwu.js` 必须保持 `module.exports = [];`。
- 网站和小程序栏目页统一显示“内容整改中”。
- 不修改备份目录，不改写 Git 历史。
- 用户现有未跟踪 `公安警察工作汇报PPT.pptx` 不纳入提交。

---

### Task 1: 增加栏目壳回归测试

**Files:**
- Modify: `tests/test_sensitive_content_removal.py`

**Interfaces:**
- Consumes: 网站首页、qinwu 栏目页、小程序首页、qinwu 小程序栏目页和数据文件。
- Produces: 对四个可见入口及空数据约束的自动化断言。

- [ ] **Step 1: 编写失败测试**

新增 `test_qinwu_web_and_miniprogram_show_remediation_shell`，断言：

```python
self.assertIn('巡防勤务', (ROOT / 'index.html').read_text(encoding='utf-8'))
self.assertIn('内容整改中', (ROOT / 'qinwu' / 'index.html').read_text(encoding='utf-8'))
self.assertIn('巡防勤务', (ROOT / 'miniprogram/pages/index/index.wxml').read_text(encoding='utf-8'))
self.assertIn('内容整改中', (ROOT / 'miniprogram/pages/qinwu/index/index.wxml').read_text(encoding='utf-8'))
self.assertEqual((ROOT / 'miniprogram/data/qinwu.js').read_text(encoding='utf-8').strip(), 'module.exports = [];')
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python -m unittest tests.test_sensitive_content_removal.SensitiveContentRemovalTests.test_qinwu_web_and_miniprogram_show_remediation_shell -v`

Expected: FAIL，首页或栏目页缺少巡防勤务整改壳。

### Task 2: 恢复网站与小程序栏目壳

**Files:**
- Modify: `index.html`
- Modify: `qinwu/index.html`
- Modify: `miniprogram/pages/index/index.js`
- Modify: `miniprogram/pages/index/index.wxml`
- Modify: `miniprogram/pages/qinwu/index/index.js`
- Modify: `miniprogram/pages/qinwu/index/index.wxml`
- Modify: `miniprogram/pages/qinwu/detail/detail.js`

**Interfaces:**
- Consumes: Task 1 的失败测试。
- Produces: 网站和小程序可见的安全整改栏目壳。

- [ ] **Step 1: 恢复网站入口与占位页**

在 `index.html` 恢复指向 `qinwu/index.html` 的模块卡，内容仅为图标、名称、`整改中` 和 `内容整改中`。在 `qinwu/index.html` 的标题后增加：

```html
<div class="empty-state">内容整改中</div>
```

- [ ] **Step 2: 恢复小程序首页入口**

在 `pages/index/index.js` 的 `show` 状态和搜索卡中恢复 `qinwu`，搜索文本只用 `巡防勤务 内容整改中`。在 `index.wxml` 恢复巡防勤务卡，内容仅显示名称和整改状态。

- [ ] **Step 3: 改造小程序栏目页与旧详情行为**

`pages/qinwu/index/index.js` 仅保留普通页面声明；`index.wxml` 只显示导航、栏目标题和“内容整改中”。`pages/qinwu/detail/detail.js` 不导入数据，在加载时提示“内容整改中”并 `wx.redirectTo` 返回 `/pages/qinwu/index/index`。

- [ ] **Step 4: 运行专项测试**

Run: `python -m unittest tests.test_sensitive_content_removal -v`

Expected: 全部 PASS。

### Task 3: 全量验证、合并与推送

**Files:**
- No additional production files.

**Interfaces:**
- Consumes: Task 2 的栏目壳实现。
- Produces: 已验证并同步到 `origin/master` 的整改栏目壳。

- [ ] **Step 1: 运行全量验证**

Run:

```powershell
python -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
```

Expected: 所有测试 PASS，diff check 无错误，24 个删除文件继续不存在。

- [ ] **Step 2: 提交实现**

```powershell
git add tests/test_sensitive_content_removal.py index.html qinwu/index.html miniprogram/pages/index miniprogram/pages/qinwu
git commit -m "fix: restore qinwu remediation shell"
```

- [ ] **Step 3: 合并到 master 并重新验证**

快进合并功能分支到 `master`，再次运行全量测试。

- [ ] **Step 4: 推送**

Run: `git push origin master`

Expected: `origin/master` 与本地 `master` 指向同一提交。
