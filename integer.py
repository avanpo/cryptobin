#!/usr/bin/env python
"""Integer and integer sequence utilities."""

import statistics
from sympy import ntheory

from lib import io


def define_arguments(parser):
    parser.set_defaults(func=integer)
    parser.add_argument(
        "-s",
        "--step",
        action="store_true",
        default=False,
        help="Calculate steps between sequence elements. Default: false.")
    parser.add_argument(
        "-x",
        "--sort",
        action="store_true",
        default=False,
        help="Sort the output of the sequence. Default: false.")


def digit(i, n):
    """Return the nth digit of the integer.

    For example, the 1st digit of 512 is 5.
    """
    e = len(str(i)) - n
    return i // 10**e % 10


def step(integers):
    """Print the deltas between each consecutive pair of integers."""
    prev = None
    for i in integers:
        if not prev:
            prev = i
            continue
        print("%s " % (i - prev), end='')
        prev = i
    print()


def sequence_stats(integers):
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

    print(f"\nSequence length:  {len(integers)}")
    print(f"Sequence sum:     {sum(integers)}")
    print(f"Sequence product: {product}")
    print(f"Sequence factors: {num_factors}")

    si = sorted(integers)
    median = statistics.median(si)
    print(f"Min/median/max:   {si[0]}/{median}/{si[-1]}")


def integer(data, args):
    integers = io.parse_int_list(data)
    if args.sort:
        integers = sorted(integers)

    if args.step:
        step(integers)
    else:
        sequence_stats(integers)
