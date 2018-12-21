#!/usr/bin/env python

import argparse
import itertools
import string
import sys

import dictionary
from lib import io

parser = argparse.ArgumentParser(description="anagram search util")
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file (anagram) to test")
parser.add_argument("-w", "--words", type=int, default=1,
                    help="the max number of words in the anagram")
parser.add_argument("-u", "--unknown", type=int, default=0,
                    help="the number of unknown letters")
parser.add_argument("-l", "--language", type=str, default=io.DEFAULT_LANG,
                    help="the language being analyzed, in ISO 639-1 (default: "
                    "en)")


def load_anagrams(lang=io.DEFAULT_LANG):
    words = dictionary.load(lang=lang)
    anagrams = {}
    for w in words:
        sw = "".join(sorted([i.lower() for i in w if i.isalpha()]))
        if sw in anagrams:
            anagrams[sw].append(w)
        else:
            anagrams[sw] = [w]
    return anagrams


def search_anagrams(anagrams, partial, unknown):
    sols = []
    for letters in map("".join, itertools.product(string.ascii_lowercase,
                                                  repeat=unknown)):
        sorted_str = "".join(sorted(partial + letters))
        if sorted_str in anagrams:
            sols.append(sorted_str)
    return sols


def anagram(data, args):
    data = "".join(data.split())
    anagrams = load_anagrams(lang=args.language)

    sols = search_anagrams(anagrams, data, args.unknown)
    print("=> possible anagrams:")
    for s in sols:
        print("%s: %s" % (s, ",".join(anagrams[s])))


def main():
    args, data = io.parse_args(parser)
    anagram(data, args)


if __name__ == "__main__":
    main()
