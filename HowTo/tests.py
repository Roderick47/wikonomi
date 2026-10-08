"""Validation for the first PNG guide-content batch."""
from importlib import import_module
from pathlib import Path

from django.test import SimpleTestCase

seeder = import_module("HowTo.migrations.0003_seed_batch1_png_guides")


class BatchOneGuideContentTests(SimpleTestCase):
    def test_all_five_guides_are_well_formed(self):
        base = Path(seeder.__file__).resolve().parents[1] / "guide_content" / "batch1"
        titles = set()
        for filename in seeder.FILENAMES:
            with self.subTest(filename=filename):
                title, description, steps = seeder._extract(
                    (base / filename).read_text(encoding="utf-8")
                )
                self.assertNotIn(title, titles)
                titles.add(title)
                self.assertTrue(description)
                self.assertGreaterEqual(len(steps), 9)
                self.assertGreaterEqual(steps[-1][1].count("https://"), 3)
                self.assertIn("8 October 2026", steps[-1][1])
                public_text = "\n".join(body for _, body in steps)
                self.assertNotIn("Editorial verification notes", public_text)

        self.assertEqual(len(titles), 5)

    def test_invalid_guide_cannot_be_imported(self):
        with self.assertRaises(ValueError):
            seeder._extract("# Incomplete guide\n\nDescription")
