import csv
from .models import PartsOfSpeech, Etymology, Classification, Attribute, DictEntry


def import_data(file_name):
    with open(file_name, "r") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            print(row)

            if row["pos"].strip() != "":
                pos = PartsOfSpeech.objects.get(code=row["pos"].strip())
            else:
                pos = None

            if row["etymology"].strip() != "":
                etymology = Etymology.objects.get(code=row["etymology"].strip())
            else:
                etymology = None

            if row["classification"].strip() != "":
                classification = Classification.objects.get(code=row["classification"].strip())
            else:
                classification = None

            attribute = Attribute(
                definition=row["definition"].strip(),
                pos=pos,
                etymology=etymology,
                classification=classification,
            )
            attribute.save()

            entry, created = DictEntry.objects.get_or_create(word=row["word"].strip())
            if attribute not in entry.attributes.all():
                entry.attributes.add(attribute)


if __name__ == "__main__":
    import_data("dictionary.csv")