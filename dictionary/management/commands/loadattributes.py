import concurrent.futures
import json
import os
from itertools import repeat

from django.core.management.base import BaseCommand, CommandError

from dictionary.models import (
    PartsOfSpeech,
    Origin,
    Classification,
)


script_dir = os.path.dirname(os.path.realpath(__file__))


class Command(BaseCommand):
    help = "Loads dictionary data."

    def add_arguments(self, parser):
        parser.add_argument("--attributes_path", type=str, help="Path to the file containing dictionary data.", default=None)

    def handle(self, *args, **options):
        attributes_path = options["attributes_path"]
        attributes_to_model(attributes_path)


def attributes_to_model(folder_path=None):
    if not folder_path:
        folder_path=os.path.join(script_dir, "../../data/attributes/")

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