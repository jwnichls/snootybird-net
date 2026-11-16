"""The static site: the page and every file it refers to are there, and the address it's served at."""
import re
import unittest
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"


class TestSite(unittest.TestCase):
    def setUp(self):
        self.html = (SITE / "index.html").read_text()

    def test_front_page(self):
        self.assertIn("<title>Snooty Bird Publishing</title>", self.html)
        # The cover and the 37 spread pages, each with its carousel dot
        self.assertEqual(self.html.count("custom-indicator"), 38)

    def test_every_referenced_file_exists(self):
        paths = re.findall(r'(?:src|href|content)="(?:https://www\.snootybird\.net)?(/static/[^"]+)"', self.html)
        self.assertGreater(len(paths), 37)
        for path in paths:
            self.assertTrue((SITE / path.lstrip("/")).is_file(), path)

    def test_root_files_and_domain(self):
        for name in ("favicon.ico", "robots.txt", ".nojekyll"):
            self.assertTrue((SITE / name).is_file(), name)
        self.assertEqual((SITE / "CNAME").read_text().strip(), "www.snootybird.net")


if __name__ == "__main__":
    unittest.main()
