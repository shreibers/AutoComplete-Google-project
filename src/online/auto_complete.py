
from typing import List, Any
from src.online.load_data import DataFiles
from utils.auxiliary_funcs import init_complete_list, get_score_for_add_delete, \
    get_options_to_change, \
    get_score_for_replace

init = DataFiles()

k = 5


def completions_with_delete(best_k_completions, substring, amount):
    res = []
    len_substring = len(substring)
    complete_list = init_complete_list(best_k_completions)

    for i in range(len_substring):
        indexes_of_sentences = init.sub_sentences.get(substring[:i] + substring[i + 1:])
        if indexes_of_sentences:
            score = get_score_for_add_delete(i, len_substring)
            res += get_options_to_change(init.sentences, indexes_of_sentences, amount, complete_list, score)
    return res


def completions_with_replace(best_k_completions, substring, amount):

    res = []
    len_substring = len(substring)
    complete_list = init_complete_list(best_k_completions)

    for i in range(len_substring):
        for letter in range(ord('a'), ord('z') + 1):
            indexes_of_sentences = init.sub_sentences.get(substring[:i] + chr(letter) + substring[i + 1:])
            if indexes_of_sentences:
                score = get_score_for_replace(i, len_substring)
                res += get_options_to_change(init.sentences, indexes_of_sentences, amount, complete_list, score)

    return res


def completions_with_add(best_k_completions, substring, amount):
    res = []
    len_substring = len(substring)
    complete_list = init_complete_list(best_k_completions)
    for i in range(len_substring+1):
        for letter in range(ord('a'), ord('z') + 1):
            indexes_of_sentences = init.sub_sentences.get(substring[:i] + chr(letter) + substring[i:])
            if indexes_of_sentences:
                score = get_score_for_add_delete(i, len_substring)
                res += get_options_to_change(init.sentences, indexes_of_sentences, amount, complete_list, score)

    return res


def get_completions_without_change(substring):
    best_k_completions = []

    if init.sub_sentences.get(substring):
        indexes = init.sub_sentences[substring]
        max_score = len(substring)
        for index in indexes:
            init.sentences[index].set_score(max_score * 2)
            best_k_completions.append(init.sentences[index])
    return best_k_completions[:k]


def get_completions_with_change(best_k_completions, substring, amount):
    res: List[Any] = completions_with_delete(best_k_completions, substring, amount)
    res += completions_with_replace(best_k_completions+res, substring, amount)
    res += completions_with_add(best_k_completions+res, substring, amount)
    max_scores = sorted(res, key=lambda x: (x.get_score(), x.get_completed()), reverse=True)
    min_ = min(amount, len(max_scores))
    return res[:min_]


def get_best_k_completions(substring):
    substring = " ".join("".join(filter(lambda x: x.isalnum() or x.isspace(), substring)).lower().split())
    best_k_completions = get_completions_without_change(substring)

    len_ = len(best_k_completions)
    if len_ < k:
        best_k_completions += get_completions_with_change(best_k_completions, substring, k - len_)
    return sorted(best_k_completions, key=lambda x: (x.get_score(), x.get_completed()), reverse=True)
