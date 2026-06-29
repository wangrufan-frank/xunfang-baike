# 装备介绍模块 — 媒体占位符补充实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为装备介绍模块6个HTML页面新增10个媒体占位符（8图2视频），遵循现有 step-media media-placeholder 模式。

**Architecture:** 纯静态HTML页面，每个占位符 `<div class="step-media media-placeholder img|video">📷|🎬 说明</div>` 插入在 step-card 内 `step-lead` 与 `expandable` 之间，与伸缩警棍页现有占位符一致。

**Tech Stack:** HTML

## Global Constraints

- 仅修改 `zhuangbei/` 目录下的 HTML 文件
- 不改动 CSS、JS、其他模块、首页
- 占位符格式：`<div class="step-media media-placeholder img">📷 说明文字</div>` 或 video 类
- 插入位置：step-card 内，step-lead 之后、expandable 之前
- 文字内容不动

---

### Task 1: 九小件概览 — 3个图片占位符

**Files:**
- Modify: `zhuangbei/jiuxiaojian-gailan.html`

- [ ] **Step 1: 在九小件清单 step-card 中插入占位符**

找到 `step-lead` 文字 "单警装备九小件是基层民警日常执勤执法中随身配备的九种标准警用装备的统称。" 所在的 `</div>`（step-lead 闭合标签），在其后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 九小件全套平铺展示图</div>
```

- [ ] **Step 2: 在佩戴三大原则 step-card 中插入占位符**

找到 `step-lead` 文字 "贴身紧靠防脱落，方便拿取按使用频率排序，武力升级由低到高体现最小武力原则。" 所在的 `</div>`，在其后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 多功能腰带全装佩戴正面照</div>
```

- [ ] **Step 3: 在佩戴顺序 step-card 中插入占位符**

找到 `step-lead` 文字 "从左至右：弹匣→伸缩警棍→强光手电→对讲机→警用水壶→手铐→工作包/急救包→手枪→催泪喷射器（强手第一选择位）。" 所在的 `</div>`，在其后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 腰带展开俯视图（标注各装备名称）</div>
```

- [ ] **Step 4: 验证**

在浏览器中打开 `zhuangbei/jiuxiaojian-gailan.html`，确认3个占位符正确显示。

- [ ] **Step 5: 提交**

```bash
git add zhuangbei/jiuxiaojian-gailan.html
git commit -m "feat: 九小件概览新增3个图片占位符"
```

---

### Task 2: 催泪喷射器 — 1个图片占位符

**Files:**
- Modify: `zhuangbei/cuilei-pensheqi.html`

- [ ] **Step 1: 在性能参数 step-card 中插入占位符**

找到第二个 step-card（class="step-card step-blue"，含"性能参数"标题），在 `step-lead` 的 `</div>` 之后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 催泪喷射器结构/型号外观图</div>
```

- [ ] **Step 2: 验证**

在浏览器中打开 `zhuangbei/cuilei-pensheqi.html`，确认新增占位符和已有的视频占位符均正确显示。

- [ ] **Step 3: 提交**

```bash
git add zhuangbei/cuilei-pensheqi.html
git commit -m "feat: 催泪喷射器性能参数新增结构图占位符"
```

---

### Task 3: 手铐 — 1个图片占位符

**Files:**
- Modify: `zhuangbei/shoukao.html`

- [ ] **Step 1: 在武力链条 step-card 中插入占位符**

找到第一个 step-card（class="step-card step-blue"，含"定位：武力链条中的约束环节"标题），在 `step-lead` 的 `</div>` 之后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 手铐结构图（铐环、锁闭机构、钥匙）</div>
```

- [ ] **Step 2: 验证**

在浏览器中打开 `zhuangbei/shoukao.html`，确认新增图片占位符和已有的视频占位符均正确显示。

- [ ] **Step 3: 提交**

```bash
git add zhuangbei/shoukao.html
git commit -m "feat: 手铐武力链条章节新增结构图占位符"
```

---

### Task 4: 防割手套 — 2个图片占位符

**Files:**
- Modify: `zhuangbei/fangge-shoutao.html`

- [ ] **Step 1: 在核心性能边界 step-card 中插入占位符**

找到第一个 step-card（class="step-card step-red"，含"核心性能边界：防割不防刺"标题），在 `step-lead` 的 `</div>` 之后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 防割不防刺对比示意 / 手套实物特写</div>
```

- [ ] **Step 2: 在使用场景 step-card 中插入占位符**

找到 step-card（class="step-card step-blue"，含"使用场景"标题），在 `step-lead` 的 `</div>` 之后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 民警佩戴手套搜身场景照</div>
```

- [ ] **Step 3: 验证**

在浏览器中打开 `zhuangbei/fangge-shoutao.html`，确认2个占位符正确显示。

- [ ] **Step 4: 提交**

```bash
git add zhuangbei/fangge-shoutao.html
git commit -m "feat: 防割手套新增2个图片占位符"
```

---

### Task 5: 执法记录仪 — 2个图片占位符

**Files:**
- Modify: `zhuangbei/zhifa-jiuyi.html`

- [ ] **Step 1: 在日常检查维护 step-card 中插入占位符**

找到第一个 step-card（class="step-card step-blue"，含"日常检查维护"标题），在 `step-lead` 的 `</div>` 之后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 记录仪开机界面/屏幕信息展示</div>
```

- [ ] **Step 2: 在使用规范 step-card 中插入占位符**

找到 step-card（class="step-card step-green"，含"使用规范"标题），在 `step-lead` 的 `</div>` 之后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 记录仪胸前/肩部佩戴位置展示</div>
```

- [ ] **Step 3: 验证**

在浏览器中打开 `zhuangbei/zhifa-jiuyi.html`，确认2个占位符正确显示。

- [ ] **Step 4: 提交**

```bash
git add zhuangbei/zhifa-jiuyi.html
git commit -m "feat: 执法记录仪新增2个图片占位符"
```

---

### Task 6: 警械警告用语 — 1个图片占位符

**Files:**
- Modify: `zhuangbei/jingxie-jinggao.html`

- [ ] **Step 1: 在标准警告用语 step-card 中插入占位符**

找到第一个 step-card（class="step-card step-red"，含"标准警告用语"标题），在 `step-lead` 的 `</div>` 之后、`<div class="expandable">` 之前插入：

```html
    <div class="step-media media-placeholder img">📷 警械警告用语快速参考卡</div>
```

- [ ] **Step 2: 验证**

在浏览器中打开 `zhuangbei/jingxie-jinggao.html`，确认占位符正确显示。

- [ ] **Step 3: 提交**

```bash
git add zhuangbei/jingxie-jinggao.html
git commit -m "feat: 警械警告用语新增参考卡片占位符"
```

---

## 执行说明

任务之间无依赖，可并行执行。每个任务 2-5 分钟。

## Self-Review

1. **Spec coverage:** 6 files × 10 placeholders, all mapped to tasks ✓
2. **Placeholder scan:** No TBD/TODO, exact HTML in each step ✓
3. **Type consistency:** All use `<div class="step-media media-placeholder img|video">` pattern ✓
