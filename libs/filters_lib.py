from functional_pipeline import join, lens
from libs.helpers import (
    filter_book_dates,
    filter_customer_creation_date,
    filter_customer_birth_date,
    filter_room_type,
    filter_email,
    filter_languages,
    filter_num_pax,
    filter_room_code,
    filter_book_price,
    filter_resellers,
    filter_guest_gender,
    filter_master_checkin_checkout,
)


class CampaignCriteria:
    @classmethod
    def criteria_selector(cls, type, *args, **kwargs):
        return getattr(cls, f"_customer_{type}")(*args, **kwargs)

    # SECCION PERFIL

    @classmethod
    def _customer_filter_country(cls, *args, **kwargs):
        """
        Filter by country
        """
        function = (
            filter,
            lambda country: lens("country")(country) == kwargs["filter_country"],
        )

        return function

    @classmethod
    def _customer_filter_city(cls, *args, **kwargs):
        """
        Filter by city
        """
        function = (
            filter,
            lambda city: lens("city")(city) == kwargs["filter_city"],
        )

        return function

    @classmethod
    def _customer_filter_company(cls, *args, **kwargs):
        """
        Filter by city
        """
        function = (
            filter,
            lambda company: lens("city")(company) == kwargs["filter_company"],
        )

        return function

    @classmethod
    def _customer_filter_create_at(cls, *args, **kwargs):
        """
        Recorrer libros
        """
        function = lambda item: filter_customer_creation_date(item, "create_at", kwargs)

        return function

    @classmethod
    def _customer_filter_email(cls, *args, **kwargs):
        """
        Filtra por email
        """
        function = lambda email: filter_email(email, kwargs)

        return function

    @classmethod
    def _customer_filter_language(cls, *args, **kwargs):
        """
        Filtra por lenguaje
        """
        function = lambda language: filter_languages(language, kwargs)

        return function

    @classmethod
    def _customer_filter_gender(cls, *args, **kwargs):
        """
        Filtra por genero
        """

        function = (
            filter,
            lambda person: lens("gender")(person) == kwargs["filter_gender"],
        )

        return function

    @classmethod
    def _customer_filter_civil_status(cls, *args, **kwargs):
        """
        Filtra por estado civil
        """

        function = (
            filter,
            lambda person: lens("civil_status")(person)
            == kwargs["filter_civil_status"],
        )

        return function

    @classmethod
    def _customer_filter_birthdate(cls, *args, **kwargs):
        """
        Filtrar por birthdate
        """
        function = lambda birthdate: filter_customer_birth_date(
            birthdate, "birthdate", kwargs
        )

        return function

    # SECCION HOSPEDAJE

    @classmethod
    def _customer_filter_checkin(cls, *args, **kwargs):
        """
        Recorrer libros
        """
        # function = lambda item: filter_checkin_checkout(item, "checkin", kwargs)
        function = lambda item: filter_book_dates(item, "checkin", kwargs)

        return function

    @classmethod
    def _customer_filter_checkout(cls, *args, **kwargs):
        """
        Recorrer libros
        """
        function = lambda item: filter_book_dates(item, "checkout", kwargs)

        return function

    @classmethod
    def _customer_filter_room_type(cls, *args, **kwargs):
        """
        Recorrer libros
        """
        function = lambda item: filter_room_type(item, kwargs)

        return function

    @classmethod
    def _customer_filter_room_code(cls, *args, **kwargs):
        """
        Recorrer libros
        """
        function = lambda item: filter_room_code(item, kwargs)

        return function

    @classmethod
    def _customer_filter_adults(cls, *args, **kwargs):
        """
        Filtra por numero de Adultos
        """
        function = lambda num_adults: filter_num_pax(num_adults, "adults", kwargs)
        return function

    @classmethod
    def _customer_filter_children(cls, *args, **kwargs):
        """
        Filtra por numero de niños
        """
        function = lambda num_children: filter_num_pax(num_children, "children", kwargs)
        return function

    @classmethod
    def _customer_filter_reservation_date(cls, *args, **kwargs):
        """
        Recorrer libros
        """
        function = lambda item: filter_book_dates(item, "reservation_date", kwargs)

        return function

    @classmethod
    def _customer_filter_book_price(cls, *args, **kwargs):
        """
        Recorrer libros
        """
        function = lambda item: filter_book_price(item, kwargs)

        return function

    # MISC

    @classmethod
    def _customer_filter_name_by_initial(cls, *args, **kwargs):
        """ """
        function = (
            filter,
            lambda person: lens("name")(person).startswith(kwargs["letter"]),
        )
        return function

    @classmethod
    def _customer_filter_by_tenant_id(cls, *args, **kwargs):
        """ """
        function = (
            filter,
            lambda tenant: lens("pms_details.tenant_id")(tenant)
            == kwargs["filter_by_tenant_id"],
        )
        return function

    @classmethod
    def _customer_filter_meal_plan(cls, *args, **kwargs):
        """
        Une los nombres en una cadena
        """
        function = (
            filter,
            lambda room_type: lens("bbooks.0.riMealPlan.id")(room_type)
            == kwargs["room_id"],
        )
        return function

    @classmethod
    def _customer_filter_number_of_nights(cls, *args, **kwargs):
        """
        Filtra por noches de la estancia
        """
        function = (
            filter,
            lambda num_nights: lens("bbooks.0.nights")(num_nights)
            == kwargs["nights_num"],
        )
        return function
