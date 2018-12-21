#!/usr/bin/env python

"""Diff utilities at char granularity.
"""

import argparse
import string

from lib import io

parser = argparse.ArgumentParser(
    description=("diff tools, on character level.")
)
parser.add_argument("files", metavar="FILES", nargs="*",
                    help="the files to be analyzed")
parser.add_argument("-i", "--case-insensitive", action="store_true",
                    default=False, help="ignore case")


def alpha_char(c1, c2, case_insensitive=False):
    """Analyze the difference in letters between two chars.

    Args:
        c1: The first char.
        c2: The second char.
        case_insensitive: Ignore letter case.

    Returns:
        The difference (expressed as a letter) between the two letters, or a
        dot (.) otherwise.
    """
    b1, b2 = ord(c1.lower()), ord(c2.lower())
    x = 46
    if c1 in string.ascii_uppercase and c2 in string.ascii_uppercase:
        x = (b2 - b1) % 26 + 65
    elif c1 in string.ascii_lowercase and c2 in string.ascii_lowercase:
        x = (b2 - b1) % 26 + 97
    elif case_insensitive and (c1 in string.ascii_letters
                               and c2 in string.ascii_letters):
        x = (b2 - b1) % 26 + 65
    return chr(x)


def letters(data1, data2, case_insensitive=False):
    """Analyze the difference in letters between two texts.

    Args:
        data1: The first text.
        data2: The second text.
        case_insensitive: Ignore letter case.

    Returns:
        A string containing the difference in letters between the two texts.
    """
    diff = []
    for c1, c2 in zip(data1, data2):
        diff.append(alpha_char(c1, c2, case_insensitive))
    return "".join(diff)


def print_diff(data1, data2, diff):
    for i in range(0, len(diff), 64):
        l = min(len(diff[i:]), 64)
        print(data1[i:l])
        print(data2[i:l])
        print("-" * l)
        print(diff[i:l])
        print()


def cdiff(data, args):
    if len(data) == 2:
        d1 = data[0].strip()
        d2 = data[1].strip()
        diff = letters(d1, d2, args.case_insensitive)
        print_diff(d1, d2, diff)
    elif len(data) > 2:
        print("not implemented yet")


def main():
    args, data = io.parse_args_multiple_files(parser)
    cdiff(data, args)


if __name__ == "__main__":
    main()
