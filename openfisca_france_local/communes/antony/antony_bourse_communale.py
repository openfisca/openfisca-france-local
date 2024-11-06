 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Famille, MONTH, Variable
from openfisca_france.model.prestations.education import TypesScolarite


class antony_bourse_communale(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Éligibilité de la famille à la Bourse Communale de la ville de Antony"
    reference = "https://www.ville-antony.fr/bourses-communales#restaurationscolaire"

    def formula(famille, period, parameters):
        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)

        condition_ressources_remplies = famille('antony_eligibilite_ressources', period)

        scolarite = famille.members('scolarite', period)
        scolarise = ((scolarite == TypesScolarite.college) + (scolarite == TypesScolarite.lycee))

        au_moins_un_enfant_scolarise = famille.any(scolarise, role=Famille.ENFANT)

        return residence_antony * condition_ressources_remplies * au_moins_un_enfant_scolarise
