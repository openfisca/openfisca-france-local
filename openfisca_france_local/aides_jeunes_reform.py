# -*- coding: utf-8 -*-

import os

import collections
import yaml
import operator

from pathlib import Path
from numpy.core.defchararray import startswith
import numpy as np

from openfisca_france.model.base import (
    TypesMention, TypesActivite, Variable, Individu, MONTH)
from openfisca_core import reforms
from openfisca_core.periods import Period, period


from openfisca_core.populations.population import Population
from openfisca_france.model.prestations.education import (
    TypesScolarite, TypesClasse)
from openfisca_france.model.caracteristiques_socio_demographiques.logement import (
    TypesCodeInseeRegion)
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import GroupeSpecialitesFormation

operations = {
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
}


def is_age_eligible(individu, period, condition):

    condition_age = condition['value']
    individus_age = individu('age', period)

    comparison = operations[condition['operator']]

    return comparison(individus_age, condition_age)


def is_department_eligible(individu: Population, period: Period, condition):
    depcom = individu.menage('depcom', period)
    return sum([startswith(depcom, code.encode('UTF-8'))for code in condition['values']]) > 0


def is_region_eligible(individu: Population, period: Period, condition):
    region = individu.menage('region', period)
    return sum([region == TypesCodeInseeRegion(code_region) for code_region in condition['values']]) > 0


def is_regime_securite_sociale_eligible(individu: Population, period: Period, condition):
    regime_securite_sociale = individu('regime_securite_sociale', period)
    return sum([regime_securite_sociale == RegimeSecuriteSociale[regime] for regime in condition['includes']]) > 0


def is_quotient_familial_eligible(individu: Population, period: Period, condition) -> np.array:

    rfr = individu.foyer_fiscal('rfr', period.this_year)
    nbptr = individu.foyer_fiscal('nbptr', period.this_year)
    quotient_familial = rfr / nbptr

    comparison = operations[condition['operator']]

    return comparison(quotient_familial, condition['value'])


def is_formation_sanitaire_social_eligible(individu: Population, period: Period, condition) -> np.array:
    id_formation_sanitaire_social = GroupeSpecialitesFormation.groupe_330
    id_formation_groupe = individu(
        'groupe_specialites_formation', period)
    return id_formation_groupe == id_formation_sanitaire_social


def is_beneficiaire_rsa_eligible(individu: Population, period: Period, condition: dict) -> np.array:
    rsa = individu.famille('rsa', period)
    return rsa > 0


def is_annee_etude_eligible(individu: Population, period: Period, condition) -> np.array:
    current_year = individu(
        'annee_etude', period)
    return sum([current_year == TypesClasse[value] for value in condition['values']]) > 0


def has_mention_baccalaureat(individu: Population, period: Period, condition) -> np.array:
    has_mention = individu(
        'mention_baccalaureat', period)
    return sum([has_mention == TypesMention[value] for value in condition['values']]) > 0


def is_boursier(individu: Population, period: Period, condition: dict) -> np.array:
    return individu('boursier', period)


def is_commune_eligible(individu: Population, period: Period, condition: dict) -> np.array:
    depcom = individu.menage('depcom', period)
    eligible_depcoms = condition['values']
    return sum([depcom == eligible_depcom.encode('UTF-8')
               for eligible_depcom
               in eligible_depcoms])


def not_implemented(_: Population, __: Period, condition: dict) -> np.array:
    raise NotImplementedError(
        f'Condition `{condition["type"]}` is not implemented')


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
    return individu('scolarite', period) == TypesScolarite.lycee


def is_etudiant(individu: Population, period: Period) -> np.array:
    return individu('etudiant', period)


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
    "attached_to_institution": not_implemented,
    "communes": is_commune_eligible,
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


ConditionEvaluator = collections.namedtuple(
    'ConditionEvaluator', ['condition', 'evaluator'])
ProfileEvaluator = collections.namedtuple(
    'ProfileEvaluator', ['predicate', 'conditions'])


def build_condition_evaluator_list(conditions):
    return [ConditionEvaluator(condition, condition_table[condition['type']])
            for condition in conditions]


def build_profil_evaluator(profil):
    predicate = profil_table[profil['type']]
    conditions = profil.get('conditions', [])
    return ProfileEvaluator(predicate, build_condition_evaluator_list(conditions))


def eval_conditions(test_conditions: "list[ConditionEvaluator]", individu: Population, period: Period) -> np.array:
    conditions_results = [
        test.evaluator(individu, period, test.condition) for test in test_conditions]
    return sum(conditions_results) == len(test_conditions)


def eval_profil(profil_evaluator: ProfileEvaluator, individu: Population, period: Period):
    profil_match = profil_evaluator.predicate(individu, period)
    if len(profil_evaluator.conditions) == 0:
        return profil_match
    else:
        return profil_match * eval_conditions(profil_evaluator.conditions, individu, period)


def calcul_montant_eligible(value_type: str, amount: int, eligibilities: np.array):
    if value_type == float:
        montant_final = amount * eligibilities
    else:
        montant_final = eligibilities
    return montant_final


def generate_variable(benefit: dict):
    value_type = type_table[benefit['type']]
    amount = benefit.get('montant')
    test_conditions_generales = build_condition_evaluator_list(
        benefit['conditions_generales'])
    test_profiles_eligible = [build_profil_evaluator(profil)
                              for profil in benefit["profils"]]

    def formula(individu: Population, period: Period):
        if len(test_profiles_eligible) == 0:
            is_profile_eligible = np.array([True] * individu.count)
        else:
            eligibilities = [eval_profil(profil, individu, period)
                             for profil in test_profiles_eligible]
            is_profile_eligible: np.array = sum(eligibilities) >= 1

        general_eligibilities = eval_conditions(
            test_conditions_generales, individu, period)
        montant_eligible = calcul_montant_eligible(
            value_type, amount, general_eligibilities * is_profile_eligible)

        return montant_eligible

    return type(benefit['slug'], (Variable,), {
        "value_type": value_type,
        "entity": Individu,
        "definition_period": MONTH,
        "formula": formula,
    })


root = '.'
path = 'benefits/'
current_path = f'{root}/{path}'


class aides_jeunes_reform_dynamic(reforms.Reform):
    def __init__(self, baseline, benefits_folder_path=current_path):
        self.benefits_folder_path = benefits_folder_path
        super().__init__(baseline)

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
                self.benefits_folder_path)
            for path in benefit_files_paths:
                self.add_variable(generate_variable(
                    self.extract_benefit_file_content(path)))
        except KeyError as e:
            raise KeyError(f"field {e} missing in file: {path}")
