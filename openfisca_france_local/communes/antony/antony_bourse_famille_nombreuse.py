 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class antony_bourse_famille_nombreuse(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Eligibilité de la famille a la Bourse Famille Nombreuse de la ville de Antony"

    def formula(famille, period, parameters):
        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)

        nb_enfants = famille.nb_persons(role=Famille.ENFANT)
        condition_nb_enfants = nb_enfants >= 3

        age_i = famille.members('age', period)
        au_moins_un_enfant_moins_de_1_an = famille.any(age_i < 1, role=Famille.ENFANT)

        return residence_antony * condition_nb_enfants * au_moins_un_enfant_moins_de_1_an
