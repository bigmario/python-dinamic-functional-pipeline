from pprint import pprint
from datetime import datetime
from functional_pipeline import join, lens

from libs.file_manager import put_data


def filter_resellers(master, key):

    reseller_list = []
    result = list(map(lambda x: x["preseller"], master))

    for reseller in result:
        reseller_list.append({reseller["name"], reseller["createdAt"]}) if reseller[
            "name"
        ] != key else None

    return reseller_list


def filter_email(master, params):

    result = []

    for customer in master:
        for email in customer["email"]:
            if email["email"] == params["filter_email"][0]:
                result.append(customer)

    return result


def filter_languages(master, params):
    result = []

    for customer in master:
        for language in customer["languages"]:
            if language == params["filter_language"][0]:
                result.append(customer)

    return result


def filter_room_type(master, params):

    result = []

    for customer in master:
        for item in customer["pms_details"]:
            if item["entity"] == "pms_booker":
                for book in item["data"]["bbooks"]:
                    if book["riRoomType"]["uuid"] == params["filter_room_type"]:
                        result.append(customer)
            elif item["entity"] == "pms_pri_guest":
                if item["data"]["riRoomType"]["uuid"] == params["filter_room_type"]:
                    result.append(customer)

    return result


def filter_book_price(master, params):

    result = []

    for customer in master:
        for item in customer["pms_details"]:
            if item["entity"] == "pms_booker":
                for book in item["data"]["bbooks"]:
                    if book["price"] == params["filter_book_price"]:
                        result.append(customer)
            elif item["entity"] == "pms_pri_guest":
                if item["data"]["riRoomType"]["uuid"] == params["filter_book_price"]:
                    result.append(customer)

    return result


def filter_room_code(master, params):

    result = []

    for customer in master:
        for item in customer["pms_details"]:
            if item["entity"] == "pms_booker":
                for book in item["data"]["bbooks"]:
                    if book["riRoom"]["uuid"] == params["filter_room_code"]:
                        result.append(customer)
            elif item["entity"] == "pms_pri_guest":
                if item["data"]["riRoom"]["uuid"] == params["filter_room_code"]:
                    result.append(customer)

    return result


def filter_guest_gender(master, params):

    result = []

    for customer in master:
        for item in customer["pms_details"]:
            if item["entity"] == "pms_booker":
                for book in item["data"]["bbooks"]:
                    for guest in book["bbookPGuests"]:
                        if guest["pguest"]["gender"] == params["filter_gender"]:
                            result.append(customer)
            else:
                for guest in item["data"]["bbookPGuests"]:
                    if guest["pguest"]["gender"] == params["filter_gender"]:
                        result.append(customer)

    return result


def filter_book_dates(master, type_, params):

    if type_ != "reservation_date":
        field = type_
    else:
        field = "createdAt"

    operator = params[f"filter_{type_}"]["condition"]

    result = []

    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    if operator == "Between":
        millis_from = params[f"filter_{type_}"]["date_range"]["from_"]
        millis_to = params[f"filter_{type_}"]["date_range"]["to"]

        date_from = (
            datetime.utcfromtimestamp(millis_from // 1000.0)
            .replace(microsecond=millis_from % 1000 * 1000)
            .strftime(time_format)
        )

        date_to = (
            datetime.utcfromtimestamp(millis_to // 1000.0)
            .replace(microsecond=millis_from % 1000 * 1000)
            .strftime(time_format)
        )
    else:
        millis_date = params[f"filter_{type_}"]["date"]
        date = (
            datetime.utcfromtimestamp(millis_date // 1000.0)
            .replace(microsecond=millis_date % 1000 * 1000)
            .strftime(time_format)
        )
    for customer in master:
        if len(customer["pms_details"]) > 0:
            for item in customer["pms_details"]:
                if item["entity"] == "pms_booker":
                    for book in item["data"]["bbooks"]:
                        if operator == "Equal to":
                            if datetime.strptime(
                                book[field], (time_format)
                            ) == datetime.strptime(date, time_format):
                                result.append(customer)
                        elif operator == "Less to":
                            if datetime.strptime(
                                book[field], time_format
                            ) < datetime.strptime(date, time_format):
                                result.append(customer)
                        elif operator == "Less than or equal to":
                            if datetime.strptime(
                                book[field], time_format
                            ) <= datetime.strptime(date, time_format):
                                result.append(customer)
                        elif operator == "Greater than":
                            if datetime.strptime(
                                book[field], time_format
                            ) > datetime.strptime(date, time_format):
                                result.append(customer)
                        elif operator == "Greater than or equal to":
                            if datetime.strptime(
                                book[field], time_format
                            ) >= datetime.strptime(date, time_format):
                                result.append(customer)
                        elif operator == "Different to":
                            if datetime.strptime(
                                book[field], time_format
                            ) != datetime.strptime(date, time_format):
                                result.append(customer)
                        elif operator == "Between":
                            if (
                                datetime.strptime(date_from, time_format)
                                <= datetime.strptime(book[field], time_format)
                                <= datetime.strptime(date_to, time_format)
                            ):
                                result.append(customer)
                elif item["entity"] == "pms_pri_guest":
                    if operator == "Equal to":
                        if datetime.strptime(
                            item["data"][field], time_format
                        ) == datetime.strptime(date, time_format):
                            result.append(customer)
                    elif operator == "Less to":
                        if datetime.strptime(
                            item["data"][field], time_format
                        ) < datetime.strptime(date, time_format):
                            result.append(customer)
                    elif operator == "Less than or equal to":
                        if datetime.strptime(
                            item["data"][field], time_format
                        ) <= datetime.strptime(date, time_format):
                            result.append(customer)
                    elif operator == "Greater than":
                        if datetime.strptime(
                            item["data"][field], time_format
                        ) > datetime.strptime(date, time_format):
                            result.append(customer)
                    elif operator == "Greater than or equal to":
                        if datetime.strptime(
                            item["data"][field], time_format
                        ) >= datetime.strptime(date, time_format):
                            result.append(customer)
                    elif operator == "Different to":
                        if datetime.strptime(
                            item["data"][field], time_format
                        ) != datetime.strptime(date, time_format):
                            result.append(customer)
                    elif operator == "Between":
                        if (
                            datetime.strptime(date_from, time_format)
                            <= datetime.strptime(item["data"][field], time_format)
                            <= datetime.strptime(date_to, time_format)
                        ):
                            result.append(customer)

    return result


def filter_master_checkin_checkout(data, type_, operator, params):

    if operator == "Between":

        millis_from = params[f"filter_{type_}"]["date_range"]["from_"]
        millis_to = params[f"filter_{type_}"]["date_range"]["to"]

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
            filter(
                lambda x: x["pms_details"]["data"][type_] >= date_from
                and x[type_] <= date_to,
                data,
            )
        )
    else:
        millis_date = params[f"filter_{type_}"]["date"]
        date = (
            datetime.utcfromtimestamp(millis_date // 1000.0)
            .replace(microsecond=millis_date % 1000 * 1000)
            .strftime("%Y-%m-%d")
        )

        if operator == "Equal to":
            result = list(filter(lambda x: x[type_] == date, data))
        elif operator == "Less to":
            result = list(filter(lambda x: x[type_] < date, data))
        elif operator == "Less than or equal to":
            result = list(filter(lambda x: x[type_] <= date, data))
        elif operator == "Greater than":
            result = list(filter(lambda x: x[type_] > date, data))
        elif operator == "Greater than or equal to":
            result = list(filter(lambda x: x[type_] >= date, data))
        elif operator == "Different to":
            result = list(filter(lambda x: x[type_] != date, data))

    return result


def filter_customer_creation_date(master, type_, params):

    operator = params[f"filter_{type_}"]["condition"]

    if operator == "Between":

        millis_from = params[f"filter_{type_}"]["date_range"]["from_"]
        millis_to = params[f"filter_{type_}"]["date_range"]["to"]

        date_from = (
            datetime.utcfromtimestamp(millis_from // 1000.0)
            .replace(microsecond=millis_from % 1000 * 1000)
            .strftime("%Y-%m-%dT%H:%M:%S.%f")
        )

        date_to = (
            datetime.utcfromtimestamp(millis_to // 1000.0)
            .replace(microsecond=millis_from % 1000 * 1000)
            .strftime("%Y-%m-%dT%H:%M:%S.%f")
        )

        result = list(
            filter(
                lambda x: datetime.strptime(date_from, "%Y-%m-%dT%H:%M:%S.%f").date()
                <= datetime.strptime(x[type_], "%Y-%m-%dT%H:%M:%S.%f").date()
                <= datetime.strptime(date_to, "%Y-%m-%dT%H:%M:%S.%f").date(),
                master,
            )
        )
    else:
        millis_date = params[f"filter_{type_}"]["date"]
        date = (
            datetime.utcfromtimestamp(millis_date // 1000.0)
            .replace(microsecond=millis_date % 1000 * 1000)
            .strftime("%Y-%m-%dT%H:%M:%S.%f")
        )

        if operator == "Equal to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], "%Y-%m-%dT%H:%M:%S.%f").date()
                    == datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").date(),
                    master,
                )
            )
        elif operator == "Less to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], "%Y-%m-%dT%H:%M:%S.%f").date()
                    < datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").date(),
                    master,
                )
            )
        elif operator == "Less than or equal to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], "%Y-%m-%dT%H:%M:%S.%f").date()
                    <= datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").date(),
                    master,
                )
            )
        elif operator == "Greater than":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], "%Y-%m-%dT%H:%M:%S.%f").date()
                    > datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").date(),
                    master,
                )
            )
        elif operator == "Greater than or equal to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], "%Y-%m-%dT%H:%M:%S.%f").date()
                    >= datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").date(),
                    master,
                )
            )
        elif operator == "Different to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], "%Y-%m-%dT%H:%M:%S.%f").date()
                    != datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f").date(),
                    master,
                )
            )

    return result


def filter_customer_birth_date(master, type_, params):

    operator = params[f"filter_{type_}"]["condition"]

    time_format = "%Y-%m-%d"

    if operator == "Between":

        millis_from = params[f"filter_{type_}"]["date_range"]["from_"]
        millis_to = params[f"filter_{type_}"]["date_range"]["to"]

        date_from = (
            datetime.utcfromtimestamp(millis_from // 1000.0)
            .replace(microsecond=millis_from % 1000 * 1000)
            .strftime(time_format)
        )

        date_to = (
            datetime.utcfromtimestamp(millis_to // 1000.0)
            .replace(microsecond=millis_from % 1000 * 1000)
            .strftime(time_format)
        )

        result = list(
            filter(
                lambda x: datetime.strptime(date_from, time_format).date()
                <= datetime.strptime(x[type_], time_format).date()
                <= datetime.strptime(date_to, time_format).date(),
                master,
            )
        )
    else:
        millis_date = params[f"filter_{type_}"]["date"]
        date = (
            datetime.utcfromtimestamp(millis_date // 1000.0)
            .replace(microsecond=millis_date % 1000 * 1000)
            .strftime(time_format)
        )

        if operator == "Equal to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], time_format).date()
                    == datetime.strptime(date, time_format).date(),
                    master,
                )
            )
        elif operator == "Less to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], time_format).date()
                    < datetime.strptime(date, time_format).date(),
                    master,
                )
            )
        elif operator == "Less than or equal to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], time_format).date()
                    <= datetime.strptime(date, time_format).date(),
                    master,
                )
            )
        elif operator == "Greater than":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], time_format).date()
                    > datetime.strptime(date, time_format).date(),
                    master,
                )
            )
        elif operator == "Greater than or equal to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], time_format).date()
                    >= datetime.strptime(date, time_format).date(),
                    master,
                )
            )
        elif operator == "Different to":
            result = list(
                filter(
                    lambda x: datetime.strptime(x[type_], time_format).date()
                    != datetime.strptime(date, time_format).date(),
                    master,
                )
            )

    return result


def filter_num_pax(master, type_, params):
    result = []

    for customer in master:
        for item in customer["pms_details"]:
            if item["entity"] == "pms_booker":
                for book in item["data"]["bbooks"]:
                    if book[type_] == params[f"filter_{type_}"]:
                        result.append(customer)
            elif item["entity"] == "pms_pri_guest":
                if item["data"][type_] == params[f"filter_{type_}"]:
                    result.append(customer)

    return result


def filter_book_price(master, params):

    operator = params["filter_book_price"]["condition"]

    result = []

    if operator == "Between":
        min_price = float(params["filter_book_price"]["price_range"]["min_price"])
        max_price = float(params["filter_book_price"]["price_range"]["max_price"])

    else:
        price = float(params["filter_book_price"]["price"])
    for customer in master:
        if len(customer["pms_details"]) > 0:
            for item in customer["pms_details"]:
                if item["entity"] == "pms_booker":
                    for book in item["data"]["bbooks"]:
                        if operator == "Equal to":
                            if book["price"] == price:
                                result.append(customer)
                        elif operator == "Less to":
                            if book["price"] < price:
                                result.append(customer)
                        elif operator == "Less than or equal to":
                            if book["price"] <= price:
                                result.append(customer)
                        elif operator == "Greater than":
                            if book["price"] > price:
                                result.append(customer)
                        elif operator == "Greater than or equal to":
                            if book["price"] >= price:
                                result.append(customer)
                        elif operator == "Different to":
                            if book["price"] != price:
                                result.append(customer)
                        elif operator == "Between":
                            if min_price <= book["price"] <= max_price:
                                result.append(customer)
                elif item["entity"] == "pms_pri_guest":
                    if operator == "Equal to":
                        if item["data"]["price"] == price:
                            result.append(customer)
                    elif operator == "Less to":
                        if item["data"]["price"] < price:
                            result.append(customer)
                    elif operator == "Less than or equal to":
                        if item["data"]["price"] <= price:
                            result.append(customer)
                    elif operator == "Greater than":
                        if item["data"]["price"] > price:
                            result.append(customer)
                    elif operator == "Greater than or equal to":
                        if item["data"]["price"] >= price:
                            result.append(customer)
                    elif operator == "Different to":
                        if item["data"]["price"] != price:
                            result.append(customer)
                    elif operator == "Between":
                        if min_price <= item["data"]["price"] <= max_price:
                            result.append(customer)
    return result
