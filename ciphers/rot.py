"""Rotation utilities."""

import plaintext
from language import dictionary


def define_arguments(parser):
    parser.set_defaults(func=rot)
    parser.add_argument("-k",
                        "--key",
                        type=int,
                        help="the rotation key (example: 13)")
    parser.add_argument("-n",
                        "--number",
                        type=int,
                        default=3,
                        help="number of results to show (default: 3)")
    parser.add_argument("-c",
                        "--case",
                        type=str,
                        default="all",
                        help="rotate all|lower|upper|numeric case letters "
                        "(default: all)")


def rot_char(c, key, case="all"):
    b = ord(c)
    if 65 <= b <= 90 and case in {"all", "upper"}:
        b = (b - 65 + key) % 26 + 65
    elif 97 <= b <= 122 and case in {"all", "lower"}:
        b = (b - 97 + key) % 26 + 97
    elif 48 <= b <= 57 and case == "numeric":
        b = (b - 48 + key) % 10 + 48
    return chr(b)


def rotate(data, key, case="all"):
    """Rotate the text by a given integer.

    Args:
        data: The text to be rotated.
        key: The integer value to rotate by.
        case: The letter case to rotate.

    Returns:
        The rotated text.
    """
    text = []
    for c in data:
        text += rot_char(c, key, case)
    return "".join(text)


def bruteforce(data, lang=dictionary.DEFAULT_LANG, case="all"):
    """Attempt to recover the plaintext using frequency analysis.

    Args:
        data: The ciphertext to be analyzed.
        lang: The language of the plaintext.
        case: The letter case to rotate.

    Returns:
        A list of all rotations of the text, ordered by standard deviation
        from the language averages.
    """
    sols = []
    for i in range(0, 26):
        text = rotate(data, i, case)
        sols.append((plaintext.std_dev(text, lang), text))

    sols.sort(key=lambda x: x[0])
    return [x[1] for x in sols]


def rot(data, args):
    data = data.strip()
    if args.key:
        output = rotate(data, args.key, args.case)
        print(output)
    else:
        sols = bruteforce(data, args.language, args.case)
        for i in range(0, min(args.number, 26)):
            print(sols[i])
