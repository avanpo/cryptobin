#!/usr/bin/env python

"""Tonal system utilities."""

import argparse
import string

from lib import io

parser = argparse.ArgumentParser(
    description=("tonal system utilities")
)
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")

zero = "noll"
tones = {
        "an": 1,
        "de": 2,
        "ti": 3,
        "go": 4,
        "su": 5,
        "by": 6,
        "ra": 7,
        "me": 8,
        "ni": 9,
        "ko": 10,
        "hu": 11,
        "vy": 12,
        "la": 13,
        "po": 14,
        "fy": 15,
        }
digits = {
        "ton": 16,
        "san": 256,
        "mill": 4096,
        "bong": 65536,
        }


def tonal_word_to_int(word):
    if word == zero:
        return 0
    total_value = 0
    prev_word = word
    while word:
        digit_value = 1
        for digit, val in digits.items():
            if word.endswith(digit):
                digit_value = val
                word = word[:-len(digit)]
                break
        for tone, val in tones.items():
            if word.endswith(tone):
                digit_value *= val
                word = word[:-len(tone)]
                break
        total_value += digit_value
        if word == prev_word:
            return -1
        else:
            prev_word = word
    return total_value


def translate_to_int(words):
    """Translate tonal to integers.

    Args:
        words: A list of strings containing tonal words.

    Returns:
        A list of integers.
    """
    return list(map(tonal_word_to_int, words))


def tonal(data, args):
    words = io.parse_list(data)
    ints = translate_to_int(words)
    for i in ints:
        print("%d " % i, end="")
    print()


def main():
    args, data = io.parse_args(parser)
    tonal(data, args)


if __name__ == "__main__":
    main()
