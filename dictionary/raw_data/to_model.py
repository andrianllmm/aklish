import json, os
from dictionary.models import PartsOfSpeech, Origin, Classification, Attribute, DictEntry
from translations.models import Language, Entry, Translation
from django.contrib.auth.models import User


script_dir = os.path.dirname(os.path.realpath(__file__))


def to_model(file_path, lang):
    with open(file_path) as infile:
        entries = json.load(infile)

        errors = []

        for entry in entries:
            print(f"{entry['word']}:", end=" ")

            lang_object = Language.objects.get(code=lang)
            entry_object, created = DictEntry.objects.get_or_create(word=entry["word"].strip(), lang=lang_object)

            for attribute in entry["attributes"]:
                print(f"{attribute['pos']};", end=" ")
                if attribute["pos"]:
                    if PartsOfSpeech.objects.filter(code=attribute["pos"].strip()).exists():
                        pos = PartsOfSpeech.objects.get(code=attribute["pos"].strip())
                    else:
                        errors.append({"error": "pos", "word": entry["word"], "attribute": attribute["pos"]})
                        continue
                else:
                    pos = None

                if attribute["origin"]:
                    if Origin.objects.filter(code=attribute["origin"].strip()).exists():
                        origin = Origin.objects.get(code=attribute["origin"].strip())
                    else:
                        errors.append({"error": "origin", "word": entry["word"], "attribute": attribute["origin"]})
                        continue
                else:
                    origin = None

                if attribute["classification"]:
                    if Classification.objects.filter(code=attribute["classification"].strip()).exists():
                        classification = Classification.objects.get(code=attribute["classification"].strip())
                    else:
                        errors.append({"error": "classification", "word": entry["word"], "attribute": attribute["classification"]})
                        continue
                else:
                    classification = None

                attribute_object = Attribute.objects.create(
                    definition=attribute["definition"],
                    pos=pos,
                    origin=origin,
                    classification=classification,
                    source=attribute["source"]
                )

                if attribute["examples"]:
                    user_object = User.objects.get(username="andrianllmm", email="maagmaandrian@gmail.com", is_superuser=True)
                    for example, example_translation in attribute["examples"].items():
                        example_entry, created = Entry.objects.get_or_create(
                            content=example, lang=lang_object, user=user_object
                        )
                        if example_translation:
                            match lang_object.code:
                                case "akl":
                                    example_translation_lang = Language.objects.get(code="eng")
                                case "eng":
                                    example_translation_lang = Language.objects.get(code="akl")
                            Translation.objects.create(
                                entry=example_entry, content=example_translation, lang=example_translation_lang, user=user_object
                            )
                        attribute_object.examples.add(example_entry)

                if attribute["similar"]:
                    for similar_word in attribute["similar"]:
                        if DictEntry.objects.filter(word=similar_word.strip()).exists():
                            similar_entry = DictEntry.objects.get(word=similar_word.strip())
                            attribute_object.similar.add(similar_entry)
                        else:
                            errors.append({"error": "similar", "word": entry["word"], "attribute": attribute["similar"]})
                            continue

                if attribute["opposite"]:
                    for opposite_word in attribute["opposite"]:
                        if DictEntry.objects.filter(word=opposite_word.strip()).exists():
                            opposite_entry = DictEntry.objects.get(word=opposite_word.strip())
                            attribute_object.opposite.add(opposite_entry)
                        else:
                            errors.append({"error": "opposite", "word": entry["word"], "attribute": attribute["opposite"]})
                            continue
                
                if not entry_object.attributes.filter(pk=attribute_object.pk).exists():
                    entry_object.attributes.add(attribute_object)
            print()
        
        print("Errors:")
        for error in errors:
            print(f"{error['error']} error from {error['word']} ({error['attribute']})")   


def delete_all_objects(Model):
    for object in Model.objects.all():
        object.delete()


if __name__ == "__main__":
    delete_all_objects(Attribute)
    delete_all_objects(DictEntry)
    to_model(f"{script_dir}/akl_dictionary.json", lang="akl")