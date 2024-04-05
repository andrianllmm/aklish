import csv, os
from dictionary.models import PartsOfSpeech, Etymology, Classification, Attribute, DictEntry


script_dir = os.path.dirname(os.path.realpath(__file__))


def to_model(file_path):
    with open(file_path, "r") as infile:
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


def delete_all_objects(Model):
    for object in Model.objects.all():
        object.delete()


if __name__ == "__main__":
    delete_all_objects(Attribute)
    delete_all_objects(DictEntry)
    to_model(f"{script_dir}/akl-dictionary.csv")