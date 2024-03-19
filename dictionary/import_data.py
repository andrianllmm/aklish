import csv
from .models import DictEntry


def import_data(file_name):
    with open(file_name, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            new_entry = DictEntry(word=row["word"], definition=row["definition"])
            new_entry.save()


if __name__ == "__main__":
    import_data("dictionary.csv")