import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.git', '.worktrees', '.superpowers', 'deliverables', 'docs'}
INJECTOR_PATH = ROOT / 'tools' / 'inject_auth_guard.py'


def runtime_html_pages():
    return sorted(
        path
        for path in ROOT.rglob('*.html')
        if not any(part in EXCLUDED_DIRS for part in path.relative_to(ROOT).parts)
    )


def load_injector():
    if not INJECTOR_PATH.exists():
        raise AssertionError(f'missing injector: {INJECTOR_PATH}')
    spec = importlib.util.spec_from_file_location('inject_auth_guard', INJECTOR_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuthIntegrationTests(unittest.TestCase):
    def test_every_runtime_page_except_auth_loads_guard_in_head(self):
        for page in runtime_html_pages():
            if page.name == 'auth.html' and page.parent == ROOT:
                continue
            html = page.read_text(encoding='utf-8')
            head = html.split('</head>', 1)[0]
            self.assertIn('auth-config.js', head, page)
            self.assertIn('auth-core.js', head, page)
            self.assertIn('auth-guard.js', head, page)

    def test_auth_page_has_accessible_account_password_controls(self):
        html = (ROOT / 'auth.html').read_text(encoding='utf-8')
        for value in ('id="username"', 'id="password"', 'id="toggle-password"',
                      'id="submit"', 'aria-live="polite"', 'js/auth-page.js'):
            self.assertIn(value, html)

    def test_plaintext_password_is_absent_from_new_runtime_sources(self):
        for path in [ROOT / 'js' / name for name in
                     ('auth-config.js', 'auth-core.js', 'auth-guard.js', 'auth-page.js')]:
            self.assertNotIn('150225', path.read_text(encoding='utf-8'))

    def test_inject_html_uses_root_prefix_and_is_idempotent(self):
        injector = load_injector()
        original = '<!doctype html>\n<html><head><title>T</title></head><body></body></html>\n'
        root_html = injector.inject_html(original, '')
        self.assertIn('src="js/auth-config.js"', root_html)
        self.assertIn('src="js/auth-core.js"', root_html)
        self.assertIn('src="js/auth-guard.js" data-root=""', root_html)
        self.assertEqual(root_html, injector.inject_html(root_html, ''))
        nested_html = injector.inject_html(original, '../')
        self.assertIn('src="../js/auth-config.js"', nested_html)
        self.assertIn('src="../js/auth-core.js"', nested_html)
        self.assertIn('src="../js/auth-guard.js" data-root="../"', nested_html)
        self.assertEqual(nested_html, injector.inject_html(nested_html, '../'))

    def test_cli_skips_auth_html(self):
        self.assertTrue(INJECTOR_PATH.exists(), f'missing injector: {INJECTOR_PATH}')
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            auth = temp_root / 'auth.html'
            index = temp_root / 'index.html'
            original = '<!doctype html><html><head></head><body></body></html>'
            auth.write_text(original, encoding='utf-8')
            index.write_text(original, encoding='utf-8')
            subprocess.run(
                [sys.executable, str(INJECTOR_PATH), str(temp_root)],
                check=True, capture_output=True, text=True,
            )
            self.assertEqual(original, auth.read_text(encoding='utf-8'))
            self.assertIn('js/auth-guard.js', index.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
