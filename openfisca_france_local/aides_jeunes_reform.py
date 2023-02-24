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
from openfisca_core.parameters.parameter_node_at_instant\
    import ParameterNodeAtInstant as ParamInstant

from openfisca_france.model.prestations.education import (
    TypesScolarite, TypesClasse)

from openfisca_france.model.caracteristiques_socio_demographiques\
    .logement import TypesCodeInseeRegion

from openfisca_france.model.caracteristiques_socio_demographiques\
    .demographie import RegimeSecuriteSociale

from openfisca_france.model.caracteristiques_socio_demographiques\
    .demographie import GroupeSpecialitesFormation
from openfisca_france.model.base import ParameterNode

from openfisca_france_local.condition_to_parameter\
    import create_benefit_parameters


operations = {
    'strictement_inferieur': operator.lt,
    'maximum': operator.le,
    'strictement_superieur': operator.gt,
    'minimum': operator.ge,
}


def is_age_eligible(individu: Population, period: Period,
                    parameters: ParamInstant) -> np.array:

    individus_age = individu('age', period)
    eligible_ages = parameters.age

    age_constraints = [(operations[constraint],  eligible_ages[constraint])
                       for constraint in eligible_ages]

    eligibilities = [constraint[0](individus_age, constraint[1])
                     for constraint in age_constraints]
    return sum(eligibilities) > 0


def is_department_eligible(individu: Population, period: Period,
                           parameters: ParamInstant) -> np.array:

    def is_from_department(individus_depcom, depcom):
        return startswith(individus_depcom, depcom.encode('UTF-8'))

    individus_depcom = individu.menage('depcom', period)

    eligible_departments = parameters.departements

    eligibilities = [is_from_department(individus_depcom, eligible_depcode)
                     for eligible_depcode
                     in eligible_departments]

    return sum(eligibilities) > 0


def is_region_eligible(individu: Population, period: Period,
                       parameters: ParamInstant) -> np.array:
    individus_region = individu.menage('region', period)
    eligible_regions = parameters.regions

    eligibilities = [individus_region == TypesCodeInseeRegion(code_region)
                     for code_region
                     in eligible_regions]

    return sum(eligibilities) > 0


def is_regime_securite_sociale_eligible(individu: Population, period: Period,
                                        parameters: ParamInstant) -> np.array:
    individus_regime_secu = individu(
        'regime_securite_sociale', period)

    if len(list(parameters.regime_securite_sociale)) > 1:
        raise ValueError(
            ('Condition "regime_securite_sociale" does not support having both'
             ' "includes" and "excludes" properties.\n'
             'Please check the YAML file.'))

    if "excludes" in parameters.regime_securite_sociale:
        not_eligible_regimes = parameters.regime_securite_sociale.excludes
        eligibilities = [individus_regime_secu != RegimeSecuriteSociale[regime]
                         for regime
                         in not_eligible_regimes]
    else:
        eligible_regimes = parameters.regime_securite_sociale.includes
        eligibilities = [individus_regime_secu == RegimeSecuriteSociale[regime]
                         for regime
                         in eligible_regimes]

    return sum(eligibilities) > 0


def is_quotient_familial_eligible(individu: Population, period: Period,
                                  parameters: ParamInstant) -> np.array:

    individus_rfr = individu.foyer_fiscal('rfr', period.this_year)
    individus_nbptr = individu.foyer_fiscal('nbptr', period.this_year)
    individus_quotient_familial = individus_rfr / individus_nbptr

    condition_QF = parameters.quotient_familial.month

    QF_constraints = [(operations[constraint],  condition_QF[constraint])
                      for constraint in condition_QF]

    eligibilities = [constraint[0](individus_quotient_familial, constraint[1])
                     for constraint in QF_constraints]
    return sum(eligibilities) > 0


def is_formation_sanitaire_social_eligible(individu: Population,
                                           period: Period, _) -> np.array:
    id_formation_sanitaire_social = GroupeSpecialitesFormation.groupe_330
    individus_id_formation_groupe = individu(
        'groupe_specialites_formation', period)
    return individus_id_formation_groupe == id_formation_sanitaire_social


def is_beneficiaire_rsa_eligible(individu: Population,
                                 period: Period, _) -> np.array:
    individus_rsa = individu.famille('rsa', period)
    return individus_rsa > 0


def is_annee_etude_eligible(individu: Population, period: Period,
                            parameters: ParamInstant) -> np.array:
    individus_current_year = individu(
        'annee_etude', period)
    annees_etude_eligible = parameters.annee_etude

    eligibilities = [individus_current_year == TypesClasse[value]
                     for value
                     in annees_etude_eligible]

    return sum(eligibilities) > 0


def has_mention_baccalaureat(individu: Population, period: Period,
                             parameters: ParamInstant) -> np.array:
    has_mention = individu(
        'mention_baccalaureat', period)
    mentions_eligibles = parameters.mention_baccalaureat

    eligibilities = [has_mention == TypesMention[mention]
                     for mention
                     in mentions_eligibles]

    return sum(eligibilities) > 0


def is_boursier(individu: Population, period: Period, _) -> np.array:
    return individu('boursier', period)


def is_chomeur(individu: Population, period: Period) -> np.array:
    return individu('activite', period) == TypesActivite.chomeur


def is_stagiaire(individu: Population, period: Period) -> np.array:
    return individu('stagiaire', period)


def is_apprenti(individu: Population, period: Period) -> np.array:
    return individu('apprenti', period)


def is_enseignement_superieur(individu: Population,
                              period: Period) -> np.array:
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

    def formula(individu: Population, period: Period,
                parameters: ParameterNode):

        def calcul_montant_eligible(amount: int, is_profile_eligible: bool,
                                    general_eligibilities: np.array):
            if value_type == float:
                montant = amount * is_profile_eligible * general_eligibilities
            else:
                montant = general_eligibilities * is_profile_eligible
            return montant

        def eval_conditions(conditions: ParamInstant) -> np.array:
            conditions_types: list[str] = list(conditions)

            test_conditions = [
                (condition_table[condition_type], conditions)
                for condition_type
                in conditions_types]

            conditions_results = [
                test[0](individu, period, test[1])
                for test
                in test_conditions]

            return sum(conditions_results) == len(test_conditions)

        amount = benefit.get('montant')

        benefit_parameters = parameters(period)[benefit['slug']]

        if 'profils' not in benefit_parameters:
            is_profile_eligible = True
        else:

            def eval_profil(profil_name: str,
                            profils_parameters: ParamInstant):

                def has_conditions(profil):
                    # As profil can be a bool in case of
                    # `enseignement_superieur` we need it to be checked.
                    # What is the most readable way to do that ?
                    return isinstance(profil, ParamInstant) and \
                        'conditions' in profil

                profil = profils_parameters[profil_name]

                predicate = profil_table[profil_name]
                profil_match = predicate(individu, period)

                if has_conditions(profil):
                    conditions_satisfied = eval_conditions(profil.conditions)
                else:
                    conditions_satisfied = True
                return profil_match * conditions_satisfied

            profils_parameters: ParamInstant = benefit_parameters.profils
            eligibilities = [eval_profil(profil_name, profils_parameters)
                             for profil_name
                             in profils_parameters]

            is_profile_eligible: bool = sum(eligibilities) >= 1

        general_eligibilities = eval_conditions(benefit_parameters.conditions)
        montant_eligible = calcul_montant_eligible(
            amount, is_profile_eligible, general_eligibilities)

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

    def extract_benefits_paths(self, benefits_folder: str) -> "list[str]":
        def isYAMLfile(path: str): return str(path).endswith(
            '.yml') or str(path).endswith('.yaml')

        liste_fichiers = [
            str(benefit)
            for benefit
            in Path(benefits_folder).iterdir()
            if isYAMLfile(benefit)
        ]
        return liste_fichiers

    def extract_benefit_file_content(self, benefit_path):

        def slug_from_filename(benefit_path):
            return benefit_path.split(
                '/')[-1].replace('-', '_').split('.')[0]

        benefit: dict = yaml.safe_load(open(benefit_path))
        benefit['slug'] = slug_from_filename(benefit_path)

        return benefit

    def create_and_add_parameters(self, benefit):
        benefit_parameter = create_benefit_parameters(benefit)
        self.parameters.add_child(
            benefit_parameter.name, benefit_parameter)

    def apply(self):
        try:
            benefit_files_paths = self.extract_benefits_paths(
                self.current_path)

            for path in benefit_files_paths:
                benefit = self.extract_benefit_file_content(path)
                self.create_and_add_parameters(benefit)
                self.add_variable(generate_variable(benefit))

        except KeyError as e:
            raise KeyError(f"field {e} missing in file: {path}")
