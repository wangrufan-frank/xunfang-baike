# 巡防百科微信小程序 MVP · 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将巡防百科的装备介绍（7篇）和警情处置（8篇）迁移到微信小程序，含密码保护、底部tabBar、数据驱动详情页、首页+每日一学。

**Architecture:** 微信原生小程序。详情页数据驱动——所有装备文章共享一个 WXML 模板，从 JS 数据文件读取内容。组件化复用 step-card / quick-card / list-item。密码用 storage 守卫。

**Tech Stack:** WXML / WXSS / JS，SubtleCrypto (SHA-256)，wx.setStorageSync

## Global Constraints

- 密码：wrf150225 → SHA-256：`c252bf49e6766b2ea0f46d6ec62f6588a12ee942d363f17cfe4785d0cc75d5fb`
- 项目根目录：`F:/frank第二大脑/xunfang-baike/miniprogram/`
- 微信开发者工具打开此目录，AppID 用测试号
- tabBar 5个标签：装备、勤务（占位）、训练（占位）、警情、更多
- 所有页面需在 app.json 的 pages 中注册
- 每个页面 4 个文件：.wxml / .wxss / .js / .json
- 每个组件 4 个文件：.wxml / .wxss / .js / .json
- 不改动现有网站文件

---

### Task 1: 项目初始化 — app.json + app.js + app.wxss

**Files:**
- Create: `miniprogram/app.json`
- Create: `miniprogram/app.js`
- Create: `miniprogram/app.wxss`
- Create: `miniprogram/sitemap.json`

- [ ] **Step 1: 创建 app.json**

```json
{
  "pages": [
    "pages/auth/auth",
    "pages/index/index",
    "pages/zhuangbei/index/index",
    "pages/zhuangbei/detail/detail",
    "pages/jingqing/index/index",
    "pages/jingqing/detail/detail",
    "pages/qinwu/index/index",
    "pages/xunlian/index/index",
    "pages/more/more"
  ],
  "window": {
    "navigationBarTitleText": "巡防百科",
    "navigationBarBackgroundColor": "#2c3e50",
    "navigationBarTextStyle": "white",
    "backgroundColor": "#f5f0e8"
  },
  "tabBar": {
    "color": "#8d6e63",
    "selectedColor": "#c0392b",
    "backgroundColor": "#ffffff",
    "borderStyle": "black",
    "list": [
      { "pagePath": "pages/zhuangbei/index/index", "text": "装备" },
      { "pagePath": "pages/qinwu/index/index", "text": "勤务" },
      { "pagePath": "pages/xunlian/index/index", "text": "训练" },
      { "pagePath": "pages/jingqing/index/index", "text": "警情" },
      { "pagePath": "pages/more/more", "text": "更多" }
    ]
  },
  "style": "v2",
  "sitemapLocation": "sitemap.json"
}
```

- [ ] **Step 2: 创建 app.js**

```javascript
App({
  onLaunch() {
    var VALID = 'c252bf49e6766b2ea0f46d6ec62f6588a12ee942d363f17cfe4785d0cc75d5fb';
    var COOKIE_KEY = 'xunfang_auth';
    var val = wx.getStorageSync(COOKIE_KEY);
    var isAuthPage = getCurrentPages().length > 0
      && getCurrentPages()[0].route === 'pages/auth/auth';

    if (!isAuthPage && val !== VALID) {
      wx.reLaunch({ url: '/pages/auth/auth' });
    }
  }
});
```

- [ ] **Step 3: 创建 app.wxss**

```css
page { --bg:#f5f0e8; --card-bg:#fff; --text:#3e2723; --text-secondary:#5d4037;
  --text-muted:#8d6e63; --nav-bg:#2c3e50; --accent-red:#c0392b; --accent-orange:#e67e22;
  --accent-blue:#2980b9; --accent-green:#27ae60; --accent-purple:#8e44ad;
  --border:#d6cec4; --shadow:0 1px 3px rgba(0,0,0,0.08); --radius:4px;
  background:var(--bg); color:var(--text); font-family:-apple-system,"Microsoft YaHei",sans-serif;
  font-size:15px; line-height:1.6; min-height:100vh; }

.page-container { padding: 0 16px 40px; }

.page-title { margin-bottom:16px; padding-bottom:8px; border-bottom:2px solid var(--border); }
.page-title .h1 { font-size:22px; font-weight:bold; color:var(--text); display:block; }
.page-title .meta { display:flex; gap:8px; font-size:12px; color:var(--text-muted); margin-top:4px; flex-wrap:wrap; }
.tag { background:var(--bg); padding:2px 8px; border-radius:3px; font-size:11px; }
.tag.risk-high { color:var(--accent-red); font-weight:bold; }

.breadcrumb { max-width:1200px; margin:0 auto; padding:12px 16px 0; font-size:13px; color:var(--text-muted); }
.breadcrumb text { color:var(--text-muted); }
.breadcrumb .link { color:var(--accent-blue); }
.breadcrumb .current { color:var(--accent-red); font-weight:bold; }

.step-card { background:var(--card-bg); border-radius:var(--radius); padding:18px 20px;
  margin-bottom:16px; box-shadow:var(--shadow); border-left:3px solid var(--accent-red); }
.step-card.red  { border-left-color:var(--accent-red); }
.step-card.orange { border-left-color:var(--accent-orange); }
.step-card.blue  { border-left-color:var(--accent-blue); }
.step-card.green { border-left-color:var(--accent-green); }
.step-card.purple { border-left-color:var(--accent-purple); }
.step-header { display:flex; align-items:center; gap:10px; margin-bottom:10px; }
.step-num { width:26px; height:26px; border-radius:50%; color:#fff; text-align:center;
  line-height:26px; font-size:13px; font-weight:bold; flex-shrink:0; background:var(--accent-red); }
.step-card.blue .step-num { background:var(--accent-blue); }
.step-card.orange .step-num { background:var(--accent-orange); }
.step-card.green .step-num { background:var(--accent-green); }
.step-card.purple .step-num { background:var(--accent-purple); }
.step-title { font-weight:bold; font-size:16px; }
.step-lead { font-size:15px; font-weight:600; margin-bottom:10px; line-height:1.6; }
.step-text { font-size:15px; color:var(--text-secondary); line-height:1.9; }
.step-text .p { margin-bottom:10px; }
.step-media { background:var(--bg); padding:10px 14px; border-radius:var(--radius);
  margin-bottom:6px; font-size:13px; color:var(--text-muted); text-align:center; }

.expand-btn { display:inline-block; background:none; border:1px solid var(--border);
  border-radius:var(--radius); padding:4px 12px; font-size:13px; color:var(--accent-blue);
  margin-top:6px; line-height:1.6; }
.expandable-full { display:none; margin-top:6px; }
.expandable-full.open { display:block; }

.quick-card { background:var(--card-bg); border:1px solid var(--border);
  border-left:4px solid var(--nav-bg); border-radius:var(--radius); padding:16px 20px;
  margin-bottom:20px; display:flex; align-items:flex-start; gap:14px; box-shadow:var(--shadow); }
.quick-icon { font-size:36px; flex-shrink:0; line-height:1; }
.quick-body .h2 { font-size:18px; font-weight:bold; margin-bottom:6px; }
.quick-tags { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:4px; }
.quick-flow { font-size:13px; color:var(--text-secondary); margin-top:4px; }

.list-item { display:block; background:var(--card-bg); border:1px solid var(--border);
  border-radius:var(--radius); padding:14px 18px; margin-bottom:10px; box-shadow:var(--shadow); }
.list-item .item-title { font-weight:bold; font-size:15px; color:var(--text); }
.list-item .item-desc { font-size:12px; color:var(--text-muted); margin-top:2px; }
.list-section-title { font-size:14px; font-weight:bold; color:var(--text-secondary);
  margin:20px 0 8px; padding-bottom:4px; border-bottom:1px solid var(--border); }

.card-grid { display:flex; flex-wrap:wrap; gap:16px; padding:0 16px; }
.module-card { flex:1 1 calc(33% - 16px); min-width:160px; background:var(--card-bg);
  border:1px solid var(--border); border-radius:6px; padding:28px 20px 22px; text-align:center;
  box-shadow:var(--shadow); }
.module-card .icon { font-size:42px; margin-bottom:10px; }
.module-card .name { font-weight:bold; font-size:16px; margin-bottom:4px; }
.module-card .desc { font-size:13px; color:var(--text-secondary); margin-bottom:4px; }
.module-card .count { font-size:12px; color:var(--text-muted); background:var(--bg);
  padding:2px 10px; border-radius:10px; display:inline-block; margin-bottom:6px; }
.module-card .hot-links { font-size:11px; color:var(--text-muted); margin-top:8px; line-height:1.7; }
.module-card.red  { border-top:3px solid var(--accent-red); }
.module-card.blue { border-top:3px solid var(--accent-blue); }
.module-card.green { border-top:3px solid var(--accent-green); }
.module-card.purple { border-top:3px solid var(--accent-purple); }
.module-card.teal { border-top:3px solid #16a085; }

.daily-section { padding:0 16px 40px; }
.daily-card { background:var(--card-bg); border:1px solid var(--border);
  border-left:4px solid var(--accent-red); border-radius:var(--radius); padding:24px 28px;
  box-shadow:var(--shadow); }
.daily-header { display:flex; justify-content:space-between; align-items:center;
  margin-bottom:16px; padding-bottom:10px; border-bottom:1px solid var(--border); }
.daily-label { font-weight:bold; font-size:16px; color:var(--accent-red); }
.daily-date { font-size:13px; color:var(--text-muted); }
.daily-case-title { font-size:18px; font-weight:bold; margin-bottom:14px; }
.daily-case-body { font-size:14px; line-height:1.9; color:var(--text-secondary); margin-bottom:16px; }
.daily-tips { background:var(--bg); border-radius:var(--radius); padding:14px 18px; margin-bottom:16px; }
.tips-title { font-size:14px; font-weight:bold; margin-bottom:8px; }
.daily-tips .tip { font-size:13px; color:var(--text-secondary); line-height:1.8; padding-left:12px; }
.daily-nav { display:flex; justify-content:space-between; align-items:center; font-size:13px; }
.daily-nav button { background:none; border:1px solid var(--border); border-radius:var(--radius);
  padding:4px 14px; font-size:13px; color:var(--accent-blue); }

.page-nav { display:flex; justify-content:space-between; margin-top:20px;
  padding-top:12px; border-top:1px solid var(--border); font-size:14px; }
.page-nav .link { color:var(--accent-blue); }

.search-bar { max-width:1200px; margin:20px auto; padding:0 16px; }
.search-bar input { width:100%; padding:10px 14px; border:1px solid var(--border);
  border-radius:var(--radius); font-size:15px; background:var(--card-bg); color:var(--text); }

.placeholder-page { display:flex; flex-direction:column; align-items:center;
  justify-content:center; height:60vh; color:var(--text-muted); }
.placeholder-page .icon { font-size:64px; margin-bottom:16px; }
.placeholder-page .text { font-size:16px; }
```

- [ ] **Step 4: 创建 sitemap.json**

```json
{
  "rules": [{ "action": "allow", "page": "*" }]
}
```

- [ ] **Step 5: 提交**

```bash
git add miniprogram/ && git commit -m "feat: 小程序项目初始化 — app.json/js/wxss"
```

---

### Task 2: 创建密码登录页

**Files:**
- Create: `miniprogram/pages/auth/auth.wxml`
- Create: `miniprogram/pages/auth/auth.wxss`
- Create: `miniprogram/pages/auth/auth.js`
- Create: `miniprogram/pages/auth/auth.json`

- [ ] **Step 1: auth.wxml**

```xml
<view class="page">
  <view class="card">
    <view class="icon">🔒</view>
    <view class="title">巡防百科</view>
    <view class="subtitle">请输入访问密码</view>
    <input class="pwd-input" type="password" placeholder="●●●●●●" maxlength="20" focus bindinput="onInput" value="{{pwd}}"/>
    <button class="btn" bindtap="onSubmit">确认</button>
    <view class="error">{{error}}</view>
  </view>
</view>
```

- [ ] **Step 2: auth.wxss**

```css
.page { display:flex; align-items:center; justify-content:center; min-height:100vh;
  background:#1a1a2e; }
.card { background:#fff; border-radius:12px; padding:48px 40px; max-width:400px; width:90%;
  text-align:center; box-shadow:0 20px 60px rgba(0,0,0,0.3); }
.icon { font-size:48px; margin-bottom:16px; }
.title { font-size:24px; font-weight:700; margin-bottom:8px; color:#1a1a2e; }
.subtitle { font-size:14px; color:#999; margin-bottom:32px; }
.pwd-input { width:100%; padding:12px 16px; font-size:16px; border:2px solid #e0e0e0;
  border-radius:8px; text-align:center; letter-spacing:4px; }
.btn { width:100%; margin-top:16px; padding:12px; font-size:16px; font-weight:600;
  color:#fff; background:#1a1a2e; border:none; border-radius:8px; }
.btn::after { border:none; }
.error { color:#e53e3e; font-size:14px; margin-top:12px; min-height:20px; }
```

- [ ] **Step 3: auth.js**

```javascript
Page({
  data: { pwd: '', error: '' },
  onInput(e) { this.setData({ pwd: e.detail.value, error: '' }); },
  async onSubmit() {
    var VALID = 'c252bf49e6766b2ea0f46d6ec62f6588a12ee942d363f17cfe4785d0cc75d5fb';
    var pwd = this.data.pwd.trim();
    if (!pwd) { this.setData({ error: '请输入密码' }); return; }
    var buf = new Uint8Array(await crypto.subtle.digest('SHA-256',
      new TextEncoder().encode(pwd)));
    var h = Array.from(buf).map(function(b){ return b.toString(16).padStart(2,'0'); }).join('');
    if (h !== VALID) { this.setData({ error: '密码错误', pwd: '' }); return; }
    wx.setStorageSync('xunfang_auth', h);
    wx.switchTab({ url: '/pages/zhuangbei/index/index' });
  }
});
```

- [ ] **Step 4: auth.json**

```json
{ "usingComponents": {}, "navigationBarTitleText": "验证访问" }
```

- [ ] **Step 5: 验证**

在微信开发者工具中打开 auth 页：
1. 不输入 → 确认 → 显示"请输入密码"
2. 输入错误密码 → 确认 → 显示"密码错误"，输入框清空
3. 输入 `wrf150225` → 确认 → 跳转 tabBar 首页
4. 检查 Storage → `xunfang_auth` 已设置

- [ ] **Step 6: 提交**

---

### Task 3: 创建数据文件

**Files:**
- Create: `miniprogram/data/zhuangbei.js`
- Create: `miniprogram/data/jingqing.js`

- [ ] **Step 1: data/zhuangbei.js — 装备介绍7篇文章数据**

```javascript
module.exports = [
  {
    id: 'jiuxiaojian-gailan',
    title: '九小件概览',
    icon: '📦',
    section: '核心装备',
    desc: '九小件清单、佩戴原则、佩戴顺序、装备分类',
    tags: ['9件标准装备', '贴身紧靠', '武力升级'],
    flow: '📋 3原则：贴身紧靠 → 方便拿取 → 武力升级',
    quickCard: {
      title: '九小件概览',
      tags: ['9件标准装备', '贴身紧靠', '武力升级'],
      flow: '📋 3原则：贴身紧靠 → 方便拿取 → 武力升级'
    },
    steps: [
      { num:1, title:'九小件清单', color:'blue', lead:'九件标准装备以多功能腰带为承载平台，涵盖作战、防护、控制通讯三大类别。', content:'单警装备九小件是基层民警日常执勤执法中随身配备的九种标准警用装备的统称。\n\n1. 多功能腰带 — 承载所有装备的基础平台\n2. 伸缩警棍 — 最常用的驱逐性、制服性警械\n3. 强光手电 — 照明与战术配合用途\n4. 执法记录仪 — 全程记录执法过程\n5. 手铐 — 约束性警械\n6. 警用工作包（含急救包）\n7. 防割手套 — 保护手部安全\n8. 催泪喷射器 — 非杀伤性驱逐警械\n9. 对讲机 — 通讯联络设备', expandable:true, media:{type:'img',label:'📷 九小件全套平铺展示图'} },
      { num:2, title:'佩戴三大原则', color:'blue', lead:'贴身紧靠防脱落，方便拿取按使用频率排序，武力升级由低到高体现最小武力原则。', content:'贴身紧靠：所有装备紧贴身体，不松动、不晃荡，避免在奔跑或对抗中脱落。\n\n方便拿取：常用装备置于强手容易够到的第一选择位。\n\n武力升级：按武力等级由低到高排列——先取非杀伤性警械，再取驱逐性警械，最后考虑致命武力。体现"最小武力原则"。', expandable:true, media:{type:'img',label:'📷 多功能腰带全装佩戴正面照'} },
      { num:3, title:'佩戴顺序', color:'blue', lead:'从左至右：弹匣→伸缩警棍→强光手电→对讲机→警用水壶→手铐→工作包→手枪→催泪喷射器。', content:'从左至右依次为：弹匣 → 伸缩警棍 → 强光手电 → 对讲机 → 警用水壶 → 手铐 → 警务工作包/急救包 → 手枪 → 催泪喷射器\n\n警用制式刀具位于警务工作包和手枪之间。催泪喷射器按喷口超前、摆放合适、快速拿取原则，一般位于强手第一选择位。', expandable:true, media:{type:'img',label:'📷 腰带展开俯视图'} },
      { num:4, title:'装备三大分类', color:'blue', lead:'作战类（警棍/喷射器/手电/臂盾）、防护类（手套/急救包/腰带）、控制通讯类（手铐/对讲机/记录仪）。', content:'作战类：伸缩警棍、催泪喷射器、强光手电、警用多功能臂盾\n防护类：防割手套、工作包（急救包）、多功能腰带、灭火器、救生圈\n控制通讯类：手铐、约束带、对讲机、执法记录仪', expandable:true }
    ],
    prevId: null, nextId: 'shensuo-jinggun'
  },
  {
    id: 'shensuo-jinggun',
    title: '伸缩警棍',
    icon: '🪠',
    section: '核心装备',
    desc: '基本介绍 · 法律支撑 · 击打部位 · 戒备/开棍/劈击/握棍技术 · 安全注意事项',
    tags: ['⚠️ 驱逐性警械', '伸长约52cm', '收缩约22cm'],
    flow: '📋 7步：介绍 → 法律 → 击打部位 → 戒备 → 开棍 → 劈击 → 握棍',
    quickCard: {
      title: '伸缩警棍',
      tags: ['⚠️ 驱逐性警械', '伸长约52cm', '收缩约22cm'],
      flow: '📋 7步：介绍 → 法律 → 击打部位 → 戒备 → 开棍 → 劈击 → 握棍'
    },
    steps: [
      { num:1, title:'基本介绍', color:'blue', lead:'伸出总长约52cm，收缩约22cm。甩动展开，按解锁按钮回收。基层使用频率最高的驱逐性警械。', content:'伸缩警棍由尾盖、解锁按钮、握把、中管、小管、棍头鼓碟组成。\n\n展开：通过甩动使各节管伸出锁定\n回收：一手按解锁按钮，一手按棍头回压收回', expandable:true, media:{type:'img',label:'📷 伸缩警棍结构图'} },
      { num:2, title:'法律支撑', color:'orange', lead:'依据《人民警察使用警械和武器条例》第七条，经警告无效后可使用。以制止为限度，行为被制止后立即停止。', content:'1. 结伙斗殴、殴打他人、寻衅滋事、侮辱妇女等流氓活动\n2. 聚众扰乱车站、码头、运动场等公共场所秩序\n3. 非法举行集会、游行、示威\n4. 强行冲越警戒线\n5. 以暴力方法抗拒或阻碍执法\n6. 袭击人民警察\n7. 危害公共安全、社会秩序和公民人身安全需当场制止\n8. 法律、行政法规规定的其他情形\n\n使用限度：以制止违法犯罪行为为限度，行为得到制止时应立即停止使用。', expandable:true },
      { num:3, title:'击打部位', color:'red', lead:'只打击大肌肉群和运动神经点，定点定位。严禁击打头部、脖子、胫骨、裆部。', content:'合法击打部位（大肌肉群）：\n· 大腿外侧/内侧中心区（腓骨神经）\n· 小臂内侧/外侧、大臂内侧/外侧（桡侧神经、桡正中神经）\n· 小腿后部\n\n严禁击打部位：\n· 头部 — 可能致命\n· 脖子、太阳穴 — 要害部位\n· 小腿胫骨 — 骨骼突出，表皮薄，易严重骨折\n· 裆部及其他骨骼脆弱处', expandable:true, media:{type:'img',label:'📷 人体击打部位示意图'} },
      { num:4, title:'戒备姿势', color:'blue', lead:'三种姿态逐级升级：隐藏戒备（腹前）→ 提棍戒备（腿后）→ 肩上戒备（攻击准备姿态）。', content:'隐藏戒备：双手抓握警棍置于腹前，双眼目视前方。警棍隐蔽不暴露，适合初期接触阶段。\n\n提棍戒备：单手持棍藏于大腿后侧。半隐蔽状态，已做好出棍准备。\n\n肩上戒备（教学重点）：右脚后撤半步，重心置于两腿之间，右手握棍尾端、棍尾朝前，手肘夹紧肋部。半侧身站位利于发力且降低暴露面积。', expandable:true, media:{type:'img',label:'📷 三种戒备姿势对比图'} },
      { num:5, title:'开棍技术', color:'green', lead:'上开棍接上劈击，下开棍接下劈击，紧急开棍边出棍边后退拉开安全距离。', content:'上开棍：棍头朝斜上方甩出，自然衔接上劈击准备姿态。\n下开棍：棍头朝斜下方甩出，自然衔接下劈击准备姿态。\n紧急开棍（教学重点）：棍头朝前甩出，左右甩动，同时左手戒备、身体战术性后退。核心是边出棍边后退，创造反应时间。', expandable:true, media:{type:'video',label:'🎬 三种开棍方式示范视频'} },
      { num:6, title:'劈击技术', color:'green', lead:'发力链条：蹬地 → 扭腰 → 送胯 → 挥肘，全身动力链传导至警棍上端。', content:'上劈击：从肩上戒备，由上方向前下方挥击，用警棍上端击打对象大臂处。\n下劈击：从肩上戒备，由下方向前上方挥击，用警棍上端击打对象大腿处。\n\n击打部位限于上臂、大腿等大肌肉群，避开骨骼和要害部位。', expandable:true, media:{type:'video',label:'🎬 上劈击与下劈击示范视频'} },
      { num:7, title:'握棍方式', color:'purple', lead:'拇指、中指、无名指三指主握，棍柄下端空出约两指距离，击打时必须紧固握棍。', content:'用拇指、中指、无名指作为三只主要握棍手指，握住警棍棍柄，棍柄下端空出约两指距离，其他手指作为辅助。击打时不能放松手腕及手部。三指主握形成稳定的三角形握力，下端留两指空间确保手腕灵活性。', expandable:true },
      { num:'!', title:'安全注意事项', color:'red', lead:'使用前口头警告，使用中以制止为限度，使用后记录并报告。开棍前观察周围环境避免误伤。', content:'法定限度：以制止为限度，行为被制止后立即停止使用。使用前必须口头警告。\n\n操作安全：开棍前观察周围环境，避免误伤围观群众。下开棍时注意不要误伤儿童。紧急开棍注意棍头朝向。使用后检查警棍状态，确认回收装置正常。\n\n执法规范：使用前先行警告（"警察别动，否则使用警械，无关人员躲避"）→ 使用中以制止为限度 → 使用后记录并报告。', expandable:true }
    ],
    prevId: 'jiuxiaojian-gailan', nextId: 'cuilei-pensheqi'
  },
  {
    id: 'cuilei-pensheqi',
    title: '催泪喷射器',
    icon: '💨',
    section: '核心装备',
    desc: '基本介绍 · 性能参数 · 喷移问口诀 · 天时地利人和 · 善后处理 · 禁止情形',
    tags: ['⚠️ 非杀伤性驱逐警械', '3-6米射程', '喷移问口诀'],
    flow: '📋 3步口诀：喷（点射≤1秒）→ 移（变换位置）→ 问（安抚净化）',
    quickCard: {
      title: '催泪喷射器',
      tags: ['⚠️ 非杀伤性驱逐警械', '3-6米射程', '喷移问口诀'],
      flow: '📋 3步口诀：喷（点射≤1秒）→ 移（变换位置）→ 问（安抚净化）'
    },
    steps: [
      { num:1, title:'基本介绍', color:'blue', lead:'最常用的非杀伤性驱逐警械，93%的警情处置中使用。3-6米攻击距离，体积小便于携带，对吸毒闹事者同样有效。', content:'催泪喷射器是最常用的非杀伤性驱逐性、制服性警械，通过喷射催泪剂（CS/OC）刺激人体感官系统使其暂时丧失抵抗能力。据不完全统计，2022年全市警情处置中共253次使用警械，其中93%用到了催泪喷射器。\n\n优势：非杀伤性、人性化、3-6米攻击距离远、体积小便于携带、对吸毒闹事者同样有效。', expandable:true },
      { num:2, title:'性能参数', color:'blue', lead:'容量40~50ml，有效射距>3m（最大6m），使用温度-30~+45°C，储存年限≥3年，不得暴晒存放以免爆炸。', content:'外径：35mm  全长：≤150mm  质量：≤0.1kg\n容量：40~50ml  有效射距：＞3m（最大6m）\n使用温度：-30 ~ +45°C  储存年限：≥3年\n喷射剂种类：催泪剂（CS或OC，具有挥发性）\n\n刺激效果：皮肤接触30秒后烧灼感；眼睛触到灼痛流泪肿胀视力受损；口鼻吸入呼吸道肿胀咳嗽呼吸不畅；面部喷射导致剧烈疼痛和不自主闭眼。\n\n存储要求：阴凉保管，不与易燃易爆品混放，不得放在暴晒汽车内等高温处以免爆炸。', expandable:true, media:{type:'img',label:'📷 催泪喷射器结构/型号外观图'} },
      { num:3, title:'使用要领（喷—移—问）', color:'orange', lead:'每次点射不超过1秒瞄准面部，喷射后立即移动位置避免反击，告诉对方服从则停止使用并帮他净化。', content:'使用前检查：装置是否正常、有无过期、喷射形态（柱状/雾状）、确认风向（严禁逆风喷射）。\n\n持握方式：单手持握（成扶带戒备姿势）或双手合握（增加稳定性）。\n\n喷射方式：上下式（单个对象）、左右式（多名对象横扫）、环状式（群体事件，环形喷射形成防护屏障）。\n\n核心口诀：喷—移—问\n① 喷：每次点射不超过1秒，瞄准面部。法言法语先行："警察别动，否则使用警械，无关人员躲避！"\n② 移：喷射后必须及时移动位置，避免对方沿喷射方向反击。持续戒备。\n③ 问：告诉被喷射者"如果服从，停止使用"。安抚对方，帮他净化。', expandable:true, media:{type:'video',label:'🎬 "喷—移—问"操作示范视频'} },
      { num:4, title:'天时地利人和原则', color:'orange', lead:'天时：顺风站位，逆风禁用。地利：不在低洼处使用，保持3米安全距离。人和：围观人群多时慎用。', content:'天时：观察天气和风向，应处在目标的上风方向，避免逆风向使用。\n地利：选择合理位置，不在低洼处使用。有效距离一般3米，保持安全距离。\n人和：围观人群较多、距离较近时慎用或不用，以免连累无辜，导致群众不理解，造成事态扩大。', expandable:true },
      { num:5, title:'善后处理五步流程', color:'green', lead:'持续警告→安抚安慰→净化处理（清水冲洗勿揉擦）→详细询问病史→后续观察（痛苦感15-30分钟消退）。', content:'第一步 · 持续警告："警察别动，请停止你的行为，否则将继续喷射。"\n第二步 · 安抚安慰："不要揉擦双眼和面部，如你配合，我们将带你清洗。"\n第三步 · 净化处理：移至通风区域 → 大量清水冲洗脸部和眼睛 → 不要揉擦 → 擤鼻咳吐 → 取下隐形眼镜 → 用湿/干纸巾吸干残留剂 → 清洗后通风。\n第四步 · 详细询问：逐项确认：是否饮酒吃药？8小时内有无饮酒吃药？是否有哮喘、心脏病、高血压、糖尿病等？是否有过敏史？女性是否怀孕？\n第五步 · 后续观察：痛苦感一般15-30分钟消退，最多1-2小时。敏感者红斑数小时内消失。症状持续应送医院。押解时不要让其卧姿或仰姿，防止压迫腹胸部造成呼吸困难。', expandable:true },
      { num:'!', title:'法定禁止情形', color:'red', lead:'五种禁止使用情形：已丧失抵抗者、近距离对眼嘴喷射、未成年人、妇女限制使用、伤残及有疾病人员。', content:'五种不得使用情形：\n1. 已失去抵抗能力者（已在车内、房间内、被制服丧失抵抗）\n2. 不得近距离直接对准眼睛和嘴巴喷射（可能造成永久性眼部损伤）\n3. 对未成年人不得使用\n4. 对妇女限制使用（以制止暴力为限度）\n5. 伤残人员及有疾病的人员\n\n催泪喷射器虽是"非杀伤性警械"，但并非"无伤害"警械。不当使用仍可能造成严重损害。', expandable:true }
    ],
    prevId: 'shensuo-jinggun', nextId: 'shoukao'
  },
  {
    id: 'shoukao',
    title: '手铐',
    icon: '🔗',
    section: '核心装备',
    desc: '六种上铐方法 · 使用注意事项 · 武力链条定位',
    tags: ['约束性警械', '六种上铐方法', '武力链条第四环节'],
    flow: '📋 6种上铐：开口 → 压腕 → 挑腕 → 背手 → 举手 → 倒地',
    quickCard: {
      title: '手铐',
      tags: ['约束性警械', '六种上铐方法', '武力链条第四环节'],
      flow: '📋 6种上铐：开口 → 压腕 → 挑腕 → 背手 → 举手 → 倒地'
    },
    steps: [
      { num:1, title:'定位：武力链条中的约束环节', color:'blue', lead:'口头警告→催泪喷射器→伸缩警棍→手铐。使用前提是行为已被制止、嫌疑人已被制服。', content:'手铐属于约束性警械，在武力链条中处于第四环节：\n口头警告 → 催泪喷射器（非杀伤性驱逐）→ 伸缩警棍（驱逐性/制服性）→ 手铐（约束性）\n\n使用手铐的前提通常是对违法行为已经得到制止、犯罪嫌疑人已被制服的情况下实施。依法使用必须符合法律规定条件，不得随意使用。', expandable:true, media:{type:'img',label:'📷 手铐结构图'} },
      { num:2, title:'六种上铐方法', color:'orange', lead:'从不配合到强烈反抗逐级应对：开口上铐→压腕上铐→挑腕上铐→背手上铐→举手上铐→倒地上铐。', content:'1. 开口上铐：对方不配合但有基本配合意愿时。以安全方位接近，快速将铐环套入对方手腕。\n\n2. 压腕上铐：对有一定反抗意图的对象。利用身体重量压制对方手腕，配合上铐动作。\n\n3. 挑腕上铐：从下方挑起对方手腕顺势上铐。适用于对方手部位置较低的情况。\n\n4. 背手上铐：将对方双手引至背后上铐。最常用、最安全的约束方式，能最大程度限制上半身活动。\n\n5. 举手上铐：令对方举双手，从正面或侧面快速上铐。适用于对方配合度较高的情形。\n\n6. 倒地上铐：将对方控制在地面后实施上铐。适用于对方强烈反抗、已被控制在地面的情形。', expandable:true, media:{type:'video',label:'🎬 六种上铐方法示范视频'} },
      { num:'!', title:'使用注意事项', color:'red', lead:'使用前确认铐环灵活，上铐后松紧以一指为宜，先上铐再搜身，押解途中注意观察。', content:'· 使用前确认铐环转动灵活、锁闭机构正常\n· 上铐后检查松紧度（以能塞入一根手指为宜），不得过紧造成手腕损伤\n· 上铐后不得让嫌疑人自行解除\n· 押解途中注意观察手铐状态和嫌疑人手腕情况\n· 搜身上铐的顺序：先上铐再搜身，确保自身安全', expandable:true }
    ],
    prevId: 'cuilei-pensheqi', nextId: 'zhifa-jiuyi'
  },
  {
    id: 'zhifa-jiuyi',
    title: '执法记录仪',
    icon: '📹',
    section: '核心装备',
    desc: '日常检查维护 · 使用规范 · 涉密警情保密纪律',
    tags: ['执法装备', '全程记录', '保密要求'],
    flow: '📋 3步：检查 → 开启 → 保存',
    quickCard: {
      title: '执法记录仪',
      tags: ['执法装备', '全程记录', '保密要求'],
      flow: '📋 3步：检查 → 开启 → 保存'
    },
    steps: [
      { num:1, title:'日常检查维护', color:'blue', lead:'每日上岗前检查电量、存储空间、镜片清洁度、日期时间是否正确。', content:'· 检查电量和存储空间是否充足\n· 检查镜片表面是否洁净\n· 检查时间日期是否正确，避免视频文件时间戳错误\n· 检查佩戴方式是否正确，确保摄像头不被遮挡\n· 发现故障立即上报更换备用设备', expandable:true, media:{type:'img',label:'📷 执法记录仪佩戴位置示意图'} },
      { num:2, title:'使用规范', color:'blue', lead:'到达现场即开启，全程录像。告知当事人\"本次执法活动全程录音录像\"。', content:'· 到达现场即开启执法记录仪，确保录制起始时间点不晚于接触当事人时间\n· 规范告知："本次执法活动全程录音录像，请你配合"\n· 保持全程录像，不得选择性录制或中断（除非涉密场所）\n· 图像内容应包含执法对象的面部、行为、周围环境\n· 记录处置的关键环节：警告、使用警械、上铐、搜身、带离', expandable:true, media:{type:'img',label:'📷 执法记录仪操作界面'} },
      { num:'!', title:'涉密警情保密纪律', color:'red', lead:'涉密警情不得摄录，非涉密录像不得私自下载、转发、传播。', content:'· 在涉密场所须关闭执法记录仪（如军事禁区、涉密单位内部）\n· 不得私自下载、复制、转发、传播执法记录仪中的任何音视频内容\n· 未经批准，严禁在社交媒体上传或传播执法视频\n· 违反上述规定将追究纪律和法律责任', expandable:true }
    ],
    prevId: 'shoukao', nextId: 'fangge-shoutao'
  },
  {
    id: 'fangge-shoutao',
    title: '防割手套',
    icon: '🧤',
    section: '核心装备',
    desc: '防割不防刺 · 使用后检查维护 · 高风险场景应用',
    tags: ['防护类装备', '防割不防刺', '及时更换'],
    flow: '📋 3要点：性能边界 → 使用场景 → 使用后维护',
    quickCard: {
      title: '防割手套',
      tags: ['防护类装备', '防割不防刺', '及时更换'],
      flow: '📋 3要点：性能边界 → 使用场景 → 使用后维护'
    },
    steps: [
      { num:'!', title:'核心性能边界：防割不防刺', color:'red', lead:'可抵御刀具的切割和划伤，但无法防御尖锐物体的穿刺伤害。不可将防割手套当作全防护手套使用。', content:'防割手套可以抵御刀具的切割和划伤，但无法防御尖锐物体的穿刺伤害。民警在使用时需明确这一区别，不可将防割手套当作全防护手套使用。', expandable:true, media:{type:'img',label:'📷 防割不防刺对比示意'} },
      { num:1, title:'使用场景', color:'blue', lead:'盘查搜身时防止锐器伤害、伸缩警棍处置中的手部防护、持刀类警情时保护手部、可疑物品安全检查。', content:'在以下高风险执法场景中发挥重要保护作用：\n\n· 盘查搜身时防止被嫌疑人携带的锐器伤害\n· 伸缩警棍处置中的手部防护\n· 处置持刀类警情时保护手部免受利刃划伤\n· 对可疑物品进行安全检查时', expandable:true, media:{type:'img',label:'📷 民警佩戴手套搜身场景照'} },
      { num:2, title:'使用后维护', color:'orange', lead:'使用后及时检查表面有无破损，发现破损必须立即更换，破损后防护能力大幅下降。', content:'· 使用后要及时检查手套表面有无破损\n· 如发现破损须及时更换，不可再继续使用\n· 破损的防割手套防护能力大幅下降，继续使用可能造成严重伤害', expandable:true }
    ],
    prevId: 'zhifa-jiuyi', nextId: 'jingxie-jinggao'
  },
  {
    id: 'jingxie-jinggao',
    title: '警械使用警告用语',
    icon: '📢',
    section: '规范用语',
    desc: '标准警告用语 · 法律依据 · 不同警械的警告变体',
    tags: ['警告用语', '法言法语', '规范执法'],
    flow: '📋 标准用语 → 警棍变体 → 喷射器变体',
    quickCard: {
      title: '警械使用警告用语',
      tags: ['警告用语', '法言法语', '规范执法'],
      flow: '📋 标准用语 → 警棍变体 → 喷射器变体'
    },
    steps: [
      { num:1, title:'标准警告用语', color:'blue', lead:'"警察，别动，否则使用警械，无关人员躲避！" 声音洪亮、语速适中、态度坚决。', content:'标准警告用语："警察，别动，否则使用警械，无关人员躲避！"\n\n要求：\n· 声音洪亮清晰，确保执法对象和周围群众都能听见\n· 语速适中，不宜过快让对象听不清，也不宜过慢丧失气势\n· 给予合理反应时间（根据现场情况判断），警告不得少于一次\n· 紧急情况下可直接使用警械（如对象即将实施严重伤害行为）', expandable:true, media:{type:'img',label:'📷 警告用语参考卡片'} },
      { num:2, title:'伸缩警棍警告变体', color:'orange', lead:'"警察，别动，否则使用伸缩警棍，无关人员躲避！"', content:'明确告知使用警棍的意图。警告后用规范动作亮出警棍（进入戒备状态），让对象看到警棍已准备使用。警告后给对象2-3秒反应时间。', expandable:true },
      { num:3, title:'催泪喷射器警告变体', color:'orange', lead:'"警察，别动，否则使用催泪喷射器，无关人员躲避！"', content:'喷前确认风向后发出警告。警告同时将喷射器置于对象可视的持握姿势，起震慑作用。', expandable:true }
    ],
    prevId: 'fangge-shoutao', nextId: null
  }
];
```

- [ ] **Step 2: data/jingqing.js — 警情处置8篇文章数据**

```javascript
module.exports = [
  {
    id: 'chidao-leiqing',
    title: '持刀类警情处置',
    icon: '🔪',
    section: '街面警情',
    desc: '梯次化处置 + 模块化策应，5人作战小组分工',
    tags: ['⚠️ 高风险', '5人小组', '安全距离≥5米'],
    flow: '📋 4步：疏散稳控 → 作战控制 → 封控取证 → 移交恢复',
    quickCard: {
      title: '持刀类警情处置',
      tags: ['⚠️ 高风险', '5人小组', '安全距离≥5米'],
      flow: '📋 4步：疏散稳控 → 作战控制 → 封控取证 → 移交恢复'
    },
    steps: [
      { num:'!', title:'处置概述', color:'red', lead:'梯次化处置 + 模块化策应，5人作战小组分职能模块，以阶段目标为导向灵活调整战术。', content:'持刀类警情采用"梯次化处置 + 模块化策应"体系，将5人作战小组分为不同职能模块，在处置前、中、后三个阶段逐步升级/降级应对。核心原则：以阶段目标为导向，灵活调整战术组合，避免流程僵化。', expandable:true, media:{type:'img',label:'📷 5人作战小组站位示意图'} },
      { num:1, title:'第一阶段：疏散稳控（2+2+1 队形）', color:'red', lead:'分割策应、避免激化。保持安全距离≥5米，语言安抚为主，避免直接冲突升级。', content:'目标：了解现场情况、疏散围观群众、明确核心对象。\n\n分工：\n· 1号位（指挥）+ 3号位（盾牌手）：伤员安抚与报警人询问\n· 2号位（盾牌手）+ 4号位（长棍）：持械人员盘查与情绪疏导\n· 5号位（支援手）：外围封控与舆情引导\n\n战术要点：分割策应、避免激化。保持安全距离≥5米，语言安抚为主，避免直接冲突升级。', expandable:true, media:{type:'img',label:'📷 2+2+1 疏散稳控队形站位图'}, media2:{type:'video',label:'🎬 疏散稳控示范视频（30秒）'} },
      { num:2, title:'第二阶段：作战控制（4+1 队形）', color:'orange', lead:'盾棍叉协同推进，将嫌疑人逼至安全角落后制伏。集中优势力量，一招制敌。', content:'目标：消除危险、控制核心对象。\n\n行动流程：\n1. 夹击阵型将嫌疑人引导至角落/墙角\n2. 盾牌手（2、3号位）在前推进，长棍手（4号位）侧翼掩护\n3. 法律告知 → 警告无效 → 盾牌撞击 → 抓捕叉锁脚踝\n\n战术要点：盾牌始终保持在嫌疑人与队员之间。多人协同同时行动，不给嫌疑人逐个击破机会。', expandable:true, media:{type:'img',label:'📷 4+1 作战控制队形图'}, media2:{type:'video',label:'🎬 盾棍叉协同制伏示范视频（45秒）'} },
      { num:3, title:'第三阶段：封控取证（3+1+1 队形）', color:'blue', lead:'上铐前务必完成搜身，排除其他危险物品。舆情封控与证据固定同步完成。', content:'目标：舆情清扫、移交程序、固定周边证据。\n\n分工：\n· 1号位（指挥）：证据收集与交接协调\n· 2、3号位（盾牌手）：上铐搜身与带离\n· 4号位（长棍手）：持续外围警戒\n· 5号位（支援手）：舆情封控与证据固定\n\n战术要点：上铐前务必完成搜身，排除其他危险物品。训练中实际使用扎带。', expandable:true, media:{type:'img',label:'📷 3+1+1 封控取证站位图'}, media2:{type:'video',label:'🎬 上铐搜身与带离示范视频'} },
      { num:4, title:'处置收尾：移交与恢复', color:'green', lead:'完整移交当事人及危险物品，确认执法记录仪保存，汇报指挥中心后恢复勤务。', content:'· 向到达的刑侦/派出所警力交接当事人及危险物品\n· 确认执法记录仪全程录像已保存\n· 汇报指挥中心处置结果\n· 解除警戒，恢复巡逻勤务', expandable:true },
      { num:5, title:'模块化策应战术要点', color:'purple', lead:'每个阶段聚焦一个主要目标，集中优势力量完成后转入下一阶段，不追求同时完成所有目标。', content:'处置前期（2+2+1）：疏散稳控、分割策应\n处置中期（4+1）：消除危险、控制核心对象\n处置后期（3+1+1）：封控取证、舆情风险消除', expandable:true }
    ],
    prevId: null, nextId: 'zuijiu-naoshi'
  },
  {
    id: 'zuijiu-naoshi',
    title: '醉酒闹事警情处置',
    icon: '🍺',
    section: '街面警情',
    desc: '醉酒人员约束控制、约束带使用、医疗联动',
    tags: ['⚠️ 高风险', '约束控制', '医疗联动'],
    flow: '📋 5步：到场评估 → 语言控制 → 约束控制 → 医疗联动 → 移交处理',
    quickCard: {
      title: '醉酒闹事警情处置',
      tags: ['⚠️ 高风险', '约束控制', '医疗联动'],
      flow: '📋 5步：到场评估 → 语言控制 → 约束控制 → 医疗联动 → 移交处理'
    },
    steps: [
      { num:1, title:'到场评估', color:'blue', lead:'到场先观察：对方饮酒程度、有无持有物品、周围环境、围观人群数量。', content:'到场先观察，不要匆忙接触：\n· 评估对方饮酒程度和情绪状态\n· 确认有无持有危险物品（酒瓶、刀具等）\n· 观察周围环境（是否在阳台、楼顶、水边等危险区域）\n· 注意围观人群数量和情绪\n· 确认是否需要消防、120协同到场', expandable:true },
      { num:2, title:'语言控制', color:'orange', lead:'态度平和、语速放缓、不与醉酒者争辩。以"朋友"身份沟通而非"警察"身份命令。', content:'态度平和、语速放缓。醉酒者判断力下降，强硬态度容易引发对抗。\n\n以"朋友"身份沟通："兄弟，怎么回事？需要帮忙吗？" 先建立沟通，再引导配合。\n\n保持安全距离≥2米，准备随时后撤。', expandable:true },
      { num:3, title:'约束控制', color:'red', lead:'语言控制无效时，多人协同使用约束带。抓住嫌疑人松懈瞬间，三人同时行动。', content:'· 先疏散围观群众，避免人群刺激嫌疑人情绪\n· 保持安全距离≥2米，语言安抚为主，不单独近身\n· 盾牌在前，抓捕手侧翼，一人外围警戒\n· 抓住嫌疑人松懈瞬间，三人同时行动，一招制敌\n· 优先使用约束带（比手铐更安全），将对象控制为侧卧位', expandable:true, media:{type:'video',label:'🎬 醉酒约束带使用示范'} },
      { num:4, title:'医疗联动', color:'green', lead:'醉酒者可能合并外伤、酒精中毒、基础疾病突发，必须呼叫120到场评估。', content:'· 约束后立即呼叫120到场评估\n· 检查有无外伤（醉酒者常常不觉疼痛）\n· 注意防范酒精中毒引起的呼吸道梗阻\n· 不得让醉酒者仰卧，应侧卧防窒息\n· 等待120期间持续观察呼吸和意识状态', expandable:true },
      { num:5, title:'移交处理', color:'purple', lead:'移交辖区派出所处理，全程执法记录仪录像，做好处置情况记录。', content:'· 移交辖区派出所或通知家属领回\n· 造成财物损失或人员伤害的，固定证据\n· 全程执法记录仪开启，记录处置过程\n· 向指挥中心报备处置结果', expandable:true }
    ],
    prevId: 'chidao-leiqing', nextId: 'dajia-douou'
  },
  {
    id: 'dajia-douou',
    title: '打架斗殴警情处置',
    icon: '👊',
    section: '街面警情',
    desc: '现场分离、伤情评估、当事人询问、证据固定',
    tags: ['街面常见', '现场分离', '证据固定'],
    flow: '📋 5步：到场分离 → 伤情评估 → 身份登记 → 取证 → 移交/和解',
    quickCard: {
      title: '打架斗殴警情处置',
      tags: ['街面常见', '现场分离', '证据固定'],
      flow: '📋 5步：到场分离 → 伤情评估 → 身份登记 → 取证 → 移交/和解'
    },
    steps: [
      { num:1, title:'到场分离', color:'red', lead:'到场后先分离双方，保持物理隔离（≥3米），防止再次发生肢体冲突。', content:'到场后第一时间分离双方：\n· 保持物理隔离距离≥3米\n· 安排队员分别看管双方\n· 注意观察双方情绪，防止再次冲突\n· 疏散围观群众，控制现场秩序', expandable:true },
      { num:2, title:'伤情评估与救治', color:'orange', lead:'先处理伤员。有明显外伤的呼叫120。注意隐蔽伤情（内出血、头部外伤）。', content:'先处理伤员，生命优先。\n· 检查双方有无明显外伤\n· 有明显出血的立即止血\n· 头部受击的注意颅内出血风险\n· 呼叫120到场评估\n· 记录伤情（拍照）作为后续证据', expandable:true },
      { num:3, title:'身份登记与询问', color:'blue', lead:'查验双方身份证件，分别询问事情经过（隔离询问防止串供）。', content:'· 查验身份证件，核实身份信息\n· 隔离询问——将双方分开，分别了解事情经过\n· 询问要点：起因、时间、参与人员、使用的物品/工具\n· 了解双方是否有意愿调解处理', expandable:true },
      { num:4, title:'现场取证', color:'blue', lead:'拍照固定现场情况、调取周边监控、寻找目击证人。', content:'· 拍照固定现场情况（物品损坏、血迹位置等）\n· 调取周边监控录像\n· 寻找并询问目击证人\n· 提取作案工具（如有）\n· 执法记录仪全程开启', expandable:true },
      { num:5, title:'后续处理', color:'purple', lead:'符合调解条件的现场调解；构成治安案件的移交派出所；构成刑事案件的移交刑侦。', content:'· 符合调解条件的：双方自愿调解的现场调解处理\n· 构成治安案件的：移交辖区派出所\n· 构成刑事案件的：移交刑侦部门\n· 向指挥中心汇报处置结果', expandable:true }
    ],
    prevId: 'zuijiu-naoshi', nextId: 'jiating-baoli'
  },
  {
    id: 'jiating-baoli',
    title: '家庭暴力警情处置',
    icon: '🏠',
    section: '街面警情',
    desc: '人身保护、告诫书出具、受害人救助与社会联动',
    tags: ['家庭暴力', '告诫书', '社会联动'],
    flow: '📋 4步：到场制止 → 人身保护 → 告诫/案件 → 社会联动',
    quickCard: {
      title: '家庭暴力警情处置',
      tags: ['家庭暴力', '告诫书', '社会联动'],
      flow: '📋 4步：到场制止 → 人身保护 → 告诫/案件 → 社会联动'
    },
    steps: [
      { num:1, title:'到场制止', color:'red', lead:'到场后立即制止暴力行为。如暴力正在发生且情节严重，应立即控制施暴者。', content:'· 到场后立即制止正在发生的暴力行为\n· 暴力情节严重（持械、多人殴打等）应立即控制施暴者\n· 注意保护在场未成年人，避免其目睹暴力场面\n· 观察现场环境，注意施暴者是否有其他危险物品', expandable:true },
      { num:2, title:'人身保护与救助', color:'orange', lead:'关注受害人伤情，必要时呼叫120。同时注意未成年人、老人等弱势家庭成员的保护。', content:'· 关注受害人伤情，有明显外伤的呼叫120\n· 对受害人进行情绪安抚\n· 注意保护在场的未成年人、老人\n· 如受害人需要离开家庭，联系妇联或社区安排临时庇护', expandable:true },
      { num:3, title:'告诫/案件处理', color:'blue', lead:'家暴是违法行为，不属单纯\"家庭纠纷\"。情节较轻的开具告诫书，情节较重的依法处理。', content:'· 家庭暴力是违法行为，不属于单纯的"家庭纠纷"，不可简单"劝和"\n· 情节较轻、受害人谅解的：开具《家庭暴力告诫书》\n· 情节较重（造成轻伤以上、多次反复、持械等）：依法治安处罚或刑事立案\n· 告诫书一式多份：施暴人、受害人、居委会/村委会各一份', expandable:true },
      { num:4, title:'社会联动与跟进', color:'purple', lead:'告知受害人有申请人身安全保护令的权利。联动妇联、社区跟进后续情况。', content:'· 告知受害人有向法院申请人身安全保护令的权利\n· 联动妇联、社区/村委会跟进后续情况\n· 做好处置记录，便于后续回访和证据累积\n· 施暴者多次家暴的从重处理', expandable:true }
    ],
    prevId: 'dajia-douou', nextId: 'renyuan-pancha'
  },
  {
    id: 'renyuan-pancha',
    title: '人员盘查',
    icon: '🪪',
    section: '盘查规范',
    desc: '六步法：表明身份 → 告知依据 → 查验身份 → 口头警告 → 口头传唤 → 强制传唤',
    tags: ['盘查规范', '六步法', '最小武力'],
    flow: '📋 6步法：表明身份 → 告知依据 → 查验 → 警告 → 传唤 → 强制传唤',
    quickCard: {
      title: '人员盘查',
      tags: ['盘查规范', '六步法', '最小武力'],
      flow: '📋 6步法：表明身份 → 告知依据 → 查验 → 警告 → 传唤 → 强制传唤'
    },
    steps: [
      { num:1, title:'第一步：表明身份', color:'blue', lead:'主动出示人民警察证，口头告知"我是XX派出所民警/巡特警"。', content:'主动出示人民警察证，口头告知身份。态度严肃但不失礼貌。', expandable:true },
      { num:2, title:'第二步：告知依据', color:'blue', lead:'告知盘查法律依据：《人民警察法》第九条+《居民身份证法》第十五条。', content:'告知盘查的法律依据。如被盘查人质疑，简要说明："根据《人民警察法》第九条和《居民身份证法》第十五条，公安机关有权对形迹可疑的人员进行盘查。"', expandable:true },
      { num:3, title:'第三步：查验身份信息', color:'blue', lead:'要求出示身份证件，核查是否为在逃人员、违法嫌疑人员。', content:'要求出示身份证件，通过警务通核查身份信息。如被盘查人未携带身份证，可通过姓名+身份证号或人脸识别等方式核验。', expandable:true },
      { num:4, title:'第四步：口头警告', color:'orange', lead:'如被盘查人不配合，先行口头警告，明确告知不配合的法律后果。', content:'警示用语："请您配合公安机关依法执行职务，否则将依法追究您的法律责任。"语气应当严肃但不粗暴。', expandable:true },
      { num:5, title:'第五步：口头传唤', color:'orange', lead:'口头警告无效的，依法口头传唤至公安机关继续盘查。', content:'口头传唤：告知因涉嫌XX行为，依法口头传唤至XX派出所继续盘查。告知传唤的法律依据和后果。', expandable:true },
      { num:6, title:'第六步：强制传唤', color:'red', lead:'拒不配合口头传唤的，依法强制传唤。使用最小武力，避免不必要伤害。', content:'强制传唤是最后手段。使用最小武力原则，多人协同控制，控制后立即上铐。传唤过程中注意保护被传唤人的合法权益，避免不必要的身体伤害。', expandable:true }
    ],
    prevId: 'jiating-baoli', nextId: 'keyi-cheliang'
  },
  {
    id: 'keyi-cheliang',
    title: '可疑车辆盘查',
    icon: '🚗',
    section: '盘查规范',
    desc: '车辆截停安全距离、人员分离、车辆搜查要点',
    tags: ['车辆盘查', '安全距离', '人员分离'],
    flow: '📋 5步：观察跟踪 → 截停 → 人员分离 → 盘问 → 车辆检查',
    quickCard: {
      title: '可疑车辆盘查',
      tags: ['车辆盘查', '安全距离', '人员分离'],
      flow: '📋 5步：观察跟踪 → 截停 → 人员分离 → 盘问 → 车辆检查'
    },
    steps: [
      { num:1, title:'观察跟踪', color:'blue', lead:'发现可疑车辆后不宜直接拦截，应跟踪观察并呼叫增援，记录车辆特征和行驶方向。', content:'发现可疑车辆后不宜直接闪灯鸣笛拦截。先跟踪观察，记录车辆特征（车牌、型号、颜色）和行驶方向，同时呼叫增援和请求核查车辆信息。', expandable:true },
      { num:2, title:'截停', color:'orange', lead:'选择安全路段截停，警车停在可疑车辆左后方约1.5-2个车身距离。', content:'选择车流量小、视野开阔的路段截停。警车停在可疑车辆左后方约1.5-2个车身距离处。截停后不下车，先观察车内人员动态。夜间使用警车探照灯照亮目标车辆。', expandable:true },
      { num:3, title:'人员分离', color:'red', lead:'先令驾驶员下车，带至警车后方隔离。再分别令其他乘员逐一接受检查。', content:'令驾驶员先下车，民警不下车，用警车扩音器发出指令。驾驶员下车后令其高举双手、背对民警后退至警车后方。由一名队员控制驾驶员，再令其他乘员逐一接受检查。', expandable:true },
      { num:4, title:'盘问', color:'blue', lead:'查验驾驶证、行驶证、身份证。核实车辆来源和行程目的。', content:'查验三证（驾驶证、行驶证、身份证），通过警务通核查。询问车辆来源、行程目的、乘车人关系等。注意观察回答是否矛盾、神态是否异常。', expandable:true },
      { num:5, title:'车辆检查', color:'orange', lead:'注意车内是否有违禁品、管制物品、隐匿人员。', content:'检查车内是否有违禁品（毒品、枪支、管制刀具）、隐匿人员（后座下方、后备箱）。检查后备箱前先令驾驶员自行打开，不代为操作。发现违禁品立即控制所有人员。', expandable:true }
    ],
    prevId: 'renyuan-pancha', nextId: 'chidao-jingqing'
  },
  {
    id: 'chidao-jingqing',
    title: '持刀警情（快反）',
    icon: '⚡',
    section: '快反处置',
    desc: '135快速反应持刀警情处置要点',
    tags: ['135快反', '持刀警情', '快速处置'],
    flow: '📋 135：1分钟响应 → 3分钟到场 → 5分钟处置',
    quickCard: {
      title: '持刀警情（快反）',
      tags: ['135快反', '持刀警情', '快速处置'],
      flow: '📋 135：1分钟响应 → 3分钟到场 → 5分钟处置'
    },
    steps: [
      { num:1, title:'1分钟响应', color:'red', lead:'接到持刀警情指令后1分钟内完成装备检查并出发。优先携带盾牌、钢叉、警棍。', content:'接到指令后1分钟内：\n· 确认警情地点和基本情况\n· 检查装备：盾牌、钢叉（抓捕叉）、伸缩警棍、催泪喷射器、执法记录仪\n· 确认防刺背心穿着\n· 出发，并持续接收指挥中心最新信息', expandable:true },
      { num:2, title:'3分钟到场', color:'orange', lead:'3分钟内到达现场。途中制定初步战术：谁持盾、谁持叉、谁主控。', content:'3分钟内到达现场。途中制定初步战术分工：明确盾牌手、钢叉手、主控手角色。到达现场后迅速评估情况，确认嫌疑人位置和周围环境。', expandable:true },
      { num:3, title:'5分钟处置', color:'blue', lead:'到场后5分钟内完成疏散、控制、上铐、带离。以最快速度消除危险。', content:'到场后5分钟内完成：\n· 疏散围观群众\n· 盾棍叉协同推进控制嫌疑人\n· 控制后上铐搜身\n· 带离现场\n· 汇报指挥中心处置结果\n\n核心原则：以最快速度消除危险，不拖延、不犹豫。', expandable:true }
    ],
    prevId: 'keyi-cheliang', nextId: 'jizhi-liucheng'
  },
  {
    id: 'jizhi-liucheng',
    title: '快反机制流程',
    icon: '🔁',
    section: '快反处置',
    desc: '135快速反应机制启动与执行流程',
    tags: ['135快反', '机制流程', '指挥协同'],
    flow: '📋 接警 → 派警 → 响应 → 到场 → 处置 → 汇报',
    quickCard: {
      title: '快反机制流程',
      tags: ['135快反', '机制流程', '指挥协同'],
      flow: '📋 接警 → 派警 → 响应 → 到场 → 处置 → 汇报'
    },
    steps: [
      { num:1, title:'接警与派警', color:'blue', lead:'指挥中心接警后30秒内完成警情等级判定，属于暴力警情的立即启动快反机制。', content:'指挥中心接警后30秒内完成：\n· 警情等级判定（暴力警情启动一级响应）\n· 确认事发地点和警情类型\n· 同步推送至最近快反小组\n· 通报警情关键信息（人数、武器、危险程度）', expandable:true },
      { num:2, title:'响应与出发', color:'orange', lead:'快反小组收到指令后1分钟内完成装备检查和人员分工并出发。', content:'快反小组收到指令后1分钟内：\n· 确认警情信息\n· 明确人员分工（指挥、盾牌、钢叉、警戒）\n· 检查装备完整性\n· 出发前往现场，途中保持与指挥中心通信', expandable:true },
      { num:3, title:'到场评估', color:'red', lead:'到场后快速评估：嫌疑人位置/人数/武器 → 环境风险 → 围观群众 → 最优处置方案。', content:'到场后30秒内完成快速评估：\n· 嫌疑人：位置、人数、持有的武器类型\n· 环境：室内/室外、有无可利用的掩体、有无危险物品\n· 群众：围观人数、有无受伤者\n· 方案：根据评估结果选择最优处置战术', expandable:true },
      { num:4, title:'处置与汇报', color:'blue', lead:'按预案实施处置，处置完成后及时向指挥中心汇报结果。', content:'按预案实施处置，处置完成后：\n· 向指挥中心汇报处置结果\n· 确认执法记录仪保存\n· 移交嫌疑人\n· 恢复巡逻勤务\n· 24小时内完成处置报告', expandable:true }
    ],
    prevId: 'chidao-jingqing', nextId: null
  }
];
```

- [ ] **Step 3: 验证** — 确保两个 JS 文件的模块导出格式正确，数组包含所有文章

- [ ] **Step 4: 提交**

---

### Task 4: 创建装备模块 (列表页 + 详情页)

**Files:**
- Create: `miniprogram/pages/zhuangbei/index/index.wxml`
- Create: `miniprogram/pages/zhuangbei/index/index.wxss`
- Create: `miniprogram/pages/zhuangbei/index/index.js`
- Create: `miniprogram/pages/zhuangbei/index/index.json`
- Create: `miniprogram/pages/zhuangbei/detail/detail.wxml`
- Create: `miniprogram/pages/zhuangbei/detail/detail.wxss`
- Create: `miniprogram/pages/zhuangbei/detail/detail.js`
- Create: `miniprogram/pages/zhuangbei/detail/detail.json`

- [ ] **Step 1: zhuangbei/index/index.wxml**

```xml
<view class="search-bar">
  <input placeholder="🔍  搜索装备..." bindinput="onSearch"/>
</view>

<view class="page-container list-page">
  <view class="page-title">
    <view class="h1">🛡️ 装备介绍</view>
    <view class="meta">
      <view class="tag">7篇</view>
      <view class="tag">预计阅读：32分钟</view>
      <view class="tag">九小件</view>
      <view class="tag">使用规范</view>
    </view>
  </view>

  <view wx:for="{{sections}}" wx:key="*this">
    <view class="list-section-title">{{item.name}}</view>
    <navigator wx:for="{{item.items}}" wx:key="id"
      url="/pages/zhuangbei/detail/detail?id={{item.id}}"
      class="list-item">
      <view class="item-title">{{item.icon}} {{item.title}}</view>
      <view class="item-desc">{{item.desc}}</view>
    </navigator>
  </view>
</view>
```

- [ ] **Step 2: zhuangbei/index/index.wxss**

```css
@import '../../../../app.wxss';
```

- [ ] **Step 3: zhuangbei/index/index.js**

```javascript
var articles = require('../../../data/zhuangbei.js');

Page({
  data: { sections: [], allItems: [] },
  onLoad() {
    var sections = [];
    var seen = {};
    articles.forEach(function(a) {
      if (!seen[a.section]) {
        seen[a.section] = { name: a.section, items: [] };
        sections.push(seen[a.section]);
      }
      seen[a.section].items.push({ id: a.id, icon: a.icon, title: a.title, desc: a.desc });
    });
    this.setData({ sections: sections, allItems: articles });
  },
  onSearch(e) {
    var q = e.detail.value.toLowerCase().trim();
    var sections = [];
    var seen = {};
    var self = this;
    this.data.allItems.forEach(function(a) {
      if (q && (a.title + a.desc).toLowerCase().indexOf(q) === -1) return;
      if (!seen[a.section]) {
        seen[a.section] = { name: a.section, items: [] };
        sections.push(seen[a.section]);
      }
      seen[a.section].items.push({ id: a.id, icon: a.icon, title: a.title, desc: a.desc });
    });
    this.setData({ sections: sections });
  }
});
```

- [ ] **Step 4: zhuangbei/index/index.json**

```json
{ "usingComponents": {}, "navigationBarTitleText": "装备介绍" }
```

- [ ] **Step 5: zhuangbei/detail/detail.wxml**

```xml
<view class="breadcrumb">
  <navigator url="/pages/index/index" class="link">首页</navigator>
  <text> &gt; </text>
  <navigator url="/pages/zhuangbei/index/index" class="link">装备介绍</navigator>
  <text> &gt; </text>
  <text class="current">{{article.title}}</text>
</view>

<view class="page-container">
  <view class="page-title">
    <view class="h1">{{article.icon}} {{article.title}}</view>
    <view class="meta">
      <view class="tag risk-high" wx:for="{{article.tags}}" wx:key="*this">{{item}}</view>
    </view>
  </view>

  <view class="quick-card" wx:if="{{article.quickCard}}">
    <view class="quick-icon">{{article.icon}}</view>
    <view class="quick-body">
      <view class="h2">{{article.quickCard.title}}</view>
      <view class="quick-tags">
        <view class="tag risk-high" wx:for="{{article.quickCard.tags}}" wx:key="*this">{{item}}</view>
      </view>
      <view class="quick-flow">{{article.quickCard.flow}}</view>
    </view>
  </view>

  <view wx:for="{{article.steps}}" wx:key="num">
    <view class="step-card {{item.color}}">
      <view class="step-header">
        <view class="step-num">{{item.num}}</view>
        <view class="step-title">{{item.title}}</view>
      </view>
      <view class="step-lead">{{item.lead}}</view>
      <view class="step-media" wx:if="{{item.media}}">{{item.media.label}}</view>
      <view wx:if="{{item.expandable}}">
        <view class="expandable-full {{item._expanded ? 'open' : ''}}">
          <view class="step-text">
            <view class="p" wx:for="{{item._contentLines}}" wx:key="*this">{{item}}</view>
          </view>
        </view>
        <view class="expand-btn" data-index="{{index}}" bindtap="onExpand">{{item._expanded ? '▸ 收起' : '▸ ' + item._expandLabel}}</view>
      </view>
      <view wx:else>
        <view class="step-text">
          <view class="p" wx:for="{{item._contentLines}}" wx:key="*this">{{item}}</view>
        </view>
      </view>
    </view>
  </view>

  <view class="page-nav">
    <navigator wx:if="{{article.prevId}}" url="/pages/zhuangbei/detail/detail?id={{article.prevId}}" class="link">← {{prevTitle}}</navigator>
    <view wx:else></view>
    <navigator wx:if="{{article.nextId}}" url="/pages/zhuangbei/detail/detail?id={{article.nextId}}" class="link">{{nextTitle}} →</navigator>
    <view wx:else></view>
  </view>
</view>
```

- [ ] **Step 6: zhuangbei/detail/detail.wxss**

```css
@import '../../../../app.wxss';
```

- [ ] **Step 7: zhuangbei/detail/detail.js**

```javascript
var articles = require('../../../data/zhuangbei.js');

function findArticle(id) {
  for (var i = 0; i < articles.length; i++) {
    if (articles[i].id === id) return articles[i];
  }
  return null;
}

Page({
  data: { article: {}, prevTitle: '', nextTitle: '' },
  onLoad: function(opts) {
    var a = findArticle(opts.id);
    if (!a) { wx.showToast({ title: '文章未找到', icon: 'none' }); return; }

    var steps = (a.steps || []).map(function(s) {
      var lines = (s.content || '').split('\n').filter(function(l) { return l.trim(); });
      return Object.assign({}, s, {
        _expanded: false,
        _expandLabel: s.title || '展开详情',
        _contentLines: lines
      });
    });

    var prevTitle = '', nextTitle = '';
    if (a.prevId) { var p = findArticle(a.prevId); if (p) prevTitle = p.title; }
    if (a.nextId) { var n = findArticle(a.nextId); if (n) nextTitle = n.title; }

    this.setData({
      article: Object.assign({}, a, { steps: steps }),
      prevTitle: prevTitle,
      nextTitle: nextTitle
    });
  },
  onExpand: function(e) {
    var idx = e.currentTarget.dataset.index;
    var steps = this.data.article.steps;
    steps[idx]._expanded = !steps[idx]._expanded;
    this.setData({ 'article.steps': steps });
  }
});
```

- [ ] **Step 8: zhuangbei/detail/detail.json**

```json
{ "usingComponents": {}, "navigationBarTitleText": "装备详情" }
```

- [ ] **Step 9: 验证**

在开发者工具中：
1. 装备列表页 — 显示7篇文章，分组正确（核心装备6篇 + 规范用语1篇）
2. 搜索 "警棍" — 只显示伸缩警棍
3. 点击伸缩警棍 → 详情页渲染 7个步骤卡片 + 速览卡片
4. 折叠/展开按钮正常
5. 底部导航 "← 九小件概览 | 催泪喷射器 →"

- [ ] **Step 10: 提交**

---

### Task 5: 创建警情模块 (列表页 + 详情页)

**Files:**
- Create: `miniprogram/pages/jingqing/index/index.wxml`
- Create: `miniprogram/pages/jingqing/index/index.wxss`
- Create: `miniprogram/pages/jingqing/index/index.js`
- Create: `miniprogram/pages/jingqing/index/index.json`
- Create: `miniprogram/pages/jingqing/detail/detail.wxml`
- Create: `miniprogram/pages/jingqing/detail/detail.wxss`
- Create: `miniprogram/pages/jingqing/detail/detail.js`
- Create: `miniprogram/pages/jingqing/detail/detail.json`

警情模块结构与装备模块相同，只需替换数据源和标题。

- [ ] **Step 1: jingqing/index/index.wxml** — 同 zhuangbei/index/index.wxml，标题改为 "🚨 警情处置"，tag 改为 "8篇" / "预计阅读：28分钟" / "常见街面警情" / "分步处置流程"

- [ ] **Step 2: jingqing/index/index.js** — 同 zhuangbei/index/index.js，require 改为 `'../../../data/jingqing.js'`

- [ ] **Step 3: jingqing/detail/detail.wxml** — 同 zhuangbei/detail/detail.wxml，面包屑中 "装备介绍" 改为 "警情处置"，链接改为 `/pages/jingqing/index/index`

- [ ] **Step 4: jingqing/detail/detail.js** — 同 zhuangbei/detail/detail.js，require 改为 `'../../../data/jingqing.js'`，detail url 中的 zhuangbei 改为 jingqing

- [ ] **Step 5: jingqing/detail/detail.json** — navigationBarTitleText 改为 "警情详情"

- [ ] **Step 6: 验证** — 列表页显示8篇文章，搜索过滤正常，详情页正常渲染步骤卡片

- [ ] **Step 7: 提交**

---

### Task 6: 创建首页 (模块卡片 + 每日一学)

**Files:**
- Create: `miniprogram/pages/index/index.wxml`
- Create: `miniprogram/pages/index/index.wxss`
- Create: `miniprogram/pages/index/index.js`
- Create: `miniprogram/pages/index/index.json`

- [ ] **Step 1: index/index.wxml**

```xml
<view class="search-bar">
  <input placeholder="🔍  搜索警情、装备、法规..." bindinput="onSearch"/>
</view>

<view class="card-grid">
  <navigator url="/pages/zhuangbei/index/index" class="module-card blue" wx:if="{{show.zhuangbei}}">
    <view class="icon">🛡️</view>
    <view class="name">装备介绍</view>
    <view class="count">7篇</view>
    <view class="desc">单警装备使用规范</view>
    <view class="hot-links">伸缩警棍 · 催泪喷射器 · 手铐 · 执法记录仪</view>
  </navigator>
  <navigator url="/pages/qinwu/index/index" class="module-card green" wx:if="{{show.qinwu}}">
    <view class="icon">📋</view>
    <view class="name">巡防勤务</view>
    <view class="count">8篇</view>
    <view class="desc">每日勤务与任务规范</view>
    <view class="hot-links">大型活动安保 · 群体事件处置 · 舆情导控</view>
  </navigator>
  <navigator url="/pages/xunlian/index/index" class="module-card purple" wx:if="{{show.xunlian}}">
    <view class="icon">⚔️</view>
    <view class="name">警务训练</view>
    <view class="count">19篇</view>
    <view class="desc">徒手 · 警械 · 战术 · 快反</view>
    <view class="hot-links">盾牌技术 · 盘查流程 · 武力升级 · 搜身带离</view>
  </navigator>
  <navigator url="/pages/jingqing/index/index" class="module-card red" wx:if="{{show.jingqing}}">
    <view class="icon">🚨</view>
    <view class="name">警情处置</view>
    <view class="count">8篇</view>
    <view class="desc">常见警情处置流程</view>
    <view class="hot-links">持刀警情 · 醉酒闹事 · 打架斗殴 · 家庭暴力</view>
  </navigator>
  <navigator url="/pages/fagui/index/index" class="module-card red" wx:if="{{show.fagui}}">
    <view class="icon">📕</view>
    <view class="name">法条规范</view>
    <view class="count">6篇</view>
    <view class="desc">执法依据速查</view>
    <view class="hot-links">治安规范 · 赌博执法 · 法律依据 · 法言法语</view>
  </navigator>
  <navigator url="/pages/zoufang/index/index" class="module-card teal" wx:if="{{show.zoufang}}">
    <view class="icon">🏫</view>
    <view class="name">走访送教</view>
    <view class="count">6篇</view>
    <view class="desc">校园社区送教服务</view>
    <view class="hot-links">校园反恐 · 现场处置 · 金融反恐 · 校园培训</view>
  </navigator>
</view>

<view class="daily-section">
  <view class="daily-card">
    <view class="daily-header">
      <view class="daily-label">每日一学</view>
      <view class="daily-date">{{daily.date}}</view>
    </view>
    <view class="daily-case-title">{{daily.title}}</view>
    <view class="daily-case-body">{{daily.body}}</view>
    <view class="daily-tips">
      <view class="tips-title">💡 处置要点</view>
      <view class="tip" wx:for="{{daily.tips}}" wx:key="*this">· {{item}}</view>
    </view>
    <view class="daily-nav">
      <button bindtap="onPrev">◁ 上一篇</button>
      <view class="daily-counter">{{dailyIdx + 1}} / {{dailyTotal}}</view>
      <button bindtap="onNext">下一篇 ▷</button>
    </view>
  </view>
</view>
```

- [ ] **Step 2: index/index.wxss**

```css
@import '../../../app.wxss';
```

- [ ] **Step 3: index/index.js**

```javascript
var dailyCases = [
  {
    date: '2026-06-29',
    title: '「醉酒闹事处置」',
    body: '某日晚间，巡逻组接报一男子在烧烤摊酒后闹事，持酒瓶威胁周围群众。民警到场后先疏散围观人员，保持安全距离，语言安抚稳定情绪。待嫌疑人情绪松懈、放下酒瓶点烟时，盾牌手在前、抓捕手从侧翼突入，三人协同控制上铐。全程执法记录仪开启，事后向指挥中心报备。',
    tips: [
      '先疏散围观群众，避免人群刺激嫌疑人情绪',
      '保持安全距离≥2米，语言安抚为主，不单独近身',
      '盾牌在前，抓捕手侧翼，一人外围警戒',
      '抓住嫌疑人松懈瞬间，三人同时行动，一招制敌'
    ]
  },
  {
    date: '2026-06-28',
    title: '「伸缩警棍使用」',
    body: '巡逻组接到家暴警情，到场时一名男子情绪激动持木凳挥舞。民警口头警告无效后，盾牌手建立安全屏障，持棍手从侧翼以肩上戒备接近。男子冲向盾牌时，持棍手趁其注意力被吸引，以劈击技术击中其大腿外侧肌肉群使其失去锐气，随即三人协同上铐。',
    tips: [
      '使用前必须口头警告，给对象反应时间',
      '击打部位锁定大肌肉群，严禁打Head/胫骨/裆部',
      '使用后立即检查对象伤情，以制止为限度',
      '使用后记录并汇报，做处置情况说明'
    ]
  },
  {
    date: '2026-06-27',
    title: '「催泪喷射器实战应用」',
    body: '接报公园内一名疑似吸毒人员情绪亢奋失控。民警到场后发现对象处于精神亢奋状态，体壮力大。盾牌手维持安全距离，持喷射器民警顺风站位，发出标准警告，对象无视继续前进，民警以点射方式（每次≤1秒）对准面部喷射，喷射后立即侧移换位，对象捂脸伏地，随即上铐并告知善后措施。',
    tips: [
      '使用前检查风向：逆风不得使用，选择上风口站位',
      '每次点射不超过1秒，点射后立即移动位置',
      '控制后及时净化处理：清水冲洗，不要揉擦',
      '呼叫120到场评估，确认对象身体状况'
    ]
  }
];

Page({
  data: {
    show: { zhuangbei: true, qinwu: true, xunlian: true, jingqing: true, fagui: true, zoufang: true },
    daily: dailyCases[0],
    dailyIdx: 0,
    dailyTotal: dailyCases.length
  },
  onSearch(e) {
    var q = e.detail.value.toLowerCase().trim();
    if (!q) {
      this.setData({ show: { zhuangbei: true, qinwu: true, xunlian: true, jingqing: true, fagui: true, zoufang: true } });
      return;
    }
    var show = { zhuangbei: false, qinwu: false, xunlian: false, jingqing: false, fagui: false, zoufang: false };
    var cards = [
      { key: 'zhuangbei', text: '装备介绍 单警装备使用规范 伸缩警棍 催泪喷射器 手铐 执法记录仪' },
      { key: 'qinwu', text: '巡防勤务 每日勤务与任务规范 大型活动安保 群体事件处置 舆情导控' },
      { key: 'xunlian', text: '警务训练 徒手 警械 战术 快反 盾牌技术 盘查流程 武力升级 搜身带离' },
      { key: 'jingqing', text: '警情处置 常见警情处置流程 持刀警情 醉酒闹事 打架斗殴 家庭暴力' },
      { key: 'fagui', text: '法条规范 执法依据速查 治安规范 赌博执法 法律依据 法言法语' },
      { key: 'zoufang', text: '走访送教 校园社区送教服务 校园反恐 现场处置 金融反恐 校园培训' }
    ];
    cards.forEach(function(c) { if (c.text.indexOf(q) !== -1) show[c.key] = true; });
    this.setData({ show: show });
  },
  onPrev() { var i = this.data.dailyIdx; i = i > 0 ? i - 1 : dailyCases.length - 1; this.setData({ daily: dailyCases[i], dailyIdx: i }); },
  onNext() { var i = this.data.dailyIdx; i = i < dailyCases.length - 1 ? i + 1 : 0; this.setData({ daily: dailyCases[i], dailyIdx: i }); }
});
```

- [ ] **Step 4: index/index.json**

```json
{ "usingComponents": {}, "navigationBarTitleText": "巡防百科" }
```

- [ ] **Step 5: 验证** — 首页显示6个模块卡片 + 每日一学，搜索过滤正常，轮播翻页正常

- [ ] **Step 6: 提交**

---

### Task 7: 创建更多页 + 占位页面

**Files:**
- Create: `miniprogram/pages/more/more.wxml`
- Create: `miniprogram/pages/more/more.wxss`
- Create: `miniprogram/pages/more/more.js`
- Create: `miniprogram/pages/more/more.json`
- Create: `miniprogram/pages/qinwu/index/index.wxml`
- Create: `miniprogram/pages/qinwu/index/index.wxss`
- Create: `miniprogram/pages/qinwu/index/index.js`
- Create: `miniprogram/pages/qinwu/index/index.json`
- Create: `miniprogram/pages/xunlian/index/index.wxml`
- Create: `miniprogram/pages/xunlian/index/index.wxss`
- Create: `miniprogram/pages/xunlian/index/index.js`
- Create: `miniprogram/pages/xunlian/index/index.json`

- [ ] **Step 1: more/more.wxml**

```xml
<view class="page-container">
  <view class="page-title">
    <view class="h1">📂 更多内容</view>
  </view>

  <navigator url="/pages/fagui/index/index" class="list-item">
    <view class="item-title">📕 法条规范</view>
    <view class="item-desc">执法依据速查 · 6篇</view>
  </navigator>
  <navigator url="/pages/zoufang/index/index" class="list-item">
    <view class="item-title">🏫 走访送教</view>
    <view class="item-desc">校园社区送教服务 · 6篇</view>
  </navigator>

  <view style="margin-top:32px; text-align:center; font-size:13px; color:var(--text-muted);">
    🛡️ 巡防百科 — 常州巡特警
  </view>
</view>
```

- [ ] **Step 2: more/more.js**

```javascript
Page({});
```

- [ ] **Step 3: more/more.json**

```json
{ "usingComponents": {}, "navigationBarTitleText": "更多" }
```

- [ ] **Step 4: 占位页面 qinwu/index/index.wxml**

```xml
<view class="placeholder-page">
  <view class="icon">📋</view>
  <view class="text">巡防勤务 — 即将上线</view>
</view>
```

- [ ] **Step 5: 占位页面 xunlian/index/index.wxml**

```xml
<view class="placeholder-page">
  <view class="icon">⚔️</view>
  <view class="text">警务训练 — 即将上线</view>
</view>
```

- [ ] **Step 6: 每个占位页面的 .js** — `Page({});`  
- [ ] **Step 7: 每个占位页面的 .json** — `{ "usingComponents": {}, "navigationBarTitleText": "..." }`（勤务/训练）  
- [ ] **Step 8: 每个占位页面的 .wxss** — `@import '../../../app.wxss';`

- [ ] **Step 9: 验证** — 点击 tabBar 勤务/训练 显示占位文字，更多页面显示法条/走访入口

- [ ] **Step 10: 提交**

---

### Task 8: 集成验证

- [ ] **Step 1: 密码守卫**

```
1. 清除 storage → 编译运行
2. 应自动进入 auth 登录页
3. 输入 wrf150225 → 进入 tabBar 首页（装备列表）
4. 关闭再打开 → 直接进入（storage 已保存）
```

- [ ] **Step 2: tabBar 导航**

```
1. 底部5个 tab 正常切换：装备 | 勤务(占位) | 训练(占位) | 警情 | 更多
2. 从首页进入详情页再返回，页面栈正常
3. 从详情页点击 prev/next 导航可顺序浏览
```

- [ ] **Step 3: 搜索 + 折叠**

```
1. 装备列表页搜索 "警棍" → 只显示伸缩警棍
2. 详情页点击 "展开详情" → 内容展开，按钮变为 "收起"
3. 再次点击 → 内容收起
```

- [ ] **Step 4: 每日一学**

```
1. 首页底部显示每日一学卡片
2. "下一篇" → 切换到下一篇案例
3. "上一篇" → 循环
```

- [ ] **Step 5: 提交**

```bash
git add -A && git commit -m "feat: 小程序MVP集成 — 装备+警情模块，密码守卫，每日一学" && git push
```
