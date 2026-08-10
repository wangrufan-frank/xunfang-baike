import json
import shutil
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
