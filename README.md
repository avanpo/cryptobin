# cryptobin

A suite of classical crypto and puzzle tools.

The project aims to provide utils that can be imported as python modules to
quickly solve unique problems, but also be used on the command line via
cryptobin.py.

## use

```
usage: cryptobin.py [-h] [-l LANGUAGE] SUBCOMMAND ... [FILE]

cryptobin cli tool.

positional arguments:
  SUBCOMMAND
    anagram             anagram utilities
    bifid               bifid cipher utilities
    count               character counting
    enc                 character encoding transformations
    fa                  frequency analysis
    int                 integer sequence analysis
    morse               morse encoding utilities
    playfair            playfair cipher utilities
    roman               roman numeral encoding utilities
    rot                 text rotation (e.g. ROT13) utilities
    submap              substitution cipher utilities
    tonal               tonal encoding utilities
    vigenere            vigenere cipher utilities
    words               word utilities
  FILE                  the input to be processed

optional arguments:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language LANGUAGE
                        the language being analyzed, in ISO 639-1 (default:
                        en)
```

## tests

In the root directory, run:

```
python -m unittest
```
