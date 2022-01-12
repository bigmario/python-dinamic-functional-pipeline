import traceback

from pprint import pprint

from functools import reduce

from functional_pipeline import pipeline

from libs.file_manager import get_criteria, get_data_file, put_data

from libs.filters_lib import CampaignCriteria

from libs.helpers import clean_null_terms

from repository import CriteriaRepo


class CriteriaService(CriteriaRepo):
    def __init__(self):
        super().__init__()

    def clean_input():
        # Se reciben los criterios de filtrado
        criteria_function_list_raw = get_criteria()

        # Secciones (Profile, Accommodation, etc.)
        sections = [
            item
            for item in criteria_function_list_raw
            if criteria_function_list_raw[item] is not None
        ]

        # Lista de funciones o filtros a ejecutar (sin aplanar)
        functions_raw = [item for item in criteria_function_list_raw.values()]

        # Lista de funciones o filtros a ejecutar (aplanada)
        functions_clean = [item for item in functions_raw if item is not None]

        # Objeto con los parametros a aplicar en cada filtro
        flatten_filters = reduce(lambda d, src: d.update(src) or d, functions_clean, {})

        criteria_function_list_clean = [
            criteria_key
            for criteria_key in flatten_filters
            if flatten_filters[criteria_key] is not None
        ]

        # Objeto con los parametros a aplicar en cada filtro (Clean)
        param_dict_clean = [
            item
            for item in flatten_filters.items()
            if flatten_filters[item[0]] is not None
        ]

        # arreglo de data a filtrar
        customer_id_list = get_data_file()

        # Query para obtener customers segun lista de Id's
        customers = [
            customer
            for customer in CriteriaRepo().get_customer_from_id(customer_id_list)
        ]

        # Se eliminan los parametros nulos
        clean_null_params = clean_null_terms(dict(param_dict_clean))

        # Objeto con toda la "input data" limpia
        result = {
            "sections": sections,
            "function_list": criteria_function_list_clean,
            "data": customers,
            "param_dict": clean_null_params,
        }

        return result

    def main(sections, function_list, data, param_dict):

        # instancia de la clase contenedora de funciones
        function_selector = CampaignCriteria()

        # se genera dinamicamente la lista de funciones a ejecutar,
        # buscandolas en la clase CampaignCriteria segun la lista de funciones
        # suministrada
        pipe = [
            function_selector.criteria_selector(type, **param_dict)
            for type in function_list
        ]

        # se ejecuta el pipeline

        try:
            result = list(pipeline(data, pipe))

            # Se escribe el resultado a disco
            put_data(result)

            # # Resultado por pantalla
            # pprint(result)

            # Conteo de customers que cumplen con los criterios de filtrado
            print("\nNumber of resulting customers: ", len(result))
        except:
            err = traceback.format_exc(1)
            print(f"Error: {err}")
