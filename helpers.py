from pprint import pprint


def filter_resellers(master, key):

    reseller_list = []
    result = list(map(lambda x: x["preseller"], master))

    for reseller in result:
        reseller_list.append({reseller["name"], reseller["createdAt"]}) if reseller[
            "name"
        ] != key else None

    return reseller_list


def filter_books(master, key):

    book_list = []
    result = list(map(lambda x: x["bbooks"], master))

    for book in result:
        for item in book:
            book_list.append(book)

    return book_list
