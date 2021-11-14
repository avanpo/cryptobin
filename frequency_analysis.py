#!/usr/bin/env python

import plaintext


def define_arguments(parser):
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
        help="restrict to printing double digrams (e.g. 'ee')",
    )


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
        print("   %3s (%.4f)  | %3s (%.4f)" %
              (o, observed_freq[o], l, lang_freq[l]))
        rows += 1
        if rows > 30:
            break
    for l in lang[rows:30]:
        print("                 | %3s (%.4f)" % (l, lang_freq[l]))


def fa(data, args):
    if args.doubles and args.ngram != 2:
        raise ValueError(
            "--doubles (restricting to double digrams) requires --ngram=2")

    observed_freq = plaintext.ngram_frequencies(data, n=args.ngram)
    lang_freq = plaintext.load_freqs(args.language, n=args.ngram)
    print_fa(observed_freq, lang_freq, doubles=args.doubles)
