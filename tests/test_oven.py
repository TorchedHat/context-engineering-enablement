"""Run with: python3 -m unittest -v tests/test_oven.py"""
import unittest

from bakery.oven import bake
from bakery.config import OVENS, RECIPES


class TestOven(unittest.TestCase):
    def test_every_recipe_bakes_on_every_oven(self):
        for package in RECIPES:
            for oven in OVENS:
                result = bake(package, oven, verbose=True)
                self.assertEqual(result["status"], "golden")


if __name__ == "__main__":
    unittest.main()
