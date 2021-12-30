from functional_pipeline import join, lens


class CampaignCriteria:
    @classmethod
    def criteria_selector(cls, type, *args, **kwargs):
        return getattr(cls, f"_client_{type}")(*args, **kwargs)

    @classmethod
    def _client_filter_name(cls, *args, **kwargs):
        """
        Busca nombres que comiencen por J
        """
        function = (
            filter,
            lambda person: lens("pguest.name")(person).startswith(kwargs["letter"]),
        )
        return function

    @classmethod
    def _client_filter_room_type(cls, *args, **kwargs):
        """
        Busca nombres que comiencen por J
        """
        function = (
            filter,
            lambda room_type: lens("bbooks.0.riRoomType.id")(room_type)
            == kwargs["room_id"],
        )
        return function

    @classmethod
    def _client_filter_by_tenant_id(cls, *args, **kwargs):
        """
        Busca nombres que comiencen por J
        """
        function = (
            filter,
            lambda tenant: lens("stenant.keycloakTenantId")(tenant)
            == kwargs["tenant_id"],
        )
        return function

    @classmethod
    def _client_map_names(cls, *args, **kwargs):
        """
        Agrega el apellido Smith a cada nombre
        """
        function = (map, lambda x: x + " Smith")
        return function

    @classmethod
    def _client_join_names(cls, *args, **kwargs):
        """
        Une los nombres en una cadena
        """
        function = join(", ")
        return function
