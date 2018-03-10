"""
Tests for phenny's tools.py
"""

import unittest
import tools


class ToolsTest(unittest.TestCase):

    def test_break_up(self):
        text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut " \
        "labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea " \
        "rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor " \
        "sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna " \
        "aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd " \
        "gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
        lines = [
            "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut",
            "labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo",
            "dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit",
            "amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor",
            "invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et",
            "justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum",
            "dolor sit amet."
        ]
        self.assertEqual(tools.break_up(text, max_length=100), lines)

    def test_truncate_short(self):
        text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut."
        self.assertEqual(tools.truncate(text, max_length=100), text)

    def test_truncate_long(self):
        text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut " \
        "labore et dolore magna aliquyam erat, sed diam voluptua."
        truncated = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt..."
        self.assertEqual(tools.truncate(text, max_length=100), truncated)
