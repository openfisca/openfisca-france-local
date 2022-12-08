# -*- coding: utf-8 -*-

import yaml

from pathlib import Path
from numpy.core.defchararray import startswith
import numpy as np

from openfisca_france.model.base import *
from openfisca_core import reforms
from openfisca_core.periods import Period


from openfisca_france.model.caracteristiques_socio_demographiques.demographie import RegimeSecuriteSociale
from openfisca_france.model.caracteristiques_socio_demographiques.demographie import GroupeSpecialitesFormation
from openfisca_france.model.prestations.education import TypesScolarite, TypesClasse
from openfisca_core.populations.population import Population


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


def is_department_eligible(individu: Population, period: Period, condition):
    depcom = individu.menage('depcom', period.first_month)
    return sum([startswith(depcom, code.encode('UTF-8'))for code in condition['values']])


def is_region_eligible(individu: Population, period: Period, condition):
    eligibilite_region_table: dict = {
        '01': 'guadeloupe_eligibilite_residence',
        '02': 'martinique_eligibilite_residence',
        '03': 'guyane_eligibilite_residence',
        '24': 'centre_val_de_loire_eligibilite_residence',
        '27': 'bourgogne_franche_comte_eligibilite_residence',
        '32': 'hauts_de_france_eligibilite_residence',
        '44': 'grand_est_eligibilite_residence',
        '53': 'bretagne_eligibilite_residence',
        '75': 'nouvelle_aquitaine_eligibilite_residence',
        '76': 'occitanie_eligibilite_residence',
        '84': 'auvergne_rhone_alpes_eligibilite_residence',
    }
    return sum([individu.menage(eligibilite_region_table[code_region], period.first_month) for code_region in condition['values']])


def is_regime_securite_sociale_eligible(individu: Population, period: Period, condition):
    regime_securite_sociale = individu('regime_securite_sociale', period)
    return sum([regime_securite_sociale == RegimeSecuriteSociale[regime] for regime in condition['includes']])


def is_quotient_familial_eligible(individu: Population, period: Period, condition) -> np.array:
    rfr = individu.foyer_fiscal('rfr', period.this_year)
    nbptr = individu.foyer_fiscal('nbptr', period.this_year)
    quotient_familial = rfr / nbptr
    return quotient_familial <= condition["ceiling"]


def is_formation_sanitaire_social_eligible(individu: Population, period: Period, condition) -> np.array:
    id_formation_sanitaire_social = GroupeSpecialitesFormation.groupe_330
    id_formation_groupe = individu(
        'groupe_specialites_formation', period.first_month)
    return id_formation_groupe == id_formation_sanitaire_social


def is_beneficiaire_rsa_eligible(individu: Population, period: Period, condition) -> np.array:
    rsa = individu.famille('rsa', period)
    return rsa > 0


def is_annee_etude_eligible(individu: Population, period: Period, condition) -> np.array:
    current_year = individu(
        'annee_etude', period.first_month)
    return sum([current_year == TypesClasse[value] for value in condition['values']])


def has_mention_baccalaureat(individu: Population, period: Period, condition) -> np.array:
    has_mention = individu(
        'mention_baccalaureat', period)
    return sum([has_mention == TypesMention[value] for value in condition['values']])


def is_boursier(individu: Population, period: Period, condition: dict) -> np.array:
    return individu('boursier', period.first_month)


def is_chomeur(individu: Population, period: Period) -> np.array:
    return individu('activite', period.first_month) == TypesActivite.chomeur


def is_stagiaire(individu: Population, period: Period) -> np.array:
    return individu('stagiaire', period.first_month)


def is_apprenti(individu: Population, period: Period) -> np.array:
    return individu('apprenti', period.first_month)


def is_enseignement_superieur(individu: Population, period: Period) -> np.array:
    return individu(
        'scolarite', period.first_month) == TypesScolarite.enseignement_superieur


def is_lyceen(individu: Population, period: Period) -> np.array:
    return individu(
        'scolarite', period.first_month) == TypesScolarite.lycee


def is_etudiant(individu: Population, period: Period) -> np.array:
    return individu(
        'etudiant', period.first_month)


def is_professionnalisation(individu: Population, period: Period) -> np.array:
    return individu('professionnalisation', period.first_month)


def is_actif(individu: Population, period: Period) -> np.array:
    return individu('activite', period.first_month) == TypesActivite.actif


def is_inactif(individu: Population, period: Period) -> np.array:
    return individu('activite', period.first_month) == TypesActivite.inactif


def is_to_implement(individu: Population, period: Period) -> np.array:
    template = individu(
        'activite', period.first_month) == TypesActivite.chomeur
    ret: np.ndarray = np.ones_like(template)
    ret[ret] = False
    return ret


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

        def formula(individu: Population, period: Period):

            def eval_conditions(conditions: dict):
                test_conditions = [(condition_table[condition['type']], condition)
                                   for condition in conditions]

                conditions_results = [
                    test[0](individu, period, test[1]) for test in test_conditions]
                return sum(conditions_results) == len(conditions)

            value_type = type_table[benefit['type']]
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
                is_profile_eligible = sum(eligibilities) >= 1

            conditions_generales = benefit['conditions_generales']
            general_eligibilities = eval_conditions(conditions_generales)
            return amount * is_profile_eligible * general_eligibilities if value_type == float else general_eligibilities * is_profile_eligible
        # Ce return fonctionnera car nos aides n'ont que deux types : bool et float
        # mais ce n'est pas élégant. (surtout qu'il faut créer une deuxième variable value_type)

    NewAidesJeunesBenefitVariable.__name__ = benefit['slug']
    return NewAidesJeunesBenefitVariable


class aides_jeunes_reform_dynamic(reforms.Reform):
    root = '.'
    path = '../git_aides-jeunes/data/benefits/javascript/'
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
            str(benefit) for benefit in Path(benefits_folder).iterdir() if isYAMLfile(benefit)]
        return liste_fichiers

    def apply(self):
        try:
            benefit_files_paths = self.extract_benefits_paths(
                self.current_path)
            for path in benefit_files_paths:
                self.add_variable(generate_variable(
                    self.extract_benefit_file_content(path)))
        except KeyError as e:
            raise KeyError(f"field {e} missing in file: {path}")
