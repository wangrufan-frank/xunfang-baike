# “巡防百科”汇报PPT讲解稿 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为现有36页《“巡防百科”网站建设及推广应用情况的汇报》制作一份可直接照读、正式但自然、包含现场演示提示的Word逐字讲解稿。

**Architecture:** 先从最终PPT、原汇报稿和已确认设计说明提取稳定事实，形成36页结构化讲稿数据；再使用 `python-docx` 生成A4正式讲稿，最后通过结构测试、DOCX渲染和逐页图像检查完成质量闭环。生成脚本与内容数据分离，便于后续按页修改文字而不破坏版式。

**Tech Stack:** bundled Python 3、python-docx、WordprocessingML、LibreOffice headless、documents skill `render_docx.py`

## Global Constraints

- 汇报对象：大队领导、支队领导。
- 形式：36页逐页对应的完整逐字稿，可基本照读。
- 口吻：正式但自然，符合现场口头表达习惯。
- 时长：不硬性限制15分钟，完整讲解预计30—40分钟，可现场删减。
- 关键数据：6个业务模块、87条内容库存、121个页面。
- 事实边界：不得虚构点击量、使用人数、满意度或推广成效。
- 安全边界：内部学习参考；不替代正式依据和现场履职；当前仅限大队内部试用；未经审查、未经批准不扩大展示。
- 现场演示路径：首页 → 代表性模块 → 关键词搜索 → 内容详情 → 手机端；必须包含“切换网站”和“返回PPT”提示。
- 文档格式：A4纵向、适合打印、首页封面、页眉、页脚页码、36页逐页标题、红色操作提示。
- 设计预设：以 `compact_reference_guide` 为基础，使用命名覆盖 `cn_formal_speaker_notes`：正文“思源宋体 CN Medium”12pt、1.4倍行距，标题“思源黑体 CN Heavy”，深蓝 `#1B3168`，强调红 `#C7202F`。

---

### Task 1: 建立36页讲稿内容模型与完整正文

**Files:**
- Create: `deliverables/xunfang-report-speaker-notes.json`
- Test: `tests/test_xunfang_report_speaker_notes.py`
- Read: `deliverables/关于巡防百科网站建设情况的报告.docx`
- Read: `F:/frank第二大脑/xunfang-baike/deliverables/关于巡防百科网站建设及推广应用情况的汇报.pptx`
- Read: `docs/superpowers/specs/2026-07-22-xunfang-report-speaker-notes-design.md`

**Interfaces:**
- Produces: UTF-8 JSON object `{title, audience, estimated_minutes, slides}`；`slides` 长度固定为36。
- Each slide: `{number: int, title: str, suggested_seconds: int, cue: str, script: str, transition: str}`。
- Consumes: PPT页面顺序、汇报稿事实和设计说明中的语言边界。

- [ ] **Step 1: 写内容结构测试**

测试必须断言：文件可解析；页码为1至36连续整数；所有 `title/script/transition` 非空；第22页含五步演示路径；第23页含“返回PPT”；全文包含6、87、121和四项安全边界；全文不含任何占位词或未经材料支持的成效数据。

Run:

```powershell
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_xunfang_report_speaker_notes -v
```

Expected: FAIL because `deliverables/xunfang-report-speaker-notes.json` does not exist.

- [ ] **Step 2: 编写36页完整逐字稿数据**

页面顺序固定为：

1. 汇报封面；2. 项目定位；3. 阶段性内容基础；4. 基本服务能力；5. 建设背景；6. 面向新警；7. 面向骨干；8. 知识归集；9. 分类整理；10. 网站发布；11. 持续更新；12. 内容架构总览；13. 装备与勤务；14. 训练与警情；15. 法规与送教；16. 三级结构；17. 浏览路径；18. 分类搜索与多媒体；19. 电脑手机双端；20. 阶段性成果与质量；21. 建设工作对应问题；22. 现场演示五步路径；23. 演示返回与应用治理；24. 日常巡逻准备；25. 理论学习；26. 训练备课；27. 复盘讨论与走访送教；28. 内部学习参考边界；29. 内容治理机制；30. 阶段性短板；31. 补充高频需求内容；32. 月度更新机制；33. 每月一学；34. 审核脱密；35. 移动端优化；36. 结束语。

正文写作规则：一般页面250—420字；重点架构、应用和计划页面350—500字；封面和结束页180—260字；每页使用完整口语句，避免列表式堆砌；过渡语不重复下一页标题。

- [ ] **Step 3: 运行内容测试**

Run the unittest command from Step 1.

Expected: `OK`，36页、关键数据、演示提示和安全边界全部通过。

- [ ] **Step 4: 提交内容模型与测试**

```powershell
git add -- deliverables/xunfang-report-speaker-notes.json tests/test_xunfang_report_speaker_notes.py
git commit -m "docs: draft report speaker notes content"
```

### Task 2: 生成正式Word讲解稿

**Files:**
- Create: `tools/build_xunfang_report_speaker_notes.py`
- Create: `deliverables/巡防百科汇报PPT讲解稿.docx`
- Read: `deliverables/xunfang-report-speaker-notes.json`

**Interfaces:**
- Consumes: Task 1 JSON schema。
- Produces: `build_document(content_path: Path, output_path: Path) -> None`。
- Produces: `apply_document_styles(doc: Document) -> None`，统一设置页面、字体、段落和颜色。
- Produces: `add_slide_section(doc: Document, item: dict) -> None`，逐页写入标题、时间、提示、正文和过渡语。

- [ ] **Step 1: 编写生成脚本结构测试**

扩展 `tests/test_xunfang_report_speaker_notes.py`，生成临时DOCX并断言：正文含36个“第X页”；含“操作提示”“建议时间”“过渡”；页眉包含“巡防百科汇报讲解稿”；正文段落不少于180个；输出文件大于50KB。

Expected: FAIL because builder does not exist.

- [ ] **Step 2: 实现固定设计令牌**

使用A4纵向；上2.2cm、下2.0cm、左2.5cm、右2.2cm；页眉1.2cm、页脚1.2cm。正文12pt、1.4倍行距、段后6pt；一级标题18pt深蓝；逐页标题15pt深蓝；元信息10pt灰色；操作提示11pt红色；过渡语11pt灰蓝并加“衔接”标签。页眉左侧为文档名，页脚居中使用Word页码字段。

- [ ] **Step 3: 实现封面与逐页内容**

封面包括主标题“关于‘巡防百科’网站建设及推广应用情况的汇报讲解稿”、副标题“36页PPT配套完整逐字稿”、汇报人“王汝凡”、日期“2026年7月”。正文从新页开始，按JSON顺序写入36节；每节标题启用 `keep_with_next`，避免标题孤行；操作提示仅在非空时显示。

- [ ] **Step 4: 生成DOCX并运行结构测试**

Run:

```powershell
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools/build_xunfang_report_speaker_notes.py --content deliverables/xunfang-report-speaker-notes.json --output deliverables/巡防百科汇报PPT讲解稿.docx
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_xunfang_report_speaker_notes -v
```

Expected: document created and tests report `OK`.

- [ ] **Step 5: 提交生成器与工作树内成品**

```powershell
git add -- tools/build_xunfang_report_speaker_notes.py deliverables/巡防百科汇报PPT讲解稿.docx tests/test_xunfang_report_speaker_notes.py
git commit -m "feat: generate report speaker notes document"
```

### Task 3: 渲染、逐页检查并交付

**Files:**
- Verify: `deliverables/巡防百科汇报PPT讲解稿.docx`
- Scratch: `C:/Users/97014/.codex/visualizations/2026/07/22/019f8770-c567-77f2-8977-734681d65c76/codex-documents/xunfang-speaker-notes/render/`
- Deliver: `F:/frank第二大脑/xunfang-baike/deliverables/巡防百科汇报PPT讲解稿.docx`

**Interfaces:**
- Consumes: Task 2 DOCX。
- Produces: final user-facing DOCX；渲染PNG仅用于内部QA。

- [ ] **Step 1: 渲染DOCX**

Run:

```powershell
$env:PYTHONUTF8='1'
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\97014\.codex\plugins\cache\openai-primary-runtime\documents\26.715.12143\skills\documents\render_docx.py' 'deliverables\巡防百科汇报PPT讲解稿.docx' --output_dir 'C:\Users\97014\.codex\visualizations\2026\07\22\019f8770-c567-77f2-8977-734681d65c76\codex-documents\xunfang-speaker-notes\render'
```

Expected: one or more `page-*.png` files and no conversion failure.

- [ ] **Step 2: 逐页查看100%渲染图**

检查全部页面：无标题孤行、正文截断、重叠、乱码、异常空白、页眉页脚错位；操作提示为红色且不喧宾夺主；页面密度适合打印阅读。

- [ ] **Step 3: 修复并重复渲染**

如发现版式问题，仅修改生成脚本中的设计令牌或分页控制，重新生成DOCX并从Step 1开始复查，直到全部页面通过。

- [ ] **Step 4: 最终结构验证**

Run:

```powershell
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest tests.test_xunfang_report_speaker_notes -v
Get-Item -LiteralPath 'deliverables\巡防百科汇报PPT讲解稿.docx' | Select-Object FullName,Length,LastWriteTime
```

Expected: tests `OK`；DOCX存在且非空。

- [ ] **Step 5: 复制最终成品到用户交付目录**

将工作树内已验证DOCX复制到 `F:/frank第二大脑/xunfang-baike/deliverables/巡防百科汇报PPT讲解稿.docx`，仅覆盖同名讲解稿，不修改现有PPT和原汇报稿。
