import json


def get_criteria():
    with open("./input/input_filters2.json") as f:
        data = json.load(f)

    return data


def get_data_file():
    with open("./input/customers_list.json") as f:
        data = json.load(f)

    return data


def put_data(data):
    with open("./output/output.txt", "a") as f:
        json.dump(data, f, indent=4)
        f.write("\n")
