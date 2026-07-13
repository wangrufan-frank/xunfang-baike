from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
THEME_JS = ROOT / 'js' / 'theme.js'
CSS = (ROOT / 'css' / 'style.css').read_text(encoding='utf-8')


class ThemeAssetTests(unittest.TestCase):
    def test_theme_script_defines_supported_themes_and_safe_storage(self):
        script = THEME_JS.read_text(encoding='utf-8')
        for theme in ('warm-police-blue', 'classic-warm-brown', 'daylight', 'night'):
            self.assertIn("'" + theme + "'", script)
        self.assertIn('xunfang-theme', script)
        self.assertIn('localStorage', script)
        self.assertIn('try', script)
        self.assertIn('window.XunfangTheme', script)
        self.assertIn('set: set', script)

    def test_each_non_default_theme_overrides_core_color_tokens(self):
        for theme in ('classic-warm-brown', 'daylight', 'night'):
            match = re.search(
                rf'html\[data-theme="{theme}"\]\s*\{{(.*?)\}}',
                CSS,
                re.DOTALL,
            )
            self.assertIsNotNone(match, theme)
            rules = match.group(1)
            for token in ('--bg', '--warm-white', '--text', '--nav-bg', '--border', '--police-blue', '--amber'):
                self.assertIn(token + ':', rules, theme + ': ' + token)

    def test_pages_load_theme_script_before_navigation_script(self):
        pages = []
        for page in ROOT.rglob('*.html'):
            source = page.read_text(encoding='utf-8')
            if 'nav.js' in source:
                pages.append(page)
                self.assertIn('theme.js', source, page.as_posix())
                self.assertLess(source.index('theme.js'), source.index('nav.js'), page.as_posix())
        self.assertGreater(len(pages), 0)

    def test_navigation_provides_accessible_theme_selector(self):
        script = (ROOT / 'js' / 'nav.js').read_text(encoding='utf-8')
        self.assertIn('class="theme-selector"', script)
        self.assertIn('class="theme-toggle"', script)
        self.assertIn('aria-haspopup="true"', script)
        self.assertIn('aria-expanded="false"', script)
        for theme in ('warm-police-blue', 'classic-warm-brown', 'daylight', 'night'):
            self.assertIn("value: '" + theme + "'", script)
        self.assertIn('data-theme-option="\' + theme.value + \'"', script)
        self.assertIn('window.XunfangTheme.set(theme)', script)

    def test_theme_selector_has_mobile_and_night_styles(self):
        for selector in (
            '.theme-selector',
            '.theme-toggle',
            '.theme-menu',
            '.theme-option[aria-checked="true"]',
            'html[data-theme="night"] .theme-menu',
        ):
            self.assertIn(selector, CSS)
        self.assertIn('.topnav .nav-links.open .theme-selector', CSS)


if __name__ == '__main__':
    unittest.main()
