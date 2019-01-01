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


def int_to_roman(number):
    """Convert an integer to a roman numeral string."""
    result = []
    for (arabic, roman) in ROMAN:
        (factor, number) = divmod(number, arabic)
        result.append(roman * factor)
        if number == 0:
            break
    return "".join(result)


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
