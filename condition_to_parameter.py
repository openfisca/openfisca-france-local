from openfisca_france.model.base import (ParameterNode, Parameter)


def condition_to_parameter(condition: dict) -> ParameterNode:

    def generate_age_parameter() -> ParameterNode:

        condition_parameter = ParameterNode(condition_type, data={})
        return condition_parameter

    def generate_simple_parameter():

        return Parameter(condition_type, data={})

    condition_table: dict = {
        "age": generate_age_parameter,
    }

    condition_type: str = condition["type"]

    if condition_type in condition_table.keys():
        condition_parameter = condition_table[condition_type]()
    else:
        condition_parameter = generate_simple_parameter()
    return condition_parameter


def conditions_list_to_parameters(parameter_name: str, conditions: "list[dict]") -> ParameterNode:
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


def create_benefit_parameters(benefit: dict):
    conditions_generales = benefit['conditions_generales']

    return conditions_list_to_parameters(benefit["slug"], conditions_generales)
