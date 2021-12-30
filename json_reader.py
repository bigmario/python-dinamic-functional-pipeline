import json


def get_data():
    with open("response.json") as f:
        data = json.load(f)

    return data
