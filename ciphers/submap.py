#!/usr/bin/env python
"""Substitution map utils. Also known as cryptograms."""

import string

import dictionary
import plaintext
from lib import io


def define_arguments(parser):
    parser.set_defaults(func=submap)
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=5,
        help="The depth of the breadth first search. Default: 5.")
    parser.add_argument(
        "-e",
        "--letter-depth",
        type=int,
        default=18,
        help=("The number of letters to attempt to swap around, ordered by "
              "observed frequency. This helps speed things up, as infrequent "
              "characters shouldn't affect readability as much. Default: 18."))
    parser.add_argument(
        "-r",
        "--replace",
        type=str,
        help=("Replace, in order, a comma-separated list of two letters with "
              "each other. For example, 'ea,ar' will swap every e->a and a->e "
              "(simultaneously), and then every a->r and r->a."))


def calc_observed_freq(data):
    counts = plaintext.count_letters(data)
    n = float(sum(counts.values()))
    return {k: c / n for k, c in counts.items()}


def generate_observed_order(observed_freq):
    return sorted(observed_freq, key=observed_freq.get, reverse=True)


def generate_lang_order(lang_freq):
    return sorted(lang_freq, key=lang_freq.get, reverse=True)


class SubMapSearch:
    def __init__(self, data, observed_freq, lang_freq):
        self.data = data
        self.best = 0
        self.plaintexts = []

        self.observed_freq = observed_freq
        self.lang_freq = lang_freq
        self.lang_order = generate_lang_order(lang_freq)

        self.seen = set()


def analyze_order(words, s, letter_order, depth):
    letter_map = {k: v for k, v in zip(letter_order, s.lang_order)}
    pt = "".join([
        letter_map[c.lower()] if c in string.ascii_letters else c
        for c in s.data
    ])

    num_words = plaintext.count_words(words, pt)
    if num_words > s.best:
        s.best = num_words
        s.plaintexts.append(pt)

    if depth == 0:
        return

    for i in range(0, 18):
        new_order = list(letter_order)
        new_order[i], new_order[i + 1] = new_order[i + 1], new_order[i]
        if "".join(new_order) not in s.seen:
            s.seen.add("".join(new_order))
            analyze_order(words, s, new_order, depth - 1)


def substitute(data, r1, r2):
    """Swap two characters in the text with each other.

    Args:
        data: The text.
        r1: The first char.
        r2: The second char.
    
    Returns:
        The text with the characters swapped.
    """
    swap = {r1: r2, r2: r1}
    return "".join([swap.get(c, c) for c in data])


def replace(data, replacements):
    """Swap a list of character pairs in the text.

    Args:
        data: The text.
        replacements: An list of tuples containing characters.

    Returns:
        The text with the swaps done.
    """
    result = data
    for r1, r2 in replacements:
        result = substitute(result, r1, r2)
    return result


def bruteforce(data, depth, letter_depth=18, lang=io.DEFAULT_LANG):
    """Recover the plaintext from a ciphertext using a letter
    substitution map.

    The initial solution orders the observed frequences according
    to the language letter frequencies. Subsequently letters are
    swapped according to a breadth first search.

    Solutions are checked for words, and added to the returned list
    if the number of words found is greater than what has been found
    up until that point.

    Args:
        data: The ciphertext.
        depth: The depth of the breadth first search.
        letter_depth: The number of most frequent letters to swap.
        lang: The language of the plaintext.

    Returns:
        An ordered list of plausible substitution maps.
    """
    observed_freq = calc_observed_freq(data)
    lang_freq = plaintext.load_freqs(lang)
    search = SubMapSearch(data, observed_freq, lang_freq)

    observed_order = generate_observed_order(observed_freq)
    search.seen.add("".join(observed_order))

    words = dictionary.load(lang=lang)
    analyze_order(words, search, observed_order, depth)

    return list(reversed(search.plaintexts))


def submap(data, args):
    if args.replace:
        replacements = args.replace.split(",")
        if any(len(r) != 2 for r in replacements):
            parser.error("--replace arg must be exactly two chars")
        replacements = list(map(list, replacements))
        pt = replace(data, replacements)
        print(pt, end="")
    else:
        pts = bruteforce(data,
                         depth=args.depth,
                         letter_depth=args.letter_depth,
                         lang=args.language)
        print(pts[0], end="")
