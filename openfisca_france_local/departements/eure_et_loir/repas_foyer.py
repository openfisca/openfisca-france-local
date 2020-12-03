 # -*- coding: utf-8 -*-
from openfisca_france.model.base import Variable, Individu, Menage, MONTH

from numpy.core.defchararray import startswith


class eure_et_loir_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de L'Eure-et-Loir"

    def formula(menage, period):
        return startswith(menage('depcom', period), b'28')


class eure_et_loir_eligibilite_repas_foyer(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité à l'aide Rapas Foyer de l'Eure-et-Loir"
    documentation = '''
    TODO ajouter le descriptif à destination du simulateur
    '''

    def formula(individu, period):
        return False
