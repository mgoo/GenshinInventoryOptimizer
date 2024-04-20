import json


def load_json_data(path):
    with open(path, "r") as file:
        return json.load(file)