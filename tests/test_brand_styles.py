from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'css' / 'style.css').read_text(encoding='utf-8')


def declaration(name):
    match = re.search(rf'{re.escape(name)}:\s*([^;]+);', CSS)
    return match.group(1).strip() if match else None


def theme_color(selector, name):
    block = re.search(rf'{re.escape(selector)}\s*\{{([^}}]+)\}}', CSS)
    if not block:
        return None
    match = re.search(rf'{re.escape(name)}:\s*(#[0-9A-Fa-f]{{6}});', block.group(1))
    return match.group(1) if match else None


def rgb(hex_color):
    return tuple(int(hex_color[index:index + 2], 16) / 255 for index in (1, 3, 5))


def mix(first, second, first_weight):
    return tuple(
        first[index] * first_weight + second[index] * (1 - first_weight)
        for index in range(3)
    )


def luminance(color):
    linear = [
        value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4
        for value in color
    ]
    return .2126 * linear[0] + .7152 * linear[1] + .0722 * linear[2]


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
            'background: linear-gradient(135deg, var(--police-blue-deep) 0%, '
            'color-mix(in srgb, var(--police-blue) 55%, var(--police-blue-deep)) 100%);',
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
        self.assertIn("color: var(--nav-text);", archive_muted.group(1))
        self.assertIn("opacity: 1;", archive_muted.group(1))

        for selector in (
            ':root', 'html[data-theme="classic-warm-brown"]',
            'html[data-theme="daylight"]', 'html[data-theme="night"]'
        ):
            deep = rgb(theme_color(selector, '--police-blue-deep'))
            blue = rgb(theme_color(selector, '--police-blue'))
            gradient_end = mix(blue, deep, .55)
            archive_background = mix((1, 1, 1), gradient_end, .06)
            contrast = 1.05 / (luminance(archive_background) + .05)
            with self.subTest(theme=selector):
                self.assertGreaterEqual(contrast, 4.5)

    def test_home_priority_cards_are_theme_driven_and_responsive(self):
        for selector in (
            '.home-priority-links', '.home-priority-card',
            '.home-priority-card--internal', '.home-priority-card--fitness'
        ):
            self.assertIn(selector, CSS)
        self.assertIn('@media (min-width: 1520px)', CSS)
        self.assertIn('var(--police-blue)', CSS)
        self.assertIn('var(--amber)', CSS)
        self.assertIn('.home-priority-card strong { color: var(--text); }', CSS)

    def test_legal_accordion_and_street_badge_use_shared_tokens(self):
        for selector in (
            '.legal-toc-chapter', '.legal-toc-chapter-heading',
            '.chapter-block', '.street-common-badge', '.street-note'
        ):
            self.assertIn(selector, CSS)
        self.assertIn('var(--amber)', CSS)
        self.assertIn('var(--police-blue)', CSS)
        self.assertRegex(CSS, r'\.article-group,\s*\.legal-article\s*\{\s*scroll-margin-top: 6rem;')

    def test_main_script_enhances_article_and_legal_toc_links(self):
        script = (ROOT / "js" / "main.js").read_text(encoding="utf-8")
        self.assertIn('.article-toc a[href^="#"], .legal-toc a[href^="#"]', script)
        self.assertIn("expandAndScrollTo(target)", script)

    def test_module_card_accents_use_one_brand_border(self):
        accent_rules = re.findall(r'\.module-card\.accent-[^{]+\{([^}]+)\}', CSS)
        self.assertGreaterEqual(len(accent_rules), 7)
        for rule in accent_rules:
            self.assertIn('border-top: 3px solid var(--police-blue);', rule)


if __name__ == '__main__':
    unittest.main()
