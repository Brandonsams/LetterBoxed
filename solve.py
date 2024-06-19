from tqdm import tqdm

def double_letters(word):
    for i in range (len(word)-1):
        if word[i] == word[i+1]:
            return True
    return False

words = []
with open("words.txt") as f:
    for line in f.readlines():
        word = line.replace("\n","")
        if not double_letters(word=word):
            words.append(word)
        

puzzle = ["veo","ims","cap","frn"]
puzzle_str = "".join(puzzle)
puzzle_set = set(puzzle_str)

def is_valid_letter_set(word):
    return set(word).issubset(puzzle_set)

word_set = list(filter(is_valid_letter_set, words))

possible_solutions = []
for a in tqdm(word_set):
    for b in word_set:
        if a[-1] != b[0]:
            continue
        if set(a + b) == puzzle_set:
            possible_solutions.append([a,b])

# for possible_solution in possible_solutions:
#     print(possible_solution)
