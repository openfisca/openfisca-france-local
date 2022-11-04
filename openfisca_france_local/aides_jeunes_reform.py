# -*- coding: utf-8 -*-

from openfisca_france.model.base import *
from openfisca_core import reforms


# from numpy.core.defchararray import startswith

import yaml

yaml_content = """slug: etat-aide-nationale-exceptionnelle-au-brevet-daptitude-aux-fonctions-danimateur-bafa
conditions_generales:
  - type: age
    operator: ">="
    value: 17
type: float
periodicite: ponctuelle
montant: 200
"""
aide = yaml.safe_load(yaml_content)


def generate_variable(benefit):

    class NewAidesJeunesBenefitVariable(Variable):
        value_type = float  # Hardcoded
        entity = Individu
        definition_period = MONTH

        def formula(individu, period):
            amount = benefit['montant']
            # age
            condition = benefit['conditions_generales'][0]
            variable_name = condition['type']
            eligibility = individu(variable_name, period) >= condition['value']
            # departement
            # eligibility = startswith(individu.menage('depcom', period), condition["values"][0])
            return amount * eligibility

    NewAidesJeunesBenefitVariable.__name__ = benefit['slug'].replace('-', '_')
    return NewAidesJeunesBenefitVariable


class aides_jeunes_reform_dynamic(reforms.Reform):

    def apply(self):

        self.add_variable(generate_variable(aide))
