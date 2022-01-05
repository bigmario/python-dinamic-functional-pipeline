from pprint import pprint
from datetime import datetime
from functional_pipeline import join, lens


def filter_resellers(master, key):

    reseller_list = []
    result = list(map(lambda x: x["preseller"], master))

    for reseller in result:
        reseller_list.append({reseller["name"], reseller["createdAt"]}) if reseller[
            "name"
        ] != key else None

    return reseller_list


def filter_room_type(master, params):

    result = []

    for item in master:
        for book in item["bbooks"]:
            if book["riRoomType"]["id"] == params["filter_room_type"]:
                result.append(item)

    return result


def filter_guest_gender(master, params):

    result = []

    for item in master:
        for book in item["bbooks"]:
            for guest in book["bbookPGuests"]:
                if guest["pguest"]["gender"] == params["filter_gender"]:
                    result.append(item)

    return result


def filter_checkin_checkout(master, type, params):

    operator = params[f"filter_{type}"]["condition"]

    if operator == "Between":

        millis_from = params[f"filter_{type}"]["date_range"]["from_"]
        millis_to = params[f"filter_{type}"]["date_range"]["to"]

        date_from = (
            datetime.utcfromtimestamp(millis_from // 1000.0)
            .replace(microsecond=millis_from % 1000 * 1000)
            .strftime("%Y-%m-%d")
        )

        date_to = (
            datetime.utcfromtimestamp(millis_to // 1000.0)
            .replace(microsecond=millis_from % 1000 * 1000)
            .strftime("%Y-%m-%d")
        )

        result = list(
            filter(lambda x: x[type] >= date_from and x[type] <= date_to, master)
        )
    else:
        millis_date = params[f"filter_{type}"]["date"]
        date = (
            datetime.utcfromtimestamp(millis_date // 1000.0)
            .replace(microsecond=millis_date % 1000 * 1000)
            .strftime("%Y-%m-%d")
        )

        if operator == "Equal to":
            result = list(filter(lambda x: x[type] == date, master))
        elif operator == "Less to":
            result = list(filter(lambda x: x[type] < date, master))
        elif operator == "Less than or equal to":
            result = list(filter(lambda x: x[type] <= date, master))
        elif operator == "Greater than":
            result = list(filter(lambda x: x[type] > date, master))
        elif operator == "Greater than or equal to":
            result = list(filter(lambda x: x[type] >= date, master))
        elif operator == "Different to":
            result = list(filter(lambda x: x[type] != date, master))

    return result
