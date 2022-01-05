import json


def get_criteria():
    with open("test_copy_2.json") as f:
        data = json.load(f)

    return data


def get_data():
    with open("main_response.json") as f:
        data = json.load(f)

    return data


def put_data(data):
    with open("output.txt", "a") as f:
        json.dump(data, f, indent=4)
        f.write("\n")
