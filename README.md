# cryptobin

A suite of crypto and puzzle tools. The project aims to provide utils that can be imported as python modules to quickly solve unique problems, but also be used on the command line.

### tools

* **ciphertext.py** [-h] [-l LANGUAGE] COMMAND [FILE]
  * **fa** analyze letter frequency for alpha ciphers
* **plaintext.py** [-h] [-l LANGUAGE] [-d DICTIONARY] COMMAND [FILE]
  * **fa** calculate standard deviation from language letter frequences
  * **wc** approximate word count in plaintext body
* **rot.py** [-h] [-k KEY] [-n NUMBER] [-l LANGUAGE] [FILE]
  * solves the caesar cipher, or rotates text by a given key
* **submap.py** [-h] [-d DEPTH] [-f LETTER_DEPTH] [-l LANGUAGE] [-r REPLACE] [FILE]
  * solves monoalphabetic simple substitution ciphers, or swaps letters
* **vigenere.py** [-h] [-m MAX_LENGTH] [-l LANGUAGE] [FILE]
  * solves vigenere ciphers
