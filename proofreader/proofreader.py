import nltk
nltk.download("punkt")
nltk.download("punkt_tab")

import lemminflect
import os
import pkg_resources
import re
import string
from aklstemmer import stemmer
from nltk.tokenize import word_tokenize
from symspellpy import SymSpell, Verbosity
from tabulate import tabulate
from typing import Optional


script_dir = os.path.dirname(os.path.realpath(__file__))


def proofread_text(text: str, lang: Optional[str] = "akl", max_suggestions: Optional[int] = 5) -> dict:
    """Proofreads Aklanon or English text.

    Args:
        text (str): Any text.
        lang (str, optional): Language of the proofreader. Defaults to 'akl'. Values can be:
            - 'akl': Aklanon
            - 'eng': English
        max_suggestions (int, optional): Maximum suggestions. Defaults to 5.

    Returns:
        dict: A dictionary containing a list of checks, word count, mistake count, and correctness.
    """
    # Get spell checkers
    if lang == "akl":
        spell = get_spellchecker("dictionary/data/akl_freqlist.csv")
    else:
        spell = get_spellchecker()

    # Initialize data
    data = {"checks": [], "word_count": 0, "mistake_count": 0, "correctness": None}

    # Tokenize text
    words = word_tokenize(text.strip())
    for token in words:
        # Clean token
        clean_token = clean(token)

        # Initialize fields
        cls = "word"
        valid = True
        suggestions = []

        # Identify punctuation
        if all(char in string.punctuation for char in token):
            cls = "punc"

        # Identify numerals
        elif token.replace(".", "").isnumeric():
            cls = "num"

        elif clean_token not in list(spell.words.keys()):
            # Get lammas and stems
            lemmas = lemminflect.getAllLemmas(clean_token)
            stems = stemmer.get_stems(clean_token, valid_words=list(spell.words.keys()))
            if clean_token in stems:
                stems.remove(clean_token)

            # If no root, invalid
            if (lang == "eng" and not lemmas) or (lang == "akl" and not stems):
                valid = False
                suggestions = spell.lookup(clean_token, Verbosity.CLOSEST, max_edit_distance=2)

            # If has root, valid
            else:
                cls = "stemmed"

        # Convert suggestions to list
        suggestions = [suggestion.term for suggestion in suggestions] if suggestions else []

        # Limit suggestions
        suggestions = (
            suggestions[:max_suggestions]
            if len(suggestions) > max_suggestions
            else suggestions
        )

        # Append data
        data["checks"].append(
            {
                "token": token,
                "cls": cls,
                "valid": valid,
                "suggestions": suggestions,
            }
        )

    # Calculate counts
    data["word_count"] = cal_word_count(data["checks"])
    data["mistake_count"] = cal_mistake_count(data["checks"])
    data["correctness"] = cal_correctness(data["word_count"], data["mistake_count"])

    return data


def clean(token: str) -> str:
    """Cleans a token."""
    return re.sub(r"[^a-zA-Z'-]", "", token.strip())


def cal_word_count(checks: list) -> int:
    """Calculates the word count."""
    word_count = 0
    for check in checks:
        if check["cls"] not in ["punc", "num"]:
            word_count += 1
    return word_count


def cal_mistake_count(checks: list) -> int:
    """Calculates the mistake count."""
    mistake_count = 0
    for check in checks:
        if check["valid"] == False:
            mistake_count += 1
    return mistake_count


def cal_correctness(word_count: int, mistake_count: int) -> float:
    """Calculates the correctness in percentage."""
    if word_count == 0:
        correctness = 0
    elif mistake_count == 0:
        correctness = 100
    else:
        correctness = round(100 * (1 - mistake_count / word_count))
    return correctness


def get_spellchecker(file_path: str = None) -> SymSpell:
    """Gets a spellchecker from a file."""
    spell = SymSpell()

    if not file_path:
        file_path = pkg_resources.resource_filename(
            "symspellpy", "frequency_dictionary_en_82_765.txt"
        )

    spell.load_dictionary(file_path, 0, 1, ",")

    return spell


if __name__ == "__main__":
    text = input("text: ")
    data = proofread_text(text)
    print("\n" + tabulate(data, headers="keys") + "\n")
