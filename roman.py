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
parser.add_argument("-n", "--numerals", action="store_true", default=False,
                    help="translate numerals to integers")

ROMAN = [
    (1000, "M", 0),
    ( 900, "CM", 3),
    ( 500, "D", 1),
    ( 400, "CD", 1),
    ( 100, "C", 0),
    (  90, "XC", 3),
    (  50, "L", 1),
    (  40, "XL", 1),
    (  10, "X", 0),
    (   9, "IX", 3),
    (   5, "V", 1),
    (   4, "IV", 1),
    (   1, "I", 0),
]


def int_to_roman(integer):
    """Convert an integer to a roman numeral string."""
    result = []
    for arabic, roman, _ in ROMAN:
        factor, integer = divmod(integer, arabic)
        result.append(roman * factor)
        if integer == 0:
            break
    return "".join(result)


def roman_to_int(numeral):
    """Convert a roman numeral string to an integer."""
    letters = numeral.upper()
    result = 0
    roman_iter = iter(ROMAN)
    for arabic, roman, skip in roman_iter:
        found = False
        for _ in range(0, 3):
            if letters.startswith(roman):
                found = True
                result += arabic
                letters = letters[len(roman):]
                if roman != "M" and roman != "C" and roman != "X" and roman != "I":
                    break
            else:
                break
        if found:
            for _ in range(0, skip):
                next(roman_iter)
    if letters:
        raise SyntaxError("Not a roman numeral: %s" % numeral)
    return result


def is_roman(numeral):
    """Check if a string is a valid roman numeral.

    Only works for strictly positive integers up until 3999."""
    try:
        roman_to_int(numeral)
        return True
    except SyntaxError:
        return False


def translate_from_int(integers):
    """Translate a list of integers to a list of roman numeral strings."""
    return [int_to_roman(i) for i in integers]


def translate_to_int(numerals):
    """Translate a list of roman numeral strings to a list of integers."""
    integers = []
    for s in numerals:
        try:
            integers.append(roman_to_int(s))
        except SyntaxError:
            integers.append(0)
    return integers


def roman(data, args):
    if args.numerals:
        integers = translate_to_int(io.parse_list(data))
        print(",".join(map(str, integers)))
    else:
        numerals = translate_from_int(io.parse_int_list(data))
        print(",".join(numerals))


def main():
    args, data = io.parse_args(parser)
    roman(data, args)


if __name__ == "__main__":
    main()
