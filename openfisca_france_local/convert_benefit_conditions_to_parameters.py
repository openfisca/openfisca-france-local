from openfisca_france.model.base import ParameterNode


def condition_to_parameter_data(condition: dict) -> dict:
    def generate_operator_parameter_data(condition: dict) -> dict:
        parameter_operator: str = comparison_operators[condition['operator']]
        return {
            condition_type: {
                parameter_operator: {
                    'values': {openfisca_parameter_date: {
                        'value': condition['value']}},
                    }
                }
            }

    def generate_quotient_familial_parameter_data(condition: dict) -> dict:
        parameter_operator: str = comparison_operators[condition['operator']]
        return {
            condition_type: {
                condition['period']: {
                    parameter_operator: {
                        'values': {openfisca_parameter_date: {
                            'value': condition['value']
                            }}
                        }
                    }
                }
            }

    def generate_regime_securite_sociale_parameter_data(condition: dict) -> dict:
        def create_regime_data(constraint) -> dict:
            return {
                constraint: {
                    'values': {
                        openfisca_parameter_date: {'value': condition[constraint]}}
                    }}

        if 'includes' in condition.keys() and 'excludes' in condition.keys():
            raise NotImplementedError(
                'Condition "regime_securite_sociale" does not support having'
                ' both "includes" and "excludes" properties.\n'
                'Please check the YAML file.'
                )

        constraint: str = 'includes' if 'includes' in condition.keys() else 'excludes'

        return {condition_type: create_regime_data(constraint)}

    def generate_common_parameter_data(condition: dict) -> dict:
        if len(condition) == 1:
            value = {'value': True}
        else:
            value = {'value': condition['values']}

        return {
            condition_type: {
                'values': {openfisca_parameter_date: value}
                }
            }

    condition_table: dict = {
        'age': generate_operator_parameter_data,
        'taux_incapacite': generate_operator_parameter_data,
        'quotient_familial': generate_quotient_familial_parameter_data,
        'regime_securite_sociale': generate_regime_securite_sociale_parameter_data,
        }

    openfisca_parameter_date = '2020-01-01'

    comparison_operators = {
        '<=': 'maximum_inclusif',
        '>=': 'minimum_inclusif',
        '<': 'maximum_exclusif',
        '>': 'minimum_exclusif',
        }

    condition_type: str = condition['type']

    if condition_type in condition_table:
        condition_parameter_data = condition_table[condition_type](condition)
    else:
        condition_parameter_data = generate_common_parameter_data(condition)

    return condition_parameter_data


def conditions_to_node_data(conditions: 'list[dict]') -> dict:

    conditions_formatted = [
        condition_to_parameter_data(condition)
        for condition in conditions
        ]

    data: dict = {'conditions': {}}

    for condition in conditions_formatted:
        for key in condition:
            if key in data['conditions']:
                data['conditions'][key].update(condition[key])
            else:
                data['conditions'].update(condition)

    return data


def profils_to_node_data(profils: 'list[dict]'):
    def create_profils_field(data: dict, profil: dict):
        if profil['type'] not in data['profils']:
            data['profils'].update({profil['type']: {}})

    def add_profil_with_conditions(data: dict, profil: dict):
        def condition_already_exists_in_node(profil_condition, conditions_in_node_data) -> bool:
            conditions_with_operator_fields = ['age', 'quotient_familial', 'situation_handicap']

            conditions_types = profil_condition.keys()

            if len(conditions_types) == 0:
                return False

            for type in conditions_types:
                if type in conditions_in_node_data:
                    if type in conditions_with_operator_fields:
                        operator = list(profil_condition[type])[0]
                        return operator in conditions_in_node_data[type]
                    else:
                        return True
            return False

        if 'conditions' not in data['profils'][profil['type']]:
            data['profils'][profil['type']] = {'conditions': {}}

        profil_condition = data['profils'][profil['type']]['conditions']
        conditions_in_node_data = conditions_to_node_data(profil['conditions'])['conditions']

        if condition_already_exists_in_node(profil_condition, conditions_in_node_data):
            raise NotImplementedError(
                'La réforme dynamique ne gère pas encore les aides avec deux profils de même type qui ont des conditions de même type pour chacun de ses profils identiques'
                )

        profil_condition.update(conditions_in_node_data)

    def add_boolean_profil(data: dict, profil: dict):
        date = '2020-01-01'
        data['profils'][profil['type']] = {date: {'value': True}}

    data: dict = {'profils': {}}

    for profil in profils:
        create_profils_field(data, profil)
        if 'conditions' in profil:
            add_profil_with_conditions(data, profil)
        else:
            add_boolean_profil(data, profil)

    return data


def generate_amount_parameter_data(montant):
    date = '2020-01-01'

    return {'montant': {date: {'value': montant}}} if montant else {}


def convert_benefit_conditions_to_parameters(benefit: dict) -> ParameterNode:
    amount_data = generate_amount_parameter_data(benefit.get('montant'))

    conditions_generales = benefit['conditions_generales']

    conditions_generales_data = conditions_to_node_data(conditions_generales)

    node_data: dict = {}
    node_data.update(conditions_generales_data)
    node_data.update(amount_data)

    profils = benefit.get('profils')
    if profils:
        profils_data = profils_to_node_data(profils)
        node_data.update(profils_data)

    return ParameterNode(benefit['slug'], data=node_data)
