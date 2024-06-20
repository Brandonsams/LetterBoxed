from tqdm import tqdm
import nltk
from wordfreq import word_frequency, zipf_frequency


def no_double_letters(word):
    for i in range(len(word)-1):
        if word[i] == word[i+1]:
            return False
    return True


nltk.download('words')
nltk_words = map(lambda x: x.lower(), nltk.corpus.words.words())
words = list(filter(no_double_letters, nltk_words))


# words = []
# with open("words.txt") as f:
#     for line in f.readlines():
#         word = line.replace("\n", "")
#         if not double_letters(word=word):
#             words.append(word)

puzzle = ["veo", "ims", "cap", "frn"]
puzzle_str = "".join(puzzle)
puzzle_set = set(puzzle_str)
puzzle_dict = {}
for side in puzzle:
    i = puzzle.index(side)
    for letter in side:
        puzzle_dict[letter] = i


def is_valid_letter_set(word):
    return set(word).issubset(puzzle_set)


word_set = list(filter(is_valid_letter_set, words))


def is_somewhat_common_word(word):
    return zipf_frequency(word=word, lang="en") > 0.0


word_set = list(filter(is_somewhat_common_word, word_set))

possible_solutions = []
for a in tqdm(word_set):
    for b in word_set:
        if a[-1] != b[0]:
            continue
        if set(a + b) == puzzle_set:
            possible_solutions.append([a, b])

# possible_solutions = [["voices","semiprofane"]]
good_solutions = []
for possible_solution in possible_solutions:
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
    s[0], "en") + zipf_frequency(s[1], "en"))

for good_solution in good_solutions:
    print(good_solution, zipf_frequency(
        good_solution[0], "en") + zipf_frequency(
        good_solution[1], "en"))

print(f"{len(good_solutions)} solutions found!")
