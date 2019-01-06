#!/usr/bin/env python

"""PoC framework."""

import argparse
import string

from lib import io

parser = argparse.ArgumentParser(
    description=("quickly write a custom program.")
)
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be processed")


def job(data, args):
    #integers = io.parse_int_list(data)
    #strings = io.parse_list(data)


def main():
    args, data = io.parse_args(parser, need_file=False)
    job(data, args)


if __name__ == "__main__":
    main()
