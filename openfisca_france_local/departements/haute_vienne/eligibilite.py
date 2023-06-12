from openfisca_france.model.base import Variable, Menage, MONTH

from numpy.core.defchararray import startswith


class haute_vienne_eligibilite_residence(Variable):
    value_type = bool
    entity = Menage
    definition_period = MONTH
    label = "Éligibilité résidentielle d'un ménage aux dipositifs de la Haute-Vienne"

    def formula(menage, period):
        return startswith(menage('depcom', period), str.encode('87'))
