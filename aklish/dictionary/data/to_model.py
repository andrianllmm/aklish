import concurrent.futures
import json
import os
from itertools import repeat

from dictionary.models import (
    PartsOfSpeech,
    Origin,
    Classification,
    Source,
    Attribute,
    DictEntry,
)
from translate.models import Language, Entry, Translation
from django.contrib.auth.models import User


script_dir = os.path.dirname(os.path.realpath(__file__))


def dictionary_to_model(lang, file_path=None):
    if not file_path:
        file_path = os.path.join(script_dir, f"{lang}_dictionary.json")

    # Only include common English words
    if lang == "eng":
        with open(os.path.join(script_dir, "eng_common.txt")) as eng_common_file:
            eng_common = [word.strip().lower() for word in eng_common_file.readlines()]

    with open(file_path) as in_file:
        entries = json.load(in_file)

        errors = []

        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     results = executor.map(entry_to_model, repeat(lang), entries)

        #     for result in results:
        #         if results:
        #             errors.append(result)

        for entry in entries:
            if lang == "eng" and entry["word"].lower() not in eng_common:
                continue

            if not entry.get("word"):
                continue

            result = entry_to_model(lang, entry)
            if result:
                errors.append(result)

        with open(os.path.join(script_dir, "errors.json"), "w") as errors_file:
            json.dump(errors, errors_file, indent=4, ensure_ascii=False)


def entry_to_model(lang, entry):
    print(f"{entry['word']}:", end=" ")

    error = None

    lang_object = Language.objects.get(code=lang)
    entry_object = DictEntry.objects.get_or_create(word=entry["word"].strip(), lang=lang_object)[0]

    for attribute in entry["attributes"]:
        print(f"{attribute['pos']};", end=" ")

        if not attribute.get("definition"):
            continue

        attribute_object = Attribute.objects.create(definition=attribute["definition"] or "")

        if attribute["pos"]:
            if PartsOfSpeech.objects.filter(code=attribute["pos"].strip()).exists():
                pos = PartsOfSpeech.objects.get(code=attribute["pos"].strip())
            else:
                error = {
                    "error": "pos",
                    "word": entry["word"],
                    "attribute": attribute["pos"],
                }
                continue
        else:
            pos = None

        if attribute["origin"]:
            if Origin.objects.filter(code=attribute["origin"].strip()).exists():
                origin = Origin.objects.get(code=attribute["origin"].strip())
            else:
                error = {
                    "error": "origin",
                    "word": entry["word"],
                    "attribute": attribute["origin"],
                }
                continue
        else:
            origin = None

        if attribute["classification"]:
            if Classification.objects.filter(code=attribute["classification"].strip()).exists():
                classification = Classification.objects.get(code=attribute["classification"].strip())
            else:
                error = {
                    "error": "classification",
                    "word": entry["word"],
                    "attribute": attribute["classification"],
                }
                continue
        else:
            classification = None

        if sources := attribute["sources"]:
            for source_title in sources:
                if source_title:
                    source = Source.objects.get_or_create(title=source_title)[0]
                    attribute_object.sources.add(source)

        attribute_object.pos = pos
        attribute_object.origin = origin
        attribute_object.classification = classification
        attribute_object.save()

        if attribute["similar"]:
            for similar_word in attribute["similar"]:
                if similar_word != entry["word"]:
                    similar_entry = DictEntry.objects.get_or_create(word=similar_word.strip(), lang=lang_object)[0]
                    similar_entry.save()
                    attribute_object.similar.add(similar_entry)
            attribute_object.save()

        if attribute["opposite"]:
            for opposite_word in attribute["opposite"]:
                if opposite_word != entry["word"]:
                    opposite_entry = DictEntry.objects.get_or_create(word=opposite_word.strip(), lang=lang_object)[0]
                    opposite_entry.save()
                    attribute_object.opposite.add(opposite_entry)
            attribute_object.save()

        if attribute["examples"]:
            user_object = User.objects.get(username="andrianllmm", email="maagmaandrian@gmail.com", is_superuser=True,)

            for example in attribute["examples"]:
                if isinstance(example, str):
                    example_entry = Entry.objects.get_or_create(
                        content=example,
                        lang=lang_object,
                        user=user_object,
                    )[0]

                elif isinstance(example, dict):
                    example_entry = Entry.objects.get_or_create(
                        content=example.get("original") or "",
                        lang=lang_object,
                        user=user_object,
                    )[0]

                    if example.get("translations"):
                        for translation_lang, translation in example["translations"].items():
                            translation_lang_object = Language.objects.get(code=translation_lang)
                            Translation.objects.get_or_create(
                                entry=example_entry,
                                content=translation,
                                lang=translation_lang_object,
                                user=user_object,
                            )

                attribute_object.examples.add(example_entry)
            attribute_object.save()

        entry_object.attributes.add(attribute_object)
    print()

    return error


def attributes_to_model(folder_path=os.path.join(script_dir, "attributes/")):
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
        classification_object = Classification.objects.get_or_create(
            code=classification["code"]
        )[0]
        classification_object.meaning = classification["meaning"]
        classification_object.save()
