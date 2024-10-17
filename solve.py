from tqdm import tqdm
import nltk
from wordfreq import zipf_frequency
from english_words import get_english_words_set
nltk.download('words', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('brown', quiet=True)
nltk.download('treebank', quiet=True)
# nltk.download()


def no_double_letters(word):
    for i in range(len(word)-1):
        if word[i] == word[i+1]:
            return False
    return True


def is_lowercased(word):
    return word[0].islower()


def is_valid_letter_set(word):
    return set(word).issubset(puzzle_set)


def is_somewhat_common_word(word):
    return zipf_frequency(word=word, lang="en") > 0.0


# puzzle = ["veo", "ims", "cap", "frn"]
# puzzle = ["kih", "tym", "rzl", "bau"]
# puzzle = ["mna", "leu", "pig", "xdw"]
# puzzle = ["bhr", "eav", "lct", "niu"]
# puzzle = ["ohp", "cdr", "tnu", "aij"]
# puzzle = ["hif", "mel", "but", "ard"]
# puzzle = ["yhi", "ucs", "qtl", "daf"]
# puzzle = ["nlb", "kge", "uro", "wca"]
# puzzle = ["bsa", "zru", "eit", "gko"]
# puzzle = ["osv", "ier", "lhw", "ynt"]
# puzzle = ["jxz", "uel", "oin", "rca"]
# puzzle = ["inc", "lwt", "ous", "par"]
# puzzle = ["lin", "ade", "htb", "ucr"]
# puzzle = ["iel", "cgn", "vra", "tyo"]
# puzzle = ["enr", "tbl", "aoi", "pxs"]
# puzzle = ["uta", "mln", "cwi", "ozr"]
# puzzle = ["ced", "inr", "hva", "ktu"]
# puzzle = ["tay", "nsm", "pxo", "jke"]
# puzzle = ["fhi", "wrt", "nko", "gls"]
# puzzle = ["tzn", "lea", "roh", "ypb"]
# puzzle = ["ubl", "set", "xma", "ior"]
puzzle = ["tap", "eio", "lmv", "xnu"]

puzzle_str = "".join(puzzle)
puzzle_set = set(puzzle_str)
puzzle_dict = {}
for side in puzzle:
    i = puzzle.index(side)
    for letter in side:
        puzzle_dict[letter] = i

# web2lowerset = get_english_words_set(['web2'])

# nltk_words = map(lambda x: x, nltk.corpus.wordnet.words())
nltk_words = set(nltk.corpus.words.words()).union(
    nltk.corpus.wordnet.words(),
    nltk.corpus.brown.words(),
    nltk.corpus.treebank.words(),
    get_english_words_set(['web2'])
)
nltk_words_lower = filter(is_lowercased, nltk_words)
words = filter(no_double_letters, nltk_words_lower)
word_set_valid = filter(is_valid_letter_set, words)
word_set = set(filter(is_somewhat_common_word, word_set_valid))

possible_solutions = []
for a in tqdm(word_set):
    a_len = len(a)
    for b in word_set:
        if a[-1] != b[0]:
            continue
        if a_len + len(b) <= 12:
            continue
        if set(a + b) == puzzle_set:
            possible_solutions.append([a, b])

good_solutions = []
for possible_solution in tqdm(possible_solutions):
    is_good_solution = True
    for word in possible_solution:
        prev_side_index = -1
        for letter in word:
            side_index = puzzle_dict[letter]
            if side_index == prev_side_index:
                is_good_solution = False
                break
            prev_side_index = side_index
        if not is_good_solution:
            break
    if is_good_solution:
        good_solutions.append(possible_solution)

good_solutions.sort(key=lambda s: zipf_frequency(
    s[0], "en") + zipf_frequency(s[1], "en"), reverse=False)

for good_solution in good_solutions:
    print(good_solution, zipf_frequency(
        good_solution[0], "en") + zipf_frequency(
        good_solution[1], "en"))
print(f"{len(good_solutions)} solutions found!")
