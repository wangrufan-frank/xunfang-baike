# 巡防百科三级内容体系重建——设计与实施规范

**日期：** 2026-07-17

**状态：** 待实施

**适用执行者：** Claude Code

**项目：** `F:\frank第二大脑\xunfang-baike`

**主要内容源：** `F:\frank第二大脑\frank知识库`

**范围：** 桌面静态网站；不修改微信小程序

---

## 1. 目标

本次改造一次性完成网站密码、模块名称、三级信息架构、全部文章内容、图片、法律引用、交叉链接和搜索索引更新。不得保留“内容整改中”“待补充”或空白文章页。

网站统一采用三级结构：

1. 一级：主模块；
2. 二级：模块内分类；
3. 三级：具体文章。

文章内部的章节标题不计为导航层级，不再建立第四级内容目录。

### 1.1 六个主模块

| 一级模块 | 保留目录 | 二级分类数 | 三级文章数 |
|---|---|---:|---:|
| 装备介绍 | `zhuangbei/` | 3 | 26 |
| 勤务保障 | `qinwu/` | 4 | 13 |
| 警务训练 | `xunlian/` | 2 | 13 |
| 警情处置 | `jingqing/` | 5 | 5 |
| 执法规范 | `fagui/` | 3 | 17 |
| 教育培训 | `zoufang/` | 3 | 13 |
| **合计** |  | **20** | **87** |

“本月精选”继续作为独立推荐入口，但不计入六个主模块和三级内容统计。

### 1.2 明确不做

- 不修改 `miniprogram/` 下任何文件。
- 不把网站改造成运行时 JSON 渲染或前端框架项目。
- 不向 Obsidian 知识库写入或重排资料。
- 不把警情文章写成内部力量部署、通信调度或精确战术参数手册。
- 不为凑齐页面而虚构本地考核标准、法律条号、装备参数或图片来源。

---

## 2. 三级信息架构与文件清单

下面的清单是实施时的内容库存基准。现有路径可直接保留；现有内容与新主题不一致时，应重写正文。新增文件使用小写拼音和连字符。

## 2.1 装备介绍 `zhuangbei/`（26篇）

### 人身装备（4篇）

| 三级文章 | 文件 |
|---|---|
| 九小件概览 | `zhuangbei/jiuxiaojian-gailan.html` |
| 防割手套 | `zhuangbei/fangge-shoutao.html` |
| 执法记录仪 | `zhuangbei/zhifa-jiuyi.html` |
| 对讲电台 | `zhuangbei/duijiang-diantai.html` |

“伸缩警棍”“催泪喷射器”“手铐”属于九小件，不在装备模块建立独立三级文章。原有三篇独立装备页面的有效内容应合并进“九小件概览”；旧路径如需要兼容收藏，可改成不参与导航和搜索的跳转页。

### 车载装备（10篇）

| 三级文章 | 文件 |
|---|---|
| 阻车钉 | `zhuangbei/zuche-ding.html` |
| 水上飞翼 | `zhuangbei/shuishang-feiyi.html` |
| 灭火毯 | `zhuangbei/miehuo-tan.html` |
| 灭火器 | `zhuangbei/miehuo-qi.html` |
| 反光锥筒 | `zhuangbei/fanguang-zhuitong.html` |
| 救生圈 | `zhuangbei/jiusheng-quan.html` |
| 救生衣 | `zhuangbei/jiusheng-yi.html` |
| 救生绳 | `zhuangbei/jiusheng-sheng.html` |
| 破拆工具 | `zhuangbei/pochai-gongju.html` |
| 5G云台 | `zhuangbei/5g-yuntai.html` |

### 战术装备（12篇）

| 三级文章 | 文件 |
|---|---|
| 防暴头盔 | `zhuangbei/fangbao-toukui.html` |
| 抓捕叉 | `zhuangbei/zhuabu-cha.html` |
| 警戒带与警告牌 | `zhuangbei/jingjiedai-jinggaopai.html` |
| 法式盾牌 | `zhuangbei/fashi-dunpai.html` |
| 臂盾 | `zhuangbei/bidun.html` |
| T字棍 | `zhuangbei/t-zi-gun.html` |
| 强光手电 | `zhuangbei/qiangguang-shoudian.html` |
| 伞式围挡 | `zhuangbei/sanshi-weidang.html` |
| 折叠式围挡 | `zhuangbei/zhedieshi-weidang.html` |
| 长棍 | `zhuangbei/changgun.html` |
| 防刺服 | `zhuangbei/fangci-fu.html` |
| 约束带 | `zhuangbei/yueshu-dai.html` |

### 装备文章模板

装备文章依次包含：装备简介、组成与用途、适用场景、基础使用、使用前后检查、安全注意事项、维护保管、相关法规与训练、图片或示意图。

定位是“明了介绍运用场景和基础技能”，不得把所有装备页写成长篇专业战术教程。

## 2.2 勤务保障 `qinwu/`（13篇）

原“巡防勤务”统一更名为“勤务保障”。

### 大型活动安保（3篇）

| 三级文章 | 文件 |
|---|---|
| 足球赛事安保 | `qinwu/zuqiu-saishi-anbao.html` |
| 大型室外演唱会安保 | `qinwu/daxing-shiwai-yanchanghui.html` |
| 小型室内演出安保 | `qinwu/xiaoxing-shinei-yanchu.html` |

### 公共秩序事件（3篇）

“公共秩序事件”替代“群体性事件”。

| 三级文章 | 文件 |
|---|---|
| 处置基本原则 | `qinwu/gonggong-zhixu-chuzhi-yuanze.html` |
| 法律适用与权利保障 | `qinwu/gonggong-zhixu-falv-quanli.html` |
| 现场沟通、记录与舆情风险 | `qinwu/gonggong-zhixu-goutong-jilu.html` |

本分类只写公开处置原则、法律边界、群众权利、沟通记录和注意事项，不汇编内部部署、警力数量、行动路线、通信方式或非公开预案。

### 支点联防（4篇）

| 三级文章 | 文件 |
|---|---|
| 小区支点走访 | `qinwu/xiaoqu-zhidian-zoufang.html` |
| 学校支点走访 | `qinwu/xuexiao-zhidian-zoufang.html` |
| 银行支点走访 | `qinwu/yinhang-zhidian-zoufang.html` |
| 商场支点走访 | `qinwu/shangchang-zhidian-zoufang.html` |

每篇覆盖安保负责人联络、治安走访、联合巡逻、装备培训、问题记录和后续反馈。

### 专项活动保障（3篇）

“专项活动保障”替代“警卫任务”。

| 三级文章 | 文件 |
|---|---|
| 专项活动保障概述 | `qinwu/zhuanxiang-huodong-gailan.html` |
| 现场秩序与安全服务 | `qinwu/zhuanxiang-xianchang-zhixu.html` |
| 部门协同与突发情况报告 | `qinwu/zhuanxiang-xietong-baogao.html` |

### 勤务文章模板

勤务文章依次包含：适用范围、法律和职责边界、勤务前检查、主要风险、现场服务与秩序维护、部门协同、群众沟通、突发情况报告、复盘要点。

## 2.3 警务训练 `xunlian/`（13篇）

### 单兵技能训练（7篇）

| 三级文章 | 文件 |
|---|---|
| 个人防护与训练安全 | `xunlian/geren-fanghu-anquan.html` |
| 伸缩警棍基础训练 | `xunlian/shensuo-jinggun-xunlian.html` |
| 催泪喷射器基础训练 | `xunlian/cuilei-pensheqi-xunlian.html` |
| 手铐基础训练 | `xunlian/shoukao-xunlian.html` |
| 执法记录仪与电台训练 | `xunlian/jiluyi-diantai-xunlian.html` |
| 强光手电基础训练 | `xunlian/qiangguang-shoudian-xunlian.html` |
| 徒手解脱与控制基础 | `xunlian/jietuo-kongzhi-jichu.html` |

伸缩警棍、催泪喷射器、手铐虽然不作为独立装备介绍文章，仍可作为单兵训练主题。

### 小组协同训练（6篇）

| 三级文章 | 文件 |
|---|---|
| 小组编成与职责分工 | `xunlian/xiaozu-biancheng-fengong.html` |
| 协同站位与基础队形 | `xunlian/xietong-zhanwei-duixing.html` |
| 盾牌与抓捕叉协同 | `xunlian/dunpai-zhuabucha-xietong.html` |
| 移动、掩护与人员带离 | `xunlian/yidong-yanhu-daili.html` |
| 现场沟通与影像记录 | `xunlian/xianchang-goutong-yingxiang.html` |
| 训练组织、复盘与考评 | `xunlian/xunlian-fupan-kaoping.html` |

### 训练文章模板

训练文章依次包含：训练目标、适用人员、场地和装备、安全检查、基础动作或协同要点、常见错误、训练组织、考核观察点、相关装备与法规。

训练模块聚焦人员与装备能力，不按五类具体警情重复编写处置教程。

## 2.4 警情处置 `jingqing/`（5篇）

| 二级分类 | 三级文章 | 文件 |
|---|---|---|
| 醉酒类警情 | 醉酒类警情处置基础 | `jingqing/zuijiu-lei.html` |
| 持刀类警情 | 持刀类警情处置基础 | `jingqing/chidao-lei.html` |
| 自伤类警情 | 自伤类警情处置基础 | `jingqing/zishang-lei.html` |
| 精神障碍类警情 | 精神障碍类警情处置基础 | `jingqing/jingshen-zhangai-lei.html` |
| 涉爆类警情 | 涉爆类警情处置基础 | `jingqing/shebao-lei.html` |

### 警情文章模板

每篇依次包含：

1. 警情范围与适用边界；
2. 接警后的任务确认；
3. 风险分析；
4. 到场处置注意事项；
5. 沟通和人员保护；
6. 医疗、消防、排爆等专业力量协同；
7. 法律边界；
8. 记录报告；
9. 禁止性事项。

接警部分写通用职责确认和分工原则，不写内部编组数量、调度规则或通信方式。精神障碍类不得由网页替代医疗诊断；涉爆类不得提供拆除、搬移或处理可疑装置的操作方法。

## 2.5 执法规范 `fagui/`（17篇）

原“法条规范”统一更名为“执法规范”。

### 现场规范用语（5篇）

| 三级文章 | 文件 |
|---|---|
| 表明身份与说明目的 | `fagui/shenfen-mudi-shuoming.html` |
| 盘查中的规范沟通 | `fagui/pancha-guifan-goutong.html` |
| 面对质疑时的依法回应 | `fagui/zhiyi-yifa-huiying.html` |
| 围观拍摄与现场秩序引导 | `fagui/weiguan-paishe-zhixu.html` |
| 权利义务和法律后果告知 | `fagui/quanli-yiwu-gaozhi.html` |

不得把群众正常拍摄一概描述为违法，不编写无依据的强制删图、删视频话术。需要限制行为时，必须说明适用条件和法律依据。

### 执法程序与法条应用（5篇）

| 三级文章 | 文件 |
|---|---|
| 盘问检查与身份证查验 | `fagui/panwen-shenfenzheng.html` |
| 传唤和强制传唤 | `fagui/chuanhuan-qiangzhi-chuanhuan.html` |
| 警械使用的条件与程序 | `fagui/jingxie-shiyong-chengxu.html` |
| 行政案件调查取证 | `fagui/xingzheng-anji-tiaocha.html` |
| 执法记录与权利保障 | `fagui/zhifa-jilu-quanli.html` |

### 法律法规库（7篇）

| 三级文章 | 文件 |
|---|---|
| 治安管理处罚法 | `fagui/zhian-guanli-chufa-fa.html` |
| 人民警察法 | `fagui/renmin-jingcha-fa.html` |
| 居民身份证法 | `fagui/jumin-shenfenzheng-fa.html` |
| 公安机关办理行政案件程序规定 | `fagui/xingzheng-anji-chengxu-guiding.html` |
| 人民警察使用警械和武器条例 | `fagui/jingxie-wuqi-tiaoli.html` |
| 现场制止违法犯罪行为操作规程 | `fagui/xianchang-zhizhi-guicheng.html` |
| 其他日常巡逻与安保规范 | `fagui/qita-xiangguan-guifan.html` |

### 执法规范文章模板

执法规范文章依次包含：适用情形、有效法律依据、法定条件、程序步骤、参考表达、权利保障、常见错误、条文原文入口、相关模块。

参考表达必须标明“示例而非唯一固定话术”。不得把表明身份、警告、口头传唤、强制传唤或使用警械错误设计成所有情形都必须逐级经过的固定流程。

法律法规库维护法规版本、效力状态、公布或修订日期、施行日期、相关条款和官方全文入口。其他模块只做交叉引用，避免复制条文后发生版本漂移。

## 2.6 教育培训 `zoufang/`（13篇）

原“走访送教”统一更名为“教育培训”。

### 规章制度（5篇）

| 三级文章 | 文件 |
|---|---|
| 人民警察内务规范 | `zoufang/neiwu-tiaoling.html` |
| 纪律要求 | `zoufang/jilv-yaoqiu.html` |
| 保密与信息安全 | `zoufang/baomi-xinxi-anquan.html` |
| 涉酒及违规宴请管理要求 | `zoufang/shejiu-yanqing-guanli.html` |
| 执法记录和工作资料管理 | `zoufang/zhifa-jilu-ziliao-guanli.html` |

### 考核规范（4篇）

| 三级文章 | 文件 |
|---|---|
| 体能考核要求 | `zoufang/tineng-kaohe.html` |
| 基础警务技能考核 | `zoufang/jichu-jingwu-kaohe.html` |
| 小组协同技能考核 | `zoufang/xiaozu-xietong-kaohe.html` |
| 考核安全、记录与补测 | `zoufang/kaohe-anquan-buce.html` |

本地单位和市局考核数值只引用知识库中的正式材料。找不到正式材料时，不得使用其他地区录用测评标准冒充常州单位内部考核标准。

### 学习课程（4篇）

| 三级文章 | 文件 |
|---|---|
| 单位优秀课程 | `zoufang/danwei-youxiu-kecheng.html` |
| 市局优秀课程 | `zoufang/shiju-youxiu-kecheng.html` |
| 创新训练方法 | `zoufang/chuangxin-xunlian-fangfa.html` |
| 课程资料使用与交流规范 | `zoufang/kecheng-ziliao-jiaoliu.html` |

### 教育培训文章模板

教育培训文章依次包含：学习目标、制度或课程依据、核心内容、执行要求、禁止性事项、自查或考核、常见问题、正式文件入口。

---

## 3. 内容来源与事实校验

本次采用“一次性补全全部内容”路线。内容来源按以下优先级处理：

1. `F:\frank第二大脑\frank知识库` 中与主题直接相关的正式材料；
2. 全国人大、中国政府网、司法部、公安部、国家卫健委等国家机关公开文件；
3. 江苏省、常州市及其他公安机关公开发布的规范、工作指南和案例；
4. 其他政府部门、学校、行业机构发布的公开辅助资料。

不得把自媒体文章、无署名培训资料、搜索结果摘要或 AI 自动生成文字作为事实依据。知识库内容与现行法律冲突时，采用当前有效官方文本，并在实施报告中列出调整。

### 3.1 必须核对的时效事项

- 2025年修订的《中华人民共和国治安管理处罚法》自2026年1月1日起施行。旧页面不得继续套用修订前条号和程序说明。官方入口：<https://www.npc.gov.cn/npc/c2/c30834/202506/t20250627_446235.html>
- 《公安机关人民警察训练条令》自2025年1月1日起施行，2014年版本同时废止。官方入口：<https://www.moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/202510/t20251021_526539.html>
- 大型赛事和演唱会应以《大型群众性活动安全管理条例》为基础，并区分预计参加人数达到1000人的大型群众性活动与场馆日常经营活动。官方入口：<https://xzfg.moj.gov.cn/front/law/detail?LawID=204&Query=%E5%A4%A7%E5%9E%8B%E7%BE%A4%E4%BC%97%E6%80%A7%E6%B4%BB%E5%8A%A8%E5%AE%89%E5%85%A8%E7%AE%A1%E7%90%86%E6%9D%A1%E4%BE%8B>
- 精神障碍类警情以《中华人民共和国精神卫生法》规定的医疗诊断、监护人协同和人身安全保护边界为基础。官方入口：<https://www.nhc.gov.cn/fzs/c100048/201808/5d03e37b37c944b08d701a0b5722160a.shtml>
- 涉爆内容以《民用爆炸物品安全管理条例》等有效公开规定为法律背景，只写识别异常、隔离风险、疏散群众、立即报告和等待专业力量等安全原则。官方入口：<https://xzfg.moj.gov.cn/front/law/detail?LawID=165&Query=>
- 内务规范使用公安部令第161号《公安机关人民警察内务条令》。官方入口：<https://www.gov.cn/gongbao/content/2022/content_5671112.htm>
- 涉酒规定可引用公安机关公开发布的《公安部关于严禁违规宴请饮酒的规定》及解释，但不得自行扩展地方或单位处分标准。公开入口：<https://gaj.sjz.gov.cn/columns/0a9c92b2-97b8-4284-9bd7-6240c789c0bf/202204/29/1c7b0edf-6eec-4110-a397-d1a4828b68d4.html>

### 3.2 内容清单

新增 `data/content-inventory.json`，作为内容库存和检查依据，不用于运行时动态生成网站。每条记录至少包含：

```json
{
  "module": "zhuangbei",
  "module_title": "装备介绍",
  "category": "人身装备",
  "title": "九小件概览",
  "slug": "jiuxiaojian-gailan",
  "path": "zhuangbei/jiuxiaojian-gailan.html",
  "source_files": [],
  "public_sources": [],
  "images": [],
  "related_pages": []
}
```

该清单用于核对三级结构、页面数量、搜索覆盖、图片路径和交叉引用，不设置“完成状态”或“保密审核状态”门槛。

### 3.3 页面来源展示

每篇三级文章应提供资料来源区，至少显示：来源标题、发布机构或知识库文件名、链接或本地相对说明、核验日期。法律文章额外显示效力状态和施行日期。

来源区用于读者核对，不要求把知识库中的每一段文字逐句标注脚注。

---

## 4. 图片规范

允许使用：

- 知识库 `06_Assets/` 中的图片；
- 政府公开资料中的图片；
- 网上开放许可素材；
- 自行绘制的示意图；
- 能够展示内部部署、装备配置细节或处置站位的现场照片。

实施要求：

1. 外部图片下载到项目 `img/`，不得热链。
2. 推荐路径为 `img/<模块>/<文章slug>/文件名`。
3. 每张图片在 `data/content-inventory.json` 中记录来源或本地文件来源。
4. 开放许可图片记录许可类型和来源链接。
5. 图片必须有准确的 `alt` 文本和必要图注。
6. 仅对明显无关的身份证号、电话号码等个人信息进行必要处理；不执行专项保密筛查。
7. 找不到合适图片时，允许自行绘制示意图或采用完整的无图版式，不得使用破损占位图或来源不明图片凑数。

---

## 5. 页面与导航设计

## 5.1 目录和URL

- 六个现有模块目录保持不变，只修改显示名称。
- 每个模块的 `index.html` 展示二级分类和对应三级文章。
- 不建立二级分类子目录，避免形成第四层URL。
- 二级分类标题必须有稳定锚点，例如：

```html
<section id="vehicle-equipment" class="article-group">
```

- 三级文章返回模块索引时应链接到所属分类锚点。

## 5.2 三级文章公共结构

每篇三级文章必须包含：

- 面包屑：一级模块 → 二级分类 → 当前文章；
- 页面标题、摘要和标签；
- 对应类型的正文模板；
- 图片、示意图或完整无图版式；
- 相关装备、训练、警情和法规；
- 资料来源；
- 上一篇、下一篇；
- 返回所属二级分类的链接。

## 5.3 首页

首页只显示六张主模块卡片。每张卡片展示：

- 一级模块名称；
- 二级分类数量；
- 三级文章总数；
- 二级分类摘要；
- 进入模块的明确入口。

删除“巡防入门指南”卡片。“本月精选”首页区域和导航特殊入口继续保留。

## 5.4 导航

修改 `js/nav.js` 的模块配置为：

```javascript
var MODULES = [
    { name: '装备介绍', path: 'zhuangbei/index.html', emoji: '🛡️' },
    { name: '勤务保障', path: 'qinwu/index.html', emoji: '📋' },
    { name: '警务训练', path: 'xunlian/index.html', emoji: '⚔️' },
    { name: '警情处置', path: 'jingqing/index.html', emoji: '🚨' },
    { name: '执法规范', path: 'fagui/index.html', emoji: '📕' },
    { name: '教育培训', path: 'zoufang/index.html', emoji: '🎓' },
    { name: '本月精选', path: 'meiyueyixue/index.html', emoji: '⭐', special: true }
];
```

遵循项目既有 JavaScript 风格：四空格缩进、单引号、分号和旧脚本中的 `var`。

## 5.5 样式

优先复用 `css/style.css` 的现有组件。仅在缺少下列能力时增加样式：

- 二级分类锚点导航；
- 文章来源区；
- 相关文章卡片；
- 图片说明和图集；
- 移动端分类导航。

不得为每个模块建立独立样式文件，不引入前端框架。

---

## 6. 登录密码

用户名继续使用 `xunfang`，通用密码改为 `XFbk150225`。

`js/auth-core.js` 使用 `SHA-256(username + ':' + password)`。因此 `js/auth-config.js` 中的摘要必须更新为：

```text
9329591fc43f75b2fb1a0aec5977e1ce20658b79ddb6a2e1d623af25af8593e7
```

该摘要对应：

```text
SHA-256("xunfang:XFbk150225")
```

源码只保存摘要，不新增明文密码常量。旧 Cookie 因摘要变化自然失效。更新认证测试，至少验证：

- 新凭据生成的摘要与配置一致；
- 任意旧密码生成的摘要与配置不一致；
- Cookie 仍保持既有一天有效期、路径和 SameSite 行为。

---

## 7. 搜索索引

现有 `parse_html.py` 用于生成微信小程序数据，本次不得运行或修改它，以免影响 `miniprogram/`。

新增 `tools/build_search_index.py`：

1. 扫描六个网站模块目录和“本月精选”；
2. 排除模块索引、认证页、删除页和静态跳转页；
3. 提取标题、一级模块、二级分类、摘要、关键词和路径；
4. 生成 `search-index.json`；
5. 对重复标题、重复路径和缺少摘要输出错误或警告；
6. 使用稳定排序，重复执行不产生无意义差异；
7. 支持 `--check`，在索引与页面不一致时返回非零状态。

同步更新 `js/search.js` 中的模块目录和显示名称逻辑，确保六个模块及本月精选均可搜索。

---

## 8. 旧内容迁移与删除

### 8.1 迁移规则

- 路径和主题均适用：保留原文件并按新模板补全。
- 内容适用但分类改变：迁移或改名，更新所有站内链接。
- 旧路径可能被收藏：建立不参与导航和搜索的静态跳转页。
- 内容重复或被新文章完整取代：删除旧正文，只保留必要跳转。
- 法条内容集中到“执法规范”，其他模块只做交叉引用。
- 现有文章中可复用的图片和段落必须先核对主题，不得因批量改名造成标题与正文不一致。

新增 `data/legacy-url-map.json`，记录旧URL、新URL和处理方式，供链接检查和交付报告使用。

### 8.2 删除巡防入门指南

删除范围包括：

- `rumen/` 目录及页面；
- 首页“入门指南”卡片；
- `js/nav.js` 中的入口；
- `search-index.json` 中的记录；
- `.generated-learning-pages.json` 中的记录；
- `data/learning-modules.json` 中的 `rumen` 模块；
- 只服务于该模块的生成逻辑和测试断言。

删除前检查五篇入门内容是否能作为“教育培训”的资料来源。可复用内容先重写到教育培训新文章，再删除原页。

---

## 9. 实施顺序

Claude Code 应按以下批次实施，每批完成后运行相关测试并创建聚焦提交。

### 批次1：基线与清单

1. 阅读根目录 `AGENTS.md` 和知识库适用说明。
2. 记录 `git status`、当前分支和最近提交。
3. 运行现有测试并保存基线结果。
4. 盘点全部HTML、图片、搜索记录和知识库资料。
5. 创建 `data/content-inventory.json` 和 `data/legacy-url-map.json`。

### 批次2：认证和三级页面骨架

1. 修改密码摘要和认证测试。
2. 更新首页六张主模块卡片。
3. 更新导航模块名称。
4. 更新六个模块索引页的二级分类骨架。
5. 添加公共文章来源、相关文章、分类锚点和图集样式。

### 批次3：装备介绍与勤务保障

1. 完成26篇装备文章。
2. 将伸缩警棍、催泪喷射器、手铐装备内容合并进九小件概览。
3. 完成13篇勤务文章。
4. 配置两模块图片、来源和交叉引用。

### 批次4：警务训练与警情处置

1. 完成13篇训练文章。
2. 完成5篇警情文章。
3. 检查训练与警情内容没有不必要重复。
4. 配置图片、专业协同提示和法规链接。

### 批次5：执法规范与教育培训

1. 完成17篇执法规范文章。
2. 核验法律效力、版本、日期和条号。
3. 完成13篇教育培训文章。
4. 本地考核数值只使用知识库正式材料。
5. 建立全站法规交叉引用。

### 批次6：搜索、迁移和清理

1. 创建并运行搜索索引生成工具。
2. 完成旧URL跳转映射。
3. 迁移可复用入门内容。
4. 删除 `rumen/` 及全部引用。
5. 确认 `miniprogram/` 无差异。

### 批次7：全站验收

1. 运行自动测试和断链检查。
2. 桌面端与移动端浏览器验收。
3. 修复控制台错误、溢出、图片比例和导航问题。
4. 生成交付报告和验收截图。

---

## 10. 自动测试与检查

新增或更新测试，覆盖：

- 六个一级模块名称和目录准确；
- 每个模块索引只出现本规格确认的二级分类；
- `content-inventory.json` 恰好包含87篇三级文章；
- 每篇清单文章均有对应HTML文件；
- 每个三级页面都有“一级模块 → 二级分类 → 当前文章”面包屑；
- 每个页面都有标题、摘要、正文、来源区和相关文章区；
- 所有内部链接无404；
- 图片引用文件真实存在且有 `alt`；
- 搜索索引覆盖87篇文章且不包含 `rumen/`；
- 导航、首页和搜索中不出现旧模块名称；
- 新密码摘要正确；
- `miniprogram/` 没有任何改动；
- HTML中不存在“内容整改中”“待补充”“TODO”等占位文字。

新增 `tools/check_site_links.py`，检查HTML中的站内链接、锚点、图片、脚本和样式路径。该工具应跳过外部URL的网络可用性检查，但验证URL格式。

建议执行：

```powershell
node --test tests/auth_core.test.js
python -m unittest discover -s tests -p "test_*.py"
python tools/build_search_index.py --check
python tools/check_site_links.py
git diff --check
git diff --exit-code -- miniprogram
```

若仓库环境要求使用指定Python或Node运行时，应优先使用项目说明中的运行时，不在仓库内临时安装依赖。

---

## 11. 浏览器验收

通过本地HTTP服务器检查，不直接用 `file://` 代替真实加载环境。

至少覆盖：

- 1440×900桌面视口；
- 390×844手机视口；
- 登录、退出和旧登录状态失效；
- 首页六张模块卡片；
- 六个模块索引及20个二级分类；
- 每个模块抽查不同模板类型的三级文章；
- 分类锚点、上一篇、下一篇和交叉引用；
- 图片加载、图注和窄屏缩放；
- 按模块名、装备名、警情名和法规名搜索；
- 浏览器控制台无错误。

最终验收需保存首页、六个模块索引和具有代表性的三级文章桌面端/移动端截图。

---

## 12. 异常处理

- 官方网页暂时无法访问：使用同一文件的其他政府站点公开版本，并在来源记录中保留原发布机关。
- 知识库与现行法律冲突：采用现行法律，在实施报告中列出调整。
- 找不到合适图片：自行绘制示意图或使用完整无图版式，不保留破损占位图。
- 无法确认单位或市局考核数值：仅写能够确认的原则和项目，不用外地标准冒充本地标准。
- 原页面存在可疑或过时结论：重写相关段落，不为保留旧内容而牺牲准确性。
- 自动生成工具会修改 `miniprogram/`：停止使用该工具，恢复为只处理网站范围的实现。
- 工作区存在用户未提交改动：不得覆盖或清理，先识别重叠范围并采取最小修改。

---

## 13. Git提交建议

使用聚焦的 Conventional Commit：

1. `docs: add site content rebuild inventory`
2. `feat: update site authentication password`
3. `feat: establish three-level site navigation`
4. `feat: rebuild equipment and duty content`
5. `feat: rebuild training and incident content`
6. `feat: rebuild legal and education content`
7. `feat: regenerate search and migrate legacy pages`
8. `test: add site structure and link validation`
9. `fix: resolve final responsive and content issues`

每个提交前运行与该批次相关的测试。不得把87篇文章、工具、样式和删除操作压成一个不可审查提交。

---

## 14. 最终交付物

Claude Code 完成实施后应交付：

1. 网站源码改动；
2. 87篇三级文章清单；
3. 知识库与公开资料来源清单；
4. 图片来源清单；
5. 旧页面迁移与跳转映射；
6. 自动测试结果；
7. 全站断链报告；
8. 桌面端与移动端验收截图；
9. `miniprogram/` 未修改确认；
10. 已知但不阻塞上线的问题列表。

---

## 15. 完成定义

只有同时满足以下条件，实施才算完成：

- 通用密码已改为 `XFbk150225`，新凭据测试通过；
- 网站显示六个主模块和20个二级分类；
- 87篇三级文章全部存在并具有实质正文；
- 伸缩警棍、催泪喷射器和手铐不再作为独立装备介绍文章；
- “巡防入门指南”已从网站内容、导航、首页和搜索中移除；
- 图片无破损链接，外部图片已本地化；
- 法律文章使用当前有效版本并提供官方入口；
- 全站交叉引用和搜索正常；
- 自动测试、断链检查和浏览器验收通过；
- 微信小程序没有改动；
- 最终报告和验收截图齐全。
