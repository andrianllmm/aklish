import lemminflect
import re
import string
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize, sent_tokenize
from .stemmer import akl_stemmer
from tabulate import tabulate


def proofread_text(text, lang="akl", max_suggestions=5):
    if lang == "akl":
        spell = get_spellchecker("dictionary/data/akl_freq.json")
    else:
        spell = get_spellchecker()

    checks = []

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
            checks.append({
                "token": token,
                "cls": cls,
                "valid": valid,
                "suggestions": suggestions,
            })

    return checks


def clean(token):
    return re.sub(r"[^a-zA-Z'-]", "", token.strip())


def get_spellchecker(file_path=None):
    if file_path:
        spell = SpellChecker(language=None)
        spell.word_frequency.load_dictionary(file_path)
    else:
        spell = SpellChecker()

    return spell


if __name__ == "__main__":
    text = input("text: ")
    checks = proofread_text(text)
    print("\n" + tabulate(checks, headers="keys") + "\n")