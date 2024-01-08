# -*- coding: utf-8 -*-

from os import path, getenv

import collections
from typing import Union
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
from openfisca_core.parameters.parameter_node_at_instant import ParameterNodeAtInstant
from openfisca_core.parameters.parameter_at_instant import ParameterAtInstant

from openfisca_france_local.convert_benefit_conditions_to_parameters import convert_benefit_conditions_to_parameters

operations = {
    'maximum_inclusif': operator.le,
    'minimum_inclusif': operator.ge,
    'maximum_exclusif': operator.lt,
    'minimum_exclusif': operator.gt,
    }


def compute_operator_condition(eligible_values: ParameterNodeAtInstant, individus_values: np.ndarray) -> np.ndarray:
    constraints_values = [
        (operations[constraint], eligible_values[constraint])
        for constraint in eligible_values
        ]

    eligibilities = [
        constraint[0](individus_values, constraint[1])
        for constraint in constraints_values
        ]

    return sum(eligibilities) >= len(constraints_values)


def is_age_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    individus_age = individu('age', period)
    eligible_ages = parameters.age

    return compute_operator_condition(eligible_ages, individus_age)


def is_department_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    depcom = individu.menage('depcom', period)
    eligible_departments = parameters.departements

    eligibilities = np.array([
        startswith(depcom, code.encode('UTF-8'))
        for code in eligible_departments
        ])

    return sum(eligibilities) > 0


def is_region_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    region = individu.menage('region', period)
    eligible_regions = parameters.regions

    eligibilities = [
        region == TypesCodeInseeRegion(code_region)
        for code_region in eligible_regions
        ]

    return sum(eligibilities) > 0


def is_regime_securite_sociale_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    individus_regime_secu = individu('regime_securite_sociale', period)

    if "excludes" in parameters.regime_securite_sociale:
        not_eligible_regimes = parameters.regime_securite_sociale.excludes
        eligibilities = [
            individus_regime_secu != RegimeSecuriteSociale[regime]
            for regime in not_eligible_regimes
            ]
    else:
        eligible_regimes = parameters.regime_securite_sociale.includes
        eligibilities = [
            individus_regime_secu == RegimeSecuriteSociale[regime]
            for regime in eligible_regimes
            ]

    return sum(eligibilities) > 0


def is_quotient_familial_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:

    if 'month' in parameters.quotient_familial:
        condition_QF = parameters.quotient_familial.month
        period_divider = 12
    elif 'year' in parameters.quotient_familial:
        condition_QF = parameters.quotient_familial.year
        period_divider = 1

    individus_rfr = individu.foyer_fiscal('rfr', period.n_2)
    individus_nbptr = individu.foyer_fiscal('nbptr', period.n_2)
    individus_quotient_familial = (individus_rfr / period_divider / individus_nbptr)

    QF_constraints = [
        (operations[constraint], condition_QF[constraint])
        for constraint in condition_QF
        ]

    eligibilities = [
        constraint[0](individus_quotient_familial, constraint[1])
        for constraint in QF_constraints
        ]

    return sum(eligibilities) > 0


def is_formation_sanitaire_social_eligible(individu: Population, period: Period, _) -> np.ndarray:
    id_formation_sanitaire_social = GroupeSpecialitesFormation.groupe_330
    id_formation_groupe = individu('groupe_specialites_formation', period)

    return id_formation_groupe == id_formation_sanitaire_social


def is_beneficiaire_rsa_eligible(individu: Population, period: Period, _ = None) -> np.ndarray:
    rsa = individu.famille('rsa', period)

    return rsa > 0


def is_annee_etude_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    current_year = individu('annee_etude', period)

    annee_etudes_eligible = parameters.annee_etude

    eligibilities = [
        current_year == TypesClasse[value]
        for value in annee_etudes_eligible
        ]

    return sum(eligibilities) > 0


def has_mention_baccalaureat(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    has_mention = individu('mention_baccalaureat', period)
    eligible_mentions = parameters.mention_baccalaureat

    eligibilities = [
        has_mention == TypesMention[value]
        for value in eligible_mentions
        ]

    return sum(eligibilities) > 0


def is_boursier(individu: Population, period: Period, _) -> np.ndarray:
    return individu('boursier', period)


def is_commune_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    depcom = individu.menage('depcom', period)
    eligible_depcoms = parameters.communes

    return sum([
        depcom == eligible_depcom.encode('UTF-8')
        for eligible_depcom in eligible_depcoms
        ]) > 0


def is_epci_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    eligible_epcis: list[str] = parameters.epcis

    eligibilities = [
        individu.menage(f'menage_dans_epci_siren_{epci}', period)
        for epci in eligible_epcis
        ]

    return sum(eligibilities) > 0


def is_taux_incapacite_eligible(individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    individus_taux_incapacite = individu('taux_incapacite', period)
    eligible_taux_incapacites = parameters.taux_incapacite

    return compute_operator_condition(eligible_taux_incapacites, individus_taux_incapacite)


def is_chomeur(individu: Population, period: Period) -> np.ndarray:
    return individu('activite', period) == TypesActivite.chomeur


def is_stagiaire(individu: Population, period: Period) -> np.ndarray:
    return individu('stagiaire', period)


def is_apprenti(individu: Population, period: Period) -> np.ndarray:
    return individu('apprenti', period)


def is_enseignement_superieur(individu: Population, period: Period) -> np.ndarray:
    return individu(
        'scolarite', period) == TypesScolarite.enseignement_superieur


def is_lyceen(individu: Population, period: Period) -> np.ndarray:
    return individu('scolarite', period) == TypesScolarite.lycee


def is_etudiant(individu: Population, period: Period) -> np.ndarray:
    return individu('etudiant', period)


def is_professionnalisation(individu: Population, period: Period) -> np.ndarray:
    return individu('professionnalisation', period)


def is_actif(individu: Population, period: Period) -> np.ndarray:
    return individu('activite', period) == TypesActivite.actif


def is_inactif(individu: Population, period: Period) -> np.ndarray:
    return individu('activite', period) == TypesActivite.inactif


def is_situation_handicap(individu: Population, period: Period) -> np.ndarray:
    return individu('handicap', period)


condition_table: dict = {
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
    }


profil_table: dict = {
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
    'beneficiaire_rsa': is_beneficiaire_rsa_eligible,
    }


type_table: dict = {
    'float': float,
    'bool': bool,
    }


ConditionEvaluator = collections.namedtuple(
    'ConditionEvaluator', ['condition', 'evaluator'])
ProfileEvaluator = collections.namedtuple(
    'ProfileEvaluator', ['profil_type', 'predicate', 'conditions'])


def build_condition_evaluator_list(conditions: 'list[dict]') -> 'list[ConditionEvaluator]':
    try:
        evaluators: 'list[ConditionEvaluator]' = [
            ConditionEvaluator(condition, condition_table[condition['type']])
            for condition in conditions
            ]
    except KeyError as e:
        raise NotImplementedError(f"Condition `{(e.args[0])}` is unknown.")

    return evaluators


def build_profil_evaluator(profil: dict) -> ProfileEvaluator:
    try:
        predicate = profil_table[profil['type']]
    except KeyError:
        raise NotImplementedError(f"Profil `{profil['type']}` is unknown.")

    conditions = profil.get('conditions', [])

    return ProfileEvaluator(profil['type'], predicate, build_condition_evaluator_list(conditions))


def eval_conditions(test_conditions: 'list[ConditionEvaluator]', individu: Population, period: Period, parameters: ParameterNodeAtInstant) -> np.ndarray:
    def get_conditions(parameters: Union[ParameterAtInstant, ParameterNodeAtInstant]):
        if hasattr(parameters, "_children") and 'conditions' in parameters._children:
            conditions = parameters.conditions
        else:
            conditions = []
        return conditions

    conditions_parameters = get_conditions(parameters)

    conditions_results = [
        test.evaluator(individu, period, conditions_parameters)
        for test in test_conditions
        ]

    return sum(conditions_results) == len(test_conditions)


def eval_profil(profil_evaluator: ProfileEvaluator,
                individu: Population, period: Period, parameters: ParameterNodeAtInstant):
    profil_match = profil_evaluator.predicate(individu, period)
    benefit_profil_parameters = parameters.profils[profil_evaluator.profil_type]

    return profil_match * eval_conditions(profil_evaluator.conditions,
                                          individu, period, benefit_profil_parameters)


def generate_variable(benefit: dict):
    variable_name: str = benefit['slug']
    amount = benefit.get('montant')

    conditions_generales_tests = build_condition_evaluator_list(benefit['conditions_generales'])

    eligible_profiles_tests = [
        build_profil_evaluator(profil)
        for profil in benefit.get('profils', [])
        ]

    def compute_amount(eligibilities: np.ndarray):
        return amount * eligibilities

    def compute_bool(eligibilities: np.ndarray):
        return eligibilities

    compute_value = compute_amount if amount else compute_bool

    def formula(individu: Population, period: Period, parameters):
        benefit_parameters: ParameterNodeAtInstant = parameters(period)[variable_name]

        eligibilities = [
            eval_profil(profil, individu, period, benefit_parameters)
            for profil in eligible_profiles_tests
            ]

        is_profile_eligible = len(eligibilities) == 0 or sum(eligibilities) >= 1

        general_eligibilities = eval_conditions(conditions_generales_tests, individu, period, benefit_parameters)

        return compute_value(general_eligibilities * is_profile_eligible)

    return type(variable_name, (Variable,), {
        'value_type': type_table[benefit['type']],
        'entity': Individu,
        'definition_period': MONTH,
        'formula': formula,
        })


default_benefit_path = 'test_data/benefits'
default_institutions_path = 'test_data/institutions'


class aides_jeunes_reform_dynamic(reforms.Reform):
    def __init__(self, baseline, benefits_folder_path=default_benefit_path, institutions_folder_path=default_institutions_path):
        self.benefits_folder_path = getenv('DYNAMIC_BENEFIT_FOLDER', benefits_folder_path)
        self.institutions_folder_path = getenv('DYNAMIC_INSTITUTION_FOLDER', institutions_folder_path)
        super().__init__(baseline)

    def apply(self):
        try:
            benefit_files_paths: 'list[str]' = self._extract_paths(self.benefits_folder_path)

            for benefit_path in benefit_files_paths:
                benefit: dict = self._extract_benefit_file_content(benefit_path)

                benefit_parameters: ParameterNode = convert_benefit_conditions_to_parameters(benefit)
                self._add_parameters_into_current_tax_and_benefits_system(benefit_parameters)

                self.add_variable(generate_variable(benefit))

        except Exception as e:
            print('\nMore informations about the error:')
            print(f'\x1b[31;20m\n{e.args[0]}\nThis happened while processing file {path}\n\x1b[0m')
            raise

    def _extract_benefit_file_content(self, benefit_path: str):
        def _convert_institution_to_condition(benefit: dict) -> dict:
            if {'type': 'attached_to_institution'} in benefit['conditions_generales']:
                conditions_generales_without_attached_institution = [
                    condition for condition
                    in benefit['conditions_generales']
                    if condition != {'type': 'attached_to_institution'}]

                with open(f'{self.institutions_folder_path}/{benefit["institution"]}.yml') as file:
                    institution: dict = yaml.safe_load(file)

                    institution_type = institution['type']
                    if institution_type in ['msa', 'caf']:
                        condition_type = 'departements'
                        condition_value = institution['departments']
                    elif institution_type == 'epci':
                        condition_type = 'epcis'
                        condition_value = [institution['code_siren']]
                    else:
                        condition_type = f"{institution_type}s"
                        condition_value = [institution['code_insee']]

                    conditions_generales_without_attached_institution.append({'type': condition_type, 'values': condition_value})

                    benefit = {**benefit, 'conditions_generales': conditions_generales_without_attached_institution}
            return benefit

        def _slug_from_path(path: str):
            return path.split('/')[-1].replace('-', '_').split('.')[0]

        with open(benefit_path) as file:
            benefit: dict = yaml.safe_load(file)
            benefit['slug'] = _slug_from_path(benefit_path)
            benefit = _convert_institution_to_condition(benefit)
        return benefit

    def _extract_paths(self, folder: str) -> 'list[str]':
        def _isYAMLfile(path: Path):
            return str(path).endswith('.yml') or str(path).endswith('.yaml')

        files: 'list[str]' = [
            str(benefit)
            for benefit in Path(folder).iterdir()
            if _isYAMLfile(benefit)
            ]

        return files

    def _add_parameters_into_current_tax_and_benefits_system(self, benefit_parameters: ParameterNode):
        self.parameters.add_child(benefit_parameters.name, benefit_parameters)
