import unittest

from language import words

_TEST_DATA = "asdfasdfexampleahelloatwo"


class TestWords(unittest.TestCase):
    def test_count_words(self):
        self.assertEqual(words.count_words({"hello"}, _TEST_DATA), 1)

        self.assertEqual(
            words.count_words({"hello", "example", "two"}, _TEST_DATA, n=4), 2)
        self.assertEqual(
            words.count_words({"hello", "example", "two"}, _TEST_DATA, n=3), 3)


if __name__ == "__main__":
    unittest.main()
