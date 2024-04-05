import csv, os


script_dir = os.path.dirname(os.path.realpath(__file__))


def to_words(infile_path, outfile_path):
    with open(infile_path, "r") as infile:
        reader = csv.DictReader(infile)
    
        with open(outfile_path, "w") as outfile:
            words = [row["word"] for row in reader]
            words = list(set(words))
            words = sorted(words, key=lambda w: w.lower())

            outfile.write("\n".join(words))


def to_wordfreq(infile_path, outfile_path):
    with open(infile_path, "r") as infile:
        reader = csv.DictReader(infile)
    
        with open(outfile_path, "w") as outfile:
            words = [row["word"] for row in reader]
            words = list(set(words))
            words = sorted(words, key=lambda w: w.lower())

            wordfreq = [{"word": word, "freq": 1} for word in words]

            writer = csv.DictWriter(outfile, fieldnames=["word", "freq"])
            writer.writeheader
            writer.writerows(wordfreq)


if __name__ == "__main__":
    to_words(f"{script_dir}/akl_dictionary.csv", f"{script_dir}/akl_words.txt")
    to_wordfreq(f"{script_dir}/akl_dictionary.csv", f"{script_dir}/akl_wordfreq.txt")