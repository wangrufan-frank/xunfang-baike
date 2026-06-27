# 全域UX重构 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 导航JS动态注入、搜索增强、索引页统一分组、首页信息密度优化

**Architecture:** 创建 `js/nav.js` 集中管理导航配置和渲染；扩展 `js/main.js` 搜索逻辑按页面类型分派；批量替换所有 HTML 的 nav 块为 placeholder + script 引用；改造4个未分组的模块索引页；首页卡片增加文章数和热门链接

**Tech Stack:** 纯静态 HTML/CSS/JS，无框架

**改前覆盖:** 现有已分组模块（快反、反恐、徒手、射击、大型活动、法律法规、群体事件）不再改动结构，仅替换 nav 块。

---

### Task 1: 创建 `js/nav.js` — 导航配置与渲染

**Files:**
- Create: `js/nav.js`

- [ ] **Step 1: 编写模块配置和 renderNav 函数**

```js
// js/nav.js
(function() {
  var MODULES = [
    { name: '首页',     path: 'index.html',          emoji: '🏠' },
    { name: '警情',     path: 'jingqing/index.html',  emoji: '🚨' },
    { name: '装备',     path: 'zhuangbei/index.html', emoji: '🛡️' },
    { name: '巡逻',     path: 'xunluo/index.html',    emoji: '📋' },
    { name: '作战',     path: 'zuozhan-danyuan/index.html', emoji: '👥' },
    { name: '反恐',     path: 'fankong/index.html',   emoji: '🎯' },
    { name: '快反',     path: 'kuaifan/index.html',   emoji: '⚡' },
    { name: '徒手防卫', path: 'tushou/index.html',    emoji: '🤼' },
    { name: '法律法规', path: 'fagui/index.html',     emoji: '📕' },
    { name: '手枪射击', path: 'shoushe/index.html',   emoji: '🔫' },
    { name: '大型活动', path: 'daxing-anbao/index.html', emoji: '🏟️' },
    { name: '群体事件', path: 'qunti-shijian/index.html', emoji: '👥' }
  ];

  function renderNav() {
    var path = window.location.pathname.replace(/\\/g, '/');
    
    // 通过路径是否包含已知模块目录名判断深度
    var moduleDirs = MODULES.map(function(m) {
      return m.path.replace(/\/index\.html$/, '');
    }).filter(function(d) { return d !== 'index.html'; });
    var depth = moduleDirs.some(function(d) { return path.indexOf('/' + d + '/') !== -1; }) ? 1 : 0;

    var linksHtml = MODULES.map(function(m) {
      var href = (depth === 0) ? m.path : ('../' + m.path);
      var moduleDir = m.path.replace(/\/index\.html$/, '');
      var isActive;
      if (moduleDir === 'index.html') {
        // 首页 active：路径不以任何模块目录结尾
        isActive = !moduleDirs.some(function(d) {
          return path.indexOf('/' + d + '/') !== -1 || path.endsWith('/' + d);
        });
      } else {
        isActive = path.indexOf('/' + moduleDir + '/') !== -1 
               || path.endsWith('/' + moduleDir);
      }
      return '<a href="' + href + '"' + (isActive ? ' class="active"' : '') + '>' 
           + m.emoji + ' ' + m.name + '</a>';
    }).join('');

    return '<nav class="topnav">' +
      '<div class="logo">🛡️ 巡防百科</div>' +
      '<button class="hamburger" aria-label="菜单">☰</button>' +
      '<div class="nav-links">' + linksHtml + '</div>' +
      '</nav>';
  }

  // 注入导航
  var placeholder = document.getElementById('nav-placeholder');
  if (placeholder) {
    placeholder.outerHTML = renderNav();
  }
})();
```

- [ ] **Step 2: 确认文件创建**

Run: `ls -la F:/frank第二大脑/xunfang-baike/js/nav.js`

---

### Task 2: 扩展搜索功能 — `js/main.js`

**Files:**
- Modify: `js/main.js`

- [ ] **Step 1: 更新搜索逻辑，增加列表页过滤**

```js
// js/main.js
document.addEventListener('DOMContentLoaded', function() {
  // 汉堡菜单切换（nav由JS注入后仍需绑定）
  document.addEventListener('click', function(e) {
    if (e.target.closest('.hamburger')) {
      var navLinks = document.querySelector('.nav-links');
      if (navLinks) navLinks.classList.toggle('open');
    }
  });

  // 搜索：按页面类型分派
  var searchInput = document.querySelector('.search-bar input');
  if (!searchInput) return;

  searchInput.addEventListener('input', function() {
    var query = this.value.toLowerCase().trim();

    // 首页：过滤模块卡片
    var moduleCards = document.querySelectorAll('.module-card');
    if (moduleCards.length > 0) {
      moduleCards.forEach(function(card) {
        var text = (card.textContent || '').toLowerCase();
        card.style.display = text.includes(query) ? '' : 'none';
      });
      return;
    }

    // 列表页：过滤 list-item 链接
    var listItems = document.querySelectorAll('.list-page .list-item');
    if (listItems.length > 0) {
      // 同时控制 list-section-title 的显隐
      var sections = document.querySelectorAll('.list-section-title');
      listItems.forEach(function(item) {
        var text = (item.textContent || '').toLowerCase();
        item.style.display = text.includes(query) ? '' : 'none';
      });
      // 如果组内所有项都隐藏，隐藏组标题
      sections.forEach(function(section) {
        var next = section.nextElementSibling;
        var allHidden = true;
        var el = section.nextElementSibling;
        while (el && !el.classList.contains('list-section-title')) {
          if (el.classList.contains('list-item') && el.style.display !== 'none') {
            allHidden = false;
          }
          el = el.nextElementSibling;
        }
        section.style.display = allHidden ? 'none' : '';
      });
      return;
    }
  });
});
```

- [ ] **Step 2: 验证搜索文件**

Run: `wc -l F:/frank第二大脑/xunfang-baike/js/main.js`

---

### Task 3: 批量替换所有 HTML 文件中的导航块

**Files:**
- Modify: 所有 `.html` 文件（~60+）

**策略：** 每个文件的 `<nav class="topnav">...</nav>` 替换为 `<div id="nav-placeholder"></div>`，并确保 `<script>` 引用正确。

页面分两类深度：
- **根目录** `index.html`：引用 `js/nav.js`
- **子目录** 所有其他 `.html`：引用 `../js/nav.js`

- [ ] **Step 1: 替换子目录 HTML（所有模块目录下的 .html）**

Run:
```bash
cd "F:/frank第二大脑/xunfang-baike"
# 子目录中所有 .html 文件：替换整个 nav 块为 placeholder + script
for dir in jingqing zhuangbei xunluo zuozhan-danyuan fankong kuaifan tushou shoushe fagui daxing-anbao qunti-shijian; do
  for f in "$dir"/*.html; do
    # 用 perl 做多行替换：删除整个 <nav class="topnav">...</nav>
    perl -i -0777 -pe '
      s{<nav class="topnav">.*?</nav>}
       {<div id="nav-placeholder"></div>}gs
    ' "$f"
    echo "OK: $f"
  done
done
```

- [ ] **Step 2: 替换根目录 `index.html` 的导航**

```bash
cd "F:/frank第二大脑/xunfang-baike"
perl -i -0777 -pe 's{<nav class="topnav">.*?</nav>}{<div id="nav-placeholder"></div>}gs' index.html
```

- [ ] **Step 3: 确认所有 nav 块已替换**

Run:
```bash
cd "F:/frank第二大脑/xunfang-baike"
# 不应该有任何残留的 <nav class="topnav">
grep -rn '<nav class="topnav"' *.html */*.html | wc -l
# 预期: 0
```

- [ ] **Step 4: 确认每个 HTML 都有 script 引用**

Run:
```bash
cd "F:/frank第二大脑/xunfang-baike"
# 确认 index.html 引用 js/nav.js
grep -l 'js/nav.js' index.html
# 确认子目录 HTML 引用 ../js/nav.js 或 js/main.js
grep -l 'js/main.js' */*.html | head -5
```

> 注意：`js/main.js` 已在所有文件中存在。`js/nav.js` 需要在 HTML 中单独引用。

- [ ] **Step 5: 给所有 HTML 加上 nav.js 引用**

根目录 `index.html`：在 `</body>` 前已有 `<script src="js/main.js"></script>`，在其前加一行。

子目录 HTML：已有 `<script src="../js/main.js"></script>`，在其前加一行。

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 根目录
perl -i -pe 's{<script src="js/main.js"></script>}{<script src="js/nav.js"></script>\n<script src="js/main.js"></script>}' index.html

# 子目录
for dir in jingqing zhuangbei xunluo zuozhan-danyuan fankong kuaifan tushou shoushe fagui daxing-anbao qunti-shijian; do
  for f in "$dir"/*.html; do
    perl -i -pe 's{<script src="\.\./js/main.js"></script>}{<script src="../js/nav.js"></script>\n<script src="../js/main.js"></script>}' "$f"
    echo "OK: $f"
  done
done
```

- [ ] **Step 6: 验证根目录和子目录的 nav.js 引用路径正确**

```bash
cd "F:/frank第二大脑/xunfang-baike"
grep 'js/nav.js' index.html
grep 'js/nav.js' jingqing/index.html
```

---

### Task 4: 警情处置索引页分组

**Files:**
- Modify: `jingqing/index.html`

- [ ] **Step 1: 在 list-item 间插入分组标题**

将 6 个 `list-item` 分为 **街面警情** (持刀、醉酒、打架、家暴) 和 **盘查规范** (人员盘查、可疑车辆) 两组。

替换内容区域（`.page-container.list-page` 内的列表部分）：

```html
<div class="page-container list-page">
  <div class="page-title">
    <h1>🚨 警情处置</h1>
    <div class="meta">
      <span class="tag">6篇</span>
      <span class="tag">预计阅读：28分钟</span>
      <span class="tag">常见街面警情</span>
      <span class="tag">分步处置流程</span>
    </div>
  </div>

  <div class="list-section-title">📌 街面警情</div>

  <a href="chidao-leiqing.html" class="list-item">
    <div class="item-title">🔪 持刀类警情处置</div>
    <div class="item-desc">梯次化处置 + 模块化策应，5人作战小组分工</div>
  </a>
  <a href="zuijiu-naoshi.html" class="list-item">
    <div class="item-title">🍺 醉酒闹事警情处置</div>
    <div class="item-desc">醉酒人员约束控制、约束带使用、医疗联动</div>
  </a>
  <a href="dajia-douou.html" class="list-item">
    <div class="item-title">👊 打架斗殴警情处置</div>
    <div class="item-desc">现场分离、伤情评估、当事人询问、证据固定</div>
  </a>
  <a href="jiating-baoli.html" class="list-item">
    <div class="item-title">🏠 家庭暴力警情处置</div>
    <div class="item-desc">人身保护、告诫书出具、受害人救助与社会联动</div>
  </a>

  <div class="list-section-title">🔍 盘查规范</div>

  <a href="renyuan-pancha.html" class="list-item">
    <div class="item-title">🪪 人员盘查</div>
    <div class="item-desc">六步法：表明身份 → 告知依据 → 查验身份 → 口头警告 → 口头传唤 → 强制传唤</div>
  </a>
  <a href="keyi-cheliang.html" class="list-item">
    <div class="item-title">🚗 可疑车辆盘查</div>
    <div class="item-desc">车辆截停安全距离、人员分离、车辆搜查要点</div>
  </a>
</div>
```

- [ ] **Step 2: 验证文件**

Run: `wc -l F:/frank第二大脑/xunfang-baike/jingqing/index.html`

---

### Task 5: 单警装备索引页分组

**Files:**
- Modify: `zhuangbei/index.html`

- [ ] **Step 1: 将 7 个 list-item 分为 核心装备 和 规范用语 两组**

```html
<div class="page-container list-page">
  <div class="page-title">
    <h1>🛡️ 单警装备</h1>
    <div class="meta">
      <span class="tag">7篇</span>
      <span class="tag">预计阅读：32分钟</span>
      <span class="tag">九小件</span>
      <span class="tag">使用规范</span>
      <span class="tag">法律依据</span>
    </div>
  </div>

  <div class="list-section-title">📦 核心装备</div>

  <a href="jiuxiaojian-gailan.html" class="list-item">
    <div class="item-title">📦 九小件概览</div>
    <div class="item-desc">九小件清单、佩戴原则、佩戴顺序、装备分类</div>
  </a>
  <a href="shensuo-jinggun.html" class="list-item">
    <div class="item-title">🪠 伸缩警棍</div>
    <div class="item-desc">基本介绍 · 法律支撑 · 击打部位 · 戒备/开棍/劈击/握棍技术 · 安全注意事项</div>
  </a>
  <a href="cuilei-pensheqi.html" class="list-item">
    <div class="item-title">💨 催泪喷射器</div>
    <div class="item-desc">基本介绍 · 使用要领 · 善后处理 · 性能参数 · 法定禁止情形</div>
  </a>
  <a href="shoukao.html" class="list-item">
    <div class="item-title">🔗 手铐</div>
    <div class="item-desc">六种上铐方法 · 使用注意事项 · 武力链条定位</div>
  </a>
  <a href="zhifa-jiuyi.html" class="list-item">
    <div class="item-title">📹 执法记录仪</div>
    <div class="item-desc">日常检查维护 · 使用规范 · 涉密警情保密纪律</div>
  </a>
  <a href="fangge-shoutao.html" class="list-item">
    <div class="item-title">🧤 防割手套</div>
    <div class="item-desc">防割不防刺 · 使用后检查维护 · 高风险场景应用</div>
  </a>

  <div class="list-section-title">📢 规范用语</div>

  <a href="jingxie-jinggao.html" class="list-item">
    <div class="item-title">📢 警械使用警告用语</div>
    <div class="item-desc">标准警告用语 · 法律依据 · 不同警械的警告变体</div>
  </a>
</div>
```

---

### Task 6: 巡逻规范索引页分组

**Files:**
- Modify: `xunluo/index.html`

- [ ] **Step 1: 将 5 个 list-item 分为 勤务规范 和 专项盘查 两组**

```html
<div class="page-container list-page">
  <div class="page-title">
    <h1>📋 巡逻规范</h1>
    <div class="meta">
      <span class="tag">5篇</span>
      <span class="tag">预计阅读：22分钟</span>
      <span class="tag">盘查流程</span>
      <span class="tag">战术站位</span>
      <span class="tag">法律依据</span>
    </div>
  </div>

  <div class="list-section-title">📌 勤务规范</div>

  <a href="faly-yiju.html" class="list-item">
    <div class="item-title">⚖️ 法律依据与法言法语</div>
    <div class="item-desc">法律依据框架 · 盘查授权条款 · 法言法语体系 · 常见应答话术</div>
  </a>
  <a href="pancha-liucheng.html" class="list-item">
    <div class="item-title">📋 盘查规范流程</div>
    <div class="item-desc">六步法：表明身份→告知依据→查验身份→口头警告→口头传唤→强制传唤</div>
  </a>
  <a href="zhanshu-zhanwei.html" class="list-item">
    <div class="item-title">📍 战术站位与装备</div>
    <div class="item-desc">三角/四角/五人站位 · 装备体系 · 安全距离控制</div>
  </a>

  <div class="list-section-title">🔍 专项盘查</div>

  <a href="shizi-fangyu.html" class="list-item">
    <div class="item-title">🛡️ 十字防御技能</div>
    <div class="item-desc">动作要领 · 实战常见问题 · 安全三要素</div>
  </a>
  <a href="xidu-pancha.html" class="list-item">
    <div class="item-title">💊 吸毒前科人员盘查</div>
    <div class="item-desc">专项盘查流程 · 特征识别 · 证据固定要点</div>
  </a>
</div>
```

---

### Task 7: 最小作战单元索引页分组

**Files:**
- Modify: `zuozhan-danyuan/index.html`

- [ ] **Step 1: 将 9 个 list-item 分为 基础认知、装备技术、战术训练 三组**

```html
<div class="page-container list-page">
  <div class="page-title">
    <h1>👥 最小作战单元</h1>
    <div class="meta">
      <span class="tag">9篇</span>
      <span class="tag">预计阅读：42分钟</span>
      <span class="tag">三防体系</span>
      <span class="tag">战术配合</span>
      <span class="tag">盾叉协同</span>
    </div>
  </div>

  <div class="list-section-title">📐 基础认知</div>

  <a href="gaishu-biancheng.html" class="list-item">
    <div class="item-title">📐 概述与编成</div>
    <div class="item-desc">定义与编成 · 3人制警组 · 职责分工 · 装备配备 · 安全理念</div>
  </a>
  <a href="zhanshu-zhanwei.html" class="list-item">
    <div class="item-title">📍 战术配合与站位</div>
    <div class="item-desc">三大支柱 · 组合式站位 · 夹击式站位 · 站位选择原则</div>
  </a>
  <a href="faly-fayanfayu.html" class="list-item">
    <div class="item-title">⚖️ 法律与法言法语</div>
    <div class="item-desc">五大执法依据 · 六级递进法言法语 · 外围管控 · 武力使用边界</div>
  </a>

  <div class="list-section-title">⚔️ 装备技术</div>

  <a href="dunpai-jishu.html" class="list-item">
    <div class="item-title">🛡️ 盾牌技术</div>
    <div class="item-desc">法式盾牌 · 持盾戒备(高贴收挺) · 持盾撞击 · 六种运用场景 · 体能训练</div>
  </a>
  <a href="jinggun-zhuabucha.html" class="list-item">
    <div class="item-title">🏒 警棍与抓捕叉</div>
    <div class="item-desc">长警棍持棍戒备与戳击 · 抓捕叉提握下滑下压 · 叉锁控制 · 胸叉捕控</div>
  </a>
  <a href="duncha-xietong.html" class="list-item">
    <div class="item-title">🤝 盾叉协同战术</div>
    <div class="item-desc">四大配合原则 · 标准配合流程 · 刀斧砍杀五步处置程序 · 五种战法组合</div>
  </a>

  <div class="list-section-title">📊 战术与训练</div>

  <a href="zhudong-hengyi.html" class="list-item">
    <div class="item-title">⚔️ 主动横移压缩空间战法</div>
    <div class="item-desc">四步操作要领 · 与两种站位的配合 · 常见失败原因</div>
  </a>
  <a href="wuli-shengji-sanfang.html" class="list-item">
    <div class="item-title">📊 武力升级与三防训练</div>
    <div class="item-desc">五级武力升级模型 · 防刀斧砍杀/车辆冲撞/纵火爆炸 · 三防概念与训练要点</div>
  </a>
  <a href="xunlian-jiaoxuefa.html" class="list-item">
    <div class="item-title">🎓 训练教学法</div>
    <div class="item-desc">五步教学法 · 游戏化教学 · 红蓝对抗三级制 · 组训点评要点</div>
  </a>
</div>
```

---

### Task 8: 首页信息密度优化

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 更新首页模块卡片，增加 `count` 和 `hot-links`**

替换 `.card-grid` 内所有 `.module-card`：

```html
<div class="card-grid">
  <a href="jingqing/index.html" class="module-card accent-red">
    <div class="icon">🚨</div>
    <div class="name">警情处置</div>
    <div class="count">6篇</div>
    <div class="desc">常见警情处置流程</div>
    <div class="hot-links">持刀警情 · 醉酒闹事 · 人员盘查</div>
  </a>
  <a href="zhuangbei/index.html" class="module-card accent-blue">
    <div class="icon">🛡️</div>
    <div class="name">单警装备</div>
    <div class="count">7篇</div>
    <div class="desc">九小件使用规范</div>
    <div class="hot-links">伸缩警棍 · 催泪喷射器 · 手铐</div>
  </a>
  <a href="xunluo/index.html" class="module-card accent-green">
    <div class="icon">📋</div>
    <div class="name">巡逻规范</div>
    <div class="count">5篇</div>
    <div class="desc">盘查与勤务标准</div>
    <div class="hot-links">盘查六步法 · 战术站位 · 十字防御</div>
  </a>
  <a href="zuozhan-danyuan/index.html" class="module-card accent-purple">
    <div class="icon">👥</div>
    <div class="name">最小作战单元</div>
    <div class="count">9篇</div>
    <div class="desc">战术配合训练</div>
    <div class="hot-links">盾牌技术 · 盾叉协同 · 武力升级</div>
  </a>
  <a href="kuaifan/index.html" class="module-card accent-orange">
    <div class="icon">⚡</div>
    <div class="name">快反处置</div>
    <div class="count">5篇</div>
    <div class="desc">135快速反应机制</div>
    <div class="hot-links">135机制 · 持刀警情 · 盾棍叉</div>
  </a>
  <a href="fankong/index.html" class="module-card accent-dark">
    <div class="icon">🎯</div>
    <div class="name">反恐防暴</div>
    <div class="count">7篇</div>
    <div class="desc">重点区域安防</div>
    <div class="hot-links">武力升级 · 核心区处置 · 校园反恐</div>
  </a>
  <a href="tushou/index.html" class="module-card accent-teal">
    <div class="icon">🤼</div>
    <div class="name">徒手防卫</div>
    <div class="count">4篇</div>
    <div class="desc">控制与带离技术</div>
    <div class="hot-links">抓握解脱 · 抱臂折腕 · 搜身带离</div>
  </a>
  <a href="fagui/index.html" class="module-card accent-red">
    <div class="icon">📕</div>
    <div class="name">法律法规</div>
    <div class="count">3篇</div>
    <div class="desc">执法依据速查</div>
    <div class="hot-links">赌博执法 · 视频条例 · 治安处罚</div>
  </a>
  <a href="shoushe/index.html" class="module-card accent-dark">
    <div class="icon">🔫</div>
    <div class="name">手枪射击</div>
    <div class="count">5篇</div>
    <div class="desc">基础射击技术</div>
    <div class="hot-links">安全规范 · 据枪动作 · 瞄准击发</div>
  </a>
  <a href="daxing-anbao/index.html" class="module-card accent-teal">
    <div class="icon">🏟️</div>
    <div class="name">大型活动安保</div>
    <div class="count">3篇</div>
    <div class="desc">演唱会/赛事执法</div>
    <div class="hot-links">演唱会 · 校园金融 · 舆情</div>
  </a>
  <a href="qunti-shijian/index.html" class="module-card accent-orange">
    <div class="icon">👥</div>
    <div class="name">群体事件处置</div>
    <div class="count">5篇</div>
    <div class="desc">聚集事件应对</div>
    <div class="hot-links">处置预案 · 控制带离 · 舆情导控</div>
  </a>
</div>
```

- [ ] **Step 2: 增加 CSS 样式**

在 `css/style.css` 中，`.module-card .desc` 之后追加：

```css
.module-card .count {
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 2px;
}

.module-card .hot-links {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 6px;
  line-height: 1.5;
}
```

---

### Task 9: 验证 — 在浏览器中检查

- [ ] **Step 1: 确认所有 HTML 文件没有残留的 `<nav class="topnav">`**

```bash
cd "F:/frank第二大脑/xunfang-baike"
grep -rn '<nav class="topnav"' *.html */*.html
# 预期输出: 无结果（空）
```

- [ ] **Step 2: 确认所有页面都引用了 nav.js**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 根目录
grep 'nav.js' index.html
# 子目录（抽检几个）
grep 'nav.js' jingqing/index.html jingqing/chidao-leiqing.html zhuangbei/index.html zuozhan-danyuan/index.html
# 每个都应显示一行引用
```

- [ ] **Step 3: 统计 nav.js 引用数量，确认覆盖全部页面**

```bash
cd "F:/frank第二大脑/xunfang-baike"
grep -rl 'nav.js' *.html */*.html | wc -l
# 应等于总 HTML 文件数
```

- [ ] **Step 4: 打开浏览器验证**

打开 `F:/frank第二大脑/xunfang-baike/index.html`，检查：
- 导航栏是否正常渲染（11个模块 + 首页）
- 首页搜索过滤是否正常
- 进入各模块列表页，搜索是否过滤 `list-item`
- 分组标题是否在 警情/装备/巡逻/作战 4 个模块中显示
- 首页卡片是否显示文章数和热门链接
- 移动端汉堡菜单是否正常
