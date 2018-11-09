 # -*- coding: utf-8 -*-
from openfisca_france.model.base import *  # noqa analysis:ignore


class alfortville_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Éligibilité résidentielle d'un ménage aux dipositifs d'Alfortville"

    def formula(menage, period, parameters):
        return (menage('depcom', period) == '94002')
