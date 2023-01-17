from openfisca_france.model.base import (ParameterNode, Parameter)


def conditions_list_to_parameters(parameter_name: str, conditions: "list[dict]") -> ParameterNode:
    root_parameter = ParameterNode(parameter_name, data={})

    return root_parameter


def create_benefit_parameters(benefit: dict):
    conditions_generales = benefit['conditions_generales']

    return conditions_list_to_parameters(benefit["slug"], conditions_generales)
