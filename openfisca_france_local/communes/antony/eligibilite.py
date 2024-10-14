 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Menage, MONTH, Variable

class antony_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs d'Antony"

    def formula(menage, period, parameters):
        return (menage('depcom', period) == b'92002')
