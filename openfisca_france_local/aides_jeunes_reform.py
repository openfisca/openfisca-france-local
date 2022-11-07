# -*- coding: utf-8 -*-

from openfisca_france.model.base import *
from openfisca_core import reforms


from numpy.core.defchararray import startswith
from numpy import array as np_array

import yaml


def generate_variable(benefit):

    class NewAidesJeunesBenefitVariable(Variable):
        value_type = float  # Hardcoded
        entity = Individu
        definition_period = MONTH

        def formula(individu, period):
            eligibilitys = []
            amount = benefit['montant']
            conditions = benefit['conditions_generales']
            for condition in conditions:
                # age
                if condition['type'] == 'age':
                    variable_name = condition['type']
                    eligibilitys.append(individu(
                        variable_name, period) >= condition['value'])
                # departement
                if condition['type'] == 'departements':
                    eligibilitys.append(startswith(individu.menage(
                        'depcom', period), condition["values"][0].encode('UTF-8')))
            total_eligibility = np_array(list(map(all, zip(*eligibilitys))))

            return amount * total_eligibility

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
            '../git_aides-jeunes/data/benefits/javascript/etat-aide-nationale-exceptionnelle-au-brevet-daptitude-aux-fonctions-danimateur-bafa.yml',
            '../git_aides-jeunes/data/benefits/javascript/caf-aide-nationale-bafa.yml',
            '../git_aides-jeunes/data/benefits/javascript/caf-ain-aide-bafa-session-generale.yml',
        ]
        for path in benefit_files_paths:
            self.add_variable(generate_variable(
                self.extract_benefit_file_content(path)))
