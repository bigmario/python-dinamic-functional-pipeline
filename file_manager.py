import json


def get_data():
    with open("response.json") as f:
        data = json.load(f)

    return data


def put_data(data):
    with open("output.txt", "w") as f:
        json.dump(data, f, indent=4)
