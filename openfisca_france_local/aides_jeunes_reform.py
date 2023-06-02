# -*- coding: utf-8 -*-

from datetime import date
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
from openfisca_core.periods import Period


from openfisca_core.populations.population import Population
from openfisca_france.model.prestations.education import TypesScolarite, TypesClasse
from openfisca_france.model.caracteristiques_socio_demographiques.logement import TypesCodeInseeRegion
from openfisca_france.model.caracteristiques_socio_demographiques.demographie \
    import (RegimeSecuriteSociale, GroupeSpecialitesFormation)
from openfisca_core.parameters.parameter_node import ParameterNode
from openfisca_core.parameters.parameter import Parameter

from openfisca_france_local.convert_benefit_conditions_to_parameters import convert_benefit_conditions_to_parameters

operations = {
    'strictement_inferieur': operator.lt,
    'maximum': operator.le,
    'strictement_superieur': operator.gt,
    'minimum': operator.ge,
    }


def is_age_eligible(individu: Population, period: Period, parameters: ParameterNode) -> np.array:
    individus_age = individu('age', period)
    eligible_ages = parameters(period).age
    age_constraints = [
        (operations[constraint], eligible_ages[constraint])
        for constraint in eligible_ages
        ]

    eligibilities = [constraint[0](individus_age, constraint[1])
                     for constraint in age_constraints]

    return sum(eligibilities) >= len(age_constraints)


def is_department_eligible(individu: Population, period: Period,
                           parameters: ParameterNode):
    depcom = individu.menage('depcom', period)
    eligible_departments = parameters(period).departements
    eligibilities = [
        startswith(depcom, code.encode('UTF-8'))
        for code in eligible_departments
        ]

    return sum(eligibilities) > 0


def is_region_eligible(individu: Population, period: Period,
                       parameters: ParameterNode):
    region = individu.menage('region', period)
    eligible_regions = parameters(period).regions
    eligibilities = [
        region == TypesCodeInseeRegion(code_region)
        for code_region in eligible_regions
        ]

    return sum(eligibilities) > 0


def is_regime_securite_sociale_eligible(individu: Population, period: Period, parameters: ParameterNode):
    individus_regime_secu = individu('regime_securite_sociale', period)
    conditions = parameters(period)
    if "excludes" in conditions.regime_securite_sociale:
        not_eligible_regimes = conditions.regime_securite_sociale.excludes
        eligibilities = [
            individus_regime_secu != RegimeSecuriteSociale[regime]
            for regime in not_eligible_regimes
            ]
    else:
        eligible_regimes = conditions.regime_securite_sociale.includes
        eligibilities = [
            individus_regime_secu == RegimeSecuriteSociale[regime]
            for regime in eligible_regimes
            ]

    return sum(eligibilities) > 0


def is_quotient_familial_eligible(individu: Population, period: Period, parameters: ParameterNode) -> np.array:

    conditions = parameters(period)

    if 'month' in conditions.quotient_familial:
        condition_QF = conditions.quotient_familial.month
        period_divider = 12
    elif 'year' in conditions.quotient_familial:
        condition_QF = conditions.quotient_familial.year
        period_divider = 1

    individus_rfr = individu.foyer_fiscal('rfr', period.this_year)
    individus_nbptr = individu.foyer_fiscal('nbptr', period.this_year)
    individus_quotient_familial = (
        individus_rfr / period_divider / individus_nbptr
        )

    QF_constraints = [
        (operations[constraint], condition_QF[constraint])
        for constraint in condition_QF
        ]

    eligibilities = [
        constraint[0](individus_quotient_familial, constraint[1])
        for constraint in QF_constraints
        ]

    return sum(eligibilities) > 0


def is_formation_sanitaire_social_eligible(individu: Population, period: Period, condition) -> np.array:
    id_formation_sanitaire_social = GroupeSpecialitesFormation.groupe_330
    id_formation_groupe = individu(
        'groupe_specialites_formation', period)

    return id_formation_groupe == id_formation_sanitaire_social


def is_beneficiaire_rsa_eligible(individu: Population, period: Period,
                                 _) -> np.array:
    rsa = individu.famille('rsa', period)

    return rsa > 0


def is_annee_etude_eligible(individu: Population, period: Period, parameters) -> np.array:
    current_year = individu(
        'annee_etude', period)

    annee_etudes_eligible = parameters(period).annee_etude
    eligibilities = [
        current_year == TypesClasse[value]
        for value in annee_etudes_eligible
        ]

    return sum(eligibilities) > 0


def has_mention_baccalaureat(individu: Population, period: Period, parameters) -> np.array:
    has_mention = individu('mention_baccalaureat', period)
    eligible_mentions = parameters(period).mention_baccalaureat
    eligibilities = [
        has_mention == TypesMention[value]
        for value in eligible_mentions
        ]

    return sum(eligibilities) > 0


def is_boursier(individu: Population, period: Period, condition: dict) -> np.array:
    return individu('boursier', period)


def is_commune_eligible(individu: Population, period: Period, parameter) -> np.array:
    depcom = individu.menage('depcom', period)
    eligible_depcoms = parameter(period).communes
    return sum([
        depcom == eligible_depcom.encode('UTF-8')
               for eligible_depcom in eligible_depcoms]
               )


def is_epci_eligible(individu: Population, period: Period, parameter) -> np.array:
    eligible_epcis: list[str] = parameter(period).epcis
    eligibilities = [
        individu.menage(f'menage_dans_epci_siren_{epci}', period)
        for epci in eligible_epcis
        ]

    return sum(eligibilities)


def is_taux_incapacite_eligible(individu: Population, period: Period, parameter) -> np.array:
    evaluates = {
        'inferieur_50': lambda taux: taux < 0.5,
        'entre_50_et_80': lambda taux: np.logical_and(taux >= 0.5, taux < 0.8),
        'superieur_ou_egal_80': lambda taux: taux >= 0.8
        }

    taux_incapacite = individu('taux_incapacite', period)
    elibible_taux = parameter(period).taux_incapacite

    eligibilities = [
        evaluates[taux](taux_incapacite)
        for taux in elibible_taux
        ]

    return sum(eligibilities) > 0


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


def is_situation_handicap(individu: Population, period: Period) -> np.array:
    return individu('handicap', period)


def not_implemented_condition(_: Population, __: Period, condition: dict) -> np.array:
    raise NotImplementedError(f'Condition `{condition["type"]}` is not implemented')


condition_table = {
    'age': is_age_eligible,
    'regions': is_region_eligible,
    'departements': is_department_eligible,
    'quotient_familial': is_quotient_familial_eligible,
    'formation_sanitaire_social': is_formation_sanitaire_social_eligible,
    'regime_securite_sociale': is_regime_securite_sociale_eligible,
    'beneficiaire_rsa': is_beneficiaire_rsa_eligible,
    'annee_etude': is_annee_etude_eligible,
    'boursier': is_boursier,
    'mention_baccalaureat': has_mention_baccalaureat,
    'communes': is_commune_eligible,
    'epcis': is_epci_eligible,
    'taux_incapacite': is_taux_incapacite_eligible,
    'attached_to_institution': not_implemented_condition,
    }


profil_table = {
    'enseignement_superieur': is_enseignement_superieur,
    'chomeur': is_chomeur,
    'apprenti': is_apprenti,
    'lyceen': is_lyceen,
    'etudiant': is_etudiant,
    'stagiaire': is_stagiaire,
    'professionnalisation': is_professionnalisation,
    'independant': is_actif,
    'salarie': is_actif,
    'service_civique': is_actif,
    'inactif': is_inactif,
    'situation_handicap': is_situation_handicap,
    }


type_table = {
    'float': float,
    'bool': bool,
    }


ConditionEvaluator = collections.namedtuple(
    'ConditionEvaluator', ['condition', 'evaluator'])
ProfileEvaluator = collections.namedtuple(
    'ProfileEvaluator', ['predicate', 'conditions'])


def build_condition_evaluator_list(conditions) -> 'list[ConditionEvaluator]':
    try:
        if isinstance(conditions, Parameter):
            conditions_types: list[str] = []
        else:
            conditions_types: list[str] = list(conditions.children)

        evaluators = [
            ConditionEvaluator(conditions, condition_table[condition_type])
            for condition_type in conditions_types
            ]
    except KeyError as e:
        raise KeyError(f"Condition: `{(e.args[0])}` is unknown")
    return evaluators


def build_profil_evaluator(profil_type: str, parameters: ParameterNode) -> ProfileEvaluator:

    def get_conditions(profil):
        if isinstance(profil, ParameterNode) and 'conditions' in profil.children:
            conditions = profil.conditions
        else:
            conditions = profil
        return conditions

    profil = parameters.profils.children[profil_type]
    try:

        predicate = profil_table[profil_type]
    except KeyError:
        raise KeyError(f"Profil: `{profil_type}` is unknown")

    conditions = get_conditions(profil)

    return ProfileEvaluator(predicate, build_condition_evaluator_list(conditions))


def eval_conditions(test_conditions: 'list[ConditionEvaluator]', individu: Population, period: Period) -> np.array:
    conditions_results = [
        test.evaluator(individu, period, test.condition)
        for test in test_conditions
        ]
    return sum(conditions_results) == len(test_conditions)


def eval_profil(profil_evaluator: ProfileEvaluator, individu: Population, period: Period):
    profil_match = profil_evaluator.predicate(individu, period)
    if len(profil_evaluator.conditions) == 0:
        return profil_match
    else:
        return profil_match * eval_conditions(profil_evaluator.conditions, individu, period)


def generate_variable(variable_name: str, parameters: ParameterNode, variable_type: type):
    if variable_type == float:
        amount = parameters(date.today()).montant

    conditions_generales_tests = build_condition_evaluator_list(parameters.conditions)

    if 'profils' in parameters.children:
        eligible_profiles_tests = [
            build_profil_evaluator(profil_type, parameters)
            for profil_type in parameters.profils.children
            ]
    else:
        eligible_profiles_tests = []

    def compute_amount(eligibilities: np.array):
        return amount * eligibilities

    def compute_bool(eligibilities: np.array):
        return eligibilities

    compute_value = compute_amount if variable_type == float else compute_bool

    def formula(individu: Population, period: Period):
        eligibilities = [
            eval_profil(profil, individu, period)
            for profil in eligible_profiles_tests
            ]
        is_profile_eligible = len(eligibilities) == 0 or sum(eligibilities) >= 1

        general_eligibilities = eval_conditions(conditions_generales_tests, individu, period)
        return compute_value(general_eligibilities * is_profile_eligible)

    return type(variable_name, (Variable,), {
        'value_type': variable_type,
        'entity': Individu,
        'definition_period': MONTH,
        'formula': formula,
        })


root = '.'
path = 'test_data/benefits'
current_path = os.path.join(root, path)


class aides_jeunes_reform_dynamic(reforms.Reform):
    def __init__(self, baseline, benefits_folder_path=current_path):
        self.benefits_folder_path = benefits_folder_path
        super().__init__(baseline)

    def apply(self):
        try:
            benefit_files_paths: 'list[str]' = self._extract_benefits_paths(
                self.benefits_folder_path)

            for path in benefit_files_paths:
                benefit = self._extract_benefit_file_content(path)
                self._create_and_add_parameters(benefit)

                benefits_parameters: ParameterNode = self.parameters.children[
                    benefit['slug']]

                benefit_type: type = bool if benefit['type'] == 'bool' else float

                self.add_variable(generate_variable(
                    benefit['slug'], benefits_parameters, benefit_type))

        except KeyError as e:
            raise KeyError(f'{e.args[0]} - Input file: {path}')
        # TODO : COmmented for debug, but, is this except a good thing anyway ?
        # except Exception as e:
        #     raise Exception(f'{e.args[0]} in file {path}')

    def _extract_benefit_file_content(self, benefit_path: str):
        def _slug_from_filename(benefit_path: str):
            return benefit_path.split('/')[-1].replace('-', '_').split('.')[0]

        benefit: dict = yaml.safe_load(open(benefit_path))
        benefit['slug'] = _slug_from_filename(benefit_path)

        return benefit

    def _extract_benefits_paths(self, benefits_folder: str) -> 'list[str]':
        def _isYAMLfile(path: str):
            return str(path).endswith('.yml') or str(path).endswith('.yaml')

        liste_fichiers = [
            str(benefit)
            for benefit in Path(benefits_folder).iterdir()
            if _isYAMLfile(benefit)
            ]

        return liste_fichiers

    def _create_and_add_parameters(self, benefit_path: str):
        benefit_parameter = convert_benefit_conditions_to_parameters(
            benefit_path)
        self.parameters.add_child(
            benefit_parameter.name, benefit_parameter)
