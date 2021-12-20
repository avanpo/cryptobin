"""Dictionary tools."""

import os

from lib import io

DEFAULT_LANG = "en"


def get_lang_filepath(prefix, lang):
    return os.path.join(io.get_data_filepath(), f"{prefix}_{lang}.txt")


def load(lang=DEFAULT_LANG, filepath=None):
    """Load the specified language's dictionary.

    Args:
        lang: The optional language (default: en).
        filepath: Specify the flle to load.

    Returns:
        A set containing each of the words in the file.
    """
    if not filepath:
        filepath = get_lang_filepath("words", lang)

    data = io.read_file(filepath, lines=True)
    d = set()
    for line in data:
        word = line.strip().lower().replace('-', '').replace(' ', '')
        d.add(word)

    return d
