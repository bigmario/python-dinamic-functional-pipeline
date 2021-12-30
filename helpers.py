from pprint import pprint
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

    book_list = []
    result = list(map(lambda x: x["bbooks"], master))

    for book in result:
        book_list.append(book)

    put_data(book_list)

    return book_list
