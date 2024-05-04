import lemminflect
import re
import string
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize, sent_tokenize
from .stemmer import akl_stemmer
from tabulate import tabulate


def proofread_text(text, lang="akl", max_suggestions=5):
    if lang == "akl":
        spell = get_spellchecker("dictionary/raw_data/akl_freq.json")
    else:
        spell = get_spellchecker()

    data = {"checks": [], "word_count": 0, "mistake_count": 0, "correctness": None}

    sents = sent_tokenize(text.strip())
    for s, sent in enumerate(sents):
        words = word_tokenize(sent.strip())
        for t, token in enumerate(words):
            cls = "word"
            valid = True
            suggestions = []

            if all(char in string.punctuation for char in token):
                cls = "punct"
            
            elif token.replace(".", "").isnumeric():
                cls = "num"

            elif len(sents) > 1 and t == 0:
                if token[0].islower():
                    valid = False
                    suggestions = [token.capitalize()]
                elif clean(token.lower()) not in spell:
                    cls = "propn"

            elif token[0].isupper():
                cls = "propn"
            
            elif clean(token) not in spell:
                if (lang == "akl" and not akl_stemmer.get_stems(clean(token), spell)) or \
                    (lang == "eng" and not lemminflect.getAllLemmas(clean(token))):
                    valid = False
                    suggestions = spell.candidates(clean(token))
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
        if check["cls"] in ["word", "propn"]:
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