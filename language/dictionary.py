"""Dictionary tools."""

from lib import io


def load(lang=io.DEFAULT_LANG, filepath=None):
    """Load the specified language's dictionary.

    Args:
        lang: The optional language (default: en).
        filepath: Specify the flle to load.

    Returns:
        A set containing each of the words in the file.
    """
    if not filepath:
        filepath = io.get_lang_filepath("words", lang)

    data = io.read_file(filepath, lines=True)
    dictionary = set()
    for line in data:
        word = line.strip().lower().replace('-', '').replace(' ', '')
        dictionary.add(word)

    return dictionary
