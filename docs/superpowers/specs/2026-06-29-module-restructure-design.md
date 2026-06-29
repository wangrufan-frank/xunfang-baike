# 网站模块重组设计

**日期:** 2026-06-29
**状态:** 已批准
**范围:** 全站模块从11个重组为6个，文件迁移、导航更新、索引重建

---

## 一、重组概览

将现有11个模块重组为6大模块：

| 新模块 | 目录 | 来源 | 页数 |
|--------|------|------|------|
| 装备介绍 | zhuangbei/ | 原单警装备7页（后续扩展车辆装备等） | 7 |
| 巡防勤务 | qinwu/ | 大型活动安保3页 + 群体事件处置5页（后续扩展巡逻规范等） | 8 |
| 警务训练 | xunlian/ | 徒手防卫3页 + 最小作战单元8页 + 盘查流程等4页 + 快反技能2页 + 反恐基础理论2页 | 19 |
| 警情处置 | jingqing/ | 原警情处置6页 + 快反警情类2页 | 8 |
| 法条规范 | fagui/ | 原法律法规3页 + 法律依据1页 + 概念法律1页 + 法言法语1页（后续大量新增） | 6 |
| 走访送教 | zoufang/ | 反恐场景处置5页 + 校园培训1页 | 6 |

总计：54个详情页 + 6个模块索引页 + 1个首页 = 61个HTML文件（原74个 − 删除手枪射击5页和首页 − 8个解散模块的旧index.html + 3个新建模块的index.html）

---

## 二、目录变化

### 删除目录（8个）
`shoushe/` `kuaifan/` `xunluo/` `daxing-anbao/` `qunti-shijian/` `tushou/` `zuozhan-danyuan/` `fankong/`

### 新建目录（3个）
`qinwu/` `xunlian/` `zoufang/`

### 保留目录（3个）
`zhuangbei/` `jingqing/` `fagui/`

---

## 三、逐页迁移清单

### 装备介绍 `zhuangbei/`（7页，不变）
| 文件 | 标题 |
|------|------|
| cuilei-pensheqi.html | 催泪喷射器 |
| fangge-shoutao.html | 防割手套 |
| jingxie-jinggao.html | 警戒带与警告牌 |
| jiuxiaojian-gailan.html | 九小件概览 |
| shensuo-jinggun.html | 伸缩警棍 |
| shoukao.html | 手铐规范 |
| zhifa-jiuyi.html | 执法记录仪 |

### 巡防勤务 `qinwu/`（8页）
来源：大型活动安保 + 群体事件处置

| 文件 | 标题 | 来源目录 |
|------|------|----------|
| yanchanghui-zhifa.html | 演唱会执法 | daxing-anbao |
| xiaoyuan-jinrong.html | 校园金融 | daxing-anbao |
| yuqing-zhanshu.html | 舆情战术 | daxing-anbao |
| chuzhi-yuan.html | 群体事件处置预案 | qunti-shijian |
| kongzhi-daili.html | 控制带离 | qunti-shijian |
| shewen-yanlian.html | 涉稳演练 | qunti-shijian |
| xuanchuan-quzheng.html | 宣传取证 | qunti-shijian |
| yuqing-daokong.html | 舆情导控 | qunti-shijian |

### 警务训练 `xunlian/`（19页）
来源：徒手防卫技能 + 最小作战单元技能 + 部分巡逻规范技能 + 快反技能 + 反恐基础理论

| 文件 | 标题 | 来源目录 |
|------|------|----------|
| jietuo-fangyu.html | 解脱防卫 | tushou |
| kongzhi-jishu.html | 控制技术 | tushou |
| soushen-daili.html | 搜身带离 | tushou |
| dunpai-jishu.html | 盾牌技术 | zuozhan-danyuan |
| duncha-xietong.html | 盾叉协同 | zuozhan-danyuan |
| gaishu-biancheng.html | 最小作战单元概述 | zuozhan-danyuan |
| jinggun-zhuabucha.html | 警棍抓捕叉 | zuozhan-danyuan |
| wuli-shengji-sanfang.html | 武力升级三防 | zuozhan-danyuan |
| xunlian-jiaoxuefa.html | 训练教学法 | zuozhan-danyuan |
| zhanshu-zhanwei.html | 战术站位 | zuozhan-danyuan |
| zhudong-hengyi.html | 主动恒义 | zuozhan-danyuan |
| pancha-liucheng.html | 盘查流程 | xunluo |
| shizi-fangyu.html | 十字防御 | xunluo |
| xidu-pancha.html | 吸毒盘查 | xunluo |
| zhanshu-zhanwei-xunluo.html | 战术站位（巡逻） | xunluo |
| duncha-zhanzhu.html | 盾叉站住 | kuaifan |
| sinengli-yaosu.html | 四能力要素 | kuaifan |
| gaishu-yuanze.html | 反恐概述原则 | fankong |
| wuli-shengji.html | 武力升级 | fankong |

> 命名冲突：两个来源的「战术站位」文件，来自 zuozhan-danyuan 的保留原名 zhanshu-zhanwei.html，来自 xunluo 的重命名为 zhanshu-zhanwei-xunluo.html。

### 警情处置 `jingqing/`（8页）
来源：原警情处置 + 快反整体警情

| 文件 | 标题 | 来源目录 |
|------|------|----------|
| chidao-leiqing.html | 持刀类警情处置 | jingqing（原） |
| dajia-douou.html | 打架斗殴 | jingqing（原） |
| jiating-baoli.html | 家庭暴力 | jingqing（原） |
| keyi-cheliang.html | 可疑车辆 | jingqing（原） |
| renyuan-pancha.html | 人员盘查 | jingqing（原） |
| zuijiu-naoshi.html | 醉酒闹事 | jingqing（原） |
| jizhi-liucheng.html | 快反机制流程 | kuaifan |
| chidao-jingqing.html | 快反持刀警情 | kuaifan |

> 注意：jingqing/ 已有 chidao-leiqing.html，kuaifan/ 的 chidao-jingqing.html 是不同角度的持刀警情内容，需检查是否合并或保留独立。

### 法条规范 `fagui/`（6页）
来源：原法律法规 + 各模块法律相关

| 文件 | 标题 | 来源目录 |
|------|------|----------|
| dubo-zhifa.html | 赌博执法 | fagui（原） |
| shipin-tiaoli.html | 视频条例 | fagui（原） |
| zhian-guifan.html | 治安规范 | fagui（原） |
| faly-yiju.html | 法律依据 | xunluo |
| gainian-falv.html | 概念法律 | tushou |
| faly-fayanfayu.html | 法言法语 | zuozhan-danyuan |

### 走访送教 `zoufang/`（6页）
来源：反恐场景处置 + 快反校园

| 文件 | 标题 | 来源目录 |
|------|------|----------|
| xianchang-chuzhi.html | 现场处置 | fankong |
| xiaoyuan-fankong.html | 校园反恐 | fankong |
| jinrong-fankong.html | 金融反恐 | fankong |
| zhengzhi-hexinqu.html | 政治核心区 | fankong |
| daxing-huodong.html | 大型活动反恐 | fankong |
| xiaoyuan-peixun.html | 校园培训 | kuaifan |

### 删除
`shoushe/` 目录整个删除：
- anquan-guifan.html（安全规范）
- dandian-pianli.html（单点偏离）
- juqiang-dongzuo.html（据枪动作）
- miaozhun-jifa.html（瞄准技法）
- richang-baoyang.html（日常保养）

---

## 四、代码改动

### 4.1 `js/nav.js` — 重写 MODULES 数组

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

其余 renderNav() 逻辑不变。

### 4.2 `index.html` — 首页卡片

6张模块卡片替换现有11张，每张含：
- 图标、模块名、文章数、描述、热门链接

### 4.3 模块索引页

- 新建 `qinwu/index.html`、`xunlian/index.html`、`zoufang/index.html`
- 更新 `zhuangbei/index.html`、`jingqing/index.html`、`fagui/index.html`（调整文章列表）

### 4.4 详情页

每个移动后的页面需修改：
- `<title>` 标签
- 面包屑导航路径
- 页面内相对链接（prev/next、图片、视频路径）

### 4.5 不改的范围

- `css/style.css` — 样式不变
- `js/main.js` — 搜索和折叠逻辑不变
- 页面正文内容 — 仅改路径，不改文字

---

## 五、实施顺序

1. **删除** shoushe/ 目录
2. **新建** qinwu/、xunlian/、zoufang/ 目录及 index.html
3. **迁移文件** — 按清单逐页移动
4. **处理命名冲突** — 重名文件加后缀或合并
5. **更新面包屑和链接** — 所有迁移页面
6. **更新 nav.js** — MODULES 数组
7. **更新首页 index.html** — 6张卡片
8. **更新保留模块的 index.html** — zhuangbei/jingqing/fagui
9. **验证** — 本地打开首页，检查每个模块的导航、搜索、链接
10. **提交推送** — git commit + git push
