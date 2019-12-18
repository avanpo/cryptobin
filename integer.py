#!/usr/bin/env python

"""Integer and integer sequence utilities."""

import argparse
import string
from sympy import ntheory

from lib import io

parser = argparse.ArgumentParser(
    description=("integer tools.")
)
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")
parser.add_argument("-s", "--step", action="store_true", default=False,
                    help="calculate step between sequence elements (default: false)")


def digit(i, n):
    """Return the nth digit of the integer.

    For example, the 1st digit of 512 is 5.
    """
    e = len(str(i)) - n
    return i // 10**e % 10


def step(integers):
    """Return the deltas between each consecutive pair of integers."""
    prev = None
    for i in integers:
        if not prev:
            prev = i
            continue
        print("%s " % (i - prev), end='')
        prev = i


def integer(integers):
    product = 1
    num_factors = 0
    for i in integers:
        print("%16d: " % i, end="")
        factors = ntheory.factorint(i)
        for factor, exp in factors.items():
            num_factors += exp
            print("%d^%d " % (factor, exp), end="")
        print()
        if i != 0:
            product *= i

    print("\nSequence length:  %d" % len(integers))
    print("Sequence sum:     %d" % sum(integers))
    print("Sequence product: %d" % product)
    print("Sequence factors: %d" % num_factors)


def main():
    args, data = io.parse_args(parser)
    integers = io.parse_int_list(data)
    if args.step:
        step(integers)
    else:
        integer(integers)


if __name__ == "__main__":
    main()
