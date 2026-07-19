from pathlib import Path
import re
import unittest

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.shared import Mm, Pt


REPORT = (
    Path(__file__).resolve().parents[1]
    / "deliverables"
    / "关于巡防百科网站建设及推广应用情况的报告.docx"
)
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

    def all_document_paragraphs(self):
        for paragraph in self.doc.paragraphs:
            yield paragraph
        for table in self.doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    yield from cell.paragraphs
        for section in self.doc.sections:
            for container in (section.header, section.footer):
                yield from container.paragraphs
                for table in container.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            yield from cell.paragraphs

    def paragraph_for(self, text):
        return next(paragraph for paragraph in self.doc.paragraphs if paragraph.text == text)

    def assert_font(self, paragraph, names, size, bold=None):
        run = next(run for run in paragraph.runs if run.text.strip())
        self.assertIn(run.font.name, names)
        self.assertAlmostEqual(run.font.size.pt, size, places=1)
        if bold is not None:
            self.assertEqual(run.bold, bold)

    def test_required_content(self):
        self.assertEqual(
            self.doc.paragraphs[0].text,
            "关于“巡防百科”网站建设及推广应用情况的报告",
        )
        for heading in HEADINGS:
            self.assertIn(heading, self.text)
        for fact in [
            "六大业务模块",
            "87条",
            "121个页面",
            "大队内部",
            "日常巡逻",
            "理论学习",
            "反馈",
            "优化",
        ]:
            self.assertIn(fact, self.text)

    def test_sensitive_content_absent(self):
        content = "\n".join(paragraph.text for paragraph in self.all_document_paragraphs())
        for forbidden in [
            "口令",
            "密码",
            "SHA-256",
            "SHA-1",
            "SHA-512",
            "MD5",
            "哈希",
            "摘要",
            "Token",
            "token",
            "令牌",
            "Bearer",
            "API Key",
            "API密钥",
            "GitHub",
            "GitLab",
            "仓库",
            "repository",
            "服务器地址",
            "服务器IP",
            "localhost",
            "http://",
            "https://",
            "index.lock",
            "F:\\",
            "C:\\",
            "\\\\",
        ]:
            self.assertNotIn(forbidden, content)
        self.assertIsNone(
            re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", content),
            "report must not disclose a server IP address",
        )

    def test_page_geometry(self):
        for section in self.doc.sections:
            self.assertAlmostEqual(section.page_width.mm, Mm(210).mm, places=1)
            self.assertAlmostEqual(section.page_height.mm, Mm(297).mm, places=1)
            for actual, expected in [
                (section.top_margin.mm, 37),
                (section.bottom_margin.mm, 35),
                (section.left_margin.mm, 28),
                (section.right_margin.mm, 26),
            ]:
                self.assertAlmostEqual(actual, expected, places=1)

    def test_title_and_heading_formatting(self):
        title = self.doc.paragraphs[0]
        self.assertEqual(title.alignment, WD_ALIGN_PARAGRAPH.CENTER)
        self.assert_font(title, ["方正小标宋简体", "小标宋", "宋体"], 22)
        self.assert_font(
            self.paragraph_for(HEADINGS[0]), ["黑体"], 16, bold=False
        )
        h2 = next(
            paragraph
            for paragraph in self.doc.paragraphs
            if paragraph.text.startswith("（一）")
        )
        self.assert_font(h2, ["楷体_GB2312"], 16, bold=True)

    def test_body_paragraph_formatting(self):
        style = self.doc.styles["Normal"]
        self.assertAlmostEqual(style.font.size.pt, Pt(16).pt, places=1)
        self.assertEqual(style.font.name, "仿宋_GB2312")
        self.assertAlmostEqual(style.paragraph_format.line_spacing.pt, Pt(28).pt, places=1)
        body = next(
            paragraph
            for paragraph in self.doc.paragraphs
            if paragraph.text
            and paragraph.style.name == "Normal"
            and not paragraph.text.startswith("（汇报人：")
            and not paragraph.text.startswith("____年")
        )
        self.assertEqual(body.alignment, WD_ALIGN_PARAGRAPH.JUSTIFY)
        self.assert_font(body, ["仿宋_GB2312"], 16)
        self.assertEqual(body.paragraph_format.line_spacing_rule, WD_LINE_SPACING.EXACTLY)
        self.assertAlmostEqual(body.paragraph_format.line_spacing.pt, Pt(28).pt, places=1)
        self.assertAlmostEqual(body.paragraph_format.first_line_indent.pt, Pt(32).pt, places=1)

    def test_footer_page_number_formatting(self):
        for section in self.doc.sections:
            footer = section.footer.paragraphs[0]
            self.assertEqual(footer.alignment, WD_ALIGN_PARAGRAPH.CENTER)
            self.assertTrue(footer.text.startswith("— "))
            self.assertTrue(footer.text.endswith(" —"))
            self.assertIn("PAGE", footer._p.xml)

    def test_signature_placeholders(self):
        self.assertIn("（汇报人：________）", self.text)
        self.assertIn("____年__月__日", self.text)


if __name__ == "__main__":
    unittest.main()
