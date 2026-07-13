# 主题选择 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement task-by-task.

**Goal:** 提供可持久化的暖警蓝、经典暖棕、日间浅色和夜间深色主题选择。

**Architecture:** `theme.js` 在页面加载初期给根元素设置 `data-theme`；CSS 通过变量覆盖主题色；`nav.js` 渲染并绑定选择器。页面结构、内容和搜索不变。

**Tech Stack:** HTML、CSS、自执行原生 JavaScript、Python `unittest`。

## Tasks

### Task 1: 主题变量与持久化脚本

**Files:** Create `js/theme.js`, modify `css/style.css`, create `tests/test_theme_assets.py`, modify all HTML pages that load `js/nav.js`.

- [ ] 写失败测试：断言 `theme.js` 含四个主题名、`xunfang-theme`、`localStorage` 容错；断言 CSS 含四个 `html[data-theme]` 覆盖。
- [ ] 运行 `python -m unittest tests/test_theme_assets.py -v`，确认失败。
- [ ] 实现 `theme.js`：仅接受四个主题名；读取存储失败时回退 `warm-police-blue`；设置 `document.documentElement.dataset.theme`；导出全局 `window.XunfangTheme.set(theme)` 并保存选择。
- [ ] 在所有现有页面的 `nav.js` 前插入 `<script src="…/js/theme.js"></script>`，相对路径与原有 `nav.js` 路径一致。
- [ ] 在 CSS 增加经典暖棕、日间、夜间覆盖变量；每套主题都定义背景、卡片、文字、导航、边框、主色和强调色。
- [ ] 重跑测试并提交 `feat: add persistent color themes`。

### Task 2: 导航选择器与回归

**Files:** Modify `js/nav.js`, `css/style.css`, `tests/test_theme_assets.py`.

- [ ] 写失败测试：断言导航包含可访问的主题按钮、四个主题选项和当前主题状态。
- [ ] 实现导航“外观”按钮与下拉选项；点击调用 `window.XunfangTheme.set`，更新选中状态；手机菜单中同一控件保持可访问。
- [ ] 为按钮、菜单、选中态和夜间主题补充样式，不修改既有链接计算、栏目数组或汉堡菜单事件。
- [ ] 运行 `python -m unittest tests/test_brand_styles.py tests/test_theme_assets.py -v`，确认全部通过；手动检查首页、栏目页、文章页和搜索页的四种主题与刷新持久化。
- [ ] 提交 `feat: add theme selector`。

### Task 3: 上线前验证

- [ ] 运行两个静态测试文件和 `git diff --check`。
- [ ] 在桌面和 390px 窄屏检查导航、主题菜单、搜索和每月专题的可读性。
- [ ] 确认未修改内容数据、链接或 `search-index.json` 后推送 `master` 触发上线。
