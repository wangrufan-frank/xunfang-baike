# 巡防百科 · 微信小程序设计

**日期:** 2026-06-30
**状态:** 已批准
**范围:** 巡防百科网站迁移至微信小程序（个人账号），MVP 含装备介绍 + 警情处置

---

## 一、概述

将巡防百科（6模块 ~60篇）从 GitHub Pages 静态网站迁移到微信小程序。个人账号无法使用 `<web-view>`，需用 WXML/WXSS/JS 原生重写。采用分批策略：MVP 先上线装备介绍 + 警情处置两个模块，验证架构后逐步搬移剩余模块。

## 二、项目结构

```
miniprogram/
├── app.json
├── app.js              ← 启动逻辑 + 密码守卫
├── app.wxss            ← 全局样式（变量 + 通用类）
├── components/
│   ├── step-card/      ← 步骤卡片（带折叠）
│   ├── quick-card/     ← 速览卡片
│   └── list-item/      ← 列表项
├── data/
│   ├── zhuangbei.js
│   └── jingqing.js
└── pages/
    ├── auth/           ← 密码登录页（不在tabBar）
    ├── index/          ← 首页 模块卡片 + 每日一学（不在tabBar）
    ├── more/           ← 更多（法规 + 走访入口）
    ├── zhuangbei/
    │   ├── index/      ← 装备列表页
    │   └── detail/     ← 装备详情页（通用模板，数据驱动）
    └── jingqing/
        ├── index/      ← 警情列表页
        └── detail/     ← 警情详情页（通用模板，数据驱动）
```

**关键决策：详情页数据驱动。** 所有装备文章共享 `zhuangbei/detail` 模板，通过 `id` 参数从 `data/zhuangbei.js` 读取内容。警情同理。15篇文章仅需2个详情页，减小包体积和注册页面数。

## 三、导航架构

底部 tabBar（4 + 1）：

| 位置 | 图标 | 页面 | 说明 |
|------|------|------|------|
| 1 | 🛡️ 装备 | pages/zhuangbei/index | MVP |
| 2 | 📋 勤务 | placeholder | 第二批 |
| 3 | ⚔️ 训练 | placeholder | 第二批 |
| 4 | 🚨 警情 | pages/jingqing/index | MVP |
| 5 | ⋯ 更多 | pages/more/more | 法规+走访入口 |

首页和登录页不在 tabBar。流程：登录 → 首页 → 点击卡片 → 模块列表页 → 详情页。页面栈返回。

## 四、内容数据模型

内容与页面分离。每个模块一个 JS 文件，导出文章数组：

```js
[{
  id: 'shensuo-jinggun',
  title: '伸缩警棍',
  icon: '🪠',
  desc: '基层使用频率最高的驱逐性警械',
  tags: ['⚠️ 驱逐性警械', '伸长约52cm'],
  quickCard: { title, tags, flow },
  steps: [
    { num, title, color, lead, content, expandable },
    ...
  ]
}]
```

列表页用 `title/icon/desc` 渲染，详情页用 `quickCard/steps` 渲染。

## 五、密码保护

网页版用 cookie → 小程序改用 `wx.setStorageSync`。

- `app.js` 启动检查 storage `xunfang_auth`
- 无记录 → `wx.redirectTo('/pages/auth/auth')`
- `auth` 页：输入密码 → SHA-256 比对 `c252bf49e...` → 正确写 storage → `wx.switchTab` 到首页
- storage 无过期（除非卸载或清缓存）
- 样式保持与现有 auth.html 一致的深色背景 + 居中卡片

## 六、复用组件

| 组件 | 用途 | 属性 |
|------|------|------|
| `step-card` | 步骤卡片（折叠展开） | num, title, color, lead, content, expandable |
| `quick-card` | 文章顶部速览卡片 | icon, title, tags[], flow |
| `list-item` | 模块列表项 | title, icon, desc, url |

## 七、MVP 范围

**包含：**
- 密码登录页
- 首页（模块卡片网格 + 每日一学轮播）
- 装备介绍模块（列表页 + 7篇详情）
- 警情处置模块（列表页 + 8篇详情）
- 更多页（法规+走访入口，占位）

**不包含（第二批）：**
- 巡防勤务（8篇）
- 警务训练（19篇）
- 法条规范详情页（6篇）
- 走访送教详情页（6篇）

## 八、不改范围

- 现有 HTML 网站不变，继续维护
- oss_upload.py 不动
- GitHub Pages 部署不动
