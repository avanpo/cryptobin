#!/usr/bin/env python

"""Tonal system utilities."""

import argparse
import string

from lib import io

parser = argparse.ArgumentParser(
    description=("convert roman numerals to and from ints")
)
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")

ROMAN = [
    (1000, "M"),
    ( 900, "CM"),
    ( 500, "D"),
    ( 400, "CD"),
    ( 100, "C"),
    (  90, "XC"),
    (  50, "L"),
    (  40, "XL"),
    (  10, "X"),
    (   9, "IX"),
    (   5, "V"),
    (   4, "IV"),
    (   1, "I"),
]
ROMAN_DIGIT = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def int_to_roman(integer):
    """Convert an integer to a roman numeral string."""
    result = []
    for (arabic, roman) in ROMAN:
        (factor, integer) = divmod(integer, arabic)
        result.append(roman * factor)
        if integer == 0:
            break
    return "".join(result)


def roman_to_int(numeral):
    """Convert a roman numeral string to an integer."""
    result = 0
    for i, c in enumerate(numeral, start=1):
        if i == len(numeral) or ROMAN_DIGIT[c] > ROMAN_DIGIT[numeral[i]]:
            result += ROMAN_DIGIT[c]
        else:
            result -= ROMAN_DIGIT[c]
    return result


def translate_from_int(integers):
    """Translate a list of integers to a list of roman numeral strings."""
    return [int_to_roman(i) for i in integers]


def roman(data, args):
    integers = io.parse_int_list(data)
    numerals = translate_from_int(integers)
    for r in numerals:
        print("%s " % r, end="")
    print()


def main():
    args, data = io.parse_args(parser)
    roman(data, args)


if __name__ == "__main__":
    main()
