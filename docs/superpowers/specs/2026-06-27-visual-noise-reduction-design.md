# 视觉降噪与图文重构设计

**日期:** 2026-06-27
**状态:** 已批准
**范围:** 全局CSS排版优化 + 详情页图文结构重构

---

## 一、排版优化（CSS 全局）

**问题：** 正文行高1.7、字号14px、卡片紧凑，导致文字密度过高，阅读疲劳。

**方案：** 纯CSS调整，不改HTML内容，全局生效。

| 属性 | 原值 | 新值 |
|------|------|------|
| `.step-text` 行高 | 1.7 | 1.9 |
| `.step-text` 字号 | 14px | 15px |
| `.step-card` 内边距 | 14px 16px | 18px 20px |
| `.step-card` 下边距 | 12px | 16px |
| 段落间距 | `<br><br>` 无样式控制 | `.step-text p` margin-bottom: 10px |

**新增：折叠组件样式**
- `.expandable` — 超过3条的列表容器
- `.expandable-preview` — 显示前3条
- `.expandable-full` — 默认隐藏，展开后显示全部
- `.expand-btn` — "展开全部 / 收起" 按钮

**影响文件：** `css/style.css`

---

## 二、图文重构（HTML 逐页改造）

### 2.1 速览卡片

每个详情页顶部加一个 `.quick-card`，步骤卡片之前：

```html
<div class="quick-card">
  <div class="quick-icon">🔪</div>
  <div class="quick-body">
    <h2>持刀类警情处置</h2>
    <div class="quick-tags">
      <span class="tag risk-high">⚠️ 高风险</span>
      <span class="tag">5人小组</span>
      <span class="tag">安全距离≥5米</span>
    </div>
    <div class="quick-flow">📋 4步：疏散稳控 → 作战控制 → 封控取证 → 移交恢复</div>
  </div>
</div>
```

**CSS：** 横向布局，emoji左对齐，左侧有淡色竖线，与步骤卡片区有明确分隔。

### 2.2 步骤卡片媒体优先

**现有结构：** 文字 → 媒体占位符（末位）

**新结构：** 核心结论(1-2句) → 图片/视频C位 → 详细信息折叠

```html
<div class="step-card step-red">
  <div class="step-header">
    <div class="step-num">2</div>
    <div class="step-title">第二阶段：作战控制</div>
  </div>
  <div class="step-lead">
    盾棍叉协同推进，将嫌疑人逼至安全角落后制伏。
  </div>
  <div class="step-media">
    <img src="../img/chidao-kongzhi.jpg" alt="作战控制队形">
  </div>
  <div class="step-detail expandable">
    <!-- 详细分工、战术要点等折叠内容 -->
  </div>
  <button class="expand-btn">▸ 展开战术细节</button>
</div>
```

**CSS新增：**
- `.step-lead` — 核心结论，字体稍大粗体，一步的核心信息一句话讲清
- `.step-detail` — 默认隐藏，折叠详细说明
- `.step-media img` / `.step-media video` — 图片视频居中、最大宽度100%、圆角

### 2.3 长列表折叠

法律条文、击打部位等 3 条以上的列表，默认只显示前 3 条：

```html
<div class="expandable">
  <div class="expandable-preview">
    <li>结伙斗殴、殴打他人...</li>
    <li>聚众扰乱车站...</li>
    <li>非法举行集会...</li>
  </div>
  <div class="expandable-full">
    <li>强行冲越警戒线</li>
    <li>以暴力方法抗拒或阻碍执法</li>
    <!-- ... -->
  </div>
</div>
<button class="expand-btn">▸ 展开全部（共8条）</button>
```

---

## 三、改造范围

### 首批改造（4个高频页面）

| 页面 | 文件 | 改造要点 |
|------|------|----------|
| 持刀类警情 | jingqing/chidao-leiqing.html | 加速览卡片、4步骤图片C位、战术要点折叠 |
| 伸缩警棍 | zhuangbei/shensuo-jinggun.html | 加速览卡片、击打部位图C位、8条法律折叠、戒备姿势图 |
| 人员盘查 | jingqing/renyuan-pancha.html | 加速览卡片、六步法流程图 |
| 盾牌技术 | zuozhan-danyuan/dunpai-jishu.html | 加速览卡片、持盾姿势图C位 |

### 后续改造（68个页面）

首批验证通过后，按同模式批量改造其余页面。

---

## 四、媒体素材

媒体占位符已存在（`.step-media.media-placeholder`），改为真实素材只需：

1. 图片放 `img/` 目录，视频放 `video/` 目录
2. 在 HTML 中把占位 div 替换为真实 `<img>` 或 `<video>` 标签

用户后续按页面提供素材，逐个替换。

---

## 五、不改的范围

- 导航系统（`js/nav.js`）
- 搜索功能（`js/main.js`）
- 首页（`index.html`）
- 模块索引页（列表页）
- 面包屑、页面导航（prev/next）
- 响应式断点
- 色板和CSS变量

---

## 六、实施顺序

1. **CSS 排版优化** — 修改 `css/style.css`，全局生效
2. **折叠交互 JS** — 在 `js/main.js` 加展开/收起逻辑
3. **首批 4 页面改造** — 加速览卡片 + 媒体优先结构 + 长列表折叠
4. **浏览器验证** — 打开首页 → 进入改造页面 → 检查效果
5. **提交推送** — `git commit` + `git push`
