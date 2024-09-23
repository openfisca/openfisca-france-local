 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, FoyerFiscal, YEAR, MONTH


class loire_atlantique_quotient_familial(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR
    label = "Quotient familial pour le calcul des dispositifs du département de Loire-Atlantique"

    def formula(foyer_fiscal, period):
        return foyer_fiscal('rfr', period) / 12 / foyer_fiscal('nbptr', period)


class loire_atlantique_aide_mobilite_eligibilite_age(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité d'âge pour l'aide à la mobilité pour le permis AM du département de Loire-Atlantique"

    def formula(individu, period, parameters):
        params = parameters(period).departements.loire_atlantique.aide_mobilite

        individus_age = individu('age', period)

        age_maximum = params.age_maximal
        age_minimum = params.age_minimal
        return (individus_age >= age_minimum) * (individus_age < age_maximum)


class loire_atlantique_aide_mobilite_permis_am(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant pour l'aide à la mobilité du département de Loire-Atlantique pour le permis AM"
    reference = [
        "Règlement relatif à l’aide départementale à la mobilité",
        "https://www.loire-atlantique.fr/upload/docs/application/pdf/2024-04/reglement_aide_a_la_mobilite_2024.pdf"
        ]

    def formula(individu, period, parameters):
        params = parameters(period).departements.loire_atlantique.aide_mobilite

        eligibilite_residentielle = individu.menage('loire_atlantique_eligibilite_residence', period)
        eligibilite_age = individu('loire_atlantique_aide_mobilite_eligibilite_age', period)
        quotient_familial = individu.foyer_fiscal('loire_atlantique_quotient_familial', period.n_2)
        montant = params.montant_en_fonction_du_quotient_familial_permis_am.calc(quotient_familial)

        return montant * eligibilite_residentielle * eligibilite_age


class loire_atlantique_aide_mobilite_permis_b(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant pour l'aide à la mobilité du département de Loire-Atlantique pour le permis B"
    reference = [
        "Règlement relatif à l’aide départementale à la mobilité",
        "https://www.loire-atlantique.fr/upload/docs/application/pdf/2024-04/reglement_aide_a_la_mobilite_2024.pdf"
        ]

    def formula(individu, period, parameters):
        params = parameters(period).departements.loire_atlantique.aide_mobilite

        eligibilite_residentielle = individu.menage('loire_atlantique_eligibilite_residence', period)
        eligibilite_age = individu('loire_atlantique_aide_mobilite_eligibilite_age', period)
        quotient_familial = individu.foyer_fiscal('loire_atlantique_quotient_familial', period.n_2)
        montant = params.montant_en_fonction_du_quotient_familial_permis_b.calc(quotient_familial)

        return montant * eligibilite_residentielle * eligibilite_age
