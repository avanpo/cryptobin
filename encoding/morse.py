"""Morse code utilities."""

from lib import io


def define_arguments(parser):
    parser.set_defaults(func=morse)
    parser.add_argument("-m",
                        "--lower",
                        action="store_true",
                        default=False,
                        help="output lower case (default: upper)")


MORSE = {
    "01": "A",
    "1000": "B",
    "1010": "C",
    "100": "D",
    "0": "E",
    "0010": "F",
    "110": "G",
    "0000": "H",
    "00": "I",
    "0111": "J",
    "101": "K",
    "0100": "L",
    "11": "M",
    "10": "N",
    "111": "O",
    "0110": "P",
    "1101": "Q",
    "010": "R",
    "000": "S",
    "1": "T",
    "001": "U",
    "0001": "V",
    "011": "W",
    "1001": "X",
    "1011": "Y",
    "1100": "Z",
    "01111": "1",
    "00111": "2",
    "00011": "3",
    "00001": "4",
    "00000": "5",
    "10000": "6",
    "11000": "7",
    "11100": "8",
    "11110": "9",
    "11111": "0",
}


def translate_to_text(data, lower=False):
    """Translate a string containing 0s (dots) and 1s (dashes) to text.

    Any other characters encountered are assumed to divide the code points.
    """
    text = []
    code_point = []
    for i in (data + ' '):
        if i == "0" or i == "1":
            code_point.append(i)
            continue
        if not code_point:
            continue
        text.append(MORSE["".join(code_point)])
        code_point.clear()
    if code_point:
        text.append(MORSE["".join(code_point)])

    if lower:
        return "".join(text).lower()
    return "".join(text)


def morse(data, args):
    text = translate_to_text(data, args.lower)
    print(text)
