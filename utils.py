import json


def load_json_data(path):
    with open(path, "r") as file:
        return json.load(file)


def percent_to_dec(value: str):
    if "%" in value:
        value = value.replace("%", "")
        value = str(float(value) / 100)
    return value