import lemminflect
import os
import re
import string
from aklstemmer import stemmer
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from tabulate import tabulate


script_dir = os.path.dirname(os.path.realpath(__file__))


def proofread_text(text, lang="akl", max_suggestions=5):
    if lang == "eng":
        spell = get_spellchecker()
    elif lang == "akl":
        spell = get_spellchecker("dictionary/data/akl_freqlist.json")

    data = {"checks": [], "word_count": 0, "mistake_count": 0, "correctness": None}

    text = text.strip()

    words = word_tokenize(text)
    for token in words:
        clean_token = clean(token)

        cls = "word"
        valid = True
        suggestions = []

        if all(char in string.punctuation for char in token):
            cls = "punc"

        elif token.replace(".", "").isnumeric():
            cls = "num"

        elif clean_token not in spell:
            lemmas = lemminflect.getAllLemmas(clean_token)

            stems = stemmer.get_stems(clean_token, valid_words=list(spell))
            if clean_token in stems:
                stems.remove(clean_token)

            if (lang == "eng" and not lemmas) or (lang == "akl" and not stems):
                valid = False
                suggestions = spell.candidates(clean_token)
            else:
                cls = "stemmed"

        suggestions = list(suggestions) if suggestions else []

        suggestions = suggestions[:max_suggestions] if len(suggestions) > max_suggestions else suggestions

        data["checks"].append({
            "token": token,
            "cls": cls,
            "valid": valid,
            "suggestions": suggestions,
        })

    data["word_count"] = cal_word_count(data["checks"])
    data["mistake_count"] = cal_mistake_count(data["checks"])
    data["correctness"] = cal_correctness(data["word_count"], data["mistake_count"])

    return data


def clean(token):
    return re.sub(r"[^a-zA-Z'-]", "", token.strip())


def cal_word_count(checks):
    word_count = 0
    for check in checks:
        if check["cls"] not in ["punc", "num"]:
            word_count += 1
    return word_count


def cal_mistake_count(checks):
    mistake_count = 0
    for check in checks:
        if check["valid"] == False:
            mistake_count += 1
    return mistake_count


def cal_correctness(word_count, mistake_count):
    correctness = None
    if word_count == 0:
        pass
    elif mistake_count == 0:
        correctness = 100
    else:
        correctness = round(100 * (1 - mistake_count / word_count))
    return correctness


def get_spellchecker(file_path=None):
    if file_path:
        spell = SpellChecker(language=None)
        spell.word_frequency.load_dictionary(file_path)
    else:
        spell = SpellChecker()

    return spell


if __name__ == "__main__":
    text = input("text: ")
    data = proofread_text(text)
    print("\n" + tabulate(data, headers="keys") + "\n")