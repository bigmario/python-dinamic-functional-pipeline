# -*- coding: utf-8 -*-
"""Dinamic pipeline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XRMwnh6O9nxNWo3o17b06SrQwfILeGLr

Mario Castro <mariocastro.pva@gmail.com>

30-12-2021
"""

from functional_pipeline import pipeline, String, join


class CampaignCriteria:
    @classmethod
    def criteria_selector(cls, type, *args, **kwargs):
        return getattr(cls, f"_client_{type}")(*args, **kwargs)

    @classmethod
    def _client_filter_name(cls, *args, **kwargs):
        """
        Busca nombres que comiencen por J
        """
        function = (filter, String.startswith("J"))
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


# lista de funciones a ejecutar
function_list = ["filter_name", "map_names", "join_names"]

# arreglo de data a tratar
names = [
    "John",
    "James",
    "Bill",
    "Tiffany",
    "Jamie",
]

# se genera dinamicamente la lista de funciones a ejecutar,
# buscandolas en la clase CampaignCriteria segun la lista de funciones
# suministrada
pipe = [CampaignCriteria.criteria_selector(type) for type in function_list]

# se ejecuta el pipeline
result = pipeline(names, pipe)


print(result)
