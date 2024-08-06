import os
from .helper import *


script_dir = os.path.dirname(os.path.realpath(__file__))


def get_stems(token, valid_words):
    """Stems a token.
	token (str): Word to be stemmed.
	valid_words (list): Valid words.
	returns (list): All valid stems.
	"""
    token = token.strip()
    all_tokens = [token]

    for _ in range(1):
        stems_duplication = stem_duplication(all_tokens, valid_words)
        all_tokens.extend(stems_duplication)

        stems_prefix = stem_prefix(all_tokens, valid_words)
        all_tokens.extend(stems_prefix)

        stems_repitition = stem_repitition(all_tokens, valid_words)
        all_tokens.extend(stems_repitition)

        stems_infix = stem_infix(all_tokens, valid_words)
        all_tokens.extend(stems_infix)

        stems_repitition = stem_repitition(all_tokens, valid_words)
        all_tokens.extend(stems_repitition)

        stems_suffix = stem_suffix(all_tokens, valid_words)
        all_tokens.extend(stems_suffix)

        stems_duplication = stem_duplication(all_tokens, valid_words)
        all_tokens.extend(stems_duplication)

        all_tokens = list(set(all_tokens))

    stems_valid = [token for token in all_tokens if is_valid(token, valid_words)]

    return stems_valid # [t for t in all_tokens if t != token]


def stem_duplication(tokens, valid_words):
    """Stems a token base on full reduplication.
	tokens (list): Words to be stemmed.
    valid_words (list): Valid words.
	returns (list): All attempted stems.
	"""
    stems_attempt = []

    for token in tokens:
        if "-" in token and "-" not in [token[0], token[-1]]:
            first, second = token.split("-")

            if len(first) > 1 and len(second) > 1:
                if first == second:
                    stems_attempt.append(first)

                elif first[-1] == "u" and replace_letter(first, -1, "o") == second or \
                    first[-2] == "u" and replace_letter(first, -2, "o")  == second:
                    stems_attempt.append(second)

                elif first[-2:] == "ng" and first[-3] == "u" and first[0:-3] + "o" == second:
                    stems_attempt.append(second)

    return stems_attempt


def stem_repitition(tokens, valid_words):
    """Stems a token base on partial reduplication.
	tokens (list): Words to be stemmed.
    valid_words (list): Valid words.
	returns (list): All attempted stems.
	"""
    stems_attempt = []

    for token in tokens:
        if "-" in token:
            token = token.replace("-", "")

        if len(token) > 2:
            if token[0] == token[1] and is_vowel(token[0:2]):
                stems_attempt.append(token[1:])

            elif token[0:2] == token[2:4] and len(token) > 4 \
                and is_consonant(token[0]):
                stems_attempt.append(token[2:])

            elif token[0:2] == token[3:5] and len(token) > 5 \
                and is_consonant(token[0:2]) and is_vowel(token[2]):
                stems_attempt.append(token[3:])

    return stems_attempt


def stem_prefix(tokens, valid_words):
    """Stems a token base on prefixes.
	tokens (list): Words to be stemmed.
    valid_words (list): Valid words.
	returns (list): All attempted stems.
	"""
    stems_attempt = []

    for token in tokens:
        for prefix in PREFIXES:
            if token.startswith(prefix) and len(token) > len(prefix):
                stem = token[len(prefix):]

                if stem[0] == "-":
                    stem = stem[1:]

                # consonant reduction
                if prefix.endswith("ng") and not is_valid(stem, valid_words):
                    for consonant in CONSONANTS:
                        if is_valid(consonant + stem, valid_words):
                            stems_attempt.append(consonant + stem)

                stems_attempt.append(stem)

        # assimilation
        for a_prefix in A_PREFIXES:
            if token.startswith(a_prefix) and len(token) > len(a_prefix):
                stem = token[len(a_prefix):]

                if stem[0] == "-":
                    stem = stem[1:]

                # consonant reduction
                if not is_valid(stem, valid_words):
                    for consonant in CONSONANTS:
                        if is_valid(consonant + stem, valid_words):
                            stems_attempt.append(consonant + stem)

                stems_attempt.append(stem)

        # VeV (e.g. a-ea-bton)
        if len(token) > 2 and token[1] == "e" and token[0] == token[2]:
            stem = token[2:]
            stems_attempt.append(stem)

    return stems_attempt


def stem_infix(tokens, valid_words):
    """Stems a token base on infixes.
	tokens (list): Words to be stemmed.
    valid_words (list): Valid words.
	returns (list): All attempted stems.
	"""
    stems_attempt = []

    for token in tokens:
        for infix in INFIXES:
            if len(token) > len(infix) + 1:
                if token[1:3] == infix and is_vowel(token[3]):
                    stem = token[0] + token[3:]

                    stems_attempt.append(stem)

                    # consonant change
                    # l => e
                    if infix == "in" and not is_valid(stem, valid_words):
                        if stem.startswith("l"):
                            stem = replace_letter(stem, 0, "e")
                            if is_valid(stem, valid_words):
                                stems_attempt.append(stem)

                if token[2:4] == infix and is_vowel(token[4]):
                    stem = token[0:2] + token[4:]

                    stems_attempt.append(stem)

                    # consonant change
                    # l => e
                    if infix == "in" and not is_valid(stem, valid_words):
                        if stem.startswith("l"):
                            stem = replace_letter(stem, 0, "e")
                            if is_valid(stem, valid_words):
                                stems_attempt.append(stem)

        # CVeV (e.g. s-ue-undon)
        if len(token) > 3 and token[2] == "e" and token[1] == token[3]:
                stem = token[0] + token[3:]
                stems_attempt.append(stem)

    return stems_attempt

def stem_suffix(tokens, valid_words):
    """Stems a token base on suffixes.
	tokens (list): Words to be stemmed.
    valid_words (list): Valid words.
	returns (list): All attempted stems.
	"""
    stems_attempt = []

    for token in tokens:
        for suffix in SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix):
                stem = token[0:len(token) - len(suffix)]

                if stem[-1] == "-":
                    stem = stem[:-1]

                # contraction
                if suffix == "t":
                    stem_contraction = stem + "n"
                    if is_valid(stem_contraction, valid_words):
                        stems_attempt.append(stem_contraction)

                if not is_valid(stem, valid_words) and len(stem) > 2:
                    # consonant change
                    # r => d or l
                    if stem.endswith("r"):
                        # r => d
                        stem_consonant_change = replace_letter(stem, -1, "d")
                        if is_valid(stem_consonant_change, valid_words):
                            stems_attempt.append(stem_consonant_change)
                        # r => l
                        else:
                            stem_consonant_change = replace_letter(stem, -1, "l")
                            if is_valid(stem_consonant_change, valid_words):
                                stems_attempt.append(stem_consonant_change)
                    # vowel change
                    # y => i
                    if stem.endswith("y"):
                        stem_vowel_change = replace_letter(stem, -1, "i")
                        if is_valid(stem_vowel_change, valid_words):
                            stems_attempt.append(stem_vowel_change)
                    # w => o
                    elif stem.endswith("w"):
                        stem_vowel_change = replace_letter(stem, -1, "o")
                        if is_valid(stem_vowel_change, valid_words):
                            stems_attempt.append(stem_vowel_change)

                    # vowel loss
                    if stems_vowel_loss := stem_vowel_loss([stem], valid_words):
                        stems_attempt.extend(stems_vowel_loss)
                    # metathesis
                    else:
                        switched_token = switch_letters(stem, -1, -2)
                        stems_metathesis = stem_vowel_loss([switched_token], valid_words)
                        stems_attempt.extend(stems_metathesis)

                stems_attempt.append(stem)

    return stems_attempt


def stem_vowel_loss(tokens, valid_words):
    stems_attempt = []

    for token in tokens:
        for vowel in VOWELS:
            if token:
                stem = token + vowel
                if is_valid(stem, valid_words):
                    stems_attempt.append(stem)

            if len(token) > 1:
                stem = token[0:-1] + vowel + token[-1]
                if is_valid(stem, valid_words):
                    stems_attempt.append(stem)
            if len(token) > 3:
                stem = token[0:-3] + vowel + token[-3:]
                if is_valid(stem, valid_words):
                    stems_attempt.append(stem)

    return stems_attempt


if __name__ == "__main__":
    token = input("Token: ")
    words = get_words("dictionary/files/akl_words.txt")
    stem = get_stems(token, words)
    print(stem)