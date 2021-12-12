import string
import unittest

import frequency

_TEST_DATA = "aaa0 ba\nacba"


class TestFrequency(unittest.TestCase):
    def test_count_chars(self):
        self.assertEqual(frequency.count_chars(_TEST_DATA), {
            "a": 6,
            "0": 1,
            " ": 1,
            "b": 2,
            "c": 1,
            "\n": 1,
        })

    def test_count_letters(self):
        expected = {l: 0 for l in string.ascii_lowercase}
        expected["a"] = 6
        expected["b"] = 2
        expected["c"] = 1
        self.assertEqual(frequency.count_letters(_TEST_DATA), expected)

    def test_letter_frequencies(self):
        expected = {"a": 6 / 9, "b": 2 / 9, "c": 1 / 9}

        self.assertEqual(frequency.letter_ngram_frequencies(_TEST_DATA, 1),
                         expected)
        self.assertEqual(frequency.letter_ngram_frequencies(_TEST_DATA),
                         expected)

    def test_letter_ngram_frequencies(self):
        self.assertEqual(frequency.letter_ngram_frequencies(_TEST_DATA, 2), {
            "aa": 0.375,
            "ab": 0.125,
            "ba": 0.25,
            "ac": 0.125,
            "cb": 0.125,
        })
