#!/usr/bin/env python

"Cryptobin CLI."

import argparse
import string

import anagram
import char_count
import dictionary
import encoding
import frequency_analysis
import integer
import morse
import roman
import rot
import submap
import tonal
from ciphers import bifid
from ciphers import playfair
from ciphers import vigenere
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
bifid.define_arguments(
    subparsers.add_parser("bifid", help="bifid cipher utilities"))
char_count.define_arguments(
    subparsers.add_parser("count", help="character counting"))
dictionary.define_arguments(
    subparsers.add_parser("dict", help="test a word against the dictionary"))
encoding.define_arguments(
    subparsers.add_parser("encoding",
                          help="character encoding transformations"))
frequency_analysis.define_arguments(
    subparsers.add_parser("fa", help="frequency analysis"))
integer.define_arguments(
    subparsers.add_parser("int", help="integer sequence analysis"))
morse.define_arguments(
    subparsers.add_parser("morse", help="morse encoding utilities"))
playfair.define_arguments(
    subparsers.add_parser("playfair", help="playfair cipher utilities"))
roman.define_arguments(
    subparsers.add_parser("roman", help="roman numeral encoding utilities"))
rot.define_arguments(
    subparsers.add_parser("rot", help="text rotation (e.g. ROT13) utilities"))
submap.define_arguments(
    subparsers.add_parser("submap", help="substitution cipher utilities"))
tonal.define_arguments(
    subparsers.add_parser("tonal", help="tonal encoding utilities"))
vigenere.define_arguments(
    subparsers.add_parser("vigenere", help="vigenere cipher utilities"))


def main():
    args, data = io.parse_args(parser)

    if hasattr(args, "func"):
        try:
            args.func(data, args)
        except ValueError as e:
            parser.error(e)
    else:
        parser.error("subcommand not recognized, use -h to list subcommands")


if __name__ == "__main__":
    main()
