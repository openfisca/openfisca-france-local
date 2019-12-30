 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore
from numpy import logical_not as not_


class logement_social_pertinent(Variable):
    entity = Famille
    value_type = bool
    definition_period = MONTH
    label = "Critère de pertinence de l'éligibilité au logement social"

    def formula_2017(famille, period, parameters):
        logement = famille.demandeur.menage('statut_occupation_logement', period)

        return not_((logement == TypesStatutOccupationLogement.proprietaire)
          + (logement == TypesStatutOccupationLogement.primo_accedant))


class logement_social(Variable):
    entity = Famille
    value_type = bool
    definition_period = MONTH
    label = "Affiche le logement social dans le simulateur"

    def formula_2017(famille, period, parameters):
        eligible = famille('logement_social_eligible', period)
        pertinent = famille('logement_social_pertinent', period)

        return eligible * pertinent
