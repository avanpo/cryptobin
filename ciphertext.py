#!/usr/bin/env python

"""Ciphertext utilities.
"""

import argparse
import string
import sys

import plaintext

parser = argparse.ArgumentParser(description="ciphertext tools")
parser.add_argument("command", metavar="COMMAND",
                    help=("the command to run. currently supported commands "
                          "include: fa"))
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the plaintext file to be analyzed")
parser.add_argument("-l", "--language", type=str,
                    default=plaintext.DEFAULT_LANG,
                    help=("the language being analyzed, in ISO 639-1"
                          "(default: en)"))


def print_fa(observed_freq, lang_freq):
    print("=> Calculated letter frequencies")
    print("   Observed    | Language")
    print("   ------------+-----------")
    observed = sorted(observed_freq, key=observed_freq.get, reverse=True)
    lang = sorted(lang_freq, key=lang_freq.get, reverse=True)
    for o, l in zip(observed, lang):
        print("   %s (%.4f)  | %s (%.4f)" % (o, observed_freq[o],
                                           l, lang_freq[l]))


def fa(data, args):
    observed_freq = plaintext.letter_frequencies(data, args.language)
    lang_freq = plaintext.load_freqs(args.language)
    print_fa(observed_freq, lang_freq)


def main():
    args = parser.parse_args()
    if args.file:
        with open(args.file) as f:
            data = f.read()
    elif not sys.stdin.isatty():
        data = sys.stdin.read()
    else:
        parser.error("no input file found")

    if args.command == "fa":
        fa(data, args)
    else:
        parser.error("command not recognized")


if __name__ == "__main__":
    main()
