import os


script_dir = os.path.dirname(os.path.realpath(__file__))


def is_valid(token, valid_words):
	"""Checks if token is valid.
	token (str): Word to be validated.
	valid_words (list): Valid words.
	returns: bool
	"""
	return token.lower() in valid_words


def is_vowel(substring):
	"""Checks if a substring is a vowel.
	substring (str): Substring to be tested.
	returns: bool
	"""
	return all(letter.lower() in VOWELS for letter in substring)


def is_consonant(substring):
	"""Checks if a substring is a consonant.
	substring (str): Substring to be tested.
	returns: bool
	"""
	return all(letter.lower() in CONSONANTS for letter in substring)


def replace_letter(token, index, letter):
	"""Replaces a letter in a token.
	token (str): Word to be updated.
	index (int): Index of the letter to be replaced.
	letter (str): Letter used to replace.
	returns (str): The updated word.
	"""
	token_as_list = list(token)

	token_as_list[index] = letter

	return "".join(token_as_list)


def switch_letters(token, index1, index2):
    """Replaces two letters in a token.
	token (str): Word to be updated.
	index1 (int): Index of the first letter to be switched.
    index2 (int): Index of the second letter to be switched.
	returns (str): The updated word.
	"""
    token_as_list = list(token)

    index1_letter = token_as_list[index1]
    token_as_list[index1] = token_as_list[index2]
    token_as_list[index2] = index1_letter

    return "".join(token_as_list)


def get_words(file_path):
    with open(file_path, "r") as infile:
        return [word.strip().lower() for word in infile.readlines()]


def get_affixes(file_path):
    with open(file_path, "r") as infile:
        affixes = [affix.strip().replace("-", "") for affix in infile.readlines()]
        return sorted(affixes, key=lambda a: len(a), reverse=True)


def get_a_prefixes(prefixes):
    assimilations = [replace_letter(prefix, -2, "m")[0:-1] for prefix in PREFIXES if prefix.endswith("ng")]
    assimilations += [replace_letter(prefix, -2, "n")[0:-1] for prefix in PREFIXES if prefix.endswith("ng")]
    return sorted(assimilations, key=lambda a: len(a), reverse=True)


VOWELS = "aeiou"
CONSONANTS = "ebcdfghjklmnpqrstvwxyz"

PREFIXES = get_affixes(f"{script_dir}/affixes/prefixes.txt")
INFIXES = get_affixes(f"{script_dir}/affixes/infixes.txt")
SUFFIXES = get_affixes(f"{script_dir}/affixes/suffixes.txt")

PREFIXES = sorted(PREFIXES + INFIXES, key=lambda p: len(p), reverse=True)

A_PREFIXES = get_a_prefixes(PREFIXES)