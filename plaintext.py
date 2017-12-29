#!/usr/bin/env python

import argparse
import math
import os
import string
import sys

DEFAULT_LANG = "en"

parser = argparse.ArgumentParser(description="plaintext tools")
parser.add_argument("command", metavar="COMMAND",
                    help="the command to run. currently supported commands include: fa, wc")
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the plaintext file to be analyzed")
parser.add_argument("-l", "--language", type=str, default=DEFAULT_LANG,
                    help="the language being analyzed, in ISO 639-1 (default: en)")
parser.add_argument("-d", "--dictionary",
                    help="the path of the dictionary to use (example: /usr/share/dict/words)")


def get_filepath(prefix, lang):
    lib_dir = os.path.dirname(__file__)
    return os.path.join(lib_dir, "lang/%s_%s.txt" % (prefix, lang))


def load_freqs(lang=DEFAULT_LANG):
    filepath = get_filepath("freq", lang)

    freqs = {}
    try:
        with open(filepath) as f:
            for line in f:
                c, val = line.split()
                freqs[c] = float(val)
    except EnvironmentError:
        print("=> ERROR: Could not open %s." % filepath)
        sys.exit()

    return freqs


def load_words(filepath=None, lang=DEFAULT_LANG):
    if not filepath:
        filepath = get_filepath("words", lang)

    words = set()
    try:
        with open(filepath) as f:
            for line in f:
                words.add(line.strip())
    except EnvironmentError:
        print("=> ERROR: Could not open %s." % filepath)
        sys.exit()

    return words


def count_letters(data):
    counts = dict.fromkeys(string.ascii_lowercase, 0)
    for c in data:
        if c.lower() in counts:
            counts[c.lower()] += 1
    return counts


def std_dev(data, lang=DEFAULT_LANG):
    """Calculate standard deviation from average letter frequencies.
    """
    # TODO: calculate this properly
    freqs = load_freqs(lang)
    counts = count_letters(data)
    n = sum(counts.values())

    if not n:
        return -1

    variance = 0.0
    for c in string.ascii_lowercase:
        variance += (freqs[c] - (counts[c] / float(n))) ** 2
    
    return math.sqrt(variance), n


def count_words(data, words):
    """Calculate the approximate number of 3+ letter words in a text.

    This function is not accurate, as it has been designed for texts with all
    punctuation and spacing removed. It does not properly handle conjugation
    or spacing. It should, however, be good enough for basic cryptanalysis.
    """
    data = "".join(data.split())

    count = 0
    i = 0
    while i < len(data):
        for l in range(12, 3, -1):
            if i + l < len(data) and data[i:i + l].lower() in words:
                print(data[i:i + l].lower())
                count += 1
                i += l - 1
                break
        i += 1
    return count


def fa(data, args):
    lscore, ln = std_dev(data, args.language)
    print("%.4f" % lscore)


def wc(data, args):
    words = load_words(filepath=args.dictionary, lang=args.language)
    count = count_words(data, words)
    print(count)


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
    elif args.command == "wc":
        wc(data, args)
    else:
        parser.error("%s command not recognized")


if __name__ == "__main__":
    main()
