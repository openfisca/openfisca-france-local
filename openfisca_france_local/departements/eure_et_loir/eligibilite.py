 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith


class eure_et_loir_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = u"Éligibilité résidentielle d'un ménage aux dipositifs de L'Eure-et-Loir"

    def formula(menage, period):
        return startswith(menage('depcom', period), b'28')
