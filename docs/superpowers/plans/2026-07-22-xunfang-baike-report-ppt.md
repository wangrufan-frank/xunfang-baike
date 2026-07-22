# “巡防百科”建设情况汇报 PPT Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 依据已确认的设计说明，制作并交付一份约 36 页、内容完整规范、可配合网站现场演示的“巡防百科”建设情况汇报 PPTX。

**Architecture:** 采用演示文稿技能的模板跟随模式，以 `F:\frank第二大脑\1225大型活动现场处置与执法规范专项培训.pptx` 为主模板，逐页审计并把每张输出页映射到可复用的源页面。使用 `@oai/artifact-tool` 导入模板起始稿、编辑继承对象、嵌入真实网站截图与项目图片、导出 PPTX 和逐页渲染；所有中间文件保存在外部可写的可视化工作区，最终文件只写入 `deliverables`。

**Tech Stack:** Node.js ES modules、`@oai/artifact-tool`、演示文稿模板跟随脚本、PowerPoint PPTX、PNG/JPG/WebP 项目素材、PowerShell、演示文稿 QA 工具。

## Global Constraints

- 受众为大队领导和支队领导。
- 汇报时长不设硬性上限；内容完整、逻辑清楚和视觉专业优先。
- 主视觉为 16:9“深蓝权威 × 红色强调”；封面、章节页和结束页深蓝，内容页白色或浅灰蓝。
- 汇报稿八个部分全部纳入，不删除项目不足、安全边界或正式文件优先等限定表述。
- 阶段性数字统一为截至 2026 年 7 月 20 日的 87 条内容、121 个页面。
- 现场演示路径固定为：首页—模块—搜索—内容详情—手机端，并有完整截图兜底。
- 使用项目真实截图和实景素材，不生成假截图、假标识或无法核实的新成果。
- 不使用 `python-pptx`；PPTX 生成和编辑必须使用 `@oai/artifact-tool`。
- 保留原汇报稿和四份参考 PPT，不修改用户现有的其他工作区变更。

---

## File Structure

- Create: `C:\Users\97014\.codex\visualizations\2026\07\22\019f8770-c567-77f2-8977-734681d65c76\codex-presentations\xunfang-report-ppt\tmp\source-notes.txt` — 汇报稿内容、数字口径和素材来源记录。
- Create: `...\tmp\template-audit.txt` — 87 张源页的模板审计、字体、颜色、可复用布局和占位符规则。
- Create: `...\tmp\template-frame-map.json` — 每张输出页到源页和继承对象的完整映射。
- Create: `...\tmp\deviation-log.txt` — 对源布局的所有有意偏离及理由。
- Create: `...\tmp\template-starter.pptx` — 按映射复制源页后形成的编辑起始稿。
- Create: `...\tmp\content-plan.json` — 36 张输出页的标题、正文、图片、截图和版式类型。
- Create: `...\tmp\build-report-deck.mjs` — 导入起始稿、编辑继承对象、嵌入素材、导出和渲染的唯一生成脚本。
- Create: `...\tmp\qa\qa-ledger.txt` — 逐页视觉检查记录、修复结果和最终通过状态。
- Create: `F:\frank第二大脑\xunfang-baike\deliverables\关于巡防百科网站建设及推广应用情况的汇报.pptx` — 最终交付文件。

---

### Task 1: 建立内容与素材清单

**Files:**
- Create: `...\tmp\source-notes.txt`
- Create: `...\tmp\content-plan.json`

**Interfaces:**
- Consumes: `deliverables/关于巡防百科网站建设情况的报告.docx`、`deliverables/site-content-rebuild-screenshots/*`、`deliverables/assets/*`、`img/*`。
- Produces: `content-plan.json`，每项包含 `slideNumber`、`title`、`narrativeRole`、`layoutType`、`body`、`assetPaths`、`fallbackPurpose`。

- [ ] **Step 1: 创建外部工作区并初始化 artifact-tool**

```powershell
& $NODE "$SKILL_DIR\container_tools\setup_artifact_tool_workspace.mjs" --workspace "$TMP_DIR"
```

Expected: `$TMP_DIR\package.json` 和可解析的 `@oai/artifact-tool` 工作区存在。

- [ ] **Step 2: 记录汇报稿内容与准确数字**

把八个章节、六大模块、三级架构、87 条内容、121 个页面、安全边界和五项下一步计划逐项写入 `source-notes.txt`，每项附源文件路径。

- [ ] **Step 3: 建立 36 页内容计划**

`content-plan.json` 的 `layoutType` 只能取以下值：

```json
["cover", "claim-image", "metric", "screenshot-explainer", "process", "module-pair", "hierarchy", "device-comparison", "demo-guide", "boundary", "closing"]
```

每页必须有一个结论式标题；除封面和结束页外，每页至少有一个视觉元素路径或一个明确的流程/结构表达。

- [ ] **Step 4: 验证内容计划完整性**

Run:

```powershell
& $NODE -e "const p=require(process.argv[1]); const n=p.slides.length; const nums=p.slides.map(s=>s.slideNumber); if(n<36||new Set(nums).size!==n||p.slides.some(s=>!s.title||!s.layoutType)) process.exit(1); console.log('CONTENT_PLAN_OK',n)" "$TMP_DIR\content-plan.json"
```

Expected: `CONTENT_PLAN_OK 36` 或更高页数，且退出码为 0。

### Task 2: 审计主模板并建立逐页映射

**Files:**
- Create: `...\tmp\template-audit.txt`
- Create: `...\tmp\template-frame-map.json`
- Create: `...\tmp\deviation-log.txt`
- Create: `...\tmp\template-starter.pptx`

**Interfaces:**
- Consumes: 主模板 PPTX、`content-plan.json`。
- Produces: 已验证的输出页映射和只包含复制源页的 `template-starter.pptx`。

- [ ] **Step 1: 检查全部 87 张源页**

```powershell
& $NODE "$SKILL_DIR\template_following_scripts\inspect_template_deck.mjs" --workspace "$TMP_DIR" --pptx "F:\frank第二大脑\1225大型活动现场处置与执法规范专项培训.pptx"
```

Expected: `template-manifest.json`、87 张渲染图、87 份布局信息和 `template-inspect.ndjson`。

- [ ] **Step 2: 完整查看源页接触表与重点源页全尺寸渲染**

至少识别封面、目录、章节页、观点大图、主截图解读、流程、数据、双图对照和结束页九类可复用布局，并把字体、字号、颜色、边距、页码和占位符规则写入 `template-audit.txt`。

- [ ] **Step 3: 为每张输出页填写继承对象映射**

每个 `outputSlides[]` 项必须包含 `outputSlide`、`sourceSlide`、`narrativeRole`、`reuseMode: "duplicate-slide"` 和 `editTargets`。`editTargets` 中的 `shapeId` 必须逐项复制自本次生成的 `template-inspect.ndjson`，并通过 `validate_template_plan.mjs` 验证；不得使用示例值或推测值。空结构占位符必须明确标记为 `rewrite`、`fill-placeholder` 或 `delete`，不得用新增文本框遮盖。

- [ ] **Step 4: 验证映射并生成起始稿**

```powershell
& $NODE "$SKILL_DIR\template_following_scripts\validate_template_plan.mjs" --workspace "$TMP_DIR" --map "$TMP_DIR\template-frame-map.json"
& $NODE "$SKILL_DIR\template_following_scripts\prepare_template_starter_deck.mjs" --workspace "$TMP_DIR" --pptx "F:\frank第二大脑\1225大型活动现场处置与执法规范专项培训.pptx" --map "$TMP_DIR\template-frame-map.json" --out "$TMP_DIR\template-starter.pptx" --preview-dir "$TMP_DIR\template-starter-preview" --layout-dir "$TMP_DIR\template-starter-layout" --contact-sheet "$TMP_DIR\template-starter-contact-sheet.png"
```

Expected: 映射验证通过，起始稿页数与 `content-plan.json` 一致。

### Task 3: 编辑继承对象并嵌入真实素材

**Files:**
- Create: `...\tmp\build-report-deck.mjs`
- Modify: `...\tmp\deviation-log.txt`
- Create: `deliverables/关于巡防百科网站建设及推广应用情况的汇报.pptx`

**Interfaces:**
- Consumes: `template-starter.pptx`、`content-plan.json`、`template-frame-map.json`、真实截图与实景图片。
- Produces: 最终 PPTX、逐页 PNG、布局 JSON 和接触表。

- [ ] **Step 1: 在生成脚本中定义唯一数据流**

脚本必须实现并只通过以下接口完成工作：

```js
/** @typedef {{starterPptx:string, contentPlan:string, frameMap:string, outputPptx:string, previewDir:string, layoutDir:string}} BuildPaths */
/** @typedef {{slideNumber:number, title:string, narrativeRole:string, layoutType:string, body:string[], assetPaths:string[], fallbackPurpose:string}} SlidePlan */
/** @typedef {{outputSlide:number, sourceSlide:number, narrativeRole:string, reuseMode:"duplicate-slide", editTargets:Array<{shapeId:string, action:string, role:string}>}} FrameMapEntry */
```

`loadInputs(paths: BuildPaths)` 返回导入后的 presentation、`SlidePlan[]` 和 `FrameMapEntry[]`；`editInheritedSlide(presentation, slidePlan, frameMapEntry)` 只解析并编辑 `editTargets` 指向的继承对象；`replaceInheritedImage(slide, targetId, assetPath, fit)` 使用真实图片字节替换继承图片；`rewriteInheritedText(slide, targetId, text)` 保留继承文本框的字体、字号、行距、内边距和对齐；`exportArtifacts(...)` 写出 PPTX、逐页 PNG、逐页布局 JSON 和接触表。`main()` 必须只导入 `template-starter.pptx`，不得调用 `presentation.slides.add()`。

- [ ] **Step 2: 按四类主版式和辅助版式实现全部页面**

实际页面必须满足：观点页使用一条结论和一张主图；截图页截图占主视觉；流程页只表达一个关系；设备页同时展示电脑和手机；安全边界页保留限定性表述；下一步计划每项单独成页。

- [ ] **Step 3: 加入现场演示与截图兜底**

演示导航页显示首页、模块、搜索、详情、手机端五步；对应五步均在前后页面中有真实截图，不依赖现场网络才能完成汇报。

- [ ] **Step 4: 导出 PPTX 和 QA 文件**

```powershell
& $NODE "$TMP_DIR\build-report-deck.mjs"
```

Expected: 最终 PPTX 存在且非空，`$PREVIEW_DIR` 中逐页 PNG 数量与 PPTX 页数一致，`$LAYOUT_DIR\final` 中逐页布局 JSON 数量一致。

### Task 4: 自动化结构与模板一致性检查

**Files:**
- Create: `...\tmp\qa\qa-ledger.txt`

**Interfaces:**
- Consumes: 最终 PPTX、最终布局 JSON、起始稿和映射。
- Produces: 自动检查结果与需要修复的页码清单。

- [ ] **Step 1: 运行页面越界检查**

```powershell
& $PYTHON "$SKILL_DIR\container_tools\slides_test.py" "F:\frank第二大脑\xunfang-baike\deliverables\关于巡防百科网站建设及推广应用情况的汇报.pptx"
```

Expected: 无内容超出 16:9 页面边界。

- [ ] **Step 2: 运行模板一致性检查**

```powershell
& $NODE "$SKILL_DIR\template_following_scripts\check_template_fidelity.mjs" --workspace "$TMP_DIR" --starter-pptx "$TMP_DIR\template-starter.pptx" --final-pptx "F:\frank第二大脑\xunfang-baike\deliverables\关于巡防百科网站建设及推广应用情况的汇报.pptx" --map "$TMP_DIR\template-frame-map.json" --starter-layout-dir "$TMP_DIR\template-starter-layout" --final-layout-dir "$LAYOUT_DIR\final" --edit-dir "$TMP_DIR"
```

Expected: 所有继承对象编辑均在映射范围内，无空占位符，无模板关键标识丢失。

- [ ] **Step 3: 检查内容口径**

搜索最终检查输出，确认只出现 `87`、`121`、`2026年7月20日` 的已确认口径；检查“内部试用”“正式文件优先”“未经审查不扩展”均至少出现一次。

### Task 5: 逐页视觉 QA 与最终交付

**Files:**
- Modify: `...\tmp\build-report-deck.mjs`
- Modify: `...\tmp\qa\qa-ledger.txt`
- Modify: `deliverables/关于巡防百科网站建设及推广应用情况的汇报.pptx`

**Interfaces:**
- Consumes: 每张最终渲染 PNG、内容计划和模板映射。
- Produces: 逐页检查通过的最终 PPTX。

- [ ] **Step 1: 逐页全尺寸检查**

对每张 PNG 检查标题层级、意外换行、文字溢出、截图裁切、图片清晰度、间距、对齐、红色强调比例、页码和章节标识；把每页结果写入 `qa-ledger.txt`。

- [ ] **Step 2: 修复问题并重新导出**

每次修改后重新运行 `build-report-deck.mjs`、`slides_test.py` 和模板一致性检查。不得通过缩小正文字号掩盖信息过载，优先缩短文案或拆页。

- [ ] **Step 3: 检查整套叙事与演示衔接**

确认开场先给成果，建设闭环逐页展开，六大模块与三级架构完整，演示前后过渡自然，四类应用场景完整，安全治理和当前不足没有弱化，五项下一步计划完整。

- [ ] **Step 4: 最终交付检查**

```powershell
Get-Item -LiteralPath 'F:\frank第二大脑\xunfang-baike\deliverables\关于巡防百科网站建设及推广应用情况的汇报.pptx' | Select-Object FullName,Length,LastWriteTime
```

Expected: 文件存在、非空、修改时间为本次制作时间；原汇报稿和四份参考 PPT 未被修改。
