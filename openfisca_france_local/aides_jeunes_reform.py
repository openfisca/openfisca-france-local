# -*- coding: utf-8 -*-
import yaml

from pathlib import Path
from numpy.core.defchararray import startswith

from openfisca_france.model.base import *
from openfisca_core import reforms

from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale


def is_age_eligible(individu, period, condition):

    condition_age = condition['value']
    individus_age = individu('age', period)

    operators = {
        '<': lambda individus_age, condition_age: individus_age < condition_age,
        '<=': lambda individus_age, condition_age: individus_age <= condition_age,
        '>': lambda individus_age, condition_age: individus_age > condition_age,
        '>=': lambda individus_age, condition_age: individus_age >= condition_age,
    }
    return operators[condition['operator']](individus_age, condition_age)


def is_department_eligible(individu, period, condition):
    depcom = individu.menage('depcom', period)
    return sum([startswith(depcom, code.encode('UTF-8'))for code in condition['values']])


def is_region_eligible(individu, period, condition):
    regcom = individu.menage('regcom', period)
    return sum([startswith(regcom, code.encode('UTF-8'))for code in condition['values']])


def is_regime_securite_sociale_eligible(individu, period, condition):
    regime_securite_sociale = individu('regime_securite_sociale', period)
    return sum([regime_securite_sociale == RegimeSecuriteSociale[regime] for regime in condition['includes']])


condition_table = {
    'age': is_age_eligible,
    'departements': is_department_eligible,
    'regions': is_region_eligible,
    'regime_securite_sociale': is_regime_securite_sociale_eligible,
}

type_table = {
    'float': float,
    'bool': bool,
}


def generate_variable(benefit):

    class NewAidesJeunesBenefitVariable(Variable):
        value_type = float  # hardcoded
        entity = Individu
        definition_period = MONTH

        def formula(individu, period):
            value_type = type_table[benefit['type']]
            amount = benefit.get('montant')
            conditions = benefit['conditions_generales']

            test_conditions = [(condition_table[condition['type']], condition)
                               for condition in conditions]

            eligibilities = [test[0](
                individu, period, test[1]) for test in test_conditions]

            total_eligibility = sum(eligibilities) == len(conditions)

            return amount * total_eligibility if value_type == float else total_eligibility
        # Ce return fonctionnera car nos aides n'ont que deux types : bool et float
        # mais ce n'est pas élégant. (surtout qu'il faut créer une deuxième variable value_type)

    NewAidesJeunesBenefitVariable.__name__ = benefit['slug']
    return NewAidesJeunesBenefitVariable


class aides_jeunes_reform_dynamic(reforms.Reform):
    root = '.'
    path = '../git_aides-jeunes/data/benefits/javascript/'
    current_path = f'{root}/{path}'

    class regcom(Variable):
        value_type = str
        max_length = 2
        entity = Menage
        label = 'Code INSEE (regcom) du lieu de résidence'
        definition_period = MONTH
        set_input = set_input_dispatch_by_period

    def extract_benefit_file_content(self, benefit_path):
        benefit: dict = yaml.safe_load(open(benefit_path))
        benefit['slug'] = benefit_path.split(
            '/')[-1].replace('-', '_').split('.')[0]
        return benefit

    def extract_benefits_paths(self, benefits_folder: str) -> "list[str]":
        def isYAMLfile(path: str): return str(path).endswith(
            '.yml') or str(path).endswith('.yaml')
        liste_fichiers = [
            str(benefit) for benefit in Path(benefits_folder).iterdir() if isYAMLfile(benefit)]
        return liste_fichiers

    def apply(self):
        try:
            self.add_variable(self.regcom)
            benefit_files_paths = self.extract_benefits_paths(
                self.current_path)
            for path in benefit_files_paths:
                self.add_variable(generate_variable(
                    self.extract_benefit_file_content(path)))
        except KeyError as e:
            raise KeyError(f"field {e} missing in file: {path}")
