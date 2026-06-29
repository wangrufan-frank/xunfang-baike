# 装备介绍模块 — 媒体占位符补充设计

**日期:** 2026-06-29
**状态:** 已批准
**范围:** 装备介绍模块 7 个页面，6 个需补充占位符（伸缩警棍已有占位符不变）

---

## 一、概述

装备介绍 7 个页面中，伸缩警棍有 5 个占位符，催泪喷射器和手铐各有 1 个，其余 4 页为零。本次为 6 个页面新增 10 个占位符（8图2视频），使装备模块每页都有媒体演示区域。

---

## 二、逐页改动

### 2.1 九小件概览 `zhuangbei/jiuxiaojian-gailan.html`

新增 3 个图片占位符：

| 插入位置 | 内容 |
|----------|------|
| 九小件清单 expandable 前 | 📷 九小件全套平铺展示图 |
| 佩戴三大原则 expandable 前 | 📷 多功能腰带全装佩戴正面照 |
| 佩戴顺序 expandable 前 | 📷 腰带展开俯视图（标注各装备名称） |

### 2.2 催泪喷射器 `zhuangbei/cuilei-pensheqi.html`

新增 1 个图片占位符：

| 插入位置 | 内容 |
|----------|------|
| 性能参数 expandable 后 | 📷 催泪喷射器结构/型号外观图 |

### 2.3 手铐 `zhuangbei/shoukao.html`

新增 1 个图片占位符：

| 插入位置 | 内容 |
|----------|------|
| 武力链条 expandable 前 | 📷 手铐结构图（铐环、锁闭机构、钥匙） |

### 2.4 防割手套 `zhuangbei/fangge-shoutao.html`

新增 2 个图片占位符：

| 插入位置 | 内容 |
|----------|------|
| 核心性能边界 expandable 前 | 📷 防割不防刺对比示意 / 手套实物特写 |
| 使用场景 expandable 前 | 📷 民警佩戴手套搜身场景照 |

### 2.5 执法记录仪 `zhuangbei/zhifa-jiuyi.html`

新增 2 个图片占位符：

| 插入位置 | 内容 |
|----------|------|
| 日常检查维护 expandable 前 | 📷 记录仪开机界面/屏幕信息展示 |
| 使用规范 expandable 前 | 📷 记录仪胸前/肩部佩戴位置展示 |

### 2.6 警械警告用语 `zhuangbei/jingxie-jinggao.html`

新增 1 个图片占位符：

| 插入位置 | 内容 |
|----------|------|
| 标准警告用语 expandable 前 | 📷 警械警告用语快速参考卡 |

### 2.7 伸缩警棍 `zhuangbei/shensuo-jinggun.html`

不改动，已有 5 个占位符。

---

## 三、占位符 HTML 模板

```html
<div class="step-media media-placeholder img">📷 图片说明</div>
<!-- 或 -->
<div class="step-media media-placeholder video">🎬 视频说明</div>
```

插入位置统一为 step-card 内 `step-lead` 与 `expandable` 之间，与伸缩警棍现有占位符一致。

---

## 四、不改的范围

- CSS/JS 不变
- 模块索引页不变
- 其他 5 个模块不动
- 伸缩警棍页不动
- 所有文字内容不动

---

## 五、素材替换指南

素材到位后，将 `media-placeholder` 替换为实际内容：

```html
<!-- 图片：替换占位符 -->
<img src="../img/zhuangbei/jiuxiaojian.jpg" alt="九小件全套" class="step-media">

<!-- 视频：替换占位符 -->
<video src="../video/zhuangbei/pen-yi-wen.mp4" controls class="step-media"></video>
```
