import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AuthBackgroundContractTests(unittest.TestCase):
    def test_login_background_has_two_nonempty_formats_and_fallback(self):
        webp = ROOT / "img" / "auth-patrol-night.webp"
        jpeg = ROOT / "img" / "auth-patrol-night.jpg"

        self.assertGreater(webp.stat().st_size, 50_000)
        self.assertGreater(jpeg.stat().st_size, 50_000)

        html = (ROOT / "auth.html").read_text(encoding="utf-8")
        self.assertIn("url('img/auth-patrol-night.webp')", html)
        self.assertIn("url('img/auth-patrol-night.jpg')", html)
        self.assertIn("linear-gradient(", html)
        self.assertIn("@media (prefers-reduced-motion: reduce)", html)


if __name__ == "__main__":
    unittest.main()
