 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith


class loire_atlantique_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de Loire-Atlantique"

    def formula(menage, period):
        return startswith(menage('depcom', period), b'44')
