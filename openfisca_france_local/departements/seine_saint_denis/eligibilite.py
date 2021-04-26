 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith


class seine_saint_denis_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la Seine-Saint-Denis"

    def formula(menage, period):
        return startswith(menage('depcom', period), b'93')
