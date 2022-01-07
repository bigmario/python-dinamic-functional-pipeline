from pprint import pprint
from datetime import datetime
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


def filter_email(master, params):
    result = []

    for item in master:
        for email in item["email"]:
            if email["email"] == params["filter_email"]:
                result.append(item)

    return result


def filter_languages(master, params):
    result = []

    for item in master:
        for language in item["languages"]:
            if language == params["filter_language"]:
                result.append(item)

    return result


def filter_room_type(master, params):

    result = []

    for item in master:
        for book in item["bbooks"]:
            if book["riRoomType"]["id"] == params["filter_room_type"]:
                result.append(item)

    return result


def filter_guest_gender(master, params):

    result = []

    for customer in master:
        for item in customer["pms_details"]:
            if item["entity"] == "pms_booker":
                for book in item["data"]["bbooks"]:
                    for guest in book["bbookPGuests"]:
                        if guest["pguest"]["gender"] == params["filter_gender"]:
                            print("SI")
                            result.append(item)
            else:
                print("NO")
                for guest in item["data"]["bbookPGuests"]:
                    if guest["pguest"]["gender"] == params["filter_gender"]:
                        result.append(item)

    return result


def filter_guest_checkin_checkout(master, type_, params):

    operator = params[f"filter_{type_}"]["condition"]

    result = []

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
    else:
        millis_date = params[f"filter_{type_}"]["date"]
        date = (
            datetime.utcfromtimestamp(millis_date // 1000.0)
            .replace(microsecond=millis_date % 1000 * 1000)
            .strftime("%Y-%m-%d")
        )
    for customer in master:
        if len(customer["pms_details"]) > 0:
            for item in customer["pms_details"]:
                if item["entity"] == "pms_booker":
                    for book in item["data"]["bbooks"]:
                        if operator == "Equal to":
                            if datetime.strptime(
                                book[type_], "%Y-%m-%d"
                            ) == datetime.strptime(date, "%Y-%m-%d"):
                                result.append(customer)
                        elif operator == "Less to":
                            if datetime.strptime(
                                book[type_], "%Y-%m-%d"
                            ) < datetime.strptime(date, "%Y-%m-%d"):
                                result.append(customer)
                        elif operator == "Less than or equal to":
                            if datetime.strptime(
                                book[type_], "%Y-%m-%d"
                            ) <= datetime.strptime(date, "%Y-%m-%d"):
                                result.append(customer)
                        elif operator == "Greater than":
                            if datetime.strptime(
                                book[type_], "%Y-%m-%d"
                            ) > datetime.strptime(date, "%Y-%m-%d"):
                                result.append(customer)
                        elif operator == "Greater than or equal to":
                            if datetime.strptime(
                                book[type_], "%Y-%m-%d"
                            ) >= datetime.strptime(date, "%Y-%m-%d"):
                                result.append(customer)
                        elif operator == "Different to":
                            if datetime.strptime(
                                book[type_], "%Y-%m-%d"
                            ) != datetime.strptime(date, "%Y-%m-%d"):
                                result.append(customer)
                        elif operator == "Between":
                            if (
                                datetime.strptime(date_from, "%Y-%m-%d")
                                <= datetime.strptime(book[type_], "%Y-%m-%d")
                                <= datetime.strptime(date_to, "%Y-%m-%d")
                            ):
                                result.append(customer)
                elif item["entity"] == "pms_pri_guest":
                    if operator == "Equal to":
                        if datetime.strptime(
                            item["data"][type_], "%Y-%m-%d"
                        ) == datetime.strptime(date, "%Y-%m-%d"):
                            result.append(customer)
                    elif operator == "Less to":
                        if datetime.strptime(
                            item["data"][type_], "%Y-%m-%d"
                        ) < datetime.strptime(date, "%Y-%m-%d"):
                            result.append(customer)
                    elif operator == "Less than or equal to":
                        if datetime.strptime(
                            item["data"][type_], "%Y-%m-%d"
                        ) <= datetime.strptime(date, "%Y-%m-%d"):
                            result.append(customer)
                    elif operator == "Greater than":
                        if datetime.strptime(
                            item["data"][type_], "%Y-%m-%d"
                        ) > datetime.strptime(date, "%Y-%m-%d"):
                            result.append(customer)
                    elif operator == "Greater than or equal to":
                        if datetime.strptime(
                            item["data"][type_], "%Y-%m-%d"
                        ) >= datetime.strptime(date, "%Y-%m-%d"):
                            result.append(customer)
                    elif operator == "Different to":
                        if datetime.strptime(
                            item["data"][type_], "%Y-%m-%d"
                        ) != datetime.strptime(date, "%Y-%m-%d"):
                            result.append(customer)
                    elif operator == "Between":
                        if (
                            datetime.strptime(date_from, "%Y-%m-%d")
                            <= datetime.strptime(item["data"][type_], "%Y-%m-%d")
                            <= datetime.strptime(date_to, "%Y-%m-%d")
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
