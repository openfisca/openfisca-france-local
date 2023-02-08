# -*- coding: utf-8 -*-

import yaml
import operator

from pathlib import Path
from numpy.core.defchararray import startswith
import numpy as np

from openfisca_france.model.base import (
    TypesMention, TypesActivite, Variable, Individu, MONTH)
from openfisca_core import reforms
from openfisca_core.periods import Period


from openfisca_core.populations.population import Population
from openfisca_france.model.prestations.education import (
    TypesScolarite, TypesClasse)
from openfisca_france.model.caracteristiques_socio_demographiques.logement import (
    TypesCodeInseeRegion)
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import GroupeSpecialitesFormation
from openfisca_france.model.base import ParameterNode
from openfisca_core.parameters.parameter_node_at_instant import ParameterNodeAtInstant
from condition_to_parameter import create_benefit_parameters

operations = {
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
}


def is_age_eligible(individu: Population, period: Period, condition: dict, parameters=None):
    operations_text = {
        'strictement_inferieur': operator.lt,
        'maximum': operator.le,
        'strictement_superieur': operator.gt,
        'minimum': operator.ge,
    }

    individus_age = individu('age', period)
    condition_age = parameters.age

    age_constraints = [(operations_text[constraint],  condition_age[constraint])
                       for constraint in condition_age]

    eligibilities = [constraint[0](individus_age, constraint[1])
                     for constraint in age_constraints]
    return sum(eligibilities)


def is_department_eligible(individu: Population, period: Period, condition: dict, parameters=None):
    depcom = individu.menage('depcom', period)

    eligible_departments = parameters.departements
    return sum([startswith(depcom, code.encode('UTF-8'))for code in eligible_departments]) > 0


def is_region_eligible(individu: Population, period: Period, condition: dict, parameters=None):
    region = individu.menage('region', period)
    eligible_regions = parameters.regions
    return sum([region == TypesCodeInseeRegion(code_region) for code_region in eligible_regions]) > 0


def is_regime_securite_sociale_eligible(individu: Population, period: Period, condition: dict, parameters=None):
    regime_securite_sociale = individu('regime_securite_sociale', period)
    eligible_regimes = parameters.regime_securite_sociale.includes
    return sum([regime_securite_sociale == RegimeSecuriteSociale[regime] for regime in eligible_regimes]) > 0


def is_quotient_familial_eligible(individu: Population, period: Period, condition: dict, parameters=None) -> np.array:

    rfr = individu.foyer_fiscal('rfr', period.this_year)
    nbptr = individu.foyer_fiscal('nbptr', period.this_year)
    quotient_familial = rfr / nbptr

    comparison = operations[condition['operator']]

    return comparison(quotient_familial, condition['value'])


def is_formation_sanitaire_social_eligible(individu: Population, period: Period, condition: dict, parameters=None) -> np.array:
    id_formation_sanitaire_social = GroupeSpecialitesFormation.groupe_330
    id_formation_groupe = individu(
        'groupe_specialites_formation', period)
    return id_formation_groupe == id_formation_sanitaire_social


def is_beneficiaire_rsa_eligible(individu: Population, period: Period, condition: dict, parameters=None) -> np.array:
    rsa = individu.famille('rsa', period)
    return rsa > 0


def is_annee_etude_eligible(individu: Population, period: Period, condition: dict, parameters=None) -> np.array:
    current_year = individu(
        'annee_etude', period)
    return sum([current_year == TypesClasse[value] for value in condition['values']]) > 0


def has_mention_baccalaureat(individu: Population, period: Period, condition: dict, parameters=None) -> np.array:
    has_mention = individu(
        'mention_baccalaureat', period)
    return sum([has_mention == TypesMention[value] for value in condition['values']]) > 0


def is_boursier(individu: Population, period: Period, condition: dict, parameters=None) -> np.array:
    return individu('boursier', period)


def is_chomeur(individu: Population, period: Period) -> np.array:
    return individu('activite', period) == TypesActivite.chomeur


def is_stagiaire(individu: Population, period: Period) -> np.array:
    return individu('stagiaire', period)


def is_apprenti(individu: Population, period: Period) -> np.array:
    return individu('apprenti', period)


def is_enseignement_superieur(individu: Population, period: Period) -> np.array:
    return individu(
        'scolarite', period) == TypesScolarite.enseignement_superieur


def is_lyceen(individu: Population, period: Period) -> np.array:
    return individu(
        'scolarite', period) == TypesScolarite.lycee


def is_etudiant(individu: Population, period: Period) -> np.array:
    return individu(
        'etudiant', period)


def is_professionnalisation(individu: Population, period: Period) -> np.array:
    return individu('professionnalisation', period)


def is_actif(individu: Population, period: Period) -> np.array:
    return individu('activite', period) == TypesActivite.actif


def is_inactif(individu: Population, period: Period) -> np.array:
    return individu('activite', period) == TypesActivite.inactif


condition_table = {
    "age": is_age_eligible,
    "regions": is_region_eligible,
    "departements": is_department_eligible,
    "quotient_familial": is_quotient_familial_eligible,
    "formation_sanitaire_social": is_formation_sanitaire_social_eligible,
    "regime_securite_sociale": is_regime_securite_sociale_eligible,
    "beneficiaire_rsa": is_beneficiaire_rsa_eligible,
    "annee_etude": is_annee_etude_eligible,
    "boursier": is_boursier,
    "mention_baccalaureat": has_mention_baccalaureat,
}

profil_table = {
    "enseignement_superieur": is_enseignement_superieur,
    "chomeur": is_chomeur,
    "apprenti": is_apprenti,
    "lyceen": is_lyceen,
    "etudiant": is_etudiant,
    "stagiaire": is_stagiaire,
    "professionnalisation": is_professionnalisation,
    "independant": is_actif,
    "salarie": is_actif,
    "service_civique": is_actif,
    "inactif": is_inactif,
}

type_table = {
    'float': float,
    'bool': bool,
}


def generate_variable(benefit: dict):

    value_type = type_table[benefit['type']]

    def formula(individu: Population, period: Period, parameters: ParameterNode):
        def calcul_montant_eligible(
                amount: int, is_profile_eligible: bool, general_eligibilities: np.array):
            if value_type == float:
                montant_final = amount * is_profile_eligible * general_eligibilities
            else:
                montant_final = general_eligibilities * is_profile_eligible
            return montant_final

        def eval_conditions(conditions: dict, parameters=None) -> np.array:
            if parameters:
                conditions_p: ParameterNodeAtInstant = parameters(
                    period)[benefit['slug']].conditions
                conditions_types: list[str] = [
                    condition for condition in conditions_p]
                test_conditions = [(condition_table[condition_type], {
                }, conditions_p) for condition_type in conditions_types]
                conditions_results = [
                    test[0](individu, period, {}, test[2]) for test in test_conditions]
                print(">>>>>>>>params<<<<<<<<<<")
                print(f"conditions_p : {conditions_p}")
                print(f"type conditions_p : {type(conditions_p)}")
                print(f"test_conditions : {test_conditions}")
                print(f"type(test_conditions[0]) : {type(test_conditions[0])}")

                print("^^^^^^^^^ params ^^^^^^^^^")
            else:
                test_conditions = [(condition_table[condition['type']], condition, parameters)
                                   for condition in conditions]

                conditions_results = [
                    test[0](individu, period, test[1]) for test in test_conditions]
            return sum(conditions_results) == len(conditions)

        amount = benefit.get('montant')

        profils_eligible: dict = benefit["profils"]
        if len(profils_eligible) == 0:
            is_profile_eligible = True
        else:
            def eval_profil(profil: dict):
                predicate = profil_table[profil['type']]
                profil_match = predicate(individu, period)
                if 'conditions' in profil:
                    conditions_satisfied = eval_conditions(
                        profil['conditions'])
                return profil_match * conditions_satisfied if 'conditions' in profil else profil_match

            eligibilities = [eval_profil(profil)
                             for profil in profils_eligible]
            is_profile_eligible: bool = sum(eligibilities) >= 1
        conditions_generales = benefit['conditions_generales']

        general_eligibilities = eval_conditions(
            conditions_generales, parameters)
        montant_eligible = calcul_montant_eligible(
            amount, is_profile_eligible, general_eligibilities)

        # return True
        return montant_eligible

    return type(benefit['slug'], (Variable,), {
        "value_type": value_type,
        "entity": Individu,
        "definition_period": MONTH,
        "formula": formula,

    })


class aides_jeunes_reform_dynamic(reforms.Reform):
    root = '.'
    path = 'benefits/'
    current_path = f'{root}/{path}'

    def extract_benefit_file_content(self, benefit_path):
        benefit: dict = yaml.safe_load(open(benefit_path))
        benefit['slug'] = benefit_path.split(
            '/')[-1].replace('-', '_').split('.')[0]
        return benefit

    def extract_benefits_paths(self, benefits_folder: str) -> "list[str]":
        def isYAMLfile(path: str): return str(path).endswith(
            '.yml') or str(path).endswith('.yaml')
        liste_fichiers = [
            str(benefit) for benefit in Path(benefits_folder).iterdir()
            if isYAMLfile(benefit)
        ]
        return liste_fichiers

    def apply(self):
        try:
            benefit_files_paths = self.extract_benefits_paths(
                self.current_path)

            for path in benefit_files_paths:
                benefit = self.extract_benefit_file_content(path)
                benefit_parameter = create_benefit_parameters(benefit)
                self.parameters.add_child(
                    benefit_parameter.name, benefit_parameter)

                self.add_variable(generate_variable(benefit))
        except KeyError as e:
            raise KeyError(f"field {e} missing in file: {path}")
