"""Character counting util."""

import collections
import string


def define_arguments(parser):
    parser.set_defaults(func=counts)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="print all character counts (default: false)",
    )


def count_chars(data):
    """Returns a dictionary of char to count."""
    counts = collections.defaultdict(int)
    for c in data:
        counts[c] += 1
    return counts


def counts_summary(data):
    la, ua, nr, p, w, np = 0, 0, 0, 0, 0, 0
    for c in data:
        if c in string.ascii_lowercase:
            la += 1
        elif c in string.ascii_uppercase:
            ua += 1
        elif c in string.digits:
            nr += 1
        elif c in string.punctuation:
            p += 1
        elif c in string.whitespace:
            w += 1
        else:
            np += 1
    print("=> Character class counts")
    print("   lalpha | ualpha |  digit |   punc | wspace | nonprint")
    print("   -------+--------+--------+--------+--------+---------")
    print("   %6d | %6d | %6d | %6d | %6d | %8d" % (la, ua, nr, p, w, np))


def counts_all(data):
    counts = count_chars(data)
    count_width = len(str(max(counts, key=counts.get)))

    print("=> Character counts")
    for c, count in sorted(counts.items()):
        representation = c
        if c == "\n":
            representation = "\\n"
        elif c in string.whitespace:
            representation = " "
        print(
            f"   {representation:>2}: {count:>{count_width}}   [{ord(c):08x}]")


def counts(data, args):
    if args.verbose:
        counts_all(data)
    else:
        counts_summary(data)
