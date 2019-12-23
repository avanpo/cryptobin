#!/usr/bin/env python

"""Ciphertext utilities.

Usage:

See the --help option for usage information.
"""

import argparse
import string
import sys

import plaintext
from lib import io

parser = argparse.ArgumentParser(description="ciphertext tools")
parser.add_argument(
    "command",
    metavar="COMMAND",
    help=("the command to run. currently supported commands " "include: counts, fa"),
)
parser.add_argument(
    "file", metavar="FILE", nargs="?", help="the plaintext file to be analyzed"
)
parser.add_argument(
    "-l",
    "--language",
    type=str,
    default=io.DEFAULT_LANG,
    help=("the language being analyzed, in ISO 639-1" "(default: en)"),
)
parser.add_argument(
    "-n",
    "--ngram",
    type=int,
    default=1,
    help="size of letter groups to analyze (default: 1)",
)


def print_fa(observed_freq, lang_freq):
    print("=> Calculated letter frequencies")
    print("   Observed      | Language")
    print("   --------------+-------------")
    observed = sorted(observed_freq, key=observed_freq.get, reverse=True)
    lang = sorted(lang_freq, key=lang_freq.get, reverse=True)
    rows = 0
    for o, l in zip(observed, lang):
        print("   %3s (%.4f)  | %3s (%.4f)" % (o, observed_freq[o], l, lang_freq[l]))
        rows += 1
        if rows > 30:
            break


def fa(data, args):
    observed_freq = plaintext.ngram_frequencies(data, n=args.ngram)
    lang_freq = plaintext.load_freqs(args.language, n=args.ngram)
    print_fa(observed_freq, lang_freq)


def counts(data, args):
    la, ua, nr, p, w, np = 0, 0, 0, 0, 0, 0
    for c in data:
        if c in string.ascii_lowercase:
            la += 1
        elif c in string.ascii_uppercase:
            ua += 1
        elif c in string.digits:
            nr += 1
        elif c in string.punctuation:
            p += 1
        elif c in string.whitespace:
            w += 1
        else:
            np += 1
    print("=> Character class counts")
    print("   lalpha | ualpha |  digit |   punc | wspace | nonprint")
    print("   -------+--------+--------+--------+--------+---------")
    print("   %6d | %6d | %6d | %6d | %6d | %8d" % (la, ua, nr, p, w, np))


def main():
    args, data = io.parse_args(parser)

    if args.command == "fa":
        fa(data, args)
    elif args.command == "counts":
        counts(data, args)
    else:
        parser.error("command not recognized")


if __name__ == "__main__":
    main()
