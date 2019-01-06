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


def integer(data, args):
    integers = io.parse_int_list(data)
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
    integer(data, args)


if __name__ == "__main__":
    main()
