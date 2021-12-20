import unittest

from language import anagram

_ANAGRAMS = {"abd": ["bad", "dab"], "abdr": ["bard"]}


class TestAnagram(unittest.TestCase):
    def test_search(self):
        self.assertEqual(anagram.search(_ANAGRAMS, "brad", 0), {"abdr"})
        self.assertEqual(anagram.search(_ANAGRAMS, "dab", 0), {"abd"})

        self.assertEqual(anagram.search(_ANAGRAMS, "ab", 0), set())

    def test_search_with_unknown(self):
        self.assertEqual(anagram.search(_ANAGRAMS, "abd", 1), {"abdr"})
        self.assertEqual(anagram.search(_ANAGRAMS, "ab", 1), {"abd"})
        self.assertEqual(anagram.search(_ANAGRAMS, "a", 2), {"abd"})

        self.assertEqual(anagram.search(_ANAGRAMS, "x", 2), set())
        self.assertEqual(anagram.search(_ANAGRAMS, "abdr", 1), set())

    def test_search_subsets(self):
        self.assertEqual(anagram.search_subsets(_ANAGRAMS, "aabdr"),
                         ["abdr", "abd"])
        self.assertEqual(anagram.search_subsets(_ANAGRAMS, "dbax"), ["abd"])
        self.assertEqual(anagram.search_subsets(_ANAGRAMS, "dbaxyz"), ["abd"])

        self.assertEqual(anagram.search_subsets(_ANAGRAMS, "xyzxyzxyz"), [])

    def test_multi_word_search(self):
        self.assertEqual(anagram.multi_word_search(_ANAGRAMS, "rabd", 1),
                         [("abdr", )])
        self.assertEqual(anagram.multi_word_search(_ANAGRAMS, "abdrabd", 2),
                         [("abdr", "abd")])

        self.assertEqual(anagram.multi_word_search(_ANAGRAMS, "abdrabda", 2),
                         [])
        self.assertEqual(anagram.multi_word_search(_ANAGRAMS, "abdrabd", 3),
                         [])


if __name__ == "__main__":
    unittest.main()
