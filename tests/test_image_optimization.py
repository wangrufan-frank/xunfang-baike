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
