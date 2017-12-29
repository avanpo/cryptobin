#!/usr/bin/env python

import argparse
import sys

import plaintext

parser = argparse.ArgumentParser(description=(
    "text rotation util. without the --key argument, this tool uses frequency"
    "analysis to find the plaintext."))
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")
parser.add_argument("-k", "--key", type=int,
                    help="the rotation key (example: 13)")
parser.add_argument("-n", "--number", type=int, default=3,
                    help="number of results to show (default: 3)")
parser.add_argument("-l", "--language", type=str, default=plaintext.DEFAULT_LANG,
                    help="the language being analyzed, in ISO 639-1 (default: en)")


def rot_char(c, key):
    b = ord(c)
    if 65 <= b <= 90:
        b = (b - 65 + key) % 26 + 65
    elif 97 <= b <= 122:
        b = (b - 97 + key) % 26 + 97
    return chr(b)


def rotate(data, key):
    text = []
    for c in data:
        text += rot_char(c, key)
    return "".join(text)


def bruteforce(data, lang=plaintext.DEFAULT_LANG):
    data = "".join(data.split())
    sols = []
    for i in range(0, 26):
        text = rotate(data, i)
        sols.append((plaintext.std_dev(text, lang), text))
    
    sols.sort(key=lambda x: x[0])
    return [x[1] for x in sols]


def rot(data, args):
    if args.key:
        output = rotate(data, args.key)
        print(output, end="")
    else:
        sols = bruteforce(data, args.language)
        for i in range(0, min(args.number, 25)):
            print(sols[i])


def main():
    args = parser.parse_args()
    if args.file:
        with open(args.file) as f:
            data = f.read()
    elif not sys.stdin.isatty():
        data = sys.stdin.read()
    else:
        parser.error("no input found")
    rot(data, args)


if __name__ == "__main__":
    main()
