#!/usr/bin/env python

"""Bifid cipher utilities."""

import argparse
import string

from lib import io

parser = argparse.ArgumentParser(description=(
    "bifid cipher utilities."))
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file to be analyzed")
parser.add_argument("-k", "--key", type=str,
                    help="the cipher key")
parser.add_argument("-d", "--decrypt", action="store_true", default=False,
                    help="decrypt instead of encrypt")


def build_maps(key):
    """Build the substitution square used by the Bifid cipher.

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


def encrypt(key, text, decrypt=False):
    """Encrypt text using the Bifid cipher.

    Args:
        key: The key in human readable form.
        text: The plaintext or ciphertext.
        decrypt: Decrypt instead of encrypt.

    Returns:
        The encrypted form of the input.
    """
    coords, letters = build_maps(key)
    rows, cols = [], []
    # Build two rows of coordinates.
    for c in text.lower():
        if c not in string.ascii_lowercase:
            continue
        c_row, c_col = coords[c]
        rows.append(c_row)
        cols.append(c_col)

    # Combine lists.
    if decrypt:
        z = [x for pair in zip(rows, cols) for x in pair]
        combined = (x for pair in zip(z[: len(z) // 2], z[len(z) // 2 :]) for x in pair)
    else:
        combined = iter(rows + cols)

    output = []
    # Divide into pairs and map back to letters.
    for x in combined:
        output.append(letters[(x, next(combined))])

    return "".join(output)


def bifid(data, args):
    data = data.strip()
    if args.decrypt:
        print(encrypt(args.key, data, decrypt=True))
    else:
        print(encrypt(args.key, data, decrypt=False))


def main():
    args, data = io.parse_args(parser)
    bifid(data, args)


if __name__ == "__main__":
    main()
