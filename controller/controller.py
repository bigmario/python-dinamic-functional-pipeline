from service import CriteriaService


def run():

    params = CriteriaService.clean_input()

    print(
        params.get("sections"),
        params.get("function_list"),
        params.get("param_dict"),
        sep="\n",
    )

    CriteriaService.main(**params)
