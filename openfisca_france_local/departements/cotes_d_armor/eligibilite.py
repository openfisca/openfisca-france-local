 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith


class cotes_d_armor_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Éligibilité résidentielle d'un ménage aux dipositifs des Côtes d'Armor"

    def formula(menage, period):
        return startswith(menage('depcom', period), b'22')
