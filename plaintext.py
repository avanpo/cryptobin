#!/usr/bin/env python

"""Plaintext utilities.

Usage:

See the --help option for usage information.
"""

import argparse
import collections
import math
import os
import string
import sys

from lib import io

parser = argparse.ArgumentParser(description="plaintext tools")
parser.add_argument(
    "command",
    metavar="COMMAND",
    help="the command to run. currently supported commands include: fa, wc",
)
parser.add_argument(
    "file", metavar="FILE", nargs="?", help="the plaintext file to be analyzed"
)
parser.add_argument(
    "-l",
    "--language",
    type=str,
    default=io.DEFAULT_LANG,
    help="the language being analyzed, in ISO 639-1 (default: en)",
)
parser.add_argument(
    "-n",
    "--ngram",
    type=int,
    default=1,
    help="size of letter groups to analyze (default: 1)",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    default=False,
    help="print out words that are counted",
)
parser.add_argument(
    "-d",
    "--dictionary",
    help="the path of the dictionary to use (example: /usr/share/dict/words)",
)


def load_freqs(lang=io.DEFAULT_LANG, n=1):
    filepath = io.get_lang_filepath("freq", lang)
    if n == 2:
        filepath = io.get_lang_filepath("digram_freq", lang)

    data = io.read_file(filepath, lines=True)
    freqs = {}
    for line in data:
        c, val = line.strip().split()
        freqs[c] = float(val)

    return freqs


def load_words(lang=io.DEFAULT_LANG, filepath=None):
    if not filepath:
        filepath = io.get_lang_filepath("words", lang)

    data = io.read_file(filepath, lines=True)
    words = set()
    for line in data:
        words.add(line.strip())

    return words


def count_letters(data):
    counts = dict.fromkeys(string.ascii_lowercase, 0)
    for c in data:
        if c.lower() in counts:
            counts[c.lower()] += 1
    return counts


def letter_frequencies(data):
    """Calculate the letter frequencies in a text.

    Args:
        data: The text to be analyzed.

    Returns:
        A dictionary of letters with frequencies.
    """
    counts = count_letters(data)
    n = sum(counts.values())
    if not n:
        print("=> ERROR: No alpha characters in input.")
        sys.exit()
    return {k: v / n for k, v in counts.items()}


def ngram_frequencies(data, n=1):
    """Calculate the n-gram frequencies in a text.

    Args:
        data: The text to be analyzed.
        n: Degree of the ngram.

    Returns:
        A dictionary of n-grams with frequencies.
    """
    total_ngrams = sum(count_letters(data).values()) - n + 1
    letters = set(string.ascii_lowercase)
    result = collections.defaultdict(lambda: 0)
    for i in range(0, len(data) - n):
        if data[i] not in letters:
            continue
        ngram = [data[i]]
        for j in range(i + 1, len(data)):
            if len(ngram) == n:
                break
            if data[j] in letters:
                ngram.append(data[j])
        result["".join(ngram)] += 1
    return {k: v / total_ngrams for k, v in result.items()}


def std_dev(data, lang=io.DEFAULT_LANG):
    """Calculate standard deviation from average letter frequencies.

    Args:
        data: The text to be analyzed.
        lang: The language to compare to.

    Returns:
        The letter frequencies' standard deviation from the specified language.
    """
    # TODO: calculate this properly
    lang_freq = load_freqs(lang=lang)
    observed_freq = letter_frequencies(data)

    variance = 0.0
    for c in string.ascii_lowercase:
        variance += (lang_freq[c] - observed_freq[c]) ** 2

    return math.sqrt(variance)


def count_words(data, n=3, lang=io.DEFAULT_LANG, verbose=False, filepath=None):
    """Calculate the approximate number of n+ letter words in a text.

    This function is not accurate, as it has been designed for texts with all
    punctuation and spacing removed. It does not properly handle conjugation
    or spacing. It should, however, be good enough for basic cryptanalysis.

    Args:
        data: The text to be analyzed.
        n: The minimum number of letters in a word. If this is 1, "iiiii" will
        be 5 words (default: 3).
        lang: The language to compare to (default: en).
        verbose: Whether to print words.
        filepath: Use a different dictionary (default: None).

    Returns:
        The approximate number of n+ letter words.
    """
    words = load_words(lang=lang, filepath=filepath)
    data = "".join(data.split())

    count = 0
    i = 0
    while i < len(data):
        for l in range(12, n - 1, -1):
            if i + l < len(data) and data[i : i + l].lower() in words:
                count += 1
                if verbose:
                    print(">", data[i : i + l].lower())
                i += l - 1
                break
        i += 1
    return count


def fa(data, args):
    score = std_dev(data, args.language)
    print("%.4f" % score)


def wc(data, args):
    count = count_words(
        data, lang=args.language, verbose=args.verbose, filepath=args.dictionary
    )
    print(count)


def main():
    args, data = io.parse_args(parser)

    if args.command == "fa":
        fa(data, args)
    elif args.command == "wc":
        wc(data, args)
    else:
        parser.error("%s command not recognized")


if __name__ == "__main__":
    main()
