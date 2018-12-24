#!/usr/bin/env python

"""Alpha encoding utilities at char granularity."""

import argparse
import string
import sys

from lib import io

parser = argparse.ArgumentParser(
        description=("alpha encoding utils, at char level"))
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")


def alpha_to_int(c):
    """Convert a character to an integer. E.g. a=1, b=2, ..."""
    if c in string.ascii_letters:
        return ord(c.lower()) - 97 + 1
    else:
        return 0


def print_encoding(data, encoding):
    for i in range(0, len(encoding), 64):
        l = min(len(encoding[i:]), 64)
        for j in range(i, l):
            print("  %s" % data[j], end="")
        print()
        for j in range(i, l):
            print("%3d" % encoding[j], end="")
        print("\n")


def cenc(data, args):
    data = data.strip()
    encoding = []
    for c in data:
        encoding.append(alpha_to_int(c))
    print_encoding(data, encoding)
    print("Sum: %s" % sum(encoding))
    product = 1
    for i in encoding:
        if i != 0:
            product *= i
    print("Product: %s" % product)


def main():
    args, data = io.parse_args(parser)
    cenc(data, args)


if __name__ == "__main__":
    main()
