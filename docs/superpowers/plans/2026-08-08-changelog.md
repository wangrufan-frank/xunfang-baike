# 更新记录板块实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为巡防百科新增"更新记录"板块：独立页 `changelog.html` + JSON 数据驱动渲染，导航栏首位加入醒目琥珀色徽章入口，记录本次"伤员救助与急救"内容更新。

**Architecture:** 数据存于 `data/updates.json`，由 `js/changelog.js` 读取并渲染到 `changelog.html` 的内容区；导航入口在 `js/nav.js` 的 MODULES 数组首位新增 `featured` 标记项，`css/style.css` 增加 `.changelog-link` 琥珀实心徽章样式（桌面横排 + 移动端汉堡下拉均生效）。

**Tech Stack:** 静态 HTML + 原生 JS + JSON；Python 3.12（完整路径 `C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe`，本会话内 `python` 命令被商店占位符遮蔽）、Node.js 24。

## Global Constraints

- 设计文档：`E:\xunfang-baike\docs\superpowers\specs\2026-08-08-changelog-design.md`（已确认）
- 导航入口放**首位**、**醒目**（填充琥珀色徽章、深色文字、高对比）；移动端汉堡下拉同为第一项
- 条目格式：仅日期 + 内容描述，无版本号
- 只记本次更新（2026-08-08 伤员救助与急救），不追溯历史
- 首页不加入口；changelog 页**不纳入搜索索引**（无 `.article-page` 标记）
- 不改动六个内容模块与既有数据台账；只新增 changelog.html、data/updates.json、js/changelog.js，修改 js/nav.js、css/style.css
- 全部中文；验证全绿（链接/索引/来源/测试）
- 所有命令本会话用完整 Python 路径 `PY="C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe"`

---
## 文件结构

**新建：**
- `data/updates.json` — 更新记录数据
- `js/changelog.js` — 读取数据并渲染
- `changelog.html` — 更新记录页面

**修改：**
- `js/nav.js` — MODULES 数组首位加 featured 项；renderNav 类逻辑加 changelog-link
- `css/style.css` — `.changelog-link` 徽章样式 + changelog 页条目样式 + 移动端适配

**模板参考：**
- 页面结构：`search.html`（根目录独立页：认证脚本 + nav-placeholder + 面包屑）
- 面包屑/页头：`jingqing/index.html`（`.page-container.list-page` + `.page-title`）
- 导航标记样式：`css/style.css` 的 `.nav-links a.monthly-link`（约 797-815 行）

---
### Task 1: 数据文件与渲染器

**Files:**
- Create: `E:\xunfang-baike\data\updates.json`
- Create: `E:\xunfang-baike\js\changelog.js`

**Interfaces:**
- Consumes: 设计文档 §3② 的本次更新内容
- Produces: `data/updates.json`（供 changelog.js 读取）、`js/changelog.js`（供 changelog.html 引入）

- [ ] **Step 1: 写 `data/updates.json`**
```json
{
  "version": 1,
  "updates": [
    {
      "date": "2026-08-08",
      "title": "新增「伤员救助与急救」内容",
      "items": [
        "警情处置新增《救助类警情处置流程》（含现场舆情管控环节）",
        "实战训练新增《心肺复苏操作要点》《止血、包扎与伤员搬运》",
        "装备操作新增《急救包组成与使用》《AED 使用方法》",
        "教育学习新增《场所急救设施与AED部署检查》",
        "同步完善搜索索引、来源台账与站内导航"
      ]
    }
  ]
}
```
- [ ] **Step 2: 写 `js/changelog.js`**（读取 JSON、转义渲染、错误兜底）
```javascript
// js/changelog.js
(function() {
  function escapeHtml(str) {
    return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  function render(updates) {
    var listEl = document.getElementById('changelog-list');
    if (!listEl) return;
    if (!updates || !updates.length) {
      listEl.innerHTML = '<div class="changelog-empty">暂无更新记录</div>';
      return;
    }
    var html = '';
    for (var i = 0; i < updates.length; i++) {
      var u = updates[i];
      html += '<div class="changelog-entry">'
        + '<div class="changelog-date">' + escapeHtml(u.date) + '</div>'
        + '<div class="changelog-title">' + escapeHtml(u.title) + '</div>'
        + '<ul class="changelog-items">';
      for (var j = 0; j < u.items.length; j++) {
        html += '<li>' + escapeHtml(u.items[j]) + '</li>';
      }
      html += '</ul></div>';
    }
    listEl.innerHTML = html;
  }
  function fail() {
    var listEl = document.getElementById('changelog-list');
    if (listEl) listEl.innerHTML = '<div class="changelog-empty">更新记录加载失败</div>';
  }
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'data/updates.json', true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      try { render(JSON.parse(xhr.responseText).updates); }
      catch (e) { fail(); }
    } else { fail(); }
  };
  xhr.onerror = fail;
  xhr.send();
})();
```
- [ ] **Step 3: 校验**
  - JSON 有效：`"$PY" -c "import json;d=json.load(open('data/updates.json',encoding='utf-8'));assert d['updates'][0]['date']=='2026-08-08'"`
  - JS 语法：`node --check js/changelog.js`

- [ ] **Step 4: 提交**
```bash
cd /e/xunfang-baike
git add data/updates.json js/changelog.js
git commit -m "feat: 新增更新记录数据与渲染器"
```

---
### Task 2: 更新记录页面

**Files:**
- Create: `E:\xunfang-baike\changelog.html`

**Interfaces:**
- Consumes: Task 1 的 js/changelog.js
- Produces: 页面（供 Task 3 导航链接、Task 4 验证）

- [ ] **Step 1: 创建 `changelog.html`**（结构参照 `search.html` + `jingqing/index.html` 页头）
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="巡防百科历次内容更新记录">
<title>更新记录 — 巡防百科</title>
<link rel="stylesheet" href="css/style.css">
<script src="js/auth-config.js"></script>
<script src="js/auth-core.js"></script>
<script src="js/auth-guard.js" data-root=""></script>
</head>
<body>

<div id="nav-placeholder"></div>

<div class="breadcrumb">
  <a href="index.html">首页</a> &gt;
  <span class="current">更新记录</span>
</div>

<div class="page-container list-page">
  <div class="page-title">
    <h1>📝 更新记录</h1>
    <div class="meta">
      <span class="tag">记录网站历次内容更新</span>
    </div>
  </div>

  <div id="changelog-list" class="changelog-list"></div>
</div>

<script src="js/theme.js"></script>
<script src="js/nav.js"></script>
<script src="js/changelog.js"></script>
</body>
</html>
```
- [ ] **Step 2: 校验**
  - 页面含 `.changelog-list` 容器、面包屑、认证脚本、`js/changelog.js` 引用；无 `.article-page` 标记（确保不进入搜索索引）

- [ ] **Step 3: 提交**
```bash
cd /e/xunfang-baike
git add changelog.html
git commit -m "feat: 新增更新记录页面"
```

---
### Task 3: 导航入口（首位醒目徽章）

**Files:**
- Modify: `E:\xunfang-baike\js\nav.js`（MODULES 数组 + renderNav 类逻辑）
- Modify: `E:\xunfang-baike\css\style.css`（徽章样式 + changelog 页样式）

**Interfaces:**
- Consumes: Task 2 的 changelog.html
- Produces: 导航栏首位"📝 更新记录"徽章入口（桌面 + 移动端）

- [ ] **Step 1: `js/nav.js` MODULES 数组首项新增**
```javascript
  var MODULES = [
    { name: '更新记录', path: 'changelog.html', emoji: '📝', featured: true },
    { name: '警情处置', path: 'jingqing/index.html', emoji: '🚨' },
    // ...其余保持原样
  ];
```
- [ ] **Step 2: `js/nav.js` renderNav 类逻辑加 changelog-link**
  将现有的 `var cls = (m.special ? 'monthly-link' : '') + (isActive ? ' active' : '');` 改为：
```javascript
      var cls = (m.featured ? 'changelog-link' : '')
             + (m.special ? 'monthly-link' : '')
             + (isActive ? ' active' : '');
```
  确认 `m.special` 与 `m.featured` 互斥（更新记录只设 featured，本月精选只设 special）。

- [ ] **Step 3: `css/style.css` 新增徽章与页面样式**（追加到 `.nav-links a.monthly-link.active` 块之后）
```css
/* === 导航栏更新记录徽章（首位醒目） === */
.nav-links a.changelog-link {
  color: var(--police-blue-deep) !important;
  background: var(--amber);
  font-weight: 600;
  border: 1px solid var(--amber);
  border-radius: var(--radius);
  padding: 2px 10px;
}
.nav-links a.changelog-link:hover {
  filter: brightness(1.08);
}
.nav-links a.changelog-link.active {
  background: var(--amber);
  color: var(--police-blue-deep) !important;
  border-bottom: none;
  box-shadow: 0 0 0 2px rgba(212,168,67,0.4);
}

/* === 更新记录页 === */
.changelog-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.changelog-entry {
  border: 1px solid var(--text-muted);
  border-radius: var(--radius);
  padding: 16px 18px;
  background: var(--card-bg);
}
.changelog-date { color: var(--amber); font-size: 13px; font-weight: 600; }
.changelog-title { font-size: 17px; font-weight: 600; margin: 4px 0 8px; }
.changelog-items { margin: 0; padding-left: 20px; }
.changelog-items li { margin-bottom: 4px; line-height: 1.6; }
.changelog-empty { padding: 40px 16px; text-align: center; color: var(--text-muted); }
```
  **移动端适配**（追加在同一 @media(max-width:900px) 或独立规则）：确保下拉列表中徽章可点、不被裁切：
```css
@media (max-width: 900px) {
  .nav-links a.changelog-link {
    align-self: flex-start;
    padding: 6px 14px;
    margin-bottom: 2px;
  }
}
```

- [ ] **Step 4: 校验**
  - `node --check js/nav.js`
  - 用浏览器/本地服务确认：`python -m http.server 8000` 打开首页，导航首位出现琥珀"📝 更新记录"徽章；点击进入 changelog.html，导航"更新记录"项 active；窗口缩窄到 <900px，汉堡菜单下拉首项为琥珀徽章且可点

- [ ] **Step 5: 提交**
```bash
cd /e/xunfang-baike
git add js/nav.js css/style.css
git commit -m "feat: 导航栏首位新增醒目的更新记录徽章入口"
```

---
### Task 4: 全量验证与提交

**Files:**
- Modify: 无（验证用）

**Interfaces:**
- Consumes: Task 1-3 全部产物
- Produces: 全绿确认

- [ ] **Step 1: 搜索索引与链接**
```bash
"$PY" tools/build_search_index.py --check   # 预期 OK 93 records（changelog 不入索引）
"$PY" tools/check_site_links.py             # 预期 OK，含新 changelog.html
```
- [ ] **Step 2: 来源台账与测试**
```bash
"$PY" tools/public_source_index.py check    # 预期 PASS 0 pending
"$PY" -m unittest discover -s tests -p "test_*.py"   # 预期 OK skipped=2
node --test tests/auth_core.test.js          # 预期 5 pass
```
- [ ] **Step 3: 修复任何失败项后重跑至全绿**
  - 若测试因新根页文件断言变化（如某测试遍历根目录 HTML），更新对应断言（仅限确实由本次新增引起的）

- [ ] **Step 4: 提交（如验证产生变更）并推送**
```bash
cd /e/xunfang-baike
git add -A
git commit -m "chore: 更新记录板块全量验证"   # 若无变更则跳过
git push origin master
```

---
## Self-Review

- **Spec coverage:** 独立页（Task 2）✓；JSON+JS 渲染（Task 1）✓；导航首位醒目徽章（Task 3）✓；移动端适配（Task 3 媒体查询）✓；只记本次、无版本号（Task 1 数据）✓；首页不加入口、不入搜索索引（Task 2 无 article-page）✓；验证全绿（Task 4）✓
- **Placeholder scan:** 各任务含完整代码与命令；无 TBD/占位
- **Type consistency:** 数据字段 `date/title/items`、渲染函数 `escapeHtml/render/fail`、页面容器 `#changelog-list`、CSS 类 `changelog-link/changelog-entry/changelog-date/changelog-title/changelog-items/changelog-empty`、导航标记 `featured` 在 Task 1-3 间保持一致
