#!/usr/bin/env python

### DRAFT

import argparse
import itertools
import string
import sys

import dictionary
from lib import io

parser = argparse.ArgumentParser(description="word build util")
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file (anagram) to test")
parser.add_argument("-s", "--size", type=int, default=3,
                    help="the length of the word"
                    "en)")
parser.add_argument("-l", "--language", type=str, default=io.DEFAULT_LANG,
                    help="the language being analyzed, in ISO 639-1 (default: "
                    "en)")


def build_words(size=3, hints={}, lang=io.DEFAULT_LANG):
    words = dictionary.load(lang=lang)
    for i in range(0, size):



def build(data, args):
    data = "".join(data.split())
    anagrams = load_anagrams(lang=args.language)

    sols = search_anagrams(anagrams, data, args.unknown)
    print("=> possible anagrams:")
    for s in sols:
        print("%s: %s" % (s, ",".join(anagrams[s])))


def main():
    args, data = io.parse_args(parser)
    build(data, args)


if __name__ == "__main__":
    main()
