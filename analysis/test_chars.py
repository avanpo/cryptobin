import unittest

from analysis import chars

_TEST_DATA = "aaa0 ba\nacba"


class TestFrequency(unittest.TestCase):
    def test_count_chars(self):
        self.assertEqual(chars.count_chars(_TEST_DATA), {
            "a": 6,
            "0": 1,
            " ": 1,
            "b": 2,
            "c": 1,
            "\n": 1,
        })
