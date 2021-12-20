import re

from language import dictionary


def define_arguments(parser):
    parser.set_defaults(func=words)


def count_words(words, data, n=4, verbose=False):
    """Calculate the approximate number of n+ letter words in a text.

    This function is not accurate, as it has been designed for texts with all
    punctuation and spacing removed. It does not properly handle conjugation
    or spacing. It should, however, be good enough for basic cryptanalysis.
    """
    data = "".join(data.split()).lower()
    count = 0
    i = 0
    while i < len(data):
        for l in range(min(11, len(data) - i), n - 1, -1):
            if data[i:i + l] in words:
                count += 1
                if verbose:
                    print(">", data[i:i + l])
                i += l - 1
                break
        i += 1
    return count


def words(data, args):
    p = re.compile(data.strip())

    for w in dictionary.load(args.language):
        if p.search(w):
            print(w)
