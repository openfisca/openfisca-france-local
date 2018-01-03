 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore

from openfisca_brestmetropole.communes import communes


class residence_brest_metropole(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = u"Le lieu de résidence se situe dans une commune faisant partie de Brest métropole"

    def formula(individu, period):
        code_insee_commune = individu.menage('depcom', period)
        return sum([code_insee_commune == code_insee for code_insee in communes])


class brest_metropole_transport(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = u"Calcul de la tarification solidaire de Brest métropole"

    def formula(individu, period, parameters):

        return individu('residence_brest_metropole', period) * 1
