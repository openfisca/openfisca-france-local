# -*- coding: utf-8 -*-

import yaml

from pathlib import Path
from numpy.core.defchararray import startswith
import numpy as np

from openfisca_france.model.base import *
from openfisca_core import reforms
from openfisca_core.entities import Entity
from openfisca_core.periods import Period


from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import GroupeSpecialitesFormation
from openfisca_france.model.prestations.education import TypesScolarite


def is_age_eligible(individu, period, condition):

    condition_age = condition['value']
    individus_age = individu('age', period.first_month)

    operators = {
        '<': lambda individus_age, condition_age: individus_age < condition_age,
        '<=': lambda individus_age, condition_age: individus_age <= condition_age,
        '>': lambda individus_age, condition_age: individus_age > condition_age,
        '>=': lambda individus_age, condition_age: individus_age >= condition_age,
    }
    return operators[condition['operator']](individus_age, condition_age)


def is_department_eligible(individu, period, condition):
    depcom = individu.menage('depcom', period.first_month)
    return sum([startswith(depcom, code.encode('UTF-8'))for code in condition['values']])


def is_region_eligible(individu, period, condition):
    regcom = individu.menage('regcom', period.first_month)
    return sum([startswith(regcom, code.encode('UTF-8'))for code in condition['values']])


def is_regime_securite_sociale_eligible(individu, period, condition):
    regime_securite_sociale = individu('regime_securite_sociale', period)
    return sum([regime_securite_sociale == RegimeSecuriteSociale[regime] for regime in condition['includes']])


def is_quotient_familial_eligible(individu, period, condition):
    rfr = individu.foyer_fiscal('rfr', period.this_year)
    nbptr = individu.foyer_fiscal('nbptr', period.this_year)
    quotient_familial = rfr / nbptr
    return quotient_familial <= condition["ceiling"]


def is_formation_sanitaire_social_eligible(individu, period, condition):
    id_formation_sanitaire_social = GroupeSpecialitesFormation.groupe_330
    id_formation_groupe = individu(
        'groupe_specialites_formation', period.first_month)
    return id_formation_groupe == id_formation_sanitaire_social


def is_beneficiaire_rsa_eligible(individu, period, condition):
    rsa = individu.famille('rsa', period)
    return rsa > 0


def is_chomeur(individu: Entity, period: Period):
    return individu('activite', period.first_month) == TypesActivite.chomeur


def is_stagiaire(individu: Entity, period: Period):
    return individu('stagiaire', period.first_month)


def is_independant(individu: Entity, period: Period):
    template = individu(
        'activite', period.first_month) == TypesActivite.chomeur
    ret: np.ndarray = np.ones_like(template)
    return ret


def is_apprenti(individu: Entity, period: Period):
    return individu('apprenti', period.first_month)


def is_enseignement_superieur(individu: Entity, period: Period):
    return individu(
        'scolarite', period.first_month) == TypesScolarite.enseignement_superieur


def is_lyceen(individu: Entity, period: Period):
    template = individu(
        'activite', period.first_month) == TypesActivite.chomeur
    ret: np.ndarray = np.ones_like(template)
    ret[ret] = False
    return ret
    # return individu(
    #     'scolarite', period.first_month) == TypesScolarite.lyceen


condition_table = {
    "age": is_age_eligible,
    "departements": is_department_eligible,
    "regions": is_region_eligible,
    "regime_securite_sociale": is_regime_securite_sociale_eligible,
    "quotient_familial": is_quotient_familial_eligible,
    "formation_sanitaire_social": is_formation_sanitaire_social_eligible,
    "beneficiaire_rsa": is_beneficiaire_rsa_eligible,
}

profil_table = {
    "chomeur": is_chomeur,
    "stagiaire": is_stagiaire,
    "independant": is_independant,
    "apprenti": is_apprenti,
    "enseignement_superieur": is_enseignement_superieur,
    "lyceen": is_lyceen,
}

type_table = {
    'float': float,
    'bool': bool,
}

period_table = {
    'ponctuelle': ETERNITY,
    'mensuelle': MONTH,
    'annuelle': YEAR,
    'autre': ETERNITY,
}


def generate_variable(benefit: dict):

    class NewAidesJeunesBenefitVariable(Variable):
        value_type = float  # hardcoded
        entity = Individu
        definition_period = period_table[benefit['periodicite']]

        def formula(individu, period):

            value_type = type_table[benefit['type']]
            amount = benefit.get('montant')

            profils = benefit["profils"]
            profils_types_eligible = [profil["type"] for profil in profils]
            if len(profils_types_eligible) == 0:
                is_profile_eligible = True
            else:
                def eval_profil(profil):
                    predicate = profil_table[profil]
                    return predicate(individu, period)
                eligibilities = [eval_profil(profil)
                                 for profil in profils_types_eligible]
                is_profile_eligible = sum(eligibilities) >= 1

            conditions = benefit['conditions_generales']

            test_conditions = [(condition_table[condition['type']], condition)
                               for condition in conditions]

            eligibilities = [test[0](
                individu, period, test[1]) for test in test_conditions]

            total_eligibility = sum(eligibilities) == len(conditions)

            return amount * is_profile_eligible * total_eligibility if value_type == float else total_eligibility * is_profile_eligible * is_profile_eligible
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
