import re
from symspellpy import SymSpell
from nltk.tokenize import WhitespaceTokenizer, sent_tokenize
from .stemmer import akl_stemmer


tokenizer = WhitespaceTokenizer()


def is_valid(word, case_insensitive=True):
    if case_insensitive:
        word = word.lower()
    
    if word.isnumeric() or (word[0] in ["$", "Php", "₱"] and word[1:].isnumeric()):
        return True

    if clean(word) in WORDS:
        return True
    else:
        return any([clean(word) in WORDS for word in akl_stemmer.get_stems(word, WORDS)])


def get_suggestions(word, max_suggestions=5, case_insensitive=True):
    if not is_valid(word):
        org_word = word

        if case_insensitive:
            word = word.lower()
    
        end_punct = ""
        start_punct = ""
        if end_match := re.search(r"([\,\.\?\!\"\)\]\}]+$)", word.strip()):
            end_punct = end_match.group(1)
        if start_match := re.search(r"(^[\"\(\[\{]+)", word.strip()):
            start_punct = start_match.group(1)

        lookedup_suggestions = spell.lookup(clean(word), verbosity="closest")

        suggestions = []
        for suggestion in lookedup_suggestions:
            term = suggestion.term
            if org_word.isupper():
                if case_insensitive:
                    term = term.upper()
            elif org_word[0].isupper():
                term = term.capitalize()
            suggestions.append(start_punct + term + end_punct)

        return suggestions[:max_suggestions] if len(suggestions) > max_suggestions else suggestions
    else:
        return []


def spellcheck_text(text, max_suggestions=5, case_insensitive=True):
    tokens = preprocess(text)

    checks = []
    for token in tokens:
        checks.append({
            "word": token,
            "valid": is_valid(token, case_insensitive),
            "suggestions": get_suggestions(token, max_suggestions, case_insensitive)
        })
    
    return checks


def preprocess(text):
    preprocessed_tokens = []
    for token in tokenizer.tokenize(text.strip()):
        preprocessed_tokens.append(token)

    return preprocessed_tokens


def clean(token):
    return re.sub(r"[^a-zA-Z-']", "", token.strip())


def get_spellchecker(file_path):
    spell = SymSpell(max_dictionary_edit_distance=2)
    spell.load_dictionary(file_path, 0, 1, separator=",")
    return spell


def get_words(file_path):
    with open(file_path, "r") as infile:
        return [word.strip() for word in infile.readlines() if word.islower()]


spell = get_spellchecker("dictionary/files/akl_wordfreq.txt")
WORDS = get_words("dictionary/files/akl_words.txt")


if __name__ == "__main__":
    text = input("text: ")
    checks = spellcheck_text
    print(checks)