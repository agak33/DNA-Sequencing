
import random

ALLOWED_CHARS = ['A', 'T', 'G', 'C']


def generate_instance(word_len: int,
                      sequence_len: int,
                      allow_repetitions: bool = False,
                      max_r: int = 92) -> [list[str], int]:
    """Returns oligonucleotide list"""
    seed: str = ''.join([random.choice(ALLOWED_CHARS) for _ in range(word_len)])
    result = [seed]
    repetitions: int = 0
    no_no = False
    for _ in range(sequence_len - word_len):
        new_word = result[-1][1:] + random.choice(ALLOWED_CHARS)

        if not allow_repetitions or repetitions >= max_r or no_no:
            while new_word in result:
                new_word = result[-1][1:] + random.choice(ALLOWED_CHARS)
            no_no = False
        else:
            new_word = list(filter(lambda word: word[:-1] == result[-1][1:], result))
            if not new_word:
                new_word = result[-1][1:] + random.choice(ALLOWED_CHARS)
                while new_word in result:
                    new_word = result[-1][1:] + random.choice(ALLOWED_CHARS)
            else:
                new_word = random.choice(new_word)
                no_no = True

        if new_word in result:
            repetitions += 1
        else:
            result.append(new_word)
    return result, repetitions


def random_remove(words_list: list[str], to_delete: int) -> list[str]:
    """Deletes randomly elements from list"""
    for _ in range(to_delete):
        words_list.pop(random.randint(0, len(words_list) - 1))
    return words_list


def random_addons(words_list: list[str], to_add: int, to_add_and_change: int) -> list[str]:
    """Inserts random words into the oligonucleotide list"""
    for _ in range(to_add_and_change):
        word = random.choice(words_list)
        while word in words_list:
            word = random.choice(ALLOWED_CHARS) + word[1:-1] + random.choice(ALLOWED_CHARS)
        words_list.append(word)

    for _ in range(to_add):
        word = ''.join([random.choice(ALLOWED_CHARS) for _ in range(len(words_list[0]))])
        while word in words_list:
            word = ''.join([random.choice(ALLOWED_CHARS) for _ in range(len(words_list[0]))])
        words_list.append(word)

    return words_list

