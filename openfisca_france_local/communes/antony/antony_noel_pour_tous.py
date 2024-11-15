 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Famille, MONTH, Variable


class antony_noel_pour_tous(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Éligibilité de la famille au Noël pour Tous de la ville de Antony"
    reference = "https://www.ville-antony.fr/actualites/noel-ccas-2024"

    def formula(famille, period, parameters):
        age_maximum = parameters(period).communes.antony.noel_pour_tous.age_maximum

        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)
        condition_ressources_remplies = famille('antony_eligibilite_ressources', period)
        age_demandeur = famille.demandeur('age', period)

        demandeur_moins_de_68_ans = age_demandeur < age_maximum

        return residence_antony * condition_ressources_remplies * demandeur_moins_de_68_ans
