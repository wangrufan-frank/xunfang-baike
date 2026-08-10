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
            for insertion_point in page["insertion_points"]:
                self.assertTrue(
                    any(insertion_point in html[max(0, position - 2500):position] for position in image_positions),
                    f"{page['path']}: insertion point is not near an image: {insertion_point}",
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
