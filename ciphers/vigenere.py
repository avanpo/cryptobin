"""Vigenere cipher utilities.

Background:

A Vigenere cipher is a polyalphabetic substitution cipher, meaning that one
character may map to many other characters. The Vigenere cipher works by using a
repeating key of a certain length, which is used to rotate each character in the
plaintext. For example, one can encrypt the following plaintext using the key
'ZEBRA':

    plaintext:  A T T A C K A T D A W N
    key:        Z E B R A Z E B R A Z E
    -----------------------------------
    ciphertext: Z X U R C J E U U A V R

The repeating nature of the key makes this cipher easy to break. For a key of
length 5, every fifth letter will be rotated using the same letter, just like
the Caesar cipher, which is easy to break using frequency analysis. Thus the
Vigenere cipher can be seen as multiple interwoven Caesar ciphers, each with a
different key.

Breaking the Vigenere cipher is therefore simply a matter of unweaving these
Caesar ciphers, breaking them individually, and putting the results back
together. If the length of the key is not known, this needs to be done for every
possible key length. This is what this tool does. To be effective, a
sufficiently large ciphertext needs to be provided.
"""

import string

from ciphers import rot
from language import dictionary
from language import words


def define_arguments(parser):
    parser.set_defaults(func=vigenere, lines=True)
    parser.add_argument("-i",
                        "--min-length",
                        type=int,
                        default=2,
                        help="the minimum key length to try (default: 2)")
    parser.add_argument("-m",
                        "--max-length",
                        type=int,
                        default=10,
                        help="the maximum key length to try (default: 10)")
    parser.add_argument("-k",
                        "--key",
                        action="store_true",
                        help="recover the encryption key")
    parser.add_argument("-n",
                        "--number",
                        type=int,
                        default=1,
                        help="number of results to show (default: 1)")


def strstrip(data):
    return "".join([i for i in data if i in string.ascii_letters])


def stagger_split(data, l):
    output = [""] * l
    for line in data:
        for i, c in enumerate(line):
            output[i % l] += c
    return output


def stagger_join(data, parts):
    output = []
    indexes = [0] * len(parts)
    for line in data:
        i = len(line)
        while i > 0:
            for j, p in enumerate(parts):
                if i == 0:
                    break
                output.append(p[indexes[j]])
                indexes[j] += 1
                i -= 1
        output.append("\n")
    return "".join(output)


def bruteforce(data,
               min_length=2,
               max_length=10,
               lang=dictionary.DEFAULT_LANG):
    """Attempt to bruteforce the solution to a Vigenere ciphertext.

    This is done by trying every key length. Whitespace and all punctuation are
    ignored, only letter positions relative to each other are used.

    Newlines are assumed to 'reset' the key.

    Args:
        data: The ciphertext to be analyzed.
        min_length: The min length of the key.
        max_length: The max length of the key.
        lang: The language of the plaintext.

    Returns:
        A list of the most likely plaintexts for each key length.
    """
    data = [strstrip(line) for line in data]
    words = dictionary.load(lang=lang)

    sols = []
    for i in range(min_length, max_length + 1):
        split = stagger_split(data, i)
        parts = []
        key = []
        for s in split:
            part_sols = rot.bruteforce(s, lang=lang)
            parts.append(part_sols[0])
            key_char = chr((26 + ord(s[0]) - ord(part_sols[0][0])) % 26 + 65)
            key.append(key_char)
        sol = stagger_join(data, parts)
        wc = words.count_words(words, sol)
        sols.append((sol, "".join(key), wc))

    return [(s, k)
            for s, k, wc in sorted(sols, key=lambda x: x[2], reverse=True)]


def vigenere(data, args):
    sols = bruteforce(data,
                      args.min_length,
                      args.max_length,
                      lang=args.language)
    if args.key:
        for sol in sols[:args.number]:
            print(sols[0][1])
    else:
        for sol in sols[:args.number]:
            print(sols[0][0], end="")
