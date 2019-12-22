#!/usr/bin/env python

"""Dictionary tools.

Usage:
See the --help option for usage information.
"""

import argparse

from lib import io

parser = argparse.ArgumentParser(description="dictionary tools")
parser.add_argument("command", metavar="COMMAND",
                    help="the command to run. currently supported commands include: test, search")
parser.add_argument("file", metavar="FILE", nargs="?",
                    help="the file (string) to test")
parser.add_argument("-l", "--language", type=str, default=io.DEFAULT_LANG,
                    help="the language being analyzed, in ISO 639-1 (default: en)")


def load(lang=io.DEFAULT_LANG, filepath=None):
    """Load the specified language's dictionary.

    Args:
        lang: The optional language (default: en).
        filepath: Specify the flle to load.

    Returns:
        A set containing each of the words in the file.
    """
    if not filepath:
        filepath = io.get_lang_filepath("all_words", lang)

    data = io.read_file(filepath, lines=True)
    dictionary = set()
    for line in data:
        word = line.strip().lower().replace('-', '').replace(' ', '')
        dictionary.add(word)

    return dictionary


def test(word, dictionary):
    """Test a word's membership in the dictionary.

    Args:
        word: The word to test.
        dictionary: The dictionary to test in.

    Returns:
        A boolean specifying whether the word is in the dictionary or not.
    """
    return True if word.strip() in dictionary else False


def dictionary(data, args):
    dictionary = load(lang=args.language)

    if args.command == "test":
        result = test(data, dictionary)
        print("true") if result else print("false")
    else:
        parser.error("%s command not recognized")


def main():
    args, data = io.parse_args(parser)
    dictionary(data, args)


if __name__ == "__main__":
    main()
