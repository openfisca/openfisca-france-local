 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class antony_noel_pour_tous(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Eligibilité de la famille au Noel pour Tous de la ville de Antony"

    def formula(famille, period, parameters):
        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)

        condition_ressources_remplies = famille('antony_eligibilite_ressources', period)

        age_demandeur = famille.demandeur('age', period)

        demandeur_moins_de_68_ans = age_demandeur < 68

        return residence_antony * condition_ressources_remplies * demandeur_moins_de_68_ans
