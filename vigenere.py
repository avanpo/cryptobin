#!/usr/bin/env python

"""Vigenere cipher utilities.
"""

import argparse
import itertools
import math
import string
import sys

import plaintext
import rot

parser = argparse.ArgumentParser(description=(
    "vigenere cipher tools. with no arguments this tool attempts to break"
    "ciphertext by trying every key length. this tool ignores whitespace"
    "and all punctuation, only letter positiions relative to each other"
    "are used. any newlines in the file are assumed to reset the key."))
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the ciphertext file to be analyzed")
parser.add_argument("-m", "--max-length", type=int, default=10,
                    help="the maximum key length to try (default: 10)")
parser.add_argument("-l", "--language", type=str, default=plaintext.DEFAULT_LANG,
                    help="the language being analyzed, in ISO 639-1 (default: en)")


def strstrip(data):
    return "".join([i for i in data if i in string.ascii_letters])


def stagger_split(data, l):
    output = [""] * l
    for line in data:
        for i, c in enumerate(line):
            output[i % l] += c
    return output


def stagger_join(parts):
    return "".join("".join(x) for x in itertools.zip_longest(*parts, fillvalue=""))


def bruteforce(data, max_length=10, lang=plaintext.DEFAULT_LANG):
    """Attempt to brute force the solution to a Vigenere ciphertext.

    Args:
        data: The ciphertext to be analyzed.
        max_length: The max length of the key.
        lang: The language of the plaintext.

    Returns:
        A list of the most likely plaintexts for each key length.
    """
    data = [strstrip(line) for line in data]

    sols = []
    for i in range(2, max_length + 1):
        split = stagger_split(data, i)
        parts = []
        for s in split:
            part_sols = rot.bruteforce(s, lang)
            parts.append(part_sols[0])
        sol = stagger_join(parts)
        sols.append(sol)
    return sols


def vigenere(data, args):
    sols = bruteforce(data, l=args.max_length, lang=args.language)
    for sol in sols:
        print(sol)


def main():
    args = parser.parse_args()
    if args.file:
        with open(args.file) as f:
            data = f.readlines()
    elif not sys.stdin.isatty():
        data = sys.stdin.readlines()
    else:
        parser.error("no input found")
    vigenere(data, args)


if __name__ == "__main__":
    main()
