#!/usr/bin/env python
"""Dictionary tools."""

from lib import io


def define_arguments(parser):
    parser.set_defaults(func=dictionary)


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

    result = test(data, dictionary)
    print("true") if result else print("false")
