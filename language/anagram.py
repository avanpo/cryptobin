import itertools
import string

from language import dictionary


def define_arguments(parser):
    parser.set_defaults(func=anagram)
    parser.add_argument("-w",
                        "--words",
                        type=int,
                        default=1,
                        help="the max number of words in the anagram")
    parser.add_argument("-u",
                        "--unknown",
                        type=int,
                        default=0,
                        help="the number of unknown letters")
    parser.add_argument("-s",
                        "--subsets",
                        action="store_true",
                        default=False,
                        help="also search subsets")


def load_anagrams(lang=dictionary.DEFAULT_LANG):
    """Get a dictionary of sorted strings to list of anagrams."""
    words = dictionary.load(lang=lang)
    anagrams = {}
    for w in words:
        # Don't include non-alpha words.
        if not w.isalpha():
            continue
        sw = "".join(sorted([i.lower() for i in w]))
        if sw in anagrams:
            anagrams[sw].append(w)
        else:
            anagrams[sw] = [w]
    return anagrams


def search(anagrams, partial, unknown):
    """Search anagrams for possible matches with a number of unknown."""
    sols = set()
    for letters in map(
            "".join,
            itertools.combinations_with_replacement(string.ascii_lowercase,
                                                    unknown)):
        sorted_str = "".join(sorted(partial + letters))
        if sorted_str in anagrams:
            sols.add(sorted_str)
    return sols


def search_subsets(anagrams, data):
    """Search anagrams for possible subset matches."""
    sols = set()
    for s in itertools.chain.from_iterable(
            itertools.combinations(sorted(data), r)
            for r in range(len(data) + 1, 1, -1)):
        # itertools.combinations keeps the order of the input, so this output
        # is sorted.
        sorted_str = "".join(s)
        if sorted_str in anagrams:
            sols.add(sorted_str)
    return sorted(sols, key=lambda x: (-len(x), x))


def multi_word_search(anagrams, data, num_words):
    """Search anagrams for multi-word matches."""
    match = "".join(sorted(data))
    sub_sols = search_subsets(anagrams, data)

    sols = []
    for candidates in itertools.combinations(sub_sols, num_words):
        uberstr = "".join(sorted("".join(candidates)))
        if uberstr == match:
            sols.append(candidates)
    return sols


def anagram(data, args):
    data = "".join(data.split())
    anagrams = load_anagrams(lang=args.language)

    if args.words == 1:
        if args.subsets:
            if args.unknown != 0:
                raise NotImplementedError
            sols = search_subsets(anagrams, data)
        else:
            sols = search(anagrams, data, args.unknown)
        print("=> possible anagrams:")
        for s in sols:
            words = ",".join(anagrams[s])
            print(f"{s}: {words}")
    elif args.words > 1:
        if args.unknown != 0 or args.subsets:
            raise NotImplementedError
        multi_sols = multi_word_search(anagrams, data, args.words)
        print("=> possible anagrams:")
        for ss in multi_sols:
            groups = " ".join(ss)
            words = " ".join(
                map(lambda x: ",".join(x), (anagrams[s] for s in ss)))
            print(f"{groups}: {words}")
