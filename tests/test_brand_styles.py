from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'css' / 'style.css').read_text(encoding='utf-8')


def declaration(name):
    match = re.search(rf'{re.escape(name)}:\s*([^;]+);', CSS)
    return match.group(1).strip() if match else None


class BrandStyleTests(unittest.TestCase):
    def test_warm_police_blue_tokens_are_defined(self):
        self.assertEqual(declaration('--police-blue'), '#1F4E79')
        self.assertEqual(declaration('--police-blue-deep'), '#163A5C')
        self.assertEqual(declaration('--mist-blue'), '#EAF2F8')
        self.assertEqual(declaration('--warm-white'), '#FFFCF7')
        self.assertEqual(declaration('--amber'), '#D98B2B')
        self.assertEqual(declaration('--radius'), '12px')

    def test_base_components_consume_shared_tokens(self):
        self.assertIn('background: var(--police-blue);', CSS)
        self.assertIn('background: var(--warm-white);', CSS)
        self.assertIn('border-radius: var(--radius);', CSS)

    def test_feature_components_use_warm_police_blue_tokens(self):
        self.assertIn(
            'background: linear-gradient(135deg, var(--police-blue-deep) 0%, var(--police-blue) 100%);',
            CSS,
        )
        self.assertIn('background: var(--amber);', CSS)
        self.assertIn('border-left: 4px solid var(--police-blue);', CSS)
        self.assertIn('box-shadow: var(--shadow);', CSS)

    def test_monthly_home_panel_uses_shared_theme_tokens(self):
        script = (ROOT / "js" / "monthly-hero.js").read_text(encoding="utf-8")
        self.assertIn('class="monthly-hero-grid"', script)
        self.assertIn('class="monthly-current"', script)
        self.assertIn('class="monthly-archive"', script)
        self.assertIn("renderMonthlyHero(monthlyData, document)", script)
        self.assertIn("var(--police-blue-deep)", CSS)
        self.assertIn(".monthly-archive", CSS)
        archive_text = re.search(
            r'\.monthly-archive-heading,\s*\.monthly-archive-item,\s*'
            r'\.monthly-archive-all\s*\{([^}]+)\}',
            CSS,
        )
        archive_muted = re.search(
            r'\.monthly-archive-heading span,\s*\.monthly-archive-item span,\s*'
            r'\.monthly-archive-empty\s*\{([^}]+)\}',
            CSS,
        )
        self.assertIsNotNone(archive_text)
        self.assertIsNotNone(archive_muted)
        self.assertIn("color: var(--nav-text);", archive_text.group(1))
        self.assertIn("color: var(--text-secondary);", archive_muted.group(1))

    def test_module_card_accents_use_one_brand_border(self):
        accent_rules = re.findall(r'\.module-card\.accent-[^{]+\{([^}]+)\}', CSS)
        self.assertGreaterEqual(len(accent_rules), 7)
        for rule in accent_rules:
            self.assertIn('border-top: 3px solid var(--police-blue);', rule)


if __name__ == '__main__':
    unittest.main()
