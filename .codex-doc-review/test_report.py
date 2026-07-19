from pathlib import Path
import unittest

from docx import Document
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
        for forbidden in ["口令", "密码", "SHA-256", "GitHub", "F:\\", "C:\\", "index.lock"]:
            self.assertNotIn(forbidden, self.text)

    def test_page_geometry(self):
        section = self.doc.sections[0]
        self.assertAlmostEqual(section.page_width.mm, Mm(210).mm, places=1)
        self.assertAlmostEqual(section.page_height.mm, Mm(297).mm, places=1)
        for actual, expected in [
            (section.top_margin.mm, 37),
            (section.bottom_margin.mm, 35),
            (section.left_margin.mm, 28),
            (section.right_margin.mm, 26),
        ]:
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
