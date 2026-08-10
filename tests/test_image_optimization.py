import json
import re
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from tools.check_image_optimization import validate_plan, validate_runtime

ROOT = Path(__file__).resolve().parents[1]

REPRESENTATIVE_SVGS = (
    "img/learning/zhuangbei/zhifa-jiuyi-structure.svg",
    "img/learning/xunlian/geren-fanghu-anquan-checklist.svg",
    "img/learning/jingqing/zuijiu-lei-chuzhi-flow.svg",
    "img/learning/qinwu/gonggong-zhixu-goutong-record.svg",
    "img/learning/fagui/panwen-shenfenzheng-procedure.svg",
    "img/learning/zoufang/changsuo-aed-jiancha.svg",
)

NEW_EQUIPMENT_SVGS = (
    "img/learning/zhuangbei/5g-yuntai-structure-label.svg",
    "img/learning/zhuangbei/bidun-structure-label.svg",
    "img/learning/zhuangbei/changgun-structure-label.svg",
    "img/learning/zhuangbei/fangci-fu-structure-label.svg",
    "img/learning/zhuangbei/pochai-gongju-structure-label.svg",
    "img/learning/zhuangbei/sanshi-weidang-structure-label.svg",
    "img/learning/zhuangbei/shuishang-feiyi-structure-label.svg",
    "img/learning/zhuangbei/t-zi-gun-structure-label.svg",
    "img/learning/zhuangbei/yueshu-dai-structure-label.svg",
    "img/learning/zhuangbei/zhedieshi-weidang-structure-label.svg",
    "img/learning/zhuangbei/zuche-ding-structure-label.svg",
)

NEW_TRAINING_SVGS = (
    "img/learning/xunlian/jietuo-kongzhi-jichu-step-flow.svg",
    "img/learning/xunlian/xiaozu-biancheng-fengong-step-flow.svg",
    "img/learning/xunlian/yidong-yanhu-daili-step-flow.svg",
    "img/learning/xunlian/xianchang-goutong-yingxiang-step-flow.svg",
    "img/learning/xunlian/xunlian-fupan-kaoping-step-flow.svg",
    "img/learning/xunlian/zhixue-baozha-banyun-step-flow.svg",
)

JINGQING_SVGS = (
    "img/learning/jingqing/zuijiu-lei-chuzhi-flow.svg",
    "img/learning/jingqing/chidao-lei-step-flow.svg",
    "img/learning/jingqing/zishang-lei-step-flow.svg",
    "img/learning/jingqing/jingshen-zhangai-lei-step-flow.svg",
    "img/learning/jingqing/shebao-lei-step-flow.svg",
    "img/learning/jingqing/jiuzhu-lei-jingqing-chuzhi-step-flow.svg",
)

NEW_QINWU_SVGS = (
    "img/learning/qinwu/zuqiu-saishi-anbao-scene-zone.svg",
    "img/learning/qinwu/daxing-shiwai-yanchanghui-scene-zone.svg",
    "img/learning/qinwu/xiaoxing-shinei-yanchu-scene-zone.svg",
    "img/learning/qinwu/gonggong-zhixu-chuzhi-yuanze-scene-zone.svg",
    "img/learning/qinwu/gonggong-zhixu-falv-quanli-scene-zone.svg",
    "img/learning/qinwu/xiaoqu-zhidian-zoufang-scene-zone.svg",
    "img/learning/qinwu/xuexiao-zhidian-zoufang-scene-zone.svg",
    "img/learning/qinwu/yinhang-zhidian-zoufang-scene-zone.svg",
    "img/learning/qinwu/shangchang-zhidian-zoufang-scene-zone.svg",
    "img/learning/qinwu/zhuanxiang-huodong-gailan-scene-zone.svg",
    "img/learning/qinwu/zhuanxiang-xianchang-zhixu-scene-zone.svg",
    "img/learning/qinwu/zhuanxiang-xietong-baogao-scene-zone.svg",
)

FAGUI_SVGS = (
    "img/learning/fagui/shenfen-mudi-shuoming-learning-map.svg",
    "img/learning/fagui/pancha-guifan-goutong-learning-map.svg",
    "img/learning/fagui/zhiyi-yifa-huiying-learning-map.svg",
    "img/learning/fagui/weiguan-paishe-zhixu-learning-map.svg",
    "img/learning/fagui/quanli-yiwu-gaozhi-learning-map.svg",
    "img/learning/fagui/panwen-shenfenzheng-learning-map.svg",
    "img/learning/fagui/chuanhuan-qiangzhi-chuanhuan-learning-map.svg",
    "img/learning/fagui/jingxie-shiyong-chengxu-learning-map.svg",
    "img/learning/fagui/xingzheng-anji-tiaocha-learning-map.svg",
    "img/learning/fagui/zhifa-jilu-quanli-learning-map.svg",
    "img/learning/fagui/zhian-guanli-chufa-fa-learning-map.svg",
    "img/learning/fagui/renmin-jingcha-fa-learning-map.svg",
    "img/learning/fagui/jumin-shenfenzheng-fa-learning-map.svg",
    "img/learning/fagui/xingzheng-anji-chengxu-guiding-learning-map.svg",
    "img/learning/fagui/jingxie-wuqi-tiaoli-learning-map.svg",
    "img/learning/fagui/xianchang-zhizhi-guicheng-learning-map.svg",
    "img/learning/fagui/qita-xiangguan-guifan-learning-map.svg",
)

RETAINED_EQUIPMENT_IMAGE_PAGES = (
    "zhuangbei/jiuxiaojian-gailan.html",
    "zhuangbei/fangge-shoutao.html",
    "zhuangbei/zhifa-jiuyi.html",
    "zhuangbei/duijiang-diantai.html",
    "zhuangbei/miehuo-tan.html",
    "zhuangbei/miehuo-qi.html",
    "zhuangbei/fanguang-zhuitong.html",
    "zhuangbei/jiusheng-quan.html",
    "zhuangbei/jiusheng-yi.html",
    "zhuangbei/jiusheng-sheng.html",
    "zhuangbei/fangbao-toukui.html",
    "zhuangbei/zhuabu-cha.html",
    "zhuangbei/jingjiedai-jinggaopai.html",
    "zhuangbei/fashi-dunpai.html",
    "zhuangbei/qiangguang-shoudian.html",
    "zhuangbei/jijiu-bao.html",
    "zhuangbei/aed-shiyong.html",
)

class ImageOptimizationPlanTests(unittest.TestCase):
    def test_representative_svgs_use_explicit_light_text_class(self):
        for relative_path in REPRESENTATIVE_SVGS:
            svg = (ROOT / relative_path).read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            text_nodes = [node for node in root.iter() if node.tag.endswith("text")]
            self.assertIn(".light", svg, relative_path)
            self.assertIn("light", (text_nodes[0].get("class") or "").split(), relative_path)
            for node in text_nodes:
                self.assertNotEqual("#fff", node.get("fill"), relative_path)
                if (node.text or "").strip() in {"1", "2", "3", "4", "5"}:
                    classes = (node.get("class") or "").split()
                    self.assertTrue({"light", "dark"}.intersection(classes), relative_path)

    def test_representative_svgs_have_readable_mobile_layer(self):
        for relative_path in REPRESENTATIVE_SVGS:
            root = ET.parse(ROOT / relative_path).getroot()
            mobile_groups = [
                node
                for node in root.iter()
                if node.tag.endswith("g") and "mobile" in (node.get("class") or "").split()
            ]
            self.assertEqual(1, len(mobile_groups), relative_path)
            mobile_text = [node for node in mobile_groups[0].iter() if node.tag.endswith("text")]
            self.assertTrue(mobile_text, relative_path)
            for node in mobile_text:
                self.assertGreaterEqual(float(node.get("font-size", "0")), 25, relative_path)

    def test_new_equipment_svgs_use_explicit_contrast_classes(self):
        for relative_path in NEW_EQUIPMENT_SVGS:
            svg = (ROOT / relative_path).read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            text_nodes = [node for node in root.iter() if node.tag.endswith("text")]
            self.assertIn(".light", svg, relative_path)
            self.assertIn(".dark", svg, relative_path)
            self.assertIn("light", (text_nodes[0].get("class") or "").split(), relative_path)
            for node in text_nodes:
                self.assertNotEqual("#fff", node.get("fill"), relative_path)

    def test_new_equipment_svgs_have_readable_mobile_layer(self):
        for relative_path in NEW_EQUIPMENT_SVGS:
            root = ET.parse(ROOT / relative_path).getroot()
            mobile_groups = [
                node
                for node in root.iter()
                if node.tag.endswith("g") and "mobile" in (node.get("class") or "").split()
            ]
            self.assertEqual(1, len(mobile_groups), relative_path)
            mobile_text = [node for node in mobile_groups[0].iter() if node.tag.endswith("text")]
            self.assertTrue(mobile_text, relative_path)
            for node in mobile_text:
                self.assertGreaterEqual(float(node.get("font-size", "0")), 25, relative_path)

    def test_new_equipment_svgs_are_self_contained_accessible_documents(self):
        for relative_path in NEW_EQUIPMENT_SVGS:
            svg = (ROOT / relative_path).read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertTrue(root.get("viewBox"), relative_path)
            self.assertTrue(any(node.tag.endswith("title") for node in root), relative_path)
            self.assertTrue(any(node.tag.endswith("desc") for node in root), relative_path)
            self.assertNotIn("http://", svg, relative_path)
            self.assertNotIn("https://", svg, relative_path)
            self.assertNotIn("href=", svg, relative_path)

    def test_new_training_svgs_are_self_contained_accessible_documents(self):
        for relative_path in NEW_TRAINING_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertTrue(root.get("viewBox"), relative_path)
            self.assertTrue(any(node.tag.endswith("title") for node in root), relative_path)
            self.assertTrue(any(node.tag.endswith("desc") for node in root), relative_path)
            self.assertNotIn("http://", svg, relative_path)
            self.assertNotIn("https://", svg, relative_path)
            self.assertNotIn("href=", svg, relative_path)

    def test_new_training_svgs_use_explicit_contrast_classes(self):
        for relative_path in NEW_TRAINING_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertIn(".light", svg, relative_path)
            self.assertIn(".dark", svg, relative_path)
            for node in (item for item in root.iter() if item.tag.endswith("text")):
                classes = (node.get("class") or "").split()
                self.assertTrue({"light", "dark"}.intersection(classes), relative_path)

    def test_new_training_svgs_have_readable_mobile_reflow(self):
        for relative_path in NEW_TRAINING_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertIn("@media (max-width:500px)", svg, relative_path)
            mobile_groups = [
                node
                for node in root.iter()
                if node.tag.endswith("g") and "mobile" in (node.get("class") or "").split()
            ]
            self.assertEqual(1, len(mobile_groups), relative_path)
            mobile_text = [node for node in mobile_groups[0].iter() if node.tag.endswith("text")]
            self.assertTrue(mobile_text, relative_path)
            for node in mobile_text:
                self.assertGreaterEqual(float(node.get("font-size", "0")), 25, relative_path)

    def test_jingqing_svgs_are_self_contained_accessible_documents(self):
        for relative_path in JINGQING_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertTrue(root.get("viewBox"), relative_path)
            self.assertTrue(any(node.tag.endswith("title") for node in root), relative_path)
            self.assertTrue(any(node.tag.endswith("desc") for node in root), relative_path)
            self.assertNotIn("http://", svg, relative_path)
            self.assertNotIn("https://", svg, relative_path)
            self.assertNotIn("href=", svg, relative_path)

    def test_jingqing_svgs_use_explicit_contrast_classes(self):
        for relative_path in JINGQING_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertIn(".light", svg, relative_path)
            self.assertIn(".dark", svg, relative_path)
            for node in (item for item in root.iter() if item.tag.endswith("text")):
                classes = (node.get("class") or "").split()
                self.assertTrue({"light", "dark"}.intersection(classes), relative_path)

    def test_jingqing_svgs_have_readable_mobile_reflow(self):
        for relative_path in JINGQING_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertIn("@media (max-width:500px)", svg, relative_path)
            mobile_groups = [
                node
                for node in root.iter()
                if node.tag.endswith("g") and "mobile" in (node.get("class") or "").split()
            ]
            self.assertEqual(1, len(mobile_groups), relative_path)
            mobile_text = [node for node in mobile_groups[0].iter() if node.tag.endswith("text")]
            self.assertTrue(mobile_text, relative_path)
            for node in mobile_text:
                self.assertGreaterEqual(float(node.get("font-size", "0")), 25, relative_path)

    def test_qinwu_svgs_are_self_contained_accessible_documents(self):
        for relative_path in NEW_QINWU_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertTrue(root.get("viewBox"), relative_path)
            self.assertTrue(any(node.tag.endswith("title") for node in root), relative_path)
            self.assertTrue(any(node.tag.endswith("desc") for node in root), relative_path)
            self.assertNotIn("http://", svg, relative_path)
            self.assertNotIn("https://", svg, relative_path)
            self.assertNotIn("href=", svg, relative_path)
            self.assertNotIn("?", svg, f"{relative_path}: replacement character leaked into SVG text")
            self.assertNotIn("\\n", svg, f"{relative_path}: literal newline escape leaked into SVG markup")

    def test_qinwu_svgs_use_explicit_contrast_classes(self):
        for relative_path in NEW_QINWU_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertIn(".light", svg, relative_path)
            self.assertIn(".dark", svg, relative_path)
            for node in (item for item in root.iter() if item.tag.endswith("text")):
                classes = (node.get("class") or "").split()
                self.assertTrue({"light", "dark"}.intersection(classes), relative_path)

    def test_qinwu_svgs_have_readable_mobile_reflow(self):
        for relative_path in NEW_QINWU_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertIn("@media (max-width:500px)", svg, relative_path)
            mobile_groups = [
                node
                for node in root.iter()
                if node.tag.endswith("g") and "mobile" in (node.get("class") or "").split()
            ]
            self.assertEqual(1, len(mobile_groups), relative_path)
            mobile_text = [node for node in mobile_groups[0].iter() if node.tag.endswith("text")]
            self.assertTrue(mobile_text, relative_path)
            for node in mobile_text:
                self.assertGreaterEqual(float(node.get("font-size", "0")), 25, relative_path)
                text = (node.text or "").strip()
                if node.get("x") == "24":
                    self.assertLessEqual(len(text), 15, f"{relative_path}: mobile card line is too long")
                if node.get("x") == "50" and node.get("font-size") == "25":
                    self.assertLessEqual(len(text), 30, f"{relative_path}: mobile alert line is too long")

    def test_qinwu_desktop_card_body_lines_fit_their_cards(self):
        for relative_path in NEW_QINWU_SVGS:
            root = ET.parse(ROOT / relative_path).getroot()
            desktop_groups = [
                node
                for node in root.iter()
                if node.tag.endswith("g") and "desktop" in (node.get("class") or "").split()
            ]
            self.assertEqual(1, len(desktop_groups), relative_path)
            body_lines = [
                node
                for node in desktop_groups[0].iter()
                if node.tag.endswith("text")
                and node.get("x") == "18"
                and node.get("font-size") == "15"
            ]
            self.assertTrue(body_lines, relative_path)
            for node in body_lines:
                self.assertLessEqual(
                    len((node.text or "").strip()),
                    11,
                    f"{relative_path}: desktop card body line is too long",
                )

    def test_fagui_svgs_are_self_contained_accessible_documents(self):
        for relative_path in FAGUI_SVGS:
            path = ROOT / relative_path
            self.assertTrue(path.exists(), relative_path)
            svg = path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertTrue(root.get("viewBox"), relative_path)
            self.assertTrue(any(node.tag.endswith("title") for node in root), relative_path)
            self.assertTrue(any(node.tag.endswith("desc") for node in root), relative_path)
            self.assertNotIn("http://", svg, relative_path)
            self.assertNotIn("https://", svg, relative_path)
            self.assertNotIn("href=", svg, relative_path)
            self.assertNotIn("?", svg, f"{relative_path}: replacement character leaked into SVG text")
            self.assertNotIn("\\n", svg, f"{relative_path}: literal newline escape leaked into SVG markup")

    def test_fagui_svgs_use_explicit_contrast_classes(self):
        for relative_path in FAGUI_SVGS:
            svg = (ROOT / relative_path).read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertIn(".light", svg, relative_path)
            self.assertIn(".dark", svg, relative_path)
            for node in (item for item in root.iter() if item.tag.endswith("text")):
                classes = (node.get("class") or "").split()
                self.assertTrue({"light", "dark"}.intersection(classes), relative_path)

    def test_fagui_svgs_have_readable_mobile_reflow(self):
        for relative_path in FAGUI_SVGS:
            svg = (ROOT / relative_path).read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            self.assertIn("@media (max-width:500px)", svg, relative_path)
            mobile_groups = [
                node
                for node in root.iter()
                if node.tag.endswith("g") and "mobile" in (node.get("class") or "").split()
            ]
            self.assertEqual(1, len(mobile_groups), relative_path)
            mobile_text = [node for node in mobile_groups[0].iter() if node.tag.endswith("text")]
            self.assertTrue(mobile_text, relative_path)
            for node in mobile_text:
                self.assertGreaterEqual(float(node.get("font-size", "0")), 25, relative_path)
                if node.get("x") == "24":
                    self.assertLessEqual(len((node.text or "").strip()), 12, relative_path)

    def test_fagui_desktop_card_body_lines_fit_their_cards(self):
        for relative_path in FAGUI_SVGS:
            root = ET.parse(ROOT / relative_path).getroot()
            desktop_groups = [
                node
                for node in root.iter()
                if node.tag.endswith("g") and "desktop" in (node.get("class") or "").split()
            ]
            self.assertEqual(1, len(desktop_groups), relative_path)
            body_lines = [
                node
                for node in desktop_groups[0].iter()
                if node.tag.endswith("text") and node.get("data-role") == "body"
            ]
            self.assertEqual(8, len(body_lines), relative_path)
            for node in body_lines:
                self.assertLessEqual(len((node.text or "").strip()), 8, relative_path)

    def test_fagui_reviewed_semantics_match_the_page_scope(self):
        inventory = json.loads((ROOT / "data/content-inventory.json").read_text(encoding="utf-8"))
        plan = json.loads((ROOT / "data/image-optimization-plan.json").read_text(encoding="utf-8"))
        articles = {
            article["path"]: article
            for module in inventory["modules"]
            for article in module["articles"]
        }
        planned = {page["path"]: page for page in plan["pages"]}
        cases = {
            "fagui/xianchang-zhizhi-guicheng.html": {
                "required": ("持续风险评估", "紧急例外", "停止使用并及时救助"),
                "forbidden": ("停止救助", "措施逐级衔接"),
            },
            "fagui/jingxie-wuqi-tiaoli.html": {
                "required": ("总则原则", "警械使用", "武器使用", "法律责任"),
                "forbidden": ("配备保管",),
            },
            "fagui/xingzheng-anji-chengxu-guiding.html": {
                "required": ("传唤", "个别询问", "证据收集核实", "全过程记录归档"),
                "forbidden": ("受案管辖", "决定执行", "监督救济"),
            },
            "fagui/qita-xiangguan-guifan.html": {
                "required": ("法规正文待补充", "主题范围", "来源核验", "不作程序推断"),
                "forbidden": ("任务准备", "巡逻防控", "安保处置", "复盘归档"),
            },
        }
        for page_path, terms in cases.items():
            page = planned[page_path]
            asset_text = (ROOT / page["assets"][0]["path"]).read_text(encoding="utf-8")
            html = (ROOT / page_path).read_text(encoding="utf-8")
            metadata = json.dumps(
                {"article": articles[page_path]["images"], "plan": page},
                ensure_ascii=False,
            )
            combined = "\n".join((asset_text, html, metadata))
            for term in terms["required"]:
                self.assertIn(term, combined, f"{page_path}: missing reviewed term {term}")
            for term in terms["forbidden"]:
                self.assertNotIn(term, combined, f"{page_path}: stale unsupported term {term}")

    def test_special_event_order_figure_consistently_describes_four_zones(self):
        page_path = "qinwu/zhuanxiang-xianchang-zhixu.html"
        asset_path = "img/learning/qinwu/zhuanxiang-xianchang-zhixu-scene-zone.svg"
        svg = (ROOT / asset_path).read_text(encoding="utf-8")
        html = (ROOT / page_path).read_text(encoding="utf-8")
        inventory = json.loads((ROOT / "data/content-inventory.json").read_text(encoding="utf-8"))
        plan = json.loads((ROOT / "data/image-optimization-plan.json").read_text(encoding="utf-8"))
        article = next(
            article
            for module in inventory["modules"]
            for article in module["articles"]
            if article["path"] == page_path
        )
        record = next(page for page in plan["pages"] if page["path"] == page_path)
        self.assertNotIn("三区", svg)
        self.assertGreaterEqual(svg.count("四区保畅"), 4)
        self.assertIn("四区保畅", html)
        self.assertTrue(all("四区" in image[field] for image in article["images"] for field in ("alt", "caption")))
        self.assertNotIn("三区", record["reason"])
        self.assertIn("四区", record["assets"][0]["purpose"])

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

    def test_equipment_image_optimization_is_complete(self):
        self.assertEqual(
            [],
            validate_runtime(ROOT, module="zhuangbei", require_complete=True),
        )

    def test_training_image_optimization_is_complete(self):
        self.assertEqual(
            [],
            validate_runtime(ROOT, module="xunlian", require_complete=True),
        )

    def test_incident_image_optimization_is_complete(self):
        self.assertEqual(
            [],
            validate_runtime(ROOT, module="jingqing", require_complete=True),
        )

    def test_public_security_duty_image_optimization_is_complete(self):
        self.assertEqual(
            [],
            validate_runtime(ROOT, module="qinwu", require_complete=True),
        )

    def test_law_and_procedure_image_optimization_is_complete(self):
        self.assertEqual(
            [],
            validate_runtime(ROOT, module="fagui", require_complete=True),
        )

    def test_retained_equipment_image_insertion_points_match_nearby_body_text(self):
        plan = json.loads((ROOT / "data/image-optimization-plan.json").read_text(encoding="utf-8"))
        by_path = {page["path"]: page for page in plan["pages"]}
        for path in RETAINED_EQUIPMENT_IMAGE_PAGES:
            html = (ROOT / path).read_text(encoding="utf-8")
            image_positions = [match.start() for match in re.finditer(r"<img\b", html)]
            self.assertTrue(image_positions, path)
            for insertion_point in by_path[path]["insertion_points"]:
                self.assertTrue(
                    any(insertion_point in html[max(0, position - 2500):position] for position in image_positions),
                    f"{path}: insertion point is not near a retained image: {insertion_point}",
                )

    def test_every_training_image_insertion_point_matches_nearby_body_text(self):
        plan = json.loads((ROOT / "data/image-optimization-plan.json").read_text(encoding="utf-8"))
        training_pages = [page for page in plan["pages"] if page["path"].startswith("xunlian/")]
        self.assertEqual(15, len(training_pages))
        for page in training_pages:
            html = (ROOT / page["path"]).read_text(encoding="utf-8")
            image_positions = [match.start() for match in re.finditer(r"<img\b", html)]
            self.assertTrue(image_positions, page["path"])
            planned_positions = []
            for asset in page["assets"]:
                asset_position = html.find(asset["path"])
                self.assertNotEqual(-1, asset_position, f"{page['path']}: {asset['path']}")
                planned_positions.append(html.rfind("<img", 0, asset_position))
            target_positions = planned_positions or image_positions
            for insertion_point in page["insertion_points"]:
                preceding_distances = [
                    position - html.rfind(insertion_point, 0, position)
                    for position in target_positions
                    if html.rfind(insertion_point, 0, position) >= 0
                ]
                self.assertTrue(
                    preceding_distances and min(preceding_distances) <= 2500,
                    f"{page['path']}: insertion point is not bound to its figure: {insertion_point}",
                )

    def test_every_jingqing_image_insertion_point_matches_nearby_body_text(self):
        plan = json.loads((ROOT / "data/image-optimization-plan.json").read_text(encoding="utf-8"))
        incident_pages = [page for page in plan["pages"] if page["path"].startswith("jingqing/")]
        self.assertEqual(6, len(incident_pages))
        for page in incident_pages:
            html = (ROOT / page["path"]).read_text(encoding="utf-8")
            for asset in page["assets"]:
                asset_position = html.find(asset["path"])
                self.assertNotEqual(-1, asset_position, f"{page['path']}: {asset['path']}")
                image_position = html.rfind("<img", 0, asset_position)
                for insertion_point in page["insertion_points"]:
                    body_position = html.rfind(insertion_point, 0, image_position)
                    self.assertGreaterEqual(body_position, 0, f"{page['path']}: {insertion_point}")
                    self.assertLessEqual(
                        image_position - body_position,
                        2500,
                        f"{page['path']}: insertion point is not bound to its figure: {insertion_point}",
                    )

    def test_every_qinwu_image_insertion_point_matches_nearby_body_text(self):
        plan = json.loads((ROOT / "data/image-optimization-plan.json").read_text(encoding="utf-8"))
        duty_pages = [page for page in plan["pages"] if page["path"].startswith("qinwu/")]
        self.assertEqual(13, len(duty_pages))
        for page in duty_pages:
            html = (ROOT / page["path"]).read_text(encoding="utf-8")
            for asset in page["assets"]:
                asset_position = html.find(asset["path"])
                self.assertNotEqual(-1, asset_position, f"{page['path']}: {asset['path']}")
                image_position = html.rfind("<img", 0, asset_position)
                for insertion_point in page["insertion_points"]:
                    body_position = html.rfind(insertion_point, 0, image_position)
                    self.assertGreaterEqual(body_position, 0, f"{page['path']}: {insertion_point}")
                    self.assertLessEqual(
                        image_position - body_position,
                        2500,
                        f"{page['path']}: insertion point is not bound to its figure: {insertion_point}",
                    )

    def test_every_fagui_image_insertion_point_matches_nearby_body_text(self):
        plan = json.loads((ROOT / "data/image-optimization-plan.json").read_text(encoding="utf-8"))
        law_pages = [page for page in plan["pages"] if page["path"].startswith("fagui/")]
        self.assertEqual(17, len(law_pages))
        for page in law_pages:
            html = (ROOT / page["path"]).read_text(encoding="utf-8")
            self.assertEqual(1, len(page["assets"]), page["path"])
            asset_position = html.find(page["assets"][0]["path"])
            self.assertNotEqual(-1, asset_position, f"{page['path']}: {page['assets'][0]['path']}")
            image_position = html.rfind("<img", 0, asset_position)
            for insertion_point in page["insertion_points"]:
                body_position = html.rfind(insertion_point, 0, image_position)
                self.assertGreaterEqual(body_position, 0, f"{page['path']}: {insertion_point}")
                self.assertLessEqual(
                    image_position - body_position,
                    2500,
                    f"{page['path']}: insertion point is not bound to its figure: {insertion_point}",
                )

    def test_plan_rejects_wrong_current_image_count(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "data", root / "data")
            plan_path = root / "data/image-optimization-plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            page = plan["pages"][0]
            page["current_images"] = 99
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            (root / page["path"]).parent.mkdir(parents=True)
            shutil.copy(ROOT / page["path"], root / page["path"])
            self.assertTrue(any("current_images" in error for error in validate_plan(root)))

    def test_module_filter_cannot_hide_inventory_module_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "data", root / "data")
            shutil.copytree(ROOT / "zhuangbei", root / "zhuangbei")
            shutil.copytree(ROOT / "img/learning/zhuangbei", root / "img/learning/zhuangbei")
            plan_path = root / "data/image-optimization-plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            page = next(item for item in plan["pages"] if item["path"] == "zhuangbei/zuche-ding.html")
            page["module"] = "qinwu"
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            expected_error = "zhuangbei/zuche-ding.html: module does not match inventory"
            self.assertIn(expected_error, validate_plan(root, module="zhuangbei", require_complete=True))
            self.assertIn(expected_error, validate_runtime(root, module="zhuangbei", require_complete=True))

    def test_plan_rejects_external_asset_without_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "data", root / "data")
            plan_path = root / "data/image-optimization-plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            asset = next(page["assets"][0] for page in plan["pages"] if page["assets"])
            asset.update({"source_status": "external", "source_url": "", "publisher": "", "accessed_at": "bad", "license": ""})
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            self.assertTrue(any("external asset" in error for error in validate_plan(root)))

    def test_plan_rejects_external_url_without_hostname(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "data", root / "data")
            plan_path = root / "data/image-optimization-plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            asset = next(page["assets"][0] for page in plan["pages"] if page["assets"])
            asset.update({"source_status": "external", "source_url": "https://", "publisher": "source", "accessed_at": "2026-08-10", "license": "CC-BY"})
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            self.assertTrue(any("external asset" in error for error in validate_plan(root)))

    def test_plan_rejects_external_url_with_malformed_netloc(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "data", root / "data")
            plan_path = root / "data/image-optimization-plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            asset = next(page["assets"][0] for page in plan["pages"] if page["assets"])
            asset.update({"source_status": "external", "source_url": "http://[", "publisher": "source", "accessed_at": "2026-08-10", "license": "CC-BY"})
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            self.assertTrue(any("external asset" in error for error in validate_plan(root)))

    def test_validators_report_malformed_path_without_crashing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "data", root / "data")
            plan_path = root / "data/image-optimization-plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["pages"][0]["path"] = None
            plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            self.assertTrue(validate_plan(root))
            self.assertTrue(validate_runtime(root))
