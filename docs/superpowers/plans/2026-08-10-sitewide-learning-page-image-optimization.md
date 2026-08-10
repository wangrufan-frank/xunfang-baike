# 全站学习页面配图优化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 对全部 93 个学习页面完成可审计的配图评估，并按学习价值保留、追加或替换图片，形成统一、美观、可追溯且适配移动端的教材信息图体系。

**Architecture:** 以 `data/image-optimization-plan.json` 作为唯一进度与验收台账，由独立校验器对页面、图片、SVG、图注和来源元数据进行约束。先完成全站评估和六个代表页，用户确认视觉方向后按模块逐批实施；每个模块完成时增加永久回归断言，最后执行全站视觉验收和现有完整测试。

**Tech Stack:** HTML5、CSS3、原生 SVG、JSON、Python 3.12 `unittest`、Node.js 20、Playwright（仅视觉验收）。

## Global Constraints

- 范围必须覆盖 `data/content-inventory.json` 中全部 93 个学习页面：装备操作 28 页、勤务工作 13 页、实战训练 15 页、警情处置 6 页、法规制度 17 页、走访教育 14 页。
- 每页必须采用 `keep`、`add`、`replace`、`no-image` 四种决策之一；不得为满足数量添加纯装饰图片。
- 普通知识页通常使用 1 张核心图，仅在存在多个独立知识结构时使用 2 至 3 张。
- SVG 必须具体表现器材、人物、步骤或空间关系，不得只使用通用图标、彩色方框和装饰箭头。
- 图片内文字以当前页面正文为主；新增操作要求、法律结论、处置标准或风险边界必须具有权威公开依据。
- 公开可见不等于允许转载；外部实物图仅可使用用户自有、明确允许复用或具有清晰开放许可的素材。
- 权属不明确的图片不得下载进仓库，改为依据可核验事实绘制原创 SVG。
- 新增图片必须具有准确 `alt`、图注、来源、用途和许可记录。
- 新增图片存放于 `img/learning/<module>/`；现有合格图片不迁移、不改名。
- 图片插入对应正文附近，不集中堆放在页首。
- 所有 SVG 使用 `viewBox`，在 1440px 桌面端和 390px 手机端不得裁切、横向溢出、文字重叠或出现不可读小字。
- 任何批次都不得破坏现有搜索、站内链接、来源台账、认证和主题功能。

---

## File Structure

### 新建文件

- `data/image-optimization-plan.json`：93 页配图评估、资产任务、来源状态和验收状态的唯一台账。
- `tools/check_image_optimization.py`：验证台账覆盖率、运行页面引用、库存元数据和 SVG 合同。
- `tests/test_image_optimization.py`：校验器单元测试、全站台账合同和逐模块完成断言。
- `img/learning/zhuangbei/*`：装备操作模块新增原创 SVG 或许可明确的本地图片。
- `img/learning/qinwu/*`：勤务工作模块新增原创 SVG 或许可明确的本地图片。
- `img/learning/xunlian/*`：实战训练模块新增原创 SVG 或许可明确的本地图片。
- `img/learning/jingqing/*`：警情处置模块新增原创 SVG 或许可明确的本地图片。
- `img/learning/fagui/*`：法规制度模块新增原创 SVG 或许可明确的本地图片。
- `img/learning/zoufang/*`：走访教育模块新增原创 SVG 或许可明确的本地图片。
- `docs/image-optimization-visual-qa.md`：六模块代表页及最终抽样页的桌面、手机视觉验收记录。

### 修改文件

- `css/style.css`：统一学习图片、图廊、图注、窄屏和打印样式。
- `data/content-inventory.json`：记录新增或替换图片的路径、替代文本、来源、来源链接和许可。
- `data/public-sources.json`：仅在图片引入新的知识结论时增加对应权威来源。
- `data/updates.json`：全站配图优化完成后增加更新记录。
- `tools/visual_acceptance.py`：改为读取本轮代表页清单并检查图片溢出。
- `zhuangbei/*.html`、`qinwu/*.html`、`xunlian/*.html`、`jingqing/*.html`、`fagui/*.html`、`zoufang/*.html`：按台账决策保留、追加或替换图片。
- `search-index.json`：页面文字或来源发生变化后由现有工具重建。

### 核心接口

`tools/check_image_optimization.py` 必须公开以下接口：

```python
def inventory_records(root: Path) -> list[dict]: ...
def load_plan(root: Path) -> dict: ...
def validate_plan(root: Path, module: str | None = None) -> list[str]: ...
def validate_runtime(
    root: Path,
    module: str | None = None,
    require_complete: bool = False,
) -> list[str]: ...
```

CLI 合同：

```text
python tools/check_image_optimization.py
python tools/check_image_optimization.py --module zhuangbei
python tools/check_image_optimization.py --module zhuangbei --require-complete
python tools/check_image_optimization.py --require-complete
```

返回码 `0` 表示无错误，`1` 表示发现合同错误，`2` 表示参数或 JSON 无法读取。

---

### Task 1: 建立 93 页评估台账与校验器

**Files:**
- Create: `data/image-optimization-plan.json`
- Create: `tools/check_image_optimization.py`
- Create: `tests/test_image_optimization.py`
- Read: `data/content-inventory.json`

**Interfaces:**
- Consumes: `data/content-inventory.json` 的 `modules[].articles[]`。
- Produces: 上述四个 Python 接口，以及后续模块任务使用的 `pages[]` 台账记录。

- [ ] **Step 1: 写入校验器的失败测试**

在 `tests/test_image_optimization.py` 写入基础合同：

```python
import json
import tempfile
import unittest
from pathlib import Path

from tools.check_image_optimization import validate_plan, validate_runtime

ROOT = Path(__file__).resolve().parents[1]


class ImageOptimizationPlanTests(unittest.TestCase):
    def test_plan_covers_inventory_exactly_once(self):
        plan = json.loads((ROOT / "data/image-optimization-plan.json").read_text(encoding="utf-8"))
        inventory = json.loads((ROOT / "data/content-inventory.json").read_text(encoding="utf-8"))
        planned = [page["path"] for page in plan["pages"]]
        expected = [
            article["path"]
            for module in inventory["modules"]
            for article in module["articles"]
        ]
        self.assertEqual(93, len(planned))
        self.assertEqual(sorted(expected), sorted(planned))
        self.assertEqual(93, len(set(planned)))

    def test_current_plan_is_schema_valid(self):
        self.assertEqual([], validate_plan(ROOT))

    def test_completed_assets_match_runtime(self):
        self.assertEqual([], validate_runtime(ROOT))
```

- [ ] **Step 2: 运行测试并确认缺少模块**

Run:

```powershell
python -m unittest tests.test_image_optimization -v
```

Expected: FAIL，错误包含 `ModuleNotFoundError: No module named 'tools.check_image_optimization'`。

- [ ] **Step 3: 实现 JSON 结构和纯校验函数**

台账顶层结构固定为：

```json
{
  "version": 1,
  "updated_at": "2026-08-10",
  "pages": []
}
```

每个 `pages[]` 记录固定包含：

```json
{
  "path": "jingqing/zuijiu-lei.html",
  "module": "jingqing",
  "current_images": 0,
  "decision": "add",
  "reason": "正文包含连续处置阶段，流程图可降低理解成本",
  "learning_targets": ["风险识别", "沟通与安全控制", "记录交接"],
  "visual_types": ["step-flow"],
  "insertion_points": ["风险分析段落之后"],
  "assets": [
    {
      "path": "img/learning/jingqing/zuijiu-lei-chuzhi-flow.svg",
      "kind": "svg",
      "purpose": "把正文处置阶段压缩为可扫描流程",
      "source_status": "original",
      "source_url": "",
      "publisher": "巡防百科",
      "accessed_at": "2026-08-10",
      "license": "本站原创",
      "status": "planned"
    }
  ],
  "implementation_status": "not-started",
  "acceptance_status": "not-reviewed",
  "blocked_reason": ""
}
```

允许值固定为：

```python
DECISIONS = {"keep", "add", "replace", "no-image"}
VISUAL_TYPES = {
    "structure-label", "step-flow", "scene-zone",
    "comparison", "checklist", "legal-relationship",
}
IMPLEMENTATION_STATUSES = {"not-started", "in-progress", "complete", "blocked"}
ACCEPTANCE_STATUSES = {"not-reviewed", "accepted", "blocked"}
ASSET_STATUSES = {"planned", "complete", "blocked"}
```

`validate_plan()` 必须检查：精确覆盖 93 页、路径唯一、模块匹配、决策和状态合法、理由非空、`add`/`replace` 至少有一个资产、`no-image` 不含资产、外部图片来源字段完整。

`validate_runtime()` 必须仅检查 `complete` 记录：资产文件存在、HTML 引用资产、库存记录含资产、SVG 可解析且包含 `viewBox`、`title`、`desc`，SVG 不包含 `http://`、`https://` 或外链 `href`。

当 `require_complete=True` 时，每页必须处于以下一种终态：`implementation_status: complete` 且 `acceptance_status: accepted`；或者 `implementation_status: blocked`、`acceptance_status: blocked` 且 `blocked_reason` 明确写出无法确认的素材权属、正文依据或图示含义。终态为 `blocked` 的页面不得包含状态为 `complete` 的新增资产。

- [ ] **Step 4: 逐页完成人工评估**

从 `content-inventory.json` 精确生成 93 条路径后，逐页阅读正文和现有 `<figure>`。每条记录必须写出具体 `reason`、`learning_targets`、`visual_types` 和 `insertion_points`；不得用“补充配图”“优化体验”等通用措辞代替页面判断。

已有图片的 `current_images` 必须与 HTML 中 `<img>` 数量一致。`keep` 页面将 `implementation_status` 设为 `complete`，但只有完成来源与显示检查后才将 `acceptance_status` 设为 `accepted`。

- [ ] **Step 5: 运行台账测试**

Run:

```powershell
python -m unittest tests.test_image_optimization -v
python tools/check_image_optimization.py
```

Expected: PASS；输出包含 `93 pages checked` 和 `0 validation errors`。

- [ ] **Step 6: 提交**

```powershell
git add data/image-optimization-plan.json tools/check_image_optimization.py tests/test_image_optimization.py
git commit -m "test: 建立全站配图评估与校验合同"
```

---

### Task 2: 建立共享样式并完成六模块代表页

**Files:**
- Modify: `css/style.css`
- Modify: `zhuangbei/zhifa-jiuyi.html`
- Modify: `xunlian/geren-fanghu-anquan.html`
- Modify: `jingqing/zuijiu-lei.html`
- Modify: `qinwu/gonggong-zhixu-goutong-jilu.html`
- Modify: `fagui/panwen-shenfenzheng.html`
- Modify: `zoufang/changsuo-aed-jiancha.html`
- Modify: `data/content-inventory.json`
- Modify: `data/image-optimization-plan.json`
- Create: six representative assets below `img/learning/<module>/`
- Modify: `tests/test_image_optimization.py`

**Interfaces:**
- Consumes: Task 1 的台账记录与校验器。
- Produces: `.learning-figure` HTML/CSS 合同和经用户确认的视觉基线。

- [ ] **Step 1: 写共享样式失败测试**

```python
def test_learning_figure_styles_cover_media_caption_mobile_and_print(self):
    css = (ROOT / "css/style.css").read_text(encoding="utf-8")
    for selector in (
        ".learning-figure",
        ".learning-figure__media",
        ".learning-figure figcaption",
        "@media (max-width: 640px)",
        "@media print",
    ):
        self.assertIn(selector, css)
```

- [ ] **Step 2: 运行测试确认缺少共享样式**

Run: `python -m unittest tests.test_image_optimization -v`

Expected: FAIL，缺少 `.learning-figure`。

- [ ] **Step 3: 添加共享图片样式**

在 `css/style.css` 的 `.article-gallery` 规则附近增加以下基线；实现时可以使用仓库现有等价颜色变量，但不得改变选择器和布局合同：

```css
.learning-figure {
    width: min(100%, 54rem);
    margin: 1.5rem auto;
    break-inside: avoid;
}

.learning-figure__media {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(18rem, 100%), 1fr));
    gap: 1rem;
    padding: 1rem;
    border: 1px solid var(--border);
    border-radius: 14px;
    background: var(--card-bg);
}

.learning-figure__media img {
    display: block;
    width: 100%;
    height: auto;
    min-width: 0;
    border-radius: 10px;
}

.learning-figure figcaption {
    margin-top: 0.65rem;
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.6;
    text-align: center;
}

@media (max-width: 640px) {
    .learning-figure__media {
        grid-template-columns: minmax(0, 1fr);
        padding: 0.7rem;
    }
}

@media print {
    .learning-figure,
    .learning-figure__media {
        break-inside: avoid;
        box-shadow: none;
    }
}
```

不得为每个页面添加内联样式。

页面统一使用：

```html
<figure class="learning-figure">
  <div class="learning-figure__media">
    <img loading="lazy" src="../img/learning/jingqing/zuijiu-lei-chuzhi-flow.svg" alt="醉酒类警情从风险识别到记录交接的处置流程信息图">
  </div>
  <figcaption>醉酒类警情处置流程：风险识别、沟通控制、协同处置与记录交接（本站绘制）</figcaption>
</figure>
```

- [ ] **Step 4: 制作六张代表图**

按批准的教材信息图体系制作：

- `img/learning/zhuangbei/zhifa-jiuyi-structure.svg`：结构标注图。
- `img/learning/xunlian/geren-fanghu-anquan-checklist.svg`：教材清单图。
- `img/learning/jingqing/zuijiu-lei-chuzhi-flow.svg`：分步流程图。
- `img/learning/qinwu/gonggong-zhixu-goutong-record.svg`：场景分区与记录要素图。
- `img/learning/fagui/panwen-shenfenzheng-procedure.svg`：法规程序关系图。
- `img/learning/zoufang/changsuo-aed-jiancha.svg`：检查清单与场所分区图。

每张图必须具有可辨认的人物、器材或场景对象，并含 `<title>`、`<desc>` 和响应式 `viewBox`。

- [ ] **Step 5: 插入代表页并同步台账**

将每张图片插入其 `insertion_points` 指定段落之后。更新 `content-inventory.json` 的 `images[]`，并将六条计划记录的资产、实施和验收状态同步为实际状态。

- [ ] **Step 6: 运行结构验证**

Run:

```powershell
python -m unittest tests.test_image_optimization tests.test_site_structure -v
python tools/check_image_optimization.py
python tools/check_site_links.py
```

Expected: PASS；无图片路径、结构或链接错误。

- [ ] **Step 7: 截取六页桌面和手机视图并请求用户确认**

使用 1440×900 和 390×900 两种视口，检查：图片内文字可读、无横向滚动、器材与人物直接可辨、图注换行正常、深色主题容器对比正常。把结论和截图路径写入 `docs/image-optimization-visual-qa.md`。

在用户明确接受六张代表图之前，不开始 Task 3。

- [ ] **Step 8: 提交视觉基线**

```powershell
git add css/style.css data/content-inventory.json data/image-optimization-plan.json tests/test_image_optimization.py docs/image-optimization-visual-qa.md zhuangbei/zhifa-jiuyi.html xunlian/geren-fanghu-anquan.html jingqing/zuijiu-lei.html qinwu/gonggong-zhixu-goutong-jilu.html fagui/panwen-shenfenzheng.html zoufang/changsuo-aed-jiancha.html img/learning
git commit -m "feat: 建立学习页面教材信息图视觉基线"
```

---

### Task 3: 完成装备操作模块 28 页

**Files:**
- Modify: `zhuangbei/*.html`
- Create/Modify: `img/learning/zhuangbei/*`
- Modify: `data/content-inventory.json`
- Modify: `data/image-optimization-plan.json`
- Modify: `data/public-sources.json` only when a new factual claim is added
- Modify: `tests/test_image_optimization.py`

**Interfaces:**
- Consumes: `validate_runtime(ROOT, module="zhuangbei", require_complete=True)`。
- Produces: 28 页全部进入 `accepted` 或有明确原因的 `blocked` 终态。

- [ ] **Step 1: 添加装备模块完成断言并确认失败**

```python
def test_equipment_image_optimization_is_complete(self):
    self.assertEqual(
        [],
        validate_runtime(ROOT, module="zhuangbei", require_complete=True),
    )
```

Run: `python -m unittest tests.test_image_optimization -v`

Expected: FAIL，并列出尚未完成的装备页面。

- [ ] **Step 2: 按台账完成“认识对象”资产**

对需要实物识别的页面，优先保留现有合格图片；只有许可信息明确时才新增外部实物图。权属不明确时绘制原创结构标注 SVG，不使用搜索结果缩略图或商品宣传图。

- [ ] **Step 3: 按台账完成“理解结构与检查”资产**

逐页实现 `structure-label`、`comparison` 或 `checklist` 资产。图中文字必须来自正文或已登记权威来源，并插入对应段落附近。

- [ ] **Step 4: 同步 28 页 HTML、库存和计划状态**

对每页执行：核对 `<img>`、`alt`、`figcaption`；更新 `content-inventory.json.images[]`；将完成的资产设为 `complete`，页面设为 `implementation_status: complete` 和 `acceptance_status: accepted`。

- [ ] **Step 5: 验证并提交**

Run:

```powershell
python tools/check_image_optimization.py --module zhuangbei --require-complete
python -m unittest tests.test_image_optimization tests.test_site_structure -v
python tools/check_site_links.py
```

Expected: PASS，28 页无错误。

```powershell
git add zhuangbei img/learning/zhuangbei data/content-inventory.json data/image-optimization-plan.json data/public-sources.json tests/test_image_optimization.py
git commit -m "feat: 完成装备操作页面配图优化"
```

---

### Task 4: 完成实战训练模块 15 页

**Files:**
- Modify: `xunlian/*.html`
- Create/Modify: `img/learning/xunlian/*`
- Modify: `data/content-inventory.json`
- Modify: `data/image-optimization-plan.json`
- Modify: `data/public-sources.json` only when a new factual claim is added
- Modify: `tests/test_image_optimization.py`

**Interfaces:**
- Consumes: `validate_runtime(ROOT, module="xunlian", require_complete=True)`。
- Produces: 15 页全部进入 `accepted` 或有明确原因的 `blocked` 终态。

- [ ] **Step 1: 添加训练模块完成断言并确认失败**

```python
def test_training_image_optimization_is_complete(self):
    self.assertEqual([], validate_runtime(ROOT, module="xunlian", require_complete=True))
```

- [ ] **Step 2: 完成动作、分工和复盘资产**

按台账为每页选择 `step-flow`、`scene-zone`、`comparison` 或 `checklist`。动作图必须表达阶段与相对关系，但不得超出正文和公开依据增加战术细节；人物使用形象化扁平插画，不使用火柴人。

- [ ] **Step 3: 同步页面、库存、来源和计划状态**

已有动作图若清晰且充分则保留；不足时追加解释图，质量不合格时替换。逐页完成 HTML、`content-inventory.json` 和计划状态同步。

- [ ] **Step 4: 验证并提交**

Run:

```powershell
python tools/check_image_optimization.py --module xunlian --require-complete
python -m unittest tests.test_image_optimization tests.test_site_structure -v
python tools/check_site_links.py
```

Expected: PASS，15 页无错误。

```powershell
git add xunlian img/learning/xunlian data/content-inventory.json data/image-optimization-plan.json data/public-sources.json tests/test_image_optimization.py
git commit -m "feat: 完成实战训练页面配图优化"
```

---

### Task 5: 完成警情处置模块 6 页

**Files:**
- Modify: `jingqing/*.html`
- Create/Modify: `img/learning/jingqing/*`
- Modify: `data/content-inventory.json`
- Modify: `data/image-optimization-plan.json`
- Modify: `data/public-sources.json` only when a new factual claim is added
- Modify: `tests/test_image_optimization.py`

**Interfaces:**
- Consumes: `validate_runtime(ROOT, module="jingqing", require_complete=True)`。
- Produces: 6 页全部进入 `accepted` 或有明确原因的 `blocked` 终态。

- [ ] **Step 1: 添加警情模块完成断言并确认失败**

```python
def test_incident_image_optimization_is_complete(self):
    self.assertEqual([], validate_runtime(ROOT, module="jingqing", require_complete=True))
```

- [ ] **Step 2: 完成流程、沟通和风险关系图**

以 `step-flow` 和 `scene-zone` 为主，使用中性、非污名化的人物表现。涉及醉酒、自伤和精神障碍的图片不得夸张危险性，不展示可模仿的伤害细节；图中文字严格以正文和权威来源为界。

- [ ] **Step 3: 同步页面、库存、来源和计划状态**

逐页核对流程顺序、人物关系、风险提示、图注和来源。所有 6 页完成后设为 `accepted`。

- [ ] **Step 4: 验证并提交**

Run:

```powershell
python tools/check_image_optimization.py --module jingqing --require-complete
python -m unittest tests.test_image_optimization tests.test_site_structure -v
python tools/check_site_links.py
```

Expected: PASS，6 页无错误。

```powershell
git add jingqing img/learning/jingqing data/content-inventory.json data/image-optimization-plan.json data/public-sources.json tests/test_image_optimization.py
git commit -m "feat: 完成警情处置页面配图优化"
```

---

### Task 6: 完成勤务工作模块 13 页

**Files:**
- Modify: `qinwu/*.html`
- Create/Modify: `img/learning/qinwu/*`
- Modify: `data/content-inventory.json`
- Modify: `data/image-optimization-plan.json`
- Modify: `data/public-sources.json` only when a new factual claim is added
- Modify: `tests/test_image_optimization.py`

**Interfaces:**
- Consumes: `validate_runtime(ROOT, module="qinwu", require_complete=True)`。
- Produces: 13 页全部进入 `accepted` 或有明确原因的 `blocked` 终态。

- [ ] **Step 1: 添加勤务模块完成断言并确认失败**

```python
def test_duty_image_optimization_is_complete(self):
    self.assertEqual([], validate_runtime(ROOT, module="qinwu", require_complete=True))
```

- [ ] **Step 2: 完成场景、流程、记录和协同资产**

大型活动、场所走访和公共秩序页面使用 `scene-zone`、`step-flow` 与 `checklist`。场景图只表达正文已有的角色、区域和信息流，不绘制具体部署参数或正文没有的行动路线。

- [ ] **Step 3: 同步页面、库存、来源和计划状态**

逐页把图片放在对应流程或记录段落之后，更新图片元数据和页面状态。

- [ ] **Step 4: 验证并提交**

Run:

```powershell
python tools/check_image_optimization.py --module qinwu --require-complete
python -m unittest tests.test_image_optimization tests.test_site_structure -v
python tools/check_site_links.py
```

Expected: PASS，13 页无错误。

```powershell
git add qinwu img/learning/qinwu data/content-inventory.json data/image-optimization-plan.json data/public-sources.json tests/test_image_optimization.py
git commit -m "feat: 完成勤务工作页面配图优化"
```

---

### Task 7: 完成法规制度模块 17 页

**Files:**
- Modify: `fagui/*.html`
- Create/Modify: `img/learning/fagui/*`
- Modify: `data/content-inventory.json`
- Modify: `data/image-optimization-plan.json`
- Modify: `data/public-sources.json`
- Modify: `tests/test_image_optimization.py`

**Interfaces:**
- Consumes: `validate_runtime(ROOT, module="fagui", require_complete=True)`。
- Produces: 17 页全部进入 `accepted` 或有明确原因的 `blocked` 终态。

- [ ] **Step 1: 添加法规模块完成断言并确认失败**

```python
def test_legal_image_optimization_is_complete(self):
    self.assertEqual([], validate_runtime(ROOT, module="fagui", require_complete=True))
```

- [ ] **Step 2: 完成程序、权利义务和适用关系图**

短知识页优先使用 `legal-relationship`、`step-flow` 和 `comparison`。法规全文页仅在导读关系图能够显著提升查阅效率时配图；不得把信息图写成法条替代文本，不得改变法条条件、主体和例外。

- [ ] **Step 3: 逐图核对权威依据**

对每个法律结论逐项核对页面现有官方链接或新增官方来源。图注标明“导读示意，具体以法规原文为准”，并确保法规正文保持完整可复制。

- [ ] **Step 4: 同步页面、库存、来源和计划状态**

更新 17 页对应记录；对两个骨架法规页面若图片不能提升理解，将决策设为 `no-image` 并写出具体原因，不用配图掩盖正文未收录状态。

- [ ] **Step 5: 验证并提交**

Run:

```powershell
python tools/check_image_optimization.py --module fagui --require-complete
python -m unittest tests.test_image_optimization tests.test_legal_documents tests.test_site_structure -v
python tools/public_source_index.py check
python tools/check_site_links.py
```

Expected: PASS，17 页无错误，法规正文和来源保持一致。

```powershell
git add fagui img/learning/fagui data/content-inventory.json data/image-optimization-plan.json data/public-sources.json tests/test_image_optimization.py
git commit -m "feat: 完成法规制度页面配图优化"
```

---

### Task 8: 完成走访教育模块 14 页

**Files:**
- Modify: `zoufang/*.html`
- Create/Modify: `img/learning/zoufang/*`
- Modify: `data/content-inventory.json`
- Modify: `data/image-optimization-plan.json`
- Modify: `data/public-sources.json` only when a new factual claim is added
- Modify: `tests/test_image_optimization.py`

**Interfaces:**
- Consumes: `validate_runtime(ROOT, module="zoufang", require_complete=True)`。
- Produces: 14 页全部进入 `accepted` 或有明确原因的 `blocked` 终态。

- [ ] **Step 1: 添加教育模块完成断言并确认失败**

```python
def test_education_image_optimization_is_complete(self):
    self.assertEqual([], validate_runtime(ROOT, module="zoufang", require_complete=True))
```

- [ ] **Step 2: 完成检查、考核、复盘和资料管理资产**

使用 `checklist`、`comparison` 和 `step-flow`，把正文中的检查项、评价维度和资料流转关系压缩为可扫描信息图。图片不代替正式表单，不新增未在正文或权威来源中定义的评分标准。

- [ ] **Step 3: 同步页面、库存、来源和计划状态**

逐页核对图文对应关系、文字密度、图注和来源，将 14 页设为 `accepted`。

- [ ] **Step 4: 验证并提交**

Run:

```powershell
python tools/check_image_optimization.py --module zoufang --require-complete
python -m unittest tests.test_image_optimization tests.test_site_structure -v
python tools/check_site_links.py
```

Expected: PASS，14 页无错误。

```powershell
git add zoufang img/learning/zoufang data/content-inventory.json data/image-optimization-plan.json data/public-sources.json tests/test_image_optimization.py
git commit -m "feat: 完成走访教育页面配图优化"
```

---

### Task 9: 完成全站索引、更新记录和自动化合同

**Files:**
- Modify: `data/updates.json`
- Modify: `search-index.json`
- Modify: `.github/workflows/validate.yml`
- Modify: `tests/test_image_optimization.py`

**Interfaces:**
- Consumes: 六模块全部 `accepted` 的台账。
- Produces: CI 中强制执行的全站配图完成合同。

- [ ] **Step 1: 添加全站完成和 CI 失败测试**

```python
def test_sitewide_image_optimization_is_complete(self):
    self.assertEqual([], validate_runtime(ROOT, require_complete=True))

def test_ci_runs_image_optimization_check(self):
    workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
    self.assertIn("python tools/check_image_optimization.py --require-complete", workflow)
```

- [ ] **Step 2: 运行测试确认 CI 尚未调用新校验器**

Run: `python -m unittest tests.test_image_optimization -v`

Expected: FAIL，缺少 CI 命令。

- [ ] **Step 3: 接入 CI 并更新记录**

在 `.github/workflows/validate.yml` 的来源台账检查之后增加：

```yaml
      - name: Check learning-page image optimization
        run: python tools/check_image_optimization.py --require-complete
```

在 `data/updates.json` 增加一条 2026-08 的全站图文学习优化记录，准确写明评估 93 页，并按台账统计实际新增、替换、保留和无需配图数量，不预先写死统计值。

- [ ] **Step 4: 重建搜索索引**

Run:

```powershell
python tools/build_search_index.py
python tools/build_search_index.py --check
```

Expected: 第二条命令输出 `search-index.json matches 93 records`。

- [ ] **Step 5: 验证并提交**

Run:

```powershell
python -m unittest tests.test_image_optimization tests.test_repository_consolidation -v
python tools/check_image_optimization.py --require-complete
```

Expected: PASS。

```powershell
git add .github/workflows/validate.yml data/updates.json search-index.json tests/test_image_optimization.py
git commit -m "ci: 强制校验全站学习页面配图合同"
```

---

### Task 10: 执行最终视觉验收与完整回归

**Files:**
- Modify: `tools/visual_acceptance.py`
- Modify: `docs/image-optimization-visual-qa.md`
- Modify: affected HTML/CSS/SVG files only when visual defects are found

**Interfaces:**
- Consumes: 已完成的 93 页和 `image-optimization-plan.json`。
- Produces: 可复核的桌面、手机视觉验收记录和全绿验证结果。

- [ ] **Step 1: 扩展视觉验收脚本**

让 `tools/visual_acceptance.py` 从评估台账中选择每模块至少 2 页：一页最长图片内文字、一页包含最多图片；同时保留 6 个代表页。每页截取 1440×900 和 390×900 两种视口。

增加以下运行时断言：

```python
overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 5")
assert not overflow
for image in page.locator(".learning-figure img").all():
    box = image.bounding_box()
    assert box and box["width"] > 0 and box["height"] > 0
```

- [ ] **Step 2: 运行视觉验收**

Run: `python tools/visual_acceptance.py`

Expected: 所有抽样页生成桌面和手机截图，无横向溢出和零尺寸图片。

- [ ] **Step 3: 人工检查并记录结果**

在 `docs/image-optimization-visual-qa.md` 对每个抽样页记录：

- 图片内文字是否可读
- 人物、器材、步骤和空间关系是否直接可辨
- 图片是否与相邻正文一致
- 图注是否正确换行
- 暖警蓝、经典暖棕、日光和夜间主题下是否保持对比
- 是否存在过度抽象、重复或装饰性内容

发现问题时修复对应 HTML、CSS 或 SVG，并重新执行该页两种视口截图。

- [ ] **Step 4: 运行完整仓库验证**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/auth_core.test.js
python tools/build_search_index.py --check
python tools/check_site_links.py
python tools/public_source_index.py check
python tools/check_image_optimization.py --require-complete
git diff --check
```

Expected: Python 和 Node 测试通过；搜索索引匹配 93 条；129 个页面无断链；来源台账无待验证点；93 页配图合同通过；`git diff --check` 无输出。

- [ ] **Step 5: 提交最终验收修正**

```powershell
git add tools/visual_acceptance.py docs/image-optimization-visual-qa.md css/style.css data img zhuangbei qinwu xunlian jingqing fagui zoufang search-index.json
git commit -m "test: 完成全站配图视觉验收"
```
