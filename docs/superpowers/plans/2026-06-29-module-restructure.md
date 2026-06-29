# 网站模块重组 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将全站从11模块重组为6大模块，涉及文件迁移、导航重写、索引重建、面包屑链接更新

**Architecture:** 纯文件系统操作 + 文本替换。删除 shoushe/ 和 8 个旧目录，新建 qinwu/xunlian/zoufang 3 个目录，逐页迁移约 40 个 HTML 文件，更新每个迁移页面的面包屑和相对链接，重写 nav.js 和首页

**Tech Stack:** 纯静态 HTML/CSS/JS，零框架依赖

**Spec:** `docs/superpowers/specs/2026-06-29-module-restructure-design.md`

---

### Task 1: 删除手枪射击模块

**Files:**
- Delete: `shoushe/` 整个目录及所有文件

- [ ] **Step 1: 删除 shoushe 目录**

```bash
cd "F:/frank第二大脑/xunfang-baike"
rm -rf shoushe/
```

- [ ] **Step 2: 提交**

```bash
git add -A
git commit -m "$(cat <<'EOF'
feat: 删除手枪射击模块 (shoushe/) — 模块重组第一步
EOF
)"
```

---

### Task 2: 新建目录和模块索引页

**Files:**
- Create: `qinwu/index.html`, `xunlian/index.html`, `zoufang/index.html`

- [ ] **Step 1: 创建空目录**

```bash
cd "F:/frank第二大脑/xunfang-baike"
mkdir -p qinwu xunlian zoufang
```

- [ ] **Step 2: 创建巡防勤务索引页 `qinwu/index.html`**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>巡防勤务 — 巡防百科</title>
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<div id="nav-placeholder"></div>

<div class="breadcrumb">
  <a href="../index.html">首页</a> &gt;
  <span class="current">巡防勤务</span>
</div>

<div class="page-container list-page">
  <div class="page-title">
    <h1>📋 巡防勤务</h1>
    <div class="meta">
      <span class="tag">8篇</span>
      <span class="tag">每日勤务 · 大型活动 · 群体事件</span>
    </div>
  </div>

  <div class="list-section-title">大型活动安保</div>
  <a href="yanchanghui-zhifa.html" class="list-item">
    <div class="item-title">🎤 演唱会执法</div>
    <div class="item-desc">大型演出活动的执法要点与注意事项</div>
  </a>
  <a href="xiaoyuan-jinrong.html" class="list-item">
    <div class="item-title">🏫 校园金融安全</div>
    <div class="item-desc">校园金融风险防范与处置</div>
  </a>
  <a href="yuqing-zhanshu.html" class="list-item">
    <div class="item-title">📱 舆情战术</div>
    <div class="item-desc">大型活动中的舆情监控与引导</div>
  </a>

  <div class="list-section-title">群体事件处置</div>
  <a href="chuzhi-yuan.html" class="list-item">
    <div class="item-title">📋 群体事件处置预案</div>
    <div class="item-desc">处置预案制定与启动流程</div>
  </a>
  <a href="kongzhi-daili.html" class="list-item">
    <div class="item-title">👥 控制带离</div>
    <div class="item-desc">群体事件中的控制与带离技术</div>
  </a>
  <a href="shewen-yanlian.html" class="list-item">
    <div class="item-title">🎯 涉稳演练</div>
    <div class="item-desc">涉稳突发事件应急演练方案</div>
  </a>
  <a href="xuanchuan-quzheng.html" class="list-item">
    <div class="item-title">📸 宣传取证</div>
    <div class="item-desc">群体事件中的宣传引导与证据固定</div>
  </a>
  <a href="yuqing-daokong.html" class="list-item">
    <div class="item-title">📱 舆情导控</div>
    <div class="item-desc">群体性事件舆情导控策略</div>
  </a>
</div>

<script src="../js/nav.js"></script>
<script src="../js/main.js"></script>
</body>
</html>
```

- [ ] **Step 3: 创建警务训练索引页 `xunlian/index.html`**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>警务训练 — 巡防百科</title>
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<div id="nav-placeholder"></div>

<div class="breadcrumb">
  <a href="../index.html">首页</a> &gt;
  <span class="current">警务训练</span>
</div>

<div class="page-container list-page">
  <div class="page-title">
    <h1>⚔️ 警务训练</h1>
    <div class="meta">
      <span class="tag">19篇</span>
      <span class="tag">徒手 · 警械 · 战术 · 射击</span>
    </div>
  </div>

  <div class="list-section-title">徒手防卫与控制</div>
  <a href="jietuo-fangyu.html" class="list-item">
    <div class="item-title">🤼 解脱防卫</div>
    <div class="item-desc">被抓握时的解脱技术与防卫反击</div>
  </a>
  <a href="kongzhi-jishu.html" class="list-item">
    <div class="item-title">✋ 控制技术</div>
    <div class="item-desc">关节控制与压点控制技术</div>
  </a>
  <a href="soushen-daili.html" class="list-item">
    <div class="item-title">🔍 搜身带离</div>
    <div class="item-desc">搜查技术与安全带离流程</div>
  </a>

  <div class="list-section-title">最小作战单元</div>
  <a href="gaishu-biancheng.html" class="list-item">
    <div class="item-title">📖 最小作战单元概述</div>
    <div class="item-desc">作战单元编成与职能分工</div>
  </a>
  <a href="dunpai-jishu.html" class="list-item">
    <div class="item-title">🛡️ 盾牌技术</div>
    <div class="item-desc">防暴盾牌持握与推进技术</div>
  </a>
  <a href="duncha-xietong.html" class="list-item">
    <div class="item-title">⚔️ 盾叉协同</div>
    <div class="item-desc">盾牌与抓捕叉协同作战技术</div>
  </a>
  <a href="jinggun-zhuabucha.html" class="list-item">
    <div class="item-title">🏏 警棍抓捕叉</div>
    <div class="item-desc">警棍与抓捕叉组合应用</div>
  </a>
  <a href="wuli-shengji-sanfang.html" class="list-item">
    <div class="item-title">⚡ 武力升级三防</div>
    <div class="item-desc">武力层级判断与三防原则</div>
  </a>
  <a href="zhanshu-zhanwei.html" class="list-item">
    <div class="item-title">📍 战术站位</div>
    <div class="item-desc">作战单元中各位置的分工站位</div>
  </a>
  <a href="zhudong-hengyi.html" class="list-item">
    <div class="item-title">💪 主动恒义</div>
    <div class="item-desc">主动防御与持续压制战术</div>
  </a>
  <a href="xunlian-jiaoxuefa.html" class="list-item">
    <div class="item-title">📝 训练教学法</div>
    <div class="item-desc">警务实战训练的组织与教学方法</div>
  </a>

  <div class="list-section-title">巡逻盘查技能</div>
  <a href="pancha-liucheng.html" class="list-item">
    <div class="item-title">🔍 盘查流程</div>
    <div class="item-desc">巡逻盘查六步法标准化流程</div>
  </a>
  <a href="zhanshu-zhanwei-xunluo.html" class="list-item">
    <div class="item-title">📍 战术站位（巡逻）</div>
    <div class="item-desc">盘查时的安全站位与队形</div>
  </a>
  <a href="shizi-fangyu.html" class="list-item">
    <div class="item-title">✚ 十字防御</div>
    <div class="item-desc">十字防御队形与协同保护</div>
  </a>
  <a href="xidu-pancha.html" class="list-item">
    <div class="item-title">💊 吸毒盘查</div>
    <div class="item-desc">吸毒人员识别与盘查要点</div>
  </a>

  <div class="list-section-title">快反技能</div>
  <a href="duncha-zhanzhu.html" class="list-item">
    <div class="item-title">⚡ 盾叉站住</div>
    <div class="item-desc">快速反应中的盾叉战术站位</div>
  </a>
  <a href="sinengli-yaosu.html" class="list-item">
    <div class="item-title">🎯 四能力要素</div>
    <div class="item-desc">快反处置四大核心能力训练</div>
  </a>

  <div class="list-section-title">反恐基础理论</div>
  <a href="gaishu-yuanze.html" class="list-item">
    <div class="item-title">📖 反恐概述原则</div>
    <div class="item-desc">反恐防暴基本理论与处置原则</div>
  </a>
  <a href="wuli-shengji.html" class="list-item">
    <div class="item-title">⚡ 武力升级</div>
    <div class="item-desc">武力升级原则与判断标准</div>
  </a>
</div>

<script src="../js/nav.js"></script>
<script src="../js/main.js"></script>
</body>
</html>
```

- [ ] **Step 4: 创建走访送教索引页 `zoufang/index.html`**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>走访送教 — 巡防百科</title>
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<div id="nav-placeholder"></div>

<div class="breadcrumb">
  <a href="../index.html">首页</a> &gt;
  <span class="current">走访送教</span>
</div>

<div class="page-container list-page">
  <div class="page-title">
    <h1>🏫 走访送教</h1>
    <div class="meta">
      <span class="tag">6篇</span>
      <span class="tag">校园安全 · 社区送教 · 场景处置</span>
    </div>
  </div>

  <div class="list-section-title">场景处置</div>
  <a href="xianchang-chuzhi.html" class="list-item">
    <div class="item-title">🚨 现场处置</div>
    <div class="item-desc">反恐防暴现场应急处置流程</div>
  </a>
  <a href="xiaoyuan-fankong.html" class="list-item">
    <div class="item-title">🏫 校园反恐</div>
    <div class="item-desc">校园反恐防暴专项预案</div>
  </a>
  <a href="jinrong-fankong.html" class="list-item">
    <div class="item-title">🏦 金融反恐</div>
    <div class="item-desc">金融网点反恐防范要点</div>
  </a>
  <a href="zhengzhi-hexinqu.html" class="list-item">
    <div class="item-title">🏛️ 政治核心区</div>
    <div class="item-desc">政治核心区域安全防范</div>
  </a>
  <a href="daxing-huodong.html" class="list-item">
    <div class="item-title">🎪 大型活动安全</div>
    <div class="item-desc">大型活动反恐安保方案</div>
  </a>

  <div class="list-section-title">校园送教</div>
  <a href="xiaoyuan-peixun.html" class="list-item">
    <div class="item-title">📚 校园培训</div>
    <div class="item-desc">校园安保力量培训与应急演练</div>
  </a>
</div>

<script src="../js/nav.js"></script>
<script src="../js/main.js"></script>
</body>
</html>
```

- [ ] **Step 5: 提交**

```bash
git add -A
git commit -m "$(cat <<'EOF'
feat: 新建 qinwu/xunlian/zoufang 目录及模块索引页
EOF
)"
```

---

### Task 3: 迁移文件到各模块目录

**Files:**
- Move: ~40 个 HTML 文件从旧目录到新目录

- [ ] **Step 1: 迁移巡防勤务文件 (qinwu/)**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 从大型活动安保迁入
mv daxing-anbao/yanchanghui-zhifa.html qinwu/
mv daxing-anbao/xiaoyuan-jinrong.html qinwu/
mv daxing-anbao/yuqing-zhanshu.html qinwu/
# 从群体事件处置迁入
mv qunti-shijian/chuzhi-yuan.html qinwu/
mv qunti-shijian/kongzhi-daili.html qinwu/
mv qunti-shijian/shewen-yanlian.html qinwu/
mv qunti-shijian/xuanchuan-quzheng.html qinwu/
mv qunti-shijian/yuqing-daokong.html qinwu/
```

- [ ] **Step 2: 迁移警务训练文件 (xunlian/)**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 从徒手防卫迁入（技能3页，概念法律已归法条规范）
mv tushou/jietuo-fangyu.html xunlian/
mv tushou/kongzhi-jishu.html xunlian/
mv tushou/soushen-daili.html xunlian/
# 从最小作战单元迁入（技能8页，法言法语已归法条规范）
mv zuozhan-danyuan/dunpai-jishu.html xunlian/
mv zuozhan-danyuan/duncha-xietong.html xunlian/
mv zuozhan-danyuan/gaishu-biancheng.html xunlian/
mv zuozhan-danyuan/jinggun-zhuabucha.html xunlian/
mv zuozhan-danyuan/wuli-shengji-sanfang.html xunlian/
mv zuozhan-danyuan/xunlian-jiaoxuefa.html xunlian/
mv zuozhan-danyuan/zhanshu-zhanwei.html xunlian/
mv zuozhan-danyuan/zhudong-hengyi.html xunlian/
# 从巡逻规范迁入（技能4页，法律依据已归法条规范）
mv xunluo/pancha-liucheng.html xunlian/
mv xunluo/shizi-fangyu.html xunlian/
mv xunluo/xidu-pancha.html xunlian/
mv xunluo/zhanshu-zhanwei.html xunlian/zhanshu-zhanwei-xunluo.html
# 从快反处置迁入（技能2页）
mv kuaifan/duncha-zhanzhu.html xunlian/
mv kuaifan/sinengli-yaosu.html xunlian/
# 从反恐防暴迁入（基础理论2页）
mv fankong/gaishu-yuanze.html xunlian/
mv fankong/wuli-shengji.html xunlian/
```

- [ ] **Step 3: 迁移警情处置文件 (jingqing/)**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 从快反处置迁入（警情类2页）
mv kuaifan/chidao-jingqing.html jingqing/
mv kuaifan/jizhi-liucheng.html jingqing/
```

- [ ] **Step 4: 迁移法条规范文件 (fagui/)**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 从巡逻规范迁入
mv xunluo/faly-yiju.html fagui/
# 从徒手防卫迁入
mv tushou/gainian-falv.html fagui/
# 从最小作战单元迁入
mv zuozhan-danyuan/faly-fayanfayu.html fagui/
```

- [ ] **Step 5: 迁移走访送教文件 (zoufang/)**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 从反恐防暴迁入（场景处置5页）
mv fankong/xianchang-chuzhi.html zoufang/
mv fankong/xiaoyuan-fankong.html zoufang/
mv fankong/jinrong-fankong.html zoufang/
mv fankong/zhengzhi-hexinqu.html zoufang/
mv fankong/daxing-huodong.html zoufang/
# 从快反处置迁入（校园培训1页）
mv kuaifan/xiaoyuan-peixun.html zoufang/
```

- [ ] **Step 6: 提交**

```bash
git add -A
git commit -m "$(cat <<'EOF'
feat: 按新模块方案迁移全部详情页
EOF
)"
```

---

### Task 4: 更新所有迁移页面中的面包屑和链接

**Files:**
- Modify: `qinwu/*.html` (8), `xunlian/*.html` (19), `jingqing/*.html` (2新增), `fagui/*.html` (3新增), `zoufang/*.html` (6)

所有迁移页面的面包屑格式统一为 `<a href="../index.html">首页</a> &gt; <a href="index.html">新模块名</a> &gt; <span class="current">...</span>`，需将旧模块名替换为新模块名。

- [ ] **Step 1: qinwu/ — 替换「大型活动安保」→「巡防勤务」(3个文件)**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 3个来自 daxing-anbao 的文件
sed -i 's|<a href="index.html">大型活动安保</a>|<a href="index.html">巡防勤务</a>|g' qinwu/yanchanghui-zhifa.html qinwu/xiaoyuan-jinrong.html qinwu/yuqing-zhanshu.html
# 5个来自 qunti-shijian 的文件
sed -i 's|<a href="index.html">群体事件处置</a>|<a href="index.html">巡防勤务</a>|g' qinwu/chuzhi-yuan.html qinwu/kongzhi-daili.html qinwu/shewen-yanlian.html qinwu/xuanchuan-quzheng.html qinwu/yuqing-daokong.html
```

- [ ] **Step 2: xunlian/ — 替换5种旧模块名 →「警务训练」(19个文件)**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 来自 tushou 的3个
sed -i 's|<a href="index.html">徒手防卫</a>|<a href="index.html">警务训练</a>|g' xunlian/jietuo-fangyu.html xunlian/kongzhi-jishu.html xunlian/soushen-daili.html
# 来自 zuozhan-danyuan 的8个
sed -i 's|<a href="index.html">最小作战单元</a>|<a href="index.html">警务训练</a>|g' xunlian/dunpai-jishu.html xunlian/duncha-xietong.html xunlian/gaishu-biancheng.html xunlian/jinggun-zhuabucha.html xunlian/wuli-shengji-sanfang.html xunlian/xunlian-jiaoxuefa.html xunlian/zhanshu-zhanwei.html xunlian/zhudong-hengyi.html
# 来自 xunluo 的4个（含重命名的 zhanshu-zhanwei-xunluo.html）
sed -i 's|<a href="index.html">巡逻规范</a>|<a href="index.html">警务训练</a>|g' xunlian/pancha-liucheng.html xunlian/shizi-fangyu.html xunlian/xidu-pancha.html xunlian/zhanshu-zhanwei-xunluo.html
# 来自 kuaifan 的2个
sed -i 's|<a href="index.html">快反处置</a>|<a href="index.html">警务训练</a>|g' xunlian/duncha-zhanzhu.html xunlian/sinengli-yaosu.html
# 来自 fankong 的2个
sed -i 's|<a href="index.html">反恐防暴</a>|<a href="index.html">警务训练</a>|g' xunlian/gaishu-yuanze.html xunlian/wuli-shengji.html
```

- [ ] **Step 3: jingqing/ — 新增2个文件的「快反处置」→「警情处置」**

```bash
cd "F:/frank第二大脑/xunfang-baike"
sed -i 's|<a href="index.html">快反处置</a>|<a href="index.html">警情处置</a>|g' jingqing/chidao-jingqing.html jingqing/jizhi-liucheng.html
```

- [ ] **Step 4: fagui/ — 新增3个文件各自不同的旧模块名 →「法条规范」**

```bash
cd "F:/frank第二大脑/xunfang-baike"
sed -i 's|<a href="index.html">巡逻规范</a>|<a href="index.html">法条规范</a>|g' fagui/faly-yiju.html
sed -i 's|<a href="index.html">徒手防卫</a>|<a href="index.html">法条规范</a>|g' fagui/gainian-falv.html
sed -i 's|<a href="index.html">最小作战单元</a>|<a href="index.html">法条规范</a>|g' fagui/faly-fayanfayu.html
```

- [ ] **Step 5: zoufang/ — 替换「反恐防暴」和「快反处置」→「走访送教」(6个文件)**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# 5个来自 fankong
sed -i 's|<a href="index.html">反恐防暴</a>|<a href="index.html">走访送教</a>|g' zoufang/xianchang-chuzhi.html zoufang/xiaoyuan-fankong.html zoufang/jinrong-fankong.html zoufang/zhengzhi-hexinqu.html zoufang/daxing-huodong.html
# 1个来自 kuaifan
sed -i 's|<a href="index.html">快反处置</a>|<a href="index.html">走访送教</a>|g' zoufang/xiaoyuan-peixun.html
```

- [ ] **Step 6: 更新 <title> 标签中的模块名（以 jingqing 新增2页为例）**

```bash
cd "F:/frank第二大脑/xunfang-baike"
# chidao-jingqing.html 标题从 "持刀警情（快反） — 巡防百科" 改为 "持刀警情（快反） — 巡防百科"
# 标题不变，保持原样即可。其他迁移页面同理，<title> 保持原标题。
```

- [ ] **Step 7: 验证图片/JS/CSS 相对路径**

所有迁移文件均在模块子目录下（如 `xunlian/xxx.html`），与旧目录深度相同（1层），`../img/`、`../js/`、`../css/`、`../video/` 路径无需修改。

- [ ] **Step 8: 提交**

```bash
git add -A
git commit -m "$(cat <<'EOF'
fix: 批量更新迁移页面面包屑为新模块名称 (38个文件)
EOF
)"
```

---

### Task 5: 更新导航配置 nav.js

**Files:**
- Modify: `js/nav.js` — MODULES 数组完整重写

- [ ] **Step 1: 替换 MODULES 数组**

将 `js/nav.js` 中的 MODULES 数组从当前12项替换为6项：

```javascript
var MODULES = [
  { name: '装备介绍', path: 'zhuangbei/index.html',  emoji: '🛡️' },
  { name: '巡防勤务', path: 'qinwu/index.html',      emoji: '📋' },
  { name: '警务训练', path: 'xunlian/index.html',    emoji: '⚔️' },
  { name: '警情处置', path: 'jingqing/index.html',    emoji: '🚨' },
  { name: '法条规范', path: 'fagui/index.html',       emoji: '📕' },
  { name: '走访送教', path: 'zoufang/index.html',     emoji: '🏫' }
];
```

其余 renderNav() 函数逻辑不变。

- [ ] **Step 2: 提交**

```bash
git add js/nav.js
git commit -m "$(cat <<'EOF'
feat: 导航栏重写为6大模块结构
EOF
)"
```

---

### Task 6: 更新首页 index.html

**Files:**
- Modify: `index.html` — 11张卡片替换为6张

- [ ] **Step 1: 替换首页卡片网格**

将 `index.html` 中 `.card-grid` 内的11张 `.module-card` 替换为6张：

```html
<div class="card-grid">
  <a href="zhuangbei/index.html" class="module-card accent-blue">
    <div class="icon">🛡️</div>
    <div class="name">装备介绍</div>
    <div class="count">7篇</div>
    <div class="desc">单警装备使用规范</div>
    <div class="hot-links">伸缩警棍 · 催泪喷射器 · 手铐 · 执法记录仪</div>
  </a>
  <a href="qinwu/index.html" class="module-card accent-green">
    <div class="icon">📋</div>
    <div class="name">巡防勤务</div>
    <div class="count">8篇</div>
    <div class="desc">每日勤务与任务规范</div>
    <div class="hot-links">大型活动安保 · 群体事件处置 · 舆情导控</div>
  </a>
  <a href="xunlian/index.html" class="module-card accent-purple">
    <div class="icon">⚔️</div>
    <div class="name">警务训练</div>
    <div class="count">19篇</div>
    <div class="desc">徒手 · 警械 · 战术 · 快反</div>
    <div class="hot-links">盾牌技术 · 盘查流程 · 武力升级 · 搜身带离</div>
  </a>
  <a href="jingqing/index.html" class="module-card accent-red">
    <div class="icon">🚨</div>
    <div class="name">警情处置</div>
    <div class="count">8篇</div>
    <div class="desc">常见警情处置流程</div>
    <div class="hot-links">持刀警情 · 醉酒闹事 · 打架斗殴 · 家庭暴力</div>
  </a>
  <a href="fagui/index.html" class="module-card accent-red">
    <div class="icon">📕</div>
    <div class="name">法条规范</div>
    <div class="count">6篇</div>
    <div class="desc">执法依据速查</div>
    <div class="hot-links">治安规范 · 赌博执法 · 法律依据 · 法言法语</div>
  </a>
  <a href="zoufang/index.html" class="module-card accent-teal">
    <div class="icon">🏫</div>
    <div class="name">走访送教</div>
    <div class="count">6篇</div>
    <div class="desc">校园社区送教服务</div>
    <div class="hot-links">校园反恐 · 现场处置 · 金融反恐 · 校园培训</div>
  </a>
</div>
```

- [ ] **Step 2: 提交**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
feat: 首页更新为6大模块卡片
EOF
)"
```

---

### Task 7: 更新现有模块的索引页

**Files:**
- Modify: `zhuangbei/index.html`, `jingqing/index.html`, `fagui/index.html`

- [ ] **Step 1: 更新 zhuangbei/index.html — 标题改为「装备介绍」**

将 `<h1>` 从 `🛡️ 单警装备` 改为 `🛡️ 装备介绍`，meta 描述更新。

- [ ] **Step 2: 更新 jingqing/index.html — 追加2篇新文章到列表**

在现有6篇文章列表后追加来自快反处置的2篇：

```html
<a href="chidao-jingqing.html" class="list-item">
  <div class="item-title">⚡ 持刀警情（快反）</div>
  <div class="item-desc">135快速反应持刀警情处置要点</div>
</a>
<a href="jizhi-liucheng.html" class="list-item">
  <div class="item-title">🔁 快反机制流程</div>
  <div class="item-desc">135快速反应机制启动与执行流程</div>
</a>
```

同时更新 meta 中的文章数从 `6篇` 改为 `8篇`。

- [ ] **Step 3: 更新 fagui/index.html — 追加3篇新文章 + 分组**

先查看 fagui 当前 index.html 的列表结构，在其尾部追加：

```html
<div class="list-section-title">执法依据</div>
<a href="faly-yiju.html" class="list-item">
  <div class="item-title">📜 法律依据</div>
  <div class="item-desc">巡逻盘查的执法法律依据汇总</div>
</a>
<a href="gainian-falv.html" class="list-item">
  <div class="item-title">⚖️ 概念法律</div>
  <div class="item-desc">徒手防卫与控制的法律概念</div>
</a>
<a href="faly-fayanfayu.html" class="list-item">
  <div class="item-title">🗣️ 法言法语</div>
  <div class="item-desc">执法过程中的规范法言法语</div>
</a>
```

更新 meta 中文章数从 `3篇` 改为 `6篇`。

- [ ] **Step 4: 提交**

```bash
git add zhuangbei/index.html jingqing/index.html fagui/index.html
git commit -m "$(cat <<'EOF'
feat: 更新 zhuangbei/jingqing/fagui 模块索引页
EOF
)"
```

---

### Task 8: 清理旧目录

**Files:**
- Delete: `kuaifan/`, `xunluo/`, `daxing-anbao/`, `qunti-shijian/`, `tushou/`, `zuozhan-danyuan/`, `fankong/`

- [ ] **Step 1: 删除已清空的旧模块目录**

这些目录在 Task 3 迁移后应只剩下 index.html，确认后删除：

```bash
cd "F:/frank第二大脑/xunfang-baike"
rm -rf kuaifan/ xunluo/ daxing-anbao/ qunti-shijian/ tushou/ zuozhan-danyuan/ fankong/
```

- [ ] **Step 2: 提交**

```bash
git add -A
git commit -m "$(cat <<'EOF'
chore: 清理8个已解散的旧模块目录
EOF
)"
```

---

### Task 9: 验证与修复

- [ ] **Step 1: 本地打开首页验证**

在浏览器打开 `F:/frank第二大脑/xunfang-baike/index.html`，检查：
1. 导航栏显示6个模块，每个可点击跳转
2. 6张模块卡片布局正常
3. 搜索功能正常（过滤卡片）

- [ ] **Step 2: 检查每个模块索引页**

依次点击6个模块卡进入索引页，检查：
1. 面包屑路径正确
2. 文章列表完整，链接可跳转
3. 分组标题显示正常
4. 搜索过滤联动隐藏空分组

- [ ] **Step 3: 抽查迁移详情页**

从每个模块各选1-2个详情页打开，检查：
1. 面包屑指向正确的模块
2. 页面导航（prev/next）链接不404
3. 图片/视频占位符路径正确
4. 折叠展开交互正常

- [ ] **Step 4: 修复发现的问题**

如发现断链或路径错误，修复。

- [ ] **Step 5: 提交**

```bash
git add -A
git commit -m "$(cat <<'EOF'
fix: 验证后修复面包屑和链接问题
EOF
)"
```

---

### Task 10: 推送上线

- [ ] **Step 1: 推送**

```bash
git push origin master
```

- [ ] **Step 2: 验证线上**

访问 `https://wangrufan-frank.github.io/xunfang-baike/`，确认首页和所有模块正常运行。
