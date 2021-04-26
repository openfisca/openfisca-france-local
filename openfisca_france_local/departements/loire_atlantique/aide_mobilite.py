 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, FoyerFiscal, YEAR, MONTH


class loire_atlantique_quotient_familial(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR
    label = "Quotient familial pour le calcul des dispositifs du département de Loire-Atlantique"

    def formula(foyer_fiscal, period):
        return foyer_fiscal('rfr', period) / 12 / foyer_fiscal('nbptr', period)


class loire_atlantique_aide_mobilite_eligibilite_financiere(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité financière pour l'aide à la mobilité du département de Loire-Atlantique"

    def formula(individu, period):
        return individu.foyer_fiscal('loire_atlantique_quotient_familial', period.n_2) <= 800


class loire_atlantique_aide_mobilite_eligibilite_age_permis_am(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'âge pour l'aide à la mobilité pour le permis AM du département de Loire-Atlantique"

    def formula(individu, period):
        age = individu('age', period)
        return (14 <= age) * (age <= 24)


class loire_atlantique_aide_mobilite_permis_am(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant pour l'aide à la mobilité du département de Loire-Atlantique pour le permis AM"
    reference = [
        "Règlement relatif à l’aide départementale à la mobilité",
        "https://www.loire-atlantique.fr/upload/docs/binary/octet-stream/2018-12/3-reglement_permis_2019_v24-08-2018.pdf"
        ]

    def formula(individu, period):
        eligibilite_financiere = individu('loire_atlantique_aide_mobilite_eligibilite_financiere', period)
        eligibilite_residentielle = individu.menage('loire_atlantique_eligibilite_residence', period)
        eligibilite_age = individu('loire_atlantique_aide_mobilite_eligibilite_age_permis_am', period)
        return 150 * eligibilite_residentielle * eligibilite_financiere * eligibilite_age


class loire_atlantique_aide_mobilite_eligibilite_age_permis_b(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'âge pour l'aide à la mobilité pour le permis B du département de Loire-Atlantique"

    def formula(individu, period):
        age = individu('age', period)
        return (17 <= age) * (age <= 24)


class loire_atlantique_aide_mobilite_permis_b(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant pour l'aide à la mobilité du département de Loire-Atlantique pour le permis B"
    reference = [
        "Règlement relatif à l’aide départementale à la mobilité",
        "https://www.loire-atlantique.fr/upload/docs/binary/octet-stream/2018-12/3-reglement_permis_2019_v24-08-2018.pdf"
        ]

    def formula(individu, period):
        eligibilite_financiere = individu('loire_atlantique_aide_mobilite_eligibilite_financiere', period)
        eligibilite_residentielle = individu.menage('loire_atlantique_eligibilite_residence', period)
        eligibilite_age = individu('loire_atlantique_aide_mobilite_eligibilite_age_permis_b', period)
        return 750 * eligibilite_residentielle * eligibilite_financiere * eligibilite_age
