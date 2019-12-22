#!/usr/bin/env python

"""Playfair cipher utilities."""

import argparse
import string
import sys

import plaintext
from lib import io

parser = argparse.ArgumentParser(description=(
    "playfair cipher utilities."))
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")
parser.add_argument("-k", "--key", type=str,
                    help="the cipher key")
parser.add_argument("-d", "--decrypt", action="store_true", default=False,
                    help="decrypt instead of encrypt")
parser.add_argument("-l", "--language", type=str, default=io.DEFAULT_LANG,
                    help="the language being analyzed, in ISO 639-1 (default: en)")


def build_maps(key):
    """Build the substitution map used by the Playfair cipher.

    Args:
        key: The key in human readable form.

    Returns:
        A tuple of maps. The first maps letters to coordinates, the second maps
        coordinates to letters.
    """
    row, col = 0, 0
    coords, letters = {}, {}

    key = key.lower() + string.ascii_lowercase
    leftover = set(string.ascii_lowercase)
    for l in key:
        if l == "j":  # treat "j" in key as "i"
            l = "i"
        if l in leftover:
            coords[l] = (row, col)
            letters[(row, col)] = l
            if l == "i":
                coords["j"] = (row, col)
            leftover.remove(l)
        else:
            continue
        # increment coords
        col += 1
        if col == 5:
            col = 0
            row += 1
    if row != 5 and col != 0:
        raise RuntimeError("Key did not turn into 5x5 table.")
    return coords, letters


def encrypt_digram(coords, letters, digram, decrypt=False):
    """Encrypt digram using the Playfair cipher."""
    x1, y1 = coords[digram[0]]
    x2, y2 = coords[digram[1]]
    if x1 == x2:  # same row
        if decrypt:
            c1 = letters[(x1, (y1 - 1) % 5)]
            c2 = letters[(x2, (y2 - 1) % 5)]
        else:
            c1 = letters[(x1, (y1 + 1) % 5)]
            c2 = letters[(x2, (y2 + 1) % 5)]
    elif y1 == y2:  # same column
        if decrypt:
            c1 = letters[((x1 - 1) % 5, y1)]
            c2 = letters[((x2 - 1) % 5, y2)]
        else:
            c1 = letters[((x1 + 1) % 5, y1)]
            c2 = letters[((x2 + 1) % 5, y2)]
    else:
        c1 = letters[(x1, y2)]
        c2 = letters[(x2, y1)]
    return c1 + c2


def encrypt(key, text, decrypt=False, uncommon="x"):
    """Encrypt text using the Playfair cipher.

    Args:
        key: The key in human readable form.
        text: The plaintext or ciphertext.

    Returns:
        The encrypted form of the input.
    """
    coords, letters = build_maps(key)
    pair = ""
    output = []
    for c in text.lower():
        # Ignore non-alpha characters.
        if c not in string.ascii_lowercase:
            output.append(c)
            continue
        # Continue if digram not complete.
        if len(pair) == 0:
            pair = c
            continue

        if c == pair:  # Insert uncommon letter for repeated digram.
            pair += uncommon.lower()
            new_pair = c
        else:
            pair += c
            new_pair = ""

        output.append(encrypt_digram(coords, letters, pair, decrypt))
        pair = new_pair

    # Pad input if required.
    if len(pair) > 0:
        pair += uncommon.lower()
        output.append(encrypt_digram(coords, letters, pair, decrypt))

    return "".join(output)


def playfair(data, args):
    data = data.strip()
    if args.decrypt:
        print(encrypt(args.key, data, decrypt=True))
    else:
        print(encrypt(args.key, data, decrypt=False))


def main():
    args, data = io.parse_args(parser)
    playfair(data, args)


if __name__ == "__main__":
    main()
