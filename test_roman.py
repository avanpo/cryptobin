import unittest

import roman


class TestRoman(unittest.TestCase):
    def test_int_to_roman(self):
        self.assertEqual(roman.int_to_roman(1), "I")
        self.assertEqual(roman.int_to_roman(2), "II")
        self.assertEqual(roman.int_to_roman(9), "IX")
        self.assertEqual(roman.int_to_roman(1791), "MDCCXCI")
        self.assertEqual(roman.int_to_roman(3999), "MMMCMXCIX")

    def test_roman_to_int(self):
        self.assertEqual(roman.roman_to_int("I"), 1)
        self.assertEqual(roman.roman_to_int("II"), 2)
        self.assertEqual(roman.roman_to_int("IX"), 9)
        self.assertEqual(roman.roman_to_int("MDCCXCI"), 1791)
        self.assertEqual(roman.roman_to_int("MMMCMXCIX"), 3999)

    def test_translate_from_int(self):
        self.assertEqual(roman.translate_from_int([1, 2]), ["I", "II"])

    def test_translate_to_int(self):
        self.assertEqual(roman.translate_to_int(["I", "II"]), [1, 2])

    def test_is_roman(self):
        self.assertTrue(roman.is_roman("I"))
        self.assertTrue(roman.is_roman("MMMCMXCIX"))

        self.assertFalse(roman.is_roman("A"))


if __name__ == "__main__":
    unittest.main()
