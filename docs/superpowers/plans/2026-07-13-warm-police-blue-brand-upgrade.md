# 暖警蓝品牌升级 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不改变既有信息架构和交互逻辑的前提下，将巡防百科统一升级为温暖、专业的暖警蓝视觉系统。

**Architecture:** 仅调整 `css/style.css` 的设计令牌和既有组件选择器。HTML、JavaScript、`search-index.json` 与内容数据保持不变，导航、搜索和栏目链接沿用现状。新增一个 Python 标准库静态断言，防止关键品牌令牌在后续修改中分叉。

**Tech Stack:** 静态 HTML、CSS、原生 JavaScript、Python 标准库 `unittest`。

## Global Constraints

- 不改变首页结构、六个栏目卡片的顺序、文案或相对链接。
- 不修改 `index.html`、`js/nav.js`、搜索逻辑、内容数据或 `search-index.json`。
- 主警蓝固定为 `#1F4E79`，深警蓝为 `#163A5C`，雾蓝为 `#EAF2F8`，暖白为 `#FFFCF7`，琥珀橙为 `#D98B2B`。
- 保持既有单文件共享样式架构，不引入 CSS 框架或构建依赖。
- 手动检查桌面与手机窄屏；不提交 `.env`、`.netlify/`、缓存或 PPT 文件。

---

## File Structure

- Modify: `css/style.css` — 暖警蓝令牌与全站组件样式。
- Create: `tests/test_brand_styles.py` — 读取共享 CSS，断言令牌和关键组件。

### Task 1: 建立品牌令牌与基础表面

**Files:**

- Create: `tests/test_brand_styles.py`
- Modify: `css/style.css:4-35`、`css/style.css:49-124`、`css/style.css:157-223`
- Test: `tests/test_brand_styles.py`

**Interfaces:**

- Consumes: `:root` 变量以及 `.topnav`、`.search-bar input`、`.module-card`、`.content-item`、`.list-page .list-item`。
- Produces: `--police-blue`、`--police-blue-deep`、`--mist-blue`、`--warm-white`、`--amber`、`--border`、`--radius` 与 `--shadow`。

- [ ] **Step 1: 写入会失败的品牌令牌静态测试**

```python
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'css' / 'style.css').read_text(encoding='utf-8')

def declaration(name):
    match = re.search(rf'{re.escape(name)}:\\s*([^;]+);', CSS)
    return match.group(1).strip() if match else None

class BrandStyleTests(unittest.TestCase):
    def test_warm_police_blue_tokens_are_defined(self):
        self.assertEqual(declaration('--police-blue'), '#1F4E79')
        self.assertEqual(declaration('--police-blue-deep'), '#163A5C')
        self.assertEqual(declaration('--mist-blue'), '#EAF2F8')
        self.assertEqual(declaration('--warm-white'), '#FFFCF7')
        self.assertEqual(declaration('--amber'), '#D98B2B')
        self.assertEqual(declaration('--radius'), '12px')

    def test_base_components_consume_shared_tokens(self):
        self.assertIn('background: var(--police-blue);', CSS)
        self.assertIn('background: var(--warm-white);', CSS)
        self.assertIn('border-radius: var(--radius);', CSS)

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests/test_brand_styles.py -v`

Expected: `test_warm_police_blue_tokens_are_defined` 失败，因为现有样式缺少规划令牌，且 `--radius` 不是 `12px`。

- [ ] **Step 3: 更新 `:root` 与基础选择器**

将 `:root` 颜色和表面令牌设置为：

```css
--bg: #EAF2F8;
--warm-white: #FFFCF7;
--card-bg: var(--warm-white);
--text: #243447;
--text-secondary: #40566B;
--text-muted: #60758C;
--nav-bg: #1F4E79;
--police-blue: #1F4E79;
--police-blue-deep: #163A5C;
--mist-blue: #EAF2F8;
--nav-text: #FFFFFF;
--amber: #D98B2B;
--border: #D8E2EC;
--shadow: 0 6px 18px rgba(22, 58, 92, 0.08);
--radius: 12px;
```

保留既有 `--accent-*` 语义令牌，并更新基础组件：

```css
body { background: var(--mist-blue); }
.topnav { background: var(--police-blue); }
.topnav .nav-links a.active { color: var(--amber); border-bottom-color: var(--amber); }
.search-bar input { background: var(--warm-white); border-color: var(--border); border-radius: var(--radius); }
.search-bar input:focus { outline: 3px solid rgba(31, 78, 121, 0.18); border-color: var(--police-blue); }
.module-card, .content-item, .list-page .list-item { background: var(--warm-white); border-radius: var(--radius); box-shadow: var(--shadow); }
```

- [ ] **Step 4: 验证基础样式**

Run: `python -m unittest tests/test_brand_styles.py -v`

Expected: 2 个测试均为 `ok`，最后显示 `OK`。

- [ ] **Step 5: 提交基础视觉令牌与断言**

```bash
git add css/style.css tests/test_brand_styles.py
git commit -m "style: add warm police blue foundation"
```

### Task 2: 统一专题、文章与搜索组件

**Files:**

- Modify: `tests/test_brand_styles.py`
- Modify: `css/style.css:292-512`、`css/style.css:553-746`
- Test: `tests/test_brand_styles.py`

**Interfaces:**

- Consumes: Task 1 的品牌令牌。
- Produces: `.quick-card`、`.step-card`、`.daily-card`、`.monthly-hero`、`.magazine-*`、`.search-dropdown` 和 `.search-page .result-card` 的一致外观。

- [ ] **Step 1: 扩展会失败的专题组件测试**

在 `BrandStyleTests` 中追加：

```python
    def test_feature_components_use_warm_police_blue_tokens(self):
        self.assertIn('background: linear-gradient(135deg, var(--police-blue-deep) 0%, var(--police-blue) 100%);', CSS)
        self.assertIn('background: var(--amber);', CSS)
        self.assertIn('border-left: 4px solid var(--police-blue);', CSS)
        self.assertIn('box-shadow: var(--shadow);', CSS)
```

- [ ] **Step 2: 运行测试并确认新增断言失败**

Run: `python -m unittest tests/test_brand_styles.py -v`

Expected: 前两项通过，`test_feature_components_use_warm_police_blue_tokens` 失败，因为月度专题仍使用硬编码蓝色和金色。

- [ ] **Step 3: 接入专题、内容与搜索样式**

保留既有选择器和媒体查询，加入或替换下列规则：

```css
.quick-card { background: var(--warm-white); border-left: 4px solid var(--police-blue); border-radius: var(--radius); box-shadow: var(--shadow); }
.daily-card, .search-dropdown, .search-page .result-card, .magazine-archive .archive-card { background: var(--warm-white); border-color: var(--border); border-radius: var(--radius); box-shadow: var(--shadow); }
.monthly-hero-inner, .magazine-cover .cover-placeholder { background: linear-gradient(135deg, var(--police-blue-deep) 0%, var(--police-blue) 100%); }
.monthly-hero .hero-label, .magazine-header .magazine-month, .magazine-archive .archive-card .archive-date { color: var(--amber); }
.monthly-hero .hero-link { background: var(--amber); color: var(--police-blue-deep); border-radius: var(--radius); }
.monthly-hero .hero-link:hover { background: #C87922; }
.nav-links a.monthly-link { color: var(--amber) !important; border-color: var(--amber); border-radius: var(--radius); }
```

将上述组件中残留的表面背景 `var(--bg)` 改为 `var(--mist-blue)`；步骤卡的 `--accent-*` 风险语义色保持不变。

- [ ] **Step 4: 验证专题组件**

Run: `python -m unittest tests/test_brand_styles.py -v`

Expected: 3 个测试均为 `ok`，最后显示 `OK`。

- [ ] **Step 5: 手动回归关键页面**

Run: `python -m http.server 8000`

Open and verify:

1. `http://localhost:8000/index.html`：月度横幅为警蓝渐变、入口为琥珀橙，六卡片链接与顺序不变。
2. `http://localhost:8000/jingqing/index.html`：列表卡、标签、悬停状态与文章链接正常。
3. `http://localhost:8000/search.html?q=%E8%AD%A6%E6%83%85`：搜索结果与高亮清晰，搜索下拉不被遮挡。
4. 任一文章页：步骤卡保留风险语义色，正文与元信息可读。

Expected: 桌面与 390px 窄屏均无横向滚动；导航展开、搜索下拉正常；控制台无新增错误，样式表无 404。

- [ ] **Step 6: 提交共享组件升级**

```bash
git add css/style.css tests/test_brand_styles.py
git commit -m "style: unify site components with warm police blue"
```

### Task 3: 发布前回归与工作区核对

**Files:**

- Modify: 无
- Test: `tests/test_brand_styles.py`

**Interfaces:**

- Consumes: Task 1 和 Task 2 的共享 CSS 令牌与静态断言。
- Produces: 可交付的回归结果，不产生运行时代码。

- [ ] **Step 1: 执行完整静态断言**

Run: `python -m unittest tests/test_brand_styles.py -v`

Expected: 所有测试为 `ok`，总结果为 `OK`。

- [ ] **Step 2: 检查变更范围与格式**

Run: `git status --short; git diff HEAD~2..HEAD --check`

Expected: 除用户已有未跟踪的 `公安警察工作汇报PPT.pptx` 外，只包含本计划文件；`git diff --check` 无输出并以 0 退出。

- [ ] **Step 3: 记录手动回归结果**

在最终交付中逐项报告首页、栏目列表、文章页、搜索页、每月一学页的桌面与 390px 窄屏结果，并确认导航、搜索下拉、链接和控制台正常。

## Plan Self-Review

- Spec coverage: Task 1 覆盖全局色彩、导航、搜索、首页卡片和移动端基础；Task 2 覆盖步骤、专题、文章、搜索和语义色保留；Task 3 覆盖链接、控制台、窄屏、工作区和格式回归。
- 占位检查: 未发现占位步骤或未定义接口。
- Type consistency: 三个测试方法复用同一 `CSS` 字符串和 `declaration()` 函数；令牌名称在所有任务中一致。
