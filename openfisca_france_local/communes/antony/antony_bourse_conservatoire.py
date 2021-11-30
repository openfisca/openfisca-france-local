 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.education import TypesScolarite


class antony_bourse_conservatoire(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Eligibilité de la famille a la Bourse du Conservatoire de la ville de Antony"

    def formula(famille, period, parameters):
        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)

        condition_ressources_remplies = famille('antony_eligibilite_ressources', period)

        scolarite = famille.members('scolarite', period)
        scolarise_i = ((scolarite == TypesScolarite.college) + (scolarite == TypesScolarite.lycee))

        age_i = famille.members('age', period)
        moins_de_18_ans_scolarise = scolarise_i * (age_i < 18)

        au_moins_un_scolarise_18_ans = famille.any(moins_de_18_ans_scolarise, role=Famille.ENFANT)

        return residence_antony * condition_ressources_remplies * au_moins_un_scolarise_18_ans
