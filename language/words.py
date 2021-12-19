import re

from language import dictionary


def define_arguments(parser):
    parser.set_defaults(func=words)


def words(data, args):
    p = re.compile(data.strip())

    for w in dictionary.load(args.language):
        if p.search(w):
            print(w)
