import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RuntimeTreeContractTests(unittest.TestCase):
    def test_generated_output_directories_are_absent(self):
        self.assertFalse((ROOT / "deliverables").exists())
        self.assertFalse((ROOT / "video").exists())

    def test_report_source_inputs_live_under_data(self):
        self.assertTrue((ROOT / "data" / "xunfang-report-speaker-notes.json").is_file())
        self.assertTrue((ROOT / "data" / "project-report-assets").is_dir())

    def test_archive_restore_document_and_manifest_exist(self):
        self.assertTrue((ROOT / "docs" / "deliverables-archive.md").is_file())
        self.assertTrue(
            (ROOT / "docs" / "deliverables-archive-manifest.tsv").is_file()
        )


if __name__ == "__main__":
    unittest.main()
