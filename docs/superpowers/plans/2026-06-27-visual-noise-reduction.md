# 视觉降噪与图文重构 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 降低页面文字密度、增加图文比——CSS全局排版优化 + 4个高频详情页加装速览卡片和媒体优先结构

**Architecture:** CSS层叠增强（style.css追加规则）、JS交互增强（main.js追加折叠逻辑）、HTML结构调整（4个详情页按新模板改造）。不改导航、搜索、首页、索引页。

**Tech Stack:** 纯静态 HTML/CSS/JS，零框架依赖

---

### Task 1: CSS 排版优化 — 提升文字呼吸感

**Files:**
- Modify: `css/style.css` — 调整现有规则 + 追加新规则

- [ ] **Step 1: 调整正文排版密度**

在 `css/style.css` 中修改以下现有规则：

```css
/* 原文: .step-text { font-size: 14px; line-height: 1.7; margin-bottom: 10px; } */
.step-text {
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.9;
  margin-bottom: 10px;
}

/* 原文: .step-card { padding: 14px 16px; margin-bottom: 12px; } */
.step-card {
  background: var(--card-bg);
  border-left: 3px solid var(--accent-red);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 16px;
  box-shadow: var(--shadow);
}

/* 新增: 段落间距，替代 <br><br> */
.step-text p {
  margin-bottom: 10px;
}
```

- [ ] **Step 2: 增加 content-item 和 list-item 内边距**

```css
/* 原文: .content-item { padding: 14px 16px; } */
.content-item {
  background: var(--card-bg);
  border-left: 3px solid var(--accent-blue);
  border-radius: var(--radius);
  padding: 18px 20px;
  box-shadow: var(--shadow);
  margin-bottom: 16px;
}

/* 原文: .list-page .list-item { padding: 12px 16px; margin-bottom: 8px; } */
.list-page .list-item {
  display: block;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 18px;
  margin-bottom: 10px;
  box-shadow: var(--shadow);
}
```

- [ ] **Step 3: 增加步骤标题字号**

```css
/* 原文: .step-card .step-title { font-size: 15px; } */
.step-card .step-title {
  font-weight: bold;
  font-size: 16px;
}
```

---

### Task 2: CSS 新组件 — 速览卡片、核心结论、折叠区域

**Files:**
- Modify: `css/style.css` — 追加新规则

- [ ] **Step 1: 追加速览卡片样式**

在 `css/style.css` 末尾追加：

```css
/* === 速览卡片 === */
.quick-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-left: 4px solid var(--nav-bg);
  border-radius: var(--radius);
  padding: 16px 20px;
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  box-shadow: var(--shadow);
}

.quick-card .quick-icon {
  font-size: 36px;
  flex-shrink: 0;
  line-height: 1;
}

.quick-card .quick-body h2 {
  font-size: 18px;
  margin-bottom: 6px;
  color: var(--text);
}

.quick-card .quick-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 4px;
}

.quick-card .quick-flow {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* === 核心结论 === */
.step-lead {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 12px;
  line-height: 1.6;
}

/* === 步骤媒体（真实图片/视频） === */
.step-media {
  margin: 10px 0;
  text-align: center;
}

.step-media img,
.step-media video {
  max-width: 100%;
  border-radius: 4px;
  border: 1px solid var(--border);
}

.step-media .caption {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
}

/* === 折叠组件 === */
.expandable-preview {
  /* 正常显示 */
}

.expandable-full {
  display: none;
  margin-top: 6px;
}

.expandable-full.open {
  display: block;
}

.expand-btn {
  display: inline-block;
  background: none;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 4px 12px;
  font-size: 13px;
  color: var(--accent-blue);
  cursor: pointer;
  margin-top: 6px;
}

.expand-btn:hover {
  background: var(--bg);
}
```

---

### Task 3: JS 折叠交互

**Files:**
- Modify: `js/main.js` — 追加展开/收起逻辑

- [ ] **Step 1: 在 main.js 末尾追加折叠交互**

在 `js/main.js` 的 DOMContentLoaded 回调内部末尾追加：

```js
  // 折叠展开交互
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('.expand-btn');
    if (!btn) return;

    var expandable = btn.previousElementSibling;
    if (!expandable || !expandable.classList.contains('expandable')) {
      // 按钮可能在 step-detail 之后
      expandable = btn.parentElement.querySelector('.expandable');
    }
    if (!expandable) return;

    var full = expandable.querySelector('.expandable-full');
    if (!full) return;

    var isOpen = full.classList.contains('open');
    if (isOpen) {
      full.classList.remove('open');
      btn.textContent = btn.getAttribute('data-expand-text') || btn.textContent.replace('收起', '展开全部');
    } else {
      full.classList.add('open');
      if (!btn.getAttribute('data-expand-text')) {
        btn.setAttribute('data-expand-text', btn.textContent);
      }
      btn.textContent = '收起';
    }
  });
```

---

### Task 4: 持刀类警情处置 — 加速览卡片 + 媒体优先结构

**Files:**
- Modify: `jingqing/chidao-leiqing.html`

- [ ] **Step 1: 在页面标题区之后、第一个步骤卡片之前插入速览卡片**

定位 `.page-title` 结束后，`.step-card.step-red` 之前，插入：

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

- [ ] **Step 2: 改造步骤卡片 — 每步提取核心结论到 step-lead，详情折叠**

持刀类警情有5个步骤卡片，逐个改造。改造模式（以步骤1为例）：

**改造前（步骤1片段）：**
```html
<div class="step-card step-red">
  <div class="step-header"><div class="step-num">1</div><div class="step-title">第一阶段：疏散稳控（2+2+1 队形）</div></div>
  <div class="step-text">
    <strong>目标：</strong>了解现场情况、疏散围观群众、明确核心对象。<br><br>
    <strong>分工：</strong><br>
    · 1号位（指挥）+ 3号位（盾牌手）：伤员安抚与报警人询问<br>
    · 2号位（盾牌手）+ 4号位（长棍）：持械人员盘查与情绪疏导<br>
    · 5号位（支援手）：外围封控与舆情引导<br><br>
    <strong>战术要点：</strong>分割策应、避免激化。保持安全距离≥5米，语言安抚为主，避免直接冲突升级。
  </div>
  <div class="step-media media-placeholder img">📷 2+2+1 疏散稳控队形站位图</div>
  <div class="step-media media-placeholder video">🎬 疏散稳控示范视频（30秒）</div>
</div>
```

**改造后：**
```html
<div class="step-card step-red">
  <div class="step-header"><div class="step-num">1</div><div class="step-title">第一阶段：疏散稳控（2+2+1 队形）</div></div>
  <div class="step-lead">
    分割策应、避免激化。保持安全距离≥5米，语言安抚为主。
  </div>
  <div class="step-media media-placeholder img">📷 2+2+1 疏散稳控队形站位图</div>
  <div class="step-media media-placeholder video">🎬 疏散稳控示范视频（30秒）</div>
  <div class="expandable">
    <div class="expandable-full">
      <div class="step-text">
        <strong>目标：</strong>了解现场情况、疏散围观群众、明确核心对象。<br><br>
        <strong>分工：</strong><br>
        · 1号位（指挥）+ 3号位（盾牌手）：伤员安抚与报警人询问<br>
        · 2号位（盾牌手）+ 4号位（长棍）：持械人员盘查与情绪疏导<br>
        · 5号位（支援手）：外围封控与舆情引导<br><br>
        <strong>战术要点：</strong>分割策应、避免激化。保持安全距离≥5米，语言安抚为主，避免直接冲突升级。
      </div>
    </div>
  </div>
  <button class="expand-btn">▸ 展开战术细节</button>
</div>
```

步骤2-5 按同样模式改造。

- [ ] **Step 3: 处置概述卡片也简化**

步骤0（处置概述）没有step-num（显示"!"），保留概述性 step-lead，详情折叠。

---

### Task 5: 伸缩警棍 — 加速览卡片 + 法律条文折叠 + 媒体C位

**Files:**
- Modify: `zhuangbei/shensuo-jinggun.html`

- [ ] **Step 1: 插入速览卡片**

```html
<div class="quick-card">
  <div class="quick-icon">🪠</div>
  <div class="quick-body">
    <h2>伸缩警棍</h2>
    <div class="quick-tags">
      <span class="tag risk-high">⚠️ 驱逐性警械</span>
      <span class="tag">伸长约52cm</span>
      <span class="tag">收缩约22cm</span>
    </div>
    <div class="quick-flow">📋 7步：介绍 → 法律 → 击打部位 → 戒备 → 开棍 → 劈击 → 握棍</div>
  </div>
</div>
```

- [ ] **Step 2: 法律支撑（步骤2）— 8条法律折叠**

```html
<div class="step-card step-orange">
  <div class="step-header"><div class="step-num">2</div><div class="step-title">法律支撑</div></div>
  <div class="step-lead">
    依据《人民警察使用警械和武器条例》第七条，经警告无效后可使用。以制止为限度。
  </div>
  <div class="expandable">
    <div class="expandable-preview">
      <ol>
        <li>结伙斗殴、殴打他人、寻衅滋事、侮辱妇女等流氓活动</li>
        <li>聚众扰乱车站、码头、运动场等公共场所秩序</li>
        <li>非法举行集会、游行、示威</li>
      </ol>
    </div>
    <div class="expandable-full">
      <ol start="4">
        <li>强行冲越警戒线</li>
        <li>以暴力方法抗拒或阻碍执法</li>
        <li>袭击人民警察</li>
        <li>危害公共安全、社会秩序和公民人身安全需当场制止</li>
        <li>法律、行政法规规定的其他情形</li>
      </ol>
      <p><strong>使用限度：</strong>以制止违法犯罪行为为限度，行为得到制止时应立即停止使用。</p>
    </div>
  </div>
  <button class="expand-btn">▸ 展开全部（共8条）</button>
</div>
```

- [ ] **Step 3: 击打部位（步骤3）— 图片C位 + 细节折叠**

```html
<div class="step-card step-red">
  <div class="step-header"><div class="step-num">3</div><div class="step-title">击打部位</div></div>
  <div class="step-lead">
    只打击大肌肉群和运动神经点，定点定位。严禁击打头部、脖子、胫骨、裆部。
  </div>
  <div class="step-media media-placeholder img">📷 人体击打部位示意图（合法区/禁区）</div>
  <div class="expandable">
    <div class="expandable-full">
      <div class="step-text">
        <strong>合法击打部位（大肌肉群）：</strong><br>
        · 大腿外侧/内侧中心区（腓骨神经）<br>
        · 小臂内侧/外侧、大臂内侧/外侧（桡侧神经、桡正中神经）<br>
        · 小腿后部<br><br>
        <strong>严禁击打部位：</strong><br>
        · 头部 —— 可能致命<br>
        · 脖子、太阳穴 —— 要害部位<br>
        · 小腿胫骨 —— 骨骼突出，表皮薄，易严重骨折<br>
        · 裆部及其他骨骼脆弱处
      </div>
    </div>
  </div>
  <button class="expand-btn">▸ 展开具体部位清单</button>
</div>
```

- [ ] **Step 4: 戒备姿势（步骤4）— 图片C位 + 细节折叠**

```html
<div class="step-card step-blue">
  <div class="step-header"><div class="step-num">4</div><div class="step-title">戒备姿势</div></div>
  <div class="step-lead">
    三种姿态逐级升级：隐藏戒备（腹前）→ 提棍戒备（腿后）→ 肩上戒备（攻击准备）。
  </div>
  <div class="step-media media-placeholder img">📷 三种戒备姿势对比图</div>
  <div class="expandable">
    <div class="expandable-full">
      <div class="step-text">
        <strong>隐藏戒备：</strong>双手抓握警棍置于腹前，双眼目视前方。警棍隐蔽不暴露，适合初期接触阶段。<br><br>
        <strong>提棍戒备：</strong>单手持棍藏于大腿后侧。半隐蔽状态，已做好出棍准备。<br><br>
        <strong>肩上戒备（教学重点）：</strong>右脚后撤半步，重心置于两腿之间，右手握棍尾端、棍尾朝前，手肘夹紧肋部。半侧身站位利于发力且降低暴露面积。
      </div>
    </div>
  </div>
  <button class="expand-btn">▸ 展开详细要领</button>
</div>
```

- [ ] **Step 5: 其余步骤（1/5/6/7/!安全）按同模式改造**

基本介绍（步骤1）、开棍技术（步骤5）、劈击技术（步骤6）、握棍方式（步骤7）、安全注意事项（!）——各自提取 step-lead + 媒体C位 + 详情折叠。

---

### Task 6: 人员盘查 — 加速览卡片 + 六步法流程图

**Files:**
- Modify: `jingqing/renyuan-pancha.html`

- [ ] **Step 1: 先读当前文件内容**

Run: `wc -l F:/frank第二大脑/xunfang-baike/jingqing/renyuan-pancha.html`

- [ ] **Step 2: 插入速览卡片**

```html
<div class="quick-card">
  <div class="quick-icon">🪪</div>
  <div class="quick-body">
    <h2>人员盘查</h2>
    <div class="quick-tags">
      <span class="tag">六步法</span>
      <span class="tag">语言控制优先</span>
    </div>
    <div class="quick-flow">📋 6步：表明身份 → 告知依据 → 查验身份 → 口头警告 → 口头传唤 → 强制传唤</div>
  </div>
</div>
```

- [ ] **Step 3: 六步法每步提取 step-lead + 媒体C位**

改造模式同前——每个 step-card 保留 step-header，新增 step-lead（1句核心），媒体位提前，详细说明折叠到 expandable。

---

### Task 7: 盾牌技术 — 加速览卡片 + 持盾姿势图C位

**Files:**
- Modify: `zuozhan-danyuan/dunpai-jishu.html`

- [ ] **Step 1: 先读当前文件内容**

Run: `wc -l F:/frank第二大脑/xunfang-baike/zuozhan-danyuan/dunpai-jishu.html`

- [ ] **Step 2: 插入速览卡片**

```html
<div class="quick-card">
  <div class="quick-icon">🛡️</div>
  <div class="quick-body">
    <h2>盾牌技术</h2>
    <div class="quick-tags">
      <span class="tag">法式盾牌</span>
      <span class="tag">持盾戒备（高贴收挺）</span>
      <span class="tag">六种运用场景</span>
    </div>
    <div class="quick-flow">📋 核心：持盾戒备姿势 → 持盾撞击 → 场景运用</div>
  </div>
</div>
```

- [ ] **Step 3: 各步骤按同模式改造**

持盾戒备姿势图放 C 位，其余详情折叠。

---

### Task 8: 验证 + 提交

**Files:**
- Modify: None (verification only)

- [ ] **Step 1: 浏览器打开首页验证**

打开 `F:/frank第二大脑/xunfang-baike/index.html`，检查：
- 首页卡片显示正常
- 点击进入 持刀类警情 → 速览卡片显示正确 → 步骤卡片有 step-lead → 折叠按钮可用
- 点击进入 伸缩警棍 → 法律条文默认只显示前3条 → 点击"展开全部"显示8条
- 人员盘查、盾牌技术同样验证
- 移动端汉堡菜单正常

- [ ] **Step 2: 提交并推送**

```bash
cd "F:/frank第二大脑/xunfang-baike"
git add css/style.css js/main.js jingqing/chidao-leiqing.html zhuangbei/shensuo-jinggun.html jingqing/renyuan-pancha.html zuozhan-danyuan/dunpai-jishu.html docs/superpowers/specs/2026-06-27-visual-noise-reduction-design.md docs/superpowers/plans/2026-06-27-visual-noise-reduction.md
git commit -m "feat: 视觉降噪 — 排版优化 + 4页面图文重构"
git push origin master
```

Expected: GitHub Pages 自动部署，1-2分钟后线上生效。

- [ ] **Step 3: 清除浏览器缓存验证线上**

打开 `https://wangrufan-frank.github.io/xunfang-baike/`，Ctrl+F5 强制刷新验证。
