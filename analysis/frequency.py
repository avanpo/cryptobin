"""Char analysis."""

import collections
import string

from lib import io


def define_arguments(parser):
    parser.set_defaults(func=fa)
    parser.add_argument(
        "-n",
        "--ngram",
        type=int,
        default=1,
        help="size of letter groups to analyze (default: 1)",
    )
    parser.add_argument(
        "-d",
        "--doubles",
        action="store_true",
        default=False,
        help="restrict to double digrams (e.g. 'ee'). requires ngram=2.",
    )


def count_chars(data):
    """Returns a dictionary of char to count."""
    counts = collections.defaultdict(int)
    for c in data:
        counts[c] += 1
    return counts


def count_letters(data):
    """Returns a dictionary of lowercase letter to count."""
    counts = count_chars(data)
    return {l: counts[l] + counts[l.upper()] for l in string.ascii_lowercase}


def letter_ngram_frequencies(data, n=1):
    """Returns a dictionary of lowercase letter n-gram to frequency."""
    data = data.lower()
    letters = set(string.ascii_lowercase)

    num_ngrams = 0
    result = collections.defaultdict(int)
    for i in range(0, len(data) - n + 1):
        if data[i] not in letters:
            continue
        ngram = [data[i]]
        for j in range(i + 1, len(data)):
            if len(ngram) == n:
                break
            if data[j] in letters:
                ngram.append(data[j])
        if len(ngram) == n:
            num_ngrams += 1
            result["".join(ngram)] += 1

    return {k: v / num_ngrams for k, v in result.items()}


def load_frequencies(lang=io.DEFAULT_LANG, n=1):
    filepath = io.get_lang_filepath("freq", lang)
    if n == 2:
        filepath = io.get_lang_filepath("digram_freq", lang)

    data = io.read_file(filepath, lines=True)
    freqs = {}
    for line in data:
        c, val = line.strip().split()
        freqs[c] = float(val)

    return freqs


def print_fa(observed_freq, lang_freq, doubles=False):
    print("=> Calculated letter frequencies")
    print("   Observed      | Language")
    print("   --------------+-------------")
    observed = sorted(observed_freq, key=observed_freq.get, reverse=True)
    lang = sorted(lang_freq, key=lang_freq.get, reverse=True)
    if doubles:
        observed = list(
            filter(lambda s: len(s) == 2 and s[0] == s[1], observed))
        lang = list(filter(lambda s: len(s) == 2 and s[0] == s[1], lang))
    rows = 0
    for o, l in zip(observed, lang):
        print(f"   {o:3} ({observed_freq[o]:.4})  | {l:3} ({lang_freq[l]:.4})")
        rows += 1
        if rows > 30:
            break
    for l in lang[rows:30]:
        print(f"                 | {l:3} ({lang_freq[l]:.4})")


def fa(data, args):
    if args.doubles and args.ngram != 2:
        raise ValueError(
            "--doubles (restricting to double digrams requires --ngram=2")

    observed_freq = letter_ngram_frequencies(data, n=args.ngram)
    lang_freq = load_frequencies(args.language, n=args.ngram)
    print_fa(observed_freq, lang_freq, doubles=args.doubles)
