 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class alfortville_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Éligibilité résidentielle d'un ménage aux dipositifs d'Alfortville"

    def formula(menage, period, parameters):
        statut_occupation = menage('statut_occupation_logement', period)
        eligibilite_occupation = (
            + (statut_occupation == TypesStatutOccupationLogement.primo_accedant)
            + (statut_occupation == TypesStatutOccupationLogement.proprietaire)
            + (statut_occupation == TypesStatutOccupationLogement.locataire_hlm)
            + (statut_occupation == TypesStatutOccupationLogement.locataire_vide)
            + (statut_occupation == TypesStatutOccupationLogement.sans_domicile)
        )
        return eligibilite_occupation * (menage('depcom', period) == '55039')
