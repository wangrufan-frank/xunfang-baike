# 巡防百科公开资料索引实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为静态网站 27 个内容页的 153 个一级知识点建立可核验的公开资料编号引用、页面底部完整来源列表和独立证据台账，同时保持来源核验与保密审查相互独立。

**Architecture:** 以 `data/public-sources.json` 作为唯一来源事实库，Python 标准库工具负责盘点、校验、生成静态 HTML 和审计报告。工具只替换明确注释标记内的引用和来源区，重复执行必须幂等；来源覆盖检查与发布门禁分别运行，发布门禁只有在有权人员填写审核信息后才能通过。

**Tech Stack:** 静态 HTML、CSS、Python 3 标准库、`unittest`、JSON

## Global Constraints

- 只覆盖 `fagui/`、`xunlian/`、`zhuangbei/`、`zoufang/` 下 27 个非 `index.html` 内容页；不修改微信小程序。
- 当前基线必须识别 153 个 `.step-card` 一级知识点：法规 33、训练 67、装备 31、走访 22。
- 来源优先顺序为政府和法律法规官方页面、公安/司法/应急/教育等权威公开页面、正式公开标准或专业机构资料、微信公众号/百度百科/知乎补充资料。
- 只有实际打开并核对正文的网页才能设置 `verification_status: "verified"`；搜索摘要、无法打开页面或身份不明页面不得进入正式来源列表。
- 法律结论、执法程序和警械使用条件不得只依赖微信公众号、百度百科或知乎。
- 不下载、镜像、重新发布或大段摘录外部网页、图片和视频；台账只保存元数据和简短的相似内容说明。
- 不把来源核验状态自动转换为保密审核通过；生成工具不得写入 `review_status: "approved"`。
- 不部署网站，不运行 `parse_html.py` 或 `oss_upload.py`，不手工编辑 `search-index.json`。
- 不提交现有未跟踪的 `公安警察工作汇报PPT.pptx`、`.env`、`.netlify/`、缓存或凭据。
- 所有 HTML、CSS 和报告保持 UTF-8；Python 只使用标准库，不新增依赖。

## File Structure

- Create: `data/public-sources.json` — 27 页、153 个知识点、来源及双状态审核台账。
- Create: `tools/public_source_index.py` — 盘点、校验、静态生成、幂等检查和审计报告入口。
- Create: `tests/test_public_source_index.py` — 工具单元测试、生产台账覆盖测试、HTML 集成测试和发布门禁测试。
- Create: `docs/public-source-index-audit.md` — 从台账生成的全站人工复核汇总，不包含外部文章全文。
- Modify: `css/style.css` — 引用标记、来源列表、固定说明、窄屏和夜间主题样式。
- Modify: 27 个内容 HTML — 仅增加受管知识点引用、稳定锚点及页面底部来源区。

---

### Task 1: 建立盘点、模式校验与失败测试

**Files:**
- Create: `tests/test_public_source_index.py`
- Create: `tools/public_source_index.py`

**Interfaces:**
- Produces: `discover_pages(root: Path) -> list[Path]`
- Produces: `extract_points(html: str) -> list[str]`
- Produces: `load_ledger(path: Path) -> dict`
- Produces: `validate_schema(ledger: dict, allow_pending: bool = False) -> list[str]`
- Produces: `validate_ledger(root: Path, ledger: dict, allow_pending: bool = False) -> list[str]`
- Produces: `publish_errors(ledger: dict) -> list[str]`
- Produces CLI: `python tools/public_source_index.py inventory|check|check-publish|write|report`

- [ ] **Step 1: 写盘点与模式校验失败测试**

在 `tests/test_public_source_index.py` 中使用临时目录和内联 JSON fixture，至少写出以下测试骨架：

```python
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'public_source_index', ROOT / 'tools' / 'public_source_index.py'
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PublicSourceIndexUnitTests(unittest.TestCase):
    @staticmethod
    def fixture_ledger(verification_status, coverage_status):
        return {
            'version': 1,
            'pages': [{
                'page_id': 'fagui-dubo-zhifa',
                'path': 'fagui/dubo-zhifa.html',
                'title': '赌博类警情执法标准',
                'review_status': 'pending',
                'reviewed_by': None,
                'reviewed_at': None,
                'points': [{
                    'point_id': 'fagui-dubo-zhifa-01',
                    'position': 1,
                    'label': '核心要点',
                    'source_ids': ['official-secrecy-law-2024'],
                    'coverage_status': coverage_status,
                    'coverage_note': '核对公开与保密审查边界。',
                }],
            }],
            'sources': [{
                'source_id': 'official-secrecy-law-2024',
                'title': '中华人民共和国保守国家秘密法（2024修订）',
                'publisher': '全国人民代表大会常务委员会',
                'platform': '工业和信息化部政府网站',
                'url': 'https://gdca.miit.gov.cn/zwgk/zcwj/flfg/art/2024/art_4870c40a6f8249389684d03786d41639.html',
                'published_at': '2024-02-27',
                'verified_at': '2026-07-14',
                'verification_status': verification_status,
                'similarity_note': '公开法律文本说明公开与保密义务的边界。',
                'source_level': 1,
                'last_checked_at': '2026-07-14',
            }],
        }

    def test_discovery_matches_current_site_inventory(self):
        pages = MODULE.discover_pages(ROOT)
        self.assertEqual(len(pages), 27)
        counts = {'fagui': 0, 'xunlian': 0, 'zhuangbei': 0, 'zoufang': 0}
        point_count = 0
        for page in pages:
            counts[page.parent.name] += 1
            point_count += len(MODULE.extract_points(page.read_text(encoding='utf-8')))
        self.assertEqual(counts, {'fagui': 6, 'xunlian': 11, 'zhuangbei': 7, 'zoufang': 3})
        self.assertEqual(point_count, 153)

    def test_pending_or_search_snippet_source_is_rejected_in_strict_mode(self):
        ledger = self.fixture_ledger(
            verification_status='needs_review', coverage_status='pending'
        )
        errors = MODULE.validate_schema(ledger)
        self.assertTrue(any('verification_status' in error for error in errors))
        self.assertTrue(any('coverage_status' in error for error in errors))

    def test_review_status_is_not_inferred_from_verified_sources(self):
        ledger = self.fixture_ledger(
            verification_status='verified', coverage_status='verified'
        )
        self.assertEqual(ledger['pages'][0]['review_status'], 'pending')
        self.assertTrue(MODULE.publish_errors(ledger))
```

fixture 中使用真实公开法规示例：工信部政府网站转载的《中华人民共和国保守国家秘密法（2024修订）》页面，URL 为 `https://gdca.miit.gov.cn/zwgk/zcwj/flfg/art/2024/art_4870c40a6f8249389684d03786d41639.html`，避免在测试里使用不存在的示例域名。

- [ ] **Step 2: 运行测试并确认因工具不存在而失败**

Run: `python -m unittest tests.test_public_source_index -v`

Expected: `ERROR`，包含无法加载 `tools/public_source_index.py`。

- [ ] **Step 3: 实现盘点和严格模式校验**

`tools/public_source_index.py` 必须：

- 只发现四个指定目录下的非 `index.html` 页面；
- 使用 UTF-8 读取文件并提取 `<h1>` 与 `.step-title`；
- 校验顶层 `version == 1`、页面路径唯一、来源 ID 唯一、知识点 ID 唯一、引用无悬空；
- 严格模式要求每个知识点为 `verified` 且至少有一个来源；
- 正式来源要求 `title`、`publisher`、`platform`、`url`、`verified_at`、`similarity_note`、`source_level`、`last_checked_at` 非空；
- 只接受 `https://` 来源 URL；
- `verified_at` 和 `last_checked_at` 必须是 `YYYY-MM-DD`；
- `publish_errors()` 独立检查 `review_status == "approved"` 以及 `reviewed_by`、`reviewed_at` 非空，不修改台账。

命令行退出码统一为：成功 `0`，数据或生成检查失败 `1`，命令用法错误 `2`。

- [ ] **Step 4: 运行专项测试**

Run: `python -m unittest tests.test_public_source_index.PublicSourceIndexUnitTests -v`

Expected: 所有单元测试 `OK`，盘点输出为 `27 pages, 153 points`。

- [ ] **Step 5: 提交工具核心**

```powershell
git add tests/test_public_source_index.py tools/public_source_index.py
git commit -m "feat: add public source ledger validation"
```

---

### Task 2: 建立完整知识点台账骨架

**Files:**
- Create: `data/public-sources.json`
- Modify: `tests/test_public_source_index.py`

**Interfaces:**
- Consumes: `discover_pages()`、`extract_points()`、`validate_ledger(..., allow_pending=True)`
- Produces: 27 个页面记录和 153 个稳定知识点记录

- [ ] **Step 1: 写生产台账盘点失败测试**

新增 `PublicSourceLedgerInventoryTests`，断言：

```python
class PublicSourceLedgerInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = MODULE.load_ledger(ROOT / 'data' / 'public-sources.json')

    def test_ledger_covers_every_current_page_and_point(self):
        errors = MODULE.validate_ledger(ROOT, self.ledger, allow_pending=True)
        self.assertEqual(errors, [])
        self.assertEqual(len(self.ledger['pages']), 27)
        self.assertEqual(
            sum(len(page['points']) for page in self.ledger['pages']), 153
        )
```

- [ ] **Step 2: 运行并确认缺少台账**

Run: `python -m unittest tests.test_public_source_index.PublicSourceLedgerInventoryTests -v`

Expected: `ERROR`，指出 `data/public-sources.json` 不存在。

- [ ] **Step 3: 生成一次性盘点并人工核对**

Run: `python tools/public_source_index.py inventory --output data/public-sources.json`

Expected: `Wrote 27 pages and 153 points; all coverage statuses are pending.`

每个页面记录必须使用相对 POSIX 路径；`page_id` 使用目录与文件名，例如 `xunlian-dunpai-jishu`；每个知识点使用 `page_id` 加两位顺序号，例如 `xunlian-dunpai-jishu-01`。每个知识点同时保存当前位置、精确标题、空 `source_ids`、`coverage_status: "pending"` 和空 `coverage_note`。页面审核状态统一初始化为 `pending`，审核人和审核日期为空。

- [ ] **Step 4: 对照页面标题逐项核验盘点**

Run: `python tools/public_source_index.py check --allow-pending`

Expected: `PASS: 27 pages, 153 points; 153 points pending source verification.`

人工抽查四类各两页，确认顺序和标题与 HTML 一致；不得通过修改计数常量掩盖漏页。

- [ ] **Step 5: 提交台账骨架**

```powershell
git add data/public-sources.json tests/test_public_source_index.py
git commit -m "chore: inventory public source knowledge points"
```

---

### Task 3: 用测试驱动实现静态引用生成器

**Files:**
- Modify: `tests/test_public_source_index.py`
- Modify: `tools/public_source_index.py`

**Interfaces:**
- Produces: `render_page(html: str, page: dict, sources: dict[str, dict]) -> str`
- Produces managed markers: `source-citations:start/end`、`public-source-index:start/end`

- [ ] **Step 1: 写渲染和幂等失败测试**

使用下面这个包含两个 `.step-card` 和 `.page-nav` 的最小 HTML fixture，完成 `page_record` 和 `source_map` 后断言：

```python
html = '''
<div class="step-card step-blue">
  <div class="step-title">第一点</div><div class="step-lead">摘要一</div>
</div>
<div class="step-card step-green">
  <div class="step-title">第二点</div><div class="step-lead">摘要二</div>
</div>
<div class="page-nav"></div>
'''
source = PublicSourceIndexUnitTests.fixture_ledger('verified', 'verified')['sources'][0]
source_map = {source['source_id']: source}
page_record = {
    'page_id': 'fixture-page',
    'path': 'fixture/page.html',
    'title': '测试页',
    'review_status': 'pending',
    'reviewed_by': None,
    'reviewed_at': None,
    'points': [
        {
            'point_id': 'point-01', 'position': 1, 'label': '第一点',
            'source_ids': [source['source_id']], 'coverage_status': 'verified',
            'coverage_note': '第一点与公开资料的相似边界。',
        },
        {
            'point_id': 'point-02', 'position': 2, 'label': '第二点',
            'source_ids': [source['source_id']], 'coverage_status': 'verified',
            'coverage_note': '第二点与公开资料的相似边界。',
        },
    ],
}
rendered = MODULE.render_page(html, page_record, source_map)
self.assertIn('id="source-ref-point-01-source-law"', rendered)
self.assertIn('href="#public-source-source-law"', rendered)
self.assertIn('class="public-source-index"', rendered)
self.assertLess(rendered.index('public-source-index'), rendered.index('page-nav'))
self.assertEqual(MODULE.render_page(rendered, page_record, source_map), rendered)
```

另写失败测试验证知识点标题不匹配、知识点数量不匹配、来源悬空和 `.page-nav` 缺失时抛出带页面上下文的 `ValueError`，不得静默跳过。

- [ ] **Step 2: 运行并确认缺少渲染接口**

Run: `python -m unittest tests.test_public_source_index.PublicSourceRenderTests -v`

Expected: `FAIL` 或 `ERROR`，指出 `render_page` 未定义。

- [ ] **Step 3: 实现受管片段渲染**

实现规则：

- 每次渲染先删除旧受管引用和来源区；
- 按台账顺序验证 `.step-title` 精确文本；
- 给 `.step-card` 添加稳定 `id="point-..."` 和 `data-source-point="..."`；
- 在 `.step-lead` 末尾写入受管引用，引用用页面内连续编号；
- 同一来源在一页只渲染一次，多个知识点复用编号；
- 每条来源包含标题、发布主体、平台、发布日期（存在时）、核验日期、原文链接和相似内容说明；
- 外链使用 `target="_blank" rel="noopener noreferrer"`；
- 来源条目提供返回第一个引用位置的链接；
- 固定说明使用设计文档中的完整文本；
- 来源区插在 `.page-nav` 前；
- 若存在任何 `pending` 或非 `verified` 数据，`write` 命令退出 `1` 且不写任何 HTML。

- [ ] **Step 4: 增加 dry-run 和原子写入**

`write --check` 只比较预期输出与磁盘，不写文件；`write` 先完成全部 27 页渲染，全部成功后才逐页写入，避免半完成状态。输出每个变更页面和最终汇总。

- [ ] **Step 5: 运行渲染测试**

Run: `python -m unittest tests.test_public_source_index.PublicSourceRenderTests -v`

Expected: 所有渲染、异常和幂等测试 `OK`。

- [ ] **Step 6: 提交生成器**

```powershell
git add tools/public_source_index.py tests/test_public_source_index.py
git commit -m "feat: generate static public source references"
```

---

### Task 4: 检索并核验法规模块 33 个知识点

**Files:**
- Modify: `data/public-sources.json`

**Interfaces:**
- Consumes: 法规模块 6 页、33 个知识点
- Produces: 已核验来源记录及知识点映射，不改变页面 `review_status`

- [ ] **Step 1: 逐页制定检索词并优先打开官方原文**

按 `dubo-zhifa`、`faly-fayanfayu`、`faly-yiju`、`gainian-falv`、`shipin-tiaoli`、`zhian-guifan` 顺序工作。法律条文必须回到国家法律法规数据库、中国政府网、中国人大网或主管机关页面核对现行条文；法规名称和条号必须与正文一致。

- [ ] **Step 2: 为每个已核验网页录入完整来源对象**

每条记录使用实际网页值，格式固定为：

```json
{
  "source_id": "official-secrecy-law-2024",
  "title": "中华人民共和国保守国家秘密法（2024修订）",
  "publisher": "全国人民代表大会常务委员会",
  "platform": "工业和信息化部政府网站",
  "url": "https://gdca.miit.gov.cn/zwgk/zcwj/flfg/art/2024/art_4870c40a6f8249389684d03786d41639.html",
  "published_at": "2024-02-27",
  "verified_at": "2026-07-14",
  "verification_status": "verified",
  "similarity_note": "公开法律文本说明国家秘密定义、公开原则及互联网传递国家秘密的禁止要求。",
  "source_level": 1,
  "last_checked_at": "2026-07-14"
}
```

`published_at` 只有在页面能可靠确认时填写；不能确认时使用 `null`，不得猜测。`similarity_note` 必须说明具体覆盖内容，不复制长段原文。

- [ ] **Step 3: 完成 33 个知识点映射**

把每个法规知识点改为 `coverage_status: "verified"`，写入至少一个 `source_id` 和明确 `coverage_note`。若官方条文与页面表述不一致，保持 `pending` 并记录差异，不得用较低等级来源覆盖冲突。

- [ ] **Step 4: 运行模块检查**

Run: `python tools/public_source_index.py check --module fagui`

Expected: `PASS: fagui 6 pages, 33 points, 0 pending.`

- [ ] **Step 5: 提交法规来源**

```powershell
git add data/public-sources.json
git commit -m "docs: map public sources for legal content"
```

---

### Task 5: 检索并核验装备模块 31 个知识点

**Files:**
- Modify: `data/public-sources.json`

**Interfaces:**
- Consumes: 装备模块 7 页、31 个知识点
- Produces: 已核验来源记录及知识点映射，不改变页面 `review_status`

- [ ] **Step 1: 按风险顺序检索官方公开资料**

先处理执法记录仪、警械使用警告和法定禁止情形，再处理手铐、警棍、催泪喷射器、防割手套和九小件。优先使用法规、政府采购公开技术资料、公安机关公开普法或公开培训材料；商品营销页只能补充非法律性的产品常识。

- [ ] **Step 2: 核对性能参数和操作性描述**

对数值参数、击打部位、开棍技术、上铐方法、喷射要领等逐句核对。相似来源只支持一般介绍而不支持具体参数或动作时，不能把整个知识点标记为已覆盖；应拆分覆盖说明或保持 `pending` 交人工决定。

- [ ] **Step 3: 录入来源并完成 31 个知识点映射**

沿用 Task 4 的来源对象格式。微信公众号、百度百科和知乎只能作为补充来源，并记录真实发布主体/作者；无法确认主体的条目不进入正式列表。

- [ ] **Step 4: 运行模块检查**

Run: `python tools/public_source_index.py check --module zhuangbei`

Expected: `PASS: zhuangbei 7 pages, 31 points, 0 pending.`

- [ ] **Step 5: 提交装备来源**

```powershell
git add data/public-sources.json
git commit -m "docs: map public sources for equipment content"
```

---

### Task 6: 检索并核验训练模块 67 个知识点

**Files:**
- Modify: `data/public-sources.json`

**Interfaces:**
- Consumes: 训练模块 11 页、67 个知识点
- Produces: 已核验来源记录及知识点映射，不改变页面 `review_status`

- [ ] **Step 1: 先处理程序与法律相关知识点**

优先核验盘查流程、法言法语、武力升级程序和武器使用标准，回到现行法律法规和公安机关公开规范。发现页面把教学模型表述为法定程序时，保持 `pending` 并记录冲突。

- [ ] **Step 2: 再处理动作、站位和战术知识点**

逐页处理盾叉协同、盾牌技术、最小作战单元编成、抓握解脱、警棍与抓捕叉、控制技术、搜身带离、三防训练、战术站位和巡逻装备应用。每个来源必须实际展示相似动作或原则；只出现相同名词不构成覆盖。

- [ ] **Step 3: 对高聚合风险内容单独记录审查提示**

刀斧砍杀步骤、阵型、人员编成、装备组合、系统名称和控制动作即使存在公开碎片，页面 `review_status` 仍保持 `pending`。在页面记录的内部审查说明中注明“公开来源存在不等于允许聚合发布”，但该内部说明不渲染到网页。

- [ ] **Step 4: 完成 67 个知识点来源映射**

不得为了达到数量要求重复使用与具体知识点无实质关联的通用页面。无法找到实质相似来源时保持 `pending`，检查应失败并列出知识点，交用户或有权审核人员决定删除、泛化或转入受控环境。

- [ ] **Step 5: 运行模块检查**

Run: `python tools/public_source_index.py check --module xunlian`

Expected after all evidence is valid: `PASS: xunlian 11 pages, 67 points, 0 pending.`

- [ ] **Step 6: 提交训练来源**

```powershell
git add data/public-sources.json
git commit -m "docs: map public sources for training content"
```

---

### Task 7: 检索并核验走访模块 22 个知识点

**Files:**
- Modify: `data/public-sources.json`

**Interfaces:**
- Consumes: 走访模块 3 页、22 个知识点
- Produces: 已核验来源记录及知识点映射，不改变页面 `review_status`

- [ ] **Step 1: 检索校园和金融机构官方公开预案原则**

优先使用教育、公安、应急、金融监管等政府部门公开页面以及可确认主体的学校、银行公开安全教育材料。媒体报道和自媒体只能补充背景，不能支持具体处置战术。

- [ ] **Step 2: 单独核对战术、专班和团队建设描述**

夹击、分割、快反、校园操作口诀、蓝军专班等内容只有在正文确有实质相似公开描述时才映射。单位内部做法或仅凭关键词相似的网页不得作为正式来源。

- [ ] **Step 3: 完成 22 个知识点来源映射**

沿用相同来源对象结构，保留页面 `review_status: "pending"`，并为聚合风险项保留内部审查说明。

- [ ] **Step 4: 运行模块检查**

Run: `python tools/public_source_index.py check --module zoufang`

Expected after all evidence is valid: `PASS: zoufang 3 pages, 22 points, 0 pending.`

- [ ] **Step 5: 提交走访来源**

```powershell
git add data/public-sources.json
git commit -m "docs: map public sources for outreach content"
```

---

### Task 8: 添加来源组件样式

**Files:**
- Modify: `tests/test_public_source_index.py`
- Modify: `css/style.css`

**Interfaces:**
- Consumes: 生成器输出的 `.source-citations`、`.source-citation`、`.public-source-index`、`.public-source-list`、`.public-source-item`、`.public-source-note`

- [ ] **Step 1: 写样式失败测试**

新增测试，要求上述选择器全部存在，来源链接具有可见 `:focus-visible` 样式，并在 `@media (max-width: 600px)` 中降低来源区内边距和允许长 URL 换行。

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_public_source_index.PublicSourceStyleTests -v`

Expected: `FAIL`，指出缺少 `.public-source-index` 等选择器。

- [ ] **Step 3: 实现桌面、窄屏和夜间样式**

使用现有 `--warm-white`、`--bg`、`--border`、`--text`、`--text-muted`、`--police-blue`、`--amber`、`--radius` 和 `--shadow` 变量。来源区位于内容卡片之后，编号清晰但不抢过正文；URL 使用 `overflow-wrap: anywhere`；引用和返回链接有键盘焦点轮廓；夜间主题不得硬编码浅色背景。

- [ ] **Step 4: 运行样式测试和现有品牌测试**

Run: `python -m unittest tests.test_public_source_index.PublicSourceStyleTests tests.test_brand_styles tests.test_theme_assets -v`

Expected: 全部 `OK`。

- [ ] **Step 5: 提交样式**

```powershell
git add css/style.css tests/test_public_source_index.py
git commit -m "style: add public source reference component"
```

---

### Task 9: 生成 27 页静态引用和审计报告

**Files:**
- Modify: 27 个内容 HTML
- Create: `docs/public-source-index-audit.md`
- Modify: `tests/test_public_source_index.py`

**Interfaces:**
- Consumes: 严格校验通过的 `data/public-sources.json`
- Produces: 静态引用 HTML 和全站审计汇总

- [ ] **Step 1: 写生产集成失败测试**

新增测试，先遍历 `for page_record in ledger['pages']` 并读取 `ROOT / page_record['path']`，然后对每个生产页面断言：

```python
self.assertEqual(html.count('<!-- public-source-index:start -->'), 1)
self.assertEqual(html.count('<!-- public-source-index:end -->'), 1)
self.assertEqual(
    html.count('<!-- source-citations:start -->'),
    len(page_record['points']),
)
self.assertNotIn('内容来源于互联网，因此不涉密', html)
self.assertNotIn('已规避涉密责任', html)
```

同时逐个解析 `href="#public-source-..."`，确认目标 ID 存在；确认来源区出现在 `.page-nav` 前；确认同页来源编号连续。

- [ ] **Step 2: 运行严格来源检查**

Run: `python tools/public_source_index.py check`

Expected: `PASS: 27 pages, 153 points, 0 pending; all formal sources verified.`

若失败，不运行生成；回到对应模块修复来源或提交人工内容处置决定。

- [ ] **Step 3: 生成静态 HTML**

Run: `python tools/public_source_index.py write`

Expected: 列出 27 个更新页面并输出 `Wrote source references to 27 pages.`

- [ ] **Step 4: 验证幂等**

Run: `python tools/public_source_index.py write --check`

Expected: `PASS: generated source markup is up to date; 0 files differ.`

- [ ] **Step 5: 生成审计报告**

Run: `python tools/public_source_index.py report --output docs/public-source-index-audit.md`

Expected: 报告列出 27 页、153 个知识点、来源总数、每页覆盖状态、保密审核状态和失效链接复核日期；不包含外部文章全文。

- [ ] **Step 6: 运行生产集成测试**

Run: `python -m unittest tests.test_public_source_index.PublicSourceProductionTests -v`

Expected: 全部 `OK`。

- [ ] **Step 7: 提交生成结果**

```powershell
git add fagui xunlian zhuangbei zoufang docs/public-source-index-audit.md tests/test_public_source_index.py
git commit -m "feat: add public source references to content pages"
```

---

### Task 10: 执行发布门禁、全量回归与人工视觉检查

**Files:**
- Modify only if a verified defect is found in files already in scope

**Interfaces:**
- Consumes: 完整台账、生成 HTML、样式和现有站点测试
- Produces: 来源索引完成证据和明确的保密审核阻止状态

- [ ] **Step 1: 运行全量自动测试**

Run: `python -m unittest discover -s tests -p "test_*.py" -v`

Expected: 所有测试 `OK`，包括现有敏感内容删除、品牌、主题和菜单回归测试。

- [ ] **Step 2: 检查生成一致性和 Git 差异**

Run: `python tools/public_source_index.py check`

Expected: 来源覆盖严格检查通过。

Run: `python tools/public_source_index.py write --check`

Expected: `0 files differ`。

Run: `git diff --check`

Expected: 无输出，退出码 `0`。

- [ ] **Step 3: 验证发布门禁保持关闭**

Run: `python tools/public_source_index.py check-publish`

Expected before authorized review: 退出码 `1`，逐页报告 `review_status=pending`，且明确输出“公开来源已核验不等于保密审查通过”。这属于正确的安全结果，不得为了让命令变绿而伪造审核人、审核日期或 `approved` 状态。

- [ ] **Step 4: 启动本地预览**

Run from `xunfang-baike`: `python -m http.server 8000`

打开至少以下页面进行桌面和窄屏检查：

- `http://localhost:8000/fagui/faly-yiju.html`
- `http://localhost:8000/xunlian/dunpai-jishu.html`
- `http://localhost:8000/zhuangbei/jingxie-jinggao.html`
- `http://localhost:8000/zoufang/xiaoyuan-fankong.html`

确认引用跳转、返回引用、长标题和 URL 换行、外链、新窗口、安全属性、夜间主题、上一篇/下一篇导航及浏览器控制台无错误。

- [ ] **Step 5: 抽样复核来源正文**

每个模块至少抽查两页，每页至少抽查两个引用；重新打开原文，确认标题、发布主体、核验日期和相似内容说明准确。高风险的法律、战术和警械页面必须列入抽样。

- [ ] **Step 6: 复核工作树边界**

Run: `git status --short`

Expected: 只包含本任务已提交文件以及任务开始前就存在的未跟踪 `公安警察工作汇报PPT.pptx`；不得提交该 PPT。

- [ ] **Step 7: 记录交付边界**

交付说明必须明确：来源索引功能和来源覆盖已完成，但 27 页仍需有权人员执行逐项保密审查；在 `check-publish` 通过前不得据此恢复公网部署。
