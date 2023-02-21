from openfisca_france.model.base import (ParameterNode, Parameter)


def condition_to_parameter(condition: dict) -> dict:

    def generate_age_parameter(condition: dict) -> dict:
        parameter_operator: str = comparison_operators[condition["operator"]]
        data: dict = {
            condition_type: {
                parameter_operator: {
                    "values": {date: {
                        "value": condition["value"]}},
                }
            }
        }
        return data

    def generate_quotient_familial_parameter(condition: dict) -> dict:
        parameter_operator: str = comparison_operators[condition["operator"]]

        data = {
            condition_type: {
                condition["period"]: {
                    parameter_operator: {
                        "values": {date: {
                            "value": condition["value"]
                        }}
                    }
                }
            }
        }
        return data

    def generate_regime_securite_sociale_parameter(
            condition: dict) -> ParameterNode:
        data: dict = {condition_type: {}}
        if "includes" in condition.keys():
            data[condition_type] = {
                "includes": {
                    "values": {
                        date: {"value": condition["includes"]}}
                }}

        if "excludes" in condition.keys():
            data[condition_type].update({
                "excludes": {
                    "values": {
                        date: {"value": condition["excludes"]}}
                }})

        return data

    def generate_simple_parameter(condition: dict) -> Parameter:
        if len(condition) == 1:
            value = {"value": True}
        else:
            value = {"value": condition["values"]}
        data: dict = {
            condition_type: {
                "values": {date: value}
            }
        }
        return data

    condition_table: dict = {
        "age": generate_age_parameter,
        "quotient_familial": generate_quotient_familial_parameter,
        "regime_securite_sociale": generate_regime_securite_sociale_parameter,
    }

    date = "2020-01-01"

    comparison_operators = {
        '<=': "maximum",
        '>=': "minimum",
        '<': "strictement_inferieur",
        '>': "strictement_superieur",
    }

    condition_type: str = condition["type"]

    if condition_type in condition_table.keys():
        condition_parameter = condition_table[condition_type](condition)
    else:
        condition_parameter = generate_simple_parameter(condition)
    return condition_parameter


def conditions_to_node_data(conditions: "list[dict]") -> dict:
    conditions_formated: "list[dict]" = [condition_to_parameter(
        condition) for condition in conditions]
    data: dict = {"conditions": {}}
    for condition in conditions_formated:
        for key in condition.keys():
            if key in data["conditions"]:
                data["conditions"][key].update(condition[key])
            else:
                data["conditions"].update(condition)

    return data


def create_benefit_parameters(benefit: dict) -> ParameterNode:
    conditions_generales = benefit['conditions_generales']
    conditions_generales_dict = conditions_to_node_data(
        conditions_generales)

    node_data: dict = {}
    node_data.update(conditions_generales_dict)

    profils: list[dict] = benefit.get("profils")
    if profils:
        profil_dict: dict = {'profils': {}}
        for profil in profils:
            profil_dict['profils'].update(
                {profil['type']: conditions_to_node_data(profil["conditions"])})

        node_data.update(profil_dict)

    return ParameterNode(benefit["slug"], data=node_data)
