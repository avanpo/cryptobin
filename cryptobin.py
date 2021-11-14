#!/usr/bin/env python

"Cryptobin CLI."

import argparse
import string

import anagram
import char_counts
import bifid
import frequency_analysis
import morse
import playfair
import roman
import rot
import tonal
from lib import io

parser = argparse.ArgumentParser(description="cryptobin cli tool.")
subparsers = parser.add_subparsers(metavar="SUBCOMMAND")

# Common arguments.
parser.add_argument("file",
                    metavar="FILE",
                    nargs="?",
                    help="the input to be processed")
parser.add_argument("-l",
                    "--language",
                    type=str,
                    default=io.DEFAULT_LANG,
                    help="the language being analyzed, in ISO 639-1 (default: "
                    "en)")

# Subcommands.
anagram.define_arguments(
    subparsers.add_parser("anagram", help="anagram utilities"))
char_counts.define_arguments(
    subparsers.add_parser("counts", help="character counting"))
bifid.define_arguments(
    subparsers.add_parser("bifid", help="bifid cipher utilities"))
frequency_analysis.define_arguments(
    subparsers.add_parser("fa", help="frequency analysis"))
morse.define_arguments(
    subparsers.add_parser("morse", help="morse encoding utilities"))
playfair.define_arguments(
    subparsers.add_parser("playfair", help="playfair cipher utilities"))
roman.define_arguments(
    subparsers.add_parser("roman", help="roman numeral encoding utilities"))
rot.define_arguments(
    subparsers.add_parser("rot", help="text rotation (e.g. ROT13) utilities"))
tonal.define_arguments(
    subparsers.add_parser("tonal", help="tonal encoding utilities"))


def dispatch(data, args):
    if hasattr(args, "func"):
        try:
            args.func(data, args)
        except ValueError as e:
            parser.error(e)
    else:
        parser.error("subcommand not recognized, use -h to list subcommands")


def main():
    args, data = io.parse_args(parser)
    dispatch(data, args)


if __name__ == "__main__":
    main()
