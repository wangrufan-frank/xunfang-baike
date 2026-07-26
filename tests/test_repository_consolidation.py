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


class DocumentationContractTests(unittest.TestCase):
    def test_readme_describes_setup_and_public_static_site_boundaries(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for value in (
            "python -m http.server 8000",
            'python -m unittest discover -s tests -p "test_*.py" -v',
            "node --test tests/auth_core.test.js",
            "python tools/build_search_index.py --check",
            "python tools/check_site_links.py",
            "python tools/public_source_index.py check",
            "GitHub Pages",
            "CNAME",
            ".nojekyll",
            "E:\\xunfang-baike-deliverables",
            "已退役的小程序",
            "公开",
            "不是服务端访问控制",
        ):
            with self.subTest(value=value):
                self.assertIn(value, readme)

    def test_requirements_declare_tracked_python_dependency_without_pytest(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("python-docx", requirements)
        self.assertNotIn("pytest", requirements.lower())


class ContinuousIntegrationContractTests(unittest.TestCase):
    def test_workflow_runs_required_validation_on_push_and_pull_request(self):
        workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(
            encoding="utf-8"
        )
        for value in (
            "push:",
            "pull_request:",
            "actions/checkout@v6",
            "actions/setup-python@v6",
            "python-version: '3.12'",
            "actions/setup-node@v6",
            "node-version: '20'",
            'python -m unittest discover -s tests -p "test_*.py" -v',
            "node --test tests/auth_core.test.js",
            "python tools/build_search_index.py --check",
            "python tools/check_site_links.py",
            "python tools/public_source_index.py check",
        ):
            with self.subTest(value=value):
                self.assertIn(value, workflow)


if __name__ == "__main__":
    unittest.main()
