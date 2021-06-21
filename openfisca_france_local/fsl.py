# -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH, TypesStatutOccupationLogement


class fsl_eligibilite(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Critère d'éligibilité à l'aide au maintien du FSL"

    def formula(menage, period):
        statut_occupation_logement = menage("statut_occupation_logement", period)
        return (statut_occupation_logement != TypesStatutOccupationLogement.loge_gratuitement) * (statut_occupation_logement != TypesStatutOccupationLogement.sans_domicile)
