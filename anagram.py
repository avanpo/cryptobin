#!/usr/bin/env python

import argparse
import itertools
import string
import sys

import dictionary
import utils

parser = argparse.ArgumentParser(description="anagram search util")
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file (anagram) to test")
parser.add_argument("-u", "--unknown", type=int, default=0,
                    help="the number of unknown letters")


def load_anagrams():
    words = dictionary.load()
    anagrams = {}
    for w in words:
        sw = "".join(sorted(w))
        if sw in anagrams:
            anagrams[sw].append(w)
        else:
            anagrams[sw] = [w]
    return anagrams


def generate_anagram_prefixes(anagrams, l):
    anagram_prefixes = set()
    for a in anagrams:
        anagram_prefixes.add(a[:l])
    return anagram_prefixes


def search_anagrams(anagrams, partial, unknown):
    sols = []
    for letters in map("".join, itertools.product(string.ascii_lowercase, repeat=unknown)):
        sorted_str = "".join(sorted(partial + letters))
        if sorted_str in anagrams:
            sols.append(sorted_str)
    return sols


def anagram(data, args):
    data = "".join(data.split())
    anagrams = load_anagrams()

    sols = search_anagrams(anagrams, data, args.unknown)
    print("=> possible anagrams:")
    for s in sols:
        print("%s: %s" % (s, " ".join(anagrams[s])))


def main():
    args, data = utils.parse_args(parser)
    anagram(data, args)


if __name__ == "__main__":
    main()
