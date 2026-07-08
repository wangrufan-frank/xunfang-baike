# 搜索功能实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现客户端 JSON 索引 + 纯 JS 中文关键词搜索，覆盖全部 51 篇文章。

**Architecture:** 预建 `search-index.json` 存储所有文章元数据，`search.js` 加载后做内存关键词匹配。首页搜索框实时下拉展示结果，`search.html` 展示完整搜索结果。

**Tech Stack:** 纯静态 HTML/CSS/JS，零依赖。

## Global Constraints

- 零外部依赖，纯静态文件
- GitHub Pages 部署兼容
- 中文子串匹配，大小写不敏感
- 200ms 输入防抖
- 下拉面板最多 8 条结果
- 搜索不可用时静默降级，不阻塞页面

---

### Task 1: 搜索索引数据文件

**Files:**
- Create: `search-index.json`

**Interfaces:**
- Produces: JSON 数组，每条 `{title, module, path, desc, tags, keywords}`

- [ ] **Step 1: 创建 search-index.json**

```json
[
  {
    "title": "催泪喷射器",
    "module": "装备介绍",
    "path": "zhuangbei/cuilei-pensheqi.html",
    "desc": "非杀伤性驱逐警械，3-6米射程，喷移问三字口诀",
    "tags": ["非杀伤性驱逐警械", "催泪喷射器", "警械使用"],
    "keywords": ["辣椒水", "喷射器", "驱逐警械", "喷移问"]
  },
  {
    "title": "防割手套",
    "module": "装备介绍",
    "path": "zhuangbei/fangge-shoutao.html",
    "desc": "防护类装备，防割不防刺，使用场景与维护要点",
    "tags": ["防护类装备", "防割手套", "防割不防刺"],
    "keywords": ["手套", "防割", "防护"]
  },
  {
    "title": "警械使用警告用语",
    "module": "装备介绍",
    "path": "zhuangbei/jingxie-jinggao.html",
    "desc": "法定前置程序，警告无效方可使用警械，标准16字用语",
    "tags": ["法定前置程序", "警械警告", "16字用语"],
    "keywords": ["警告", "警告语", "前置程序", "警械条例"]
  },
  {
    "title": "九小件概览",
    "module": "装备介绍",
    "path": "zhuangbei/jiuxiaojian-gailan.html",
    "desc": "9件标准单警装备配备标准，贴身紧靠方便拿取",
    "tags": ["9件标准装备", "单警装备", "配备标准"],
    "keywords": ["九小件", "单警", "装备配备", "八大件"]
  },
  {
    "title": "手铐",
    "module": "装备介绍",
    "path": "zhuangbei/shoukao.html",
    "desc": "约束性警械，六种上铐方法，武力链条第四环节",
    "tags": ["约束性警械", "上铐", "武力链条"],
    "keywords": ["手铐", "铐", "上铐", "约束", "背铐"]
  },
  {
    "title": "执法记录仪",
    "module": "装备介绍",
    "path": "zhuangbei/zhifa-jiuyi.html",
    "desc": "证据固定类装备，全程记录执法过程，证据与武力链条保障",
    "tags": ["证据固定类装备", "执法记录仪", "全程记录"],
    "keywords": ["记录仪", "录像", "取证", "执法记录"]
  },
  {
    "title": "伸缩警棍",
    "module": "装备介绍",
    "path": "zhuangbei/shensuo-jinggun.html",
    "desc": "驱逐性警械，伸长约52cm，击打部位、戒备姿势与操作流程",
    "tags": ["驱逐性警械", "伸缩警棍", "警械使用"],
    "keywords": ["警棍", "甩棍", "开棍", "劈击", "戒备"]
  },
  {
    "title": "处置预案与分级响应",
    "module": "巡防勤务",
    "path": "qinwu/chuzhi-yuan.html",
    "desc": "预案体系，三级响应机制，力量部署与现场管控策略",
    "tags": ["预案体系", "三级响应", "力量部署"],
    "keywords": ["预案", "分级响应", "应急处置", "力量部署"]
  },
  {
    "title": "胡搅蛮缠人员控制带离",
    "module": "巡防勤务",
    "path": "qinwu/kongzhi-daili.html",
    "desc": "四类特征识别，四人协作带离模式，隐私保护要点",
    "tags": ["控制带离", "四人协作", "特征识别"],
    "keywords": ["胡搅蛮缠", "带离", "控制", "闹事"]
  },
  {
    "title": "涉稳警情演练要点",
    "module": "巡防勤务",
    "path": "qinwu/shewen-yanlian.html",
    "desc": "涉稳叠加自残警情演练，谈判切换时机与多部门协同",
    "tags": ["涉稳警情", "演练", "谈判切换"],
    "keywords": ["涉稳", "演练", "自残", "谈判", "协同"]
  },
  {
    "title": "校园与金融机构安保",
    "module": "巡防勤务",
    "path": "qinwu/xiaoyuan-jinrong.html",
    "desc": "情景植入式培训，校园四大模块与金融机构防暴要点",
    "tags": ["场景执法", "校园安保", "金融安保"],
    "keywords": ["校园", "金融", "银行", "学校", "安保"]
  },
  {
    "title": "宣传取证操作规范",
    "module": "巡防勤务",
    "path": "qinwu/xuanchuan-quzheng.html",
    "desc": "全息记录规范，证据链保全，法律宣传与取证装备清单",
    "tags": ["取证与舆情", "全息记录", "证据链"],
    "keywords": ["宣传", "取证", "证据", "拍照", "摄像"]
  },
  {
    "title": "演唱会安保执法要点",
    "module": "巡防勤务",
    "path": "qinwu/yanchanghui-zhifa.html",
    "desc": "假票倒票快速带离，便衣与制服结合，音乐节专项执法",
    "tags": ["场景执法", "演唱会", "快速带离"],
    "keywords": ["演唱会", "音乐节", "假票", "倒票", "黄牛"]
  },
  {
    "title": "舆情导控要点",
    "module": "巡防勤务",
    "path": "qinwu/yuqing-daokong.html",
    "desc": "被拍摄意识，画面管理，三规范防火墙与舆情导控",
    "tags": ["取证与舆情", "被拍摄意识", "舆情导控"],
    "keywords": ["舆情", "拍摄", "导控", "媒体"]
  },
  {
    "title": "舆情管控与战术分析",
    "module": "巡防勤务",
    "path": "qinwu/yuqing-zhanshu.html",
    "desc": "被拍摄意识，处置力度平衡，音视频防线建设",
    "tags": ["战术与舆情", "被拍摄意识", "力度平衡"],
    "keywords": ["舆情", "战术", "拍摄", "音视频", "力度"]
  },
  {
    "title": "盾叉协同战术",
    "module": "警务训练",
    "path": "xunlian/duncha-xietong.html",
    "desc": "核心协同战法，盾牌手加抓捕叉手，刀斧砍杀五步处置",
    "tags": ["核心协同战法", "盾叉协同", "刀斧砍杀"],
    "keywords": ["盾牌", "抓捕叉", "协同", "刀斧", "砍杀"]
  },
  {
    "title": "盾牌技术",
    "module": "警务训练",
    "path": "xunlian/dunpai-jishu.html",
    "desc": "法式盾牌持盾戒备姿势（高贴收挺），六种运用场景",
    "tags": ["法式盾牌", "持盾戒备", "盾牌技术"],
    "keywords": ["盾牌", "法式盾牌", "持盾", "撞击", "防护"]
  },
  {
    "title": "概述与编成",
    "module": "警务训练",
    "path": "xunlian/gaishu-biancheng.html",
    "desc": "3人制警组标准定义，三级装备体系，安全三要素与加一理念",
    "tags": ["3人制警组", "三级装备", "安全理念"],
    "keywords": ["编成", "警组", "三人", "编制", "装备体系"]
  },
  {
    "title": "概述与基本原则",
    "module": "警务训练",
    "path": "xunlian/gaishu-yuanze.html",
    "desc": "核心理念，软硬兼施，四大能力，三重点与三要素",
    "tags": ["核心理念", "软硬兼施", "安全三要素"],
    "keywords": ["原则", "理念", "四大能力", "三重点"]
  },
  {
    "title": "抓握解脱与防御",
    "module": "警务训练",
    "path": "xunlian/jietuo-fangyu.html",
    "desc": "四大解脱技术，十字防御与潜水推击",
    "tags": ["防卫解脱", "十字防御", "潜水推击"],
    "keywords": ["解脱", "抓握", "防御", "十字", "潜水"]
  },
  {
    "title": "警棍与抓捕叉",
    "module": "警务训练",
    "path": "xunlian/jinggun-zhuabucha.html",
    "desc": "中远距离控制，长警棍加抓捕叉，六字诀两快一准",
    "tags": ["中远距离控制", "长警棍", "抓捕叉"],
    "keywords": ["长警棍", "抓捕叉", "戳击", "插锁", "胸叉"]
  },
  {
    "title": "抱臂折腕控制",
    "module": "警务训练",
    "path": "xunlian/kongzhi-jishu.html",
    "desc": "反关节控制技术，抱臂控制与折腕控制二级递进",
    "tags": ["控制技术", "反关节", "二级递进"],
    "keywords": ["抱臂", "折腕", "控制", "反关节", "擒拿"]
  },
  {
    "title": "盘查规范流程",
    "module": "警务训练",
    "path": "xunlian/pancha-liucheng.html",
    "desc": "六步法标准处置程序，表明身份到强制传唤递进逻辑",
    "tags": ["六步法", "盘查", "标准程序"],
    "keywords": ["盘查", "六步法", "查验", "传唤", "身份证"]
  },
  {
    "title": "十字防御技能",
    "module": "警务训练",
    "path": "xunlian/shizi-fangyu.html",
    "desc": "徒手防卫肌肉记忆训练，130°夹角十字防御与潜水推击",
    "tags": ["徒手防卫", "肌肉记忆", "十字防御"],
    "keywords": ["十字", "防御", "徒手", "潜水推击", "格挡"]
  },
  {
    "title": "四能力与安全三要素",
    "module": "警务训练",
    "path": "xunlian/sinengli-yaosu.html",
    "desc": "现场操作核心，看找分退四字诀，危险加一理念",
    "tags": ["现场操作核心", "四能力", "危险加一"],
    "keywords": ["四能力", "安全三要素", "看找分退", "危险加一"]
  },
  {
    "title": "俯卧式搜身带离",
    "module": "警务训练",
    "path": "xunlian/soushen-daili.html",
    "desc": "搜身五步与别臂带离五步，控制带离教学重点",
    "tags": ["控制带离", "搜身五步", "别臂带离"],
    "keywords": ["搜身", "带离", "俯卧", "别臂"]
  },
  {
    "title": "武力升级与三防训练",
    "module": "警务训练",
    "path": "xunlian/wuli-shengji-sanfang.html",
    "desc": "五级武力升级模型，三防概念（刀斧砍杀、车辆冲撞、纵火爆炸）",
    "tags": ["武力升级", "三防训练", "比例原则"],
    "keywords": ["武力升级", "三防", "刀斧", "冲撞", "爆炸"]
  },
  {
    "title": "武力升级与法律依据",
    "module": "警务训练",
    "path": "xunlian/wuli-shengji.html",
    "desc": "比例原则，四级递进模型（口头→徒手→警械→武器）",
    "tags": ["比例原则", "四级递进", "警告前置"],
    "keywords": ["武力升级", "法律依据", "四级", "比例", "警告"]
  },
  {
    "title": "训练教学法",
    "module": "警务训练",
    "path": "xunlian/xunlian-jiaoxuefa.html",
    "desc": "五步教学法，游戏化教学，红蓝对抗三级递进",
    "tags": ["五步教学法", "游戏化教学", "红蓝对抗"],
    "keywords": ["教学法", "训练", "五步", "游戏化", "红蓝对抗"]
  },
  {
    "title": "战术站位与装备应用",
    "module": "警务训练",
    "path": "xunlian/zhanshu-zhanwei-xunluo.html",
    "desc": "三大阵型（三角/四角/五人分割站位），三大装备类突发处置",
    "tags": ["战术站位", "三大阵型", "装备应用"],
    "keywords": ["站位", "三角", "四角", "五人", "阵型"]
  },
  {
    "title": "战术配合与站位",
    "module": "警务训练",
    "path": "xunlian/zhanshu-zhanwei.html",
    "desc": "组合式与夹击式站位，战术配合三大支柱，攻防一体",
    "tags": ["组合式站位", "夹击式站位", "战术配合"],
    "keywords": ["战术", "配合", "站位", "组合", "夹击"]
  },
  {
    "title": "主动横移压缩空间战法",
    "module": "警务训练",
    "path": "xunlian/zhudong-hengyi.html",
    "desc": "核心战法，四步压缩，应对逃跑和追砍群众的专项战法",
    "tags": ["核心战法", "横移压缩", "四步压缩"],
    "keywords": ["横移", "压缩空间", "战法", "主动"]
  },
  {
    "title": "持刀类警情处置（标准版）",
    "module": "警情处置",
    "path": "jingqing/chidao-jingqing.html",
    "desc": "梯次化模块化处置，5人小组三阶段策应，7步完整流程",
    "tags": ["梯次化", "模块化", "5人小组"],
    "keywords": ["持刀", "刀", "警情", "砍杀", "小组"]
  },
  {
    "title": "持刀类警情处置（快反版）",
    "module": "警情处置",
    "path": "jingqing/chidao-leiqing.html",
    "desc": "高风险持刀警情快速处置，安全距离≥5米，疏散稳控到移交恢复",
    "tags": ["高风险", "持刀警情", "快速处置"],
    "keywords": ["持刀", "刀", "快反", "安全距离", "高风险"]
  },
  {
    "title": "打架斗殴警情处置",
    "module": "警情处置",
    "path": "jingqing/dajia-douou.html",
    "desc": "5步处置流程，控制场面→分别隔离→伤情评估→询问取证→调解移交",
    "tags": ["中风险", "打架斗殴", "5步处置"],
    "keywords": ["打架", "斗殴", "纠纷", "调解", "治安"]
  },
  {
    "title": "135机制与响应流程",
    "module": "警情处置",
    "path": "jingqing/jizhi-liucheng.html",
    "desc": "1·3·5分钟圈层响应机制，屯警街面，七步作业链",
    "tags": ["核心机制", "135机制", "圈层响应"],
    "keywords": ["135", "响应", "机制", "圈层", "屯警"]
  },
  {
    "title": "可疑车辆盘查",
    "module": "警情处置",
    "path": "jingqing/keyi-cheliang.html",
    "desc": "高风险车辆盘查，安全距离7米，人员分离与车辆搜查",
    "tags": ["高风险", "车辆盘查", "人员分离"],
    "keywords": ["车辆", "盘查", "截停", "查车", "可疑车辆"]
  },
  {
    "title": "人员盘查",
    "module": "警情处置",
    "path": "jingqing/renyuan-pancha.html",
    "desc": "六步法人员盘查，语言控制优先，表明身份到强制传唤",
    "tags": ["六步法", "人员盘查", "语言控制"],
    "keywords": ["盘查", "身份证", "查验", "传唤"]
  },
  {
    "title": "醉酒闹事警情处置",
    "module": "警情处置",
    "path": "jingqing/zuijiu-naoshi.html",
    "desc": "中风险醉酒警情，保护性约束，安全距离≥2米，5步处置",
    "tags": ["中风险", "醉酒", "保护性约束"],
    "keywords": ["醉酒", "酒", "闹事", "约束", "醒酒"]
  },
  {
    "title": "赌博类警情执法标准",
    "module": "法条规范",
    "path": "fagui/dubo-zhifa.html",
    "desc": "江苏省公安机关现场执法标准，警力不足先求援，立即分离防串供",
    "tags": ["执法标准", "赌博", "现场执法"],
    "keywords": ["赌博", "赌", "执法标准", "江苏"]
  },
  {
    "title": "法律与法言法语",
    "module": "法条规范",
    "path": "fagui/faly-fayanfayu.html",
    "desc": "五大执法依据，六级递进法言法语体系，武力使用宣告",
    "tags": ["执法依据", "法言法语", "六级递进"],
    "keywords": ["法言法语", "法律", "宣告", "递进", "依据"]
  },
  {
    "title": "法律依据与法言法语",
    "module": "法条规范",
    "path": "fagui/faly-yiju.html",
    "desc": "核心法律依据，四阶递进法言法语（表明身份→警告→传唤→强制）",
    "tags": ["核心法律依据", "四阶递进", "强制传唤"],
    "keywords": ["法律依据", "四阶", "传唤", "24小时", "48小时"]
  },
  {
    "title": "概念与法律依据",
    "module": "法条规范",
    "path": "fagui/gainian-falv.html",
    "desc": "第二级武力执法控制，武力对等原则，规范法言法语",
    "tags": ["基础理论", "第二级武力", "执法控制"],
    "keywords": ["概念", "武力", "对等", "执法控制"]
  },
  {
    "title": "视频图像管理系统条例",
    "module": "法条规范",
    "path": "fagui/shipin-tiaoli.html",
    "desc": "2025年条例，调取权限与隐私合规，记录仪管理规范",
    "tags": ["法规依据", "视频条例", "隐私合规"],
    "keywords": ["视频", "图像", "条例", "隐私", "监控", "摄像头"]
  },
  {
    "title": "治安管理处罚法与执法规范",
    "module": "法条规范",
    "path": "fagui/zhian-guifan.html",
    "desc": "新旧法对比，流程标准化，党建加执法规范化建设",
    "tags": ["法规依据", "治安管理", "执法规范"],
    "keywords": ["治安", "处罚法", "新旧", "党建", "规范化"]
  },
  {
    "title": "大型活动安保执法",
    "module": "走访送教",
    "path": "zoufang/daxing-huodong.html",
    "desc": "高舆情风险，演唱会音乐节体育赛事，四大执法能力贯穿",
    "tags": ["高舆情风险", "大型活动", "安保执法"],
    "keywords": ["大型活动", "演唱会", "赛事", "马拉松", "音乐节"]
  },
  {
    "title": "金融机构反恐防暴",
    "module": "走访送教",
    "path": "zoufang/jinrong-fankong.html",
    "desc": "资金密集场所特殊场景，夹击与分割战术，快反研训",
    "tags": ["特殊场景", "金融反恐", "夹击战术"],
    "keywords": ["金融", "银行", "反恐", "防暴", "分割"]
  },
  {
    "title": "现场处置执法规范",
    "module": "走访送教",
    "path": "zoufang/xianchang-chuzhi.html",
    "desc": "标准化模块化接处警规范，四组分工，三种战法",
    "tags": ["标准化模块化", "四组分工", "三种战法"],
    "keywords": ["现场处置", "接处警", "四组", "战法", "规范"]
  },
  {
    "title": "校园反恐防暴",
    "module": "走访送教",
    "path": "zoufang/xiaoyuan-fankong.html",
    "desc": "学生欺凌入法，三级装备，实战技能三层次与口诀",
    "tags": ["特殊场景", "校园反恐", "三级装备"],
    "keywords": ["校园", "反恐", "防暴", "学生", "欺凌"]
  },
  {
    "title": "校园安保与培训组织",
    "module": "走访送教",
    "path": "zoufang/xiaoyuan-peixun.html",
    "desc": "快反培训体系，蓝军建设，红蓝对抗与培训口诀",
    "tags": ["特殊场景", "校园培训", "蓝军建设"],
    "keywords": ["校园", "培训", "蓝军", "红蓝", "课程"]
  },
  {
    "title": "政治核心区处置",
    "module": "走访送教",
    "path": "zoufang/zhengzhi-hexinqu.html",
    "desc": "最高敏感度，群体性事件与极端案事件，四组联动舆情降级",
    "tags": ["最高敏感度", "四组联动", "舆情降级"],
    "keywords": ["政治核心区", "敏感", "群体", "极端", "四组"]
  }
]
```

- [ ] **Step 2: 验证 JSON 格式**

Run: `python -c "import json; json.load(open('F:/frank第二大脑/xunfang-baike/search-index.json', encoding='utf-8')); print('valid JSON,', len(json.load(open('F:/frank第二大脑/xunfang-baike/search-index.json', encoding='utf-8'))), 'entries')"`
Expected: `valid JSON, 51 entries`

- [ ] **Step 3: Commit**

```bash
git add search-index.json
git commit -m "feat: add search index with 51 article entries"
```

---

### Task 2: 搜索 CSS 样式

**Files:**
- Modify: `css/style.css` (追加样式)

**Interfaces:**
- Consumes: 现有 CSS 变量（`--bg`, `--card-bg`, `--text`, `--text-secondary`, `--text-muted`, `--accent-blue`, `--accent-red`, `--border`, `--shadow`, `--radius`, `--nav-bg`）
- Produces: `.search-dropdown`, `.search-result-item`, `.search-highlight`, `.search-more`, `.search-empty`, `.search-page` 等样式类

- [ ] **Step 1: 在 style.css 末尾追加搜索相关样式**

追加以下内容到 `css/style.css` 文件末尾：

```css
/* === 搜索下拉面板 === */
.search-dropdown {
  display: none;
  position: absolute;
  top: 100%;
  left: 16px;
  right: 16px;
  max-width: calc(var(--max-width) - 32px);
  margin: 4px auto 0;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  z-index: 200;
  max-height: 480px;
  overflow-y: auto;
}

.search-dropdown.open {
  display: block;
}

.search-result-item {
  display: block;
  padding: 14px 18px;
  border-bottom: 1px solid var(--bg);
  text-decoration: none;
  transition: background 0.1s;
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: var(--bg);
  text-decoration: none;
}

.search-result-item .result-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text);
  margin-bottom: 4px;
}

.search-result-item .result-module {
  display: inline-block;
  font-size: 11px;
  color: var(--text-muted);
  background: var(--bg);
  padding: 1px 8px;
  border-radius: 3px;
  margin-bottom: 4px;
}

.search-result-item .result-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
}

.search-highlight {
  color: var(--accent-red);
  font-weight: bold;
}

.search-more {
  display: block;
  text-align: center;
  padding: 12px;
  font-size: 13px;
  color: var(--accent-blue);
  border-top: 1px solid var(--bg);
  text-decoration: none;
}

.search-more:hover {
  background: var(--bg);
  text-decoration: none;
}

.search-empty {
  text-align: center;
  padding: 24px 18px;
  color: var(--text-muted);
  font-size: 14px;
}

.search-empty .empty-hint {
  font-size: 12px;
  margin-top: 6px;
  color: #bbb;
}

/* 搜索框下拉时的样式 */
.search-wrapper {
  position: relative;
  max-width: var(--max-width);
  margin: 20px auto;
  padding: 0 16px;
}

/* === 搜索结果全页 === */
.search-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px 60px;
}

.search-page .search-header {
  padding: 28px 0 20px;
  border-bottom: 2px solid var(--border);
  margin-bottom: 24px;
}

.search-page .search-query {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.search-page .search-query strong {
  color: var(--accent-red);
  font-size: 15px;
}

.search-page .search-count {
  font-size: 12px;
  color: var(--text-muted);
}

.search-page .result-card {
  display: block;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 22px;
  margin-bottom: 12px;
  box-shadow: var(--shadow);
  text-decoration: none;
  transition: border-color 0.15s;
}

.search-page .result-card:hover {
  border-color: var(--accent-red);
  text-decoration: none;
}

.search-page .result-card .card-title {
  font-size: 17px;
  font-weight: bold;
  color: var(--text);
  margin-bottom: 6px;
}

.search-page .result-card .card-module {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.search-page .result-card .card-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.search-page .result-card .card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 8px;
}

.search-page .back-link {
  display: inline-block;
  margin-top: 20px;
  font-size: 14px;
  color: var(--accent-blue);
}
```

- [ ] **Step 2: Commit**

```bash
git add css/style.css
git commit -m "style: add search dropdown and results page styles"
```

---

### Task 3: 搜索 JS 逻辑

**Files:**
- Create: `js/search.js`

**Interfaces:**
- Produces: 全局搜索功能，绑定首页搜索框 input/click/ESC 事件
- Consumes: `search-index.json`（fetch 加载）

- [ ] **Step 1: 创建 js/search.js**

```js
// js/search.js
(function() {
  var SEARCH_INDEX_URL = 'search-index.json';
  var DEBOUNCE_MS = 200;
  var MAX_DROPDOWN_RESULTS = 8;

  var searchIndex = null;
  var debounceTimer = null;
  var dropdownEl = null;
  var searchInput = null;
  var searchBar = null;
  var loaded = false;
  var loadError = false;

  // 判断当前页面深度
  function getDepth() {
    var path = window.location.pathname.replace(/\\/g, '/');
    var dirs = path.split('/').filter(function(d) { return d && d !== 'index.html'; });
    // 如果在子目录中（路径包含模块目录），depth=1
    var moduleDirs = ['zhuangbei','qinwu','xunlian','jingqing','fagui','zoufang','meiyueyixue'];
    for (var i = 0; i < moduleDirs.length; i++) {
      if (dirs.indexOf(moduleDirs[i]) !== -1) return 1;
    }
    return 0;
  }

  function getIndexUrl() {
    var depth = getDepth();
    return (depth === 0) ? SEARCH_INDEX_URL : ('../' + SEARCH_INDEX_URL);
  }

  function getSearchPageUrl() {
    var depth = getDepth();
    return (depth === 0) ? 'search.html' : '../search.html';
  }

  // 加载索引
  function loadIndex(callback) {
    if (searchIndex) { callback(); return; }
    if (loadError) { callback(new Error('load failed')); return; }

    var xhr = new XMLHttpRequest();
    xhr.open('GET', getIndexUrl(), true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          searchIndex = JSON.parse(xhr.responseText);
          loaded = true;
          callback();
        } catch(e) {
          loadError = true;
          callback(e);
        }
      } else {
        loadError = true;
        callback(new Error('HTTP ' + xhr.status));
      }
    };
    xhr.onerror = function() {
      loadError = true;
      callback(new Error('network error'));
    };
    xhr.send();
  }

  // 匹配分数计算
  function matchScore(item, queryLower) {
    var score = 0;
    var titleLower = item.title.toLowerCase();
    var descLower = item.desc.toLowerCase();

    if (titleLower.indexOf(queryLower) !== -1) score += 5;
    if (descLower.indexOf(queryLower) !== -1) score += 1;

    if (item.tags) {
      for (var i = 0; i < item.tags.length; i++) {
        if (item.tags[i].toLowerCase().indexOf(queryLower) !== -1) { score += 3; break; }
      }
    }

    if (item.keywords) {
      for (var i = 0; i < item.keywords.length; i++) {
        if (item.keywords[i].toLowerCase().indexOf(queryLower) !== -1) { score += 3; }
      }
    }

    return score;
  }

  // 高亮匹配文本
  function highlight(text, queryLower) {
    if (!queryLower) return escapeHtml(text);
    var escaped = escapeHtml(text);
    var idx = escaped.toLowerCase().indexOf(queryLower);
    if (idx === -1) return escaped;

    var prefix = escaped.substring(0, idx);
    var match = escaped.substring(idx, idx + queryLower.length);
    var suffix = escaped.substring(idx + queryLower.length);
    return prefix + '<span class="search-highlight">' + match + '</span>' + suffix;
  }

  function escapeHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  // 执行搜索
  function doSearch(query) {
    if (!query || query.trim().length === 0) {
      closeDropdown();
      return;
    }

    if (!searchIndex) {
      loadIndex(function(err) {
        if (err) return;
        doSearch(query);
      });
      return;
    }

    var queryLower = query.trim().toLowerCase();
    var scored = [];

    for (var i = 0; i < searchIndex.length; i++) {
      var s = matchScore(searchIndex[i], queryLower);
      if (s > 0) {
        scored.push({ item: searchIndex[i], score: s });
      }
    }

    scored.sort(function(a, b) { return b.score - a.score; });

    var results = scored.slice(0, MAX_DROPDOWN_RESULTS);
    var totalCount = scored.length;

    renderDropdown(results, totalCount, queryLower, query.trim());
  }

  // 渲染下拉面板
  function renderDropdown(results, totalCount, queryLower, rawQuery) {
    if (!dropdownEl) {
      dropdownEl = document.createElement('div');
      dropdownEl.className = 'search-dropdown';
      searchBar.appendChild(dropdownEl);

      // 点击外部关闭
      document.addEventListener('click', function(e) {
        if (dropdownEl && !dropdownEl.contains(e.target) && e.target !== searchInput) {
          closeDropdown();
        }
      });
    }

    if (results.length === 0) {
      dropdownEl.innerHTML =
        '<div class="search-empty">未找到相关内容' +
        '<div class="empty-hint">试试其他关键词，如"警棍""盘查""持刀"</div>' +
        '</div>';
    } else {
      var depth = getDepth();
      var prefix = (depth === 0) ? '' : '../';

      var itemsHtml = '';
      for (var i = 0; i < results.length; i++) {
        var item = results[i].item;
        itemsHtml +=
          '<a href="' + prefix + item.path + '" class="search-result-item">' +
            '<div class="result-title">' + highlight(item.title, queryLower) + '</div>' +
            '<span class="result-module">' + escapeHtml(item.module) + '</span>' +
            '<div class="result-desc">' + highlight(item.desc, queryLower) + '</div>' +
          '</a>';
      }

      if (totalCount > MAX_DROPDOWN_RESULTS) {
        itemsHtml += '<a href="' + getSearchPageUrl() + '?q=' + encodeURIComponent(rawQuery) + '" class="search-more">查看全部 ' + totalCount + ' 条结果 →</a>';
      }

      dropdownEl.innerHTML = itemsHtml;
    }

    dropdownEl.classList.add('open');
  }

  function closeDropdown() {
    if (dropdownEl) {
      dropdownEl.classList.remove('open');
    }
  }

  // 初始化
  function init() {
    searchInput = document.querySelector('.search-bar input');
    if (!searchInput) return;

    searchBar = searchInput.parentElement;
    // 给搜索栏加 wrapper 以便定位下拉面板
    searchBar.classList.add('search-wrapper');

    // 输入事件（防抖）
    searchInput.addEventListener('input', function() {
      clearTimeout(debounceTimer);
      var query = searchInput.value;
      debounceTimer = setTimeout(function() {
        loadIndex(function(err) {
          if (err) {
            // 索引加载失败，不影响正常使用
            return;
          }
          doSearch(query);
        });
      }, DEBOUNCE_MS);
    });

    // 回车跳转搜索结果页
    searchInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        var query = searchInput.value.trim();
        if (query) {
          window.location.href = getSearchPageUrl() + '?q=' + encodeURIComponent(query);
        }
      }
      if (e.key === 'Escape') {
        closeDropdown();
      }
    });

    // 聚焦时如果输入框有内容则重新搜索
    searchInput.addEventListener('focus', function() {
      if (searchInput.value.trim()) {
        doSearch(searchInput.value);
      }
    });

    // 预加载索引
    loadIndex(function() {});
  }

  // DOM ready 后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

- [ ] **Step 2: Commit**

```bash
git add js/search.js
git commit -m "feat: add client-side search logic with dropdown panel"
```

---

### Task 4: 搜索结果全页

**Files:**
- Create: `search.html`

**Interfaces:**
- Consumes: URL 参数 `?q=关键词`，`search-index.json`（fetch），`js/nav.js`（导航），`css/style.css`（样式），`js/search.js` 可复用但本页独立实现（内联）
- Produces: 完整搜索结果页面

- [ ] **Step 1: 创建 search.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>搜索结果 — 巡防百科</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body>

<div id="nav-placeholder"></div>

<div class="search-page">
  <div class="search-header">
    <div class="search-query">搜索：<strong id="query-text"></strong></div>
    <div class="search-count" id="result-count"></div>
  </div>
  <div id="result-list"></div>
  <a href="index.html" class="back-link">← 返回首页</a>
</div>

<script src="js/nav.js"></script>
<script>
(function() {
  // 解析 URL 参数
  function getParam(name) {
    var m = window.location.search.match(new RegExp('[?&]' + name + '=([^&]*)'));
    return m ? decodeURIComponent(m[1]) : '';
  }

  var query = getParam('q').trim();
  if (!query) {
    window.location.href = 'index.html';
    return;
  }

  document.getElementById('query-text').textContent = query;
  document.title = query + ' — 搜索结果 — 巡防百科';

  var queryLower = query.toLowerCase();

  function matchScore(item) {
    var score = 0;
    if (item.title.toLowerCase().indexOf(queryLower) !== -1) score += 5;
    if (item.desc.toLowerCase().indexOf(queryLower) !== -1) score += 1;
    if (item.tags) {
      for (var i = 0; i < item.tags.length; i++) {
        if (item.tags[i].toLowerCase().indexOf(queryLower) !== -1) { score += 3; break; }
      }
    }
    if (item.keywords) {
      for (var i = 0; i < item.keywords.length; i++) {
        if (item.keywords[i].toLowerCase().indexOf(queryLower) !== -1) { score += 3; }
      }
    }
    return score;
  }

  function escapeHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function highlight(text) {
    if (!queryLower) return escapeHtml(text);
    var escaped = escapeHtml(text);
    var idx = escaped.toLowerCase().indexOf(queryLower);
    if (idx === -1) return escaped;
    return escaped.substring(0, idx) +
      '<span class="search-highlight">' + escaped.substring(idx, idx + queryLower.length) + '</span>' +
      escaped.substring(idx + queryLower.length);
  }

  function render(articles) {
    var scored = [];
    for (var i = 0; i < articles.length; i++) {
      var s = matchScore(articles[i]);
      if (s > 0) scored.push({ item: articles[i], score: s });
    }
    scored.sort(function(a, b) { return b.score - a.score; });

    document.getElementById('result-count').textContent = '共找到 ' + scored.length + ' 条结果';

    var listEl = document.getElementById('result-list');
    if (scored.length === 0) {
      listEl.innerHTML =
        '<div class="search-empty">未找到与「' + escapeHtml(query) + '」相关的内容' +
        '<div class="empty-hint">试试其他关键词，如"警棍""盘查""持刀""武力升级"</div>' +
        '</div>';
      return;
    }

    var html = '';
    for (var i = 0; i < scored.length; i++) {
      var item = scored[i].item;
      html +=
        '<a href="' + item.path + '" class="result-card">' +
          '<div class="card-title">' + highlight(item.title) + '</div>' +
          '<div class="card-module">' + escapeHtml(item.module) + '</div>' +
          '<div class="card-desc">' + highlight(item.desc) + '</div>' +
          '<div class="card-tags">' +
            item.tags.map(function(t) { return '<span class="tag">' + highlight(t) + '</span>'; }).join('') +
          '</div>' +
        '</a>';
    }
    listEl.innerHTML = html;
  }

  // 加载索引并渲染
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'search-index.json', true);
  xhr.onload = function() {
    if (xhr.status === 200) {
      try {
        var data = JSON.parse(xhr.responseText);
        render(data);
      } catch(e) {
        document.getElementById('result-list').innerHTML =
          '<div class="search-empty">搜索索引加载失败，请稍后重试</div>';
      }
    } else {
      document.getElementById('result-list').innerHTML =
        '<div class="search-empty">搜索索引加载失败，请稍后重试</div>';
    }
  };
  xhr.onerror = function() {
    document.getElementById('result-list').innerHTML =
      '<div class="search-empty">搜索索引加载失败，请稍后重试</div>';
  };
  xhr.send();
})();
</script>

</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add search.html
git commit -m "feat: add search results full page"
```

---

### Task 5: 首页搜索框绑定

**Files:**
- Modify: `index.html`（引入 search.js，搜索框改写为 wrapper 结构）

**Interfaces:**
- Consumes: `js/search.js`（搜索逻辑）
- Produces: 搜索框支持实时下拉搜索

- [ ] **Step 1: 修改 index.html**

将 index.html 中的搜索栏 div：

```html
<div class="search-bar">
  <input type="search" placeholder="🔍  搜索警情、装备、法规...">
</div>
```

改为（placeholder 保持不变）：

```html
<div class="search-bar">
  <input type="search" placeholder="🔍  搜索警情、装备、法规...">
</div>
```

并在 `</body>` 前，在现有 script 标签之后添加一行：

```html
<script src="js/search.js"></script>
```

即 index.html 底部的 script 引入区域变为：

```html
<script src="meiyueyixue/data.js"></script>
<script src="js/monthly-hero.js"></script>
<script src="js/nav.js"></script>
<script src="js/main.js"></script>
<script src="js/search.js"></script>
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "feat: wire search box with search.js"
```

---

### Task 6: 各子页面引入搜索 JS

**Files:**
- Modify: 所有内容页面 HTML（约 55 个文件），在 `</body>` 前的 script 区域末尾添加 `<script src="../js/search.js"></script>`

**Interfaces:**
- Consumes: `js/search.js`（自动适配 ../ 路径）

- [ ] **Step 1: 批量修改所有子页面**

以下每个 HTML 文件的 `</body>` 前都有一组 script 标签（通常是 `<script src="../js/nav.js"></script>`），在最后一个 script 标签后、`</body>` 前添加 `<script src="../js/search.js"></script>`。

需要修改的文件列表（51 篇内容文章 + 7 个模块首页）：

**zhuangbei/ (7+1):**
- `zhuangbei/index.html`
- `zhuangbei/cuilei-pensheqi.html`
- `zhuangbei/fangge-shoutao.html`
- `zhuangbei/jingxie-jinggao.html`
- `zhuangbei/jiuxiaojian-gailan.html`
- `zhuangbei/shoukao.html`
- `zhuangbei/zhifa-jiuyi.html`
- `zhuangbei/shensuo-jinggun.html`

**qinwu/ (8+1):**
- `qinwu/index.html`
- `qinwu/chuzhi-yuan.html`
- `qinwu/kongzhi-daili.html`
- `qinwu/shewen-yanlian.html`
- `qinwu/xiaoyuan-jinrong.html`
- `qinwu/xuanchuan-quzheng.html`
- `qinwu/yanchanghui-zhifa.html`
- `qinwu/yuqing-daokong.html`
- `qinwu/yuqing-zhanshu.html`

**xunlian/ (17+1):**
- `xunlian/index.html`
- `xunlian/duncha-xietong.html`
- `xunlian/dunpai-jishu.html`
- `xunlian/gaishu-biancheng.html`
- `xunlian/gaishu-yuanze.html`
- `xunlian/jietuo-fangyu.html`
- `xunlian/jinggun-zhuabucha.html`
- `xunlian/kongzhi-jishu.html`
- `xunlian/pancha-liucheng.html`
- `xunlian/shizi-fangyu.html`
- `xunlian/sinengli-yaosu.html`
- `xunlian/soushen-daili.html`
- `xunlian/wuli-shengji-sanfang.html`
- `xunlian/wuli-shengji.html`
- `xunlian/xunlian-jiaoxuefa.html`
- `xunlian/zhanshu-zhanwei-xunluo.html`
- `xunlian/zhanshu-zhanwei.html`
- `xunlian/zhudong-hengyi.html`

**jingqing/ (7+1):**
- `jingqing/index.html`
- `jingqing/chidao-jingqing.html`
- `jingqing/chidao-leiqing.html`
- `jingqing/dajia-douou.html`
- `jingqing/jizhi-liucheng.html`
- `jingqing/keyi-cheliang.html`
- `jingqing/renyuan-pancha.html`
- `jingqing/zuijiu-naoshi.html`

**fagui/ (6+1):**
- `fagui/index.html`
- `fagui/dubo-zhifa.html`
- `fagui/faly-fayanfayu.html`
- `fagui/faly-yiju.html`
- `fagui/gainian-falv.html`
- `fagui/shipin-tiaoli.html`
- `fagui/zhian-guifan.html`

**zoufang/ (6+1):**
- `zoufang/index.html`
- `zoufang/daxing-huodong.html`
- `zoufang/jinrong-fankong.html`
- `zoufang/xianchang-chuzhi.html`
- `zoufang/xiaoyuan-fankong.html`
- `zoufang/xiaoyuan-peixun.html`
- `zoufang/zhengzhi-hexinqu.html`

**meiyueyixue/ (1):**
- `meiyueyixue/index.html`

对于每个文件，找到 `</body>` 前的最后一个 `<script>` 标签，在它下方添加一行：

```html
<script src="../js/search.js"></script>
```

（meiyueyixue/index.html 已有 `data.js` 引用，同样在 `</body>` 前添加 `<script src="../js/search.js"></script>`）

- [ ] **Step 2: Commit**

```bash
git add zhuangbei/ qinwu/ xunlian/ jingqing/ fagui/ zoufang/ meiyueyixue/
git commit -m "feat: add search.js to all content pages"
```

---

### Task 7: 端到端验证

- [ ] **Step 1: 本地启动服务器测试**

```bash
cd "F:\frank第二大脑\xunfang-baike" && python -m http.server 8080
```

然后访问 `http://localhost:8080` 进行以下测试：

- [ ] **Step 2: 测试下拉搜索**
  - 在搜索框输入"警棍"，确认下拉面板出现，显示伸缩警棍、警棍与抓捕叉等结果
  - 确认匹配关键词有高亮（红色加粗）
  - 点击结果，确认能正确跳转到文章页
  - 按 ESC 确认下拉面板关闭
  - 点击搜索框外部确认下拉面板关闭

- [ ] **Step 3: 测试回车跳转**
  - 输入"盘查"后按 Enter，确认跳转到 `search.html?q=盘查`
  - 搜索结果页确认显示人员盘查、可疑车辆盘查、盘查规范流程等
  - 点击结果确认能正确跳转

- [ ] **Step 4: 测试无结果**
  - 输入"xyz123"，确认下拉面板显示"未找到相关内容"
  - 搜索结果页同样显示空状态

- [ ] **Step 5: 测试子页面搜索**
  - 进入任意文章页（如 `zhuangbei/shensuo-jinggun.html`）
  - 在搜索框输入"手铐"，确认能搜索并正确跳转（路径已处理 ../ 前缀）

- [ ] **Step 6: 验证完成后停止服务器**

按 Ctrl+C 停止 Python HTTP server。
