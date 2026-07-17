import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_site_links", ROOT / "tools" / "check_site_links.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SiteLinkTests(unittest.TestCase):
    def test_site_has_no_broken_local_links(self):
        self.assertEqual([], MODULE.check_site(ROOT))


if __name__ == "__main__":
    unittest.main()
