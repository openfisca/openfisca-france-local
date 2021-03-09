 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, FoyerFiscal, YEAR, MONTH


class loire_atlantique_quotient_familial(Variable):
    value_type = float
    entity = FoyerFiscal
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        return foyer_fiscal('rfr', period) / 12 / foyer_fiscal('nbptr', period)


class loire_atlantique_aide_mobilite_eligibilite_financiere(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        return individu.foyer_fiscal('loire_atlantique_quotient_familial', period.n_2) <= 800


class loire_atlantique_aide_mobilite_eligibilite_age_permis_am(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        age = individu('age', period)
        return (14 <= age) * (age <= 24)


class loire_atlantique_aide_mobilite_permis_am(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant pour l'aide à la mobilité du département de Loire Atlantique pour le permis AM"

    def formula(individu, period):
        fin = individu('loire_atlantique_aide_mobilite_eligibilite_financiere', period)
        resid = individu.menage('loire_atlantique_eligibilite_residence', period)
        age = individu('loire_atlantique_aide_mobilite_eligibilite_age_permis_am', period)
        return 150 * resid * fin * age


class loire_atlantique_aide_mobilite_eligibilite_age_permis_b(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        age = individu('age', period)
        return (17 <= age) * (age <= 24)


class loire_atlantique_aide_mobilite_permis_b(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Montant pour l'aide à la mobilité du département de Loire Atlantique pour le permis B"

    def formula(individu, period):
        fin = individu('loire_atlantique_aide_mobilite_eligibilite_financiere', period)
        resid = individu.menage('loire_atlantique_eligibilite_residence', period)
        age = individu('loire_atlantique_aide_mobilite_eligibilite_age_permis_b', period)
        return 750 * resid * fin * age
