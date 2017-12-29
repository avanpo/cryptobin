# cryptobin

A suite of crypto and puzzle tools. The project aims to provide utils that can be imported as python modules to quickly solve unique problems, but also be used on the command line.

### tools

* **plaintext.py** [-h] [-l LANGUAGE] [-d DICTIONARY] COMMAND [FILE]
  * plaintext.py fa, frequency analysis
  * plaintext.py wc, approximate language word count
* **rot.py** [-h] [-k KEY] [-n NUMBER] [-l LANGUAGE] [FILE]
  * plaintext.py, brute force the plaintext, based on frequency analysis
  * plaintext.py -k 13, rotate text by a given key
