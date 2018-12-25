#!/usr/bin/env python

"""Encoding utilities at char granularity."""

import argparse
import string
import sys

from lib import io

parser = argparse.ArgumentParser(
        description=("encoding utils, at char level"))
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")
parser.add_argument("-i", "--input", type=str, default="ascii",
                    help="input type (ascii, alpha, int, hex)")
parser.add_argument("-o", "--output", type=str, default="ascii",
                    help="output type (ascii, alpha, int, hex)")
parser.add_argument("-t", "--io", type=str, default="ai",
                    help="convenience method; 'ai' is alpha in, int out")
parser.add_argument("-0", "--zero-based", action="store_true", default=False,
                    help="encoding is zero-based (default: false)")
parser.add_argument("-f", "--overflow", action="store_true", default=False,
                    help="allow encoding overflow (default: false)")
parser.add_argument("-v", "--verbose", action="store_true", default=False,
                    help="print the original data over the encoding")

types = {
        "a": "a",
        "alpha": "a",
        "c": "c",
        "ascii": "c",
        "i": "i",
        "int": "i",
        "x": "x",
        "hex": "x",
        }


def alpha_to_int_single(c, zero_based=False, overflow=False):
    offset = 0 if zero_based else 1
    if c in string.ascii_letters:
        return ord(c.lower()) - 97 + offset
    elif overflow:
        return ((260 + ord(c.lower()) - 97) % 26) + offset
    else:
        return -1


def alpha_to_int(data, zero_based=False, overflow=False):
    """Convert an alpha text to a sequence of integers.

    E.g. a=1, b=2, ...

    Args:
        data: The string text.
        zero_based: Whether a=0 or a=1. Default is a=1.

    Returns:
        A list of integers.
    """
    return list(map(lambda c: alpha_to_int_single(c, zero_based, overflow),
                    data))


def int_to_alpha_single(i, zero_based=False, overflow=False):
    offset = 0 if zero_based else 1
    if overflow:
        i = ((i - offset) % 26) + offset
    if i < offset or i >= 26 + offset:
        return "."
    return chr(i + 97 - offset)


def int_to_alpha(sequence, zero_based=False, overflow=False):
    """Convert a list of integers to a list of alpha characters.

    E.g. 1=a, 2=b, ...

    Args:
        sequence: A list of integers.
        zero_based: Whether 1=a or 1=b. Default is 1=a.
        overflow: Whether 27=a or 27 is nothing (represented as .)

    Returns:
        A list of chars.
    """
    return list(map(lambda i: int_to_alpha_single(i, zero_based, overflow),
                    sequence))


def print_encoding(data, encoding, sep=None, verbose=False):
    if verbose:
        print_verbose(data, encoding)
        return
    if not sep:
        sep = ""
    print(sep.join(encoding))


def print_verbose(data, encoding):
    for i in range(0, len(encoding), 16):
        l = min(len(encoding[i:]), 16)
        for j in range(i, i + l):
            print("%4s" % data[j], end="")
        print()
        for j in range(i, i + l):
            print("%4s" % encoding[j], end="")
        print("\n")


def get_int_list(data):
    return list(map(lambda s: int(s.strip()),
                    data.replace("\n", ",").replace(" ", ",").split(",")))


def encoding(data, args):
    data = data.strip()
    if len(args.io) == 2:
        args.input = args.io[0]
        args.output = args.io[1]

    if types[args.input] == "a" and types[args.output] == "i":
        encoding = list(map(str,
                            alpha_to_int(data, args.zero_based, args.overflow)))
        print_encoding(data, encoding, sep=" ", verbose=args.verbose)
    elif types[args.input] == "i" and types[args.output] == "a":
        data = get_int_list(data)
        encoding = int_to_alpha(data, args.zero_based, args.overflow)
        print_encoding(data, encoding, verbose=args.verbose)
    else:
        print("unknown input/output combination")


def main():
    args, data = io.parse_args(parser)
    encoding(data, args)


if __name__ == "__main__":
    main()
