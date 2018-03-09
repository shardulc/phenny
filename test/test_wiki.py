"""
Tests for phenny's wiki.py
"""

import unittest
import wiki


class WikiTest(unittest.TestCase):

    def test_clean_text(self):
        dirty = "Lorem <tag> ipsum\tdolor\rsit\namet </tag>"
        clean = "Lorem ipsum dolor sit amet"
        self.assertEqual(wiki.clean_text(dirty), clean)
