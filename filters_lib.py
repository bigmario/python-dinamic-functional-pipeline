from functional_pipeline import join, lens
from helpers import filter_resellers, filter_books


class CampaignCriteria:
    @classmethod
    def criteria_selector(cls, type, *args, **kwargs):
        return getattr(cls, f"_client_{type}")(*args, **kwargs)

    @classmethod
    def _client_filter_name_by_initial(cls, *args, **kwargs):
        """ """
        function = (
            filter,
            lambda person: lens("pguest.name")(person).startswith(kwargs["letter"]),
        )
        return function

    @classmethod
    def _client_filter_room_type(cls, *args, **kwargs):
        """ """
        function = (
            filter,
            lambda room_type: lens("bbooks.0.riRoomType.id")(room_type)
            == kwargs["room_id"],
        )
        return function

    @classmethod
    def _client_filter_by_tenant_id(cls, *args, **kwargs):
        """ """
        function = (
            filter,
            lambda tenant: lens("stenant.keycloakTenantId")(tenant)
            == kwargs["tenant_id"],
        )
        return function

    @classmethod
    def _client_filter_number_of_childrens(cls, *args, **kwargs):
        """
        Agrega el apellido Smith a cada nombre
        """
        function = (
            filter,
            lambda num_childrens: lens("bbooks.0.children")(num_childrens)
            == kwargs["childrens_num"],
        )
        return function

    @classmethod
    def _client_filter_meal_plan(cls, *args, **kwargs):
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
    def _client_filter_number_of_nights(cls, *args, **kwargs):
        """
        Filtra por noches de la estancia
        """
        function = (
            filter,
            lambda num_nights: lens("bbooks.0.nights")(num_nights)
            == kwargs["nights_num"],
        )
        return function

    @classmethod
    def _client_filter_email(cls, *args, **kwargs):
        """
        Filtra por email
        """
        function = (
            filter,
            lambda email: lens("pguest.email")(email) == kwargs["email"],
        )

        return function

    @classmethod
    def _client_filter_books(cls, *args, **kwargs):
        """
        Recorrer libros
        """
        function = lambda item: filter_books(item)

        return function
