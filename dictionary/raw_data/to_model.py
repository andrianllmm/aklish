import json, os
from dictionary.models import PartsOfSpeech, Origin, Classification, Source, Attribute, DictEntry
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
            entry_object = DictEntry.objects.get_or_create(word=entry["word"].strip(), lang=lang_object)[0]

            for attribute in entry["attributes"]:
                print(f"{attribute['pos']};", end=" ")

                attribute_object = Attribute.objects.get_or_create(
                    definition=attribute["definition"],
                )[0]

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

                if source_title := attribute["source"]:
                    source = Source.objects.get_or_create(title=source_title)[0]
                
                attribute_object.pos = pos
                attribute_object.origin = origin
                attribute_object.classification = classification
                attribute_object.source = source
                attribute_object.save()

                if attribute["similar"]:
                    for similar_word in attribute["similar"]:
                        similar_entry = DictEntry.objects.get_or_create(word=similar_word.strip(), lang=lang_object)[0]
                        attribute_object.similar.add(similar_entry)
                    attribute_object.save()

                if attribute["opposite"]:
                    for opposite_word in attribute["opposite"]:
                        opposite_entry = DictEntry.objects.get_or_create(word=opposite_word.strip(), lang=lang_object)[0]
                        attribute_object.opposite.add(opposite_entry)
                    attribute_object.save()
                
                if attribute["examples"]:
                    user_object = User.objects.get(username="andrianllmm", email="maagmaandrian@gmail.com", is_superuser=True)
                    for example in attribute["examples"]:
                        example_entry = Entry.objects.get_or_create(
                            content=example["original"], lang=lang_object, user=user_object
                        )[0]
                        if example["translations"]:
                            for translation_lang, translation in example["translations"].items():
                                translation_lang_object = Language.objects.get(code=translation_lang)
                                Translation.objects.get_or_create(
                                    entry=example_entry, content=translation, lang=translation_lang_object, user=user_object
                                )
                        attribute_object.examples.add(example_entry)
                    attribute_object.save()
                
                entry_object.attributes.add(attribute_object)
            print()
        
        with open(f"{script_dir}/errors.json", "w") as errors_file:
            json.dump(errors, errors_file, indent=4, ensure_ascii=False)


def attributes_to_model(folder_path=f"{script_dir}/attributes/"):
    with open(f"{folder_path}/pos.json") as pos_file:
        pos_list = json.load(pos_file)
    
    for pos in pos_list:
        print(pos)
        pos_object = PartsOfSpeech.objects.get_or_create(code=pos["code"])[0]
        pos_object.meaning = pos["meaning"]
        pos_object.save()
    
    with open(f"{folder_path}/origin.json") as origin_file:
        origin_list = json.load(origin_file)
    
    for origin in origin_list:
        print(origin)
        origin_object = Origin.objects.get_or_create(code=origin["code"])[0]
        origin_object.meaning = origin["meaning"]
        origin_object.save()
    
    with open(f"{folder_path}/classification.json") as classification_file:
        classification_list = json.load(classification_file)
    
    for classification in classification_list:
        print(classification)
        classification_object = Classification.objects.get_or_create(code=classification["code"])[0]
        classification_object.meaning = classification["meaning"]
        classification_object.save()


# def delete_all_objects(Model):
#     Model.objects.all().delete()


if __name__ == "__main__":
    pass
    # Attribute.objects.all().delete()
    # DictEntry.objects.all().delete()
    # to_model(f"{script_dir}/akl_dictionary.json", lang="akl")