# 伤员救助与急救内容实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为巡防百科网站新增 6 篇伤员救助与急救内容文章，同步写入 Obsidian 知识库原子笔记，并清理 content-inventory.json 中 165 处旧路径引用。

**Architecture:** 内容源在 Obsidian 知识库（`E:\frank知识库`）——急救内容新建 `03_Knowledge/警务技能/伤员救助与急救/` 原子笔记，救助处置/舆情管控归入现有 `快反处置/`；再按现有 HTML 模板转写为网站文章，同步 `content-inventory.json`、`public-sources.json`、模块 index 页与搜索索引。

**Tech Stack:** Python 3.12（完整路径 `C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe`，本会话内 `python` 命令被商店占位符遮蔽）、Node.js 24、HTML/CSS/JS、JSON 台账。

## Global Constraints

- 设计文档：`E:\xunfang-baike\docs\superpowers\specs\2026-08-07-jiuyuan-jijiu-design.md`（已确认）
- 网站共新增 **6 篇**文章：警情1、训练2、装备2、走访1；舆情管控**并入**救助处置流程文，不单独成文
- 不做：骨折固定、法规模块新增、勤务模块新增、走访急救培训普及
- Obsidian 笔记按 `E:\frank知识库\CLAUDE.md` 宪法：原子化、短横线命名、`#标签/层级`、`[[双向链接]]`、末尾注来源、主题≥5篇建 MOC
- Obsidian 可写目录仅 `00_Inbox` 与 `03_Knowledge`；其余目录只读
- 网站每篇新文章必须：带 `.article-page` 标记、`data-module`/`data-category`、meta keywords/description、`.article-summary`、速览卡片、`<!-- public-source-index -->` 区块
- 新条目 `source_files` 一律使用当前正确路径 `E:\frank知识库\...`
- `public_sources` 使用真实可访问 URL；舆情/处置类内容来源受限时如实标注"基于公开资料整理"，不虚构出处
- 不虚构、不歪曲来源内容；只改与本次相关的内容
- 所有命令在本会话用完整 Python 路径 `PY="C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe"`

---
## 文件结构

**Obsidian 知识库（E:\frank知识库）— 新建/修改：**
- `00_Inbox/2026-08-07-急救素材清单.md` — 网络搜索素材与来源清单（收集箱，写入后不归档）
- `03_Knowledge/警务技能/伤员救助与急救/*.md` — 急救原子笔记（约10-12篇）
- `03_Knowledge/警务技能/伤员救助与急救/MOC - 伤员救助与急救.md` — 主题地图
- `03_Knowledge/警务技能/快反处置/*.md` — 救助处置与舆情管控原子笔记（新增）

**网站（E:\xunfang-baike）— 新建：**
- `jingqing/jiuzhu-lei-jingqing-chuzhi.html` — 救助类警情处置流程（含舆情管控环节）
- `xunlian/xinfeifusu-cpr.html` — 心肺复苏操作要点
- `xunlian/zhixue-baozha-banyun.html` — 止血、包扎与伤员搬运
- `zhuangbei/jijiu-bao.html` — 急救包组成与使用
- `zhuangbei/aed-shiyong.html` — AED 使用方法
- `zoufang/changsuo-aed-jiancha.html` — 场所急救设施与AED部署检查

**网站 — 修改：**
- `jingqing/index.html`、`xunlian/index.html`、`zhuangbei/index.html`、`zoufang/index.html` — 新增文章链接、分类区块、更新计数
- `data/content-inventory.json` — 新增6条文章 + 修复165处旧路径
- `data/public-sources.json` — 新增来源与6个页面的 points
- `search-index.json` — 工具重建

**参考模板：**
- 文章 HTML：`jingqing/zishang-lei.html`（结构完整，含速览卡片/TOC/折叠学习区/legal-basis-card/key-warning/来源索引）
- Obsidian 笔记：`03_Knowledge/警务技能/单警装备/伸缩警棍基本介绍.md`、模板 `05_Templates/知识笔记模板.md`
- 模块 index：`jingqing/index.html`

---
### Task 1: 网络素材搜索与整理

**Files:**
- Create: `E:\frank知识库\00_Inbox\2026-08-07-急救素材清单.md`

**Interfaces:**
- Consumes: 设计文档中的 6 篇文章内容大纲
- Produces: `00_Inbox/2026-08-07-急救素材清单.md`（各子主题的要点 + 权威公开来源 URL），供 Task 2 引用来源

- [ ] **Step 1: 分 6 个子主题搜索**
  - 子主题：① 救助类警情处置流程（现场评估/呼救/先期救助/现场保护/交接）；② 救助现场舆情管控（警戒线/围挡/劝离/法律宣传）；③ 心肺复苏 CPR；④ 止血/包扎/搬运；⑤ 急救包组成；⑥ AED 使用与公共场所 AED 配置检查
  - 优先使用权威源：中国红十字会急救资料、国家卫健委及地方卫健委 AED 配置文件、三甲医院/医学科普、公安机关现场执法规范公开版、《人民警察法》第21条、《民法典》第184条
  - 用 WebSearch 逐个子主题搜索，记录要点与 URL

- [ ] **Step 2: 整理素材清单写入 `00_Inbox/2026-08-07-急救素材清单.md`**
  - 格式：按子主题分节，每节列出「要点提炼」+「来源链接（标题/发布方/URL/发布日期）」
  - 舆情管控/处置流程如无权威公开出处，标注"基于公开资料整理"，链接真实存在的通用参考
  - 每条 URL 必须真实可访问（后续 public-sources 核验会检查）

- [ ] **Step 3: 检查清单完整性**
  - 确认 6 个子主题均有要点与来源；无空节、无占位
  - 确认来源覆盖每个后续任务需要的知识点

---
### Task 2: 急救原子笔记（新建 `伤员救助与急救/` 目录）

**Files:**
- Create: `E:\frank知识库\03_Knowledge\警务技能\伤员救助与急救\*.md`（约10-12篇）

**Interfaces:**
- Consumes: `00_Inbox/2026-08-07-急救素材清单.md` 的要点与来源
- Produces: 原子笔记集。建议拆分：`心肺复苏基本流程.md`、`胸外按压操作要领.md`、`人工呼吸操作要领.md`、`AED基本介绍.md`、`AED使用步骤.md`、`直接压迫止血.md`、`加压包扎止血.md`、`止血带使用.md`、`绷带包扎.md`、`三角巾包扎.md`、`伤员搬运方法.md`、`急救包组成与使用.md`。每篇文件名用短横线命名

- [ ] **Step 1: 建立目录并逐篇写笔记（每篇一个原子概念）**
  - 每篇使用 `05_Templates/知识笔记模板.md` 结构：
    ```
    ---
    tags:
      - 警务技能/急救
      - status/已完成
      - type/笔记
    created: 2026-08-07
    source: <来源标题/URL>
    ---
    # 标题
    ## 核心定义
    ## 详细阐述
    ## 相关概念
    - [[...]]
    ```
  - 每篇加 2-3 个标签、至少 3 个 `[[双向链接]]`（指向目录内其他笔记与既有笔记如 `[[心肺复苏基本流程]]` 等）、末尾注明来源

- [ ] **Step 2: 校验笔记格式**
  - 抽查每篇：frontmatter 完整、tags 层级格式、相关概念 ≥3 个、有来源
  - 笔记间互链闭环（新目录内无孤立笔记）

---
### Task 3: 救助处置/舆情管控笔记 + 急救 MOC

**Files:**
- Create: `E:\frank知识库\03_Knowledge\警务技能\快反处置\救助类警情先期处置.md`
- Create: `E:\frank知识库\03_Knowledge\警务技能\快反处置\救助警情现场舆情管控.md`
- Create: `E:\frank知识库\03_Knowledge\警务技能\伤员救助与急救\MOC - 伤员救助与急救.md`

**Interfaces:**
- Consumes: Task 2 笔记集（MOC 链接它们）
- Produces: 2 篇处置/舆情笔记 + MOC

- [ ] **Step 1: 写救助处置笔记**
  - `救助类警情先期处置.md`：处置原则→现场评估→呼救→先期救助→现场保护→交接记录的流程要点；用模板格式，链到急救笔记
- [ ] **Step 2: 写舆情管控笔记**
  - `救助警情现场舆情管控.md`：短小精悍，聚焦拉警戒线、架设围挡、围观劝离、法律宣传、信息发布纪律；链到处置笔记与急救笔记
- [ ] **Step 3: 建 MOC**
  - `MOC - 伤员救助与急救.md`：核心概念列表（带简介）、应用场景、相关主题链接，覆盖全部急救笔记
- [ ] **Step 4: 校验**
  - 确认新目录笔记数 ≥5 篇（MOC 触发条件满足）；MOC 链接了所有急救笔记；处置/舆情笔记无孤立

---
### Task 4: 警情文章《救助类警情处置流程》

**Files:**
- Create: `E:\xunfang-baike\jingqing\jiuzhu-lei-jingqing-chuzhi.html`

**Interfaces:**
- Consumes: Task 1 素材清单（子主题①、②）、Task 3 处置/舆情笔记
- Produces: 完整文章 HTML（供 Task 8 index 链接、Task 9 inventory 登记）

- [ ] **Step 1: 复制模板结构**
  - 以 `jingqing/zishang-lei.html` 为模板；`data-module="jingqing"`，`data-category="救助类警情"`
  - breadcrumb：首页 > 警情处置 > 救助类警情 > 救助类警情处置流程
  - meta keywords/description 按内容填写
- [ ] **Step 2: 写正文（处置原则→舆情管控→现场评估→呼救→先期救助→现场保护→交接记录）**
  - **速览卡片**：核心结论（先救助后处置、生命优先）；先做什么（警戒/围挡→评估→呼救→先期救助）；不能做什么（不贸然移动疑有脊柱伤者等）；法律依据（《人民警察法》第21条救助义务、《民法典》第184条）
  - **TOC** 七节对应七个环节
  - 默认可见节：处置原则、舆情管控（重点，短小精悍）
  - **舆情管控节**（短小精悍，讲清 4 个动作 + 纪律）：
    - 拉警戒线：划定现场边界、控制无关人员进入
    - 架设围挡：遮蔽伤员隐私与血腥画面，防围观拍摄传播
    - 围观人员劝离：言语劝离、疏导交通、防二次事故
    - 法律宣传：向围观拍摄者说明不得干扰救援、不得传播血腥画面、恶意造谣的法律后果
    - 信息发布纪律：不擅自对外发布现场信息，报告与统一口径
  - 折叠学习区（`<details class="learning-section">`）：现场评估、呼救、先期救助、现场保护、交接记录
  - 法律依据节用 `legal-basis-card` 结构引用《人民警察法》《民法典》
  - 结尾含 `<!-- public-source-index:start -->` 注释对（内容由 Task 10 工具注入）
- [ ] **Step 3: 内链与页脚**
  - `related-links`：链到训练/装备新文章（如 `../xunlian/xinfeifusu-cpr.html`、`../zhuangbei/aed-shiyong.html`）
  - `page-nav` 上一/下一篇
- [ ] **Step 4: 校验**
  - 用 `PY tools/check_site_links.py` 确认无断链（此时其它新文章尚未建会告警——先跳过，Task 11 统一验证）

---
### Task 5: 训练模块两篇文章

**Files:**
- Create: `E:\xunfang-baike\xunlian\xinfeifusu-cpr.html`
- Create: `E:\xunfang-baike\xunlian\zhixue-baozha-banyun.html`

**Interfaces:**
- Consumes: Task 1 素材（子主题③、④）
- Produces: 2 篇 HTML（供 Task 8/9/10）

- [ ] **Step 1: 写《心肺复苏操作要点》**
  - `data-module="xunlian"`，`data-category="伤员救助"`；以 zishang-lei.html 为模板
  - 内容：适用判断（无反应无呼吸）、胸外按压（部位/深度5-6cm/频率100-120次/分/按压呼吸比30:2）、人工呼吸要点、AED 衔接提示、常见错误与注意事项（如不中断按压）
  - 速览卡片 4 张；legal-basis-card 引用红十字会/AHA 公开指南；related-links 链向 AED 文章
- [ ] **Step 2: 写《止血、包扎与伤员搬运》**
  - 内容：直接压迫止血→加压包扎→止血带（部位/松紧/时间记录）；绷带包扎（环形/螺旋/八字）；三角巾包扎（头部/手臂悬吊）；伤员搬运（脊柱保护、多人平托、担架使用）
  - 速览卡片强调"不能做什么"（止血带过紧/时间过长、疑脊柱伤随意搬动）
- [ ] **Step 3: 校验两篇结构完整**
  - 均有 `.article-page`、meta、速览卡片、来源索引注释对

---
### Task 6: 装备模块两篇文章

**Files:**
- Create: `E:\xunfang-baike\zhuangbei\jijiu-bao.html`
- Create: `E:\xunfang-baike\zhuangbei\aed-shiyong.html`

**Interfaces:**
- Consumes: Task 1 素材（子主题⑤、⑥）
- Produces: 2 篇 HTML

- [ ] **Step 1: 写《急救包组成与使用》**
  - `data-module="zhuangbei"`，`data-category="急救装备"`
  - 内容：常用急救物资清单（止血带、绷带、三角巾、无菌敷料、敷贴、碘伏、剪刀、手套等）、各物品用途、检查维护（有效期/完整性/定期检查）
- [ ] **Step 2: 写《AED 使用方法》**
  - 内容：AED 原理简述（除颤）、操作步骤（开机→贴电极片→听语音提示→确保无人接触→按下电击）、注意事项（胸毛/湿水/起搏器/儿童模式）、与 CPR 交替衔接
- [ ] **Step 3: 校验两篇结构完整**
  - related-links 互链 + 链向训练 CPR 文章

---
### Task 7: 走访模块文章

**Files:**
- Create: `E:\xunfang-baike\zoufang\changsuo-aed-jiancha.html`

**Interfaces:**
- Consumes: Task 1 素材（子主题⑥ AED 配置检查）
- Produces: 1 篇 HTML

- [ ] **Step 1: 写《场所急救设施与AED部署检查》**
  - `data-module="zoufang"`，`data-category="走访检查"`
  - 内容：走访中对商场/学校/车站等场所急救设施检查要点（AED 是否配备、位置标识、有效期、电池/电极片状态、有无定期巡检记录）、记录与上报
- [ ] **Step 2: 校验结构完整**
  - related-links 链向 AED 使用文章

---
### Task 8: 更新四个模块 index 页

**Files:**
- Modify: `E:\xunfang-baike\jingqing\index.html`（新增"救助类警情"分类区块 + 计数 5→6）
- Modify: `E:\xunfang-baike\xunlian\index.html`（新增"伤员救助"分类区块 + 更新计数）
- Modify: `E:\xunfang-baike\zhuangbei\index.html`（新增"急救装备"分类区块 + 更新计数）
- Modify: `E:\xunfang-baike\zoufang\index.html`（新增"走访检查"或并入既有分类 + 更新计数）

- [ ] **Step 1: 逐页添加 `section.article-group`**
  - 参照 `jingqing/index.html` 中 `#self-harm-incidents` 区块写法；`id` 锚点与文章 `data-category` 分类对应（用于 breadcrumb `index.html#锚点`）
  - 更新 meta description 与顶部 `meta` 标签的篇数（`<span class="tag">N篇</span>`）
- [ ] **Step 2: 校验**
  - `PY tools/check_site_links.py` 确认 index 新增链接与锚点有效（配合 Task 11）

---
### Task 9: 更新 content-inventory.json（新增条目 + 旧路径清理）

**Files:**
- Modify: `E:\xunfang-baike\data\content-inventory.json`

**Interfaces:**
- Consumes: Task 4-7 生成的 6 篇 HTML 及其 source_files
- Produces: 完整 inventory（6 新条目 + 165 处旧路径修复），供 Task 11 校验

- [ ] **Step 1: 修复 165 处旧路径**
  - 用脚本将全部 `source_files` 中前缀 `F:\frank第二大脑\frank知识库` 替换为 `E:\frank知识库`（已验证替换后文件 0 处缺失）
- [ ] **Step 2: 新增 6 个文章条目**
  - 字段：`module`、`module_title`、`category`、`category_anchor`、`title`、`slug`、`path`、`source_files`（用新路径，指向 Task 2/3 的原子笔记）、`public_sources`（与 Task 10 一致）、`images`（可空数组）、`related_pages`（对应相关文章）
  - 分类与锚点必须与文章 `data-category`、index 页锚点一致
- [ ] **Step 3: 校验**
  - 用 `PY tools/build_search_index.py --check` 确认索引与清单一致（此时需先跑重建，见 Task 11）

---
### Task 10: 更新 public-sources.json

**Files:**
- Modify: `E:\xunfang-baike\data\public-sources.json`

**Interfaces:**
- Consumes: Task 1 素材清单中的真实 URL
- Produces: 新增 sources + 6 个 pages 的 points（coverage_status 均为 verified）

- [ ] **Step 1: 新增 sources**
  - 参照现有 `sources[]` 结构（source_id/title/publisher/platform/url/published_at/verified_at/verification_status/similarity_note/source_level/last_checked_at），只加入真实可访问的 URL；处置/舆情类无权威出处的用公开通用参考并如实写 similarity_note
- [ ] **Step 2: 新增 6 个 pages 条目**
  - 每页 `page_id`=slug、`path`、`title`、points（position/label/source_ids/coverage_status: verified/coverage_note）
- [ ] **Step 3: 运行工具注入文章 HTML 的来源区块**
  - `PY tools/public_source_index.py write`（会重写各文章 `<!-- public-source-index -->` 区块）
  - 运行 `PY tools/public_source_index.py check`，预期 PASS 且 0 pending（不允许 pending，否则默认 check 失败）

---
### Task 11: 全量验证

**Files:**
- Modify: `E:\xunfang-baike\search-index.json`（重建）
- Modify: `E:\xunfang-baike\data\legal-basis-cards.json`、`data\legal-search-entries.json`（测试生成的既有产物，若测试重写则为变更）

- [ ] **Step 1: 重建搜索索引**
  - `PY tools/build_search_index.py`（重建）后 `PY tools/build_search_index.py --check`，预期 OK 且记录数=清单文章数
- [ ] **Step 2: 站内链接检查**
  - `PY tools/check_site_links.py`，预期 OK、无断链无锚点失效
- [ ] **Step 3: 来源台账 check**
  - `PY tools/public_source_index.py check`，预期 PASS、0 pending
- [ ] **Step 4: 全部测试**
  - `PY -m unittest discover -s tests -p "test_*.py"`（预期 OK，跳过项与基线一致）
  - `node --test tests/auth_core.test.js`（预期 5 pass）
- [ ] **Step 5: 修复任何失败项后重跑至全绿**

---
### Task 12: 提交

- [ ] **Step 1: 提交网站仓库变更**
  ```bash
  cd /e/xunfang-baike
  git add jingqing/ xunlian/ zhuangbei/ zoufang/ data/ search-index.json docs/
  git commit -m "feat: 新增伤员救助与急救内容6篇，修复content-inventory旧路径"
  ```
  - 提交前确认：6 篇文章在 git status 中、index 页与台账变更在列、无无关文件混入
- [ ] **Step 2: 说明 Obsidian 变更**
  - Obsidian 知识库（`E:\frank知识库`）非本仓库，不在 git 提交范围；实施完成后向用户列出新增的笔记文件清单供其在 Obsidian 中核对

---
## Self-Review

- **Spec coverage:** 6 篇文章（Task 4-7）✓；舆情管控并入处置流程且短小精悍（Task 4）✓；不做骨折固定/法规/勤务/走访培训（Task 定义范围内未包含）✓；Obsidian 原子笔记+MOC（Task 2/3）✓；source_files 新路径（Task 9）✓；来源台账不虚构（Task 1/10）✓；老路径清理（Task 9）✓；验证（Task 11）✓
- **Placeholder scan:** 各任务均有具体文件路径、结构要求、校验命令；正文文案在实施时基于 Task 1 素材撰写（内容需实时搜索，无法在计划中预写全文，属计划约定范围内的执行工作）
- **Type consistency:** slug/路径在 Task 4-9 间保持一致：`jiuzhu-lei-jingqing-chuzhi`、`xinfeifusu-cpr`、`zhixue-baozha-banyun`、`jijiu-bao`、`aed-shiyong`、`changsuo-aed-jiancha`；分类锚点在文章、index 页、inventory 三者一致
