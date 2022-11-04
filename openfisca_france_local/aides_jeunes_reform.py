# -*- coding: utf-8 -*-

from openfisca_france.model.base import *
from openfisca_core import reforms


# from numpy.core.defchararray import startswith

import yaml


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

    NewAidesJeunesBenefitVariable.__name__ = benefit['slug']
    return NewAidesJeunesBenefitVariable


class aides_jeunes_reform_dynamic(reforms.Reform):

    def extract_benefit_file_content(self, benefit_path):
        benefit: dict = yaml.safe_load(open(benefit_path))
        benefit['slug'] = benefit_path.split(
            '/')[-1].replace('-', '_').split('.')[0]
        return benefit

    def apply(self):
        benefit_file_path = '../git_aides-jeunes/data/benefits/javascript/etat-aide-nationale-exceptionnelle-au-brevet-daptitude-aux-fonctions-danimateur-bafa.yml'

        self.add_variable(generate_variable(
            self.extract_benefit_file_content(benefit_file_path)))
