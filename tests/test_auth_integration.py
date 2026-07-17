import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.git', '.worktrees', '.superpowers', 'deliverables', 'docs'}
INJECTOR_PATH = ROOT / 'tools' / 'inject_auth_guard.py'
AUTH_SCRIPT_RE = re.compile(
    r'<script\b[^>]*\bsrc=["\'][^"\']*js/auth-(?:config|core|guard)\.js["\'][^>]*>'
    r'\s*</script>',
    re.IGNORECASE,
)


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
            relative = page.relative_to(ROOT)
            self.assertIn(len(relative.parts), (1, 2), page)
            prefix = '' if page.parent == ROOT else '../'
            expected = [
                f'<script src="{prefix}js/auth-config.js"></script>',
                f'<script src="{prefix}js/auth-core.js"></script>',
                f'<script src="{prefix}js/auth-guard.js" data-root="{prefix}"></script>',
            ]
            self.assertIn('\n'.join(expected) + '\n', head, page)
            self.assertEqual(expected, AUTH_SCRIPT_RE.findall(head), page)
            self.assertEqual(expected, AUTH_SCRIPT_RE.findall(html), page)

    def test_auth_page_has_accessible_account_password_controls(self):
        html = (ROOT / 'auth.html').read_text(encoding='utf-8')
        for value in ('id="username"', 'id="password"', 'id="toggle-password"',
                      'id="submit"', 'aria-live="polite"', 'js/auth-page.js'):
            self.assertIn(value, html)

    def test_auth_config_stores_only_a_digest_as_credential_material(self):
        config = (ROOT / 'js' / 'auth-config.js').read_text(encoding='utf-8')
        fields = set(re.findall(r'^\s{4}([A-Za-z_$][\w$]*):', config, re.MULTILINE))
        self.assertEqual({'username', 'digest', 'cookieName', 'maxAgeSeconds'}, fields)
        self.assertRegex(config, r"digest:\s*'[0-9a-f]{64}'")
        self.assertNotRegex(
            config,
            r'(?i)\b(?:password|passcode|secret|credential|plaintext)\w*\s*:',
        )

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

    def test_inject_html_normalizes_partial_or_incorrect_auth_scripts(self):
        injector = load_injector()
        expected = (
            '<script src="js/auth-config.js"></script>\n'
            '<script src="js/auth-core.js"></script>\n'
            '<script src="js/auth-guard.js" data-root=""></script>\n'
        )
        cases = (
            '<html><head><script src="js/auth-guard.js"></script></head><body></body></html>',
            '<html><head><script async src="js/auth-core.js"></script>'
            '<script src="../js/auth-config.js"></script></head><body></body></html>',
            '<html><head><script src="../js/auth-guard.js" data-root="bad"></script>'
            '<script defer src="../js/auth-core.js"></script>'
            '<script src="../js/auth-config.js"></script></head><body></body></html>',
            '<html><head></head><body>Documentation mentions auth-guard.js.</body></html>',
        )
        for html in cases:
            with self.subTest(html=html):
                injected = injector.inject_html(html, '')
                self.assertEqual(expected.splitlines(), AUTH_SCRIPT_RE.findall(injected))
                self.assertIn(expected + '</head>', injected)
                self.assertEqual(injected, injector.inject_html(injected, ''))

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
