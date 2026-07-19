# “巡防百科”网站项目报告 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 生成一份内容真实、格式规范、面向支队及公安局领导的“巡防百科”网站建设与推广应用情况报告 `.docx`，并完成结构检查和逐页视觉验收。

**Architecture:** 使用一个独立的 Python 构建脚本集中管理报告事实、正文段落和中文公文样式，通过 `python-docx` 生成 DOCX。使用结构测试检查标题、章节、数字口径、敏感词和页面设置，再使用文档技能提供的 `render_docx.py` 转为逐页 PNG，人工检查后按需迭代。

**Tech Stack:** Bundled Python 3、python-docx、OOXML、LibreOffice、Poppler、Codex documents renderer。

## Global Constraints

- 最终文件路径：`deliverables/关于巡防百科网站建设及推广应用情况的报告.docx`。
- 纸张为 A4 纵向，页边距上 37 毫米、下 35 毫米、左 28 毫米、右 26 毫米。
- 标题使用方正小标宋简体二号；兼容回退为小标宋体或宋体加粗。
- 正文使用仿宋_GB2312三号、固定值 28 磅、两端对齐、首行缩进 2 字符；一级标题黑体三号，二级标题楷体_GB2312三号加粗。
- 页码采用“— 1 —”样式，置于页脚中部；署名和日期使用可编辑占位符。
- 仅写已核实事实：六大模块、87 条阶段内容、121 个受检页面、大队内部使用、日常巡逻和理论学习、可视化/内容/图视频反馈闭环。
- 不写使用人数、访问量、满意度、未实施推广成效、认证摘要、口令、服务器地址、仓库信息和内部路径。
- 公开来源核验不得表述为内部发布审批。
- 最终交付前必须渲染全部页面并逐页检查；除最终 DOCX 外不向用户交付 QA 中间文件。

---

### Task 1: 建立结构验收测试

**Files:**
- Create: `.codex-doc-review/test_report.py`
- Test: `deliverables/关于巡防百科网站建设及推广应用情况的报告.docx`

**Interfaces:**
- Consumes: 最终 DOCX 路径。
- Produces: `python .codex-doc-review/test_report.py -v` 可运行的结构验收测试。

- [ ] **Step 1: 编写预期失败的测试**

测试必须读取 DOCX，断言：文件存在；标题精确匹配；八个一级部分齐全；正文包含六大模块、87 条、121 个页面、大队内部推广、日常巡逻、理论学习、反馈优化；正文不含口令、SHA、GitHub、内部盘符路径等敏感信息；A4 与四边页边距正确；正文样式字号、字体、行距和首行缩进正确；结尾包含署名、日期占位符。

```python
from pathlib import Path
import unittest
from docx import Document
from docx.shared import Mm, Pt

REPORT = Path(__file__).resolve().parents[1] / "deliverables" / "关于巡防百科网站建设及推广应用情况的报告.docx"
HEADINGS = [
    "一、项目建设背景与初衷",
    "二、总体建设思路与服务对象",
    "三、前期建设工作及阶段性成果",
    "四、建设方法与安全管理",
    "五、大队内部推广应用情况",
    "六、当前存在的不足",
    "七、下一步建设计划",
    "八、结语及有关建议",
]

class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = Document(REPORT)
        cls.text = "\n".join(p.text for p in cls.doc.paragraphs)

    def test_required_content(self):
        self.assertEqual(self.doc.paragraphs[0].text, "关于“巡防百科”网站建设及推广应用情况的报告")
        for heading in HEADINGS:
            self.assertIn(heading, self.text)
        for fact in ["六大业务模块", "87条", "121个页面", "大队内部", "日常巡逻", "理论学习", "反馈", "优化"]:
            self.assertIn(fact, self.text)

    def test_sensitive_content_absent(self):
        for forbidden in ["口令", "密码", "SHA-256", "GitHub", "F:\\", "C:\\", "index.lock"]:
            self.assertNotIn(forbidden, self.text)

    def test_page_geometry(self):
        section = self.doc.sections[0]
        self.assertAlmostEqual(section.page_width.mm, Mm(210).mm, places=1)
        self.assertAlmostEqual(section.page_height.mm, Mm(297).mm, places=1)
        for actual, expected in [(section.top_margin.mm, 37), (section.bottom_margin.mm, 35), (section.left_margin.mm, 28), (section.right_margin.mm, 26)]:
            self.assertAlmostEqual(actual, expected, places=1)

    def test_body_style(self):
        style = self.doc.styles["Normal"]
        self.assertAlmostEqual(style.font.size.pt, Pt(16).pt, places=1)
        self.assertEqual(style.font.name, "仿宋_GB2312")
        self.assertAlmostEqual(style.paragraph_format.line_spacing.pt, Pt(28).pt, places=1)

    def test_signature_placeholders(self):
        self.assertIn("（汇报人：________）", self.text)
        self.assertIn("____年__月__日", self.text)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: 运行测试并确认失败**

Run:

```powershell
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' '.codex-doc-review/test_report.py' -v
```

Expected: FAIL，原因是最终 DOCX 尚不存在。

### Task 2: 撰写正文并生成 DOCX

**Files:**
- Create: `.codex-doc-review/build_report.py`
- Create: `deliverables/关于巡防百科网站建设及推广应用情况的报告.docx`
- Test: `.codex-doc-review/test_report.py`

**Interfaces:**
- Consumes: 设计说明中的八部分结构、事实边界和版式令牌。
- Produces: `build_report(output_path: Path) -> None` 以及最终 DOCX。

- [ ] **Step 1: 实现构建脚本**

构建脚本必须包含以下明确单元：

```python
def set_run_font(run, latin: str, east_asia: str, size_pt: float, bold: bool = False): ...
def configure_page(section): ...
def configure_styles(document): ...
def add_title(document, text: str): ...
def add_body(document, text: str): ...
def add_heading(document, text: str, level: int = 1): ...
def add_numbered_points(document, items: list[str]): ...
def add_summary_table(document): ...
def add_page_number(paragraph): ...
def build_report(output_path: Path) -> None: ...
```

`build_report` 按八个部分依次写入完整正文；阶段成果表只设置“建设领域、已完成工作、实际作用”三列，内容分别覆盖内容框架、查询能力、适配验收、安全治理和推广反馈。表格宽度总和必须等于版心宽度 156 毫米，列宽为 32、58、66 毫米，不设置固定行高。

正文须把技术工具转述为“知识库归集整理、静态页面生成、站内索引、自动检查和多终端验收”，不得出现内部命令或平台凭据。最后写入“（汇报人：________）”和“____年__月__日”。

- [ ] **Step 2: 运行构建脚本**

Run:

```powershell
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' '.codex-doc-review/build_report.py'
```

Expected: 输出 `deliverables/关于巡防百科网站建设及推广应用情况的报告.docx`，程序返回码为 0。

- [ ] **Step 3: 运行结构测试**

Run:

```powershell
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' '.codex-doc-review/test_report.py' -v
```

Expected: 5 tests，全部 PASS。

### Task 3: 版式与 OOXML 审计

**Files:**
- Modify: `.codex-doc-review/build_report.py`
- Regenerate: `deliverables/关于巡防百科网站建设及推广应用情况的报告.docx`

**Interfaces:**
- Consumes: Task 2 生成的 DOCX。
- Produces: 通过样式、分节、标题和表格几何审计的 DOCX。

- [ ] **Step 1: 执行结构审计**

使用 `python-docx` 和 ZIP/XML 检查：`Normal`、一级标题、二级标题样式存在；标题字体设置包含东亚字体；A4 和页边距值写入 `sectPr`；页脚包含 `PAGE` 字段；表格 `tblW`、`tblGrid` 和每个 `tcW` 一致；全文没有假项目符号、手工页码和固定行高。

Run:

```powershell
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\97014\.codex\plugins\cache\openai-primary-runtime\documents\26.715.12143\skills\documents\scripts\table_geometry.py' 'deliverables/关于巡防百科网站建设及推广应用情况的报告.docx'
```

Expected: 程序返回码为 0，并报告所有表格的 `tblW`、`tblInd`、`tblGrid` 和 `tcW` 一致，无宽度不一致项。

- [ ] **Step 2: 修正审计发现并重新生成**

若审计指出不一致，修改对应的 `configure_styles`、`configure_page`、`add_summary_table` 或 `add_page_number`，重新运行构建脚本和全部结构测试，预期均返回 0。

### Task 4: 逐页渲染与视觉验收

**Files:**
- Create QA output: `.codex-doc-review/rendered-report/page-*.png`
- Modify when needed: `.codex-doc-review/build_report.py`
- Regenerate: `deliverables/关于巡防百科网站建设及推广应用情况的报告.docx`

**Interfaces:**
- Consumes: 审计通过的 DOCX。
- Produces: 逐页视觉检查通过的最终 DOCX。

- [ ] **Step 1: 渲染 DOCX**

Run:

```powershell
& 'C:\Users\97014\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\97014\.codex\plugins\cache\openai-primary-runtime\documents\26.715.12143\skills\documents\render_docx.py' 'deliverables/关于巡防百科网站建设及推广应用情况的报告.docx' --output_dir '.codex-doc-review/rendered-report' --emit_pdf
```

Expected: 生成连续编号的 `page-1.png` 至 `page-N.png` 和非空 PDF。

- [ ] **Step 2: 逐页检查**

逐页以 100% 比例查看，确认：标题不折行或挤压；正文无乱码、裁切或重叠；各级标题不孤悬在页尾；表格无跨页断裂、边界贴字或列宽失衡；页码居中且连续；署名和日期不单独落在空白页；全文字体替代可接受、无大面积空白。

- [ ] **Step 3: 迭代至视觉通过**

每次修正后重新运行构建、结构测试、表格审计和渲染。最终一次的所有结构测试必须 PASS，全部页面 PNG 必须重新生成并逐页复核。

### Task 5: 最终交付检查

**Files:**
- Final: `deliverables/关于巡防百科网站建设及推广应用情况的报告.docx`

**Interfaces:**
- Consumes: 最新一次通过结构和视觉检查的 DOCX。
- Produces: 只包含最终 DOCX 的用户交付结果。

- [ ] **Step 1: 检查文件与时间戳**

Run:

```powershell
Get-Item -LiteralPath 'deliverables/关于巡防百科网站建设及推广应用情况的报告.docx' | Select-Object FullName,Length,LastWriteTime
```

Expected: 文件存在、大小非零、修改时间晚于最后一次构建。

- [ ] **Step 2: 最终回归**

再次运行全部 `unittest`，确认 5 tests PASS；确认渲染页数与 PDF 页数一致；确认 DOCX 中没有未完成标记、内部路径、工具引用标记或未解释的技术命令。

- [ ] **Step 3: 交付**

最终回复只提供一条指向正式 DOCX 的本地 Markdown 链接，并简要说明报告已经完成内容、结构和逐页版式检查，不链接渲染 PNG、PDF、构建脚本或测试文件。
