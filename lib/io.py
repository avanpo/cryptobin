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
    
    
def parse_args(parser, lines=False):
    args = parser.parse_args()
    if args.file:
        data = read_file(args.file, lines)
    elif not sys.stdin.isatty():
        if lines:
            data = sys.stdin.readlines()
        else:
            data = sys.stdin.read()
    else:
        parser.error("no input file found")

    return args, data


def parse_args_multiple_files(parser):
    args = parser.parse_args()
    if len(args.files) < 2:
        parser.error("not enough input files")

    data = [read_file(filepath) for filepath in args.files]
    return args, data