 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Famille, MONTH, Variable


class antony_bourse_conservatoire(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Éligibilité de la famille à la Bourse du Conservatoire de la ville de Antony"
    reference = "https://www.ville-antony.fr/bourses-communales#conservatoire"

    def formula(famille, period, parameters):
        age_maximum = parameters(period).communes.antony.bourse_conservatoire.age_maximum

        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)
        condition_ressources_remplies = famille('antony_eligibilite_ressources', period)
        age_i = famille.members('age', period)

        au_moins_un_enfant_moins_de_18_ans = famille.any(age_i < age_maximum, role=Famille.ENFANT)

        return residence_antony * condition_ressources_remplies * au_moins_un_enfant_moins_de_18_ans
