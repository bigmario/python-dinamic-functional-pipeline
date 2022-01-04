import json


def get_criteria():
    with open("test.json") as f:
        data = json.load(f)

    return data


def get_data():
    with open("pms_response.json") as f:
        data = json.load(f)

    return data


def put_data(data):
    with open("output.txt", "a") as f:
        json.dump(data, f, indent=4)
        f.write("\n")
