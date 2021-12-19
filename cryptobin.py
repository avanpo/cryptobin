#!/usr/bin/env python

"Cryptobin CLI."

import argparse
import string

import char_count
from analysis import frequency
from ciphers import bifid
from ciphers import playfair
from ciphers import rot
from ciphers import submap
from ciphers import vigenere
from encoding import encoding
from encoding import morse
from encoding import roman
from encoding import tonal
from language import anagram
from language import words
from maths import integer
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
                    default=dictionary.dictionary,
                    help="the language being analyzed, in ISO 639-1 (default: "
                    "en)")

# Subcommands.
anagram.define_arguments(
    subparsers.add_parser("anagram", help="anagram utilities"))
bifid.define_arguments(
    subparsers.add_parser("bifid", help="bifid cipher utilities"))
char_count.define_arguments(
    subparsers.add_parser("count", help="character counting"))
encoding.define_arguments(
    subparsers.add_parser("enc", help="character encoding transformations"))
frequency.define_arguments(
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
words.define_arguments(subparsers.add_parser("words", help="word utilities"))


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
