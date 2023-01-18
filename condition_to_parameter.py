from openfisca_france.model.base import (ParameterNode, Parameter)


def condition_to_parameter(condition: dict) -> ParameterNode:

    def generate_age_parameter(condition: dict) -> ParameterNode:
        parameter_operator: str = comparison_operators[condition["operator"]]
        condition_parameter = ParameterNode(condition_type, data={
            parameter_operator: {
                date: {
                    "value": condition["value"]},
            }
        })
        return condition_parameter

    def generate_quotient_familial_parameter(condition: dict) -> ParameterNode:
        parameter_operator: str = comparison_operators[condition["operator"]]

        condition_parameter = ParameterNode(condition_type, data={
            condition["period"]: {
                parameter_operator: {
                    date: {
                        "value": condition["value"]
                    }
                }
            }
        })
        return condition_parameter

    def generate_regime_securite_sociale_parameter(
            condition: dict) -> Parameter:
        return Parameter(condition_type, data={
            date: {
                "value": condition["includes"]
            }
        })

    def generate_simple_parameter(condition: dict):
        if len(condition) == 1:
            value = {"value": True}
        else:
            value = {"value": condition["values"]}

        return Parameter(condition_type, data={date: value})

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


def conditions_list_to_parameters(
        parameter_name: str, conditions: "list[dict]") -> ParameterNode:
    root_parameter = ParameterNode(parameter_name, data={})
    node_parameters: "list[ParameterNode]" = [
        condition_to_parameter(condition) for condition in conditions
    ]
    for node in node_parameters:
        if node.name in root_parameter.children:
            root_parameter.children[node.name].merge(node)
        else:
            root_parameter.add_child(node.name, node)
    return root_parameter


def create_benefit_parameters(benefit: dict) -> ParameterNode:
    conditions_generales = benefit['conditions_generales']

    return conditions_list_to_parameters(benefit["slug"], conditions_generales)
