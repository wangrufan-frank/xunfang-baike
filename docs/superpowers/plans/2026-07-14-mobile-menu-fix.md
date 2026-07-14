# 手机端菜单修复实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 消除手机端汉堡菜单的重复点击处理，使每次点击只切换一次菜单状态。

**Architecture:** 保留 `js/nav.js` 作为导航注入和交互的唯一负责人，从 `js/main.js` 删除重复的汉堡事件委托。以回归测试锁定单一监听所有权，并运行全量测试防止影响搜索、主题和敏感内容整改状态。

**Tech Stack:** JavaScript、Python `unittest`

## Global Constraints

- 不修改导航结构、CSS、主题选择器或内容数据。
- 不处理单机微信代理状态，不迁移网站托管。
- 不提交现有未跟踪 PPT。

---

### Task 1: 建立失败回归测试

**Files:**
- Modify: `tests/test_theme_assets.py`

- [ ] 新增 `test_hamburger_has_single_click_owner`，断言 `js/nav.js` 包含 `.hamburger` 和点击监听，`js/main.js` 不包含 `.hamburger`。
- [ ] 运行该测试，确认因 `js/main.js` 仍有重复监听而失败。

### Task 2: 删除重复监听

**Files:**
- Modify: `js/main.js`

- [ ] 删除 `DOMContentLoaded` 内第一个“汉堡菜单切换”事件委托块，保留搜索和折叠展开逻辑。
- [ ] 运行专项测试和全量测试，预期全部通过。
- [ ] 运行 `git diff --check`，预期无错误。
- [ ] 提交：`fix: prevent duplicate mobile menu toggle`。

### Task 3: 合并与推送

- [ ] 快进合并功能分支到 `master`。
- [ ] 在主工作区重新运行全量测试。
- [ ] 清理隔离工作树和已合并分支。
- [ ] 推送 `master` 到已确认可信的 `origin/master`。
- [ ] 核对本地与远程提交一致。
