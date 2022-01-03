from pprint import pprint
import json

from functional_pipeline import join, lens

from file_manager import put_data


def filter_resellers(master, key):

    reseller_list = []
    result = list(map(lambda x: x["preseller"], master))

    for reseller in result:
        reseller_list.append({reseller["name"], reseller["createdAt"]}) if reseller[
            "name"
        ] != key else None

    return reseller_list


def filter_books(master):
    book_list = [book["bbooks"][0] for book in master]

    result = list(filter(lambda x: x["riRoomType"]["id"] == 107, book_list))

    for item in result:
        put_data(item["riRoomType"])

    return book_list
