import os
import sys

DEFAULT_LANG = "en"


def get_lang_filepath(prefix, lang):
    lib_dir = os.path.dirname(__file__)
    return os.path.join(lib_dir, "../lang/%s_%s.txt" % (prefix, lang))


def read_file(filepath, lines=False, encoding="UTF-8"):
    try:
        with open(filepath) as f:
            if lines:
                return f.readlines()
            else:
                return f.read()
    except EnvironmentError:
        print("=> ERROR: Could not open %s." % filepath)
        sys.exit()


def parse_args(parser, need_file=True):
    args = parser.parse_args()

    # Some utilities want to read files as lines rather than a blob. They can
    # do this by setting a default arg for 'lines'.
    lines = False
    if hasattr(args, "lines"):
        lines = args.lines

    if args.file:
        data = read_file(args.file, lines)
    elif not sys.stdin.isatty():
        if lines:
            data = sys.stdin.readlines()
        else:
            data = sys.stdin.read()
    elif need_file:
        parser.error("no input file found")
    else:
        data = ""

    return args, data


def parse_args_multiple_files(parser):
    args = parser.parse_args()
    if len(args.files) < 2:
        parser.error("not enough input files")

    data = [read_file(filepath) for filepath in args.files]
    return args, data


def parse_list(data, sep=None):
    """Parse input into a list of strings.

    Uses newlines, spaces and commas as separators.

    Args:
        data: Input string

    Returns:
        List of nonempty strings.
    """
    split = data.strip().replace("\n", ",").replace(" ", ",").split(",")
    return [s.strip() for s in split if s.strip()]


def parse_int_list(data):
    """Parse input into a list of ints."""
    return [int(s) for s in parse_list(data)]
