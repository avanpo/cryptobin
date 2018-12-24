#!/usr/bin/env python

"""Integer and integer sequence utilities."""

import argparse
import string
from sympy.ntheory import factorint

from lib import io

parser = argparse.ArgumentParser(
    description=("integer tools.")
)
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")


def integer(data, args):
    integers = list(map(lambda s: int(s.strip()),
                        data.strip().replace("\n", ",").split(",")))
    product = 1
    for i in integers:
        print("%16d: " % i, end="")
        factors = factorint(i)
        for factor, exp in factors.items():
            print("%d^%d " % (factor, exp), end="")
        print()
        if i != 0:
            product *= i

    print("\nSequence length:  %d" % len(integers))
    print("Sequence sum:     %d" % sum(integers))
    print("Sequence product: %d" % product)


def main():
    args, data = io.parse_args(parser)
    integer(data, args)


if __name__ == "__main__":
    main()
