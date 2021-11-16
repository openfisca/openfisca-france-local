 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class antony_bourse_conservatoire(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Eligibilité de la famille a la Bourse du Conservatoire de la ville de Antony"

    def formula(famille, period, parameters):
        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)

        condition_ressources_remplies = famille('antony_eligibilite_ressources', period)

        age_i = famille.members('age', period)
        au_moins_un_enfant_moins_de_18_ans = famille.any(age_i < 18, role=Famille.ENFANT)

        return residence_antony * condition_ressources_remplies * au_moins_un_enfant_moins_de_18_ans
