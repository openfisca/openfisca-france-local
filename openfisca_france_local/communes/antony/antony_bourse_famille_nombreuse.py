 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Famille, MONTH, Variable


class antony_bourse_famille_nombreuse(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH
    label = "Éligibilité de la famille à la Bourse Famille Nombreuse de la ville de Antony"
    reference = "https://www.ville-antony.fr/bourses-communales#famillesnombreuses"

    def formula(famille, period, parameters):
        parameters = parameters(period).communes.antony.bourse_famille_nombreuse
        nb_enfants_minimum = parameters.nb_enfants_minimum
        age_maximum = parameters.age_maximum

        residence_antony = famille.demandeur.menage('antony_eligibilite_residence', period)

        nb_enfants = famille.nb_persons(role=Famille.ENFANT)
        condition_nb_enfants = nb_enfants >= nb_enfants_minimum

        age_i = famille.members('age', period)
        au_moins_un_enfant_moins_de_1_an = famille.any(age_i < age_maximum, role=Famille.ENFANT)

        return residence_antony * condition_nb_enfants * au_moins_un_enfant_moins_de_1_an
