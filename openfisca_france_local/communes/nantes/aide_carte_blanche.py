 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, MONTH, Individu

class aide_carte_blanche(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité à l'obtention d'une carte blanche donnant accès à de nombreuses offres de loisirs culturelles et sportives à tarif réduit."
    reference = "https://metropole.nantes.fr/carte-blanche"

    def formula(individu, period, parameters):
        eligibilite_commune = individu.menage('depcom', period) == b"44109"

        quotient_familial = individu.foyer_fiscal('rfr', period.n_2) / 12 / individu.foyer_fiscal('nbptr', period.n_2)
        eligibilite_quotient_familial = quotient_familial <= parameters(period).communes.nantes.aide_carte_blanche.plafond_quotient_familial

        return eligibilite_commune * eligibilite_quotient_familial
