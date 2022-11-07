# -*- coding: utf-8 -*-

from openfisca_france.model.base import *
from openfisca_core import reforms


from numpy.core.defchararray import startswith

import yaml


def generate_variable(benefit):

    class NewAidesJeunesBenefitVariable(Variable):
        value_type = float  # Hardcoded
        entity = Individu
        definition_period = MONTH

        def formula(individu, period):
            amount = benefit['montant']
            # age
            condition_age = benefit['conditions_generales'][0]
            variable_name = condition_age['type']
            eligibility_age = individu(
                variable_name, period) >= condition_age['value']
            # departement
            condition_departement = benefit['conditions_generales'][1]
            eligibility_departement = startswith(individu.menage(
                'depcom', period), condition_departement["values"][0].encode('UTF-8'))
            eligibility = eligibility_age & eligibility_departement
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
        benefit_files_paths = [
            # '../git_aides-jeunes/data/benefits/javascript/etat-aide-nationale-exceptionnelle-au-brevet-daptitude-aux-fonctions-danimateur-bafa.yml',
            # '../git_aides-jeunes/data/benefits/javascript/caf-aide-nationale-bafa.yml',
            '../git_aides-jeunes/data/benefits/javascript/caf-ain-aide-bafa-session-generale.yml',
        ]
        for path in benefit_files_paths:
            self.add_variable(generate_variable(
                self.extract_benefit_file_content(path)))
