# 每月一学模块实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将首页嵌入式"每日一学"改造为独立的"每月一学"品牌模块 — 首页大幅精选横幅 + 杂志化内页 + data.js 配置驱动。

**Architecture:** 静态 HTML + JS 驱动的杂志化模块。`data.js` 作为元数据配置，首页横幅和内页均由 JS 读取配置动态渲染。当月内容内联在 `index.html` 中，历史月份独立 HTML 文件归档。导航栏新增金色高亮入口。

**Tech Stack:** 纯静态 HTML + CSS + Vanilla JS（与现有项目一致）

## Global Constraints

- 零框架依赖，纯静态文件
- CSS 变量统一在 `css/style.css` `:root` 中管理
- 导航通过 `js/nav.js` MODULES 数组 + `renderNav()` IIFE 自执行
- 路径深度计算沿用现有 `moduleDirs` 逻辑
- 所有 JS 通过 `<script>` 标签加载，无模块系统
- 目标仓库：`F:/frank第二大脑/xunfang-baike/`
- 部署方式：`git push origin master` → GitHub Pages 自动部署

---

### Task 1: 新建 `meiyueyixue/data.js` — 元数据配置文件

**Files:**
- Create: `meiyueyixue/data.js`

**Interfaces:**
- Produces: 全局变量 `monthlyData = { current: string, articles: { [key: string]: { theme, summary, author, tags, image, file } } }`
- Consumed by: `js/monthly-hero.js` (Task 3), `meiyueyixue/index.html` (Task 6)

- [ ] **Step 1: 创建 data.js 初始版本**

```js
// meiyueyixue/data.js
var monthlyData = {
  current: "2026-07",
  articles: {
    "2026-07": {
      theme: "车辆盘查战术要点",
      summary: "本月经典案例复盘 + 最新执法规范解读",
      author: "巡防百科编辑部",
      tags: ["盘查", "车辆", "战术"],
      image: "",
      file: "2026-07.html"
    }
  }
};
```

- [ ] **Step 2: 提交**

```bash
cd "F:/frank第二大脑/xunfang-baike"
git add meiyueyixue/data.js
git commit -m "feat: add monthly learning metadata config (data.js)"
```

---

### Task 2: 新增 CSS 样式 — 首页横幅 + 杂志页 + 金色导航

**Files:**
- Modify: `css/style.css`

**Interfaces:**
- Produces: CSS 类族 `.monthly-hero`, `.magazine-*`, `.nav-links a.monthly-link`
- Consumed by: `index.html` (Task 5), `meiyueyixue/index.html` (Task 6), `js/nav.js` (Task 4)

- [ ] **Step 1: 在 style.css 末尾追加全部新样式**

在 `css/style.css` 文件末尾（第594行之后）追加以下内容：

```css
/* === 每月一学首页横幅 === */
.monthly-hero {
  max-width: var(--max-width);
  margin: 0 auto 24px;
  padding: 0 16px;
}

.monthly-hero-inner {
  background: var(--nav-bg);
  border-radius: 8px;
  padding: 32px 36px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: relative;
  overflow: hidden;
}

.monthly-hero-inner::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 120px; height: 120px;
  background: radial-gradient(circle, rgba(212,168,67,0.15) 0%, transparent 70%);
  pointer-events: none;
}

.monthly-hero .hero-label {
  font-size: 12px;
  color: #d4a843;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: 600;
}

.monthly-hero .hero-theme {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
  line-height: 1.3;
}

.monthly-hero .hero-summary {
  font-size: 14px;
  color: #bbb;
  line-height: 1.6;
}

.monthly-hero .hero-link {
  display: inline-block;
  margin-top: 6px;
  padding: 8px 20px;
  background: #d4a843;
  color: #1a1a2e;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  align-self: flex-start;
  transition: background 0.15s;
}

.monthly-hero .hero-link:hover {
  background: #c59a30;
  text-decoration: none;
}

@media (max-width: 600px) {
  .monthly-hero-inner {
    padding: 24px 20px;
  }
  .monthly-hero .hero-theme {
    font-size: 20px;
  }
}

/* === 导航栏金色入口 === */
.nav-links a.monthly-link {
  color: #d4a843 !important;
  font-weight: 600;
  border: 1px solid #d4a843;
  border-radius: 4px;
  padding: 2px 10px;
}

.nav-links a.monthly-link:hover {
  background: rgba(212,168,67,0.15);
}

.nav-links a.monthly-link.active {
  background: #d4a843;
  color: #1a1a2e !important;
  border-bottom: none;
}

/* === 杂志内页 === */
.magazine-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px 60px;
}

.magazine-header {
  text-align: center;
  padding: 40px 0 32px;
}

.magazine-header .magazine-month {
  font-size: 14px;
  color: #d4a843;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.magazine-header .magazine-title {
  font-size: 28px;
  font-weight: bold;
  color: var(--text);
  line-height: 1.3;
  margin-bottom: 12px;
}

.magazine-header .magazine-subtitle {
  font-size: 15px;
  color: var(--text-muted);
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.magazine-cover {
  margin: 0 auto 36px;
  max-width: 700px;
}

.magazine-cover img {
  width: 100%;
  border-radius: 6px;
  border: 1px solid var(--border);
}

.magazine-cover .cover-placeholder {
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, var(--nav-bg) 0%, #34495e 100%);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #d4a843;
  font-size: 48px;
}

.magazine-body {
  font-size: 15px;
  line-height: 1.9;
  color: var(--text-secondary);
}

.magazine-body h2 {
  font-size: 20px;
  color: var(--text);
  margin: 36px 0 14px;
  padding-left: 12px;
  border-left: 3px solid #d4a843;
}

.magazine-body h2:first-child {
  margin-top: 0;
}

.magazine-body p {
  margin-bottom: 14px;
}

.magazine-body ul,
.magazine-body ol {
  margin: 8px 0 16px 20px;
}

.magazine-body li {
  margin-bottom: 6px;
}

.magazine-body blockquote {
  margin: 16px 0;
  padding: 12px 18px;
  background: var(--bg);
  border-left: 3px solid var(--accent-orange);
  border-radius: var(--radius);
  font-size: 14px;
  color: var(--text-muted);
}

/* 参考资料区 */
.magazine-refs {
  margin-top: 40px;
  padding: 20px 24px;
  background: var(--bg);
  border-radius: 6px;
}

.magazine-refs h3 {
  font-size: 15px;
  color: var(--text);
  margin-bottom: 10px;
}

.magazine-refs a {
  display: block;
  font-size: 13px;
  color: var(--accent-blue);
  margin-bottom: 4px;
}

/* 往期精选 */
.magazine-archive {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 2px solid var(--border);
}

.magazine-archive h3 {
  font-size: 16px;
  color: var(--text);
  margin-bottom: 16px;
}

.magazine-archive .archive-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

@media (max-width: 600px) {
  .magazine-archive .archive-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .magazine-header .magazine-title {
    font-size: 22px;
  }
  .magazine-body h2 {
    font-size: 18px;
  }
}

.magazine-archive .archive-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 16px;
  text-align: center;
  box-shadow: var(--shadow);
  transition: transform 0.15s;
  display: block;
  text-decoration: none;
}

.magazine-archive .archive-card:hover {
  transform: translateY(-2px);
  text-decoration: none;
}

.magazine-archive .archive-card .archive-date {
  font-size: 12px;
  color: #d4a843;
  margin-bottom: 6px;
}

.magazine-archive .archive-card .archive-title {
  font-size: 14px;
  font-weight: bold;
  color: var(--text);
}
```

- [ ] **Step 2: 提交**

```bash
git add css/style.css
git commit -m "style: add monthly-hero, magazine page, and gold nav styles"
```

---

### Task 3: 新建 `js/monthly-hero.js` — 首页横幅渲染

**Files:**
- Create: `js/monthly-hero.js`

**Interfaces:**
- Consumes: `monthlyData` 全局变量（由 `meiyueyixue/data.js` 定义，Task 1）
- Produces: 渲染 `#monthly-hero-placeholder` 为横幅 HTML
- 容错：如果 `monthlyData` 未定义或 DOM 容器不存在，静默退出

- [ ] **Step 1: 创建 monthly-hero.js**

```js
// js/monthly-hero.js
(function() {
  if (typeof monthlyData === 'undefined') return;

  var placeholder = document.getElementById('monthly-hero-placeholder');
  if (!placeholder) return;

  var currentKey = monthlyData.current;
  var article = monthlyData.articles[currentKey];
  if (!article) return;

  var parts = currentKey.split('-');
  var label = parts[0] + '年' + parseInt(parts[1]) + '月 · 每月一学';

  var html =
    '<div class="monthly-hero">' +
      '<div class="monthly-hero-inner">' +
        '<div class="hero-label">' + label + '</div>' +
        '<div class="hero-theme">' + article.theme + '</div>' +
        '<div class="hero-summary">' + article.summary + '</div>' +
        '<a href="meiyueyixue/index.html" class="hero-link">查看全文 →</a>' +
      '</div>' +
    '</div>';

  placeholder.outerHTML = html;
})();
```

- [ ] **Step 2: 提交**

```bash
git add js/monthly-hero.js
git commit -m "feat: add monthly hero banner renderer for homepage"
```

---

### Task 4: 更新 `js/nav.js` — 添加每月一学导航入口

**Files:**
- Modify: `js/nav.js`

**Interfaces:**
- 扩展 MODULES 数组，新增第 7 项「本月精选」
- `renderNav()` 中对该项输出特殊 CSS class `monthly-link`
- 深度计算逻辑需包含 `meiyueyixue`

- [ ] **Step 1: 修改 MODULES 数组**

在 `js/nav.js` 中，将 MODULES 数组替换为包含第 7 项的新数组，并修改链接渲染逻辑。

定位到 `var MODULES = [...]`（第3-10行），替换为：

```js
  var MODULES = [
    { name: '装备介绍', path: 'zhuangbei/index.html',  emoji: '🛡️' },
    { name: '巡防勤务', path: 'qinwu/index.html',      emoji: '📋' },
    { name: '警务训练', path: 'xunlian/index.html',    emoji: '⚔️' },
    { name: '警情处置', path: 'jingqing/index.html',    emoji: '🚨' },
    { name: '法条规范', path: 'fagui/index.html',       emoji: '📕' },
    { name: '走访送教', path: 'zoufang/index.html',     emoji: '🏫' },
    { name: '本月精选', path: 'meiyueyixue/index.html', emoji: '⭐', special: true }
  ];
```

- [ ] **Step 2: 修改 linksHtml 渲染逻辑**

将 `var linksHtml = MODULES.map(...)` 中的 `<a>` 标签替换为带条件 class 的版本。

将原有行（第34行）：
```js
      return '<a href="' + href + '"' + (isActive ? ' class="active"' : '') + '>'
           + m.emoji + ' ' + m.name + '</a>';
```

替换为：
```js
      var cls = (m.special ? 'monthly-link' : '') + (isActive ? ' active' : '');
      return '<a href="' + href + '" class="' + cls.trim() + '">'
           + m.emoji + ' ' + m.name + '</a>';
```

注：`cls` 为空字符串时输出 `class=""`，HTML 合法且无副作用。

- [ ] **Step 3: 提交**

```bash
git add js/nav.js
git commit -m "feat: add monthly-learning nav entry with gold styling"
```

---

### Task 5: 更新 `index.html` — 首页集成横幅 + 加载依赖

**Files:**
- Modify: `index.html`

**Interfaces:**
- 在搜索栏与卡片网格之间插入 `<div id="monthly-hero-placeholder"></div>`
- 在 `<script src="js/nav.js"></script>` 之前加载 `meiyueyixue/data.js` 和 `js/monthly-hero.js`
- 保留每日一学区不变

- [ ] **Step 1: 插入横幅占位符**

在 `index.html` 第16行（`<div class="card-grid">` 之前）插入：

```html
<div id="monthly-hero-placeholder"></div>
```

- [ ] **Step 2: 添加脚本加载**

在 `<script src="js/nav.js"></script>` 之前（第66行）插入：

```html
<script src="meiyueyixue/data.js"></script>
<script src="js/monthly-hero.js"></script>
```

最终脚本加载顺序应为：
```html
<script src="meiyueyixue/data.js"></script>
<script src="js/monthly-hero.js"></script>
<script src="js/nav.js"></script>
<script src="js/main.js"></script>
```

- [ ] **Step 3: 提交**

```bash
git add index.html
git commit -m "feat: add monthly hero banner to homepage"
```

---

### Task 6: 创建 `meiyueyixue/index.html` — 杂志化内页模板

**Files:**
- Create: `meiyueyixue/index.html`

**Interfaces:**
- Consumes: `monthlyData`（由 `../meiyueyixue/data.js` 加载，但内页路径下的 `data.js` 就在同目录）
- JS 读取 `monthlyData` 渲染头部元数据和底部往期精选
- 文章正文直接写死在 HTML 中（当月内容，下月归档时重命名）
- 往期精选从 `monthlyData.articles` 去重当前月份后按日期倒序生成

- [ ] **Step 1: 创建杂志内页 HTML**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>本月精选 — 巡防百科</title>
<link rel="stylesheet" href="../css/style.css">
</head>
<body>

<div id="nav-placeholder"></div>

<div class="breadcrumb">
  <a href="../index.html">首页</a> &gt;
  <span class="current">本月精选</span>
</div>

<div class="magazine-page">
  <div class="magazine-header" id="magazineHeader"></div>

  <div class="magazine-cover" id="magazineCover"></div>

  <div class="magazine-body">
    <!-- 当月文章正文内联在此 -->
    <h2>一、场景概述</h2>
    <p>文章内容由 Obsidian 素材整合生成。</p>

    <h2>二、核心要点</h2>
    <p>待填充。</p>

    <h2>三、经典案例复盘</h2>
    <p>待填充。</p>

    <h2>四、法规依据速查</h2>
    <p>待填充。</p>

    <h2>五、实操注意事项</h2>
    <p>待填充。</p>
  </div>

  <div class="magazine-refs" id="magazineRefs">
    <h3>参考资料</h3>
    <p style="color:var(--text-muted);font-size:13px;">本期内容整合自以下 Obsidian 知识库笔记。</p>
  </div>

  <div class="magazine-archive">
    <h3>往期精选</h3>
    <div class="archive-grid" id="archiveGrid"></div>
  </div>
</div>

<script src="data.js"></script>
<script src="../js/nav.js"></script>
<script>
(function() {
  if (typeof monthlyData === 'undefined') return;

  var currentKey = monthlyData.current;
  var article = monthlyData.articles[currentKey];
  if (!article) return;

  // 渲染头部
  var parts = currentKey.split('-');
  var monthLabel = parts[0] + '年' + parseInt(parts[1]) + '月';
  document.getElementById('magazineHeader').innerHTML =
    '<div class="magazine-month">' + monthLabel + '</div>' +
    '<h1 class="magazine-title">' + article.theme + '</h1>' +
    '<div class="magazine-subtitle">' + article.summary + '</div>';

  // 渲染封面
  var cover = document.getElementById('magazineCover');
  if (article.image) {
    cover.innerHTML = '<img src="../' + article.image + '" alt="' + article.theme + '" loading="lazy">';
  } else {
    cover.innerHTML = '<div class="cover-placeholder">⭐</div>';
  }

  // 渲染参考资料
  if (article.tags && article.tags.length) {
    var refsDiv = document.getElementById('magazineRefs');
    var tagHtml = article.tags.map(function(t) {
      return '<span class="tag" style="margin-right:6px;">' + t + '</span>';
    }).join('');
    refsDiv.innerHTML = '<h3>参考资料</h3>' +
      '<p style="color:var(--text-muted);font-size:13px;">本期内容整合自 Obsidian 知识库警务技能笔记。</p>' +
      '<div style="margin-top:8px;">' + tagHtml + '</div>';
  }

  // 渲染往期精选（排除当前月份）
  var archiveKeys = Object.keys(monthlyData.articles)
    .filter(function(k) { return k !== currentKey; })
    .sort()
    .reverse();

  var archiveGrid = document.getElementById('archiveGrid');
  if (archiveKeys.length === 0) {
    archiveGrid.innerHTML = '<p style="color:var(--text-muted);font-size:13px;">暂无往期内容，敬请期待。</p>';
    return;
  }

  var cardsHtml = archiveKeys.map(function(key) {
    var a = monthlyData.articles[key];
    var displayDate = key.split('-').join('年') + '月';
    return '<a href="' + (a.file || (key + '.html')) + '" class="archive-card">' +
      '<div class="archive-date">' + displayDate + '</div>' +
      '<div class="archive-title">' + a.theme + '</div>' +
      '</a>';
  }).join('');

  archiveGrid.innerHTML = cardsHtml;
})();
</script>

</body>
</html>
```

- [ ] **Step 2: 提交**

```bash
git add meiyueyixue/index.html
git commit -m "feat: create magazine-style monthly learning page template"
```

---

### Task 7: 撰写首月内容（2026年7月）并验证

**Files:**
- Modify: `meiyueyixue/index.html`（替换正文占位符为实际内容）
- Modify: `meiyueyixue/data.js`（更新主题如需要）

**说明:**
- 此步需要读取 Obsidian 知识库 `03_Knowledge/警务技能/` 下的相关笔记
- 根据素材丰度确定最终主题，可能调整 `data.js` 中的 theme/summary
- 文章正文替换模板中的占位段落

- [ ] **Step 1: 扫描 Obsidian 知识库，确定主题**

```bash
ls "F:/frank第二大脑/frank知识库/03_Knowledge/警务技能/"
```

检查各子目录下的 .md 笔记，找出素材最丰富、适合开篇的方向。目前已知巡逻盘查目录有6篇笔记，素材充足，以此作为首月主题候选。

- [ ] **Step 2: 精读素材 + 撰写长文**

读取相关 Obsidian 笔记内容，整合为五段式结构化长文（场景概述 → 核心要点 → 经典案例 → 法规依据 → 实操注意）。
将文章 HTML 替换 `meiyueyixue/index.html` 中 `<div class="magazine-body">` 内的占位段落。
如有必要，更新 `data.js` 中的 theme/summary 以匹配最终内容。

- [ ] **Step 3: 提交首月内容**

```bash
git add meiyueyixue/
git commit -m "feat: first monthly learning article (2026-07)"
```

- [ ] **Step 4: 本地验证**

用浏览器打开 `index.html`，检查：
- 首页横幅是否显示当月主题和摘要
- 点击「查看全文」是否进入杂志页
- 导航栏「本月精选」金色按钮是否高亮
- 杂志页头部、正文、往期精选是否正常渲染
- 移动端（≤600px）布局是否正常

- [ ] **Step 5: 部署**

```bash
git push origin master
```
