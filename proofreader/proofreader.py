import re
from spellchecker import SpellChecker
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from .stemmer import akl_stemmer
from tabulate import tabulate


def proofread_text(text, max_suggestions=5):
    checks = []

    sents = sent_tokenize(text.strip())
    for s, sent in enumerate(sents):
        words = word_tokenize(sent.strip())
        for t, token in enumerate(words):
            cls = "word"
            valid = True
            suggestions = []

            if all(char in string.punctuation for char in token):
                cls = "punc"
            
            elif token.replace(".", "").isnumeric():
                cls = "num"

            elif len(sents) > 1 and t == 0:
                if token[0].islower():
                    valid = False
                    suggestions = [token.capitalize()]
                elif clean(token.lower()) not in spell:
                    cls = "NE"

            elif token[0].isupper():
                cls = "NE"
            
            elif clean(token) not in spell:
                if not akl_stemmer.get_stems(clean(token), spell):
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
    return re.sub(r"[^a-zA-Z-']", "", token.strip())


def get_spellchecker(file_path=None):
    if file_path:
        spell = SpellChecker(language=None)
        spell.word_frequency.load_text_file(file_path)
    else:
        spell = SpellChecker()
    return spell


spell = get_spellchecker("dictionary/files/akl_words.txt")


if __name__ == "__main__":
    text = input("text: ")
    checks = proofread_text(text)
    print("\n" + tabulate(checks, headers="keys") + "\n")